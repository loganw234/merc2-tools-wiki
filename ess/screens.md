---
title: Player Screens & Map Surfaces
parent: Essentials (Ess)
nav_order: 22
---

# Player Screens & Map Surfaces

## Overview

Four namespaces, all new in **Ess 0.5.0**, all covering something the player actually looks at rather than
something that happens in the world:

| Namespace | Source | What it is |
|---|---|---|
| `Ess.Pda` | `src/58_pda.lua` | The mission log, the dossier database, the statistics screen, and the map layer underneath `Ess.Mark`'s blips. |
| `Ess.Minimap` | `src/57_minimap.lua` | The minimap **widget** — range, rotation, visibility, border. Not the objectives drawn on it. |
| `Ess.Gps` | `src/57_gps.lua` | The map beacon: the waypoint the player drops on the PDA map and drives towards. |
| `Ess.Shop` | `src/58_shop.lua` | The game's own full-screen purchase UI, filled with your own items. |

**The screen surfaces themselves are not engine natives.** `resident/mrxguiinterface.lua` sets
`_G.Pda = PdaInterface` (and `_G.oPda` as a second name for the same table) and `_G.Hud = HudInterface`
(`mrxguiinterface.lua:13-16`); every function on them is a thin wrapper that resolves a Scaleform widget and
forwards to it. Two of the namespaces below do reach a real engine native at the edges — `Ess.Gps.clear()`
calls `Player.ClearGPS`, and `Ess.Minimap.autoZoom`'s replacement handler reads `Object.GetVelocity` — but
neither of those is a *screen* call. That reclassification was part of the same
release — see `CHANGELOG.md` 0.5.0, *"`natives.json` is honest about what is native"* — and it means all four
namespaces here sit on **readable Lua**, not on a black box. `Ess.Minimap` is the odd one out even by that
standard: what it drives is the widget object itself, re-resolved from the widget registry on every call
rather than reached through any interface table.

The framework's own release notes are explicit about where this cluster came from, and it is worth repeating
before any of the detail below:

> Most of this came out of live probing against a running game rather than reading the decompiled scripts,
> and the traps below are recorded because none of them are guessable from a function name.

Three of those traps are load-bearing enough to state up front:

- **A minimap zoom does not stick unless you own the update handler.** The game recomputes minimap range from
  player speed on *every* update, so a plain `range()` call is overwritten within moments. That is why
  [`lockRange()`](#range-vs-lockrange--why-a-naive-zoom-appears-to-do-nothing) exists.
- **A beacon placed by `Ess.Gps.set()` is cosmetic.** There is no `Player.SetGPS`. The marker draws
  correctly; the engine does not treat it as the player's destination. See [Ess.Gps](#essgps).
- **`Ess.Shop` is modal and can strand the player without controls.** `Ess.Shop.close()` is as much a rescue
  call as a teardown call. See [`close()`](#close--the-escape-hatch).

## Status

These four namespaces have a **different evidence profile** from most of the framework, and it is worth being
precise about it rather than inheriting the confidence of neighbouring pages.

**What is strong.** The behavioural findings below were live-confirmed on screen against a running game on
**2026-07-26**, and the source files record them with the specific measurements that produced them — a
four-blip cross to establish the map's axis orientation, four otherwise-identical blips side by side to
establish that an icon draws nothing, a real purchase to establish the shop's buy path. Where this page cites
a number, that number comes from a recorded measurement, not a reconstruction.

**What is weaker.** Unlike [`Ess.Pursuit`](pursuit#status), which has a dedicated repeatable smoke recipe,
**no script in `samples/recipes/` exercises any of these four namespaces.** Nothing re-runs these checks on a
release build. The offline gate that does cover them is `tools/checksyntax.py` (also new in 0.5.0), which
compiles every `src/` file plus the built dist — so these files are known to parse, which is a much lower bar
than known to work. Treat the dated findings as one-off probe sessions carefully written down, because that
is exactly what they are.

**Neither 0.5.1 nor 0.5.2 touched any of this.** 0.5.1 was data-only (`1_Ess.lua` unchanged apart from the
version string; it added `published_global` to `api/natives.json` for downstream tooling), and 0.5.2 shipped
the missing `ess_ui.gfx` movie in `vz-patch.wad` — an `Ess.UI` fix with no bearing here. This cluster is as it
shipped in 0.5.0.

A short ledger of what was actually observed, so the rest of the page can be read against it:

| Finding | How it was established |
|---|---|
| PDA log `sType` `"objective"`/`"event"`/`"dialog"` all route and display | On screen, 2026-07-26 |
| Re-adding a dossier entry with the same `sTitle` edits rather than duplicates | On screen, 2026-07-26 |
| `icon_yellow_mc` draws nothing | Four otherwise-identical blips side by side; `icon_action_1_mc` and `icon_deliverable_1_mc` rendered, `icon_yellow_mc` and a no-texture blip were both blank |
| An unlabelled blip displays its texture name | On screen — the blip read `"icon_verify_1_mc"` |
| The PDA map's X axis is mirrored | Four-blip cross: `nY+400` drew above the player, `nX+400` drew **left**, `nX-400` drew **right** |
| `missionExists()` is a genuine existence test | Verified against three real missions, one never-registered name, and one the wrapper's guard had rejected |
| `selectedMission()` returns `nil` with nothing selected | Measured |
| A bare minimap `SetRange` is one-shot | Range 1500 while standing still visibly zoomed out **and held**, then snapped back the moment the map turned |
| `lockRange()` holds | Same zoom held through turning and driving, same day |
| `_G.MinimapDataUpdateHandler` is `nil` | Measured live — `import()` namespaces it as `MrxGuiBase.MinimapDataUpdateHandler` |
| The PDA's stored `nMarkerX`/`nMarkerZ` lag the real GPS state | Read `3008` after the player had cleared the beacon; correctly `nil` after a later cycle |
| The GPS script events are exact | Four firings across two set/clear cycles, in order, with the right coordinates |
| `Player.ClearGPS` exists and `Player.SetGPS` does not | Full `pairs(_G)` walk of the running game |
| The shop works end to end | A real purchase — `BUY ess_covert x4` — on an item added with `nOwned = 0` |
| Closing the shop with Escape strands the player | Measured: focus queue depth 0, holder `nil`, control mode flag still `true`, with every callback having fired correctly |
| The `supplies_*` icon family renders | On screen, 2026-07-26. `HUD_ICON_support_crate` drew a placeholder box instead |

## Ess.Pda

Source: `src/58_pda.lua`. Twenty functions over four surfaces — the log, the reference database, the map, and
the PDA screen itself.

**Read the return value carefully.** Almost every function here returns `true` as soon as its own argument
guard passes; it does **not** confirm the widget did anything. That is not laziness in the wrapper, it is
forced: `Pda.Map`'s interface functions loop the matching widgets and discard each result, so
`Pda.Map:AddMission` always returns `nil` even when the underlying `AddMapMission` returned a meaningful
boolean. The source records that an earlier version of `Ess.Pda.mission` reported `false` for three missions
that had all been created correctly. [`missionExists()`](#missions) is the workaround, and the only read
channel of its kind on this namespace.

| Function | Signature | Wraps |
|---|---|---|
| `log` | `Ess.Pda.log(sMessage [,tOpts]) -> ok` | `Pda.Database:AddLogEntry` |
| `dossier` | `Ess.Pda.dossier(sTitle, sText [,sIcon]) -> ok` | `Pda.Database:AddDossierEntry` |
| `statCategory` | `Ess.Pda.statCategory(sCategory [,sIcon]) -> ok` | `Pda.Database:AddStatisticCategory` |
| `stat` | `Ess.Pda.stat(sCategory, sDesc, sData) -> ok` | `Pda.Database:AddStatisticEntry` |
| `blip` | `Ess.Pda.blip(sName, tOpts) -> ok` | `Pda.Map:AddBlip` |
| `removeBlip` | `Ess.Pda.removeBlip(sName) -> ok` | `Pda.Map:RemoveBlip` |
| `selectedMission` | `Ess.Pda.selectedMission() -> sName \| nil` | `Pda.Map:GetSelectedMission` |
| `mission` | `Ess.Pda.mission(sName, tOpts) -> ok` | `Pda.Map:AddMission` |
| `missionExists` | `Ess.Pda.missionExists(sName) -> bool` | (composed — see below) |
| `removeMission` | `Ess.Pda.removeMission(sName) -> ok` | `Pda.Map:RemoveMission` |
| `selectMission` | `Ess.Pda.selectMission(sName) -> ok` | `Pda.Map:SetSelectedMission` |
| `trackable` | `Ess.Pda.trackable(sName, bOn) -> ok` | `Pda.Map:SetMissionTrackable` |
| `onMissionTrack` | `Ess.Pda.onMissionTrack(fn) -> ok` | `Pda.Map:SetMissionTrackCallback` |
| `allowMissionChange` | `Ess.Pda.allowMissionChange(bOn) -> ok` | `Pda.Map:SetMissionChangeAllowed` |
| `fakePlayerLocation` | `Ess.Pda.fakePlayerLocation(x, y, z) -> ok` | `Pda.Map:SetFakePlayerLocation` |
| `region` | `Ess.Pda.region(uGuid, tOpts) -> ok` | `Pda.Map:AddLineRegion` |
| `removeRegion` | `Ess.Pda.removeRegion(uGuid) -> ok` | `Pda.Map:RemoveLineRegion` |
| `beaconTutorial` | `Ess.Pda.beaconTutorial(bOn) -> ok` | `Pda.Map:SetBeaconTutorialMode` |
| `suppress` | `Ess.Pda.suppress(bOn) -> ok` | `Pda:SetSuppressed` |
| `attitude` | `Ess.Pda.attitude(sFaction, nAttitude [,sTexture]) -> ok` | `Pda.Database:SetFactionAttitude` |

**Colours are bare hex strings** wherever they appear on this namespace — no `#`, no `0x`. The game passes
`"3399FF"` for events and `"FFFFFF"` for dialogue. [`Ess.Color`](core#esscolor) is deliberately *not* used
here, because it produces numbers and the widget wants the string.

**Text fields accept literal strings**, which is the only reason any of this is usable from a mod. The
shipped game almost always passes a **localization token** instead — `"[Generic.CheckpointReached]"`,
`"[PDA.Support.denied]"` — which the widget resolves against the string database. A token that does not
resolve renders as the raw bracketed text, so literal square brackets on screen mean exactly that. Inline
colour tags use the same syntax (`"[red]some text"`), so a leading `[` in your own text is worth avoiding.

### The log, the dossier and the statistics screen

`Ess.Pda.log(sMessage, tOpts)` is the most useful function in the file, and the reason the namespace exists:
Ess already had several ways to put text on screen for a few seconds, but no way to leave a **permanent,
scrollable, player-reviewable record** of what a mod did.

- `tOpts.sType` — the log section. `"objective"`, `"event"` and `"dialog"` are the three the shipped game
  uses, and all three were confirmed to route and display live. Defaults to `"event"`. The value is passed
  straight through, so an unrecognised one is the widget's problem rather than an error in the wrapper.
- `tOpts.sName` — a short label. Defaults to `""`, which is what the game passes everywhere.
- `tOpts.sColor` — bare hex. Defaults to `"3399FF"`, the game's own event blue.

`Ess.Pda.dossier(sTitle, sText, sIcon)` adds a database entry. **Re-adding the same `sTitle` edits that entry
rather than duplicating it** (the widget keys its index by title), so this doubles as the edit call. `sIcon`
is optional and renders blank if omitted.

`Ess.Pda.statCategory(sCategory, sIcon)` must run before `Ess.Pda.stat(sCategory, sDesc, sData)` can add rows
to that category. Both are additive and **there is no remove** for either.

> **`Pda.Database.AddHelpEntry` is deliberately not wrapped.** It is a write-only dead end. The widget stores
> it exactly like a dossier entry — same shape, same indexing — into `oPda.CustomData.tDataHelp`, and that
> table is initialised in one place, appended to in one place, and read in none. `tDataDossiers` by contrast
> is read at `mrxguipda.lua:1388` and rendered, which is why dossier entries appear and help entries do not.
> Live testing agreed: an added help entry was nowhere in the PDA. No argument fixes it, so there is no
> wrapper for it.

### Map blips

`Ess.Pda.blip(sName, tOpts)` exposes the parameters [`Ess.Mark`](mark) does not. `AddMapBlip` takes
**thirteen** parameters (`mrxguipda.lua:209`); `Ess.Raw.Mark.pda` fills five of them — `sName`, `uGuid`,
`sTexture`, `sLabel`, `nSortOrder` — because that is all the single corpus call site it was derived from used.
The two that matter most here:

- **`nX`/`nY` place a blip at a fixed map coordinate with no object behind it.** `Ess.Mark` cannot do this at
  all — it needs a guid to attach to. This is how you mark a destination, a search area, or the place where
  something used to be.
- **`sLabel`/`sDesc` give the blip a name and description in the PDA's own list**, so it reads as a real
  objective rather than an anonymous dot.

| Option | Meaning |
|---|---|
| `nX`, `nY` | World coordinates. **`nY` is world Z**, not world Y. |
| `sLabel`, `sDesc` | Name and description in the PDA list. `sLabel` defaults to `sName`. |
| `uGuid` | Attach to an object instead of to coordinates. |
| `sTexture` | Icon name from [`Ess.Pda.ICONS`](#the-icon-vocabulary). Defaults to `"icon_action_1_mc"`. Pass `false` to genuinely opt out. |
| `sMission` | Name a registered mission to make this a mission blip — see [Missions](#missions). |
| `nMeter` | Passed through, but **apparently inert** — see below. |
| `bSticky` | Force sticky, overriding the mission-tracked default. |
| `bTodoList` | Renders the blip as its own pseudo-mission, using its own `sLabel`/`sFaction` in place of a mission's (`mrxguipda.lua:577-581`). |
| `sFaction` | One of `Ess.Pda.FACTIONS`. Effectively defaults to `"PMC"` — see below. |
| `nSortOrder` | Position in the list. Effectively defaults to `5` — see below. |

**On `sFaction` and `nSortOrder`'s defaults**, because it is easy to attribute them to the wrong layer:
`58_pda.lua`'s own header describes the wrapper as defaulting them. It does not — it passes both straight
through. The defaults are the game's, applied one level down in `PdaInterface.Map:AddBlip`, which calls
`AddMapBlip(..., tArgs.sFaction or "PMC", tArgs.nSortOrder or 5)` at `mrxguiinterface.lua:1144`. The
behaviour you get is the same; the reason to be precise is that these are **not** defaults Ess could change,
and anything reading `Pda.Map:AddBlip` directly inherits them too.

**`nMeter` looks inert.** `AddMapBlip` stores it on the blip record (`mrxguipda.lua:219`) and **nothing in the
decompiled corpus ever reads it back** — a whole-corpus search finds it only in the parameter list, that one
assignment, and the interface call that forwards it. The 15-slot positional array the render path hands to the
Flash movie does not include it. Ess exposes it because the native takes it, not because it is known to do
anything. Untested in-game; treat it as inert until someone shows otherwise.

**Coordinates.** `nX`/`nY` are world coordinates and `nY` is world **Z** — the render path adds `nXOffset` to
one and `nZOffset` to the other (`mrxguipda.lua:597-598`). Height is not representable; a top-down map has
nowhere to put it. **The X axis is mirrored on the map**: measured with a four-blip cross, `nY+400` drew
*above* the player, `nX+400` drew to the *left* and `nX-400` to the *right*. Increasing world X moves a blip
left across the PDA. Nothing in the script layer says so — the flip happens inside the Flash movie.

Two related behaviours, both read from `mrxguipda.lua` rather than measured:

- **A blip with `uGuid` follows the object.** The render path overwrites the stored `nX`/`nY` from
  `Object.GetPosition(tBlip.uGuid)` on every refresh (`mrxguipda.lua:554-560`), so passing both a guid and
  coordinates is not a conflict — the guid wins, continuously.
- **A blip with neither lands at world origin.** `AddMapBlip` stores `nX or 0` / `nY or 0`
  (`mrxguipda.lua:212-213`), so an under-specified blip is at `(0, 0)` on the map, not absent from it.

**The two defaults exist because of measured failures.** `sTexture` defaults to `"icon_action_1_mc"` and
`sLabel` defaults to `sName`, because omitting either fails in a way that looks like the call did nothing:

- **A blip with no drawable icon is invisible** — placed and hoverable, but nothing rendered until the cursor
  is over it. Note this is not simply "no texture": the engine's fallback chain ends at `icon_yellow_mc`,
  which itself draws nothing, so falling through is exactly as invisible as passing nothing.
- **No label means the blip displays its texture name.** The render path builds a positional array whose 6th
  slot is `tBlip.sLabel or tMissionData.sDefaultBlipLabel` (`mrxguipda.lua:600`); with no label and no owning
  mission that slot goes `nil`, and the movie shows the texture instead. Confirmed live — an unlabelled blip
  read `"icon_verify_1_mc"` on screen.

⚠ **Both defaults are suppressed when the blip belongs to a mission**, and that matters. The render path is
`tBlip.sTexture or tMissionData.sDefaultBlipTexture or "icon_yellow_mc"` (`mrxguipda.lua:596`) and the label
works the same way, so a default supplied by the wrapper would win over the mission's and the blip could never
inherit. Defaulting unconditionally made `sMission`'s whole reason for existing unreachable — caught on
screen, where mission blips showed the generic yellow dot instead of their mission's icon. With `sMission`
set, the wrapper leaves both fields `nil` so the mission supplies them.

**Blips are not tracked for teardown here.** Use [`Ess.Track:pda(sName)`](tracking#esstrack) if you want
automatic cleanup — that is what it already exists for.

#### The icon vocabulary

`Ess.Pda.ICONS` is a flat array of **31** names, and `Ess.Pda.FACTIONS` is the seven the PDA recognises
(`"PMC"`, `"AN"`, `"CH"`, `"GR"`, `"OC"`, `"PR"`, `"VZ"`, uppercase — anything else resolves to `nil` and
shows no faction).

The icon names come from a fixed engine table, `mrxutil.lua`'s `tObjPdaMarker`, which
`MrxUtil.MarkerGetIndexByName_Pda` linear-searches, complaining and returning index `0` for anything it does
not recognise. **That lookup gates the co-op broadcast only** — the net path sends an index rather than a
string, while local rendering passes the string straight to the movie. So an unlisted name can still draw
locally and simply fail to replicate.

The `_1`/`_2`/`_3` suffixes are objective tiers. Tier 3 is the "tertiary" set the PDA can filter out
wholesale — the render path drops exactly `icon_action_3_mc`, `icon_outpost_3_mc`, `icon_defend_3_mc`,
`icon_destroy_3_mc`, `icon_verify_3_mc` and `icon_deliverable_3_mc` when that filter is on
(`mrxguipda.lua:612-613`).

⚠ **`icon_yellow_mc` is deliberately absent from `Ess.Pda.ICONS`, even though the engine's table contains it
— twice, in fact (indices 1 and 33 of 34, the last entry being an empty string). It draws nothing.** That is
worth more than a footnote, because `icon_yellow_mc` is the engine's own final fallback and was
`AddMapMission`'s default for `sDefaultBlipTexture`. Any blip that falls all the way through the chain is
invisible by construction — which is also the real reason `Ess.Mark`'s PDA blips had never shown up, a symptom
previously blamed on their missing label.

### Missions

`Ess.Pda.mission(sName, tOpts)` is the piece that turns a loose blip into something the PDA treats as a real
objective. It registers a mission, or updates one that already exists.

| Option | Meaning |
|---|---|
| `sLabel` | The mission's name in the PDA list. **Required for a new mission.** |
| `sDesc` | Its description. **Required for a new mission.** |
| `sFaction` | One of `Ess.Pda.FACTIONS`. **Required for a new mission.** |
| `sIcon` | Default blip texture for its blips (`sDefaultBlipTexture`). |
| `sBlipLabel` | Default blip label for its blips (`sDefaultBlipLabel`). |
| `bTrackable` | Defaults to **true** for a new mission. |
| `bSuppress` | Hide it. Forces `bTrackable` false and blanks the faction. |
| `nSortOrder` | Position in the list. |

**The interaction worth knowing:** a blip whose `sMission` names a registered mission is rendered as a
**mission blip** and inherits that mission's default icon and label. Two things follow from the same
association, both read directly from the render path:

- It turns **sticky** while its mission is the tracked one — `mrxguipda.lua:566-569` sets `bSticky` true when
  the blip left `bSticky` unset and its mission is the selected one. That is what makes it stand out.
- It becomes selectable as a **tracking target**, but only when `Ess.Pda.allowMissionChange(true)` is on —
  `mrxguipda.lua:571-572` reads the mission's `bTrackable` only inside that gate.

Two precisions the changelog's one-line summary does not carry, both read straight from the render path:

- **The "mission blip" flag requires a *trackable* mission.** It is
  `not tMissionData.bNoMission and tMissionData.bTrackable` (`mrxguipda.lua:590-592`), so naming a
  registered-but-untrackable mission still inherits its icon and label while producing an ordinary blip.
- ⚠ **A suppressed or misspelled mission name inherits nothing, and that is worse than it sounds.** The
  render path resolves `tMissions[tBlip.sMission] or tEmptyMission` and then swaps in `tEmptyMission` again
  if the mission is suppressed (`mrxguipda.lua:565`, `:573-575`), and `tEmptyMission` is
  `{ bNoMission = true, sId = "", sLabel = "" }` (`mrxguipda.lua:487-491`) — no default texture, no default
  blip label. Since Ess deliberately withholds its own `sTexture`/`sLabel` defaults for any blip that names a
  mission, **a typo in `sMission` produces an invisible blip whose label is its own texture name** — both
  failure modes at once. If a blip vanishes, check the mission name before anything else.

[`Ess.Contract`](contract) is the obvious consumer of all of this.

Three things the native does that you would not guess from the name:

1. **A new mission is rejected outright** unless `sLabel`, `sDesc` *and* `sFaction` are all strings —
   `AddMapMission` returns `false` and does nothing. The native's own test is
   `if not bSuppress and ("string" ~= type(sLabel) or ...)` (`mrxguipda.lua:262`), so a call that sets
   `bSuppress` is exempt. Only for a *new* mission, either way: updating an existing one may omit any of the
   three, and each omitted field keeps its old value. The wrapper mirrors that gate up front so the failure
   is explained rather than silent — but note its exact shape, because it is a compromise. It is
   `if not o.bSuppress and (o.sLabel or o.sDesc or o.sFaction)`: it carries the native's `bSuppress`
   exemption, and beyond that it only fires if you supplied *at least one* of the three. Supplying none is
   read as "you are relying on an existing entry" and passes straight through, since the wrapper cannot see
   the engine's mission table from where it stands.
2. **`sBlipLabel` defaults to the literal string `"DESIGNER ERROR"`.** Not a placeholder Ess invented — that
   is what `mrxguipda.lua:277` puts there, and it renders on the map, which reads like a deliberate QA
   tripwire. Ess leaves it as the engine's default rather than substituting something quieter, because seeing
   it means you forgot `sBlipLabel`.
3. **Updates deliberately go through `AddMission`, never `UpdateMission`.** `Pda.Map:UpdateMission` is
   **broken** by a parameter shift across the wrapper/widget boundary: the interface passes `tArgs.bTrackable`
   as its 8th positional argument (`mrxguiinterface.lua:1190`) and `UpdateMapMission`'s 8th parameter is
   `nSortOrder` (`mrxguipda.lua:318`). Asking `UpdateMission` for `bTrackable = true` therefore sets the
   **sort order** to `true` and leaves the trackable flag untouched — and `UpdateMapMission`'s body then
   forwards an undeclared global `bTrackable` on to `AddMapMission`. Use `Ess.Pda.trackable` to change
   tracking.

⚠ **A mission registered without `sIcon` gives its blips an invisible default.** `AddMapMission` stores
`sDefaultBlipTexture or "icon_yellow_mc"` (`mrxguipda.lua:276`) — and `icon_yellow_mc` draws nothing. Since
Ess deliberately does *not* default `sTexture` on a blip that belongs to a mission (so the mission can supply
it), a mission with no `sIcon` produces exactly the invisible-blip case the blip defaults exist to prevent.
Set `sIcon` on any mission whose blips you want to see. *(Read from source; the failure mode itself was
confirmed live, the specific mission-without-icon path was not separately measured.)*

**`Ess.Pda.missionExists(sName)` is the only existence test there is.** There is no getter for the mission
table, and every `Pda.Map` wrapper discards its widget's return value, so nothing reports success directly.
This exploits the one native that is *conditional* on existence: `SetSelectedMission` stores the name only if
it is a registered mission, and stores `nil` otherwise. Selecting a name and reading it back is therefore a
genuine test — verified live against three real missions, one never-registered name, and one the guard had
rejected. It restores the previous selection afterwards, so it is non-destructive.

⚠ **It is not free. Do not poll it.** Each selection change emits a `Debug.Printf` and, on a server, a
network event.

The rest of the mission surface:

- **`Ess.Pda.removeMission(sName)`** removes the mission *and* every blip attached to it. The cascade is the
  native's own behaviour — `RemoveMapMission` sweeps `tMapBlips` for blips whose `sMission` matches — and it
  also clears the selection if this was the tracked mission. No separate teardown is needed for a mission's
  blips.
- **`Ess.Pda.selectMission(sName)`** sets the tracked mission; `nil` clears it. A name that is not a
  registered mission clears the selection rather than erroring — the native's behaviour, and the mechanism
  `missionExists` is built on.
- **`Ess.Pda.trackable(sName, bOn)`** is the working way to change the trackable flag. A suppressed mission is
  forced untrackable by the native regardless of what you pass (`mrxguipda.lua:325-327`).
- **`Ess.Pda.allowMissionChange(bOn)`** — whether the player may change which mission is tracked. The native
  **ignores a `true` on a network client** and always disallows there.
- **`Ess.Pda.onMissionTrack(fn)`** — `fn(sMission)` when the player *tracks* a mission, and `fn(nil)` when
  they *untrack* one. One callback for both; the argument is how you tell them apart. That asymmetry is in
  the game, not invented by Ess: `_HandleTrackEvent` appends the mission name to the callback data before
  unpacking it (`mrxguipda.lua:756-757`), and `_HandleUntrackEvent` unpacks the callback data alone
  (`:765-766`) — so with no callback data (which is what Ess passes, for the same reason as everywhere else
  in the framework) the game calls with one argument on track and **zero** on untrack. Ess normalises that
  last step: it registers `function(sMission) pcall(fn, sMission) end`, so your `fn` is always handed exactly
  one argument and the untrack case arrives as an explicit `nil` rather than an empty argument list. Test the
  value, not `select("#", ...)`.

  Unlike [`Ess.On.*`](reactive-hotkeys#esson--reactive-world-hooks) this does **not** return a `stop()`: the native stores a single
  callback per PDA, so registering is inherently last-one-wins. Pass `nil` to unregister.

### Map presentation and the PDA itself

- **`Ess.Pda.fakePlayerLocation(x, y, z)`** draws the player marker somewhere other than where they are; call
  it with no arguments to clear. The game uses this in the PMC interior, where the real position is
  meaningless on a world map. All three coordinates must be numbers or the native ignores the call, so the
  wrapper rejects a partial set rather than passing it on.
- **`Ess.Pda.region(uGuid, tOpts)` / `removeRegion(uGuid)`** shade a line region on the PDA map — the
  counterpart to `Ess.Raw.Mark.radarRegion` on the minimap. Colour handling is the native's and it is
  unusual: each channel is clamped to `0..255`, the defaults are **64 / 64 / 160 at alpha 128** (a muted blue,
  not black like the radar's), and **the alpha is converted to a percentage internally** (`a / 255 * 100`)
  while r/g/b become a `"0xRRGGBB"` string for the Flash movie (`mrxguipda.lua:339-348`). Pass alpha in
  `0..255` like the other channels and let it convert. `tOpts.rgb` is a `{r, g, b}` table; `tOpts.nAlpha` and
  `tOpts.bInvert` are the rest.

  The wrapper runs `tonumber` on the channels, not just the alpha, and that is a fix rather than a formality:
  the native clamps with a helper that returns `nil` for a non-number, and each channel then falls back to
  its own default — so a stringy `"64"` from a UI field silently produced the default colour instead of the
  one asked for, while the converted `nAlpha` worked.
- **`Ess.Pda.beaconTutorial(bOn)`** puts the map into the beacon-tutorial mode that prompts the player to
  place a GPS beacon — see [Ess.Gps](#essgps). The game's own GPS tutorial contract uses it.
- **`Ess.Pda.suppress(bOn)`** hides the PDA entirely. The game uses this for briefings and cutscenes.
- **`Ess.Pda.attitude(sFaction, nAttitude, sTexture)`** sets a faction's *displayed* attitude on the database
  screen. **Display only** — the real relation lives in `Ess.Relations`.

## Ess.Minimap

Source: `src/57_minimap.lua`. The minimap widget, as opposed to the things drawn on it.

**This exists because `Hud.*` cannot reach it.** `Hud.Radar` — the namespace [`Ess.Mark`](mark) drives — can
only add, remove and animate *objectives*. The widget underneath carries `SetRange`, `SetRotation`,
`SetBorder` and `SetVisible`, **none of which is reachable through any `Hud.*` function**. Getting at it means
asking the widget registry directly, `MrxGuiBase.GetWidgetByName("Minimap")` — which is a documented pattern
in the game's own code, since `mrxguiinterface.lua:511` does exactly the same thing for the objective tray.

There *is* a `_G.Minimap` global holding the same widget — `mrxguimanager.lua:60` assigns it (alongside
`_G.MessageBox`, `_G.ObjectiveTray`, `_G.SubtitleBuffer` and `_G.MapLabel`) when the local player's HUD is
built. `Ess.Minimap` deliberately does not use it: that global is a **cached handle**, and the widget is
rebuilt on level load, so re-resolving through the registry every call is the difference between a call that
works after a load and one that silently stops.

| Function | Signature | Notes |
|---|---|---|
| `widget` | `Ess.Minimap.widget() -> w \| nil` | The raw `MinimapWidget`, for anything not wrapped here. **Not cached** — the widget is rebuilt across level loads, so a stale handle would silently stop working. |
| `range` | `Ess.Minimap.range(n) -> ok` | **One-shot.** See below. |
| `lockRange` | `Ess.Minimap.lockRange(n) -> ok` | Sets the range and keeps it. |
| `unlockRange` | `Ess.Minimap.unlockRange() -> ok` | Restores the game's speed-based auto-zoom. |
| `autoZoom` | `Ess.Minimap.autoZoom(tOpts) -> ok` | Retunes the auto-zoom instead of defeating it. |
| `rotation` | `Ess.Minimap.rotation(n) -> ok` | **One-shot** — see below. |
| `show` | `Ess.Minimap.show(bOn) -> ok` | `SetVisible(bOn ~= false)`, so a bare `show()` shows. |
| `border` | `Ess.Minimap.border(sTexture, nWidth, nHeight) -> ok` | Swaps the frame texture. |

Unlike `Ess.Pda`, a `false` from these is informative — but the message depends on which function you called.
`range`, `rotation`, `show` and `border` share one helper, so a missing widget reports
`"the Minimap widget is not available -- wrong level state, or the HUD has not been built yet"` on the
[`Ess.DEBUG`](core#essdebug--two-channels-of-silence) channel. `lockRange` and `autoZoom` fail the same way
but say so differently — `"could not install the update handler -- no Minimap widget, or it has no
GuiMinimapUpdate handler to wrap"` — because they need a handler to wrap, not just a widget. The two
exceptions: `unlockRange()` returns `true` whether or not it found anything to restore, and `widget()`
returns `nil` silently. A missing widget is by far the most likely reason a minimap call appears to do
nothing, other than the range trap below.

⚠ **The widget is rebuilt on level load, which takes any override with it.** Re-apply after a load.

### `range()` vs `lockRange()` — why a naive zoom appears to do nothing

**The range is recomputed from player speed.** `MinimapDataUpdateHandler` (`mrxguibase.lua:1532`) runs on
every minimap data update and ends by calling `MinimapSetRange` with a value derived purely from
`Object.GetVelocity`: **150 below speed 10, 400 above speed 50, linear between** (`mrxguibase.lua:1540-1552`).
So a plain `SetRange` applies immediately and is then overwritten by the next update.

Measured 2026-07-26: setting range **1500** while standing still visibly zoomed the map out **and held** —
until the map was turned, at which point the handler ran and snapped it back. That is exactly the shape the
source predicts, and it is why `range()` is documented as a one-shot. With `lockRange` the same zoom held
through turning and driving, confirmed the same day.

`Ess.Minimap.lockRange(n)` **takes ownership of the recomputation** rather than fighting it on a timer. Two
things had to be right to do that, and both were traps hit in the process:

- **The handler is not a plain global.** `_G.MinimapDataUpdateHandler` is `nil` live (measured). Resident
  modules declare bare globals and the engine's `import()` machinery namespaces them, so it is really
  `MrxGuiBase.MinimapDataUpdateHandler`.
- **Patching that module entry would not work anyway.** The widget captures the function **by value** at
  construction — `self:SetEventHandler("GuiMinimapUpdate", MinimapDataUpdateHandler)` at
  `mrxguibase.lua:1445` — so it holds the original regardless of what the module table says afterwards.

The override therefore goes **on the widget**, via its own `SetEventHandler`, wrapping whatever handler is
currently registered. That is narrower than a global patch (one widget, not every consumer of the module) and
properly reversible, because `Widget:SetEventHandler` deletes the previous `Event` registration before making
the new one rather than leaking it. The wrapper always **wraps** rather than replaces: the original handler
performs the `MinimapUpdate` that actually *draws* the map before it ever touches the range, so a handler that
skipped it would freeze the minimap rather than zoom it.

`Ess.Minimap.unlockRange()` puts the original handler back and lets the auto-zoom resume.

### `autoZoom(tOpts)` — retune the curve instead

`Ess.Minimap.autoZoom(tOpts)` reproduces the game's own speed curve with your numbers instead of defeating it.
**Passing no options reinstates the stock figures, so it doubles as a reset.**

| Option | Stock value |
|---|---|
| `nMinSpeed` | `10` |
| `nMaxSpeed` | `50` |
| `nMinRange` | `150` |
| `nMaxRange` | `400` |

It rejects when `nMaxSpeed <= nMinSpeed`, because the curve divides by their difference. If it replaces an
active `lockRange`, it says so on the log:
`Ess.Minimap.autoZoom: replaced an active lockRange(<n>)`. The install is attempted **before** the existing
lock is dropped, so a failed install leaves the previous lock intact rather than leaving the wrapper on the
widget with no range to force.

One engine detail the reimplementation depends on: **`Object.GetVelocity` returns a scalar on this engine**,
not a vector — the stock handler relies on the same thing. A `nil` reading means leave the range alone, which
is what the original does too.

### The rest

- **`Ess.Minimap.rotation(n)`** is a **one-shot**, for the same reason a bare `range()` is: the game drives
  rotation from camera heading through the same update handler, and `lockRange`'s wrapper deliberately only
  forces the *range*. Owning rotation too would mean suppressing the original handler's rotation argument,
  which would break the map's north-up behaviour. Fine for a momentary flourish.
- **`Ess.Minimap.show(bOn)`** hides or shows the whole minimap. This is what the game's own E3-demo HUD mode
  does (`MinimapHandleE3HudModeEvent`, `mrxguibase.lua:1558`), so it is a supported state rather than a hack.
- **`Ess.Minimap.border(sTexture, nWidth, nHeight)`** swaps the frame texture. ⚠ It is guarded inside the
  widget by `if _GuiInternal.SetMinimapBorder then`, so on a build without that native it is a **silent
  no-op** — which also means a `true` from this call does not prove anything changed.

## Ess.Gps

Source: `src/57_gps.lua`. The player's map beacon — the waypoint they drop on the PDA map and drive towards.

**It is not a routing system**, and the name promises more than the engine delivers. There is no pathfinding,
no route line, no turn-by-turn anything. The entire GPS feature at the script layer is **one radar objective
with a reserved name**; `mrxguihudradar.lua:142-144` is the whole handler:

```lua
_sGPSName = "GPS Beacon Marker"

function HandleSetGPSDest(oMap, tEvent)
  oMap:AddObjective(_sGPSName, tEvent.PosX, 0, tEvent.PosZ, 255, 255, 255,
                    10.666667, 10.666667, "MiniMap_Icon_GPS_Marker", nil, true, nil, nil, 4)
end
```

That is good news for a mod: placing a beacon needs no special native, just an objective under the same name,
and that is what `.set()` does — with the name, texture, size and sort order taken verbatim from the game's
handler so a beacon placed by Ess and one placed by the game are the same object. Setting yours replaces
theirs rather than stacking on top.

| Function | Signature | Notes |
|---|---|---|
| `set` | `Ess.Gps.set(x, z [,tOpts]) -> ok` | Places the marker at a world X/Z. Y is deliberately absent — the game's own handler passes `0`, because the minimap is top-down. |
| `clear` | `Ess.Gps.clear() -> ok` | Clears **both halves**. Safe with no beacon set. |
| `get` | `Ess.Gps.get() -> x, z \| nil` | Where the beacon is. |
| `distance` | `Ess.Gps.distance([i]) -> n \| nil` | World units from player `i` (default `0`) to the beacon, in the **XZ plane only**. |
| `onSet` | `Ess.Gps.onSet(fn) -> stop()` | `fn(x, z)` when the **player** sets a beacon. |
| `onClear` | `Ess.Gps.onClear(fn) -> stop()` | `fn()` when the player clears one. |

`set()`'s options: `tOpts.rgb` (tint, default white like the game's), `tOpts.sTexture` (default
`"MiniMap_Icon_GPS_Marker"`), `tOpts.nSize` (default the game's own `10.666667`).

`set()` is one of the few calls in this cluster whose return value carries real information — it hands back
the guarded call's own result, so `false` means either bad arguments or a native that threw. `clear()` always
returns `true`; it is meant to be safe to fire blind. `onSet`/`onClear` return a **no-op `stop()`** rather
than failing if you pass something that is not a function, so a `stop()` you never armed is harmless to call.

⚠ **A beacon placed by `.set()` is cosmetic.** `Player.ClearGPS(uPlayer)` is a real engine native — confirmed
present live — but **there is no `Player.SetGPS`**. Not undocumented: absent, from a full `pairs(_G)` walk of
the running game. Setting a beacon is a **UI action** the player performs on the PDA map, which fires the
widget's `SetGPSDest` event. So `.set()` draws the marker and it shows on the minimap correctly, but the
engine does not consider it the player's GPS destination. `.clear()` does both halves — it calls the native
(clearing whatever engine state backs a real beacon, including one the player placed) *and* deletes the marker
(which is all a script-placed one ever was).

**On the texture, and what it proves.** `"MiniMap_Icon_GPS_Marker"` is **not** in `mrxutil.lua`'s
`tObjRadarMaker` — the closed list `MarkerGetIndexByName_Radar` validates against — and the game's own GPS
handler uses it anyway. That is the proof that these icon tables gate only the **co-op net-sync path** (which
sends an index, so it needs the name to be in the list) and not local rendering, which passes the string
straight to the widget. Textures outside the list therefore work locally and silently fail to replicate to a
co-op client. This corrects an earlier, broader claim that the icon tables were closed sets for all purposes.

### Why the module tracks the beacon itself

The obvious way to answer "where is the beacon" is to read the PDA widget: `mrxguipda.lua`'s
`HandleMarkerUpdate` stores `nMarkerX`/`nMarkerZ` on its `CustomData`. **That source does not update
promptly.** Measured 2026-07-26: after the player set a beacon and then cleared it, `nMarkerX` still read
`3008` — and a later reading of the same field, after another cycle, was correctly `nil`. It catches up
eventually but lags by an unknown amount, which makes it useless for "is there a beacon right now".

The **script events**, by contrast, were exact: four in a row across two cycles, in order, with the right
coordinates. So the module listens to those from load — it arms its own
[`Ess.On.script`](reactive-hotkeys#essonscript--the-shipped-games-own-script-events) listeners for
`"GPS Beacon Set"` and `"GPS Beacon Cleared"` at file scope — and keeps its own answer; the PDA fields are
consulted only as a cold-start fallback, for a beacon placed before Ess loaded, where a possibly-stale value
still beats none.

The practical consequence for `get()`: **once any beacon event has been seen, it is accurate.** Before that, a
`nil` return always means "no beacon", but a non-nil return from a cold start might be a beacon already gone.

*(Worth knowing if you go looking: `HandleMarkerUpdate` and `HandleMarkerClear`, the only corpus code that
writes those fields, are both **unbound** — absent from the `SetFlashEventHandler` block that wires the PDA's
other twelve callbacks — and yet the events fire anyway. Whatever posts them is outside the script layer, so
the corpus cannot tell you when those fields are written. That is the deeper reason to trust the events: their
behaviour is observable, the field's is not.)*

**`onSet`/`onClear` report the player's actions, not yours.** Both are the game's own script events, so they
fire for a beacon dropped in the PDA and **not** for one placed by `Ess.Gps.set`, which draws the marker
directly. Both were verified firing across two full set/clear cycles.

⚠ **The set payload's field names do not match their meaning.** It arrives as `{nX = ..., nY = ...}` and the
field called `nY` holds a **Z** coordinate. `onSet`'s `fn` receives `(x, z)` already untangled. The clear
payload carries no coordinates at all — measured as `CLEARED(nil, nil)` — so `onClear`'s `fn` takes no
arguments.

## Ess.Shop

Source: `src/58_shop.lua`. **The game's own full-screen purchase UI, driven from a mod.** This is the notable
one: not a custom-drawn menu, but the shipped stockpile/support store — a real modal Flash interface
(`store.gfx`) with item tiles, icons, prices, stock counts, an equip flow and a live cash/fuel readout —
filled with arbitrary items, with a callback when the player buys one.

The native surface is six calls that must happen in order — `Create` → `AddItem*` → `SetCallback` →
`SetCloseCallback` → `Commence`, then `Close` — each taking the player guid again, each silently returning
`false` on a wrong argument. `Ess.Shop.open` does the whole sequence and reports which step failed.

| Function | Signature | Notes |
|---|---|---|
| `open` | `Ess.Shop.open(tItems [,tOpts]) -> ok` | Builds and shows a shop in one call. Returns `false` with a reject naming the failing step. |
| `close` | `Ess.Shop.close() -> ok` | Tears it down **and repairs the player's input**. Safe when nothing is open. |
| `isOpen` | `Ess.Shop.isOpen() -> bool` | Whether a shop is registered for the local player (the wrapper's own flag). |
| `ICONS` | `Ess.Shop.ICONS` | 12 known-good item icon names. |

`Ess.Shop.ICONS` is the `supplies_*` family from `MrxSupportData`, all verified rendering live 2026-07-26.
**Not a closed set** — any loaded texture works — but an unresolvable name draws a **black box with an X**
rather than failing, so the tile still appears and the mistake is easy to miss in a list.
`"HUD_ICON_support_crate"` is deliberately absent: it sits in `mrxsupportdata.lua` alongside the twelve that
are listed, and it is the one that drew the placeholder box in testing. Proximity in the source is not
evidence that a texture resolves in this widget — test an icon before relying on it.

**The shop injects the player's three equipped support slots on top of whatever you add.** `_SetupShopFlash`
reads them from the PDA (`oPda:GetEquippedSupport(n)` for slots 1-3) and inserts them into the same item list
(`mrxguisupportshop.lua:257-271`), so your items are never the only things on screen.

### `open(tItems, tOpts)`

`tItems` is an array of item tables. **Required per item:** `sName`, `sDesc`, `sTexture`, `nCost`. An item
missing any of those is silently skipped; if *no* item is accepted, `open` closes the shop it just created and
rejects with `"no item was accepted -- each needs sName, sDesc, sTexture, nCost"`.

| Field | Native name | Default |
|---|---|---|
| `sName` | `sName` | — (required) |
| `sDesc` | `sDescription` | — (required) |
| `sTexture` | `sTexture` | — (required) |
| `nCost` | `nCashCost` | — (required) |
| `sId` | `sId` | `sName` |
| `nOwned` | `nCurrentStock` | `0` |
| `nCap` | `nMaxStock` | `99` |
| `bUnlocked` | `bUnlocked` | **`true`** (the native's own default is `false`) |
| `bNew` | `bMarkAsNew` | `false` |
| `bFuelTank` | `bFuelTank` | `false` |
| `nFuelQuantity` | `nFuelQuantity` | `nil` |
| `sRawName` | `sRawName` | `sName` |

`sId` is what the buy callback reports, so give it a stable value if `sName` is localised. `sRawName` is what
the widget matches against the player's equipped support entries to relabel them
(`mrxguisupportshop.lua:328-332`); defaulting it to `sName` is fine for custom items that are not trying to
shadow a shipped one.

`tOpts` has two entries, and the distinction matters:

- **`tOpts.onBuy(sId, nQuantity)`** — fires when the player buys. **Not** when they close.
- **`tOpts.onClose()`** — fires on close, however it happens: the button, or `Ess.Shop.close()`.

#### Five things that will cost you an hour

1. **Use the full item form for custom items.** The native has a short `AddItem` and a long `AddItemFull`, and
   the short one is **not** a convenience — it is for the game's own catalogue. `_SetupShopFlash` renders an
   item only if it has `sDesc` *and* `sTexture` *and* `nCurrentStock`, or if its `sId` is found in
   `MrxSupportData.tSupportData` (`mrxguisupportshop.lua:295`, `:311`). A short-form item with an id the game
   does not know **renders nothing, with no error.** `Ess.Shop` always uses the full form and requires
   `sDesc`/`sTexture`, so this cannot happen through it.
2. **The buy callback's arguments come *after* your callback data.** `_FlashSupportBoughtCallback` copies your
   `tCallbackData`, appends the item's `sId` and the quantity, and unpacks the lot. Passing **no** callback
   data — which is what this wrapper does — makes the signature simply `fn(sId, nQuantity)`. Same trap as
   [`Ess.On.script`](reactive-hotkeys#essonscript--the-shipped-games-own-script-events), and the same fix.
3. **A second `Create` for the same player returns `false`.** The shop is keyed by player guid in
   `_tShopList` and `Create` refuses if an entry exists (`mrxguisupportshop.lua:13`), so a shop left open
   blocks every later one. `Ess.Shop.open` closes any existing shop first rather than failing.
4. **It is modal and it can strand the player.** `_RunShop` takes control focus and toggles the HUD off
   (`mrxguisupportshop.lua:208-213`). Closing with Escape was measured to leave the player **with no game
   control**: the buy and close callbacks all fired correctly and the shop deregistered itself, but input
   never came back.
5. **The root cause is in `ReleaseControlFocus`, and it applies to any modal.** It pops the focus queue, then
   only reassigns `ControlModeManager[uOwner]` **if there is a next holder** — so draining the queue to empty
   leaves the mode flag stuck at its previous value. Measured exactly that: queue depth `0`, holder `nil`,
   mode still `true`. Anything in Ess that takes control focus and is the last holder inherits this.

**`nOwned`/`nCap` are the player's stockpile, not shelf inventory.** The native calls them `nCurrentStock` and
`nMaxStock`, which reads like "how many are for sale". They are not: they describe **how many the player
already has** and the cap on holding them — the purchase dialog labels the first one STOCKPILE and counts
upward from it as you pick a quantity. An item with `nOwned = 0` is not sold out; it is one the player owns
none of yet, and they can still buy as many as `nCap` allows. Confirmed on screen: an item added with `0` was
bought four at a time. Ess renames them so the wrong reading is not available.

A minimal shop, in the shape `Ess.Shop.open` expects:

{% raw %}
```lua
Ess.Shop.open({
    { sName = "Covert Ops Crate", sDesc = "A crate of covert supplies.",
      sTexture = "supplies_covert", nCost = 5000, sId = "ess_covert", nCap = 8 },
    { sName = "Anti-Tank Crate",  sDesc = "For when the problem has armour.",
      sTexture = "supplies_anti_tank", nCost = 12000, sId = "ess_at", bNew = true },
}, {
    onBuy   = function(sId, nQty) Ess.Log("bought " .. tostring(sId) .. " x" .. tostring(nQty)) end,
    onClose = function() Ess.Log("shop closed") end,
})
```
{% endraw %}

*(The shape above matches the confirmed item/opts contract; the live end-to-end confirmation was a purchase of
`ess_covert x4`, which is where that id comes from. The exact snippet is not itself a recorded test script —
there is no recipe file for `Ess.Shop`, see [Status](#status).)*

### `close()` — the escape hatch

`Ess.Shop.close()` does more than call the native, **because the native alone is not enough to get unstuck**.
That was established the hard way on 2026-07-26, when closing a test shop with Escape left the player with no
game control and `MrxGuiSupportShop.Close` could not help — it returns early unless `_tShopList` still has an
entry, and by then it did not.

Three separate pieces of state outlive the widget, and `close()` repairs all three:

1. **`LTILibName.ChangeShellState(true)`**, set by `_RunShop` and never cleared —
   `mrxguisupportshop.lua` contains **exactly one** call to it (line 217), while `mrxbriefing.lua` balances
   its pairs properly. `close()` calls the matching `false`.
2. **`ControlModeManager`**, the real culprit described above. `close()` clears the stale flag — calling
   `SetDialogBoxMode(p, false)` or `SetSupportMenuMode(p, false)` as appropriate, then nilling the entry.
3. **The HUD**, toggled off by `_RunShop` and restored only on the normal path. `close()` calls
   `MrxGuiManager.ToggleHud(p, true)`.

⚠ **The `ControlModeManager` repair is deliberately conditional.** It only fires when the focus queue is
actually empty, which is what makes a leftover flag provably stale. Clearing it unconditionally would stamp on
a legitimate holder — a dialog box, the support menu — that is genuinely mid-interaction.

**Calling `close()` when nothing is open is valid and supported.** That is the point: it is the rescue call,
not just the teardown call.

### On tiering: there is no `Ess.Easy.Shop`

Deliberately. Per the source's own reasoning: the [Easy tier](index#the-three-tiers) is for verbs a beginner
reaches for constantly (mark this, spawn that); a modal storefront is a niche, deliberate thing to build, and
a one-liner preset would mostly hide the item table — which *is* the content. `Ess.Shop.open` is already the
whole six-call native sequence collapsed into one call, so the Core tier is doing that job.

## See also

- [Markers](mark) — `Ess.Mark` / `Ess.Raw.Mark`, the multi-surface marking layer whose PDA blips
  `Ess.Pda.blip` extends. The `icon_yellow_mc` finding above is why those blips had never been visible.
- [Tracking & Cleanup](tracking#esstrack) — `Ess.Track:pda(sName)`, the automatic teardown `Ess.Pda.blip`
  deliberately does not do for you.
- [Sound & HUD](sound-hud) — `Ess.Hud`, the same `_G.Hud = HudInterface` published-global surface these
  namespaces sit alongside.
- [Contracts](contract) — the obvious consumer of `Ess.Pda.mission`: a contract that registers as a real,
  trackable PDA mission rather than a loose blip.
- [Reactive Hooks & Hotkeys](reactive-hotkeys#essonscript--the-shipped-games-own-script-events) —
  `Ess.On.script`, the 0.5.0 sibling that `Ess.Gps` is built on and that shares the shop callback's
  argument-order trap.
- [Core Primitives](core) — [`Ess.Safe`](core#esssafe) and
  [`Ess.DEBUG`](core#essdebug--two-channels-of-silence), the channel every guard rejection on this page
  reports to, and [`Ess.Color`](core#esscolor), which these namespaces deliberately do not use.
- [Pursuit & Wanted System](pursuit#status) — a sibling focused-namespace page, and the contrast worth
  drawing: it has a repeatable smoke recipe behind it, and this cluster does not.
