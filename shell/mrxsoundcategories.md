---
title: MrxSoundCategories
parent: Shell Modules
nav_order: 27
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxSoundCategories

*Byte-for-byte identical to [`resident/MrxSoundCategories`](../resident/mrxsoundcategories) — see that
page for full documentation of its functions, inheritance, and events.*

## In the shell context
Category fade/pitch ducking tables (`Fade`/`Pitch`, keyed by mode strings like `"actionhijack"`/
`"survivalmode"`/`"satelliteview"`), configured both here (`_AdditionalFadeSetup`, credits ducking) and
from the shell-only `MrxSoundShellBootstrap.Init()` (which registers the `vosequence`/`actionhijack`/
`survivalmode`/`fanfare`/`satelliteview` entries). `MrxSound.lua`'s `BeginActionHijack`/`BeginSurvivalMode`/
etc. call into this same table regardless of which tree the call originates from.
