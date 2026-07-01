---
title: MrxGuiHudDamageIndicator
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
---

# MrxGuiHudDamageIndicator

*Module: mrxguihuddamageindicator.lua*

## Overview
The `MrxGuiHudDamageIndicator` module is responsible for displaying directional "took damage" fading arcs on the HUD, centered on the reticle widget. These arcs indicate the direction and amount of damage received by the player's controlled object.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGui`

## Instance pattern
This is a stateless manager/utility module (no per-instance table). It does not maintain any persistent state but manages HUD widgets dynamically in response to damage events.

## Functions
### `HandleReceiveDamageEvent(oWidget, nDamageDirection, nDamageAmount)`
Called when the player receives damage. Initializes the widget if necessary, calculates the damage amount relative to the object's max health, and creates a new image widget representing the damage arc. Sets the texture, rotation, location, and translucency of the new indicator based on the damage direction and amount.

### `_Finish(oWidget)`
Resets the damage amount for the widget and hides it.

### `HandleUpdateEvent(oWidget, tEvent)`
Updates the rotation and translucency of the damage indicator widget over time. Reduces the translucency until it reaches zero, at which point it deletes the widget.

### `DeleteDamageIndicatorCallback(oWidget)`
Removes the damage indicator widget from the HUD and deletes it.

### `HandleE3HudModeEvent(oWidget, tEvent)`
Toggles the event handler for the "GuiPlayerReceiveDamage" event based on whether the E3 hud mode is active. Disables the handler when E3 mode is on to prevent damage indicators from showing during that mode.

## Events
- Listens for `GuiPlayerReceiveDamage` to create and update damage indicator widgets.
- Listens for custom event `E3HudModeEvent` to toggle the damage indicator display based on E3 hud mode.

## Notes for modders
- Ensure that the reticle widget is correctly named `"reticle"` in your HUD layout to allow proper positioning of damage indicators.
- Customize the appearance and behavior of damage indicators by modifying the texture, rotation, location, and translucency settings in `HandleReceiveDamageEvent`.
- Be aware that disabling the "GuiPlayerReceiveDamage" event handler during E3 mode prevents damage indicators from showing, which can be useful for maintaining a clean HUD interface.