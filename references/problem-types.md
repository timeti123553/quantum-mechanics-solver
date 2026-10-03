# 题型判据与标准解法路径

用法：先按「判据」定位题型，沿「标准路径」推进，最后扫一眼「陷阱」。公式一律见 `formulas.md`。

---

## 1. 波函数、概率与期望值

**判据**：直接给出 $\psi(x)$ 或 $\psi(x,t)$；问归一化常数、$\langle x\rangle$、$\langle p\rangle$、$\Delta x$、某区间概率、概率流、随时间演化、Ehrenfest 定理、守恒量。

**标准路径**
1. **归一化**：$N=1/\sqrt{\int|\psi|^2\mathrm dx}$（注意积分区域与维数；1D 量纲 $[\text{长度}]^{-1/2}$）。
2. **期望值**：$\langle \hat A\rangle=\dfrac{\int\psi^*\hat A\psi\,\mathrm dx}{\int|\psi|^2\mathrm dx}$；$\hat p=-i\hbar\dfrac{\partial}{\partial x}$，$\hat T=-\dfrac{\hbar^2}{2m}\dfrac{\partial^2}{\partial x^2}$。
3. **不确定度**：$\Delta A=\sqrt{\langle \hat A^2\rangle-\langle \hat A\rangle^2}$；最后核对 $\Delta x\Delta p\ge\hbar/2$。
4. **区间概率**：$P(a,b)=\int_a^b|\psi|^2\mathrm dx$；若是分立本征态叠加，也可用 $P=\sum|c_n|^2$。
5. **概率流**：$j=\dfrac\hbar m\mathrm{Im}(\psi^*\psi')$；核对连续性方程 $\partial_t|\psi|^2+\partial_xj=0$。
6. **含时演化**：先求 $\hat H$ 的本征态，把初态展开
   $$|\psi(0)\rangle=\sum_nc_n|n\rangle,\qquad |\psi(t)\rangle=\sum_nc_ne^{-iE_nt/\hbar}|n\rangle .$$
7. **守恒量**：若 $[\hat A,\hat H]=0$ 且初态是 $\hat A$ 本征态，则该量不随时间变。

**陷阱**
- 没归一化就代期望值公式；复数 $\psi$ 忘记共轭。
- $\hat p$ 的 $i$ 漏掉或写成 $+i\hbar\partial_x$。
- 含时演化漏掉 $e^{-iE_nt/\hbar}$ 或写成 $e^{+iE_nt/\hbar}$。
- $\Delta x$ 用了 $\langle x^2\rangle$ 忘了减 $\langle x\rangle^2$。
- 1D 与 3D 归一化常数混淆（$r^2\mathrm dr$ vs $\mathrm dx$）。

---

## 2. 一维定态与束缚态

**判据**：分段势（方阱、有限深阱、$\delta$ 势、双 $\delta$、周期势），求能级与波函数；出现「束缚态」「基态能量」「束缚态个数」。

**标准路径**
1. 分区写出 Schrödinger 方程，令
   $$k=\frac{\sqrt{2mE}}{\hbar}\ (\text{阱内}),\qquad \kappa=\frac{\sqrt{2m(V_0-E)}}{\hbar}\ (\text{垒外，}E<V_0) .$$
2. 每区写通解（$e^{\pm ikx}$ 或 $e^{\pm\kappa x}$）；**舍弃不能归一化的项**。
3. **对称势先分奇偶**：只解 $x>0$ 半区，用 $\psi'(0)=0$（偶）或 $\psi(0)=0$（奇）替代一处匹配。
4. 匹配边界：$\psi$ 连续；$\psi'$ 连续（$\delta$ 势处 $\psi$ 连续，$\psi'$ 跃变 $\dfrac{2m\lambda}{\hbar^2}\psi(x_0)$）。
5. 消去系数得**超越方程**（如 $k\tan ka=\kappa$），用图解法/数值法求根并讨论解数。
6. 归一化、写出 $\psi_n$；给出 $E_n$ 的小 $V_0$ 与大 $V_0$ 极限。

**陷阱**
- 漏掉某处匹配条件，或把 $\psi'$ 连续用在 $\delta$ 势上。
- 混淆 $k$ 与 $\kappa$；指数写成 $e^{\pm ikx}$ 却当作束缚态（应衰减）。
- 忘记「束缚态要求 $E<V_0$」，把连续谱当束缚态。
- 有限深阱**至少有一个束缚态**（1D 对称势恒成立），束缚态总数由深度与宽度共同决定。
- 对称势中束缚态非简并，奇偶解要分别讨论。

---

## 3. 一维散射

**判据**：入射粒子、透射/反射系数、势垒/台阶/势阱、共振透射、$E$ 与 $V_0$ 比大小。

**标准路径**
1. 写「入射 + 反射」与「透射」波（势垒内用 $e^{\pm\kappa x}$ 或 $\sinh/\cosh$）。
2. 边界匹配求振幅比 $B/A$、$F/A$。
3. **用概率流**定义：$R=\left|\dfrac j_{\text{ref}}\right|/\left|j_{\text{inc}}\right|$，$T=\left|j_{\text{trans}}\right|/\left|j_{\text{inc}}\right|$，其中 $j=\dfrac{\hbar k}{m}|A|^2$。
4. 核对 $R+T=1$。
5. 讨论极限：$E\ll V_0$（指数压制）、$E\gg V_0$（趋近 1）、$E=V_0$、共振点。

**陷阱**
- 用 $|\psi|^2$ 之比当 $T$（势垒两侧 $k$ 不同，必须带 $k$ 因子）。
- 势垒内部漏写 $e^{+\kappa x}$ 项（有限宽势垒两项都要保留）。
- 把 $T$ 写成 $1-R$ 却不验证 $R$ 的表达式是否自洽。
- 隧穿中 $\sinh^2(\kappa a)$ 写成 $\sin^2$。

---

## 4. 谐振子

**判据**：$\frac12m\omega^2x^2$ 势、升降算符、Hermite 多项式、矩阵元、相干态、以 $x^3$/$x^4$ 为微扰。

**标准路径**
1. 用 $\hat a,\hat a^\dagger$ 改写 $\hat x,\hat p,\hat H$，能级 $E_n=(n+\tfrac12)\hbar\omega$ 与零点能。
2. 需要矩阵元时把待求算符**用 $\hat a,\hat a^\dagger$ 表出并展开**，再用 $\hat a|n\rangle=\sqrt n|n-1\rangle$、$\hat a^\dagger|n\rangle=\sqrt{n+1}|n+1\rangle$。
3. 若给的是波函数（Hermite 形式），按第 1 节算期望值，或用递推关系。
4. 微扰题：把 $\hat H'$ 展开成 $\hat a,\hat a^\dagger$ 的多项式，只保留连接 $\Delta n$ 符合要求的项。
5. 相干态：$\hat a|\alpha\rangle=\alpha|\alpha\rangle$，$\langle x\rangle$ 做简谐振荡，$\Delta x\Delta p=\hbar/2$。

**陷阱**
- 零点能 $\dfrac12\hbar\omega$ 丢失。
- $\hat x,\hat p$ 的系数写成 $\sqrt{\hbar/m\omega}$（应为 $\sqrt{\hbar/2m\omega}$）。
- $\hat x^2$ 只连接 $n$ 与 $n\pm2$（不会连接 $n\pm1$），算矩阵元时漏掉对角项。
- 一阶微扰 $\langle n|\hat x^3|n\rangle=0$（奇函数），不要算成非零。
- 非简并微扰公式用于谐振子的 $\hat x^4$ 微扰是可行的（$\Delta n\neq0$ 的项进入二阶）。

---

## 5. 角动量与自旋

**判据**：$\hat L^2,\hat L_z$ 本征值、升降算符、自旋 $1/2$、泡利矩阵、磁场中的自旋、Stern–Gerlach、进动、Rabi 振荡。

**标准路径**
1. 明确用哪个角动量（轨道 $l$、自旋 $s$、总 $j$）与其本征值 $\hbar^2l(l+1)$、$\hbar m$。
2. 升降算符作用：$\hat L_\pm|lm\rangle=\hbar\sqrt{l(l+1)-m(m\pm1)}|l,m\pm1\rangle$。
3. 自旋：$\hat{\mathbf S}=\frac\hbar2\boldsymbol\sigma$，写出 $2\times2$ 矩阵，求 $\hat H=-\boldsymbol\mu\cdot\mathbf B$ 的本征值与本征矢。
4. 时间演化：$\hat U=e^{-i\hat Ht/\hbar}$（自旋 $1/2$ 用 $\boldsymbol\sigma$ 的指数公式）。
5. 需要 $\langle L_x\rangle$ 之类，先用 $\hat L_\pm$ 表示 $\hat L_x=\frac12(\hat L_++\hat L_-)$。

**陷阱**
- 写成 $l^2\hbar^2$（应为 $l(l+1)\hbar^2$）。
- 升降算符的根式写反（$m(m\pm1)$ 与 $m(m\mp1)$）；相位约定要与所用教材一致。
- $e^{-i\theta\mathbf n\cdot\boldsymbol\sigma/2}$ 里的 $\theta/2$（自旋 $1/2$ 旋转 $2\pi$ 变号）。
- 回旋/Larmor 频率漏掉 $g$ 因子或 $\hbar$。

---

## 6. 中心力场与氢原子

**判据**：球对称势、氢原子/类氢离子、径向方程、$R_{nl}$、简并度、$\langle r\rangle$、$\langle1/r\rangle$、能级修正。

**标准路径**
1. 分离变量 $\psi=R(r)Y_{lm}(\theta,\phi)$，令 $u(r)=rR(r)$，得
   $$-\frac{\hbar^2}{2m}u''+\left[V(r)+\frac{l(l+1)\hbar^2}{2mr^2}\right]u=Eu .$$
2. 讨论 $r\to0$ 与 $r\to\infty$ 的渐近行为，提取 $u\sim r^{l+1}e^{-\kappa r}$，再设级数解。
3. 级数截断条件给出能级量子化；写出归一化 $R_{nl}$。
4. 期望值优先用递推/维里定理，避免硬算积分。
5. 简并度计数（不计自旋 $n^2$，含自旋 $2n^2$）。

**陷阱**
- 体积元写成 $\mathrm dr$（应为 $r^2\mathrm dr$），归一化积分 $\int|R|^2r^2\mathrm dr=1$。
- 离心势项写成 $l(l+1)$ 少了 $\hbar^2/2mr^2$ 的系数。
- $\langle1/r\rangle$ 与 $\langle r\rangle$ 混用；前者与 $l$ 无关。
- 忘记 $u(0)=0$ 边界条件。

---

## 7. 定态微扰论

**判据**：「小量/弱场/微扰」、$H=H_0+\lambda H'$、Stark 效应、Zeeman 效应、能级修正与态修正。

**标准路径**
1. **先判断简并性**（这一步决定用哪套公式；近简并也要当简并处理）。
2. 非简并：$E_n^{(1)}=\langle n|\hat H'|n\rangle$，$E_n^{(2)}=\sum_{m\neq n}\dfrac{|H'_{mn}|^2}{E_n^{(0)}-E_m^{(0)}}$；校验 $|H'_{mn}|\ll|E_n^{(0)}-E_m^{(0)}|$。
3. 简并：在简并子空间内构造矩阵 $W_{ij}=\langle i|\hat H'|j\rangle$，解 $\det(W-E^{(1)}I)=0$，本征矢即零级正确态；**子空间外的耦合再进二阶**。
4. 讨论微扰使简并解除的方式（哪些态分裂、分裂间隔）。
5. 对称性/选择定则可先杀掉大量矩阵元，再动手积分。

**陷阱**
- 分母写成 $E_m-E_n$（应为 $E_n-E_m$）。
- 一阶修正用非对角元（应是对角元 $\langle n|H'|n\rangle$）。
- 简并子空间没对角化，直接用原基矢算修正。
- 氢原子 $n=2$ 的 Stark 效应必须用简并微扰，且要包含 $2s$ 与 $2p$ 四个态；经典结论是分裂 $\pm3eEa_0$。
- 忘记说明微扰论适用条件。

---

## 8. 含时微扰与跃迁

**判据**：随时间变化的微扰 $V(t)$、跃迁概率、共振、Fermi 黄金规则、选择定则、自发/受激辐射、突发/绝热近似。

**标准路径**
1. 一阶：$c_f^{(1)}(t)=-\dfrac{i}{\hbar}\displaystyle\int_0^tV_{fi}(t')e^{i\omega_{fi}t'}\mathrm dt'$，$\omega_{fi}=(E_f-E_i)/\hbar$。
2. 概率 $P_{i\to f}=|c_f^{(1)}|^2$；给出共振条件并讨论短时（$\propto t^2$）与长时行为。
3. 末态连续谱 → Fermi 黄金规则 $\Gamma=\dfrac{2\pi}{\hbar}|V_{fi}|^2\rho(E_f)$；态密度按维数写。
4. 简谐驱动 → Rabi 公式；$\Delta=0$ 时 $\sin^2(\Omega t/2)$。
5. 用选择定则先判断哪些末态允许，再算矩阵元。

**陷阱**
- 忘记模方，或把 $c_f$ 当概率。
- 黄金规则里 $\rho(E_f)$ 与 $\rho(\omega)$ 混用（差 $\hbar$ 因子）。
- 共振时直接把 $\sin^2(\omega_{fi}t/2)/\omega_{fi}^2$ 取 $t\to\infty$（需取 $\delta$ 函数或时间平均）。
- 突发近似下错把波函数当作「瞬时本征态」（那是绝热近似）。
- 选择定则记错：电偶极 $\Delta l=\pm1$、$\Delta m=0,\pm1$。

---

## 9. 变分法与 WKB

**判据**：试探波函数、上界估计、参数优化、隧穿概率、半经典量子化、经典转折点。

**标准路径**
1. 变分：写 $E[\psi]=\dfrac{\langle\psi|\hat H|\psi\rangle}{\langle\psi|\psi\rangle}$，先归一化（或保留分母），对参数求 $\partial E/\partial\alpha=0$，回代得上界；说明与真值的关系（$E\ge E_0$）。
2. WKB 贯穿：$T\approx\exp\left(-\dfrac2\hbar\int_{x_1}^{x_2}\sqrt{2m(V-E)}\mathrm dx\right)$，积分区间是经典禁区。
3. 量子化：$\oint p\,\mathrm dx=(n+\tfrac12)h$；识别转折点与积分路径。
4. 检验适用性：势在一个德布罗意波长内变化很小；转折点附近需用 Airy 连接公式。

**陷阱**
- 试探波函数未归一化直接代 $\langle H\rangle$。
- WKB 指数积分上下限取成经典允许区（应为禁区）。
- 量子化条件漏掉 $\tfrac12$（这正是零点能的来源）。
- 把变分结果当作严格解（它只是上界）。

---

## 10. 全同粒子

**判据**：两个及以上全同费米子/玻色子、交换对称性、氦原子、Slater 行列式、泡利不相容、正氦/仲氦、交换能。

**标准路径**
1. 判断粒子统计 → 总波函数（空间 × 自旋）必须对称（玻色）或反对称（费米）。
2. 用对称化/反对称化组合构造态：$\frac{1}{\sqrt2}[\psi_a(1)\psi_b(2)\pm\psi_b(1)\psi_a(2)]$；多粒子写 Slater 行列式。
3. 算能量期望：$\langle H\rangle=\dfrac{1}{1\pm|\langle a|b\rangle|^2}\left(\langle a|h|a\rangle+\langle b|h|b\rangle\pm\cdots\right)$，识别直接项与交换项。
4. 结合自旋：空间对称配自旋反对称（单态），反之配三重态。
5. 泡利原理 → 能级填充与简并压。

**陷阱**
- 交换项符号搞反（反对称 → 负号）。
- 自旋与空间对称性搭配错误（三重态是自旋对称，故空间必须反对称）。
- 归一化因子漏 $1/\sqrt2$ 或漏 $1\pm|\langle a|b\rangle|^2$。
- 把「两个电子不能同态」误用为「不能同位置」。

---

## 11. 矩阵力学与表象

**判据**：给出哈密顿量矩阵、二能级系统、时间演化算符、密度矩阵、表象变换、测量概率。

**标准路径**
1. 求 $\hat H$ 的本征值与本征矢（`qm.py eigen`）；确认厄米性与正交归一。
2. 时间演化：$\hat U(t)=\sum_ne^{-iE_nt/\hbar}|n\rangle\langle n|$；初态用本征基展开求各态概率。
3. 二能级：写成 $\hat H=\frac\hbar2(\Delta\sigma_z+\Omega\sigma_x)$ 形式，用 $\boldsymbol\sigma$ 的代数或直接解耦成 Rabi 振荡。
4. 密度矩阵：$\hat\rho=\sum_ip_i|i\rangle\langle i|$，$\dfrac{\mathrm d\hat\rho}{\mathrm dt}=\dfrac1{i\hbar}[\hat H,\hat\rho]$，$\langle\hat A\rangle=\mathrm{Tr}(\hat\rho\hat A)$。
5. 测量：把态投影到被测算符本征基上，概率 $|\langle a_n|\psi\rangle|^2$。

**陷阱**
- 本征矢忘记归一化或忘记整体相位无关性。
- 简并本征子空间的基矢选取需说明。
- 矩阵函数 $f(\hat A)$ 用逐元素函数（错），必须本征分解。
- 混淆 Schrödinger 表象与相互作用表象中的时间演化。

---

## 12. 电磁场中的粒子

**判据**：磁场/电场中的带电粒子、Landau 能级、规范变换、Aharonov–Bohm 效应、磁通、磁矩、Zeeman 分裂。

**标准路径**
1. 最小耦合：$\hat{\mathbf p}\to\hat{\mathbf p}-q\mathbf A$，$\hat H=\dfrac{(\hat{\mathbf p}-q\mathbf A)^2}{2m}+q\varphi$。
2. 选合适规范（Landau 规范 $\mathbf A=Bx\hat y$ 或对称规范）化简方程。
3. 均匀磁场 ⊥ 平面运动 → 等效谐振子，能级 $E_n=\left(n+\tfrac12\right)\hbar\omega_c$，$\omega_c=\dfrac{|q|B}{m}$；简并度与磁通量子化相关。
4. Aharonov–Bohm：相位 $\Delta\varphi=\dfrac{q}{\hbar}\oint\mathbf A\cdot\mathrm d\mathbf l=\dfrac{q\Phi}{\hbar}$。
5. 规范变换下物理量不变（能级、$|\psi|^2$、概率流），只有相位改变。

**陷阱**
- 规范选择不当使方程难以分离；换规范后忘记同时乘相位因子。
- 混淆 $\omega_c=\frac{|q|B}{m}$ 与自旋 Larmor 频率 $\omega_L=\gamma B$。
- AB 相位漏掉电荷 $q$ 或写成 $\Phi/\hbar$（少 $q$）。
- 把朗道能级当连续谱处理。

---

## 13. 竞赛进阶套路

- **角动量合成与 CG**：先确定可能的 $j$ 范围，再用升降算符从「最大 $m$」态递推构造所有 $|jm\rangle$；$\hat J_z=m\hbar$ 必须匹配。查表时注意相位约定。
- **张量算符与 Wigner–Eckart**：矩阵元 $\propto$ CG 系数 × 约化矩阵元；只要问「比例关系」（如 $\langle jm'|T_q^k|jm\rangle$ 之间的相对大小），用 W–E 定理可跳过积分。
- **选择定则的来源**：宇称、角动量代数（$\hat x$ 是秩 1 球张量 $\Rightarrow\Delta l=\pm1$）、以及 $\hat L_z$ 守恒（$\Delta m$）。
- **对称性与守恒量**：平移 ↔ 动量、旋转 ↔ 角动量、宇称、时间反演（Kramers 简并）。先用对称性定零级态，再算修正。
- **不确定性关系的推广**：$\Delta A\Delta B\ge\frac12|\langle[\hat A,\hat B]\rangle|$；注意它依赖具体态，找「最小不确定态」用变分/算符分解。
- **最小不确定态**的构造：令 $(\hat A-\langle A\rangle)|\psi\rangle=i\lambda(\hat B-\langle B\rangle)|\psi\rangle$，解出高斯型态（相干态、压缩态）。
- **混合近似题**（微扰 + 变分）：先用变分定零级，再用微扰修正；说明两步近似的适用条件。
- **量级估算题**：把 $\hbar,m,L,e^2/4\pi\varepsilon_0$ 凑出目标量纲，再用已知数（$a_0$、$13.6\,\mathrm{eV}$、$\hbar c$）换算；结果写成「$\sim$」并说明忽略了什么。
- **陷阱题常见形态**：非厄米「哈密顿量」（$PT$ 对称）、复数势、初态不是本征态、简并导致微扰论失效、共振导致微扰论失效、经典禁区内的「负动能」。遇到这类先停下来说明前提被破坏。
