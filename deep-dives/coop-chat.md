---
title: "A Basic Co-op Text Chat"
parent: Deep Dives
nav_order: 4
---

# Deep Dive: A Theoretical Co-op Text Chat

**Less speculative than it was — display is now confirmed, input is implemented, send is the one piece
still fully unproven.** Display (the [chat/log UI](coop-chat-ui)) has actually been built and run in-game,
engine bug and all. Input (`Loader.PopKeyEvents` and friends, see [lua-bridge API](../lua-bridge-api/loader))
is real and shipped, though not independently confirmed here via an actual live keystroke-capture report.
What's left is send: whether `Net.SendCustomEvent` really crosses the network the way the
[networking deep dive](networking) hopes it does, and whether all three pieces actually work together
end-to-end across two real players — neither has been tested yet.

## The problem, broken into three pieces

1. **Input** — capturing what the player types.
2. **Send** — getting that text to the other player.
3. **Display** — showing it on their screen.

Piece 2's mechanism is described by the [networking deep dive](networking#a-concrete-test-ping-pong-via-a-hijacked-neteventcallback) — the same hijacked-`Alarm.NetEventCallback` pattern that carries a ping/pong tag can just as easily carry a
string message, though whether it actually crosses the network at all remains that page's open question.
Piece 3 has a real, working answer, detailed on its own page: [Building a Chat/Log UI](coop-chat-ui). Piece
1 — capturing what's typed — turned out to have no answer anywhere in the *game's* Lua surface at all:
`LTIStartKeyboardInput`/`LTIEndKeyboardInput` (`resident/mrxguishell.lua`) is the one native hook that
smells like free-text entry, but it's wired to profile-name creation specifically, and whether it accepts
arbitrary text was never tested, because the real answer turned out to live one level down, in
**lua-bridge itself** (the injection tool this whole wiki is built around) — not the game.

## Input: solved — a real lua-bridge addition, not a Lua trick

`OnKey`'s hotkey detection was never happening inside the game's Lua VM at all — it's lua-bridge's own
background thread, polling for whatever small set of virtual-key codes have a registered `OnKey` script
file bound to them. The game's Lua layer was never going to expose text input on its own, because routing
full keyboard state through it was never lua-bridge's job before now.

That's since changed. lua-bridge now ships a real `Loader.*` input API — full documentation on the
[lua-bridge API: Loader](../lua-bridge-api/loader) page — built specifically to unblock this page:
`Loader.PopKeyEvents()` returns every keystroke since the last call as a ring-buffered, edge-triggered
queue (so nothing gets missed to polling timing), gated to the game's own foreground focus so a chat box
built on it can't accidentally capture keystrokes meant for another window. `Loader.ClearKeyEvents()`
gives a clean reset point for the moment a chat box opens. This is a strictly better foundation than the
single on-demand snapshot function originally scoped for this problem — it solves the "don't miss a
keystroke between polls" problem that a plain snapshot function would have pushed onto every script that
used it.

This is still the one piece of any Deep Dive on this wiki that depends on a specific lua-bridge build
rather than just a dropped-in `.lua` file — worth remembering, since every other page here (including the
rest of this one) only assumes a stock install.

## Send: reusing the networking deep dive's mechanism, carrying a string instead of a tag

Whatever ends up capturing the typed text, sending it uses the same mechanism as the networking deep
dive's ping-pong test — `Net.SendCustomEvent("Alarm", 102, {Net.GetHostName(), sMessage}, true)`, event ID
`102` chosen to avoid colliding with `Alarm`'s own real IDs (`0`, `1`) and the ping-pong test's `100`/`101`.
The receiving side extends the exact same override from the networking deep dive with one more branch,
now displaying into the real chat UI instead of a placeholder:

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
    CoopChatUI:AddMessage(tostring(sSender) .. ": " .. tostring(sMessage))
  else
    fOriginalCallback(nEventType, tArgs)
  end
end
```

## Display: solved — see its own Deep Dive

Full writeup, including a real confirmed engine bug and the workaround for it, on
[Building a Chat/Log UI](coop-chat-ui). Short version: `MrxGuiTextBuffer` (the engine's own built-in
scrolling-message-log widget) has a genuine crash bug in its documented constructor, worked around by
calling a second, bug-free internal function directly. The result is `CoopChatUI`, a small reusable
module — `CoopChatUI:AddMessage(sText)` to push a line, `CoopChatUI:Toggle()` to show/hide,
`CoopChatUI:SetInputText(sText)` for a live-updating "what am I typing" preview — confirmed working by
live testing as a standalone HUD element.

## Known limitations of this whole page

- **Requires a lua-bridge build that includes the `Loader` input functions.** Real and implemented, but
  still not part of every lua-bridge install by default — see the
  [lua-bridge API section](../lua-bridge-api/) note on that.
- **Display is confirmed standalone, not as part of a working chat flow.** `CoopChatUI` was built and run
  in-game successfully on its own; wiring it up to real keystrokes and a real second player hasn't been
  tested as one connected pipeline yet.
- **Send is still the one fully unproven piece.** If `Net.SendCustomEvent` doesn't actually cross the
  network the way the [networking deep dive](networking) hopes it does, nothing here reaches a second
  player regardless of how solid input and display are individually.
- **`LTIStartKeyboardInput`/`LTIEndKeyboardInput` remains untested** as a possible game-native alternative —
  moot now that the lua-bridge-side input API is real, but worth remembering it exists.
