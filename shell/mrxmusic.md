---
title: MrxMusic
parent: Shell Modules
nav_order: 24
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxMusic

*Byte-for-byte identical to [`resident/MrxMusic`](../resident/mrxmusic) — see that page for full
documentation of its functions, inheritance, and events.*

## In the shell context
This module's cue tables carry an explicit `shell`/`pause` state (bound to `"mu_shell_01"`) for every
faction and freeplay region right alongside the gameplay states — `MrxSound.EnterShellState()`'s
`_StartShellMusic()` calls `Sound.TransitionMusic("shell")`, which resolves through these same bound
cues. The main-menu music runs on the identical state machine used in missions, just parked on the
"shell" state instead of "explore"/"action".
