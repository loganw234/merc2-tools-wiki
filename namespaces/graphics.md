---
title: Graphics
parent: Engine Namespaces
nav_order: 15
---

# Graphics

## Overview

`Graphics` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it,
no `import()` call needed, and it's always globally available to every script. Unlike most other engine
namespaces, most of `Graphics` is not flat functions but a set of nested sub-namespace tables, each grouping
a family of rendering/visual-tuning controls: `Graphics.Atmosphere` (weather/sky/lighting), `Graphics.Bloom`,
`Graphics.Contrast`, `Graphics.Grainy`, `Graphics.Monochrome`, `Graphics.MotionBlur`, `Graphics.AA`
(post-process tuning), `Graphics.Effect` (screen-space effects like camera fade), `Graphics.FuelTrail`
(particle-trail control), and `Graphics.Camera` (near/far, FOV, and LOD parameters for the render camera).
A handful of flat top-level utility functions round out the namespace: screenshotting, gamma, shadow draw
distance, and a "tiny geometry" debug/LOD toggle.

**Naming collision — read this first:** `Graphics.Camera` is a completely different table from the
top-level [`Camera`](camera) namespace already documented elsewhere on this wiki. The top-level `Camera`
operates on a per-player camera guid obtained from `Player.GetCamera(uPlayerGuid)` and controls yaw/pitch/
FOV/look-at/shake for that specific camera instance. `Graphics.Camera`, documented below, instead exposes
global-feeling near/far-plane, focus (depth-of-blur), FOV-blend, and LOD parameter calls that in practice
are also called with a player-camera-index-like first argument (see the Functions table). The two tables
happen to share the name "Camera" and nothing else; do not assume a function exists on one because you saw
it on the other.

## Provenance

This page's function list comes from a live `pairs(Graphics)` enumeration in-game (via lua-bridge), not from
reading engine source — the engine implementation isn't available to us. That means the list of 21
top-level entries (most of which are themselves sub-namespace tables) is complete and authoritative: every
name below really exists. It does **not** mean every entry is documented with confirmed arguments. Where a
function is actually called somewhere in the ~230 decompiled `.lua` scripts, we can show a real argument
pattern. Where it isn't called anywhere in that corpus, we only know the name.

`Graphics.Atmosphere` alone has 36 methods, which is too many to individually trace within this pass's
research budget. Call sites confirm the general calling convention (`Begin()` / repeated `SetValue(sKey,
nValue)` / `End()` for a scoped override, plus a `ChangeLineRegionSetting` call for region-based weather),
but the remaining ~30 Atmosphere method names below are listed by name only and were **not individually
checked** against the decompiled corpus in this pass — treat them as confirmed-to-exist, unconfirmed-in-use.

## Functions

### Top-Level Utility

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetGamma` | `Graphics.SetGamma(nMin, nMax, nGamma)` | Confirmed identically in `shell/shellbootstrap.lua:69` and `resident/gamebootstrap.lua:42`: `Graphics.SetGamma(0, 0.8, 1)`, called once at boot. |
| `GetShadowBaseDistance` | `n = Graphics.GetShadowBaseDistance()` | Confirmed in `resident/mrxbriefing.lua:259,565` — called with no arguments to save off the current shadow distance before temporarily overriding it, restored later via `SetShadowBaseDistance(_nBaseShadowDistance)`. |
| `SetShadowBaseDistance` | `Graphics.SetShadowBaseDistance(nDistance)` | Confirmed in `resident/mrxbriefing.lua` (set to `2` during cinematic briefings, restored afterward) and `vz/xQ!L.lua:582` (set to `10`). Single numeric argument, presumably a distance multiplier/scale rather than raw world units given the small values used. |
| `SetBoundaryEffect` | `Graphics.SetBoundaryEffect(nOpacity)` | Confirmed in `resident/mrxguisatellite.lua:57,71` (`0` and `0.25`) and `resident/mrxutil.lua:713` (`Graphics.SetBoundaryEffect(fOpacity)`, a named opacity variable) — controls the visual "boundary" (map edge / no-go zone) overlay effect. |
| `InitTinyGeometry` | `Graphics.InitTinyGeometry()` | Confirmed in `resident/mrxtaskmission.lua:14`, called with no arguments. Presumably initializes a small/LOD geometry render pass; exact behavior unconfirmed beyond the call site. |
| `ShowTinyGeometryObject` | `Graphics.ShowTinyGeometryObject(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed companion to `InitTinyGeometry`. |
| `ScreenShot` | `Graphics.ScreenShot(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `ReloadShaders` | `Graphics.ReloadShaders()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed; name strongly suggests a dev/debug shader-hotreload utility. |
| `GetScreenRatio` | `n = Graphics.GetScreenRatio()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetScreenRatio` | `Graphics.SetScreenRatio(n)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed counterpart to `GetScreenRatio`. |
| `SetNumFrameSync` | `Graphics.SetNumFrameSync(n)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed; name suggests a frame-sync/vsync-count control. |

### Graphics.Atmosphere

Confirmed calling convention: a scoped override block of `Begin()`, then one or more `SetValue(sKey, nValue)`
calls with string keys, then `End()` to restore. Seen identically across all `resident/airstrike_atomsphere_*.lua`
files (bombrun, carpetbomb, clusterbomb, daisycutter, fuelairbomb, moab), which apply a temporary
bloom/lighting/atmosphere-force override for the duration of an airstrike weapon effect.

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Begin` | `Graphics.Atmosphere.Begin()` | Confirmed with no arguments in every `resident/airstrike_atomsphere_*.lua` file — opens a scoped atmosphere-override block. |
| `SetValue` | `Graphics.Atmosphere.SetValue(sKey, nValue)` | Confirmed extensively in `resident/airstrike_atomsphere_*.lua`, e.g. `Graphics.Atmosphere.SetValue("fBloomAmount", 0.75)`, `SetValue("fAtmosphereLimit", 200)`, `SetValue("fLightIntensity", 1.55)`, `SetValue("fTimeRestore", 0.5)`. Confirmed string keys in use include `fAtmosphereForce`, `fAtmosphereLimit`, `fBloomAdaptiveLuminancePercent`, `fBloomAdaptiveLuminanceScale`, `fBloomAmount`, `fBloomBlurRadius`, `fBloomContastLimit` (sic), `fBloomContastMultiplier` (sic), `fBloomMultiplier`, `fBloomTargetLuminance`, `fBloomThreshold`, `fLightIntensity`, `fTimeRestore`. |
| `End` | `Graphics.Atmosphere.End()` | Confirmed with no arguments in every `resident/airstrike_atomsphere_*.lua` file — closes the scoped override opened by `Begin`. |
| `ChangeLineRegionSetting` | `Graphics.Atmosphere.ChangeLineRegionSetting(uRegionGuid, sSettingName)` | Confirmed in `vz/allcon003.lua:142`: `Graphics.Atmosphere.ChangeLineRegionSetting(Pg.GetGuidByName("rgn_atmo_caracas"), "warzone")` — applies a named weather/atmosphere preset (`"warzone"`) to a specific map region. |
| `SetTimeSpeed` | `Graphics.Atmosphere.SetTimeSpeed(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetHaze` | `Graphics.Atmosphere.SetHaze(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetWindDirection` | `Graphics.Atmosphere.SetWindDirection(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `EnableImmediatelyChangeMode` | `Graphics.Atmosphere.EnableImmediatelyChangeMode(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetRainDensity` | `Graphics.Atmosphere.SetRainDensity(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetAmbientCube` | `Graphics.Atmosphere.SetAmbientCube(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetExtinctionMultiplier` | `Graphics.Atmosphere.SetExtinctionMultiplier(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetParticlesPerSecond` | `Graphics.Atmosphere.SetParticlesPerSecond(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `GetLineRegion` | `Graphics.Atmosphere.GetLineRegion(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetRimColor` | `Graphics.Atmosphere.SetRimColor(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `GetValue` | `Graphics.Atmosphere.GetValue(sKey)` | Not individually checked in this pass — presumed getter counterpart to the confirmed `SetValue`, same string-key convention assumed but unconfirmed. |
| `SetLightModifier` | `Graphics.Atmosphere.SetLightModifier(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetLightIntensity` | `Graphics.Atmosphere.SetLightIntensity(...)` | Not individually checked in this pass — name only, exists per live enumeration. Distinct from the confirmed `SetValue("fLightIntensity", n)` key. |
| `SetAtmosphere` | `Graphics.Atmosphere.SetAtmosphere(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `IsInterpolating` | `b = Graphics.Atmosphere.IsInterpolating()` | Not individually checked in this pass — name only, exists per live enumeration. |
| `Restore` | `Graphics.Atmosphere.Restore(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetInscatteringMultiplier` | `Graphics.Atmosphere.SetInscatteringMultiplier(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `GetIntValue` | `Graphics.Atmosphere.GetIntValue(sKey)` | Not individually checked in this pass — presumed integer-typed variant of `GetValue`. |
| `SetAmbientColor` | `Graphics.Atmosphere.SetAmbientColor(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `Change` | `Graphics.Atmosphere.Change(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `GetCurrentSetting` | `Graphics.Atmosphere.GetCurrentSetting(...)` | Not individually checked in this pass — name only, exists per live enumeration. Presumed getter counterpart to `ChangeLineRegionSetting`/`Change`. |
| `SetSky` | `Graphics.Atmosphere.SetSky(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetIntValue` | `Graphics.Atmosphere.SetIntValue(sKey, nValue)` | Not individually checked in this pass — presumed integer-typed variant of `SetValue`. |
| `SetTime` | `Graphics.Atmosphere.SetTime(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetBetaRayMultiplier` | `Graphics.Atmosphere.SetBetaRayMultiplier(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetTurbinity` | `Graphics.Atmosphere.SetTurbinity(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `GetColorValue` | `Graphics.Atmosphere.GetColorValue(sKey)` | Not individually checked in this pass — presumed color-typed variant of `GetValue`. |
| `SetHenyeyGreensteinConst` | `Graphics.Atmosphere.SetHenyeyGreensteinConst(...)` | Not individually checked in this pass — name only, exists per live enumeration (Henyey-Greenstein is a standard atmospheric-scattering phase function, consistent with the other sky/scattering tuning parameters here). |
| `SetBetaMieMultiplier` | `Graphics.Atmosphere.SetBetaMieMultiplier(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetLightAngle` | `Graphics.Atmosphere.SetLightAngle(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `SetColorValue` | `Graphics.Atmosphere.SetColorValue(sKey, ...)` | Not individually checked in this pass — presumed color-typed variant of `SetValue`. |
| `SetRainSpeed` | `Graphics.Atmosphere.SetRainSpeed(...)` | Not individually checked in this pass — name only, exists per live enumeration. |
| `GetLineRegionSetting` | `Graphics.Atmosphere.GetLineRegionSetting(...)` | Not individually checked in this pass — presumed getter counterpart to the confirmed `ChangeLineRegionSetting`. |

### Bloom, Contrast & Post-Process

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Bloom.SetBlurRadius` | `Graphics.Bloom.SetBlurRadius(n)` | Confirmed in `resident/mrxbootstrap.lua:91`: `Graphics.Bloom.SetBlurRadius(0.5)`, called once at boot alongside the other post-process defaults below. |
| `Bloom.SetThreshold` | `Graphics.Bloom.SetThreshold(n)` | Confirmed in `resident/mrxbootstrap.lua:92`: `Graphics.Bloom.SetThreshold(0.775)`. |
| `Bloom.SetMultiplier` | `Graphics.Bloom.SetMultiplier(n)` | Confirmed in `resident/mrxbootstrap.lua:93`: `Graphics.Bloom.SetMultiplier(0)`. |
| `Bloom.SetTargetLuminance` | `Graphics.Bloom.SetTargetLuminance(n)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. Corresponds to the `fBloomTargetLuminance` key confirmed in use via `Atmosphere.SetValue`. |
| `Bloom.SetAdaptiveLuminancePercent` | `Graphics.Bloom.SetAdaptiveLuminancePercent(n)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. Corresponds to `fBloomAdaptiveLuminancePercent`. |
| `Bloom.SetAdaptiveLuminanceScale` | `Graphics.Bloom.SetAdaptiveLuminanceScale(n)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. Corresponds to `fBloomAdaptiveLuminanceScale`. |
| `Contrast.SetLimit` | `Graphics.Contrast.SetLimit(n)` | Confirmed in `resident/mrxbootstrap.lua:96`: `Graphics.Contrast.SetLimit(0.1)`. |
| `Contrast.SetMultiplier` | `Graphics.Contrast.SetMultiplier(n)` | Confirmed in `resident/mrxbootstrap.lua:97`: `Graphics.Contrast.SetMultiplier(1.5)`. |
| `Monochrome.SetGradient` | `Graphics.Monochrome.SetGradient(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10)` | Confirmed with 10 numeric arguments in `resident/mrxbootstrap.lua:94-95`, e.g. `Graphics.Monochrome.SetGradient(0, 128, 0, 0, 0, 0, 0, 0.65, 0.35, 0)` and `Graphics.Monochrome.SetGradient(128, 255, 0, 0.65, 0.35, 0, 1, 1, 1, 0)` — two calls back-to-back, presumably defining a two-stop color grading/tone curve (shadow and highlight ranges), but the exact per-argument meaning is not confirmed. |
| `Grainy.SetGrainOpacity` | `Graphics.Grainy.SetGrainOpacity(n)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `MotionBlur.SetVelocityMultiplier` | `Graphics.MotionBlur.SetVelocityMultiplier(n)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `AA.SetThreshold` | `Graphics.AA.SetThreshold(n)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. Presumably an anti-aliasing edge-detection threshold. |

### Graphics.Camera

**Distinct from the top-level [`Camera`](camera) namespace** — see the naming-collision note above. These
functions all take a leading numeric first argument (confirmed as `0` at every call site seen, matching the
pattern of a player/camera index rather than a `uGuid`), consistent with `Graphics.Camera` operating on the
same per-player camera slot that `Player.GetCamera(uPlayerGuid)` would resolve to a guid for, but expressed
as an index instead.

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetFocusParams` | `Graphics.Camera.SetFocusParams(nCameraIndex, nStartNear, nEndNear, nStartFar, nEndFar, nBlur, nDuration)` | Confirmed with 7 arguments in `resident/mrxactionhijack.lua:222,334`: `Graphics.Camera.SetFocusParams(nPlayerCam, nStartNear, nEndNear, nStartFar, nEndFar, nBlur, nDuration)`, and with literal values in `resident/emplaced.lua:46` (`Graphics.Camera.SetFocusParams(0, 0, 2, 2, 600, 4, 0)`) and `resident/mrxactionhijack.lua:93` (6 args: `SetFocusParams(0, 0, 0.1, 4, 6, 1)`) — controls depth-of-field blur transition (near/far focus planes blending over a duration), used during hijack and turret-mount cinematics. |
| `RestoreFocusParams` | `Graphics.Camera.RestoreFocusParams(nCameraIndex, nDuration)` | Confirmed in `resident/emplaced.lua:59` (`RestoreFocusParams(0, 0)`), `resident/mrxactionhijack.lua:1010` (`RestoreFocusParams(0, 0.6)`), `resident/mrxbriefing.lua:3053`, and `vz/xQ!L.lua:583` (`RestoreFocusParams(0, 1)`) — reverts a `SetFocusParams` override over the given duration. |
| `SetFovParams` | `Graphics.Camera.SetFovParams(nCameraIndex, nAngle, nDuration)` | Confirmed in `resident/mrxactionhijack.lua:335`: `Graphics.Camera.SetFovParams(nPlayerCam, nAngle, nDuration)`, and `resident/mrxbriefing.lua:3057` — blends the field-of-view angle to a new value over a duration. |
| `RestoreFovParams` | `Graphics.Camera.RestoreFovParams(nCameraIndex, nDuration)` | Confirmed in `resident/mrxbriefing.lua:3048,3051` and `vz/xQ!L.lua:584` (`RestoreFovParams(0, 1)`) — reverts a `SetFovParams` override. |
| `SetNearFar` | `Graphics.Camera.SetNearFar(nCameraIndex, nNear, nFar, nUnknown)` | Confirmed in `vz/wifpmcinterior.lua:423,1733` (`Graphics.Camera.SetNearFar(0, 0.3, 500, 0)`) and `resident/mrxhq.lua:643` (`Graphics.Camera.SetNearFar(0, 0.3, self:GetDrawDistance(), 0)`) — sets the near/far clip planes directly (as opposed to `SetFocusParams`' blended depth-of-field near/far). The trailing 4th argument is `0` at every call site; meaning unconfirmed. |
| `RestoreNearFar` | `Graphics.Camera.RestoreNearFar(nCameraIndex)` | Confirmed in `vz/wifpmcinterior.lua:1746`, `vz/xQ!L.lua:585`, and `resident/mrxhq.lua:579` — all called as `RestoreNearFar(0)`, reverting a `SetNearFar` override. |
| `SetLodParams` | `Graphics.Camera.SetLodParams(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed to control level-of-detail distance thresholds by analogy with the sibling near/far/focus/FOV setters. |

### Effects & Fuel Trail

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Effect.CameraFade` | `Graphics.Effect.CameraFade(nAmount)` | Confirmed in `resident/mrxactionhijack.lua:94,1011`: `Graphics.Effect.CameraFade(0)` and `Graphics.Effect.CameraFade(1)`, called at the start/end of a hijack cinematic — a full-screen fade-to-black/fade-in effect keyed by a `0`/`1` amount, not tied to a specific camera guid. |
| `Effect.Terrain` | `Graphics.Effect.Terrain(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Effect.AmbientTop` | `Graphics.Effect.AmbientTop(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Effect.AmbientSides` | `Graphics.Effect.AmbientSides(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed paired with `AmbientTop` for directional ambient-lighting tuning. |
| `FuelTrail.Ignite` | `Graphics.FuelTrail.Ignite(...)` | No call sites found anywhere in the decompiled corpus, including vehicle-fuel-tank-damage code in `resident/mrxpmc.lua` — exists (confirmed via live `pairs()` enumeration) but usage/arguments completely unconfirmed. The name strongly suggests it starts a leaking-fuel particle trail (e.g. on a damaged vehicle fuel tank), but no in-repo evidence connects it to that or any other system. |
| `FuelTrail.Put` | `Graphics.FuelTrail.Put(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `FuelTrail.Extinguish` | `Graphics.FuelTrail.Extinguish(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed counterpart to `Ignite`. |

## Notes for modders

- **`Graphics.Camera` is not the same table as the top-level [`Camera`](camera) namespace.** They share a
  name and nothing else. Top-level `Camera` takes a per-player camera guid from `Player.GetCamera(uPlayerGuid)`
  and controls yaw/pitch/FOV/position/look-at/shake for that instance. `Graphics.Camera`, documented above,
  controls near/far clip planes, depth-of-field focus blending, FOV blending, and LOD parameters, and its
  confirmed call sites all pass a plain numeric first argument (`0` in every case seen) rather than a guid.
  If you're looking for "how do I shake the camera" or "how do I change FOV for a look-at shot," that's the
  top-level `Camera` namespace, not this one.
- `Graphics.Atmosphere`'s `Begin()` / `SetValue(sKey, nValue)` / `End()` pattern is the one clearly-confirmed
  convention on that sub-table, used consistently across every `resident/airstrike_atomsphere_*.lua` script
  to apply a temporary bloom/lighting override for the duration of an airstrike effect. The remaining ~30
  `Atmosphere` methods were not individually traced in this pass (see Provenance) — treat their signatures as
  unconfirmed even though the names are real.
- `Graphics.FuelTrail` has zero call sites anywhere in the decompiled corpus. Despite the name suggesting a
  connection to vehicle fuel-tank damage (compare `resident/mrxpmc.lua`'s health/damage-node handling), no
  such link exists in the available source — this is a real, callable sub-namespace with completely unknown
  argument shapes. Test carefully in-game before relying on it.
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Graphics)` dump, including
  its sub-tables) but their argument shape is a guess based on naming convention and analogy to confirmed
  siblings only — don't build mods around them without testing in-game first.
