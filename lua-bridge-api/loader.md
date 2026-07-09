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
Two safety features were added here across v0.2.0/v0.2.1, both worth knowing since they change what
happens around a keypress rather than anything a script calls directly.

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
- **These are lua-bridge additions, not engine features** — the keyboard input functions shipped in the
  stock install as of **v0.1.6**; `SaveVar`/`LoadVar` and the hot-path performance guarantee above are
  **v0.3.0+** only. See the [lua-bridge API](./) section landing page for the full per-version breakdown.
