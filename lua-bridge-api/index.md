---
title: lua-bridge API
nav_order: 13
has_children: true
has_toc: false
---

# lua-bridge API

Every other reference section on this wiki — [Resident Modules](../resident/), [Engine Namespaces](../namespaces/) —
documents things that are part of Mercenaries 2 itself: real game code, reachable because lua-bridge gives
a live Lua console into the running engine. This section is different. It documents globals that
**lua-bridge itself adds** to that environment — functions with no `.lua` file behind them and no engine
namespace to enumerate via `pairs()`, because the game never shipped them. They exist purely because
modding needed something the engine's own Lua surface didn't expose.

That distinction matters for one practical reason: everything in [Engine Namespaces](../namespaces/) is
guaranteed present in any copy of the game lua-bridge can attach to, regardless of which lua-bridge build
you're running. Everything here ships in the stock lua-bridge install — but which specific pieces you can
rely on depends on which build you're running, since this section has grown across several releases:

| Added in | What |
|---|---|
| v0.1.6 | `Loader`'s keyboard input API; `math.sin`/`math.cos` |
| v0.2.0 | The rest of `math.*` (trig, hyperbolic, `sqrt`/`log`/`log10`, low-level number manipulation, `random`/`randomseed`, `pi`/`huge`) and `assert(v, msg)`; missing-file guard for OnKey scripts |
| v0.2.1 | Per-script OnKey reentrancy cooldown; fixes to `assert`'s error location and the stdlib polyfill's own success/failure logging |
| v0.3.0 | `Loader.SaveVar`/`Loader.LoadVar` (key-value persistence across game restarts); a hot-path rewrite dropping `Loader`'s input functions and every `math.*` function to sub-microsecond, measured-safe-in-a-per-frame-loop cost |
| v0.3.1 | Watchdog reliability patch — a new detection path catches the bridge hanging *inside* a native call from Lua (e.g. a wedged D3D call, an infinite loop) that previously blocked the very detours the watchdog relied on to notice; no user-facing API change |
| v0.4.0 | WebSocket transport (same port as the raw-TCP REPL, auto-detected) plus the `Loader.WsSend` global — see [WebSocket Transport](websocket) |
| v0.4.1 | Concurrent WebSocket clients (up to 16 at once) — same wire contract, no user-facing API change, no config change |
| v0.5.0 | Reliability pass on the loader half: `OnBoot`/`OnLoad` now correctly re-run after a main-menu round trip (previously a startup script silently never ran again once you'd visited the main menu, until the game process restarted); two long-standing REPL correctness bugs fixed — a stack-frame corruption bug and the `[ok]`/`[runtime]` result-label bug (see [Getting Started](../getting-started#1-the-repl-fastest-for-iterating)); `Loader.GetLoadPhase()`/`Loader.LoadFile()` added (see [Loader](loader)); OnKey fixes for background-focus gating, modifier-key support (`ctrl+`/`shift+`/`alt+`), and many more bindable keys; `lua_loader.ini` no longer shipped — auto-generated on first run instead |
| v0.5.1 | Two transport-layer correctness fixes, no API change and no config change: the raw-TCP result channel was **one execution behind** whenever a client disconnected before its result arrived — results are now tagged with the raw-TCP session that submitted them and dropped rather than misdelivered (see [Getting Started](../getting-started#if-youre-upgrading-from-before-v051-the-socket-result-channel-was-one-execution-behind)); and WebSocket TEXT frames could carry invalid UTF-8, because bytes `0x80`–`0xFF` were passed through unescaped — now emitted as `\uXXXX` using the real CP1252 mapping (see [Text frame encoding](websocket#text-frame-encoding)). **Behavior change:** OnKey/OnBoot/OnLoad results no longer reach the raw-TCP channel at all; they still go to the log and the WebSocket `{type:"log"}` feed |
| v0.5.2 | Correctness fix, no API change and no config change: on v0.5.0/v0.5.1 the **first Lua chunk of a session could permanently halve the framerate** — 60 fps down to ~25 and never recovering, reproducible on `return 1+1`. Three chained defects, the first of which read an idle REPL as a 186-second stall (see [Loader](loader#the-first-lua-chunk-of-a-session-could-permanently-halve-the-framerate-v052)) |
| v0.5.3 | Correctness fix, no API change and no config change: **`OnLoad` never fired at all if the player alt-tabbed during a level load** — a backgrounded game is throttled hard while the wall clock keeps running, so an ordinary load blew v0.5.2's 60-second milestone-scan ceiling, and the give-up was terminal for the rest of the session. The ceiling is now 300s and a new load cycle clears the give-up (see [Loader](loader#onload-never-fired-if-you-alt-tabbed-during-a-level-load-v053)) |

If you're relying on anything past the keyboard API and basic trig, confirm you're on **v0.2.0 or later**;
for persistence or the hot-loop performance guarantee, confirm **v0.3.0 or later**; for the WebSocket
transport, confirm **v0.4.0 or later** (**v0.4.1 or later** for more than one simultaneous client); and if
you need the loader half to actually be reliable — `OnLoad`/`OnBoot` surviving a main-menu round-trip, or
accurate REPL `[ok]`/`[runtime]` results — confirm **v0.5.0 or later**.

The v0.5.x rows are where that framing stops being about features at all. **v0.5.1, v0.5.2 and v0.5.3 add
no API and no config. They are correctness bars, and anyone on v0.5.0-v0.5.2 should update.** v0.5.2 fixes
a framerate halving triggered by the *first Lua chunk of the session* — it affects v0.5.0 and v0.5.1, it
reproduces on `return 1+1` (a chunk that touches no engine function at all), and once triggered the drop
persists rather than settling back. v0.5.3 then fixes a defect introduced by v0.5.2's own fix: the
60-second ceiling that release put on the load-milestone scan is wall-clock, and a backgrounded game is
throttled hard, so alt-tabbing during a level load blew a budget an on-screen load would never approach —
`OnLoad` never fired, the give-up was terminal, and a startup mod (Ess included) simply never loaded for
the rest of that session. Neither of these was a missing feature on the earlier builds: both were silently
wrong behavior you had no way to see from Lua.

## Available namespaces

- **[Loader](loader)** — logging, the game's first real general-purpose keyboard input API (full
  keyboard-state snapshots, a single-key predicate, an edge-triggered keystroke queue, foreground-focus
  detection), the OnKey dispatch safety behavior added in v0.2.0/v0.2.1 (reentrancy cooldown, missing-file
  guard), and — new in v0.3.0 — `SaveVar`/`LoadVar` key-value persistence across game restarts, the first
  lua-bridge addition that doesn't just fill a gap in a single session's capabilities. The keyboard API was
  added specifically to unblock the [co-op text chat](../deep-dives/coop-chat) idea, whose "Input" problem
  had no answer anywhere in the game's own Lua surface.
- **[Stdlib Additions](stdlib)** — standard Lua 5.1 `math`/base-library functions (full trig, `sqrt`,
  `random`, `assert`, and more) that exist in a normal Lua build but were stripped from this game's
  runtime, patched back in as of v0.2.0.

`Tcp.Send(host, port, msg)` (see the [lua-bridge README](https://github.com/loganw234/Mercenaries2)) is
also a lua-bridge-provided global, registered the same way — not yet written up as its own page here.
