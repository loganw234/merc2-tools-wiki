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

## Input: one `OnKey` script per character (clunky, but fully buildable today)

`OnKey`'s hotkey binding already resolves individual Windows virtual-key codes — that's confirmed,
ordinary behavior (see [Your First Mod](../first-mod)), and it's the one piece of "detect this specific
keypress" machinery this project has never had to guess at. The idea: don't try to capture free-form
typing at all — instead, give every character its own tiny dedicated `OnKey` script, each one checking a
shared "am I in chat mode" flag before doing anything.

Shared state, in `scripts/OnBoot/ChatState.lua` so it exists before any of the per-key scripts need it:

```lua
_G.ChatState = _G.ChatState or {
  active = false,
  buffer = "",
}
```

`scripts/OnKey/ChatToggle.lua` — `Enter` both opens chat mode and sends/closes it on a second press:

```lua
local KEYVAL = "return"  -- must be in the first 10 lines

if not _G.ChatState.active then
  _G.ChatState.active = true
  _G.ChatState.buffer = ""
  Loader.Printf("CHAT: input mode on, start typing")
else
  local sMessage = _G.ChatState.buffer
  _G.ChatState.active = false
  _G.ChatState.buffer = ""
  if sMessage ~= "" then
    import("Alarm")  -- same hijacked module as the networking deep dive's ping-pong test
    Net.SendCustomEvent("Alarm", 102, {Net.GetHostName(), sMessage}, true)  -- 102: unused by Alarm itself
    Loader.Printf("CHAT: sent -> " .. sMessage)
  end
end
```

`scripts/OnKey/ChatLetterA.lua` (repeat this exact pattern for every other letter, `0`-`9`, and a couple
of punctuation keys — tedious, but each file is identical apart from `KEYVAL` and the one character
appended):

```lua
local KEYVAL = "a"  -- must be in the first 10 lines

if _G.ChatState.active then
  _G.ChatState.buffer = _G.ChatState.buffer .. "a"
end
```

`scripts/OnKey/ChatSpace.lua` and `scripts/OnKey/ChatBackspace.lua` follow the same shape:

```lua
local KEYVAL = "space"

if _G.ChatState.active then
  _G.ChatState.buffer = _G.ChatState.buffer .. " "
end
```

```lua
local KEYVAL = "back"

if _G.ChatState.active then
  _G.ChatState.buffer = string.sub(_G.ChatState.buffer, 1, string.len(_G.ChatState.buffer) - 1)
end
```

**Known rough edge, not fixed here**: every one of these per-letter scripts fires on every press of that
key regardless of chat mode being the intended context — the `if _G.ChatState.active` guard stops them
from doing anything while chat is closed, but it does nothing to stop the *normal* gameplay action bound
to that same key (movement, aiming, whatever) from also firing at the same time while typing. A real
version of this would need a way to suppress normal input while chat mode is open — `Player.SetInputEnabled`
(confirmed real, [Player](../namespaces/player#input--control)) is the obvious candidate to try, but
disabling all input might also block the letter-key `OnKey` scripts themselves, which hasn't been checked.

## Send: reusing the networking deep dive's mechanism, carrying a string instead of a tag

Already shown above — `Net.SendCustomEvent("Alarm", 102, {Net.GetHostName(), sMessage}, true)`, event ID
`102` chosen to avoid colliding with `Alarm`'s own real IDs (`0`, `1`) and the ping-pong test's `100`/`101`.
The receiving side extends the exact same override from the networking deep dive with one more branch:

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

- **Nothing here has been live-tested**, input, send, or display.
- **Depends entirely on the networking deep dive's unconfirmed transport claim** — if `SendCustomEvent`
  doesn't actually cross the network symmetrically, this doesn't send anything either.
- **The per-letter `OnKey` approach doesn't suppress normal gameplay input** while typing — a real version
  needs that solved first, or every chat message doubles as an accidental input storm.
- **`LTIStartKeyboardInput`/`LTIEndKeyboardInput` were never tested** as a cleaner alternative to the
  one-script-per-character approach — if that native hook turns out to accept arbitrary text rather than
  being hardcoded to the profile-name field, most of the "Input" section above becomes unnecessary.
