# Q1
## a: 证明旋转矩阵中的每一个元素小于等于1
![q1a](pic/q1_a.png)

旋转矩阵 $ \R\in\mathrm{SO}(3) $ 满足
$$
R^\top R = I.
$$

这意味着任意一列（或一行）都是**单位向量**，且列与列（行与行）**两两正交**。

记$\mathbf{R}$的第 $j$ 列为 $\mathbf{c}_j =(r_{1j},r_{2j},r_{3j})^\top$。由 $R^\top R=I$ 可知
$$
\mathbf{c}_j^\top\mathbf{c}_j= \sum_{i=1}^3 r_{ij}^2 = 1.
$$

因为三个非负数的平方和为 1，则每个平方不超过 1，从而每个元素的绝对值不超过 1：
$$
||r_{ij}|| \le 1 \quad (\forall\,i,\forall j, 0 \le i,j \le 3).
$$


## b: 证明 $R_{\mathbf{u},\theta}=R_{-\mathbf{u},-\theta}$
![b](pic/q1_b.png)

基于罗德里格斯公式，可得旋转矩阵为
$$
R(\mathbf{u},\theta) \;=\; I + \sin\theta\, [\mathbf{u}]_\times + (1-\cos\theta)\,[\mathbf{u}]_\times^2,
$$
其中，$\mathbf{u}$ 为单位向量与 $\theta$为旋转角度，$[\mathbf{u}]_\times$ 为 $\mathbf{u}$ 的反对称矩阵。


**Step 2（代入 $-\mathbf{u},-\theta$ 的恒等变换）**  

由反对称矩阵性质与三角函数可知
$$
[-\mathbf{u}]_\times = -[\mathbf{u}]_\times,\quad [-\mathbf{u}]_\times^2 = [\mathbf{u}]_\times^2,\\ \sin(-\theta)=-\sin\theta,\quad \cos(-\theta)=\cos\theta,
$$
代入$R(\mathbf{u},\theta)$可得
$$
\begin{aligned}
R(-\mathbf{u},-\theta)
&= I + \sin(-\theta)\,[-\mathbf{u}]_\times + (1-\cos(-\theta))[-\mathbf{u}]_\times^2 \\
&= I + (-\sin\theta)(- [\mathbf{u}]_\times) + (1-\cos\theta)[\mathbf{u}]_\times^2 \\
&= I + \sin\theta\, [\mathbf{u}]_\times + (1-\cos\theta)[\mathbf{u}]_\times^2 \\
&= R(\mathbf{u},\theta).
\end{aligned}
$$
得到 $R_{\mathbf{u},\theta}=R_{-\mathbf{u},-\theta}$（$\mathbf{u}$ 为单位轴）。

## c: 两坐标系 $(a,b)$ 下，矩阵 ${}^a\!R_b$ 的每一行代表什么？
![q3](pic/q1_c.png)

${}^a\!R_b$ 用于将 $b$ 系中的坐标向量换算到 $a$ 系，故存在：
$$
\mathbf{v}_a = {}^{a}\!R_b\, \mathbf{v}_b .
$$
其中, $v$为空间里同一几何向量, 使得相同向量在不同坐标系a,b下表达一致。而${}^a\!R_b$ 的三列分别表示 $b$ 系三个单位轴 $(\hat{\mathbf{x}}_b,\hat{\mathbf{y}}_b,\hat{\mathbf{z}}_b)$ 在 $a$ 系中的坐标。第 $j$ 列即 $\hat{\mathbf{e}}_{b,j}$ 在 $a$ 系下的分量。

由于
$$
({}^{a}\!R_b)^\top = {}^{b}\!R_a,
$$
且后者的列是 $a$ 轴在 $b$ 中的坐标，可知 ${}^a\!R_b$ 的第 i 行就是 $a$ 系第 $i$ 个单位轴在 $b$ 系下的坐标。

所以存在$({}^{a}\!R_b)_{ij} = \hat{e}_{a,i} \cdot \hat{e}_{b,j}$

所以${}^{a}\!R_b$表示：$b$ 的轴在 $a$ 中的坐标，而${}^{a}\!R_b$每一行表示：$a$ 的轴在 $b$ 中的坐标。

## d 旋转矩阵关系推导
![q4](pic/q1_d.png)


令$\mathbf{R} \in \mathbf{SO(3)}$,表示三维空间中的一次纯旋转，同时记旋转角为$\mathbf{\theta}$，旋转轴为$\mathbf{u} \in \mathbb{R}^3, ||u||=1$,并对旋转轴$\mathbf{u}$，存在反对称矩阵$\mathbf{[u]}_\times$

由 Rodrigues 公式可知
$$
R(\mathbf{u},\theta) \;=\; I + \sin\theta\, [\mathbf{u}]_\times + (1-\cos\theta)\,[\mathbf{u}]_\times^2,
$$

由于对矩阵方程，任意向量x存在
$$
|u|=1, \mathbf{[u]_\times^2x=u\times(u\times x)}=\mathbf{u(u^\top x)-x(u^\top u)}
$$
同时对于反对称矩阵$[\mathbf{u}]_\times$，存在以下性质

$$
[\mathbf{u}]_\times \mathbf{u} = \mathbf{u}\times \mathbf{u} = 0, [\mathbf{u}]_\times^2 = \mathbf{u}\mathbf{u}^\top-\mathbf{I}
$$

将上述公式代入Rodrigues中,两边同时乘以旋转轴$\mathbf{u}$可得
$$
\begin{aligned}
R(\mathbf{u},\theta)\mathbf{u}&= \mathbf{u} + \sin\theta\,(\mathbf{[u]_\times}\mathbf{u}) + (1-\cos\theta)\,\mathbf{u}(\mathbf{u}^\top\mathbf{u}) \\
&= \mathbf{u} + \sin\theta*\mathbf{0} + (1-\cos\theta)\,\mathbf{u} \\
&= \mathbf{u}.
\end{aligned}
$$

证明旋转轴方向在旋转后不变

对实正交矩阵 $\mathrm{SO}(3)$，谱为 $\{1,e^{i\theta},e^{-i\theta}\}$，模长为1。因此存在
$$
\operatorname{tr}(R)=\lambda_1+\lambda_2+\lambda_3=1+2\cos\theta
\quad\Rightarrow\quad
\boxed{\;\theta=\arccos\!\Big(\frac{\operatorname{tr}(R)-1}{2}\Big).}
$$

当 $\sin\theta\neq 0$（即 $\theta\notin\{0,\pi\}$）时，旋转轴可由 $R$ 的反对称部分求得：
$$
\boxed{
\mathbf{u} = \frac{1}{2\sin\theta}
\begin{bmatrix}
R_{32} - R_{23} \\[2pt]
R_{13} - R_{31} \\[2pt]
R_{21} - R_{12}
\end{bmatrix},\quad \theta \notin \{0,\pi\}.
}
$$

而当$\theta\in\{0,\pi\}$

- $\theta=0$：$R=I$，旋转轴任意（未定义）。
- $\theta=\pi$：由 $R = -I + 2\,\mathbf{u}\mathbf{u}^\top$ 可知

$$
R+I = 2\,\mathbf{u}\mathbf{u}^\top \ (\mathrm{rank}=1),
$$
因此可取 $\mathbf{u}\propto$ 任意非零列（或行）向量 $(R+I)_{:j}$ 并单位化，即得旋转轴（符号仅确定到 $\pm\mathbf{u}$）。

# Q2

## a证明
![q2a](pic/q2_a.png)
已知三维旋转矩阵为：
$$
\begin{gathered}
R_x(\alpha)=\begin{bmatrix}1&0&0\\[2pt]0&\cos\alpha&-\sin\alpha\\[2pt]0&\sin\alpha&\cos\alpha\end{bmatrix},

R_y(\beta)=\begin{bmatrix}\cos\beta&0&\sin\beta\\[2pt]0&1&0\\[2pt]-\sin\beta&0&\cos\beta\end{bmatrix},

R_z(\gamma)=\begin{bmatrix}\cos\gamma&-\sin\gamma&0\\[2pt]\sin\gamma&\cos\gamma&0\\[2pt]0&0&1\end{bmatrix}.
\end{gathered}
$$
故存在：
### Y–Z–Y（Proper Euler，外在）

外在三连乘按左乘堆叠：
$$
R_{\text{YZY}}^{\text{(extrinsic)}}(\alpha,\beta,\gamma)=R_Y(\gamma)\,R_Z(\beta)\,R_Y(\alpha).
$$
example: 当中间角 $\beta=0$ or $\pi$ 时：
$$
R=R_Y(\gamma)\,I\,R_Y(\alpha)=R_Y(\alpha+\gamma)\quad(\beta=0),
$$
或 
$$
R=R_Y(\gamma)\,R_Z(\pi)\,R_Y(\alpha)=R_Y(\gamma-\alpha)\,R_Z(\pi)
$$
本质上亦丢一自由度）。
于是 $(\alpha,\gamma)$ 的无穷多组赋值产生同一个总旋转（只与 $\alpha+\gamma$ 的和有关），自由度减少。


### X–Y–Z（Tait–Bryan，内在）

同理，以 z–y–x 为例并写出一般形式：
$$
R_{\text{xyz}}^{\text{(intrinsic)}}(\alpha,\beta,\gamma)
=R_z(\alpha)\,R_y(\beta)\,R_x(\gamma).
$$

example:取俯仰 $\beta=\frac{\pi}{2}$，得到：
$$
R=R_z(\alpha)R_y\!\bigl(\tfrac{\pi}{2}\bigr)R_x(\gamma)
=\begin{bmatrix}
0&-\sin(\alpha-\gamma)&\cos(\alpha-\gamma)\\
0& \cos(\alpha-\gamma)&\sin(\alpha-\gamma)\\
-1&0&0
\end{bmatrix}.
$$
可见结果只依赖差角 $\alpha-\gamma，\alpha$ 与 $\gamma$ 被“锁”在一起 —— 这就是 x–y–z（内在）在 $\beta=\pm\frac{\pi}{2}$ 的 gimbal lock。

**为什么在机器人手臂控制中要避免 gimbal lock**
- 自由度丢失 / 参数奇异：在锁死处，欧拉角映射对姿态的参数化非一一，姿态微调变成不可能或不稳定。
- 雅可比奇异 / 无穷关节速度：姿态误差要求的末端角速度投到关节空间时，因雅可比失去秩而需要无限大的关节速度（数值爆炸）。
- 控制不稳定 / 抖振：小姿态变化可能导致参数跳变（角度突然换支），引起控制器震荡、路径不可行。
- 规划失败：逆解多解/不可解、优化问题病态，导致跟踪精度差或无法收敛。

**工程上如何规避？**
- 不用欧拉角做内部状态（或仅作展示）：
使用单位四元数、轴角（指数映射）或直接用正交矩阵表示并在控制中闭环，避免参数化奇异。
- 奇异性鲁棒逆解：
逆运动学用阻尼最小二乘（DLS / Levenberg–Marquardt），或基于奇异值阈值的伪逆，避免在雅可比近奇异时爆炸。
- 冗余与零空间规避：
冗余机械臂在零空间加入代价函数，使关节姿态主动远离奇异面（如让 wrist pitch 远离 ±90°）。
- 路径/任务层约束：
规划时显式加入奇异规避项与关节限位、关节速度/加速度限幅；必要时切换参数 chart（多张坐标图覆盖）。
- 四元数插值：
轨迹生成用 SLERP 或双四元数插值，保证姿态过渡平滑、无跳变。


## b 从四元数到旋转矩阵（要给出步骤，不只公式）
![q2_b](pic/q2_b.png)
设四元数 
$$
q=(w,\mathbf{v}), \mathbf{v=(x,y,z)^\top, ||q||=1\Rightarrow \mathbb{w}^2+||v||^2 = 1},
$$
将三维向量$\mathbf{p} \in \mathbb{R}^3$计作四元数$p_1 = (0, \mathbf{p})$。使用四元数的共轭表示旋转可得
$$
p_2 = q\,p_1\,q^{-1},q^{-1} = \bar q = (w,-v)
$$
用四元数将$q,p_1,\bar q$展开为向量式，满足
$$
(a,\mathbf{u})(b,\mathbf{v})=(ab-\mathbf{uv},a\mathbf{v}+b\mathbf{u}+\mathbf{u\times v})
$$
可得 

$$
qp_1 = (w,\mathbf{v})(0,\mathbf{p}_1)=(-\mathbf{v}\cdot \mathbf{p_1},w\mathbf{p_1}+\mathbf{v}\times \mathbf{p_1})
$$
设$s=-\mathbf{v}\cdot\mathbf{p}, \mathbf u=w\mathbf p+\mathbf v\times\mathbf p.$ 再乘$\bar q = (w,-\mathbf{v})$可得
$$
p_2 = qp_1q^{-1} = (s,\mathbf{u})(w,-\mathbf{v}) = (sw+\mathbf{u\cdot v},-s\mathbf{v}+w\mathbf{u}-\mathbf{u\times v})
$$
由于$p_2$的标量部分，由于叉乘向量与参与叉乘的两个向量都正交，可得:
$$
sw+\mathbf u\!\cdot\!\mathbf v
=(-\mathbf v\!\cdot\!\mathbf p)w+\big(w\mathbf p+\mathbf v\times\mathbf p\big)\!\cdot\!\mathbf v
=-w\,\mathbf v\!\cdot\!\mathbf p+w\,\mathbf p\!\cdot\!\mathbf v+0=0.
$$
对$p_2$向量部分,可得
$$
-s\,\mathbf v+w\mathbf u-\mathbf u\times\mathbf v \\
=(\mathbf v\!\cdot\!\mathbf p)\mathbf v+w^2\mathbf p+2w(\mathbf v\times\mathbf p)-\big(\|\mathbf v\|^2\mathbf p-(\mathbf v\!\cdot\!\mathbf p)\mathbf v\big)\\
=(w^2-\|\mathbf v\|^2)\mathbf p+2(\mathbf v\!\cdot\!\mathbf p)\mathbf v+2w(\mathbf v\times\mathbf p)
$$

令 $\mathbf v=(q_x,q_y,q_z),\ w=q_w，$, 则记叉乘矩阵为
$$
[\mathbf v]_\times=\begin{bmatrix}
0&-q_z&q_y\\ q_z&0&-q_x\\ -q_y&q_x&0
\end{bmatrix}, [\mathbf v]_\times\mathbf p=\mathbf v\times\mathbf p,
$$
代入$[\mathbf v]_\times^2=\mathbf v\mathbf v^\top-(\mathbf v^\top\mathbf v)I$求的旋转矩阵$R$为
$$
R=(w^2-\mathbf v^\top\mathbf v)\,I+2\,\mathbf v\mathbf v^\top+2w[\mathbf v]_\times,\\
\boxed{R=I+2w[\mathbf v]\times+2[\mathbf v]_\times^2},xw
$$

把上式逐项展开，得到显式矩阵：
$$
\boxed{
R(q)=
\begin{bmatrix}
1-2(q_y^2+q_z^2) & 2(q_x q_y - q_z q_w) & 2(q_x q_z + q_y q_w)\\[2pt]
2(q_x q_y + q_z q_w) & 1-2(q_x^2+q_z^2) & 2(q_y q_z - q_x q_w)\\[2pt]
2(q_x q_z - q_y q_w) & 2(q_y q_z + q_x q_w) & 1-2(q_x^2+q_y^2)
\end{bmatrix}}
$$

小结：先用 $p_2=q\,p_1\,q^{-1}$ 展开式 → 用向量恒等式整理成线性算子 → 展开成条目式矩阵。

## c 四种应用场景下建议的旋转表示（按课件对比表给出理由）
![q2_c](pic/q2_c.png)


### 情况1:超小存储的纳米机器人
→ 轴—角（Axis–angle）：只要 3 个参数，无 gimbal lock；代价是有 $0/2\pi$ 不连续（可通过小角度增量与归一化缓解）。 ￼
### 情况2:极其受限的计算能力
→ 旋转矩阵：对向量做旋转是线性运算（矩阵–向量乘），避免三角函数；内存虽 9 参数，但 CPU 代价最低、实现最直接。 ￼
### 情况3:iPhone 导航系统
→ 四元数（内部状态）+ Euler（仅用于 UI 显示）：四元数无奇异/无不连续、数值稳定、易做滤波和插值；显示给用户时再转成偏航/俯仰/横滚角。 ￼
### 情况4:6-自由度机械臂
→ 链式位姿用旋转矩阵（或齐次变换）表示，控制/估计中的姿态误差常用四元数或 $R_d^\top R$ 的李代数误差；避免 Euler 以规避 gimbal lock。 

# Q3
## a: 证明 $q$ 与 $-q$ 等价
![q3a](pic/q3_a.png)

轴角 $(\mathbf u,\theta)$ 到四元数的式子：
$$
q \;=\; e^{\frac{\theta}{2}(u_x\mathbf i+u_y\mathbf j+u_z\mathbf k)}
= \cos(\frac{\theta}{2})\;+\;(u_x\mathbf i+u_y\mathbf j+u_z\mathbf k)\,\sin(\frac{\theta}{2}),
$$
且为单位四元数。 

当 $\theta = \theta+2\pi$代入得到：
$$
q’ = \cos\!\Big(\frac{\theta}{2}+\pi\Big)+\mathbf u\,\sin\!\Big(\frac{\theta}{2}+\pi\Big)
= -\cos\!\frac{\theta}{2}-\mathbf u\sin\!\frac{\theta}{2}=-q.
$$
而 $(\mathbf u,\theta)$ 与 $(\mathbf u,\theta+2\pi)$ 表示同一几何旋转，所以 $q$ 与 $-q$ 表示同一旋转。

也可用“四元数共轭旋转向量”的公式：
$$
\mathbf p’ \;=\; q\,\mathbf p\,q^{-1}.
$$
若把 $q$ 换成 $-q$：
$$
(-q)\,\mathbf p\,(-q)^{-1}=(-1)\,q\,\mathbf p\,(-1)\,q^{-1}=q\,\mathbf p\,q^{-1},
$$
因为 $(-q)^{-1}=-\,q^{-1}$，标量 -1 与一切四元数可交换。故两者产生完全相同的旋转。 ￼

## b:何时两个三维旋转矩阵可交换？
![q3b](pic/q3_b.png)

设$\mathbf{R_a,R_b} \in \mathbf{SO(3)}$为任意两旋转矩阵，$\mathbf{R_aR_b}=\mathbf{R_bR_a}$


把两个旋转分别写成单位四元数 $q_a=(w_a,\mathbf v_a), q_b=(w_b,\mathbf v_b)$，其中
$$
w=\cos\!\frac{\theta}{2},\quad \mathbf v=\mathbf u\,\sin\!\frac{\theta}{2}.
$$
将轴角转换为四元数,连续施加两次旋转对应“四元数相乘”：
$$
q_1q_2=\Big(w_1w_2-\mathbf v_1\!\cdot\!\mathbf v_2,\;\; w_1\mathbf v_2+w_2\mathbf v_1+\mathbf v_1\times\mathbf v_2\Big).
$$
并且“四元数乘法对应依次旋转”。由于Question3-a已证明$R(q)=R(-q)$代入得到：
$$
R_aR_b=R_bR_a \;\Longleftrightarrow\; R(q_aq_b)=R(q_bq_a)
\;\Longleftrightarrow\; q_aq_b=\pm\,q_bq_a,
$$
分两种情形求解：

- $q_aq_b=q_bq_a$ 

  比较向量部可得 $\mathbf v_a\times\mathbf v_b=0$。于是 $\mathbf v_a$ 与 $\mathbf v_b$ 共线，也就是两轴平行/反平行（同一几何轴），或其中一个 $\sin(\theta/2)=0$（恒等旋转）。可得到：同轴的任意两旋转（含恒等）都可交换。 ￼

- $q_aq_b=-\,q_bq_a$

  把上式的标量部与向量部分别相等，并化简得到
  $$
  \begin{cases}
  w_aw_b=\mathbf v_a\!\cdot\!\mathbf v_b,\\[4pt]
  w_a\mathbf v_b+w_b\mathbf v_a=\mathbf 0.
  \end{cases}
  $$
  代入 $w=\cos\frac{\theta}{2},\ \mathbf v=\mathbf u\sin\frac{\theta}{2}，$
  对第二式分别与 $\mathbf u_a,\mathbf u_b $点乘，可推出要么有恒等旋转，要么
  $\cos\frac{\theta_a}{2}=\cos\frac{\theta_b}{2}=0\Rightarrow \theta_a=\theta_b=\pi$。
  再由第一式得到 $\mathbf u_a\!\cdot\!\mathbf u_b=0$。因此出现的非常情形为：两者都是 $180^\circ$ 旋转，且两轴互相正交。 ￼

总 结
三维旋转矩阵 $R_a,R_b$ 可交换，当且仅当满足以下之一：

1. 绕同一条轴的任意角度（包括恒等）；
2. 二者皆为 $180^\circ$ 且两轴正交。

补充：一般情况下旋转不交换（教材也专门给了反例说明“次序会改变结果”）。 ￼

# Q4
## a:把四元数转成 Z-Y-X（Tait-Bryan）欧拉角
![q4a](pic/q4_a.png)
根据题意完成代码即可

## b:
![q4b](pic/q4_b.png)
在任务a中，已经完成了有关cw1q4_interface中关于.srv文件的定义。任务b要求通过ROS2实现一个服务器节点，用于将输入的四元数转换为Z-Y-X（Tait-Bryan）的欧拉较表示。应通过服务传入一个四元数，响应返回三个欧拉角值，单位为弧度。


## c:
![q4c](pic/q4_c.png)

# Q5
## a