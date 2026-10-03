# 解答排版与风格约定

默认产物是**对话内的分步详解**（不主动生成文件）。本文给出模板、**渲染硬约束**与一个完整范例。

## 1. 整体骨架

```
**题意**：一句话复述题目（图片题在此先给出转录结果或题意复述）。
**符号与约定**：列出用到的符号；声明 ħ 是否取 1、坐标系、近似。
**题型**：属于哪一类，标准路径是什么；一句话点出关键。

### 第 1 步：<这步做什么>
（推导 + 一句「为什么可以这样做」）

### 第 2 步：……
…

**核验**
- 量纲：…
- 极限 / 特例：…

> **答案：** <最终结果>

**说明**：物理含义一两句；必要时补易错点与变式。
```

## 2. 数学公式渲染硬约束（必须遵守，否则整段解答报废）

本机 GUI 的 Markdown 渲染器**不是** react-markdown，而是 DSH 自带的 mdast→React 渲染器（`@deepseek-ai/dsh-client-ui-primitives`，`lib/types/markdown/`）。它给 `$$` 加了一条硬规则：

> 源码 `lib/types/markdown/mathCompatibility.js`：
> `const sameLineDollarMathFlow = createMathFlow(codes.dollarSign, codes.dollarSign, codes.dollarSign, false);`
> 分词器里：`if (markdownLineEnding(code)) return multiline ? effects.attempt(...) : nok(code);`

也就是说：**独立公式 `$$...$$` 只有整块写在同一行才被识别**（构造名就叫 `sameLineDollarMathFlow`，`multiline = false`，注释写的是 "same-line display-dollar blocks"）。

⚠️ **踩中的后果不是「公式没渲染」，而是整段解释报废**：`$$` 块内一旦出现换行，公式构造直接失败，那段裸 TeX 交给 KaTeX 也解析不了，渲染器走兜底分支 `span.katex-error` 把内容**当纯文本原样输出**——从那里开始，`###` 标题、`**加粗**`、表格、行内 `$...$` 全部变成生文本。

**四条硬规则**

1. `$$...$$` 必须**单行开闭**，内部不能有换行。
2. `$$` 必须在**行首**（前面只能有空白），否则不会被当作独立公式块。
3. **收尾的 `$$` 之后只能是空白**（不能紧跟 `，`、文字、单位等）。
4. 行内 `$...$` **不能跨行**。

**长公式的正确做法：拆成多个单行 `$$`**

```markdown
由 Ehrenfest 定理，
$$\frac{\mathrm{d}\langle \hat x\rangle}{\mathrm{d}t}=\frac{1}{i\hbar}\langle[\hat x,\hat H]\rangle$$
把 $\hat H=\hat p^2/2m$ 代入得
$$\frac{1}{i\hbar}\langle[\hat x,\hat H]\rangle=\frac{\langle \hat p\rangle}{m}$$
```

**分段函数 / 多行对齐：把整个环境压到一行，用 `\\` 在公式内部换行**

```markdown
$$V(x)=\begin{cases}0,&|x|<a\\ V_0,&|x|>a\end{cases}$$
$$\langle m|\hat x|n\rangle=\begin{cases}\sqrt{\hbar/2m\omega}\sqrt{n},&m=n-1\\ \sqrt{\hbar/2m\omega}\sqrt{n+1},&m=n+1\\ 0,&\text{其它}\end{cases}$$
```

**实在需要跨行的独立公式：用 `\[ ... \]`**（渲染器对这条构造是 `multiline = true`，源码里明确允许换行）。但 `$$` 在别处也通用，所以**优先用单行 `$$`**，只在公式确实很长时才用它：

```markdown
\[
\begin{aligned}
\hat H|n\rangle &= E_n|n\rangle \\
\langle m|\hat H|n\rangle &= E_n\,\delta_{mn}
\end{aligned}
\]
```

**写长解答前的自检**（把草稿存成文件再跑）：

```bash
python <skill>/scripts/check_math_md.py 草稿.md          # 只检查
python <skill>/scripts/check_math_md.py --fix 草稿.md    # 自动把跨行 $$ 并成一行
```

## 3. 排版细则

- **语言**：中文讲解，公式 LaTeX。行内用 `$...$`；独立公式用单行 `$$...$$`（见第 2 节）。
- **步骤编号**：用 `### 第 N 步：…`，每步一个主题。一步内不要混做两件事（例如既做变量代换又做归一化）。
- **「为什么」**：每步开头或结尾一句，说明依据（定理/近似/对易关系/选择定则/边界条件）。
- **公式后的解读**：给一句物理解读，例如「可见能级间距与 $n$ 成正比，这正是经典频率的倍频结构」。
- **数学记号尽量用物理惯例**：$\hbar$、$\hat H$、$\langle A\rangle$、$\psi_n(x)$、$|n\rangle$、$\mathrm{d}x$ 用直立体。
- **不要滥用 emoji、不要用表格堆公式**；表格只用于参数对照、能级简并度计数、极限比较这类真正需要并列的内容。
- **多解与约定**：出现 $\pm$、整体相位、简并子空间基矢选取、规范选择时，说明物理等价性以及你的约定。
- **数值结果**：给 3~4 位有效数字 + 单位；只有确实跑过脚本或手算可查时才给数值。

## 4. 详略控制

| 题目类型 | 详略 |
| --- | --- |
| 常规本科计算题 | 完整推导，中间步骤不省 |
| 考研真题 | 完整推导 + 明确指出「考点」与「易错点」 |
| 竞赛难题 | 完整推导 + 说明思路来源（为什么想到这个近似/变换）+ 备选思路 |
| 用户只要核对结果 | 给出关键几步 + 结果比对，不铺满全篇 |
| 用户明确说「只要答案」 | 给答案 + 一段核验，但**仍要说明关键假设** |

## 5. 公式书写示例

好的写法：

```markdown
由 $[\hat x,\hat p]=i\hbar$ 以及 $\hat H=\dfrac{\hat p^2}{2m}+\dfrac12 m\omega^2\hat x^2$，先算
$$\frac{\mathrm{d}\langle \hat x\rangle}{\mathrm{d}t}=\frac{1}{i\hbar}\langle[\hat x,\hat H]\rangle=\frac{\langle \hat p\rangle}{m}$$
这里只用到 $\hat x$ 与 $\hat p^2$ 的对易关系，不涉及具体波函数——这正是 Ehrenfest 定理的特点。
```

避免：

- 把 `$$...$$` 写成多行（本机渲染器会把它整段当纯文本，见第 2 节）；
- 在 `$$...$$` 收尾之后同一行继续写文字；
- 一口气写五行不带解释的等式链；
- 把 `hbar`、`pi` 直接写进 LaTeX；
- 用 `*` 当乘号（LaTeX 中直接用并列或 `\cdot`）。

## 6. 完整范例（可直接照此风格）

> **题意**：粒子处于一维无限深方势阱 $V(x)=0\,(0<x<L)$，$V=\infty$ 在其余处，处于第 $n$ 个定态，求 $\langle x\rangle$、$\langle x^2\rangle$、$\Delta x$，并求粒子出现在左半阱 $0<x<L/2$ 的概率。
>
> **符号与约定**：$\hbar$ 保留符号；坐标范围取 $0\le x\le L$；$\psi_n$ 取实数归一化形式。
>
> **题型**：波函数与期望值（第 1 类）。标准路径：写出归一化波函数 → 算期望值 → 算不确定度 → 算区间概率。

### 第 1 步：写出归一化波函数

无限深方阱的定态为
$$\psi_n(x)=\sqrt{\frac{2}{L}}\sin\frac{n\pi x}{L},\qquad E_n=\frac{n^2\pi^2\hbar^2}{2mL^2},\quad n=1,2,3,\dots$$
边界条件 $\psi(0)=\psi(L)=0$ 已自动满足；系数 $\sqrt{2/L}$ 由 $\int_0^L|\psi_n|^2\mathrm{d}x=1$ 定出。

### 第 2 步：$\langle x\rangle$

由对称性 $\psi_n^2$ 关于 $x=L/2$ 对称，故 $\langle x\rangle=L/2$。直接积分验证：
$$\langle x\rangle=\frac{2}{L}\int_0^L x\sin^2\frac{n\pi x}{L}\mathrm{d}x=\frac{L}{2}.$$

### 第 3 步：$\langle x^2\rangle$ 与 $\Delta x$

$$\langle x^2\rangle=\frac{2}{L}\int_0^L x^2\sin^2\frac{n\pi x}{L}\mathrm{d}x =L^2\left(\frac13-\frac{1}{2n^2\pi^2}\right),$$
$$\Delta x=\sqrt{\langle x^2\rangle-\langle x\rangle^2} =L\sqrt{\frac{1}{12}-\frac{1}{2n^2\pi^2}} .$$

### 第 4 步：左半阱概率

$$P=\int_0^{L/2}|\psi_n|^2\mathrm{d}x=\frac12\quad(\text{对一切 } n).$$
因为 $|\psi_n|^2$ 关于 $x=L/2$ 对称，左右两半概率必然各占一半。

**核验**
- 量纲：$\langle x\rangle,\ \langle x^2\rangle^{1/2}$ 均为长度，$\Delta x$ 量纲正确。
- 极限 $n\to\infty$：$\Delta x\to L/\sqrt{12}$，正是经典均匀分布在 $[0,L]$ 上的标准差 —— 对应原理成立。
- 校验：$n=1$ 时 $\Delta x\approx0.1808L$，与脚本 `qm.py expect "sin(pi*x/L)" -v x -a 0 -b L` 的符号结果一致。

> **答案：** $\langle x\rangle=\dfrac{L}{2}$，$\langle x^2\rangle=L^2\left(\dfrac13-\dfrac{1}{2n^2\pi^2}\right)$，$\Delta x=L\sqrt{\dfrac{1}{12}-\dfrac{1}{2n^2\pi^2}}$；左半阱概率恒为 $1/2$。

**说明**：半阱概率与 $n$ 无关，是宇称对称的直接后果；不要误以为「$n$ 越大粒子越靠边」。相应的动量不确定度 $\Delta p=n\pi\hbar/L$，于是 $\Delta x\,\Delta p\ge\hbar/2$ 在 $n$ 很大时趋于饱和（最小不确定度关系被无限深阱在经典极限下逼近）。
