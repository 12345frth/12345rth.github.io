# ROS 2 机器人开发 — 学习用例与文档

> 基于《ROS 2机器人开发从入门到实践》配套代码（作者：小鱼 fishros）
> 项目地址：`D:\workSpace\hermes_workspace\ros2bookcode`

---

## 一、项目概述

本项目是一本 ROS 2 机器人开发书籍的完整配套代码，涵盖从 C++/Python 基础、ROS 2 核心概念，到嵌入式运动控制、LiDAR 驱动、Micro-ROS 通信、Navigation2 自主导航的完整技术栈。

### 1.1 技术栈全景

```
┌─────────────────────────────────────────────────┐
│                   ROS 2 层                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │ Bringup  │ │ Nav2 导航 │ │  YDLidar 驱动    │ │
│  │ (TF/URDF)│ │(规划/控制)│ │  (SDK + ROS2)   │ │
│  └──────────┘ └──────────┘ └──────────────────┘ │
├─────────────────────────────────────────────────┤
│              通信桥接层                          │
│  ┌──────────────┐ ┌──────────────┐              │
│  │ Micro-ROS    │ │ Serial2WiFi  │              │
│  │ (Agent+Msgs) │ │ (TCP Server) │              │
│  └──────────────┘ └──────────────┘              │
├─────────────────────────────────────────────────┤
│              嵌入式层 (ESP32)                    │
│  ┌────────┐ ┌──────┐ ┌────────┐ ┌───────────┐  │
│  │运动控制│ │ IMU  │ │ 超声波 │ │ LED/GPIO  │  │
│  │(PID+K) │ │      │ │        │ │           │  │
│  └────────┘ └──────┘ └────────┘ └───────────┘  │
└─────────────────────────────────────────────────┘
```

### 1.2 目录结构

```
ros2bookcode/
├── README.md                          # 项目说明
├── image/book.jpg                     # 书籍封面
├── learn_cpp/                         # C++ 基础学习
├── learn_py/                          # Python 基础学习
├── learn_pluginlib/                   # ROS2 插件机制
└── chapt9/                            # 第9章：机器人开发实战
    ├── fishbot_ws/src/                # ROS2 工作空间
    │   ├── fishbot_bringup/           # 启动与TF转换
    │   ├── fishbot_description/       # URDF机器人模型
    │   ├── fishbot_navigation2/       # Nav2导航配置
    │   ├── micro-ROS-Agent/           # Micro-ROS代理
    │   ├── micro_ros_msgs/            # Micro-ROS消息
    │   ├── ros_serial2wifi/           # WiFi串口桥接
    │   └── ydlidar_ros2/              # YDLidar驱动+SDK
    ├── example_imu/                   # IMU传感器示例
    ├── example_led/                   # LED控制示例
    ├── example_project/               # PlatformIO模板
    ├── example_ultrasound/            # 超声波测距示例
    ├── fishbot_motion_control/        # 运动控制(基础版)
    ├── fishbot_motion_control_9.3/    # 运动控制v9.3
    ├── fishbot_motion_control_9.3.4/  # 运动控制v9.3.4(+IMU)
    └── fishbot_motion_control_9.4.1/  # 运动控制v9.4.1(micro-ROS)
```

---

## 二、环境准备

### 2.1 ROS 2 环境

```bash
# Ubuntu 22.04 + ROS 2 Humble
sudo apt install ros-humble-desktop
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
sudo apt install ros-humble-tf-transformations

# 创建工作空间
mkdir -p ~/fishbot_ws/src
cd ~/fishbot_ws/src
# 将 fishbot_ws/src/ 下所有包拷贝到此目录
```

### 2.2 嵌入式环境 (ESP32)

```ini
# PlatformIO 配置示例 (platformio.ini)
[env:fishbot]
platform = espressif32
board = esp32dev
framework = arduino
board_microros_transport = wifi
monitor_speed = 115200
lib_deps =
    Esp32McpwmMotor   # 电机PWM控制
    Esp32PcntEncoder  # 编码器脉冲计数
    micro_ros_platformio  # Micro-ROS库
```

### 2.3 硬件清单

| 组件 | 型号 | 用途 |
|------|------|------|
| 主控 | ESP32 | 运动控制+通信 |
| 电机驱动 | Mcpwm | PWM电机控制 |
| 编码器 | PCNT | 轮速反馈 |
| IMU | MPU6050等 | 姿态检测 |
| 超声波 | HC-SR04 | 障碍物检测 |
| LiDAR | YDLidar系列 | 2D激光扫描 |

---

## 三、学习路径

```
第1阶段：基础入门
  ├── learn_cpp/ → C++ 语法基础
  ├── learn_py/ → Python 语法基础
  └── learn_pluginlib/ → ROS2 插件机制

第2阶段：嵌入式基础
  ├── example_project → PlatformIO项目模板
  ├── example_led → GPIO控制/LED闪烁
  ├── example_imu → IMU数据读取
  └── example_ultrasound → 超声波测距+PID

第3阶段：运动控制
  ├── fishbot_motion_control_9.3 → 本地PID+运动学
  ├── fishbot_motion_control_9.3.4 → 加入IMU
  └── fishbot_motion_control_9.4.1 → micro-ROS联网

第4阶段：ROS 2 集成
  ├── fishbot_description → URDF建模
  ├── fishbot_bringup → 启动+TF
  ├── ydlidar_ros2 → LiDAR驱动
  ├── micro_ros_msgs + micro-ROS-Agent → 通信桥接
  └── ros_serial2wifi → WiFi串口

第5阶段：自主导航
  └── fishbot_navigation2 → Nav2建图定位导航
```

---

## 四、模块详解

### 4.1 嵌入式基础模块

#### 4.1.1 example_project — PlatformIO 模板

**学习目标：** 掌握 PlatformIO 项目结构和 ESP32 开发环境

**核心文件：** `platformio.ini`, `src/main.cpp`

```cpp
// 最小化模板
#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    Serial.println("Hello FishBot!");
}

void loop() {
    delay(1000);
}
```

**运行方法：**
```bash
# 在 VSCode 中打开项目文件夹，点击 PlatformIO 上传按钮
# 或命令行
pio run --target upload
pio device monitor
```

---

#### 4.1.2 example_led — LED 控制

**学习目标：** ESP32 GPIO 输出控制，理解数字IO

```cpp
#define LED_PIN 2

void setup() {
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_PIN, HIGH);   // 亮
    delay(500);
    digitalWrite(LED_PIN, LOW);    // 灭
    delay(500);
}
```

**关键知识点：**
- `pinMode(pin, mode)` — 设置引脚模式
- `digitalWrite(pin, value)` — 输出高低电平
- `delay(ms)` — 毫秒延时

---

#### 4.1.3 example_imu — IMU 传感器

**学习目标：** I2C 通信、IMU 数据读取（加速度、角速度）

**硬件连接：** SDA→GPIO21, SCL→GPIO22

**运行方法：**
```bash
pio run --target upload
pio device monitor  # 查看串口输出的加速度/角速度数据
```

---

#### 4.1.4 example_ultrasound — 超声波测距 + PID

**学习目标：** 超声波传感器原理、PID 控制算法

**原理：**
```
1. TRIG 发 10us 高脉冲 → 模块发射超声波
2. ECHO 返回高电平 → 持续时间 = 声波来回时间
3. 距离 = 高电平时间 × 0.0343 / 2 （单位 cm）
```

```cpp
// 超声波测距核心代码
#define TRIG 5
#define ECHO 18

float getDistance() {
    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    
    double delta_time = pulseIn(ECHO, HIGH);       // 高电平时间(us)
    float distance = delta_time * 0.0343 / 2;      // 计算距离(cm)
    return distance;
}
```

**本模块还引入了 PidController 库：**
```
PID公式: output = Kp*e + Ki*∫e + Kd*de/dt
参数:   Kp=0.625, Ki=0.125, Kd=0.0
输出限幅: [-100, 100]
```

---

### 4.2 运动控制模块（渐进式学习）

这是项目最核心的章节，通过 4 个版本展示从本地控制到 ROS 2 联网的完整演进。

#### 4.2.1 fishbot_motion_control_9.3 — 本地运动控制

**学习目标：** 差速运动学、PID 速度控制、编码器反馈

**硬件引脚映射：**
```
电机0: PWM_22, DIR_23  |  编码器0: GPIO_32, GPIO_33
电机1: PWM_12, DIR_13  |  编码器1: GPIO_26, GPIO_25
轮距: 175mm
```

**核心代码：**
```cpp
#include <Esp32PcntEncoder.h>   // 编码器
#include <Esp32McpwmMotor.h>    // 电机PWM
#include <PidController.h>      // PID控制
#include <Kinematics.h>         // 运动学

Esp32PcntEncoder encoders[2];
Esp32McpwmMotor motor;
PidController pid_controller[2];
Kinematics kinematics;

// 目标速度（硬编码，无ROS通信）
float target_linear_speed = 20.0;   // mm/s
float target_angular_speed = 0.1;   // rad/s

void setup() {
    Serial.begin(115200);
    
    // 绑定电机引脚
    motor.attachMotor(0, 22, 23);
    motor.attachMotor(1, 12, 13);
    
    // 初始化编码器
    encoders[0].init(0, 32, 33);
    encoders[1].init(1, 26, 25);
    
    // 配置PID (P=0.625, I=0.125, D=0.0)
    pid_controller[0].update_pid(0.625, 0.125, 0.0);
    pid_controller[1].update_pid(0.625, 0.125, 0.0);
    pid_controller[0].out_limit(-100, 100);
    pid_controller[1].out_limit(-100, 100);
    
    // 差速运动学逆解
    kinematics.set_wheel_distance(175);
    kinematics.set_motor_param(0, 0.105805);
    kinematics.set_motor_param(1, 0.105805);
    kinematics.kinematics_inverse(
        target_linear_speed, target_angular_speed,
        &out_left_speed, &out_right_speed);
    
    pid_controller[0].update_target(out_left_speed);
    pid_controller[1].update_target(out_right_speed);
}

void loop() {
    // 读取编码器 → 计算实际速度 → PID计算 → 输出PWM
    kinematics.update_speed(
        encoders[0].getTicks(), encoders[1].getTicks(),
        encoders[0].getRpm(), encoders[1].getRpm());
    
    motor.updateMotorSpeed(
        0, pid_controller[0].update(
            kinematics.motor_speed(0)));
    motor.updateMotorSpeed(
        1, pid_controller[1].update(
            kinematics.motor_speed(1)));
    
    delay(10);
}
```

**控制回路：**
```
目标速度 → [运动学逆解] → [PID控制器] → [PWM输出] → 电机
                                        ↑
                         编码器速度 ← [运动学正解] ← 编码器脉冲
```

**运行方法：**
```bash
pio run --target upload
pio device monitor  # 查看串口速度/位置输出
```

---

#### 4.2.2 fishbot_motion_control_9.3.4 — 加入 IMU

**与 v9.3 的差异：**
- 新增 IMU 数据融合
- 利用角速度辅助姿态估计

---

#### 4.2.3 fishbot_motion_control_9.4.1 — micro-ROS 联网控制

**学习目标：** 将 ESP32 接入 ROS 2 网络，通过 WiFi + micro-ROS 接收速度指令

**重大升级：**
```
v9.3:  硬编码目标速度 → 串口输出
v9.4.1: ROS2 /cmd_vel → WiFi → micro-ROS → PID → 电机
```

**micro-ROS 通信流程：**
```
ROS 2 PC (Agent) ←→ WiFi ←→ ESP32 (micro-ROS Client)
     ↑                            ↑
  192.168.1.103:8888        订阅 /cmd_vel
                            发布 /odom
```

```cpp
#include <micro_ros_platformio.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <geometry_msgs/msg/twist.h>  // cmd_vel

// micro-ROS 核心对象
rcl_allocator_t allocator;
rclc_support_t support;
rclc_executor_t executor;
rcl_node_t node;
rcl_subscription_t cmd_vel_sub;
geometry_msgs__msg__Twist cmd_vel_msg;

// micro-ROS 任务（独立线程）
void microros_task(void* args) {
    // 1. WiFi连接 micro-ROS Agent
    IPAddress agent_ip;
    agent_ip.fromString("192.168.1.103");
    set_microros_wifi_transports(
        "fishros", "88888888", agent_ip, 8888);
    delay(3000);
    
    // 2. 初始化 micro-ROS
    allocator = rcl_get_default_allocator();
    rclc_support_init(&support, 0, NULL, &allocator);
    rclc_node_init_default(&node, "fishbot_motion_control",
                           "", &support);
    
    // 3. 订阅 /cmd_vel
    rclc_subscription_init_default(
        &cmd_vel_sub, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(
            geometry_msgs, msg, Twist),
        "/cmd_vel");
    
    // 4. 创建执行器
    rclc_executor_init(&executor, &support.context,
                       1, &allocator);
    rclc_executor_add_subscription(
        &executor, &cmd_vel_sub, &cmd_vel_msg,
        &cmd_vel_callback, ON_NEW_DATA);
    
    // 5. 循环执行
    while (true) {
        rclc_executor_spin_some(&executor,
            RCL_MS_TO_NS(100));
    }
}

// 速度指令回调
void cmd_vel_callback(const void* msgin) {
    const geometry_msgs__msg__Twist* msg =
        (const geometry_msgs__msg__Twist*)msgin;
    
    // 更新运动学目标
    kinematics.kinematics_inverse(
        msg->linear.x * 1000,   // m/s → mm/s
        msg->angular.z,
        &out_left_speed, &out_right_speed);
    
    pid_controller[0].update_target(out_left_speed);
    pid_controller[1].update_target(out_right_speed);
}

void setup() {
    // ... 电机/编码器/PID 初始化（同 9.3）...
    
    // 启动 micro-ROS 线程
    xTaskCreatePinnedToCore(
        microros_task, "microros_task",
        10240, NULL, 1, NULL, 0);
}
```

**运行方法：**
```bash
# 步骤1: PC端启动 micro-ROS Agent
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888

# 步骤2: ESP32 上电 → 自动连接 WiFi → 连接 Agent

# 步骤3: PC端发布速度指令
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.1}, angular: {z: 0.0}}"

# 步骤4: 查看机器人里程计
ros2 topic echo /odom
```

---

### 4.3 ROS 2 包详解

#### 4.3.1 fishbot_description — URDF 机器人模型

**学习目标：** ROS 2 中的机器人建模

**功能：**
- 定义机器人的物理结构（URDF/XACRO）
- 发布 `robot_description` 参数
- 提供 `joint_state_publisher` + `robot_state_publisher`

**依赖：**
- `robot_state_publisher`
- `joint_state_publisher`

---

#### 4.3.2 fishbot_bringup — 启动 + TF 转换

**学习目标：** ROS 2 Launch 文件、TF2 坐标变换

**核心节点：`odom2tf`** — 将 odometry 消息转为 TF 广播

```cpp
class OdomTopic2TF : public rclcpp::Node {
public:
  OdomTopic2TF(std::string name) : Node(name) {
    // 订阅 odom，使用 SensorDataQoS（可靠传输）
    odom_subscribe_ = this->create_subscription<nav_msgs::msg::Odometry>(
        "odom", rclcpp::SensorDataQoS(),
        std::bind(&OdomTopic2TF::odom_callback_, this,
                  std::placeholders::_1));
    
    // 创建 TF 广播器
    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(this);
  }

private:
  void odom_callback_(const nav_msgs::msg::Odometry::SharedPtr msg) {
    // 将 odom.pose.pose 转换为 TransformStamped 并广播
    geometry_msgs::msg::TransformStamped transform;
    transform.header = msg->header;
    transform.child_frame_id = msg->child_frame_id;
    transform.transform.translation.x = msg->pose.pose.position.x;
    // ... y, z, rotation ...
    tf_broadcaster_->sendTransform(transform);
  }
};
```

**启动文件：**
```python
# bringup.launch.py
# 启动: urdf2tf (URDF→TF) + fishbot_bringup 节点
```

**运行方法：**
```bash
ros2 launch fishbot_bringup bringup.launch.py
ros2 run tf2_tools view_frames  # 查看TF树
```

---

#### 4.3.3 ydlidar_ros2 — YDLidar 激光雷达驱动

**学习目标：** 传感器驱动开发、ROS 2 Node 生命周期

**包结构：**
```
ydlidar_ros2/
├── src/
│   ├── ydlidar_node.cpp              # 主节点
│   ├── ydlidar_client.cpp            # 客户端
│   └── ydlidar_ros2_driver_node.cpp  # 驱动节点(新版)
├── sdk/                              # 完整 YDLidar SDK
│   ├── src/
│   │   ├── serial.cpp                # 串口通信
│   │   ├── CYdLidar.cpp              # 核心驱动
│   │   ├── YDlidarDriver.cpp         # 协议解析
│   │   └── ...更多驱动变体...
│   ├── serial/                       # 跨平台串口(win/unix)
│   └── math/                         # 数学库
├── launch/
│   ├── ydlidar.py                    # Python启动
│   └── ydlidar_launch.py             # 新版启动
├── params/ydlidar.yaml               # 参数配置
└── config/ydlidar.rviz               # RViz配置
```

**启动方法：**
```bash
ros2 launch ydlidar_ros2 ydlidar_launch.py

# 或在 RViz 中查看
rviz2 -d src/ydlidar_ros2/config/ydlidar.rviz
```

**参数配置 (`ydlidar.yaml`)：**
```yaml
ydlidar_node:
  ros__parameters:
    port: /dev/ttyUSB0
    baudrate: 230400
    frame_id: laser_frame
    frequency: 10.0       # 扫描频率 Hz
    angle_min: -180.0
    angle_max: 180.0
    range_min: 0.08       # 最小测距 m
    range_max: 16.0       # 最大测距 m
```

---

#### 4.3.4 micro_ros_msgs + micro-ROS-Agent — 嵌入式通信

**学习目标：** Micro-ROS 架构、DDS-XRCE 协议

**架构：**
```
ESP32 (micro-ROS Client)
    ↓ UDP/WiFi
micro-ROS Agent (PC端)
    ↓ DDS
ROS 2 网络
```

**micro_ros_msgs：** 自定义消息类型定义，用于 ESP32 ⇔ PC 通信

**micro-ROS-Agent：** PC 端代理程序，桥接 XRCE 与 DDS

```bash
# 启动 Agent
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888
```

---

#### 4.3.5 ros_serial2wifi — WiFi 串口桥接

**学习目标：** TCP Socket 编程、串口通信

**功能：** 将物理串口数据通过 WiFi TCP 转发到 ROS 2 网络

```python
# setup.py 入口点
entry_points={
    'console_scripts': [
        'tcp_server=ros_serail2wifi.tcpserver:main'
    ],
},
```

**运行方法：**
```bash
ros2 run ros_serail2wifi tcp_server
```

---

#### 4.3.6 fishbot_navigation2 — Nav2 自主导航

**学习目标：** Navigation2 完整导航栈配置与使用

**启动文件逻辑：**
```python
# navigation2.launch.py
def generate_launch_description():
    return LaunchDescription([
        # 1. 声明参数
        DeclareLaunchArgument('map',       # 地图文件
            default='.../maps/room.yaml'),
        DeclareLaunchArgument('params_file',  # Nav2参数
            default='.../config/nav2_params.yaml'),
        DeclareLaunchArgument('use_sim_time',  # 仿真时间
            default='true'),
        
        # 2. 引入 nav2_bringup
        IncludeLaunchDescription(
            nav2_bringup/bringup_launch.py,
            launch_arguments={...}),
        
        # 3. 启动 RViz
        Node(package='rviz2', executable='rviz2'),
    ])
```

**Nav2 参数配置 (`nav2_params.yaml`) 核心模块：**

| 模块 | 插件 | 作用 |
|------|------|------|
| `planner_server` | `NavfnPlanner` | 全局路径规划 (A*) |
| `controller_server` | `RegulatedPurePursuit` | 局部路径跟踪 |
| `behavior_server` | `Spin/Backup/Wait` | 行为恢复 |
| `bt_navigator` | `NavigateToPose` | 行为树导航 |
| `velocity_smoother` | — | 速度平滑 |
| `waypoint_follower` | `WaitAtWaypoint` | 航点跟随 |
| `smoother_server` | `SimpleSmoother` | 路径平滑 |

**运行完整导航：**
```bash
# 1. 启动机器人驱动
ros2 launch fishbot_bringup bringup.launch.py

# 2. 启动 LiDAR
ros2 launch ydlidar_ros2 ydlidar_launch.py

# 3. 启动 micro-ROS Agent
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888

# 4. 启动导航
ros2 launch fishbot_navigation2 navigation2.launch.py

# 5. 在 RViz 中设置目标点即可开始自主导航
```

---

### 4.4 库文件详解

#### 4.4.1 Kinematics — 差速运动学

**核心概念：**
```
差速机器人运动学:
  v = (v_left + v_right) / 2          # 线速度
  ω = (v_right - v_left) / wheel_distance  # 角速度

逆解(给定v,ω求轮速):
  v_left  = v - ω * wheel_distance / 2
  v_right = v + ω * wheel_distance / 2
```

**关键参数：**
```cpp
kinematics.set_wheel_distance(175);          // 轮距 mm
kinematics.set_motor_param(0, 0.105805);     // 左轮减速比
kinematics.set_motor_param(1, 0.105805);     // 右轮减速比
```

#### 4.4.2 PidController — PID 控制

```
PID 公式: u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt

参数调优经验：
- Kp=0.625: 比例增益，增大加快响应但易超调
- Ki=0.125: 积分增益，消除稳态误差
- Kd=0.0:   微分增益，抑制超调（暂未启用）
- 输出限幅: [-100, 100]（对应 PWM 占空比范围）
```

---

## 五、版本演进对照表

### 运动控制版本对比

| 版本 | ROS通信 | IMU | 控制方式 | 适用场景 |
|------|---------|-----|---------|---------|
| v9.3 | 无(串口) | 无 | 硬编码速度 | 学习运动学+PID |
| v9.3.4 | 无 | 有 | 硬编码速度+姿态 | 学习IMU融合 |
| v9.4.1 | micro-ROS/WiFi | 有 | 订阅/cmd_vel | 联网遥控实战 |

---

## 六、实战练习建议

### 入门级
1. 在 ESP32 上运行 `example_led`，修改闪烁频率
2. 运行 `example_ultrasound`，在串口监控中观察距离变化
3. 运行 `example_imu`，晃动传感器观察数据变化

### 进阶级
4. 修改 `fishbot_motion_control_9.3` 的 PID 参数，观察控制效果差异
5. 调整 `kinematics.set_wheel_distance()` 的值，观察运动轨迹偏差
6. 将 `fishbot_navigation2` 的地图替换为自己的环境地图

### 实战级
7. 搭建完整系统：ESP32 + LiDAR + PC，实现遥控行走
8. 使用 `slam_toolbox` 进行 SLAM 建图
9. 在 Nav2 中设置航点，实现多点自主巡逻

---

## 七、常见问题

**Q: ESP32 连接不上 Agent？**
- 检查 WiFi SSID/密码是否正确（默认 fishros/88888888）
- 确认 Agent IP 地址（代码中 192.168.1.103）
- 确认 PC 防火墙允许 UDP 8888 端口

**Q: LiDAR 无数据？**
- 检查串口权限：`sudo chmod 666 /dev/ttyUSB0`
- 确认 `baudrate` 参数与雷达型号匹配
- 运行 `ros2 topic list` 确认 `/scan` 话题存在

**Q: Nav2 导航失败？**
- 确认 TF 树完整：`ros2 run tf2_tools view_frames`
- 检查 `map → odom → base_link` 变换链
- 验证 `nav2_params.yaml` 中的 `robot_base_frame` 与实际一致

---

*文档生成时间：2026-05-19*
*基于项目：D:\workSpace\hermes_workspace\ros2bookcode*
