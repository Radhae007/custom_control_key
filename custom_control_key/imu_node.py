import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import serial

class ImuSerialNode(Node):
    def __init__(self):
        super().__init__('imu_node')
        self.publisher_ = self.create_publisher(Imu, 'imu/data', 10)
        self.ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=0.1)
        self.timer = self.create_timer(0.02, self.publish_imu)

    def publish_imu(self):
        if self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                data = line.split(',')
                if len(data) == 6:
                    msg = Imu()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.header.frame_id = 'imu_link'

                    msg.linear_acceleration.x = float(data[0])
                    msg.linear_acceleration.y = float(data[1])
                    msg.linear_acceleration.z = float(data[2])
                    msg.angular_velocity.x    = float(data[3])
                    msg.angular_velocity.y    = float(data[4])
                    msg.angular_velocity.z    = float(data[5])

                    # No orientation from this IMU
                    msg.orientation_covariance = [
                        .0001, 0.001, 0.001,
                         0.001, 0.001, 0.001,
                         0.001, 0.001, 0.001
                    ]

                    # Angular velocity covariance
                    # Z (yaw rate) = 0.0001 → BEATS encoder's 0.0005 on vyaw
                    # X,Y kept high (0.05) since we dont use them in EKF
                    msg.angular_velocity_covariance = [
                        0.001,   0.001,    0.0,
                        0.0,    0.05,   0.0,
                        0.0,    0.0,    0.0000000001   # ← key change
                    ]

                    # Linear acceleration covariance
                    # Keep high since EKF config has accel fusing disabled
                    # If you ever enable ax in EKF, lower [0] to ~0.0005
                    msg.linear_acceleration_covariance = [
                        0.05,  0.0,   0.0,
                        0.0,   0.05,  0.0,
                        0.0,   0.0,   0.05
                    ]

                    self.publisher_.publish(msg)

            except Exception as e:
                self.get_logger().error(f"Error parsing serial data: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ImuSerialNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
