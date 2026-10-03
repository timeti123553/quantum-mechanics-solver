#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""示例 01 的核验与作图脚本：一维有限深方势阱（深势阱）

    V(x) = 0   (|x| < a)
    V(x) = V0  (|x| > a)

无量纲量：xi = k a, eta = kappa a, R = a*sqrt(2 m V0)/hbar
偶宇称：eta = xi tan xi        奇宇称：eta = -xi cot xi        两者都满足 xi^2 + eta^2 = R^2

产物：
  * 控制台：R、束缚态个数（公式 vs 逐区间枚举）、各能级与无限深方阱对比、深势阱修正
  * 本目录：01-finite-square-well-graph.png、01-finite-square-well-levels.png

用法（用哪个 Python 启动都行，脚本会自动切换到装了 sympy/scipy/matplotlib 的解释器）：
    python 01-finite-square-well-check.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))
sys.dont_write_bytecode = True  # 不要把 __pycache__ 写进 skill 目录
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

import qmenv  # noqa: E402

qmenv.ensure(("sympy", "scipy", "matplotlib"))

import numpy as np  # noqa: E402
from scipy.optimize import brentq  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager, rcParams  # noqa: E402

GRAPH_PNG = os.path.join(HERE, "01-finite-square-well-graph.png")
LEVELS_PNG = os.path.join(HERE, "01-finite-square-well-levels.png")

_CJK = [n for n in ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC"]
        if n in {f.name for f in font_manager.fontManager.ttflist}]
if _CJK:
    rcParams["font.sans-serif"] = _CJK + list(rcParams["font.sans-serif"])
rcParams["axes.unicode_minus"] = False
rcParams["savefig.bbox"] = "tight"

# ---------------- 参数（GaAs/AlGaAs 量子阱）
m_e = 9.1093837015e-31
hbar = 1.054571817e-34
eV = 1.602176634e-19

m = 0.067 * m_e
a = 5.0e-9
V0 = 2.0 * eV

R = a * np.sqrt(2 * m * V0) / hbar
print("=" * 66)
print("一维有限深方势阱：m* = 0.067 m_e, 2a = %.1f nm, V0 = %.3f eV" % (2 * a * 1e9, V0 / eV))
print("R = a*sqrt(2mV0)/hbar = %.6f" % R)
N_even = int(np.ceil(R / np.pi))
N_odd = int(np.ceil(R / np.pi - 0.5))
print("束缚态个数：N_even = %d, N_odd = %d, 合计 %d ; 公式 ceil(2R/pi) = %d"
      % (N_even, N_odd, N_even + N_odd, int(np.ceil(2 * R / np.pi))))


# ---------------- 逐区间求根
def g_even(x):
    return x * np.tan(x) - np.sqrt(max(R * R - x * x, 0.0))


def g_odd(x):
    with np.errstate(divide="ignore", invalid="ignore"):
        return -x / np.tan(x) - np.sqrt(max(R * R - x * x, 0.0))


roots = []
for mm in range(int(np.ceil(2 * R / np.pi)) + 2):
    lo = mm * np.pi / 2 + 1e-12
    hi = min((mm + 1) * np.pi / 2 - 1e-12, R - 1e-12)
    if lo >= hi:
        continue
    f = g_even if mm % 2 == 0 else g_odd
    flo, fhi = f(lo), f(hi)
    if not np.isfinite(flo) or not np.isfinite(fhi) or flo * fhi >= 0:
        continue
    roots.append((mm, brentq(f, lo, hi, xtol=1e-15, rtol=8.9e-16),
                  "even" if mm % 2 == 0 else "odd"))

print("枚举得到的根（区间 m、xi=ka、宇称、xi^2+eta^2-R^2 残差）：")
levels = []
for mm, xi, par in roots:
    eta = xi * (np.tan(xi) if par == "even" else -1.0 / np.tan(xi))
    resid = xi * xi + eta * eta - R * R
    E = hbar**2 * (xi / a) ** 2 / (2 * m) / eV
    levels.append((xi, par, E, eta))
    print("  m=%d  xi=%9.6f  %-4s  E=%9.6f eV  eta=%8.4f  残差=%+.2e"
          % (mm, xi, par, E, eta, resid))

E_inf = [((n + 1) ** 2 * np.pi**2 * hbar**2 / (2 * m * (2 * a) ** 2)) / eV
         for n in range(len(levels))]
print("")
print("与同宽度无限深方阱 E_n^inf = n^2 pi^2 hbar^2/(8 m a^2) 对比：")
print("  n   E_finite(eV)   E_inf(eV)   比值     阱外衰减长度 a/eta")
for i, (xi, par, E, eta) in enumerate(levels, 1):
    print("  %d   %10.6f   %10.6f   %.5f   %.4f a" % (i, E, E_inf[i - 1], E / E_inf[i - 1], 1.0 / eta))

print("")
print("V0 以下的无限深阱能级数 = %d，有限深阱束缚态数 = %d（恒多 1 个）"
      % (int(np.sum(np.array(E_inf) < V0 / eV)), len(levels)))

E1_inf = E_inf[0]
est_lead = E1_inf * (1 - 2 / R)
est_refined = E1_inf * (R / (R + 1)) ** 2
print("深势阱修正（基态）：")
print("  零级      E1_inf               = %.6f eV   相对偏差 %.2e"
      % (E1_inf, abs(levels[0][2] / E1_inf - 1)))
print("  领头修正  E1_inf (1 - 2/R)     = %.6f eV   相对偏差 %.2e"
      % (est_lead, abs(levels[0][2] / est_lead - 1)))
print("  精细式    E1_inf [R/(R+1)]^2   = %.6f eV   相对偏差 %.2e"
      % (est_refined, abs(levels[0][2] / est_refined - 1)))
print("  实际      E1                   = %.6f eV" % levels[0][2])

# ---------------- 图 1：图形解 + 阱外指数尾
fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.6))

xi_grid = np.linspace(1e-4, R * 1.02, 4000)
with np.errstate(divide="ignore", invalid="ignore"):
    tan_curve = xi_grid * np.tan(xi_grid)
    cot_curve = -xi_grid / np.tan(xi_grid)
tan_curve[np.abs(tan_curve) > 12] = np.nan
cot_curve[np.abs(cot_curve) > 12] = np.nan
circle = np.sqrt(np.clip(R * R - xi_grid**2, 0, None))

axes[0].plot(xi_grid, np.clip(tan_curve, 0, 12), color="C0", lw=1.6, label=r"偶: $\eta=\xi\tan\xi$")
axes[0].plot(xi_grid, np.clip(cot_curve, 0, 12), color="C3", lw=1.6, label=r"奇: $\eta=-\xi\cot\xi$")
axes[0].plot(xi_grid, circle, "k--", lw=1.6, label=r"$\eta=\sqrt{R^2-\xi^2}$  ($R=%.2f$)" % R)
for mm, xi, par in roots:
    axes[0].plot([xi], [np.sqrt(max(R * R - xi * xi, 0.0))], "o", ms=7, mfc="gold", mec="k", zorder=5)
axes[0].set_xlim(0, R * 1.02)
axes[0].set_ylim(0, 12)
axes[0].set_xlabel(r"$\xi=ka$")
axes[0].set_ylabel(r"$\eta=\kappa a$")
axes[0].set_title("图形解：圆弧与两支曲线的交点即束缚态")
axes[0].legend(fontsize=9, loc="upper right")
axes[0].grid(alpha=0.25)

x = np.linspace(-2.2 * a, 2.2 * a, 4001)
for i, (xi, par, E, eta) in enumerate(levels):
    k, kappa = xi / a, eta / a
    inside = np.cos(k * x) if par == "even" else np.sin(k * x)
    tail = (np.cos(xi) if par == "even" else np.sign(x) * np.sin(xi)) * np.exp(-kappa * (np.abs(x) - a))
    psi = np.where(np.abs(x) <= a, inside, tail)
    psi = psi / np.sqrt(np.trapezoid(psi**2, x))
    axes[1].semilogy(x / a, np.abs(psi) * a**0.5 + 1e-8, lw=1.5,
                     label=r"$n=%d$ ($E=%.3f$ eV)" % (i + 1, E))
axes[1].axvline(-1, color="k", ls=":", lw=1.0)
axes[1].axvline(1, color="k", ls=":", lw=1.0)
axes[1].set_xlabel(r"$x/a$")
axes[1].set_ylabel(r"$|\psi_n|\,/\sqrt{a}$  （对数）")
axes[1].set_title("束缚态波函数（对数纵轴：阱外为直线 $\\propto e^{-\\kappa|x|}$）")
axes[1].legend(fontsize=8, ncol=2)
axes[1].grid(alpha=0.25, which="both")
fig.savefig(GRAPH_PNG, dpi=150)
plt.close(fig)
print("")
print("已保存: %s" % GRAPH_PNG)

# ---------------- 图 2：能级对比
fig, ax = plt.subplots(figsize=(5.6, 5.8))
for i, (xi, par, E, eta) in enumerate(levels):
    ax.hlines(E, 0.06, 0.42, color="C0", lw=2.4)
    ax.hlines(E_inf[i], 0.55, 0.91, color="C3", lw=2.0, ls="--")
    ax.text(0.44, E, "$n=%d$" % (i + 1), va="center", fontsize=9)
    ax.text(0.93, E, "%.3f" % E, va="center", fontsize=8)
ax.axhline(V0 / eV, color="k", lw=1.2)
ax.text(0.05, V0 / eV + 0.03, r"$V_0=%.1f$ eV" % (V0 / eV), fontsize=9)
ax.text(0.06, V0 / eV - 0.16, "有限深阱", fontsize=9, color="C0")
ax.text(0.55, V0 / eV - 0.16, "同宽无限深阱", fontsize=9, color="C3")
ax.set_xlim(0, 1.05)
ax.set_ylim(0, V0 / eV + 0.22)
ax.set_xticks([])
ax.set_ylabel("能量 (eV)")
ax.set_title("深势阱中的能级：向无限深阱能级靠拢")
fig.savefig(LEVELS_PNG, dpi=150)
plt.close(fig)
print("已保存: %s" % LEVELS_PNG)
