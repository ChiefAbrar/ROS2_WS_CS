```markdown
# Documentation

## 1. Workspace Setup

```
mkdir -p ~/ros2_ws_CS/src
cd ~/ros2_ws_CS/src
```

## 2. Create your packages:
```
ros2 pkg crete --build-type ament_python basic_comm
ros2 pkg create --build-type ament_python serial_comm
ros2 pkg create --build-type ament_python inverse_kinematics
```

## 3. Build workspace:
```
cd ~/ros2_ws_CS
colcon build
source install/setup.bash
```
**Note:** After every changes you have again run the *colcon build* command. Also in every terminal before running the code you have to do sourcing by running the *source install/setup.bash* command and if you don't want to run the source command in every terminal rather want this to execute at every terminal execution you can run the following command:
```
echo "source ~/ros2_ws_CS/install/setup.bash" >> ~/.bashrc
```

## Check Serial Ports (for Arduino)
Run the following to list available serial ports:
```
dmesg | grep/tty
```
or,
```
ls /dev/tty*
```
In a simulated environment, you can skip serial access and manually publish data to simulate Arduino behavior. Also, you can use *sample_arduino.py* to do that, which is discuss at the last part of the documentation (C6).

---

## Task C1: Basic Communication

Create two ROS2 nodes of which:
1. First node takes input from the user as string and publish it to a topic.
   - File is within *basic_comm/basic_comm/talker.py*
   - To run it put below command in terminal:
     ```
     ros2 run basic_comm talker
     ```
2. Second node subscribes to that topic and print whatever message it receives.
   - File is within *basic_comm/basic_comm/listener.py*
   - To run it put below command in terminal:
     ```
     ros2 run basic_comm listener
     ```
### Test
Type a message in the publisher terminal and see it appear in the subscriber's terminal.

---

## Task C2: Serial Communication

### Arduino Code (serial.ino)
Simulates sensor data and responds to LED on/off commands.

### ROS2 Nodes

- `serial_comm/serial_comm/serial_node.py`: communicates with Arduino
- `serial_comm/serial_comm/user_input_node.py`: sends LED toggle commands

### Serial Data Format

Sent: `valueA,valueB,valueC,valueD\n`

- A: Integer  [-100, 100]
- B: Float    [-1.0, 1.0]
- C: Integer  [0, 1023]
- D: String   hello

### Topics

- `/sensor_data/value_a`: `Int64`
- `/sensor_data/value_b`: `Float64`
- `/sensor_data/value_c`: `Int64`
- `/sensor_data/value_d`: `String`

### Run
```
ros2 run serial_comm serial_node
ros2 run serial_comm user_input_node
```

---

## Task C3: Inverse Kinematics

### Goal

- Given target (x, y), calculate joint angles (`theta1`, `theta2`) to reach the position.
- Publish angles to `/miniarm/angles` as `Vector3`.

### IK Formulas

Assuming:

- `L1 = 14.0` cm (segment 1)
- `L2 = 15.5` cm (segment 2)

Given: Target (x, y)

1. Compute distance to point:
   d = sqrt(x^2 + y^2)
2. Check reachability:
   ```
   if d > L1 + L2 or d < |L1 - L2|:
      error("Out of reach")
   ```
3. Compute elbow angle (theta2):
   phi = acos((L1^2 + L2^2 - d^2) / (2 * L1 * L2))
   theta2 = degrees(pi - phi)
4. Compute shoulder angle (theta1):
   beta = acos((L1^2 + d^2 - L2^2) / (2 * L1 * d))
   alpha = atan2(y, x)
   theta1 = degrees(alpha - beta)

### Run

```
ros2 run inverse_kinematics ik_node
```

### Test

```
ros2 topic pub /miniarm/target geometry_msgs/msg/Vector3 '{x: 10.0, y: 20.0, z: 0.0}'
```

---

## Task C4: Launch File + Logger Node

### Logger Node

Prints sensor topic values.

File: `serial_comm/logger_node.py`

### Launch File

Path: `serial_comm/launch/system_launch.py`

### Launch Content:

```
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='serial_comm', executable='serial_node', name='serial_node'),
        Node(package='serial_comm', executable='user_input_node', name='user_input_node'),
        Node(package='serial_comm', executable='logger_node', name='logger_node'),
    ])
```

### Run (All)

```
ros2 launch serial_comm system_launch.py
```

---

## Task C5: Forward Kinematics

### Goal

- Input: Angles from `/miniarm/angles`
- Output: Compute (x, y) of arm tip and print

### Formulas

Given `theta1`, `theta2` in degrees:

```
x1 = L1 * cos(theta1)
y1 = L1 * sin(theta1)
x2 = x1 + L2 * cos(theta1 + theta2)
y2 = y1 + L2 * sin(theta1 + theta2)
```

### Run

```
ros2 run inverse_kinematics fk_node
```

### Test

```
ros2 topic pub /miniarm/angles geometry_msgs/msg/Vector3 '{x: 90.0, y: 0.0, z: 0.0}'
```

Expected output: `x = 0.00, y = 29.5`

---

## Task C6: Demo Run without a Real Arduino

To test run without a real Arduino, you can simply use *sample_arduino.py*. Follow the steps below:
1. Open a terminal and run:
   ```
   socat -d -d PTY, raw, echo=0 PTY, raw, echo=0
   ```
   Here, *-d -d* enables debug output to show the port names.
2. Then put the port number in the *sample_arduino.py* necessary informations are given there.
```
