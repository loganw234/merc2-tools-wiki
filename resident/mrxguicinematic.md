---
title: MrxGuiCinematic
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, cinematic]
verified: true
verified_note: 'deeper pass: fixed Imports (MrxGuiBase/MrxGui/MrxGuiManager/MrxSound, not MrxUtil); rewrote Events (removed hallucinated Event.ObjectHibernation/Event.InputEvent — only Event.Create(Event.TimerRelative)/Event.Delete are real; input is a "ControllerInput" widget handler); added net-sync, 01_VIK_01 subtitle special-case, and 30fps/fade tunables'
---

# MrxGuiCinematic

*Module: mrxguicinematic.lua*

## Overview
The `MrxGuiCinematic` module is responsible for managing the display of cinematic movies and subtitles within the game's GUI. It provides functions to show, hide, and manage the lifecycle of these cinematic elements, including handling fade-in and fade-out animations, subtitle rendering, and input events. The actual widget tree it drives (the "Cinematic Placeholder" root, its movie/subtitle/text children) is defined in the paired layout file [MrxGuiCinematicLayout](mrxguicinematiclayout), which binds this module's `_HandleInitializationEvent` and `_InitializeSubtitleBuffer` to those widgets.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase`, `MrxGui`, `MrxGuiManager`, `MrxSound` (the source's `import(...)` lines — the previous draft's "MrxUtil" was wrong)

See [MrxGuiBase](mrxguibase) (widget/animation primitives, `Joystick` button constants, control focus), [MrxGui](mrxgui) (fade helpers), [MrxGuiManager](mrxguimanager) (`ToggleHud`/`GetHudState`), and [MrxSound](mrxsound) (`EnterCinematicState`/`ExitCinematicState`).

## Instance pattern
**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry anywhere
in source — `Show`/etc. operate on a caller-supplied `oWidget` parameter, not a self-managed per-object
table. This is one shared movie-playback element, not something spawned per world object. Key fields:
- `bShowMoviePending`: A boolean flag indicating whether a movie is pending to be shown.
- Other state fields related to movie playback, subtitles, and widget management are not explicitly listed here but are managed internally within the module.

## Functions

### Show(oWidget, sTexture, sText, nFadeInTime, nFadeOutTime, fCallback, tCallbackData)
- **Description**: Displays a widget with a texture and text, setting up fade-in animations and event handlers.
- **Parameters**:
  - `oWidget`: The widget to display.
  - `sTexture`: The texture file to set on the widget.
  - `sText`: The text to display.
  - `nFadeInTime`: Duration of the fade-in effect in seconds.
  - `nFadeOutTime`: Duration of the fade-out effect in seconds.
  - `fCallback`: A callback function to be called after the movie is shown.
  - `tCallbackData`: Data to pass to the callback function.

### IsMovieRunning(oWidget)
- **Description**: Checks if a movie is currently running or fading out.
- **Parameters**:
  - `oWidget`: The widget to check.
- **Returns**: A boolean indicating whether the movie is running or fading out.

### IsMovieHiding(oWidget)
- **Description**: Checks if a movie is in the process of hiding slowly.
- **Parameters**:
  - `oWidget`: The widget to check.
- **Returns**: A boolean indicating whether the movie is hiding slowly.

### ShowMovie(oWidget, sFile, nFadeInTime, nFadeOutTime, fCallback, tCallbackData, bSubtitles, tSubtitles)
- **Description**: Shows a cinematic movie with optional subtitles, handling loading and playing of the movie.
- **Parameters**:
  - `oWidget`: The widget to display the movie in.
  - `sFile`: The file name of the movie to play.
  - `nFadeInTime`: Duration of the fade-in effect in seconds.
  - `nFadeOutTime`: Duration of the fade-out effect in seconds.
  - `fCallback`: A callback function to be called after the movie is shown.
  - `tCallbackData`: Data to pass to the callback function.
  - `bSubtitles`: Boolean indicating whether subtitles should be displayed.
  - `tSubtitles`: Table containing subtitle data.

### SubtitleImportCallback(tArgs, oModule)
- **Description**: Callback for dynamic import of subtitle data, then calls `ShowMovie` with the loaded data.
- **Parameters**:
  - `tArgs`: Arguments passed to the callback.
  - `oModule`: The module containing the imported subtitle data.

### PlayMovie(oWidget)
- **Description**: Plays the movie currently set in the widget.
- **Parameters**:
  - `oWidget`: The widget containing the movie.

### PauseMovie(oWidget)
- **Description**: Pauses the movie currently set in the widget.
- **Parameters**:
  - `oWidget`: The widget containing the movie.

### _Hide(oWidget)
- **Description**: Hides the widget and cleans up resources, calling any registered callback function.
- **Parameters**:
  - `oWidget`: The widget to hide.

### HideSlow(oWidget)
- **Description**: Initiates a slow hiding process for the widget, fading out elements and stopping the movie.
- **Parameters**:
  - `oWidget`: The widget to hide slowly.

### _HandleInitializationEvent(oWidget)
- **Description**: Handles initialization of the widget, setting up child widgets and custom data.
- **Parameters**:
  - `oWidget`: The widget being initialized.

### _HandleInputEvent(oWidget, tEvent)
- **Description**: Handles input events for the widget, such as hiding the movie when a specific button is pressed.
- **Parameters**:
  - `oWidget`: The widget handling the event.
  - `tEvent`: The event data.

### _FadeInElements(oUnused, oWidget, nFadeInTime, tSubtitleData, nPlaceholder)
- **Description**: Animates elements of the widget to fade in, setting up subtitle and movie playback.
- **Parameters**:
  - `oUnused`: Unused parameter.
  - `oWidget`: The widget being animated.
  - `nFadeInTime`: Duration of the fade-in effect in seconds.
  - `tSubtitleData`: Table containing subtitle data.
  - `nPlaceholder`: Placeholder parameter.

### _ActivateCinematicState(oUnused, oWidget, tSubtitleData, nPlaceholder)
- **Description**: Activates the cinematic state by setting up focus, game state, and playing the movie with subtitles.
- **Parameters**:
  - `oUnused`: Unused parameter.
  - `oWidget`: The widget being activated.
  - `tSubtitleData`: Table containing subtitle data.
  - `nPlaceholder`: Placeholder parameter.

### _EndHideAnimation(oWidget)
- **Description**: Ends the hiding animation by setting the widget to invisible and removing child widgets.
- **Parameters**:
  - `oWidget`: The widget ending its hide animation.

### _InitializeSubtitleBuffer(oSubtitle)
- **Description**: Initializes subtitle buffer settings, including wrapping text and setting up event handlers.
- **Parameters**:
  - `oSubtitle`: The subtitle widget to initialize.

### BeginSubtitles(oSubtitle, tRawSubtitleData)
- **Description**: Begins displaying subtitles based on the provided raw subtitle data.
- **Parameters**:
  - `oSubtitle`: The subtitle widget.
  - `tRawSubtitleData`: Raw subtitle data to process and display.

### _TimeLessThan(tData1, tData2)
- **Description**: Compares two subtitle data entries by their time values.
- **Parameters**:
  - `tData1`: First subtitle data entry.
  - `tData2`: Second subtitle data entry.
- **Returns**: A boolean indicating whether the first entry's time is less than the second's.

### StopSubtitles(oSubtitle)
This function stops the subtitles for a given subtitle object. It clears all relevant data fields in the subtitle's custom data table, sets event handlers to nil, and resets the text of both the main subtitle and the super subtitle.

### HandleSubtitleUpdate(oSubtitle, nDeltaTime)
This function handles the update of subtitles based on the elapsed time (`nDeltaTime`). It processes the subtitle data, updates the display times, and collects new subtitles to be displayed. If the current display time or super display time reaches zero, it clears the respective text fields. The function also wraps the text for both the main and super subtitles and sets their locations accordingly.

## Events

The only real event-system call in this file is a **retry timer**: when `ShowMovie` is asked to play
while a movie is already visible/fading, it schedules itself again in 0.05 s via
`Event.Create(Event.TimerRelative, {0.05}, ShowMovie, {...})`, storing the handle on
`oWidget.retryEvent`; `_Hide` cancels it with `Event.Delete`. There are **no** `Event.ObjectHibernation`
or `Event.InputEvent` subscriptions — the previous draft invented those.

Everything else is widget-level, not `Event.*` engine events:
- **Input** is wired with `oWidget:SetEventHandler("ControllerInput", _HandleInputEvent)`; the skip
  button is `MrxGuiBase.Joystick.BUTTON_PAD2_D`, and only fires on the server / in single-player.
- **Subtitle ticking** uses `oSubtitle:SetEventHandler("GuiUpdate", HandleSubtitleUpdate)` — a per-frame
  GUI callback, not a timer.
- **Multiplayer sync**: the server calls `Net.SendEvent_ShowMovie(sFile, nFadeInTime, nFadeOutTime, bSubtitles)`
  on start and `Net.SendEvent_HideMovie()` on hide, so clients mirror the cinematic; clients that don't
  yet have subtitles loaded bail early instead of playing unsynced.

## Notes for modders

- **Movies are Scaleform `.gfx` clips**, set by name with `oMovie:SetMovie(sFile)`. `sFile` is the movie
  identifier (e.g. `"01_VIK_01"`), not a `.md`/texture path.
- **Subtitle files are loaded dynamically** via `dynamic_import("Subtitles_" .. sFile, ...)`. There is one
  hard-coded special case: movie `"01_VIK_01"` loads subtitle module `"TECHNOV"` instead of
  `"Subtitles_01_VIK_01"`. If you add a movie and want subtitles, ship a matching `Subtitles_<name>` module
  (returning a `SubtitleData` table) or pass `tSubtitles` directly.
- **Subtitle table row format** (confirmed from `HandleSubtitleUpdate`): `{startTime, text, duration, bSuper}`.
  `startTime` is compared against movie time; `bSuper` (index 4) routes the line to the top "supersubtitle"
  band and, when false, the line is also skipped entirely if the player has subtitles disabled
  (`Sys.SubtitlesEnabled()`). Default duration if `[3]` is nil is `3` seconds.
- **Movie time is derived from frame count** as `0.033333335 * oMovie:GetCurrentFrame()`, i.e. the code
  assumes **30 fps** — subtitle `startTime` values are in that 30-fps timebase.
- **Fade tunables**: `nFadeInTime`/`nFadeOutTime` default to **0.2 s** when not a number (in both `Show` and
  `ShowMovie`). `Show` also pins subtitle/text baseline at `nBottom = 400`.
- **`Show` vs `ShowMovie`**: `Show` displays a still texture + text (no `.gfx`); `ShowMovie` plays an actual
  movie and, on the server, auto-hides via `oMovie:SetEndCallback(HideSlow, {oWidget})`. `Hide`/`HideSlow`
  are the same function (aliased in `_HandleInitializationEvent`); `_Hide` is the immediate teardown.
- **HUD is force-off during playback**: `_ActivateCinematicState` records each player's HUD state in
  `CustomData.tHudStates` and restores it on hide via `MrxGuiManager.ToggleHud(uPlayer, true)`. It also
  requests game state `"cinematic"` (restored to `"ingame"` on hide) and toggles `MrxSound` cinematic state.
- **Decompiler artifacts**: `oUnused`/`nPlaceholder` params on some internal callbacks are unused; the local
  `sTexture` referenced in `ShowMovie` is never assigned there (dead branch). Harmless — don't rely on them.