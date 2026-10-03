#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""示例 02 的核验与作图脚本：一维奇异谐振子 V(x) = V0 (a/x - x/a)^2

解析结果（本脚本用来验证它）：
    omega = sqrt(2 V0 /(m a^2)),   nu = m*omega/hbar,   Lambda = 2 m V0 a^2/hbar^2
    alpha = (1/2)(1 + sqrt(1 + 4 Lambda)) = (1/2)(1 + sqrt(1 + 8 m V0 a^2/hbar^2))
    E_n   = hbar*omega*(2n + alpha + 1/2) - 2 V0
    psi_n(x) = N_n x^alpha exp(-nu x^2/2) L_n^{(alpha-1/2)}(nu x^2)
    N_n      = sqrt(2 n! nu^{alpha+1/2} / Gamma(n + alpha + 1/2))

三项彼此独立的核验：
  1) 在 x 上直接三点有限差分（Dirichlet 边界）求最低若干能级 —— Dirichlet 边界给变分上界
  2) sympy 把解析 psi_0 代回定态方程，残差应恒等于 0
  3) 归一化常数数值积分 ∫|psi_n|^2 dx 应为 1

产物（写在本示例目录下）：
  02-isotonic-oscillator-graph.png      势阱 + 最低三个定态
  02-isotonic-oscillator-spectrum.png   解析 vs 数值能级

用法（用哪个 Python 启动都行，脚本会自动切换到装了 sympy/scipy/matplotlib 的解释器）：
    python 02-isotonic-oscillator-check.py
"""
import math
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
import sympy as sp  # noqa: E402
from scipy.linalg import eigh_tridiagonal  # noqa: E402
from scipy.special import gamma as gamma_fn  # noqa: E402
from scipy.special import genlaguerre  # noqa: E402
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager, rcParams  # noqa: E402

GRAPH_PNG = os.path.join(HERE, "02-isotonic-oscillator-graph.png")
SPECTRUM_PNG = os.path.join(HERE, "02-isotonic-oscillator-spectrum.png")

_CJK = [n for n in ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC"]
        if n in {f.name for f in font_manager.fontManager.ttflist}]
if _CJK:
    rcParams["font.sans-serif"] = _CJK + list(rcParams["font.sans-serif"])
rcParams["axes.unicode_minus"] = False
rcParams["savefig.bbox"] = "tight"

# ---------------- 参数（电子，a = 1 Å，V0 = 1 eV）
eV = 1.602176634e-19
hbar = 1.054571817e-34
m = 9.1093837015e-31
V0 = 1.0 * eV
a = 1.0e-10
NLEV = 4

Lam = 2 * m * V0 * a**2 / hbar**2
alpha = 0.5 * (1 + np.sqrt(1 + 4 * Lam))
hw = np.sqrt(2 * V0 * hbar**2 / (m * a**2))
nu = m * hw / hbar**2                       # 单位 1/m^2
E_an = np.array([hw * (2 * n + alpha + 0.5) - 2 * V0 for n in range(NLEV)]) / eV


def psi_exact(n, xs):
    """解析波函数（未归一化）：psi_n ∝ x^alpha exp(-nu x^2/2) L_n^{(alpha-1/2)}(nu x^2)"""
    return xs**alpha * np.exp(-nu * xs**2 / 2) * genlaguerre(n, alpha - 0.5)(nu * xs**2)


print("=" * 74)
print("V(x) = V0 (a/x - x/a)^2     参数: m = m_e, a = %.2f A, V0 = %.2f eV"
      % (a * 1e10, V0 / eV))
print("Lambda = 2 m V0 a^2/hbar^2 = %.6f" % Lam)
print("alpha  = %.6f     alpha(alpha-1) = %.6f  (= Lambda)" % (alpha, alpha * (alpha - 1)))
print("hbar*omega = %.6f eV       nu = %.6f A^-2" % (hw / eV, nu * 1e-20))
print("解析能级 E_n = hbar*omega(2n + alpha + 1/2) - 2V0：")
for n, e in enumerate(E_an):
    print("   n=%d   E = %12.6f eV" % (n, e))
print("相邻能级间距（应恒为 2*hbar*omega = %.6f eV）: %s"
      % (2 * hw / eV, np.round(np.diff(E_an), 6)))

# ---------------- 核验 1：x 上直接有限差分
T = hbar**2 / (2 * m)
x_min, x_max, N = 1e-3 * a, 10.0 * a, 160000
x = np.linspace(x_min, x_max, N + 2)
h = x[1] - x[0]
xi = x[1:-1]
diag = 2 * T / h**2 + V0 * (a / xi - xi / a) ** 2
off = np.full(N - 1, -T / h**2)
vals = eigh_tridiagonal(diag, off, select="i", select_range=(0, NLEV - 1))[0] / eV

print("")
print("核验 1 —— 直接有限差分（N=%d, x∈[%.0e, %.0f]a）:" % (N, x_min / a, x_max / a))
for n in range(NLEV):
    print("   n=%d   数值 = %12.6f eV   解析 = %12.6f eV   相对偏差 = %.2e"
          % (n, vals[n], E_an[n], abs(vals[n] / E_an[n] - 1)))
print("   最大相对偏差 = %.2e ；数值均不低于解析（变分上界）= %s"
      % (max(abs(vals / E_an - 1)), bool(np.all(vals >= E_an - 1e-9))))

# ---------------- 核验 2：sympy 精确残差
xs_, a_, m_, hb_, nu_, al_ = sp.symbols("x a m hbar nu alpha", positive=True)
psi_s = xs_**al_ * sp.exp(-nu_ * xs_**2 / 2)
V0_s = hb_**2 * al_ * (al_ - 1) / (2 * m_ * a_**2)      # 由 alpha(alpha-1) = 2 m V0 a^2/hbar^2
E_s = hb_**2 * nu_ * (al_ + sp.Rational(1, 2)) / m_ - hb_**2 * al_ * (al_ - 1) / (m_ * a_**2)
resid_raw = sp.simplify(-hb_**2 / (2 * m_) * sp.diff(psi_s, xs_, 2)
                        + V0_s * (a_ / xs_ - xs_ / a_) ** 2 * psi_s - E_s * psi_s)
resid = sp.simplify(resid_raw.subs(nu_, sp.sqrt(al_ * (al_ - 1)) / a_**2))
print("")
print("核验 2 —— sympy 精确核验：ψ_0 代回方程并代入 ν=√(α(α-1))/a² 后残差 = %s  ->  %s"
      % (resid, "恒等于 0" if resid == 0 else "非零（有问题）"))

# ---------------- 核验 3：归一化
xg = np.linspace(1e-8 * a, 12.0 * a, 400000)
print("")
print("核验 3 —— 归一化 N_n = sqrt(2 n! ν^(α+1/2)/Γ(n+α+1/2))：")
for n in range(NLEV):
    Nn = np.sqrt(2 * math.factorial(n) * nu ** (alpha + 0.5) / gamma_fn(n + alpha + 0.5))
    print("   n=%d   ∫|ψ_n|²dx = %.8f" % (n, np.trapezoid((Nn * psi_exact(n, xg)) ** 2, xg)))

# ---------------- 图 1：势阱 + 能级 + 波函数
fig, ax = plt.subplots(figsize=(7.6, 4.8))
xp = np.linspace(0.16, 8.0, 3000) * a
ax.plot(xp / a, (V0 / eV) * (a / xp - xp / a) ** 2, "k-", lw=1.6,
        label=r"$V(x)=V_0(a/x-x/a)^2$")
colors = ["C0", "C1", "C2"]
for n in range(3):
    ax.axhline(E_an[n], color=colors[n], lw=1.0, ls=":")
    ax.text(6.35, E_an[n] + 1.1, r"$n=%d$: %.2f eV" % (n, E_an[n]), fontsize=9, color=colors[n])
    psi = psi_exact(n, xp)
    ax.plot(xp / a, E_an[n] + 5.0 * psi / np.max(np.abs(psi)), color=colors[n], lw=1.5)
ax.set_xlim(0.16, 8.0)
ax.set_ylim(-1, 34)
ax.set_xlabel(r"$x/a$")
ax.set_ylabel("能量 (eV)")
ax.set_title(r"势阱与最低三个定态（曲线为 $\psi_n$，按 $E_n$ 偏移）")
ax.legend(fontsize=9, loc="upper center")
ax.grid(alpha=0.25)
fig.savefig(GRAPH_PNG, dpi=150)
plt.close(fig)
print("")
print("已保存: %s" % GRAPH_PNG)

# ---------------- 图 2：解析 vs 数值
fig, ax = plt.subplots(figsize=(5.6, 4.6))
idx = np.arange(NLEV)
ax.bar(idx - 0.2, E_an, width=0.4, color="C0", label="解析")
ax.bar(idx + 0.2, vals, width=0.4, color="C3", label="数值（x 上直接 FD）")
for n in idx:
    ax.text(n, max(E_an[n], vals[n]) + 0.8, "%.1e" % abs(vals[n] / E_an[n] - 1),
            ha="center", fontsize=8)
ax.set_xticks(idx)
ax.set_xticklabels([r"$n=%d$" % n for n in idx])
ax.set_ylabel("能量 (eV)")
ax.set_title("解析 vs 数值（标注相对偏差）")
ax.legend(fontsize=9)
ax.grid(alpha=0.25, axis="y")
fig.savefig(SPECTRUM_PNG, dpi=150)
plt.close(fig)
print("已保存: %s" % SPECTRUM_PNG)
