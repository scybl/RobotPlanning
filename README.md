# RobotPlanning

[English](README_en.md)

RobotPlanning 是一个 ROS 2 机器人规划与动力学工作空间，包含 YouBot 运动学、路径规划、逆运动学轨迹和 KUKA IIWA14 动力学验证。

![RobotPlanning 演示预览](docs/images/robot-planning-preview.svg)

## 功能说明

- 提供四元数转换、YouBot 正运动学和雅可比矩阵计算。
- 实现检查点路径排序、SE(3) 插值和逆运动学轨迹生成。
- 包含 IIWA14 动力学建模、加速度分析和验证脚本。
- 支持无 ROS 快速数值演示、Docker 构建和本地 ROS 运行。

## 结果展示

| 项目 | 结果 |
| --- | --- |
| YouBot Jacobian | shape/rank = `(6, 5) / 5` |
| Checkpoint path | 0.7969 m |
| IIWA inertia symmetry error | 0.00e+00 |
| 支持模式 | quick / docker / ros-build |

## 快速上手

无 ROS 快速演示：

```bash
bash scripts/run_project.sh quick
```

复用已有 conda 环境：

```bash
conda run -n codex_python bash scripts/run_project.sh quick
```

Docker 验证：

```bash
bash scripts/run_project.sh docker
```

## 环境要求

- 快速演示：Python 3 + NumPy
- 完整 ROS 运行：Ubuntu 20.04 + ROS 2 Foxy
- 可选：Docker、RViz、Gazebo、MoveIt 2

## 数据说明

项目不依赖外部数据集。`docs/results/` 保留了示例运行日志，`docs/reports/` 保留了参考报告。

## 目录结构

```text
portfolio_robotics/        无 ROS 算法封装
demos/                     轻量数值演示
youbot_*                   YouBot 运动学、仿真和可视化包
iiwa_*                     IIWA 动力学、Gazebo 和 MoveIt 包
robot_description/         YouBot 模型文件
scripts/                   运行、检查和构建脚本
docker/                    ROS 2 Foxy Docker 环境
docs/                      结果和报告
```

## 测试

```bash
pytest tests/ -q
```
