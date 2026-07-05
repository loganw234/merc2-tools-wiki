---
title: RandomlyTeleportPlayer
parent: Cheats & Dev Tools
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [stress test, teleportation]
verified: true
verified_note: "deeper pass: re-confirmed Init/Go + Event.TimerRelative reschedule against source; surfaced the actual tLocation marker names, the +20 Y offset, the 5-20s delay, and the bad-location 0.1s retry path; documented two real bugs — the last tLocation entry is unreachable (randf upper bound is table.maxn, exclusive after floor) and x/y/z/n/s/e/guid are shared file-scope locals, not per-call"
---

# RandomlyTeleportPlayer

*Module: randomlyteleportplayer.lua*

## Overview
The `RandomlyTeleportPlayer` module is a stress test utility that randomly teleports the local player to predefined locations in the game world. It sets up a timer to repeatedly perform this teleportation, adding variability by changing both the destination and the delay between teleports.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless utility module (no per-instance tables). It holds one `local` destination list,
`tLocation`, and a set of **file-scope** `local` scratch variables `x, y, z, n, s, e, guid` shared across
calls (declared once at the top, reused by `Go` each tick — they are *not* fresh per-call locals). `e`
holds the current `Event.TimerRelative` handle.

### `tLocation` — the destination markers
The hardcoded jump targets are named world markers resolved at runtime via `Pg.GetGuidByName`:
`"All_HQ"`, `"Gur_HQ2"`, `"GurHQ"`, `"MecRecruit"`, `"OilHQ"`, `"PMC1.1"`, `"Teleporter 0x000921c5"`.
Edit this list to point the stress test at your own markers.

## Functions
### `Init()`
Called once when the module initializes. It starts the teleportation process by calling `Go`.

### `Go()`
Performs one random teleport and reschedules itself:
1. Picks `tLocation[Math.floor(Math.randf(1, table.maxn(tLocation)))]`.
2. Resolves it to a GUID with `Pg.GetGuidByName`; if that fails, `x/y/z` are set nil.
3. **Bad-location path** — if no position resolved, logs `"STRESS TEST: Bad location: …"` and retries
   quickly via `Event.Create(Event.TimerRelative, {0.1}, Go)` (0.1 s).
4. **Good path** — logs the destination + delay, then teleports the local character with
   `Object.SetPosition(Player.GetLocalCharacter(), x, y + 20, z)` (the `+ 20` Y offset drops the player in
   from slightly above the marker), and reschedules `Go` after `Math.randf(5, 20)` seconds.

{: .warning }
> **Off-by-one in the picker:** the index is `Math.floor(Math.randf(1, table.maxn(tLocation)))`, i.e. a
> float in `[1, 7)` floored — which yields `1`–`6`, never `7`. The last entry (`"Teleporter 0x000921c5"`)
> is therefore **unreachable**. If you add markers to `tLocation`, the final one you add is always the one
> that never gets picked.

## Events
Uses `Event.Create(Event.TimerRelative, {<delay>}, Go)` to re-arm itself each cycle — a real
[`Event`](../namespaces/event) scheduling call (a one-shot relative timer), re-created every tick rather
than a persistent subscription. The good path schedules `Go` after 5–20 s; the bad-location path after
0.1 s. `Init` kicks the first `Go` off directly (no timer).

## Notes for modders
- Stress-test utility, not for production — it teleports the local player indefinitely once `Init` runs.
- Retarget it by editing `tLocation` (see above) — but remember the **last entry is never chosen** (the
  off-by-one above), so pad the list with a throwaway final marker if you want all your real ones reachable.
- Change the cadence via the two `Math.randf(5, 20)` calls in `Go`; change the drop height via the `y + 20`
  offset.
- It teleports `Player.GetLocalCharacter()` only — the local player, not every player (contrast
  [`_G.DebugTeleport`](mrxcheatbootstrap) in the cheat bootstrap, which moves all players).