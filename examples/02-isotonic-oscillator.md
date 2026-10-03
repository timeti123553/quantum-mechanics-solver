# 示例 02：一维奇异谐振子（isotonic oscillator）

> **难度**：本科高年级 / 考研
> **知识点**：奇异势（$1/x^2$ 双重极点）、指标方程、渐近分析、合流超几何方程与多项式截断、等间距能级、无穷高壁垒导致的二重简并
> **演示了 skill 的哪些环节**：题型判定（`references/problem-types.md` 第 2 节 奇异势）→ 指标方程定正则解 → 渐近代换 → 化为合流超几何方程 → 多项式截断给能级 → 归一化 → **三项独立核验**（直接有限差分 / sympy 精确残差 / 归一化数值积分）→ 极限核验（深势阱、浅势阱）
> **可复现**：`python examples/02-isotonic-oscillator-check.py`（生成本文两张插图与核验数据）

---

## 题目

**1.10** 粒子在一维势场 $V(x)=V_0\left(\dfrac{a}{x}-\dfrac{x}{a}\right)^{2}$ 中运动，其中 $V_0,\,a$ 是正的常数。求定态能量和波函数。

---

## 解答

**符号与约定**：$m$ 为粒子质量，$V_0>0$、$a>0$；$\hbar$ 保留符号。势在 $x=0$ 处是 $1/x^2$ 型无穷高壁垒，故 $x>0$ 与 $x<0$ 两支互不相通——下文先解 $x>0$ 支，第 8 步说明整条直线上的简并。

**题型**：一维定态 + 奇异势。**关键在**：势在原点有双重极点，必须先用指标方程定出正则解 $\psi\sim x^{\alpha}$，再用高斯型渐近解把方程化为合流超几何方程，由多项式截断读出能级。

### 第 1 步：把势改写成"抛物线 + 反平方壁 − 常数"

展开平方：

$$V(x)=\frac{V_0}{a^{2}}x^{2}+\frac{V_0a^{2}}{x^{2}}-2V_0$$

三部分各司其职：$x^{2}$ 项是谐振子势，$1/x^{2}$ 项是原点处的排斥壁（它把 $x=0$ 变成不可穿越的边界），$-2V_0$ 只是能量零点平移。**这一步不能省**：不展开就看不出它与"奇异谐振子"的关系。

### 第 2 步：定标，引入标度参数

令 $\frac12m\omega^{2}=V_0/a^{2}$，即

$$\omega=\sqrt{\frac{2V_0}{ma^{2}}}$$

把 $1/x^{2}$ 项写成规范形式，并定义无量纲常数 $\Lambda$：

$$V(x)=\frac12m\omega^{2}x^{2}+\frac{\hbar^{2}\Lambda}{2mx^{2}}-2V_0,\qquad \Lambda\equiv\frac{2mV_0a^{2}}{\hbar^{2}}$$

（因为 $\hbar^{2}\Lambda/2m=V_0a^{2}$。）于是定态方程 $-\frac{\hbar^{2}}{2m}\psi''+V\psi=E\psi$ 化为

$$\psi''+\left[k^{2}-\nu^{2}x^{2}-\frac{\Lambda}{x^{2}}\right]\psi=0,\qquad k^{2}\equiv\frac{2m(E+2V_0)}{\hbar^{2}},\qquad \nu\equiv\frac{m\omega}{\hbar}$$

### 第 3 步：$x\to0$ 的指标方程定出 $\alpha$

设 $\psi\sim x^{\alpha}$，代入后最低阶 $x^{\alpha-2}$ 项给出指标方程

$$\alpha(\alpha-1)=\Lambda\ \Longrightarrow\ \alpha=\frac12\left(1+\sqrt{1+4\Lambda}\right)=\frac12\left(1+\sqrt{1+\frac{8mV_0a^{2}}{\hbar^{2}}}\right)$$

**为什么只取正根**：另一根 $\frac12\big(1-\sqrt{1+4\Lambda}\big)<0$ 对应 $x\to0$ 发散、不可归一化的解，必须丢弃。

### 第 4 步：$x\to\infty$ 的渐近行为与代换

$x\to\infty$ 时方程由 $-\nu^{2}x^{2}$ 主导，$\psi\sim e^{\pm\nu x^{2}/2}$；只有 $e^{-\nu x^{2}/2}$ 可归一化。于是令

$$\psi(x)=x^{\alpha}e^{-\nu x^{2}/2}F(y),\qquad y\equiv\nu x^{2}$$

**为什么这样设**：$x^{\alpha}$ 消掉原点的奇异项，$e^{-\nu x^{2}/2}$ 消掉无穷远的增长项，剩下的 $F$ 只需处理多项式级别的行为。

### 第 5 步：化为合流超几何方程

把代换代入并整理：$x^{\alpha+2}$ 项自动抵消（高斯因子正是为此而设），$x^{\alpha-2}$ 项由 $\alpha(\alpha-1)=\Lambda$ 抵消，只剩

$$yF''+\left(\alpha+\frac12-y\right)F'+\left[\frac{k^{2}}{4\nu}-\frac{2\alpha+1}{4}\right]F=0$$

这就是标准的合流超几何方程 $yF''+(b-y)F'-aF=0$，其中

$$b=\alpha+\frac12,\qquad a=\frac{2\alpha+1}{4}-\frac{k^{2}}{4\nu}$$

### 第 6 步：多项式截断给出能级

通解为 $F={}_1F_1(a,b;y)$。但 $y\to\infty$ 时 ${}_1F_1(a,b;y)\sim\frac{\Gamma(b)}{\Gamma(a)}e^{y}y^{a-b}$，会压过 $e^{-y/2}$ 使 $\psi$ 发散，因此级数必须**截断成多项式**：

$$a=-n,\qquad n=0,1,2,\dots$$

于是 $k^{2}=2\nu\left(2n+\alpha+\frac12\right)$。代回 $k^{2}=\frac{2m(E+2V_0)}{\hbar^{2}}$ 与 $\nu=\frac{m\omega}{\hbar}$ 得

$$E_n=\hbar\omega\left(2n+\alpha+\frac12\right)-2V_0$$

写成显式形式：

$$E_n=\hbar\sqrt{\frac{2V_0}{ma^{2}}}\left(2n+1+\frac12\sqrt{1+\frac{8mV_0a^{2}}{\hbar^{2}}}\right)-2V_0,\qquad n=0,1,2,\dots$$

**物理解读**：能级是**等间距**的，间距恒为 $2\hbar\omega$。

### 第 7 步：波函数与归一化

多项式解即广义拉盖尔多项式 $F\propto L_n^{(\alpha-1/2)}(y)$，故

$$\psi_n(x)=N_n\,x^{\alpha}e^{-\nu x^{2}/2}L_n^{(\alpha-1/2)}\!\left(\nu x^{2}\right)$$

归一化用 $\int_0^{\infty}y^{\beta}e^{-y}\left[L_n^{(\beta)}(y)\right]^{2}\mathrm{d}y=\frac{\Gamma(n+\beta+1)}{n!}$（取 $\beta=\alpha-\frac12$），得

$$N_n=\sqrt{\frac{2\,n!\,\nu^{\alpha+1/2}}{\Gamma\left(n+\alpha+\frac12\right)}}$$

### 第 8 步：整条直线上的二重简并

势是偶函数，但 $x=0$ 处 $V\to+\infty$ 是**不可穿越**的壁垒：$x>0$ 与 $x<0$ 是两个完全退耦的独立问题，谱完全相同。因此**每个能级二重简并，且无隧穿劈裂**。两个独立解可取为偶、奇延拓：

$$\psi_n^{(+)}(x)=N_n|x|^{\alpha}e^{-\nu x^{2}/2}L_n^{(\alpha-1/2)}\!\left(\nu x^{2}\right),\qquad \psi_n^{(-)}(x)=\mathrm{sgn}(x)\,\psi_n^{(+)}(x)$$

因 $\alpha>1$，二者在 $x=0$ 处都为零，与无穷高壁垒相容。

### 第 9 步：数值例与核验

取 $m=m_e$、$a=1\ \text{Å}$、$V_0=1\ \mathrm{eV}$：$\Lambda=0.262468$，$\alpha=1.215869$，$\hbar\omega=3.903835\ \mathrm{eV}$，$\nu=0.512317\ \text{Å}^{-2}$。

解析能级为 $E_0=4.698470$、$E_1=12.506140$、$E_2=20.313810$、$E_3=28.121480\ \mathrm{eV}$，相邻间距恒为 $7.807670\ \mathrm{eV}=2\hbar\omega$。

**独立数值核验**（在 $x$ 上直接三点有限差分，$N=1.6\times10^{5}$，$x\in[10^{-3},10]a$，Dirichlet 边界）：

| $n$ | 解析 (eV) | 数值 (eV) | 相对偏差 |
| --- | --- | --- | --- |
| 0 | 4.698470 | 4.698662 | 4.1e-05 |
| 1 | 12.506140 | 12.506470 | 2.6e-05 |
| 2 | 20.313810 | 20.314258 | 2.2e-05 |
| 3 | 28.121480 | 28.122035 | 2.0e-05 |

数值一律**不低于**解析值（Dirichlet 边界给出变分上界），符合变分原理。另外：用 sympy 把解析 $\psi_0$ 代回定态方程，残差化简为 $0$（恒等）；归一化常数经数值积分给 $\int_0^{\infty}|\psi_n|^{2}\mathrm{d}x=1.00000000$（$n=0,1,2,3$）。

![势阱与最低三个定态（曲线为波函数，按能级偏移）](<02-isotonic-oscillator-graph.png>)

![解析与数值能级对比](<02-isotonic-oscillator-spectrum.png>)

---

## 核验（按 `references/verification.md` 清单）

- **量纲**：$\Lambda,\alpha$ 无量纲，$E\sim\hbar\omega=\hbar\sqrt{2V_0/ma^{2}}$ 为能量 ✓
- **边界条件**：正则解 $\psi\sim x^{\alpha}$（$\alpha>1$）自动满足 $\psi(0)=0$；$\psi(\infty)=0$ 由高斯因子保证 ✓
- **等间距**：$\Delta E=2\hbar\omega$ 与数值一致 ✓
- **深势阱极限 $\Lambda\gg1$**：$\alpha=\sqrt{\Lambda}+\frac12+O(\Lambda^{-1/2})$，而 $\hbar\omega\sqrt{\Lambda}=2V_0$，故 $E_n\to2\hbar\omega\left(n+\frac12\right)+\frac{\hbar\omega}{8\sqrt{\Lambda}}+\cdots$。这正是"在两个极小点 $x=\pm a$ 附近、频率 $\omega_{\mathrm{eff}}=2\omega$ 的谐振子"：由 $V''(\pm a)=8V_0/a^{2}$ 得 $\omega_{\mathrm{eff}}=\sqrt{8V_0/(ma^{2})}=2\omega$ ✓；壁垒无穷高，故两支不劈裂 ✓
- **浅势阱极限 $V_0\to0$**：$\hbar\omega\propto\sqrt{V_0}\to0$，离散谱整体塌缩到 $E\to0^{+}$，与"势变平后只剩连续谱"一致 ✓
- **数值代入**：直接有限差分四个能级全部与解析值符合到 $4\times10^{-5}$ 以内 ✓
- **结构自洽**：$V(a^{2}/x)=V(x)$（势在 $x\to a^{2}/x$ 反演下不变），这正是它能精确求解的原因之一 ✓

> **答案：** 记 $\omega=\sqrt{2V_0/(ma^{2})}$、$\nu=m\omega/\hbar$、$\alpha=\frac12\left(1+\sqrt{1+8mV_0a^{2}/\hbar^{2}}\right)$，则定态能量与波函数为 $E_n=\hbar\omega\left(2n+\alpha+\frac12\right)-2V_0=\hbar\sqrt{\frac{2V_0}{ma^{2}}}\left(2n+1+\frac12\sqrt{1+\frac{8mV_0a^{2}}{\hbar^{2}}}\right)-2V_0$，$\psi_n(x)=N_nx^{\alpha}e^{-\nu x^{2}/2}L_n^{(\alpha-1/2)}(\nu x^{2})$，$N_n=\sqrt{2n!\nu^{\alpha+1/2}/\Gamma\left(n+\alpha+\frac12\right)}$，$n=0,1,2,\dots$；每个能级在整条直线上**二重简并**（$x>0$ 与 $x<0$ 两支同谱，无隧穿劈裂）。

---

## 易错点

1. 不展开平方，直接当普通谐振子处理 → 丢掉 $1/x^{2}$ 壁与 $-2V_0$ 常数项。
2. 指标方程取错根：正则解必须取 $\alpha=\frac12(1+\sqrt{1+4\Lambda})>1$，负根在原点不可归一。
3. 误以为 $x=0$ 的奇异性会带来隧穿劈裂 → 壁垒无穷高，两支完全简并。
4. 把 $\omega$ 与极小点附近的局部频率 $\omega_{\mathrm{eff}}=2\omega$ 混淆（深阱极限里出现的是后者）。
5. 归一化时漏掉 $1/x^{2}$ 壁带来的 $x^{\alpha}$ 因子，直接套谐振子的 $N_n$。

## 变式

- **对偶性**：$V(a^{2}/x)=V(x)$，可用来独立验证 $\Lambda$ 与 $\alpha$ 的关系。
- **超对称伙伴**：该势与其 SUSY 伙伴只差一个基态能级，是"形状不变势"的标准例子。
- **径向版本**：把 $1/x^{2}$ 换成离心项 $\hbar^{2}l(l+1)/(2mr^{2})$ 并与 $\hbar^{2}\Lambda/(2mr^{2})$ 合并，等价于把 $l$ 重新标定。

## 复现

```bash
python examples/02-isotonic-oscillator-check.py
```

脚本会解析求能级、用直接有限差分独立复算、sympy 精确核验 $\psi_0$、数值核验归一化，并把两张插图写回本目录。
