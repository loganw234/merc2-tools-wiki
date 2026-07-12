---
title: MrxSoundShellBootstrap
parent: Shell Modules
nav_order: 6
inherits: none
tags: [shell]
verified: false
---

# MrxSoundShellBootstrap

## Overview
Sets up the front end's audio: ducking/fade rules for five mix categories, 69 per-faction and per-region music-cue bindings, then calls `MrxSound.Initialize()`. Also owns the audio half of shell teardown — fading the master volume out as the shell exits, called from [`ShellBootstrap`](shellbootstrap)'s `ResetSingleton`/`ShellExitComplete`.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxSound`, `MrxMusic`, `MrxSoundCategories`, `MrxSoundBanks`

`MrxSoundBanks` is imported but never referenced by name in this file's body — likely imported to guarantee sound banks are loaded/registered before `Init()` tries to bind cues against them.

## Instance pattern
Stateless manager module. One tunable module-level constant: `EXITSHELL_FADELENGTH = 0.5` (seconds), read by both this file's own `PreExitShell()` and by [`ShellBootstrap.ResetSingleton()`](shellbootstrap).

## Functions

### Init()
Logs `"SoundShellBootstrap.Init"`, then:
- Registers five fade/ducking categories via `MrxSoundCategories.SetFadeCategory(sCategory, sTargetBus, ...)`: `"vosequence"` ducks `sfx`/`chatter`/`music`; `"actionhijack"` ducks `Non_Action_Hijack`/`chatter`; `"survivalmode"` ducks `sfx`/`chatter`/`music`; `"fanfare"` ducks `sfx`/`vo`; `"satelliteview"` ducks `sfx`/`chatter`.
- Binds 69 music cues via `MrxMusic.BindMusicCue(sFactionOrRegion, sMood, nVariant, sCueName)`, covering the faction codes `an`, `oc`, `gr`, `ch`, `pmc` — these line up with the lowercased **PDA ID** column of [`MrxFactionManager`'s faction catalog](../resident/mrxfactionmanager#faction-catalog) (`AN` = Allied, `OC` = Oil Company, `GR` = Guerilla, `CH` = China, `PMC` = the player's company) — plus three freeplay region codes, `freeplay_city`, `freeplay_jungle`, `freeplay_water`. Moods bound per faction: `explore`, `action`, `mission_success`, `mission_failure`, `hijack` (1-3 variants depending on faction), `hijack_success`, `shell`, `pause`; the freeplay regions swap `hijack`/`hijack_success` for `high_action` and reuse the `mu_fac_pmc_win_01` cue for their own `mission_success`.
- Calls `MrxSound.Initialize()` last, after every category and cue is registered.

### PreExitShell()
`Sound.SetMasterVolume(0, EXITSHELL_FADELENGTH)` — fades the master volume to silence over `EXITSHELL_FADELENGTH` (0.5s). Called by [`ShellBootstrap.ResetSingleton()`](shellbootstrap).

### ExitShell()
`MrxSound.ExitShellState()`. Called by [`ShellBootstrap.ShellExitComplete()`](shellbootstrap), after the fade from `PreExitShell()` has had time to finish.

## Events
None — no `Event.*` calls in this file. (The timer that waits out the fade before calling `ExitShell()` lives in `ShellBootstrap`, not here.)

## Notes for modders
- **Every faction's and region's `"shell"` and `"pause"` cue binds to the same underlying cue name, `"mu_shell_01"`** — there's one shared main-menu/pause track regardless of context. To swap the menu music, override those `BindMusicCue(..., "shell", 1, ...)` / `(..., "pause", 1, ...)` calls (or just replace the `"mu_shell_01"` asset itself).
- The `Pir`/`Civ`/`Vza` factions from `MrxFactionManager`'s catalog have no cues bound here at all — only the five combat-relevant faction codes plus the three freeplay regions get music bindings in this file.
- `EXITSHELL_FADELENGTH` is the one real tunable in this file — raise it for a slower fade-to-silence on shell exit, and it'll stay in sync with `ShellBootstrap.ResetSingleton()` automatically, since that function times its own teardown event off this same constant (`+ 0.05`).
