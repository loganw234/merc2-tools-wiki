#!/usr/bin/env python3
"""Build the wiki assistant's context pack.

Reads the wiki content in this repo and emits a single byte-stable text file that
the Cloudflare Worker sends as the first system message on every request. Because
DeepSeek (and every other provider we might swap to) caches on an exact prefix
match, this file MUST be byte-identical between builds when the wiki hasn't
changed -- otherwise every request pays the cache-miss rate instead of the
cache-hit rate. That is why nothing here writes a timestamp, iterates a directory
unsorted, or depends on dict ordering.

Usage:
    python build_pack.py                 # build pack/pack.txt + pack/pack.meta.json
    python build_pack.py --verbose       # per-section token report
    python build_pack.py --check         # exit 1 if the committed pack is stale (CI gate)

Output is ASCII-only on stdout (the Windows console is cp1252).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HELPBOT_DIR = Path(__file__).resolve().parent
WIKI = HELPBOT_DIR.parent
PACK_SRC = HELPBOT_DIR / "pack_src"
PACK_OUT = HELPBOT_DIR / "pack"

# Rough chars-per-token for English prose + code. Good enough for budgeting;
# swap for a real tokenizer only if we start bumping the context ceiling.
CHARS_PER_TOKEN = 4

# Max template names inlined per spawn-reference page (see build_spawn).
SPAWN_NAME_CAP = 700

SEPARATOR = "\n\n" + "=" * 78 + "\n"


# --------------------------------------------------------------------------
# page reading / markdown cleanup
# --------------------------------------------------------------------------

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
TD_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL | re.IGNORECASE)


def read_page(path: Path) -> tuple[dict, str]:
    """Return (front_matter, body). Front matter is parsed shallowly -- we only
    need title/parent/verified, and a real YAML parse would add a dependency for
    no benefit (some verified_note values contain unescaped colons)."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    fm: dict[str, str] = {}
    m = FRONT_MATTER_RE.match(raw)
    body = raw
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "\t", "-", "#")):
                key, _, val = line.partition(":")
                fm[key.strip()] = val.strip().strip('"').strip("'")
        body = raw[m.end():]
    return fm, body


def clean_inline(s: str) -> str:
    """Flatten a markdown cell/paragraph to compact plain text."""
    s = MD_LINK_RE.sub(r"\1", s)          # [`Camera`](../ns/camera) -> `Camera`
    s = HTML_TAG_RE.sub("", s)
    s = s.replace("\\|", "|")
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def truncate(s: str, limit: int) -> str:
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(" ", 1)[0]
    return cut + "..."


def section_body(body: str, heading: str) -> str:
    """Slice out one '## Heading' section, up to the next same-level heading."""
    pat = re.compile(r"^##\s+" + re.escape(heading) + r"\s*$", re.MULTILINE)
    m = pat.search(body)
    if not m:
        return ""
    rest = body[m.end():]
    nxt = re.search(r"^##\s+", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def table_rows(text: str) -> list[list[str]]:
    """Parse markdown table rows, skipping header and separator rows."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.count("|") < 3:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(cells)
    return rows


def is_header_row(cells: list[str]) -> bool:
    first = cells[0].strip("`* ").lower()
    return first in {"function", "function(s)", "ess function(s)", "name", "constant", "field", "event"}


def fn_name(cell: str) -> str:
    """Pull a bare function name out of a table's first cell."""
    m = re.search(r"`([^`]+)`", cell)
    return (m.group(1) if m else clean_inline(cell)).strip()


# --------------------------------------------------------------------------
# section builders -- each returns the section body (no title header)
# --------------------------------------------------------------------------


def build_curated(filename: str) -> str:
    path = PACK_SRC / filename
    if not path.exists():
        raise SystemExit("missing curated section: %s" % path)
    _, body = read_page(path)
    return body.strip()


def _signature_pages(folder: str, note_limit: int, skip: set[str] | None = None) -> str:
    """Namespace- and Ess-style pages: markdown tables of
    | `Fn` | `signature` | notes |. Used for wiki/namespaces and wiki/ess."""
    skip = skip or {"index.md"}
    out: list[str] = []
    for path in sorted((WIKI / folder).glob("*.md")):
        if path.name in skip:
            continue
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        lines = [f"### {title}"]
        seen: set[str] = set()
        for cells in table_rows(body):
            if len(cells) < 2 or is_header_row(cells):
                continue
            name = fn_name(cells[0])
            sig = clean_inline(cells[1])
            if not name or not sig or name in seen:
                continue
            # Signature cell should look like a call, not prose.
            if "(" not in sig and "." not in sig:
                continue
            seen.add(name)
            note = truncate(clean_inline(cells[2]), note_limit) if len(cells) > 2 else ""
            lines.append(f"  {sig}" + (f"  -- {note}" if note else ""))
        if len(lines) > 1:
            out.append("\n".join(lines))
    return "\n\n".join(out)


def build_namespaces() -> str:
    header = (
        "Engine namespaces. Always global -- never import() these. There is no .lua\n"
        "source behind them; every function name below was confirmed by a live\n"
        "pairs() enumeration in-game, so the NAMES are authoritative. Argument\n"
        "detail is only confirmed where a real call site exists in the decompiled\n"
        "corpus -- notes say so where it does not.\n"
    )
    return header + "\n" + _signature_pages("namespaces", note_limit=130)


def build_ess() -> str:
    """Ess gets fuller treatment than the other generated sections: it is the
    recommended path for new mods precisely because it guards the calls people
    otherwise get wrong, so we keep each page's prose overview alongside its
    signature tables."""
    header = (
        "Essentials (Ess) -- a mod-authored framework, NOT part of the game or\n"
        "lua-bridge. This is the recommended starting point for new mods: it wraps\n"
        "the sharp native calls with pcall-guarded, named-parameter equivalents.\n"
        "PREFER Ess over the raw engine namespace when both can do the job, and say\n"
        "so when answering. Deploy 1_Ess.lua to scripts/OnLoad/ with a low\n"
        "lua_loader.ini number; guard consumers with:\n"
        "    if not _G.Ess then Loader.Printf('load Ess first') return end\n"
        "Three tiers, reach for the highest that fits:\n"
        "    Ess.Easy.*  (intent-named one-liners)\n"
        "    Ess.*       (core: named params, sensible defaults)\n"
        "    Ess.Raw.*   (primitives, for composing what Ess did not anticipate)\n"
    )
    out: list[str] = []
    for path in sorted((WIKI / "ess").glob("*.md")):
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        lines = [f"### {title}"]
        overview = section_body(body, "Overview")
        if overview:
            text = re.sub(r"\n{2,}", " ", MD_LINK_RE.sub(r"\1", overview)).strip()
            lines.append(truncate(re.sub(r"\s+", " ", text), 900))
        seen: set[str] = set()
        for cells in table_rows(body):
            if len(cells) < 2 or is_header_row(cells):
                continue
            name = fn_name(cells[0])
            sig = clean_inline(cells[1])
            if not name or not sig or name in seen or ("(" not in sig and "." not in sig):
                continue
            seen.add(name)
            note = truncate(clean_inline(cells[2]), 220) if len(cells) > 2 else ""
            lines.append(f"  {sig}" + (f"  -- {note}" if note else ""))
        if len(lines) > 1:
            out.append("\n".join(lines))
    return header + "\n" + "\n\n".join(out)


def build_resident() -> str:
    """228 resident module pages. Signatures only -- the job here is to answer
    'does this function exist and what are its arguments', not to explain it."""
    header = (
        "Resident modules (src/resident/*.lua). Each file is one global module\n"
        "table named after its filename. Reach them with import(\"Name\") -- which is\n"
        "FILE-SCOPED, so every file needs its own import line.\n"
        "Signatures only below. Pages marked [UNVERIFIED] were drafted from source\n"
        "by an LLM and have NOT been confirmed in-game: when you answer from one,\n"
        "say that the wiki page is not yet verified.\n"
        "For anything beyond a signature, name the module and tell the user to open\n"
        "its page at https://wiki.mercs2.tools/resident/<module-in-lowercase>\n"
    )
    out: list[str] = []
    for path in sorted((WIKI / "resident").glob("*.md")):
        if path.name == "index.md":
            continue
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        verified = str(fm.get("verified", "")).lower() == "true"
        fns = section_body(body, "Functions")
        names: list[str] = []
        seen: set[str] = set()
        for m in re.finditer(r"^###\s+(.+?)\s*$", fns, re.MULTILINE):
            sig = clean_inline(m.group(1)).strip("`")
            if not sig or sig in seen:
                continue
            seen.add(sig)
            names.append(sig)
        if not names:
            continue
        tag = "" if verified else " [UNVERIFIED]"
        out.append(f"{title}{tag}: " + ", ".join(names))
    return header + "\n" + "\n".join(out)


def _verbatim_pages(folder: str, char_cap: int) -> str:
    """Small high-traffic folders: keep near-verbatim, just de-linked and
    whitespace-collapsed."""
    out: list[str] = []
    for path in sorted((WIKI / folder).glob("*.md")):
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        text = MD_LINK_RE.sub(r"\1", body)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        out.append(f"### {title}\n{truncate(text, char_cap)}")
    return "\n\n".join(out)


def build_luabridge() -> str:
    header = (
        "lua-bridge additions -- the ASI injection layer, NOT part of the base game.\n"
        "Loader.* only exists when lua-bridge is loaded.\n"
    )
    return header + "\n" + _verbatim_pages("lua-bridge-api", char_cap=9000)


def build_tutorials() -> str:
    return _verbatim_pages("tutorials", char_cap=2400)


def build_spawn() -> str:
    """Spawn tables are HTML, not markdown. We only need the exact strings --
    the whole point is that the model quotes a real template name instead of
    inventing a plausible one."""
    header = (
        "Spawnable template names -- EXACT strings for Pg.Spawn(\"<name>\", x, y, z)\n"
        "and Pg.GetGuidByName(\"<name>\"). If a name a user wants is not in these\n"
        "lists, say so rather than guessing a spelling; template names are not\n"
        "predictable from the in-game display name.\n"
    )
    out: list[str] = []
    for path in sorted((WIKI / "spawn-reference").glob("*.md")):
        if path.name == "index.md":
            continue
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        names: list[str] = []
        seen: set[str] = set()
        for cell in TD_RE.findall(body):
            name = clean_inline(cell).strip("`")
            if not name or len(name) > 80 or name in seen:
                continue
            seen.add(name)
            names.append(name)
        for cells in table_rows(body):
            if is_header_row(cells):
                continue
            name = fn_name(cells[0])
            if name and len(name) <= 80 and name not in seen:
                seen.add(name)
                names.append(name)
        if not names:
            continue
        # Per-page cap keeps the biggest dump (all-vehicles, which its own page
        # notes is full of non-drivable noise) from eating the whole budget.
        # When we truncate we SAY so -- otherwise the model would treat a missing
        # name as proof it does not exist, which is exactly the wrong answer.
        cap = SPAWN_NAME_CAP
        if len(names) > cap:
            shown = names[:cap]
            out.append(
                f"### {title} (showing {cap} of {len(names)} -- this list is TRUNCATED;\n"
                f"a name missing from here may still exist, send the user to\n"
                f"https://wiki.mercs2.tools/spawn-reference/{path.stem} for the full list)\n"
                + ", ".join(shown)
            )
        else:
            out.append(f"### {title} ({len(names)} names, complete)\n" + ", ".join(names))
    return header + "\n" + "\n\n".join(out)


# id, human title, builder, soft token budget
# Budgets are set a little above current actuals so that "OVER" means the wiki
# grew enough to need re-tuning, not that we are 50 tokens past a round number.
SECTIONS = [
    ("system",     "OPERATING INSTRUCTIONS",        lambda: build_curated("00_system.md"),  3_000),
    ("gotchas",    "ENGINE FACTS AND GOTCHAS",      lambda: build_curated("10_gotchas.md"), 4_000),
    ("namespaces", "ENGINE NAMESPACE REFERENCE",    build_namespaces,                      35_000),
    ("ess",        "ESSENTIALS (Ess) FRAMEWORK",    build_ess,                             24_000),
    ("resident",   "RESIDENT MODULE INDEX",         build_resident,                        31_000),
    ("luabridge",  "LUA-BRIDGE API",                build_luabridge,                        8_000),
    ("spawn",      "SPAWN / TEMPLATE NAMES",        build_spawn,                            9_000),
    ("tutorials",  "GETTING STARTED",               build_tutorials,                        8_000),
    ("idioms",     "CANONICAL CODE PATTERNS",       lambda: build_curated("90_idioms.md"),  4_000),
]

# We aim for ~100k; this is the ceiling at which the build complains loudly.
TARGET_TOKENS = 112_000


def est_tokens(s: str) -> int:
    return len(s) // CHARS_PER_TOKEN


def build() -> tuple[str, list[dict]]:
    parts: list[str] = []
    report: list[dict] = []
    for sid, title, fn, budget in SECTIONS:
        body = fn().strip()
        block = f"{SEPARATOR}## {title}\n{'=' * 78}\n\n{body}"
        parts.append(block)
        report.append({
            "id": sid,
            "title": title,
            "chars": len(block),
            "est_tokens": est_tokens(block),
            "budget": budget,
            "over_budget": est_tokens(block) > budget,
        })
    pack = (
        "MERCENARIES 2 MODDING WIKI -- ASSISTANT CONTEXT PACK\n"
        "Generated from https://wiki.mercs2.tools content. Do not edit by hand;\n"
        "edit the wiki or helpbot/pack_src/ and re-run helpbot/build_pack.py.\n"
        + "".join(parts)
        + "\n"
    )
    return pack, report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed pack differs from a fresh build")
    ap.add_argument("--verbose", "-v", action="store_true", help="per-section report")
    args = ap.parse_args()

    pack, report = build()
    digest = hashlib.sha256(pack.encode("utf-8")).hexdigest()
    total = est_tokens(pack)

    meta = {
        "sha256": digest,
        "chars": len(pack),
        "est_tokens": total,
        "target_tokens": TARGET_TOKENS,
        "chars_per_token_assumed": CHARS_PER_TOKEN,
        "sections": report,
    }

    out_txt = PACK_OUT / "pack.txt"
    out_meta = PACK_OUT / "pack.meta.json"

    if args.check:
        if not out_txt.exists():
            print("[FAIL] pack.txt missing -- run build_pack.py")
            return 1
        committed = out_txt.read_text(encoding="utf-8")
        if committed != pack:
            print("[FAIL] pack.txt is stale. Run: python helpbot/build_pack.py")
            return 1
        print("[ok] pack.txt is up to date (%d est tokens)" % total)
        return 0

    PACK_OUT.mkdir(parents=True, exist_ok=True)
    # newline="\n" so a Windows build and a Linux CI build produce identical bytes.
    out_txt.write_text(pack, encoding="utf-8", newline="\n")
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8", newline="\n")

    if args.verbose:
        print("%-12s %9s %9s  %s" % ("section", "tokens", "budget", "status"))
        for r in report:
            print("%-12s %9d %9d  %s" % (
                r["id"], r["est_tokens"], r["budget"],
                "OVER" if r["over_budget"] else "ok"))
        print("-" * 44)
    print("[ok] wrote %s" % out_txt.relative_to(WIKI))
    print("     %d chars, ~%d est tokens (target %d)" % (len(pack), total, TARGET_TOKENS))
    print("     sha256 %s" % digest[:16])
    if total > TARGET_TOKENS:
        print("[warn] pack is %d tokens over target -- trim a section budget" %
              (total - TARGET_TOKENS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
