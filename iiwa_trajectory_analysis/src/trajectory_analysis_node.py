#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import numpy as np
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import os

import matplotlib.pyplot as plt

import sqlite3
import glob
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
from ament_index_python.packages import get_package_share_directory

from sensor_msgs.msg import JointState

from iiwa_dynamics.iiwa14_dynamic_model import Iiwa14DynamicModel

def load_ros2_bag(db3_path):

    conn = sqlite3.connect(db3_path)
    cursor = conn.cursor()

    # read topic 
    cursor.execute("SELECT id, name, type FROM topics")
    topic_id, topic_name, msg_type_name = cursor.fetchall()[0]

    MsgClass = get_message(msg_type_name)

    # read information
    cursor.execute(
        "SELECT timestamp, data FROM messages WHERE topic_id=?",
        (topic_id,)
    )
    rows = cursor.fetchall()

    messages = []
    for ts, raw in rows:
        msg = deserialize_message(raw, MsgClass)
        messages.append((ts, msg))

    conn.close()

    return topic_name, msg_type_name, messages


class TrajPublisher(Node):

    def __init__(self):
        super().__init__('traj_pub')

        # create publisher
        self.pub = self.create_publisher(
            JointTrajectory,
            "/iiwa_controller/joint_trajectory",
            10
        )

        # joint
        self.joint_names = [
            'joint_1',
            'joint_2',
            'joint_3',
            'joint_4',
            'joint_5',
            'joint_6',
            'joint_7'
        ]
        # plt init and time recording
        self.start_time = self.get_clock().now().nanoseconds * 1e-9
        self.time_log = []
        self.qdd_log = []
        self.max_duration = 40.0   # sec

        self.create_timer(1.0, self.timer_cb)
        self.t = 0.0
        self.get_logger().info("tracking publisher has been created")
        bag_path = os.path.join(
            get_package_share_directory("iiwa_trajectory_analysis"),
            "bag",
            "data_ros2",
            "data_ros2.db3",
        )

        topic, msg_type, messages = load_ros2_bag(bag_path)

        self.bag_positions = []

        for _, msg in messages:
            for pt in msg.points:
                self.bag_positions.append(list(pt.positions))

        self.idx = 0
        self.sub = self.create_subscription(
            JointState,
            "/joint_states",
            self.joint_state_cb,
            10
        )
        self.dyn = Iiwa14DynamicModel()


        self.prev_time = None
        self.prev_qd = None


    def timer_cb(self):

        if hasattr(self, "_traj_sent") and self._traj_sent:
            return

        traj = JointTrajectory()
        traj.joint_names = self.joint_names

        # three point
        target_positions = self.bag_positions[:3]
        target_times = [10.0, 20.0, 30.0]

        for i, (q, t) in enumerate(zip(target_positions, target_times)):
            pt = JointTrajectoryPoint()
            pt.positions = q

            pt.time_from_start.sec = int(t)
            pt.time_from_start.nanosec = int((t - int(t)) * 1e9)

            traj.points.append(pt)

            self.get_logger().info(
                f"[Target #{i}] reach at t={t:.1f}s, q = "
                + ", ".join([f"{v:+.3f}" for v in q])
            )

        self.pub.publish(traj)
        self.get_logger().info("JointTrajectory has been published")

        self._traj_sent = True


    def joint_state_cb(self, msg):
        # current time
        now = self.get_clock().now().nanoseconds * 1e-9
        t = now - self.start_time

        q = list(msg.position)
        qd = list(msg.velocity)

        B = self.dyn.get_B(q)
        Cq = self.dyn.get_C_times_qdot(q, qd)
        G = self.dyn.get_G(q)

        tau = np.zeros(7)
        qdd = np.linalg.solve(B, tau - Cq - G)

        # recording all the return data
        self.time_log.append(t)
        self.qdd_log.append(qdd)
        
        # max = 35 sec
        if t >= self.max_duration:
            self.get_logger().info("35s reached, stopping node and plotting results.")
            rclpy.shutdown()
            return


def interpolate_positions(self, q_start, q_end, num_steps=50):
    """
    Linear interpolation between two joint position vectors
    """
    q_start = np.array(q_start)
    q_end = np.array(q_end)

    traj = []
    for i in range(num_steps):
        alpha = i / num_steps
        q = (1 - alpha) * q_start + alpha * q_end
        traj.append(q.tolist())

    return traj

def main():

    rclpy.init()
    node = TrajPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    if len(node.time_log) == 0:
        print("No joint acceleration data recorded.")
        node.destroy_node()
        rclpy.shutdown()
        return

    # to numpy
    time = np.array(node.time_log)
    qdd = np.array(node.qdd_log)   # shape: [N, 7]
    # clear the useless data
    mask = time >= 5.0
    time = time[mask]
    qdd = qdd[mask, :]

    # draw the picture
    plt.figure(figsize=(10, 6))

    time_dense = np.linspace(time.min(), time.max(), 5 * len(time))

    for i in range(7):
        qdd_dense = np.interp(time_dense, time, qdd[:, i])
        plt.plot(time_dense, qdd_dense, label=f'Joint {i+1}')

    plt.xlabel("Time [s]")
    plt.ylabel("Joint acceleration [rad/s²]")
    plt.title("Joint accelerations vs time (dense interpolation)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()
