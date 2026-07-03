---
title: "A Basic Co-op Text Chat"
parent: Deep Dives
nav_order: 4
---

# Deep Dive: A Theoretical Co-op Text Chat

**Speculative, not live-tested — but less speculative than it was.** Input and display are now backed by
real, implemented pieces rather than plans (see below); what's still unproven is assembling them
end-to-end across two actual players, and that still depends entirely on the transport claims made in the
[networking deep dive](networking) this page builds on — if `Net.SendCustomEvent` doesn't actually cross
the network the way that page hopes it does, none of this sends anywhere either.

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

- **Requires a lua-bridge build that includes the `Loader` input functions.** Real and implemented, but
  still not part of every lua-bridge install by default — see the
  [lua-bridge API section](../lua-bridge-api/) note on that.
- **Nothing here has been live-tested end-to-end across two players** — input and display are each backed
  by real implemented pieces individually, but assembling the whole chat flow in an actual co-op session
  hasn't been reported yet.
- **Depends entirely on the networking deep dive's unconfirmed transport claim** — if `SendCustomEvent`
  doesn't actually cross the network symmetrically, this doesn't send anything either.
- **`LTIStartKeyboardInput`/`LTIEndKeyboardInput` remains untested** as a possible game-native alternative —
  moot now that the lua-bridge-side input API is real, but worth remembering it exists.
