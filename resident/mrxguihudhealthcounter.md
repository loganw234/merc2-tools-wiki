---

title: MrxGuiHudHealthCounter

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, hud]
verified: true
verified_note: verified stray-fence bug still clean (already fixed in earlier pass); confirmed all 21 top-level functions covered; corrected Events section — only 2 confirmed SetEventHandler call sites (GuiUpdate, ShowAllCounters), other named "events" (HealthChangedEventNew, ShowHealthEvent, E3HudModeEvent) have no SetEventHandler call site in this file and were unconfirmed guesses from function names

---



# MrxGuiHudHealthCounter



*Module: mrxguihudhealthcounter.lua*



## Overview

The `MrxGuiHudHealthCounter` module is responsible for managing the health counter display on the HUD. It handles various events related to health changes, visibility, and icon updates for both human and vehicle health counters. The module ensures that the health bar's color, length, and visibility are appropriately adjusted based on the current health status.



## Inheritance

- Inherits from: `none` (base/utility module)

- Imports: `MrxGui`, `MrxUtil`



## Instance pattern

This is a stateless manager/utility module. It does not track per-instance state but manages global settings and functions related to health counter display. Key fields include:



- **Constants**:

  - `_knShowTime = 2`: Duration for which the health counter is visible.

  - `_knPulsingThreshold = 20`: Health percentage below which pulsing effect starts.

  - `_knVisibleThreshold = 100`: Health percentage above which the counter remains visible.

  - `_knPulseTime = 0.4`: Duration of a single pulse animation cycle.



- **Tables**:

  - `_tDefaultIcon`: Default icon for human health counter with texture coordinates.

    ```lua

    {

      texture = "global_gui_hud02",

      u1 = 0.443359,

      v1 = 0.466797,

      u2 = 0.552734,

      v2 = 0.576172

    }

    ```

  - `_tArmorToIcon`: Mapping of vehicle armor labels to corresponding icons.

    ```lua

    {

      ArmorVehicle = { texture = "HUD_vehicle_armor_1", u1 = 0, v1 = 0, u2 = 1, v2 = 1 },

      ArmorLight = { texture = "HUD_vehicle_armor_2", u1 = 0, v1 = 0, u2 = 1, v2 = 1 },

      ArmorMedium = { texture = "HUD_vehicle_armor_3", u1 = 0, v1 = 0, u2 = 1, v2 = 1 },

      ArmorTank = { texture = "HUD_vehicle_armor_4", u1 = 0, v1 = 0, u2 = 1, v2 = 1 }

    }

    ```



## Functions



### HandleHealthChangedEventNew(oWidget, nCurHealth, nMaxHealth, bVehicle)

- Updates the health counter text and handles color transitions based on health changes.

- Adjusts the health bar's length and color to reflect current health.



### HandleInitializationNew(oWidget)

- Initializes custom data for the widget, storing its initial color and setting default values.



### HandleHealthChangedEventMain(oWidget, nCurHealth, nMaxHealth, bVehicle)

- Updates the health counter's visibility and pulsing effect based on current health.

- Adjusts the health bar's length and color to reflect current health.



### _SetCounterVisible(oUnused, oCounter)

- Sets the visibility of a counter widget to true.



### HandleUpdateMain(oWidget, nDeltaTime)

- Manages the countdown for hiding the health counter after it becomes fully visible.

- Hides the counter if its remaining time reaches zero.



### _LoopToRed(oWidget)

- Animates the health bar's color to red and loops back to neutral.



### _LoopToNeutral(oWidget)

- Animates the health bar's color back to neutral and loops to red.



### HandleShowHealthEvent(oWidget, tEvent)

- Shows the health counter if it is hidden and sets its remaining time based on an event.



### HandleInitializationMain(oWidget)

- Initializes various animation points and custom data for the widget.

- Sets up event handlers for `GuiUpdate` and `ShowAllCounters`.



### HandleIconUpdateHuman(oWidget, nCurHealth, nMaxHealth, bVehicle)

- Updates the translucency of the human health icon based on whether it's a vehicle.



### SetVehicleIcon(oWidget, tIcon)

- Sets the texture and coordinates for the vehicle icon widget.



### HandleIconUpdateVehicle(oWidget, nCurHealth, nMaxHealth, bVehicle)

- Updates the translucency and icon of the vehicle health counter.

- Determines the correct armor icon based on vehicle labels.



### HandleUpdateEvent(oWidget, nTimeSinceLastUpdate)

- Updates the health bar's length and texture coordinates based on time since last update.

- Manages the ghost bar's position to create a depleting effect.



### Min(nA, nB)

- Returns the minimum of two numbers.



### HandleHealthChangedEvent(oWidget, nCurHealth, nMaxHealth)

- Updates the health counter text and handles color transitions based on health changes.

- Adjusts the health bar's length and visibility to reflect current health.



### HandleInitialization(oWidget, Event)

- Initializes custom data for the widget, storing its initial health value and bar length.



### HandleVehicleInitialization(oWidget, Event)

- Sets the visibility of the vehicle icon to false and initializes it like a regular health counter.



### HandleUpdateEventForBackground(oWidget, nTimeSinceLastUpdate)

- Updates the background color of the health bar based on pulsing effects.

- Manages transitions between white and red colors for pulsing effect.



### HandleVehicleEvent(oWidget, nCurHealth, nMaxHealth, bInVehicle)

- Handles vehicle-specific logic for the health counter, including visibility and transition effects.



### HandleE3HudModeEvent(oWidget, tEvent)

This function handles the E3 HUD mode event for a given widget. It checks if the event is turned on or off and adjusts the visibility of the widget accordingly.



- If `tEvent.bOn` is true:

  - If the widget is not already in E3 HUD mode (`oWidget.CustomData.bE3HudMode` is false):

    - If the widget is currently invisible, it sets a flag `bStayInvisible` to true.

    - It hides the widget by setting its visibility to false.

    - It marks the widget as being in E3 HUD mode by setting `oWidget.CustomData.bE3HudMode` to true.



- If `tEvent.bOn` is false:

  - If the widget should not stay invisible (`bStayInvisible` is false), it sets the widget's visibility to true.

  - It marks the widget as no longer being in E3 HUD mode by setting `oWidget.CustomData.bE3HudMode` to false.



### DrawDebugRectangle(TargetWidget, t)

This function draws a debug rectangle on a target widget. It creates a text command with specified properties and adds it to the widget's drawing commands.



- The text command is created as a table with the following fields:

  - `CommandType`: "text"

  - `x`: 100

  - `y`: 100

  - `text`: The input string `t`

  - `font`: "lucida12"

  - `RedLevel`: 255 (red)

  - `GreenLevel`: 0 (green)

  - `BlueLevel`: 0 (blue)

  - `TranslucencyLevel`: 255 (fully opaque)

  - `HorizontalAnchor`: "left"

  - `VerticalAnchor`: "top"



- The text command is added to the first position of `TargetWidget.DrawingCommands`.



## Events

No `Event.*`/`Event.Create(...)` engine-event references appear in this file — confirmed by grep. There are exactly two confirmed `SetEventHandler` call sites, both inside `HandleInitializationMain`:

- **`"GuiUpdate"`** → `HandleUpdateMain` — per-frame countdown that hides the health counter after it's been fully visible for `_knShowTime` seconds.
- **`"ShowAllCounters"`** → `HandleShowHealthEvent` — re-shows the counter (if hidden) and resets its remaining visible time, using `tEvent.nTime` from the event payload if present.

The remaining `Handle*Event*`-named functions (`HandleHealthChangedEventNew`, `HandleHealthChangedEventMain`, `HandleHealthChangedEvent`, `HandleVehicleEvent`, `HandleIconUpdateHuman`, `HandleIconUpdateVehicle`, `HandleE3HudModeEvent`, etc.) have **no `SetEventHandler` call site anywhere in this file** — they follow the `Handle*` naming convention used elsewhere in the GUI code, but this file never wires them to a widget event key itself. They're presumably registered externally (in a layout file, similar to `mrxguihudactionhijack.lua`'s `_HandleInitialization`), or invoked directly by other modules by name — no call site found in the decompiled `resident/` corpus search performed for this page. Treat their names as suggestive, not confirmed subscriptions.



## Notes for modders

- **Call-order requirements**: Ensure that `HandleInitializationMain` is called before any other functions to properly initialize the widget's custom data and event handlers.

- **Pitfalls**: Be cautious with modifying the health counter's visibility and pulsing effects, as incorrect handling can lead to visual inconsistencies or performance issues.

- **Tunables**: The following constants can be adjusted for different behaviors:

  - `_knShowTime`: Duration for which the health counter is visible.

  - `_knPulsingThreshold`: Health percentage below which pulsing effect starts.

  - `_knVisibleThreshold`: Health percentage above which the counter remains visible.

  - `_knPulseTime`: Duration of a single pulse animation cycle.

- **Decompiler artifacts**: The function `Min(nA, nB)` is used to return the minimum of two numbers. This function appears redundant as Lua's built-in `math.min` could be used instead, but it is present in the decompiled code.