---
title: MrxGuiHudDamageIndicator
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: 'deeper pass: re-confirmed all 5 functions + zero Event.* calls; surfaced the damage-normalization (dmg*100/maxHealth), translucency formula min(sqrt(dmg)*100,255), fade rate (~100 alpha/s), default damage 20, and the camera-relative rotation math (Player.GetCameraXZHeading); cross-linked reticle/Player/Object'
---

# MrxGuiHudDamageIndicator

*Module: mrxguihuddamageindicator.lua*

## Overview
The `MrxGuiHudDamageIndicator` module displays directional "took damage" fading arcs on the HUD — the red wedges that appear around the crosshair pointing toward the source of incoming fire. Each hit spawns a fresh [`MrxGui.ImageWidget`](mrxgui) that is rotated to face the damage source, faded out over roughly a second, then deleted. The whole indicator group is re-centered on the reticle widget (the [MrxGuiHudReticle](mrxguihudreticle) `"reticle"` widget) the first time damage arrives.

Built on the **native GUI widget framework** ([MrxGui](mrxgui)), not Scaleform. It reads player/object state through the [Player](../namespaces/player) and [Object](../namespaces/object) namespaces.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGui` (via [`import("MrxGui")`](../glossary#importname))

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
- **Damage is normalized to a % of max health**, not raw: `nDamageAmount = nDamageAmount * 100 / Object.GetMaxHealth(uObject)` where `uObject = Player.GetControlledObject(uPlayer)`. A hit that removes 20 HP from a 200-HP object registers as `10`. Default `nDamageAmount` is `20` if none is passed; a value `<= 0` returns early (no indicator).
- **Opacity (intensity) formula**: each arc's starting translucency is `math.min(math.pow(nDamageAmount, 0.5) * 100, 255)` — i.e. `sqrt(normalized_damage) * 100`, capped at fully opaque. Bigger hits start brighter. Change the `0.5` exponent or `100` multiplier to re-tune how strongly damage maps to opacity.
- **Fade rate**: `HandleUpdateEvent` subtracts `100 * tEvent` from translucency each frame, where `tEvent` is the frame delta-time (seconds) — so an arc fades at ~100 alpha/second and lives ~1s at half opacity, ~2.5s at full. When it reaches 0 the widget is removed and `:delete()`d (`DeleteDamageIndicatorCallback`).
- **Direction math**: each arc is rotated to `Player.GetCameraXZHeading(owner) - nDamageDirection` at spawn and re-rotated to `nDamageDirection + cameraHeading` every update, so it stays pinned to the world-space damage source as the camera turns. `nDamageDirection` comes in as the second arg to `HandleReceiveDamageEvent`.
- **Positioning depends on the reticle widget**: the group centers itself on the widget named exactly `"reticle"` (looked up via `MrxGui.GetWidgetByNameAndOwner("reticle", owner)`). If that widget is renamed/absent in your HUD layout, the arcs won't recenter (they fall back to the parent's authored location).
- **Texture**: new arcs copy the base widget's texture via `oNewIndicator:SetTexture(oWidget:GetTexture())` — there is no hard-coded texture string here; swap the arc art by changing the base widget's texture in the layout.
- **E3 mode toggle**: `HandleE3HudModeEvent` disables/enables the `"GuiPlayerReceiveDamage"` handler for the E3 demo HUD. Note this file never establishes the *initial* `"GuiPlayerReceiveDamage"` binding — a layout file must set it, or `HandleE3HudModeEvent` must run once with `bOn == false` before any indicator can appear.