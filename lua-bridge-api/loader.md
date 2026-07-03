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

## Notes for modders

- **`PopKeyEvents` is the right tool for "the player typed something"**; `GetKeyboardState`/`IsKeyDown` are
  the right tools for "is this specific key currently held" (movement, aiming-style continuous input).
  Don't build a text-input loop on repeatedly polling `GetKeyboardState` for edges yourself — the ring
  buffer already solved the "don't miss a keystroke between polls" problem, and hand-rolling it again on
  top would just reintroduce timing gaps the ring buffer exists to avoid.
- **These are lua-bridge additions, not engine features** — included in the stock install as of
  **v0.1.6**; see the [lua-bridge API](./) section landing page for what that distinction means in
  practice otherwise (mainly: make sure you're not on an older build that predates them).
