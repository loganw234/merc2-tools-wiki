---

title: MrxFactionManager

parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [faction, relation, attitude]

verified: true
verified_note: "deeper pass: corrected Imports (None -> MrxUtil/MrxPmc/MrxGui/MrxSupport/MrxAchievements/MrxVoSequence/MrxTutorialManager/WifMissionFlow), surfaced the exact attitude thresholds/price-scales/RGB from _tAttitudes and the relation/meter ranges, rewrote Events (real subs are Event.ScriptEvent mpPlayerJoin + Event.ObjectDeath civ&&human + TimerRelative flybys; posts Attitude/CollateralDamage/HeroReported — no ObjectHibernation/PlayerJoined here); faction catalog + SetRelation gotcha re-confirmed"

---



# MrxFactionManager



*Module: mrxfactionmanager.lua*



## Overview

The `MrxFactionManager` module is responsible for managing faction relations, attitudes, and reporting systems within the game. It handles various aspects such as setting up faction templates, managing mutable attitudes, tracking civilian casualties, and coordinating flybys. This module ensures that factions have appropriate relations with each other and with the player, affecting gameplay dynamics and interactions.

**Confirmed always-resident, and the safe hijack target for custom networked events.** Unlike per-object
world scripts (e.g. [`Alarm`](alarm)), `import("MrxFactionManager")` works from anywhere, any time — no
level-specific object needs to exist first. That's exactly why it's the module both the
[networking deep dive](../deep-dives/networking) and [co-op chat feature](../deep-dives/coop-chat) hijack
`NetEventCallback` on to send their own custom data: it's guaranteed loaded, and confirmed by live testing
to actually dispatch a hijacked callback across a real 2-player network connection.



## Inheritance

- Inherits from: none — base/utility module
- Imports: [`MrxUtil`](mrxutil), [`MrxPmc`](mrxpmc), [`MrxGui`](mrxgui), [`MrxSupport`](mrxsupport),
  [`MrxAchievements`](mrxachievements), [`MrxVoSequence`](mrxvosequence),
  [`MrxTutorialManager`](mrxtutorialmanager), `WifMissionFlow` (an earlier draft said "None" — the source has
  all eight `import()` lines).



## Instance pattern

Stateless manager module — no `Create`/`uGuid` pattern. Module-level tables hold shared, global state
instead of per-object instances:

- `_tEvents`: Stores event handles for various faction-related events.
- `_tInvestigatorBlips`: Likely stores investigator blip data.
- `_tTressPassGeneric`: Contains generic trespassing zone identifiers.
- `_tAttitudes`: Defines different attitude levels with their ranges, price scales, and RGB colors.
- `_tFactions`: Maps faction abbreviations to faction data — see the live-captured catalog below.
- `_bSetupComplete`: Indicates if the setup is complete.
- `_bVoPlayed`: Likely indicates if a voice-over has been played.
- `bReportingDisabled`: A boolean flag indicating whether reporting is disabled.
- `bActiveReporter`: A variable that holds the active reporter's GUID, if any.
- `tFlybys`: A nested table defining various flyby configurations for different factions.

## Faction catalog

**Captured by live runtime dump** — see [Snippets](../snippets) for the general table-dumping approach.
All 8 factions that exist in `_tFactions`:

| Abbrev | Template | PDA ID | Dynamic | Can report | Max-relation achievement |
|---|---|---|---|---|---|
| `All` | Allied | AN | true | true | `ACHIEVEMENT_STAND_UP_AND_SHOUT` |
| `Chi` | China | CH | true | true | `ACHIEVEMENT_LONGING_FOR_FIRE` |
| `Civ` | Civ | — | false | — | — |
| `Gur` | Guerilla | GR | true | true | `ACHIEVEMENT_FOREVER_FREE` |
| `Oil` | OC | OC | true | true | `ACHIEVEMENT_DIRTY_DEEDS` |
| `Pir` | Pirate | PR | true | true | `ACHIEVEMENT_ISLAND_DOMINATION` |
| `Pmc` | PMC | PMC | false | — | — |
| `Vza` | VZ | VZ | false | — | — |

`Civ`, `Pmc`, and `Vza` are the three **non-dynamic** factions — `bDynamic` (a static, source-level flag,
not the runtime `bAttitudeMutable` flag) is `false` for all three, meaning
[`SetAttitudeMutable`](#setattitudemutable-sabbrev-brestorefromsave) can never turn on relation-tracking
for them at all, by design — see the [`MrxCheatBootstrap`](mrxcheatbootstrap) page's `SetRelation`
caveat for the full mechanism this gates. `Pmc` is presumably excluded because it's the player's own
faction; `Civ`/`Vza` (civilians/the setting's neutral wildlife-adjacent faction) apparently aren't meant
to have a trackable attitude at all.

## Attitude thresholds, ranges & price scales

The core relation model lives in three module constants plus the `_tAttitudes` table:

| Constant | Value | Meaning |
|---|---|---|
| `_knRelationMin` / `_knRelationMax` | `-100` / `100` | The raw relation scale `Ai.GetRelation`/`Ai.SetRelation` operate on. |
| `_knAttitudeMeterMin` / `_knAttitudeMeterMax` | `0` / `100` | HUD meter scale; `ConvertRelationToMeterValue` linearly maps `[-100,100] → [0,100]`. |

`_tAttitudes` (order = attitude level 1→3) defines the bands, shop price scale, and blip color:

| Level | Label | Relation range | Price scale (`nPrices`) | RGB |
|---|---|---|---|---|
| 1 | `Hostile` | `[-100, -33)` | `nil` (won't sell) | 255,0,0 (red) |
| 2 | `Neutral` | `[-33, 33)` | `1.5` | 200,200,200 (grey) |
| 3 | `Friendly` | `[33, 100]` | `1.0` | 0,127,255 (blue) |

So the `>= 33` relation is the "Friendly" cutoff, `< -33` is "Hostile", and the shop charges 1.5× at Neutral
vs 1.0× at Friendly (via [`GetPriceScale`](#getpricescale-ssubjectabbrev-sobjectabbrev), which is what
[`MrxShop._GetPriceScale`](mrxshop) calls). Editing these ranges/prices re-tunes the whole reputation economy.

## Functions



### Init()

Initializes attitude level mappings and faction template to abbreviation mappings. It populates `_tAttitudeLevelsToLabels` and `_tAttitudeLabelsToLevels` based on `_tAttitudes`, and assigns unique GUIDs to each faction in `_tFactions`.



### Reset()

Resets the report system by initializing it with default parameters.



### Setup()

Sets up the report system, initializes pursuit level times, and configures various aspects of faction management. It also sets up next flybys, achievements, disguise handling, faction zone handling, and HUD faction display thresholds. It ensures that each faction has a maximum relation with itself.



### SendPlayerJoinEvents()

Sends network events to synchronize mutable factions and civilian casualties when a player joins the game.



### GetFactionStringIndex(uStringHash)

Retrieves the faction abbreviation based on a string hash. Returns "NO NAME" if no matching faction is found.



### NetEventCallback(eventId, tArgs)

Handles network events related to faction management. It processes mutable factions and civilian casualties based on the event ID. Real event IDs: `NETEVENT_SETMUTABLE=0`, `NETEVENT_CIVKILLINIT=1`,
`NETEVENT_CIVKILL=2` — see the [full `NETEVENT_` catalog](../deep-dives/networking#the-full-netevent_-catalog).

**If you hijack this callback for your own custom event, confirmed by live testing: keep your event ID
below 8.** The transport masks `nEventId` down to a small numeric range (observed: `100` arrived as `4`) —
see [Custom Networked Events](../deep-dives/networking#two-confirmed-constraints-on-custom-payloads) for
the full story, including the same live test's other discovery: string arguments in `tArgs` arrive as
unusable opaque handles, not their original text, so custom payloads have to be encoded as numbers.



### NetInitializeClientFactionRelations(nNext)

Initializes client-side faction relations in a staggered manner to avoid performance issues.



### SetAttitudeMutable(sAbbrev, bRestoreFromSave)

Sets a faction's attitude as mutable, adds it to the HUD meter, and initializes its relation with PMC. It also sends a network event if the change is made on the server.

**Confirmed working by live testing** — see [`MrxCheatBootstrap`](mrxcheatbootstrap)'s `SetRelation`
caveat for the full worked example (this is the fix for `SetRelation`'s silent no-op on
non-mutable factions).



### IsAttitudeMutable(sAbbrev)

Checks if a faction's attitude is mutable by returning the boolean value stored in `_tFactions`.



### CanAttitudeBeMutable(sAbbrev)

- **Description**: Checks if the attitude of a faction with the given abbreviation (`sAbbrev`) can be dynamically changed.

- **Parameters**:

  - `sAbbrev` (string): The abbreviation of the faction.

- **Returns**: 

  - `boolean`: True if the attitude is mutable, false otherwise.



### GetRelation(sSubjectAbbrev, sObjectAbbrev)

- **Description**: Retrieves the relation value between two factions based on their abbreviations.

- **Parameters**:

  - `sSubjectAbbrev` (string): The abbreviation of the subject faction.

  - `sObjectAbbrev` (string): The abbreviation of the object faction.

- **Returns**: 

  - `number`: The relation value between the two factions.



### TestAttitude(sSubjectAbbrev, sObjectAbbrev, sComparison, sAttitude)

- **Description**: Tests if the attitude between two factions meets a specified comparison condition against a given attitude label.

- **Parameters**:

  - `sSubjectAbbrev` (string): The abbreviation of the subject faction.

  - `sObjectAbbrev` (string): The abbreviation of the object faction.

  - `sComparison` (string): The comparison operator (`"=="`, `"<"`, `"<="`, `">"`, `">="`).

  - `sAttitude` (string): The attitude label to compare against.

- **Returns**: 

  - `boolean`: True if the condition is met, false otherwise.



### GetAttitudeLevel(sSubjectAbbrev, sObjectAbbrev)

- **Description**: Retrieves the attitude level between two factions based on their abbreviations.

- **Parameters**:

  - `sSubjectAbbrev` (string): The abbreviation of the subject faction.

  - `sObjectAbbrev` (string): The abbreviation of the object faction.

- **Returns**: 

  - `number`: The attitude level between the two factions.



### GetAttitudeLabel(sSubjectAbbrev, sObjectAbbrev)

- **Description**: Retrieves the attitude label between two factions based on their abbreviations.

- **Parameters**:

  - `sSubjectAbbrev` (string): The abbreviation of the subject faction.

  - `sObjectAbbrev` (string): The abbreviation of the object faction.

- **Returns**: 

  - `string`: The attitude label between the two factions.



### GetMeterValue(sSubjectAbbrev, sObjectAbbrev)

- **Description**: Retrieves the meter value representing the attitude between two factions based on their abbreviations.

- **Parameters**:

  - `sSubjectAbbrev` (string): The abbreviation of the subject faction.

  - `sObjectAbbrev` (string): The abbreviation of the object faction.

- **Returns**: 

  - `number`: The meter value representing the attitude.



### GetPriceScale(sSubjectAbbrev, sObjectAbbrev)

- **Description**: Retrieves the price scale factor based on the attitude between two factions.

- **Parameters**:

  - `sSubjectAbbrev` (string): The abbreviation of the subject faction.

  - `sObjectAbbrev` (string): The abbreviation of the object faction.

- **Returns**: 

  - `number`: The price scale factor.



### SetRelation(sSubjectAbbrev, sObjectAbbrev, nRelation, bInitialize)

- **Description**: Sets the relation value between two factions and updates related UI elements and events.

- **Parameters**:

  - `sSubjectAbbrev` (string): The abbreviation of the subject faction.

  - `sObjectAbbrev` (string): The abbreviation of the object faction.

  - `nRelation` (number): The new relation value to set.

  - `bInitialize` (boolean): Whether to initialize related UI elements.

**Confirmed working by live testing** — with a real gotcha: silently no-ops toward `"Pmc"` if the
subject faction isn't currently mutable. Full explanation and the fix
(`SetAttitudeMutable` first) on [`MrxCheatBootstrap`](mrxcheatbootstrap).



### ChangeRelation(sSubjectAbbrev, sObjectAbbrev, nRelation)

- **Description**: Changes the relation value between two factions by a specified amount.

- **Parameters**:

  - `sSubjectAbbrev` (string): The abbreviation of the subject faction.

  - `sObjectAbbrev` (string): The abbreviation of the object faction.

  - `nRelation` (number): The amount to change the relation value.



### CreateAttitudeChangeEvent(tParams, fCallback, tCallbackData)

- **Description**: Creates a non-persistent attitude change event with specified parameters and callback.

- **Parameters**:

  - `tParams` (table): Parameters for the event.

  - `fCallback` (function): Callback function to be executed when the event occurs.

  - `tCallbackData` (table): Data to pass to the callback function.



### CreatePersistentAttitudeChangeEvent(tParams, fCallback, tCallbackData)

- **Description**: Creates a persistent attitude change event with specified parameters and callback.

- **Parameters**:

  - `tParams` (table): Parameters for the event.

  - `fCallback` (function): Callback function to be executed when the event occurs.

  - `tCallbackData` (table): Data to pass to the callback function.



### _CreateAttitudeChangeEvent(bPersistent, tParams, fCallback, tCallbackData)

- **Description**: Internal function to create an attitude change event, either persistent or non-persistent.

- **Parameters**:

  - `bPersistent` (boolean): Whether the event should be persistent.

  - `tParams` (table): Parameters for the event.

  - `fCallback` (function): Callback function to be executed when the event occurs.

  - `tCallbackData` (table): Data to pass to the callback function.



### ConvertRelationToMeterValue(nRelation)

- **Description**: Converts a relation value to a meter value representing attitude.

- **Parameters**:

  - `nRelation` (number): The relation value to convert.

- **Returns**: 

  - `number`: The converted meter value.



### ConvertRelationToAttitudeLevel(nRelation)

- **Description**: Converts a relation value to an attitude level based on defined ranges.

- **Parameters**:

  - `nRelation` (number): The relation value to convert.

- **Returns**: 

  - `number`: The corresponding attitude level.



### GetAttitudeFromLevel(nLevel)

- **Description**: Retrieves the attitude label from a given attitude level.

- **Parameters**:

  - `nLevel` (number): The attitude level.

- **Returns**: 

  - `string`: The corresponding attitude label.



### GetFactionAbbrevs()

- **Description**: Retrieves a sorted list of all faction abbreviations.

- **Returns**: 

  - `table`: A table containing the sorted faction abbreviations.



### GetFactionAbbrev(sFactionTemplate)

- **Description**: Retrieves the abbreviation for a given faction template.

- **Parameters**:

  - `sFactionTemplate` (string): The faction template name.

- **Returns**: 

  - `string`: The corresponding faction abbreviation.



### GetFactionAbbrevFromFactionGuid(sFactionGuid)

- **Description**: Retrieves the abbreviation for a faction based on its GUID.

- **Parameters**:

  - `sFactionGuid` (string): The GUID of the faction.

- **Returns**: 

  - `string`: The corresponding faction abbreviation.



### GetFactionTemplateName(sFactionAbbrev)

- **Description**: Retrieves the template name for a given faction abbreviation.

- **Parameters**:

  - `sFactionAbbrev` (string): The faction abbreviation.

- **Returns**: 

  - `string`: The corresponding faction template name.



### GetBribableFactions()

- **Description**: Retrieves a list of factions that can be bribed based on their attitude towards the PMC and mutability.

- **Returns**: 

  - `table`: A table containing the abbreviations of bribe-able factions.



### GetAttitudes()

- **Description**: Retrieves a table mapping attitude labels to their median values.

- **Returns**: 

  - `table`: A table where keys are attitude labels and values are their median values.



### GetAttitudeMedianValue(sLabel)

- **Description**: Retrieves the median value for a given attitude label.

- **Parameters**:

  - `sLabel` (string): The attitude label.

- **Returns**: 

  - `number`: The median value of the attitude.



### GetRgbColor(sSubjectAbbrev, sObjectAbbrev)

- **Description**: Retrieves the RGB color associated with the attitude between two factions.

- **Parameters**:

  - `sSubjectAbbrev` (string): The abbreviation of the subject faction.

  - `sObjectAbbrev` (string): The abbreviation of the object faction.

- **Returns**: 

  - `table`: A table containing the RGB color values.



### SaveSingleton()

- **Description**: Saves the current state of faction relations and mutable factions for persistence.

- **Returns**: 

  - `table`: A table containing saved data including relations, mutable factions, civilian casualties, and penalties.



### LoadSingleton(tSaveData)

- **Description**: Loads the saved state of faction relations and mutable factions from provided save data.

- **Parameters**:

  - `tSaveData` (table): The saved data to load.



### GetPlayerVisibleName(sAbbrev)

- **Description**: Retrieves the player-visible name for a given faction abbreviation.

- **Parameters**:

  - `sAbbrev` (string): The faction abbreviation.

- **Returns**: 

  - `string`: The player-visible name of the faction.



### GetShortPlayerVisibleName(sAbbrev)

- **Description**: Retrieves the short player-visible name for a given faction abbreviation.

- **Parameters**:

  - `sAbbrev` (string): The faction abbreviation.

- **Returns**: 

  - `string`: The short player-visible name of the faction.



### GetAdjective(sAbbrev)

- **Description**: Retrieves the adjective associated with a given faction abbreviation.

- **Parameters**:

  - `sAbbrev` (string): The faction abbreviation.

- **Returns**: 

  - `string`: The adjective for the faction.



### GetInlineIcon(sAbbrev)

- **Description**: Retrieves the inline icon texture for a given faction abbreviation.

- **Parameters**:

  - `sAbbrev` (string): The faction abbreviation.

- **Returns**: 

  - `string`: The inline icon texture name.



### GetMarkerTexture(sAbbrev)

- **Description**: Retrieves the marker texture for a given faction abbreviation.

- **Parameters**:

  - `sAbbrev` (string): The faction abbreviation.

- **Returns**: 

  - `string`: The marker texture name.



### CivCasualtySetup()

- **Description**: Sets up event handling for civilian casualties, initializing a persistent event to resolve civilian deaths.



### ResolveCivCasualty(uTarget, uCause, uKiller)

- **Description**: Resolves the consequences of a civilian death, including determining if it was caused by the player and charging penalties.

- **Parameters**:

  - `uTarget` (string): The GUID of the killed target.

  - `uCause` (string): The cause of death.

  - `uKiller` (string): The GUID of the killer.



### ChargeCivCasualty(uKiller)

- **Description**: Charges penalties for civilian casualties, updates player statistics, and triggers related events and voice cues.

- **Parameters**:

  - `uKiller` (string): The GUID of the killer.



### GetFactionStringAbbrev(uGuid, uAbbrev)

Retrieves the faction abbreviation string for a given GUID and optional hash. If `uAbbrev` is provided, it searches `_tFactions` for a matching hash; otherwise, it calls `GetFactionAbbrev(GetFaction(uGuid))`. Logs an error message if no faction abbrev is found.



### NetSafeRemoveReportingDisplay(uGuid, uAbbrev, bCancelTimer)

Safely removes the reporting display by calling `GetFactionStringAbbrev` to get the faction abbreviation and then invoking `RemoveReportingDisplay`.



### NetSafeHandleReporter0(uGuid, uAbbrev)

Handles reporter state 0 by getting the faction abbreviation and calling `HandleReporter0`.



### NetSafeHandleReporter1(uGuid, uAbbrev, bStartTimer)

Handles reporter state 1 by getting the faction abbreviation and calling `HandleReporter1`.



### NetSafeHandleReporter2(uGuid, uAbbrev)

Handles reporter state 2 by getting the faction abbreviation and calling `HandleReporter2`.



### NetSafeFinishedReporting(uGuid, uAbbrev)

Safely finishes reporting by getting the faction abbreviation and calling `FinishedReporting`.



### RemoveReportingDisplay(uGuid, sAbbrev, bCancelTimer)

Removes the reporting display for a given GUID and faction abbreviation. It removes markers, halts pulses, deletes minimap objectives, and cancels timers if specified.



### HandleReporter0(uGuid, sAbbrev, bDontSendMessage)

Handles reporter state 0 by setting up markers, radar objectives, and voice sequences based on the faction data. It also starts a timer if necessary and sends a network message if on the server.



### HandleInvestigator(uPlayerGuid, uInvestigatorGuid, state)

Placeholder function for handling investigators.



### HandleTressPasser(uTressPasserGuid, bTresspassing, uFactionGuid)

Handles tresspassers by playing voice-over messages and setting timers. It checks if a VO has already been played to avoid repetition.



### HandleReporter1(uGuid, sAbbrev, bStartTimer)

Handles reporter state 1 by checking for jamming conditions, starting timers, and playing voice sequences based on faction data. It also updates the network state if on the server.



### HandleReporter2(uGuid, sAbbrev)

Handles reporter state 2 by removing reporting displays, updating active reporters, and setting report delays. It also updates the network state if on the server.



### AmIBeingJammed(uGuid)

Checks if a given GUID is being jammed by comparing factions of drivers in vehicles with AA levels.



### HandleReporter(uGuid, state)

Handles different reporter states (0, 1, 2) by calling appropriate functions based on the current state.



### ValidateReporter(uGuid)

Validates a reporter by checking faction mutability, disabled reporters, and other conditions. Logs reasons for cancellation if validation fails.



### FinishedReporting(uGuid, sFactionAbbrev)

Handles the completion of reporting by adjusting relations, setting delays, incrementing pursuits if necessary, playing voice sequences, posting events, and updating network states.



### expand(a)

Expands a table by printing each entry's index and values. This function is defined twice in this part.



### SetReportDelay(nDelay)

Sets the report delay for various factions based on the provided delay value.



### GetFaction(uGuid)

Retrieves the faction label for a given GUID from a predefined list of factions. Logs an error if no faction label is found.



### GetPerceivedFaction(uGuid)

Gets the perceived faction by checking if the object is disguised and retrieving the faction accordingly.



### DisableReporter(uGuid)

Disables a reporter by setting its GUID in `tDisabledReporters` and handling active reporters.



### EnableReporter(uGuid)

Enables a reporter by removing its GUID from `tDisabledReporters`.



### DisableReporting(bDisable)

Disables or enables reporting based on the input boolean `bDisable`. If reporting is disabled, it logs "Reporting DISABLED" and handles any active reporter. If enabled, it logs "Reporting ENABLED" and sets the delay for faction templates that can report.



### SetFactionReporting(sFaction, bDisable)

Sets the reporting status for a specific faction (`sFaction`). Logs whether the faction was found and updates its `bCanReport` field in `_tFactions`.



### IncrementPursuit(sFactionAbbrev)

Increments the pursuit level for a given faction abbreviation. It retrieves the faction's GUID, adjusts the pursuit level to a maximum of 3, sets the pursuit duration, starts the pursuit on the HUD, and optionally plays a voice-over cue if available.



### LockPursuit(uGuid, nLevel)

Locks the pursuit for a specific faction identified by `uGuid` at a given `nLevel`. It updates the pursuit state in `Pg`, starts the pursuit display on the HUD, and hides any meters for factions.



### ClearPursuitLock()

Clears all pursuit locks. It hides meters for all factions and clears the pursuit lock in `Pg`.



### SetCustomPursuit(uFaction, nDuration, tSettings)

Sets a custom pursuit for a specific faction with a given duration and settings. It updates the pursuit state in `Pg`, starts the pursuit display on the HUD, and hides any meters for factions.



### ClearCustomPursuit()

Clears all custom pursuits. It hides meters for all factions and clears the custom pursuit in `Pg`.



### RandomFlyby()

Generates a random flyby based on faction configurations defined in `tFlybys`. It selects a random faction, template, and number of aircraft to spawn, calculates positions, and triggers the flyby using `Airstrike.Flyby`. It also sets up the next flyby timer.



### SetupNextFlyby()

Sets up a timer for the next random flyby. It creates an event that triggers `RandomFlyby` after a random interval between 19 and 90 seconds.



### GetPdaFactionIdFromFactionId(sFactionId)

Retrieves the PDA faction ID from a given faction ID by looking up `_tFactions`.



### GetFactionIdFromIndex(nIndex)

Retrieves the faction ID at a specific index in `_tFactions`.



### GetIndexFromFactionId(sFactionId)

Retrieves the index of a specific faction ID in `_tFactions`.



## Events

Real subscriptions (created in `Setup`/`CivCasualtySetup`):

- **`Event.CreatePersistent(Event.ScriptEvent, {"mpPlayerJoin", <filter>}, SendPlayerJoinEvents)`** — on the
  server, syncs mutable factions + civ-casualty counts to a joining remote player.
- **`Event.CreatePersistent(Event.ObjectDeath, {"civ && human"}, ResolveCivCasualty)`** — every civilian human
  death routes here; if the local player was the killer, `ChargeCivCasualty` applies the escalating penalty.
- **`Event.Create(Event.TimerRelative, {19 + Math.randi(71)}, RandomFlyby)`** — self-rescheduling ambient
  flyby timer (≈19–90 s), set up by `SetupNextFlyby`.
- `Event.TimerRelative` is also used as a retry/backoff in `NetEventCallback` and
  `NetInitializeClientFactionRelations` (waiting until `_bSetupComplete`).

Events this module **posts** (other modules subscribe): `Event.Post("Attitude", {subj, obj, oldLabel, newLabel})`
on any attitude-level change (the hook `CreateAttitudeChangeEvent`/`CreatePersistentAttitudeChangeEvent` filter
on, only for `obj == "Pmc"`); `Event.Post("CollateralDamage", {uKiller})`; `Event.Post("HeroReported", {template, uGuid})`.

{: .note }
> `CreateAttitudeChangeEvent`/`CreatePersistentAttitudeChangeEvent` subscribe to the `"Attitude"` script event
> above but silently return `nil` unless `tParams[2] == "Pmc"` — you can only watch attitude changes *toward the
> player faction* through these helpers.



## Notes for modders

- **Changing player reputation with a faction** goes through
  [`SetRelation`](#setrelation-ssubjectabbrev-sobjectabbrev-nrelation-binitialize) /
  [`ChangeRelation`](#changerelation-ssubjectabbrev-sobjectabbrev-nrelation) with `sObjectAbbrev == "Pmc"`. Both
  **silently no-op** if the subject faction isn't currently mutable — call
  [`SetAttitudeMutable(sAbbrev)`](#setattitudemutable-sabbrev-brestorefromsave) first. Only the five `bDynamic`
  factions (`All`/`Chi`/`Gur`/`Oil`/`Pir`) can be made mutable at all; `Civ`/`Pmc`/`Vza` never can. Full worked
  example: [`MrxCheatBootstrap`](mrxcheatbootstrap).
- **Rebalance the reputation economy** by editing the `_tAttitudes` bands/prices/colors and the `_knRelation*`
  ranges above — those are the "friendly at what number / how much does the shop overcharge / what color is the
  blip" knobs.
- **Ambient flybys**: `tFlybys` is 5 aircraft-set groups (Tucano / OV10 / Cessna+727 / a large "invasion" mix /
  Q5). `RandomFlyby` picks group 1–3 normally, +2 (→ groups 3–5) once `WifMissionFlow.HasKey("Invasion")`.
  Frequency is the `19 + Math.randi(71)` timer in `SetupNextFlyby`; `DisableReporting(true)` also suppresses
  flybys (`RandomFlyby` early-outs on `bReportingDisabled`).
- **Reporting/pursuit levers**: `DisableReporting(bDisable)` (global), `SetFactionReporting(sFaction, bValue)`
  (per-faction `bCanReport`), `DisableReporter`/`EnableReporter(uGuid)` (per-object). Civ-casualty penalty
  starts at `-5000`, doubles every 20 kills, floored at `-1000000`.

{: .warning }
> Source bug: `ValidateReporter` reads a local `sFaction` that is never assigned inside the function (it's
> `nil`), so its `sFaction ~= "Civ" and sFaction ~= "VZ"` sub-check is effectively always true. The `Civ`/`VZ`
> exclusion it looks like it intends doesn't work via that clause. Don't rely on `ValidateReporter` to filter
> those factions — they're kept out of reporting by `bDynamic`/`bCanReport` instead.

Decompiler artifacts to ignore: `function expand(a)` is defined twice (identical), and some literal tables have
duplicate keys (last wins).