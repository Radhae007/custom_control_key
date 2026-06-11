import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import serial

class ImuSerialNode(Node):
    def __init__(self):
        super().__init__('imu_serial_node')
        self.publisher_ = self.create_publisher(Imu, 'imu/data', 10)
        # CHANGE /dev/ttyUSB0 to your actual port (check with ls /dev/tty*)
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
        self.timer = self.create_timer(0.02, self.publish_imu) # 50Hz

    def publish_imu(self):
        if self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                data = line.split(',')
                if len(data) == 6:
                    msg = Imu()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.header.frame_id = 'imu_link'

                    # Mapping data: ax, ay, az, gx, gy, gz
                    msg.linear_acceleration.x = float(data[0])
                    msg.linear_acceleration.y = float(data[1])
                    msg.linear_acceleration.z = float(data[2])
                    msg.angular_velocity.x = float(data[3])
                    msg.angular_velocity.y = float(data[4])
                    msg.angular_velocity.z = float(data[5])

                    self.publisher_.publish(msg)
            except Exception as e:
                self.get_logger().error(f"Error parsing data: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ImuSerialNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
