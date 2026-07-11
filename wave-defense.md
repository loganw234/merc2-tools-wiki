---
title: WaveDefense
parent: Frameworks
nav_order: 4
---

# WaveDefense

> **Status: skeleton, in active development.** The file's own header calls this out directly: "SKELETON
> SCOPE: prep -> spawn a ring of enemies around the host -> poll until cleared -> next (bigger) wave ->
> fixed:win after N / endless:track best. Enough to prove the contract->engine->ModNet.Shared->HUD chain end
> to end in SP first." Its own TODO list — quoted in full [below](#status-skeleton-explicitly) — includes
> "co-op verify," so treat the single-player path as the tested one and co-op as designed-but-unconfirmed.

`WaveDefense.lua` isn't a fourth framework — it's the worked example of gluing the other three together into
a real gamemode: [Contract Framework](contract-framework/) as the launcher, [ModNet](modnet) for co-op sync
and authority, and [UI Kit](uilib/) for a fully custom HUD and setup menu. A wave-survival mode ("Hold out
where you stand against escalating enemy waves") where the contract's only job is to *start* the mode; from
there, `WaveDefense.lua`'s own engine and heartbeat run the whole thing.

It lives at the top level of the `lua-wave-defense` mod, not inside `scripts/OnLoad/` alongside the three
frameworks it depends on — its own deploy comment is explicit about why:

```lua
-- DEPLOY: OnLoad/WaveDefense.lua, AFTER uilib + ModNet + ContractFramework load.
```

and it guards the same way every consumer script in this wiki guards a missing dependency, just checking
three globals instead of one:

```lua
if not (_G.ModNet and _G.Contract and _G.UI) then
    if Loader and Loader.Printf then
        Loader.Printf("[WaveDef] need ModNet + ContractFramework + uilib loaded first (check [OnLoad] order)")
    end
    return
end
```

## The launcher pattern

The entire integration with [Contract Framework](contract-framework/) is one `Contract.Register` call at the
bottom of the file:

```lua
Contract.Register{
    id = "wavedef",
    title = "Wave Defense",
    desc = "Hold out where you stand against escalating enemy waves.",
    hideTracker = true,                                     -- our mode owns the screen: suppress the board tracker + objective tray
    onBegin = function(inst) W.inst = inst; W.openSetup() end,   -- capture inst (for win/fail completion) + open the config menu
    objectives = { Contract.Survive{ desc = "Survive the waves", time = 3600 } },  -- placeholder; engine drives real end
}
```

This is the exact pattern
[Contract.Register & Lifecycle](contract-framework/register-and-lifecycle#handing-off-to-a-bespoke-gamemode)
describes as the escape hatch for a bespoke gamemode:

- **`hideTracker = true`** suppresses both the native HUD objective-tray line and the
  [Contract Board](contract-framework/contract-board#the-tracker)'s own floating tracker panel, so nothing
  the framework or board draws competes with WaveDefense's own [UI Kit](uilib/) HUD.
- **`objectives = { Contract.Survive{ time = 3600 } }`** is a placeholder, not a real win condition — an hour
  is long enough that it never naturally completes in practice. It exists only so the contract has at least
  one objective (`Contract.Register` logs a warning otherwise) and so the framework's objective runner has
  something to run. The actual win/lose decision never goes through it.
- **`onBegin(inst)`** fires once, right after the framework has teleported the player (if `start` were set;
  WaveDefense doesn't use it) and wired up relations/support, but before the placeholder objective starts
  running. WaveDefense's handler just stashes `inst` for later and opens the setup menu — the real game
  hasn't started yet at this point, only configuration has.
- Ending the run bypasses the placeholder objective entirely: `endRun()` (below) calls
  `Contract._finish(W.inst or Contract.active, won)` **directly**, exactly the "call finish yourself,
  whenever your own logic decides the run is over" pattern the framework's `onBegin` doc describes.

So accepting "Wave Defense" on the [Contract Board](contract-framework/contract-board) (F5 by default) opens
straight into WaveDefense's own setup menu, not into a running mission — the contract is a thin shell that
hands control to `WaveDef` immediately and gets control back only at the very end, once, to report a win or
a loss.

## Authority model

Only one machine ever runs the simulation. `WaveDef.begin`, `WaveDef.stop`, `WaveDef.openSetup`, and the
engine tick all early-return unless [`ModNet.IsAuthority()`](modnet#identity--authority) is true — which
means single-player always, and only the host in co-op:

```lua
function W.begin(cfg)
    if not ModNet.IsAuthority() then return end
    ...
end
function W.stop()
    if not ModNet.IsAuthority() then return end
    ...
end
function W.openSetup()
    if not ModNet.IsAuthority() then return end                       -- host/SP only; the co-op partner just watches the HUD
    ...
end
```

The HUD update, by contrast, runs unconditionally on **both** machines every tick, and only ever reads from
the synced state table — never `Player`/`Object`/`Ai`/`Pg` directly:

```lua
local function loop(gen)
    if W.gen ~= gen then return end
    if ModNet.IsAuthority() then pcall(engineTick) end     -- host/SP drives the sim
    pcall(updateHud)                                       -- everyone draws from S
    Event.Create(Event.TimerRelative, { TICK }, function() loop(gen) end)
end
```

That split is the entire co-op design in one function: the authority computes the wave, the partner's screen
is a pure mirror of whatever the authority publishes. `W.gen`, incremented once per `OnLoad` re-run and
captured by each `loop` closure, is the same generation-guard idiom [UI Kit](uilib/) and
[ForgeMenu](deep-dives/forge-menu) use to stop a reload from stacking a second heartbeat alongside the first.

## Messages vs. shared state

WaveDefense uses both halves of [ModNet](modnet)'s API, for deliberately different reasons.

**[Synced state](modnet#1-synced-state-simplest)** (`ModNet.Shared("wd")`, held in the local `S`) carries
everything both machines should simply agree on — `wave`, `enemiesLeft`, `enemiesTotal`, `best`, `kills`,
`cash`, `state`, `cfg`. Last-writer-wins is fine here because only the authority ever writes it; the client
just reads. Writes go through a local guard against ModNet's broadcast-on-every-write behavior:

```lua
local S = ModNet.Shared("wd")                 -- host writes / both read (last-writer-wins)
-- ModNet broadcasts on EVERY write, so guard scalar writes on change (avoid flooding the wire).
local function put(k, v) if S[k] ~= v then S[k] = v end end
```

**A [message](modnet#2-messages)** (`ModNet.On("wd_reward", ...)` / `ModNet.Send("wd_reward", reward)`)
carries the per-wave cash payout instead, because paying out cash is a **local action**
(`MrxPmc.AddCashQty`) that has to actually run on each machine — if the reward were synced state instead,
the client would only see a number change in a shared table, and would never call `AddCashQty` itself:

```lua
ModNet.On("wd_reward", function(_, amount)
    if ModNet.IsAuthority() then return end
    safe(function() MrxPmc.AddCashQty(tonumber(amount) or 0) end)
end)
```

```lua
safe(function() MrxPmc.AddCashQty(reward) end)             -- pay the host player
if ModNet.IsCoop() then ModNet.Send("wd_reward", reward) end   -- pay the co-op partner too
```

The handler's own `IsAuthority()` check exists because the host already paid itself locally, inline, right
next to the `Send` call — without that check a host running its own message back through `ModNet.On` (if it
ever loops back) would double-pay itself.

## The cycler menu

The setup screen is one [`UI.Menu`](uilib/menu), built once at load time, with every config field rendered by
a small hand-rolled helper — the same "cycler" convenience the rest of [UI Kit](uilib/) doesn't provide as a
stock feature:

```lua
local function cyclerEntry(m, item)
    m:entry(
        function() return item.label .. ":  " .. tostring(W.cfg[item.key]) end,
        function(_)
            local cur, idx = W.cfg[item.key], 1
            for i, x in ipairs(item.values) do if x == cur then idx = i; break end end
            local nv = item.values[(idx % #item.values) + 1]           -- next value, wrapping
            W.cfg[item.key] = nv; W.saveVal(item.key, nv)              -- persist immediately
        end)
end
```

The label is a function (a live, dynamic label, the same technique [`UI.Menu`](uilib/menu) documents), so it
always shows the current value; picking the entry advances circularly through `item.values` and saves
immediately, rather than waiting for a separate confirm step. `UI.Menu`'s own choose handler re-paints the
current level after every action specifically so a dynamic label like this one updates the instant it's
picked — see [Building the tree](uilib/menu#building-the-tree) for the cursor-preserving re-paint that makes
that work without kicking the selection back to the top of the list.

The whole setup screen is generated from one schema table, `W.CONFIG` — mode, wave count (fixed mode), enemy
faction, wave-1 size, per-wave growth, arena radius, and prep time — plus a header and two extra entries
(`START WAVE DEFENSE`, which closes the menu and calls `W.begin(W.cfg)`; `Reset to defaults`).

It opens on a short delay after `onBegin` fires, specifically so the Contract Board finishes closing first
instead of fighting the new menu for input focus:

```lua
if Event and Event.Create then Event.Create(Event.TimerRelative, { 0.2 }, function() if W.menu then W.menu:open() end end)
```

## Config schema & persistence

Each `W.CONFIG` entry (`{ key, label, default, values }`) saves and loads through its own
`Loader.SaveVar("WaveDef_" .. key, ...)` / `LoadVar` call — the source comment notes this is because
"SaveVar has no tables," so there's no single blob to persist and each field is its own save slot instead:

```lua
function W.saveVal(key, v) Loader.SaveVar("WaveDef_" .. key, v) end
function W.loadCfg()
    local cfg = {}
    for _, c in ipairs(W.CONFIG) do local v = Loader.LoadVar("WaveDef_" .. c.key); cfg[c.key] = (v == nil) and c.default or v end
    return cfg
end
```

Endless mode's high score is a separate, single persisted value, independent of the per-field config keys —
`Loader.LoadVar("WaveDef_best")` / `SaveVar("WaveDef_best", n)` — so the best wave reached survives across
sessions and config changes alike.

## The wave loop

`spawnWave` reads the host's current position, computes `count = baseCount + (wave - 1) * perWave`, and
places that many enemies in a ring of `arenaRadius` around the host, cycling deterministically through
`TEMPLATES[faction]` (no RNG dependency — template assignment is just `(i - 1) % #tmpls`), each given a
best-effort initial `Attack` goal aimed at the host.

`engineTick` — which only ever runs on the authority, driven by the shared heartbeat — checks for a loss
first (host health `<= 0`), then branches on `run.state`: in `"prep"` it waits out `prepUntil` and spawns the
next wave; in `"active"` it polls `countAlive()` every tick, tallies kills from the alive-count delta, and
once the wave is cleared, pays out `1000 * waveKills + 5000` (both locally and via the `"wd_reward"` message
above) before either ending the run as a win (fixed mode, final wave cleared) or looping back to `"prep"`
(endless mode, or fixed mode with waves remaining).

`endRun(run, won)` sets a terminal state, publishes it once more, and calls `Contract._finish` directly —
then clears `W.run` a few seconds later on a one-shot timer, so the HUD lingers on victory/defeat briefly
before disappearing.

## Status: skeleton, explicitly

The file's own header lists what's still open, verbatim:

> TODO (later passes): tie win/lose back to the contract objective; real lose handling (respawn); faction
> relations for non-VZ; config UI; co-op verify.

Read literally: the placeholder `Contract.Survive` objective is never reconciled with the real outcome (a
cosmetic gap, since `endRun` finishes the contract directly regardless); a dead host currently just ends the
run rather than offering a respawn; only the `VZ` faction's relations are assumed correct out of the box;
the setup screen exists (the cycler menu above) even though the header predates it; and — as the status
banner at the top of this page repeats — co-op has not yet been verified live.

## Deploy

1. [`uilib.lua`](uilib/source), [`ModNet.lua`](modnet#the-full-script), and
   [`ContractFramework.lua`](contract-framework/source) must all load first — give `WaveDefense.lua` a
   higher `[OnLoad]` number than all three.
2. Copy `WaveDefense.lua` to `scripts/OnLoad/`.
3. Accept **Wave Defense** from the [Contract Board](contract-framework/contract-board) (`F5` by default) to
   open the setup menu, configure, and start.

## The full script

```lua
-- =====================================================================
-- WaveDefense.lua  (OnLoad)  --  wave-defense gamemode ENGINE (skeleton)
--
-- Combines: ContractFramework (launcher via def.onBegin) + ModNet (co-op sync,
-- host-authoritative) + uilib (live HUD). The contract is only the entry point:
-- accept "Wave Defense" on the F5 board -> its onBegin calls WaveDef.begin(cfg).
--
-- AUTHORITY MODEL: the wave sim runs on the AUTHORITY only (SP or the co-op host,
-- via ModNet.IsAuthority()). It writes live state into ModNet.Shared("wd"); the
-- HUD loop runs on BOTH machines and just reads that shared table, so the co-op
-- partner sees the same wave/enemy counts with no logic of their own.
--
-- SKELETON SCOPE: prep -> spawn a ring of enemies around the host -> poll until
-- cleared -> next (bigger) wave -> fixed:win after N / endless:track best. Enough
-- to prove the contract->engine->ModNet.Shared->HUD chain end to end in SP first.
-- TODO (later passes): tie win/lose back to the contract objective; real lose
-- handling (respawn); faction relations for non-VZ; config UI; co-op verify.
--
-- DEPLOY: OnLoad/WaveDefense.lua, AFTER uilib + ModNet + ContractFramework load.
-- =====================================================================

if not (_G.ModNet and _G.Contract and _G.UI) then
    if Loader and Loader.Printf then
        Loader.Printf("[WaveDef] need ModNet + ContractFramework + uilib loaded first (check [OnLoad] order)")
    end
    return
end

_G.WaveDef = _G.WaveDef or {}
local W = _G.WaveDef

local TICK = 0.5                              -- engine + HUD poll (Hz/2; plenty for waves)
local S = ModNet.Shared("wd")                 -- host writes / both read (last-writer-wins)

-- ModNet broadcasts on EVERY write, so guard scalar writes on change (avoid flooding the wire).
local function put(k, v) if S[k] ~= v then S[k] = v end end

-- ===== config (schema drives the setup UI + load/save; SaveVar keys are "WaveDef_<key>") =====
W.CONFIG = {
    { key = "mode",        label = "Mode",          default = "endless", values = { "endless", "fixed" } },
    { key = "waves",       label = "Waves (fixed)", default = 10,        values = { 5, 10, 15, 20, 30 } },
    { key = "faction",     label = "Enemy",         default = "VZ",      values = { "VZ", "GUERILLA", "CHINA", "ALLIED", "OC", "PIRATE" } },
    { key = "baseCount",   label = "Wave 1 size",   default = 4,         values = { 2, 4, 6, 8, 10 } },
    { key = "perWave",     label = "+ Per wave",    default = 2,         values = { 1, 2, 3, 4, 5 } },
    { key = "arenaRadius", label = "Arena radius",  default = 25,        values = { 15, 20, 25, 30, 40 } },
    { key = "prepTime",    label = "Prep time (s)", default = 5,         values = { 3, 5, 8, 10, 15 } },
}
function W.saveVal(key, v) Loader.SaveVar("WaveDef_" .. key, v) end     -- per-field (SaveVar has no tables)
function W.loadCfg()                                                     -- saved options, schema defaults fill any gaps
    local cfg = {}
    for _, c in ipairs(W.CONFIG) do local v = Loader.LoadVar("WaveDef_" .. c.key); cfg[c.key] = (v == nil) and c.default or v end
    return cfg
end
local function defaultCfg() return W.loadCfg() end                      -- "default" now honours the saved config

-- enemy templates per faction (skeleton: a few each; extend freely)
local TEMPLATES = {
    VZ       = { "VZ Soldier", "VZ Heavy (Light MG)", "VZ Elite" },
    GUERILLA = { "Guerilla Soldier", "Guerilla Heavy (RPG)", "Guerilla Elite Soldier" },
    CHINA    = { "Chinese Soldier", "Chinese Heavy (Light MG)", "Chinese Elite Soldier" },
    ALLIED   = { "Allied Soldier", "Allied Heavy (Light MG)", "Allied Airborne" },
    OC       = { "OC Soldier", "OC Heavy (Light MG)", "OC Elite" },
    PIRATE   = { "Pirate Thug", "Pirate Thug (RPG)", "Pirate Officer (RPG)" },
}

-- ===== helpers =====
local function safe(fn, ...) local ok, a, b, c = pcall(fn, ...); if ok then return a, b, c end end
local function rtime() return safe(Sys.RealTime) or 0 end
local function hostPose()
    local ch = Player.GetLocalCharacter(); if not ch then return nil end
    local x, y, z = safe(Object.GetPosition, ch); if not x then return nil, nil, nil, ch end
    return x, y, z, ch
end

-- ===== persistence (endless high score) =====
local function loadBest() return Loader.LoadVar("WaveDef_best") or 0 end
local function saveBest(n) Loader.SaveVar("WaveDef_best", n) end

-- ===== state -> shared (authority) =====
pcall(function() import("MrxPmc") end)   -- for MrxPmc.AddCashQty (cash rewards); usually already resident

-- CO-OP: the host broadcasts each wave's payout so the partner gets paid too. The host already paid
-- itself locally, so the authority ignores its own (possible) loopback; only the client applies it.
ModNet.On("wd_reward", function(_, amount)
    if ModNet.IsAuthority() then return end
    safe(function() MrxPmc.AddCashQty(tonumber(amount) or 0) end)
end)

local function publish(run)
    put("state", run.state)
    put("wave", run.wave)
    put("enemiesLeft", run.left or 0)
    put("enemiesTotal", run.total or 0)
    put("best", run.best or 0)
    put("kills", run.kills or 0)
    put("cash", run.cash or 0)
end

local function countAlive(run)
    local n = 0
    for _, g in ipairs(run.enemies or {}) do
        local hp = safe(Object.GetHealth, g)
        if hp and hp > 0 then n = n + 1 end
    end
    return n
end

local function spawnWave(run)
    local cx, cy, cz, hch = hostPose()
    if not cx then return end                 -- host not ready; stay in prep, retry next tick
    run.wave = run.wave + 1
    local cfg = run.cfg
    local count = (cfg.baseCount or 4) + (run.wave - 1) * (cfg.perWave or 2)
    local tmpls = TEMPLATES[cfg.faction] or TEMPLATES.VZ
    local r = cfg.arenaRadius or 25
    run.enemies = {}
    for i = 1, count do
        local ang = 2 * math.pi * (i / count)
        local x = cx + r * math.cos(ang)
        local z = cz + r * math.sin(ang)
        local tmpl = tmpls[1 + ((i - 1) % #tmpls)]        -- cycle templates (no RNG dependency)
        local u = safe(Pg.Spawn, tmpl, x, cy, z)
        if u then
            -- best-effort aggro toward the host (they'd likely engage anyway; refine later)
            if hch then safe(function() Ai.Goal({ AIGuid = u, Goal = "Attack", Target = hch, Priority = "HiPri", Force = true }) end) end
            run.enemies[#run.enemies + 1] = u
        end
    end
    run.total = #run.enemies
    run.left = run.total
    run.lastAlive = run.total      -- baseline for kill-delta tracking
    run.waveKills = 0
    run.state = "active"
    Loader.Printf("[WaveDef] wave " .. run.wave .. ": spawned " .. run.total .. " " .. tostring(cfg.faction))
end

-- end the run: terminal state -> publish -> complete/fail the CONTRACT (native fanfare + cleanup via the
-- inst onBegin handed us), then clear the HUD a few seconds later so a fresh accept starts clean.
local function endRun(run, won)
    run.state = won and "won" or "lost"
    publish(run)
    safe(function() Contract._finish(W.inst or Contract.active, won) end)
    W.inst = nil
    if Event and Event.Create then Event.Create(Event.TimerRelative, { 6 }, function() if W.run == run then W.stop() end end) end
end

local function engineTick()
    local run = W.run
    if not run or run.state == "won" or run.state == "lost" then return end

    -- lose: host down (skeleton = health<=0; respawn handling is a later pass)
    local _, _, _, hch = hostPose()
    if hch then local hp = safe(Object.GetHealth, hch); if hp and hp <= 0 then endRun(run, false); return end end

    local t = rtime()
    if run.state == "prep" then
        if t >= (run.prepUntil or 0) then spawnWave(run) end
    elseif run.state == "active" then
        local alive = countAlive(run)
        local died = (run.lastAlive or run.total) - alive              -- eliminations since last tick
        if died > 0 then run.kills = (run.kills or 0) + died; run.waveKills = (run.waveKills or 0) + died end
        run.lastAlive, run.left = alive, alive
        if alive <= 0 then                                             -- wave cleared
            local reward = 1000 * (run.waveKills or 0) + 5000          -- 1k per kill this wave + 5k per wave
            run.cash = (run.cash or 0) + reward
            safe(function() MrxPmc.AddCashQty(reward) end)             -- pay the host player
            if ModNet.IsCoop() then ModNet.Send("wd_reward", reward) end   -- pay the co-op partner too
            if run.cfg.mode == "fixed" and run.wave >= (run.cfg.waves or 0) then
                endRun(run, true); return                              -- final wave cleared -> WIN (contract complete)
            else
                if run.wave > (run.best or 0) then run.best = run.wave; saveBest(run.best) end
                run.state = "prep"; run.prepUntil = t + (run.cfg.prepTime or 5)
            end
        end
    end
    publish(run)
end

-- ===== HUD (BOTH machines) -- pure read of the synced state =====
local STATE_TXT = { prep = "Prepare...", active = "FIGHT!", won = "VICTORY", lost = "DEFEATED" }
local function updateHud()
    local state = S.state
    if not state then
        if W.panel then W.panel:hide() end
        if W.bar then W.bar:hide() end
        return
    end
    if not W.panel then W.panel = UI.Panel{ x = 8, y = 8, w = 210, title = "WAVE DEFENSE" } end
    if not W.bar   then W.bar   = UI.Bar{ x = 8, y = 130, w = 210, label = "" } end
    local wave, left, total = S.wave or 0, S.enemiesLeft or 0, S.enemiesTotal or 0
    local cfg = S.cfg or {}
    if cfg.mode == "fixed" then W.panel:line(0, "Wave " .. wave .. " / " .. (cfg.waves or "?"))
    else W.panel:line(0, "Wave " .. wave .. "     Best " .. (S.best or 0)) end
    W.panel:line(1, "Enemies " .. left .. " / " .. total)
    W.panel:line(2, "Kills " .. (S.kills or 0) .. "     $" .. UI.comma(S.cash or 0))
    W.panel:line(3, STATE_TXT[state] or tostring(state))
    W.panel:show()
    local frac = (total > 0) and ((total - left) / total) or 0
    W.bar:set(frac); W.bar:label("Cleared " .. math.floor(frac * 100) .. "%"); W.bar:show()
end

-- ===== lifecycle (authority sets up the run; client just displays synced state) =====
function W.begin(cfg)
    if not ModNet.IsAuthority() then return end
    cfg = cfg or defaultCfg()
    W.run = { cfg = cfg, wave = 0, state = "prep", enemies = {}, total = 0, left = 0,
              kills = 0, cash = 0, lastAlive = 0, waveKills = 0,
              best = loadBest(), prepUntil = rtime() + (cfg.prepTime or 5) }
    S.cfg = cfg                                            -- push the config table to the client (once)
    publish(W.run)
    Loader.Printf("[WaveDef] begin: " .. tostring(cfg.mode) .. ", faction " .. tostring(cfg.faction))
end
function W.stop()
    if not ModNet.IsAuthority() then return end
    W.run = nil
    put("state", nil)                                      -- hides the HUD on both machines
    Loader.Printf("[WaveDef] stop")
end

-- ===== heartbeat (runs continuously on BOTH machines; gen-guarded so a reload doesn't stack) =====
local function loop(gen)
    if W.gen ~= gen then return end
    if ModNet.IsAuthority() then pcall(engineTick) end     -- host/SP drives the sim
    pcall(updateHud)                                       -- everyone draws from S
    Event.Create(Event.TimerRelative, { TICK }, function() loop(gen) end)
end
W.gen = (W.gen or 0) + 1
do local g = W.gen; Event.Create(Event.TimerRelative, { TICK }, function() loop(g) end) end

-- ===== setup UI (built once; opened on accept for a seamless accept -> configure -> start flow) =====
-- a "cycler" entry: shows "Label: value", steps through item.values on pick, persists immediately.
-- reads/writes W.cfg by MODULE field so W.openSetup can refresh it from SaveVar before each open.
local function cyclerEntry(m, item)
    m:entry(
        function() return item.label .. ":  " .. tostring(W.cfg[item.key]) end,
        function(_)
            local cur, idx = W.cfg[item.key], 1
            for i, x in ipairs(item.values) do if x == cur then idx = i; break end end
            local nv = item.values[(idx % #item.values) + 1]           -- next value, wrapping
            W.cfg[item.key] = nv; W.saveVal(item.key, nv)              -- persist immediately
        end)
end
W.cfg = W.loadCfg()
W.menu = UI.Menu{ title = "WAVE DEFENSE SETUP" }
W.menu:header("OPTIONS")
for _, item in ipairs(W.CONFIG) do cyclerEntry(W.menu, item) end
W.menu:header("LAUNCH")
W.menu:entry("START WAVE DEFENSE", function(ctx) ctx:close(); W.begin(W.cfg) end)
W.menu:entry("Reset to defaults", function(ctx)
    for _, c in ipairs(W.CONFIG) do W.cfg[c.key] = c.default; W.saveVal(c.key, c.default) end
    ctx:hint("Reset to defaults")
end)
function W.openSetup()
    if not ModNet.IsAuthority() then return end                       -- host/SP only; the co-op partner just watches the HUD
    W.cfg = W.loadCfg()                                                -- refresh from SaveVar
    -- open on the next tick so the F5 contract board finishes closing first (avoids input contention)
    if Event and Event.Create then Event.Create(Event.TimerRelative, { 0.2 }, function() if W.menu then W.menu:open() end end)
    elseif W.menu then W.menu:open() end
end

-- ===== the contract = the launcher: accept -> open setup -> START -> engine (one seamless script) =====
Contract.Register{
    id = "wavedef",
    title = "Wave Defense",
    desc = "Hold out where you stand against escalating enemy waves.",
    hideTracker = true,                                     -- our mode owns the screen: suppress the board tracker + objective tray
    onBegin = function(inst) W.inst = inst; W.openSetup() end,   -- capture inst (for win/fail completion) + open the config menu
    objectives = { Contract.Survive{ desc = "Survive the waves", time = 3600 } },  -- placeholder; engine drives real end
}

Loader.Printf("[WaveDef] ready. Accept 'Wave Defense' on the F5 board -> configure -> START.")
```

## See also

- [Contract.Register & Lifecycle: Handing off to a bespoke gamemode](contract-framework/register-and-lifecycle#handing-off-to-a-bespoke-gamemode)
  — the `onBegin`/`hideTracker` escape hatch this whole mode is built on.
- [The Contract Board](contract-framework/contract-board) — the board WaveDefense's `hideTracker` opts out
  of, and the F5 key that launches it.
- [ModNet: Identity & authority](modnet#identity--authority) — `IsAuthority`/`IsCoop`/`IsHost`, and why
  `IsHost` alone would be wrong here.
- [UI.Menu](uilib/menu) — the dynamic-label re-paint mechanic the cycler menu depends on.
- [ContractFramework.lua](contract-framework/source) / [uilib.lua](uilib/source) — the complete source of
  the two frameworks this page cites throughout.
