---
title: "Custom Networked Events"
parent: Deep Dives
nav_order: 3
---

# Deep Dive: Custom Networked Events

**Core mechanism confirmed live, with two real constraints discovered along the way.** This page
investigates one specific question: once two players are already in a co-op session, can mod-authored Lua
scripts exchange their *own* custom data between them, riding on the game's existing real-time sync layer?
**Yes** — confirmed by an actual 2-player test while building the [co-op chat feature](coop-chat): a
hijacked module's `NetEventCallback` really does fire on the *other* player's machine when triggered by
`Net.SendCustomEvent`, and it works in both directions (host→client and client→host). That test also
surfaced two real constraints on what you can actually put in the payload — both covered below, and both
were surprises, not things anyone predicted from reading the source alone.

**Out of scope on purpose**: this page is not about restoring or replacing the game's original online
matchmaking. That ground has already been covered — an earlier community investigation established that
the matchmaking backend isn't reachable from Lua at all, and multiplayer has separately been restored
already via server emulation, entirely outside Lua. Nothing here revisits that. This page only cares about
what mods can do with a session that's already connected, however that connection came to exist.

## `Net.SendCustomEvent` and `NetEventCallback`

Confirmed on the [Net namespace page](../namespaces/net#sendcustomevent-general-purpose-mission-sync):

```lua
Net.SendCustomEvent(sModuleName, nEventId, tArgs, bReliable)
```

The receiving side, confirmed directly in `resident/alarm.lua`:

```lua
NETEVENT_ALARMACTIVATE = 0
NETEVENT_ALARMDEACTIVATE = 1

function NetEventCallback(nEventType, tArgs)
  if nEventType == NETEVENT_ALARMACTIVATE then
    NetSafeAlarmActivated(tArgs[1])
  elseif nEventType == NETEVENT_ALARMDEACTIVATE then
    NetSafeAlarmDeactivated(tArgs[1])
  end
end
```

There's no explicit registration call anywhere for this. `NetEventCallback` is just a global function name
the engine looks up and calls, keyed by the `sModuleName` string passed into `SendCustomEvent` — the same
"callback by naming convention" pattern documented elsewhere on this wiki for `Awake`/`OnActivate` on world
objects (see the [Resident Modules](../resident/) landing page). Every `resident/`/`vz/` module that wants
to sync something across a co-op session defines its own `NetEventCallback` and its own small set of
numeric event IDs, entirely independently of every other module's.

`Alarm` is shown above purely because it's a short, readable example already in the decompiled corpus —
don't actually pick it as a hijack target. It's a per-object world-entity script, not an always-resident
module, so `import("Alarm")` throws `attempt to index global 'Alarm' (a nil value)` unless the current
level happens to have a real alarm object loaded. `MrxFactionManager` is confirmed always-resident (used
throughout this wiki already) and is the module the working ping-pong test and the [co-op chat
feature](coop-chat) both actually hijack.

**This is the interesting part.** If dispatch really is just "look up a global function named
`NetEventCallback` belonging to the module named by this string," there's no obvious reason custom
cross-player events couldn't ride on top of it.

There are two ways to try reaching that dispatch, though, and they carry very different amounts of risk:

- **Register a wholly new module name of your own** — untested, and genuinely uncertain, since the
  registry backing `sModuleName` resolution (`_MODULES`, presumably) is never touched by any Lua script
  anywhere in the corpus. Every `import()` call in this entire project has been for a module that's real
  original game content; whether the native side accepts an invented name it's never seen before is
  unknown.
- **Hijack an existing module's `NetEventCallback`** — the safer bet, because it reuses exactly the same
  "reassign a name, the next call sees your version" mechanism already proven working in the
  [function-override deep dive](function-override), riding on a module that's *already* genuinely
  registered on both host and client (since it's real game content, loaded normally). This is the
  approach the test below uses.

## Two confirmed constraints on custom payloads

Both of these were discovered live, during the [co-op chat](coop-chat) 2-player test, not predicted from
source. Anyone hijacking a `NetEventCallback` for their own data needs to know both.

**The event ID gets masked to a small numeric range.** The first live test sent `nEventId = 100` and the
receiving machine's `NetEventCallback` fired with `nEventType` reported as `4`. That's not corruption —
`100 mod 8 = 4` (and also `mod 16` and `mod 32`, so the exact bit width isn't pinned down by this one data
point, only somewhere between 3 and 5 bits). `MrxFactionManager` only ever ships IDs `0`, `1`, `2` in the
decompiled source, consistent with nobody needing more than a couple of bits for this module. **Safe
guidance: keep custom event IDs below 8**, and pick one that doesn't collide with the target module's own
real IDs (check the catalog below).

**String arguments do not survive as text.** Passing a Lua string in `tArgs` (a sender name via
`Net.GetHostName()`, a chat message, anything) arrives on the other machine as an opaque lightuserdata
handle — visible as `userdata: 89C0BD32` if you `tostring()` it, not the original text. This isn't a bug in
any particular script, it's the actual wire format: the decompiled source already shows this everywhere a
string crosses `SendCustomEvent` — `mrxfactionmanager.lua`'s own `NetEventCallback` receives a
`uStringHash` for `NETEVENT_SETMUTABLE` and recovers the original faction abbreviation only by iterating
every abbreviation *it already knows locally* and checking `String.GetHash(sFactionAbbrev) == uStringHash`
until one matches (same pattern in `mrxbriefing.lua`). There is no reverse function from handle back to
arbitrary text — every string ever sent this way in the shipped game is from a small closed set the
receiver already knows in advance (faction codes, achievement names, music-state names), never free text.
**Numbers don't have this problem** — `uGuid`s, player indices, and quantity counts all cross intact and
get used directly by the receiving side. Anything that needs to carry arbitrary text (like a chat message)
has to be encoded as numbers — see [the co-op chat page](coop-chat#send) for the actual encoding used.

## A concrete test: ping-pong via a hijacked `NetEventCallback`

Two small scripts, meant to be dropped onto **both players'** machines identically. One overrides
`MrxFactionManager`'s callback to also handle two new event IDs it never uses natively (its own real ones
are `0`, `1`, `2` — see the catalog below, and IDs must stay below 8 per the masking constraint above); the
other is a hotkey that kicks off the exchange. If this works, a single keypress from either player should
produce a log line on **both** machines: the sender logs "sent PING," the other player logs "received
PING ... sending PONG back," and the original sender then logs "received PONG ... round trip complete" — a
full, observable round trip confirming the override fired, the event actually crossed the network, and the
reply made it back.

`scripts/OnLoad/NetEventPingPongSetup.lua`:

```lua
import("MrxFactionManager")

local NETEVENT_PING = 3  -- avoids MrxFactionManager's own real IDs (0, 1, 2); stays below the ~8 ceiling
local NETEVENT_PONG = 4

if not MrxFactionManager._bPingPongHijacked then
  MrxFactionManager._bPingPongHijacked = true
  local fOriginalCallback = MrxFactionManager.NetEventCallback  -- preserve the real behavior

  MrxFactionManager.NetEventCallback = function(nEventType, tArgs)
    if nEventType == NETEVENT_PING then
      Loader.Printf("PINGPONG: received PING -- sending PONG back")
      Net.SendCustomEvent("MrxFactionManager", NETEVENT_PONG, {}, true)
    elseif nEventType == NETEVENT_PONG then
      Loader.Printf("PINGPONG: received PONG -- round trip complete!")
    else
      fOriginalCallback(nEventType, tArgs)  -- not our event, let the module handle it normally
    end
  end
end

Loader.Printf("PINGPONG: MrxFactionManager.NetEventCallback overridden, ready to test")
```

`scripts/OnKey/NetEventPing.lua`:

```lua
local KEYVAL = "f6"  -- must be in the first 10 lines

Net.SendCustomEvent("MrxFactionManager", 3, {}, true)
Loader.Printf("PINGPONG: sent PING")
```

**How to run it**: both players load into the same co-op session with both scripts present, then either
player presses `f6`. No sender-identity tag is sent (dropping the earlier `Net.GetHostName()` label
deliberately — per the constraints above, that string would arrive as an unreadable userdata handle
anyway, and with only 2 players in co-op, receiving the event already tells you who it's from). The
`_bPingPongHijacked` guard exists because `OnLoad` scripts re-run on every level load — without it, loading
a second level would wrap the callback in another layer each time.

This exact pattern (hijack `MrxFactionManager`, IDs below 8, no string payloads) is confirmed live via the
[co-op chat feature](coop-chat), which uses the identical mechanism with a real chat message instead of a
ping/pong tag. `SendCustomEvent` is confirmed symmetric — both directions were exercised in that same test,
not just one player triggering it. Still genuinely open: whether the override survives a level load
mid-session on both ends (the guard above defends against it, but that specific scenario — reload after the
hijack is already installed — hasn't been separately exercised yet).

## The full `NETEVENT_` catalog

Every `NETEVENT_*` constant found in the decompiled corpus, grouped by the module that owns it. **Read
the caveat below the table before using any of these** — they are not a single shared ID space. Note this
isn't necessarily every custom-event constant in the game — `resident/mrxachievements.lua` uses the same
`SendCustomEvent`/`NetEventCallback` mechanism with a differently-prefixed constant
(`EVENT_GRANTACHIEVEMENT`, no `NETEVENT_`), so other naming conventions may exist uncounted here; this
table is scoped to the `NETEVENT_` prefix specifically.

| Module (`sModuleName` in `SendCustomEvent`) | Source file | Event constants |
|---|---|---|
| `AllCon002` | `vz/allcon002.lua` | `STARTEMITTERS=0`, `STARTPLUMES=1`, `CLEANSMOKE=2`, `AIRSTRUCK=3` |
| `Alarm` | `resident/alarm.lua` | `ALARMACTIVATE=0`, `ALARMDEACTIVATE=1` |
| `MrxMusic` | `resident/mrxmusic.lua`, `shell/mrxmusic.lua` | `ENTERFREEPLAY=0`, `ENTERCONTRACT=1`, `PLAYSPECIALMUSIC=2`, `STOPSPECIALMUSIC=3` |
| `DanceRadio` | `resident/danceradio.lua` | `STARTDANCING=0` |
| `JetCon001` | `vz/jetcon001.lua` | `SETBBQTY=0` |
| `MecCon001` | `vz/meccon001.lua` | `ENTERVEHICLE=0`, `SPAWNEXPLOSION=5`, `SHOWTUT=10`, `HIDETUT=11`, `CLIENTTUTCOMPLETE=12` |
| `OilCon002` | `vz/oilcon002.lua` | `STARTHACK=0`, `STOPHACK=1`, `MOVE_LUCKY_LADY=2` |
| `OilCon020` | `vz/oilcon020.lua` | `CLIENTSETUP=0`, `CLIENTSETUP2=1` |
| `OilCon021` | `vz/oilcon021.lua` | `CLIENTSETUP=0` |
| `PirCon004` | `vz/pircon004.lua` | `CLIENTDIAGSHOW=0`, `CLIENTDIAGSELECT=1` |
| `PmcCon001` | `vz/pmccon001.lua` | `SETSTARTUPWEAPONS=0`, `MOVECOLLISION=1` |
| `moonpatrol` | `resident/moonpatrol.lua` | `STARTEMITTERS=0`, `STOPEMITTERS=1` |
| `PmcCon004` | `vz/pmccon004.lua` | `HIJACKSOLANO=0`, `ARTILLERYATTACK=1`, `KILLBRIDGE=2`, `CHANGEATMOSPHERE=3` |
| `PmcCon018` | `vz/pmccon018.lua` | `SETSTARTUPWEAPONS=0`, `RETURNWEAPONS=1` |
| `PmcCon031` | `vz/pmccon031.lua` | `SETSTARTUPWEAPONS=0`, `RETURNWEAPONS=1` |
| `PmcCon032` | `vz/pmccon032.lua` | `SETSTARTUPWEAPONS=0`, `RETURNWEAPONS=1` |
| `PmcCon033` | `vz/pmccon033.lua` | `SETSTARTUPWEAPONS=0`, `RETURNWEAPONS=1`, `TARGETSDOWN=2`, `TARGETSUP=3` |
| `PmcCon034` | `vz/pmccon034.lua` | `SETSTARTUPWEAPONS=0`, `RETURNWEAPONS=1` |
| `MrxBriefing` | `resident/mrxbriefing.lua` | `ENABLEMARKERS=0`, `DISABLEMARKERS=1`, `DISPLAYMENU=2`, `HIDEMENU=3` |
| `VzaCon001` | `vz/vzacon001.lua` | `CLIENTSETUP=0` |
| `MrxFactionManager` | `resident/mrxfactionmanager.lua` | `SETMUTABLE=0`, `CIVKILLINIT=1`, `CIVKILL=2` |
| `WifMissionFlow` | `vz/wifmissionflow.lua` | `CLIENTCREDITS=0` |
| [`WifPmcInterior`](../vz/wifpmcinterior) | `vz/wifpmcinterior.lua` | `UPDATESTOCKPILE=0`, `CHANGEOUTFIT=1`, `NOTIFYOUTFITCHANGE=2` |
| `MrxGuiPda` | `resident/mrxguipda.lua` | `SETSELECTEDMISSION=0`, `PDAOPEN=1`, `PDACLOSE=2` |
| `MrxMissionFlow` | `resident/mrxmissionflow.lua` | `SETGRAPPLE=0`, `AUTOSAVE=1`, `SETVEHICLEDISGUISE=2` |
| `MrxOilCon002Delivery` | `resident/mrxoilcon002delivery.lua` | `SETDELIVERYLOCATIONS=0` |
| `MrxPlayer` | `resident/mrxplayer.lua` | `CLIENTSELECTMEDEVAC=0`, `CLIENTDONESTREAMING=1`, `HOST_SELECT_MEDEVAC=2`, `CLIENTKILL=3`, `CLIENT_OUT_BOUNDARY_DEATH=4` |
| `MrxSupportData` | `resident/mrxsupportdata.lua` | `ADDFREEBIE=0`, `REMOVEFREEBIE=1` |
| `MrxSupportDesignatorSmoke` | `resident/mrxsupportdesignatorsmoke.lua` | `SMOKEACTIVATE=0` |
| `MrxSupportManager` | `resident/mrxsupportmanager.lua` | `RECRUITSTATE=0`, `STARTTIMER=1` |
| `MrxSupportTransit` | `resident/mrxsupporttransit.lua` | `ENTERVEHICLE=0`, `EXITVEHICLE=1`, `SHOWMESSAGE=2`, `CLEARMESSAGE=3` |
| `MrxTaskContract` | `resident/mrxtaskcontract.lua` | `CLIENTPAUSE=0` |
| `MrxTaskObjectiveDeliver` | `resident/mrxtaskobjectivedeliver.lua` | `EXITVEHICLE=0`, `UNWINCH=1`, `CLEARTUTORIAL=5` |
| `MrxTaskObjectiveVerify` | `resident/mrxtaskobjectiveverify.lua` | `VERIFY=0` |
| `MrxTaskRace` | `resident/mrxtaskrace.lua` | `MARKLOC=0`, `UNMARKLOC=1`, `MARKFINISH=2` |
| `MrxTransit` | `resident/mrxtransit.lua` | `CLIENTTRANSIT=0`, `STARTTRANSIT=1` |
| `Munitions` | `resident/munitions.lua` | `SETTAGGABLE=0`, `CLIENTSTOCKPILEQUERY=1`, `CLIENTSTOCKPILEACK=2`, `PICKUP=3`, `MARKERPULSE=4`, `ISMUNITIONTAGGED=5` |
| `Outpost` | `resident/outpost.lua` | `UPDATEHEALTHDISPLAY=0`, `CLEARHEALTHDISPLAY=1` |
| `SpyHunter` | `resident/spyhunter.lua` | `STARTEMITTERS=0`, `STOPEMITTERS=1`, `STARTEMITTERSMOKE=2`, `STOPEMITTERSMOKE=3` |

**Important caveat**: every constant above is declared **without `local`** in its source file (e.g.
`NETEVENT_STARTEMITTERS = 0`, not `local NETEVENT_STARTEMITTERS = 0`), which makes them real Lua
globals — but every module reuses the same small integers (`0`, `1`, `2`...) for completely different
meanings, and the *name itself* isn't unique either (three separate modules all define
`NETEVENT_STARTEMITTERS`). If two of these modules are loaded at once, whichever loaded last silently
wins that global name — a real footgun if you ever reference `NETEVENT_X` by name from your own script
rather than passing the literal number directly. These are not a coordinated ID space; they're
per-module-private integers whose meaning only makes sense paired with the specific module name string
you're sending to.

## Status: confirmed vs still open

**Confirmed live** (via the co-op chat 2-player test):
- A hijacked module's `NetEventCallback` really fires on the *other* player's machine — dispatch crosses
  the network, it's not just a local reassignment.
- `SendCustomEvent` is genuinely symmetric — both host→client and client→host were exercised, not just one
  direction.
- The event ID is masked to a small range (safe below 8) and string arguments arrive as unusable opaque
  handles, not text — both covered in detail above.

**Still open**:
- **Whether the override survives a level load *after* it's already installed.** The guard pattern shown
  above (`if not Module._bXHijacked then`) defends against double-wrapping if `OnLoad` re-runs, but nobody
  has yet tested loading a second level mid-session with the hijack already active and confirmed it still
  answers correctly.
- **The real maximum size of `tArgs` per call.** The largest example anywhere in the decompiled corpus is
  5 elements (`wifpmcinterior.lua`'s stockpile sync); whether that's an actual engine-enforced cap or just
  the largest the shipped game happened to need is unconfirmed. Relevant if you need to send more data than
  fits in a handful of numbers per event — see the [co-op chat page](coop-chat) for where this matters in
  practice. Both [`coopchat.lua`](../uilib/coopchat) and [ModNet](../modnet) now operate on exactly this
  ceiling (`SLOTS = 5`) — real, working code depending on the number, without resolving whether it's a hard
  engine limit or just never tested past.
- **The actual network wire protocol is still invisible to us.** Everything past the Lua call boundary is
  compiled native code — rate limits and behavior under packet loss (even with `bReliable = true`) remain
  unknowable from source alone.
