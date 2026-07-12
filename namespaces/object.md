---
title: Object
parent: Engine Namespaces
nav_order: 1
---

# Object

## Overview

`Object` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it,
no `import()` call needed, and it's always globally available to every script. Its functions operate on
`uGuid` handles (the opaque object-instance identifiers used throughout the game's Lua layer) and cover
position/transform, health and damage, physics and impulses, animation playback, winch/cargo operations,
attachment, labels, the "disposer" system, and general object-state queries (alive, visible, valid, etc.).

## Provenance

This page's function list comes from a live `pairs(Object)` enumeration in-game (via lua-bridge), not from
reading engine source — the engine implementation isn't available to us. That means the list of 87 function
names below is complete and authoritative: every one of them really exists on the namespace. It does **not**
mean every entry is documented with confirmed arguments. Where a function is actually called somewhere in
the ~230 decompiled `.lua` scripts, we can show a real argument pattern. Where it isn't called anywhere in
that corpus, we only know the name — arguments, return values, and behavior for those are unconfirmed and
not guessed beyond the `uGuid`-first convention that holds for every confirmed function on this namespace.

## Functions

### Position & Transform

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetPosition` | `x, y, z = Object.GetPosition(uGuid)` | **Confirmed working by live testing** — see [Snippets](../snippets#get-your-current-position). Also widely used in real scripts, e.g. `Object.GetPosition(Player.GetLocalCharacter())`. |
| `SetPosition` | `Object.SetPosition(uGuid, x, y, z [, bSomeFlag])` | Used with a plain `uGuid` and three coordinates in real game scripts; one call site passes a 4th boolean-looking argument (`Object.SetPosition(uHelo, 2632, 155, -1000, false)`), meaning unconfirmed. |
| `GetYaw` | `nYaw = Object.GetYaw(uGuid)` | Used with a plain `uGuid` argument in real game scripts, returns a single yaw value. **Unit (degrees vs. radians) unconfirmed** — and the wiki's own sample scripts don't agree with each other: [`DestroyerTool.lua`](../sample-scripts-onkey) feeds it straight into a function named `customSin(nDegrees)` (implying degrees), while [`Fireworks.lua`](../sample-scripts-onkey) adds a hand-tuned correction constant converted from degrees to radians before combining it with the raw value (implying radians) — and that script's own write-up already flags the correction as an empirical fudge factor, not a confirmed derivation. Don't trust either script's implicit assumption without testing it yourself first. |
| `SetYaw` | `Object.SetYaw(uGuid, nYaw)` | Used with `uGuid` and a numeric yaw in real game scripts. Same unit caveat as `GetYaw` above. |
| `SetPositionToObject` | `Object.SetPositionToObject(uGuid, uTargetGuid [, sHardpoint])` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `SetTransformToObject` below; treat with caution. |
| `SetTransformToObject` | `Object.SetTransformToObject(uGuid, uTargetGuid [, sHardpoint])` | Used with two `uGuid`s in real scripts (e.g. `Object.SetTransformToObject(self.guid, uPoint)`), and with an optional 3rd hardpoint-name string argument in others (e.g. `Object.SetTransformToObject(uGuid, uObject, sHardpoint)`). |
| `TransformLocalToWorld` | `Object.TransformLocalToWorld(uGuid, ...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed beyond the presumed leading `uGuid`. |
| `GetHardpointPosition` | `x, y, z = Object.GetHardpointPosition(uGuid, sHardpointName)` | Used with a `uGuid` and a hardpoint-name string in real scripts (e.g. `Object.GetHardpointPosition(uMainTruck, "HP_Truckbed")`), returns 3 coordinates. |
| `GetHardpointYaw` | `Object.GetHardpointYaw(uGuid, sHardpointName)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `GetHardpointPosition`. |
| `GetHardpointPitch` | `Object.GetHardpointPitch(uGuid, sHardpointName)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `GetHardpointPosition`. |
| `GetDistanceFrom` | `n = Object.GetDistanceFrom(uGuidA, uGuidB [, bIgnoreY])` or `n = Object.GetDistanceFrom(uGuidA, nX, nY, nZ [, bIgnoreY])` | Confirmed with both an object-to-object form (`Object.GetDistanceFrom(uObjectA, uObjectB, bIgnoreY)`) and an object-to-coordinates form (`Object.GetDistanceFrom(uObjectA, nX, nY, nZ, bIgnoreY)`) in real scripts. |
| `GetHeightAboveTerrain` | `n = Object.GetHeightAboveTerrain(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `InsideBoundary` | `b = Object.InsideBoundary(uGuid, uZoneGuid [, bIgnoreY])` | Used in real scripts as `Object.InsideBoundary(self.exec.guid, Pg.GetGuidByName("oc001.rgn.warehouse01"), true)`. |
| `OutsideBoundary` | `b = Object.OutsideBoundary(uGuid, uZoneGuid)` | Used in real scripts as `Object.OutsideBoundary(self.uVehicle, self.inRegion)`. |

### Health & Damage

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetHealth` | `n = Object.GetHealth(uGuid)` | Extremely common in real scripts, always a plain `uGuid` argument, returns a single numeric health value. |
| `SetHealth` | `Object.SetHealth(uGuid, nHealth)` | Used with a plain `uGuid` and numeric value in real scripts, e.g. `Object.SetHealth(uJeep, 8)`, and to fully heal via `Object.SetHealth(uGuid, Object.GetMaxHealth(uGuid))`. |
| `GetMaxHealth` | `n = Object.GetMaxHealth(uGuid)` | Used with a plain `uGuid` argument in real scripts, paired with `GetHealth` in HUD/health-bar code. |
| `GetNodeHealth` | `n = Object.GetNodeHealth(uGuid, sNodeName)` | Used with a `uGuid` and a node-name string in real scripts, e.g. `Object.GetNodeHealth(uGuid, sNodeName)` for destructible sub-parts. |
| `Kill` | `Object.Kill(uGuid)` | Used with a plain `uGuid` argument in real scripts. See Notes for modders below. |
| `Revive` | `Object.Revive(uGuid [, nDelay])` | Used with a plain `uGuid` in real scripts, and with an optional numeric second argument (e.g. `Object.Revive(uChar, 0.5)`) that call-site patterns suggest is a delay. |
| `GetInvincible` | `b = Object.GetInvincible(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetInvincible` | `Object.SetInvincible(uGuid, bInvincible [, sReason])` | Very common in real scripts; the optional 3rd string argument is used consistently as a named "reason" tag (e.g. `Object.SetInvincible(uGuid, true, "Survival")`, `"Hijack"`, `"HQ"`, `"Fanfare"`). |
| `SetUnkillable` | `Object.SetUnkillable(uGuid, bUnkillable [, sReason])` | Used in real scripts with the same shape as `SetInvincible`, e.g. `Object.SetUnkillable(uGuid, true, "Support")`. |
| `GetCashValue` | `n = Object.GetCashValue(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. to compute a collectible's cash reward. |

### Physics & Impulses

| Function | Signature (best-known) | Notes |
|---|---|---|
| `DisablePhysics` | `Object.DisablePhysics(uGuid)` | Used with a plain `uGuid` argument in real scripts, very common. |
| `EnablePhysics` | `Object.EnablePhysics(uGuid)` | Used with a plain `uGuid` argument in real scripts, always paired with `DisablePhysics` elsewhere in the same modules. |
| `GetPhysicsType` | `Object.GetPhysicsType(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetMass` | `n = Object.GetMass(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `local myMass = Object.GetMass(uGuid)`. |
| `SetMass` | `Object.SetMass(uGuid, nMass)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetVelocity` | `n = Object.GetVelocity(uGuid)` | Used with a plain `uGuid` argument in real scripts, returns what call sites treat as a single scalar speed value. |
| `GetVelocityVector` | `Object.GetVelocityVector(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed; presumably returns a vector/multiple components given `GetVelocity` returns a scalar, but that is not verified. |
| `GetVelocitySquared` | `Object.GetVelocitySquared(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `ApplyImpulse` | `Object.ApplyImpulse(uGuid, nX, nY, nZ [, bLocalSpace])` | Confirmed in real scripts with a `uGuid` and 3 numeric components plus a trailing boolean, e.g. `Object.ApplyImpulse(uGuid, 0, 10000, 6 * myMass, true)`. |
| `ApplyPointImpulse` | `Object.ApplyPointImpulse(uGuid, nX, nY, nZ, nPX, nPY, nPZ [, bFlag])` | Confirmed in real scripts with 6 numeric arguments plus a trailing boolean, e.g. `Object.ApplyPointImpulse(uGuid, 0, 10 * myMass, 0.1 * myMass, 0, 0, 0.15, true)` — likely impulse vector + application-point offset, but the exact meaning of each component is not confirmed. |
| `ApplyAngularImpulse` | `Object.ApplyAngularImpulse(uGuid, ...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed beyond the presumed leading `uGuid`. |
| `QueueAcceleration` | `Object.QueueAcceleration(uGuid, ...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `BeginQueuedAcceleration` | `Object.BeginQueuedAcceleration(uGuid, ...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumably pairs with `QueueAcceleration`, but that pairing is inferred from naming only. |

### Animation

| Function | Signature (best-known) | Notes |
|---|---|---|
| `PlayAnimation` | `Object.PlayAnimation(uGuid, sAnimName, bLoop, sChannel, nBlendTime, bFlag)` | Confirmed with 6 arguments in real scripts, e.g. `Object.PlayAnimation(self._vehicle, sVehicleAnimation, false, "hijack", nVehicleAnimBlendTime, true)`; one call site passes `nil` for the channel argument. |
| `StopAnimation` | `Object.StopAnimation(uGuid [, sAnimName])` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `StopAnimationChannel` | `Object.StopAnimationChannel(uGuid, sChannel)` | Used with a `uGuid` and a channel-name string in real scripts, e.g. `Object.StopAnimationChannel(self._vehicle, "hijack")` — matches the channel argument seen in `PlayAnimation`. |
| `StopAllAnimation` | `Object.StopAllAnimation(uGuid)` | Used with a plain `uGuid` argument in real scripts. |
| `PlayMaterialAnimation` | `Object.PlayMaterialAnimation(uGuid, sAnimName, bLoop)` | Confirmed with 3 arguments in real scripts, e.g. `Object.PlayMaterialAnimation(uGuid, "global_gpsjammer_anim", true)`. |
| `StopMaterialAnimation` | `Object.StopMaterialAnimation(uGuid, sAnimName)` | Confirmed with 2 arguments in real scripts, e.g. `Object.StopMaterialAnimation(uGuid, "global_weapon_beacon")`. |

### Winch & Cargo

| Function | Signature (best-known) | Notes |
|---|---|---|
| `HasWinch` | `b = Object.HasWinch(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetWinchState` | `Object.GetWinchState(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. The confirmed setter (below) uses string states like `"deployed"`, so the getter presumably returns the same, but that's inferred, not confirmed. |
| `SetWinchState` | `Object.SetWinchState(uGuid, sState)` | Used in real scripts with a string state argument, always seen as `Object.SetWinchState(uGuid, "deployed")`. |
| `AttachCargoToWinch` | `Object.AttachCargoToWinch(uCargo, uHeli)` | Confirmed with two `uGuid` arguments (cargo first, then the winching vehicle) in real scripts, e.g. `Object.AttachCargoToWinch(uCargo, uHeli)`. |
| `DetachCargoFromWinch` | `Object.DetachCargoFromWinch(uHeli)` | Confirmed with a single `uGuid` argument (the winching vehicle) in real scripts, e.g. `Object.DetachCargoFromWinch(uHeli)`. |
| `IsWinched` | `b = Object.IsWinched(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `if Object.IsWinched(uGuid) then`. |
| `IsWinching` | `Object.IsWinching(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### Attachment

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Attach` | `bResult, uAttachedGuid = Object.Attach(uParentGuid, sHardpoint, uChildGuid)` | Confirmed in real scripts with a parent `uGuid`, a hardpoint-name string, and a child `uGuid`, returning a success boolean and (per one call site) an attachment handle: `bResult, uRibbonInstance = Object.Attach(objectInstance, objectHPBone, uRibbonTemplate)`. |
| `Detach` | `bResult = Object.Detach(uParentGuid, uChildOrAttachmentGuid)` | Confirmed in real scripts with two `uGuid`-shaped arguments and a returned success boolean, e.g. `bResult = Object.Detach(objectInstance, uRibbonInstance)`. |
| `IsAttached` | `b = Object.IsAttached(uGuidA, uGuidB)` | Confirmed with two `uGuid` arguments in real scripts, e.g. `Object.IsAttached(uPlayerGuid, uDesignatorGuid)`. |
| `GetAttachedObjects` | `t = Object.GetAttachedObjects(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `tSeats = Object.GetAttachedObjects(uTruck)`, returning what call-site usage treats as a table/list. |
| `GetParent` | `uParentGuid = Object.GetParent(uGuid)` | Used with a plain `uGuid` argument in real scripts, very common for walking up an attachment/ownership chain. |

### Labels & Metadata

| Function | Signature (best-known) | Notes |
|---|---|---|
| `AddLabel` | `Object.AddLabel(uGuid, sLabel)` | Confirmed with a `uGuid` and a string label in real scripts, e.g. `Object.AddLabel(uHeli, "Disposable")`. |
| `RemoveLabel` | `Object.RemoveLabel(uGuid, sLabel)` | Confirmed with a `uGuid` and a string label in real scripts, e.g. `Object.RemoveLabel(uVehicle, "garage")`. |
| `HasLabel` | `b = Object.HasLabel(uGuid, sLabel)` | Extremely common in real scripts, always a `uGuid` and a string label, e.g. `Object.HasLabel(uGuid, "PMC")`. |
| `AddQualityRef` | `ref = Object.AddQualityRef(uGuid, nQuality)` | Confirmed in real scripts, e.g. `self._tQualityRefs[uGuid] = Object.AddQualityRef(uGuid, 1)` — the return value is stored and later passed to `RemoveQualityRef`. |
| `RemoveQualityRef` | `Object.RemoveQualityRef(ref)` | Used in real scripts with the value previously returned by `AddQualityRef` (not a raw `uGuid`), e.g. `Object.RemoveQualityRef(uRef)`. |
| `GetName` | `s = Object.GetName(uGuid)` | Used with a plain `uGuid` argument in real scripts, returns an internal/debug name (contrast with `GetLocalizedName` below). |
| `SetName` | `bSuccess = Object.SetName(uGuid, sName)` | Confirmed in real scripts, e.g. `local bSuccess = Object.SetName(Mendez_Spawn, "Mendez")`, returns a success boolean. |
| `GetLocalizedName` | `s = Object.GetLocalizedName(uGuid [, bFlag])` | Very common in real scripts for HUD/display text; one call site passes an extra boolean (`Object.GetLocalizedName(uVehicle, true)`), meaning unconfirmed. |
| `GetModelName` | `s = Object.GetModelName(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetModelName` | `Object.SetModelName(uGuid, sModelName)` | Confirmed with a `uGuid` and a model-name string in real scripts, e.g. `Object.SetModelName(uCharacterGuid, sModelName)`. |
| `AreEqual` | `b = Object.AreEqual(uGuidA, uGuidB)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### Visibility & State

| Function | Signature (best-known) | Notes |
|---|---|---|
| `IsVisible` | `b = Object.IsVisible(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `Object.IsVisible(Pg.GetGuidByName("Turncoat"))`. |
| `SetVisible` | `Object.SetVisible(uGuid, bVisible)` | Confirmed with a `uGuid` and boolean in real scripts, e.g. `Object.SetVisible(self._hijackee, true)`. |
| `IsAlive` | `b = Object.IsAlive(uGuid)` | Extremely common in real scripts, always a plain `uGuid` argument. |
| `IsAwake` | `b = Object.IsAwake(uGuid)` | Used with a plain `uGuid` argument in real scripts, related to the hibernation/streaming system alongside `GetHibernationDistance`. |
| `IsHibernated` | `b = Object.IsHibernated(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `if Object.IsHibernated(self.exec.guid) then`. |
| `GetHibernationDistance` | `n = Object.GetHibernationDistance(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `Object.GetHibernationDistance(uGuid) <= _tPrototype[iArg].nAARange`. |
| `SetHibernationDistance` | `Object.SetHibernationDistance(uGuid, nDistance)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed pair of the confirmed `GetHibernationDistance` / `RevertHibernationDistance`. |
| `RevertHibernationDistance` | `Object.RevertHibernationDistance(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `IsValid` | `b = Object.IsValid(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `if Object.IsValid(civAmbulance) then`. |
| `IsTemplate` | `b = Object.IsTemplate(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `if Object.IsTemplate(uVehicle) then`. |
| `IsDisguised` | `b = Object.IsDisguised(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `if Object.IsDisguised(uGuid) then`. |
| `IsPlayerControlled` | `b = Object.IsPlayerControlled(uGuid)` | Very common in real scripts, always a plain `uGuid` argument — used to distinguish AI-driven vs. player-driven vehicles/characters. |
| `InSeat` | `uVehicleGuid = Object.InSeat(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `local veh = Object.InSeat(self.exec.guid)` — return value treated as a vehicle handle at the call site. |
| `InVehicle` | `uVehicleGuid = Object.InVehicle(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `local uVeh = Object.InVehicle(uRunner)`. |
| `FadeOut` | `Object.FadeOut(uGuid, nDuration, bFlag)` | Confirmed with 3 arguments in real scripts, e.g. `Object.FadeOut(uVehicle, 0.2, true)`. |

### Object Lifecycle

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Remove` | `Object.Remove(uGuid)` | Extremely common in real scripts, always a plain `uGuid` argument. See Notes for modders below. |
| `AddToDisposer` | `Object.AddToDisposer(uGuid, sCategory)` | Confirmed with a `uGuid` and a category string in real scripts, e.g. `Object.AddToDisposer(uHeli, "Vehicle")`, `Object.AddToDisposer(uCargo, "vehicle")`. |
| `RemoveFromDisposer` | `Object.RemoveFromDisposer(uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed counterpart to the confirmed `AddToDisposer`. |
| `OpenGate` | `Object.OpenGate(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `Object.OpenGate(self.garage)`. |
| `CloseGate` | `Object.CloseGate(uGuid)` | Used with a plain `uGuid` argument in real scripts, e.g. `Object.CloseGate(self.garage)` — always paired with `OpenGate` in the same modules. |
| `SetInfiniteAmmo` | `Object.SetInfiniteAmmo(uGuid, bEnabled)` | **Confirmed working by live testing** — see [Snippets](../snippets#toggle-infinite-ammo). Note the documented nuance there: it maxes out reserve ammo, not the current magazine. |

## Notes for modders

- `Kill` and `Remove` are presumably destructive/irreversible operations — consistent with how this codebase
  generally treats teardown calls elsewhere — but this has not been verified through live testing on this
  namespace specifically. Treat both as one-way unless you've confirmed otherwise.
- Virtually everything on this namespace requires a valid, already-existing `uGuid`. There's no create/spawn
  function here — spawning new objects is handled by a different namespace (`Pg`), not `Object`.
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Object)` dump) but their
  argument shape beyond a presumed leading `uGuid` is a guess based on naming convention only — don't build
  mods around them without testing in-game first.
