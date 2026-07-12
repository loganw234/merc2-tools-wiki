---
title: MrxUtilShell
parent: Shell Modules
nav_order: 28
inherits: none
tags: [shell, identical-to-resident]
verified: false
---

# MrxUtilShell

*Byte-for-byte identical to [`resident/MrxUtilShell`](../resident/mrxutil_shell) — see that page for full
documentation of its functions, inheritance, and events.*

## In the shell context
A two-function utility (`CallWithOptionalArgs`, `ProcessCallbackTable`) with no shell-specific behavior of
its own — imported by `MrxGui.lua` (used inside `GlobalFadeToBlack`/`_FadeUpdate` to fire queued fade
callbacks) and by `MrxGuiManager.lua` (`SetLoadingCompleteCallback`) purely as a safe "call this callback
if it exists" helper. It's named for the tree it originally shipped in rather than for anything unique to
the front end.
