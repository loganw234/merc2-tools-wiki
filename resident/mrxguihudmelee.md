---
title: MrxGuiHudMelee
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: 'deeper pass: re-confirmed 6 stubs + the one real function (SetContextActionMessage) and its priority-queue/sound-cue mechanics; documented the "[action] " text prefix token, the sound cue string, and lazy _Initialize; re-verified the sCurrentText=sText (should be sNewText) bug at line 51; zero Event.*/SetEventHandler'
---

# MrxGuiHudMelee

*Module: mrxguihudmelee.lua*

## Overview
The `MrxGuiHudMelee` module drives the **context-action HUD prompt** — the on-screen "[action] Do X" text that appears when the player can perform a contextual action (enter vehicle, hijack, use an object, etc.). Despite the "melee" name, the only working function is `SetContextActionMessage`; the melee/counter-message functions are empty stubs. It manages a priority-keyed message queue on one shared "Context Action Text" widget, shows the highest-priority message, plays an alert sound when the text changes, and fades the prompt out when cleared.

Built on the native GUI framework ([MrxGui](mrxgui)); text/animation only, no Scaleform. Uses [Sound](../namespaces/sound) for the alert cue.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGui` (via [`import("MrxGui")`](../glossary#importname))

## Instance pattern
**Stateless module + per-widget `CustomData`.** No per-instance tables at module level. All state lives on the "Context Action Text" widget's `CustomData`, set up lazily by the local `_Initialize` on first `SetContextActionMessage` call: `tMessageQueue` (priority → text string), `nCurrentPriority`, `sCurrentText`, and the `nVisiblePoint`/`nFadePoint` translucency animation points.

## Functions
### `SetCounterMessageVisible(bShow, uPlayerGuid)`
Sets the visibility of a counter message for a specific player. This function is currently stubbed and does not perform any action.

### `SetMeleeMessage(sString, uPlayerGuid)`
Sets a melee message for a specific player. This function is currently stubbed and does not perform any action.

### `DisplayCounterMessage(nDisplayTime, uPlayerGuid)`
Displays a counter message for a specified duration to a specific player. This function is currently stubbed and does not perform any action.

### `HandleUpdateEvent(oWidget, nTime)`
Handles update events for a given widget. This function is currently stubbed and does not perform any action.

### `HandleInitializationEvent(oWidget, oEvent)`
Handles initialization events for a given widget. This function is currently stubbed and does not perform any action.

### `HideOnComplete(oWidget)`
Hides a widget when its animation completes. This function is currently stubbed and does not perform any action.

### `SetContextActionMessage(sText, uPlayer, nPriority)`
Sets the context action message for a player or all players. It retrieves the appropriate HUD widget, initializes it if necessary, and updates the message queue based on priority. If the message changes, it triggers a sound cue and animates the widget to display the new message.

**Likely bug in the clear-and-fall-back-to-next-queued-message path** (`sText == nil` and `nPriority == oContextActionWidget.CustomData.nCurrentPriority`): the widget text is correctly set to the next queued message via the local `sNewText` (line 48, `SetText("[action] " .. sNewText)`), but `sCurrentText` is then assigned from `sText` instead of `sNewText` (line 51) — and `sText` is `nil` in this branch. So `sCurrentText` ends up `nil` even though the widget is now showing `sNewText`. Net effect: the dedup check earlier in the same branch (line 45, `sCurrentText ~= sNewText`) never has a chance to correctly suppress a repeat sound cue for this fallback path on a subsequent call, since `sCurrentText` never actually records what's displayed here.

### `ContextActionWidgetRemovalCallback(oContextActionWidget)`
A callback function that is called when the context action widget's removal animation completes. It hides the widget, clears its text, resets its priority, and sets its translucency level.

### `_Initialize(oWidget)`
Initializes a HUD widget by setting up custom data fields such as message queue, current priority, and animation points for visibility and fade effects.

## Events
No `Event.*`/`Event.Create(...)` engine-event references and no `SetEventHandler` calls appear anywhere in this file — confirmed by grep. `HandleUpdateEvent(oWidget, nTime)` and `HandleInitializationEvent(oWidget, oEvent)` are named following the `Handle*Event` convention used elsewhere for widget event handlers, but neither is registered to any handler key in this file — both are empty stubs (see Functions). `SetContextActionMessage` is the module's real entry point and is called directly by name from other modules (not event-driven); it looks up the "Context Action Text" widget via `MrxGui.GetWidgetByName`/`GetWidgetByNameAndOwner`, lazily calls the local `_Initialize` on first use, and manages message text/priority/animation itself.

## Notes for modders
- **`SetContextActionMessage(sText, uPlayer, nPriority)` is the only working entry point.** Call with a `sText` string to post a prompt at priority `nPriority` (default `1`); call with `sText = nil` at the same priority to clear that entry (the widget then shows the next-highest queued message, or fades out if the queue is empty). If `uPlayer` is not `userdata`, it targets the global "Context Action Text" widget (`MrxGui.GetWidgetByName`); otherwise the owning player's copy (`MrxGui.GetWidgetByNameAndOwner`).
- **Displayed text is prefixed with the literal `"[action] "`** before your string (`SetText("[action] " .. sText)`). `[action]` is a substitution/markup token the text renderer replaces with the current action-button glyph — pass just the verb ("Enter vehicle"), not the button.
- **Alert sound**: `Sound.CueSound(0, "ui_HUD_Contextual_Action_Alert")` fires whenever the shown text actually changes (deduped against `sCurrentText`). Repeated identical messages don't re-alert.
- **Priority queue**: `tMessageQueue` is keyed by priority number. Note the "pick next" loop (`for ... in pairs`) just takes the last iterated entry — with numeric-but-sparse keys `pairs` order is unspecified, so which queued message wins after a clear is not strictly the highest priority. Keep priorities simple.
- **Six stub functions** — `SetCounterMessageVisible`, `SetMeleeMessage`, `DisplayCounterMessage`, `HandleUpdateEvent`, `HandleInitializationEvent`, `HideOnComplete` — are all empty (`function ... end`). They do nothing; the melee/counter-prompt feature they imply is not implemented in this file.

{: .warning }
> **Confirmed bug (line 51).** In the clear-and-fall-back path (`sText == nil`, priority matches current), the widget correctly shows the next queued message via `sNewText`, but then writes `CustomData.sCurrentText = sText` — and `sText` is `nil` here. It should be `sNewText`. Result: `sCurrentText` doesn't record what's actually displayed, so the sound-dedup check can mis-fire (re-alert) on the next call for that fallback message.