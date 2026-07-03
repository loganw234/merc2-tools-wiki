---
title: MrxSupportDelivery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, delivery]
verified: true
verified_note: read directly from source -- corrects the Instance pattern (class-factory, not per-uGuid) and Events section (the previous version listed internal functions as if they were subscribed-to custom events), and documents a real confirmed bug in SetCargoDropHeight
---

# MrxSupportDelivery

*Module: mrxsupportdelivery.lua*

## Overview
`MrxSupportDelivery` extends [`MrxSupport`](mrxsupport) with the "spawn cargo, spawn a helicopter, winch
the cargo, fly to target, drop it" sequence used by every support type that delivers something via
helicopter (vehicles, reinforcements, supply crates). It's the concrete worked example
[`MrxSupport`](mrxsupport)'s own page points to for how a real support-type module is actually built on
top of that base.

**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uOwnerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: `MrxSupportManager`, `MrxSupportDesignatorSmoke`, `MrxGui`, `MrxUtil`

## Instance pattern
Class-style object (see Overview). Fields set by `Create`:
- `bCareless` — passed to `Ai.Deliver` later; skips whatever "careless" gates in delivery AI (source
  doesn't spell out exactly what changes, but it's a real parameter that reaches the AI call, not cosmetic).
- `oTarget` / `sFinalDestination` — target-location fields (`sFinalDestination` is set here but the actual
  delivery-completion logic reads `self.oFinalDestination` — see `SetFinalDestination`'s note below).
- `sDeliveryVehicle`/`uDeliveryVehicle` — defaults to `"UH1 Transport (PMC) (Driver)"`.
- `sCargoToDeliver`/`uCargoToDeliver` — defaults to `"box"`.
- `nCargoDropHeight` — defaults to `0.5`. **See the confirmed bug in `SetCargoDropHeight` below before
  relying on this being independently settable.**
- `bNeedsConnection`, `oUpdateEvent` — set to `false`/`nil` in `Create` but never read or written anywhere
  else in this file. Likely vestigial fields inherited from a shared pattern with other support types, or
  dead code — don't build logic depending on them without checking a specific subclass that actually uses
  them.
- `oDesignator` — a [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke) instance, created fresh in
  `Create` and defaulted to blue smoke color.

## Functions

### `Create(self, uOwnerGuid)`
Builds the instance (see Overview/Instance pattern), creates a blue-smoke designator, sets the recruit
type to `"Copter"`, and registers the module name as `"MrxSupportDelivery"`.

### `DesignationCallback(self)`
Just calls `_DesignatorCallback(self)` — the actual entry point once a target has been designated.

### `SetCargoGuid(self, uCargoTemplate)` / `SetCargo(self, sCargoTemplateName)` / `PickCargo(self, sCargoTemplateName)`
Three ways to choose what gets delivered. `SetCargoGuid` sets a specific template GUID directly and marks
`bSetCargoGuidCalled` (so `_DesignatorCallback` won't re-roll it). `SetCargo`/`PickCargo` take a template
*name* — or a table of names, in which case one is picked at random via `MrxUtil.GetRandomTableElement`.

### `SetCareless(self, bCareless)`
Sets `self.bCareless` — guarded by a `type(self) == "table"` check (a defensive no-op if called
incorrectly, not a real validation of `bCareless` itself).

### `SetFinalDestination(self, oFinalDestination)`
**A real, confirmed naming mismatch**: this sets `self.oFinalDestination`, but `Create` populates a
*different* field, `self.sFinalDestination`, from the prototype's own `sFinalDestination`. Nothing in this
file's visible logic reads `oFinalDestination` back — treat this function with suspicion until you've
confirmed (via a specific subclass or live testing) which field actually drives delivery targeting.

### `SetCargoDropHeight(self, sCargoTemplateName)`
**Confirmed bug, read directly from source: this function ignores its own argument entirely.**

```lua
function SetCargoDropHeight(self, sCargoTemplateName)
  if "table" ~= type(self) then
    return
  end
  if "number" ~= type(nCargoDropHeight) then    -- reads the *global* nCargoDropHeight, not the parameter
    return
  end
  self.nCargoDropHeight = nCargoDropHeight        -- and copies that same global onto self
end
```

The parameter is misleadingly named `sCargoTemplateName` (almost certainly copy-pasted from `PickCargo`
just above it) and is never referenced in the body at all. Both checks and the assignment read the
module-level global `nCargoDropHeight` (declared once at the top of the file, `0.5`) instead — so calling
`oSupport:SetCargoDropHeight(50)` does not set the drop height to `50`; it silently resets
`self.nCargoDropHeight` back to whatever the module-level default currently is. If you need a custom drop
height, set `self.nCargoDropHeight = <value>` directly rather than calling this function.

### `_DesignatorCallback(self)`
The real delivery sequence starts here: no-ops on the client (`Net.IsClient()`), picks cargo if not
already chosen, spawns the cargo object from the camera, computes a spawn point via
`Pg.FindPointFromCamera`, spawns the delivery helicopter there, orients it toward the target, and waits
(`Event.ObjectHibernation`) for the helicopter to wake up before calling `_DeployWinch`.

### `_DeployWinch(self, uHeli, uCargo)`
Plays a faction-appropriate "incoming support" voice-over line (a hardcoded table keyed by faction
display name — `PMC`/`Allied`/`China`/`VZ`/`Guerilla`/`OC`), deploys the winch
(`Object.SetWinchState(uHeli, "deployed")`), then waits for the cargo object itself to wake up before
calling `_WaitCallback`.

### `_WaitCallback(self, uHeli, uCargo)`
Attaches the cargo to the winch, sets up the damage-abort event
(`MrxSupport.SetupDamageEvent`), and issues the actual `Ai.Deliver(...)` order (passing
`self.nCargoDropHeight`/`self.bCareless`). Registers `CargoDropped` to fire when the cargo detaches from
the winch (`Event.ObjectWinched`).

### `CargoDropped(self, uHeli, uCargo)`
Sends the helicopter home (`MrxSupport.GoHome`) and marks the cargo for disposal.

## Events
Confirmed directly from source — these are one-shot registrations tied to a specific delivery in
progress, not persistent subscriptions:
- `Event.ObjectHibernation` — waits for the spawned helicopter to wake (`_DesignatorCallback` →
  `_DeployWinch`), then separately for the spawned cargo to wake (`_DeployWinch` → `_WaitCallback`).
- `Event.ObjectWinched` (`"Detach"`) — fires `CargoDropped` once the cargo detaches from the winch.

**Not events**: `DesignationCallback`, `_DesignatorCallback`, `_DeployWinch`, `_WaitCallback`, and
`CargoDropped` are plain functions called directly or passed as one-shot event callbacks above — none of
them are subscribed-to custom events themselves. An earlier version of this page incorrectly described
each as something the module "listens for."

## Notes for modders
- **`SetCargoDropHeight` doesn't work as its signature implies — see the confirmed bug above.** Set
  `self.nCargoDropHeight` directly instead.
- **`SetFinalDestination` writes a field (`oFinalDestination`) that nothing visible in this file reads
  back** (`Create` populates `sFinalDestination` from the prototype instead) — verify against a real
  subclass before depending on this.
- Use `SetCargoGuid` (exact template) or `SetCargo`/`PickCargo` (name, or random from a list) to choose
  what gets delivered — `SetCargoGuid` takes precedence if called, via the `bSetCargoGuidCalled` flag.
- `Net.IsClient()` gates the entire delivery sequence in `_DesignatorCallback` — this only runs
  server-side; a client triggering a delivery relies on the server-side replication of whatever
  spawns/events result, not on this function running locally.
