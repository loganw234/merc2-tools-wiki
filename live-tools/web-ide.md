---
title: Lua Web IDE
parent: Live Tools
nav_order: 1
---

# Lua Web IDE

## Overview

`mercs2-lua-web-ide` is a real, browser-based Lua IDE for Mercenaries 2 modding — not an offline-only code
editor. Write a script, hit **Run**, and it executes inside your actual **running game**, with results and
the live game log streaming straight back to the page. Live at **https://ide.mercs2.tools/** (confirmed
reachable); source at [github.com/loganw234/mercs2-lua-web-ide](https://github.com/loganw234/mercs2-lua-web-ide).
It ships as a single self-contained `dist/index.html` — editor, API reference, examples, and the WebSocket
client all inlined — so it works hosted on GitHub Pages or downloaded and opened straight off disk. No
install and no build step to *use* it; only *running* code against the game needs the bridge.

## Editor and autocomplete

The editor is CodeMirror 6 (vendored, zero external requests): Lua syntax highlighting, undo/redo, find &
replace, bracket matching, auto-indent, and folding. Autocomplete is three-layered:

- **`Ess.*`-aware completion** — generated from `mercs2-lua-essentials`'s own machine-readable API manifest
  (`api/ess.json`, a format Ess began shipping in v0.4; `tools/gen_api.py`), covering **79 `Ess` namespaces /
  548 calls**, tier-badged Easy/Core/Raw, with Easy-tier calls boosted to the top of the list. A call is in
  this list because Ess's own source *defines* it, not because a document mentions it — `CAPABILITIES.md`
  (still vendored) now only decorates the data rather than being parsed for the calls themselves. See "API
  reference" below for what changed and why it matters.
- **Native-engine-call completion** — `tools/gen_natives.py` now merges two sources: `tools/scrape_natives.py`'s
  scan of this wiki's own decompiled Lua corpus for every function *called but never defined* anywhere in it
  (a real call site and observed argument count), and Ess's own live `pairs(_G)` dump of a running game
  (authoritative for what *exists*, though with no call site of its own). Together: **96 namespaces / 1,332
  calls**. A small slice of that data — `Loader`, the patched `math` functions, `Tcp.Send` — is actually
  lua-bridge's own addition, not the engine's; see "API reference" below for how it's labeled apart. See
  [Engine Namespaces](../namespaces/) for this wiki's own documentation of the native surface.
- **Template-name completion** — typing inside an open `"`/`'` offers every confirmed spawnable template
  name (`20_editor.js`'s `templateCompletions`, fed from `src/data/templates.json`). See "Template names"
  below for where that list comes from and its other two homes.

Accepted completions insert as tab-through snippet placeholders, not bare text.

Hovering any `Ess.*`, native, lua-bridge, or resident-module token — even ones like `assert` that aren't
offered as autocomplete suggestions at all — shows a tooltip (`CM.hoverTooltip`, `20_editor.js` ~line 195)
with its signature, tier, doc string, a documented return value when the reference has one, and — the single
best moment to see it — a **gotcha** warning if the call has one. It reuses the exact same lookup the
API-reference sidebar uses (`IDE.api.lookup`, further down this page), rather than fetching or building a
second copy.

### Template names

`tools/gen_templates.py` mines two real, hand-curated spawn-menu scripts — `AllInOneSpawnMenu.lua` and the
`CommonSpawnMenu.lua` embedded in the [OnKey sample scripts](../sample-scripts-onkey) page — plus this
wiki's own [Spawn Reference](../spawn-reference/) pages (for the Skins/FX names those two menus don't cover
at all) into `src/data/templates.json`: **667 confirmed names** as of 2026-07-18, split Vehicles 515 /
Weapons 50 / Skins 4 / FX 31 / Other 67. Per the generated file's own credit line, the two source spawn
menus are the hand-found and maintained work of community members **@Ferdilanz** and **@Cosmic76Guardian**.

That data feeds three places: the in-string autocomplete above, an info-level linter nudge (see Lint pass,
below) when a spawn-like call gets a string it doesn't recognize, and its own sidebar tab — **Templates**
(`src/app/52_templates.js`) — browsable by category, filterable by search, click a name to insert it quoted
at the caret.

## Lint pass

A vendored `luaparse` (Lua 5.1 grammar) gives a real parse before anything is sent. On top of that, a
checker tuned for first-script mistakes runs:

- Genuine **syntax errors** are retold in plain English (missing `end`, `=` vs `==`, `!=` vs `~=`, unclosed
  strings…) and are the *only* thing that actually blocks Run — a beginner should never wonder why the game
  ignored a script that couldn't have parsed.
- Everything else is a live squiggle that does **not** block sending the code: did-you-mean suggestions for
  typo'd `Ess.*` / native / `Loader.*` calls, colon-vs-dot fixes (`Object:GetPosition` → `Object.GetPosition`),
  argument-count checks (backed by how the game's own scripts actually call each native), a `print()` →
  `Ess.Log` hint, and a check for a bare `while true` loop with no `break`/`return` — flagged with a
  red, error-styled warning ("This loop never ends and will FREEZE the game...") because scripts run on the
  game's own thread, but it's a strong visual warning, not a send-blocking gate the way an actual syntax
  error is.
- An info-level nudge (`25_lint.js`) when a spawn-like call — `Pg.Spawn`, `Ess.Object.spawn`,
  `Ess.Object.spawnAhead`, `Ess.Easy.Vehicle.summon` — gets a string literal that isn't in the 667-name
  template list above: "double-check the spelling, or browse the Templates tab." Same soft, non-blocking
  treatment as the rest of this list.
- A **missing-`import()` check** — flags a resident Lua module (e.g. `MrxPmc`, `MrxUtil`; see
  [Resident Modules](../resident/)) used without its own [`import("Name")`](../glossary#importname) first.
  `import()` only affects the importing script's own environment, so skipping it doesn't misbehave subtly —
  it dies immediately with `attempt to index global 'MrxPmc' (a nil value)`, and the warning names the exact
  import needed and quotes that real error. Reported once per script no matter how many times the module is
  used; a sub-table reached through a parent (`MrxGui.FlashWidget`) is exempt, since the parent's own import
  is the one that actually matters. Engine natives, Ess, and lua-bridge's own calls need no import and are
  never flagged.

## Running code

**Ctrl/Cmd+Enter** runs the selection (or the whole file). This sends the code over a real WebSocket to
`ws://127.0.0.1:27050` — see [WebSocket Transport](../lua-bridge-api/websocket) for the wire protocol —
wrapping it in a `pcall`, tagging it with a nonce, and sending it to the bridge's hidden `Loader.WsSend`
channel; the client then awaits a matching tagged result line. `run()` always resolves (never hangs or
rejects) to `{ok, value, acked, timedOut}` — an 8-second timeout is the safety net if no tagged line comes
back. A return value that's a Lua table is pretty-printed (e.g. `{x=1, y={...}}`) instead of `table: 0x...`,
via a small depth-capped (3), item-capped (40), cycle-safe serializer embedded directly in the wrapped
chunk, sitting alongside a one-line REPL under the output (bare expressions auto-wrap in `return`, so
`Ess.VERSION` just works).

### Grabbing a live guid

A header button, **"Grab what I'm aiming at"** (`src/app/60_ui.js`, ~lines 53-67), runs
`Ess.Player.targetUnderReticle(0)` plus `Ess.Probe.describeSafe` against the connected game and inserts a
ready-to-use `Sys.StringToGuid(...)` call at the caret, flashing the target's description.

That call shape matters for a reason worth stating plainly, as general knowledge and not just an
implementation detail: **a guid is Lua userdata, not a number.** Calling `tostring()` on one gives an
opaque, non-reusable string (something like `userdata: 0012B69E`) — it can't be typed back into a script or
compared across runs. The real, portable round trip is `Ess.Name(uGuid)` (a `pcall`-wrapped
`Sys.GuidToString`) to get a stable hex string like `"0x0012B69E"` out, and `Sys.StringToGuid(s)` to turn
that string back into the identical handle going back in. `src/app/46_inspector.js`'s own source comment
(lines 8-14) states this was tested against a real in-game target — matching `Ess.Object.health` values
read before and after the round trip. Both the grab-target button here and the Object Inspector below deal
exclusively in that hex-string form.

### Watch panel and Object Inspector

Two ways to keep an eye on live game state without re-running code by hand:

- **Watch** (`src/app/45_watch.js`) — a third output tab alongside Results and the log. Pin any expression
  (`Ess.Player.pose(0)`, `Ess.Loop.isRunning("demo")`); each pinned row re-polls every 2 seconds over the
  same `IDE.bridge.run` path the REPL uses, has its own kill switch, and the pinned expressions themselves
  (not their last values) persist in `localStorage` across reloads.
- **Object Inspector** (`src/app/46_inspector.js`) — its own sidebar tab, not a Watch row. Feed it a guid by
  grabbing your target, typing or pasting a hex guid, or clicking 🔍 on a Results row, and it takes over the
  sidebar with a live, 2-second-polled view — name, position, health, max health, faction, alive, and
  `Ess.Probe.describeSafe` — all in one compound round trip per poll.

### Ess-version drift warning

On every successful connect, `src/app/76_versioncheck.js` asks the live game `return Ess.VERSION` and
compares it to the `Ess.VERSION` the bundled API/autocomplete data was generated against (stamped in at
build time by `tools/gen_api.py`). A mismatch shows one dismissible line, not a blocker; dismissing
remembers that exact (reference, game) version pair, so a future mismatch on either side reopens it.

### Reading results and the log

- A **runtime-error explainer** (`src/app/40_console.js`) pattern-matches common Lua runtime errors —
  `attempt to index/call a nil value`, `bad argument #N`, arithmetic/concat/compare on nil, and similar —
  into a plain-English second line shown under the red result, so a beginner's first crash comes with a
  guess at "why," not just the raw engine message.
- **Log highlight rules** (`src/app/40_console.js`): built-in tints for `PASS`/`FAIL`/`error`/`[recipe]`,
  plus a small popover for user-defined pattern → color rules (plain text or `/regex/flags`, persisted in
  `localStorage`, checked before the built-ins so a user rule can override one).

## Script library and examples

Named scripts persist in the browser's `localStorage`, with rename, duplicate, delete, `.lua` import/export,
and shareable links — a share link decodes into a **new** script on load, so opening one never clobbers
anyone's existing work. A 45-item Examples gallery (8 categories) is generated straight from the Ess repo's
smoke-tested `samples/recipes/`; one click opens any example as a new script.

Share links carry more than a bare script now: the **Share** button (`src/app/60_ui.js`) runs the payload
(script name + code) through a real vendored `lz-string` (`CM.LZString.compressToEncodedURIComponent`) into
a `#z=` link — several times more script fits in a URL, and the name travels along with it. The old `#s=`
format (plain `encodeURIComponent`, code only, no name) still parses forever as a permanent fallback, so no
link minted before this shipped ever breaks.

**Library backup and restore** (`IDE.store.exportAll`/`.importAll`, `src/app/15_store.js`, wired to two
Scripts-panel actions) exports the whole library as one JSON file and restores from one. Restore is always
additive: imported scripts land as brand-new entries with fresh ids and name-deduplication, exactly like a
fresh "+ New" would — it can never silently overwrite anything already in the library.

**Deploy as OnKey** (`src/app/55_scripts.js`, ~lines 88-121) wraps the open script in the same
guard/state/action shape every `Ess` OnKey mod uses (`samples/OnKey/StarterMod.lua`'s own pattern) — an
`Ess`-loaded guard first, an `Ess.State(...)` scratch table, then the script unchanged below — names the
file after the script, and downloads it with a `lua_loader.ini` binding comment baked in, ready to drop
into `scripts/OnKey/`.

## API reference

A sidebar browsable by four categories, each labeled and badged so a result never looks more authoritative
than it is: the full **Ess API** (tier-badged Easy/Core/Raw), the engine's own **natives** ("Native"),
**lua-bridge's own additions** ("lua-bridge"), and **resident Lua modules** ("resident module"). Clicking a
call opens a doc pane — signature, tier, description, a documented return value and a **gotcha** warning
where the data has one, a real call-site example for natives — with an Insert button.

The Ess side is now generated from Ess's own machine-readable manifest (`api/ess.json`, a format Ess began
shipping in v0.4) rather than parsed out of `CAPABILITIES.md`'s markdown tables — a call is in the reference
because Ess's source *defines* it, not because a document mentions it. That retired a fragile shorthand rule
that had been silently mis-attributing real `Ess.Squad` methods (`.setFormation`/`.clearFormation`/`.on`) to
`Ess.Squad.Tactics`, a namespace that doesn't have them, and reading `Ess.Color.NAMES` (a preset table, not
a call) as one. `CAPABILITIES.md` is still vendored, but now only decorates: section grouping, per-namespace
blurbs, and richer hand-written signatures for the calls documented with option-table keys. The native side
is likewise now a **merge** of the wiki's own decompiled-corpus scrape (real call sites, observed argument
counts) with Ess's own live `pairs(_G)` dump of a running game (authoritative for what *exists*) — which
also stopped the linter flagging a real engine function as unrecognized purely because no shipped script
happens to call it.

**lua-bridge's own API** — `Loader`'s nine functions (full detail: [Loader](../lua-bridge-api/loader)), the
19 stdlib `math` functions plus `math.pi`/`math.huge` it patches back into this game's stripped Lua runtime
(full detail: [Stdlib Additions](../lua-bridge-api/stdlib)), one-function `Tcp.Send` (see
[Getting Started](../getting-started)), and the bare global `assert` — used to show up badged "Native" and
described as "the engine's own functions," which was wrong on both counts: they're injected by the mod and
only exist while lua-bridge is loaded. They're badged **lua-bridge** now instead. `math` is marked partial —
the engine's own pre-existing `math.floor`/`math.abs`/`math.max`/`math.min`/`math.randf` live alongside the
patched functions but aren't enumerated here — so the linter never flags one of those as unrecognized.

**Resident Lua modules** — all 18 canonical top-level ones (562 functions: `MrxPmc`, `MrxUtil`,
`MrxGuiBase`, and 15 others — see [Resident Modules](../resident/)) are browsable here too, each namespace
summary naming the exact [`import("Name")`](../glossary#importname) it needs — the same requirement the
Lint pass's missing-`import()` check enforces.

Every doc, return line, and gotcha is sourced — mined from this wiki, Ess's own source, and the decompiled
corpus, never invented — and a gotcha is the single most useful thing the panel can surface on an engine
whose characteristic failure is silent wrong behavior rather than an error: `Loader.Printf` quietly ignores
format arguments despite its name, `Tcp.Send` fails **silently** outside `127.0.0.0/8`, and `math.random` is
a completely different generator from the engine's own `math.randf`. In total: 548/548 Ess calls, 791/1,332
natives (59%), and all 562 resident-module functions carry a real description — roughly **1,900 documented
entries and 310 sourced gotchas**. The gap in natives is left visible on purpose: around 540 native
functions exist at runtime, are called by no shipped script, and appear in no document, so they stay
undescribed rather than guessed at.

## Stop loops

A panic **■ Stop loops** button runs one small Lua snippet:

```lua
local n = 0
for id in pairs(Ess.Loop._reg) do Ess.Loop.stop(id) n = n + 1 end
if Ess.Time and Ess.Time.restoreScale then Ess.Time.restoreScale() end
return "stopped " .. n .. " loop(s), time scale restored"
```

— iterating [`Ess.Loop`](../ess/timing-input#essloop)'s internal registry to stop every registered loop and
restore the time scale, for the "my script went wild" moment.

## Interactive first-script tutorial

A floating, non-blocking guided panel (`src/app/78_tutorial.js`) walks a brand-new user through their first
real script, one step at a time: connect, type `return Ess.VERSION` themselves, read their own position
(`Ess.Player.pose(0)`), teleport to a live-captured street outside the PMC HQ (a fresh player starts inside
the HQ lobby, where a summoned car has nowhere to go), summon a taxi and meet the teardown pattern
(`Ess.State` plus "remove last run's taxi unless you're in it" — the teardown block visibly grows a line
every time the script learns to create something new), find a fare (the nearest *living* civilian, not just
the first match — civilians wander, so an empty scan is treated as normal rather than an error), hold them,
mark the pickup and drop a "go here" ring, two "your turn" steps where the learner edits the search radius
and the drop-off distance themselves, and finally deploy as OnKey.

It's one script, built additively in place inside its own dedicated "Tutorial: Taxi Fare" library entry
(guarded so wandering to another script mid-tutorial can never get it clobbered). Every step advances off a
real signal from the bridge — a `"ran"` event carrying the code and its result, `"status"`/`"deployed"` for
the two ends — never a bare "Next" button, and a per-step `need` marker means an unrelated REPL run can't
accidentally advance or fail a step. The two "your turn" steps verify the edit by inspecting the code that
actually ran, and later steps are templated on the learner's own values (radius, drop-off distance) rather
than reverting them. Progress persists across a reload (the 🎓 button becomes "Resume tutorial"), and the
finish panel hands out two small graduation challenges instead of just closing.

The repo's own `ROADMAP.md` states all the Lua in the tutorial was "live-verified against a running game
(incl. the 'Civ' faction string)"; the same entry notes the whole flow is also walked end-to-end in
`tools/vendor/smoke.js` — but on simulated bridge signals, not a live game (see Status, below, for what that
distinction means here).

## A from-scratch rebuild

This is a from-scratch rebuild of an earlier bundled prototype IDE that shipped inside
`mercs2-lua-essentials`'s own `tools/` folder (`tools/mercs2-lua-ide.html`) — this standalone repo is now the
one to use going forward.

## Status

The live-execution path — actually running code against a real game process over the WebSocket — has
complete, non-trivial client code: reconnect with exponential backoff (capped at 3s), ack/result correlation
by nonce tag, and an 8s timeout that never hangs.

The repository's own `ROADMAP.md` goes further than "should work," though: it contains several specific,
first-person claims of live-game verification. A few, quoted directly: the whole Tier-1 batch (templates,
hover docs, grab-target, watch panel, backup/restore, log highlighting, share-link compression) is recorded
as "built, smoke-tested, and browser-verified in one session"; the Object Inspector's guid-handling fix is
recorded as "confirmed live against a running game," matching `Ess.Object.health` values before and after
the `Ess.Name`/`Sys.StringToGuid` round trip; and the tutorial's Lua is recorded as "live-verified against a
running game (incl. the 'Civ' faction string)."

That's developer testimony recorded in the repo, not a captured log or transcript this wiki has inspected —
a meaningfully stronger evidentiary position than "purely theoretical," short of this wiki independently
confirming a live round trip itself. Worth keeping distinct: `tools/vendor/smoke.js` is an automated but
explicitly **simulated** test — it boots the built `dist/index.html` in `jsdom` and stubs `window.WebSocket`
with a fake that never opens (it only ever fires `onclose`, 5ms after construction). Passing it proves the
page's own code boots and its modules behave correctly against canned/simulated signals; it is not evidence
of a real WebSocket round trip to a running game. `ROADMAP.md` itself treats "smoke-tested" and
"browser-verified" as two separate, named things for exactly this reason, and this page does the same.

## See also

- [Live Map](live-map) — the other WebSocket-transport client, tracking a live player position instead of
  running arbitrary code.
- [WebSocket Transport](../lua-bridge-api/websocket) — the wire protocol both tools' `Loader.WsSend`-based
  round trip rides on.
- [Ess.Loop](../ess/timing-input#essloop) — the loop registry the Stop-loops button iterates.
- [Ess.Player](../ess/identity-query#essplayer) — `pose(0)`, the same call Live Map streams every tick.
- [Engine Namespaces](../namespaces/) — this wiki's own documentation of the native surface the IDE's
  second autocomplete layer scrapes.
- [Loader](../lua-bridge-api/loader) and [Stdlib Additions](../lua-bridge-api/stdlib) — full detail on the
  lua-bridge-authored functions (`Loader.*`, the `math` patches, `Tcp.Send`, `assert`) the API reference now
  documents and badges apart from real engine natives.
- [Resident Modules](../resident/) — the 18 modules now browsable in the API reference and covered by the
  Lint pass's missing-`import()` check.
