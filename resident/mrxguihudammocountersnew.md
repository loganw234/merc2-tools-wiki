---
title: MrxGuiHudAmmoCountersNew
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud, ammo]
verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- no OnActivate/Create/tInstance anywhere in source)
---

# MrxGuiHudAmmoCountersNew

*Module: mrxguihudammocountersnew.lua*

## Overview
The `MrxGuiHudAmmoCountersNew` module is responsible for managing the display and animation of ammo counters in the HUD. It handles various events related to weapon and explosive ammo updates, manages color animations, and controls widget visibility and rotation animations.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase`

## Instance pattern
**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry anywhere
in source. This is one shared HUD element, not something spawned per world object — the fields below are
plain module-level state. Key fields:
- `_knPulseTime`: 0.4 seconds, used for color pulse animations.
- `_knRotateTime`: 0.5 seconds, used for rotation animations.
- `_knRotateDelay`: 0.05 seconds, delay before starting rotation animations.
- `bSuppressAnimation`: Boolean flag to suppress animations.
- `tEventHandlers`: Table to store event handlers.
- `nLastGunSwitchTime`: Timestamp of the last gun switch event.
- `nLastExplosiveSwitchTime`: Timestamp of the last explosive switch event.
- `uCurrentGun`: GUID of the currently equipped weapon.
- `uNewWeapon`: GUID of the new weapon being switched to.
- `bWaitingForSupport`: Boolean flag indicating if waiting for support before switching weapons.

## Functions

### Min(nA, nB)
Returns the minimum of two numbers `nA` and `nB`.

### HandleCurrentGunAmmoUpdateEvent(oWidget, tEvent)
Updates the current ammo count for the primary weapon in the HUD widget based on the event data. It also handles low-ammo threshold logic and color animation.

### _PulseToRed(oWidget, nSpeed)
Animates the widget's color to red over a specified speed.

### _PulseToNeutral(oWidget, nSpeed)
Animates the widget's color back to neutral (original) over a specified speed.

### HandleCurrentGunClipSizeUpdateEvent(oWidget, tEvent)
Updates the clip size for the primary weapon in the HUD widget based on the event data.

### HandleStoredGunAmmoUpdateEvent(oWidget, tEvent)
Updates the stored ammo count for the primary weapon in the HUD widget based on the event data.

### HandleUnreloadableGunAmmoUpdateEvent(oWidget, tEvent)
Handles the display of ammo for weapons that cannot be reloaded.

### HandleExplosivesAmmoUpdateEvent(oWidget, tEvent)
Updates the total explosives ammo count in the HUD widget based on the event data and handles low-ammo threshold logic and color animation.

### HandleTopLevelUpdateEvent(oWidget, nDeltaTime)
Handles the visibility timing for the top-level HUD widget based on delta time.

### HandleTopLevelGunAmmoUpdateEvent(oWidget, tEvent)
Updates the cached ammo values for the primary weapon in the custom data of the widget.

### HandleTopLevelExplosiveAmmoUpdateEvent(oWidget, tEvent)
Updates the cached ammo values for explosives in the custom data of the widget.

### HandleTopLevelInitialization(oWidget, tEvent)
Initializes the top-level HUD widget by setting up child widgets and their behaviors.

### _SetSuppressAnimation(oWidget, bSuppress)
Sets whether the animation should be suppressed for the widget.

### HandleGunShowEvent(oWidget, tEvent)
Handles the display of the primary weapon ammo based on the event data.

### HandleExplosiveShowEvent(oWidget, tEvent)
Handles the display of explosives ammo based on the event data.

### _ShowForDuration(oWidget, nDuration)
Sets the widget to be visible for a specified duration or indefinitely if no duration is provided.

### HandleGunSwitchEvent(oWidget, tEvent)
Handles the switch event for the primary weapon in the HUD widget.

### _NameDelay(oName)
Delays the visibility of the name label after it becomes visible.

### HandleExplosiveSwitchEvent(oWidget, tEvent)
Handles the switch event for explosives in the HUD widget.

### FindEquippedSupportTexture(uPlayer)
Returns `nil` (no support texture found).

### HandleE3HudModeEvent(oWidget, tEvent)
Handles the E3 HUD mode event by toggling the visibility of certain widgets.

### _SetUpFadeBehavior(oWidget)
Sets up fade behavior for the widget, including animation points and initial visibility settings.

### _GreenFade(oWidget)
Animates the widget's color to green over 2 seconds.

### _PerformIconSwitchAnimation(oWidget, uNewCurrentGun)
Performs an icon switch animation for the weapon icon in the HUD widget.

### _SwitchTexture(oWidget)
Switches the texture of the weapon icon based on the new texture provided.

### _SetUpFlippingPoints(oWidget)
Sets up flipping points for the widget to enable smooth animations.

### _AnimateFrameClose(oWidget, fCallback, tCallbackData)
Animates the frame closing with a callback function and data.

### _AnimateFrameOpen(oWidget)
Animates the frame opening and sets text visibility.

### _SetTextVisible(oUnused, oWidget, bVisible)
Sets the visibility of text widgets based on the provided boolean.

### _InitializeRotationAnimation(oWidget)
Initializes the rotation animation for a widget's children. It sets up each child image with an original rotation and adds an animation point to rotate by 180 degrees in either direction based on its index.

### _AnimateBackgroundRotation(oWidget)
Animates the background rotation of a widget. It retrieves the second child, animates it to a predefined point, and schedules the next animation step using a timer event.

### _AnimateNext(oWidget, nIndex)
Handles the sequential animation of widgets' children. It animates each child to its respective point and schedules the next animation if not at the last child.

### HandleGunSwitchForAnimation(oWidget, tEvent)
Handles the weapon switch animation when a new gun is selected. If suppression is active, it sets up for support; otherwise, it begins the weapon switch animation.

### HandleExplosiveSwitchForAnimation(oWidget, tEvent)
Handles the weapon switch animation when a new explosive is selected by calling `_BeginWeaponSwitchAnimation`.

### _WeaponSwitchAccessor(oWidget, uNewWeapon)
Accesses and starts the weapon switch animation if waiting for support.

### _BeginWeaponSwitchAnimation(oWidget, uNewWeapon)
Begins the process of switching weapons. It sets up event handlers, initializes animation states, and animates bullets and icons accordingly.

### _SetUpCustomTextVisibility(oWidget)
Sets up custom visibility handling for widgets by replacing their `SetVisible` method with a custom function `_CustomSetVisible`.

### _CustomSetVisible(oWidget, bVisible)
A custom visibility setter that respects suppression flags to prevent unintended visibility changes.

### _UpdateControllingWidget(oWidget, nDeltaTime)
Updates the controlling widget's animation state based on delta time. It animates bullets and icons at specific points in the timeline and handles the final frame animation.

### _AnimateBullet(oBullets, nNumber)
Animates a bullet by rotating it to its predefined point.

### _PassedPoint(nPreviousValue, nNewValue, nPoint)
Checks if a given point has been passed between two values, considering both increasing and decreasing scenarios.

## Events

- **`Event.CurrentGunAmmoUpdate`**: Triggered when the current ammo count for the primary weapon changes. The module updates the HUD widget's ammo display and handles low-ammo threshold logic.
  
- **`Event.CurrentGunClipSizeUpdate`**: Triggered when the clip size for the primary weapon changes. The module updates the HUD widget's clip size display.

- **`Event.StoredGunAmmoUpdate`**: Triggered when the stored ammo count for the primary weapon changes. The module updates the HUD widget's stored ammo display.

- **`Event.UnreloadableGunAmmoUpdate`**: Triggered when the ammo count for a weapon that cannot be reloaded changes. The module handles the display of this ammo.

- **`Event.ExplosivesAmmoUpdate`**: Triggered when the total explosives ammo count changes. The module updates the HUD widget's explosives ammo display and handles low-ammo threshold logic.

- **`Event.TopLevelUpdate`**: Triggered periodically with delta time. The module handles the visibility timing for the top-level HUD widget.

- **`Event.TopLevelGunAmmoUpdate`**: Triggered when cached ammo values for the primary weapon need to be updated in the custom data of the widget.

- **`Event.TopLevelExplosiveAmmoUpdate`**: Triggered when cached ammo values for explosives need to be updated in the custom data of the widget.

- **`Event.TopLevelInitialization`**: Triggered during the initialization of the top-level HUD widget. The module sets up child widgets and their behaviors.

- **`Event.GunShow`**: Triggered when the primary weapon ammo needs to be displayed based on event data.

- **`Event.ExplosiveShow`**: Triggered when explosives ammo needs to be displayed based on event data.

- **`Event.GunSwitch`**: Triggered when a new gun is selected. The module handles the switch event for the primary weapon in the HUD widget.

- **`Event.ExplosiveSwitch`**: Triggered when a new explosive is selected. The module handles the switch event for explosives in the HUD widget.

- **`Event.E3HudMode`**: Triggered to handle the E3 HUD mode event by toggling the visibility of certain widgets.

## Notes for modders

- **Call-order requirements**: Ensure that `HandleTopLevelInitialization` is called before any other initialization functions to properly set up child widgets and their behaviors.
  
- **Pitfalls**: Be cautious with modifying animation speeds or durations, as they can affect the overall user experience. Avoid directly manipulating widget properties outside of designated functions to maintain consistency.

- **Tunables**: The constants `_knPulseTime`, `_knRotateTime`, and `_knRotateDelay` control various animation timings. Modifying these values can change the behavior of color animations and rotations.

- **Decompiler artifacts**: There are no known decompiler artifacts in this module that require special attention. All functions and variables appear to be correctly defined and used within the context of the module.