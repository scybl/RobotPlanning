#!/usr/bin/env python3
import time
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from ament_index_python.packages import get_package_share_directory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from visualization_msgs.msg import Marker
from builtin_interfaces.msg import Duration

# --- ROS 2 Bag Reader Import ---
import sqlite3
import glob
from rclpy.serialization import deserialize_message
# -------------------------------

from youbot_kdl_utils import YoubotKinematicKDL
import itertools

class YoubotTrajectoryPlanning(Node):
    def __init__(self):
        super().__init__('youbot_motion_planner')
        self.kdl_youbot = YoubotKinematicKDL(self)

        # 1. Trajectory Publisher
        self.traj_pub = self.create_publisher(
            JointTrajectory,
            '/EffortJointInterface_trajectory_controller/command',
            5
        )

        # 2. Marker Publisher 
        # Topic: visualization_marker (Matches default RViz config you provided)
        marker_qos = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL, 
            history=QoSHistoryPolicy.KEEP_LAST
        )
        self.checkpoint_pub = self.create_publisher(Marker, 'visualization_marker', marker_qos)
        
        # 3. Joint State Publisher
        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 10)

        self._q_path = None
        self._path_index = 0
        self._publish_timer = None
        
        # Cache for markers
        self._checkpoint_markers = [] 
        self._checkpoint_positions = []
        self._checkpoint_reached = []
        self._marker_timer = None

    def run(self):
        """Run checkpoint ordering, interpolation, and inverse kinematics."""
        self.get_logger().info('Waiting 2 seconds for everything to load up.')
        time.sleep(2.0)
        traj, q_path = self.build_checkpoint_trajectory()
        self._q_path = q_path
        self._path_index = 0
        self.get_logger().info('Markers published. Starting movement in 1 second...')
        time.sleep(1.0)
        traj.header.stamp = self.get_clock().now().to_msg()
        traj.joint_names = ["arm_joint_1", "arm_joint_2", "arm_joint_3", "arm_joint_4", "arm_joint_5"]
        self.traj_pub.publish(traj)
        self._publish_timer = self.create_timer(0.05, self._publish_next_state)
        self._marker_timer = self.create_timer(1.0, self._republish_markers)

    def build_checkpoint_trajectory(self):
        # Load targets.
        target_checkpoint_tfs = self.load_targets()   # (4,4,N)
        num_checkpoints = target_checkpoint_tfs.shape[2]
        if num_checkpoints < 2:
            raise RuntimeError("Not enough checkpoints loaded from bag file.")

        # Shortest path through the checkpoint set.
        sorted_idx = self.get_shortest_path(target_checkpoint_tfs)


        # Interpolate transforms along the ordered checkpoint path.
        num_points_per_segment = 50
        full_checkpoint_tfs = self.intermediate_tfs(
            sorted_idx,
            target_checkpoint_tfs,
            num_points_per_segment
        )   # (4,4,M)


        # Position-only inverse kinematics.
        q0 = self.target_joint_positions[:, int(sorted_idx[0])]
        q_path = self.full_checkpoints_to_joints(full_checkpoint_tfs, q0)  # (5,M)


        # Trajectory message.
        traj = JointTrajectory()
        traj.header.frame_id = "base_link"
        traj.joint_names = [
            "arm_joint_1",
            "arm_joint_2",
            "arm_joint_3",
            "arm_joint_4",
            "arm_joint_5"
        ]

        dt = 0.05 # fixed time step

        for i in range(q_path.shape[1]):
            pt = JointTrajectoryPoint()
            pt.positions = q_path[:, i].tolist()
            pt.time_from_start = Duration(
                sec=int(dt * i),
                nanosec=int((dt * i) % 1.0 * 1e9)
            )
            traj.points.append(pt)

        targets = (traj, q_path)

        # some patch
        if not hasattr(self, "_gripper_tf_fix_enabled"):
            self._gripper_tf_fix_enabled = True

            finger_names = ["gripper_finger_joint_l", "gripper_finger_joint_r"]
            finger_pos = [0.006, 0.006]

            def _jointstate_fix_cb(msg: JointState):

                # already contains finger joints → ignore
                if ("gripper_finger_joint_l" in msg.name) or \
                ("gripper_finger_joint_r" in msg.name):
                    return

                # only process arm-only messages
                if len(msg.name) < 5:
                    return
                if not all(n.startswith("arm_joint_") for n in msg.name[:5]):
                    return

                fixed = JointState()
                fixed.header.stamp = msg.header.stamp
                fixed.name = list(msg.name) + finger_names
                fixed.position = list(msg.position) + finger_pos

                self.joint_state_pub.publish(fixed)

            self._gripper_tf_fix_sub = self.create_subscription(
                JointState,
                "/joint_states",
                _jointstate_fix_cb,
                10
            )
        return targets
        ############################################################################
        ############################################################################

    def load_targets(self):
        """
        Loads the target joint positions from the bagfile
        and computes corresponding end-effector positions.
        """
        ############################################################################
        ############################################################################

        # path
        bag_path = get_package_share_directory('youbot_motion_planning') + '/bags/data_ros2/data_ros2.db3'

        # open the dataset
        db = sqlite3.connect(bag_path)
        cursor = db.cursor()

        # topic id
        cursor.execute("SELECT id FROM topics WHERE name LIKE '%joint%'")
        joint_topic_id = cursor.fetchone()[0]

        # topic data
        cursor.execute("SELECT data FROM messages WHERE topic_id = ?",(joint_topic_id,))
        rows = cursor.fetchall()

        # init save data
        target_joint_positions = []
        for row in rows:
            msg = deserialize_message(row[0], JointState)
            target_joint_positions.append(list(msg.position[:5]))

        db.close()

        # N×5 -> 5×N
        q_arr = np.array(target_joint_positions).T
        self.target_joint_positions = q_arr       # shape = (5,N)

        # get FK
        N = self.target_joint_positions.shape[1]
        target_tfs = np.zeros((4,4,N))

        for i in range(N):
            q = self.target_joint_positions[:, i]
            target_tfs[:,:,i] = self.kdl_youbot.forward_kinematics(q)

        print("Loaded", N, "target checkpoints")

        return target_tfs

        ############################################################################
        ############################################################################

    def get_shortest_path(self, checkpoints_tf):
        """
        Computes the order of checkpoints that minimises the total Euclidean path
        length in Cartesian space.
        """
        ############################################################################
        ############################################################################
        # get checkpoint position (x,y,z)
        num_cp = checkpoints_tf.shape[2]
        positions = np.zeros((num_cp, 3))
        for i in range(num_cp):
            positions[i, :] = checkpoints_tf[:3, 3, i]

        indices = list(range(num_cp))

        # final position
        start_pos = np.array(self.kdl_youbot.forward_kinematics([0.0]*5))[:3, 3]

        best_order = None
        best_length = np.inf

        # TSP
        for perm in itertools.permutations(indices):

            length = 0.0

            first_pos = positions[perm[0]]
            length += np.linalg.norm(first_pos - start_pos)

            for a, b in zip(perm[:-1], perm[1:]):
                da = positions[a]
                db = positions[b]
                length += np.linalg.norm(db - da)

            # update
            if length < best_length:
                best_length = length
                best_order = perm

        return list(best_order)
        ############################################################################
        ############################################################################

    def intermediate_tfs(self, sorted_checkpoint_idx, target_checkpoint_tfs, num_points):
        """
        Create intermediate transformations along the path defined by sorted_checkpoint_idx.
        For each consecutive pair of checkpoints, interpolate num_points transforms using
        decoupled_rot_and_trans, and concatenate them into one full list.
        """
        ############################################################################
        ############################################################################
        full_tfs_list = []

        for seg_i in range(len(sorted_checkpoint_idx) - 1):
            a_idx = int(sorted_checkpoint_idx[seg_i])
            b_idx = int(sorted_checkpoint_idx[seg_i + 1])

            T_a = target_checkpoint_tfs[:, :, a_idx]
            T_b = target_checkpoint_tfs[:, :, b_idx]

            seg_tfs = self.decoupled_rot_and_trans(T_a, T_b, num_points)  # (4,4,num_points)

            if seg_i == 0:
                # append all point
                for k in range(seg_tfs.shape[2]):
                    full_tfs_list.append(seg_tfs[:, :, k])
            else:
                for k in range(1, seg_tfs.shape[2]):
                    full_tfs_list.append(seg_tfs[:, :, k])

        M = len(full_tfs_list)
        full_tfs = np.zeros((4, 4, M))
        for i, T in enumerate(full_tfs_list):
            full_tfs[:, :, i] = T

        return full_tfs
        ############################################################################
        ############################################################################

    def decoupled_rot_and_trans(self, checkpoint_a_tf, checkpoint_b_tf, num_points):
        """
        Interpolate between two transforms by decoupling translation and rotation.
        - Translation: linear interpolation
        - Rotation: quaternion SLERP
        Returns: tfs of shape (4,4,num_points)
        """
        ############################################################################
        ############################################################################
        def rot_to_quat(R):
            """Rotation matrix -> quaternion [x, y, z, w]"""
            m00, m01, m02 = R[0, 0], R[0, 1], R[0, 2]
            m10, m11, m12 = R[1, 0], R[1, 1], R[1, 2]
            m20, m21, m22 = R[2, 0], R[2, 1], R[2, 2]

            tr = m00 + m11 + m22
            if tr > 0.0:
                S = np.sqrt(tr + 1.0) * 2.0
                qw = 0.25 * S
                qx = (m21 - m12) / S
                qy = (m02 - m20) / S
                qz = (m10 - m01) / S
            elif (m00 > m11) and (m00 > m22):
                S = np.sqrt(1.0 + m00 - m11 - m22) * 2.0
                qw = (m21 - m12) / S
                qx = 0.25 * S
                qy = (m01 + m10) / S
                qz = (m02 + m20) / S
            elif m11 > m22:
                S = np.sqrt(1.0 + m11 - m00 - m22) * 2.0
                qw = (m02 - m20) / S
                qx = (m01 + m10) / S
                qy = 0.25 * S
                qz = (m12 + m21) / S
            else:
                S = np.sqrt(1.0 + m22 - m00 - m11) * 2.0
                qw = (m10 - m01) / S
                qx = (m02 + m20) / S
                qy = (m12 + m21) / S
                qz = 0.25 * S
            return np.array([qx, qy, qz, qw])

        def quat_to_rot(q):
            """Quaternion [x, y, z, w] -> rotation matrix"""
            qx, qy, qz, qw = q
            n = np.linalg.norm(q)
            if n == 0.0:
                return np.eye(3)
            qx, qy, qz, qw = q / n

            xx = qx * qx
            yy = qy * qy
            zz = qz * qz
            xy = qx * qy
            xz = qx * qz
            yz = qy * qz
            wx = qw * qx
            wy = qw * qy
            wz = qw * qz

            R = np.array([
                [1.0 - 2.0 * (yy + zz),     2.0 * (xy - wz),         2.0 * (xz + wy)],
                [    2.0 * (xy + wz),   1.0 - 2.0 * (xx + zz),       2.0 * (yz - wx)],
                [    2.0 * (xz - wy),       2.0 * (yz + wx),     1.0 - 2.0 * (xx + yy)]
            ])
            return R

        def slerp(q0, q1, t):
            """Quaternion slerp."""
            q0 = q0 / np.linalg.norm(q0)
            q1 = q1 / np.linalg.norm(q1)

            dot = np.dot(q0, q1)
            if dot < 0.0:
                q1 = -q1
                dot = -dot

            if dot > 0.9995:
                q = q0 + t * (q1 - q0)
                return q / np.linalg.norm(q)

            theta_0 = np.arccos(dot)
            sin_theta_0 = np.sin(theta_0)
            theta = theta_0 * t
            sin_theta = np.sin(theta)

            s0 = np.sin(theta_0 - theta) / sin_theta_0
            s1 = sin_theta / sin_theta_0
            return (s0 * q0) + (s1 * q1)

        # start point and end one
        R_a = checkpoint_a_tf[:3, :3]
        t_a = checkpoint_a_tf[:3, 3]
        R_b = checkpoint_b_tf[:3, :3]
        t_b = checkpoint_b_tf[:3, 3]

        q_a = rot_to_quat(R_a)
        q_b = rot_to_quat(R_b)

        tfs = np.zeros((4, 4, num_points))
        for i in range(num_points):
            if num_points == 1:
                s = 1.0
            else:
                s = i / (num_points - 1)

            t = (1.0 - s) * t_a + s * t_b
            q = slerp(q_a, q_b, s)
            R = quat_to_rot(q)

            T = np.eye(4)
            T[:3, :3] = R
            T[:3, 3] = t
            tfs[:, :, i] = T

        return tfs
        ############################################################################
        ############################################################################

    def full_checkpoints_to_joints(self, full_checkpoint_tfs, init_joint_position):
        """
        Compute associated joint positions for each checkpoint (including intermediate
        ones) using position-only IK. Uses the previous solution as the initial guess
        for the next point to keep motion smooth.
        """
        ############################################################################
        ############################################################################
        num_points = full_checkpoint_tfs.shape[2]
        num_joints = init_joint_position.shape[0]

        q_path = np.zeros((num_joints, num_points))
        q_prev = init_joint_position.astype(float).copy()

        def unwrap(q_new, q_old):
            q = q_new.copy()
            for j in range(len(q)):
                while q[j] - q_old[j] > np.pi:
                    q[j] -= 2*np.pi
                while q[j] - q_old[j] < -np.pi:
                    q[j] += 2*np.pi
            return q

        for i in range(num_points):
            pose = full_checkpoint_tfs[:, :, i]

            q_try = self.ik_position_only(pose, q_prev)
            q_try = unwrap(q_try, q_prev)

            q_sol = q_try

            q_path[:, i] = q_sol
            q_prev = q_sol

        return q_path

        ############################################################################
        ############################################################################

    def ik_position_only(self, pose, q0):
        """
        Iterative Inverse Kinematics.
        Position-only IK:
        - Only enforces end-effector position (x,y,z), ignores orientation.
        - Uses Jacobian pseudo-inverse from YoubotKinematicKDL.get_jacobian().
        """
        ############################################################################
        ############################################################################
        max_iters = 200
        tol = 1e-3
        alpha = 0.3
        max_step = 0.05 

        target_pos = pose[:3, 3].copy()
        q = q0.astype(float).copy()

        for _ in range(max_iters):
            # end point pos
            T_cur = self.kdl_youbot.forward_kinematics(q)
            cur_pos = T_cur[:3, 3]

            err = target_pos - cur_pos  # (3,)
            if np.linalg.norm(err) < tol:
                break

            # Jacobian (6x5) -> get the position (3x5)
            J = self.kdl_youbot.get_jacobian(q)
            J_pos = J[0:3, :]

            J_pinv = np.linalg.pinv(J_pos)
            dq = alpha * J_pinv.dot(err)

            step_norm = np.linalg.norm(dq)
            if step_norm > max_step:
                dq *= max_step / (step_norm + 1e-8)

            q = q + dq

        return q
        ############################################################################
        ############################################################################

    def init_markers(self, tfs):
        """
        Creates markers ONLY for the 5 checkpoints.
        """
        self._checkpoint_markers = []
        marker_id = 0
        
        for i in range(0, tfs.shape[2]):
            marker = Marker()
            marker.id = marker_id
            marker_id += 1
            marker.header.frame_id = 'base_link' 
            marker.ns = "points_and_lines" 
            marker.type = Marker.CUBE
            marker.action = Marker.ADD
            
            marker.scale.x = 0.04 
            marker.scale.y = 0.04
            marker.scale.z = 0.04
            
            marker.color.a = 1.0
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            
            marker.lifetime = Duration(sec=0, nanosec=0)
            marker.frame_locked = True
            
            marker.pose.orientation.w = 1.0
            marker.pose.position.x = float(tfs[0, -1, i])
            marker.pose.position.y = float(tfs[1, -1, i])
            marker.pose.position.z = float(tfs[2, -1, i])
            
            self._checkpoint_markers.append(marker)
        
        self._republish_markers()

    def _republish_markers(self):
        """Timer callback to keep markers visible and update colors."""
        if not self._checkpoint_markers:
            return
        stamp_zero = rclpy.time.Time(seconds=0).to_msg()
            
        for i, marker in enumerate(self._checkpoint_markers):
            marker.header.stamp = stamp_zero
            reached = self._checkpoint_reached[i] if i < len(self._checkpoint_reached) else False
            
            if reached:
                marker.color.r = 0.0
                marker.color.g = 1.0
            else:
                marker.color.r = 1.0
                marker.color.g = 0.0
            marker.color.b = 0.0
            
            self.checkpoint_pub.publish(marker)

    def _publish_next_state(self):
        """Timer callback to visualize the robot moving."""
        if self._q_path is None:
            return
        if self._path_index >= self._q_path.shape[1]:
            self.destroy_timer(self._publish_timer)
            return
            
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ["arm_joint_1", "arm_joint_2", "arm_joint_3", "arm_joint_4", "arm_joint_5"]
        msg.position = self._q_path[:, self._path_index].tolist()
        self.joint_state_pub.publish(msg)
        
        ee_pose = self.kdl_youbot.forward_kinematics(self._q_path[:, self._path_index])
        ee_pos = ee_pose[:3, 3]
        
        for idx, cp in enumerate(self._checkpoint_positions):
            if cp is None or len(cp) == 0: continue
            if np.linalg.norm(ee_pos - cp) < 0.03: 
                self._checkpoint_reached[idx] = True
                
        self._path_index += 1

def main(args=None):
    rclpy.init(args=args)
    node = YoubotTrajectoryPlanning()
    print("")
    node.run()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
