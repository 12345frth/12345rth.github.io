SLAM相关知识点
一、基本概念
激光雷达类型分类：https://zhuanlan.zhihu.com/p/685395877


二、标定
标定雷达LiDAR和雷达LiDAR之间的外参
https://github.com/Livox-SDK/livox_automatic_calibration?utm_source=chatgpt.com
标定相机和雷达
https://github.com/Livox-SDK/livox_camera_lidar_calibration
 标定内置 IMU 和 LiDAR 外参 / 时间偏移
https://github.com/hku-mars/LiDAR_IMU_Init/tree/main
标定IMU的内参/多相机系统的当中的相机的内外参/相机到IMU的外参+时间延时
https://github.com/ethz-asl/kalibr?utm_source=chatgpt.com
IMU分析
https://github.com/gaowenliang/imu_utils?utm_source=chatgpt.com
静止状态下 IMU 原始陀螺仪和加速度计数据的噪声统计特性，
主要关注：白噪声、零偏漂移 / 偏置不稳定性，
方法是：Allan Variance（阿伦方差）分析。  
三、数据集
https://projects.asl.ethz.ch/datasets/
https://github.com/MIT-SPARK/Kimera-Multi-Data
https://thisparticle.github.io/geode/
采用的数据集为：https://github.com/rvp-group/vbr-devkit
当前跑通的数据集是：开源数据集 `GEODE / Stairs / stairs_alpha.bag` 。
数据集下载和调用：
下载工具：
显示可下载的数据集：
下载数据集到指定的目录：
四、livox雷达
SDK
对于跑通当中的Fast-lio算法，目前开源社区存在下面算法：
https://github.com/hku-mars/FAST_LIO
官方 FAST-LIO README 的运行入口和配置本质上是单个 lid_topic + 单个 imu_topic，外参也是按“LiDAR 在 IMU 坐标系下的位姿”来定义的
多雷达跑fast-lio
https://github.com/engcang/FAST_LIO_MULTI?utm_source=chatgpt.com
ROS2
https://github.com/Ericsii/FAST_LIO_ROS2
“FAST-LIO2 的 ROS2 版移植”
更接近原仓库逻辑
更偏算法本体
对 Livox 传统链路更友好
https://github.com/MIT-SPARK/spark-fast-lio/blob/main/README.md
“MIT-SPARK 重新整理过的 ROS2 工程版 FAST-LIO2”
更偏 ROS2 工程可用性
更适合直接跑现成 ROS2 bag
示例更开箱即用
四、Fast-lio

fast-lio2被当作是视觉里程计，也就是前端部分；
前端：FAST-LIO2
回环候选：Scan Context
回环验证：ICP / GICP
后端：Pose Graph Optimization
结果：完整一些的 SLAM 系统
前端：FAST-LIO2
输入：LiDAR + IMU
输出：实时 odom、当前点云、局部地图
回环检测
从前端选关键帧
为关键帧生成 Scan Context
从历史库找相似地点
ICP / GICP 做几何验证
成功后生成回环约束
后端优化
节点：关键帧位姿
边：相邻关键帧边 + 回环边
优化器：因子图 / 位姿图
全局建图
根据优化后的关键帧位姿
重新拼接关键帧点云
输出全局一致地图
原理解析：https://zhuanlan.zhihu.com/p/471876531
1. LIO的类型
LIO 是 LiDAR-Inertial Odometry，也就是把 激光雷达 + IMU 融合起来做实时位姿估计与局部建图。FAST-LIO 官方自己也是这样定义的：它是一个 LiDAR-inertial odometry 包。 
LIO 不是只有一种，常见可以按“方法路线”分
第一类：滤波器式 LIO
代表就是 FAST-LIO / FAST-LIO2。
这一路的核心特点是：
紧耦合 LiDAR 与 IMU
用迭代 EKF / IEKF 一类滤波框架
强调实时性、计算效率、前端鲁棒性
FAST-LIO 官方 README 和论文都明确说它使用 tightly-coupled iterated extended Kalman filter。FAST-LIO2 进一步强调“fast, robust, versatile”，并且支持直接将原始点注册到地图。
 第二类：优化 / 因子图式 LIO
代表是 LIO-SAM。
这一路的特点是：
用因子图 / smoothing / optimization
更容易接入回环、GPS、其他约束
更像“前端 + 后端”的完整框架
LIO-SAM 官方 README 和 Autoware 文档都把它描述为 tightly-coupled lidar inertial odometry via smoothing and mapping，并明确强调因子图。 
第三类：扩展融合式 LIO
是在 LIO 基础上继续加别的传感器或任务。比如：
LVI-SAM：LiDAR + Visual + IMU
R3LIVE：LiDAR + IMU + 相机
一些动态环境增强版，比如加入目标跟踪或强度信息
这些系统本质上仍然建立在 LIO 思路上，只是进一步融合了视觉或动态环境处理。 
所以可以这样记：
LIO：一大类方法
FAST-LIO：滤波器派、强调实时前端
LIO-SAM：优化派、强调因子图与更完整系统
LVI-SAM / R3LIVE：扩展融合派
1.1 为什么叫 FAST-LIO
因为它的设计目标就是“快”。
FAST-LIO 官方 README 直接写的是 A computationally efficient and robust LiDAR-inertial odometry package；论文里也强调它通过紧耦合 iEKF 和更高效的 Kalman gain 计算，把计算负担降下来，从而实现实时运行。FAST-LIO2 则进一步通过 直接点到地图配准 和 ikd-Tree 增量 kd-tree 提高效率与适配性。 
通俗点说，叫 FAST，主要因为它重点追求的是：
高频实时输出
更低计算量
在机器人板载算力上也能跑
跑通fast-lio需要
1.2 FAST_LIO_LC 相比 FAST_LIO_SLAM
FAST_LIO_LC 相比 FAST_LIO_SLAM 的核心优势，是“后端修正更深地反馈前端”，也就是耦合更紧。
这点两个 README 的表述很清楚：
FAST_LIO_SLAM：README 明确说它是
FAST-LIO2 + SC-PGO，而且“FAST-LIO2 and SC-PGO run separately”，SC-PGO 从 FAST-LIO2 订阅 odometry 和 lidar point cloud，最后在 SC-PGO 节点里生成优化地图。也就是一种比较典型的“前端一个模块，后端一个模块”的外挂式组合。 
FAST_LIO_LC：README 明确说它实现了 loop closure 和 pose graph optimization，并特别强调优化结果会更新到 FAST-LIO 的 pose 和 map；同时还明确写了它参考了 FAST_LIO_SLAM。 
所以 FAST_LIO_LC 相比 FAST_LIO_SLAM，优势主要有这几点：
第一，后端结果会回写前端
这是最关键的一点。
FAST_LIO_SLAM 更像“FAST-LIO2 提供前端轨迹，SC-PGO 在后面做优化并输出优化地图”；
而 FAST_LIO_LC 更强调“优化后的结果继续修正 FAST-LIO 本身的 pose 和 map”。 
这意味着，如果你更在意：
后端回环修正后，前端地图状态也被一起拉正
不是只得到一份“后处理优化结果”
而是想让整个系统内部状态更一致
那 FAST_LIO_LC 的思路更占优。 
第二，系统耦合更紧
FAST_LIO_SLAM 的优点是清晰、好理解、好拆模块：
FAST-LIO2 跑前端，SC-PGO 跑后端。 
FAST_LIO_LC 的优点则不是“更容易理解”，而是：
前后端联动更强
后端图优化不只是附加显示层
更像“闭环修正真正进入系统内部” 
第三，从工程目标上更偏“最终地图一致性”
如果你的目标是：
长轨迹建图
回环后尽量把前端累计偏差一起修回来
更看重最终地图和在线状态的一致性
那 FAST_LIO_LC 这条路线通常比 FAST_LIO_SLAM 更有吸引力。这个判断是基于其“优化结果更新回 pose 和 map”的设计做出的工程推断。 

你可以直接这样记：
FAST_LIO_SLAM 的优势：
结构清晰，FAST-LIO2 + SC-PGO 分开跑，更容易理解和替换模块。 
FAST_LIO_LC 的优势：
后端优化结果会回写前端 pose/map，前后端耦合更紧，更适合追求系统内部一致性。 
五、Cartographer
原理：
cartographer算法简介
Real-Time Correlative Scan Matching完全解析（CSM帧匹配算法）
SLAM算法工程师之路：激光点云降采样方法学习与改进应用
开源解释代码：
cartographer_detailed_comments_ws
1. 传感器数据
Input Sensor Data：传感器输入，主要包含——激光雷达数据、底盘odom数据、imu数据、
激光雷达数据：2d 扫描点云原生数据 ——> 体素滤波器（Voxel Filter） ——> 自适应体素滤波器 ——> 扫描匹配 (Scan Matching)
底盘odom数据：odom位置信息（包含 x , y , θ ）——> 姿态外推器 (PoseExtrapolator) ——> 扫描匹配
imu数据：imu数据（包含 两个方向的线加速度，角速度）——> 预处理 （ImuTracker）——> 姿态外推器 ——>扫描匹配
体素滤波器（Voxel Filter）：https://zhuanlan.zhihu.com/p/526174201
定义：体素滤波器（Voxel Filter）本质上就是一种点云降采样方法：把三维空间切成很多小立方体（voxel，体素），落在同一个小立方体里的很多激光点，不再全部保留，而是只保留一个代表点。这样做的目的，是让点云更稀疏、计算更快，同时尽量保留空间结构。 
举例：
假设雷达扫到一面墙，原来某一小块区域里有 30 个点。
如果体素大小设置为 5cm × 5cm × 5cm，那么这 30 个点如果都落进同一个体素里，滤波后就可能只留下 1 个代表点。于是这一小块墙面从“30 个点”变成“1 个点”，整张点云就会稀疏很多。
为什么它叫“体素”？
在 2D 图像里，最小单元叫 像素 pixel；
在 3D 空间里，最小立方体单元就叫 体素 voxel；
自适应体素滤波器
它也是体素滤波器，但“体素大小不是提前写死一个值”，而是会在一定范围内自动调整，目标是让滤波后的点云点数达到一个合适的数量。 Cartographer 官方文档直接说，它会在 max_length 的约束下，尝试找到一个“合适的体素尺寸”，以达到目标点数；在 3D 中还会用两套自适应体素滤波，生成高分辨率和低分辨率点云供 Local SLAM 使用。 
你先别把它想复杂。
普通体素滤波器是：
我直接规定体素边长，比如 5 cm
所有帧都按 5 cm 去降采样
而自适应体素滤波器是：
我不想死板地永远用 5 cm
我希望“滤波后大概还剩下足够多、但又不过多的点”
所以程序会自动调体素大小，找到一个更合适的值去做降采样。
为什么要“自适应”？
因为不同场景下，原始点云密度差很多：
有时点特别密，数据量很大
有时点本来就稀疏
有时近处点很多，远处点很少
有时环境简单，有时环境结构很复杂
如果你始终用一个固定体素大小，就会有两个问题：
情况 1：体素太小
降采样不够，点还是很多，后面的扫描匹配计算就重。
情况 2：体素太大
点被删得太狠，几何细节丢失，扫描匹配可能不稳。
所以 Cartographer 才加了这个“自适应”机制：
自动在“计算量”和“几何信息保留”之间找平衡。 官方调参文档里也明确说明了，自适应体素滤波相关参数会直接影响 Local SLAM / Global SLAM 的延迟与效果。
核心适应的是这几个量：
max_length：体素边长允许到多大
min_num_points：滤波后至少希望保留多少点
max_range：只考虑多远范围内的点。 
所以它的逻辑可以粗理解成：
扫描匹配 (Scan Matching)
如何理解概率栅格地图（Probability Grid Map）& 概率更新公式
Real-Time Correlative Scan Matching完全解析（CSM帧匹配算法）
2. 姿态外推器 PoseExtrapolator
PoseExtrapolator（姿态外推器） 理解成 Cartographer 前端里的一个“短时间运动预测器”。
它不是最终定位结果，也不是优化器；它的核心作用是：
Cartographer 官方调参文档也明确说：Local SLAM 会把一帧 scan 插入当前 submap，scan matching 使用的初始猜测来自 PoseExtrapolator；PoseExtrapolator 的思想是用雷达以外的传感器数据预测下一帧 scan 应该插入到 submap 的位置。
正常建图当中的顺序：
总结：
两帧点云之间的 IMU/odom 会一直被 PoseExtrapolator 接收和融合；
等第二帧点云来了，PoseExtrapolator 根据这段时间内积累的 IMU/odom 和历史 matched pose，
外推出第二帧点云时间戳对应的 initial pose；
然后这个 initial pose 才会作为 scan matching 的初值。
2.1 Scan matching和PoseExtrapolator的关系
PoseExtrapolator 在两帧点云之间利用 IMU/odom 和历史 scan matching pose 持续维护一个运动预测状态；
当新点云到来时，它输出该点云时间戳对应的 initial pose；
Scan Matching 使用这个 initial pose，把当前点云和 active submap 做匹配，优化出 corrected pose；
这个 corrected pose 代表 tracking_frame 在 local/map 坐标系下的位姿，并被反馈给 PoseExtrapolator；
如果 published_frame 是 base_link，Cartographer 再通过 TF 把 tracking_frame 位姿转换/发布成机器人 base_link 相关的 TF；
如果 tracked_pose 发布频率高于点云频率，中间的 pose 大多是 PoseExtrapolator 根据 IMU/odom 外推出来的，不是每次都经过 scan matching。
例如对于当前的整机建图：
雷达点云的帧率为10hz; imu的帧率为200hz, odom的频率为100hz，那么最后发出来的/tracker_pose的帧率如果要求小于或者等于10hz，那么这里实际上的pose是包含每帧的scan matching的修正后的pose的，如果大于10hz，那么这里实际上会有只有pose extrapolator的推测的位姿；
LiDAR 为 10Hz、IMU 为 200Hz、odom 为 100Hz 时，
scan matching 修正 pose 的频率主要受 LiDAR 帧率限制，约为 10Hz；
tracked_pose 的发布频率如果高于 10Hz，中间 pose 主要由 PoseExtrapolator 根据最近一次 scan matching pose、IMU 和 odom 外推得到；
tracking_frame 通常设置为 imu_link，是因为 Cartographer 内部姿态预测和重力方向估计以 IMU 为核心；
发布频率理论上可以超过 200Hz，但工程上通常不建议超过 IMU 频率太多。
tracked_pose 频率大于 200Hz 可以设置吗？
理论上可以设置，但通常没有意义，也不推荐
对于当前的传感器的情况来说：
如果你把 tracked_pose 发布到 400Hz、500Hz、1000Hz，那么中间那些 pose 基本都是：
用最近的 IMU / odom / 历史 pose 继续外推出来的插值/预测值；它不代表系统真的有 500Hz 的测量信息。

3. 局部建图 (Local SLAM)

4. 动作滤波器


5. 全局建图


6. 其他
6.1 对 Cartographer 来说，/map 是怎么来的
Cartographer 本体更核心的是维护 submaps。
官方文档写得很清楚：occupancy_grid_node 是监听 submap_list，再生成一个单体的 map (nav_msgs/OccupancyGrid) 发布出来。也就是说：
6.2 定义的坐标系
tracking_frame：Cartographer 内部拿来“跟踪运动”的参考坐标系
published_frame：Cartographer 对外发布位姿时，用作 child frame 的坐标系
官方文档就是这么定义的：tracking_frame 是 “the frame that is tracked by the SLAM algorithm”；published_frame 是 “the child frame for publishing poses”。如果用了 IMU，tracking_frame 应该在 IMU 的位置，常见是 imu_link；而 published_frame 如果没有别的 odom 模块，通常设成 base_link 更合适。 
第一个更偏“算法内部参考点”，第二个更偏“对外显示机器人是谁”。
所以常见配置就是：
tracking_frame = imu_link
published_frame = base_link
这俩不是同一个概念，也不一定必须设成同一个 frame。
odom 是一个world-fixed 的局部参考坐标系，理论上它自己不会“跟着机器人跑”。 
base_link 才是机器人本体坐标系，会随着机器人运动不断变化。 
map 也是 world-fixed，但它允许因为定位更新、回环闭合而发生离散跳变；odom 则要求连续、平滑、不跳。
坐标系之间的转换
```
tracking_frame = imu
```
表示 Cartographer 内部跟踪的是 IMU 这个 frame
如果 provide_odom_frame = true，内部/逻辑上就可以理解为它维护着一条
map -> odom -> tracking_frame 的关系
但它对外主发布的 TF 不是看 tracking_frame，而是看 published_frame。官方明确写的是：会提供 map_frame -> published_frame；若开启 provide_odom_frame，还会提供 odom_frame -> published_frame 的连续变换。 
所以如果你配的是：
那么含义就是：
内部跟踪：imu
对外发布：base_link
这时只有在系统里已经有 imu <-> base_link 这条固定外参 TF 的前提下，published_frame = base_link 才能正常工作。因为官方要求：所有传感器 frame 到 tracking_frame 和 published_frame 的变换都必须可用，通常由 robot_state_publisher 或 static_transform_publisher 提供。 
你可以把它理解成这两层：
第一层：内部
Cartographer 盯着 IMU 这个点在算，所以逻辑上你可以认为它知道：
或者至少它在维护“IMU 相对于地图”的连续估计。官方的 tracked_pose 话题就是“tracked frame 相对于 map frame 的 pose”。如果 tracking_frame=imu，那这个 tracked_pose 本质上就是 IMU 在 map 里的 pose。
第二层：对外
如果你要求它发布的是：
那它就必须知道：
否则它没法把“内部跟踪到的 IMU 位姿”换算成“外部要发布的 base_link 位姿”。Cartographer 不会自己替你标定这条固定外参。文档的要求是这条 TF 必须已经存在。
6.3 submap_list
是 当前所有 submap 的列表；
Cartographer ROS 文档明确写了：submap_list 包含“所有 submap 的列表，以及每个 submap 的 pose 和最新版本号，覆盖所有 trajectories”；
它的消息类型是 cartographer_ros_msgs/SubmapList； 
你可以把它理解成：
Cartographer 不会一边扫一边只维护“一张大地图”
它会把地图拆成很多个 局部小地图块
每个小地图块就是一个 submap
submap_list 就是在告诉你：

现在有哪些 submap
每个 submap 属于哪条 trajectory
它的编号是多少
它当前在 map 坐标系下的位姿是多少
它是不是更新过了
submap 本身主要属于 Cartographer 的前端 / Local SLAM 产物；
而 submap_list 这个话题，只是把当前系统里已经存在的这些 submap 及其位姿整理后发布出来。Cartographer 官方文档把整个系统分成两个相关子系统：第一个是 local SLAM（也叫 frontend / local trajectory builder），它的工作就是连续构建一系列 submaps；第二个是 global SLAM，也就是 pose graph，用来做约束、回环和全局优化。
参数设置
情况 A：你不用底盘驱动的 odom 作为 TF 主链
这时：
Cartographer 自己发布
map -> odom
odom -> base_link（连续局部结果）
你的底盘驱动如果也在发 odom -> base_link，就冲突了
也就是说，这时 TF 里的 odom 应该由 Cartographer 这一套来主导。
情况 B：底盘驱动已经在稳定发布 odom -> base_link
当前底盘的驱动，已经存在odom这个坐标系，能够稳定的发布：odom -> base_link
那么这里设置为：
这时：
底盘驱动负责 odom -> base_link；
Cartographer 负责 map -> odom；
6.4 cartographer_pbstream_to_ros_map


6.5 tracker_pose的频率设置
pose_publish_period_sec
这个参数影响下面三个：
```
/tracked_pose
/scan_matched_points2
/tf
```
当前我/tracked_pose的发布频率受限于传感器的频率吗？当前雷达点云的频率最大就是10hz，tracker_pose的频率可以比点云的频率高吗？
会受限，但不是简单地“雷达 10Hz，所以 /tracked_pose 最高 10Hz”。
在当前 localization_full_body.lua 里：
```
pose_publish_period_sec = 0.1
publish_tracked_pose = true
use_pose_extrapolator = true
```
所以 Cartographer 理论上会按 0.1s 定时发布 /tracked_pose，也就是目标 10Hz。这个发布频率不一定必须等于点云频率，因为 use_pose_extrapolator = true 时，Cartographer 可以用 IMU/odom 在两帧点云之间外推 pose。
但要分清两种频率：
scan-matched correction 频率：真正经过点云 scan matching 修正的位姿，最高通常不超过点云输入频率，也就是约 10Hz。
/tracked_pose 发布频率：可以比点云频率高，靠 IMU/odom 外推发布中间位姿；但这些中间位姿不是每次都经过新点云匹配修正。
你现在 /tracked_pose 只有 3.2Hz，说明它不是被“雷达只有 10Hz”限制住，而是 Cartographer 前端每帧处理约 300ms，把本该 10Hz 的发布链路拖慢了。换句话说：
雷达 10Hz = 理论输入上限
pose_publish_period_sec=0.1 = 理论发布目标 10Hz
scan matching 300ms/帧 = 实际只能约 3.2Hz
如果前端处理足够快，当前配置下 /tracked_pose 应该能接近 10Hz。
如果你把 pose_publish_period_sec 改成 0.02，理论上 /tracked_pose 可以发布到 50Hz，但只有外推 pose 更高频，点云修正仍然最多 10Hz，而且在当前前端卡住的情况下，改发布周期本身不会解决 3.2Hz。



七、其他部分
雷达点云运动畸变补偿

ICP：https://zhuanlan.zhihu.com/p/708794525

NDT

sensor_msgs/msg/PointCloud2的数据格式

IP地址可能会变，可以根据mac地址反推找到对应的ip：
例如：
先查本机 ARP 缓存：




你这里把 packet / frame / point 三个层级混在一起了。按从小到大讲：
7. packet 是什么？
这里的 packet 指的是 雷达通过以太网发出来的一个 UDP 数据包 / UDP data segment，不是 ROS 里看到的一帧点云。
MID-360 官方协议里写明，点云数据协议是通过 UDP 数据段封装的，点云数据从 LiDAR 发往 host computer；协议表里也有 length、timestamp、data、dot_num 等字段。dot_num 的说明是：当前 UDP packet 的 data 字段里包含的点数量。也就是说，一个 packet 只是网络传输中的一个小包。 
对 MID-360 的点云数据格式，官方协议列出的点云 data type 1/2/3 的 N 都是 96，也就是一个原始 UDP packet 里通常包含 96 个采样点。 
所以：
2. time_interval 是什么意思？
time_interval 是 这个 packet 内部的采样时间跨度。
官方协议对 time_interval 的描述是：单位是 0.1 微秒；含义是“这一段点云数据中，最后一个点的时间减去第一个点的时间”。同一页又写明：每个 packet 的 timestamp 表示该 packet 里第一个点云点的时间，packet 内有 N 个点，这 N 个点的时间是等间隔分布的，总时间间隔就是 time_interval。 
可以理解成：
注意：这个 time_interval 不是 0.1 s 那种大帧时长。它只是一个 UDP 小包内部的时间跨度，通常是几百微秒量级。

按 MID-360 规格粗算：官方点率是 200,000 points/s，典型帧率是 10 Hz。如果一个 packet 有 96 个点，那么一个 packet 大概覆盖：
更准确地说，因为 time_interval = 最后点 - 第一点，如果按 96 个点之间 95 个间隔算，就是约：
这是 packet 级别的时间，不是 0.1 s 级别的时间。MID-360 官方规格给出的点率和典型帧率分别是 200,000 points/s 和 10 Hz。 
3. “每一帧”是不是 0.1 s 之间的点云数据？
在 ROS driver / 算法里，通常是的：如果发布频率是 10 Hz，一帧就是大约 0.1 s 内积累的点云。
MID-360 官方规格写的是典型 10 Hz frame rate，所以常见理解是：
在这 0.1 s 内，按 200,000 points/s 粗算，会有：
也就是一帧大约两万个点，具体数量会因为回波、过滤、发布配置等变化。官方 driver2 的 launch 示例里 publish_freq 默认也是 10.0，这意味着 driver 默认也倾向于按 10 Hz 发布 ROS 点云消息。 

但是要注意两种“frame”：
所以你问的“0.1 s 之间的点云数据”，更接近 ROS 点云帧，不是原始通信协议里的一个 packet。
4. 一个 0.1 s 帧里有很多 packet 吗？
是的。
粗略算：
所以大概是：
这也是为什么“packet timestamp 是首点时间”不等于“整帧 ROS 点云只有一个 packet”。真实数据流更像这样：
5. 激光反射回来是按照光速计算的吗？
是，基本原理是 ToF / time-of-flight，飞行时间测距：雷达发出激光，光打到物体表面后反射回来，接收器测量发射到接收之间的往返时间，再根据光速换算距离：
除以 2 是因为光走了“去程 + 回程”。NASA 对 LiDAR 的解释也是：测量激光脉冲从发出到被地表反射回来的往返时间，并根据光速把 travel-time 转换成距离。 
不过你在 Livox packet 里一般看不到“飞行时间原始值”。MID-360 输出给你的已经是处理后的点云数据，例如 Cartesian 格式里直接给 x/y/z，单位是 mm，同时还有 reflectivity、tag 等字段。 
6. 这些点是打到物体上的点吗？
可以这么理解：一个点就是一次有效激光回波对应的三维测量结果。
也就是：
所以点云里的点不是“真实存在的小点”，而是雷达对环境表面的一次测量样本。一个墙面会被很多束激光扫到，于是点云里就出现很多落在墙面上的点。
也不是每束激光都会产生好点：太远、反射太弱、黑色/水面/玻璃/雨雾灰尘等都可能导致弱回波、噪声或低置信度。Livox 官方说明 FOV 内不是所有对象都一定能被检测到，因为雷达只能照亮扫描路径上的目标，且过远或反射太弱会导致无法识别。 
7. 包是不是一帧，也就是 0.1 s 内所有点云？
不是。
最重要的结论就是这句：
更具体地说：

点击图片可查看完整电子表格
所以 MID-360 的数据流可以画成：
8. 和“帧首/帧尾时间戳”的关系
原始 packet 级别：
driver 发布 ROS 点云帧时：
所以你之前问的“Livox 发出来的是帧首还是帧尾”，更精确地说是：
一句话总结：packet 是 UDP 小包，不是 0.1 s 整帧；time_interval 是这个小包里最后点和第一点的时间差；0.1 s 的 ROS 点云帧通常由约 200 多个 packet、约 2 万个点组成；这些点是激光照到物体表面并产生回波后计算出来的三维测量点。

| Plain Text pip3 install vbr-devkit |
| --- |


| Plain Text vbr list |
| --- |


| Plain Text vbr download colosseo_train0 /Users/psibot/workspace_haoyi/spark-fast-lio/datasets |
| --- |


| “我想把点云滤得稀一点，但不能稀到没法匹配。 只要保留下来的点数还不少于一个最低要求，我就可以适当把体素调大； 如果调太大导致点数太少，那我就把体素调小一点。”  |
| --- |


| 在下一帧雷达点云进来时，先根据 IMU、odom、上一帧 scan matching 结果，预测一个大概位姿，作为 Scan Matching 的初始值。 |
| --- |


| Plain Text 第 1 帧点云 t0   ↓ scan matching / 或初始化   ↓ 得到 pose_0   ↓ PoseExtrapolator.AddPose(t0, pose_0)  t0 ~ t1 之间：   IMU 高频到来  -> AddImuData()   odom 高频到来 -> AddOdometryData()   它们更新 PoseExtrapolator 内部状态/缓存   但通常不触发 scan matching  第 2 帧点云 t1 到来：   ↓ initial_pose = PoseExtrapolator.ExtrapolatePose(t1)   ↓ 用 initial_pose 作为初值   ↓ 当前第 2 帧点云和 active submap 做 scan matching   ↓ 得到 corrected_pose   ↓ PoseExtrapolator.AddPose(t1, corrected_pose) |
| --- |


| PoseExtrapolator：预测器 Scan Matching：修正器 |
| --- |


| Plain Text tracking_frame = "imu" published_frame = "base_link" provide_odom_frame = true odom_frame = "odom" |
| --- |


| Plain Text map -> odom -> imu |
| --- |


| Plain Text map -> odom -> base_link |
| --- |


| Plain Text imu <-> base_link |
| --- |


| Plain Text published_frame = "base_link" odom_frame = "odom" provide_odom_frame = true use_odometry = false   -- 或 true，仅作为观测输入 |
| --- |


| Plain Text published_frame = "odom" provide_odom_frame = false use_odometry = true |
| --- |


| YAML header:   stamp: ...   frame_id: "lidar"  height: 1 width: 3  fields:   - {name: "x",         offset: 0,  datatype: FLOAT32, count: 1}   - {name: "y",         offset: 4,  datatype: FLOAT32, count: 1}   - {name: "z",         offset: 8,  datatype: FLOAT32, count: 1}   - {name: "intensity", offset: 12, datatype: FLOAT32, count: 1}   - {name: "ring",      offset: 16, datatype: UINT16,  count: 1}   - {name: "time",      offset: 20, datatype: FLOAT32, count: 1}  is_bigendian: false point_step: 24 row_step: 72 data: [...] is_dense: true |
| --- |


| Plain Text arp -an | grep -i "a8:dd:9f:cc:b3:e5" |
| --- |


| Plain Text 一个点 point   ↓ 很多个点组成 一个 UDP packet，通常 96 个点左右   ↓ 很多个 UDP packet 被 driver 攒起来 一个 ROS 点云帧 / 算法点云帧，典型 10 Hz，也就是约 0.1 s |
| --- |


| Plain Text packet ≠ 0.1 s 的整帧点云 packet = 雷达连续吐出来的一个小 UDP 包，里面通常只有几十/约 96 个点 |
| --- |


| Plain Text packet.timestamp   = 这个 UDP packet 第 1 个点的时间  packet.time_interval   = 这个 UDP packet 最后 1 个点时间 - 第 1 个点时间  packet 内第 i 个点时间   ≈ packet.timestamp + i * 点间隔 |
| --- |


| Plain Text 96 / 200000 s ≈ 0.00048 s = 0.48 ms |
| --- |


| Plain Text 95 / 200000 s ≈ 0.000475 s = 475 μs |
| --- |


| Plain Text 1 帧 ≈ 1 / 10 Hz = 0.1 s |
| --- |


| Plain Text 200000 * 0.1 = 20000 个点 |
| --- |


| Plain Text 硬件协议里的 UDP packet:   小包，通常 96 个点，约 0.48 ms  ROS/SLAM 里的一帧 PointCloud:   driver 攒了很多 UDP packet 后发布出来   典型 10 Hz，也就是约 0.1 s   大约 20000 个点 |
| --- |


| Plain Text 一帧点数 ≈ 20000 点 一个 packet ≈ 96 点  一帧包含的 packet 数 ≈ 20000 / 96 ≈ 208 个 packet |
| --- |


| Plain Text 1 个 ROS 点云帧，0.1 s   ≈ 200 多个 UDP packet   ≈ 20000 个点 |
| --- |


| Plain Text packet 0: 96 点，timestamp = 第 1 点时间 packet 1: 96 点，timestamp = 下一批第 1 点时间 packet 2: 96 点，timestamp = 下一批第 1 点时间 ... 约 200 多个 packet 被 driver 攒成一个 0.1 s 的 ROS 点云帧 |
| --- |


| Plain Text 距离 ≈ 光速 × 往返时间 / 2 |
| --- |


| Plain Text 雷达朝某个方向发出/扫描激光   ↓ 激光照到墙、地面、桌子、树、人、机器人外壳等表面   ↓ 有足够强的反射光返回   ↓ 雷达根据距离 + 角度/扫描方向算出 x,y,z   ↓ 形成一个 point cloud 点 |
| --- |


| Plain Text packet 不是一帧。 packet 是 UDP 小包。 一帧 0.1 s 点云通常由很多个 packet 组成。 |
| --- |


| Plain Text 连续扫描 / 连续测距     ↓ point point point point point ...     ↓ 每 96 个左右打成一个 UDP packet     ↓ packet packet packet packet ...     ↓ driver 按 publish_freq，例如 10 Hz，攒约 0.1 s     ↓ 发布一个 ROS PointCloud2 或 Livox CustomMsg     ↓ FAST-LIO2 / Cartographer / 其他 SLAM 算法处理这一帧 |
| --- |


| Plain Text packet.timestamp = 这个 packet 第一个点的时间 packet.time_interval = 这个 packet 最后点 - 第一个点 |
| --- |


| Plain Text ROS 一帧 = 很多个 packet 拼起来 ROS header.stamp / timebase 通常 = 这一帧第一个点的时间 每个点还有自己的 offset_time / timestamp |
| --- |


| Plain Text 原始 UDP packet:   timestamp 是 packet 首点时间  driver 发布的一帧点云:   header.stamp / timebase 是该 ROS 帧首点时间  帧尾时间:   需要用 帧首时间 + 最后一个点的 offset_time 算出来 |
| --- |
