#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
import numpy as np
from std_msgs.msg import Float64

# ###################### STUDENT CODE START (IMPORT SERVICE) ######################
from quaternion_conversion_interfaces.srv import QuatToEuler, QuatToRodrigues
# ####################### STUDENT CODE END (IMPORT SERVICE) #######################

class QuatToEulerService(Node):
    def __init__(self):
        super().__init__('quat_to_euler_service_node', start_parameter_services=False)
        self.srv = self.create_service(QuatToEuler, 'quat_to_euler', self.quat_to_euler_callback)

    def quat_to_euler_callback(self, request, response):
        q_x, q_y, q_z, q_w = request.q.x, request.q.y, request.q.z, request.q.w
        self.get_logger().info(f'Euler service received quaternion: [w={q_w}, x={q_x}, y={q_y}, z={q_z}]')
        response.z, response.y, response.x = Float64(), Float64(), Float64()

        # ###################### STUDENT CODE START (QUATERNION TO EULER) ######################
        # Store the results in response.z.data, response.y.data, and response.x.data
        # Z-angle (yaw)
        q = np.array([q_w, q_x, q_y, q_z], dtype=float)
        n = np.linalg.norm(q)
        if n > 0.0:
            q /= n
        w, x, y, z = q

        # Z-Y-X (yaw-pitch-roll)
        # roll (x)
        roll = np.arctan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
        # pitch (y)
        s = 2.0 * (w * y - z * x)
        s = np.clip(s, -1.0, 1.0)
        pitch = np.arcsin(s)
        # yaw (z)
        yaw = np.arctan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))

        response.z.data = float(yaw)
        response.y.data = float(pitch)
        response.x.data = float(roll)
        # ####################### STUDENT CODE END (QUATERNION TO EULER) #######################

        self.get_logger().info(f'Calculated Euler Angles: [z={response.z.data}, y={response.y.data}, x={response.x.data}]')
        return response

class QuatToRodriguesService(Node):
    def __init__(self):
        super().__init__('quat_to_rodrigues_service_node', start_parameter_services=False)
        self.srv = self.create_service(QuatToRodrigues, 'quat_to_rodrigues', self.quat_to_rodrigues_callback)

    def quat_to_rodrigues_callback(self, request, response):
        q_x, q_y, q_z, q_w = request.q.x, request.q.y, request.q.z, request.q.w
        self.get_logger().info(f'Rodrigues service received quaternion: [w={q_w}, x={q_x}, y={q_y}, z={q_z}]')
        response.x, response.y, response.z = Float64(), Float64(), Float64()

        # ###################### STUDENT CODE START (QUATERNION TO RODRIGUES) ##################
        q = np.array([q_w, q_x, q_y, q_z], dtype=float)
        n = np.linalg.norm(q)
        if n > 0.0:
            q /= n
        w, x, y, z = q
        v = np.array([x, y, z], dtype=float)
        v_norm = np.linalg.norm(v)
        eps = 1e-12

        if v_norm < eps:
            r_vec = np.array([0.0, 0.0, 0.0], dtype=float)
        else:
            theta = 2.0 * np.arctan2(v_norm, max(w, 0.0) if abs(w) < eps else w)
            axis = v / v_norm
            t = np.tan(theta / 2.0)
            r_vec = axis * t

        response.x.data = float(r_vec[0])
        response.y.data = float(r_vec[1])
        response.z.data = float(r_vec[2])
        # ####################### STUDENT CODE END (QUATERNION TO RODRIGUES) ###################

        self.get_logger().info(f'Calculated Rodrigues Vector: [x={response.x.data}, y={response.y.data}, z={response.z.data}]')
        return response

def main(args=None):
    rclpy.init(args=args)
    try:
        # Create instances of both service nodes
        quat_to_euler_node = QuatToEulerService()
        quat_to_rodrigues_node = QuatToRodriguesService()

        # Use a MultiThreadedExecutor to handle callbacks from both services concurrently
        executor = MultiThreadedExecutor(num_threads=2)
        executor.add_node(quat_to_euler_node)
        executor.add_node(quat_to_rodrigues_node)

        print("Both Quaternion conversion services are ready.")

        try:
            executor.spin()
        finally:
            executor.shutdown()
            quat_to_euler_node.destroy_node()
            quat_to_rodrigues_node.destroy_node()
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()