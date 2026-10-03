# 公式与积分速查

约定：$\hbar$ 保留符号；$\hat p=-i\hbar\nabla$；$[\hat x,\hat p]=i\hbar$；粒子质量记 $m$（磁量子数记 $m_l,m_s$）。所有公式都可直接用 `scripts/qm.py` 复核。

## 1. 基本算符与对易关系

| 关系 | 形式 |
| --- | --- |
| 正则对易 | $[\hat x_i,\hat p_j]=i\hbar\delta_{ij}$，$[\hat x_i,\hat x_j]=[\hat p_i,\hat p_j]=0$ |
| 与函数 | $[\hat x,\hat p^n]=i\hbar n\hat p^{n-1}$，$[f(\hat x),\hat p]=i\hbar f'(\hat x)$ |
| 角动量 | $[\hat L_i,\hat L_j]=i\hbar\varepsilon_{ijk}\hat L_k$，$[\hat L^2,\hat L_i]=0$ |
| 升降 | $\hat L_\pm=\hat L_x\pm i\hat L_y$，$[\hat L_z,\hat L_\pm]=\pm\hbar\hat L_\pm$，$[\hat L_+,\hat L_-]=2\hbar\hat L_z$ |
| 谐振子 | $[\hat a,\hat a^\dagger]=1$，$\hat H=\hbar\omega(\hat a^\dagger\hat a+\tfrac12)$ |
| 时间演化 | $\dfrac{\mathrm d\langle \hat A\rangle}{\mathrm dt}=\dfrac{1}{i\hbar}\langle[\hat A,\hat H]\rangle+\left\langle\dfrac{\partial \hat A}{\partial t}\right\rangle$（Ehrenfest） |
| 不确定关系 | $\Delta A\,\Delta B\ge\dfrac12|\langle[\hat A,\hat B]\rangle|$；$\Delta x\,\Delta p\ge\dfrac{\hbar}{2}$ |

## 2. 常用积分

$$\int_0^L\sin\frac{n\pi x}{L}\sin\frac{m\pi x}{L}\mathrm dx=\frac L2\delta_{mn},\qquad \int_0^L\cos\frac{n\pi x}{L}\cos\frac{m\pi x}{L}\mathrm dx=\frac L2\delta_{mn}\ (n,m\ge1)$$

$$\int_0^L\sin\frac{n\pi x}{L}\cos\frac{m\pi x}{L}\mathrm dx=\begin{cases}0,&n+m\ \text{偶}\\[2pt]\dfrac{2nL}{\pi(n^2-m^2)},&n+m\ \text{奇}\end{cases}$$

$$\int_0^L x\sin^2\frac{n\pi x}{L}\mathrm dx=\frac{L^2}{4},\qquad \int_0^L x^2\sin^2\frac{n\pi x}{L}\mathrm dx=L^3\left(\frac16-\frac{1}{4n^2\pi^2}\right)$$

$$\int_0^\infty x^ne^{-\alpha x}\mathrm dx=\frac{n!}{\alpha^{n+1}},\qquad \int_0^\infty e^{-\alpha x^2}\mathrm dx=\frac12\sqrt{\frac{\pi}{\alpha}},\qquad \int_{-\infty}^{\infty}x^2e^{-\alpha x^2}\mathrm dx=\frac{1}{2\alpha}\sqrt{\frac{\pi}{\alpha}}$$

$$\int_{-\infty}^{\infty}e^{-\alpha x^2+\beta x}\mathrm dx=\sqrt{\frac{\pi}{\alpha}}\,e^{\beta^2/4\alpha},\qquad \int_0^\infty x^{2n}e^{-\alpha x^2}\mathrm dx=\frac{(2n-1)!!}{2^{n+1}\alpha^n}\sqrt{\frac{\pi}{\alpha}}$$

$$\int_{-\infty}^{\infty}\frac{\sin ax}{x}\mathrm dx=\pi\,\mathrm{sgn}(a),\qquad \int_0^\infty\frac{\sin^2ax}{x^2}\mathrm dx=\frac{\pi a}{2},\qquad \int_0^\infty\frac{x^3}{e^x-1}\mathrm dx=\frac{\pi^4}{15}$$

$\delta$ 函数：$\displaystyle\int f(x)\delta'(x-a)\mathrm dx=-f'(a)$，$\delta(ax)=\dfrac{\delta(x)}{|a|}$，$\delta(g(x))=\sum_i\dfrac{\delta(x-x_i)}{|g'(x_i)|}$，$\dfrac{1}{2\pi}\displaystyle\int e^{ikx}\mathrm dk=\delta(x)$。

## 3. 一维定态结果汇总

| 体系 | 能级 | 波函数要点 |
| --- | --- | --- |
| 无限深方阱 $[0,L]$ | $E_n=\dfrac{n^2\pi^2\hbar^2}{2mL^2}$，$n\ge1$ | $\psi_n=\sqrt{2/L}\sin(n\pi x/L)$ |
| 自由粒子（箱归一化长度 $L$） | 连续谱 $E=\dfrac{\hbar^2k^2}{2m}$ | $\psi_k=L^{-1/2}e^{ikx}$，$k=2\pi n/L$ |
| 有限深阱宽 $2a$ 深 $V_0$ | 超越方程，束缚态数 $\approx\left\lceil\dfrac{2a\sqrt{2mV_0}}{\pi\hbar}\right\rceil$ | 偶/奇解；$\psi,\psi'$ 连续 |
| 谐振子 | $E_n=\left(n+\dfrac12\right)\hbar\omega$ | 见第 4 节 |
| $\delta$ 势 $V=-\lambda\delta(x)$ | 唯一束缚态 $E=-\dfrac{m\lambda^2}{2\hbar^2}$ | $\psi\propto e^{-m\lambda|x|/\hbar^2}$ |
| 双 $\delta$ 势 / Kronig–Penney | 能带结构，$ka$ 与 $\cos$ 相关 | Bloch 条件 $\psi(x+a)=e^{ika}\psi(x)$ |
| 刚性转子 | $E_l=\dfrac{l(l+1)\hbar^2}{2I}$ | $Y_{lm}(\theta,\phi)$ |

概率流：$j=\dfrac{\hbar}{m}\mathrm{Im}\!\left(\psi^*\dfrac{\partial\psi}{\partial x}\right)$（1D）；$\mathbf j=\dfrac{\hbar}{m}\mathrm{Im}(\psi^*\nabla\psi)$。

## 4. 谐振子（代数解）

$$\hat x=\sqrt{\frac{\hbar}{2m\omega}}\,(\hat a+\hat a^\dagger),\qquad \hat p=i\sqrt{\frac{m\hbar\omega}{2}}\,(\hat a^\dagger-\hat a)$$

$$\hat a|n\rangle=\sqrt n\,|n-1\rangle,\qquad \hat a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle,\qquad |n\rangle=\frac{(\hat a^\dagger)^n}{\sqrt{n!}}|0\rangle$$

$$\psi_n(x)=\left(\frac{m\omega}{\pi\hbar}\right)^{1/4}\frac{1}{\sqrt{2^nn!}}H_n(\xi)e^{-\xi^2/2},\qquad \xi=\sqrt{\frac{m\omega}{\hbar}}\,x$$

Hermite 多项式：$H_n(\xi)=(-1)^ne^{\xi^2}\dfrac{\mathrm d^n}{\mathrm d\xi^n}e^{-\xi^2}$，$H_0=1$，$H_1=2\xi$，$H_2=4\xi^2-2$，$H_3=8\xi^3-12\xi$；递推 $H_{n+1}=2\xi H_n-2nH_{n-1}$；正交 $\int H_mH_ne^{-\xi^2}\mathrm d\xi=2^nn!\sqrt\pi\,\delta_{mn}$。

常用矩阵元：

$$\langle m|\hat x|n\rangle=\sqrt{\frac{\hbar}{2m\omega}}\left(\sqrt n\,\delta_{m,n-1}+\sqrt{n+1}\,\delta_{m,n+1}\right)$$
$$\langle n|\hat x^2|n\rangle=\frac{\hbar}{2m\omega}(2n+1),\qquad \langle n+2|\hat x^2|n\rangle=\frac{\hbar}{2m\omega}\sqrt{(n+1)(n+2)},\qquad \langle n-2|\hat x^2|n\rangle=\frac{\hbar}{2m\omega}\sqrt{n(n-1)}$$

相干态 $|\alpha\rangle=e^{-|\alpha|^2/2}\sum_n\dfrac{\alpha^n}{\sqrt{n!}}|n\rangle$ 满足 $\hat a|\alpha\rangle=\alpha|\alpha\rangle$，$\Delta x\,\Delta p=\hbar/2$（最小不确定态）。

## 5. 角动量与自旋

$\hat L^2|lm\rangle=l(l+1)\hbar^2|lm\rangle$，$\hat L_z|lm\rangle=m\hbar|lm\rangle$，$m=-l,\dots,l$。

$$\hat L_\pm|lm\rangle=\hbar\sqrt{l(l+1)-m(m\pm1)}\,|l,m\pm1\rangle$$

球谐函数（正交归一 $\int Y^*_{l'm'}Y_{lm}\mathrm d\Omega=\delta_{ll'}\delta_{mm'}$）：

$$Y_{00}=\frac{1}{\sqrt{4\pi}},\quad Y_{10}=\sqrt{\frac{3}{4\pi}}\cos\theta,\quad Y_{1,\pm1}=\mp\sqrt{\frac{3}{8\pi}}\sin\theta\,e^{\pm i\phi}$$

角动量相加：$|j_1-j_2|\le j\le j_1+j_2$；$\hat{\mathbf J}=\hat{\mathbf L}+\hat{\mathbf S}$，$|jm\rangle=\sum_{m_1m_2}\langle j_1m_1j_2m_2|jm\rangle|j_1m_1\rangle|j_2m_2\rangle$（CG 系数可查表；$\hat J_z$ 本征值 $m\hbar$）。

自旋 $1/2$：$\hat{\mathbf S}=\dfrac{\hbar}{2}\boldsymbol\sigma$，

$$\sigma_x=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad \sigma_y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad \sigma_z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad \sigma_i\sigma_j=\delta_{ij}I+i\varepsilon_{ijk}\sigma_k$$

磁场中 $\hat H=-\boldsymbol\mu\cdot\mathbf B$，$\boldsymbol\mu=\gamma\hat{\mathbf S}$；自旋进动（Larmor）频率 $\omega_L=\gamma B$。
二能级 Rabi：$P_{\text{flip}}=\dfrac{\Omega^2}{\Omega^2+\Delta^2}\sin^2\!\left(\dfrac{\sqrt{\Omega^2+\Delta^2}}{2}t\right)$，$\Omega=|V_{fi}|/\hbar$，$\Delta=\omega-\omega_{fi}$。
旋转算符：$e^{-i\theta\,\mathbf n\cdot\boldsymbol\sigma/2}=\cos\dfrac\theta2\,I-i\sin\dfrac\theta2\,\mathbf n\cdot\boldsymbol\sigma$。

## 6. 中心力场与氢原子

径向方程（$u=rR$）：

$$-\frac{\hbar^2}{2m}\frac{\mathrm d^2u}{\mathrm dr^2}+\left[V(r)+\frac{l(l+1)\hbar^2}{2mr^2}\right]u=Eu$$

氢原子（$a_0=\dfrac{4\pi\varepsilon_0\hbar^2}{me^2}$）：

$$E_n=-\frac{me^4}{2(4\pi\varepsilon_0)^2\hbar^2n^2}=-\frac{13.6057\,\mathrm{eV}}{n^2},\qquad R_{nl}(r)=\left(\frac{2}{na_0}\right)^{3/2}\sqrt{\frac{(n-l-1)!}{2n\,[(n+l)!]^3}}\;e^{-r/na_0}\left(\frac{2r}{na_0}\right)^l L^{2l+1}_{n-l-1}\!\left(\frac{2r}{na_0}\right)$$

低阶径向函数（便于直接核对）：

$$R_{10}=2a_0^{-3/2}e^{-r/a_0},\quad R_{20}=\frac{1}{2\sqrt2}a_0^{-3/2}\left(2-\frac ra_0\right)e^{-r/2a_0},\quad R_{21}=\frac{1}{2\sqrt6}a_0^{-3/2}\frac ra_0e^{-r/2a_0}$$

期望值（$Z=1$）：$\langle r\rangle=\dfrac{a_0}{2}[3n^2-l(l+1)]$，$\left\langle\dfrac1r\right\rangle=\dfrac{1}{n^2a_0}$，$\left\langle\dfrac{1}{r^2}\right\rangle=\dfrac{1}{(l+\frac12)n^3a_0^2}$，$\langle r^2\rangle=\dfrac{a_0^2n^2}{2}[5n^2+1-3l(l+1)]$。

维里定理：$2\langle T\rangle=-\langle V\rangle$；对库仑势 $\langle T\rangle=-E_n$，$\langle V\rangle=2E_n$。
简并度：不计自旋 $n^2$，含自旋 $2n^2$。

## 7. 微扰论与近似方法

**定态非简并**：
$$E_n^{(1)}=\langle n|\hat H'|n\rangle,\qquad E_n^{(2)}=\sum_{m\ne n}\frac{|H'_{mn}|^2}{E_n^{(0)}-E_m^{(0)}},\qquad |n^{(1)}\rangle=\sum_{m\ne n}\frac{H'_{mn}}{E_n^{(0)}-E_m^{(0)}}|m\rangle$$
适用条件：$|H'_{mn}|\ll|E_n^{(0)}-E_m^{(0)}|$。

**简并微扰**：在简并子空间内构造 $\hat H'$ 矩阵 $W_{ij}=\langle i|\hat H'|j\rangle$，解 $\det(W-E^{(1)}I)=0$，用本征矢作为零级态。近简并（准简并）时把准简并态一并放入矩阵。

**变分法**：任意归一化试探波函数给出 $E[\psi]=\langle\psi|\hat H|\psi\rangle\ge E_0$；对含参数 $\alpha$ 的试探函数取 $\partial E/\partial\alpha=0$。

**WKB**：
$$T\approx\exp\!\left(-\frac{2}{\hbar}\int_{x_1}^{x_2}\sqrt{2m(V-E)}\,\mathrm dx\right),\qquad \oint p\,\mathrm dx=\left(n+\frac12\right)h$$
适用条件：势在德布罗意波长尺度上缓慢变化，$|p'|/p^2\ll1/\hbar$。

**1D 散射**（$R+T=1$）：
$$T_{\text{方垒}}=\left[1+\frac{V_0^2\sinh^2(\kappa a)}{4E(V_0-E)}\right]^{-1}\ (E<V_0),\qquad \kappa=\frac{\sqrt{2m(V_0-E)}}{\hbar}$$
$$T_{\text{阶跃}}=\frac{4k_1k_2}{(k_1+k_2)^2}\ (E>V_0),\qquad T_{\delta}=\left[1+\frac{m\lambda^2}{2\hbar^2E}\right]^{-1}\ (V=\lambda\delta(x))$$

**3D 玻恩近似**：$f(\theta)=-\dfrac{m}{2\pi\hbar^2}\displaystyle\int e^{i\mathbf q\cdot\mathbf r'}V(\mathbf r')\mathrm d^3r'$，$\mathbf q=\mathbf k-\mathbf k'$；$\dfrac{\mathrm d\sigma}{\mathrm d\Omega}=|f(\theta)|^2$。
分波法：$\sigma=\dfrac{4\pi}{k^2}\sum_l(2l+1)\sin^2\delta_l$；光学定理 $\sigma_{\text{tot}}=\dfrac{4\pi}{k}\mathrm{Im}f(0)$。

## 8. 含时微扰与跃迁

$$c_f^{(1)}(t)=-\frac{i}{\hbar}\int_0^tV_{fi}(t')e^{i\omega_{fi}t'}\mathrm dt',\qquad \omega_{fi}=\frac{E_f-E_i}{\hbar}$$

- 常微扰：$P_{i\to f}=\dfrac{|V_{fi}|^2}{\hbar^2}\dfrac{4\sin^2(\omega_{fi}t/2)}{\omega_{fi}^2}$，短时 $\propto t^2$。
- 简谐微扰 $V\cos\omega t$：共振 $\omega\approx\omega_{fi}$，用 Rabi 公式；长期行为需用黄金规则。
- Fermi 黄金规则：$\Gamma_{i\to f}=\dfrac{2\pi}{\hbar}|V_{fi}|^2\rho(E_f)$（需末态连续谱）。
- 电偶极跃迁选择定则：$\Delta l=\pm1$，$\Delta m=0,\pm1$；谐振子 $\Delta n=\pm1$。
- 突发近似（sudden）：$\psi$ 来不及改变，展开到新本征基上求各态概率。
- 绝热近似（adiabatic）：留在瞬时本征态上，只积累动力学相位。

## 9. 全同粒子与表象

- 交换算符 $\hat P_{12}$：玻色子 $+1$，费米子 $-1$。费米子多体态为 Slater 行列式。
- 两粒子自旋态：三重态（对称，$S=1$）$\uparrow\uparrow,\ \frac{1}{\sqrt2}(\uparrow\downarrow+\downarrow\uparrow),\ \downarrow\downarrow$；单态（反对称，$S=0$）$\frac{1}{\sqrt2}(\uparrow\downarrow-\downarrow\uparrow)$。
- 泡利不相容：两费米子不能占据同一单粒子态；空间对称 $\leftrightarrow$ 自旋反对称。
- 密度算符：$\hat\rho=\sum_i p_i|i\rangle\langle i|$，$\langle\hat A\rangle=\mathrm{Tr}(\hat\rho\hat A)$，$\dfrac{\mathrm d\hat\rho}{\mathrm dt}=\dfrac{1}{i\hbar}[\hat H,\hat\rho]$，纯态 $\mathrm{Tr}\hat\rho^2=1$。
- 矩阵函数：$f(\hat A)=\sum_nf(a_n)|n\rangle\langle n|$；$\hat U(t)=e^{-i\hat Ht/\hbar}$。

## 10. 常数与单位

| 常数 | 数值 |
| --- | --- |
| $\hbar$ | $1.054571817\times10^{-34}\ \mathrm{J\cdot s}=6.582119569\times10^{-16}\ \mathrm{eV\cdot s}$ |
| $\hbar c$ | $197.3269804\ \mathrm{MeV\cdot fm}$ |
| $e$ | $1.602176634\times10^{-19}\ \mathrm C$ |
| $m_e$ | $9.1093837015\times10^{-31}\ \mathrm{kg}=0.51099895\ \mathrm{MeV}/c^2$ |
| $m_p$ | $938.27208816\ \mathrm{MeV}/c^2$ |
| $a_0$ | $5.29177210903\times10^{-11}\ \mathrm m$ |
| Rydberg | $13.605693122994\ \mathrm{eV}$ |
| 精细结构常数 $\alpha$ | $7.2973525693\times10^{-3}\approx1/137.036$ |
| $k_B$ | $8.617333262\times10^{-5}\ \mathrm{eV/K}$ |
| $\mu_B=e\hbar/2m_e$ | $9.2740100783\times10^{-24}\ \mathrm{J/T}=5.7883818060\times10^{-5}\ \mathrm{eV/T}$ |
| $c$ | $2.99792458\times10^{8}\ \mathrm{m/s}$ |

常用组合：$\dfrac{\hbar^2}{2m_ea_0^2}=13.6\,\mathrm{eV}$，$\dfrac{e^2}{4\pi\varepsilon_0}=1.44\,\mathrm{eV\cdot nm}$，$\dfrac{\hbar^2}{m_e}=7.62\,\mathrm{eV\cdot\mathring{A}^2}$。
