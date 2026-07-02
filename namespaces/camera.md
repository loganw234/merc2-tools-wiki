---
title: Camera
parent: Engine Namespaces
nav_order: 14
---

# Camera

## Overview

`Camera` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it,
no `import()` call needed, and it's always globally available to every script. Its functions operate on
camera guids, which are obtained via `Player.GetCamera(uPlayerGuid)` (see [Player](player#camera--viewport)) —
`Camera` itself has no way to look up a camera on its own. It covers orientation (yaw/pitch/FOV), positioning
and look-at targeting, following, blending between camera states, scripted "shots", and screen shake.

Note: this is a different table from `Graphics.Camera`, a nested sub-table under the `Graphics` namespace
that handles near/far-plane and FOV/LOD parameters (`Graphics.Camera.SetNearFar`, `SetFovParams`,
`SetFocusParams`, etc.). The two are unrelated aside from the name, and `Graphics.Camera` is documented
separately.

## Provenance

This page's function list comes from a live `pairs(Camera)` enumeration in-game (via lua-bridge), not from
reading engine source — the engine implementation isn't available to us. That means the list of 14 function
names below is complete and authoritative: every one of them really exists on the namespace. It does **not**
mean every entry is documented with confirmed arguments. Where a function is actually called somewhere in
the ~230 decompiled `.lua` scripts, we can show a real argument pattern. Where it isn't called anywhere in
that corpus, we only know the name — arguments, return values, and behavior for those are unconfirmed.

## Functions

### Orientation

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetYaw` | `nYaw = Camera.GetYaw(uCameraGuid)` | Confirmed in real scripts, e.g. `self.nHeading = Camera.GetYaw(Player.GetCamera(self:GetOwner()))` in `resident/mrxcarpetbomb.lua:22`, and similarly in `resident/mrxguipda.lua`. This is the exact call site cross-referenced from [Player](player#camera--viewport). |
| `SetYaw` | `Camera.SetYaw(uCameraGuid, nYaw)` | Confirmed in real scripts with a numeric yaw, e.g. `Camera.SetYaw(uCamera, 0)` in `resident/mrxutil.lua:369` and `resident/wifpmcgarage.lua:567`, and `Camera.SetYaw(uCamera, 80)` in `resident/mrxplayer.lua:513`. |
| `GetPitch` | `nPitch = Camera.GetPitch(uCameraGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. Presumed counterpart to the confirmed `SetPitch`. |
| `SetPitch` | `Camera.SetPitch(uCameraGuid, nPitch)` | Confirmed in real scripts, e.g. `Camera.SetPitch(uCamera, 0.302)` in `resident/mrxutil.lua:370`, paired with `Camera.SetYaw(uCamera, 0)` right before it — both called on the camera obtained from `Player.GetCamera(tOperation.uPlayer)` during a teleport-recovery sequence. |
| `GetFOV` | `nFOV = Camera.GetFOV(uCameraGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Do not confuse with `Graphics.Camera.SetFovParams`, which is a different, confirmed-in-use function on the separate `Graphics.Camera` sub-table. |
| `SetFOV` | `Camera.SetFOV(uCameraGuid, nFOV)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Same caveat as `GetFOV` above regarding `Graphics.Camera.SetFovParams`. |

### Positioning & Following

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetPosition` | `Camera.SetPosition(uCameraGuid, nX, nY, nZ [, bFlag])` or `Camera.SetPosition(uCameraGuid, uObjectGuid, sHardpoint [, bFlag])` | Confirmed with both forms in `resident/mrxbriefing.lua`: a plain-coordinates form (`Camera.SetPosition(uCamera, tSettings.tPosition[1], tSettings.tPosition[2], tSettings.tPosition[3], true)`, line 1894) and an object+hardpoint form (`Camera.SetPosition(uCamera, tSettings.uPositionObject, tSettings.sPositionHardpoint, true)`, line 1897), both used for cinematic camera setup. The trailing boolean's exact meaning is unconfirmed. |
| `SetLookAt` | `Camera.SetLookAt(uCameraGuid, nX, nY, nZ, bLookAtDirection [, bFlag])` or `Camera.SetLookAt(uCameraGuid, uObjectGuid, sHardpoint, bLookAtDirection [, bFlag])` | Confirmed with both forms in `resident/mrxbriefing.lua` (lines 1901 and 1904), mirroring the two `SetPosition` forms. Also confirmed with a simpler 3-argument object+hardpoint call in `resident/mrxactionhijack.lua:916`: `Camera.SetLookAt(uCamera, self._hijacker, "bone_chest")`, aiming the camera at a specific bone during a hijack-fail cinematic. |
| `Follow` | `Camera.Follow(uCameraGuid, ...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed beyond the presumed leading camera guid. |
| `Hold` | `Camera.Hold(uCameraGuid, bHold, bFlag2 [, bFlag3])` | Confirmed in real scripts with two or three booleans, e.g. `Camera.Hold(uCamera, true, false)` in `resident/mrxactionhijack.lua:917` (used right after `SetLookAt` during a ragdoll-minigame cinematic) and `Camera.Hold(uCamera, tSettings.bHold, tSettings.bHold, true)` in `resident/mrxbriefing.lua:1887`. Exact per-argument meaning beyond "hold the camera in place" is unconfirmed. |

### Blending & Effects

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Blend` | `Camera.Blend(uCameraGuid, nBlendTime [, bFlag])` | Confirmed in real scripts, e.g. `Camera.Blend(uCamera, 1)` in `resident/mrxactionhijack.lua:915` and `Camera.Blend(uCamera, tSettings.nBlendTime, true)` in `resident/mrxbriefing.lua:1890`, both starting a timed blend into a new camera state (position/look-at/shot set immediately afterward). |
| `StopBlending` | `Camera.StopBlending(uCameraGuid)` | Confirmed in real scripts, e.g. `Camera.StopBlending(uCam)` in `vz/vzacon001.lua:138`, guarded by an existence check (`if uCam and Camera.StopBlending then`) before calling — the only call site also defensively checks that the function exists on the namespace. |
| `SetShot` | `Camera.SetShot(uCameraGuid, sShotName, uBaseActor, uTargetActor [, bFlag])` | Confirmed in `resident/mrxbriefing.lua:1911`: `Camera.SetShot(uCamera, tSettings.tShot.sName, tSettings.tShot.uBaseActor, tSettings.tShot.uTargetActor, true)` — selects a named scripted "shot" (e.g. an over-the-shoulder or two-shot framing) between a base actor and a target actor, used in the cinematic-briefing system alongside `Blend` and `Hold`. |
| `Shake` | `Camera.Shake(uCameraGuid, sShakeName, uSourceGuid, nAmplitude, nDuration)` | Confirmed with 5 arguments in multiple real scripts: `Camera.Shake(playerCamera, "ShakeCameraMedium", playerCharacter, 6, 5)` in `vz/pmccon004.lua:117` and `resident/mrxactionhijack.lua` (explosion/impact feedback), and `Camera.Shake(StringToGuid("0x1"), "ShakeCameraConstantlyRandom", uiGuid, 0.5, 2000)` in `resident/oilrig.lua:38` (ongoing destruction sequence, stopped later via `Camera.Shake(StringToGuid("0x1"), "StopShakeCameraConstantly", uiGuid)` at line 60). Named shake presets seen in the corpus: `"ShakeCameraMedium"`, `"ShakeCameraConstantlyRandom"`, `"StopShakeCameraConstantly"`. The first argument is usually a real per-player camera guid from `Player.GetCamera(...)`, but `resident/oilrig.lua` instead passes `StringToGuid("0x1")` — possibly a fixed/broadcast camera handle; unconfirmed. |

## Notes for modders

- There's no lookup function on this namespace itself — you must first obtain a camera guid via
  `Player.GetCamera(uPlayerGuid)` (see [Player](player#camera--viewport)) and pass that into every `Camera.*`
  call here.
- `SetPosition` and `SetLookAt` both accept either raw coordinates or an object-guid-plus-hardpoint-name pair,
  confirmed side-by-side in the same cinematic-briefing code (`resident/mrxbriefing.lua`). `Blend`, `Hold`, and
  `SetShot` are used together in that same system to sequence cinematic camera cuts.
- `Shake`'s name string appears to select a preset defined elsewhere in the engine (not in the decompiled Lua
  corpus) — treat the specific preset names listed above as the only confirmed values; others may exist but
  are unconfirmed.
- Do not confuse this namespace with `Graphics.Camera`, a separate nested sub-table under `Graphics` for
  near/far-plane and FOV/LOD parameters — documented separately.
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Camera)` dump) but their
  argument shape is a guess based on naming convention and analogy to confirmed siblings only — don't build
  mods around them without testing in-game first.
