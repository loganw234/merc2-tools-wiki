---

title: MrxGuiHudReticle

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, hud]

verified: true
verified_note: 'deeper pass: CORRECTED imports (source imports only MrxGui — MrxUtil/Sound were wrong; Sound is a namespace, not an import); DELETED fabricated Events section (zero Event.* calls — all wiring is SetEventHandler widget-event keys); surfaced Stinger lock-on constants (flash times, neutral/lockon colors, med/high thresholds, targeting sound), the health pie-slice geometry, target-relation colors, and the sReticleType values ("Normal"/"Homing"/"Laser"/"None"); noted the empty _MoveCrosshairChildToPoint stub'

---



# MrxGuiHudReticle



*Module: mrxguihudreticle.lua*



## Overview

The `MrxGuiHudReticle` module is responsible for managing the various types of reticles used in the game's heads-up display (HUD). It handles events related to reticle color changes, position updates, and type switches. The module also manages health bars and crosshairs associated with these reticles.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxGui` only (via [`import("MrxGui")`](../glossary#importname)). It also calls the [Gui](../namespaces/gui) namespace (`Gui.GetReticlePosition`, `Gui.LoadTexture`), [Sound](../namespaces/sound) (`Sound.CueSound`/`StopSound`), and the internal `_GuiInternal` singleton — but those are namespaces, not `import()`s.

{: .note }
> The earlier draft listed `Imports: MrxUtil, Sound`. **Neither is imported** — the only `import()` is `MrxGui`, and `Sound`/`Gui` are engine namespaces. Corrected.

## Instance pattern

**Stateless module + per-widget `CustomData`.** No `tInstance`/metatable. The module hosts several *distinct* reticle widget types (normal reticle, crosshair, circular + straight health bars, Stinger lock-on, laser), each with its own `Handle*Initialization` that stashes child-widget references and animation points in that widget's `CustomData` and copies methods onto it (e.g. `oWidget.SetHealth = _SetHealth`, `oWidget.SetOwner = SetReticleOwner`). Module-level names are just the constants below plus two `local` tables (`_tSpread`, and the color/threshold constants).

### Module constants (the tunables)
- `_bFloatCrosshair = false` — if true, the crosshair follows the passed `nScreenX/Y`; if false it snaps to `Gui.GetReticlePosition`.
- `_ksTargettingSound = "ui_HUD_SAM_targeting"` — looping Stinger lock-on beep (via [Sound](../namespaces/sound)).
- **Reticle screen mapping**: aim coords map to screen via `320 + aimX*320`, `240 - aimY*240` (640×480 virtual canvas). Crosshair spread base is `320` per unit (`_tSpread` gives the four arm directions).
- **Circular health pie** (`HandleHealthInitialization`): `_nHealthLength = 100`, `_nHalfHealthLength = 50`, `_nHealthCenter = 180` (degrees), `_nBaseAlpha = 80` (visible translucency). Rendered with `SetPieSliceRender`.
- **Target-relation colors** (`HandleReticleColorChangeEvent`): friendly (`nTargetRelation > 0`) = blue `(0,0,255)`, hostile (`< 0`) = red `(255,0,0)`, neutral/none = white `(255,255,255)`.
- **Stinger lock-on flash** (`HandleStingerReticleDataUpdate`/`Update`): flash times `_kNoFlashTime = -1` (solid, at 100% lock), `_kSlowFlashTime = 0.15`, `_kMedFlashTime = 0.15`, `_kFastFlashTime = 0.01`; progress thresholds `_kMedBegin = 0.4`, `_kHighBegin = 0.75`; colors `_ktNeutralColor = (128,128,128)`, `_ktLockonColor = (0,255,0)`. Target texture `global_gui_reticle_stinger_target`.
- **Reticle types** (`tEvent.sReticleType` string): `"Normal"`, `"Homing"`, `"Laser"`, `"None"` — select which reticle widget shows.
- **Laser reticle**: arrow spins one full turn (`nRotation = 359`); enter/exit fade to translucency `128`/`0` over `0.5`s; circles play frames `0..30`.



## Functions



### HandleReticleColorChangeEvent(oWidget, nTargetRelation, nScreenX, nScreenY, nSpreadX, nSpreadY, nHealth, nMaxHealth)

Handles color changes of the reticle based on the target's relation and health. Sets the widget and its parent's color accordingly. Updates the custom data with spread and health information.



### HandleReticleGunSwitchEvent(oWidget, tEvent)

Handles changes in the reticle type (e.g., "Homing", "Normal", "None"). Adjusts the visibility, texture, and crosshair settings of the widget based on the new reticle type.



### HandleReticleInitialization(oWidget)

Initializes the reticle by setting its owner and event handlers. Moves the reticle to the initial position and sets up custom data for spread and health.



### HandleReticlePositionChange(oWidget, tEvent)

Handles changes in the reticle's position. Updates the widget's location based on the new position provided in the event or retrieves it from the engine.



### _MoveReticle(oWidget, nAimX, nAimY)

Moves the reticle to a specified aim position by adjusting its location.



### HandleCrosshairInitialization(oWidget)

Initializes the crosshair by setting up offsets for each child widget and linking them to the parent's health widgets. Sets up event handlers and initial positions.



### _MoveCrosshairChildToPoint(oChild, nXOffset, nYOffset, nTime, nIndex)

(Placeholder function) Intended to move a crosshair child to a specified point with interpolation over time.



### Interpolate(nFrom, nTo, nRatio)

Interpolates between two values based on a given ratio. Returns the interpolated value.



### HandleCrosshairUpdate(oWidget, nDt)

Updates the position and spread of the crosshair children based on the current set and current positions, interpolating over time.



### HandleHealthInitialization(oWidget)

Initializes health rendering for circular health bars by setting up pie slice render settings and custom data for animation points.



### _SetHealth(oWidget, nCurrent, nMax)

Sets the health value of a circular health bar. Handles fading in and out based on the current and maximum health values.



### _ForceHideHealth(oWidget)

Forces the health bar to fade out completely.



### _HealthFadeInEnd(oWidget)

Callback function for when the health bar's fade-in animation ends.



### HandleHealthInitializationBar(oWidget)

Initializes health rendering for straight health bars by setting up location and custom data for animation points.



### _SetHealthStraight(oWidget, nCurrent, nMax)

Sets the health value of a straight health bar. Handles fading in and out based on the current and maximum health values.



### SetReticleOwner(oWidget, uGuid)

Sets the owner of the reticle widget and updates its position based on the new owner's aim position.



### HandleStingerReticleInitialization(oWidget, tData)

Initializes the Stinger lock-on reticle by setting up custom data for flashing and health. Loads the target texture and sets initial colors.



### HandleStingerReticleColorChangeEvent(oWidget, nTargetRelation, nScreenX, nScreenY, nSpreadX, nSpreadY, nHealth, nMaxHealth)

Updates the health of the Stinger lock-on reticle based on the provided data.



### HandleStingerReticleDataUpdate(oWidget, tData)

Handles updates to the Stinger lock-on reticle's data. Adjusts flashing behavior and colors based on the percentage of lock-on progress. Updates the position of the targeting reticle.



### HandleStingerReticleUpdate(oWidget, nDeltaTime)

This function handles the update logic for a stinger reticle widget. It increments a frame counter and checks if the widget has gone too long without an update. If so, it sets the widget's color to neutral, hides it, and stops any looping sounds. It also manages the flashing effect by toggling the widget's color between lock-on and neutral colors based on a timer.



### HandleStingerReticleGunSwitchEvent(oWidget, tEvent)

This function handles events related to switching the stinger reticle type. If the event specifies a "Homing" reticle, it makes the stinger reticle visible, hides any targetting reticle, and updates its radius and dimensions if provided in the event data. For other reticle types, it hides the stinger reticle and stops any looping sounds.



### SetStingerReticleRadius(oWidget, nRadius)

This function sets the radius of a stinger reticle widget by adjusting its coordinates to form a square centered at the widget's current position.



### SetStingerReticleDimensions(oWidget, nWidth, nHeight)

This function sets the dimensions (width and height) of a stinger reticle widget. It calculates new coordinates for the widget and its child widgets based on the provided width and height, ensuring that the health bar is scaled proportionally.



### HandleLaserReticleInitialization(oWidget)

This function initializes a laser reticle widget by setting up its children (circles and an arrow) with animation points and initializing other custom data fields. It also disables the reticle initially.



### HandleLaserReticleGunSwitchEvent(oWidget, tEvent)

This function handles events related to switching the laser reticle type. If the event specifies a "Laser" reticle, it makes the laser reticle visible, starts its animation, and snaps it to neutral position. For other reticle types, it disables the laser reticle.



### HandleLaserReticleStateChangeEvent(oWidget, tEvent)

This function handles state change events for the laser reticle. If the event indicates that the reticle is active with a specific time, it animates the reticle accordingly. Otherwise, it snaps the reticle to its neutral position.



### _LaserReticleDisable(oWidget)

This helper function disables the laser reticle by snapping it to neutral position, hiding it, and setting its enabled state to false.



### _LaserReticleAnimate(oWidget, nTime)

This helper function animates the circles of a laser reticle widget. It plays an animation for each circle and calls another helper function to animate the arrow.



### _LaserReticleAnimateArrow(oWidget, nTime)

This helper function animates the arrow of a laser reticle widget. If the time is negative, it stops the arrow's animation. Otherwise, it sets the arrow's rotation and starts its animation loop.



### _LaserReticleSnapToNeutral(oWidget)

This helper function snaps the circles and arrow of a laser reticle widget to their neutral positions by halting any animations and setting them to their initial frames.



### _LaserReticleArrowLoop(oArrow)

This helper function loops the arrow's animation by resetting its rotation and starting it again.



## Events

{: .warning }
> **This file has zero `Event.*` engine calls** (grep-confirmed). The earlier draft listed `Event.ReticleColorChange`, `Event.ReticleGunSwitch`, `Event.StingerReticleUpdate`, `Event.LaserReticleStateChange`, and ~11 others — **none of these engine constants exist in the source.** Removed. The `Handle*Event` functions are **widget event-handler callbacks**, wired to named widget events in the HUD layout, not `Event.Create` subscriptions.

Real widget-handler registrations found in this file (via `SetEventHandler`, a widget `EventHandlers` key — not `Event.*`):
- `HandleReticleInitialization` sets `"GuiReticlePositionChange"` → `HandleReticlePositionChange`.
- `HandleCrosshairInitialization` sets `"GuiUpdate"` → `HandleCrosshairUpdate` (crosshair position/spread interpolation).
- `HandleStingerReticleDataUpdate` sets `"GuiUpdate"` → `HandleStingerReticleUpdate` (drives the lock-on flash, and self-clears the handler after a frame with no data update).

Everything else (`HandleReticleColorChangeEvent`, `HandleReticleGunSwitchEvent`, the `Stinger*`/`Laser*` handlers, and the various `*Initialization` functions) is invoked by the framework by handler-key convention wired in a layout file, or called directly — no `SetEventHandler` call site for them exists in *this* file. The gun-switch handlers key off the `tEvent.sReticleType` string (`"Normal"`/`"Homing"`/`"Laser"`/`"None"`).

## Notes for modders

- **Change the aim-to-screen mapping** by editing the `320 + aimX*320` / `240 - aimY*240` math in `_MoveReticle`/`SetReticleOwner`/`HandleCrosshairUpdate` — this assumes a 640×480 virtual HUD canvas. `Gui.GetReticlePosition(owner)` returns aim in −1..1 units.
- **Stinger lock-on feel**: the beep speeds up as lock progresses — `_kSlowFlashTime` below `_kMedBegin` (40%), `_kMedFlashTime` at `_kMedBegin`, `_kFastFlashTime` above `_kHighBegin` (75%), then solid green (`_ktLockonColor`) with the loop sound stopped at 100%. Adjust the thresholds/times to re-tune SAM lock urgency. The looping cue is `_ksTargettingSound = "ui_HUD_SAM_targeting"`.
- **Health bar styles**: two implementations — circular pie-slice (`HandleHealthInitialization`/`_SetHealth`, arc centered at `_nHealthCenter = 180°`, span `_nHealthLength = 100`) and straight bar (`HandleHealthInitializationBar`/`_SetHealthStraight`). The reticle picks between them per gun via `tEvent.sReticleHealthType == "straight (bottom)"`. Base opacity is `_nBaseAlpha = 80`; both fade out over `0.5`s when health is unavailable (`nCurrent < 0` or `nMax <= 0`).
- **Crosshair float**: set `_bFloatCrosshair = true` to let the crosshair track a passed screen position (`nScreenX/Y`) instead of snapping to the engine reticle position — useful for free-aim weapons.
- **`_MoveCrosshairChildToPoint(oChild, ...)` is an empty stub** (`function ... end`) — it does nothing; the actual crosshair movement is done inline in `HandleCrosshairUpdate` via `Interpolate` (rate `nDt * 5`). Don't call the stub.