#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""qm.py — 量子力学习题符号/数值工具箱（sympy 驱动）

用于**校验手写推导**：定积分、归一化与期望值、本征系统、ODE、级数、极限、
对易关系、数值代入。

子命令：
  symbols     打印可用符号与约定
  integrate   定/不定积分
  expect      归一化常数、<x>、<x^2>、<p>、<p^2>、Δx、Δp、区间概率
  solve       解方程（代数/超越）
  dsolve      解 ODE（薛定谔方程），支持边界条件
  eigen       矩阵本征值/本征矢 + 简并度
  series      泰勒/洛朗展开
  limit       极限
  simplify    化简
  commute     对易子（支持自定义复合算符）
  check       数值代入校验

示例：
  python qm.py symbols
  python qm.py integrate "x**2*sin(n*pi*x/L)**2" -v x -a 0 -b L
  python qm.py expect "sin(n*pi*x/L)" -v x -a 0 -b L --prob-range 0,L/2
  python qm.py dsolve "psi'' + k**2*psi = 0" -f psi -v x --ics "psi(0)=0, psi(L)=0"
  python qm.py eigen "[[E1, V],[V, E2]]"
  python qm.py commute Lx Ly --def "Lx=y*pz-z*py" --def "Ly=z*px-x*pz"
  python qm.py check "sqrt(2/L)*sin(pi*x/L)" --subs "L=1, x=0.5" --expected 1.41421

表达式语法：sympy 语法，支持 `^` 表示乘方、隐式乘法（`2x`、`n pi x/L`）。
"""
from __future__ import annotations

import argparse
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

qmenv.ensure(("sympy",))

import sympy as sp  # noqa: E402
from sympy.parsing.sympy_parser import (  # noqa: E402
    convert_xor,
    implicit_multiplication,
    parse_expr,
    rationalize,
    standard_transformations,
)

# 注意：这里刻意不用 implicit_multiplication_application —— 它会把 `V0`、`E2` 这类
# 「符号+数字」的名字拆成乘积（V*0 = 0），对物理题是灾难性的。
TRANSFORMS = standard_transformations + (
    convert_xor,
    rationalize,
    implicit_multiplication,
)

PLAIN = False  # 由 --plain-symbols 置位

# ---------------------------------------------------------------- 符号表


def _build_symbols():
    s = {}
    real = ["x", "y", "z", "t", "theta", "phi", "xi", "eta"]
    real += ["b", "c", "d", "k", "p", "E", "V", "beta", "gamma", "delta", "eps", "epsilon"]
    real += ["mu", "tau", "A", "B", "C", "e", "x0", "p0", "R", "r0", "Omega", "Delta", "V0", "g"]
    for name in real:
        s[name] = sp.Symbol(name, real=True)
    pos = ["a", "L", "N", "Z", "omega", "nu", "sigma", "alpha", "lambda_", "k_B", "T"]
    pos += ["I_", "a0", "hbar", "m", "kappa", "sigma_x", "sigma_p", "w"]
    for name in pos:
        s[name] = sp.Symbol(name, positive=True)
    s["r"] = sp.Symbol("r", nonnegative=True)
    s["n"] = sp.Symbol("n", integer=True, positive=True)
    s["mm"] = sp.Symbol("mm", integer=True, positive=True)
    s["l"] = sp.Symbol("l", integer=True, nonnegative=True)
    s["j"] = sp.Symbol("j", integer=True, nonnegative=True)
    s["s_"] = sp.Symbol("s_", integer=True, nonnegative=True)
    s["q"] = sp.Symbol("q", integer=True)
    s["m_l"] = sp.Symbol("m_l", integer=True)
    s["m_s"] = sp.Symbol("m_s", real=True)
    return s


SYMS = _build_symbols()


_NAME_DIGIT = re.compile(r"\b([A-Za-z_][A-Za-z_]*?)(\d+)\b")


def _protect_names(text):
    """把 `E1` 改写成 `E_1`，避免解析器把「符号 + 数字」拆成乘积。

    已经定义过的名字（如 `V0`、`a0`、`m_l`）原样保留。
    """

    def repl(m):
        whole, base, digits = m.group(0), m.group(1), m.group(2)
        if whole in SYMS:
            return whole
        if base in SYMS:
            return "%s_%s" % (base, digits)
        return whole

    return _NAME_DIGIT.sub(repl, text)


def P(text, plain=None):
    """解析用户输入的表达式。"""
    if plain is None:
        plain = PLAIN
    if not plain:
        text = _protect_names(text)
    local = {} if plain else dict(SYMS)
    return parse_expr(text, local_dict=local, transformations=TRANSFORMS, evaluate=True)


def fmt(expr, pretty=False):
    expr = sp.simplify(expr)
    if pretty:
        return sp.pretty(expr)
    return sp.sstr(expr)


def _num(expr):
    try:
        val = complex(sp.N(expr, 12))
    except Exception:
        return None
    if abs(val.imag) < 1e-12:
        return val.real
    return val


# ---------------------------------------------------------------- symbols


def cmd_symbols(args):
    print("表达式语法：sympy 语法；`^` 等同 `**`；支持隐式乘法（2x、n pi x/L）。")
    print("")
    print("已预定义符号（带常用假设）：")

    def tag(sym):
        if sym.is_integer and sym.is_positive:
            return "正整数"
        if sym.is_integer and sym.is_nonnegative:
            return "非负整数"
        if sym.is_integer:
            return "整数"
        if sym.is_positive:
            return "正数"
        if sym.is_nonnegative:
            return "非负数"
        if sym.is_real:
            return "实数"
        return "无假设"

    groups = {}
    for name, sym in sorted(SYMS.items()):
        groups.setdefault(tag(sym), []).append(name)
    for key in ["正整数", "非负整数", "整数", "正数", "非负数", "实数", "无假设"]:
        if key in groups:
            print("  %-8s %s" % (key, ", ".join(groups[key])))
    print("")
    print("约定与提醒：")
    print("  * hbar 为符号（正数）；需要取 1 时用 --subs 或命令的数值参数。")
    print("  * m 是质量（正数）；磁量子数请写 m_l / m_s，求和指标用 mm。")
    print("  * e 是电荷（实数）；自然常数请写 exp(1)，指数函数写 exp(...)。")
    print("  * E 是能量（实数）；不要用 E 表示电场，电场请写 EE。")
    print("  * 假设不合适时加 --plain-symbols，所有符号退化为无假设符号。")
    return 0


# ---------------------------------------------------------------- integrate


def cmd_integrate(args):
    var = P(args.var)
    expr = P(args.expr)
    print("被积函数 : %s" % fmt(expr))
    if (args.lower is None) != (args.upper is None):
        print("错误：-a/--lower 与 -b/--upper 必须同时给出或同时省略。")
        return 2
    try:
        if args.lower is None:
            res = sp.integrate(expr, var)
            print("不定积分 : ∫ %s d%s = %s" % (fmt(expr), args.var, fmt(res)))
        else:
            lo, hi = P(args.lower), P(args.upper)
            res = sp.integrate(expr, (var, lo, hi))
            print("积分区间 : [%s, %s]" % (args.lower, args.upper))
            print("定积分   : %s" % fmt(res))
    except Exception as exc:  # noqa: BLE001
        print("符号积分失败：%s: %s" % (type(exc).__name__, exc))
        res = None
    if res is not None:
        if res.has(sp.Integral) or args.numeric:
            try:
                val = sp.N(res, 12)
                print("数值     : %s" % val)
            except Exception:  # noqa: BLE001
                pass
        else:
            n = _num(res)
            if n is not None and not res.free_symbols:
                print("数值     : %s" % ("%.10g" % n))
        if isinstance(res, sp.Piecewise):
            print("提示：结果是分段函数，通常因符号假设不足；可加 --plain-symbols 或直接代入具体 n 再看。")
    return 0 if res is not None else 1


# ---------------------------------------------------------------- expect


def _dens(psi, var, real_psi):
    """返回 |psi|^2（必要时按实波函数处理）。"""
    prod = sp.simplify(sp.conjugate(psi) * psi)
    if prod.has(sp.conjugate):
        if real_psi:
            return sp.simplify(psi**2), True
        prod2 = sp.simplify(sp.expand_complex(prod))
        if prod2.has(sp.conjugate):
            return sp.simplify(psi**2), True
        return prod2, False
    return prod, False


def cmd_expect(args):
    var = P(args.var)
    psi = P(args.psi)
    if args.lower is None or args.upper is None:
        print("错误：expect 需要 -a/--lower 与 -b/--upper 指定积分区间。")
        return 2
    lo, hi = P(args.lower), P(args.upper)
    dens, assumed_real = _dens(psi, var, args.real_psi)

    norm = sp.integrate(dens, (var, lo, hi))
    if norm.has(sp.Integral):
        print("归一化积分无法解析求解，请检查区间或加 --plain-symbols。")
        return 1
    if sp.simplify(norm) == 0:
        print("错误：∫|ψ|² = 0，波函数或区间有误。")
        return 1
    N = sp.simplify(1 / sp.sqrt(norm))

    m = SYMS["m"]
    hb = SYMS["hbar"]
    dpsi = sp.diff(psi, var)
    ddpsi = sp.diff(psi, var, 2)

    def avg(op_expr):
        val = sp.integrate(sp.conjugate(psi) * op_expr, (var, lo, hi))
        if val.has(sp.conjugate):
            val = sp.integrate(sp.simplify(psi * op_expr), (var, lo, hi))
        return sp.simplify(val / norm)

    x = var
    x1 = avg(x * psi)
    x2 = avg(x**2 * psi)
    p1 = avg(-sp.I * hb * dpsi)
    p2 = avg(-(hb**2) * ddpsi)

    dx2 = sp.simplify(x2 - x1**2)
    dp2 = sp.simplify(p2 - p1**2)

    def safe_sqrt(e):
        e = sp.simplify(e)
        try:
            return sp.simplify(sp.sqrt(e))
        except Exception:  # noqa: BLE001
            return sp.sqrt(e)

    dx = safe_sqrt(dx2)
    dp = safe_sqrt(dp2)

    print("波函数   : ψ = %s" % fmt(psi))
    print("区间     : [%s, %s]" % (args.lower, args.upper))
    if assumed_real:
        print("提示     : 已按**实波函数**处理（否则请用 --plain-symbols 指定完整假设）。")
    print("")
    print("归一化   : N = %s" % fmt(N))
    print("           N·ψ = %s" % fmt(sp.simplify(N * psi)))
    print("  <x>    = %s" % fmt(x1))
    print("  <x^2>  = %s" % fmt(x2))
    print("  Δx     = %s" % fmt(dx))
    print("  <p>    = %s" % fmt(p1))
    print("  <p^2>  = %s" % fmt(p2))
    print("  Δp     = %s" % fmt(dp))
    print("  <T>    = <p^2>/2m = %s" % fmt(sp.simplify(p2 / (2 * m))))
    print("  Δx·Δp  = %s   (需 ≥ ħ/2 = %s)" % (fmt(sp.simplify(dx * dp)), fmt(hb / 2)))
    prod_ratio = sp.simplify(dx * dp / (hb / 2))
    print("  Δx·Δp /(ħ/2) = %s" % fmt(prod_ratio))

    if args.prob_range:
        try:
            c, d = [s.strip() for s in args.prob_range.split(",")]
            pc, pd = P(c), P(d)
            prob = sp.simplify(sp.integrate(dens, (var, pc, pd)) / norm)
            print("")
            print("P(%s < %s < %s) = %s" % (c, args.var, d, fmt(prob)))
        except Exception as exc:  # noqa: BLE001
            print("区间概率计算出错：%s" % exc)

    n1, n2 = _num(x1), _num(sp.simplify(dx * dp / hb))
    if n1 is not None or n2 is not None:
        print("")
        if n1 is not None:
            print("数值     : <x> = %.10g" % n1)
        if n2 is not None:
            print("数值     : Δx·Δp/ħ = %.10g  (需 ≥ 0.5)" % n2)
    return 0


# ---------------------------------------------------------------- solve / dsolve


def cmd_solve(args):
    var = P(args.var)
    expr = P(args.expr)
    print("方程     : %s = 0" % fmt(expr))
    try:
        sols = sp.solve(expr, var)
    except Exception as exc:  # noqa: BLE001
        print("solve 失败：%s" % exc)
        return 1
    if not sols:
        print("解析解为空；尝试 solveset（实数域）：")
        try:
            ss = sp.solveset(expr, var, domain=sp.S.Reals)
            print("  %s" % fmt(ss))
            sols = list(ss) if isinstance(ss, sp.FiniteSet) else []
        except Exception as exc:  # noqa: BLE001
            print("  solveset 也失败：%s" % exc)
    for i, s in enumerate(sols, 1):
        line = "  %s%d = %s" % (args.var, i, fmt(s))
        n = _num(s)
        if n is not None:
            line += "   (≈ %.10g)" % n
        print(line)
    if args.lower is not None and args.upper is not None:
        lo, hi = _num(P(args.lower)), _num(P(args.upper))
        if lo is not None and hi is not None:
            kept = []
            for s in sols:
                n = _num(s)
                if n is not None and lo - 1e-12 <= n <= hi + 1e-12:
                    kept.append((s, n))
            print("落在 [%s, %s] 内的根：%s" % (args.lower, args.upper, ", ".join("%.10g" % n for _, n in kept) or "无"))
    return 0


def _prep_ode(text, func, var):
    """把 psi'' 之类简写转成 sympy 的 Derivative 形式，并把 `=` 变成 Eq。"""

    def repl(m):
        order = len(m.group(1))
        if order == 1:
            return "Derivative(%s(%s), %s)" % (func, var, var)
        return "Derivative(%s(%s), (%s, %d))" % (func, var, var, order)

    body = re.sub(r"\b%s('+)" % re.escape(func), repl, text)
    # 裸函数名补上自变量：k**2*psi -> k**2*psi(x)
    body = re.sub(r"\b%s\b(?!\s*\()" % re.escape(func), "%s(%s)" % (func, var), body)
    if "=" in body and not re.search(r"[<>=!]=", body):
        lhs, rhs = body.split("=", 1)
        return lhs, rhs
    return body, None


def cmd_dsolve(args):
    func, var = args.fname, args.var
    lhs, rhs = _prep_ode(args.eq, func, var)
    local = dict(SYMS)
    local[func] = sp.Function(func)
    tr = TRANSFORMS
    L = parse_expr(lhs, local_dict=local, transformations=tr, evaluate=True)
    extern = SYMS.get(var, sp.Symbol(var))
    R = parse_expr(rhs, local_dict=local, transformations=tr, evaluate=True) if rhs is not None else sp.Integer(0)
    eq = sp.Eq(L, R)
    print("ODE      : %s" % fmt(eq))
    ics = None
    if args.ics:
        ics = {}
        for pair in args.ics.split(","):
            if "=" not in pair:
                continue
            k, v = pair.split("=", 1)
            ics[parse_expr(k.strip(), local_dict=local, transformations=tr, evaluate=True)] = parse_expr(
                v.strip(), local_dict=local, transformations=tr, evaluate=True
            )
    try:
        sol = sp.dsolve(eq, sp.Function(func)(extern), ics=ics)
    except Exception as exc:  # noqa: BLE001
        print("dsolve 失败：%s: %s" % (type(exc).__name__, exc))
        if ics:
            print("提示：先不带 --ics 求通解，再手工代入边界条件定常数，往往更可靠。")
        return 1
    for s in sol if isinstance(sol, list) else [sol]:
        print("通解/特解: %s" % fmt(s))
    if ics:
        print("已代入边界条件：%s" % args.ics)
    return 0


# ---------------------------------------------------------------- eigen


def _group_degenerate(vals, tol):
    groups = []
    for i, v in enumerate(vals):
        placed = False
        for grp in groups:
            if abs(v - grp["value"]) < tol:
                grp["idx"].append(i)
                placed = True
                break
        if not placed:
            groups.append({"value": v, "idx": [i]})
    return groups


def cmd_eigen(args):
    M = sp.Matrix(P(args.matrix))
    print("矩阵 (%d×%d):" % (M.rows, M.cols))
    for row in M.tolist():
        print("  [%s]" % ", ".join(fmt(x) for x in row))
    if M.rows != M.cols:
        print("错误：需要方阵。")
        return 2
    if M.free_symbols:
        print("")
        print("符号本征系统：")
        try:
            for val, mult, vecs in M.eigenvects():
                print("  E = %s   简并度 %d" % (fmt(val), mult))
                for v in vecs:
                    print("     本征矢: %s" % fmt(v.T))
        except Exception as exc:  # noqa: BLE001
            print("  符号求解失败：%s: %s" % (type(exc).__name__, exc))
            return 1
        # 特征多项式，便于核对
        lam = sp.Symbol("lambda")
        print("")
        print("特征多项式: det(H - λI) = %s" % fmt(sp.factor(M.charpoly(lam).as_expr())))
        return 0

    import numpy as np  # noqa: PLC0415

    A = np.array(M.tolist(), dtype=complex)
    herm = np.allclose(A, A.conj().T, atol=1e-12)
    if not herm:
        print("注意：矩阵不是厄米的（数值上），本征值可能为复。")
    w, v = np.linalg.eigh(A) if herm else np.linalg.eig(A)
    order = np.argsort(w.real)
    w, v = w[order], v[:, order]
    tol = args.tolerance
    print("")
    print("数值本征系统（厄米: %s）：" % herm)
    for grp in _group_degenerate(w, tol):
        val = grp["value"]
        print("  E = %.12g   简并度 %d" % (val.real, len(grp["idx"])))
        for i in grp["idx"]:
            vec = v[:, i]
            nrm = np.linalg.norm(vec)
            if nrm > 0:
                vec = vec / nrm
            print("     本征矢: [%s]" % ", ".join("%.8g%+.8gj" % (z.real, z.imag) for z in vec))
    print("")
    lam = sp.Symbol("lambda")
    print("特征多项式: %s" % fmt(sp.factor(M.charpoly(lam).as_expr())))
    return 0


# ---------------------------------------------------------------- 简单符号运算


def cmd_series(args):
    var = P(args.var)
    expr = P(args.expr)
    pt = P(args.point) if args.point else sp.Integer(0)
    res = sp.series(expr, var, pt, args.order).removeO()
    print("展开 (%s → %s, 至 %d 阶): %s" % (args.expr, args.point or "0", args.order, fmt(res)))
    return 0


def cmd_limit(args):
    var = P(args.var)
    expr = P(args.expr)
    to = P(args.to)
    try:
        res = sp.limit(expr, var, to)
        print("极限 (%s → %s): %s" % (args.expr, args.to, fmt(res)))
        n = _num(res)
        if n is not None:
            print("数值     : %.10g" % n)
    except Exception as exc:  # noqa: BLE001
        print("极限计算失败：%s" % exc)
        return 1
    return 0


def cmd_simplify(args):
    expr = P(args.expr)
    print("原式     : %s" % fmt(expr))
    print("simplify : %s" % fmt(sp.simplify(expr)))
    print("expand   : %s" % fmt(sp.expand(expr)))
    print("factor   : %s" % fmt(sp.factor(expr)))
    try:
        print("trigsimp : %s" % fmt(sp.trigsimp(expr)))
    except Exception:  # noqa: BLE001
        pass
    try:
        print("radsimp  : %s" % fmt(sp.radsimp(expr)))
    except Exception:  # noqa: BLE001
        pass
    return 0


# ---------------------------------------------------------------- commute

NC_NAMES = ("x", "y", "z", "px", "py", "pz")
NC = {name: sp.Symbol(name, commutative=False) for name in NC_NAMES}
MOM_COORD = {"px": "x", "py": "y", "pz": "z"}
COORDS = ("x", "y", "z")
HBAR = sp.Symbol("hbar", positive=True)


def _nc_parse(text, defs):
    local = dict(NC)
    local["hbar"] = HBAR
    for name, body in defs.items():
        if name not in local:
            local[name] = _nc_parse(body, {})
    return parse_expr(text, local_dict=local, transformations=TRANSFORMS, evaluate=True)


def _zero_state():
    return {((), (0, 0, 0)): sp.Integer(1)}


def _add_state(d1, d2, sign=1):
    out = dict(d1)
    for k, c in d2.items():
        out[k] = out.get(k, 0) + sign * c
    return {k: v for k, v in out.items() if sp.simplify(v) != 0}


def _scale_state(d, factor):
    return {k: sp.expand(v * factor) for k, v in d.items()}


def _canon(syms):
    """坐标之间对易、动量之间对易，但坐标与动量不对易 —— 只在同类内排序。"""
    coords = sorted(s for s in syms if s in COORDS)
    moms = sorted(s for s in syms if s not in COORDS)
    out, ci, mi = [], 0, 0
    for s in syms:
        if s in COORDS:
            out.append(coords[ci])
            ci += 1
        else:
            out.append(moms[mi])
            mi += 1
    return tuple(out)


def _act_p(d, pname):
    target = MOM_COORD[pname]
    ci = COORDS.index(target)
    out = {}
    for (syms, alpha), c in d.items():
        # 乘积法则：∂_x 作用在坐标算符 x 上得 1（导数的阶数不变）
        for i, sn in enumerate(syms):
            if sn == target:
                ns = syms[:i] + syms[i + 1 :]
                k = (_canon(ns), alpha)
                out[k] = out.get(k, 0) + c
        # ∂_x 作用在 f 上：导数阶数 +1，坐标算符全部保留
        na = list(alpha)
        na[ci] += 1
        k = (syms, tuple(na))
        out[k] = out.get(k, 0) + c
    return _scale_state(out, -sp.I * HBAR)


def _act_coord(d, name):
    out = {}
    for (syms, alpha), c in d.items():
        k = (_canon((name,) + syms), alpha)
        out[k] = out.get(k, 0) + c
    return out


def _act_factor(factor, d):
    if factor.is_Pow:
        base, exp = factor.args
        base_name = getattr(base, "name", "")
        if base_name in MOM_COORD or base_name in COORDS:
            if not exp.is_Integer:
                raise ValueError("只支持整数次幂的算符：%s" % factor)
            for _ in range(int(exp)):
                d = _act_factor(base, d)
            return d
        # 1/sqrt(2)、hbar**2 这类不是算符的幂，按标量处理
        return _scale_state(d, factor)
    name = getattr(factor, "name", "")
    if name in MOM_COORD:
        return _act_p(d, name)
    if name in COORDS:
        return _act_coord(d, name)
    return _scale_state(d, factor)


def _act_product(term, d):
    if term.is_Mul:
        factors = list(term.args)
    else:
        factors = [term]
    for factor in reversed(factors):
        d = _act_factor(factor, d)
    return d


def _act(expr, d):
    expr = sp.expand(expr)
    if expr.is_Add:
        out = {}
        for term in expr.args:
            out = _add_state(out, _act_product(term, d))
        return out
    return _act_product(expr, d)


def _deriv_str(alpha):
    total = sum(alpha)
    if total == 0:
        return "f"
    denom = "".join(
        "d" + COORDS[i] + (str(alpha[i]) if alpha[i] > 1 else "") for i in range(3) if alpha[i]
    )
    prefix = "d" if total == 1 else "d%d" % total
    return "%sf/%s" % (prefix, denom)


def _disp_name(name):
    return {"px": "p_x", "py": "p_y", "pz": "p_z"}.get(name, name)


def _fmt_state(d):
    if not d:
        return "0"
    items = sorted(d.items(), key=lambda kv: (-sum(kv[0][1]), "".join(kv[0][0])))
    parts = []
    for (syms, alpha), c in items:
        c = sp.simplify(c)
        body = "*".join([_disp_name(s) for s in syms] + [_deriv_str(alpha)])
        if c == 1:
            parts.append(body)
        elif c == -1:
            parts.append("-" + body)
        else:
            parts.append("%s*%s" % (sp.sstr(c), body))
    text = " + ".join(parts).replace("+ -", "- ")
    return text


def cmd_commute(args):
    defs = {}
    for item in args.defs or []:
        if "=" not in item:
            print("--def 需要 NAME=EXPR 形式：%s" % item)
            return 2
        name, body = item.split("=", 1)
        defs[name.strip()] = body.strip()
    try:
        A = _nc_parse(args.A, defs)
        B = _nc_parse(args.B, defs)
    except Exception as exc:  # noqa: BLE001
        print("解析算符失败：%s: %s" % (type(exc).__name__, exc))
        return 1
    if defs:
        print("算符定义 : %s" % "; ".join("%s = %s" % (k, v) for k, v in defs.items()))
    try:
        ab = _act(A, _act(B, _zero_state()))
        ba = _act(B, _act(A, _zero_state()))
    except Exception as exc:  # noqa: BLE001
        print("算符作用失败：%s: %s" % (type(exc).__name__, exc))
        return 1
    comm = _add_state(ab, ba, sign=-1)
    print("对易子   : [%s, %s] 作用在测试函数 f(x,y,z) 上" % (args.A, args.B))
    print("  AB f   = %s" % _fmt_state(ab))
    print("  BA f   = %s" % _fmt_state(ba))
    print("  [A,B]f = %s" % _fmt_state(comm))
    print("")
    print("读法：把结果写成算符形式即可（例如结果 i*hbar*f 表示 [A,B] = i·ħ·1）。")
    return 0


# ---------------------------------------------------------------- check


def cmd_check(args):
    expr = P(args.expr)
    subs = {}
    if args.subs:
        for pair in args.subs.split(","):
            if "=" not in pair:
                continue
            k, v = pair.split("=", 1)
            subs[P(k.strip())] = P(v.strip())
    val = expr.subs(subs)
    num = _num(val)
    print("表达式   : %s" % fmt(expr))
    if subs:
        print("代入     : %s" % ", ".join("%s = %s" % (fmt(k), fmt(v)) for k, v in subs.items()))
    print("化简值   : %s" % fmt(val))
    if num is None:
        print("数值     : (无法数值化)")
    elif isinstance(num, complex):
        print("数值     : %.12g %+.12gj" % (num.real, num.imag))
    else:
        print("数值     : %.12g" % num)
    if args.expected is not None:
        exp = _num(P(args.expected))
        if exp is None or num is None:
            print("无法比较（期望值或计算值不能数值化）。")
            return 1
        diff = abs(complex(num) - complex(exp))
        ok = diff <= args.tol
        print("期望值   : %.12g" % exp.real if isinstance(exp, complex) else "期望值   : %.12g" % exp)
        print("偏差     : %.3e  (容差 %.1e)  =>  %s" % (diff, args.tol, "一致" if ok else "不一致"))
        return 0 if ok else 1
    return 0


# ---------------------------------------------------------------- CLI


def build_parser():
    ap = argparse.ArgumentParser(
        prog="qm.py",
        description="量子力学习题符号/数值工具箱（sympy）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("-P", "--plain-symbols", action="store_true", help="不使用预定义假设（纯符号）")
    ap.add_argument("--pretty", action="store_true", help="用 sympy 二维漂亮打印")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("symbols", help="打印可用符号与约定")
    p.set_defaults(func=cmd_symbols)

    p = sub.add_parser("integrate", help="积分")
    p.add_argument("expr")
    p.add_argument("-v", "--var", default="x")
    p.add_argument("-a", "--lower", default=None)
    p.add_argument("-b", "--upper", default=None)
    p.add_argument("--numeric", action="store_true", help="强制再给数值结果")
    p.set_defaults(func=cmd_integrate)

    p = sub.add_parser("expect", help="归一化常数与期望值")
    p.add_argument("psi", help="未归一化波函数，如 \"sin(n*pi*x/L)\"")
    p.add_argument("-v", "--var", default="x")
    p.add_argument("-a", "--lower", default=None)
    p.add_argument("-b", "--upper", default=None)
    p.add_argument("--prob-range", default=None, help="区间概率，如 \"0,L/2\"")
    p.add_argument("--real-psi", action="store_true", help="强制按实波函数处理")
    p.set_defaults(func=cmd_expect)

    p = sub.add_parser("solve", help="解方程")
    p.add_argument("expr", help="表达式，默认按 = 0 处理")
    p.add_argument("-v", "--var", default="x")
    p.add_argument("-a", "--lower", default=None)
    p.add_argument("-b", "--upper", default=None)
    p.set_defaults(func=cmd_solve)

    p = sub.add_parser("dsolve", help="解常微分方程（薛定谔方程）")
    p.add_argument("eq", help="如 \"psi'' + k**2*psi = 0\"")
    p.add_argument("-f", "--fname", default="psi", help="未知函数名（默认 psi）")
    p.add_argument("-v", "--var", default="x")
    p.add_argument("--ics", default=None, help="边界/初始条件，如 \"psi(0)=0, psi(L)=0\"")
    p.set_defaults(func=cmd_dsolve)

    p = sub.add_parser("eigen", help="矩阵本征值/本征矢与简并度")
    p.add_argument("matrix", help="sympy 嵌套列表，如 \"[[E1, V],[V, E2]]\"")
    p.add_argument("--tolerance", type=float, default=1e-9)
    p.set_defaults(func=cmd_eigen)

    p = sub.add_parser("series", help="级数展开")
    p.add_argument("expr")
    p.add_argument("-v", "--var", default="x")
    p.add_argument("-p", "--point", default=None)
    p.add_argument("-n", "--order", type=int, default=5)
    p.set_defaults(func=cmd_series)

    p = sub.add_parser("limit", help="极限")
    p.add_argument("expr")
    p.add_argument("-v", "--var", default="x")
    p.add_argument("-t", "--to", default="oo")
    p.set_defaults(func=cmd_limit)

    p = sub.add_parser("simplify", help="化简")
    p.add_argument("expr")
    p.set_defaults(func=cmd_simplify)

    p = sub.add_parser("commute", help="对易子")
    p.add_argument("A")
    p.add_argument("B")
    p.add_argument("--def", dest="defs", action="append", default=[], help="定义复合算符 NAME=EXPR，可重复")
    p.set_defaults(func=cmd_commute)

    p = sub.add_parser("check", help="数值代入校验")
    p.add_argument("expr")
    p.add_argument("--subs", default=None, help="如 \"L=1, x=0.5\"")
    p.add_argument("--expected", default=None)
    p.add_argument("--tol", type=float, default=1e-6)
    p.set_defaults(func=cmd_check)
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
    """把 `-a -a`、`-a -oo`、`--xrange -3,3` 改写成 `-a=-a` 形式。

    只对「需要值」的选项生效：紧跟其后的 token 一律当作它的值（这与 argparse 的
    取值规则本身一致，只是补上以 `-` 开头的情形）。
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
    global PLAIN
    ap = build_parser()
    raw = list(sys.argv[1:] if argv is None else argv)
    raw = _normalize_argv(raw, _value_options(ap))
    args = ap.parse_args(raw)
    PLAIN = bool(args.plain_symbols)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
