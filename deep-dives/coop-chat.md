---
title: "A Basic Co-op Text Chat"
parent: Deep Dives
nav_order: 4
---

# Deep Dive: A Basic Co-op Text Chat

**Confirmed working end-to-end across two real players** — input, send, and display all fire correctly
together, including real cross-network delivery. One piece is still being tuned: raw chat text can't be
sent as a Lua string at all (see the [networking deep dive](networking#two-confirmed-constraints-on-custom-payloads)
for why), so the message has to be re-encoded as numbers on the way out and decoded back into text on the
way in. The current encoding works for short messages; the exact safe maximum length hasn't been pinned
down yet.

## The problem, broken into three pieces

1. **Input** — capturing what the player types.
2. **Send** — getting that text to the other player.
3. **Display** — showing it on their screen.

All three are solved and confirmed working together. Piece 2's mechanism is the same hijacked-
`NetEventCallback` pattern documented on the [networking deep dive](networking) — confirmed live in this
exact feature, which is also where the event-ID-masking and string-payload constraints described there were
actually discovered. Piece 3 has a real, working answer, detailed on its own page: [Building a Chat/Log
UI](coop-chat-ui). Piece 1 — capturing what's typed — turned out to have no answer anywhere in the *game's*
Lua surface at all: `LTIStartKeyboardInput`/`LTIEndKeyboardInput` (`resident/mrxguishell.lua`) is the one
native hook that smells like free-text entry, but it's wired to profile-name creation specifically, and
whether it accepts arbitrary text was never tested, because the real answer turned out to live one level
down, in **lua-bridge itself** (the injection tool this whole wiki is built around) — not the game.

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

## Send

Confirmed working live, in both directions, between two real players — but getting there took two fixes
past the first working draft:

- **Hijack target**: `Alarm` doesn't work — it's a per-object world script, not always-resident, so
  `import("Alarm")` throws unless the current level happens to have a real alarm object loaded.
  `MrxFactionManager` is always-resident and is the actual hijack target used.
- **The message can't be sent as a string.** The first live test sent `{Net.GetHostName(), sMessage}` and
  it arrived on the other machine as `userdata: 89C0BD32: userdata: 942328DD` — unreadable handles, not
  text. See [the networking deep dive](networking#two-confirmed-constraints-on-custom-payloads) for why:
  strings crossing `SendCustomEvent` become opaque hash handles, not their original content, and there's no
  way to recover arbitrary text from one. Only numbers survive intact, so the message is sent as an array
  of raw character codes (`string.byte`/`string.char`) instead of a string. Sender identity was dropped
  entirely rather than worked around — co-op is capped at 2 players, so whoever receives a message already
  knows who sent it.

```lua
import("MrxFactionManager")

local NETEVENT_CHAT = 5  -- below 8 per the ID-masking constraint; avoids MrxFactionManager's own 0/1/2

if not MrxFactionManager._bChatHijacked then
  MrxFactionManager._bChatHijacked = true
  local fOriginalCallback = MrxFactionManager.NetEventCallback

  MrxFactionManager.NetEventCallback = function(nEventType, tArgs)
    if nEventType == NETEVENT_CHAT then
      local tChars = {}
      for i, nByte in ipairs(tArgs) do
        tChars[i] = string.char(nByte)
      end
      CoopChatUI:AddMessage("Partner: " .. table.concat(tChars))
    else
      fOriginalCallback(nEventType, tArgs)
    end
  end
end

function SendChatMessage(sMessage)
  CoopChatUI:AddMessage("You: " .. sMessage)

  local tArgs = {}
  for i = 1, string.len(sMessage) do
    tArgs[i] = string.byte(sMessage, i)
  end

  Net.SendCustomEvent("MrxFactionManager", NETEVENT_CHAT, tArgs, true)
end
```

`SendChatMessage` also does the optimistic local echo — adding "You: ..." to your own chat window
immediately, rather than waiting on any loopback. That's deliberate, not a workaround: a peer never
receives its own broadcast back (confirmed — this is normal, not a bug), so without the local echo you'd
never see your own sent messages at all.

**Not yet nailed down**: the real safe maximum message length. One character per `tArgs` slot is simple and
confirmed working for short test messages, but the largest array size confirmed safe anywhere in the
decompiled corpus is 5 elements (see the [networking deep dive](networking#status-confirmed-vs-still-open)).
Whether that's a hard cap or coincidence — and whether longer messages need bit-packing multiple characters
per slot, or splitting across multiple sequential `SendCustomEvent` calls — is the next thing to test.

## Display: solved — see its own Deep Dive

Full writeup, including a real confirmed engine bug and the workaround for it, on
[Building a Chat/Log UI](coop-chat-ui). Short version: `MrxGuiTextBuffer` (the engine's own built-in
scrolling-message-log widget) has a genuine crash bug in its documented constructor, worked around by
calling a second, bug-free internal function directly. The result is `CoopChatUI`, a small reusable
module — `CoopChatUI:AddMessage(sText)` to push a line, `CoopChatUI:Toggle()` to show/hide,
`CoopChatUI:SetInputText(sText)` for a live-updating "what am I typing" preview — confirmed working both
standalone and as part of the full input→send→display pipeline described above.

## Known limitations of this whole page

- **Requires a lua-bridge build that includes the `Loader` input functions.** Real and implemented, but
  still not part of every lua-bridge install by default — see the
  [lua-bridge API section](../lua-bridge-api/) note on that.
- **Character set is limited to uppercase letters, digits, and space.** Input capture reads raw VK codes
  (see [lua-bridge API: Loader](../lua-bridge-api/loader)), which carry no Shift-state information — no
  lowercase, no punctuation. A real, current limitation, not yet addressed.
- **No sender identity is transmitted.** Messages are always labeled "Partner" on receipt, relying on the
  2-player cap. Would need rework (a numeric role tag, not a string — see Send above) to support more than
  2 players.
- **Safe maximum message length is unconfirmed.** See the Send section above — messages longer than
  whatever the real per-call limit turns out to be will need a different encoding or multiple chunked
  sends. Not yet tested.
- **`LTIStartKeyboardInput`/`LTIEndKeyboardInput` remains untested** as a possible game-native alternative —
  moot now that the lua-bridge-side input API is real, but worth remembering it exists.
