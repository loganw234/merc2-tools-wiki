---
title: Event
parent: Engine Namespaces
nav_order: 3
---

# Event

## Overview

`Event` is an **engine namespace**: implemented natively by the game engine, not by any decompiled
`.lua` file in `resident/` or elsewhere. It's always available as a global table — no `import()`
required.

Unlike `Object` or `Vehicle`, most of `Event`'s ~48 entries are not functions. `pairs(Event)` shows
44 plain integer constants (event-type IDs, 0-43) and exactly 4 real functions: `Create`,
`CreatePersistent`, `Delete`, and `Post`.

The core pattern used throughout the decompiled scripts is:

```lua
local uHandle = Event.Create(Event.SomeEventType, {typeSpecificArgs}, callbackFunction, {callbackArgs})
```

`Event.Create` registers `callbackFunction` to run when an event of type `Event.SomeEventType`
occurs. The second argument (`{typeSpecificArgs}`) is a filter/parameter table whose shape depends
entirely on which event type you're registering for — e.g. `Event.ObjectDeath` wants `{targetGuid}`,
while `Event.ObjectProximity` wants `{guidA, guidB, "<", distance, bool, bool}`. There is no single
universal argument shape; see the per-type table below. The call returns a handle (a number/userdata)
that can later be passed to `Event.Delete(handle)` to unregister it.

`Event.Create(Event.TimerRelative, {2}, function() ... end, {})` — fire a callback once after a
delay — is **confirmed working by live testing**; see
[Snippets: React to an event instead of polling](../snippets#react-to-an-event-instead-of-polling)
for the tested example (reliable at 2s, 5s, and 20s delays, fires exactly once).

## Provenance

- The full list of 44 numeric IDs and the 4 function names comes from a live `pairs(Event)`
  enumeration in-game (ground truth for *what exists*).
- Which functions are real, and what argument shapes each event type expects, comes from grepping
  real call sites across the ~230 decompiled `.lua` files (ground truth for *how it's used*).
- Event types below are marked **Confirmed** when a real decompiled call site was found showing the
  argument shape, or **Name only** when the only evidence is the live enumeration (the name is
  presumably self-explanatory, but no call site was found to confirm the argument shape or exact
  trigger condition).

## The 4 core functions

| Function | Signature (observed) | Notes |
|---|---|---|
| `Event.Create` | `Event.Create(eventType, {args}, callback, {callbackArgs})` | Registers a one-shot-per-occurrence callback for `eventType`. Returns a handle usable with `Event.Delete`. By far the most common call in the codebase — used hundreds of times across `resident/`, `vz/`, and `shell/`. |
| `Event.CreatePersistent` | `Event.CreatePersistent(eventType, {args}, callback, {callbackArgs} [, bImmortalEvents])` | Same shape as `Create`, plus an optional 5th boolean argument seen in `shell/mrxguibase.lua:536` and `:730` (passed through as `self.BasicData.bImmortalEvents`). The exact semantic difference from `Create` (e.g. whether it re-fires repeatedly, or simply survives something `Create` doesn't) is **not confirmed** from source alone — no comment or contrasting behavior was found. Used for events that should keep listening across multiple occurrences (e.g. `resident/enemyblippable.lua` driver-enter/exit, `resident/hero.lua` repeated health-drop tracking) rather than a single fire-and-forget. Treat "persistent" as "stays registered / can fire more than once" pending live confirmation. |
| `Event.Delete` | `Event.Delete(handle)` | Unregisters an event previously returned by `Create`/`CreatePersistent`. Used pervasively for cleanup, e.g. `vz/allcon002.lua:182`, `resident/alarm.lua:43,47`. Safe/expected pattern: store the handle, delete it in a cleanup/teardown function. |
| `Event.Post` | `Event.Post(name, {data})` | Distinct usage pattern: takes a **string name** (not one of the `Event.*` numeric constants) plus a data table, e.g. `Event.Post("SurvivalMode", {uGuid})` (`resident/hero.lua:222`), `Event.Post("MunitionsPickup", {vStock, uGuid})` (`resident/laptop.lua:112`), `Event.Post("ActionHijackStart", {self})` (`resident/mrxactionhijack.lua:130`). This looks like a custom/named broadcast-event mechanism, separate from the numeric `Event.ScriptEvent` ID also present in the enumeration. No decompiled call site was found that both posts and listens for the same custom name via `Event.Create(Event.ScriptEvent, ...)` in the same file, so the exact delivery mechanism (whether `Event.ScriptEvent` listeners receive `Post`ed names) is **not confirmed**. |

## Event types

Columns: `ID` is the numeric value from the live enumeration. Modders should always reference
events by name (`Event.ObjectDeath`), never by number — see Notes below.

### Gameplay / Object events

| Event Type | ID | Args shape | Notes |
|---|---|---|---|
| `ObjectHealth` | 0 | `{guid, ">"\|"<", threshold}` | **Confirmed.** `Event.Create(Event.ObjectHealth, {uGuid, ">", 5}, ...)` (`resident/hero.lua:71`); also with `"<"` and a dynamic threshold from `Object.GetHealth(uGuid)` (`resident/hero.lua:158`, via `CreatePersistent`). Fires when the object's health crosses the given comparison against the threshold. |
| `ObjectHealthLessThan` | 1 | `{guid, healthValue}` | **Confirmed.** `Event.Create(Event.ObjectHealthLessThan, {uTarget, nHealth / 2}, ...)` (`vz/chicon001.lua:75`). Simpler sibling of `ObjectHealth` — no explicit comparator argument, always "less than". |
| `ObjectDeath` | 2 | `{guid}` | **Confirmed.** `Event.Create(Event.ObjectDeath, {thisBldg}, function() ... end)` (`vz/chicon001.lua:39`); also seen via `CreatePersistent` with a filter guid in `vz/oilcon001.lua:1111`. |
| `ObjectDelete` | 3 | name only | **Name only.** No confirmed call site found. Presumably fires when the object is deleted/despawned (distinct from `ObjectDeath`, which is a gameplay-death event). |
| `ObjectProximity` | 4 | `{guidA, guidB, "<"\|">", distance, bool, bool}` | **Confirmed.** `Event.Create(Event.ObjectProximity, {Player.GetAnyCharacter(), Pg.GetGuidByName("Civ_VIP_2"), "<", 20, false, false}, ...)` (`vz/allcon001.lua:33`). Fires based on distance comparison between two objects; meaning of the two trailing booleans not confirmed. |
| `Boundary` | 5 | name only | **Name only.** No confirmed call site found. |
| `ObjectInSeat` | 6 | `{guid, seatSpec, ...}` | **Confirmed** (shape partially). Used repeatedly, e.g. `resident/emplaced.lua:20,30` (enter/exit pairs), `vz/gurcon003.lua:290,323,331`. Full argument shape (seat index/name conventions) not fully enumerated here — check call sites directly for the specific pattern needed. |
| `ObjectWinched` | 7 | `{guid, number, "any"\|...}` | **Confirmed.** `Event.CreatePersistent(Event.ObjectWinched, {uGuid, 0, "any"}, ...)` (`resident/crate.lua:12`). |
| `ObjectTowed` | 8 | name only | **Name only.** No confirmed call site found. |
| `ObjectHibernation` | 9 | `{guid, "awake"\|"asleep"\|"hibernated"\|"s"}` | **Confirmed** — the single most common event type in the codebase by call-site count. E.g. `Event.Create(Event.ObjectHibernation, {oCopter01, "awake"}, self.AssetsLoaded, {self})` (`vz/allcon008.lua:144`), `{uVeh, "hibernated"}` (`vz/allcon008.lua:152`). Used to detect when an object wakes up / goes dormant, commonly to defer expensive setup until an object is actually active. |
| `ObjectIsReady` | 10 | name only | **Name only.** No confirmed call site found. |
| `ObjectIsGrounded` | 11 | name only | **Name only.** No confirmed call site found. |
| `ObjectPhysicsEvent` | 12 | name only | **Name only.** No confirmed call site found. |
| `ObjectIsVisible` | 13 | name only | **Name only.** No confirmed call site found. |

### Human / animation events

| Event Type | ID | Args shape | Notes |
|---|---|---|---|
| `HumanStateTransition` | 36 | `{guid, fromStatePattern, toStatePattern}` | **Confirmed.** `Event.Create(Event.HumanStateTransition, {uPlayer, "*", "Swim.*"}, self.ActivateTutorial, {self, true})` (`vz/wiftutorialswimming.lua:9`) and the mirror-image exit case `{uPlayer, "Swim.*", "Upright.*"}` / `{uPlayer, "Swim.*", "InVehicle.*"}` (same file, lines 18-27). State patterns appear to be glob-style strings (`"*"` wildcard, `"Swim.*"` prefix match) over the character's animation/action state machine. |
| `HumanActionComplete` | 38 | name only | **Name only.** No confirmed call site found. |
| `HumanAnimationNearlyCompleted` | 41 | name only | **Name only.** No confirmed call site found. |
| `AnimationEvent` | 35 | name only | **Name only.** No confirmed call site found. |
| `AirstrikeDeliveryReady` | 34 | name only | **Name only.** No confirmed call site found. |
| `Minigame` | 37 | name only | **Name only.** No confirmed call site found. |
| `Movie` | 40 | name only | **Name only.** No confirmed call site found. |
| `WeaponEvent` | 43 | name only | **Name only.** No confirmed call site found. |

### Input / player events

| Event Type | ID | Args shape | Notes |
|---|---|---|---|
| `Button` | 39 | `{playerOrGuid, buttonName, "press"\|"release"?, bool}` | **Confirmed, and confirmed live by testing.** Exactly 4 button-name strings are ever used in the whole decompiled corpus: `"lbutton"` (`vz/gurcon003.lua:317`, `resident/spyhunter.lua:138`), `"rtrigger"` (`vz/meccon001.lua:246,736`, `resident/moonpatrol.lua:122`), `"cancel"` and `"selection"` (both `resident/mrxguihudmessage.lua`). Live-tested by registering listeners for all 4: `lbutton`, `rtrigger`, and `selection` fired reliably on left-click / right-trigger / a selection-confirm input respectively; `cancel` was not observed firing in that test but is real per source. This is a small, fixed set of semantic action buttons (interact/trigger/cancel/select) tied to specific tutorial and HUD features, not a general raw-input or movement-direction API — there is no confirmed evidence of directional/stick button names anywhere in this system. (An earlier version of this page incorrectly listed `"lsleft"`/`"lsright"` here — those come from a completely unrelated mechanism, `MrxGuiBase.Joystick.BUTTON_L_STICK_D`/`U` constants compared against a `tEvent.ButtonPress` field inside GUI widget callbacks in `shell/mrxguidialogbox.lua`/`shell/mrxguicinematic.lua`, not `Event.Button` at all.) |
| `ContextAction` | 33 | `{playerGuid, targetGuid}` | **Confirmed.** `Event.Create(Event.ContextAction, {Player.GetAnyCharacter(), uGuid}, Junk.ToggleAlarm, {uGuid})` (`resident/alarm.lua:59`); also `resident/collectable.lua:24`. Fires on the player's "use/interact" context action against a target object. |
| `Player` | 32 | name only | **Name only.** No confirmed call site found (distinct from the `Player` engine namespace itself — this is just an event-ID constant that happens to share the name). |
| `GameStateChange` | 31 | `{fromState, toState}` | **Confirmed.** `Event.Create(Event.GameStateChange, {"Pause", "Exit"}, ...)` and `{"Loading", "Exit"}` (`shell/mrxguishell.lua:231,576`); also `{"unloading", "enter"}` (`shell/mrxsound.lua:38`). Fires on named game-state transitions (`"Pause"`, `"Loading"`, `"unloading"`, etc., with `"Exit"`/`"enter"` as the transition direction). |

### Gui events

All `Gui*` types below are **name only** — no confirmed call sites were found showing their argument
shapes (they're presumably consumed by the native Flash/Scaleform GUI layer rather than by
decompiled Lua directly). Names are self-explanatory from the live enumeration.

| Event Type | ID |
|---|---|
| `GuiUpdate` | 14 |
| `GuiAmmoUpdate` | 15 |
| `GuiMinimapUpdate` | 16 |
| `GuiHealthUpdate` | 17 |
| `GuiVehicleHealthUpdate` | 18 |
| `GuiReticleUpdate` | 19 |
| `GuiPauseStateChange` | 20 |
| `GuiAnimateUpdate` | 21 |
| `GuiWeaponEquippedUpdate` | 22 |
| `GuiSupportMenuEnter` | 23 |
| `GuiSeatMenuEnter` | 24 |
| `GuiGameStateChange` | 25 |
| `GuiPlayerReceiveDamage` | 26 |
| `GuiVehicleNameUpdate` | 27 |
| `GuiVehicleDisguiseUpdate` | 28 |
| `GuiGameTimer` | 29 |

### Timer / misc events

| Event Type | ID | Args shape | Notes |
|---|---|---|---|
| `TimerRelative` | 30 | `{seconds}` | **Confirmed**, and the only event type with in-game live-tested confirmation (not just static source evidence). `Event.Create(Event.TimerRelative, {2}, callback, {})` fires `callback` once, `seconds` after registration. Used hundreds of times throughout `vz/` mission scripts for delayed one-shot actions (e.g. `vz/allcon002.lua` has dozens of staggered `TimerRelative` calls for sequenced events). See [Snippets](../snippets#react-to-an-event-instead-of-polling). |
| `ScriptEvent` | 42 | `{name, callback}` (as filter args to `Create`/`CreatePersistent`) | **Confirmed.** `Event.CreatePersistent(Event.ScriptEvent, {"mpPlayerJoin", function(tData) ... end}, ...)` (`resident/alarm.lua:64`, `shell/mrxmusic.lua:318`). Appears to be a named-signal mechanism similar in spirit to `Event.Post`, but registered like any other event type rather than posted directly; relationship between this and `Event.Post`'s string-named events is not confirmed from source. |

## Notes for modders

- The numeric IDs (0-43) are stable within a given game build, but **always reference events by
  name** — `Event.ObjectDeath`, not the literal `2` — since that is what every real decompiled
  script does, and it self-documents and survives if the underlying numbering ever changes.
- Argument shapes are positional tables with no labeled fields; get the shape wrong (wrong arg
  count, wrong type, wrong string literal) and the event silently won't fire the way you expect.
  When in doubt, copy the closest matching real call site above rather than guessing.
- Store the handle returned by `Event.Create`/`Event.CreatePersistent` if you'll need to
  `Event.Delete` it later (e.g. on mission cleanup, object death, or teardown) — leaked event
  registrations are a common source of callbacks firing after the object/context they reference is
  gone.
