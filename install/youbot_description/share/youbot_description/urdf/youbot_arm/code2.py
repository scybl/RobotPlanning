#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import numpy as np
import sys
from pathlib import Path

M_PI = np.pi


def eval_token(tok: str) -> float:
    """把 '0' / '0.024' / '${170 * M_PI / 180}' 变成 float."""
    tok = tok.strip()
    if tok.startswith("${") and tok.endswith("}"):
        expr = tok[2:-1]
        # 只给它 M_PI 常量，防止乱 eval
        return float(eval(expr, {"__builtins__": {}}, {"M_PI": M_PI}))
    return float(tok)


def parse_vector3(s: str):
    """
    安全解析 xyz/rpy="0 0 ${170 * M_PI / 180}" 这样的 xacro 表达式。
    规则：把 ${ ... } 中的内容当成一个 token。
    """
    s = s.strip()
    result = []
    current = ""
    inside_expr = False
    i = 0

    while i < len(s):
        ch = s[i]

        # 发现 ${ —— 开始进入表达式
        if not inside_expr and ch == '$' and i + 1 < len(s) and s[i+1] == '{':
            inside_expr = True
            current += "${"
            i += 2
            continue

        # 发现 } —— 结束表达式
        if inside_expr and ch == '}':
            inside_expr = False
            current += "}"
            result.append(current.strip())
            current = ""
            i += 1
            continue

        # token 分割（不在表达式里）
        if not inside_expr and ch.isspace():
            if current.strip():
                result.append(current.strip())
                current = ""
            i += 1
            continue

        # 普通字符
        current += ch
        i += 1

    # append 最后一个 token
    if current.strip():
        result.append(current.strip())

    if len(result) != 3:
        raise ValueError(f"Expect 3 components, got tokens: {result}")

    return [eval_token(tok) for tok in result]



def extract_joints_from_xacro(xacro_path: str):
    """
    只解析你发的这个 xacro 中 1~5 号关节：
    ${name}_joint_1 ... ${name}_joint_5
    返回按 1..5 顺序排好的 joint 列表。
    """
    tree = ET.parse(xacro_path)
    root = tree.getroot()

    joints = []
    for j in root.findall(".//joint"):
        name = j.get("name", "")
        if "_joint_" in name:
            # 形如 ${name}_joint_3
            idx_str = name.split("_joint_")[-1]
            try:
                idx = int(idx_str)
            except ValueError:
                continue
            if 1 <= idx <= 5:
                joints.append((idx, j))

    # 按 joint 编号排序
    joints.sort(key=lambda x: x[0])
    return [j for _, j in joints]


def extract_dh_offset_polarity(xacro_path: str):
    joints = extract_joints_from_xacro(xacro_path)

    a_list = []
    d_list = []
    offsets = []
    polarities = []

    for j in joints:
        origin = j.find("origin")
        axis   = j.find("axis")

        if origin is None or axis is None:
            raise RuntimeError(f"Joint {j.get('name')} missing origin or axis")

        xyz_str = origin.get("xyz", "0 0 0")
        rpy_str = origin.get("rpy", "0 0 0")

        xyz = parse_vector3(xyz_str)
        rpy = parse_vector3(rpy_str)
        axis_vec = parse_vector3(axis.get("xyz", "0 0 1"))

        # ---- a, d 的提取：对 youBot 来说就是 x, z ----
        a_i = xyz[0]
        d_i = xyz[2]
        a_list.append(a_i)
        d_list.append(d_i)

        # ---- 偏置 offset：rpy 中沿着关节轴的那个分量 ----
        ax = np.array(axis_vec, dtype=float)
        main_idx = int(np.argmax(np.abs(ax)))  # 0:x, 1:y, 2:z

        if main_idx == 0:
            off = rpy[0]
        elif main_idx == 1:
            off = rpy[1]
        else:
            off = rpy[2]

        offsets.append(off)

        # ---- 读数极性：沿主轴分量的符号 ----
        pol = np.sign(ax[main_idx])
        if pol == 0:
            pol = 1.0
        polarities.append(int(pol))

    # youBot 的 alpha / 基础 theta（这部分 URDF 里并不唯一，
    # 下面是课程/官方给定的一套标准 DH）
    alpha = [M_PI/2, 0.0, 0.0, -M_PI/2, 0.0]
    theta_base = [0.0, M_PI/2, 0.0, -M_PI/2, 0.0]

    dh = {
        "a":     a_list,
        "alpha": alpha,
        "d":     d_list,
        "theta": theta_base,
    }

    return dh, offsets, polarities


def main():
    if len(sys.argv) != 2:
        print("用法: python3 extract_youbot_dh_from_xacro.py youbot_arm.urdf.xacro")
        sys.exit(1)

    xacro_path = sys.argv[1]
    if not Path(xacro_path).is_file():
        print(f"文件不存在: {xacro_path}")
        sys.exit(1)

    dh, offsets, polarities = extract_dh_offset_polarity(xacro_path)

    print("=== DH parameters (from xacro) ===")
    print("a     =", dh["a"])
    print("alpha =", dh["alpha"])
    print("d     =", dh["d"])
    print("theta =", dh["theta"])
    print()
    print("=== joint offsets (rad) ===")
    print(offsets)
    print("=== joint offsets (deg) ===")
    print([o * 180.0 / M_PI for o in offsets])
    print()
    print("=== joint reading polarity ===")
    print(polarities)


if __name__ == "__main__":
    main()

