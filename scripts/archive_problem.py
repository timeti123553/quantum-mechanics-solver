#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""archive_problem.py — 量子力学习题档案：把「题目 + 解题过程」存到本地，便于日后查阅复用。

存档位置（默认）：<skill>/references/local/archive/
    * 每条记录一个 markdown：YYYYMMDD-NNN-<题目>.md（带 YAML 头 + 题目指纹）
    * index.md：按日期倒序的索引表（每次 add 后自动重建）
可用环境变量 QM_ARCHIVE_DIR 或 --dir 改到别处。纯标准库，无第三方依赖，任何 Python 都能跑。

用法：
    # 存档：正文（含 ## 题目 / ## 解答 / 核验 / 答案）写在草稿文件里
    python archive_problem.py add --file 草稿.md --title "一维有限深方势阱" \
        --tags "势阱,宇称,超越方程" --difficulty 考研 --source "用户提问（文本）"
    python archive_problem.py add --file 草稿.md --question "题面文字"     # 题面单独给
    python archive_problem.py add --file 草稿.md --update 20260214-001     # 更新既有记录
    python archive_problem.py add --file 草稿.md --force                   # 明知重复仍新建

    python archive_problem.py list [--tag 势阱] [--limit 20] [--json]
    python archive_problem.py search "深势阱"      # 解题前先查档
    python archive_problem.py show 20260214-001 [--path]
    python archive_problem.py index                # 只重建索引
    python archive_problem.py path                 # 打印档案目录与条数

退出码：0 成功；3 命中重复（未写入）；2 参数/输入错误。
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
DEFAULT_DIR = os.path.join(SKILL_ROOT, "references", "local", "archive")

RECORD_RE = re.compile(r"^(\d{8})-(\d{3})-(.+)\.md$")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.S)
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
HEAD_RE = re.compile(r"^(#{1,6})\s*(.+?)\s*$")
BAD_CHARS = re.compile(r'[\\/:*?"<>|\r\n\t]+')
QUESTION_HEADS = ("题目", "题意", "问题")

META_ORDER = ("id", "date", "title", "tags", "difficulty", "source", "fingerprint")


def warn(msg):
    sys.stderr.write("[archive] %s\n" % msg)


def die(msg, code=2):
    sys.stderr.write("[archive] 错误：%s\n" % msg)
    sys.exit(code)


# ------------------------------------------------------------------ 目录与记录


def archive_dir(args=None):
    cand = None
    if args is not None:
        cand = getattr(args, "dir", None)
    cand = cand or os.environ.get("QM_ARCHIVE_DIR") or DEFAULT_DIR
    return os.path.abspath(cand)


def ensure_dir(adir):
    os.makedirs(adir, exist_ok=True)
    return adir


def split_frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            meta[key.strip()] = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
        else:
            meta[key.strip()] = val.strip("'\"")
    return meta, text[m.end() :]


def render_frontmatter(meta):
    lines = ["---"]
    for key in META_ORDER:
        if key not in meta:
            continue
        val = meta[key]
        if isinstance(val, (list, tuple)):
            lines.append("%s: [%s]" % (key, ", ".join(str(v) for v in val)))
        else:
            lines.append("%s: %s" % (key, val))
    lines.append("---")
    return "\n".join(lines)


def iter_records(adir):
    if not os.path.isdir(adir):
        return []
    out = []
    for name in sorted(os.listdir(adir)):
        m = RECORD_RE.match(name)
        if not m:
            continue
        path = os.path.join(adir, name)
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            continue
        meta, body = split_frontmatter(text)
        meta.setdefault("id", "%s-%s" % (m.group(1), m.group(2)))
        meta.setdefault("date", "%s-%s-%s" % (m.group(1)[:4], m.group(1)[4:6], m.group(1)[6:]))
        out.append({"path": path, "name": name, "meta": meta, "body": body})
    return out


def find_by_id(adir, rid):
    for rec in iter_records(adir):
        if rec["meta"].get("id") == rid:
            return rec
    return None


def find_by_fingerprint(adir, fp):
    for rec in iter_records(adir):
        if rec["meta"].get("fingerprint") == fp:
            return rec
    return None


# ------------------------------------------------------------------ 工具函数


def fingerprint(text):
    norm = "".join(ch for ch in text.lower() if ch.isalnum())
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:12]


def slugify(title, limit=36):
    slug = BAD_CHARS.sub("", str(title)).strip()
    slug = re.sub(r"\s+", "-", slug).strip("-. ")
    return slug[:limit] or "problem"


def strip_first_h1(body):
    m = H1_RE.search(body)
    if not m:
        return body
    return body[: m.start()] + body[m.end() :]


def first_h1(text):
    m = H1_RE.search(text)
    return m.group(1).strip() if m else ""


def extract_section(body, names=QUESTION_HEADS):
    lines = body.splitlines()
    for i, line in enumerate(lines):
        m = HEAD_RE.match(line)
        if m and any(n in m.group(2) for n in names):
            level = len(m.group(1))
            for j in range(i + 1, len(lines)):
                m2 = HEAD_RE.match(lines[j])
                if m2 and len(m2.group(1)) <= level:
                    return "\n".join(lines[i + 1 : j]).strip()
            return "\n".join(lines[i + 1 :]).strip()
    return ""


def next_id(adir, day):
    prefix = day.strftime("%Y%m%d")
    used = set()
    for rec in iter_records(adir):
        m = RECORD_RE.match(rec["name"])
        if m and m.group(1) == prefix:
            used.add(int(m.group(2)))
    n = 1
    while n in used:
        n += 1
    return "%s-%03d" % (prefix, n)


def as_tags(value):
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        items = value
    else:
        items = re.split(r"[,，;；]", str(value))
    return [t.strip() for t in items if str(t).strip()]


# ------------------------------------------------------------------ 索引


def rebuild_index(adir):
    recs = iter_records(adir)
    recs.sort(key=lambda r: r["meta"].get("id", ""), reverse=True)
    lines = [
        "# 题库存档索引",
        "",
        "共 %d 道题。本文件由 `scripts/archive_problem.py` 自动重建，不要手改。" % len(recs),
        "",
        "查阅：`python scripts/archive_problem.py list|search <关键词>|show <id>`",
        "",
    ]
    if recs:
        lines += [
            "| id | 日期 | 题目 | 标签 | 难度 |",
            "| --- | --- | --- | --- | --- |",
        ]
        for rec in recs:
            meta = rec["meta"]
            tags = meta.get("tags") or []
            tags = ", ".join(tags) if isinstance(tags, (list, tuple)) else str(tags)
            lines.append(
                "| %s | %s | [%s](<%s>) | %s | %s |"
                % (
                    meta.get("id", ""),
                    meta.get("date", ""),
                    meta.get("title", ""),
                    rec["name"],
                    tags,
                    meta.get("difficulty", ""),
                )
            )
    else:
        lines.append("_（还没有记录）_")
    path = os.path.join(adir, "index.md")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return path, len(recs)


# ------------------------------------------------------------------ 子命令


def cmd_add(args):
    adir = ensure_dir(archive_dir(args))
    if args.file:
        if not os.path.isfile(args.file):
            die("找不到正文文件：%s" % args.file)
        with open(args.file, encoding="utf-8") as fh:
            raw = fh.read()
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        die("需要 --file <草稿文件>，或把正文从 stdin 传进来")

    meta0, body = split_frontmatter(raw)
    title = args.title or meta0.get("title") or first_h1(raw) or "（未命名题目）"
    body = strip_first_h1(body).strip() + "\n"
    tags = as_tags(args.tags or meta0.get("tags"))
    difficulty = args.difficulty or meta0.get("difficulty") or ""
    source = args.source or meta0.get("source") or ""

    question = ""
    if args.question:
        question = args.question
    elif args.question_file:
        if not os.path.isfile(args.question_file):
            die("找不到题面文件：%s" % args.question_file)
        with open(args.question_file, encoding="utf-8") as fh:
            question = fh.read()
    if not question:
        question = extract_section(body)
    if not question:
        question = body[:400]
        warn("正文里没找到 `## 题目`（或 题意/问题）小节，改用正文前 400 字做指纹")

    fp = fingerprint(question)
    if len("".join(ch for ch in question if ch.isalnum())) < 8:
        warn("题面过短，指纹可靠性低")

    today = datetime.date.today()
    if args.update:
        rec = find_by_id(adir, args.update)
        if rec is None:
            die("--update 指定的记录不存在：%s" % args.update)
        rid = rec["meta"].get("id", args.update)
        path = rec["path"]
        day = rid.split("-")[0]
        date_str = "%s-%s-%s" % (day[:4], day[4:6], day[6:8])
    else:
        dup = find_by_fingerprint(adir, fp)
        if dup and not args.force:
            sys.stderr.write(
                "[archive] 命中重复：同一道题已存档 -> %s\n"
                "          如需更新该记录：加 --update %s\n"
                "          确实是不同题：加 --force\n"
                % (dup["path"], dup["meta"].get("id", ""))
            )
            return 3
        rid = next_id(adir, today)
        date_str = today.isoformat()
        path = os.path.join(adir, "%s-%s.md" % (rid, slugify(title)))
        if os.path.exists(path):
            path = os.path.join(adir, "%s-%s-2.md" % (rid, slugify(title)))

    meta = {
        "id": rid,
        "date": date_str,
        "title": title,
        "tags": tags,
        "difficulty": difficulty,
        "source": source,
        "fingerprint": fp,
    }
    content = "%s\n\n# %s\n\n%s" % (render_frontmatter(meta), title, body)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    index_path, count = rebuild_index(adir)

    if args.json:
        print(json.dumps({"id": rid, "path": path, "fingerprint": fp, "total": count},
                         ensure_ascii=False, indent=2))
    else:
        print("已存档 : %s" % path)
        print("编号   : %s" % rid)
        print("指纹   : %s" % fp)
        print("索引   : %s（共 %d 条）" % (index_path, count))
    return 0


def cmd_list(args):
    adir = archive_dir(args)
    recs = iter_records(adir)
    recs.sort(key=lambda r: r["meta"].get("id", ""))
    if args.tag:
        want = args.tag.lower()
        recs = [r for r in recs
                if want in " ".join(r["meta"].get("tags") or []).lower()]
    if args.limit and len(recs) > args.limit:
        recs = recs[-args.limit :]
    if args.json:
        print(json.dumps(
            [{"id": r["meta"].get("id"), "date": r["meta"].get("date"),
              "title": r["meta"].get("title"), "tags": r["meta"].get("tags"),
              "difficulty": r["meta"].get("difficulty"), "path": r["path"]} for r in recs],
            ensure_ascii=False, indent=2))
        return 0
    if not recs:
        print("档案目录：%s\n（还没有记录）" % adir)
        return 0
    print("档案目录：%s（%d 条）" % (adir, len(recs)))
    for rec in recs:
        meta = rec["meta"]
        tags = meta.get("tags") or []
        tags = ", ".join(tags) if isinstance(tags, (list, tuple)) else str(tags)
        print("  %s  %-12s %s%s" % (meta.get("id", ""), meta.get("date", ""),
                                    meta.get("title", ""),
                                    ("   [%s]" % tags) if tags else ""))
    return 0


def cmd_search(args):
    adir = archive_dir(args)
    terms = [t.lower() for t in args.terms if t.strip()]
    hits = 0
    for rec in sorted(iter_records(adir), key=lambda r: r["meta"].get("id", ""), reverse=True):
        meta = rec["meta"]
        tags = meta.get("tags") or []
        tags = tags if isinstance(tags, (list, tuple)) else [str(tags)]
        haystack = "\n".join([str(meta.get("title", "")), " ".join(tags), rec["body"]]).lower()
        if not all(t in haystack for t in terms):
            continue
        hits += 1
        print("%s  %s  %s" % (meta.get("id", ""), meta.get("date", ""), meta.get("title", "")))
        print("    %s" % rec["path"])
        shown = 0
        for i, line in enumerate(rec["body"].splitlines(), 1):
            low = line.lower()
            if any(t in low for t in terms) and line.strip():
                print("    L%d: %s" % (i, line.strip()[:110]))
                shown += 1
                if shown >= 3:
                    break
        if hits >= args.limit:
            break
    if not hits:
        print("未命中：%s" % " ".join(args.terms))
        print("档案目录：%s" % adir)
        return 1 % 256
    print("\n共命中 %d 条。" % hits)
    return 0


def cmd_show(args):
    adir = archive_dir(args)
    rec = find_by_id(adir, args.id)
    if rec is None:
        die("找不到记录：%s（用 list 查看全部编号）" % args.id)
    if args.path:
        print(rec["path"])
        return 0
    with open(rec["path"], encoding="utf-8") as fh:
        sys.stdout.write(fh.read())
    return 0


def cmd_index(args):
    adir = ensure_dir(archive_dir(args))
    path, count = rebuild_index(adir)
    print("已重建索引：%s（共 %d 条）" % (path, count))
    return 0


def cmd_path(args):
    adir = archive_dir(args)
    recs = iter_records(adir)
    print("档案目录：%s" % adir)
    print("记录条数：%d" % len(recs))
    print("索引文件：%s%s" % (os.path.join(adir, "index.md"),
                             "" if os.path.isfile(os.path.join(adir, "index.md")) else "（尚未生成）"))
    return 0


def build_parser():
    ap = argparse.ArgumentParser(prog="archive_problem.py",
                                 description="量子力学习题档案：题目 + 解题过程的本地存档与检索")
    ap.add_argument("--dir", default=None, help="档案目录（默认 <skill>/references/local/archive）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add", help="新增/更新一条记录")
    p.add_argument("--file", "--body-file", dest="file", default=None,
                   help="正文文件（含 ## 题目 / ## 解答 / 核验 / 答案）")
    p.add_argument("--question", default=None, help="题面文字（不写则从正文的 ## 题目 小节提取）")
    p.add_argument("--question-file", default=None, help="题面文件")
    p.add_argument("--title", default=None)
    p.add_argument("--tags", default=None, help="逗号分隔，如 \"势阱,宇称,超越方程\"")
    p.add_argument("--difficulty", default=None, help="如 本科 / 考研 / 竞赛")
    p.add_argument("--source", default=None, help="如 用户提问（图片）/ 用户提问（文本）")
    p.add_argument("--update", default=None, help="更新指定 id 的记录，而不是新建")
    p.add_argument("--force", action="store_true", help="命中重复时仍然新建")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="列出记录")
    p.add_argument("--tag", default=None)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("search", help="全文检索（解题前先跑这个查重）")
    p.add_argument("terms", nargs="+")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("show", help="打印一条记录")
    p.add_argument("id")
    p.add_argument("--path", action="store_true", help="只打印文件路径")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("index", help="重建 index.md")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("path", help="打印档案目录与条数")
    p.set_defaults(func=cmd_path)
    return ap


def main(argv=None):
    ap = build_parser()
    args = ap.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
