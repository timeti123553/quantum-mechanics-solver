# 示例索引

每个示例都是**可复现**的：题目、完整求解、插图与核验脚本放在同一个目录下，图片由脚本生成。

| 示例 | 题目 | 知识点 | 入口 |
| --- | --- | --- | --- |
| 01 | 一维有限深方势阱（深势阱） | 分段势定态、宇称守恒、超越方程与图形解、束缚态计数、深势阱极限 | [01-finite-square-well.md](<01-finite-square-well.md>) |
| 02 | 一维奇异谐振子（isotonic oscillator） | 奇异势 $1/x^2$ 双重极点、指标方程、合流超几何与多项式截断、等间距能级、无穷高壁垒的二重简并 | [02-isotonic-oscillator.md](<02-isotonic-oscillator.md>) |

## 约定

- 每个示例的文件名统一为 `<编号>-<kebab-case-题目>.md`；插图、脚本用同样的前缀，便于归档。
- 示例正文里的独立公式一律**单行** `$$...$$`（见 `references/output-format.md` 第 2 节的渲染硬约束）。
- 新增示例后请跑一遍检查：

```bash
python scripts/check_math_md.py examples
```

## 想加新示例？

把「题目 + 7 步解答 + 核验 + 答案 + 易错点/变式」按 `references/output-format.md` 的模板写成 markdown，配上可复现的核验脚本与插图即可；建议同时在本文的表格里登记一行。
