#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import math

class OdomToDegrees(Node):
    def __init__(self):
        super().__init__('odom_to_degrees_node')
        
        # Subscribe directly to your filtered odometry topic
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        
        self.get_logger().info("Converter Node Started (0° - 360° Mode). Waiting for /odom...")

    def odom_callback(self, msg):
        # 1. Grab the position coordinates
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        
        # 2. Grab the raw quaternion values
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        
        # 3. Convert Quaternion (Z, W) back to Euler Yaw (Radians)
        yaw_radians = math.atan2(2.0 * qw * qz, 1.0 - 2.0 * (qz * qz))
        
        # 4. Convert to degrees and map strictly to a 0 to 360 range
        yaw_degrees = math.degrees(yaw_radians) % 360.0
        
        # 5. Print a clean, single-line readout to the console
        # Changed the spacing slightly (:6.2f) to perfectly align 3-digit angles
        print(f"Position -> X: {x:6.2f}m | Y: {y:6.2f}m  ||  Orientation -> Heading: {yaw_degrees:6.2f}°", end="\r")

def main(args=None):
    rclpy.init(args=args)
    node = OdomToDegrees()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nExiting...")
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
