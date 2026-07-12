---
title: MrxGuiLoadScreen
parent: Shell Modules
nav_order: 15
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiLoadScreen

*Byte-for-byte identical to [`resident/MrxGuiLoadScreen`](../resident/mrxguiloadscreen) — see that page
for full documentation of its functions, inheritance, and events.*

## In the shell context
Shows and hides the loading-screen Flash movie and the spinning-skull "[SHELL.LoadSave.Saving]" icon in
response to the `LoadStateChange` event bound in `MrxGuiLoadLayout`. The same widget covers both leaving
the shell to start a mission and any later in-mission save, which is why its localization key is
`SHELL`-prefixed even though the code itself runs identically from either tree.
