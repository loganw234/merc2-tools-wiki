---
title: MrxGuiHudDamageIndicator
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: confirmed zero Event.* calls in file (widget EventHandlers keys only); corrected Events section — HandleE3HudModeEvent has no call site in this file, GuiPlayerReceiveDamage is toggled but never initially bound here
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
No `Event.*`/`Event.Create(...)` engine-event references appear in this file — confirmed by grep. All triggering is via widget-level `EventHandlers`/`SetEventHandler` keys (strings), not `Event.*` constants:
- `HandleReceiveDamageEvent` is set as the `"GuiPlayerReceiveDamage"` handler on a widget — but only from inside `HandleE3HudModeEvent` (toggled on/off depending on `tEvent.bOn`); this file never establishes the *initial* binding, so something outside this file (a layout file) must set it first, or `HandleE3HudModeEvent` must run once with `bOn == false` before damage indicators can appear.
- The new per-hit indicator widget created in `HandleReceiveDamageEvent` is given its own `"GuiUpdate"` handler, `HandleUpdateEvent`, to animate/fade it out frame-by-frame.
- `HandleE3HudModeEvent` itself has no call site within this file — nothing here calls it or registers it as a handler for any key. It's invoked externally (by naming convention, likely wired to an `"E3HudModeEvent"`-style key in a layout file not covered by this module) — no call site found in the decompiled `resident/` corpus search performed for this page.

## Notes for modders
- Ensure that the reticle widget is correctly named `"reticle"` in your HUD layout to allow proper positioning of damage indicators.
- Customize the appearance and behavior of damage indicators by modifying the texture, rotation, location, and translucency settings in `HandleReceiveDamageEvent`.
- Be aware that disabling the "GuiPlayerReceiveDamage" event handler during E3 mode prevents damage indicators from showing, which can be useful for maintaining a clean HUD interface.