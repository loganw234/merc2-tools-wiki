---
title: MrxGuiNumericBox
parent: Shell Modules
nav_order: 19
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxGuiNumericBox

*Byte-for-byte identical to [`resident/MrxGuiNumericBox`](../resident/mrxguinumericbox) — see that page
for full documentation of its functions, inheritance, and events.*

## In the shell context
Builds the digit-entry spinner dialog (`DisplayNumericBox`), aliased into the shared `MrxGui` facade right
alongside `MrxGuiDialogBox` (`MrxGui.Init()` sets `DisplayNumericBox = MrxGuiNumericBox.DisplayNumericBox`).
`DisplayNumericBox` itself calls `LTILibName.ChangeShellState(true)` before building the box, directly
announcing to the front end's shell-state machine that a modal numeric input is open.
