---
title: MrxGuiDialogBox
parent: Shell Modules
nav_order: 13
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiDialogBox

*Byte-for-byte identical to [`resident/MrxGuiDialogBox`](../resident/mrxguidialogbox) — see that page for
full documentation of its functions, inheritance, and events.*

## In the shell context
Builds the modal dialog boxes (plus the scrolling/wager variant and a Flash-driven
`OpenSystemDialogBox`) that back `MrxMultiPageMenu` — which in turn backs `MrxGuiShell`'s developer-only
skip-to-mission and HDD-install menus. `MrxGui.Init()` aliases `DisplayDialogBox`/`CloseDialogBox` straight
to this module's `DisplayDialogBox`/`Close`, so any shell code calling `MrxGui.DisplayDialogBox(...)` ends
up here.
