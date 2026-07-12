---
title: MrxSoundBanks
parent: Shell Modules
nav_order: 26
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxSoundBanks

*Byte-for-byte identical to [`resident/MrxSoundBanks`](../resident/mrxsoundbanks) — see that page for full
documentation of its functions, inheritance, and events.*

## In the shell context
The low-level, throttled asset-loading queue (`LoadSoundBank`/`UnloadSoundBank`/`LoadWaveBank`/
`UnloadWaveBank`, capped at `MAX_SUBMITTED = 64` in-flight requests) that `MrxSound.EnterShellState()`/
`ExitShellState()` call directly for the `"ui_shell"`, `"ui_hud"`, and `"music"` banks. This is the module
that actually issues the engine's `Sound.LoadBankWithCallback` calls when the main menu opens or closes.
