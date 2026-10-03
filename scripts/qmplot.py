#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""qmplot.py — 量子力学常用图像（matplotlib, Agg 后端）

子命令：
  well        一维无限深方阱的 ψ_n 与 |ψ_n|²
  harmonic    谐振子的 ψ_n 与势能+能级
  custom      任意函数绘图（sympy 表达式，多个用 ';' 分隔）
  levels      能级图（可标简并度）
  wavepacket  自由高斯波包的时间演化

示例：
  python qmplot.py well --L 1 --n 1,2,3 --out well.png
  python qmplot.py harmonic --n 0,1,2,3 --out sho.png
  python qmplot.py levels --energies "1,4,9,16" --out levels.png
  python qmplot.py custom --expr "exp(-x^2); x^2*exp(-x^2)" --xrange -3,3 --out custom.png
  python qmplot.py wavepacket --x0 0 --sigma 0.4 --k0 2 --times 0,1,2,4 --out packet.png
"""
from __future__ import annotations

import argparse
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.dont_write_bytecode = True  # 不要把 __pycache__ 写进 skill 目录

import qmenv  # noqa: E402

qmenv.ensure(("sympy", "matplotlib"))

import numpy as np  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager, rcParams  # noqa: E402

_CJK_CANDIDATES = [
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "WenQuanYi Zen Hei",
]
_available = {f.name for f in font_manager.fontManager.ttflist}
CJK = [n for n in _CJK_CANDIDATES if n in _available]
if CJK:
    rcParams["font.sans-serif"] = CJK + list(rcParams["font.sans-serif"])
rcParams["axes.unicode_minus"] = False
rcParams["figure.dpi"] = 120
rcParams["savefig.bbox"] = "tight"


def L(zh, en):
    """中英文标签：本机有中文字体时用中文，否则退回英文（避免方框）。"""
    return zh if CJK else en


def _save(fig, out, dpi):
    fig.savefig(out, dpi=dpi)
    plt.close(fig)
    print("已保存图像: %s" % out)


def _parse_list(text, dtype=float):
    return [dtype(s.strip()) for s in str(text).split(",") if s.strip()]


def _trapz(y, x, axis=-1):
    """兼容 numpy 1.x/2.x 的梯形积分（np.trapz 在 2.x 改名 np.trapezoid）。"""
    fn = getattr(np, "trapezoid", None) or getattr(np, "trapz")
    return fn(y, x, axis=axis)


# ---------------------------------------------------------------- well


def cmd_well(args):
    Lw = args.L
    ns = _parse_list(args.n, int)
    x = np.linspace(0.0, Lw, args.points)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for n in ns:
        psi = np.sqrt(2.0 / Lw) * np.sin(n * np.pi * x / Lw)
        axes[0].plot(x, psi, label="$n=%d$" % n)
        axes[1].plot(x, psi**2, label="$n=%d$" % n)
    axes[0].axhline(0, color="k", lw=0.6)
    axes[0].set_title(L("无限深方阱：波函数 $\\psi_n(x)$", "Infinite well: $\\psi_n(x)$"))
    axes[0].set_ylabel("$\\psi_n$")
    axes[1].set_title(L("概率密度 $|\\psi_n|^2$", "Probability density $|\\psi_n|^2$"))
    axes[1].set_ylabel("$|\\psi_n|^2$")
    for ax in axes:
        ax.set_xlabel("$x$")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=9)
    _save(fig, args.out, args.dpi)
    return 0


# ---------------------------------------------------------------- harmonic


def cmd_harmonic(args):
    from numpy.polynomial.hermite import hermval  # noqa: PLC0415

    ns = _parse_list(args.n, int)
    xi = np.linspace(-args.xmax, args.xmax, args.points)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for n in ns:
        coeffs = np.zeros(n + 1)
        coeffs[n] = 1.0
        Hn = hermval(xi, coeffs)
        psi = np.pi ** -0.25 / np.sqrt(2.0**n * float(math.factorial(n))) * Hn * np.exp(-(xi**2) / 2.0)
        axes[0].plot(xi, psi, label="$n=%d$" % n)
        axes[1].axhline(n + 0.5, lw=1.0)
        axes[1].text(args.xmax * 0.72, n + 0.6, "$n=%d$" % n, fontsize=9)
    vx = np.linspace(-args.xmax, args.xmax, args.points)
    axes[1].plot(vx, 0.5 * vx**2, "k--", lw=1.0, label=L("势能 $V(x)$", "potential $V(x)$"))
    axes[1].set_ylim(0, max(1.0, float(max(ns)) + 2.0))
    axes[0].set_title(L("谐振子波函数 $\\psi_n$", "Harmonic oscillator $\\psi_n$"))
    axes[0].set_ylabel("$\\psi_n(\\xi)$")
    axes[1].set_title(L("势能与能级 $E_n=(n+\\frac{1}{2})\\hbar\\omega$", "Levels $E_n=(n+1/2)\\hbar\\omega$"))
    axes[1].legend(fontsize=9)
    for ax in axes:
        ax.set_xlabel("$\\xi=\\sqrt{m\\omega/\\hbar}\\,x$")
        ax.grid(alpha=0.25)
    axes[0].legend(fontsize=9)
    _save(fig, args.out, args.dpi)
    return 0


# ---------------------------------------------------------------- custom


def cmd_custom(args):
    import sympy as sp  # noqa: PLC0415

    lo, hi = _parse_list(args.xrange)
    x = np.linspace(lo, hi, args.points)
    sym = sp.Symbol("x", real=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    exprs = [e.strip() for e in args.expr.split(";") if e.strip()]
    for i, text in enumerate(exprs):
        try:
            func = sp.lambdify(sym, sp.sympify(text.replace("^", "**")), "numpy")
            y = func(x)
        except Exception as exc:  # noqa: BLE001
            print("表达式 %s 处理失败：%s" % (text, exc))
            continue
        y = np.asarray(y)
        if np.iscomplexobj(y):
            if args.abs:
                y = np.abs(y)
            else:
                print("提示：%s 为复值，绘制其实部（用 --abs 可画模）。" % text)
                y = np.real(y)
        elif args.abs:
            y = np.abs(y)
        ax.plot(x, np.asarray(y, dtype=float), label=text)
    if not exprs:
        print("请用 --expr 给出至少一个表达式。")
        return 2
    if args.ylim:
        y0, y1 = _parse_list(args.ylim)
        ax.set_ylim(y0, y1)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel("$x$")
    ax.set_ylabel(L("函数值", "value"))
    ax.set_title(args.title or L("自定义曲线", "Custom plot"))
    ax.grid(alpha=0.25)
    ax.legend(fontsize=9)
    _save(fig, args.out, args.dpi)
    return 0


# ---------------------------------------------------------------- levels


def cmd_levels(args):
    energies = _parse_list(args.energies)
    degs = _parse_list(args.degeneracy, int) if args.degeneracy else [1] * len(energies)
    if len(degs) < len(energies):
        degs = degs + [1] * (len(energies) - len(degs))
    fig, ax = plt.subplots(figsize=(5.2, 5.6))
    for i, (e, d) in enumerate(zip(energies, degs)):
        for j in range(d):
            x0 = 0.08 + 0.14 * j
            ax.hlines(e, x0, x0 + 0.07, lw=2.0, color="C%d" % (i % 10))
        label = "$E_{%d}=%g$" % (i, e)
        if d > 1:
            label += L("（简并度 %d）" % d, " (deg %d)" % d)
        ax.text(0.30 + 0.14 * (d - 1), e, label, va="center", fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_ylabel(L("能量", "energy"))
    ax.set_title(args.title or L("能级图", "Energy levels"))
    ax.grid(axis="y", alpha=0.25)
    _save(fig, args.out, args.dpi)
    return 0


# ---------------------------------------------------------------- wavepacket


def cmd_wavepacket(args):
    sigma = args.sigma
    x0 = args.x0
    k0 = args.k0
    hbar = args.hbar
    mass = args.mass
    lo, hi = _parse_list(args.xrange)
    x = np.linspace(lo, hi, args.points)

    half_width = 4.0 / sigma
    k = np.linspace(k0 - half_width, k0 + half_width, 4 * args.points)
    phi = (2.0 * sigma**2 / np.pi) ** 0.25 * np.exp(-(sigma**2) * (k - k0) ** 2) * np.exp(-1j * k * x0)

    times = _parse_list(args.times)
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    for t in times:
        integrand = phi[None, :] * np.exp(1j * (k[None, :] * x[:, None] - hbar * k[None, :] ** 2 * t / (2.0 * mass)))
        psi = _trapz(integrand, k, axis=1) / np.sqrt(2.0 * np.pi)
        if args.psi_real:
            ax.plot(x, np.real(psi), lw=1.2, label="$t=%g$" % t)
        else:
            ax.plot(x, np.abs(psi) ** 2, lw=1.5, label="$t=%g$" % t)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$|\\psi(x,t)|^2$" if not args.psi_real else "$\\mathrm{Re}\\,\\psi(x,t)$")
    ax.set_title(L("自由高斯波包演化（$\\hbar=m=1$）", "Free Gaussian packet ($\\hbar=m=1$)"))
    ax.grid(alpha=0.25)
    ax.legend(fontsize=9)
    _save(fig, args.out, args.dpi)
    return 0


# ---------------------------------------------------------------- CLI


def build_parser():
    ap = argparse.ArgumentParser(prog="qmplot.py", description="量子力学常用图像")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--out", default=None, help="输出图片路径")
        p.add_argument("--dpi", type=int, default=150)
        p.add_argument("--points", type=int, default=800)

    p = sub.add_parser("well", help="一维无限深方阱")
    p.add_argument("--L", type=float, default=1.0)
    p.add_argument("--n", default="1,2,3")
    common(p)
    p.set_defaults(func=cmd_well, out="qm_well.png")

    p = sub.add_parser("harmonic", help="谐振子")
    p.add_argument("--n", default="0,1,2")
    p.add_argument("--xmax", type=float, default=5.0)
    common(p)
    p.set_defaults(func=cmd_harmonic, out="qm_harmonic.png")

    p = sub.add_parser("custom", help="任意函数")
    p.add_argument("--expr", required=True, help="sympy 表达式，多个用 ';' 分隔")
    p.add_argument("--xrange", default="-5,5")
    p.add_argument("--ylim", default=None)
    p.add_argument("--title", default=None)
    p.add_argument("--abs", action="store_true", help="画 |f(x)|")
    p.add_argument("--real", action="store_true", help="只取实部")
    common(p)
    p.set_defaults(func=cmd_custom, out="qm_custom.png")

    p = sub.add_parser("levels", help="能级图")
    p.add_argument("--energies", required=True, help="逗号分隔，如 \"1,4,9,16\"")
    p.add_argument("--degeneracy", default=None)
    p.add_argument("--title", default=None)
    common(p)
    p.set_defaults(func=cmd_levels, out="qm_levels.png")

    p = sub.add_parser("wavepacket", help="自由高斯波包演化")
    p.add_argument("--x0", type=float, default=0.0)
    p.add_argument("--k0", type=float, default=2.0)
    p.add_argument("--sigma", type=float, default=0.4)
    p.add_argument("--times", default="0,1,2,4")
    p.add_argument("--hbar", type=float, default=1.0)
    p.add_argument("--mass", type=float, default=1.0)
    p.add_argument("--xrange", default="-12,12")
    p.add_argument("--psi-real", action="store_true", help="画 Re ψ 而不是 |ψ|²")
    common(p)
    p.set_defaults(func=cmd_wavepacket, out="qm_wavepacket.png")

    return ap


def _value_options(parser):
    """收集所有子命令里「需要一个值」的选项字符串（含短选项）。"""
    opts, stack = set(), [parser]
    while stack:
        current = stack.pop()
        for act in getattr(current, "_actions", []):
            if act.option_strings and act.nargs is None:
                opts.update(act.option_strings)
            choices = getattr(act, "choices", None)
            if isinstance(choices, dict):
                stack.extend(choices.values())
    return opts


def _normalize_argv(argv, opts):
    """把 `--xrange -3,3`、`--ylim -1,1` 改写成 `--xrange=-3,3` 形式。

    只对「需要值」的选项生效：紧跟其后的 token 一律当作它的值（与 argparse 的取值
    规则本身一致，只是补上以 `-` 开头的情形）。
    """
    out, i = [], 0
    while i < len(argv):
        tok = argv[i]
        out.append(tok)
        i += 1
        if tok in opts and i < len(argv) and argv[i].startswith("-"):
            out[-1] = "%s=%s" % (tok, argv[i])
            i += 1
    return out


def main(argv=None):
    ap = build_parser()
    raw = list(sys.argv[1:] if argv is None else argv)
    raw = _normalize_argv(raw, _value_options(ap))
    args = ap.parse_args(raw)
    if not getattr(args, "out", None):
        args.out = "qm_plot.png"
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
