---
title: MrxTaskObjectiveAccept
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjectiveAction
tags: [task, objective]
verified: true
verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTaskObjectiveAction](mrxtaskobjectiveaction) for the general mechanism.
---

# MrxTaskObjectiveAccept

*Module: mrxtaskobjectiveaccept.lua*

## Overview
The `MrxTaskObjectiveAccept` module is a task objective action that handles the acceptance of a task by a player. It displays a confirmation dialog to the player and processes their response.

## Inheritance
- Inherits from: `MrxTaskObjectiveAction`
- Imports: `MrxGui`, `MrxPlayer`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjectiveAction`](mrxtaskobjectiveaction)'s class-factory pattern**
(itself inherited from [`MrxTaskObjective`](mrxtaskobjective)/[`MrxTask`](mrxtask); see that page for the
general mechanism), identified by name/lineage rather than a world-object GUID. Key fields:
- `_bConfPromptDisplayed`: A boolean indicating whether the confirmation prompt has been displayed.

## Functions
### `_TargetActioned(self, uActionerGuid, uActioneeGuid)`
Called when an action target is acted upon. If the confirmation prompt has not been displayed yet, it sets `_bConfPromptDisplayed` to true and shows a dialog box to the player asking for confirmation.

### `_ConfPromptDismissed(self, uActionerGuid, uActioneeGuid, nSelectedIndex)`
Called when the player dismisses the confirmation dialog. It resets `_bConfPromptDisplayed` to false and checks if the player selected "Yes". If so, it calls the base class's `_TargetActioned` method.

### `_PrintObjectiveMessage(self, sMsgType)`
A placeholder function that does nothing. This is likely a stub for future functionality related to printing objective messages.

## Events
- Listens for an internal event (not explicitly defined in this file) to call `_ConfPromptDismissed` when the player dismisses the confirmation dialog.

## Notes for modders
- Ensure that `_TargetActioned` is called appropriately when an action target is acted upon.
- Customize the dialog text by setting the `sDialogText` field in the configuration.
- Be aware that this module relies on the `MrxGui` and `MrxPlayer` modules for displaying dialogs and player-related operations.