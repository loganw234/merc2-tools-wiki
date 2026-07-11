---
title: "coopchat.lua"
parent: UI Kit Scripts
nav_order: 1
---

# coopchat.lua

> **Status: new, built on already-confirmed pieces.** Every individual mechanism here — the
> hijacked-`NetEventCallback` pattern, the below-8 event ID constraint, `UI.Chat`'s Shift-aware typing — is
> independently confirmed elsewhere on this wiki (see the citations throughout below). This specific
> combined script hasn't yet accumulated its own separate live-test history.

The current, improved implementation of **[A Basic Co-op Text Chat](../deep-dives/coop-chat)** — see that
deep dive's [Update section](../deep-dives/coop-chat#update-a-ui-kit-rewrite-closes-the-open-limitations)
for exactly how this replaces the original approach and which of its limitations this closes.

## What it does

A co-op text chat window bound to a toggle key (`F2` by default): press it to open a typed-input line on a
[`UI.Chat`](chat-and-board) window, type a message, Enter sends it to the other player over the network,
Esc cancels. Received messages appear in the same scrolling log, titled by sender (`P1`/`P2`).

## Setup

1. [`uilib.lua`](../uilib/) loaded first, on **both machines** (`OnLoad`).
2. Copy this file to `scripts/OnKey/coopchat.lua` on both machines, and add `coopchat.lua=f2` under
   `[OnKey]`.
3. Press **F2** to open the input line. Type, **Enter** sends, **Esc** cancels.

`local KEYVAL = "f2"` is deliberately the very first line — the loader only picks up a script's default
hotkey by reading its first 10 lines, so a `KEYVAL` declaration sitting any later than that (as in an
earlier draft of this file, past a long header comment) is silently never found, and the key falls back to
needing an explicit `lua_loader.ini` entry instead of just working out of the box.

## How the pieces fit

- **Front end**: one [`UI.Chat`](chat-and-board) window supplies the entire display + typed-input side —
  scrolling log, Shift-aware character input, focus handling. Nothing here reimplements any of that.
- **Transport**: `Net.SendCustomEvent("MrxFactionManager", EV_CHAT, ...)` — the identical
  hijacked-`NetEventCallback` mechanism, always-resident target, and below-8 event ID constraint the
  [networking deep dive](../deep-dives/networking) and the original
  [coop-chat deep dive](../deep-dives/coop-chat) both establish. `EV_CHAT = 5`, chosen (per the source
  comment) to avoid `MrxFactionManager`'s own real event IDs (`0`/`1`/`2`).
- **Encoding**: `Net.SendCustomEvent` can't carry a raw string — only numbers survive the trip intact (see
  [coop-chat's Send section](../deep-dives/coop-chat#send) for why). `packBytes`/`unpackBytes` pack **3
  characters per numeric argument** (24-bit-safe: `byte1*65536 + byte2*256 + byte3`), instead of the
  original approach's one character per argument slot.
- **Chunking**: `SLOTS = 5` (matching the largest array size confirmed safe anywhere in the decompiled
  corpus), of which the first two are a packed header (message id + chunk sequence + chunk total, all
  three packed into *one* number the same way `packBytes` packs characters) and a sender id, leaving 3
  payload slots — 9 characters — per call. A message longer than that is split across multiple sequential
  `SendCustomEvent` calls and reassembled on the receiving end keyed by `sender*256 + msgId`, so out-of-order
  or partially-arrived chunks resolve correctly once every piece has shown up.
- **Sender identity**: `localId()` tries `Player.GetLocalPlayerId`, then `Player.GetLocalId`, then falls
  back to a `Net.IsServer()` guess (server = 0, client = 1) if neither exists — sent in slot 2, decoded to
  `"P1"`/`"P2"` on receipt.
- **Movement freeze**: `Player.SetInputEnabled` — the same native control gate the briefing/state-machine
  code uses — wraps `UI.Chat`'s `prompt()`/`_endInput()`, so the player can't move or fire while composing a
  message. Confirmed (per the source comment) not to block lua-bridge's own key capture, which sits below
  the game's own input-enabled flag entirely.
- **Local echo retitling**: `UI.Chat:push()` already shows what you type as a bare line the moment you
  submit it (via the input prompt's own echo); `onSubmit` removes that bare line and re-pushes it prefixed
  with your own `"P<id>:"` label, so your own sent messages look consistent with received ones instead of
  the only unlabeled line in the log.

## The full script

```lua
local KEYVAL = "f2"   -- must be in the first 10 lines (toggle key; add "coopchat.lua=f2" under [OnKey])

-- coopchat.lua --------------------------------------------------------------
-- Co-op text chat: a UI.Chat window (uilib) + the pack/chunk encoding that
-- carries arbitrary text over Net.SendCustomEvent (past the string->hash wall).
--
-- UI.Chat supplies the whole front end (scrolling log + Shift-aware typed input);
-- we supply encode/decode, P1/P2 sender titling, and a movement freeze while
-- typing (Player.SetInputEnabled -- the game's own control gate, same call the
-- briefing/state code uses; it does NOT block the lua-bridge key capture).
--
-- DEPLOY (both machines): uilib.lua loaded first (OnLoad). Then copy this to
-- <game>\scripts\OnKey\coopchat.lua and add  coopchat.lua=f2  under [OnKey].
-- Press F2 to open the input line; type, Enter sends, Esc cancels.
----------------------------------------------------------------------------

if not (_G.UI and UI.Chat) then
  if Loader and Loader.Printf then Loader.Printf("[coopchat] load uilib.lua first (press its key)") end
  return
end
import("MrxFactionManager")   -- always-resident hijack target

-- ===== wire constants (bump SLOTS to just under the coopchat_test CAP result) =====
local EV_CHAT       = 5     -- <8 event-id; avoids MrxFactionManager's own 0/1/2
local BYTES_PER_NUM = 3     -- 24-bit float-safe
local SLOTS         = 5     -- slot1=header, slot2=senderId, rest=payload
local PAY_SLOTS     = SLOTS - 2
local CHARS_PER_SEND = PAY_SLOTS * BYTES_PER_NUM

local function try(f, ...) if type(f) == "function" then local ok, v = pcall(f, ...); if ok then return v end end end
local function packBytes(s, i)
  return (string.byte(s, i)   or 0) * 65536
       + (string.byte(s, i+1) or 0) * 256
       + (string.byte(s, i+2) or 0)
end
local function unpackBytes(n, out)
  local b1 = math.floor(n/65536) % 256
  local b2 = math.floor(n/256)   % 256
  local b3 = n % 256
  if b1 > 0 then out[#out+1] = string.char(b1) end
  if b2 > 0 then out[#out+1] = string.char(b2) end
  if b3 > 0 then out[#out+1] = string.char(b3) end
end
local function localId()
  return try(Player and Player.GetLocalPlayerId)
      or try(Player and Player.GetLocalId)
      or ((Net and Net.IsServer and Net.IsServer()) and 0 or 1)
end
local function label(id) return "P" .. (tonumber(id or 0) + 1) end   -- id 0/1 -> P1/P2

-- freeze/unfreeze the local player's movement (game control gate; leaves chat input intact)
local function setMove(on)
  local p = try(Player and Player.GetLocalPlayer)
  if p and Player.SetInputEnabled then pcall(Player.SetInputEnabled, p, on) end
end

local function nextMsgId() _G.__cc_mid = ((_G.__cc_mid or 0) + 1) % 255; return _G.__cc_mid end

local function SendChat(text)
  if not (Net and Net.SendCustomEvent) then return end
  local me    = localId()
  local total = math.max(1, math.ceil(string.len(text) / CHARS_PER_SEND))
  local mid   = nextMsgId()
  for c = 0, total - 1 do
    local a = { mid * 65536 + c * 256 + total, me }
    local base = c * CHARS_PER_SEND
    for p = 0, PAY_SLOTS - 1 do
      local bi = base + p * BYTES_PER_NUM + 1
      if bi <= string.len(text) then a[#a + 1] = packBytes(text, bi) end
    end
    Net.SendCustomEvent("MrxFactionManager", EV_CHAT, a, true)
  end
end

-- onSubmit: send, then retitle prompt's bare local echo to "P<me>: text"
local function onSubmit(text)
  SendChat(text)
  if _G.COOPCHAT and _G.COOPCHAT.ui then
    local ui = _G.COOPCHAT.ui
    local wrap = UI.wrap and UI.wrap(text, 52)
    if type(wrap) == "table" and ui._log then
      for _ = 1, #wrap do table.remove(ui._log) end   -- drop the bare lines prompt just pushed
      ui:push(label(localId()) .. ": " .. text)        -- re-push titled
    end
  end
end

-- ===== build once: the UI.Chat window + the receiver hijack + movement wraps =====
if not _G.COOPCHAT then
  _G.COOPCHAT = {}
  local C = _G.COOPCHAT
  C.ui = UI.Chat{ x = 20, y = 330, w = 384, title = "CO-OP CHAT", onSubmit = onSubmit }

  -- wrap prompt()/_endInput() to freeze movement only while the input line is open
  local basePrompt, baseEnd = C.ui.prompt, C.ui._endInput
  C.ui.prompt   = function(self, cb) setMove(false); return basePrompt(self, cb) end
  C.ui._endInput = function(self)     setMove(true);  return baseEnd(self)      end

  -- receiver: decode + reassemble chunks, then push the titled line
  local orig = MrxFactionManager.NetEventCallback
  local rx = {}   -- rx[sender*256+msgId] = { total=, parts={[seq]=str} }
  MrxFactionManager.NetEventCallback = function(evt, tArgs)
    if evt == EV_CHAT then
      local h      = tArgs[1] or 0
      local msgId  = math.floor(h/65536) % 256
      local seq    = math.floor(h/256)   % 256
      local total  = h % 256
      local sender = tArgs[2] or 0
      local buf = {}; local i = 3; while tArgs[i] ~= nil do unpackBytes(tArgs[i], buf); i = i + 1 end
      local key = sender * 256 + msgId
      local m = rx[key]; if not m then m = { total = total, parts = {} }; rx[key] = m end
      m.parts[seq] = table.concat(buf)
      local have = 0; for _ in pairs(m.parts) do have = have + 1 end
      if have >= m.total then
        local o = {}; for cc = 0, m.total - 1 do o[#o + 1] = m.parts[cc] or "" end
        rx[key] = nil
        C.ui:push(label(sender) .. ": " .. table.concat(o))
      end
    elseif orig then
      orig(evt, tArgs)
    end
  end

  C.ui:push("[co-op chat ready -- press " .. KEYVAL .. " to type]")
  Loader.Printf("[coopchat] built (UI.Chat + receiver + movement freeze)")
end

-- ===== each keypress: (re)bind send so file edits apply, then open the input line =====
_G.COOPCHAT.ui:prompt(onSubmit)
```

## See also

- [A Basic Co-op Text Chat](../deep-dives/coop-chat) — the original discovery story (why input needed
  lua-bridge, the hijack-target dead end, the string-argument wall) this script's answer builds on.
- [Custom Networked Events](../deep-dives/networking) — the full `NetEventCallback` mechanism, the event-ID
  masking constraint, and the catalog of every `NETEVENT_*` constant already in use.
- [UI.Chat / UI.Board](chat-and-board) — the front-end widget this script is built on.
