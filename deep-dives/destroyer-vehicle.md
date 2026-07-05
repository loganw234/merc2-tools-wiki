---
title: "Making the Destroyer Driveable"
parent: Deep Dives
nav_order: 8
---

# Deep Dive: Making the Destroyer Driveable

> **Status: partially working.** Spawning either destroyer variant and boarding as driver or gunner —
> for both the local player and a coop partner — is confirmed working end to end. Two things aren't:
> physics (the ship doesn't float or move like a real boat) and the camera (badly broken while driving or
> gunning). The seat-naming mystery that looked like it might unlock full multi-gun-turret access turned
> out to be a red herring. This page is the full record of what was tried, what's confirmed, and what's
> very likely a hard wall rather than a bug still waiting to be found — see the [current script](#the-
> current-script) for what's actually deployed, and the [basic version](../sample-scripts-onkey)
> on the OnKey sample scripts page for a simpler, non-diagnostic starting point.

## The goal

A community member's mod request: the "Chinese Destroyer"/"Allied Destroyer" ships — normally just static
set-dressing in Lake Maracaibo, never driveable in the base game (see the
[MrxLayerManager](../resident/mrxlayermanager) world-state layer catalog and the
[World Inspector deep dive](world-inspector) for how this was originally discovered) — turned into a
real, spawnable, driveable vehicle for both players in co-op.

## What's confirmed working

`Pg.Spawn("Chinese Destroyer", ...)` / `Pg.Spawn("Allied Destroyer", ...)` both spawn a real, enterable
vehicle instance. `MrxUtil.EnterBestAvailableSeat` — the same real, already-existing engine utility every
other vehicle-boarding script on this wiki uses, checking `"d"`/`"g"`/`"p"`/`"c"` seat-type codes in that
order — puts the local player into the driver's seat on both variants directly, no workaround needed. A
second, explicit check that skips `"d"` (see [below](#the-seat-naming-red-herring)) reliably gets a coop
partner into a gunner seat. Exit works normally via `Vehicle.Exit`.

## The seat-naming red herring

The [Hash Lookup](../hash-lookup) page's "destroyer" filter surfaces entries like `Vehicle Seat
(Destroyer) (cannon)`, `(ciwsFL)`, `(ciwsFM)`, `(ciwsFR)`, `(ciwsRL)`, `(ciwsRR)`, `(sam)`, `(samFM)`,
`(samRR)`, and `Vehicle Seat (CH Destroyer) (Driver)` — nine gunner-type positions plus a driver seat,
which looked at first like it might mean the ship has 10 individually enterable seats, each needing its
own access path.

It doesn't, in the sense that matters for a player. Reading `resident/mrxutil.lua:381-412` directly
confirmed `EnterBestAvailableSeat` only ever checks the four generic type codes and returns the *first*
match per type — meaning even if all nine gunner-type positions genuinely exist as `"g"`-typed seats, this
function (and every other vehicle-boarding script in the game) can only ever reach one of them. That's
consistent with what a live test found: the "auto grabber" reliably found exactly two working seats
(driver and one gunner), no more.

A full seat-discovery pass was built to find the rest anyway. `Object.GetAttachedObjects(uBoat)` returns
this ship's ~32 attached objects — mostly structural/decorative, not seats — filtered against the known
seat-name hashes (each position's own `Object.GetLocalizedName` hash, matched against the exact hashes
pulled from the Hash Lookup page). This *did* find guids resolving to the named positions. But actually
entering one via `Vehicle.EnterBySeatGuid`/`Vehicle.TransferToSeat` teleported the player to a broken,
floating position above the ship — not a real, usable seat. This was scrapped rather than pursued
further: whatever's wrong with those specific attachments, it's a "why don't these behave like real
seats" problem, not a "how do we find them" problem, and finding them was the easy part.

One other theory tested and ruled out along the way: that the extra gun positions might be separate,
individually-spawnable sub-vehicles (like `"Mounted Destroyer Cannon"`, another set of Hash Lookup
entries) glued onto the hull via `Object.Attach`. A dedicated research pass found **zero** confirmed call
sites anywhere in the ~230 decompiled files that attach a weapon or turret to a vehicle via that function
— every real `Object.Attach` call site attaches a VFX ribbon, a linked prop, a human actor, or a camera,
and nothing anywhere ever spawns a template named `"Mounted..."`/`"Turret..."`/`"Cannon..."`. Those
positions are almost certainly compiled directly into the vehicle's own template, the same way `"Amx30
(Full)"`/`"M113 (VZ) (Full)"` bundle their own turrets elsewhere in this game.

## Physics: confirmed not fixable from Lua

The base game's destroyer never moves — it's static set-dressing, so the working theory was that its
compiled template simply ships with physics disabled by default, and that a script could turn it back on.
`Object.EnablePhysics(uGuid)` is real and confirmed always-paired with `DisablePhysics` elsewhere in this
corpus (`resident/mrxutil.lua:365`, re-activating a hero character's own physics after a state
transition) — called right after spawn, it had no visible effect.

A `WorldProbe` detailed dump (see the [World Inspector deep dive](world-inspector)) on the spawned ship
turned up a likely reason: `Object.GetMass(uBoat)` read `0.00`. Most physics engines special-case a
zero-mass object as static/infinite-mass — i.e., immovable regardless of any other flag. `Object.SetMass
(uGuid, nMass)` exists (confirmed via a live `pairs()` enumeration) but has zero call sites anywhere in
the decompiled corpus — genuinely untested ground. Setting it to `50000` (a placeholder guess, not
derived from anything confirmed) alongside `EnablePhysics` still produced no change.

Conclusion, per the user's own assessment after this result: this is very likely **out of reach until
tools exist for editing the compiled vehicle templates directly** (the WAD/asset files themselves, not
anything reachable from Lua). Not pursued further in this revision.

## The camera investigation

This was the largest single thread of the whole effort — a genuinely thorough, methodical search for any
Lua-reachable way to fix a camera that "pulls focus to the bottom presumed root of the boat model" while
driving or gunning, instead of a normal chase/aim view.

### Round 1: the object+hardpoint form, on the vehicle

`Camera.SetPosition`/`SetLookAt` both have a confirmed real **object+hardpoint** form
(`Camera.SetPosition(uCamera, uObjectGuid, sHardpoint, bFlag)`), not just raw coordinates — confirmed in
`resident/mrxbriefing.lua`'s cinematic-briefing code. The obvious first thing to try was pointing the
camera at a hardpoint on the ship itself.

No hardpoint name for this ship was known going in. Rather than guess blind, a **systematic probe** was
built: `Object.GetHardpointPosition(uBoat, sName)` was tried against every combination of a curated list
of confirmed-real hardpoint naming conventions found by grepping the whole corpus (`"hp_camera_X"` from
cinematic camera positioning, `"hp_seat_X"` from a tank's confirmed `"hp_seat_lt"` in
`resident/mrxactionhijack.lua:149`) — prefixes crossed with the ship's own known position names, 127
candidates total. This found real, working hardpoints on both variants:

```
Allied: hp_seat_cannon, hp_seat_ciwsfm, hp_seat_ciwsrl, hp_seat_samfm, hp_seat_samrr
Chinese: hp_seat_cannon, hp_seat_ciwsfl, hp_seat_ciwsfr, hp_seat_ciwsrl, hp_seat_ciwsrr, hp_seat_sam, hp_seat_driver
```

A single static jump to `"hp_seat_cannon"` via `Camera.Hold` + the object+hardpoint form produced no
visible change — ambiguous on its own, since a subtle jump could simply go unnoticed. To remove that
ambiguity, the camera was cycled through *every* confirmed hardpoint on the ship, each held for 2 seconds
— these are spatially far apart (raw coordinates from the probe confirm this), so a real effect would be
unmistakable. **Nothing moved, across all 10 hardpoints, on either variant.**

A CSV export of the ship's actual bone hierarchy (`al_veh_boat_destroyer_bones.csv` /
`ch_veh_boat_destroyer_bones.csv`, obtained externally, not from the decompiled Lua corpus) confirmed no
bone anywhere is named anything camera-related on either variant, and revealed a real difference between
them: the Allied ship's seat hardpoints are all flagged `intact`, while every one of the Chinese ship's is
flagged `break_piece` (the destructible/debris hierarchy). This didn't explain the negative result on its
own, since the *intact* Allied hardpoints failed identically.

### Round 2: coordinate tracking instead of hardpoint attachment

Given every confirmed real use of the object+hardpoint camera form anywhere in the corpus targets
**static level geometry** (e.g. `"HqInterior"`), never a spawned vehicle, the likely explanation was that
this form simply doesn't apply to a dynamic vehicle instance at all. The fallback: re-read
`Object.GetHardpointPosition(uBoat, "hp_seat_cannon")`'s live coordinates every tick (0.05s,
`Event.TimerRelative`) and feed them into the plain coordinate form of `Camera.SetPosition` — the exact
mechanism the [Freecam deep dive](freecam) already proved works for a detached, on-foot camera. A
`Camera.SetLookAt` was also set each tick (pointed a fixed distance ahead along the ship's own yaw, not
the turret's actual aim direction, which isn't Lua-readable — see the
[Vehicle namespace](../namespaces/vehicle)'s own confirmed finding that no function exposes what a turret
is aiming at or firing) — Freecam's own deep dive confirms `SetPosition` silently no-ops without an
active `SetLookAt` binding.

**Still no movement**, seated in the vehicle, at all.

### Round 3: recipe testing around `Player.SetCinematicMode` and `Camera.Blend`

Every confirmed real camera-lock in this corpus up to this point came from one of three contexts: a
fully-detached, world-paused spectator camera (Freecam); a scripted cinematic/menu sequence
(`mrxbriefing.lua`); or a ragdoll/hijack cutscene (`resident/mrxactionhijack.lua`). That last one is the
only confirmed example of locking a camera during **live, unpaused gameplay** — and its recipe had never
been tried:

```lua
Player.SetCinematicMode(uPlayer, true, true)
Camera.Blend(uCamera, 1)
Camera.SetLookAt(uCamera, self._hijacker, "bone_chest")
Camera.Hold(uCamera, true, false)
```

Neither `SetCinematicMode` nor `Blend` had been used in any test up to this point. A systematic
recipe-test harness ran 8 distinct combinations — with and without `SetCinematicMode`/`Blend`, call-order
swaps, a trailing-flag variation (`true` vs. `false`, since that argument's meaning is explicitly
unconfirmed per the [Camera namespace](../namespaces/camera) page), and a couple of `Hold`-flag
variations — all aimed at the same obviously-wrong fixed test point (30 units straight up from the boat)
so a real effect would be unmistakable, decoupled from whether the actual gun-seat offset looked right.

The result: `Player.SetCinematicMode(uPlayer, true, true)` **broke mouse-driven aim control** the moment
it engaged. And even with control broken — the biggest intervention this engine's camera API offers —
**the camera still didn't move.** Every non-`SetCinematicMode` recipe also produced nothing.

### Round 4: is the camera bound to the character instead of the vehicle?

`Vehicle.GetSeatParams(uSeat)` had only ever been confirmed used elsewhere to check one field
(`IsGunner`). Dumping the *whole* table on this ship's gunner seat turned up something new:

```
IsHijackBlocker = false
IsDriver = false
IsCargo = false
IsGunner = true
IsRiderVulnerable = false
IsStowable = false
IsRiderBashable = false
IsHijackable = false
StowSeatGuid = userdata: 00000000
IsRiderInvisible = true
```

`IsRiderInvisible = true` raised a real hypothesis: if the camera is anchored to the (hidden, possibly
not being updated while invisible) rider character's own bone/position rather than a fixed vehicle
offset, a collapsed or stale character transform would exactly explain "pulling focus to the bottom root
of the boat model." Forcing the rider visible and logging both the rider's and the boat's position side
by side showed the rider *does* have a real, valid, non-degenerate tracked position — distinct from the
boat's own position in all three axes, and distinct again on a second reading (evidently from a different
seat, since `EnterBoat`'s standard check found the driver's seat free and moved the player there between
the two readings). No collapsed/degenerate value at any point.

Following the theory anyway, `Camera.SetPosition`/`SetLookAt` were tried targeting the **character**
instead of the vehicle — both the object+hardpoint form (using `"bone_chest"`, the exact bone name
confirmed real in `mrxactionhijack.lua`'s own camera-lock) and a per-tick coordinate-follow of the
character's live position. **Neither produced any movement either.**

### Conclusion

Every reasonable combination has now been tried: object+hardpoint attachment and manual per-tick
coordinate tracking; targeting both the vehicle and the character; every `Camera.Hold`/`Blend`/
`SetCinematicMode`/trailing-flag combination a reasonable reading of the confirmed real call sites
suggested, including the exact recipe from the one confirmed live-gameplay camera lock in the whole
corpus. Nothing moved the camera even once, and the one technique that's confirmed to matter for *other*
camera contexts (`SetCinematicMode`) broke player control without fixing anything.

The most likely explanation, and a directly analogous one already confirmed earlier in this exact
investigation: the [Vehicle namespace](../namespaces/vehicle) page documents that **no function anywhere
selects what a turret fires** — "a player-operated vehicle's mounted gun fires via a mechanism with no
Lua touchpoint at all." Vehicle/turret camera positioning during active gunning is very likely part of
that same native, no-Lua-touchpoint subsystem, not a chase-cam that simply needs the right override call.
This isn't presented as certain — there's no way to prove a negative from black-box Lua experimentation
alone — but the breadth of what's been tried, and the total lack of any effect from even the heaviest
tool available (`SetCinematicMode`), makes it the best-supported conclusion available.

One low-confidence lead not pursued: `Camera.SetShot(uCameraGuid, sShotName, uBaseActor, uTargetActor,
bFlag)` is real and untried, but its only confirmed real use is generic dialogue framing in cinematics,
with no confirmed shot names that would plausibly apply to a gunner view — trying it would mean guessing
string names blind again, the exact pattern this investigation otherwise avoided throughout.

## Open questions / where to pick this up

- **Physics** — needs external tooling to edit the compiled vehicle template directly; not solvable from
  Lua as things stand.
- **Camera** — very likely a hard wall, not an unsolved bug; `Camera.SetShot` with a real shot name is the
  one untried, low-confidence lead if someone wants to keep pushing.
- **Multi-gun-seat access** — scrapped, not actively being pursued; would need to start from "why do these
  specific attachments not behave like real seats" rather than "how do we find them," which is already
  solved.

## The current script

This is the full experimental version currently deployed, with every diagnostic tool built during this
investigation left in (hardpoint probing, seat-params dumping, rider-visibility toggling, camera cycling/
following/recipe-testing). For a simpler, non-diagnostic version with just spawning and boarding, see `DestroyerTool.lua` on the
[OnKey sample scripts page](../sample-scripts-onkey).

```lua
local KEYVAL = "f9"  -- must be in the first 10 lines -- f2-f8 already taken by the other OnKey scripts in this folder; reuses SpawnDestroyer.lua's old slot, which this replaces

-- DestroyerTool: replaces SpawnDestroyer.lua. Built for a community mod request -- turn the "Chinese
-- Destroyer"/"Allied Destroyer" set-dressing ships into a real, driveable vehicle. Menu-driven (not an
-- instant single-key spawn) so it can offer a choice of which variant to spawn, and tracks whether a boat
-- is already out so Enter/Exit/Despawn are plain menu options instead of needing a continuous keybind poll.
--
-- Status: entering/exiting as driver AND as a gunner both work via the standard function
-- (MrxUtil.EnterBestAvailableSeat's "d"/"g"/"p"/"c" per-type check, called for the local player and,
-- separately excluding "d", for the coop partner) -- this ship really only has 2 usable seats. The
-- display names on the Hash Lookup page ("Vehicle Seat (Destroyer) (cannon)", "(ciwsFL)", etc.) turned
-- out NOT to be additional player-usable seats: a full seat-discovery pass (walking
-- Object.GetAttachedObjects and filtering by those names' own hashes) found guids that resolved to those
-- names, but actually entering one teleported the player to a broken floating position above the ship,
-- not a real seat. Scrapped -- not worth pursuing further right now. Multi-gun-seat access, if it's ever
-- wanted again, would need to start from scratch on why those specific attachments don't behave like
-- real seats, not just how to find them.
--
-- Open item: Physics. Confirmed NOT working as hoped: Object.EnablePhysics(uGuid) (a real, always-paired-
-- with-DisablePhysics function -- see resident/mrxutil.lua:365 for a confirmed call site re-activating a
-- hero character's own physics after a state transition) plus Object.SetMass(uGuid, 50000) (an
-- EXPERIMENTAL, untested-elsewhere call, tried after a live dump showed the ship's mass reading 0.00)
-- were both called right after spawn, and the ship still doesn't behave like a real boat. Not addressed
-- further in this revision.
--
-- In progress: Camera. Badly broken while driving or gunning (looks anchored near the model's own
-- origin/base rather than a normal chase/aim view). ProbeHardpoints confirmed this ship really does use
-- an "hp_seat_<name>" hardpoint convention (same family as a tank's confirmed "hp_seat_lt" at
-- resident/mrxactionhijack.lua:149) -- both variants have "hp_seat_cannon" specifically, among others. A
-- single static jump to it via the confirmed object+hardpoint form of Camera.SetPosition/SetLookAt
-- (resident/mrxbriefing.lua) produced no visible change, which is ambiguous on its own -- CycleHardpoint-
-- Cameras instead cycles the camera through every confirmed hardpoint (spatially far apart on the ship)
-- with a visible delay between each, so a real effect would be unmistakable either way. Still untested
-- whether Camera.Hold (required to make SetPosition stick against the native chase-cam) breaks
-- mouse-driven aim look -- ReleaseCameraHold undoes it if so.

import("MrxMultiPageMenu")
import("MrxUtil")

local nSpawnForwardOffset = 150  -- tweak me: same caveat as before -- destroyer dimensions unconfirmed
local nSpawnHeightOffset = 10    -- tweak me: small lift so it doesn't spawn clipped into the ground/water
local nEnterRetrySeconds = 0.5   -- tweak me: how often to retry boarding once spawned
local nMaxEnterAttempts = 10     -- tweak me: give up after this many retries (5 seconds by default)

-- EXPERIMENTAL: a live WorldProbe detailed dump showed Object.GetMass(uBoat) reading 0.00 -- most physics
-- engines special-case mass=0 as "static/infinite mass" (i.e. immovable), which would fully explain why
-- Object.EnablePhysics alone had no visible effect. Object.SetMass(uGuid, nMass) exists (confirmed via
-- live pairs() enumeration) but has zero call sites anywhere in the decompiled corpus -- genuinely
-- untested. This value is a placeholder guess for a destroyer-scale vessel, not derived from anything
-- confirmed -- tweak me based on what actually happens live.
local nBoatMass = 50000

-- customSin/customCos -- copied from Freecam.lua/Fireworks.lua/SpawnDestroyer.lua. math.sin/math.cos
-- don't exist in this Lua build; this Taylor-series approximation is the established workaround used
-- elsewhere on this wiki.
local function normalizeAngle(nDegrees)
  while nDegrees > 180 do
    nDegrees = nDegrees - 360
  end
  while nDegrees < -180 do
    nDegrees = nDegrees + 360
  end
  return nDegrees
end
local function customSin(nDegrees)
  local nRad = normalizeAngle(nDegrees) * 3.14159265 / 180
  return nRad - nRad ^ 3 / 6 + nRad ^ 5 / 120 - nRad ^ 7 / 5040
end
local function customCos(nDegrees)
  return customSin(nDegrees + 90)
end

_G.DestroyerToolState = _G.DestroyerToolState or {
  uBoat = nil,
  sVariant = nil,
  bCameraFollowActive = false,
  bRecipeTestActive = false,
}
local State = _G.DestroyerToolState

local tVariants = {
  {sLabel = "Chinese Destroyer", sTemplate = "Chinese Destroyer"},
  {sLabel = "Allied Destroyer", sTemplate = "Allied Destroyer"},
}

-- Deliberately excludes "d"/driver -- future hotkeys are expected to assume the driver's seat belongs to
-- the local/primary player, so the coop partner should never end up there via this button.
local tPartnerSeatTypes = {"g", "p", "c"}

local function EnterPartnerSeat(uChar, uBoat)
  for _, sSeatName in ipairs(tPartnerSeatTypes) do
    local bOkSeat, uSeat = pcall(Vehicle.GetSeatByType, uBoat, sSeatName, true)
    if bOkSeat and uSeat then
      local bOkEnter, bEntered = pcall(Vehicle.EnterBySeatGuid, uBoat, uChar, uSeat, true)
      if bOkEnter and bEntered then
        return sSeatName
      end
    end
  end
  return nil
end

local function EnterPartnerBoat()
  local uPartner = Player.GetSecondaryCharacter()
  if not uPartner or not State.uBoat then
    Loader.Printf("DestroyerTool: no coop partner found (Player.GetSecondaryCharacter returned nothing)")
    return
  end
  local sSeatUsed = EnterPartnerSeat(uPartner, State.uBoat)
  Loader.Printf("DestroyerTool: coop partner boarding -- "
    .. (sSeatUsed and ("entered via \"" .. sSeatUsed .. "\"") or "no non-driver seat available"))
end

local function ExitPartnerBoat()
  local uPartner = Player.GetSecondaryCharacter()
  if not uPartner or not State.uBoat then
    return
  end
  local bOk, vResult = pcall(Vehicle.Exit, State.uBoat, uPartner, true)
  Loader.Printf("DestroyerTool: coop partner Vehicle.Exit "
    .. (bOk and ("returned " .. tostring(vResult)) or ("failed: " .. tostring(vResult))))
end

local function SpawnBoat(sTemplate)
  local uChar = Player.GetLocalCharacter()
  if not uChar then
    return
  end
  if State.uBoat then
    Loader.Printf("DestroyerTool: a boat is already tracked -- exit or despawn it first")
    return
  end
  local x, y, z = Object.GetPosition(uChar)
  local nYaw = Object.GetYaw(uChar)
  local nForwardX = customSin(nYaw) * nSpawnForwardOffset
  local nForwardZ = customCos(nYaw) * nSpawnForwardOffset

  local uBoat = Pg.Spawn(sTemplate, x + nForwardX, y + nSpawnHeightOffset, z + nForwardZ)
  if not uBoat then
    Loader.Printf("DestroyerTool: Pg.Spawn(\"" .. sTemplate .. "\") returned nothing")
    return
  end
  State.uBoat = uBoat
  State.sVariant = sTemplate

  local bOkPhysics, vErr = pcall(Object.EnablePhysics, uBoat)
  Loader.Printf("DestroyerTool: spawned " .. sTemplate .. " -- Object.EnablePhysics "
    .. (bOkPhysics and "called" or ("failed: " .. tostring(vErr))))

  local bOkMass, vMassErr = pcall(Object.SetMass, uBoat, nBoatMass)
  Loader.Printf("DestroyerTool: Object.SetMass(" .. tostring(nBoatMass) .. ") "
    .. (bOkMass and "called" or ("failed: " .. tostring(vMassErr))))
end

local function EnterBoat()
  local uChar = Player.GetLocalCharacter()
  if not uChar or not State.uBoat then
    return
  end
  local nAttempt = 0
  local function TryEnter()
    nAttempt = nAttempt + 1
    local bOk, bEntered = pcall(MrxUtil.EnterBestAvailableSeat, uChar, State.uBoat, nil, true)
    if bOk and bEntered then
      Loader.Printf("DestroyerTool: aboard via the standard d/g/p/c seat check")
      return
    end
    if nAttempt >= nMaxEnterAttempts then
      Loader.Printf("DestroyerTool: gave up boarding after " .. tostring(nAttempt) .. " attempt(s)")
      return
    end
    Event.Create(Event.TimerRelative, {nEnterRetrySeconds}, TryEnter, {})
  end
  TryEnter()
end

local function ExitBoat()
  local uChar = Player.GetLocalCharacter()
  if not uChar or not State.uBoat then
    return
  end
  local bOk, vResult = pcall(Vehicle.Exit, State.uBoat, uChar, true)
  Loader.Printf("DestroyerTool: Vehicle.Exit "
    .. (bOk and ("returned " .. tostring(vResult)) or ("failed: " .. tostring(vResult))))
end

local function DespawnBoat()
  if not State.uBoat then
    return
  end
  pcall(Object.Remove, State.uBoat)
  Loader.Printf("DestroyerTool: despawned " .. tostring(State.sVariant))
  State.uBoat = nil
  State.sVariant = nil
end

-- ============================================================
-- Seat params dump -- EXPERIMENTAL. Vehicle.GetSeatParams(uSeat) is only ever confirmed used elsewhere on
-- this wiki to check a single field (IsGunner) -- the rest of the table has never been dumped. If this
-- ship's seats carry a data-driven camera height/offset config, this is where it would show up, and
-- would sidestep fighting the native camera-override system entirely. Requires actually being seated
-- (uses Vehicle.GetSeatFromRider on the local character), not just having a boat spawned.
-- ============================================================
local function DumpSeatParams()
  local uChar = Player.GetLocalCharacter()
  if not uChar or not State.uBoat then
    Loader.Printf("DestroyerTool: no character or no boat tracked")
    return
  end
  local bOkSeat, uSeat = pcall(Vehicle.GetSeatFromRider, uChar)
  if not (bOkSeat and uSeat) then
    Loader.Printf("DestroyerTool: not currently seated -- board the boat first")
    return
  end
  local bOkParams, tParams = pcall(Vehicle.GetSeatParams, uSeat)
  if not (bOkParams and type(tParams) == "table") then
    Loader.Printf("DestroyerTool: Vehicle.GetSeatParams failed or returned no table")
    return
  end
  Loader.Printf("DestroyerTool: seat params dump:")
  for sKey, vValue in pairs(tParams) do
    Loader.Printf("DestroyerTool:   " .. tostring(sKey) .. " = " .. tostring(vValue))
  end
end

-- ============================================================
-- Rider visibility toggle -- EXPERIMENTAL. DumpSeatParams found "IsRiderInvisible = true" on this seat --
-- new information, not previously known. Theory: if the camera is anchored to the (invisible, possibly
-- not being updated while hidden) rider character's own bone/position rather than a fixed vehicle offset,
-- a collapsed/degenerate character transform would exactly explain "pulling focus to the bottom root of
-- the boat model." This forces the rider visible (or back to invisible on a second press -- a toggle, not
-- one-shot) and logs both the rider's and the boat's own position side by side, so a broken/degenerate
-- rider position would be directly visible in the log even before checking the screen.
-- ============================================================
local function ToggleRiderVisible()
  local uChar = Player.GetLocalCharacter()
  if not uChar then
    Loader.Printf("DestroyerTool: no character found")
    return
  end
  local bOkCur, bCurVisible = pcall(Object.IsVisible, uChar)
  local bNewVisible = not (bOkCur and bCurVisible)
  local bOkVis, vVisErr = pcall(Object.SetVisible, uChar, bNewVisible)
  Loader.Printf("DestroyerTool: Object.SetVisible(" .. tostring(bNewVisible) .. ") "
    .. (bOkVis and "called" or ("failed: " .. tostring(vVisErr))))

  local bOkPos, x, y, z = pcall(Object.GetPosition, uChar)
  if bOkPos and x then
    Loader.Printf("DestroyerTool: rider position = " .. tostring(x) .. ", " .. tostring(y) .. ", " .. tostring(z))
  end
  if State.uBoat then
    local bOkBoatPos, bx, by, bz = pcall(Object.GetPosition, State.uBoat)
    if bOkBoatPos and bx then
      Loader.Printf("DestroyerTool: boat position = " .. tostring(bx) .. ", " .. tostring(by) .. ", " .. tostring(bz))
    end
  end
end

-- ============================================================
-- Hardpoint probe -- EXPERIMENTAL. Systematically tries Object.GetHardpointPosition(uBoat, sName) against
-- a curated list of candidate names instead of guessing one blind. The candidates come from two
-- confirmed-real naming conventions found by grepping the whole decompiled corpus: "hp_camera_X" (camera
-- positioning hardpoints, resident/mrxbriefing.lua) and "hp_seat_X" (a vehicle seat hardpoint, confirmed
-- on a TANK via resident/mrxactionhijack.lua:149's "hp_seat_lt" -- NOT confirmed for this ship
-- specifically, since nothing in the whole corpus ever scripts the destroyer as a player vehicle). Logs
-- every name that actually returns real coordinates; anything that errors or returns nil is silently
-- skipped, so a long "no results" run isn't a sign anything is broken -- most combinations are expected
-- to miss.
-- ============================================================
local tHardpointExact = {"hp_seat_lt", "hp_camera_a", "hp_camera_b", "hp_menu_camera"}
local tHardpointPrefixes = {"hp_camera_", "hp_seat_", "hp_gun_", "hp_barrel_", "hp_muzzle_", "hp_turret_", "hp_"}
local tHardpointSuffixes = {
  "cannon", "ciwsfl", "ciwsfm", "ciwsfr", "ciwsrl", "ciwsrr", "sam", "samfm", "samrr",
  "driver", "d", "g", "lt", "rt", "a", "b", "gunner", "gun",
}

local function ProbeHardpoints()
  if not State.uBoat then
    Loader.Printf("DestroyerTool: no boat tracked -- spawn one first")
    return
  end
  Loader.Printf("DestroyerTool: probing hardpoint names on " .. tostring(State.sVariant) .. "...")

  local tTried = {}
  local nTotal = 0
  local nFound = 0

  local function TryName(sName)
    if tTried[sName] then
      return
    end
    tTried[sName] = true
    nTotal = nTotal + 1
    local bOk, x, y, z = pcall(Object.GetHardpointPosition, State.uBoat, sName)
    if bOk and x then
      nFound = nFound + 1
      Loader.Printf("DestroyerTool:   FOUND \"" .. sName .. "\" = " .. tostring(x) .. ", " .. tostring(y) .. ", " .. tostring(z))
    end
  end

  for _, sName in ipairs(tHardpointExact) do
    TryName(sName)
  end
  for _, sPrefix in ipairs(tHardpointPrefixes) do
    for _, sSuffix in ipairs(tHardpointSuffixes) do
      TryName(sPrefix .. sSuffix)
    end
  end

  Loader.Printf("DestroyerTool: hardpoint probe complete -- " .. tostring(nFound) .. " of " .. tostring(nTotal)
    .. " candidate name(s) resolved")
end

-- ============================================================
-- Hardpoint camera cycle -- EXPERIMENTAL. A single static jump to "hp_seat_cannon" produced no visible
-- change, which is ambiguous on its own -- could mean the call genuinely does nothing on a live spawned
-- vehicle (every confirmed real object+hardpoint call site elsewhere attaches to a static level object
-- instead, e.g. "HqInterior", never a spawned vehicle), or could just mean the jump was too subtle to
-- notice. This instead cycles the camera through every hardpoint ProbeHardpoints confirmed real across
-- both variants -- these are spatially far apart on the ship (see the raw coordinates from that probe),
-- so if Camera.SetPosition/SetLookAt is doing anything at all here, the view jumping between them every
-- couple seconds should be unmistakable. If nothing visibly changes through the entire cycle, that's
-- reasonably strong evidence this whole mechanism doesn't take effect on a spawned vehicle's own
-- hardpoint at all, not just that the "cannon" one specifically didn't work. Camera.Hold (required to
-- make SetPosition stick against the game's own automatic chase-cam -- see the Freecam deep dive) is the
-- one thing that could break mouse-driven aim look -- ReleaseCameraHold below exists so this is always
-- reversible; use it immediately if aiming stops responding.
-- ============================================================
local tHardpointCycleList = {
  "hp_seat_cannon", "hp_seat_ciwsfl", "hp_seat_ciwsfm", "hp_seat_ciwsfr",
  "hp_seat_ciwsrl", "hp_seat_ciwsrr", "hp_seat_sam", "hp_seat_samfm",
  "hp_seat_samrr", "hp_seat_driver",
}
local nHardpointCycleSeconds = 2  -- tweak me: how long to hold each hardpoint before jumping to the next

local function CycleHardpointCameras()
  local uPlayer = Player.GetLocalPlayer()
  local uCamera = uPlayer and Player.GetCamera(uPlayer)
  if not uCamera or not State.uBoat then
    Loader.Printf("DestroyerTool: no camera or no boat tracked")
    return
  end

  local bOkHold, vHoldErr = pcall(Camera.Hold, uCamera, true, false)
  Loader.Printf("DestroyerTool: Camera.Hold(true) " .. (bOkHold and "called" or ("failed: " .. tostring(vHoldErr))))

  local nIndex = 0
  local function StepToNext()
    nIndex = nIndex + 1
    local sHardpoint = tHardpointCycleList[nIndex]
    if not sHardpoint then
      Loader.Printf("DestroyerTool: hardpoint camera cycle finished -- did the view visibly jump at any point?")
      return
    end
    Loader.Printf("DestroyerTool: [" .. tostring(nIndex) .. "/" .. tostring(table.getn(tHardpointCycleList))
      .. "] moving camera to \"" .. sHardpoint .. "\"")
    local bOkPos, vPosErr = pcall(Camera.SetPosition, uCamera, State.uBoat, sHardpoint, true)
    if not bOkPos then
      Loader.Printf("DestroyerTool:   SetPosition failed: " .. tostring(vPosErr))
    end
    local bOkLook, vLookErr = pcall(Camera.SetLookAt, uCamera, State.uBoat, sHardpoint, true, true)
    if not bOkLook then
      Loader.Printf("DestroyerTool:   SetLookAt failed: " .. tostring(vLookErr))
    end
    Event.Create(Event.TimerRelative, {nHardpointCycleSeconds}, StepToNext, {})
  end
  StepToNext()
end

-- Stops every camera experiment below (the follow-loop and the recipe-test cycle), releases Camera.Hold,
-- and turns Player.SetCinematicMode back off -- the one, general "undo everything camera-related" button.
local function ReleaseCameraHold()
  State.bCameraFollowActive = false
  State.bRecipeTestActive = false
  local uPlayer = Player.GetLocalPlayer()
  local uCamera = uPlayer and Player.GetCamera(uPlayer)
  if uCamera then
    local bOk, vErr = pcall(Camera.Hold, uCamera, false, false)
    Loader.Printf("DestroyerTool: Camera.Hold(false) " .. (bOk and "called" or ("failed: " .. tostring(vErr))))
  end
  if uPlayer then
    pcall(Player.SetCinematicMode, uPlayer, false)
  end
end

-- ============================================================
-- Coordinate-based hardpoint tracking -- EXPERIMENTAL. The object+hardpoint form of Camera.SetPosition/
-- SetLookAt produced zero visible change across every confirmed hardpoint on both variants -- likely
-- because every real use of that form anywhere in the corpus (resident/mrxbriefing.lua) attaches to
-- static level geometry, never a spawned vehicle instance. This instead re-reads "hp_seat_cannon"'s
-- current world position every tick via Object.GetHardpointPosition (confirmed to return real
-- coordinates during ProbeHardpoints) and feeds those into the plain coordinate form of
-- Camera.SetPosition -- the same mechanism the Freecam deep dive already proved works, just never
-- confirmed yet while seated in a vehicle specifically, which may have its own separate camera-override
-- system from the on-foot chase-cam Freecam overrode.
--
-- Per the Freecam deep dive's own confirmed finding, Camera.SetPosition silently does nothing without an
-- active Camera.SetLookAt binding, so this also sets one -- pointed a fixed distance ahead of the
-- hardpoint along the SHIP's current yaw (Object.GetYaw(uBoat)), not the turret's actual aim direction
-- (which isn't readable from Lua -- see the Vehicle namespace page's confirmed finding that no function
-- exposes what a turret is aiming at or firing). This is only enough to test whether repositioning works
-- at all while seated -- it will NOT track your mouse-aim correctly, so don't judge the final camera feel
-- from this, only whether the position moves at all.
-- ============================================================
local nCameraFollowInterval = 0.05  -- tweak me: how often to refresh the tracked position, seconds
local nCameraLookAhead = 20         -- tweak me: how far ahead of the hardpoint the look-at point sits

local function StartCameraFollow()
  local uPlayer = Player.GetLocalPlayer()
  local uCamera = uPlayer and Player.GetCamera(uPlayer)
  if not uCamera or not State.uBoat then
    Loader.Printf("DestroyerTool: no camera or no boat tracked")
    return
  end
  if State.bCameraFollowActive then
    Loader.Printf("DestroyerTool: camera follow already running")
    return
  end
  State.bCameraFollowActive = true

  local bOkHold, vHoldErr = pcall(Camera.Hold, uCamera, true, false)
  Loader.Printf("DestroyerTool: Camera.Hold(true) " .. (bOkHold and "called" or ("failed: " .. tostring(vHoldErr))))

  local function Tick()
    if not State.bCameraFollowActive then
      return
    end
    Event.Create(Event.TimerRelative, {nCameraFollowInterval}, Tick, {})

    local bOkPos, x, y, z = pcall(Object.GetHardpointPosition, State.uBoat, "hp_seat_cannon")
    if not (bOkPos and x) then
      return
    end
    pcall(Camera.SetPosition, uCamera, x, y, z, true)

    local bOkYaw, nYaw = pcall(Object.GetYaw, State.uBoat)
    if bOkYaw and nYaw then
      local nLookX = x + customSin(nYaw) * nCameraLookAhead
      local nLookZ = z + customCos(nYaw) * nCameraLookAhead
      pcall(Camera.SetLookAt, uCamera, nLookX, y, nLookZ, false, true)
    end
  end
  Tick()
  Loader.Printf("DestroyerTool: camera follow started -- tracking hp_seat_cannon every tick; use \"Release Camera Hold\" to stop")
end

-- ============================================================
-- Player-bone camera -- EXPERIMENTAL. ToggleRiderVisible confirmed the rider has a real, valid tracked
-- position that's nowhere near where the camera's been stuck -- two separate readings (evidently two
-- different seats, since EnterBoat fired again between them) both gave sensible, distinct coordinates,
-- never a degenerate/collapsed value. That raises the question of whether the camera should be bound to
-- the PLAYER CHARACTER instead of the vehicle/hardpoint. This reuses the exact object+hardpoint form
-- already confirmed real, but points it at the character with "bone_chest" -- the exact bone name
-- confirmed real in resident/mrxactionhijack.lua:916's own camera-lock
-- (Camera.SetLookAt(uCamera, self._hijacker, "bone_chest")) -- rather than a vehicle hardpoint. No
-- SetCinematicMode (confirmed to both break control and still not move the camera).
-- ============================================================
local function TestPlayerBoneCamera()
  local uPlayer = Player.GetLocalPlayer()
  local uChar = Player.GetLocalCharacter()
  local uCamera = uPlayer and Player.GetCamera(uPlayer)
  if not uCamera or not uChar then
    Loader.Printf("DestroyerTool: no camera or no character found")
    return
  end

  local bOkHold, vHoldErr = pcall(Camera.Hold, uCamera, true, false)
  Loader.Printf("DestroyerTool: Camera.Hold(true) " .. (bOkHold and "called" or ("failed: " .. tostring(vHoldErr))))

  local bOkPos, vPosErr = pcall(Camera.SetPosition, uCamera, uChar, "bone_chest", true)
  Loader.Printf("DestroyerTool: Camera.SetPosition(player, bone_chest) "
    .. (bOkPos and "called" or ("failed: " .. tostring(vPosErr))))

  local bOkLook, vLookErr = pcall(Camera.SetLookAt, uCamera, uChar, "bone_chest", true, true)
  Loader.Printf("DestroyerTool: Camera.SetLookAt(player, bone_chest) "
    .. (bOkLook and "called" or ("failed: " .. tostring(vLookErr))))
end

-- Coordinate-based fallback in case the object+hardpoint form above doesn't move anything (same pattern
-- already proven for the boat's hp_seat_cannon hardpoint, retargeted at the character's own live
-- position instead).
local function StartPlayerCameraFollow()
  local uPlayer = Player.GetLocalPlayer()
  local uChar = Player.GetLocalCharacter()
  local uCamera = uPlayer and Player.GetCamera(uPlayer)
  if not uCamera or not uChar then
    Loader.Printf("DestroyerTool: no camera or no character found")
    return
  end
  if State.bCameraFollowActive then
    Loader.Printf("DestroyerTool: camera follow already running")
    return
  end
  State.bCameraFollowActive = true

  local bOkHold, vHoldErr = pcall(Camera.Hold, uCamera, true, false)
  Loader.Printf("DestroyerTool: Camera.Hold(true) " .. (bOkHold and "called" or ("failed: " .. tostring(vHoldErr))))

  local function Tick()
    if not State.bCameraFollowActive then
      return
    end
    Event.Create(Event.TimerRelative, {nCameraFollowInterval}, Tick, {})

    local bOkPos, x, y, z = pcall(Object.GetPosition, uChar)
    if not (bOkPos and x) then
      return
    end
    pcall(Camera.SetPosition, uCamera, x, y + 2, z, true)

    local bOkYaw, nYaw = pcall(Object.GetYaw, uChar)
    if bOkYaw and nYaw then
      local nLookX = x + customSin(nYaw) * nCameraLookAhead
      local nLookZ = z + customCos(nYaw) * nCameraLookAhead
      pcall(Camera.SetLookAt, uCamera, nLookX, y + 2, nLookZ, false, true)
    end
  end
  Tick()
  Loader.Printf("DestroyerTool: player-bone camera follow started -- tracking the character every tick; use \"Release Camera Hold\" to stop")
end

-- ============================================================
-- Camera recipe tests -- EXPERIMENTAL. Neither the object+hardpoint form nor per-tick coordinate tracking
-- produced any visible change while seated -- both were only ever confirmed working in contexts other
-- than "seated in a vehicle during live gameplay" (Freecam is fully detached and world-paused;
-- mrxbriefing's object+hardpoint form only targets static level geometry). The one confirmed example of
-- locking a camera during LIVE, UNPAUSED gameplay -- resident/mrxactionhijack.lua:914-917, a ragdoll
-- knockdown cinematic -- uses a sequence never tried yet:
--   Player.SetCinematicMode(uPlayer, true, true)
--   Camera.Blend(uCamera, 1)
--   Camera.SetLookAt(uCamera, self._hijacker, "bone_chest")
--   Camera.Hold(uCamera, true, false)
-- Two ingredients here (SetCinematicMode, Blend) have never been tried in any test so far. This runs a
-- series of distinct recipes built around that finding -- with and without SetCinematicMode/Blend, a
-- couple of call-order swaps, and a couple of Hold-flag variations -- one at a time with a pause between
-- each, all aimed at the SAME obvious fixed test point (30 units straight up from the boat, looking back
-- down at it) rather than the cannon seat specifically. That deliberately decouples "does this recipe
-- move the camera at all" from "does the cannon-seat position look right" -- worth answering separately
-- once something actually works. Whichever recipe (if any) produces a visible jump is the one to build
-- the real fix on.
--
-- Player.SetCinematicMode is a bigger intervention than anything tried so far -- confirmed elsewhere (see
-- the Freecam deep dive) to hide/disable normal player control in other contexts. "Release Camera Hold"
-- explicitly turns it back off in addition to releasing Hold, and each step below also resets both before
-- trying the next recipe, so state never leaks from one attempt into the next.
-- ============================================================
local nRecipeStepSeconds = 3  -- tweak me: how long each recipe gets before moving to the next

local tCameraRecipes = {
  {
    sLabel = "Hold, then SetPosition+SetLookAt (same as the earlier follow test)",
    fRun = function(uCamera, uPlayer, x, y, z, lx, ly, lz)
      pcall(Camera.Hold, uCamera, true, false)
      pcall(Camera.SetPosition, uCamera, x, y, z, true)
      pcall(Camera.SetLookAt, uCamera, lx, ly, lz, false, true)
    end,
  },
  {
    sLabel = "SetPosition+SetLookAt, then Hold (order swap)",
    fRun = function(uCamera, uPlayer, x, y, z, lx, ly, lz)
      pcall(Camera.SetPosition, uCamera, x, y, z, true)
      pcall(Camera.SetLookAt, uCamera, lx, ly, lz, false, true)
      pcall(Camera.Hold, uCamera, true, false)
    end,
  },
  {
    -- The trailing boolean on SetPosition/SetLookAt has an explicitly unconfirmed meaning per the Camera
    -- wiki page -- every other recipe here passes true; this tries false instead, no SetCinematicMode.
    sLabel = "Hold, then SetPosition+SetLookAt with trailing flag false instead of true",
    fRun = function(uCamera, uPlayer, x, y, z, lx, ly, lz)
      pcall(Camera.Hold, uCamera, true, false)
      pcall(Camera.SetPosition, uCamera, x, y, z, false)
      pcall(Camera.SetLookAt, uCamera, lx, ly, lz, false, false)
    end,
  },
  {
    sLabel = "Add Camera.Blend(0) before SetPosition/SetLookAt/Hold",
    fRun = function(uCamera, uPlayer, x, y, z, lx, ly, lz)
      pcall(Camera.Blend, uCamera, 0)
      pcall(Camera.SetPosition, uCamera, x, y, z, true)
      pcall(Camera.SetLookAt, uCamera, lx, ly, lz, false, true)
      pcall(Camera.Hold, uCamera, true, false)
    end,
  },
  {
    sLabel = "Add Player.SetCinematicMode before everything, then Blend+SetPosition+SetLookAt+Hold",
    fRun = function(uCamera, uPlayer, x, y, z, lx, ly, lz)
      pcall(Player.SetCinematicMode, uPlayer, true, true)
      pcall(Camera.Blend, uCamera, 1)
      pcall(Camera.SetPosition, uCamera, x, y, z, true)
      pcall(Camera.SetLookAt, uCamera, lx, ly, lz, false, true)
      pcall(Camera.Hold, uCamera, true, false)
    end,
  },
  {
    sLabel = "Exact confirmed hijack order: CinematicMode, Blend, SetLookAt, Hold (no SetPosition)",
    fRun = function(uCamera, uPlayer, x, y, z, lx, ly, lz)
      pcall(Player.SetCinematicMode, uPlayer, true, true)
      pcall(Camera.Blend, uCamera, 1)
      pcall(Camera.SetLookAt, uCamera, lx, ly, lz, false, true)
      pcall(Camera.Hold, uCamera, true, false)
    end,
  },
  {
    sLabel = "CinematicMode + SetPosition/SetLookAt + Hold with bFlag2=true",
    fRun = function(uCamera, uPlayer, x, y, z, lx, ly, lz)
      pcall(Player.SetCinematicMode, uPlayer, true, true)
      pcall(Camera.SetPosition, uCamera, x, y, z, true)
      pcall(Camera.SetLookAt, uCamera, lx, ly, lz, false, true)
      pcall(Camera.Hold, uCamera, true, true)
    end,
  },
  {
    sLabel = "CinematicMode + SetPosition/SetLookAt + Hold with 3rd flag true",
    fRun = function(uCamera, uPlayer, x, y, z, lx, ly, lz)
      pcall(Player.SetCinematicMode, uPlayer, true, true)
      pcall(Camera.SetPosition, uCamera, x, y, z, true)
      pcall(Camera.SetLookAt, uCamera, lx, ly, lz, false, true)
      pcall(Camera.Hold, uCamera, true, false, true)
    end,
  },
}

local function RunCameraRecipeTests()
  local uPlayer = Player.GetLocalPlayer()
  local uCamera = uPlayer and Player.GetCamera(uPlayer)
  if not uCamera or not State.uBoat then
    Loader.Printf("DestroyerTool: no camera or no boat tracked")
    return
  end
  if State.bRecipeTestActive then
    Loader.Printf("DestroyerTool: recipe tests already running")
    return
  end
  State.bRecipeTestActive = true

  local bOkPos, bx, by, bz = pcall(Object.GetPosition, State.uBoat)
  if not (bOkPos and bx) then
    Loader.Printf("DestroyerTool: couldn't get boat position")
    State.bRecipeTestActive = false
    return
  end
  -- Fixed, obviously-wrong test point: 30 units straight up from the boat, looking back down at it.
  local x, y, z = bx, by + 30, bz
  local lx, ly, lz = bx, by, bz

  local nIndex = 0
  local function StepToNext()
    if not State.bRecipeTestActive then
      return
    end
    pcall(Camera.Hold, uCamera, false, false)
    pcall(Player.SetCinematicMode, uPlayer, false)

    nIndex = nIndex + 1
    local tRecipe = tCameraRecipes[nIndex]
    if not tRecipe then
      State.bRecipeTestActive = false
      Loader.Printf("DestroyerTool: camera recipe tests finished -- did the view visibly jump at any point? "
        .. "Also confirm whether aiming/control still works right now.")
      return
    end
    Loader.Printf("DestroyerTool: [" .. tostring(nIndex) .. "/" .. tostring(table.getn(tCameraRecipes))
      .. "] trying: " .. tRecipe.sLabel)
    tRecipe.fRun(uCamera, uPlayer, x, y, z, lx, ly, lz)
    Event.Create(Event.TimerRelative, {nRecipeStepSeconds}, StepToNext, {})
  end
  StepToNext()
end

-- ============================================================
-- Menu -- rebuilt fresh on every keypress, same pattern as every other OnKey menu on this wiki. Shows
-- spawn choices when no boat is tracked, or enter/exit/despawn for both players once one is.
-- ============================================================
MrxMultiPageMenu.Reset()
if State.uBoat then
  MrxMultiPageMenu.AddOption("Enter " .. tostring(State.sVariant), EnterBoat)
  MrxMultiPageMenu.AddOption("Exit boat", ExitBoat)
  MrxMultiPageMenu.AddOption("Enter Coop Partner", EnterPartnerBoat)
  MrxMultiPageMenu.AddOption("Exit Coop Partner", ExitPartnerBoat)
  MrxMultiPageMenu.AddOption("Probe Hardpoints (experimental)", ProbeHardpoints)
  MrxMultiPageMenu.AddOption("Dump Seat Params (experimental, must be seated)", DumpSeatParams)
  MrxMultiPageMenu.AddOption("Toggle Rider Visible (experimental)", ToggleRiderVisible)
  MrxMultiPageMenu.AddOption("Cycle Camera Through Hardpoints (experimental)", CycleHardpointCameras)
  MrxMultiPageMenu.AddOption("Start Camera Follow (experimental)", StartCameraFollow)
  MrxMultiPageMenu.AddOption("Test Player Bone Camera (experimental)", TestPlayerBoneCamera)
  MrxMultiPageMenu.AddOption("Start Player Camera Follow (experimental)", StartPlayerCameraFollow)
  MrxMultiPageMenu.AddOption("Run Camera Recipe Tests (experimental)", RunCameraRecipeTests)
  MrxMultiPageMenu.AddOption("Release Camera Hold (undo all camera experiments)", ReleaseCameraHold)
  MrxMultiPageMenu.AddOption("Despawn boat", DespawnBoat)
else
  for _, tVariant in ipairs(tVariants) do
    local sTemplate = tVariant.sTemplate
    MrxMultiPageMenu.AddOption("Spawn " .. tVariant.sLabel, function()
      SpawnBoat(sTemplate)
    end)
  end
end
MrxMultiPageMenu.AddOption("Close this menu", nil, nil, true, true)
MrxMultiPageMenu.Display("Destroyer Tool:")
```

## General lessons

1. **When a single test result is ambiguous, make the next one impossible to misread.** A static jump to
   one hardpoint producing "no visible change" could mean the mechanism doesn't work, or could mean the
   jump was too subtle to notice. Cycling through ten spatially-separated positions with a visible pause
   between each removes that ambiguity entirely — the same pattern used for the fixed 30-units-straight-up
   test point in the recipe tests later.
2. **Systematic probing beats guessing, and it's cheap.** Rather than guess one hardpoint name, a curated
   list of confirmed-real naming conventions crossed against known position suffixes (127 candidates, one
   `pcall`-wrapped read-only query each) found the real names directly — and cost nothing to run.
3. **Dump the whole table, not just the one field you think you need.** `Vehicle.GetSeatParams` had only
   ever been checked for `IsGunner` anywhere in this project. Dumping every field turned up
   `IsRiderInvisible`, a fact nobody had looked for because nobody had reason to look.
4. **A confirmed negative result across a genuinely broad test is itself real information.** Ruling out
   object+hardpoint attachment, coordinate tracking, every `Hold`/`Blend`/`SetCinematicMode` combination
   the corpus suggested, and both plausible camera-anchor targets (vehicle and character) is a strong
   basis for "this is a wall," even without being able to read the native code that proves it.
5. **A pattern noticed once is worth checking for again.** The Vehicle namespace's already-documented "no
   Lua touchpoint for what a turret fires" finding turned out to be the single best predictor for how the
   camera investigation would end — the same category of limitation, confirmed independently, twice.
