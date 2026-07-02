---
title: MrxGuiCinematic
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, cinematic]
---

# MrxGuiCinematic

*Module: mrxguicinematic.lua*

## Overview
The `MrxGuiCinematic` module is responsible for managing the display of cinematic movies and subtitles within the game's GUI. It provides functions to show, hide, and manage the lifecycle of these cinematic elements, including handling fade-in and fade-out animations, subtitle rendering, and input events.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
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

- **`Event.ObjectHibernation`**: Listens for object hibernation events to manage widget visibility and resource cleanup.
- **`Event.InputEvent`**: Handles input events, such as button presses, to control movie playback and hiding.
- **`Event.TimerRelative`**: Used for timing fade-in and fade-out effects, subtitle updates, and other timed actions.

## Notes for modders

1. **Call Order Requirements**:
   - Ensure that `ShowMovie` or `Show` is called before attempting to play or pause the movie.
   - Subtitle data should be properly formatted and passed to `ShowMovie` if subtitles are enabled.

2. **Pitfalls**:
   - Do not attempt to directly manipulate widget properties without using the provided functions, as this can lead to inconsistent state management.
   - Be cautious with subtitle timing; ensure that subtitle events do not overlap or conflict with each other.

3. **Tunables**:
   - Adjust `nFadeInTime` and `nFadeOutTime` parameters in `ShowMovie` and `Show` functions to control the duration of fade effects.
   - Modify subtitle display times within the subtitle data table to fine-tune when subtitles appear on screen.

4. **Decompiler Artifacts**:
   - Unused parameters (`oUnused`, `nPlaceholder`) are present in some internal functions but do not affect functionality.
   - Local variables that appear unused or are assigned but never read may be due to decompiler artifacts and can be ignored.