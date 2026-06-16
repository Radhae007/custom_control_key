# 🤖 Avibot Documentation

> **Version:** 15-06-26 &nbsp;|&nbsp; **Platform:** ROS 2 Humble &nbsp;|&nbsp; **Drive:** Differential (2-Wheel + Castor)

---

## 📦 Components

| # | Component | Details |
|---|-----------|---------|
| 1 | Raspberry Pi 5 | 16 GB RAM, 128 GB SD Card |
| 2 | Microcontrollers | 2× ESP8266 |
| 3 | IMU | MPU6050 |
| 4 | LiDAR | YDLidar T Mini Plus |
| 5 | Encoders | 2× OE-775 |
| 6 | Motors | 2× Orange Motors |
| 7 | Motor Driver | Cytron Motor Driver |

---

## 🧭 Introduction

Avibot is a 2-wheeled differential drive robot with a castor wheel in the front. It is configured to run:

- **SLAM** (Manual)
- **Nav2 Navigation**

---

## 🚀 Steps to Run the Bot

### 1. Power & SSH into the Pi

Connect to the `avibot` Wi-Fi network, then SSH into the Pi:

| Field    | Value          |
|----------|----------------|
| SSID     | `avibot`       |
| Password | `avibot1234`   |
| SSH User | `avibot`       |
| SSH Pass | `avibot`       |

```bash
ssh avibot@avibot.local
```

> You will be prompted for the SSH password: **`avibot`**

---

### 2. Start the Docker Container

Run the following commands to start and enter the container:

```bash
# Start the container
docker start avibot

# Enter the running container
docker exec -it avibot bash
```

---

### 3. Source ROS 2 Environment

Run these inside the container every time you open a new terminal session:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

---

### 4. Micro ROS (Encoders)

1. Plug in the USB cable from the **ESP8266 connected to the Encoders** into the Pi.
2. Run the Micro ROS agent:

```bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
```

3. Once the command is running, **press the RST button** on the ESP8266 to establish the connection.

---

### 5. LiDAR

1. Connect **both USB cables** (Power and Data) from the YDLidar T Mini Plus to the Pi.
2. Open a **new terminal**, SSH into the Pi, and follow the [source commands](#3-source-ros-2-environment).

> ⚠️ **Skip** `docker start avibot` — the container is already running from Step 2.

```bash
ros2 launch ydlidar_ros2_driver ydlidar_launch.py
```

---

### 6. IMU

1. Plug in the USB cable from the **second ESP8266** (IMU) into the Pi.
2. Open **3 new terminals**, SSH into the Pi in each, and follow the [source commands](#3-source-ros-2-environment) in all three.

> ⚠️ **Skip** `docker start avibot` in all three — the container is already running.

**Terminal 1** — IMU Node:
```bash
ros2 run custom_control_key imu_node
```

**Terminal 2** — Pose Integrator:
```bash
cd src/custom_control_key/custom_control_key
python3 pose_integrator.py
```

**Terminal 3** — Velocity Fusion:
```bash
cd src/custom_control_key/custom_control_key
python3 velocity_fusion_node.py
```

---

### 7. SLAM & Nav2

Open a new terminal, follow the [usual procedure](#3-source-ros-2-environment), then launch:

```bash
ros2 launch custom_control_key launch.py
```

---

### 8. Teleoperation (Movement Control)

Open a new terminal, follow the [usual procedure](#3-source-ros-2-environment), then run:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

> Use the keyboard keys shown in the terminal to drive the robot.

---

## 🗂️ Terminal Launch Order Summary

| Step | What | Command |
|------|------|---------|
| 1 | Micro ROS (Encoders) | `ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0` |
| 2 | LiDAR | `ros2 launch ydlidar_ros2_driver ydlidar_launch.py` |
| 3 | IMU Node | `ros2 run custom_control_key imu_node` |
| 4 | Pose Integrator | `python3 pose_integrator.py` |
| 5 | Velocity Fusion | `python3 velocity_fusion_node.py` |
| 6 | SLAM / Nav2 | `ros2 launch custom_control_key launch.py` |
| 7 | Teleop | `ros2 run teleop_twist_keyboard teleop_twist_keyboard` |

---

## 📝 Notes

- Always source ROS 2 and the workspace in every new terminal before running any `ros2` command.
- The Docker container only needs to be **started once** (`docker start avibot`). Subsequent terminals use `docker exec -it avibot bash`.
- Make sure all USB devices are plugged in **before** running their respective ROS nodes.
