---
title: MrxShootingGallery
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mission, player]
verified: true
verified_note: 'deeper pass: re-confirmed all 9 functions + 5 Event.* subscriptions against source; flagged the module-global event-handle pattern (_BorderEventP1/P2, uFireLockVO, tWeapons are bare globals, not locals) and the RemoveWeapons double-read quirk; cross-linked Human/Object/Player/Event/Net namespaces + MrxVoSequence; replaced boilerplate modder notes.'
---

# MrxShootingGallery

*Module: mrxshootinggallery.lua*

## Overview
The `MrxShootingGallery` module drives the "shooting gallery" minor-contract scenario (the one that
hands you a gallery weapon inside a bounded firing range). It temporarily strips the player's normal
weapons and stows them below the character, sets up an invisible boundary around the range, and
toggles each character's **firelock** (weapon-firing disable) as they step in and out of that
boundary. When the mission ends it hands the original weapons back.

## Inheritance
- Inherits from: `none`
- Imports: [`MrxSubtitle`](mrxsubtitle), [`MrxVoSequence`](mrxvosequence)

`MrxSubtitle` is imported but not referenced in this file; only [`MrxVoSequence.Start`](mrxvosequence)
is actually called (the firelock warning VO).

## Instance pattern
Stateless module — all state lives in **module-level globals**, not a per-instance table. The event
handles it stores (`_BorderEventP1`, `_BorderEventP2`, `uFireLockVO`, `tWeapons`, `uPrimaryWeapon`,
`_evNetSafeSetupBorder`) are plain globals; only `_evPlayerJoined` is declared `local`. This means a
single active gallery at a time is assumed — there is no `tInstance[uGuid]` bookkeeping.

## Functions
### `RemoveWeapons(uPlayer)`
Drops the player's primary and secondary weapons, disables their physics, and teleports each one to
5 units below the player (`Object.SetPosition(w, x, y - 5, z)`) so they are out of reach for the
duration. Returns a `tWeapons` table with keys `Primary1`, `Primary2`, `Secondary1`, `Secondary2`
(any of which may be nil). Note it re-reads `Human.Inventory.GetPrimaryWeapon` a *second* time after
dropping the first (and likewise for secondary) to catch a second held weapon — the two reads are
against the live inventory, so what lands in `Primary2` is whatever is primary *after* `Primary1` was
dropped.

### `ReturnWeapons(uPlayer, tWeapons)`
Turns off infinite ammo (`Object.SetInfiniteAmmo(uPlayer, false)`), drops the temporary gallery
weapon the player is holding, then re-equips the saved weapons in reverse order (`Secondary1`,
`Secondary2`, `Primary2`, `Primary1`) so `Primary1` ends up as the active weapon.

### `ClearEvents()`
Deletes all registered events related to the shooting gallery mission, ensuring no lingering event handlers remain.

### `Reset()`
Resets the firelock states for both primary and secondary characters and clears any existing events. This function is called when resetting the mission state.

### `NetSafeSetupBorder(uBorderName)`
Sets up the border for the shooting gallery on the client side if the player is not local. It creates an event to call `SetupBorder` when the game state changes to "WaitForTether".

### `SetupClientBorder(uBorderName)`
Sets up boundary events for the secondary character on the client side. This function ensures that firelock states are managed correctly when the player exits or enters the designated area.

### `SetupBorder(uBorderName)`
Sets up the shooting gallery border on both server and client sides. It configures firelock states, creates boundary events, and handles player join events to ensure proper mission setup.

### `SteppedOut(uChar, uBorderName)`
Called when a character exits the designated boundary area. This function sets the firelock state to true for the character and starts a voice sequence warning about restricted weapon usage. Contains an empty `if Player.GetLocalCharacter() == uChar then end` block with no body — likely lost/stripped logic from decompilation, has no effect either way.

### `SteppedIn(uChar, uBorderName)`
Called when a character enters the designated boundary area. This function sets the firelock state to false for the character and re-creates boundary events to manage further transitions.

## Events
All subscriptions below are real [`Event.Create`](../namespaces/event)/`Event.CreatePersistent` calls.

- `Event.GameStateChange` filtered on `"WaitForTether", "exit"` (via `NetSafeSetupBorder`, handle `_evNetSafeSetupBorder`) — re-runs `SetupBorder(uBorderName)` once the tether wait state exits, client-only (`Net.IsClient()` gate).
- `Event.ObjectHibernation` filtered on `"awake"` (via `SetupClientBorder`) — one-shot, waits for the secondary character to wake before wiring up `_BorderEventP2`.
- `Event.ScriptEvent` named `"mpPlayerJoin"` (persistent, via `SetupBorder`, handle `_evPlayerJoined`) — guarded to only fire when `Net.IsServer()` and the joining player is not local; calls `SetupClientBorder`.
- `Event.Boundary` (via `SetupBorder`/`SteppedOut`/`SteppedIn`, handles `_BorderEventP1`/`_BorderEventP2`) — fires on `"exit"`/`"enter"` of `uBorderName` for the primary/secondary character; `SteppedOut` and `SteppedIn` re-create each other's opposite-direction listener every time they fire, forming a ping-pong chain.
- `Event.WeaponEvent` filtered on `"FireLock"` for the primary weapon (via `SteppedOut`, handle `uFireLockVO`) — triggers `MrxVoSequence.Start` with the VO line `"Fiona-In-Mission-MinorContract-Pmc31-08"` when the locked weapon is fired.

## Module constants & tunables
- **VO line on firelock**: `"Fiona-In-Mission-MinorContract-Pmc31-08"` — the [`MrxVoSequence.Start`](mrxvosequence)
  bark played when a firelocked weapon is pulled outside the boundary (via the `Event.WeaponEvent`
  handler in `SteppedOut`). Swap this string to change the "you can't shoot here" warning.
- **Drop depth**: weapons are stashed at `y - 5` (5 world units below the player). No other magic
  numbers or template names in this file.
- The boundary object itself is passed in as `uBorderName` (a named world region); this module does
  not create it — it only subscribes to `Event.Boundary` on it.

## Notes for modders
- All the mission wiring is **overridable** — every function here is a plain global (not `local`), so
  a mod can replace `SteppedOut`/`SteppedIn` to change what firelock/VO behavior happens at the
  boundary. See [Function override](../deep-dives/function-override).
- The boundary handlers are self-rearming: `SteppedOut` deletes the current `"exit"` listener and
  creates the opposite `"enter"` listener via `SteppedIn`, and vice-versa. If you add work in either,
  keep that delete/recreate pair intact or the ping-pong chain breaks.
- [`Human.SetFireLock(uChar, bLock)`](../namespaces/human) is the actual firing gate — `true` locks,
  `false` unlocks. `Reset()` unlocks both characters and tears down all events; call it (or let the
  `uBorderName == nil` path of `SetupBorder` call it) to fully clean up.
- {: .warning } The event handles are module globals, so only one gallery boundary can be active at a
  time. Two concurrent `SetupBorder` calls would clobber `_BorderEventP1`/`_BorderEventP2` and leak
  the previous listeners.
- Client/host split: `SetupBorder` runs the server-authoritative `Net.SetShootingGalleryBorder` and
  wires the `"mpPlayerJoin"` [`ScriptEvent`](../namespaces/event); `NetSafeSetupBorder` and
  `SetupClientBorder` handle the client/joining-player side. See [`Net`](../namespaces/net).