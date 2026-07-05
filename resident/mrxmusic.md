---

title: MrxMusic

parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [music, dynamic]

---



# MrxMusic



*Module: mrxmusic.lua*



## Overview

The `MrxMusic` module is responsible for managing and controlling the music in the game. It handles various music states, transitions, and special music cues, ensuring that the music aligns with the player's actions and game events. The module also manages dynamic music settings and network synchronization to maintain consistent audio experiences across multiplayer sessions.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxUtil`, `Net`



## Instance pattern

This is a stateless manager/utility module (no per-instance tables). It tracks the following key fields:

- **NETEVENT_ENTERFREEPLAY**: Constant representing the event for entering freeplay mode.

- **NETEVENT_ENTERCONTRACT**: Constant representing the event for entering contract mode.

- **NETEVENT_PLAYSPECIALMUSIC**: Constant representing the event for playing special music.

- **NETEVENT_STOPSPECIALMUSIC**: Constant representing the event for stopping special music.

- **_bPrevDynamic**: Boolean flag to track whether dynamic music was previously enabled.

- **_tMusicCues**: Table containing music cues categorized by factions and freeplay modes. Each category has subcategories for different states like explore, action, mission_success, etc., with lists of music cue names.

- **_sRootFactionRegion**: String representing the root faction region for music.

- **_sSourceMusicState**: String representing the source music state.

- **_tSourceMusicTransitions**: Table defining transitions between different source music states.

- **_sHijackSuccessMusicState**: String representing the hijack success music state.

- **_sHijackResumeMusicState**: String representing the hijack resume music state.

- **_fNonActionInterval**: Float representing the non-action interval for music.

- **_fActionInterval**: Float representing the action interval for music.

- **_tMiscMusicStates**: Table containing miscellaneous music states.

- **_evClientJoined**: Event handle for client joined event.



## Functions



### _DisableDynamicMusic()

Disables dynamic music and stores its previous state.



### _RestoreDynamicMusic()

Restores the dynamic music to its previous state.



### SetMusicActionInterval(fActionInterval)

Sets the action interval for music. If the provided interval is less than 0, it logs a warning and uses the default interval.



### BindMusicCue(sFaction, sState, iCueIndex, sCue)

Binds a music cue to a specific faction, state, and index. Logs warnings if the faction or state is not found or if the cue index is out of range.



### _InitializeMusic()

Initializes music by setting up factions, states, transitions, and other configurations. It also sets up network events for player joining and sends relevant custom events.



### SendPlayerJoinEvents()

Sends custom network events to handle player join scenarios, including entering freeplay or contract modes and playing special music if applicable.



### _InitializeFaction(sFaction)

Initializes music states and transitions specific to a faction. It adds various music states and sets action thresholds and transitions accordingly.



### _InitializeFreeplay(sFreeplay)

Initializes music states and transitions specific to freeplay modes. Similar to `_InitializeFaction`, but with additional states like high_action.



### _BindMusicStateCues(sFaction, tCues)

Binds music cues to their respective states for a given faction.



### Reset()

Resets the music settings by enabling dynamic music, cleaning up special music, and resetting various flags and locks.



### EnterFreeplayMusic()

Handles entering freeplay mode by resetting music settings, activating faction region music, transitioning to explore state, and sending relevant network events.



### EnterContractMusic(sFaction)

Handles entering contract mode by setting the faction music, locking it, transitioning to explore state, and sending relevant network events.



### PlayFanfare(bMissionSuccess)

Plays a fanfare based on whether the mission was successful or not. It cleans up special music and transitions to the appropriate music state (mission_success or mission_failure).



### PlaySpecialMusic(sMusicCue)

Plays a special music cue. It locks faction music, sets the current miscellaneous music index, clears and binds the specified music cue, transitions to it, and sends a network event if the server is active.



### _SetMiscMusicIndex()

Toggles the current miscellaneous music index between 1 and 0.



### _ResumeSpecialMusic()

Resumes playing special music by transitioning to the current miscellaneous music state if special music is currently playing.



### _IsPlayingSpecialMusic()

Returns whether special music is currently playing.



### StopSpecialMusic(sNewState)

Stops the special music, cleans up the music state, transitions to a new state or "none" if no state is provided, and sends a network event if the server is active.



### _CleanupSpecialMusic()

Cleans up the special music by unlocking faction music, resetting the miscellaneous music index, setting the playing flag to false, and sending a network event if the server is active.



### AddMusicPlaylist(sPlaylist, fGap)

Adds a music playlist with a specified gap between tracks.



### BindPlaylistCue(sPlaylist, sCue)

Binds a music cue to a specified playlist.



### ClearMusicPlaylist(sPlaylist)

Clears a specified music playlist.



### GetFactionByStringHash(uFactionStringHash)

Retrieves the faction name by its string hash from the `_tMusicCues` table. Returns "nil" if no matching faction is found.



### GetStateByStringHash(uStateStringHash)

Retrieves the state name by its string hash from the `_tMusicCues` table. Returns "silence" if no matching state is found.



### NetEventCallback(nEventType, tArgs)

Handles network events related to music:

- `NETEVENT_ENTERFREEPLAY`: Enters freeplay music.

- `NETEVENT_ENTERCONTRACT`: Enters contract music for a specified faction.

- `NETEVENT_PLAYSPECIALMUSIC`: Plays a special music cue.

- `NETEVENT_STOPSPECIALMUSIC`: Stops the special music and cleans up if necessary.



## Events

This module subscribes to and fires several engine events related to music management:



- **`NETEVENT_ENTERFREEPLAY`**: Triggered when entering freeplay mode. The module handles this by resetting music settings, activating faction region music, transitioning to explore state, and sending relevant network events.

  

- **`NETEVENT_ENTERCONTRACT`**: Triggered when entering contract mode for a specific faction. The module sets the faction music, locks it, transitions to explore state, and sends relevant network events.



- **`NETEVENT_PLAYSPECIALMUSIC`**: Triggered to play a special music cue. The module locks faction music, sets the current miscellaneous music index, clears and binds the specified music cue, transitions to it, and sends a network event if the server is active.



- **`NETEVENT_STOPSPECIALMUSIC`**: Triggered to stop the special music. The module cleans up the music state, transitions to a new state or "none" if no state is provided, and sends a network event if the server is active.



## Notes for modders

- **Call-order requirements**: Ensure that `_InitializeMusic()` is called during initialization to set up all necessary configurations and network events.

  

- **Pitfalls**: Be cautious with music cue bindings; ensure that faction and state names are correctly specified to avoid warnings or errors. Also, be aware of the action intervals (`_fNonActionInterval` and `_fActionInterval`) which can affect music transitions.



- **Tunables**: The module provides tunable parameters such as `_fNonActionInterval` and `_fActionInterval`. Adjusting these values can help fine-tune the music experience based on gameplay dynamics.



- **Decompiler artifacts**: There are no significant decompiler artifacts noted in this module. All variables and functions appear to be used correctly, and there are no redundant or unused assignments.