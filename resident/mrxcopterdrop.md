---
title: MrxCopterDrop
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, delivery]
---

# MrxCopterDrop

*Module: mrxcopterdrop.lua*

## Overview
The `MrxCopterDrop` module is responsible for managing the delivery of cargo using helicopters. It handles the spawning of both the helicopter and the cargo, deploying the winch to attach the cargo, and ensuring the delivery process completes successfully.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxSupport`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state but provides functions to manage helicopter-based deliveries.

## Functions
### `Create(sFaction, sCargo, nDesX, nDesY, nDesZ, bCareless, nTargetX, nTargetY, nTargetZ)`
Spawns a helicopter and cargo for delivery. It checks if the current client is the server, retrieves GUIDs for the cargo and helicopter templates based on the faction, spawns the objects at appropriate positions, and sets up events to handle the winch deployment and cargo attachment.

### `_DeployWinch(uHeli, uCargo, nDesX, nDesY, nDesZ, bCareless)`
Called when the helicopter is awake. It deploys the winch on the helicopter and sets up a timer event to wait for the cargo to become active before proceeding with further delivery steps.

### `_WaitCallback(uHeli, uCargo, nDesX, nDesY, nDesZ, bCareless)`
Called after the cargo becomes active. It aligns the cargo's yaw with the helicopter's, attaches the cargo to the winch, and initiates the delivery process using AI control.

### `DeliveryComplete(uHeli)`
Called when the delivery is complete. It detaches the cargo from the winch and calls a function from `MrxSupport` to return the helicopter home.

## Events
- Listens for `Event.ObjectHibernation` to deploy the winch when the helicopter becomes active.
- Listens for `Event.TimerRelative` to wait for the cargo to become active before proceeding with further delivery steps.
- Listens for `Event.ObjectWinched` to detach the cargo from the winch after the delivery is complete.

## Notes for modders
- Ensure that the server is handling the creation of helicopter and cargo objects to maintain consistency across multiplayer sessions.
- Customize the faction and cargo types by modifying the `tCopterData` table and the `sCargoToDeliver` variable.
- Be aware that network synchronization (`Net.IsClient()`) may affect the behavior in multiplayer environments.
- The `_DeployWinch` and `_WaitCallback` functions are internal helpers and should not be called directly by modders.