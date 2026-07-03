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
string message. Piece 3 has a fast, already-proven answer too. Piece 1 is the genuinely hard part, and
worth being upfront about: **there is no confirmed general-purpose text-input API anywhere in this
engine's Lua surface.** `LTIStartKeyboardInput`/`LTIEndKeyboardInput` (`resident/mrxguishell.lua`) is the
one real native hook that smells like free-text entry, used for profile-name creation — if it turns out
to be repurposable for arbitrary text, it would make everything below unnecessary. Untested, so this page
doesn't rely on it.

## Input: genuinely unsolved — deliberately not papering over it

`OnKey`'s hotkey binding resolves individual Windows virtual-key codes (confirmed, ordinary behavior —
see [Your First Mod](../first-mod)), which means a "one tiny dedicated script per character" approach is
*technically* buildable today. It was cut from this page on purpose: two dozen-plus near-identical files
just to capture typing is real clutter for a highly speculative feature, and it still wouldn't solve the
harder half of the problem (nothing stops the normal gameplay action already bound to that same key from
also firing while "typing" — `Player.SetInputEnabled` is a candidate for suppressing that, untested,
and might block the chat-input scripts right along with everything else).

**The right first move is testing `LTIStartKeyboardInput`/`LTIEndKeyboardInput`** (`resident/mrxguishell.lua`)
directly — the one real native text-entry hook already found, currently wired to profile-name creation.
If it turns out to accept arbitrary text rather than being hardcoded to that one field, it solves input
outright and this whole section becomes moot. If it doesn't pan out, the next step is looking for *other*
angles before falling back to anything resembling the per-key-script approach — this page intentionally
leaves that search undone rather than committing to a clunky answer prematurely.

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

- **Input is genuinely unsolved.** `LTIStartKeyboardInput`/`LTIEndKeyboardInput` is the one real lead and
  hasn't been tested. This page deliberately doesn't commit to a fallback (like a script per character)
  until that lead is actually checked and other angles have had a chance first.
- **Nothing here has been live-tested**, send or display included.
- **Depends entirely on the networking deep dive's unconfirmed transport claim** — if `SendCustomEvent`
  doesn't actually cross the network symmetrically, this doesn't send anything either.
