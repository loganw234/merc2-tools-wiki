---
title: MrxApcDrop
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, mission]
verified: true
verified_note: re-verified previously-documented DropCallback bug and class-factory pattern against source, both still accurate; no other gaps found
---

# MrxApcDrop

*Module: mrxapcdrop.lua*

## Overview
The `MrxApcDrop` module is a generic helper for mission scripts that involves flying in an APC (Armored Personnel Carrier), deploying a squad of passengers, and then flying out. It is config-driven and can handle different types of destinations (path, object, or coordinate) with customizable speeds.

## Inheritance
- Inherits from: `none` — base/utility module
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module that does not follow the per-instance pattern. It manages the lifecycle of an APC drop operation without maintaining persistent state across activations.

## Functions
### `Create(srcObj, tConfig)`
Initializes and starts the APC drop operation based on the provided configuration. It sets up AI goals for moving to the destination, deploying passengers, and flying out. If the vehicle is not alive, it logs an error message and returns early.

**Not mentioned above but confirmed in source:** if `tConfig.inDest` is falsy (no `inDest` configured), `Create`
skips the AI-goal setup entirely and instead calls `self:DropCallback()` immediately. This looks like a bug in
the game's own code — only `_DropCallback` (with a leading underscore) is actually defined anywhere in this
module, so that call would fail with an "attempt to call a nil value" error. This path is likely dead/never
exercised in practice, since every real caller apparently always supplies `inDest`.

### `Cancel(self)`
Cancels any ongoing events related to the APC drop operation, such as death events and exit delays.

### `_DropCallback(self)`
A private callback function that handles the deployment of passengers from the APC. It retrieves the riders and sets up a new AI goal for deploying them.

### `_DropCallback2(self)`
Another private callback function that handles the post-deployment actions, including taking off if it's a helicopter and moving to the out destination. It also commands the squad to move within a boundary around the target.

### `_CommandSquad(self)`
A private function that adds the deployed passengers to a specified squad and issues a command for them to move within a boundary around the target. It also calls any provided callback function once the operation is complete.

### `_GetGuidIfString(param)`
A helper function that converts a string parameter into a GUID using `Pg.GetGuidByName`. If the parameter is not a string, it returns the parameter as-is.

## Events
- Listens for `Event.ObjectDeath` to call `Cancel` if the driver dies during the operation.
- Uses custom events and callbacks (`_DropCallback`, `_DropCallback2`) to manage different stages of the APC drop operation.

## Notes for modders
- Ensure that the vehicle and driver are alive and unhibernated before calling `Create`.
- Customize the drop operation by providing a configuration table with fields like `inDest`, `outDest`, `squadName`, etc.
- Be aware that default speeds for in and out destinations are set to 0.8, and the squad MoveWithinBoundary radius is set to 8.
- Use `_GetGuidIfString` to convert string names to GUIDs if needed.
- This module does not maintain persistent state across activations; each call to `Create` starts a new operation.