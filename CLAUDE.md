# CLAUDE.md

Guidance for Claude Code sessions working in this repo (`merc2-tools-wiki`, a community modding wiki for
*Mercenaries 2: World in Flames*). See [about.md](about.md) for what the site itself is; this file is for
maintaining the wiki and the tooling it documents, not for readers of the site.

## Critical rule: never commit or push without asking first

Every commit/push to this repo (or any related repo) needs an explicit go-ahead on that specific pending
change — describe the diff, then ask. See the `feedback_commit_confirmation` memory file for the full
rule and why it matters; this is the one rule in this project that has zero exceptions.

## Persistent memory

Sessions rooted in this project maintain memory files under
`~/.claude/projects/<project-slug>/memory/` (slug is derived from the working directory Claude Code was
launched from — a session started in this repo's parent, `docs/mercs2-luacd/src`, currently resolves to
`C--Users-logan-Desktop-Mercs2-Decompiled-Lua-docs-mercs2-luacd-src`; a session started directly in
`wiki/` would resolve to a different slug and would **not** automatically see those files). As of this
writing that directory holds:

- `user_role` — who Logan is and how to calibrate explanations (skip basics; trust his live-test reports).
- `feedback_commit_confirmation` — the rule above, in full.
- `feedback_wiki_quality_practices` — mechanical link/fence checks, never invent facts/paths, verify
  before shipping, prefer direct work over subagents for editorial judgment.
- `feedback_ai_primer_editorial` — editorial rules specific to `ai-primer.md` (no version-gating, durable
  findings over point-in-time snapshots, stay compressed).
- `project_wiki_identity` — this repo's identity and the git-root-is-`wiki/`-subfolder quirk.
- `project_gfx_tooling` — status of the toolchain documented in full below.
- `reference_repos_and_domains` — every related repo (with local clone paths), live domain, and the local
  live-test deployment path.

If those files aren't present in a given session, that's expected (see the slug caveat above) rather than
a sign anything was lost — this CLAUDE.md is the fallback source of truth for anything load-bearing.

## Repo layout note

This repo's git root is `wiki/` itself — the parent `mercs2-luacd` folder (which also holds `tools/docgen`
and the decompiled source tree) is **not** part of this repo. Run all git commands from inside `wiki/`.

---

# GFx Custom-UI Toolchain (gfxforge / gfxforge-web / gfx_tool)

Maintainer-facing reference for the toolchain behind [deep-dives/custom-ui.md](deep-dives/custom-ui.md) —
that page documents the *modder-facing* capabilities; this section is the build/format/deployment detail
needed to actually maintain and extend the tools themselves.

## Repos, binaries, paths

- **gfxforge-web** (browser editor, JS) — `C:\Users\logan\source\repos\gfxforge-web` →
  `github.com/loganw234/mercs2-tools-gfxforge-web` (main). **Live: https://gfx.mercs2.tools**
  (GitHub Pages + CNAME; also reachable at `loganw234.github.io/mercs2-tools-gfxforge-web`). Zero-dep,
  offline single-file bundle, MIT.
- **gfxforge** (Python lib / byte-reference) — `C:\Users\logan\source\repos\gfxforge` →
  `mercs2-tools-gfxforge`. stdlib-only, MIT. The JS port is checked byte-identical against it.
- **gfx_tool** (Rust WAD injector) — `C:\Users\logan\source\repos\mercs2-gfx-tool`, binary at
  `target\release\gfx_tool.exe` → `mercs2-tools-gfxtool`. Git-dependency (rev-pinned, with permission) on
  `Mercenaries-Fan-Build/mercs2-wad-simulator`'s `mercs2_formats` crate.
- **gfx-sdk** — `C:\Users\logan\source\repos\gfx-sdk`, local-only (not yet public), builds
  `gfxexport.exe` (GFxExport 2.15). Only needed for images/DXT/real-AS2 authoring — **not** required for
  vector + text + script, which is everything gfxforge/gfxforge-web actually emit today.
- **Game** — `C:\Games\Mercenaries 2 World in Flames\`. Base `data\vz.wad` (2,565,537,792 bytes). Deploy
  target is `data\vz-patch.wad` (an auto-loaded overlay; revert by deleting it). Scripts live in
  `scripts\OnKey\*.lua` / `scripts\lua_loader.ini`; `scripts\Misc\` is used to park scripts not currently
  bound to a key.
- **Wiki** — this repo, `...\mercs2-luacd\wiki\`. Modder-facing deep dive at `deep-dives/custom-ui.md`;
  native widget API reference at `resident/mrxguibase.md` and `resident/mrxguimanager.md`. **This repo IS
  a working local git repo with a functioning GitHub remote** (`github.com/loganw234/merc2-tools-wiki`,
  pushed to successfully many times) — a note from an earlier, differently-scoped session claiming
  otherwise was almost certainly looking at the outer `Mercs2_Decompiled_Lua` folder (which indeed has no
  `.git` of its own) rather than descending into this `wiki/` subfolder. Don't trust that claim.
- cargo is **not** on Git-Bash's PATH on this machine → use `/c/Users/logan/.cargo/bin/cargo.exe`
  directly. The **`gh` CLI is not installed**.

## The `.gfx` movie format

- SWF tag stream with magic **`GFX`** (raw) or **`CFX`** (zlib), version byte 8. **`ExporterInfo` (tag
  1000) must be the first tag.** Retail movies are `CFX v8`; our tools emit raw `GFX v8` (both render
  fine in-game).
- Minimal renderable movie: `RECT` + framerate + framecount, then `ExporterInfo(1000)` /
  `FileAttributes(69)` / `SetBackgroundColor(9)` / `DefineShape3(32)` / `PlaceObject2(26)` /
  `ShowFrame(1)` / `End(0)`.
- `ExporterInfo`'s version field (u16): emit **`0x0207`** (retail 2.07 era) — our exporter's own default
  is `0x020F` (2.15), patched down to `0x0207` as a cosmetic match (not proven necessary for rendering).
- In-game, movies are ASET **`type_id 23`** (type hash `0xFE0E8320`, `cfx_pack`) blocks named after the
  movie; external textures are a separate `type_id 27` (`scaleform_*`). The asset name has **no
  extension** — `pandemic_hash_m2("minimap") == 0x71A70B2A`; `SetSwfFile("minimap.gfx")` is the filename,
  `"minimap"` is the asset key.
- Browser-side CFX inflate: `DecompressionStream('deflate')`, then rebuild the GFX header around the
  decompressed tag stream.

## What renders vs. what doesn't (a GFx constraint, not a codec bug)

**Renders:** solid rects, rounded corners, outline strokes, imported-font text (static and
variable-bound), named clips, buttons, menus, AVM1 logic.

**Does not render inline** — GFx externalizes these to asset types the injection pipeline doesn't produce
yet:
- **Gradients** — GFx wants `DefineExternalGradient` (tag 1003); the inline SWF gradient fill styles
  (0x10/0x12) render **flat**.
- **Images** — GFx wants `DefineExternalImage` (tag 1001) + a `type_id 27` texture asset; an inline
  `DefineBitsLossless2` (tag 36) renders **blank**, and zero real game movies use tag 36 at all.

Both are disabled in the gfxforge-web editor UI (the codec still round-trips them for old projects, just
doesn't let you author new ones).

Text: **import** the shared `_normal_Font` via `ImportAssets2` (tag 71, `_normal_Font.swf`) and reference
it from `DefineEditText` — don't embed a font. Dynamic text is a variable-bound field; **there is no
`SetFlashVariable` in the Lua bridge**, so the only way to update one is an AS2 function called from Lua.

Clips are for anything that needs to move/scale/hide at runtime (`_root.<name>._x/._y/._xscale/._yscale/
._rotation/._alpha/._visible`) — static content should just be a rect or text field, not a clip.

AVM1 (two authoring paths): hand-assembled via the `avm1` module, or compiled from an AS2 subset via
`compiler`. The **Python subset has no `for` loop**; **the gfxforge-web compiler adds `for`, arrays, and
`break`/`continue`** on top of it. `&&`/`||` are non-short-circuit in both. `fscommand(cmd, val)` compiles
to an `ActionGetURL2` with a `"FSCommand:"` URL.

## gfxforge-web architecture (for maintenance)

Browser-style IIFE modules loaded as plain `<script>` tags — no bundler, no npm. **Codec load order
matters:** `bitio → swf → avm1 → compiler → movie → verify → avm1-interpreter → bitmap → decode →
luagen`. Editor load order: `project-io → render → interaction → touch → panels → layers-script →
lua-panel → play → reference-image → wiring → autosave → init`. Exposed globals: `Bitio`, `Swf`, `Avm1`,
`Compiler`, `GFMovie`, `Verify`, `Avm1Interp`, `Bitmap`, `Decode`, `Luagen`.

**Tests:** `require('./tests/run.js').loadContext()` runs everything in a `vm` sandbox with a DOM stub;
`tests/suite.*.js` files are auto-discovered. Run with `node tests/run.js` (currently **116 passing**). vm
gotcha: top-level `let`/`const` don't cross module boundaries in the sandbox, so `run.js` re-exposes
needed names via an eval shim; `function`/`var` declarations do become context globals — meaning
top-level module code must stay side-effect-free at load time.

**Bundling:** `python build.py` produces `dist/gfxforge-editor.bundled.html`. Adding a new module means
updating **all three** of: `build.py`'s file lists, `index.html`'s `<script>` tags, and `tests/run.js`'s
codec/editor lists — `build.py` asserts every listed tag is actually present, so a missed spot fails loud.

**Item model:** items have a runtime `id` (`it` + counter, not persisted across saves). Project JSON uses
snake_case (`var`/`fill`/`width`); `loadProjectFromObject` normalizes it to the internal shape
(`varName`/`color`/`w`). `buildMovieFromState()` reads the global `state.{stage, items, script}` into
`GFMovie.Movie`, `.build()` produces bytes, `Verify.verifyMovie` checks them. **Menu shorthand expands on
load** (`expandMenuSpec`): a `kind: 'menu'` item becomes N buttons (event = the menu's event name,
`arg = index`) plus a `sel` clip, and appends a generated `function SetSelected(i){ _root.sel._y = y +
i*step; }` to the script. `renderProperties()` is the selection-changed hook; `afterStructuralChange()` is
the structural-edit hook.

Layout: `.main` is a CSS grid `var(--lua-w,320px) 7px 1fr 7px var(--props-w,300px)`; gutters are
resizable and persist their width to localStorage; `.lua-hidden` toggles the Lua panel; the layout stacks
vertically below 880px.

## Lua host-script generation (`js/codec/luagen.js`, global `Luagen`)

`generate({stage, items, script}, {existing, key}) -> {code, regions, events, functions}`.

- **Managed regions:** `--#region gfxforge:<kind> [key] … --#endregion` marks regenerated glue;
  `--#user <key> … --#enduser` marks modder-written code that survives a full-file regeneration (matched
  and re-inserted by key). Keys are the **event name** (stable across edits — item ids reset on reload,
  event names don't).
- Events are scraped from buttons/menus **and** from any `fscommand("name")` call found in the script
  (the movie → Lua direction); functions are scraped by looking for `_root.<var> = ` (a value update) or
  `_root.<clip>._prop` (a clip move). N buttons sharing one event name are treated as a single menu row.
- Generated output: the `FlashWidget` spawn, one `SetFlashEventHandler` per event, a
  `CallActionScriptCallback` cheat-sheet annotated with what each call updates or moves, an on-build
  initial-values block, and — when the scene has both a menu and a generated `SetSelected` — a full
  **live menu key-watch** (see the Gotchas section below for why this can't be automatic).
- The Lua panel (`lua-panel.js`) is a zero-dependency syntax highlighter: a transparent `<textarea>`
  layered over a syntax-highlighted `<pre>`, chosen deliberately over Monaco/a CDN dependency to keep the
  bundle offline-capable. Selecting an item highlights its `on <event>` region (via `findRegions`); the
  script auto-regenerates on structural change unless the textarea currently has focus (in which case it
  shows a "scene changed" badge instead of clobbering what's being typed).

## Injection & deployment (gfx_tool)

- `gfx_tool new --wad <vz.wad> --name <asset> --movie <file.gfx> --out <patch.wad>` (optional
  `--template minimap`, `--merge <existing>`). **Omitting `--merge` produces a fresh, clean,
  single-asset patch** rather than trying to preserve an existing patch's other assets.
- `gfx_tool find --wad <wad> <names...>` — reports hashes and which of the given names are present in
  that WAD's ASET, by block index.
- `gfx_tool inspect --wad <wad> --block-name|--block-index <n>` / `extract` / `build` (overrides an
  existing movie in place).
- **Deploy** = copy the built patch to `data\vz-patch.wad`. Verify with `find` (check block 0) or
  `Get-FileHash` — built vs. deployed sizes usually match (block alignment), so hash, don't just compare
  size.
- **OnKey binding:** needs `local KEYVAL = "<key>"` in the script's first 10 lines **and** a matching
  `<script>.lua=<key>` line under `[OnKey]` in `lua_loader.ini`. The loader **re-reads the script file on
  every keypress** (so code edits are live without relaunching), but an `.ini` binding change, or a
  script that's new/moved, needs a **game relaunch** to be picked up. `_G.<NAME>` persists across a
  script's separate per-press re-runs — guard "build the widget" vs. "toggle it" on that, the same
  `_G`-guard idiom used everywhere else on this wiki.

## MrxGui bridge / widget API (native side)

```lua
import("MrxGuiBase"); import("MrxGuiManager")

local w = MrxGuiBase.FlashWidget:new()
w:SetOwner(player)
w:SetLocation(x, y, width, height)
w:SetSwfFile("asset.gfx", nil, nil)
MrxGuiBase.AddWidget(w)
w:SetVisible(true)
MrxGuiManager.AddWidgetToHud(player, w)
```

- Lua → movie: `w:CallActionScriptCallback("Fn", {args})`.
- Movie → Lua: `w:SetFlashEventHandler("evt", function(_, v) ... end, {})` — note the `(_, v)` parameter
  shape and the required trailing `{}`.
- Other confirmed-working methods: `AddWidget`/`RemoveWidget`, `AddWidgetToHud`,
  `Widget:SetVisible`/`GetVisible`/`delete()` (the flash teardown on `delete()` is deferred ~1s internally
  to avoid tearing down mid-frame).

## Gotchas

**Rendering / GFx format**
- `PlaceObject2`'s flags byte must be **`0x06`** (`HasCharacter 0x02 | HasMatrix 0x04`), **not `0x40`**
  (`HasClipDepth`) — the wrong bit defines the shape but never places it on the display list, producing a
  clean blank with no error at all. This was the root cause of a months-long "custom movies render blank"
  problem. Full flag byte, MSB→LSB: `0x80` ClipActions, `0x40` ClipDepth, `0x20` Name, `0x10` Ratio,
  `0x08` ColorTransform, `0x04` Matrix, `0x02` Character, `0x01` Move.
- Gradients render flat and inline bitmaps render blank because both are externalized by GFx — see above;
  both are disabled in the editor rather than silently producing broken output.
- **A HUD `FlashWidget` composites transparent.** The movie's own `SetBackgroundColor` (tag 9) is **not
  painted** — the game world shows through anywhere no shape is drawn. The editor's own stage
  "background" swatch is preview-only chrome, not a real render setting. For a solid panel, draw a
  **full-stage rectangle as the bottom layer**.
- Known latent bug: `expandMenuSpec` writes the generated `SetSelected` function against the *original*
  `highlightName` (`sel`), but names the actual clip via `uniqueClipName(highlightName)` — these can
  mismatch if `sel` collides with another clip. Harmless for a single menu per scene; needs a fix before
  multi-menu scenes are supported.

**Lua runtime**
- The visibility getter is **`GetVisible()`**, not `IsVisible()` (which doesn't exist — calling it nil-calls
  and gets silently swallowed by `pcall`, so nothing visibly breaks, it just never toggles). And
  `not w:GetVisible()` is *also* wrong even once you use the right name — engine getters return `1`/`0`,
  and in Lua **only `nil`/`false` are falsy**, so `not 0` evaluates to `false` — the expression never
  flips. Fix: track a boolean in `_G` state and call `SetVisible(S.shown)` directly.
- **Menu keyboard navigation is never automatic.** `SetSelected(i)`/`Move`/`Choose` only move the
  highlight when the *host* calls them — a HUD widget receives no mouse or gamepad input on its own. The
  working pattern: poll `Loader.IsKeyDown(0x26/0x28/0x0D)` (up/down/enter) on a self-rescheduling
  `Event.Create(Event.TimerRelative, {0.05}, poll)`, **edge-trigger** it against the previous frame's
  state (a raw poll fires ~20×/sec, so without edge-triggering one press moves many rows), track the
  selected index, clamp to `[0, rows-1]`, and call `SetSelected`. Start the poll loop guarded by its own
  `_G` flag so it also (re)starts correctly if the HUD was already built earlier in the same session.
  `wiki/deep-dives/custom-ui.md`'s stress-test listing is a complete worked example.
- `SetSwfFile` is **asynchronous** — don't call movie functions from inside `build()` itself; call them
  from the first timer tick after building, or on a later re-press, or var-bound fields will stay blank.
- `Event.Create(Event.TimerRelative, {sec}, fn)` fires **once** — `fn` must re-arm its own next call as
  its first line to behave like a repeating timer.
- HUD input is *polled*, not *consumed* — pressing Up/Down/Enter while a custom HUD is open still does
  whatever the game itself does with those keys, too.

**Build / tooling / Windows**
- The Windows console is cp1252 — **no Unicode in printed CLI output** (use `[ok]`/`[FAIL]`/`-`, not
  fancy glyphs).
- Windows Python needs Windows-style paths (`cygpath -w`/`-m`, or just `C:/...`), not MSYS `/c/...` —
  and run it from the repo directory so cwd lands on `sys.path`. Run the Rust exe from PowerShell with
  Windows paths too.
- **Don't redirect stderr to `/dev/null` while diagnosing git** — it hides real fatals (like "dubious
  ownership") and can make a genuinely-a-repo directory look like it isn't one.
- **PowerShell's `Set-Content -Encoding ascii` mangles non-ASCII** (an em dash `—` becomes `???`) —
  rebuild text as an ASCII-only array and join with `` "`r`n" `` instead. Also, a naive
  `-replace '\[OnKey\]'` can match the literal string inside a comment line, not just the real ini
  section header — anchor the replace more specifically. Preserve CRLF explicitly (`-NoNewline` plus
  `` `r`n ``) rather than letting PowerShell's default line endings sneak in.
- **The WAD file is memory-mapped while the game is running** — you can't overwrite `vz-patch.wad` while
  it's open, and `Copy-Item` can also hit a *transient* lock from mercs2-modkit/OneDrive even with the
  game closed — retry with a short backoff rather than assuming a real problem. A built patch and an old
  one are often the same file size (block alignment) — verify with a hash, not a size comparison.
- Building `gfxexport` itself (niche, only needed for images/DXT) needs libjpeg compiled as C++ (`/TP`,
  `GFC_CPP_LIBJPEG`); nvtt is stubbed out; `GFx.vcproj` is stale and needs a glob over
  `Src/GFxPlayer/Text/*.cpp`; include flags need forward slashes with no trailing separator. MTASC/libming
  are effectively walled off on this machine's MSYS2 (camlp5/autotools issues) — hence hand-emitting AVM1
  directly instead of using a real AS2 compiler toolchain.

**Wiki / Jekyll**
- Lua double-brace table literals (`{{...}}`) break the Liquid build — wrap them in `{% raw %}...{%
  endraw %}` (a single-brace `{}` / `or {}` is fine as-is).
- An unquoted front-matter value containing a literal `: ` breaks YAML parsing and silently drops that
  page's nav placement — quote the whole value.

## Current state (as of the gfxforge-web build-out)

- gfxforge-web: full editor (select/rect/text/button/clip/menu tools, a properties panel, layers, an AS2
  script tab, a Play-mode AVM1 interpreter, a reference-image overlay, a `.gfx` importer, a resizable
  3-column layout, and the Lua host-script panel). Gradient and image tools are present in the codec but
  disabled in the UI. Live at gfx.mercs2.tools. 116 passing tests.
- Game: asset `hud` deployed in a clean single-asset `vz-patch.wad` (a `.bak` of the old multi-asset patch
  exists alongside it). `OnKey\hud.lua` is bound to **End**, with a working show/hide toggle and live menu
  key-watch. `battery_test.lua`/`stress_test.lua` are parked in `scripts\Misc\` (not currently bound).
  `lua_loader.ini`'s `[OnKey]` section: `hud.lua=end`, `MasterCheatMenu.lua=f10`, `SpawnFlash.lua=insert`.
- Sample authoring source: `C:\Users\logan\OneDrive\Desktop\WebForgeTest\{hud.gfx (1601 bytes, has a
  background panel), hud.lua}`.
- Maturity: **polished-beta for authoring/export; the Lua-generation layer is beta/hardening** — three
  generated-code bugs (visibility toggle, menu nav, missing background panel) were found and fixed in one
  session, all caught by actually testing in-game rather than by inspection.

## Open threads

- Exercise `luagen` across more scene shapes (no menu / multiple menus / clips-only / many events) and
  confirm each in-game once, individually.
- Add an in-tool "known limitations" note (gradients/images disabled, why) so it's visible without
  needing to find this file.
- Add more verified-in-game sample projects; add real-browser smoke tests (the Node test stub can't
  exercise canvas or mouse interaction, only logic).
- Not built yet: an external-texture/image authoring pipeline (needs `gfxexport` + DXT), custom embedded
  fonts (needs a TrueType→glyph converter), and a full `.gfx` → editable-AVM1 decompiler (the current
  importer is lossy — external images, external gradients, and compiled AVM1 aren't recoverable, and are
  surfaced as notes instead of silently dropped).
