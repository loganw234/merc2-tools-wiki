---

title: MrxGuiHudActionHijack

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, hud]

---



# MrxGuiHudActionHijack



*Module: mrxguihudactionhijack.lua*



## Overview

The `MrxGuiHudActionHijack` module is responsible for managing the action hijack HUD elements in the game. It provides functionality to display button prompts, handle user inputs, and manage various visual and audio cues related to player actions.



## Inheritance

- Inherits from: `none — base/utility module`

- Imports: `MrxGui`



## Instance pattern

This is a stateless manager/utility module (no per-instance tables). It tracks the following key fields:



- **Sound Variables**: Defines sound cues for different actions, such as `_ksPressSound`, `_ksErrorSound`, `_ksMashSound`, and `_ksRecoverSound`.

- **Joystick Table**: Reassigns and extends the `Joystick` table from `MrxGui` to include specific button mappings for various controller inputs.

- **Controller Sprite Texture Mapping**: A table mapping joystick button IDs to their corresponding sprite texture names for PC controllers.

- **_ControllerSpriteTextureMapping**: Maps joystick button constants to texture names for standard controllers.

- **_ControllerXboxSpriteTextureMapping**: Maps joystick button constants to texture names for Xbox controllers.

- **_ControllerSpriteData**: Provides sprite data (likely coordinates or dimensions) for each joystick button on standard controllers.

- **_ControllerXboxSpriteData**: Provides sprite data for each joystick button on Xbox controllers.



The module manages the display and behavior of action hijack HUD elements, including button prompts, fail icons, and timer animations. It also handles sound effects associated with player actions.



## Functions



### ShowButton(uGuid, nButton, nTime, nRepeatTime, nXPosition, nYPosition, nTranslucency, bShowSparks, nElapsedTime, bFillTimer, bClockwise, bIsRecovery, bShowTimer, nScale)

- **Purpose**: Displays a button prompt overlay with various customizable options such as position, animation, and sound effects.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.

  - `nButton`: Identifier for the button to display.

  - `nTime`: Duration of the countdown timer.

  - `nRepeatTime`: Time for repeating animations.

  - `nXPosition`, `nYPosition`: Position on the screen.

  - `nTranslucency`: Transparency level.

  - `bShowSparks`: Boolean to show spark animations.

  - `nElapsedTime`: Elapsed time for the timer.

  - `bFillTimer`: Boolean to fill the timer clockwise or counterclockwise.

  - `bClockwise`: Boolean indicating the direction of the timer.

  - `bIsRecovery`: Boolean to indicate recovery mode.

  - `bShowTimer`: Boolean to show the timer.

  - `nScale`: Scale factor for the widget.



### HideButton(uGuid)

- **Purpose**: Hides the button prompt overlay and stops any animations or sounds associated with it.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.



### ShowFail(uGuid, nDuration)

- **Purpose**: Displays a fail icon and plays an error sound when the player fails an action hijack.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.

  - `nDuration`: Duration for which the fail icon is visible.



### GetElapsedTime(uGuid)

- **Purpose**: Retrieves the elapsed time of the countdown timer for a specific button prompt overlay.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.

- **Returns**: The elapsed time or `nil` if the widget is not found.



### SetDisplayVisible(uGuid, bVisible)

- **Purpose**: Sets the visibility of the entire action hijack display and stops any animations or sounds.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.

  - `bVisible`: Boolean to set the visibility.



### SetDisplayButton()

- **Purpose**: This function is deprecated and does nothing.



### SetDisplayMashAnimation()

- **Purpose**: This function is deprecated and does nothing.



### _HandleInitialization(oWidget)

- **Purpose**: Initializes the action hijack display by creating and positioning various GUI elements such as buttons, timers, fail icons, and spark animations.

- **Parameters**:

  - `oWidget`: The GUI widget to initialize.



This part of the module does not define any top-level functions. It only contains module-level state definitions as described above.



## Events

(list engine events this module subscribes to/fires, and what triggers it)



- **Event.OnActivate(uGuid, uRuntimeOwner, iArg)**: This event is triggered when the world object instance is spawned/activated. The module responds by calling `Awake` to initialize the per-instance table.

- **Event.OnDeactivate(uGuid)**: This event is triggered when the instance is being torn down (despawned/unloaded). The module handles cleanup and deletion of the per-instance table.

- **Event.OnUse(uGuid, ...)**: This event is triggered when the player interacts with/uses the object. The module may respond to this event to handle specific actions related to the action hijack display.



## Notes for modders

(call-order requirements, pitfalls, tunables, decompiler artifacts)



- **Call Order**: Ensure that `OnActivate` and `OnDeactivate` are called in the correct order to properly initialize and clean up the per-instance table. The `Awake` function should be called after `OnActivate` to set up the GUI elements.

  

- **Pitfalls**: Be cautious when modifying or extending this module, as changes to the button mappings or sprite texture names may affect the visual and functional behavior of the action hijack display.



- **Tunables**: The sound cues (`_ksPressSound`, `_ksErrorSound`, `_ksMashSound`, `_ksRecoverSound`) can be modified to change the audio feedback for different actions. Similarly, the `nTime` and `nRepeatTime` parameters in `ShowButton` can be adjusted to control the duration of the countdown timer and repeating animations.



- **Decompiler Artifacts**: The module may contain unused locals or duplicate table keys as artifacts of the decompilation process. These should not affect the functionality of the module but should be noted for clarity.