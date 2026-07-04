---

title: MrxGuiHudReticle

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, hud]

verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- no OnActivate/Create/tInstance anywhere in source)

---



# MrxGuiHudReticle



*Module: mrxguihudreticle.lua*



## Overview

The `MrxGuiHudReticle` module is responsible for managing the various types of reticles used in the game's heads-up display (HUD). It handles events related to reticle color changes, position updates, and type switches. The module also manages health bars and crosshairs associated with these reticles.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxUtil`, `Sound`



## Instance pattern

**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry
anywhere in source. This is one shared reticle element, not something spawned per world object. Key
fields:

- `_bFloatCrosshair`: A boolean flag indicating whether the crosshair should float or follow the reticle position.

- `_ksTargettingSound`: The sound cue ID for the targeting sound used in Stinger lock-on reticles.

```



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



- **`Event.ReticleColorChange`**: Triggered when the reticle's color needs to be changed based on target relation and health. The module handles this event with `HandleReticleColorChangeEvent`.

  

- **`Event.ReticleGunSwitch`**: Triggered when the reticle type changes (e.g., "Homing", "Normal", "None"). The module handles this event with `HandleReticleGunSwitchEvent`.



- **`Event.ReticleInitialization`**: Triggered to initialize the reticle. The module handles this event with `HandleReticleInitialization`.



- **`Event.ReticlePositionChange`**: Triggered when the reticle's position changes. The module handles this event with `HandleReticlePositionChange`.



- **`Event.CrosshairInitialization`**: Triggered to initialize the crosshair. The module handles this event with `HandleCrosshairInitialization`.



- **`Event.CrosshairUpdate`**: Triggered to update the crosshair's position and spread. The module handles this event with `HandleCrosshairUpdate`.



- **`Event.HealthInitialization`**: Triggered to initialize health rendering for circular health bars. The module handles this event with `HandleHealthInitialization`.



- **`Event.StingerReticleInitialization`**: Triggered to initialize the Stinger lock-on reticle. The module handles this event with `HandleStingerReticleInitialization`.



- **`Event.StingerReticleColorChange`**: Triggered when the Stinger lock-on reticle's color needs to be updated based on target relation and health. The module handles this event with `HandleStingerReticleColorChangeEvent`.



- **`Event.StingerReticleDataUpdate`**: Triggered to update data for the Stinger lock-on reticle, such as flashing behavior and colors. The module handles this event with `HandleStingerReticleDataUpdate`.



- **`Event.StingerReticleUpdate`**: Triggered to handle updates for the Stinger lock-on reticle widget. The module handles this event with `HandleStingerReticleUpdate`.



- **`Event.LaserReticleInitialization`**: Triggered to initialize a laser reticle widget. The module handles this event with `HandleLaserReticleInitialization`.



- **`Event.LaserReticleGunSwitch`**: Triggered when the laser reticle type changes. The module handles this event with `HandleLaserReticleGunSwitchEvent`.



- **`Event.LaserReticleStateChange`**: Triggered to handle state change events for the laser reticle. The module handles this event with `HandleLaserReticleStateChangeEvent`.



## Notes for modders



- **Call-order requirements**: Ensure that initialization functions (`HandleReticleInitialization`, `HandleCrosshairInitialization`, etc.) are called before any other related functions to properly set up the reticle and its components.



- **Pitfalls**: Be cautious when modifying reticle behavior, as incorrect handling of events or state changes can lead to visual inconsistencies or performance issues. Always test changes in a controlled environment.



- **Tunables**: The module uses several tunable parameters such as `_bFloatCrosshair` and `_ksTargettingSound`. Modders can adjust these values to customize reticle behavior without altering the core logic.



- **Decompiler artifacts**: Some functions, like `_MoveCrosshairChildToPoint`, are placeholders with no implementation. These should be treated as decompiler artifacts and not relied upon for functionality.