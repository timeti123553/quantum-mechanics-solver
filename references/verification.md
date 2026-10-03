# 结果核验清单

解完每道题，按本清单过一遍。**至少完成第 1 条与第 3 条中的一项，并把这两步写进解答。**

## 1. 量纲与量级

| 量 | 量纲 |
| --- | --- |
| 波函数（3D） | $[\text{长度}]^{-3/2}$；（1D）$[\text{长度}]^{-1/2}$ |
| 归一化常数 | 取决于维数，必须使 $\int|\psi|^2\mathrm{d}^dx=1$ 无量纲 |
| 能量 | $[\hbar]^2/([m][L]^2)$，即 $\hbar\omega$、$\hbar^2/(mL^2)$ |
| $\langle p^2\rangle$ | $(\hbar/L)^2$ |
| 概率、透射/反射系数 | 无量纲，且 $R+T=1$ |
| 矩阵元 $\langle m|\hat A|n\rangle$ | 与 $\hat A$ 同量纲 |

**量级快速判据**：把 $\hbar,m,L$ 唯一组合出的能量尺度是 $\hbar^2/(mL^2)$。任何束缚态能量若与它相差若干数量级，先怀疑代数错误。

## 2. 边界条件与连续性

- 无限深阱 / 硬壁：$\psi=0$ 于边界。
- 有限深阱 / 势垒：$\psi$ 与 $\psi'$ 连续（除 $\delta$ 势外）。$\delta$ 势处 $\psi$ 连续、$\psi'$ 跃变为 $\dfrac{2m\lambda}{\hbar^2}\psi(x_0)$。
- 束缚态：$x\to\pm\infty$ 时 $\psi\to0$（可归一化）；束缚态在 1D 中**非简并**（对称势中必为奇或偶宇称）。
- 中心力场：$r\to0$ 时 $u(r)=rR(r)\to0$；$\int_0^\infty|R|^2r^2\mathrm{d}r=1$。
- 周期势：Bloch 形式 $\psi(x+a)=e^{ika}\psi(x)$。

## 3. 极限与特例

常用的「自由检验」：

| 极限 | 应该回到 |
| --- | --- |
| $n\to\infty$ / $\hbar\to0$ | 经典结果（对应原理）：概率密度趋于经典分布，能级趋于连续 |
| 耦合常数 / 微扰 $\lambda\to0$ | 未微扰的已知结果 |
| 势垒高度 $V_0\to0$ 或宽度 $a\to0$ | 无势垒：$T\to1,\ R\to0$ |
| 势垒 $V_0\to\infty$ | $T\to0$；无限深阱能级 $E_n=n^2\pi^2\hbar^2/(2mL^2)$ |
| 谐振子 $n$ 大 | 概率密度趋于经典（在转折点附近发散） |
| 温度 $T\to0$ / $T\to\infty$ | 玻尔兹曼因子或高低温极限 |
| 小参数展开 $x\ll1$ | 与泰勒展开前几项一致 |
| 氢原子 $n$ 大、$l=n-1$ | 径向分布趋向经典的开普勒轨道（一个峰） |

**已知特例对照**：一维无限深阱、谐振子基态 $\hbar\omega/2$、氢原子 $-13.6\,\mathrm{eV}/n^2$、刚性转子 $l(l+1)\hbar^2/2I$、自由粒子波包扩散。

## 4. 结构性检查

- **厄米性**：可观测量的矩阵必须厄米（$A_{mn}=A_{nm}^*$），本征值为实。
- **正交归一与完备性**：$\langle m|n\rangle=\delta_{mn}$；按一套完备基展开时系数满足 $\sum|c_n|^2=1$。
- **守恒量**：$[\hat A,\hat H]=0$ 才对应对守恒量；对称性 → 宇称/角动量量子数必为守恒量。
- **简并度计数**：氢原子（不考虑自旋）第 $n$ 层简并度 $n^2$，含自旋 $2n^2$；三维各向同性谐振子简并度 $(n+1)(n+2)/2$。
- **选择定则**：电偶极跃迁 $\Delta l=\pm1$、$\Delta m=0,\pm1$；谐振子 $\Delta n=\pm1$。若算出「允许」的跃迁违反定则，先查矩阵元。
- **对称性**：宇称允许的矩阵元 $\langle m|\hat x|n\rangle$ 在 $m,n$ 同宇称时必为 0。
- **概率归一**：所有分支概率之和为 1（透射 + 反射、各本征态概率）。

## 5. 高频错因子（考场上最常丢分的地方）

| 易错点 | 正确形式 |
| --- | --- |
| 不确定关系 | $\Delta x\,\Delta p\ge\hbar/2$（不是 $\hbar$） |
| 谐振子零点能 | $\hbar\omega/2$（不是 $\hbar\omega$） |
| 动量算符 | $\hat p=-i\hbar\nabla$（不是 $+i\hbar$，也不是 $-i\hbar/2$） |
| 基本对易关系 | $[\hat x,\hat p]=i\hbar$（符号！） |
| 角动量本征值 | $\hat L^2$ 为 $l(l+1)\hbar^2$（**不是** $l^2\hbar^2$），$\hat L_z$ 为 $m\hbar$ |
| 一维无限深阱 | $E_n=\dfrac{n^2\pi^2\hbar^2}{2mL^2}$，$\psi_n=\sqrt{\dfrac2L}\sin\dfrac{n\pi x}{L}$ |
| 玻尔半径 | $a_0=\dfrac{4\pi\varepsilon_0\hbar^2}{me^2}=\dfrac{\hbar}{m c\alpha}$ |
| 氢原子能级 | $E_n=-\dfrac{me^4}{2(4\pi\varepsilon_0)^2\hbar^2n^2}=-\dfrac{13.6\,\mathrm{eV}}{n^2}$ |
| 一阶微扰 | $E_n^{(1)}=\langle n|\hat H'|n\rangle$（对角元，不是非对角元） |
| 二阶微扰 | $E_n^{(2)}=\sum_{m\ne n}\dfrac{|H'_{mn}|^2}{E_n^{(0)}-E_m^{(0)}}$（分母是**未微扰**能级差，符号为 $E_n-E_m$） |
| 简并微扰 | 先在对角化简并子空间内的 $\hat H'$ 矩阵；近似简并时也需对角化 |
| 含时微扰一阶 | $c_f^{(1)}(t)=-\dfrac{i}{\hbar}\displaystyle\int_0^t V_{fi}(t')e^{i\omega_{fi}t'}\mathrm{d}t'$ |
| Fermi 黄金规则 | $\Gamma=\dfrac{2\pi}{\hbar}|V_{fi}|^2\rho(E_f)$（$\rho$ 是**末态密度**） |
| 跃迁概率 | 用 $|c_f|^2$，别漏模方；共振时 $\propto t^2$，需取 $t$ 内平均或短时极限 |
| 平面波归一化 | $\langle p'|p\rangle=\delta(p-p')$，$\psi_p=(2\pi\hbar)^{-1/2}e^{ipx/\hbar}$ |
| WKB 量子化 | $\oint p\,\mathrm{d}x=\left(n+\dfrac12\right)h$（$\tfrac12$ 不能丢） |
| 3D 态密度 | $\rho(E)=\dfrac{1}{2\pi^2}\left(\dfrac{2m}{\hbar^2}\right)^{3/2}\sqrt E$ |
| 透射系数 | $T=\dfrac{j_{\text{trans}}}{j_{\text{inc}}}$，用**概率流**定义而非 $|\psi|^2$ 之比 |
| $\delta$ 势束缚态 | 唯一束缚态 $E=-\dfrac{m\lambda^2}{2\hbar^2}$（$V=-\lambda\delta(x)$，$\lambda>0$） |
| 全同粒子 | 费米子交换反对称（Slater 行列式），玻色子对称；空间-自旋对称性要搭配正确 |
| 时间演化 | $|\psi(t)\rangle=e^{-i\hat Ht/\hbar}|\psi(0)\rangle$（注意 $i$ 与 $-$） |

## 6. 数值代入

- 只有**确实执行过脚本或手算可复核**时才给数值。
- 常用代入：$\hbar c=197.327\,\mathrm{MeV\cdot fm}$，$m_ec^2=0.511\,\mathrm{MeV}$，$a_0=0.0529\,\mathrm{nm}$，$\hbar=1.0546\times10^{-34}\,\mathrm{J\cdot s}$。
- 注意单位一致（eV ↔ J、nm ↔ m、无量纲量不要带单位）。
- 代入 2~3 组参数比只代一组更能暴露错误（尤其能暴露符号与因子问题）。
