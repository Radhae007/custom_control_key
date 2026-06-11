#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
from geometry_msgs.msg import TwistStamped, TransformStamped
from nav_msgs.msg import Odometry
import tf2_ros

class PoseIntegratorNode(Node):
    def __init__(self):
        super().__init__('pose_integrator_node')
        
        # Subscriber to File 1's output
        self.twist_sub = self.create_subscription(TwistStamped, '/velocity/fused', self.velocity_callback, 10)
        
        # Publishers & TF Broadcaster
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        
        # Internal Dead-Reckoning Tracking State
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_time = None

    def velocity_callback(self, msg):
        current_time = rclpy.time.Time.from_msg(msg.header.stamp)
        
        # Initialize tracking on the very first frame received
        if self.last_time is None:
            self.last_time = current_time
            return
            
        # Calculate precise dt based on the message timestamps
        dt = (current_time - self.last_time).nanoseconds / 1e9
        if dt <= 0:
            return
        self.last_time = current_time

        # Extract clean velocities
        vx = msg.twist.linear.x
        wz = msg.twist.angular.z

        # 1. Integrate Orientation (Yaw)
        self.theta += wz * dt
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta)) # Map to [-pi, pi]

        # 2. Integrate Position (Project body frame forward velocity into world coordinates)
        self.x += vx * math.cos(self.theta) * dt
        self.y += vx * math.sin(self.theta) * dt

        # 3. Publish Odometry and TF Transform
        self.publish_state(msg.header.stamp, vx, wz)

    def publish_state(self, stamp, vx, wz):
        qz = math.sin(self.theta / 2.0)
        qw = math.cos(self.theta / 2.0)

        # Build Odometry Msg
        odom = Odometry()
        odom.header.stamp = stamp
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'
        
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw
        
        odom.twist.twist.linear.x = vx
        odom.twist.twist.angular.z = wz
        self.odom_pub.publish(odom)

        # Build TF Transform Frame
        t = TransformStamped()
        t.header.stamp = stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw
        self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = PoseIntegratorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
