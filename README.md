# Avibot Docs[15-06-26]

## Components List
1. Raspberry pi-5 [16Gb Ram , 128Gb SD Card]
2. 2 x Microcontrollers(ESP8266)
3. IMU (MPU6050)
4. YDLidar T Mini Plus
5. 2 x Encoders OE-775
6. 2 x Orange Motors
7. Cytron Motor Driver 

## Introduction
The avibot has a proper setup to run SLAM(Manual), Navigation in it. This is a 2 Wheeled Diff drive bot with a castor wheel in the front. 

## Steps to run the bot

### Power the pi 
- Run the below commands to ssh into the pi (ssid:avibot , password:avibot1234)

``` ssh avibot@avibot.local``` -- It asks for password to ssh into it. [Pswd: avibot]

Docker commands 
``` docker start avibot``` -- to run the container in avibot
``` docker exec -it avibot``` -- to enter inside the running container 
Source commands 
```source /opt/ros/humble/setup.bash```
```source install/setup.bash```
### Micro ROS
Now plug the USB cable from ESP8266 connected with Encoders to the pi and then run the below code in the terminal, once yoy run it press RST on the ESP8266 to start the connection 
```ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 ```

### Lidar
For lidar open a new terminal instance follow all the processes, get inside pi using ssh, skip the <docker start> part as the container is running (used by the Micro ros terminal). 

For lidar connect the both USB cables (Power and Data) to the USB ports of the Pi, then run the following 
```ros2 launch ydlidar_ros2_driver ydlidar_launch.py```

### IMU
For imu similarly open 3  new terminal and follow usual procedure in all the 3. 
<Connection>
Connect the USB cable from the Other ESP8266 to the pi and run the below commands  
Terminal -1 
```ros2 run custom_control_key imu_node```

Terminal -2
```cd src/custom_control_key/custom_control_key```
```python3 pose_integrator.py```

Terminal -3
```cd src/custom_control_key/custom_control_key```
```python3 velocity_fusion_node.py```

### Running the SLAM, Nav2 package 
Open the terminal and follow usual procedure. And run the below commands 
```ros2 launch custom_control_key launch.py```

### Teleopertaion(Movement control)
```ros2 run teleop_twist_keyboard teleop_twist_keyboard```






