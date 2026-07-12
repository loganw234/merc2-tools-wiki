---
title: "Building a World Inspector (WAILA) — work in progress"
parent: Deep Dives
nav_order: 7
---

# Deep Dive: Building a World Inspector (WAILA)

> **Status: work in progress.** The tool itself — a menu-driven "what am I looking at" mode plus a bulk
> nearby-object dump — is built, deployed, and confirmed working live: WAILA toggles on/off, cycles
> candidates with the arrow keys, shows an in-world marker, and logs full detail on demand. But the actual
> goal behind it — extracting enough real, identifying information about an arbitrary game object to be
> useful for modding, not just a hashed name and a boolean flag or two — hit a hard, confirmed ceiling
> partway through. Investigating *around* that ceiling opened three follow-on threads that are all still
> open: whether `Pg.Spawn` is even the right thing to be watching for world population, what (if anything)
> a deeper native hook would look like, and a proposed but unbuilt "layer delamination" tool. This page is
> a running record of all of it, not a finished recipe.

## The goal

A user asked for a custom menu to help identify and probe things in the game world — something built
around the `Pg.FastCollect*` family, but with real thought put into making it a genuinely useful tool for
future modders who want to physically walk up to something in-game and learn how its Lua side works, not
just read raw `FastCollect` results in isolation. The design converged on a "WAILA" (What Am I Looking At)
mode as the centerpiece — a background loop that keeps identifying whatever's nearest the player and lets
you dig into it — plus a handful of bulk utility options layered around it.

## Design: reticle-targeting turned out to be the wrong idea

The first design pass leaned on `Player.GetTargetUnderReticle(uPlayerGuid)` as "what's under my crosshair."
It's confirmed real (`nX, nY, nZ, uGuid = Player.GetTargetUnderReticle(uPlayerGuid)`), but its only two real
call sites in the whole decompiled corpus are `mrxguisatellite.lua` and `mrxguisniperscope.lua` — special
targeting-overlay contexts (the airstrike support-call satellite view and the sniper scope), not the
ordinary player camera. Building WAILA on it would have rested on an unconfirmed assumption about what it
returns outside those two contexts.

The actual fix sidesteps the question entirely: run a low-radius `Pg.FastCollect*` sweep around the player,
sort by distance, and let the left/right arrow keys cycle through candidates if the nearest one isn't the
one you meant. No unconfirmed native behavior required — and as a side effect, it naturally supports
"cycle through everything near me," not just whatever's on one fixed camera ray.

## What's built and confirmed working

`scripts/OnKey/WorldProbe.lua` (`F7`):

- **Candidate pool** — merges all 12 `Pg.FastCollect*` family members (6 with confirmed real call sites
  elsewhere in the corpus, 6 — `Boats`/`Cars`/`Jets`/`Props`/`Usables`/`GroundVehiclesExceptTanks` — with
  zero known call sites anywhere) into one deduplicated, distance-sorted list. Every call is wrapped in
  `pcall`, which doubles as a live test of the six unconfirmed members.
- **WAILA mode** — `RefreshWaila` (every 1s: re-collects and re-sorts candidates, preserving the current
  selection by guid if it's still in range) plus `WailaKeyPoll` (every 0.08s: edge-detects left/right/down
  via `Loader.IsKeyDown` rather than `Loader.PopKeyEvents`, specifically so it doesn't contend with
  `CommonSpawnMenu.lua`'s own key-event-buffer-draining free-text console if both happen to be active at
  once).
- Left/right cycles candidates; down arrow dumps full detail on the *current* selection to
  `Loader.Printf`, independent of cycling, so you can get the complete picture on one specific thing without
  needing the bulk dump option.
- An in-world marker (`Marker.AddBlip`, reusing the one exact call already confirmed live-tested elsewhere
  on this wiki, in [Snippets](../snippets)) follows the current selection.
- "Dump nearby objects to log" menu option — one-shot wide-radius sweep, everything found described and
  logged at once.
- An on-screen scrolling log window — a second, independently-named clone of the `MrxGuiTextBuffer` pattern
  already confirmed working in `CommonSpawnMenu.lua`, given its own global name so the two scripts don't
  fight over one widget instance if both are active in the same session.

## Bugs found and fixed along the way

- **WAILA silently never turning on, `DumpNearby` quitting after one entry.** Root cause: unprotected
  `Object.GetName`/`Sys.GuidToString` calls threw outright for some objects, and `RefreshWaila`'s reschedule
  call sat at the *end* of the function — one uncaught error permanently killed the whole timer chain. Fix:
  `pcall`-wrap every native call, and move both loops' `Event.Create` reschedule to fire immediately after
  the `wailaActive` check, before any of the actual per-tick work.
- **`"attempt to concatenate...userdata"` errors with no diagnostic info.** `Object.GetName` sometimes
  returns a bare userdata instead of a string or nil — a real, confirmed live finding, not a hypothetical.
  Fix: `SafeString`, which type-checks and folds the unexpected value into readable diagnostic text instead
  of crashing or failing silently, and `DescribeTargetSafe`, which surfaces the *real* pcall error message,
  `type(uGuid)`, and — for table-typed failures — a raw `MrxUtil.GetTableAsString` dump.
- **Missing in-world marker.** Designed in the original brainstorm, dropped during implementation, caught
  by the user testing it live ("We also dont seem to be adding the icon to the selected thing inworld").
  Fix: `Marker.AddBlip`/`ClearMarker` lifecycle tied to `State.uMarker`.
- **Excessive float precision in on-screen output.** `Round2()` — display-only, never used for anything
  actually compared or computed with.
- **A multi-minute WAILA lockout after a bulk dump.** `MrxGuiTextBuffer.AddMessage`'s real confirmed
  signature includes `nDisplayDuration`/`nFadeDuration`, and each message occupies the box for the sum of
  both before the next one can show. An early version of `DumpNearby` blindly copied `CommonSpawnMenu.lua`'s
  15-second default across all 194 dumped lines — nearly 50 minutes of queued messages, silently blocking
  every later WAILA update. Fix: an explicit, much shorter duration (1s) for anything logged in bulk.

## The ceiling: no literal spawn-template string is reachable

This is the part worth being explicit about, since it shaped everything that came after.
`ProbeMysteryUserdata` chases every unfamiliar userdata this tool encounters through `SafeGuidString`,
`Object.GetPosition`, `Object.GetHealth`, `Object.GetName`, `Object.GetLocalizedName`, `Object.IsTemplate`,
and `Object.GetModelName`, and `DescribeTargetDetailed` reads all 87 confirmed functions on the
[`Object` namespace](../namespaces/object) page against a selected target — not just the handful this file
otherwise uses day to day.

The single most interesting confirmed finding from that: `Object.GetParent(uGuid)` really does return a
reference to the object's own spawn template, not some shared "spawn group" container (an earlier, wrong
guess based on its `0x8000xxxx` address range — corrected once live data showed the parent's own
`GetLocalizedName` matching the instance's own name exactly, and `Object.IsTemplate` true, every single
time). But chasing that confirmed template reference through every other read-only query available still
never surfaces a plain literal template/spawn-name string: `Object.GetLocalizedName` on the template comes
back a hashed localization key (`"[0x7a4c1e28]"`-shaped, often shared identically across many different
instances of the same generic NPC/vehicle type), and `Object.GetModelName` returns yet another opaque
userdata handle rather than a string, for most objects tested.

**The literal, `Pg.Spawn`-able name string for an already-existing object appears not to be retained
anywhere Lua-reachable, unless something explicitly called `Object.SetName` on it.**

**Update:** a promising resolution path exists now, though it's a lookup table, not a new Lua-reachable
call. See the [Hash Lookup](../hash-lookup) page — a 6,119-entry name-to-hash table cross-referenced
against several template names already confirmed real on this wiki (`Veyron`, `Supply Drop (Blueprints)`,
`Chinese Destroyer`), all matching exactly. If a live `Sys.GuidToString(Object.GetParent(uGuid))` capture
ever matches that table's `value_hex` column, that would fully resolve this ceiling for any object with a
compiled template entry -- not yet live-tested, flagged as the next thing to try there.

## What this tool led to (three open threads)

1. **`SpawnScraper.lua`** (`scripts/OnLoad/`) — hooks `Pg.Spawn` itself, logging every first-seen template
   name for the rest of the session. Deployed and working exactly as designed, but live testing turned up
   something bigger than a bug: flying around an actively-playing session for an extended period produced
   exactly 2 log lines — a scripted car spawn outside the HQ, and the player's own manually-spawned
   helicopter. The overwhelming majority of what populates this game's open world is **not** created via
   any Lua-visible `Pg.Spawn` call at all.
2. **Chasing a "deeper" hook.** Checked whether the `Event` namespace has any universal "an object was just
   created" broadcast — it doesn't; all 44 event-type IDs were checked, and the closest, `ObjectHibernation`,
   still requires already having the guid you're asking about. Checked whether each `resident/` module's own
   `OnActivate(uGuid, uRuntimeOwner, iArg)` lifecycle hook could substitute — it's real and fires per-object,
   but the engine dispatches natively straight into each module's own isolated environment by object type,
   with no single shared chokepoint. Catching "literally everything" this way would mean wrapping
   `OnActivate` across every resident module individually — a fundamentally bigger and riskier undertaking
   than the one clean `Pg.Spawn` wrap, and one that would still miss any placed object with no resident
   module at all. The real mechanism turned out to be the **layer system** —
   `Pg.LoadLayer`/`Pg.UnloadLayer`, native, bulk, and opaque at the per-object level from Lua. See the
   [MrxLayerManager page](../resident/mrxlayermanager)'s boot-time layer manifest section for the concrete
   catalog this surfaced.
3. **A proposed "layer delamination" tool.** Snapshot every guid reachable via `FastCollect*` immediately
   before and after a given layer loads, diff the two sets, and describe whatever's new with
   `DescribeTargetDetailed`, tagged with the layer name that produced it. **Not yet built.** Still subject to
   the ceiling above (hashed names, not literal template strings) and two structural gaps: it can only see
   objects covered by some `FastCollect*` variant, and the snapshot has to be centered somewhere — almost
   certainly the player — so a layer loading far away would be invisible to it regardless.

## Open questions / where to pick this up

- **The layer-delamination sweep tool itself — designed, not built.** It now has a concrete, safe seed list
  to iterate: the ~416 names in [`xQ!L.lua`](../vz/xql)'s boot manifest (see the layer manager page), which removes the
  need for either riskier approach originally considered — racing the boot sequence to intercept early
  `Pg.LoadLayer` calls, or mass-unloading currently-loaded layers to get back to some "clean" state.
- **`SpawnScraper.lua` has no guid→name cross-reference yet.** Flagged earlier as a small, easy addition —
  WAILA could show the real template name for anything spawned during an active tracking session — but not
  yet built.
- **Whether wrapping `OnActivate` broadly across resident modules is worth the risk hasn't been decided
  either way.** It would be the most complete per-object creation hook available in principle, but the
  blast radius of getting it wrong (potentially breaking object activation game-wide, across every module,
  rather than one contained feature) hasn't been weighed against how much it would actually add beyond what
  the layer system already explains.
- **The ambient traffic/pedestrian population still has no identified mechanism at all.** Neither
  `Pg.Spawn` nor the ~416 known boot-time layer names contain anything that reads as a traffic/pedestrian/
  population system by name. Most likely a proximity-driven native streaming system with no Lua-facing hook
  whatsoever — but that's inference, not confirmed. Genuinely unresolved.

## Current script

`scripts/OnKey/WorldProbe.lua`:

```lua
local KEYVAL = "f7"  -- must be in the first 10 lines -- f2-f6 already taken by the other OnKey scripts in this folder

-- WorldProbe: an exploratory toolkit for identifying and inspecting nearby objects in the game world --
-- built for people who want to poke at how things work under the hood, not just play the game.
--
-- "WAILA" (What Am I Looking At) mode does NOT use the native reticle-targeting function
-- (Player.GetTargetUnderReticle) -- that function is confirmed real, but its only two real call sites
-- in the whole decompiled corpus are both special targeting-overlay contexts (the satellite support-call
-- screen and the sniper scope widget), not the normal player camera, so building on it here would rest
-- on an unconfirmed assumption about what it does outside those two contexts. Instead, this runs a
-- low-radius Pg.FastCollect* sweep around the player, sorts by distance, and lets you cycle through
-- candidates with the left/right arrow keys if the nearest one isn't what you wanted -- this sidesteps
-- the question entirely.

import("MrxMultiPageMenu")
import("MrxUtil")
import("MrxFactionManager")
import("MrxGui")
import("MrxGuiTextBuffer")

local VK_LEFT = 0x25
local VK_RIGHT = 0x27
local VK_DOWN = 0x28

local nWailaRadius = 20          -- tweak me: how far around the player WAILA looks for candidates
local nWailaRefreshInterval = 1  -- tweak me: seconds between candidate-list refreshes
local nWailaPollInterval = 0.08  -- tweak me: how often the cycle-key check runs
local nDumpRadius = 100          -- tweak me: radius used by the "Dump nearby objects" menu option

-- Marker.AddBlip(uGuid, "temp_radar_icon_airplane", 48, 255, 255, 255, 255, 0.5, 16, 20) is the one
-- exact call confirmed live-tested elsewhere on this wiki (Snippets) -- reusing it verbatim rather than
-- guessing a different, untested texture name that might just silently fail to load. It's a generic
-- placeholder icon, not a reflection of what kind of object is actually selected -- known quirk from
-- that same test: it renders at ground level under the object, not at the object's own height.
local sMarkerTexture = "temp_radar_icon_airplane"

_G.WorldProbeState = _G.WorldProbeState or {
  wailaActive = false,
  tCandidates = {},
  nIndex = 1,
  sCurrentGuidString = nil,
  bLeftWasDown = false,
  bRightWasDown = false,
  bDownWasDown = false,
  uMarker = nil,
}
local State = _G.WorldProbeState

-- ============================================================
-- Nearby-object collection, merged across every FastCollect* family member -- including several
-- (Boats/Cars/Jets/Props/Usables/GroundVehiclesExceptTanks) with no confirmed real call site anywhere
-- in the decompiled corpus. Each call is wrapped in pcall so one unconfirmed member erroring doesn't
-- take the others down with it -- this doubles as a live test of those, which is worth watching
-- Loader.Printf output for.
-- ============================================================
local tCollectFns = {
  Pg.FastCollectHumans, Pg.FastCollectGroundVehicles, Pg.FastCollectBuildings,
  Pg.FastCollectFlying, Pg.FastCollectTanks, Pg.FastCollectHelicopters,
  Pg.FastCollectBoats, Pg.FastCollectCars, Pg.FastCollectJets,
  Pg.FastCollectProps, Pg.FastCollectUsables, Pg.FastCollectGroundVehiclesExceptTanks,
}

-- Raw floats out of this engine print with a dozen+ digits of noise (e.g. "2743.6677246094") --
-- rounding for display only, never for anything actually compared/computed with.
local function Round2(n)
  if type(n) ~= "number" then
    return tostring(n)
  end
  return string.format("%.2f", n)
end

-- Sys.GuidToString wrapped everywhere it's called in this file -- confirmed necessary: a live test
-- showed a native call throwing outright (not just returning nil) for at least one object among a
-- FastCollect merge, and this was one of the two unprotected candidates for what did it.
local function SafeGuidString(uGuid)
  local bOk, sResult = pcall(Sys.GuidToString, uGuid)
  if bOk and type(sResult) == "string" then
    return sResult
  end
  return nil
end

-- When a native hands back a userdata we weren't expecting (instead of the string we asked for), don't
-- just tostring() it and give up -- try treating it as a real object reference in its own right, the
-- same way the seat userdata this was built for (Vehicle.GetSeatByType's return) sit right next to
-- their parent vehicle's own guid in the same numeric neighborhood (0x4000BBB0/0x4000BBAF next to the
-- vehicle's own 0x4000BBAC), a strong sign they're genuine references, not junk. Sys.GuidToString comes
-- first since that hex-string form is the actual "paste this into another script" reference format used
-- everywhere else in this engine (Pg.GetGuidByName/StringToGuid round-trip on exactly this shape).
-- Position/health/name are cheap follow-up probes to see if it resolves to something spatial/alive too.
local function ProbeMysteryUserdata(vValue)
  if type(vValue) ~= "userdata" then
    return nil
  end
  local tParts = {}

  local sGuidStr = SafeGuidString(vValue)
  if sGuidStr then
    table.insert(tParts, "guid=" .. sGuidStr)
  end

  local bOkPos, x, y, z = pcall(Object.GetPosition, vValue)
  if bOkPos and x then
    table.insert(tParts, "pos=" .. Round2(x) .. "," .. Round2(y) .. "," .. Round2(z))
  end

  local bOkHealth, nHealth = pcall(Object.GetHealth, vValue)
  if bOkHealth and nHealth then
    table.insert(tParts, "hp=" .. Round2(nHealth))
  end

  local bOkName, vName = pcall(Object.GetName, vValue)
  if bOkName and type(vName) == "string" then
    table.insert(tParts, "name=" .. vName)
  end

  -- Live find: Object.GetModelName doesn't return a text string for a lot of objects -- it returns
  -- *another* userdata handle, which this same probe resolves in turn. Object.IsTemplate on that handle
  -- tests directly whether it's actually a reference to the spawn template itself, in which case its own
  -- GetLocalizedName could be the real Pg.Spawn-able template string, not just more internal plumbing.
  local bOkLocName, vLocName = pcall(Object.GetLocalizedName, vValue)
  if bOkLocName and type(vLocName) == "string" then
    table.insert(tParts, "locName=" .. vLocName)
  end

  local bOkTemplate, bIsTemplate = pcall(Object.IsTemplate, vValue)
  if bOkTemplate and bIsTemplate then
    table.insert(tParts, "isTemplate=true")
  end

  -- Only kept when it resolves to a plain string, not recursed into further if it's yet another
  -- userdata -- this is specifically hoping a *template*'s own GetModelName succeeds where a live
  -- instance's didn't, without risking an unbounded chain of nested mystery handles.
  local bOkModelName, vModelName = pcall(Object.GetModelName, vValue)
  if bOkModelName and type(vModelName) == "string" then
    table.insert(tParts, "modelName=" .. vModelName)
  end

  if table.getn(tParts) == 0 then
    return nil
  end
  local sJoined = ""
  for i, sPart in ipairs(tParts) do
    if i > 1 then
      sJoined = sJoined .. ", "
    end
    sJoined = sJoined .. sPart
  end
  return sJoined
end

-- Several natives here turned out to sometimes return something other than a string/nil even when the
-- call itself succeeds (Object.GetName returning a bare userdata for at least some objects was a real,
-- confirmed live find, not a guess -- see DescribeTarget below). Checking type() explicitly rather than
-- just truthiness avoids feeding an unexpected type straight into string concatenation, and the
-- unexpected type/value gets kept in the fallback text rather than silently discarded, since "this came
-- back as a userdata instead of a string" is itself a useful thing for this tool to surface.
local function SafeString(bOk, vValue, sFallback)
  if bOk and type(vValue) == "string" then
    return vValue
  elseif bOk and vValue ~= nil then
    local sProbe = ProbeMysteryUserdata(vValue)
    if sProbe then
      return "(" .. type(vValue) .. ": " .. sProbe .. ")"
    end
    return "(" .. type(vValue) .. " value: " .. tostring(vValue) .. ")"
  end
  return sFallback
end

local function CollectNearby(x, y, z, fRadius)
  local tSeen = {}
  local tResults = {}
  for _, fCollect in ipairs(tCollectFns) do
    local bOk, tFound = pcall(fCollect, x, y, z, fRadius)
    if bOk and type(tFound) == "table" then
      for _, uGuid in pairs(tFound) do
        if uGuid then
          local sKey = SafeGuidString(uGuid)
          if sKey and not tSeen[sKey] then
            tSeen[sKey] = true
            table.insert(tResults, uGuid)
          end
        end
      end
    end
  end
  return tResults
end

local function BuildCandidateList()
  local uChar = Player.GetLocalCharacter()
  if not uChar then
    return {}
  end
  local x, y, z = Object.GetPosition(uChar)
  local sMyKey = SafeGuidString(uChar)
  local tRaw = CollectNearby(x, y, z, nWailaRadius)

  local tWithDist = {}
  for _, uGuid in ipairs(tRaw) do
    if SafeGuidString(uGuid) ~= sMyKey then
      local bOkDist, nDist = pcall(MrxUtil.GetDistanceToObject, uGuid, x, y, z)
      if bOkDist and nDist then
        table.insert(tWithDist, {uGuid = uGuid, nDist = nDist})
      end
    end
  end

  table.sort(tWithDist, function(a, b) return a.nDist < b.nDist end)

  local tSorted = {}
  for _, tEntry in ipairs(tWithDist) do
    table.insert(tSorted, tEntry.uGuid)
  end
  return tSorted
end

-- ============================================================
-- Per-object description -- name, distance-independent identity, health, faction, a curated label
-- checklist (there's no "list all labels" function, only Object.HasLabel(uGuid, sLabel) checked one at
-- a time, so this checks a fixed list rather than enumerating), and a small vehicle-specific block if
-- the "Vehicle" label hits.
-- ============================================================
local tLabelChecklist = {
  "Human", "Hero", "PMC", "Vehicle", "Occupied", "Prisoner", "Disposable",
  "Allied", "China", "Guerilla", "VZ", "OC", "Oil",
}

local function DescribeTarget(uGuid)
  -- GetName is the internal/debug name; GetLocalizedName is the actual display string shown to the
  -- player (often a shared, hashed key like "[0x7a4c1e28]" for generic/non-unique NPCs -- confirmed
  -- live: several different soldier instances all shared the exact same one, consistent with a
  -- per-type, not per-instance, display name). Only keep GetName's result when it's a real string --
  -- confirmed live that it's just as often a bare userdata as it is nil, and GetLocalizedName is more
  -- likely to actually be populated in either of those cases, not just the nil one.
  local bOkName, vName = pcall(Object.GetName, uGuid)
  local sName = (bOkName and type(vName) == "string") and vName or nil
  if not sName then
    local bOkLocName, vLocName = pcall(Object.GetLocalizedName, uGuid)
    sName = SafeString(bOkLocName, vLocName, "(unnamed)")
  end
  local sGuid = SafeGuidString(uGuid) or "?"
  local bOkHealth, nHealth = pcall(Object.GetHealth, uGuid)

  local sLabels = ""
  local bIsVehicle = false
  for _, sLabel in ipairs(tLabelChecklist) do
    local bOkLabel, bHasLabel = pcall(Object.HasLabel, uGuid, sLabel)
    if bOkLabel and bHasLabel then
      if sLabels ~= "" then
        sLabels = sLabels .. ","
      end
      sLabels = sLabels .. sLabel
      if sLabel == "Vehicle" then
        bIsVehicle = true
      end
    end
  end

  local sFaction = nil
  local bOkFaction, vFactionLabel = pcall(MrxUtil.GetFaction, uGuid)
  if bOkFaction and vFactionLabel ~= nil then
    local sFactionLabel = SafeString(true, vFactionLabel, "?")
    local bOkAbbrev, vAbbrev = pcall(MrxFactionManager.GetFactionAbbrev, vFactionLabel)
    sFaction = SafeString(bOkAbbrev, vAbbrev, sFactionLabel)
  end

  local sLine = sName .. " [" .. sGuid .. "]"
  if bOkHealth and nHealth then
    sLine = sLine .. " hp=" .. Round2(nHealth)
  end
  if sFaction then
    sLine = sLine .. " faction=" .. sFaction
  end
  if sLabels ~= "" then
    sLine = sLine .. " labels={" .. sLabels .. "}"
  end
  if bIsVehicle then
    local bOkDriver, uDriver = pcall(Vehicle.GetDriver, uGuid)
    sLine = sLine .. " driver=" .. tostring(bOkDriver and uDriver ~= nil)
  end
  return sLine
end

-- Wraps DescribeTarget and, on failure, surfaces the *real* pcall error message plus type(uGuid) and
-- (if it's a table rather than a plain uGuid) a raw MrxUtil.GetTableAsString dump of its contents --
-- the errors seen live came back completely blank before this, which made it impossible to tell which
-- FastCollect* family member was actually the problem, or in what way.
local function DescribeTargetSafe(uGuid)
  local bOk, sResult = pcall(DescribeTarget, uGuid)
  if bOk then
    return sResult
  end
  local sType = type(uGuid)
  local sLine = "(error: " .. tostring(sResult) .. ", type=" .. sType .. ")"
  if sType == "table" then
    local bOkDump, sDump = pcall(MrxUtil.GetTableAsString, uGuid)
    if bOkDump and sDump then
      sLine = sLine .. " contents=" .. sDump
    end
  end
  return sLine
end

-- Fuller dump for one specific object, to Loader.Printf (no display-duration/queue concerns there,
-- unlike the on-screen box) rather than the terse one-liner every candidate gets during cycling. This
-- is "dump the entire object" as completely as this engine's API actually allows -- uGuids are opaque
-- native handles, not real Lua tables, so there's no generic reflection possible; this instead tries
-- every relevant read-only Object.* query confirmed on the Object namespace page (87 functions total),
-- not just the handful used elsewhere in this file, plus GetAttachedObjects (which can enumerate seats
-- and other attachments directly, a better source than checking Vehicle.GetSeatByType one type at a
-- time) and the Vehicle seat checks as a second, overlapping source.
local function DescribeTargetDetailed(uGuid)
  Loader.Printf("WorldProbe: ===== detailed info =====")
  Loader.Printf("WorldProbe: " .. DescribeTargetSafe(uGuid))

  -- Three different, genuinely distinct name-shaped fields.
  local bOkLocName, vLocName = pcall(Object.GetLocalizedName, uGuid)
  local sLocName = SafeString(bOkLocName, vLocName, nil)
  if sLocName then
    Loader.Printf("WorldProbe:   localized name = " .. sLocName)
  end
  local bOkModel, vModel = pcall(Object.GetModelName, uGuid)
  local sModel = SafeString(bOkModel, vModel, nil)
  if sModel then
    Loader.Printf("WorldProbe:   model name = " .. sModel)
  end

  local bOkPos, x, y, z = pcall(Object.GetPosition, uGuid)
  if bOkPos and x then
    Loader.Printf("WorldProbe:   position = " .. Round2(x) .. ", " .. Round2(y) .. ", " .. Round2(z))
  end

  local bOkYaw, nYaw = pcall(Object.GetYaw, uGuid)
  if bOkYaw and nYaw then
    Loader.Printf("WorldProbe:   yaw = " .. Round2(nYaw))
  end

  local uChar = Player.GetLocalCharacter()
  if uChar then
    local bOkDist, nDist = pcall(MrxUtil.GetDistanceBetween, uChar, uGuid)
    if bOkDist and nDist then
      Loader.Printf("WorldProbe:   distance from you = " .. Round2(nDist))
    end
  end

  local bOkMaxHp, nMaxHp = pcall(Object.GetMaxHealth, uGuid)
  if bOkMaxHp and nMaxHp then
    Loader.Printf("WorldProbe:   max health = " .. Round2(nMaxHp))
  end

  local bOkVel, nVel = pcall(Object.GetVelocity, uGuid)
  if bOkVel and nVel then
    Loader.Printf("WorldProbe:   velocity = " .. Round2(nVel))
  end

  local bOkMass, nMass = pcall(Object.GetMass, uGuid)
  if bOkMass and nMass then
    Loader.Printf("WorldProbe:   mass = " .. Round2(nMass))
  end

  -- Boolean state flags -- only the ones that come back true get printed, to keep this readable.
  local tBoolChecks = {
    {"alive", Object.IsAlive}, {"awake", Object.IsAwake}, {"hibernated", Object.IsHibernated},
    {"valid", Object.IsValid}, {"visible", Object.IsVisible}, {"template", Object.IsTemplate},
    {"disguised", Object.IsDisguised}, {"playerControlled", Object.IsPlayerControlled},
  }
  local sFlags = ""
  for _, tCheck in ipairs(tBoolChecks) do
    local bOkFlag, bFlagVal = pcall(tCheck[2], uGuid)
    if bOkFlag and bFlagVal then
      if sFlags ~= "" then
        sFlags = sFlags .. ","
      end
      sFlags = sFlags .. tCheck[1]
    end
  end
  if sFlags ~= "" then
    Loader.Printf("WorldProbe:   flags = " .. sFlags)
  end

  -- CONFIRMED live, not just a guess: Object.GetParent(uGuid) returns this object's own spawn template,
  -- not some shared container -- every single live test showed the parent's own locName matching the
  -- instance's own localized name exactly, plus isTemplate=true every time. Address range (0x8000xxxx)
  -- is consistently different from live dynamic instances (0x4000xxxx) but *different per object*, not
  -- shared across a cluster -- ruling out the earlier "spawn group/encounter container" guess. Labeled
  -- "parent/template" below to make that relationship explicit rather than leaving it implicit.
  local bOkParent, uParent = pcall(Object.GetParent, uGuid)
  if bOkParent and uParent then
    Loader.Printf("WorldProbe:   parent/template = " .. (ProbeMysteryUserdata(uParent) or tostring(uParent)))
  end

  local bOkInVeh, uInVeh = pcall(Object.InVehicle, uGuid)
  if bOkInVeh and uInVeh then
    Loader.Printf("WorldProbe:   in vehicle = " .. (ProbeMysteryUserdata(uInVeh) or tostring(uInVeh)))
  end

  local bOkAttached, tAttached = pcall(Object.GetAttachedObjects, uGuid)
  if bOkAttached and type(tAttached) == "table" then
    local nAttachedCount = table.getn(tAttached)
    if nAttachedCount > 0 then
      Loader.Printf("WorldProbe:   attached objects (" .. tostring(nAttachedCount) .. "):")
      for _, uAttached in ipairs(tAttached) do
        Loader.Printf("WorldProbe:     - " .. DescribeTargetSafe(uAttached))
      end
    end
  end

  for _, sSeatType in ipairs({"d", "p", "g"}) do
    local bOkSeat, vSeat = pcall(Vehicle.GetSeatByType, uGuid, sSeatType)
    if bOkSeat and vSeat then
      local sSeatLine = "seat[" .. sSeatType .. "] = " .. tostring(vSeat)
      local sProbe = ProbeMysteryUserdata(vSeat)
      if sProbe then
        sSeatLine = sSeatLine .. " (" .. sProbe .. ")"
      end
      Loader.Printf("WorldProbe:   " .. sSeatLine)
    end
  end
end

-- ============================================================
-- On-screen scrolling log -- same MrxGuiTextBuffer widget pattern already confirmed working in
-- CommonSpawnMenu.lua's free-text console, minus the text-input half (WAILA only needs to display,
-- never type). Given its own global name (not reused from CommonSpawnMenu) so the two scripts don't
-- share -- and potentially fight over -- the same widget instance if both are used in the same session.
-- ============================================================
WorldProbeLogUI = WorldProbeLogUI or {
  logBox = nil,
  isVisible = false,
}

function WorldProbeLogUI:Init(x, y, width, height)
  if self.logBox then
    return true
  end

  x = x or 20
  y = y or 150
  width = width or 340
  height = height or 220

  self.logBox = MrxGui.ImageWidget:new()
  self.logBox:SetLocation(x, y, x + width, y + height)
  self.logBox.BasicData = self.logBox.BasicData or {}
  self.logBox.BasicData.name = "MessageBox"

  local initFunc = _G.HandleInstantiationEventForTextBuffer or (_G.MrxGuiTextBuffer and _G.MrxGuiTextBuffer.HandleInstantiationEventForTextBuffer)
  if initFunc then
    initFunc(self.logBox, {})
  else
    return false
  end

  self.logBox:SetColor(24, 24, 24)
  self.logBox:SetTranslucency(200)

  if _G.Player and _G.Player.GetLocalPlayer then
    local p = _G.Player.GetLocalPlayer()
    self.logBox:SetOwner(p)
  end

  MrxGui.AddWidget(self.logBox)
  self.logBox:SetVisible(false)
  self.isVisible = false
  return true
end

function WorldProbeLogUI:Show(bVisible)
  if bVisible and not self.logBox then
    self:Init()
  end
  if not self.logBox then
    return
  end
  self.isVisible = bVisible
  self.logBox:SetVisible(bVisible)
end

function WorldProbeLogUI:AddMessage(sMessage, nDuration)
  if not self.logBox then
    self:Init()
  end
  if not self.logBox or not self.logBox.AddMessage then
    return
  end
  -- Real confirmed signature (mrxguitextbuffer.lua): AddMessage(oTextBuffer, sMessage, nPriority,
  -- nDisplayDuration, nFadeDuration, bClearBuffer, bAllowsAppends, ...). There's a real pending-message
  -- queue behind this -- each message occupies the box for nDisplayDuration + nFadeDuration seconds
  -- before the next one can show, so dumping 194 lines at the old (blindly-copied-from-CommonSpawnMenu)
  -- 15-second duration meant a multi-minute backlog blocking any later WAILA update. 3s default here,
  -- with dump messages explicitly passing 1s -- see DumpNearby below.
  self.logBox:AddMessage(sMessage, 5, nDuration or 3, 1, false, true)
  self:Show(true)
end

-- ============================================================
-- WAILA loops: a slow refresh (re-collect + re-sort candidates, preserving the current selection by
-- guid if it's still in range) and a fast poll (watch for left/right arrow edges to cycle). Both check
-- State.wailaActive at the top and simply stop rescheduling themselves once it's false -- toggling off
-- is what actually halts them, not any explicit cancellation.
-- ============================================================
local function ClearMarker()
  if State.uMarker then
    pcall(Marker.Remove, State.uMarker)
    State.uMarker = nil
  end
end

local function UpdateWailaDisplay()
  local uGuid = State.tCandidates[State.nIndex]
  if not uGuid then
    if State.sCurrentGuidString ~= nil then
      State.sCurrentGuidString = nil
      ClearMarker()
      WorldProbeLogUI:AddMessage("(nothing nearby)")
    end
    return
  end
  local sKey = SafeGuidString(uGuid)
  if sKey ~= State.sCurrentGuidString then
    State.sCurrentGuidString = sKey
    WorldProbeLogUI:AddMessage(DescribeTargetSafe(uGuid))

    ClearMarker()
    local bOkMarker, uNewMarker = pcall(Marker.AddBlip, uGuid, sMarkerTexture, 48, 255, 255, 255, 255, 0.5, 16, 20)
    if bOkMarker then
      State.uMarker = uNewMarker
    end
  end
end

-- Both loops below reschedule themselves FIRST, immediately after the wailaActive check, before doing
-- any of the actual (occasionally-erroring, despite the pcalls above) per-tick work -- so an error
-- anywhere in that work costs at most one tick's update instead of silently killing the whole loop.
-- This is what was actually wrong before: RefreshWaila's reschedule call sat at the very end, after
-- UpdateWailaDisplay, so a single uncaught error there meant the timer chain just never continued.
local function RefreshWaila()
  if not State.wailaActive then
    return
  end
  Event.Create(Event.TimerRelative, {nWailaRefreshInterval}, RefreshWaila, {})

  local tNewCandidates = BuildCandidateList()
  local nNewIndex = 1
  if State.sCurrentGuidString then
    for i, uGuid in ipairs(tNewCandidates) do
      if SafeGuidString(uGuid) == State.sCurrentGuidString then
        nNewIndex = i
        break
      end
    end
  end
  State.tCandidates = tNewCandidates
  State.nIndex = nNewIndex
  UpdateWailaDisplay()
end

local function WailaKeyPoll()
  if not State.wailaActive then
    return
  end
  Event.Create(Event.TimerRelative, {nWailaPollInterval}, WailaKeyPoll, {})

  local bLeftDown = Loader.IsKeyDown(VK_LEFT)
  local bRightDown = Loader.IsKeyDown(VK_RIGHT)
  local bDownDown = Loader.IsKeyDown(VK_DOWN)
  local n = table.getn(State.tCandidates)
  if n > 0 then
    if bLeftDown and not State.bLeftWasDown then
      State.nIndex = State.nIndex - 1
      if State.nIndex < 1 then
        State.nIndex = n
      end
      UpdateWailaDisplay()
    elseif bRightDown and not State.bRightWasDown then
      State.nIndex = State.nIndex + 1
      if State.nIndex > n then
        State.nIndex = 1
      end
      UpdateWailaDisplay()
    end
    -- Down arrow doesn't cycle -- it dumps a fuller detailed view of whatever's currently selected to
    -- Loader.Printf, independent of left/right, so you can get the full picture on just one thing
    -- without needing the bulk "Dump nearby objects" menu option.
    if bDownDown and not State.bDownWasDown then
      local uCurrent = State.tCandidates[State.nIndex]
      if uCurrent then
        DescribeTargetDetailed(uCurrent)
        WorldProbeLogUI:AddMessage("Detailed info logged -- check lua_loader_printf.log", 2)
      end
    end
  end
  State.bLeftWasDown = bLeftDown
  State.bRightWasDown = bRightDown
  State.bDownWasDown = bDownDown
end

local function ToggleWaila()
  State.wailaActive = not State.wailaActive
  if State.wailaActive then
    WorldProbeLogUI:Show(true)
    WorldProbeLogUI:AddMessage("WAILA enabled -- left/right arrows cycle, down arrow logs full detail")
    RefreshWaila()
    WailaKeyPoll()
  else
    ClearMarker()
    WorldProbeLogUI:AddMessage("WAILA disabled")
    WorldProbeLogUI:Show(false)
  end
end

-- ============================================================
-- Bulk utility: one-shot dump of everything in a wider radius, to the log window and Loader.Printf both.
-- ============================================================
local function DumpNearby()
  local uChar = Player.GetLocalCharacter()
  if not uChar then
    return
  end
  local x, y, z = Object.GetPosition(uChar)
  local tFound = CollectNearby(x, y, z, nDumpRadius)
  local nCount = table.getn(tFound)
  local sHeader = "--- " .. tostring(nCount) .. " objects within " .. tostring(nDumpRadius) .. " units ---"
  Loader.Printf("WorldProbe: " .. sHeader)
  WorldProbeLogUI:AddMessage(sHeader, 1)  -- 1s here and below: a 194-line dump at the old 15s-per-message
                                          -- default queued up for minutes and blocked WAILA the whole time
  for _, uGuid in ipairs(tFound) do
    local sLine = DescribeTargetSafe(uGuid)
    Loader.Printf("WorldProbe:   " .. sLine)
    WorldProbeLogUI:AddMessage(sLine, 1)
  end
end

-- ============================================================
-- Menu -- rebuilt fresh on every keypress (same pattern as ConsoleCheatsMenu.lua/CommonSpawnMenu.lua),
-- so the WAILA option's label always reflects current state.
-- ============================================================
MrxMultiPageMenu.Reset()
MrxMultiPageMenu.AddOption(State.wailaActive and "Disable WAILA" or "Enable WAILA", ToggleWaila)
MrxMultiPageMenu.AddOption("Dump nearby objects to log", DumpNearby)
MrxMultiPageMenu.AddOption("Close this menu", nil, nil, true, true)
MrxMultiPageMenu.Display("World Probe:")
```

`scripts/OnLoad/SpawnScraper.lua`:

```lua
-- SpawnScraper.lua -- drop this in scripts/OnLoad/. Passively catalogs every unique Pg.Spawn template
-- name used during the session, by wrapping the native and logging each NEW (not-yet-seen) name to
-- Loader.Printf the moment it's first spawned. The log file itself becomes the running, deduplicated
-- catalog -- there's no separate "dump" action, just watch lua_loader_printf.log accumulate over play.
--
-- Misses anything spawned before this hook installs -- very early level-load spawns, and anything
-- already placed/loaded before OnLoad scripts run at all (which is most of what a typical WorldProbe.lua
-- session actually finds, since that's pre-placed level content, not live Pg.Spawn calls). Accepted
-- tradeoff, not a bug -- everything spawned via Pg.Spawn from here on, for the rest of the session
-- (across level transitions too -- both the hook and the accumulated name list persist via _G, guarded
-- so re-running this OnLoad script on a later level load doesn't wrap an already-wrapped Pg.Spawn again),
-- gets caught.
--
-- Pg.Spawn is architecturally nothing like dynamic_import -- it's called constantly throughout the
-- entire decompiled corpus (every civilian, vehicle, prop) with no sign of the caller-stack-level
-- sensitivity that made dynamic_import unsafe to wrap. Its return value IS used by every real caller
-- though, so the wrapper captures it in a local and returns that local on a separate line -- not
-- `return fOriginal(...)`, which is a tail call and the exact phrasing that broke dynamic_import
-- elsewhere in this project's history.

_G.SpawnScraperNames = _G.SpawnScraperNames or {}
_G.SpawnScraperCount = _G.SpawnScraperCount or 0

if not _G._bSpawnScraperHooked then
  _G._bSpawnScraperHooked = true

  local fOriginalSpawn = Pg.Spawn
  Pg.Spawn = function(sTemplateName, ...)
    local uSpawned = fOriginalSpawn(sTemplateName, ...)
    if type(sTemplateName) == "string" and not _G.SpawnScraperNames[sTemplateName] then
      _G.SpawnScraperNames[sTemplateName] = true
      _G.SpawnScraperCount = _G.SpawnScraperCount + 1
      Loader.Printf("SpawnScraper: [" .. tostring(_G.SpawnScraperCount) .. "] " .. sTemplateName)
    end
    return uSpawned
  end

  Loader.Printf("SpawnScraper: hook installed, monitoring Pg.Spawn for the rest of the session")
end
```

## General lessons

1. **Reschedule a recurring `Event.Create` timer loop *before* doing any per-tick work, not after.** One
   uncaught error in the work should cost a single tick, not silently end the whole loop — this was the
   actual root cause behind WAILA appearing to never activate at all.
2. **A native call "succeeding" (no error) doesn't mean it returned the type you expected.**
   `Object.GetName` returning a bare userdata instead of a string or nil was real and confirmed live, and
   swallowing that behind a generic `tostring()` or a blank failure message makes it impossible to diagnose
   from the log alone. Keep the real error text and `type()` in every failure path.
3. **`MrxGuiTextBuffer.AddMessage`'s queue is real.** Display duration times message count is wall-clock
   time the box is unavailable for anything else. Use a short duration for anything dumped in bulk.
4. **Chase every mystery userdata through the same small set of generic probes** (`SafeGuidString`,
   position, health, name variants, `IsTemplate`) rather than special-casing each call site — this is what
   actually turned "returns some userdata" into a documented, comparable pattern, worth reusing wholesale
   for the next tool that runs into an unfamiliar returned handle.
5. **A negative result is still a real result.** The fact that chasing `Object.GetParent`'s confirmed
   template reference through every other `Object.*` query *still* never produced a literal name string is
   exactly what established the ceiling documented above, rather than just one more thing left "not yet
   tried."
