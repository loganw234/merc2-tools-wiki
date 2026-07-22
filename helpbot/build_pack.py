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
SPAWN_NAME_CAP = 100000  # effectively uncapped; the full list is its own section

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


def md_pages(folder: str) -> list[Path]:
    """Every .md in a wiki folder, in a platform-independent order.

    Do NOT use `sorted(dir.glob("*.md"))`. Sorting Path objects compares
    case-INsensitively on Windows and case-SENSITIVELY on Linux, so
    resident/Init.md and resident/Multi.md (the only capitalised pages in the
    corpus) land in different positions on a dev machine than in CI. That
    yields a byte-different pack, which breaks `--check` and -- far worse --
    silently breaks the provider's prefix cache, since the cache only hits on
    an exact match. Sorting by the plain filename string is identical on every
    platform because Python compares strings by code point.
    """
    return sorted((WIKI / folder).glob("*.md"), key=lambda p: p.name)


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


def label_rows(body: str, note_limit: int) -> list[str]:
    """Tables whose second column is PROSE, not a call.

    The signature extractor only keeps rows whose second cell looks like a call,
    which silently drops enum/behaviour tables. That is how the eleven
    `Ess.AIOrders.command` behaviours (`enter`, `deploy`, `patrol`, ...) ended up
    absent from the pack: the model knew the module existed but not one legal
    behaviour name, so it invented `enterVehicle` / `disembark` / `.move`.

    Same shape of hole as Controller's constants table. Capture `label -- prose`
    for any row whose first cell is a short bare identifier.
    """
    out: list[str] = []
    seen: set[str] = set()
    for cells in table_rows(body):
        if len(cells) < 2 or is_header_row(cells):
            continue
        label = fn_name(cells[0])
        desc = clean_inline(cells[1])
        # Reject only if the description IS a signature (that row belongs to the
        # signature extractor). An incidental "(" in prose is fine -- guarding on
        # that dropped `attack` and `animate`, whose descriptions open with an
        # aside like "Hunts opts.target (the first guid ...".
        if (not label or not desc or label in seen
                or len(label) > 28 or " " in label or "(" in label
                or re.match(r"^[A-Za-z_][A-Za-z0-9_.]*\(", desc)):
            continue
        seen.add(label)
        out.append(f"  {label} -- {truncate(desc, note_limit)}")
    return out


def code_signatures(body: str, prefix: str) -> list[str]:
    """API signatures written in prose/code fences rather than tables, e.g.
    `Ess.AIOrders.command(guids, behavior, opts, tracker) -> ok`. Table-only
    extraction misses these entirely."""
    out: list[str] = []
    seen: set[str] = set()
    pat = re.compile(r"^\s*(" + re.escape(prefix) + r"[A-Za-z0-9_.]*\([^)\n]*\)[^\n]{0,60})$",
                     re.MULTILINE)
    for m in pat.finditer(body):
        sig = clean_inline(m.group(1))
        key = sig.split("(")[0]
        if key in seen:
            continue
        seen.add(key)
        out.append(f"  {sig}")
    return out


def constant_rows(body: str, note_limit: int) -> list[str]:
    """Pages like namespaces/controller.md are `| Constant | Value | Notes |`
    tables, not function tables. The signature extractor requires a call-shaped
    second cell, so it silently produced NOTHING for those pages -- Controller
    contributed zero lines to the pack and nobody noticed until an answer went
    wrong. Pull name = value pairs so constants land too."""
    out: list[str] = []
    seen: set[str] = set()
    for cells in table_rows(body):
        if len(cells) < 2 or is_header_row(cells):
            continue
        name = fn_name(cells[0])
        val = clean_inline(cells[1]).strip("`")
        # a constant's value is short and literal; skip prose cells
        if not name or not val or len(val) > 40 or "(" in val or name in seen:
            continue
        seen.add(name)
        note = truncate(clean_inline(cells[2]), note_limit) if len(cells) > 2 else ""
        out.append(f"  {name} = {val}" + (f"  -- {note}" if note else ""))
    return out


def fn_name(cell: str) -> str:
    """Pull a bare function name out of a table's first cell."""
    m = re.search(r"`([^`]+)`", cell)
    return (m.group(1) if m else clean_inline(cell)).strip()


# --------------------------------------------------------------------------
# section builders -- each returns the section body (no title header)
# --------------------------------------------------------------------------


def build_curated(filename: str) -> str:
    """A hand-written pack section.

    HTML comments are stripped: they carry maintainer instructions (e.g. how to
    resolve the [VERIFY] tags in 05_game.md) that the model should never see.
    The [VERIFY] tags themselves DO ship -- they mark claims not sourced from a
    wiki page, and flagging that uncertainty to the model is the same contract
    as the [UNVERIFIED] markers on resident pages.
    """
    path = PACK_SRC / filename
    if not path.exists():
        raise SystemExit("missing curated section: %s" % path)
    _, body = read_page(path)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def curated(filename: str):
    """Build a curated section AND mark it as hand-written.

    CURATED_SECTION_IDS is derived from this marker, so the coverage check can
    tell prose we wrote (which deliberately names fake symbols to warn against
    them) from text the extractor produced (where a fake symbol is a real bug).
    Use this instead of `lambda: build_curated(...)` for every pack_src section.
    """
    fn = lambda: build_curated(filename)   # noqa: E731
    fn.is_curated = True
    return fn


def qualify(sig: str, name: str, title: str) -> str:
    """Force `Namespace.Function(...)` form.

    Wiki pages are inconsistent: object.md writes `Object.GetPosition(uGuid)`
    but vehicle.md writes a bare `GetFromRider(uCharacter)`. Emitting the bare
    form leaves the model to infer the namespace from the section header, which
    is precisely the kind of guessing that produces invented calls. Qualify it
    here so every line in the pack is copy-pasteable as written.
    """
    if not name or f"{title}." in sig:
        return sig
    # only rewrite a standalone occurrence of the function name
    return re.sub(r"(?<![\w.])" + re.escape(name) + r"(?=\s*\()",
                  f"{title}.{name}", sig, count=1)


def _signature_pages(folder: str, note_limit: int, skip: set[str] | None = None,
                     qualify_names: bool = False) -> str:
    """Namespace- and Ess-style pages: markdown tables of
    | `Fn` | `signature` | notes |. Used for wiki/namespaces and wiki/ess."""
    skip = skip or {"index.md"}
    out: list[str] = []
    for path in md_pages(folder):
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
            if qualify_names:
                sig = qualify(sig, name, title)
            note = truncate(clean_inline(cells[2]), note_limit) if len(cells) > 2 else ""
            lines.append(f"  {sig}" + (f"  -- {note}" if note else ""))
        # Constants-table pages (Controller) yield no call-shaped rows at all.
        if len(lines) == 1:
            lines.extend(constant_rows(body, note_limit))
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
    return header + "\n" + _signature_pages("namespaces", note_limit=130, qualify_names=True)


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
    for path in md_pages("ess"):
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
        # Signatures that live in prose/code fences rather than tables, and
        # enum/behaviour tables whose second column is prose. Without these the
        # Ess.AIOrders dispatch API and its eleven behaviour names were invisible.
        extra = code_signatures(body, "Ess.") + label_rows(body, 150)
        for line in extra:
            if line not in lines:
                lines.append(line)
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
    for path in md_pages("resident"):
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
    for path in md_pages(folder):
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        text = MD_LINK_RE.sub(r"\1", body)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        out.append(f"### {title}\n{truncate(text, char_cap)}")
    return "\n\n".join(out)


def build_luabridge() -> str:
    """Loader.* and friends.

    websocket.md is excluded on purpose. It documents Loader.WsSend, which is
    how a browser tool subscribes to a feed -- plumbing for building something
    like this IDE, not for writing game scripts. It cost ~2.8k tokens, nearly a
    fifth of the smallest tier, and no question the assistant is actually asked
    needs it. Anyone building a browser client is reading the wiki page anyway.
    """
    header = (
        "lua-bridge additions -- the ASI injection layer, NOT part of the base game.\n"
        "Loader.* only exists when lua-bridge is loaded.\n"
        "(Loader.WsSend / the WebSocket transport is omitted here; see\n"
        "https://wiki.mercs2.tools/lua-bridge-api/websocket if a user asks.)\n"
    )
    out: list[str] = []
    for path in md_pages("lua-bridge-api"):
        if path.name == "websocket.md":
            continue
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        text = MD_LINK_RE.sub(r"\1", body)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        out.append(f"### {title}\n{truncate(text, 9000)}")
    return header + "\n" + "\n\n".join(out)


def build_world() -> str:
    """World and story context from vz/.

    The rest of the pack is pure API reference: it uses words like PMC (469
    times), outpost (477) and faction (252) as identifiers while never once
    explaining what any of them MEAN. A model reading that has to infer the
    domain from general knowledge -- which is exactly how "PMC" got read as a
    generic private-military faction and `"PMC Soldier"` got invented.

    These pages are the wiki's own description of the actual game world, so
    intent ("I want troops under my command") can be mapped onto the right
    mechanics instead of guessed at.
    """
    header = (
        "What the game world actually contains -- factions, story contracts,\n"
        "characters, HQ and economy data. Use this to understand what a user\n"
        "MEANS, then answer with the API sections above. These pages describe\n"
        "the shipped game; they are not a modding API.\n"
    )
    wanted = [p for p in md_pages("vz")
              if p.name.startswith("cat-")
              or p.stem in {"wifbios", "wifbriefingdata", "wifhqdata",
                            "wifmissiondata", "wifstarterdata", "wiffreeplay"}]
    out: list[str] = []
    for path in wanted:
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        text = MD_LINK_RE.sub(r"\1", body)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        out.append(f"### {title}\n{truncate(text, 5200)}")
    return header + "\n" + "\n\n".join(out)


def build_contract_framework() -> str:
    """The Contract Framework docs + source.

    Another folder the builder never walked. It is the only place documenting
    that `Ai.Goal`'s raw XYZ destination key is `Location` -- so the pack said no
    such key existed, a curated gotcha repeated that as fact, and a live answer
    told a user it was impossible and invented a TinyGeometry workaround. The
    fourth extraction hole of the same shape: a real source folder simply absent.

    source.md is the framework's actual Lua, which is where the confirmed call
    sites live; it is capped rather than dropped so the API-shaped head survives
    without 19k tokens of implementation body.
    """
    header = (
        "Contract Framework (Ess.Contract) -- the save-safe way to author custom\n"
        "missions, as opposed to the native MrxTask* classes the shipped vz/\n"
        "contracts subclass. Includes real, confirmed Ai.Goal/Ai.Role call sites.\n"
    )
    out: list[str] = []
    for path in md_pages("contract-framework"):
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        text = MD_LINK_RE.sub(r"\1", body)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        out.append(f"### {title}\n{truncate(text, 12000)}")
    return header + "\n" + "\n\n".join(out)


def build_tutorials() -> str:
    return _verbatim_pages("tutorials", char_cap=2400)


def build_spawn() -> str:
    """Spawn tables are HTML, not markdown. We only need the exact strings --
    the whole point is that the model quotes a real template name instead of
    inventing a plausible one."""
    header = (
        "Curated spawn lists -- EXACT strings for Pg.Spawn(\"<name>\", x, y, z) and\n"
        "Pg.GetGuidByName(\"<name>\"). These are the cleaned, categorised subsets;\n"
        "the complete name list is in the AUTHORITATIVE TEMPLATE NAMES section.\n"
        "Template names are NOT predictable from the in-game display name -- never\n"
        "construct one by guessing at a pattern.\n"
    )
    out: list[str] = []
    for path in md_pages("spawn-reference"):
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
        out.append(f"### {title} ({len(names)} names)\n" + ", ".join(names))
    return header + "\n" + "\n\n".join(out)


def build_templates() -> str:
    """The authoritative name list from hash-lookup.md.

    This page is a top-level wiki page, and the builder only ever walked
    subfolders -- so the single most important anti-hallucination resource in
    the wiki (its own ai-primer calls this "the full real-template-name list")
    was absent from the pack entirely. A user asked how to spawn a PMC soldier,
    the model had no character templates in context at all, and invented
    "PMC Soldier". Every `pmc` entry in this table is a building or a prop;
    there is no PMC troop template, and now the model can see that.
    """
    hl = WIKI / "hash-lookup.md"
    if not hl.exists():
        return "(hash-lookup.md not found)"
    _fm, body = read_page(hl)
    rows = re.findall(r"<tr><td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td></tr>", body)
    names, seen = [], set()
    for name, _hash, _is_vehicle in rows:
        name = name.strip()
        if not name or name == "(unnamed)" or name in seen:
            continue
        seen.add(name)
        names.append(name)
    header = (
        "AUTHORITATIVE TEMPLATE NAME LIST -- every named entry in the game's own\n"
        "asset/string hash table (%d names). This is the complete set of real\n"
        "names. Use it two ways:\n"
        "  1. To quote an EXACT string for Pg.Spawn / Pg.GetGuidByName.\n"
        "  2. To answer 'does X exist?' -- if a name is NOT in this list, it is\n"
        "     not a real template. Say so plainly instead of guessing a spelling.\n"
        "Caveats: the table also contains non-spawnable assets (decals, interior\n"
        "props, test assets), so presence here means the NAME is real, not that\n"
        "it is necessarily spawnable. Names are case- and spacing-sensitive.\n"
        "\n"
        "SOURCE PAGE, for sending a user to browse/search it themselves:\n"
        "  https://wiki.mercs2.tools/hash-lookup\n"
        "That is the ONLY correct URL for this data. Do not build a URL out of\n"
        "this section's heading -- there is no /authoritative-template-names page.\n"
        "\n"
        "FACTION TROOPS: troop templates DO exist for most factions, named\n"
        "'<Faction> Soldier' and variants -- e.g. 'VZ Soldier', 'Allied Soldier',\n"
        "'Guerilla Soldier', 'Chinese Soldier', 'OC Soldier' (Oil Company),\n"
        "'Pirate Thug', plus Elite/Paratrooper/Female/B variants. Quote them\n"
        "exactly from the list below. The ONE exception is PMC: it is the\n"
        "player's own outfit and has no troop template at all -- do not offer one.\n"
        % len(names)
    )
    return header + "\n" + ", ".join(names)


def build_toplevel() -> str:
    """Top-level wiki pages. The builder originally walked only subfolders, so
    every one of these -- snippets, the tutorials index, the worked sample
    scripts -- was missing from the pack."""
    pages = [
        ("snippets.md", 34000),
        ("glossary.md", 9000),
        ("getting-started.md", 16000),
        ("first-mod.md", 10000),
        ("first-menu.md", 8000),
        ("sample-scripts-onkey.md", 46000),
        ("sample-scripts-onload.md", 11000),
        ("sample-scripts-onboot.md", 2000),
        ("cheat-menu.md", 30000),
        ("sound-music-effects.md", 13000),
        ("deprecated-frameworks.md", 2500),
        ("frameworks.md", 2000),
    ]
    out: list[str] = []
    for fname, cap in pages:
        path = WIKI / fname
        if not path.exists():
            continue
        fm, body = read_page(path)
        title = fm.get("title", path.stem)
        text = MD_LINK_RE.sub(r"\1", body)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        out.append(f"### {title}\n{truncate(text, cap)}")
    return "\n\n".join(out)


# id, human title, builder, soft token budget
# Budgets are set a little above current actuals so that "OVER" means the wiki
# grew enough to need re-tuning, not that we are 50 tokens past a round number.
SECTIONS = [
    ("system",     "OPERATING INSTRUCTIONS",        curated("00_system.md")           ,  4_000),
    ("game",       "WHAT THIS GAME IS",             curated("05_game.md")             ,    4_000),
    ("guide",      "GAME OVERVIEW (SECONDARY SOURCE)", curated("06_guide.md")            , 7_000),
    ("gotchas",    "ENGINE FACTS AND GOTCHAS",      curated("10_gotchas.md")          , 5_000),
    ("namespaces", "ENGINE NAMESPACE REFERENCE",    build_namespaces,                      36_000),
    ("ess",        "ESSENTIALS (Ess) FRAMEWORK",    build_ess,                             28_000),
    ("resident",   "RESIDENT MODULE INDEX",         build_resident,                        31_000),
    ("luabridge",  "LUA-BRIDGE API",                build_luabridge,                        8_000),
    ("spawn",      "SPAWN REFERENCE LISTS",         build_spawn,                           20_000),
    ("templates",  "AUTHORITATIVE TEMPLATE NAMES",  build_templates,                       45_000),
    ("contracts",  "CONTRACT FRAMEWORK",            build_contract_framework,              30_000),
    ("world",      "GAME WORLD AND STORY CONTEXT",  build_world,                           20_000),
    ("tutorials",  "TUTORIALS",                     build_tutorials,                        8_000),
    ("toplevel",   "GUIDES, SNIPPETS AND SAMPLES",  build_toplevel,                        60_000),
    ("idioms",     "CANONICAL CODE PATTERNS",       curated("90_idioms.md")           ,  4_000),
]

# Pack tiers. The Worker gets the full pack; smaller-context and local models
# get a subset. Order within a tier always follows SECTIONS, so a tier is still
# a stable prefix and still caches.
#
# Choosing what to drop is a real trade, not a size exercise. `templates` is the
# only thing preventing invented spawn names and `resident` the only thing
# preventing invented module functions -- both were live failures. So the
# reduced tiers keep the curated rules (which are cheap and carry the hard-won
# gotchas) and shed breadth, and every tier below `full` ships a banner telling
# the model exactly which references it does NOT have, so it refuses instead of
# guessing. A small pack without that banner is worse than no pack at all.
TIERS: dict[str, list[str] | None] = {
    # ~10k -- the honest floor, for a 16k-context model.
    #
    # There was briefly an 8k "tiny" tier. It is gone: 6k of pack in an 8k window
    # leaves nothing to hold a conversation in, and shipping a tier that barely
    # works is worse advice than saying "you need more context". 16k is the
    # lowest window where this is genuinely usable, and this tier is sized so
    # that ~6k remains for the actual exchange after the pack.
    #
    # Sizing matters more than it looks: a model whose context is smaller than
    # the pack does not error, it TRUNCATES FROM THE FRONT -- verified on
    # gemma2:27b (CONTEXT 8192), where a canary token at position 0 never came
    # back. The front is the system rules and the tier banner, so an oversized
    # pack silently deletes exactly the anti-invention instructions and leaves a
    # model that looks configured and is not.
    "small":  ["system", "gotchas", "idioms", "luabridge"],
    # ~46k -- 64k context
    "small+": ["system", "game", "gotchas", "idioms", "luabridge", "namespaces"],
    # ~70k -- ~100k context. Fills the gap between small+ (64k models) and
    # medium (128k models): small+ plus the whole Ess framework, which is the
    # foundational library most scripts build on, so it earns its place before
    # the 228-module resident dump does. Exactly "medium minus resident", which
    # keeps the tiers a clean nested chain (small+ subset ess subset medium).
    "ess":    ["system", "game", "gotchas", "idioms", "luabridge", "namespaces",
               "ess"],
    # ~100k -- 128k context, the common cloud tier
    "medium": ["system", "game", "gotchas", "idioms", "luabridge", "namespaces",
               "ess", "resident"],
    # ~159k -- 200k context
    "large":  ["system", "game", "gotchas", "idioms", "luabridge", "namespaces",
               "ess", "resident", "templates", "contracts"],
    # everything
    "full":   None,
}

# Human-readable names for what each section provides, used to build the
# "you do not have" banner on reduced tiers.
SECTION_MEANS = {
    "namespaces": "engine namespace signatures (Object.*, Ai.*, Player.*, ...)",
    "ess":        "the Essentials (Ess) framework API",
    "resident":   "the resident module index (228 modules and their functions)",
    "spawn":      "the spawn-reference lists",
    "templates":  "the authoritative template-name list",
    "contracts":  "the Contract Framework reference",
    "world":      "game world, faction and story context",
    "tutorials":  "the step-by-step tutorials",
    "toplevel":   "guides, snippets and worked sample scripts",
    "guide":      "the game overview",
    "luabridge":  "the lua-bridge (Loader.*) API",
}


def tier_banner(missing: list[str]) -> str:
    """Tell a reduced pack what it is blind to, so it refuses rather than guesses."""
    if not missing:
        return ""
    lines = [
        "REDUCED PACK -- YOU ARE MISSING REFERENCE MATERIAL.",
        "This build omits the sections listed below to fit a smaller context window.",
        "For anything that would need one of them you do NOT have the authoritative",
        "data, so you must NOT answer from memory. Say which reference you would need",
        "and send the user to the wiki page instead. Guessing a name here is the exact",
        "failure this pack exists to prevent.",
        "",
        "Omitted:",
    ]
    for sid in missing:
        lines.append("  - " + SECTION_MEANS.get(sid, sid))
    if "templates" in missing:
        lines.append("")
        lines.append("CRITICAL: without the template list you cannot verify ANY Pg.Spawn or")
        lines.append("Pg.GetGuidByName string. Never produce one. Point the user at")
        lines.append("https://wiki.mercs2.tools/hash-lookup and let them copy the exact name.")
    if "resident" in missing:
        lines.append("")
        lines.append("Without the resident index you cannot confirm a module function exists.")
        lines.append("Name the module and send the user to /resident/<module> rather than")
        lines.append("inventing a call on it.")
    if "ess" in missing:
        lines.append("")
        lines.append("Without the Ess API listing you know Ess EXISTS but not what is on it.")
        lines.append("A local 7B on this tier invented `Ess.GameUnits()`. Only use the few Ess")
        lines.append("calls quoted verbatim in the gotchas and patterns above; for anything")
        lines.append("else say you would need to check https://wiki.mercs2.tools/ess/ and let")
        lines.append("the user read the real signature.")
    if "namespaces" in missing:
        lines.append("")
        lines.append("Without the namespace reference you cannot confirm any engine call's")
        lines.append("arguments. Use only calls quoted verbatim above; do not infer a")
        lines.append("signature from a name.")
    return "\n".join(lines)


# Raised from 112k after a live hallucination traced to missing coverage: the
# assistant invented spawn template names because the authoritative list (a
# top-level page) was never in the pack. DeepSeek V4 Pro has a 1M context
# window, and cached prefix tokens cost ~$0.0036/M, so breadth is close to free
# -- completeness matters more here than compactness.
TARGET_TOKENS = 250_000

# Symbols that MUST survive extraction. Every entry here is something the
# assistant got wrong in production because the extractor silently dropped the
# page shape that documented it:
#   Controller constants     -> constants table, no call-shaped column
#   hash-lookup template names -> top-level page, never walked
#   AIOrders behaviours      -> enum table with prose in column 2
# A parser change that reintroduces any of these holes fails `--check`.
CANARIES = [
    "Ess.AIOrders.command(guids, behavior",   # dispatch signature (prose, not a table)
    "\n  enter -- ",                          # behaviour enum rows
    "\n  deploy -- ",
    "\n  patrol -- ",
    "\n  attack -- ",
    "RPad_Up = 5",                            # Controller constants table
    "Ai.SetFeeling(",                         # ordinary namespace signature
    "_pmcoutpost_beerA",                      # hash-lookup template names
    "Ess.Vehicle.riders",                     # Ess signature tables
    "Loader.Printf",                          # lua-bridge section
    "PMC is the player's own outfit",         # curated game primer (05_game.md)
    "Solano",                                 # vz/ world + story context
    "Venezuelan Army",                        # faction code<->fiction mapping
    "Misha Milanich",                         # curated guide section (06_guide.md)
    'Goal = "MoveToPos", Location',            # contract-framework: the Location key
]


def est_tokens(s: str) -> int:
    return len(s) // CHARS_PER_TOKEN


def build(tier: str = "full") -> tuple[str, list[dict]]:
    keep = TIERS.get(tier)
    parts: list[str] = []
    report: list[dict] = []
    missing: list[str] = []
    for sid, title, fn, budget in SECTIONS:
        if keep is not None and sid not in keep:
            missing.append(sid)
            continue
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
    banner = tier_banner(missing)
    pack = (
        "MERCENARIES 2 MODDING WIKI -- ASSISTANT CONTEXT PACK\n"
        "Generated from https://wiki.mercs2.tools content. Do not edit by hand;\n"
        "edit the wiki or helpbot/pack_src/ and re-run helpbot/build_pack.py.\n"
        + (f"\nBuild tier: {tier}\n\n{banner}\n" if banner else "")
        + "".join(parts)
        + "\n"
    )
    return pack, report


# Symbols that are definitely real. If one of these stops appearing, an
# extractor has silently gone blind for a whole page or folder -- which is how
# the assistant ended up inventing spawn template names in the first place: the
# pack simply had no character templates and nothing failed loudly.
# (symbol, section id it must appear IN). Scoping to a section matters: an
# earlier version of this check only asked whether the symbol was somewhere in
# the pack, and passed even with the whole Ai namespace removed -- because
# "Ai.SetRelation" also occurs in prose on other pages.
COVERAGE_MUST_EXIST = [
    ("Object.GetPosition", "namespaces"),
    ("Object.SetInvincible", "namespaces"),
    ("Ai.SetRelation", "namespaces"),
    ("Ai.GetFactionGuid", "namespaces"),
    ("Vehicle.GetFromRider", "namespaces"),
    ("LPad_Up", "namespaces"),          # controller.md constants table
    ("Loader.Printf", "luabridge"),
    ("MrxPmc", "resident"),
    ("Ess.Easy", "ess"),
    ("Veyron", "templates"),
    ("_pmcoutpost_bld_hq", "templates"),
    ("Pg.Spawn", "spawn"),
]

# Plausible-looking names that do NOT exist. If one of these ever appears in a
# GENERATED section it means we are feeding the model the very fiction we are
# trying to stop. (The curated sections name them on purpose, as warnings.)
COVERAGE_MUST_NOT_EXIST = [
    "PMC Soldier", "China Soldier", "Ai.SetFactionGuid",
]

# Sections written by hand in pack_src/ rather than extracted from the wiki.
#
# Derived from SECTIONS, not hardcoded. A hardcoded set went stale the moment
# 05_game.md and 06_guide.md were added: their curated prose names "PMC Soldier"
# on purpose (to warn the model off it) and was then scanned as though the
# extractor had emitted it, failing CI on a false positive. Deriving the set
# means adding a curated section can never reintroduce that.
CURATED_SECTION_IDS = {sid for sid, _t, fn, _b in SECTIONS
                       if getattr(fn, "is_curated", False)}


def coverage_report() -> int:
    """Structural + canary check for silent extraction holes.

    Deliberately does NOT reuse md_pages() to enumerate the wiki: an earlier
    version did, and when md_pages() itself was sabotaged in a negative test the
    check happily passed, because it was asking the broken code what it should
    have found. It globs the filesystem directly instead.
    """
    sections = {sid: fn() for sid, _t, fn, _b in SECTIONS}
    problems: list[str] = []

    # 1. no generated section may come back (nearly) empty
    for sid, body in sections.items():
        if sid in CURATED_SECTION_IDS:
            continue
        if est_tokens(body) < 200:
            problems.append("section '%s' is nearly empty (%d tokens)"
                            % (sid, est_tokens(body)))

    # 2. every namespace/ess page must contribute entries to its own section
    for folder, sid in (("namespaces", "namespaces"), ("ess", "ess")):
        body = sections.get(sid, "")
        for path in sorted((WIKI / folder).glob("*.md"), key=lambda p: p.name):
            if path.name == "index.md":
                continue
            fm, _b = read_page(path)
            title = fm.get("title", path.stem)
            marker = "### %s\n" % title
            idx = body.find(marker)
            if idx < 0:
                problems.append("%s/%s contributed NOTHING to section '%s'"
                                % (folder, path.name, sid))
                continue
            rest = body[idx + len(marker):]
            end = rest.find("\n\n")
            entries = rest[:end if end > 0 else len(rest)].strip().splitlines()
            if not entries:
                problems.append("%s/%s produced a header but no entries"
                                % (folder, path.name))

    # 3. canaries, scoped to the section each belongs in
    for sym, sid in COVERAGE_MUST_EXIST:
        if sym not in sections.get(sid, ""):
            problems.append("expected symbol '%s' missing from section '%s'" % (sym, sid))

    # must-NOT-exist is checked against GENERATED sections only: the curated
    # sections name these fakes on purpose, to warn the model off them.
    generated = "\n".join(b for sid, b in sections.items() if sid not in CURATED_SECTION_IDS)
    for sym in COVERAGE_MUST_NOT_EXIST:
        if sym in generated:
            problems.append("INVENTED symbol present in generated content: %s" % sym)

    if problems:
        print("[FAIL] pack coverage problems:")
        for p in problems:
            print("   - %s" % p)
        return 1
    print("[ok] coverage: every namespace/ess page contributes; %d scoped canaries "
          "present, %d absent" % (len(COVERAGE_MUST_EXIST), len(COVERAGE_MUST_NOT_EXIST)))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed pack differs from a fresh build")
    ap.add_argument("--coverage", action="store_true",
                    help="exit 1 if a page contributes nothing or a canary symbol is wrong")
    ap.add_argument("--verbose", "-v", action="store_true", help="per-section report")
    ap.add_argument("--tiers", action="store_true",
                    help="also emit reduced packs for smaller-context / local models")
    args = ap.parse_args()

    if args.coverage:
        return coverage_report()

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

    missing = [c for c in CANARIES if c not in pack]
    if missing:
        print("[FAIL] %d canary symbol(s) missing from the pack -- an extractor"
              % len(missing))
        print("       hole has reopened. Each of these caused a real wrong answer:")
        for c in missing:
            print("         %r" % c)
        return 1

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

    # Reduced tiers, for smaller-context and local models (BYOK / IDE use).
    # These are NOT canary-checked: a tier omits sections on purpose, so the
    # canaries for omitted sections are expected to be absent. The full pack
    # above is the one that guards extraction health.
    if args.tiers:
        print()
        print("%-8s %10s %10s  %s" % ("tier", "tokens", "chars", "file"))
        print("-" * 60)
        for name in TIERS:
            if name == "full":
                continue
            tp, _rep = build(name)
            fp = PACK_OUT / ("pack-%s.txt" % name.replace("+", "plus"))
            fp.write_text(tp, encoding="utf-8", newline="\n")
            print("%-8s %10d %10d  %s"
                  % (name, est_tokens(tp), len(tp), fp.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
