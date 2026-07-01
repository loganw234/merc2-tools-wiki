---
title: Support & Airstrikes
parent: Resident Modules
nav_order: 3
has_children: true
has_toc: false
---

# Support & Airstrikes

The support/supply-drop system: every airstrike, bombing run, artillery strike, and delivery type callable by the player, plus the designator/targeting objects and the shared `MrxSupport` base they all build on. The single largest category -- if you're looking for "how do air strikes work" or want to add a new support type, start with `MrxSupport` and `MrxSupportDelivery`.

## Modules in this category

- **[Airstrike_Atmosphere_Daisycutter](airstrike_atomsphere_daisycutter)** — The `Airstrike_Atmosphere_Daisycutter` module is responsible for setting up the atmospheric effects and visual settings when a daisy cutter airstrike occurs.
- **[Airstrike_Atmosphere_FuelAirBomb](airstrike_atomsphere_fuelairbomb)** — The `Airstrike_Atmosphere_FuelAirBomb` module is responsible for handling the atmospheric effects triggered by a fuel air bomb airstrike.
- **[Airstrike_Atmosphere_MOAB](airstrike_atomsphere_moab)** — The `Airstrike_Atmosphere_MOAB` module is responsible for setting up atmospheric effects and visual graphics when a MOAB (Massive Ordnance Air Blast) airstrike occurs.
- **[AirstrikeAtomsphereBombrun](airstrike_atomsphere_bombrun)** — The `AirstrikeAtomsphereBombrun` module is responsible for adjusting the atmospheric and visual effects during an airstrike event.
- **[AirstrikeAtomsphereCarpetbomb](airstrike_atomsphere_carpetbomb)** — The `AirstrikeAtomsphereCarpetbomb` module is responsible for initiating a specific atmospheric effect when an airstrike event occurs.
- **[AirstrikeAtomsphereClusterbomb](airstrike_atomsphere_clusterbomb)** — The `AirstrikeAtomsphereClusterbomb` module is responsible for modifying the atmospheric and visual effects of the game world when an airstrike with cluster bombs occurs.
- **[AirstrikeAtomsphereTactNuke](airstrike_atomsphere_tactnuke)** — The `AirstrikeAtomsphereTactNuke` module is responsible for handling the atmospheric effects triggered by a tactical nuke airstrike.
- **[MrxApcDrop](mrxapcdrop)** — The `MrxApcDrop` module is a generic helper for mission scripts that involves flying in an APC (Armored Personnel Carrier), deploying a squad of passengers, and then flying out.
- **[MrxArtillery](mrxartillery)** — The `MrxArtillery` module is responsible for managing the deployment and behavior of artillery support in the game.
- **[MrxArtilleryAttack](mrxartilleryattack)** — The `MrxArtilleryAttack` module is responsible for executing a staggered falling-ordnance strike.
- **[MrxBoatDelivery](mrxboatdelivery)** — The `MrxBoatDelivery` module is a specialized support delivery system for water-based operations.
- **[MrxBombingRun](mrxbombingrun)** — The `MrxBombingRun` module is a support system for executing bombing runs in the game.
- **[MrxBunkerBuster](mrxbunkerbuster)** — The `MrxBunkerBuster` module is responsible for managing the behavior of a bunker buster support weapon in the game.
- **[MrxCarpetBomb](mrxcarpetbomb)** — The `MrxCarpetBomb` module is a support system that allows players to deploy carpet bomb airstrikes.
- **[MrxChiCon001Rescue](mrxchicon001rescue)** — The `MrxChiCon001Rescue` module defines the behavior for a rescue copter support pickup.
- **[MrxClusterBomb](mrxclusterbomb)** — The `MrxClusterBomb` module is responsible for managing the deployment and behavior of a cluster bomb support system in the game.
- **[MrxCombatAirPatrol](mrxcombatairpatrol)** — The `MrxCombatAirPatrol` module is a support system for aerial combat.
- **[MrxCopterDrop](mrxcopterdrop)** — The `MrxCopterDrop` module is responsible for managing the delivery of cargo using helicopters.
- **[MrxCrateDelivery](mrxcratedelivery)** — The `MrxCrateDelivery` module is a specialized support delivery system for ground-based cargo drops.
- **[MrxCruiseMissile](mrxcruisemissile)** — The `MrxCruiseMissile` module is responsible for managing the deployment and behavior of cruise missiles in the game.
- **[MrxDaisyCutter](mrxdaisycutter)** — The `MrxDaisyCutter` module is responsible for managing the Daisy Cutter support operation in the game.
- **[MrxFuelAirBomb](mrxfuelairbomb)** — The `MrxFuelAirBomb` module is responsible for managing the deployment and detonation of fuel air bombs as a support action in the game.
- **[MrxGunship](mrxgunship)** — The `MrxGunship` module is responsible for managing a support vehicle (AC130) that provides aerial fire support to players.
- **[MrxHARMStrike](mrxharmstrike)** — The `MrxHARMStrike` module is a support system for initiating and managing HARM (High-speed Anti-Radiation Missile) strikes.
- **[MrxLaserGuidedBomb](mrxlaserguidedbomb)** — The `MrxLaserGuidedBomb` module is responsible for managing the deployment and behavior of a laser-guided bomb support system.
- **[MrxMOAB](mrxmoab)** — The `MrxMOAB` module is a specialized support module for the MOAB (Massive Ordnance Air Blast) weapon.
- **[MrxMunitionsPickup](mrxmunitionspickup)** — The `MrxMunitionsPickup` module is responsible for handling the pickup of tagged munitions by a heli.
- **[MrxOilCon002Delivery](mrxoilcon002delivery)** — The `MrxOilCon002Delivery` module manages the listening-post delivery support mission.
- **[MrxRocketArtillery](mrxrocketartillery)** — The `MrxRocketArtillery` module is responsible for managing the rocket artillery support system in the game.
- **[MrxSatClusterBomb](mrxsatclusterbomb)** — The `MrxSatClusterBomb` module represents the support system for deploying cluster bombs via a satellite.
- **[MrxSatelliteGuidedBomb](mrxsatelliteguidedbomb)** — The `MrxSatelliteGuidedBomb` module is responsible for managing the guided bomb support system in the game.
- **[MrxSmartBomb](mrxsmartbomb)** — The `MrxSmartBomb` module is responsible for handling the functionality of the Smart Bomb support type in the game.
- **[MrxSoldierDelivery](mrxsoldierdelivery)** — The `MrxSoldierDelivery` module is responsible for delivering troop reinforcements in the game.
- **[MrxStrategicMissile](mrxstrategicmissile)** — The `MrxStrategicMissile` module is responsible for managing the launch and detonation of strategic missiles in the game.
- **[MrxSupport](mrxsupport)** — The `MrxSupport` module is responsible for managing various support operations in the game, including designating targets, handling costs, and coordinating with other systems like anti-air defenses.
- **[MrxSupportCopterDelivery](mrxsupportcopterdelivery)** — The `MrxSupportCopterDelivery` module is responsible for delivering a flyable helicopter to the player's designated point.
- **[MrxSupportData](mrxsupportdata)** — The `MrxSupportData` module manages support items and their delivery in the game.
- **[MrxSupportDelivery](mrxsupportdelivery)** — The `MrxSupportDelivery` module is responsible for handling the delivery of cargo using a helicopter.
- **[MrxSupportDesignator](mrxsupportdesignator)** — The `MrxSupportDesignator` module is a base class for support designators in the game.
- **[MrxSupportDesignatorBeacon](mrxsupportdesignatorbeacon)** — The `MrxSupportDesignatorBeacon` module is a subclass of `MrxSupportDesignator` that handles the creation and management of beacon designators.
- **[MrxSupportDesignatorFlare](mrxsupportdesignatorflare)** — The `MrxSupportDesignatorFlare` module is a subclass of `MrxSupportDesignator` that handles the creation and management of flare designators.
- **[MrxSupportDesignatorLaser](mrxsupportdesignatorlaser)** — The `MrxSupportDesignatorLaser` module is responsible for managing the behavior and lifecycle of a laser designator support system in the game.
- **[MrxSupportDesignatorSatellite](mrxsupportdesignatorsatellite)** — The `MrxSupportDesignatorSatellite` module is responsible for handling the satellite designator support type in the game.
- **[MrxSupportDesignatorSmoke](mrxsupportdesignatorsmoke)** — The `MrxSupportDesignatorSmoke` module is responsible for handling the functionality of smoke support designators in the game.
- **[MrxSupportManager](mrxsupportmanager)** — The `MrxSupportManager` module is responsible for managing the designation queues and recruit cooldowns in the game.
- **[MrxSupportPickup](mrxsupportpickup)** — The `MrxSupportPickup` module manages the extraction helicopter support system in the game.
- **[MrxSupportTransit](mrxsupporttransit)** — The `MrxSupportTransit` module is responsible for managing the support transit system in the game.
- **[MrxSurgicalStrike](mrxsurgicalstrike)** — The `MrxSurgicalStrike` module is a specialized support system for surgical airstrikes.
- **[MrxTankBuster](mrxtankbuster)** — The `MrxTankBuster` module is a support system that provides an aerial strike capability to players.
