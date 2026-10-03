# 示例 01：一维有限深方势阱（深势阱）

> **难度**：本科高年级 / 考研
> **知识点**：分段势定态、宇称守恒、超越方程与图形解、束缚态计数、深势阱极限
> **演示了 skill 的哪些环节**：题型判定（`problem-types.md` 第 2 节）→ 宇称分类 → 无量纲化 → 图形解 → 数值核验（`scripts/qm.py`）→ 出图 → 深势阱极限与修正
> **可复现**：`python examples/01-finite-square-well-check.py`（生成本文两张插图与能级表）

---

## 题目

质量 $m$ 的粒子在一维方势阱中运动，阱深 $V_0>0$、半宽 $a$：

$$V(x)=\begin{cases}0,&|x|<a\\ V_0,&|x|>a\end{cases}$$

求：

1. 束缚态（$0<E<V_0$）的能级方程与波函数；
2. 束缚态的个数；
3. 深势阱极限 $V_0\to\infty$ 下能级与无限深方阱的关系，以及有限深度带来的修正。

---

## 解答

**符号与约定**：$\hbar$ 保留符号；阱底取作能量零点；$k=\dfrac{\sqrt{2mE}}{\hbar}$ 为阱内波数，$\kappa=\dfrac{\sqrt{2m(V_0-E)}}{\hbar}$ 为阱外衰减常数；无量纲量 $\xi=ka,\ \eta=\kappa a,\ R=\dfrac{a\sqrt{2mV_0}}{\hbar}$。

**题型**：一维定态分段势。**关键在**：$V$ 是偶函数 → 宇称是好量子数 → 四处匹配条件劈成"偶、奇"两套、各只剩一个条件，全部信息压缩成一条超越方程加一个圆弧条件。

### 第 1 步：分区写方程，说明阱外只有衰减解

阱内薛定谔方程给出 $\psi''=-k^{2}\psi$，阱外给出 $\psi''=+\kappa^{2}\psi$（因 $E<V_0$，此处 $\kappa$ 为实数）。

**为什么阱外只能取衰减支**：$E<V_0$ 时阱外是经典禁区，解是实指数 $e^{\pm\kappa|x|}$，只有 $e^{-\kappa|x|}$ 在 $|x|\to\infty$ 时可归一化。这正是"束缚态"的定义性条件，也是 $\kappa$ 必须取正的来源。

### 第 2 步：用宇称把问题劈成偶、奇两类

$V(-x)=V(x)$ 给出 $[\hat P,\hat H]=0$，故可取宇称本征态；一维对称势的束缚态非简并，必为偶或奇。于是只解 $x>0$ 半区，$x<0$ 由宇称补全——偶态：

$$\psi(x)=\begin{cases}A\cos kx,&|x|<a\\ Be^{-\kappa|x|},&|x|>a\end{cases}$$

奇态：

$$\psi(x)=\begin{cases}A\sin kx,&|x|<a\\ \mathrm{sgn}(x)\,Be^{-\kappa|x|},&|x|>a\end{cases}$$

原点条件由宇称自动满足：偶态 $\psi'(0)=0$，奇态 $\psi(0)=0$。

### 第 3 步：在 $x=a$ 处匹配 $\psi$ 与 $\psi'$，相除消去系数

**偶态**：由 $A\cos ka=Be^{-\kappa a}$ 与 $-kA\sin ka=-\kappa Be^{-\kappa a}$ 两式相除得

$$k\tan ka=\kappa$$

**奇态**：由 $A\sin ka=Be^{-\kappa a}$ 与 $kA\cos ka=-\kappa Be^{-\kappa a}$ 两式相除得

$$-k\cot ka=\kappa$$

**为什么可以相除**：$\psi$ 与 $\psi'$ 在 $|x|=a$ 连续给出两个方程，含 $A,B,E$ 三个未知量；相除恰好消掉 $A,B$，留下只含 $E$ 的量子化条件。注意奇态那个**负号**，它来自外侧导数的方向，是最常丢的地方。

### 第 4 步：无量纲化，得到"曲线 + 圆弧"

记 $\xi=ka,\ \eta=\kappa a$，则约束条件与两个量子化条件分别是

$$\xi^{2}+\eta^{2}=R^{2},\qquad R\equiv\frac{a\sqrt{2mV_0}}{\hbar}$$

$$\text{偶}:\ \eta=\xi\tan\xi,\qquad \text{奇}:\ \eta=-\xi\cot\xi$$

**为什么可以把两者画在同一张 $\xi$-$\eta$ 图上**：所有束缚态都是"这两支曲线与半径 $R$ 的圆弧的交点"，而 $R$ 只由 $V_0,a,m$ 决定。于是"有几个束缚态""能级在哪里"变成纯几何问题。

### 第 5 步：图形解得到束缚态个数

- **偶**解落在 $\xi\in(n\pi,\ n\pi+\tfrac{\pi}{2})$，$n=0,1,2,\dots$
- **奇**解落在 $\xi\in(n\pi+\tfrac{\pi}{2},\ (n+1)\pi)$
- 在每个区间 $\left(\tfrac{m\pi}{2},\tfrac{(m+1)\pi}{2}\right)$ 内，曲线从左端的 $0$ 单调升到右端的 $+\infty$，圆弧单调下降，故**至多一个交点**，且

$$\left(\text{该区间有解}\right)\iff R>\frac{m\pi}{2}$$

因此束缚态总数为

$$N=\#\left\{m\ge0:\ R>\frac{m\pi}{2}\right\}=\left\lceil\frac{2R}{\pi}\right\rceil=\left\lceil\frac{2a}{\pi\hbar}\sqrt{2mV_0}\right\rceil$$

其中偶态 $N_e=\lceil R/\pi\rceil$ 个，奇态 $N_o=\lceil R/\pi-\tfrac12\rceil$ 个（$R\le\pi/2$ 时为 $0$）。

**物理结论**：$N\ge1$ 恒成立——**任意浅的一维对称势阱都至少有一个束缚态**。这是维度效应，三维势阱太浅就绑不住粒子。

### 第 6 步：能级与波函数

数值求出第 $n$ 个根 $\xi_n$（按 $\xi$ 从小到大编号）后

$$E_n=\frac{\hbar^{2}\xi_n^{2}}{2ma^{2}},\qquad k_n=\frac{\xi_n}{a},\qquad \kappa_n=\frac{\sqrt{R^{2}-\xi_n^{2}}}{a}$$

波函数在阱内是 $\cos k_nx$（偶）或 $\sin k_nx$（奇），阱外按宇称接指数尾；归一化常数由下式定出：

$$A_n^{-2}=a+\frac{\sin 2k_na}{2k_n}+\frac{\cos^{2}k_na}{\kappa_n}\ \ (\text{偶}),\qquad A_n^{-2}=a-\frac{\sin 2k_na}{2k_n}+\frac{\sin^{2}k_na}{\kappa_n}\ \ (\text{奇})$$

**物理解读**：阱外不是零，而是衰减长度 $1/\kappa_n$ 的指数尾。能级越高 $\kappa_n$ 越小、尾巴越长，越"漏"出阱外。

### 第 7 步：深势阱极限 $R\gg1$

$R\gg1$ 时圆弧半径很大，所有交点趋向各自区间的**右端点** $\xi\to\frac{(m+1)\pi}{2}$；偶奇两支合并即 $\xi_n\to\frac{n\pi}{2}$，于是

$$E_n\to\frac{n^{2}\pi^{2}\hbar^{2}}{8ma^{2}}=\frac{n^{2}\pi^{2}\hbar^{2}}{2m(2a)^{2}}$$

正是**宽度 $L=2a$ 的无限深方阱**能级。定量修正（以基态为例）：令 $\xi=\tfrac{\pi}{2}-\varepsilon$，由 $\tan\xi=\cot\varepsilon\simeq\frac1\varepsilon-\frac\varepsilon3$ 得 $\eta=\xi\tan\xi\simeq\frac{\pi}{2\varepsilon}-1$，又 $\eta\simeq R$，故 $\varepsilon\simeq\frac{\pi}{2(R+1)}$，即

$$E_1\simeq E_1^{\infty}\left(\frac{R}{R+1}\right)^{2}=E_1^{\infty}\left(1-\frac{2}{R}+\frac{3}{R^{2}}-\cdots\right)$$

**这里必须讲清一点**：能级修正是**幂律** $\sim2/R\propto1/\sqrt{V_0}$，**不是**指数小量；指数小的只是阱外波函数幅度 $\sim e^{-\kappa a}$。二者不矛盾，却常被混为一谈。等价图像是"有效宽度" $2a+2/\kappa$ 的方阱：

$$E_n\approx\frac{n^{2}\pi^{2}\hbar^{2}}{2m\left(2a+2/\kappa\right)^{2}}=E_n^{\infty}\left(\frac{R}{R+1}\right)^{2}$$

适用于 $\kappa a\gg1$ 的深束缚能级；最上面那个刚露出头的能级（$\kappa a\sim1$）修正最大。

### 第 8 步：数值例（GaAs/AlGaAs 量子阱）

取 $m^{*}=0.067\,m_e$、$2a=10\ \mathrm{nm}$、$V_0=2\ \mathrm{eV}$，得 $R=9.3769$，$N=\lceil2R/\pi\rceil=6$（偶 $3$ + 奇 $3$）：

| $n$ | 宇称 | $\xi_n=ka$ | $E_n\ (\mathrm{eV})$ | $E_n^{\infty}\ (\mathrm{eV})$ | $E_n/E_n^{\infty}$ | 阱外衰减长度 $a/\eta$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 偶 | 1.418895 | 0.045794 | 0.056124 | 0.816 | 0.108 $a$ |
| 2 | 奇 | 2.834504 | 0.182752 | 0.224496 | 0.814 | 0.112 $a$ |
| 3 | 偶 | 4.242848 | 0.409471 | 0.505115 | 0.811 | 0.120 $a$ |
| 4 | 奇 | 5.638093 | 0.723057 | 0.897982 | 0.805 | 0.134 $a$ |
| 5 | 偶 | 7.009631 | 1.117631 | 1.403098 | 0.797 | 0.161 $a$ |
| 6 | 奇 | 8.330843 | 1.578651 | 2.020461 | 0.781 | 0.232 $a$ |

$R=9.38$ 只算中等深，能级修正约 $20\%$；但精细式 $E_1^{\infty}[R/(R+1)]^{2}$ 与数值解只差 $0.07\%$。

**一个漂亮对照**：$V_0$ 以下的无限深阱能级有 $5$ 个，而有限深阱有 $6$ 个束缚态——**恒多一个**，因为 $\lceil2R/\pi\rceil=\lfloor2R/\pi\rfloor+1$。

![图形解与阱外指数尾](<01-finite-square-well-graph.png>)

![有限深阱能级向无限深阱能级靠拢](<01-finite-square-well-levels.png>)

---

## 核验（按 `references/verification.md` 清单）

- **量纲**：$\xi,\eta,R$ 均无量纲（$a\sqrt{2mV_0}/\hbar$ 是长度乘动量再除 $\hbar$）；$E=\hbar^{2}\xi^{2}/2ma^{2}$ 为能量 ✓
- **边界与连续**：解按构造在 $x=\pm a$ 连续可导；数值根满足 $\xi^{2}+\eta^{2}-R^{2}$ 的残差 $\sim10^{-13}$ ✓
- **极限一（$V_0\to\infty$，$R\to\infty$）**：$E_n\to n^{2}\pi^{2}\hbar^{2}/8ma^{2}$，回到宽度 $2a$ 的无限深方阱 ✓
- **特例核对**：深势阱极限的零级态就是无限深方阱基态 $\cos\frac{\pi x}{2a}$（$|x|<a$）。用 `scripts/qm.py expect "cos(pi*x/(2a))" -v x -a -a -b a` 核验得 $N=1/\sqrt a$、$\langle p^{2}\rangle=\pi^{2}\hbar^{2}/4a^{2}$，于是 $E=\pi^{2}\hbar^{2}/8ma^{2}=E_1^{\infty}$ 精确一致；且 $\Delta x\,\Delta p/\hbar=\sqrt{3\pi^{2}-18}/3\approx0.5679\ge\tfrac12$ ✓（与 $[0,L]$ 上 $\sin\frac{\pi x}{L}$ 的结果完全相同，正是平移等价性的体现）
- **极限二（$V_0\to0$，$R\to0$）**：$N=\lceil2R/\pi\rceil=1$，唯一束缚态能量 $\to0^{-}$ ✓
- **计数公式 vs 枚举**：公式 $N=6$，逐区间数值求根也正好 $6$ 个 ✓
- **解析修正 vs 数值**：$E_1\approx E_1^{\infty}[R/(R+1)]^{2}$ 偏差 $7.4\times10^{-4}$ ✓

> **答案：** 能级方程（$k=\frac{\sqrt{2mE}}{\hbar}$，$\kappa=\frac{\sqrt{2m(V_0-E)}}{\hbar}$）为偶宇称 $k\tan ka=\kappa$、奇宇称 $-k\cot ka=\kappa$；无量纲形式 $\xi\tan\xi=\eta$ 与 $-\xi\cot\xi=\eta$，约束 $\xi^{2}+\eta^{2}=R^{2}$（$R=\frac{a\sqrt{2mV_0}}{\hbar}$）；能级 $E_n=\frac{\hbar^{2}\xi_n^{2}}{2ma^{2}}$；束缚态个数 $N=\left\lceil\frac{2R}{\pi}\right\rceil=\left\lceil\frac{2a}{\pi\hbar}\sqrt{2mV_0}\right\rceil\ge1$（偶 $\lceil R/\pi\rceil$ 个、奇 $\lceil R/\pi-\frac12\rceil$ 个）；深势阱极限 $E_n\to\frac{n^{2}\pi^{2}\hbar^{2}}{8ma^{2}}$，修正 $E_n\approx E_n^{\infty}\left(\frac{R}{R+1}\right)^{2}$。

---

## 易错点

1. 不做奇偶分类、四个匹配条件硬解 → 极易漏解或搞错符号，尤其奇态的 $-k\cot ka=\kappa$。
2. 把"$V_0$ 以下的无限深阱能级数"当成有限深阱的束缚态数 → 实际**恒多一个**。
3. 以为深势阱的能级修正是 $e^{-\kappa a}$ 级的指数小量 → 那是阱外波函数幅度；能级修正是 $\sim1/\sqrt{V_0}$ 的幂律。
4. 用无限深阱波函数去算有限深阱的性质（它在阱外恒为零，会漏掉穿透效应）。

## 变式

- **非对称有限深阱**：无确定宇称，须分别解两个独立的超越方程，且不再保证至少一个束缚态。
- **双 $\delta$ 势 / 双阱**：能级劈裂 $\leftrightarrow$ 隧穿。
- **$\delta$ 势阱** $V=-\lambda\delta(x)$：唯一束缚态 $E=-m\lambda^{2}/2\hbar^{2}$，是"有限深阱取零宽极限"的对照。
- **三维/球形方势阱**：需要 $l=0$ 时与一维相同的超越方程，但**存在最小深度阈值**——与一维"任意浅都有束缚态"形成对照，是很好的概念题。

## 复现

```bash
python examples/01-finite-square-well-check.py
```

脚本会用 `scripts/qmenv.py` 自动切换到装有 sympy/matplotlib 的解释器，重新解超越方程、打印能级表，并把两张插图写回本目录。
