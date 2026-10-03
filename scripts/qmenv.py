#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""qmenv.py — 解释器与依赖解析（qm.py / qmplot.py 共用）

目的：让 `python scripts/qm.py ...` 无论用哪个 python 启动，都能自动切换到一个
装有 sympy / matplotlib 的解释器上运行。

解析顺序：
  1. 环境变量 QM_PYTHON
  2. 本 skill 的 references/local/env.md 中形如 `python: <路径>` 的行
  3. 常见安装位置（miniconda / anaconda / 用户级 Python）
  4. 当前解释器

也可直接运行查看解析结果：
  python qmenv.py [--need sympy,matplotlib]
"""
from __future__ import annotations

import argparse
import glob
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
ENV_MD = os.path.join(SKILL_ROOT, "references", "local", "env.md")


def _norm(path):
    try:
        return os.path.normcase(os.path.abspath(path))
    except Exception:
        return path


def has_current(need):
    """当前解释器是否具备 need 中的全部模块。"""
    for mod in need:
        try:
            if importlib.util.find_spec(mod) is None:
                return False
        except (ImportError, ValueError):
            return False
    return True


def has_modules(py, need, timeout=120):
    """指定解释器是否具备 need 中的全部模块（不创建管道，沙箱下也安全）。"""
    if not py or not os.path.isfile(py):
        return False
    if _norm(py) == _norm(sys.executable):
        return has_current(need)
    code = "; ".join("import %s" % m for m in need) or "pass"
    try:
        proc = subprocess.run(
            [py, "-c", code],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
        )
    except Exception:
        return False
    return proc.returncode == 0


def _from_env_md():
    out = []
    try:
        with open(ENV_MD, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"^\s*[-*]?\s*python\s*[:：]\s*(.+?)\s*$", line, re.I)
                if m:
                    cand = m.group(1).strip().strip("`").strip().strip('"').strip("'")
                    if cand and cand.lower() not in ("n/a", "none", "-"):
                        out.append(cand)
    except OSError:
        pass
    return out


def _common_paths():
    home = os.path.expanduser("~")
    local = os.environ.get("LOCALAPPDATA", "")
    cands = [
        r"C:\ProgramData\miniconda3\python.exe",
        r"C:\ProgramData\anaconda3\python.exe",
        r"C:\ProgramData\Miniconda3\python.exe",
        r"C:\ProgramData\Anaconda3\python.exe",
        os.path.join(home, "miniconda3", "python.exe"),
        os.path.join(home, "Miniconda3", "python.exe"),
        os.path.join(home, "anaconda3", "python.exe"),
        os.path.join(home, "Anaconda3", "python.exe"),
        os.path.join(local, "miniconda3", "python.exe"),
        os.path.join(local, "Continuum", "anaconda3", "python.exe"),
    ]
    if local:
        cands += sorted(
            glob.glob(os.path.join(local, "Programs", "Python", "Python3*", "python.exe")),
            reverse=True,
        )
    cands += [r"C:\Python313\python.exe", r"C:\Python312\python.exe", r"C:\Python311\python.exe"]
    return cands


def candidates():
    """按解析顺序返回去重后的候选解释器路径。"""
    raw = [os.environ.get("QM_PYTHON")]
    raw += _from_env_md()
    raw += _common_paths()
    raw.append(sys.executable)
    seen, out = set(), []
    for path in raw:
        if not path:
            continue
        key = _norm(path)
        if key in seen:
            continue
        seen.add(key)
        out.append(os.path.abspath(path))
    return out


def resolve(need=("sympy",)):
    """返回第一个具备 need 的解释器路径；都没有则返回 None。"""
    for py in candidates():
        if has_modules(py, need):
            return py
    return None


def ensure(need=("sympy",)):
    """确保当前解释器具备 need；否则用解析到的解释器重启当前脚本。

    返回实际应当使用的解释器路径（不重启时就是 sys.executable）。
    """
    need = tuple(need)
    if has_current(need):
        return sys.executable
    if os.environ.get("QM_RELAUNCHED") == "1":
        sys.stderr.write(
            "[qmenv] 提示：已切换到 %s，但仍缺少 %s。\n" % (sys.executable, "/".join(need))
        )
        return sys.executable
    target = resolve(need)
    if target and _norm(target) != _norm(sys.executable):
        env = dict(os.environ)
        env["QM_RELAUNCHED"] = "1"
        env["QM_PYTHON"] = target
        script = os.path.abspath(sys.argv[0])
        sys.stderr.write(
            "[qmenv] 当前解释器缺少 %s，自动改用 %s 运行。\n" % ("/".join(need), target)
        )
        sys.stderr.flush()
        rc = subprocess.call(
            [target, "-X", "utf8", script] + sys.argv[1:],
            env=env,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        sys.exit(rc)
    sys.stderr.write(
        "[qmenv] 找不到同时具备 %s 的解释器，将用当前解释器继续（可能报 ModuleNotFoundError）。\n"
        % "/".join(need)
    )
    sys.stderr.write("[qmenv] 可用 `python scripts/qmenv.py` 查看候选清单；或用 QM_PYTHON 指定。\n")
    return sys.executable


def main():
    ap = argparse.ArgumentParser(description="解析本机可用于本 skill 的 Python 解释器")
    ap.add_argument("--need", default="sympy,matplotlib", help="逗号分隔的必需模块（默认 sympy,matplotlib）")
    args = ap.parse_args()
    need = tuple(x.strip() for x in args.need.split(",") if x.strip())

    print("环境文件           : %s (%s)" % (ENV_MD, "存在" if os.path.isfile(ENV_MD) else "不存在"))
    print("当前解释器         : %s" % sys.executable)
    print("当前解释器具备需求 : %s" % has_current(need))
    hit = resolve(need)
    print("解析结果           : %s" % (hit or "(未找到)"))
    print("候选清单（[OK] 表示具备 %s）：" % ",".join(need))
    for py in candidates():
        print("  [%s] %s" % ("OK" if has_modules(py, need) else "  ", py))
    return 0 if hit else 1


if __name__ == "__main__":
    sys.exit(main())
