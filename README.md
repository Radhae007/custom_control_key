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

## 🔁 Usual Procedure — Full Steps for Every New Terminal

> This section is referenced throughout the docs. Every time you open a **new terminal**, follow these 3 steps in order before running any `ros2` command.

---

### Step 1 — Connect to avibot Wi-Fi & SSH into the Pi

Make sure your machine is connected to the **`avibot`** Wi-Fi network first.

| Field    | Value        |
|----------|--------------|
| SSID     | `avibot`     |
| Password | `avibot1234` |

Then open a terminal and run:

```bash
ssh avibot@avibot.local
```

Enter the SSH password when prompted:

```
avibot
```

---

### Step 2 — Enter the Docker Container

The container should already be running (it was started in the very first terminal). So **skip** `docker start` and go straight to:

```bash
docker exec -it avibot bash
```

> **If the Pi was just rebooted** and the container isn't running yet, start it first:
> ```bash
> docker start avibot
> docker exec -it avibot bash
> ```

---

### Step 3 — Source the ROS 2 Environment

Once inside the container, run both source commands:

```bash
source /opt/ros/humble/setup.bash
```

```bash
source install/setup.bash
```

> ⚠️ You must do this **every time** you enter the container in a new terminal. The environment does not persist between sessions.

| Command | What it does |
|---|---|
| `source /opt/ros/humble/setup.bash` | Loads the core ROS 2 Humble system — makes `ros2` available |
| `source install/setup.bash` | Loads your workspace packages (`custom_control_key`, `ydlidar_ros2_driver`, etc.) |

Skipping either one will cause `ros2` commands to fail with *"package not found"* errors.

---

✅ **You're ready. Now run your `ros2` command for that terminal.**

---

## 🚀 Steps to Run the Bot

> **First terminal only:** Start the Docker container with `docker start avibot` before `docker exec`. All subsequent terminals skip `docker start` — see [Usual Procedure](#-usual-procedure--full-steps-for-every-new-terminal).

---

### 1. Micro ROS (Encoders)

1. Plug in the USB cable from the **ESP8266 connected to the Encoders** into the Pi.
2. Open a terminal and follow the [Usual Procedure](#-usual-procedure--full-steps-for-every-new-terminal) *(this is the first terminal — run `docker start avibot` here)*.
3. Run the Micro ROS agent:

```bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0
```

4. Once the command is running, **press the RST button** on the ESP8266 to establish the connection.

---

### 2. LiDAR

1. Connect **both USB cables** (Power and Data) from the YDLidar T Mini Plus to the Pi.
2. Open a **new terminal** and follow the [Usual Procedure](#-usual-procedure--full-steps-for-every-new-terminal) *(skip `docker start` — container is already running)*.
3. Run:

```bash
ros2 launch ydlidar_ros2_driver ydlidar_launch.py
```

---

### 3. IMU

1. Plug in the USB cable from the **second ESP8266** (IMU) into the Pi.
2. Open **3 new terminals** and follow the [Usual Procedure](#-usual-procedure--full-steps-for-every-new-terminal) in each *(skip `docker start` in all three)*.

**Terminal 1** — IMU Node:

```bash
ros2 run custom_control_key imu_node
```

**Terminal 2** — Pose Integrator:

```bash
cd src/custom_control_key/custom_control_key
```
```bash
python3 pose_integrator.py
```

**Terminal 3** — Velocity Fusion:

```bash
cd src/custom_control_key/custom_control_key
```
```bash
python3 velocity_fusion_node.py
```

---

### 4. SLAM & Nav2

1. Open a **new terminal** and follow the [Usual Procedure](#-usual-procedure--full-steps-for-every-new-terminal) *(skip `docker start`)*.
2. Run:

```bash
ros2 launch custom_control_key launch.py
```

---

### 5. Teleoperation (Movement Control)

1. Open a **new terminal** and follow the [Usual Procedure](#-usual-procedure--full-steps-for-every-new-terminal) *(skip `docker start`)*.
2. Run:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

> Use the keyboard keys shown in the terminal to drive the robot.

---

## 🗂️ Terminal Launch Order Summary

| Terminal # | Purpose | First: [Usual Procedure](#-usual-procedure--full-steps-for-every-new-terminal) | Then Run |
|------------|---------|----------------|----------|
| 1 | Micro ROS (Encoders) | ✅ + `docker start avibot` | `ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0` |
| 2 | LiDAR | ✅ | `ros2 launch ydlidar_ros2_driver ydlidar_launch.py` |
| 3 | IMU Node | ✅ | `ros2 run custom_control_key imu_node` |
| 4 | Pose Integrator | ✅ | `cd src/custom_control_key/custom_control_key` → `python3 pose_integrator.py` |
| 5 | Velocity Fusion | ✅ | `cd src/custom_control_key/custom_control_key` → `python3 velocity_fusion_node.py` |
| 6 | SLAM / Nav2 | ✅ | `ros2 launch custom_control_key launch.py` |
| 7 | Teleop | ✅ | `ros2 run teleop_twist_keyboard teleop_twist_keyboard` |

---

## 📝 Notes

- `docker start avibot` only needs to be run **once** (Terminal 1). All other terminals use only `docker exec -it avibot bash`.
- Always run **both** source commands inside the container for every new terminal session.
- Plug in all USB devices **before** running their respective ROS nodes.
- After running the Micro ROS agent, always **press RST** on the encoder ESP8266 to initialise the connection.
