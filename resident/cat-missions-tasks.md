---
title: Missions & Tasks
parent: Resident Modules
nav_order: 4
has_children: true
has_toc: false
---

# Missions & Tasks

The mission/task tree: contracts, jobs, objectives, briefing flow, and the state machine gating when each stage is allowed to run. Denser and more interlinked than most categories -- `MrxTask` and `MrxTaskMission` are the base classes nearly everything else here inherits from.

## Modules in this category

- **[mrxbriefing](mrxbriefing)** — The `mrxbriefing` module is responsible for managing the briefing system in Mercenaries 2.
- **[MrxCoop](mrxcoop)** — The `MrxCoop` module manages co-op gameplay mechanics, specifically the tethering system that keeps players within a certain distance of each other.
- **[MrxMissionBoundary](mrxmissionboundary)** — The `MrxMissionBoundary` module is designed to manage mission boundaries or proximity-based triggers in the game.
- **[mrxmissionflow](mrxmissionflow)** — The `mrxmissionflow` module is responsible for managing the mission flow in the game.
- **[MrxOutpostManager](mrxoutpostmanager)** — The `MrxOutpostManager` module is responsible for managing outposts in the game world.
- **[MrxPlayState](mrxplaystate)** — The `MrxPlayState` module manages the game's play state between free-play and mission modes.
- **[MrxStarter](mrxstarter)** — The `MrxStarter` module is responsible for managing the briefing process, handling missions, and maintaining various state related to player interactions with NPCs (Non-Player Characters).
- **[MrxStarterManager](mrxstartermanager)** — The `MrxStarterManager` module is responsible for managing game starters, which are likely key mission or support elements in the game.
- **[MrxState](mrxstate)** — The `MrxState` module manages the global state transitions and lifecycle events in the game.
- **[MrxTask](mrxtask)** — The `MrxTask` module is the base class for all mission-related tasks in the game.
- **[Mrxtaskcontract](mrxtaskcontract)** — The `Mrxtaskcontract` module is responsible for managing contract missions within the game.
- **[MrxTaskContractOutpost](mrxtaskcontractoutpost)** — The `MrxTaskContractOutpost` module is responsible for managing outpost-capture contracts in the game.
- **[MrxTaskContractPlaceholder](mrxtaskcontractplaceholder)** — The `MrxTaskContractPlaceholder` module is a stub implementation of a task contract.
- **[MrxTaskJob](mrxtaskjob)** — The `MrxTaskJob` module is a base class for multi-target mission tasks.
- **[MrxTaskJobCollectType](mrxtaskjobcollecttype)** — The `MrxTaskJobCollectType` module is responsible for managing a mission task where the player needs to collect a quota of label-filtered items.
- **[MrxTaskJobDestroySet](mrxtaskjobdestroyset)** — The `MrxTaskJobDestroySet` module is a subclass of `MrxTaskJob` designed to handle mission tasks where the player must destroy a set of named targets.
- **[MrxTaskJobDestroyType](mrxtaskjobdestroytype)** — The `MrxTaskJobDestroyType` module is a subclass of `MrxTaskJob` designed to handle tasks where the player must destroy objects filtered by a specific label.
- **[MrxTaskJobVerifySet](mrxtaskjobverifyset)** — The `MrxTaskJobVerifySet` module is a subclass of `MrxTaskJob` designed to handle mission tasks where players need to verify or capture specific high-value targets (HVTs).
- **[MrxTaskMission](mrxtaskmission)** — The `MrxTaskMission` module is a base class for mission tasks in the game.
- **[MrxTaskObjective](mrxtaskobjective)** — The `MrxTaskObjective` module is responsible for managing task objectives within the game.
- **[MrxTaskObjectiveAccept](mrxtaskobjectiveaccept)** — The `MrxTaskObjectiveAccept` module is a task objective action that handles the acceptance of a task by a player.
- **[MrxTaskObjectiveAction](mrxtaskobjectiveaction)** — The `MrxTaskObjectiveAction` module is a specialized task objective that involves player interaction with specific game objects.
- **[MrxTaskObjectiveCaptureOutpost](mrxtaskobjectivecaptureoutpost)** — The `MrxTaskObjectiveCaptureOutpost` module is a specific type of task objective that focuses on capturing or destroying outposts.
- **[MrxTaskObjectiveDeliver](mrxtaskobjectivedeliver)** — The `MrxTaskObjectiveDeliver` module is responsible for managing task objectives related to delivering specific objects or entities to designated destinations.
- **[MrxTaskObjectiveDestroy](mrxtaskobjectivedestroy)** — The `MrxTaskObjectiveDestroy` module is a specific type of task objective that requires the player to destroy certain game objects.
- **[MrxTaskObjectiveEnterVehicle](mrxtaskobjectiveentervehicle)** — The `MrxTaskObjectiveEnterVehicle` module is a task objective that requires the player to enter a specified vehicle.
- **[MrxTaskObjectiveExtract](mrxtaskobjectiveextract)** — The `MrxTaskObjectiveExtract` module is responsible for handling the extraction task objective in the game.
- **[MrxTaskObjectiveProtect](mrxtaskobjectiveprotect)** — The `MrxTaskObjectiveProtect` module is a specific type of task objective that focuses on protecting targets.
- **[MrxTaskObjectiveRelease](mrxtaskobjectiverelease)** — The `MrxTaskObjectiveRelease` module is a specific type of task objective that deals with the release of prisoners or controlled entities.
- **[MrxTaskObjectiveVerify](mrxtaskobjectiveverify)** — The `MrxTaskObjectiveVerify` module is responsible for handling the verification process of a high-value target (HVT) in the game.
- **[MrxTaskRace](mrxtaskrace)** — The `MrxTaskRace` module is responsible for managing checkpoint-based racing tasks in the game.
- **[MrxTaskState](mrxtaskstate)** — The `MrxTaskState` module defines the enumeration for task states in the game.
