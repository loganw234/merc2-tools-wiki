---

title: MrxGuiHudHealthCounter

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, hud]
verified: true
verified_note: 'deeper pass: CORRECTED imports (source has NO import() at all — the claimed MrxGui/MrxUtil imports were fabricated; it uses Player/Vehicle/Object namespaces directly); surfaced the _tArmorToIcon armor-label→texture map and _tDefaultIcon; confirmed the 2 SetEventHandler sites (GuiUpdate/ShowAllCounters) and all constants; all 21 functions re-verified'

---



# MrxGuiHudHealthCounter



*Module: mrxguihudhealthcounter.lua*



## Overview

The `MrxGuiHudHealthCounter` module is responsible for managing the health counter display on the HUD. It handles various events related to health changes, visibility, and icon updates for both human and vehicle health counters. The module ensures that the health bar's color, length, and visibility are appropriately adjusted based on the current health status.



## Inheritance

- Inherits from: `none` (base/utility module)

- Imports: **none** — this file has no `import()` line. It calls engine namespaces directly: [Player](../namespaces/player) (`Player.GetCharacter`, `Player.GetOwner` via `oWidget:GetOwner()`), [Vehicle](../namespaces/vehicle) (`Vehicle.GetFromRider`), and [Object](../namespaces/object) (`Object.HasLabel`), plus `string.format` and `Debug.Printf`.

{: .note }
> The earlier draft listed `Imports: MrxGui, MrxUtil`. **Neither is imported** — there is no `import(...)` statement anywhere in the source, and no `MrxGui.`/`MrxUtil.` call. Corrected.

## Instance pattern

**Stateless module + per-widget `CustomData`.** No `import`, no `tInstance`, no metatable. Each health-counter widget stores its own state in `oWidget.CustomData` (color rest-point, `nHealthValue`, `nBarLength`, `nRemainingTime`, `bPulsing`, `bHidden`, `bE3HudMode`, etc.). Note there are **two parallel implementations** in this one file — a "Main/New" set (`HandleInitializationMain`, `HandleHealthChangedEventMain`, `HandleHealthChangedEventNew`) that animates via named animation points, and an older child-index set (`HandleInitialization`, `HandleHealthChangedEvent`, `HandleUpdateEvent`) that manipulates `oWidget:GetChildren()[3/4/5]` bar segments directly. A given HUD layout wires up one or the other.

Module-level constants and tables:



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

- **Tunable constants** (top of file): `_knShowTime = 2` (seconds the counter stays up after a change before auto-hiding), `_knPulsingThreshold = 20` (health % below which the low-health red pulse starts), `_knVisibleThreshold = 100` (at/above this % the auto-hide countdown is allowed to run — i.e. only a full-health counter auto-hides), `_knPulseTime = 0.4` (seconds per pulse half-cycle).
- **Vehicle armor icon mapping** (`_tArmorToIcon`, `local`): the vehicle health icon is chosen by [`Object.HasLabel`](../namespaces/object) on the ridden vehicle: `ArmorVehicle → HUD_vehicle_armor_1`, `ArmorLight → HUD_vehicle_armor_2`, `ArmorMedium → HUD_vehicle_armor_3`, `ArmorTank → HUD_vehicle_armor_4` (all full-texture `u/v = 0..1`). If none match it falls back to `_tDefaultIcon` (`global_gui_hud02`, sub-rect `u1=0.443359 v1=0.466797 u2=0.552734 v2=0.576172`). These `local` tables aren't accessible from other files — to change the icon set, edit them in this module. Lookup path: `Vehicle.GetFromRider(Player.GetCharacter(owner))`.
- **Low-health color logic**: the "New" path snaps the neutral animation point to `(128,16,16)` when crossing below 20% and back to the original color above 20%; damage flashes `(216,16,16)` red, healing flashes `(16,128,16)` green, then eases back over `1`s. The "Main" pulse point is `(210,0,0)`. The background-pulse path (`HandleUpdateEventForBackground`) ramps color at `192`/s normally and `512`/s while pulsing.
- **Two implementations, pick one**: don't wire both the `*Main`/`*New` handlers and the child-index `HandleInitialization`/`HandleHealthChangedEvent`/`HandleUpdateEvent` handlers to the same widget — they assume different child layouts (the latter reads `GetChildren()[3]`=background, `[4]`=ghost/delta bar, `[5]`=fill bar, `[1]`=pulse layer).
- **Debug noise**: `HandleHealthChangedEvent` prints `"<--> HandleHealthChangedEvent"` every call via `Debug.Printf` — engine log spam, harmless. `DrawDebugRectangle(TargetWidget, t)` is a dev-only helper that stamps red `lucida12` text at (100,100) via `TargetWidget.DrawingCommands[1]`; nothing in this file calls it.
- **`Min(nA, nB)`** duplicates `math.min` (decompiler-preserved); used by the background-pulse color ramp. `_SetCounterVisible(oUnused, oCounter)` takes a leading unused arg because it's used as an `AnimateToPoint` completion callback (the callback receives the animating widget first).