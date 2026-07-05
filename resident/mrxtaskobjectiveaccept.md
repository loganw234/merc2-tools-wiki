---
title: MrxTaskObjectiveAccept
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjectiveAction
tags: [task, objective]
verified: true
verified_note: deeper pass — clarified this subclass ONLY overrides _TargetActioned (to insert a Yes/No dialog before accepting) and stubs _PrintObjectiveMessage to a no-op; corrected the Events section (the dialog callback is a MrxGui dialog callback, NOT an Event subscription); default dialog text "[Generic.Accept]?"
---

# MrxTaskObjectiveAccept

*Module: mrxtaskobjectiveaccept.lua*

## Overview
`MrxTaskObjectiveAccept` is a thin subclass of [`MrxTaskObjectiveAction`](mrxtaskobjectiveaction) that
inserts a Yes/No confirmation dialog between the player pressing the interact button and the objective
actually completing. Its whole reason to exist is those two overrides: `_TargetActioned` (pop the dialog
first) and `_PrintObjectiveMessage` (silenced). Everything else — the context-action setup, the target/death
events, the icons — is inherited unchanged from `MrxTaskObjectiveAction`.

## Inheritance
- Inherits from: `MrxTaskObjectiveAction`
- Imports: `MrxGui`, `MrxPlayer`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjectiveAction`](mrxtaskobjectiveaction)'s class-factory pattern**
(itself inherited from [`MrxTaskObjective`](mrxtaskobjective)/[`MrxTask`](mrxtask); see that page for the
general mechanism), identified by name/lineage rather than a world-object GUID. Key fields:
- `_bConfPromptDisplayed`: A boolean indicating whether the confirmation prompt has been displayed.

## Functions
### `_TargetActioned(self, uActionerGuid, uActioneeGuid)` *(override)*
**Overrides** [`MrxTaskObjectiveAction`](mrxtaskobjectiveaction)'s version. Instead of immediately
completing the part, it shows a Yes/No dialog via `MrxGui.DisplayDialogBox` (guarded by
`_bConfPromptDisplayed` so it can't stack) with buttons `"[Generic.Yes]"` / `"[Generic.No]"` and text from
config `sDialogText`, defaulting to `"[Generic.Accept]?"`. The player's answer is delivered to
`_ConfPromptDismissed`.

### `_ConfPromptDismissed(self, uActionerGuid, uActioneeGuid, nSelectedIndex)`
Dialog callback (a plain overridable function, not an event handler). Clears `_bConfPromptDisplayed`; if the
player picked index `1` ("Yes"), it calls the base `MrxTaskObjectiveAction._TargetActioned` to actually
complete the part. Picking "No" leaves the objective open so the player can be re-prompted.

### `_PrintObjectiveMessage(self, sMsgType)` *(override)*
**Overrides** the base to an empty no-op, suppressing this objective's HUD add/update/complete messages —
the dialog is the whole interaction, so the standard objective banners would be noise.

## Events
This subclass **subscribes to no events of its own** — it inherits `MrxTaskObjectiveAction`'s
`Event.ContextAction` / `Event.ObjectDeath` subscriptions. The confirmation flow runs through a
`MrxGui.DisplayDialogBox` **callback**, not an `Event.*` subscription.

## Notes for modders
- **Change the prompt text** with config `sDialogText` (default `"[Generic.Accept]?"`). Buttons are hardcoded
  to `"[Generic.Yes]"` / `"[Generic.No]"`.
- Use this instead of plain [`MrxTaskObjectiveAction`](mrxtaskobjectiveaction) whenever accepting should be a
  deliberate confirm rather than a single button press (e.g. picking up a job).
- Depends on [`MrxGui`](mrxgui) for the dialog and `MrxPlayer` for resolving the actioner to a player
  character; the dialog is shown to `Player.GetCharacter(uActionerGuid)`.