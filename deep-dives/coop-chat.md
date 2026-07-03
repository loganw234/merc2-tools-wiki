---
title: "A Basic Co-op Text Chat"
parent: Deep Dives
nav_order: 4
---

# Deep Dive: A Theoretical Co-op Text Chat

**Speculative, not live-tested.** Same framing as the [networking deep dive](networking) this one builds
directly on: everything below is "the pieces exist and plausibly compose," not "this was confirmed
working in a real co-op session." It also depends on the transport claims made in that page — if
`Net.SendCustomEvent` doesn't actually cross the network the way that page hopes it does, none of this
sends anywhere either.

## The problem, broken into three pieces

1. **Input** — capturing what the player types.
2. **Send** — getting that text to the other player.
3. **Display** — showing it on their screen.

Piece 2 is already solved by the [networking deep dive](networking#a-concrete-test-ping-pong-via-a-hijacked-neteventcallback) — the same hijacked-`Alarm.NetEventCallback` pattern that carries a ping/pong tag can just as easily carry a
string message. Piece 3 has a fast, already-proven answer too. Piece 1 — capturing what's typed — turns
out to have no answer anywhere in the *game's* Lua surface at all, confirmed or otherwise:
`LTIStartKeyboardInput`/`LTIEndKeyboardInput` (`resident/mrxguishell.lua`) is the one native hook that
smells like free-text entry, but it's wired to profile-name creation specifically, and whether it accepts
arbitrary text is untested. The real answer turned out to live one level down, in **lua-bridge itself**
(the injection tool this whole wiki is built around) — not the game.

## Input: a lua-bridge-side addition, not a Lua trick

`OnKey`'s hotkey detection isn't happening inside the game's Lua VM at all — it's lua-bridge's own
background thread (`LoaderKeyThread`, in `lua_bridge_DEV.c`), polling `GetAsyncKeyState()` at 30Hz for
whatever small set of virtual-key codes have a registered `OnKey` script file bound to them. A "script
per character" approach (checked and rejected earlier as directory clutter) would have worked, but only
by working around a limitation that doesn't need to exist in the first place — the game's Lua layer was
never going to expose text input, because it was never lua-bridge's job to route full keyboard state
through it as a `KEYVAL` match.

The actual fix: add one new function to lua-bridge's existing `Loader.*` table —
`Loader.GetKeyboardState()` — that a script can call **on demand** to get a full snapshot of every key's
current state, independent of `OnKey`'s one-script-one-key model entirely. Concretely, this is a small,
well-scoped change given how lua-bridge is already built:

- `Loader.*` functions are registered through a small static table, `loader_lib[]` (currently just
  `{"Printf", LuaLoaderPrintf}`), handed to the game's own `luaL_register` — adding an entry is one line:
  `{"GetKeyboardState", LuaLoaderGetKeyboardState}`.
- That new C function loops over the 256 possible virtual-key codes calling `GetAsyncKeyState()` for
  each — the same underlying call `LoaderKeyThread` already trusts for `OnKey`, **not** the similarly-named
  `GetKeyboardState()` Win32 API, which reflects a calling thread's message-queue history rather than raw
  hardware state and could return stale/empty data depending on which thread ends up calling it.
- The result gets packed into either a raw 256-byte Lua string (cheapest to implement; a script reads it
  with `string.byte(sState, vk + 1) >= 128`) or a Lua table of 256 booleans (nicer to consume,
  `if tKeys[65] then`) — either works, the string form is simpler on the C side.
- `LoaderKeyThread`/`InitializeKeyScripts`/the existing `OnKey` file-matching behavior are **completely
  untouched** by this — it's a pure addition, not a modification.

Performance is a non-issue either way it's implemented: this only spends any CPU at all in the instant a
Lua script actually calls it, at whatever cadence that script chooses — genuinely zero idle cost, better
than even the (already negligible) cost of widening `LoaderKeyThread`'s own poll loop would have been.

This is the one piece of any Deep Dive on this wiki that requires touching lua-bridge's own native source
rather than dropping in a `.lua` file — worth calling out plainly, since every other page here (including
the rest of this one) only assumes a stock lua-bridge install.

## Send: reusing the networking deep dive's mechanism, carrying a string instead of a tag

Whatever ends up capturing the typed text, sending it is already solved —
`Net.SendCustomEvent("Alarm", 102, {Net.GetHostName(), sMessage}, true)`, event ID `102` chosen to avoid
colliding with `Alarm`'s own real IDs (`0`, `1`) and the ping-pong test's `100`/`101`. The receiving side
extends the exact same override from the networking deep dive with one more branch:

```lua
import("Alarm")

local fOriginalCallback = Alarm.NetEventCallback

Alarm.NetEventCallback = function(nEventType, tArgs)
  if nEventType == 100 then
    -- ping-pong test, see the networking deep dive
  elseif nEventType == 101 then
    -- ping-pong test, see the networking deep dive
  elseif nEventType == 102 then
    local sSender, sMessage = tArgs[1], tArgs[2]
    import("MrxTutorialManager")
    MrxTutorialManager.ShowMessage(tostring(sSender) .. ": " .. tostring(sMessage))
  else
    fOriginalCallback(nEventType, tArgs)
  end
end
```

## Display: the fast, already-proven answer

`MrxTutorialManager.ShowMessage(sMessage)` is already confirmed working by live testing (see
[Snippets: Show a custom HUD message](../snippets#show-a-custom-hud-message-with-icon-and-sound)) —
reusing it here means zero new UI work for a first version. The honest limitations that come with that
shortcut, carried over directly from what's already documented about it:

- **No scrollback.** It's one message at a time, in the same popup widget the game's own tutorials use.
  A second incoming chat message before the first is dismissed will either get suppressed or overwrite
  it, not queue — this page hasn't tested which.
- **No auto-hide.** The message stays up until something explicitly clears it
  (`MrxTutorialManager.HideMessage()`), so a real version would want a timer
  (`Event.Create(Event.TimerRelative, {5}, MrxTutorialManager.HideMessage)`, the same pattern used
  throughout [Snippets](../snippets)) to clear each message after a few seconds automatically.
- **It's the game's own tutorial-hint widget**, not a purpose-built chat box — visually, an incoming chat
  message will look identical to a tutorial hint, book icon and notification sound included, which may or
  may not be desirable.

A genuine persistent, multi-line chat log — the "other UI element we'd likely have to make" — would need
real custom widget work: `MrxGuiBase.Widget:new({})` (the same bare-widget creation call investigated,
and found insufficient on its own, for continuous input in the [freecam deep dive](freecam)) plus building
out actual text rendering and layout for it, which is a meaningfully bigger undertaking than anything on
this page and hasn't been attempted here.

## Known limitations of this whole page

- **The input plan requires a lua-bridge rebuild, not just a script.** `Loader.GetKeyboardState()` doesn't
  exist in lua-bridge today — this page describes a concretely-scoped addition, not a shipped feature.
  Until it's actually written and built, this piece is still just a plan.
- **Nothing here has been live-tested**, input, send, or display.
- **Depends entirely on the networking deep dive's unconfirmed transport claim** — if `SendCustomEvent`
  doesn't actually cross the network symmetrically, this doesn't send anything either.
- **`LTIStartKeyboardInput`/`LTIEndKeyboardInput` remains untested** as a possible game-side alternative —
  not pursued further once the lua-bridge-side plan above turned out to be the more concrete, controllable
  option, but worth remembering it exists.
