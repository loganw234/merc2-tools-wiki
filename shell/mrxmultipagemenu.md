---
title: MrxMultipageMenu
parent: Shell Modules
nav_order: 23
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxMultipageMenu

*Byte-for-byte identical to [`resident/MrxMultipageMenu`](../resident/mrxmultipagemenu) — see that page
for full documentation of its functions, inheritance, and events.*

## In the shell context
Generic paginated dialog-box menu (`AddOption`/`Display`, with automatic Next-page/Previous-page options
once more than 8 entries are added). In this file set it's used exclusively by `MrxGuiShell`'s two
developer-only menus — `OpenSkipToMissionDialog` (the full mission skip list) and `OpenInstallDialog`
(HDD install choices) — both of which it renders through `MrxGui.DisplayDialogBox`.
