#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from geometry_msgs.msg import TwistStamped

class VelocityFusionNode(Node):
    def __init__(self):
        super().__init__('velocity_fusion_node')
        
        # Subscriptions
        self.odom_sub = self.create_subscription(Odometry, '/odom1', self.odom_callback, 10)
        self.imu_sub = self.create_subscription(Imu, '/imu/data', self.imu_callback, 10)
        
        # Publisher
        self.twist_pub = self.create_publisher(TwistStamped, '/velocity/fused', 10)
        
        # Input Cache
        self.odom_vx = 0.0
        self.odom_wz = 0.0
        
        # --- THE ONLY TUNING PARAMETER ---
        # Adjust this value (rad/s) to determine when the robot is considered "turning"
        self.TURN_THRESHOLD = 0.25  

    def odom_callback(self, msg):
        self.odom_vx = msg.twist.twist.linear.x
        self.odom_wz = msg.twist.twist.angular.z

    def imu_callback(self, msg):
        twist_msg = TwistStamped()
        twist_msg.header.stamp = msg.header.stamp  # Sync to sensor clock
        twist_msg.header.frame_id = 'base_footprint'
        
        # 1. Linear Velocities (2D Planar Constraints)
        twist_msg.twist.linear.x = self.odom_vx  # Always trust wheels for forward speed
        twist_msg.twist.linear.y = 0.0           # Explicitly zeroed (No strafing)
        twist_msg.twist.linear.z = 0.0           # Explicitly zeroed (No vertical lift)
        
        # 2. Angular Velocities (2D Planar Constraints)
        twist_msg.twist.angular.x = 0.0          # Explicitly zeroed (Ignore body roll noise)
        twist_msg.twist.angular.y = 0.0          # Explicitly zeroed (Ignore body pitch noise)
        
        # 3. Hard-Switch Angular Z Logic
        imu_wz = msg.angular_velocity.z
        if abs(imu_wz) > self.TURN_THRESHOLD:
            twist_msg.twist.angular.z = imu_wz   # Active Turning: Trust the gyro completely
        else:
            twist_msg.twist.angular.z = self.odom_wz  # Straight/Idle: Trust Odometry completely
            
        self.twist_pub.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = VelocityFusionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
