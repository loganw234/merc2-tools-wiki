---
title: Soldier
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, pickup]
---

# Soldier

*Module: soldier.lua*

## Overview
The `Soldier` module handles the death logic for soldier AI entities in the game. It determines what type of pickup to drop based on the soldier's class and the player's current state, such as health and ammo reserve.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module with no per-instance tables. It tracks the following key fields:
- `deathCount`: A global counter to track how many times soldiers have died.
- `tDrops`: A table mapping indices to pickup types.

## Functions
### `OnDeath(uGuid, iArg)`
Called when a soldier instance dies. Increments the death count and checks if a pickup should be dropped based on various conditions:
- If the soldier is in a seat, no pickup is spawned.
- For every third death or for heavy soldiers, it determines the type of pickup to spawn based on the soldier's class (e.g., "RocketSoldier", "HeavySoldier").
- It checks the player's health and ammo reserve to decide between different types of pickups like "Ammo Pickup (Bullet)", "Ammo Pickup (Rocket)", "Ammo Pickup (Grenades)", or "Health Pickup".
- Spawns the chosen pickup slightly above the soldier's position with a downward impulse and adds it to the disposer for cleanup.

## Events
- Listens for `Event.ObjectDeath` to call `OnDeath` when a soldier dies.

## Notes for modders
- Ensure that `OnDeath` is called appropriately to manage pickup spawning logic.
- Customize the types of pickups dropped by modifying the `tDrops` table or adjusting the conditions in `OnDeath`.
- Be aware that network synchronization (`Pg.Spawn`) may affect multiplayer behavior when spawning pickups.