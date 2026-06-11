import rospy
from sensor_msgs.msg import Imu
import numpy as np

class ImuCalibrator:
    def __init__(self, num_samples=500):
        self.num_samples = num_samples
        self.accel_samples = []
        self.gyro_samples = []
        self.is_calibrated = False
        
        self.sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        rospy.loginfo(f"Collecting {num_samples} samples for calibration...")

    def imu_callback(self, msg):
        if not self.is_calibrated:
            self.accel_samples.append([
                msg.linear_acceleration.x,
                msg.linear_acceleration.y,
                msg.linear_acceleration.z
            ])
            self.gyro_samples.append([
                msg.angular_velocity.x,
                msg.angular_velocity.y,
                msg.angular_velocity.z
            ])
            
            if len(self.accel_samples) % 100 == 0:
                rospy.loginfo(f"Progress: {len(self.accel_samples)}/{self.num_samples}")

            if len(self.accel_samples) >= self.num_samples:
                self.calculate_offsets()

    def calculate_offsets(self):
        self.is_calibrated = True
        
        accel_means = np.mean(np.array(self.accel_samples), axis=0)
        gyro_means = np.mean(np.array(self.gyro_samples), axis=0)
        
        rospy.loginfo("--- Calibration Complete ---")
        rospy.loginfo(f"Accel Offsets (x,y,z): {accel_means}")
        rospy.loginfo(f"Gyro Offsets (x,y,z): {gyro_means}")
        
        rospy.signal_shutdown("Calibration finished.")

if __name__ == '__main__':
    rospy.init_node('imu_calibrator')
    calibrator = ImuCalibrator(num_samples=500)
    rospy.spin()
