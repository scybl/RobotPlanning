# RobotPlanning

[English](README_en.md)

RobotPlanning 是一个 ROS 2 机器人规划与动力学工作空间，覆盖四元数转换、YouBot 运动学、检查点路径排序、SE(3) 插值、逆运动学轨迹、KUKA IIWA14 动力学建模和 Docker 化验证。

项目同时提供无 ROS 的快速数值 demo 和完整 ROS 2 Foxy 工作流。前者便于在普通 Python 环境中检查核心算法，后者用于 RViz、Gazebo、MoveIt 2 和 IIWA 动力学验证。

![RobotPlanning 演示预览](docs/images/robot-planning-preview.svg)

## 功能说明

| 模块 | 能力 |
| --- | --- |
| 四元数转换 | 支持 ZYX 欧拉角和 Rodrigues 向量转换 |
| YouBot 运动学 | 提供正运动学、DH 参数封装和 6x5 Jacobian 计算 |
| 路径规划 | 实现检查点排序、路径长度计算和 SE(3) 姿态插值 |
| IIWA 动力学 | 建模惯性矩阵、重力项、科氏项和被动加速度估计 |
| ROS 工作流 | 提供 YouBot RViz 演示、运动规划 launch、IIWA 验证和 Docker 构建 |

`portfolio_robotics/` 是无需 ROS 依赖的纯 NumPy 算法核心层，将运动学、动力学和路径规划与中间件解耦；因此同一套实现可以直接用于轻量 demo、数值单元测试和可复现图表生成。

## 运行过程展示

无 ROS quick demo 会直接输出核心数值结果，适合快速验证算法实现和 README 指标。

![RobotPlanning quick run](docs/images/planning-quick-run.svg)

完整工作流从 colcon 构建进入 RViz/Gazebo/MoveIt 2 演示，并通过 IIWA 动力学验证路径闭环。

![RobotPlanning ROS stack](docs/images/planning-stack-run.svg)

## 结果展示

| 项目 | 结果 |
| --- | --- |
| Quaternion pitch | `+0.7854 rad` |
| Rodrigues vector | `[+0.0000, +0.4142, +0.0000]` |
| YouBot end-effector xyz | `[-0.0378, +0.0330, +0.4490] m` |
| YouBot Jacobian | shape/rank = `(6, 5) / 5` |
| Checkpoint order | `[1, 2, 0, 3]` |
| Checkpoint path | `0.7969 m` |
| First interpolation point | `[+0.2260, -0.1380, +0.3340]` |
| IIWA inertia symmetry error | `0.00e+00` |
| IIWA gravity norm | `3.0920` |
| 支持模式 | `quick`, `docker`, `ros-build`, `iiwa-validation`, `youbot-fk`, `youbot-planning` |

下面的路径图由 `shortest_path_order` 求出检查点顺序，再由 `interpolate_transform` 对每段位姿进行 SE(3) 插值。图中的最优顺序 `[1, 2, 0, 3]`、总长度 `0.7969 m` 和 97 个插值位姿均为脚本实时计算结果。

![真实 checkpoint 路径规划与 SE(3) 插值结果](docs/images/checkpoint-planning-results.png)

YouBot 图通过 `youbot_forward_kinematics` 扫描关节 2 的 121 个角度得到末端轨迹，右侧热力图则来自 quick demo 位形处的 `youbot_jacobian` 真实矩阵（shape `(6, 5)`、rank `5`）。

![真实 YouBot 末端轨迹与 Jacobian 结果](docs/images/youbot-kinematics-results.png)

结果文件：

- `docs/results/run_quick_2026-08-09.txt`
- `docs/results/run_validation_summary_2026-08-09.md`
- `docs/results/lightweight_demo.txt`

## 快速上手

无 ROS 快速演示：

```bash
bash scripts/run_project.sh quick
```

复用已有 conda 环境：

```bash
conda run -n codex_python bash scripts/run_project.sh quick
```

重新生成真实计算图表：

```bash
python scripts/generate_visuals.py
```

Docker 验证：

```bash
bash scripts/run_project.sh docker
```

本地 ROS 2 Foxy 工作流：

```bash
bash scripts/run_project.sh ros-build
bash scripts/run_project.sh youbot-fk
bash scripts/run_project.sh youbot-planning
bash scripts/run_project.sh iiwa-validation
```

## 环境要求

- 快速演示：Python 3 + NumPy
- 图表生成：Matplotlib
- 完整 ROS 运行：Ubuntu 20.04 + ROS 2 Foxy
- 可选：Docker、RViz、Gazebo、MoveIt 2、PyKDL、xacro

## 数据说明

项目不依赖外部数据集。YouBot 与 IIWA 模型、launch、RViz 配置、rosbag 示例和数值 demo 都保存在仓库内。`docs/results/` 保留可复现运行摘要；`demos/lightweight_demo.py` 是 README 指标的主要来源。

## 目录结构

```text
portfolio_robotics/        无 ROS 算法封装
demos/                     轻量数值演示
youbot_*                   YouBot 运动学、仿真和可视化包
iiwa_*                     IIWA 动力学、Gazebo 和 MoveIt 包
robot_description/         YouBot 模型文件
scripts/                   运行、检查和构建脚本
docker/                    ROS 2 Foxy Docker 环境
docs/images/               README 预览图和运行过程图
docs/results/              quick run 和验证摘要
tests/                     结构测试与算法数值正确性测试
```

## 测试

```bash
pytest tests/ -q
```
