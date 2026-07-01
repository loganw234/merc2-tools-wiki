---
title: Core Engine & Utilities
parent: Resident Modules
nav_order: 8
has_children: true
has_toc: false
---

# Core Engine & Utilities

Boot sequence, cross-cutting managers (player, faction, HQ, layers), and the base classes (`Inheritable`, `Blippable`, ...) most other modules in this wiki build on. Less immediately useful for a first mod, but essential once you're extending something instead of just calling into it.

## Modules in this category

- **[Blippable](blippable)** — The `Blippable` module is responsible for adding and removing radar objectives and off-screen world markers for game objects.
- **[EnemyBlippable](enemyblippable)** — The `EnemyBlippable` module extends the functionality of the `Blippable` module to manage radar objectives and off-screen world markers specifically for enemy vehicles.
- **[GameBootstrap](gamebootstrap)** — The `GameBootstrap` module is responsible for initializing the game environment and playing introductory movies.
- **[Inheritable](inheritable)** — The `Inheritable` module serves as the base class for all world objects in the game.
- **[Init](Init)** — The `Init` module is responsible for initializing a global table to manage events and handling the activation and deactivation of world objects.
- **[LevelBootstrap](levelbootstrap)** — The `LevelBootstrap` module is responsible for loading a game level and its associated master script.
- **[MrxAchievements](mrxachievements)** — The `MrxAchievements` module is responsible for managing and tracking player achievements in the game.
- **[MrxActionHijack](mrxactionhijack)** — The `MrxActionHijack` module is responsible for managing the action hijack sequence in the game.
- **[MrxAi](mrxai)** — The `MrxAi` module provides a thin, awake-gated shim over the engine `Ai.*` API.
- **[MrxBootstrap](mrxbootstrap)** — The `MrxBootstrap` module is responsible for initializing the game world by handling GUI loading and local player joining events.
- **[MrxCinematic](mrxcinematic)** — The `MrxCinematic` module is a placeholder slideshow system used for displaying sequences of slides in the game's HUD.
- **[MrxFactionManager](mrxfactionmanager)** — The `MrxFactionManager` module is responsible for managing faction relations, attitudes, and reporting systems within the game.
- **[MrxFollow](mrxfollow)** — The `MrxFollow` module manages the escort/follow behavior for companion characters in the game.
- **[mrxhq](mrxhq)** — The `mrxhq` module is responsible for managing the HQ portal in the game.
- **[MrxHqManager](mrxhqmanager)** — The `MrxHqManager` module is responsible for managing Headquarters (HQ) in the game.
- **[MrxLayerManager](mrxlayermanager)** — The `MrxLayerManager` module is responsible for managing dynamic and static layers in the game world.
- **[MrxParkingLotManager](mrxparkinglotmanager)** — The `MrxParkingLotManager` module is responsible for managing parking lots in the game.
- **[MrxPlayer](mrxplayer)** — The `MrxPlayer` module is responsible for managing player characters in the game.
- **[MrxPmc](mrxpmc)** — The `MrxPmc` module manages the player's economy and support items in Mercenaries 2.
- **[mrxrewarddata](mrxrewarddata)** — The `mrxrewarddata` module manages reward configurations and dispenses rewards for various game events, missions, and milestones.
- **[MrxShop](mrxshop)** — The `MrxShop` module is responsible for managing the in-game store system, including generating and displaying shop lists, handling item purchases, and maintaining persistence of purchased items.
- **[MrxSoundBootstrap](mrxsoundbootstrap)** — The `MrxSoundBootstrap` module is responsible for initializing and managing the sound system in the game.
- **[MrxStatsManager](mrxstatsmanager)** — The `MrxStatsManager` module is responsible for tracking and managing various statistics and progress metrics for the player.
- **[MrxTimer](mrxtimer)** — The `MrxTimer` module is responsible for managing countdown and stopwatch timers in the game's user interface.
- **[MrxTransit](mrxtransit)** — The `MrxTransit` module manages the transit system in the game, including handling player fast-travel to different landing zones.
- **[MrxTutorial](mrxtutorial)** — The `MrxTutorial` module is responsible for managing in-game tutorials.
- **[MrxTutorialManager](mrxtutorialmanager)** — The `MrxTutorialManager` module is responsible for managing in-game tutorials.
- **[MrxUnlockFanfare](mrxunlockfanfare)** — The `MrxUnlockFanfare` module is responsible for displaying unlock banners on the HUD when players acquire new items or complete certain game objectives.
- **[MrxUtil](mrxutil)** — The `MrxUtil` module is a comprehensive utility library providing a wide range of helper functions for various tasks in the game.
- **[MrxUtilShell](mrxutil_shell)** — The `MrxUtilShell` module provides utility functions for calling functions with optional arguments and processing callback tables.
- **[MrxVoSequence](mrxvosequence)** — The `MrxVoSequence` module is responsible for playing voice-over (VO) sequences in the game.
- **[Multi](Multi)** — The `Multi` module provides utility functions for spawning multiple game objects in the world.
- **[OrientedBlippable](orientedblippable)** — The `OrientedBlippable` module extends the functionality of the `Blippable` module by adding support for oriented blips, which rotate based on the object's orientation.
