---
title: Loader
parent: lua-bridge API
nav_order: 1
---

# Loader

## Overview

`Loader` is a global table lua-bridge itself registers — there's no `.lua` file behind it and no engine
namespace to enumerate, unlike everything in [Engine Namespaces](../namespaces/). It's registered through
the same custom-ABI `luaL_register` path used for `Tcp.Send`, and re-registered on every queue pump
specifically so a `_G` wipe across a game-state transition (level load, menu transition) can't strand the
globals — you don't need to re-`import` or re-check for it after a level change.

This page documents it directly from the implementation, by the person who wrote it — a different kind of
source than the reverse-engineered [Engine Namespaces](../namespaces/) pages, which infer behavior from
`pairs()` enumeration and decompiled call sites. Treat function behavior here as accurate to the
implementation; "confirmed working by live testing" language is reserved for claims actually verified by
pressing keys and observing the result in-game, which hasn't been reported yet for the newer input
functions below.

## Why the input functions exist

Every attempt to find continuous, general-purpose input in the *game's* own Lua surface came up empty —
see the [freecam deep dive](../deep-dives/freecam) for `Event.Button`'s fixed 4-action vocabulary,
`Event.Minigame`'s motion-pulse-not-continuous behavior, and bare widgets never receiving dispatch. The
[co-op chat deep dive](../deep-dives/coop-chat) hit the same wall trying to capture typed text, and
proposed a small lua-bridge-side addition as the fix. `Loader.GetKeyboardState`/`IsKeyDown`/`PopKeyEvents`/
`ClearKeyEvents`/`IsGameFocused` are that addition, actually implemented — and go further than what was
originally scoped, adding edge-triggered event queuing and focus-gating that a simple state-snapshot
function wouldn't have provided on its own.

## Functions

| Function | Signature | Notes |
|---|---|---|
| `Printf` | `Loader.Printf(sMsg)` | Appends a line to `lua_loader_printf.log` next to the `.asi`. Low-noise alternative to the engine's own `Debug.Printf`, which fires thousands of times per frame from stock game scripts — this is the logging call used throughout every Snippet and Deep Dive on this wiki. |
| `GetKeyboardState` | `s = Loader.GetKeyboardState()` | Returns a 256-byte string, one byte per virtual-key code, high bit set if that key is currently pressed. Read a specific key with `string.byte(s, vk + 1) >= 128`. Backed by `GetAsyncKeyState` (system-wide physical keyboard state) — deliberately **not** the similarly-named Win32 `GetKeyboardState()`, which reflects the calling thread's message-queue history and can return stale data depending on which thread ends up calling it. |
| `IsKeyDown` | `b = Loader.IsKeyDown(vk)` | Beginner-friendly single-key predicate — wraps one `GetAsyncKeyState` call and returns a plain boolean, for when you only care about one key and don't want to index a 256-byte string yourself. |
| `PopKeyEvents` | `s = Loader.PopKeyEvents()` | Returns a string of raw VK-code bytes, one byte per up→down edge (keypress) observed since the last call, in press order. Filled continuously by a dedicated ~60Hz C-side sampler thread into a 128-slot ring buffer — a script only needs to poll this once per frame to never miss a keystroke to timing, unlike hand-rolling edge detection over `GetKeyboardState`/`IsKeyDown` snapshots yourself. Returns an empty string when no keys have been pressed since the last call. **Focus-gated**: keystrokes are silently dropped while the game process isn't the foreground window, specifically so a chat box, key-rebind UI, or debug console built on this can't accidentally capture keystrokes meant for a different application. |
| `ClearKeyEvents` | `Loader.ClearKeyEvents()` | Drops every buffered event without returning them. Meant as an explicit reset point — e.g. call this the instant a chat input box opens, so whatever the player was pressing right before opening it doesn't leak in as the first characters typed. |
| `IsGameFocused` | `b = Loader.IsGameFocused()` | Returns whether the foreground window belongs to the game's own process, via process-ID match rather than window-handle/style checks — so it stays correct regardless of borderless/fullscreen/multi-window setups. This is the same check gating `PopKeyEvents` internally, exposed directly in case a script wants to branch on focus state itself (e.g. pause a typing UI rather than silently losing keystrokes). |
| `SaveVar` | `Loader.SaveVar(sKey, xValue)` | **New in v0.3.0.** Persists a number, string, or boolean under `sKey`, surviving a full game restart. See [Persistence](#persistence) below. |
| `LoadVar` | `x = Loader.LoadVar(sKey)` | **New in v0.3.0.** Reads back a value saved with `SaveVar`, preserving its original type. Returns `nil` for a key that was never saved. |
| `GetLoadPhase` | `nIndex, sName = Loader.GetLoadPhase()` | **New in v0.5.0.** Where the current world load has gotten to on loadprobe's 0..20 phase ladder — e.g. `11` is `"Player spawn"`, `20` is `"World fully loaded (GlobalExit)"` — so a script can confirm it's actually in a world before touching entities, instead of inferring that from whether an `OnLoad` hook has fired. Returns `-1, "none"` before any load has been observed, or whenever tracking is off, and resets at the start of each new load so it tracks the *current* load rather than a process-wide high-water mark. The scan feeding this is confined to the duration of an actual load — it stops once the fully-loaded phase is reached and re-arms for the next load — so the cost sits inside a loading screen, not the steady-state per-frame loop. Ini lever: `loader_track_phase = 0` disables tracking (and this then always reports `-1`). |
| `LoadFile` | `bLoaded = Loader.LoadFile(sRelPath)` | **New in v0.5.0.** Executes another `.lua` file, resolved relative to `<game>/scripts/`, synchronously, on the calling VM — a way for two scripts to share library code, previously only possible via `_G` pollution from an `OnBoot` script (see the re-arm fix below for why that's fragile). Rejects absolute paths and any `..` segment, and refuses to run while another `LoadFile` is already in progress — which also stops a file from loading itself. Pairs with `_`-prefixed directories (below): put shared helpers somewhere like `scripts/OnLoad/_lib/`, which the folder scanner skips, then pull one in with `Loader.LoadFile("OnLoad/_lib/util.lua")`. Returns `true` once the file is found and handed to the executor — a runtime error *inside* the loaded file doesn't make this `false`; that error is logged and reaches the same live Printf/WebSocket feed as `OnBoot`/`OnLoad` (see below), through its own separate 4 KB result buffer. |

## OnBoot and OnLoad re-arm after a menu round-trip

This is the single most important fix in v0.5.0 — worth its own section rather than a line in the table above, because of how completely it was broken and how quietly it broke.

**The bug, present in every lua-bridge build before v0.5.0:** exiting to the main menu wipes `_G`, and the next load builds fresh Lua VMs — confirmed live, two new `lua_State`s per load. `OnBoot` and `OnLoad` were each guarded by a once-per-process flag, so after that first menu round-trip, neither one ever ran again for the rest of the process's life. Whatever a startup script had installed — functions, tables, hooks, an entire framework — was silently gone and stayed gone, not just for the rest of that level, but until the whole game process was restarted. This was confirmed live two independent ways in the same session: a sentinel value planted directly in `_G`, and a real 616 KB framework loaded from `OnLoad`, were both `nil` after a single trip to the main menu and back.

This is a different mechanism from the `Loader` table's own re-registration described in the [Overview](#overview) above, and that part was never broken — `Loader.Printf` and every other `Loader.*` function kept working fine after a menu trip, because lua-bridge re-registers its own globals against every newly-seen VM regardless of this bug. What broke was anything a *script* put into `_G` (or anywhere else) from inside `OnBoot`/`OnLoad` — because the once-per-process guard meant those scripts themselves never got a second chance to run and reinstall it.

**Practical effect: this means any framework or mod relying on `OnLoad` to install itself — including [Ess](../ess/) itself — was silently non-functional after the player returned to the main menu even once, on any lua-bridge build before v0.5.0.** If a mod or framework "just stopped working" mid-session with nothing obviously wrong and no error, a main-menu trip is the first thing to suspect on a pre-0.5.0 build.

**The fix:** both `OnBoot` and `OnLoad` now re-arm correctly. Detection hangs off `CaptureL` (the function that validates and registers a Lua VM the first time lua-bridge sees it) noticing a genuinely fresh `lua_State`: since a menu round-trip demonstrably builds new VMs, a previously-unseen `L` arriving after a load cycle has already completed *is* the "we started over" signal, and checking for it costs nothing extra, because that slow path only ever runs for VMs lua-bridge has never seen before. The initial boot's own second VM is correctly excluded from triggering a false re-arm, since it appears before `OnLoad` has run even once. Level-to-level transitions do **not** wipe `_G` and correctly do **not** re-trigger this — it's specifically a main-menu round-trip, not every level change, that resets things.

`scripts/OnKey/` is re-scanned at the same moment, so a `.lua` file dropped into that folder mid-session is picked up with no restart needed. That required making `InitializeKeyScripts` safe to call more than once: previously, a second call would have left two hotkey-polling threads running at the same time, silently firing every hotkey twice per press. It now spawns its polling thread exactly once and swaps the live script table under a lock on every rescan.

Ini lever: `loader_rearm_on_menu = 0` restores the old, broken, once-per-process behavior, for the unlikely case some workflow actually depends on `OnBoot`/`OnLoad` running exactly once per process.

**Also fixed in the same release: loader script results now reach live clients.** `OnBoot`/`OnLoad`/`LoadFile` results and errors now also go out through the `Loader.Printf` log and the WebSocket `{"type":"log"}` feed (see [WebSocket Transport](websocket)) — previously they only reached the local `lua_bridge_DEV.log` file, so a connected REPL or browser client never saw a startup-script failure at all. `OnBoot`/`OnLoad`'s own result buffer also grew from 4 KB to 16 KB, matching the main execution queue's buffer, since it was silently truncating longer results and error messages before. (`LoadFile`'s result buffer, noted above, is separate and is still 4 KB.)

**Also deprecated in the same release: `loader_delay_ms`.** This used to `Sleep()` the game thread between scripts within one `OnBoot`/`OnLoad` batch. It's now a documented no-op: `ExecuteLuaFolder` runs *on* the game thread, so sleeping there could only freeze the engine — there was never anything else running for the sleep to let "settle." The setting is still parsed so an existing `lua_bridge_DEV.ini` with it set doesn't break; it just no longer does anything.

## `lua_loader.ini` and shared library code

Not to be confused with `lua_loader_data.ini` — the separate file [Persistence](#persistence) below uses for `SaveVar`/`LoadVar`. `lua_loader.ini`, next to `lua_bridge.asi`, is the config file that sets execution order for `[OnBoot]`/`[OnLoad]` scripts and hotkey bindings for `[OnKey]` scripts (the `KEYVAL` convention described in [Your First Mod](../first-mod) and [OnKey Scripts](../sample-scripts-onkey)).

**No longer shipped in the release zip, as of v0.5.0.** `EnsureLoaderIniHeader` — code that predates this release — writes a fresh, commented `lua_loader.ini` the first time it doesn't find one, and does nothing if the file already exists. Pre-0.5.0 releases shipped a stub `lua_loader.ini` anyway, which defeated that generator entirely: a fresh install got a stripped file referencing three sample scripts that weren't even in the zip, and never saw the commented Virtual-Key-code reference the generator actually writes. As of v0.5.0 the file is simply not bundled, so a fresh install finally gets the generator's real output instead. **Existing installs keep their current `lua_loader.ini` exactly as it is** — this only changes what a brand-new install sees on first run.

**Per-script disable, new in v0.5.0.** Setting a script's value in `lua_loader.ini` to `off`, `no`, or `disabled` (case-insensitive) skips it without deleting the file — this works for `[OnBoot]`/`[OnLoad]` order entries and `[OnKey]` bindings alike. This deliberately does **not** reuse `0` for the same purpose: an existing config may already use `0` to mean "run first," a valid load-order value, and repurposing it would have silently broken those configs.

**`_`-prefixed directories are never scanned, new in v0.5.0.** A directory whose name starts with `_` — e.g. `scripts/OnLoad/_lib/` — is skipped entirely by the recursive folder scan, so a `.lua` file placed there never auto-runs as its own script. Before this, the scan picked up every `.lua` file under `OnBoot`/`OnLoad`/`OnKey` no matter how deep, so there was nowhere to put shared helper code without it also running on its own as an independent script. This is meant to pair directly with `Loader.LoadFile` above:

```lua
-- scripts/OnLoad/MyFramework.lua -- runs normally, like any OnLoad script
Loader.LoadFile("OnLoad/_lib/Util.lua")  -- scripts/OnLoad/_lib/ is never auto-run on its own
```

Also new in v0.5.0, and lower-stakes: **source-encoding normalization.** The engine's own text renderers consume strings as single-byte CP1252, so a `.lua` file saved as UTF-8 with a non-ASCII character — `Möbius`, say — used to render corrupted on-screen (`MÃ¶bius`) even though lua-bridge itself never touched the bytes wrong; it's now fixed at load time instead. `loader_source_encoding = auto` (the current default) transcodes a file to CP1252 only when it's valid UTF-8 *and* contains a byte >= 0x80 — pure-ASCII files and already-CP1252 files are both left untouched. BOMs are stripped unconditionally regardless of this setting, since a UTF-8 BOM is a hard Lua 5.1 syntax error. Set `loader_source_encoding = off` for the raw pre-0.5.0 passthrough.

## Persistence

The first lua-bridge addition that lets a script do something previously impossible on this platform:
survive a game restart with saved state, without touching (or risking corrupting) the actual game save —
see [Contract Framework](../contract-framework/)'s save-safety writeup for why touching the real save file
is a real, cited risk this sidesteps entirely for anything that doesn't need to persist *inside* a
specific save slot.

```lua
Loader.SaveVar("MyMod_Progress", 18)
Loader.SaveVar("MyMod_TutorialSeen", true)
Loader.SaveVar("MyMod_Setting", "hardcore")

local nProgress = Loader.LoadVar("MyMod_Progress") or 0   -- standard nil-default idiom for a fresh install
```

- **Types are preserved across the round trip** — `SaveVar("count", 5)` then `LoadVar("count")` returns the
  *number* `5`, not the string `"5"`. Same for booleans and strings.
- **Stored on disk** as `lua_loader_data.ini`, in the same `scripts/` folder as `lua_bridge.asi` itself
  (alongside `lua_loader_printf.log`/`lua_bridge_DEV.ini`) — human-readable and safe to hand-edit while the
  game is closed:
  ```ini
  ; Format: key=type:value  (n=number, s=string, b=boolean 0/1)
  MasterCheatMenu_Progress=n:18
  MyMod_TutorialSeen=b:1
  MyMod_Setting=s:hardcore
  ```
- **Atomic writes.** Each save writes to a temporary file first, then swaps it in
  (`MoveFileExA(MOVEFILE_REPLACE_EXISTING)`) — a crash mid-write can't leave a truncated, unparseable file
  behind.
- **Flat, shared namespace** — every script's keys live in the same file. **Prefix your keys with your
  script's own name** (`MyMod_progress`, not `progress`) to avoid colliding with another mod's data; there's
  no per-script isolation enforced for you.
- **String memory is bounded, not free.** Each `SaveVar` call with a string value allocates a fresh
  internal string; an *older* value stays valid for as long as some Lua variable still holds a reference to
  a prior `LoadVar` result (ordinary Lua semantics — nothing special about this API), so memory grows with
  write *frequency*, not just key count. In practice this is small (roughly 100 KB for 1,000 writes of a
  100-character string) and bounded for a normal session — worth knowing if a script saves the same key in
  a tight loop rather than on meaningful state changes.

## OnKey dispatch behavior

Separate from the `Loader` table's own functions above, this section covers `LoaderKeyThread` — the
background thread that actually detects a hotkey press and runs the matching `scripts/OnKey/*.lua` file.
Safety features and binding behavior here have grown across v0.2.0, v0.2.1, and v0.5.0 — all of them
change what happens around a keypress, or how a binding is parsed, rather than anything a script calls
directly.

- **Per-script reentrancy cooldown (v0.2.1).** Rapid double-presses of the same hotkey used to queue two
  back-to-back runs of a script — sequential, not concurrent, but many OnKey scripts on this wiki aren't
  written to be reentrant, and a second run executing on state the first run left behind (a half-open
  menu, a partially-typed console buffer) could destabilize the engine. `LoaderKeyThread` now tracks
  `last_fired_tick` per script and skips re-firing if the last fire was within
  `loader_onkey_cooldown_ms` (default **250 ms**) of the current one. The *first* time this throttles a
  given script in a session, it logs `[!] lua_bridge: OnKey '<key>' throttled (...)` so you notice the
  cooldown engaging instead of silently wondering why a press didn't register; subsequent throttles for
  that same script are silent, to avoid log spam. Set `loader_onkey_cooldown_ms = 0` in
  `lua_bridge_DEV.ini` to disable it entirely. Implemented with unsigned subtraction, so it's correct
  across `GetTickCount` wraparound (~49.7-day uptime cycle) rather than glitching once every 49 days.
- **Missing-file guard (v0.2.0).** Pressing a hotkey whose backing `.lua` file had been deleted after the
  game booted (e.g. mid-session cleanup, a renamed script) could destabilize the game. `GetFileAttributesA`
  now runs before every `fopen`; a missing file logs a clear
  `[!] lua_bridge: OnKey '<key>' bound to missing file: <name> (skipped)` warning and is safely skipped
  instead.
- **Focus-gating fix (v0.5.0).** `LoaderKeyThread` itself was not gated on window focus before v0.5.0 —
  even though its sibling `LoaderKeyEventThread` (the thread feeding `PopKeyEvents` above) always was, and
  the README already documented OnKey as focus-gated. In practice, pressing `F5` to refresh a browser tab,
  or `F11` to go fullscreen in some other application, could silently run a game script in the background.
  Both threads are now gated on the same `IsGameFocused()` check, with each script's edge state cleared on
  focus loss, so refocusing the game with a key still held down doesn't fire on that stale transition. Ini
  lever: `loader_onkey_require_focus = 0` restores the old always-fires-regardless-of-focus behavior.
- **Modifier combinations (v0.5.0).** `ctrl+`, `shift+`, and `alt+` prefixes now work in any order in a
  `KEYVAL`/`lua_loader.ini` binding (`ctrl+F5`, `shift+alt+k`, etc.). Held modifiers must match a binding
  **exactly**, so a plain `F5` binding and a `ctrl+F5` binding can drive two different scripts independently
  — the one behavior change for pre-existing bindings is that a plain `F5` no longer also fires while
  ctrl/shift/alt happens to be held. Ini lever: `loader_onkey_exact_modifiers = 0` restores the old
  modifier-insensitive matching, where holding extra modifiers never stopped a plain binding from firing.
- **Many more bindable keys (v0.5.0), purely additive** — every key name that worked before v0.5.0 still
  resolves identically. New: `numpad0`-`numpad9` and the numpad operators, `F13`-`F24`,
  `capslock`/`numlock`/`scrolllock`/`pause`/`printscreen`, left/right-specific modifiers
  (`lshift`/`rshift`/`lctrl`/`rctrl`/`lalt`/`ralt`), the punctuation/OEM row (`tilde`, `minus`, `plus`,
  brackets, `backslash`, `semicolon`, `quote`, `comma`, `period`, `slash`), and the thumb buttons
  `mouse4`/`mouse5`. `tilde` — the traditional console key — was previously unbindable, which is exactly
  what pushed people onto F-keys that browsers also claim.
- **Unrecognized key names now warn loudly (v0.5.0).** A typo like `pgup`, or `F13` on a pre-0.5.0 build,
  used to resolve silently to VK 0 and just never fire — indistinguishable in the log from a correctly
  working binding. A name that doesn't resolve (and isn't the explicit `unassigned` sentinel) now logs a
  warning naming the valid forms at registration time, so a dead binding is visible immediately instead of
  only once you notice the hotkey "doesn't work."
- **Binding collisions are now logged at registration (v0.5.0).** Two scripts sharing one key (same VK code
  *and* the same modifier mask) is a supported, intentional feature — but it's also exactly what an
  accidental `KEYVAL` typo-collision looks like, and previously nothing logged it either way. Both cases now
  produce a log line naming both scripts (bindings that resolve to nothing, like several scripts left at
  `unassigned`, don't trigger this).
- **The oversize-script cap now matches the executor's real buffer (v0.5.0).** The loader used to check a
  script's file size against a separate 1 MB constant that could disagree with the executor's own buffer; it
  now checks against that same buffer, so "the loader accepted this file" and "the executor can run it"
  can't disagree with each other. This cap is shared by every script the loader runs — `OnBoot`, `OnLoad`,
  `OnKey`, and `LoadFile` alike — and exceeding it is now logged instead of the file being silently skipped.

**Practical effect for scripts on this wiki:** none of the persistent, `_G`-guarded OnKey tools documented
here (the [destroyer tool](../deep-dives/destroyer-vehicle), [master cheat menu](../cheat-menu), etc.) are
designed to fire faster than 250ms apart under normal use — deliberate menu navigation is well outside
that window. The cooldown mainly guards against a stuck/bouncing physical key or a scripted rapid-fire
input source, not normal play.

## Notes for modders

- **`PopKeyEvents` is the right tool for "the player typed something"**; `GetKeyboardState`/`IsKeyDown` are
  the right tools for "is this specific key currently held" (movement, aiming-style continuous input).
  Don't build a text-input loop on repeatedly polling `GetKeyboardState` for edges yourself — the ring
  buffer already solved the "don't miss a keystroke between polls" problem, and hand-rolling it again on
  top would just reintroduce timing gaps the ring buffer exists to avoid.
- **`IsKeyDown`/`GetKeyboardState`/`PopKeyEvents`/`IsGameFocused` are measured-safe in a per-frame hot
  loop, as of v0.3.0.** Earlier builds carried defensive validation on every call; profiling showed that
  overhead was unnecessary (the engine already guarantees a valid Lua state on this call path) and removed
  it, dropping per-call cost from roughly 15 µs to about **0.81 µs** (~1.24 million calls/sec, measured over
  500,000 calls). A script can call one of these tens of thousands of times in a single frame at 60 FPS and
  stay under 2% of the frame budget — this is no longer a reason to hand-roll batching or throttle these
  specific calls, on v0.3.0+. Several deep dives on this wiki (e.g. [ForgeCam](../deep-dives/forgecam),
  [MissionForge](../deep-dives/mission-forge)) reduced *call count* for these functions before this number
  existed, based on observed framerate impact rather than a measured per-call cost — that call-count
  reduction is still good practice on any lua-bridge version, but the *urgency* of it is lower on v0.3.0+
  than it was when those pages were written.
- **A silently-dead OnKey binding is much easier to catch as of v0.5.0.** A typo in a `KEYVAL`/
  `lua_loader.ini` key name — or a key that simply didn't exist yet on your build, like `F13` before
  v0.5.0 — used to resolve to VK 0 and just never fire, with nothing in the log to tell that apart from a
  correctly-bound key nobody had pressed yet. As of v0.5.0 that case logs a warning naming the problem key
  — see [OnKey dispatch behavior](#onkey-dispatch-behavior) above. If a hotkey "does nothing," checking the
  exact spelling against [Microsoft's Virtual-Key reference](https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes)
  is the first thing to try.
- **These are lua-bridge additions, not engine features** — the keyboard input functions shipped in the
  stock install as of **v0.1.6**; `SaveVar`/`LoadVar` and the hot-path performance guarantee above are
  **v0.3.0+** only; `GetLoadPhase`, `LoadFile`, the `_`-prefixed-directory convention, per-script disable,
  the `OnBoot`/`OnLoad` menu re-arm, and every `OnKey` addition described above (focus-gating for
  whole-script hotkeys, modifier combinations, the expanded key list, and warnings for bad key names and
  binding collisions) are **v0.5.0+** only. See the [lua-bridge API](./) section landing page for the full
  per-version breakdown.
