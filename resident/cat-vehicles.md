---
title: Vehicles
parent: Resident Modules
nav_order: 2
has_children: true
has_toc: false
---

# Vehicles

Drivable/flyable vehicle objects (planes, helicopters, tanks) and the shared vehicle-blip base class they build on. Mostly thin wrappers -- most of the interesting behavior lives in what they inherit from, so check `VehicleBlippable` and `OrientedBlippable` (under Core Engine & Utilities) alongside any page here.

## Modules in this category

- **[Airplane](airplane)** — The `Airplane` module represents a specific type of vehicle in the game world.
- **[AntiAir](antiair)** — The `AntiAir` module represents anti-aircraft systems in the game.
- **[Autogunship](autogunship)** — The `Autogunship` module represents an AI-controlled gunship that targets and attacks ground vehicles.
- **[BountyCopter](bountycopter)** — The `BountyCopter` module is a world-spawn helper that drops supply crates via winch.
- **[Helicopter](helicopter)** — The `Helicopter` module represents a helicopter vehicle in the game.
- **[MoonPatrol](moonpatrol)** — The `MoonPatrol` module manages the behavior of a moon patrol vehicle in the game.
- **[OpenTankHatch](opentankhatch)** — The `OpenTankHatch` module is designed to open the driver hatch of a tank vehicle when it is activated.
- **[PursuitCopter](pursuitcopter)** — The `PursuitCopter` module represents a pursuit helicopter that lands near the player and deploys passengers.
- **[SupportAirplane](supportairplane)** — The `SupportAirplane` module is responsible for managing support aircraft in the game.
- **[Tank](tank)** — The `Tank` module represents a tank vehicle in the game.
- **[VehicleBlippable](vehicleblippable)** — The `VehicleBlippable` module is responsible for managing radar and off-screen world markers for vehicles.
