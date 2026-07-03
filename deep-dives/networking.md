---
title: "Networking: A Lua-Only Restoration?"
parent: Deep Dives
nav_order: 3
---

# Deep Dive: Is a Lua-Only Multiplayer Restoration Possible?

**This page is different from the other Deep Dives — everything on it is speculative.** The freecam and
function-override writeups document techniques that were built and live-tested in-game. Nothing here has
been. This is a source-reading investigation into what the `Net` namespace exposes and what might be
possible with it, written up because the findings are concrete and interesting enough to be worth
recording — but every claim below is "the source says this is callable," not "this was confirmed to
work." Live testing (ideally two machines/instances on a LAN) is the obvious next step, not yet done.

## The question

Mercenaries 2's online multiplayer depended on a matchmaking backend that's almost certainly long dead —
this is a ~2008 release. The question worth asking from a modding angle: does the Lua layer expose enough
of the underlying networking primitives that a script could route around the dead matchmaking service
entirely, rather than needing it?

## Three distinct connection paths, not one

Reading every real call site of the connection-related `Net.*` functions across the whole decompiled
corpus turns up three architecturally separate systems, all living under the same `Net` namespace:

**LAN/local lobby** — `Net.EnterLobby()`. The game's own debug logging calls this out explicitly:
`Debug.Printf("Entered lan lobby")` runs immediately after the call, in `resident/mrxguishell.lua`. This
is the path most likely to still work today, since it doesn't depend on any external service at all —
just local network discovery.

**Friends lobby** — `Net.EnterFriendsLobby()`, a separate function entirely, almost certainly backed by a
platform-level friends/identity service (Xbox Live-style, going by the naming and surrounding code). This
is the path most likely to be permanently dead, since it needs an external identity backend, not just a
network transport.

**Internet matchmaking** — `Net.ConnectToServer(sServerName, "online")` — note the literal string
`"online"` as the second argument, distinct from the other calling conventions below. Every real call
site is guarded by `Net.IsMatchmakingInternet()`. This is the piece almost certainly tied to a defunct
GameSpy-era matchmaking backend.

## The most important finding: direct IP connect is real

`Net.ConnectToServer` takes a **raw IP address string** as its second argument in its most common real
usage:

```lua
local bSuccess = Net.ConnectToServer(tData.sName, tData.sIPAddress)
```

`tData.sIPAddress` is read directly off a discovered-server entry (`resident/mrxguishell.lua:685`,
confirmed via `Debug.Printf("joinGame info: " .. tData.sName .. tData.sIPAddress)` printing it right
before the call). The same function is also called with an empty string (`""`, for friends-lobby joins,
where presumably the platform layer resolves the connection some other way) and with the literal string
`"online"` (for matchmaking joins) — three different calling conventions on one function, selected by
what the second argument actually is.

**What this means**: if `sIPAddress` is a genuine dotted-quad string in the confirmed case, there's no
apparent reason a script couldn't construct that same call directly —
`Net.ConnectToServer("SomeName", "192.168.1.50")` — without ever going through the lobby UI, the LAN
discovery system, or the (dead) matchmaking service at all. This is the single most promising lead on
this whole page, and also the easiest to test directly.

## Hosting: the one real open question

```lua
if Net.IsMatchmakingInternet() and Net.IsPlatformConnected() then
  Net.StartServer(Net.GetHostName(), Sys.GetLevelName(), Sys.GetMasterScriptName())
else
  Sys.StartSingleplayer(sLevelName, sMasterScript)
end
```

Every real call site of `Net.StartServer` in the entire corpus — three of them, all near-identical — is
gated behind this exact same check. There is no confirmed example anywhere in source of `StartServer`
being called *without* that gate. That leaves a genuine unknown, and it's the crux of the whole question:
is `IsMatchmakingInternet()`/`IsPlatformConnected()` just how *this particular menu flow* happens to be
wired, with the underlying native `StartServer` perfectly able to host a LAN-only game if called
directly — or does the native implementation itself refuse to function without a live matchmaking
handshake, regardless of how it's invoked from Lua? **This cannot be answered from decompiled Lua source
alone** — the actual network protocol is compiled, native code, invisible to us. It needs a live test:
call `Net.StartServer(...)` directly from a script, skipping the `IsMatchmakingInternet()` check
entirely, and see what happens.

## How discovered servers reach Lua at all

Worth understanding before trying any of this: `resident/mrxguishell.lua` defines
`HandleServerAdd(oWidget, tEvent)`, `HandleServerUpdate(oWidget, tEvent)`, and
`HandleServerRemove(oWidget, tEvent)` — but **there is no `SetEventHandler` call anywhere in the corpus
registering them**. Every other widget event in this wiki (`"OpenShell"`, `"CloseShell"`, etc.) is
explicitly wired with `oWidget:SetEventHandler("EventName", handlerFunction)`. These three aren't. The
only explanation that fits: the engine's native networking layer calls these global functions directly,
by exact name, whenever it discovers/updates/loses a server — the same "callback by naming convention"
pattern used elsewhere in this codebase for `Awake`/`OnActivate` on world objects (see the
[Resident Modules](../resident/) landing page). Lua doesn't drive discovery here; it only reacts to
results the native layer hands it. `tEvent` carries `uKey` (an opaque server handle), `sName`, `nStatus`,
`sMap`, `sContract`, `bFriendlyFire` — notably, **not `sIPAddress`** in the fields actually copied by
`HandleServerAdd`, which raises its own question about how `tData.sIPAddress` gets onto entries that
`_JoinGameFlashCallback` later reads. Not resolved by anything found in this pass.

## `Net.SendCustomEvent` and `NetEventCallback` — a second instance of the same pattern

Completely separate from server discovery, there's a second native-dispatch-by-convention mechanism
already confirmed on the [Net namespace page](../namespaces/net#sendcustomevent-general-purpose-mission-sync):
`Net.SendCustomEvent`.

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

Again: no explicit registration call anywhere. `NetEventCallback` is just a global function name the
engine looks up and calls, keyed by the `sModuleName` string passed into `SendCustomEvent`. Every
`resident/`/`vz/` module that wants to sync something across a co-op session defines its own
`NetEventCallback` and its own small set of numeric event IDs, entirely independently of every other
module's.

**This is the second-most-interesting lead here.** If dispatch really is just "look up a global function
named `NetEventCallback` belonging to the module named by this string," there's no obvious reason custom
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

### A concrete test: ping-pong via a hijacked `NetEventCallback`

Two small scripts, meant to be dropped onto **both players'** machines identically. One overrides
`Alarm`'s callback to also handle two new event IDs `Alarm` itself never uses (its own real ones are `0`
and `1` — see the catalog below); the other is a hotkey that kicks off the exchange. If this works, a
single keypress from either player should produce a log line on **both** machines: the sender logs
"sent PING," the other player logs "received PING ... sending PONG back," and the original sender then
logs "received PONG ... round trip complete" — a full, observable round trip confirming the override
fired, the event actually crossed the network, and the reply made it back.

`scripts/OnLoad/NetEventPingPongSetup.lua`:

```lua
import("Alarm")

local NETEVENT_PING = 100  -- picked to avoid Alarm's own real IDs (0, 1)
local NETEVENT_PONG = 101

local fOriginalCallback = Alarm.NetEventCallback  -- preserve Alarm's real behavior

Alarm.NetEventCallback = function(nEventType, tArgs)
  if nEventType == NETEVENT_PING then
    Loader.Printf("PINGPONG: received PING from " .. tostring(tArgs[1]) .. " -- sending PONG back")
    Net.SendCustomEvent("Alarm", NETEVENT_PONG, {Net.GetHostName()}, true)
  elseif nEventType == NETEVENT_PONG then
    Loader.Printf("PINGPONG: received PONG from " .. tostring(tArgs[1]) .. " -- round trip complete!")
  else
    fOriginalCallback(nEventType, tArgs)  -- not our event, let Alarm handle it normally
  end
end

Loader.Printf("PINGPONG: Alarm.NetEventCallback overridden, ready to test")
```

`scripts/OnKey/NetEventPing.lua`:

```lua
local KEYVAL = "f6"  -- must be in the first 10 lines

Net.SendCustomEvent("Alarm", 100, {Net.GetHostName()}, true)
Loader.Printf("PINGPONG: sent PING")
```

**How to run it**: both players load into the same co-op session with both scripts present, then either
player presses `f6`. `Net.GetHostName()` is used purely as a "who sent this" tag in the log output — its
exact return value hasn't been independently confirmed beyond its real use as an argument to
`Net.StartServer`, so treat it as a label, not something to depend on. This is untested end to end; the
event IDs (`100`/`101`), the assumption that `SendCustomEvent` is symmetric (not host-only — one
suggestive data point in `alarm.lua` itself: nothing gates its own `SendCustomEvent` call behind
`Net.IsServer()`, only the decision of *when* to send does), and whether the override even survives
across a level load on both ends, are all things this test is specifically designed to surface, not
assumptions it relies on.

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
| `WifPmcInterior` | `vz/wifpmcinterior.lua` | `UPDATESTOCKPILE=0`, `CHANGEOUTFIT=1`, `NOTIFYOUTFITCHANGE=2` |
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

## What a live test would actually need to check

In rough priority order:

1. **Direct IP connect**: `Net.ConnectToServer("Test", "<LAN IP of a second instance>")` from one machine,
   with the second machine having called `Net.StartServer(...)` (bypassing the `IsMatchmakingInternet()`
   gate entirely) — does a connection actually establish?
2. **Custom `NetEventCallback`**: the ping-pong test above — confirm a hijacked callback actually fires on
   the *other* player's machine, not just locally.
3. **What `IsPlatformConnected()`/`IsOnlineEnabled()` actually return** with no matchmaking backend
   reachable — do they fail gracefully (return `false`), or does calling networking functions while
   they're `false` error out / hang?

## Known limitations of this whole page

- **Nothing here is live-tested.** Every claim is "the source supports this reading," not "this was
  confirmed to work." Treat this page as a research starting point, not a working guide.
- **The actual network wire protocol is invisible to us.** Everything past the Lua call boundary is
  compiled native code. Lua can call `Net.StartServer`/`Net.ConnectToServer`; whether the underlying
  implementation still functions without whatever backend it originally talked to is fundamentally
  unknowable from source alone.
- **`sIPAddress`'s origin on a discovered-server entry is unresolved** — `HandleServerAdd` doesn't
  visibly copy it from the native `tEvent`, yet code elsewhere reads it. Either it's set somewhere not
  found in this pass, or there's a real gap in this analysis.
- **Friends lobby is almost certainly the deadest of the three paths**, being the most tightly coupled to
  an external identity service — not a promising restoration target even if the LAN/direct-IP path turns
  out to work.
