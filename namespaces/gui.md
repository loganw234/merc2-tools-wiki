---
title: Gui
parent: Engine Namespaces
nav_order: 11
---

# Gui

## Overview

`Gui` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it, no
`import()` call needed, and it's always globally available to every script. It covers low-level GUI
plumbing: toggling which marker types render on screen (faction/pickup/player/vehicle-entrance), a set of
underscore-prefixed internal marker primitives that the public `Marker` namespace appears to wrap, font and
texture loading for the HUD, language/localization queries, controller-type detection, reticle screen
position, and a handful of shell-lifecycle/dev-only hooks.

**A live-probing caveat worth knowing before concluding a function "doesn't exist":** during a live
WebSocket lua-bridge probe (2026-07-22), some `Gui` functions came back nil/inert when called on the
runtime global `_G.Gui`. Gui functionality apparently does not live entirely on `_G.Gui` itself — some of
it lives only under a separate `_GuiInternal` table instead (a real, separate table the wiki already
documents extensively as the primitive layer beneath `MrxGuiBase`'s widget methods — see
`resident/mrxguibase.lua`). This is a real, confirmed finding, not a guess: don't conclude a `Gui` function
"doesn't exist" just because it's absent/nil on `_G.Gui` — it may only be reachable via `_GuiInternal`.

## Provenance

This page's function list comes from a live `pairs(Gui)` enumeration in-game (via lua-bridge), not from
reading engine source — the engine implementation isn't available to us. That means the list of 38 function
names below is complete and authoritative: every one of them really exists on the namespace. It does **not**
mean every entry is documented with confirmed arguments. Where a function is actually called somewhere in
the ~230 decompiled `.lua` scripts, we can show a real argument pattern. Where it isn't called anywhere in
that corpus, we only know the name — arguments, return values, and behavior for those are unconfirmed.

## Functions

### Marker Enable Toggles

| Function | Signature (best-known) | Notes |
|---|---|---|
| `EnablePlayerMarkers` | `Gui.EnablePlayerMarkers(bEnabled)` | Confirmed with a single boolean argument in real scripts, e.g. `Gui.EnablePlayerMarkers(false)` / `Gui.EnablePlayerMarkers(true)` (`mrxbriefing.lua`), used to hide/show player markers during cutscenes/briefings. |
| `EnableFactionMarkers` | `Gui.EnableFactionMarkers(bEnabled)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `EnablePlayerMarkers`. |
| `EnablePickupMarkers` | `Gui.EnablePickupMarkers(bEnabled)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `EnablePlayerMarkers`. |
| `EnableVehicleEntranceMarkers` | `Gui.EnableVehicleEntranceMarkers(bEnabled)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `EnablePlayerMarkers`. |
| `SetFactionMarkerSize` | `Gui.SetFactionMarkerSize(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetFactionMarkerVisibleDistance` | `Gui.SetFactionMarkerVisibleDistance(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetPickupMarkerSize` | `Gui.SetPickupMarkerSize(nSize, bFlag)` | Confirmed in real scripts, e.g. `Gui.SetPickupMarkerSize(18, false)` immediately followed by `Gui.SetPickupMarkerSize(18, true)` (`hero.lua`) — same numeric size passed with the boolean flipped, meaning of the flag unconfirmed (possibly a "near"/"far" or "friendly"/"enemy" marker-set selector). |
| `SetPickupMarkerVisibleDistance` | `Gui.SetPickupMarkerVisibleDistance(nDistance, bFlag)` | Confirmed in real scripts, e.g. `Gui.SetPickupMarkerVisibleDistance(20, false)` (`hero.lua`), same call site as `SetPickupMarkerSize` above, run inside a 3-second delayed `Event.Create(Event.TimerRelative, ...)` block during survival-mode setup. |
| `SetVehicleEntranceMarkerSize` | `Gui.SetVehicleEntranceMarkerSize(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetVehicleEntranceMarkerVisibleDistance` | `Gui.SetVehicleEntranceMarkerVisibleDistance(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### Internal Marker Primitives

These are almost certainly the internal implementation behind the separate public `Marker` namespace
(documented on its own page). None of them turned up call sites in the decompiled `.lua` corpus, which is
consistent with the underscore-prefix convention elsewhere in this codebase marking "internal, not meant to
be called directly from game scripts" — the public `Marker.*` wrapper is presumably what real scripts call
instead.

| Function | Notes |
|---|---|
| `_MarkerAdd` | No call sites found. Name corresponds closely to public `Marker.Add`. |
| `_MarkerAddOld` | No call sites found. An older/legacy variant of `_MarkerAdd`, judging by the name — the exact relationship to `Marker.AddBlip` (which has no equally-named `_Marker*` counterpart) is unconfirmed; flagged as a naming mismatch rather than assumed. |
| `_MarkerAdd3D` | No call sites found. Name corresponds closely to public `Marker.Add3D`. |
| `_MarkerAddDisc` | No call sites found. Name corresponds closely to public `Marker.AddDisc`. |
| `_MarkerAddTripwire` | No call sites found. Name corresponds closely to public `Marker.AddTripwire`. |
| `_MarkerHaltPulse` | No call sites found. Name corresponds closely to public `Marker.HaltPulse`. |
| `_MarkerPulse` | No call sites found. Name corresponds closely to public `Marker.Pulse`. |
| `_MarkerRemove` | No call sites found. Name corresponds closely to public `Marker.Remove`. |
| `_MarkerSetBlipLimit` | No call sites found. Name corresponds closely to public `Marker.SetGroupedBlipLimit` (not an exact string match, but the closest by function). |
| `_MarkerSetColor` | No call sites found. Name corresponds closely to public `Marker.SetColor`. |
| `_MarkerSetFollowGuid` | No call sites found. Name corresponds closely to public `Marker.SetFollowGuid`. |
| `_MarkerSetLocation` | No call sites found. Name corresponds closely to public `Marker.SetLocation`. |
| `_MarkerSetScale` | No call sites found. Name corresponds closely to public `Marker.SetScale`. |

**On the naming correspondence:** the match between these 13 `Gui._Marker*` names and the 13 public
`Marker.*` function names is a strong naming-pattern observation from the two live `pairs()` dumps, not a
confirmed engine-internals finding — the engine's native (C++) implementation isn't available to us, so we
cannot show that `Marker.Add` literally calls `Gui._MarkerAdd` under the hood. Treat it as a well-supported
hypothesis: `Marker.Add`/`Add3D`/`AddDisc`/`AddTripwire`/`HaltPulse`/`Pulse`/`Remove`/`SetColor`/
`SetFollowGuid`/`SetLocation`/`SetScale` line up 1:1 by name with `_MarkerAdd`/`_MarkerAdd3D`/`_MarkerAddDisc`/
`_MarkerAddTripwire`/`_MarkerHaltPulse`/`_MarkerPulse`/`_MarkerRemove`/`_MarkerSetColor`/`_MarkerSetFollowGuid`/
`_MarkerSetLocation`/`_MarkerSetScale`. Two names don't line up as cleanly: `Marker.SetGroupedBlipLimit` vs.
`_MarkerSetBlipLimit` (close but not exact), and `Marker.AddBlip` has no matching `_MarkerAddBlip` at all —
the closest candidate is `_MarkerAddOld`, which is a plausible but unconfirmed guess given the "Old" naming.

### Localization & Language

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetLanguageName` | `s = Gui.GetLanguageName()` | Confirmed with no arguments in real scripts, e.g. `local sLanguage = Gui.GetLanguageName()` (`mrxsoundbanks.lua`), used to pick the correct localized sound bank. |
| `GetLanguageNum` | `n = Gui.GetLanguageNum()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed numeric-ID counterpart to the confirmed `GetLanguageName`. |
| `LoadFont` | `Gui.LoadFont(sFontName)` | Confirmed with a single font-name string in real scripts, e.g. `Gui.LoadFont("fanfare_36")` (`mrxguihudmessage.lua`). |
| `LoadTexture` | `Gui.LoadTexture(sTextureName [, sType])` | Confirmed extensively in real scripts, always at least a texture-name string; commonly called with an explicit `"texture"` type string as the 2nd argument, e.g. `Gui.LoadTexture("icon_hijack_button_A", "texture")` (24 consecutive calls in `mrxguihudactionhijack.lua` preloading HUD icons), and also called with just the name in other places (e.g. `Gui.LoadTexture("global_gui_reticle_stinger_target")` in `mrxguihudreticle.lua`), meaning the 2nd argument is optional. |

### Input/Controller Detection

| Function | Signature (best-known) | Notes |
|---|---|---|
| `IsXboxController` | `b = Gui.IsXboxController()` | Confirmed with no arguments in real scripts, always guarded by an existence check first, e.g. `if Gui.IsXboxController and Gui.IsXboxController() then` (`mrxguihudactionhijack.lua`) — the guard pattern suggests this function may not exist on all platform builds. |
| `ControllerInUse` | `b = Gui.ControllerInUse()` | Confirmed with no arguments in real scripts, also always guard-checked first, e.g. `if Gui.ControllerInUse and Gui.ControllerInUse() then` (`vzacon001.lua`, `wiftutorialboat.lua`, `wiftutorialwheeledvehiclebasic.lua`) — same existence-guard pattern as `IsXboxController`, used to branch tutorial prompts between mouse/keyboard and controller phrasing. |
| `GetReticlePosition` | `nX, nY = Gui.GetReticlePosition(uOwnerGuid)` | Confirmed in real scripts with an `oWidget:GetOwner()`-style argument, e.g. `local nAimX, nAimY = Gui.GetReticlePosition(oWidget:GetOwner())` (`mrxguihudreticle.lua`, 5 call sites), returning 2D screen-space reticle coordinates. Also always guard-checked at one call site: `if Gui.GetReticlePosition then`. This is a **different function from** `Player.GetTargetUnderReticle` (see [Player](player#notes-for-modders)) — `Gui.GetReticlePosition` returns 2D screen coordinates of the reticle itself, while `Player.GetTargetUnderReticle` returns the 3D world position and `uGuid` of whatever the reticle is aimed at. The two are complementary, not duplicates. |
| `FindGuiLocation` | `nX1, nY1, nX2, nY2 = Gui.FindGuiLocation(uOwnerOrPlayerGuid, uTargetGuid)` | Confirmed in real scripts with two arguments and 4 return values, e.g. `local nX1, nY1, nX2, nY2 = Gui.FindGuiLocation(oOverlay:GetOwner(), tEvent.uGuid)` (`mrxguisatellite.lua`) and `local nX, nY, nX2, nY2 = Gui.FindGuiLocation(uPlayerGuid, uGuid)` (`mrxguitutorial.lua`, guarded by `if Gui.FindGuiLocation then`) — likely a screen-space bounding box (two corner points) for a world object, used to anchor UI overlays/tutorial callouts onto it. |
| `IsPdaOnSelect` | `b = Gui.IsPdaOnSelect()` | Confirmed with no arguments in real scripts, guard-checked first: `if Gui.IsPdaOnSelect and Gui.IsPdaOnSelect() then` (`mrxguipda.lua`). |

### Misc/Dev

| Function | Signature (best-known) | Notes |
|---|---|---|
| `AddObjective` | `Gui.AddObjective(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `DoSigninCheck` | `Gui.DoSigninCheck()` | Confirmed with no arguments in real scripts, e.g. `Gui.DoSigninCheck()` (`mrxguishell.lua`), part of the shell/platform-signin flow. |
| `OnGlobalExit` | `Gui.OnGlobalExit()` | Confirmed with no arguments in real scripts, e.g. `Gui.OnGlobalExit()` (`mrxstate.lua`), invoked as part of global game-exit teardown. |
| `OnShellLoaded` | `Gui.OnShellLoaded()` | Confirmed with no arguments in real scripts, guard-checked first: `if Gui.OnShellLoaded then Gui.OnShellLoaded() end` (`mrxguishell.lua`). |
| `OutputToPIX` | `Gui.OutputToPIX(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Name suggests a PIX (graphics-debugger) event/marker output hook for dev builds. |
| `ShowLoadingHints` | `Gui.ShowLoadingHints(bShow)` | Confirmed with a single boolean argument in real scripts, always guard-checked first, e.g. `if Gui.ShowLoadingHints then Gui.ShowLoadingHints(false) end` / `Gui.ShowLoadingHints(true)` (`mrxgui.lua`), toggling the loading-screen hint text. |

## Notes for modders

- Prefer the public [`Marker`](marker) namespace over calling the `_Marker*` functions on this page
  directly. The leading underscore is this codebase's naming convention for "internal, not meant to be
  called externally" — `Marker.*` is very likely a thin wrapper around exactly these primitives (see the
  naming-correspondence discussion above), and using the public API is both safer and more likely to match
  whatever validation/bookkeeping the wrapper does around the raw primitive.
- Several functions here are consistently called behind an existence guard in real scripts (`if
  Gui.ControllerInUse and Gui.ControllerInUse() then`, `if Gui.ShowLoadingHints then ... end`, etc.). That's
  a strong signal these functions may not exist on every platform/build target — copy the guard pattern in
  your own mods rather than calling them unconditionally.
- `Gui.GetReticlePosition` and `Player.GetTargetUnderReticle` are easy to confuse but answer different
  questions (2D screen position of the reticle vs. 3D world target under it) — see the comparison note in
  the Input/Controller Detection table above.
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Gui)` dump) but their
  argument shape is a guess based on naming convention and analogy only — don't build mods around them
  without testing in-game first.
