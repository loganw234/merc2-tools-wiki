---
title: MrxGuiHudAmmoCountersNew
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud, ammo]
verified: true
verified_note: 'deeper pass: rewrote the Events section — the Handle*Event functions are widget event-handler callbacks (wired via SetEventHandler / the layout), NOT Event.Create(Event.*) subscriptions; the only real Event.* calls are Event.Post("Ammo low"/"Ammo not low") and Event.Create(Event.TimerRelative, ...). Surfaced the native HUD field names read (PrimaryCurrentAmmo/PrimaryClipSize/PrimaryStoredAmmo/ExplosivesCurrentAmmo/ExplosivesStoredAmmo), the low-ammo threshold (clip/3), and the red-pulse RGB (216,16,16). All functions re-confirmed.'
---

# MrxGuiHudAmmoCountersNew

*Module: mrxguihudammocountersnew.lua*

## Overview
The `MrxGuiHudAmmoCountersNew` module drives the HUD ammo counters — the numeric clip/stored-ammo readouts, the low-ammo red pulse, the weapon-name label, and the animated weapon-icon "switch" flip/rotate effect. Every function is a **widget event-handler callback**: it receives an `oWidget` (the counter widget) and a `tEvent` table of native HUD ammo fields, updates the widget's text/color/animation, and returns. The module is stateless at module level; all per-counter state lives in `oWidget.CustomData`.

The `tEvent` tables carry native HUD fields the engine fills in: `PrimaryCurrentAmmo`, `PrimaryClipSize`, `PrimaryStoredAmmo` (guns) and `ExplosivesCurrentAmmo`, `ExplosivesStoredAmmo` (grenades/explosives). A value of `-1` means "not applicable" and blanks the readout.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase` (via [`import("MrxGuiBase")`](../glossary#importname)) — used for `MrxGuiBase.PushWidgetToFront`, `MrxGuiBase.RemoveWidgetWithChildren`, `MrxGuiBase.AddWidgetWithChildren`. See [MrxGuiBase](mrxguibase).

## Instance pattern
**Stateless module + per-widget `CustomData`.** There is no `OnActivate`/`Create`/`tInstance` registry and no `setmetatable` instance pattern. The module defines only three module-level constants (below); all mutable state is stored on the individual counter widgets in `oWidget.CustomData`. The functions never touch module globals for state — they read/write `oWidget.CustomData.*` and `oWidget:GetChildren()`. Per-widget state you'll see in the code includes `.bAnimating`, `.nRedPoint`/`.nNeutralPoint` (color animation points), `.nCachedClipAmmo`/`.nCachedClipSize`/`.nCachedStoredAmmo`, `.nVisibilityTime`/`.nRemainingVisibleTime`, `.bHaveWeapon`, `.bWaitingForSupport`, and `.bSuppress`.

Module-level constants (the only three top-level names, and the real tunables):
- `_knPulseTime = 0.4` — seconds for the low-ammo red-pulse color animation.
- `_knRotateTime = 0.5` — seconds for each bullet/background rotation step in the weapon-switch animation.
- `_knRotateDelay = 0.05` — delay between successive rotation steps (scheduled via `Event.Create(Event.TimerRelative, ...)`).

{: .note }
> The earlier draft listed module-level fields like `bSuppressAnimation`, `tEventHandlers`, `nLastGunSwitchTime`, `uCurrentGun`, `uNewWeapon`, `bWaitingForSupport`. **None of those exist in the source** — the analogous flags live in `oWidget.CustomData` (e.g. `.bSuppress`, `.bWaitingForSupport`, `.uNewWeapon`). Removed.

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

{: .warning }
> The `Handle*Event` functions in this file are **widget event-handler callbacks, not `Event.Create(Event.*)` subscriptions.** There is no `Event.Create` for any ammo update in this source. The engine/layout drives these by calling the widget's registered handler for a named widget event (see `oWidget:SetEventHandler("GuiUpdate", ...)` in the code) — the handler *names* (e.g. `HandleCurrentGunAmmoUpdateEvent`) are wired to widget events in the HUD layout file, not here. Do not expect a global `Event.CurrentGunAmmoUpdate` engine constant to exist.

The **only real `Event.*` engine calls** in the file are:
- `Event.Post("Ammo low", {uPlayer = oWidget:GetOwner()})` and `Event.Post("Ammo not low", {...})` — posted from `HandleCurrentGunAmmoUpdateEvent` when the primary clip crosses the low-ammo threshold (`PrimaryClipSize / 3`). Other modules can subscribe to these two string events. See [Event](../namespaces/event).
- `Event.Create(Event.TimerRelative, {_knRotateDelay}, _AnimateNext, {...})` — schedules the staggered bullet-rotation steps of the weapon-switch animation.

The widget-event handler callbacks (invoked with `(oWidget, tEvent)` or `(oWidget, nDeltaTime)`) and the native HUD fields they read:
- **Current-gun ammo / clip / stored** (`HandleCurrentGunAmmoUpdateEvent`, `HandleCurrentGunClipSizeUpdateEvent`, `HandleStoredGunAmmoUpdateEvent`) — read `tEvent.PrimaryCurrentAmmo`, `tEvent.PrimaryClipSize`, `tEvent.PrimaryStoredAmmo`. Blank (`" "`) when the value is `-1` (or clip size `0`).
- **Unreloadable gun** (`HandleUnreloadableGunAmmoUpdateEvent`) — shows `PrimaryCurrentAmmo` when `PrimaryClipSize` is `-1`/`0` (weapons with no clip).
- **Explosives total** (`HandleExplosivesAmmoUpdateEvent`) — shows `ExplosivesCurrentAmmo + ExplosivesStoredAmmo`; red-pulses when the total is `<= 0`.
- **Top-level cache/visibility** (`HandleTopLevelGunAmmoUpdateEvent`, `HandleTopLevelExplosiveAmmoUpdateEvent`, `HandleTopLevelUpdateEvent`, `HandleTopLevelInitialization`) — cache ammo into `CustomData`, drive the 3-second auto-hide fade, and build the child widgets.
- **Show / switch** (`HandleGunShowEvent`, `HandleExplosiveShowEvent`, `HandleGunSwitchEvent`, `HandleExplosiveSwitchEvent`, `HandleGunSwitchForAnimation`, `HandleExplosiveSwitchForAnimation`) — show for a duration and play the weapon-icon flip animation. `HandleGunSwitchEvent` reads `tEvent.uNewCurrentGun`/`tEvent.uNewCurrentGunGuid` and pulls the display name via `Object.GetLocalizedName`.
- **E3 demo mode** (`HandleE3HudModeEvent`) — reads `tEvent.bOn`; strips/restores the first two child widgets for the E3 press-build HUD.

## Notes for modders

- **Low-ammo threshold** (the key tunable): the counter pulses red when `PrimaryCurrentAmmo < PrimaryClipSize / 3` (guns) or when the explosives total is `<= 0`. That same `/3` threshold also forces the counter to stay visible indefinitely (`nDuration = -1` in `_ShowForDuration`). Change the divisor to re-tune when "low ammo" triggers.
- **Red-pulse color**: the pulse animates to RGB `(216, 16, 16)` (`RedLevel`/`GreenLevel`/`BlueLevel` in the `nRedPoint` animation point) and back to the widget's original color. `_GreenFade` (used elsewhere) flashes `(0, 216, 0)`.
- **Auto-hide timing**: `CustomData.nVisibilityTime` is set to `3` (seconds) in `_SetUpFadeBehavior` — how long the counter stays up after a change before fading. Passing `nDuration = -1` (or a low clip) keeps it up permanently; `0` hides immediately.
- **"Ammo low" / "Ammo not low" events**: subscribe to these string events (via [Event](../namespaces/event)) to react to the player's primary weapon running low — they carry `uPlayer`. Only the primary gun posts them; explosives do not.
- **Animation timing constants**: `_knPulseTime` (0.4s), `_knRotateTime` (0.5s), `_knRotateDelay` (0.05s) — see Instance pattern. Lowering `_knRotateDelay` tightens the bullet-rotation cascade in the switch animation.
- **`FindEquippedSupportTexture(uPlayer)` is a stub** — it unconditionally `return nil`. Nothing in this file uses a support texture; treat it as dead/placeholder.
- **E3 HUD mode** (`HandleE3HudModeEvent`) is a demo-only path that removes the counter's first two children — irrelevant to normal play.