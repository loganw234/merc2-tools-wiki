---

title: MrxSupportData

parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1


inherits: Inheritable

tags: [support, supply, delivery]

---

# MrxSupportData

*Module: mrxsupportdata.lua*

## Overview

The `MrxSupportData` module manages support items and their delivery in the game. It handles various types of support such as supplies, vehicles, airstrikes, and freebies. The module tracks the availability, cost, and requirements for each support item and provides functions to initialize, manage, and synchronize these items across the network.

## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxUtil`, `MrxPmc`, `mrxsupport`, `mrxartillery`, etc.

## Instance pattern

This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:

- `tSupportData`: A table that holds data about all purchasable support items, including their names, descriptions, icons, costs, and associated support objects.

- `tFreebieData`: A table that tracks mission-granted free uses of support items.

- `tRequirementsObtained`: A table that records whether specific recruit requirements have been obtained.

- `tRequirementStrings`: A table that holds strings describing the requirements for each recruit.

- `_kMaxStock`: A constant representing the maximum stock limit for support items, set to 99.

```

## Functions

### IsSupportEquippable(sKey)

- **Description**: Checks if a support item is equippable based on its key (`sKey`). It considers whether the recruit requirement has been met and any additional optional requirements.

- **Arguments**:

  - `sKey`: The unique identifier of the support item to check.

- **Returns**:

  - A boolean indicating whether the support item is equippable.

  - An optional string describing why the item is not equippable (e.g., missing recruit or requirement).

### SetHeliPilotRecruited(bRecruited)

- **Description**: Sets the recruitment status of the helicopter pilot. If `bRecruited` is true, it marks the helicopter pilot as recruited.

- **Arguments**:

  - `bRecruited`: A boolean indicating whether the helicopter pilot has been recruited.

### SetMechanicRecruited(bRecruited)

- **Description**: Sets the recruitment status of the mechanic. If `bRecruited` is true, it marks the mechanic as recruited.

- **Arguments**:

  - `bRecruited`: A boolean indicating whether the mechanic has been recruited.

### SetJetPilotRecruited(bRecruited)

- **Description**: Sets the recruitment status of the jet pilot. If `bRecruited` is true, it marks the jet pilot as recruited.

- **Arguments**:

  - `bRecruited`: A boolean indicating whether the jet pilot has been recruited.

### SetRequirement(sRequirement, bObtained)

- **Description**: Sets the status of a specific requirement. If `bObtained` is true, it marks the requirement as obtained.

- **Arguments**:

  - `sRequirement`: The identifier of the requirement to set.

  - `bObtained`: A boolean indicating whether the requirement has been obtained.

### SynchNetRecruits(tRecruits)

- **Description**: Synchronizes the recruitment status across the network. If the current instance is a server, it sends an event with the updated recruitment status. Otherwise, it updates the local recruitment status based on the received data.

- **Arguments**:

  - `tRecruits`: A table containing the recruitment status of various recruits.

### SetIgnoreRequirements(bIgnore)

- **Description**: Sets whether to ignore recruit requirements globally. If `bIgnore` is true, all recruit requirements are ignored.

- **Arguments**:

  - `bIgnore`: A boolean indicating whether to ignore recruit requirements.

### Init()

- **Description**: Initializes module-level state by setting up tables for requirements and requirement strings, and creating various support data entries.

- **Details**:

  - `tRequirementsObtained` is initialized as a table with keys representing different support types ("Fiona", "Copter", "Mechanic", "Pilot") and values set to `true`.

  - `tRequirementStrings` is initialized as a table mapping each support type to a corresponding string identifier.

  - Several support data entries are created using various support delivery modules (`mrxcratedelivery`, `mrxsupportcopterdelivery`, etc.). Each entry includes fields such as:

    - `sName`: Name of the support.

    - `sDescription`: Description of the support.

    - `sIcon`: Icon associated with the support.

    - `nMaxStock`: Maximum stock available for the support.

    - `nCashCost`: Cash cost to purchase the support.

    - `nFuelCost`: Fuel cost to use the support.

    - `oSupport`: The actual support object created by the respective delivery module.

    - `sType`: Type of the support (e.g., "Supply", "Heli", "Heavy", "Airstrike").

### Example Support Data Entries

- **tSupportData.aa**

  ```lua

  {

    sName = "[support.supply.aa.name]",

    sDescription = "[support.supply.aa.desc]",

    sIcon = "supplies_anti_air",

    nMaxStock = 99,

    nCashCost = 15000,

    nFuelCost = 40,

    oSupport = oSupport,  -- Instance of mrxcratedelivery

    sType = "Supply"

  }

  ```

- **tSupportData.ah1z**

  ```lua

  {

    sName = "[vehicle.ah1z]",

    sDescription = "[support.vehicle.ah1z.desc]",

    sIcon = "vehicles_heli_ah1z",

    nMaxStock = 99,

    nCashCost = 200000,

    nFuelCost = 180,

    oSupport = oSupport,  -- Instance of mrxsupportcopterdelivery

    sType = "Heli"

  }

  ```

- **tSupportData.al**

  ```lua

  {

    sName = "[support.supply.al.name]",

    sDescription = "[support.supply.al.desc]",

    sIcon = "supplies_AN_crate",

    nMaxStock = 99,

    nCashCost = 10000,

    nFuelCost = 40,

    oSupport = oSupport,  -- Instance of mrxcratedelivery

    sType = "Supply"

  }

  ```

### mrxsupportdata.cqb()

- **Description**: Initializes support data for the CQB (Close Quarters Battle) supply drop.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object with specific cargo, carelessness settings, and metadata. The support type is marked as "Supply".

### mrxsupportdata.cruisemissile()

- **Description**: Initializes support data for the Cruise Missile airstrike.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object configured for an aerial strike with specific costs and metadata. The support type is marked as "Airstrike".

### mrxsupportdata.daisycutter()

- **Description**: Initializes support data for the Daisy Cutter airstrike.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object for another type of aerial strike, with associated costs and metadata. The support type is marked as "Airstrike".

### mrxsupportdata.dinghy()

- **Description**: Initializes support data for the Dinghy boat delivery.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver various types of boats, including civilian and military variants. Sets carelessness and metadata. The support type is marked as "Boat".

### mrxsupportdata.dsvscoutvehicle()

- **Description**: Initializes support data for the DSV Scout Vehicle delivery.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object to deliver a specific vehicle, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.endriagoattack()

- **Description**: Initializes support data for the Endriago Attack helicopter delivery.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver a specific helicopter variant with associated costs and metadata. The support type is marked as "Heli".

### mrxsupportdata.endriagoelite()

- **Description**: Initializes support data for the Endriago Elite helicopter delivery.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver another helicopter variant, with specific costs and metadata. The support type is marked as "Heli".

### mrxsupportdata.endriagosuperiority()

- **Description**: Initializes support data for the Endriago Superiority helicopter delivery.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver a high-end helicopter variant, with associated costs and metadata. The support type is marked as "Heli".

### mrxsupportdata.ext()

- **Description**: Initializes support data for the EXT (Extended Transport) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object to deliver a specific vehicle, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.extgl()

- **Description**: Initializes support data for the EXT GL (Extended Transport with Grenade Launcher) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver a variant of the EXT vehicle equipped with a grenade launcher, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.fiona()

- **Description**: Initializes support data for the Fiona supply drop.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver specific supplies, with carelessness settings and metadata. The support type is marked as "Supply".

### mrxsupportdata.fuelairbomb()

- **Description**: Initializes support data for the Fuel Air Bomb airstrike.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object configured for an aerial strike using fuel air bombs, with associated costs and metadata. The support type is marked as "Airstrike".

### mrxsupportdata.gl()

- **Description**: Initializes support data for the GL (Grenade Launcher) supply drop.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver specific supplies, with carelessness settings and metadata. The support type is marked as "Supply".

### mrxsupportdata.gr()

- **Description**: Initializes support data for the GR (Guerilla) supply drop.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver specific supplies, with carelessness settings and metadata. The support type is marked as "Supply".

### mrxsupportdata.guntruckoc()

- **Description**: Initializes support data for the Guntruck (OC) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object to deliver a specific vehicle, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.hmmwvarmored50cal()

- **Description**: Initializes support data for the HMMWV (Armored) 50Cal vehicle delivery.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver a specific armored variant of the HMMWV, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.hmmwvarmoredgl()

- **Description**: Initializes support data for the HMMWV (Armored) GL vehicle delivery.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver another armored variant of the HMMWV equipped with a grenade launcher, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.hmmwvarmoredtow()

- **Description**: Initializes support data for the HMMWV (Armored) TOW vehicle delivery.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object to deliver a high-end armored variant of the HMMWV equipped with a TOW missile launcher, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.hmmwvavenger()

- **Description**: Initializes support data for the HMMWV (Avenger) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver a specific variant of the HMMWV, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.hmmwvsofttop()

- **Description**: Initializes support data for the HMMWV (Softtop) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver a civilian variant of the HMMWV, setting cargo, costs, and metadata. The support type is marked as "Civilian".

### mrxsupportdata.jetskiciv()

- **Description**: Initializes support data for the Jetski (Civ) boat delivery.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object to deliver various types of jetskis, including civilian and military variants. Sets carelessness and metadata. The support type is marked as "Boat".

### mrxsupportdata.junkers()

- **Description**: Initializes support data for the Junkers vehicle delivery.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver various types of junker vehicles, setting cargo, costs, and metadata. The support type is marked as "Civilian".

### mrxsupportdata.ka29b()

- **Description**: Initializes support data for the Ka29b helicopter delivery.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver a specific helicopter variant, with associated costs and metadata. The support type is marked as "Heli".

### mrxsupportdata.laserguidedbomb()

- **Description**: Initializes support data for the Laser Guided Bomb airstrike.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object configured for an aerial strike using laser-guided bombs, with associated costs and metadata. The support type is marked as "Airstrike".

### mrxsupportdata.laviii25mm()

- **Description**: Initializes support data for the LAVIII (25mm) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver a specific armored variant of the LAVIII, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.laviii50cal()

- **Description**: Initializes support data for the LAVIII (Minigun) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver another armored variant of the LAVIII equipped with a minigun, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.laviiiad()

- **Description**: Initializes support data for the LAVIII (AD) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object to deliver a high-end armored variant of the LAVIII equipped with an anti-drone system, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.laviiiat()

- **Description**: Initializes support data for the LAVIII (AT) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver another armored variant of the LAVIII equipped with an anti-tank system, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.laviiimewss()

- **Description**: Initializes support data for the LAVIII (MEWSS) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver a high-end armored variant of the LAVIII equipped with a multi-purpose weapon system, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.laviiimgs()

- **Description**: Initializes support data for the LAVIII (MGS) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object to deliver another armored variant of the LAVIII equipped with a machine gun system, setting cargo, costs, and metadata. The support type is marked as "Light".

### mrxsupportdata.lightmg()

- **Description**: Initializes support data for the Light MG supply drop.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver specific light machine guns, with carelessness settings and metadata. The support type is marked as "Supply".

### mrxsupportdata.luxury()

- **Description**: Initializes support data for the Luxury vehicle delivery.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver various types of luxury vehicles, setting cargo, costs, and metadata. The support type is marked as "Civilian".

### mrxsupportdata.m113aagr()

- **Description**: Initializes support data for the M113 AA (GR) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object to deliver a specific armored variant of the M113, setting cargo, costs, and metadata. The support type is marked as "Heavy".

### mrxsupportdata.m113aavz()

- **Description**: Initializes support data for the M113 AA (VZ) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Configures a `Support` object to deliver another armored variant of the M113, setting cargo, costs, and metadata. The support type is marked as "Heavy".

### mrxsupportdata.m113gr()

- **Description**: Initializes support data for the M113 (GR) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Sets up a `Support` object to deliver another armored variant of the M113, setting cargo, costs, and metadata. The support type is marked as "Heavy".

### mrxsupportdata.m113jammervz()

- **Description**: Initializes support data for the M113 Jammer (VZ) vehicle delivery.

- **Parameters**: None.

- **Behavior**: Creates a `Support` object to deliver a high-end armored variant of the M113 equipped with a jamming system, setting cargo, costs, and metadata. The support type is marked as "Heavy".

### GetFreebie(sSupportName)

Retrieves the freebie data for a given support name.

### AddAllFreebies()

Adds all freebies to the player's inventory.

### GetLocalRemote(vPlayers)

Determines if the players are local or remote. Returns two boolean values indicating whether there are local and/or remote players.

### _AddFreebie(sSupportName, nQty, bAddingAllFreebies, nMaxQty)

Adds a specified quantity of a freebie to the player's inventory. Handles network synchronization and updates the HUD support menu if necessary.

### _RemoveFreebie(sSupportName)

Removes a freebie from the player's inventory and updates the HUD support menu.

### AddFreebie(sSupportName, nQty, vPlayers, bAddingAllFreebies, nMaxQty)

Adds a specified quantity of a freebie to the player's inventory. Handles network synchronization if necessary.

### RemoveFreebie(sSupportName, vPlayers)

Removes a freebie from the player's inventory. Handles network synchronization if necessary.

### GetFreebieStringIndex(uStringHash)

Retrieves the support name associated with a given string hash.

### GetSupportStringIndex(uStringHash)

Retrieves the support name associated with a given string hash.

### NetEventCallback(nEventId, tArgs)

Handles network events related to adding or removing freebies.

### Add(tSupport, sFaction)

Adds support items to the player's inventory based on faction. Updates unlock status and checks for achievements.

### IsItemUnlocked(sSupportId, sFaction)

Checks if a support item is unlocked for a given faction.

### IsItemNew(sSupportId, sFaction)

Checks if a support item is new (not viewed) for a given faction.

### SetItemViewed(sSupportId, sFaction)

Marks a support item as viewed for a given faction.

### SaveSingleton()

Saves the current state of support data to a save table.

### LoadSingleton(tSaveData)

Loads the saved state of support data from a save table.

### AddSupportData(tSupportDataToAdd, sKey)

Adds new support data to the existing support data. Returns true if successful, nil otherwise.

### GetMaxQuantity()

Retrieves the maximum stock quantity for freebies.

### GetPlayerVisibleName(sSupportId)

Retrieves the player-visible name of a support item.

### GetFreebieName(sSupportId)

Retrieves the name of a freebie.

## Events

- **`Event.PlayerJoined(uGuid)`**: Listens for when a new player joins the session and updates the recruitment status accordingly.

- **`Event.PlayerLeft(uGuid)`**: Listens for when a player leaves the session and updates the recruitment status accordingly.

- **`Event.NetworkRecruitSync(tRecruits)`**: Listens for network events related to synchronizing recruit statuses across players.

## Notes for modders

- **Call-order requirements**: Ensure that `Init()` is called before any other functions in this module, as it sets up essential tables and initializes support data.

- **Pitfalls**: Be cautious when modifying the recruitment status or freebie quantities, as these changes can affect player progression and game balance.

- **Tunables**: The maximum stock limit for support items (`_kMaxStock`) is set to 99. This value can be adjusted in the module's constants if needed.

- **Decompiler artifacts**: There are no known decompiler artifacts in this module that require special attention.