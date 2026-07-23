---
title: Vehicle
parent: Engine Namespaces
nav_order: 2
---

# Vehicle

## Overview
`Vehicle` is an engine namespace: implemented natively by the game engine, not by any decompiled `.lua` module. It lives under `resident/` in no source file — it requires no `import()` and is always available as a global table from any script. Its functions operate on vehicle object `uGuid`s and cover rider/seat management, doors and hatches, turrets, the hijacking state machine, and a few vehicle-specific physics helpers (flip state, flight state, heli spin).

## Provenance
The 40 functions listed below are a complete, authoritative enumeration taken from a live `pairs(Vehicle)` dump in-game — every name here is confirmed to exist. That dump gives names and raw function pointers only, nothing about parameters or behavior. Everything beyond that (argument shapes, likely purpose) is inferred from real call sites in the ~230 decompiled `.lua` files; where no call site exists anywhere in that corpus, this page says so explicitly rather than guessing.

## Functions

### Seats & Riders

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetDriver` | `GetDriver(uVehicle)` | Very widely used with a plain `uGuid` argument in real game scripts; returns the driver's character guid (or `nil` if unmanned — see e.g. usage guarded with `if Vehicle.GetDriver(uVeh) == nil`). |
| `GetRiders` | `GetRiders(uVehicle, sSeatType?)` | Used with a plain `uGuid`, and commonly with a second string argument such as `"p"`, `"g"`, or `"driver"` to filter by seat type; returns a table of rider guids. |
| `GetFromRider` | `GetFromRider(uCharacter)` | Used with a plain character `uGuid`; returns the vehicle guid the character is currently riding in, or `nil` if on foot. |
| `GetSeatFromRider` | `GetSeatFromRider(uCharacter)` | Used with a plain character `uGuid`; returns a seat guid. |
| `GetRiderFromSeat` | `Vehicle.GetRiderFromSeat(uVehicle, seat)` | **Probed live over the WebSocket lua-bridge (2026-07-22)** — same inconclusive result as `GetFromSeat` below: neither `'d'` nor `0` as the `seat` argument returned anything but `nil`. The correct seat-id shape is still unconfirmed. Still presumed the inverse of `GetSeatFromRider` by naming symmetry, but that remains inference, not evidence. |
| `GetSeatByType` | `GetSeatByType(uVehicle, sSeatType, bBoolFlag?)` | Used with a vehicle `uGuid` plus a seat-type string (`"p"`, `"d"`), and in at least one call site a third boolean argument. |
| `GetSeatToSeat` | `GetSeatToSeat(uSeat, bBoolFlag)` | Used with a seat guid and a boolean; appears to return possible seat-transfer targets. |
| `GetFromSeat` | `Vehicle.GetFromSeat(uVehicle, seat)` | **Probed live over the WebSocket lua-bridge (2026-07-22)** — inconclusive, not solved: the call takes a vehicle guid and a `seat` identifier, but neither shape tried, `'d'` (string) nor `0` (number), returned anything but `nil`. The correct seat-id shape is still unconfirmed — don't treat this as a working call yet; it needs a follow-up probe (e.g. a seat guid obtained from `GetSeatByType`/`GetSeatToSeat` above) rather than a guessed literal. Still no call sites in the decompiled corpus. |
| `GetSeatParams` | `GetSeatParams(uSeat)` | Used with a seat guid; returns a table with at least an `IsGunner` field per observed usage. |
| `TransferToSeat` | `TransferToSeat(uVehicle, uSeat, bBoolFlag)` | Used with a vehicle guid, a seat guid, and a boolean flag. |
| `EnterBySeatGuid` | `EnterBySeatGuid(uVehicle, uCharacter, uSeat, bImmediate, bFlag2?)` | Used with a vehicle guid, character guid, seat guid, and one or two boolean flags; returns a success boolean. |
| `Enter` | `Enter(uVehicle, uCharacter, sSeatType, bImmediate, bFlag2?)` | Used with a vehicle guid, character guid, a seat-type string (`"d"`, `"p"`), and one or two boolean flags. |
| `Exit` | `Exit(uVehicle, uCharacter, bFlag?)` | Used with a vehicle guid and a character guid, frequently with a trailing boolean. |
| `IsSeatALadder` | `IsSeatALadder(uSeat)` | Used with a plain seat guid; returns a boolean. |
| `IsSeatBlocked` | `IsSeatBlocked(uSeat)` | Used with a plain seat guid; returns a boolean. |

### Doors & Turrets

| Function | Signature (best-known) | Notes |
|---|---|---|
| `OpenDoor` | `OpenDoor(uVehicle, sDoorName)` | Used with a vehicle guid and a door/part name string (e.g. `"pivot"`, `"DriverHatch"`). `Vehicle.OpenDoor(uGuid, "DriverHatch")` has been proposed in this project as a live test for opening a tank hatch, but as of this writing no wiki page marks that call as confirmed by live testing — treat it as proposed-but-unconfirmed, not verified. |
| `CloseDoor` | `CloseDoor(uVehicle, sDoorName)` | Used with a vehicle guid and a door/part name string (e.g. `"pivot"`), mirroring `OpenDoor`. |
| `EnableTurret` | `EnableTurret(uVehicle, sTurretName, bEnable, sAxis?, bAxisFlag?)` | Used with a vehicle guid, a turret/part name (`"head"`, `"main_turret"`), a boolean, and in some call sites additional axis-related arguments (`"pitch"`, `"all"`, plus a boolean). **Confirmed control/orientation-only — not weapon selection.** Every real call site (`resident/mrxactionhijack.lua:83,123,955,1069,1072`) is disabling or re-enabling the turret's own control during a vehicle-hijack cinematic (`Vehicle.EnableTurret(self._hijackee, "head", false, "all", false)` before the cinematic, `Vehicle.EnableTurret(self._hijackee, "head", true)` after) — none of them touch what the turret fires. |
| `SetTurretPitch` | `SetTurretPitch(uVehicle, sTurretName, nValue)` | Used with a vehicle guid, turret name, and a numeric value (observed as `0`, `resident/mrxactionhijack.lua:124`, resetting the turret's pitch to level right after disabling it during hijack). Orientation only, same caveat as `EnableTurret`. |
| `SetTurretYaw` | `Vehicle.SetTurretYaw(uVehicle, nAngle)` | **Live-confirmed via WebSocket lua-bridge probe (2026-07-22)**, marked **EFFECT** — a write, not a read: confirmed to execute with a vehicle guid and a numeric angle, no return value. Presumed analogous to the confirmed `SetTurretPitch` by naming only (including whether it's orientation-only the way `SetTurretPitch`/`EnableTurret` are confirmed to be above — that specific point wasn't independently re-verified by this probe). Still no call sites in the decompiled corpus. |
| `SetParts` | `SetParts(uVehicle, sPartName, bState)` | Used with a vehicle/object guid, a part name string (e.g. `"LightFront"`, `"CtrlRotation"`), and a boolean; returns a boolean. Also used on non-vehicle gate/alarm objects in the decompiled source, suggesting broader applicability than just player vehicles. |
| `SetCanPlayerUse` | `SetCanPlayerUse(uVehicle, sSeatType, bCanUse)` | Used with a vehicle guid, a seat-type string (`"d"`, `"a"`), and a boolean. |
| `Usable` | `Usable(uVehicle, bUsable)` | Used with a vehicle guid and a boolean; toggles whether the vehicle can be entered/used. |

### Hijacking

| Function | Signature (best-known) | Notes |
|---|---|---|
| `HijackStart` | `HijackStart(uHijacker, uHijackee, uVehicle, oSelf?)` | Used with hijacker guid, hijackee guid, vehicle guid, and (in the one observed call site) a fourth argument that was a table/object reference (`self`). |
| `HijackAbort` | `HijackAbort(uHijacker)` | Used with a plain character guid. |
| `HijackAbortDone` | `HijackAbortDone(uHijacker)` | Used with a plain character guid. |
| `HijackComplete` | `HijackComplete(uHijacker)` | Used with a plain character guid. |
| `SetHijackState` | `SetHijackState(uHijacker, nState)` | Used with a character guid and a numeric state value. |
| `SetHijackSuccess` | `SetHijackSuccess(uHijacker, bSuccess)` | Used with a character guid and a boolean (observed as `false`). |
| `IsHijackRemote` | `IsHijackRemote(uHijacker)` | Used with a character guid; call site guards the call itself with `Vehicle.IsHijackRemote and ...`, implying the function's presence was historically uncertain in some contexts. |
| `IsHijackBad` | `b = Vehicle.IsHijackBad(uGuid)` | **Live-confirmed via WebSocket lua-bridge probe (2026-07-22)**: confirmed to return a boolean. The probe didn't disambiguate which guid this expects (hijacker character vs. vehicle) — naming symmetry with the adjacent `uHijacker`-taking hijack functions makes hijacker guid the likelier reading, but that's inference, not confirmed. Still no call sites in the decompiled corpus. |
| `CancelHijack` | `CancelHijack(uCharacter)` | Used with a plain character guid, called on player logout/cleanup in the observed call site. |
| `StartTankHijackMotion` | — | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `StopTankHijackMotion` | `StopTankHijackMotion(uVehicle)` | Used with a plain vehicle guid. |

### Vehicle State & Physics

| Function | Signature (best-known) | Notes |
|---|---|---|
| `IsFlying` | `IsFlying(uVehicle)` | Used with a plain vehicle guid; returns a boolean, checked before flight-specific hijack logic. |
| `IsFlipped` | `b = Vehicle.IsFlipped(uVehicle)` | **Live-confirmed via WebSocket lua-bridge probe (2026-07-22)**: confirmed to return a boolean. Still no call sites in the decompiled corpus. |
| `SpinHeli` | — | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `RestoreAmmo` | `Vehicle.RestoreAmmo(uVehicle)` | **Live-confirmed via WebSocket lua-bridge probe (2026-07-22)**, marked **EFFECT** — a write, not a read: confirmed to execute cleanly, no return value. Still no call sites in the decompiled corpus. |
| `RestoreHealth` | `Vehicle.RestoreHealth(uVehicle)` | **Live-confirmed via WebSocket lua-bridge probe (2026-07-22)**, marked **EFFECT** — a write, not a read: confirmed to heal the vehicle to full health (observed 98.9 → 100 in the probe). Still no call sites in the decompiled corpus. |
| `ClearControls` | `ClearControls(uVehicle)` | Used with a plain vehicle guid, called alongside turret-disable logic during hijack setup. |

## Notes for modders

**No function on this namespace selects what a turret fires.** Investigated directly while researching
whether a "vehicle weapon editor" mod was feasible: the turret functions above only ever control
orientation and enable/disable state, never which weapon or ordnance fires. The actual mechanism for
spawning a projectile in this engine is the [`Airstrike`](airstrike) namespace — but no call site anywhere
in the corpus connects it to a vehicle's own turret; the modules that call it (`autogunship.lua`,
`mrxartillery.lua`, etc.) are all separate AI/scripted objects, not the player-driven vehicle turrets these
functions manage. As far as the decompiled corpus shows, a player-operated vehicle's mounted gun fires via
a mechanism with no Lua touchpoint at all.

**Update: this is specifically about firing, not aiming.** [Reading and Attaching to Any Bone](../deep-dives/bone-manipulation)
found that a turret's aim direction *is* readable — the vector between two of its own hardpoints (e.g.
`hp_seat_cannon`/`hp_barreltip_cannon`) gives the real barrel line. What's confirmed above still holds
unchanged: knowing where a gun points is not the same as knowing what makes it fire, and no Lua touchpoint
for the latter has been found.

The eleven hijack-related functions — `HijackStart`, `HijackAbort`, `HijackAbortDone`, `HijackComplete`, `SetHijackState`, `SetHijackSuccess`, `IsHijackBad`, `IsHijackRemote`, `CancelHijack`, `StartTankHijackMotion`, and `StopTankHijackMotion` — clearly belong to a single state machine driving the game's hijack-a-vehicle mechanic, based on their co-occurrence in the hijack-handling source. Beyond that, this page does not attempt to describe the actual flow (what triggers each transition, what states `SetHijackState`'s numeric argument accepts, etc.) — that would go beyond what the call-site evidence supports. This is a strong candidate for future live-testing to map out the real sequencing.

Two functions, `SpinHeli` and `StartTankHijackMotion`, have zero call sites anywhere in the decompiled corpus and no live-probe data either — they're confirmed to exist via the live `pairs(Vehicle)` dump, but nothing is known about their arguments or behavior beyond what their names suggest; treat any assumption about them as a guess, not a fact. `IsFlipped`, `RestoreAmmo`, `RestoreHealth`, `SetTurretYaw`, and `IsHijackBad` also have zero call sites in the decompiled corpus, but now have live-confirmed signatures from a 2026-07-22 WebSocket lua-bridge probe — see their rows above rather than treating them as unknowns. `GetRiderFromSeat` and `GetFromSeat` were probed the same session but remain genuinely unresolved (see their rows above) — don't lump them in with the fully-confirmed ones.
