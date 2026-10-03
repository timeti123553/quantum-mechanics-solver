#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""check_math_md.py — 检查/修正 Markdown 中的数学公式写法是否适配 DSH 前端渲染器。

约束来自本机 DSH 前端源码（包 @deepseek-ai/dsh-client-ui-primitives，
lib/types/markdown/mathCompatibility.js）：

  * 独立公式只有「**同一行内开闭**的 $$...$$」才会被当成 math 块
    —— 构造名 sameLineDollarMathFlow，createMathFlow(..., multiline=false)；
  * $$ 必须位于行首（flow 构造按行首分派），且收尾的 $$ 之后**只能有空白**；
  * 跨行的 $$ 块不会被识别为公式；失败后 KaTeX 也解析不了那段裸 TeX，
    渲染器走 span.katex-error 兜底，把后续内容当**纯文本**原样输出
    （`###`、`**`、`$...$` 全部不再渲染）；
  * 需要跨行的独立公式请用 \\[ ... \\]（该构造 multiline=true，官方支持）；
  * 行内 $...$ 不要跨行。

用法：
    python check_math_md.py <文件或目录> [...]
    python check_math_md.py --fix <文件或目录> [...]      # 把跨行的 $$ 块并成单行
    python check_math_md.py --fix --dry-run <路径>         # 只看会改成什么样

退出码：0 = 没有 error；1 = 存在 error。
"""
from __future__ import annotations

import argparse
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

DOLLAR = "$$"
FENCE_MARKS = ("```", "~~~")


def _strip_fences_and_inline(text):
    """把围栏代码块整段挖掉、把行内 code span 抹平，返回 (行列表, 是否在围栏内)。"""
    lines = text.split("\n")
    out = []
    fence = None
    for line in lines:
        stripped = line.lstrip()
        if fence is None and stripped.startswith(FENCE_MARKS):
            fence = stripped[:3]
            out.append("\x00FENCE")
            continue
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            out.append("\x00FENCE")
            continue
        # 抹掉行内 code span（成对的单反引号）
        cleaned = line
        while cleaned.count("`") >= 2:
            i = cleaned.find("`")
            j = cleaned.find("`", i + 1)
            if j < 0:
                break
            cleaned = cleaned[:i] + " " * (j - i + 1) + cleaned[j + 1 :]
        out.append(cleaned)
    return out


def _occurrences(lines):
    occ = []
    for idx, line in enumerate(lines):
        if line == "\x00FENCE":
            continue
        start = 0
        while True:
            col = line.find(DOLLAR, start)
            if col < 0:
                break
            occ.append((idx, col))
            start = col + 2
    return occ


def analyze(text):
    """返回 (issues, lines)；issue = (行号, 级别, 说明)。"""
    raw_lines = text.split("\n")
    lines = _strip_fences_and_inline(text)
    issues = []
    occ = _occurrences(lines)
    if len(occ) % 2:
        line_no, _ = occ[-1]
        issues.append((line_no + 1, "error", "未闭合的 $$ —— 文件结束都没有配对的 $$"))
    pairs = list(zip(occ[0::2], occ[1::2]))
    for (l1, c1), (l2, c2) in pairs:
        if l1 != l2:
            issues.append(
                (
                    l1 + 1,
                    "error",
                    "$$ 块跨行（第 %d–%d 行）：本机渲染器只认同一行内开闭的 $$ —— "
                    "请拆成多个单行 $$，或改用 \\[ ... \\]" % (l1 + 1, l2 + 1),
                )
            )
        tail = lines[l2][c2 + 2 :] if l2 < len(lines) else ""
        if tail.strip():
            issues.append(
                (
                    l2 + 1,
                    "error",
                    "收尾的 $$ 之后同一行还有内容 %r —— 渲染器要求 $$ 后只能是空白" % tail.strip()[:40],
                )
            )
        head = lines[l1][:c1]
        if head.strip():
            issues.append(
                (
                    l1 + 1,
                    "warn",
                    "$$ 不在行首（前面有 %r）—— flow 构造按行首分派，这不会被当成独立公式块"
                    % head.strip()[:30],
                )
            )
    # 行内 $...$ 跨行检查（粗略：一行的 $ 个数为奇数，且下一行还有 $）
    for idx, line in enumerate(lines):
        if line == "\x00FENCE":
            continue
        stripped = line.replace(DOLLAR, "")
        if stripped.count("$") % 2 == 1:
            nxt = lines[idx + 1] if idx + 1 < len(lines) else ""
            if nxt != "\x00FENCE" and "$" in nxt.replace(DOLLAR, ""):
                issues.append((idx + 1, "warn", "行内 $ 数量为奇数，疑似行内公式跨行（行内 $...$ 不能跨行）"))
    # \[ ... \] 收尾后不能有正文
    for idx, line in enumerate(lines):
        col = line.find("\\]")
        if col >= 0 and line[col + 2 :].strip():
            issues.append((idx + 1, "warn", "\\] 之后同一行还有内容 %r" % line[col + 2 :].strip()[:40]))
    return sorted(issues), lines


def fix_text(text):
    """把跨行的 $$ 块并成一行；返回 (新文本, 修改处数)。"""
    lines = text.split("\n")
    changed = 0
    while True:
        scan_lines = _strip_fences_and_inline("\n".join(lines))
        occ = _occurrences(scan_lines)
        pairs = list(zip(occ[0::2], occ[1::2]))
        target = next(((a, b) for a, b in pairs if a[0] != b[0]), None)
        if target is None:
            break
        (l1, c1), (l2, c2) = target
        parts = [lines[l1][c1 + 2 :].strip()]
        parts += [x.strip() for x in lines[l1 + 1 : l2]]
        parts += [lines[l2][:c2].strip()]
        body = " ".join(p for p in parts if p)
        new_line = "%s$$%s$$%s" % (lines[l1][:c1], body, lines[l2][c2 + 2 :])
        lines[l1 : l2 + 1] = [new_line]
        changed += 1
    return "\n".join(lines), changed


def collect(paths):
    files = []
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, names in os.walk(path):
                dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "node_modules")]
                for name in sorted(names):
                    if name.lower().endswith((".md", ".markdown")):
                        files.append(os.path.join(root, name))
        else:
            files.append(path)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description="检查 Markdown 数学公式是否适配 DSH 前端渲染器")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--fix", action="store_true", help="把跨行的 $$ 块并成单行")
    ap.add_argument("--dry-run", action="store_true", help="配合 --fix：只显示结果，不写回")
    args = ap.parse_args(argv)

    files = collect(args.paths)
    total_err = 0
    total_warn = 0
    changed_files = 0
    for path in files:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print("跳过 %s: %s" % (path, exc))
            continue
        if args.fix:
            new_text, changed = fix_text(text)
            if changed:
                changed_files += 1
                if not args.dry_run:
                    with open(path, "w", encoding="utf-8", newline="\n") as fh:
                        fh.write(new_text)
                print("[fix%s] %s：合并 %d 个跨行 $$ 块"
                      % ("-dry" if args.dry_run else "", path, changed))
                text = new_text
        issues, _ = analyze(text)
        errs = [i for i in issues if i[1] == "error"]
        warns = [i for i in issues if i[1] == "warn"]
        total_err += len(errs)
        total_warn += len(warns)
        if issues:
            print("")
            print("== %s ==" % path)
            for line_no, level, msg in issues:
                print("  %s  第 %d 行: %s" % ("ERROR" if level == "error" else "warn ", line_no, msg))

    print("")
    print("检查 %d 个文件：error %d，warn %d%s"
          % (len(files), total_err, total_warn,
             "，已修复 %d 个文件" % changed_files if args.fix else ""))
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
