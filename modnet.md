---
title: ModNet
parent: Frameworks
nav_order: 3
---

# ModNet

> **Status: new, built on already-confirmed pieces.** The hijack target, event ID constraint, and
> 3-bytes-per-number wire packing are the exact mechanics [`coopchat.lua`](uilib/coopchat) already uses,
> which are themselves built on the confirmed [networking](deep-dives/networking) foundation. The
> generalizations specific to this library — channel multiplexing, value serialization, last-writer-wins
> state sync — haven't yet accumulated their own separate live-test history.

`ModNet.lua` (`_G.ModNet`) takes [`coopchat.lua`](uilib/coopchat)'s pack/chunk transport — built for exactly
one job, sending chat text — and generalizes it into a reusable co-op data-sync library: any number of
named channels, arbitrary Lua values (not just strings), and a synced-variable layer on top so a mod can
just write to a shared table instead of thinking about the network at all.
[`ModNet_CoopChat.lua`](uilib/coopchat-modnet) is chat, rebuilt on top of it — worth reading side by side
with the original to see exactly how much of `coopchat.lua` was really "the network problem" versus "the
chat problem."

## Three layers — use the highest one that fits

### 1. Synced state (simplest)

```lua
local S = ModNet.Shared("mymod")   -- a table whose fields auto-sync
S.score = 100                       -- write -> broadcast to the other player
print(S.score)                      -- read -> last known value, local or remote

ModNet.Set("k", v)   -- shortcut: same idea, default namespace
ModNet.Get("k")

ModNet.Track("hp", function() return myHp end)   -- push a LOCAL variable out whenever it changes
```

`Shared(ns)` returns a plain table with `__index`/`__newindex` metamethods wired to `ModNet.getv`/`setv` —
reading or writing a field *is* reading or writing synced state, with no explicit send/receive call
anywhere in your own code. `Track(key, getter)` is the other direction: a function you supply, polled once
per heartbeat, that gets pushed out automatically the moment its return value actually changes (diffed
against the last value seen — a getter that returns the same number every tick sends nothing).

### 2. Messages

```lua
ModNet.On("chat", function(sender, text) ... end)    -- sender = 0/1 player id
ModNet.Send("chat", "hello")                          -- any value: string/number/bool/table
```

Named, one-shot messages instead of persistent state — the closest analogue to `coopchat.lua`'s own
`SendChat`/receiver pair, except the payload can be **any serializable Lua value**, including a nested
table, not just a string.

### 3. Raw (experts)

```lua
ModNet.OnRaw("ch", function(sender, nums) ... end)
ModNet.SendRaw("ch", { 1, 2, 3 })
```

Bypasses serialization entirely — you hand over (and receive) plain number arrays yourself. This is
essentially `coopchat.lua`'s own approach, exposed directly for a caller who wants to hand-roll their own
encoding for some reason. **`Send`/`On` and `SendRaw`/`OnRaw` are separate pairs per channel** — the
receiving side has to register with the same one the sender used, since that's what determines whether the
incoming bytes get deserialized or handed back raw.

## How it works

### Same foundation as `coopchat.lua`, generalized to many channels at once

The hijack target (`MrxFactionManager`), the below-8 event ID (`M.EV = 5`), and the
3-bytes-per-number wire packing are unchanged from [`coopchat.lua`](uilib/coopchat) — see that page (and
the [networking deep dive](deep-dives/networking) underneath it) for why each of those specific choices is
correct. What's new is that a single event ID now carries **every** channel a mod registers, not just one
hardcoded chat message type. Two mechanisms make that possible:

- **Channel names hash to a 16-bit id** (`chash`, a simple rolling hash — `h = (h*33 + byte) % 65536`
  per character) that's identical on both machines for the same string, so `"chat"` and `"score"` never
  collide with each other on the wire without needing a manually-assigned numeric id per channel the way a
  single-purpose script would.
- **The reassembly key includes the channel**, not just sender and message id
  (`sender .. "/" .. ch .. "/" .. mid`, versus `coopchat.lua`'s plain `sender*256+msgId`) — necessary
  precisely because multiple channels' chunks can now be in flight at the same time and must not be
  reassembled into each other.

### Serialization: a small TLV encoding under the "Messages" layer

`Send`/`On` support arbitrary values by serializing to a byte string first, with one tag byte ahead of each
value: `0`=nil, `1`=false, `2`=true, `3`=number (a length byte, then the number as ASCII digits from
`tostring`), `4`=string (a 2-byte length, then the raw bytes), `5`=table (a 2-byte pair count, then each
key and value serialized recursively, key immediately followed by its value). This is deliberately simple,
not compact — a table serializes to noticeably more bytes than the equivalent hand-packed encoding would,
which is the tradeoff for not having to write a custom encoder per message type the way `coopchat.lua` had
to for plain text.

### Last-writer-wins keeps synced state convergent

Every `Shared`/`Set` write carries a per-key version counter (`ver`) and the writer's sender id. On
receipt:

```lua
if not e or ver > e.ver or (ver == e.ver and (src or -1) > (e.src or -1)) then
  st[key] = { v = value, ver = ver, src = src }
end
```

A strictly newer version always wins; a **tied** version (both players happened to write the same key at
the same local "tick") is broken by sender id, deterministically, so both machines land on the identical
final value even though they can't agree on true wall-clock ordering. This is why the library's own
constraints note host-authoritative or single-writer keys as the cleanest use — LWW guarantees convergence,
not that "the version you wanted" wins if two players write the same key at once.

### The heartbeat's three jobs

One `Event.TimerRelative` loop (`M.HB`, default 2s) handles everything time-based:

1. **Poll every `Track`ed getter** and broadcast whichever ones actually changed since last check.
2. **Every 5th beat, re-broadcast all synced state** — cheap duplicate sends the receiver's LWW check just
   ignores if nothing's actually new, but the mechanism a **late-joining player** needs to ever learn state
   that was set before they connected (nothing else pushes existing state to a new arrival).
3. **Garbage-collect reassembly buffers older than 10 seconds** — a message that never fully arrives
   (a dropped chunk) would otherwise leak its partial-reassembly entry forever.

## Config

| Field | Default | What |
|---|---|---|
| `M.EV` | `5` | The shared `SendCustomEvent` id every ModNet channel multiplexes over. Below 8, per the [networking deep dive](deep-dives/networking#a-concrete-test-ping-pong-via-a-hijacked-neteventcallback)'s event-ID-masking constraint. |
| `M.SLOTS` | `5` | `tArgs` per send (2 are header — message id/sequence/total packed into one number, plus sender+channel packed into another); the rest carry payload. Matches the largest array size confirmed safe anywhere in the decompiled corpus. |
| `M.HB` | `2.0` | Heartbeat interval, seconds. |

## Constraints

- **Numbers are 24-bit-safe** (`byte1*65536 + byte2*256 + byte3`), same ceiling as `coopchat.lua`'s own
  encoding.
- **A small-payload control plane, not a file transfer** — sync *state*, not large blobs; every send still
  costs one or more real `SendCustomEvent` calls.
- **Host-authoritative or single-writer keys are cleanest.** LWW resolves conflicting writes
  deterministically, but "deterministic" isn't the same as "the outcome either player actually intended" —
  design keys so only one side is expected to write a given one where that matters.

## The full script

```lua
-- ModNet.lua -- co-op data-sync library over Net.SendCustomEvent -------------
-- One reliable, chunked, arbitrary-data channel between the two co-op clients,
-- with a simple "synced variable" layer on top. Deploy as OnLoad/ModNet.lua on
-- BOTH machines (load it before any consumer). Numbers cross the wire intact;
-- strings/tables are serialized to bytes here, so callers just pass Lua values.
--
-- LAYERS (use the highest one that fits):
--   1. Synced state (simplest):
--        local S = ModNet.Shared("mymod")   -- a table whose fields auto-sync (LWW)
--        S.score = 100                       -- write -> broadcast; read S.score anywhere
--        ModNet.Set("k", v) / ModNet.Get("k")            -- default namespace shortcuts
--        ModNet.Track("hp", function() return myHp end)  -- push a local var out on a heartbeat
--   2. Messages:
--        ModNet.On("chat", function(sender, text) ... end)    -- sender = 0/1 player id
--        ModNet.Send("chat", "hello")                          -- any value: str/num/bool/table
--   3. Raw (experts): ModNet.OnRaw("ch", fn) / ModNet.SendRaw("ch", {numbers})
-- Pair Send<->On and SendRaw<->OnRaw per channel (the receiver interprets by how it registered).
-- Constraints: numbers are 24-bit-safe; it's a small-payload control plane (sync STATE, not files);
-- host-authoritative or single-writer keys are cleanest (writes converge last-writer-wins).
----------------------------------------------------------------------------

_G.ModNet = _G.ModNet or {}
local M = _G.ModNet
M.VERSION = "1.0"

-- ===== config (experts may tune before/after load) =====
M.EV    = M.EV    or 5     -- SendCustomEvent id (<8); all ModNet traffic shares it, namespaced by channel
M.SLOTS = M.SLOTS or 5     -- tArgs per send (2 are header); bump toward the coopchat_test CAP result
M.HB    = M.HB    or 2.0   -- heartbeat seconds (Track polling + late-join reconcile)

-- ===== persistent state (survives a reload) =====
M._chan  = M._chan  or {}  -- chash -> { fn, raw, name }
M._rx    = M._rx    or {}  -- reassembly buffers
M._store = M._store or {}  -- _store[ns][key] = { v, ver, src }
M._watch = M._watch or {}  -- { ns, key, get, last }

local function try(f, ...) if type(f) == "function" then local ok, v = pcall(f, ...); if ok then return v end end end
local function now() return try(Sys and Sys.RealTime) or 0 end
local function localId()
  return try(Player and Player.GetLocalPlayerId) or try(Player and Player.GetLocalId)
      or ((Net and Net.IsServer and Net.IsServer()) and 0 or 1)
end
local function chash(name)   -- name -> 16-bit id, identical on both machines
  local h = 0
  for i = 1, #name do h = (h * 33 + string.byte(name, i)) % 65536 end
  return h
end

-- ---- serialize a Lua value <-> byte string (number/string/bool/nil/nested table) ----
local function u16(n) return string.char(math.floor(n/256) % 256, n % 256) end
local function serInto(v, out)
  local t = type(v)
  if v == nil then out[#out+1] = "\000"
  elseif t == "boolean" then out[#out+1] = v and "\002" or "\001"
  elseif t == "number" then local s = tostring(v); out[#out+1] = "\003" .. string.char(#s) .. s
  elseif t == "string" then out[#out+1] = "\004" .. u16(#v) .. v
  elseif t == "table" then
    local n = 0; for _ in pairs(v) do n = n + 1 end
    out[#out+1] = "\005" .. u16(n)
    for k, val in pairs(v) do serInto(k, out); serInto(val, out) end
  else out[#out+1] = "\000" end   -- functions/userdata -> nil
end
local function serialize(v) local o = {}; serInto(v, o); return table.concat(o) end
local function deser(s, i)
  local tag = string.byte(s, i); i = i + 1
  if tag == 0 then return nil, i
  elseif tag == 1 then return false, i
  elseif tag == 2 then return true, i
  elseif tag == 3 then local ln = string.byte(s, i); i = i + 1; return tonumber(string.sub(s, i, i + ln - 1)), i + ln
  elseif tag == 4 then local ln = string.byte(s, i) * 256 + string.byte(s, i + 1); i = i + 2; return string.sub(s, i, i + ln - 1), i + ln
  elseif tag == 5 then
    local n = string.byte(s, i) * 256 + string.byte(s, i + 1); i = i + 2; local tb = {}
    for _ = 1, n do local k; k, i = deser(s, i); local val; val, i = deser(s, i); tb[k] = val end
    return tb, i
  end
  return nil, i + 1
end
local function unserialize(s) local ok, v = pcall(deser, s, 1); if ok then return v end end

-- ---- bytes <-> numbers (3 bytes/number; faithful, incl. NULs -- TLV self-delimits any trailing pad) ----
local function bytesToNums(s)
  local n = {}
  for i = 1, #s, 3 do n[#n+1] = (string.byte(s,i) or 0)*65536 + (string.byte(s,i+1) or 0)*256 + (string.byte(s,i+2) or 0) end
  return n
end
local function numsToBytes(nums)
  local t = {}
  for _, x in ipairs(nums) do t[#t+1] = string.char(math.floor(x/65536)%256, math.floor(x/256)%256, x%256) end
  return table.concat(t)
end

-- ===== wire: chunked send + reassembly =====
local function wireSend(ch, nums, reliable)
  if not (Net and Net.SendCustomEvent) then return end
  local PAY = M.SLOTS - 2; if PAY < 1 then PAY = 1 end
  local total = math.max(1, math.ceil(#nums / PAY))
  M._mid = ((M._mid or 0) + 1) % 255
  local me = localId()
  for c = 0, total - 1 do
    local a = { M._mid * 65536 + c * 256 + total, me * 65536 + ch }   -- slot1=header, slot2=sender+channel
    for p = 1, PAY do local v = nums[c * PAY + p]; if v ~= nil then a[#a+1] = v end end
    Net.SendCustomEvent("MrxFactionManager", M.EV, a, reliable ~= false)
  end
end
local function dispatch(ch, sender, nums)
  local c = M._chan[ch]; if not c then return end
  if c.raw then pcall(c.fn, sender, nums)
  else pcall(c.fn, sender, unserialize(numsToBytes(nums))) end
end
local function wireRecv(tArgs)
  local h  = tArgs[1] or 0
  local mid = math.floor(h/65536) % 256; local seq = math.floor(h/256) % 256; local total = h % 256
  local s2 = tArgs[2] or 0
  local sender = math.floor(s2/65536) % 256; local ch = s2 % 65536
  local nums = {}; local i = 3; while tArgs[i] ~= nil do nums[#nums+1] = tArgs[i]; i = i + 1 end
  local key = sender .. "/" .. ch .. "/" .. mid
  local m = M._rx[key]; if not m then m = { total = total, parts = {}, t = now() }; M._rx[key] = m end
  m.parts[seq] = nums; m.t = now()
  local have = 0; for _ in pairs(m.parts) do have = have + 1 end
  if have >= m.total then
    M._rx[key] = nil
    local all = {}
    for c2 = 0, m.total - 1 do local pr = m.parts[c2]; if pr then for _, v in ipairs(pr) do all[#all+1] = v end end end
    dispatch(ch, sender, all)
  end
end
M._recv = wireRecv   -- routed through M so a reload picks up edits

-- ===== public: messages + raw =====
function M.On(name, fn)    M._chan[chash(name)] = { fn = fn, raw = false, name = name } end
function M.OnRaw(name, fn) M._chan[chash(name)] = { fn = fn, raw = true,  name = name } end
function M.Send(name, value, reliable)   wireSend(chash(name), bytesToNums(serialize(value)), reliable) end
function M.SendRaw(name, nums, reliable) wireSend(chash(name), nums, reliable) end

-- ===== public: synced state (last-writer-wins) + tracked locals =====
local STATE = "ModNet$state"
local function broadcastKey(ns, key)
  local e = M._store[ns] and M._store[ns][key]; if not e then return end
  M.Send(STATE, { ns, key, e.ver, e.src, e.v }, true)
end
function M.setv(ns, key, value)
  local st = M._store[ns]; if not st then st = {}; M._store[ns] = st end
  local e = st[key]; local ver = (e and e.ver or 0) + 1
  st[key] = { v = value, ver = ver, src = localId() }
  broadcastKey(ns, key)
end
function M.getv(ns, key) local st = M._store[ns]; local e = st and st[key]; if e then return e.v end end
function M.Shared(ns)
  return setmetatable({}, {
    __index    = function(_, k) return M.getv(ns, k) end,
    __newindex = function(_, k, v) M.setv(ns, k, v) end,
  })
end
function M.Set(key, value) M.setv("_", key, value) end
function M.Get(key)        return M.getv("_", key) end
function M.Track(key, getter, ns)   -- idempotent: safe to call again on a reload
  ns = ns or "_"
  for _, w in ipairs(M._watch) do if w.ns == ns and w.key == key then w.get = getter; return end end
  M._watch[#M._watch+1] = { ns = ns, key = key, get = getter, last = nil }
end

-- state channel receiver: apply last-writer-wins (ver, then higher sender id breaks ties -> converges)
if not M._stateOn then
  M._stateOn = true
  M.On(STATE, function(_, msg)
    if type(msg) ~= "table" then return end
    local ns, key, ver, src, value = msg[1], msg[2], msg[3], msg[4], msg[5]
    if ns == nil or key == nil then return end
    local st = M._store[ns]; if not st then st = {}; M._store[ns] = st end
    local e = st[key]
    if not e or ver > e.ver or (ver == e.ver and (src or -1) > (e.src or -1)) then
      st[key] = { v = value, ver = ver, src = src }
    end
  end)
end

-- ===== heartbeat: poll tracked locals; periodically re-broadcast state for late joiners =====
local function heartbeat()
  if Net and Net.IsMultiplayer and Net.IsMultiplayer() then
    for _, w in ipairs(M._watch) do
      local ok, v = pcall(w.get)
      if ok and v ~= w.last then w.last = v; M.setv(w.ns, w.key, v) end
    end
    M._hbN = (M._hbN or 0) + 1
    if M._hbN % 5 == 0 then   -- every ~5 beats: full reconcile (cheap dupes; receiver's LWW ignores them)
      for ns, st in pairs(M._store) do for key in pairs(st) do broadcastKey(ns, key) end end
    end
    local t = now(); for k, m in pairs(M._rx) do if t - (m.t or 0) > 10 then M._rx[k] = nil end end
  end
  if Event and Event.Create then Event.Create(Event.TimerRelative, { M.HB }, M._hb) end
end
M._hb = heartbeat

-- ===== install once =====
import("MrxFactionManager")   -- always-resident hijack target
if not M._hijacked then
  M._hijacked = true
  local orig = MrxFactionManager.NetEventCallback
  MrxFactionManager.NetEventCallback = function(evt, tArgs)
    if evt == M.EV then M._recv(tArgs) elseif orig then orig(evt, tArgs) end
  end
  Loader.Printf("[ModNet] receiver installed on MrxFactionManager")
end
if not M._hbStarted then
  M._hbStarted = true
  if Event and Event.Create then Event.Create(Event.TimerRelative, { M.HB }, M._hb) end
end

Loader.Printf("[ModNet] v" .. M.VERSION .. " ready (EV=" .. M.EV .. " SLOTS=" .. M.SLOTS .. " HB=" .. M.HB .. ")")
return "ModNet v" .. M.VERSION
```

## See also

- [`coopchat.lua`](uilib/coopchat) — the hand-rolled, single-purpose transport this library generalizes;
  read this one first for how the underlying wire mechanics were originally worked out.
- [`ModNet_CoopChat.lua`](uilib/coopchat-modnet) — the same chat feature, rebuilt on top of ModNet — compare
  the two directly to see what the library actually absorbs.
- [Custom Networked Events](deep-dives/networking) — the `NetEventCallback` hijack mechanism, the event-ID
  masking constraint, and the full `NETEVENT_*` catalog this and every other custom-networking page here
  builds on.
- [A Basic Co-op Text Chat](deep-dives/coop-chat) — the original discovery story.
