---
title: "Squad — Team & Tactics Layer"
parent: Essentials (Ess)
nav_order: 21
---

# Squad — Team & Tactics Layer

## Overview

`Ess.Squad` (`src/67_squad.lua`, plus `67_squad_easy.lua`/`67_squad_formation.lua`/`67_squad_queue.lua`/
`67_squad_tactics.lua`) is an opt-in team/role layer over [`Ess.Followers`](followers), for a script managing
enough followers that "the whole roster" stops being the right unit of command. New in **v0.3.4**, which
`CHANGELOG.md` headlines as **"the `Ess.Squad` team/orchestration pass."**

`Ess.Squad` is two layers removed from the native engine: it wraps `Ess.Followers`, and `Ess.Followers` itself
wraps [`Ess.AIOrders`](encounter-toolkit#aiorders) (see that page's AIOrders section for the actual
`Ai.Goal`/`Ai.Anchor`/`Ai.Deploy` primitives underneath). `Ess.Squad` adds no new native calls of its own and
keeps no separate roster — a "team" is just a named, ordered subset of guids that are already
`Ess.Followers` members, and every order Squad issues ultimately flows through the same `Ess.Followers`
machinery a plain `Ess.Followers.order()` call would use. This page assumes you're already familiar with
`Ess.Followers`' own roster/recruit/dismiss/order/markers/auto-resume-follow model — see [Followers](followers)
for all of that; here we only cover what Squad adds on top.

**No inherited-bug caveat needed.** Several fixes/refinements landed in `Ess.Followers` itself in this *same*
0.3.4 release — vehicle-aware "return to following," the on-foot Follow-role-drift fix, and
`Ess.Easy.Followers.orderEnter` (see [Followers](followers) and the CHANGELOG's `[0.3.4]` section) — and
`Ess.Squad` is built on the already-fixed version. There's no earlier-Followers-bug window Squad shipped
into.

## Teams and roles

```lua
Ess.Squad.createTeam(teamName, guids) -> ok
Ess.Squad.team(teamName) -> guids
Ess.Squad.teamOf(guid) -> teamName | nil
Ess.Squad.assignRole(guid, roleType) -> ok
Ess.Squad.roleOf(guid) -> roleType | nil
```

`createTeam(teamName, guids)` (re)defines a team's membership from a guid list. Only guids that are
currently `Ess.Followers.isFollower()` members are kept — anything else in the list is silently dropped, not
an error. `teamName` can't be `"__all__"`: that string is `Ess.Followers._orderScoped`'s own reserved scope
key for the whole-roster case (see [`orderTeam`](#orderteamteamname-behavior-opts) below), and
`createTeam` refuses it outright so a same-named team could never collide with that tracking.

`team(teamName)` returns the **current live membership**, not whatever was last passed to `createTeam`. Every
read re-checks `Ess.Followers.isFollower()` on each stored guid and drops any that no longer qualify (dead,
dismissed, or otherwise pruned out of the Followers roster). There's no dismiss/death hook on the team side —
membership is filtered on *read* instead, the mirror image of `Ess.Followers.list()`'s own self-healing prune
on *write*. Practically: a team can never hand you back a guid that's no longer a follower, but calling
`team()` is what does the pruning, not some background listener.

`teamOf(guid)` is a best-effort auxiliary index — "which team was this guid last assigned to via
`createTeam`" — not a live-membership check. It's never cleared when a guid stops being a follower, so it can
answer with a team name for a guid that `team(teamName)` would no longer include. Use `team()` when you need
current membership; use `teamOf()` only for "what was this guid's last assignment."

`assignRole(guid, roleType)` stores a free-form string (`"driver"`, `"heavy"`, anything a script chooses) —
Squad itself doesn't validate or enforce it. Only [`Ess.Squad.Tactics.mountUp`](#tactics-mountupvehguid-targetgroup-opts--dismountandsecuretargetgroup-atpos-radius)
actually reads a role back (`"driver"` specifically, to decide seating order); everything else that stores a
role is just bookkeeping for a later module. `roleOf(guid)` reads it back, `nil` if never assigned.

## `orderTeam(teamName, behavior, opts)`

`Ess.Followers.order(behavior, opts)` scoped to one team instead of the whole roster — same behavior names,
same `opts` shape `Ess.AIOrders.command`/`Ess.Followers.order` already take. An empty or unknown team name is
a safe no-op (`false`), matching `Ess.Followers.order()`'s own "empty roster does nothing" contract.

```lua
function Ess.Squad.orderTeam(teamName, behavior, opts)
    local list = Ess.Squad.team(teamName)
    if #list == 0 then return false end
    return Ess.Followers._orderScoped(tostring(teamName), list, behavior, opts)
end
```

It's built directly on the new `Ess.Followers._orderScoped` — the scoped core that `Ess.Followers.order()`
itself now calls internally too (as the `"__all__"` scope). This is a brief internal-refactor note, not part
of Squad's own public surface: the point is that `orderTeam` isn't a bolted-on filter over `order()`'s
result, it's the *same* underlying mechanism `order()` uses, just handed a team's guid list and a team-name
scope instead of the whole roster and `"__all__"`.

**That scoping is the actual interesting engineering point here, confirmed live:** ordering one team leaves
every other follower — whether they're in a different team, or in no team at all — completely undisturbed.
Two things `_orderScoped` tracks per order (destination markers, and the natural-completion
auto-resume-follow callback) are keyed **per scope** in a table called `orderMarksByScope`, not against one
shared "last order" slot:

- Each `orderTeam` call clears only *its own scope's* previous marker batch first (`clearOrderMarks(scope)`),
  never another scope's.
- The floating destination marker(s) it places (world-space icon on an attack target, a ground ring on a
  move/guard point or patrol waypoints) get stored under `orderMarksByScope[teamName]`.
- When the order naturally completes (a non-looping move/patrol finishing, or an attack target dying — see
  [Followers](followers) for exactly which behaviors have a "natural completion" at all), the callback that
  clears those markers and resumes Follow only touches *that* scope's entry, and only if it's still the
  current one for that scope (a newer order in the *same* scope may have already replaced it).

Concretely: if Team A is mid-`attack` and Team B gets an independent `orderTeam(..., "move", ...)`, Team B's
move completing can't accidentally clear Team A's still-active attack marker or resume-follow Team A early —
and vice versa. Before this scoping existed (or if `orderTeam` were just a naive filter over `order()`),
two teams ordered independently could step on each other's in-flight order tracking; `orderMarksByScope`,
keyed by team name (or `"__all__"` for the whole-roster case `Ess.Followers.order()` itself uses), is
specifically what prevents that.

## `Ess.Easy.Squad`

Mirrors [`Ess.Easy.Followers`](followers)' own shape — named one-liners over the team layer instead of the
whole roster:

| Function | Wraps |
|---|---|
| `createTeam(teamName, guids)` | `Ess.Squad.createTeam` |
| `assignRole(guid, roleType)` | `Ess.Squad.assignRole` |
| `orderTeamAttack(teamName, target)` | `orderTeam(teamName, "attack", { target = target })` |
| `orderTeamPatrol(teamName, points)` | `orderTeam(teamName, "patrol", { points = points })` |
| `orderTeamGuard(teamName, at)` | `orderTeam(teamName, "defend", { at = at })` |
| `orderTeamFollow(teamName)` | `orderTeam(teamName, "follow", {})` |

Those six are the ones that mirror `Ess.Easy.Followers`' `attack`/`patrol`/`guard`(-as-`defend`)/`follow`
shape one-for-one. `Ess.Easy.Squad` also carries thin pass-throughs for the rest of this page —
`queue(teamName, steps, onComplete)` (a named-callback-only shorthand: use `Ess.Squad.queue` directly for
`onCancel` or per-step timeouts), `cancelQueue(teamName)`, `mountUp(vehGuid, teamName)`,
`dismountAndSecure(teamName, atPos, radius)`, `setFormation(teamName, formationType)`, and
`clearFormation(teamName)` — each just forwarding to its `Ess.Squad`/`Ess.Squad.Tactics` counterpart below
with no added logic.

## `Ess.Squad.on(eventName, fn)`

```lua
Ess.Squad.on = Ess.Followers.on
```

This is a literal alias, not a wrapper — `Ess.Squad.on` **is** `Ess.Followers.on`, forwarding to the exact
same event bus `Ess.Followers.on` publishes to rather than standing up a second one. It's easy to misread
"forwards to the same bus" as "there's a separate Squad bus that relays onto the Followers bus" — that's not
what's happening. There is exactly one listener registry in the whole framework (living in
`66_followers.lua`); `Ess.Squad.on(...)` and `Ess.Followers.on(...)` register a listener on that one registry
interchangeably. A script never needs to know or care which namespace it used to subscribe — an event fired
by Squad and an event fired by Followers land on the same listeners either way.

`"onRecruit"`, `"onDismiss"(guid, wasKilled)`, and `"onFollowerDown"` (a `wasKilled` dismiss, fired alongside
`onDismiss`) are `Ess.Followers`' own events — see [Followers](followers) for those. `Ess.Squad` adds its own
higher-level events on top of the same bus: `"onStepComplete"`/`"onQueueComplete"` (from
[`queue`](#queuetargetgroup-steps-queueopts--cancelqueuetargetgroup)) and `"onVehicleMounted"` (from
[`Tactics.mountUp`](#tactics-mountupvehguid-targetgroup-opts--dismountandsecuretargetgroup-atpos-radius)).

## `queue(targetGroup, steps, queueOpts)` / `cancelQueue(targetGroup)`

An asynchronous multi-step sequence — e.g. enter a vehicle → wait until seated → move to the LZ → wait for
arrival → deploy — for either a team name or a raw guid list:

```lua
Ess.Squad.queue(targetGroup, steps, queueOpts) -> ok
--   targetGroup: a team name (string, resolved via Ess.Squad.team) OR a raw guid list
--   steps:       { {behavior=..., opts={...}, timeout=seconds}, ... }
--                opts is the same shape Ess.AIOrders.command/Ess.Followers.order already take;
--                timeout defaults to 30s per step
--   queueOpts:    { onComplete = fn(), onCancel = fn() }

Ess.Squad.cancelQueue(targetGroup) -> ok
```

`targetGroup` goes through the same `Ess.Squad._resolveGuids` helper `setFormation`/`Tactics` also use: a
string resolves via `Ess.Squad.team` (already live-pruned), anything else is used as a raw guid list directly.
Calling `queue` again for the same `targetGroup` replaces any queue already running for it (same key
derivation `cancelQueue` uses — a team name is keyed by name, a raw guid list by its *sorted* contents, so a
freshly-built table containing the same guids still matches the original) rather than running two queues over
the same guids in parallel.

**Deliberately does not go through `Ess.Followers._orderScoped`.** `queue` is built on
`Ess.Followers._issue` — the raw order-issuing core that `_orderScoped` itself layers marker-tracking and
auto-resume-follow on top of (see [`orderTeam`](#orderteamteamname-behavior-opts) above) — and calls `_issue`
directly for each step instead. This is deliberate, not an oversight: `_orderScoped`'s auto-resume-follow
fires on *any* natural completion, and resuming Follow the instant step 1 finishes would be exactly wrong
mid-sequence — a follower would peel off toward the player instead of starting step 2. `queue` wires its own
step-advancement logic in place of that auto-resume, and only returns the group to Follow at the very end
(via the caller's own `onComplete`, if it asks for that) or on `cancelQueue`.

**Step completion signal, by behavior** — each step reuses whatever completion signal the behavior already
provides, the same set `_orderScoped` itself understands:

| Step behavior | Completion signal |
|---|---|
| `move`, or `patrol` with `opts.loop == false` | `opts.onComplete` — the native per-unit `Callback` fan-in (see [Encounter Toolkit → AIOrders](encounter-toolkit#aiorders)) |
| `attack` (with `opts.target`) | `Ess.On.death(opts.target, ...)` — waits for the *target* to die, not the followers |
| `enter` | Polls `Ess.Object.vehicleOf(guid)` for every guid in the step every 0.5s, advances once **all** are seated in *some* vehicle (a squad might board different seats/vehicles — "seated at all" is the signal, not "seated in the same one") |
| Anything else (`hold`/`defend`/`guard`/a looping `patrol`/`face`/`animate`/`flee`/`deploy`) | No natural completion signal exists — the step just runs until its own timeout |

**Every step also gets a timeout watchdog regardless of which signal it's using** — `step.timeout`, defaulting
to 30 seconds. This isn't a fallback only for behaviors with no natural signal; it applies unconditionally,
racing whichever fires first (natural signal or timeout) to advance the queue, with the other becoming a
no-op once the step has already advanced. **This specifically matters, confirmed live:** a single unit's
`Ai.Goal` call can silently fail to register at all — no handle, no error — a real engine bug also documented
on [Encounter Toolkit → AIOrders](encounter-toolkit#aiorders) (fixed there for `move`/`patrol`'s own
`onComplete` fan-in in this same 0.3.4 release). Without a per-step timeout, that one silently-failed goal
would starve the fan-in counter for its *entire step* and hang the **whole queue** forever — not just fail
that one unit. The watchdog is what turns a single bad `Ai.Goal` call into "this step ran its full timeout and
moved on" instead of "the sequence never finishes."

`cancelQueue(targetGroup)` aborts whatever step is currently running and reverts the group to Follow —
`Ess.Followers._issue(guids, "follow", {})` — its documented safe fallback. A no-op (`false`) if nothing is
currently queued for that `targetGroup`.

Both `"onStepComplete"(guids, stepIndex, behavior)` (fired as each step advances) and
`"onQueueComplete"(guids)` (fired once every step has run) go out on the same event bus described in
[`Ess.Squad.on`](#esssquadoneventname-fn) above — a listener registered via either `Ess.Followers.on` or
`Ess.Squad.on` sees both.

## Tactics: `mountUp(vehGuid, targetGroup, opts)` / `dismountAndSecure(targetGroup, atPos, radius)`

`Ess.Squad.Tactics` is pre-packaged multi-stage vehicle boarding/disembarking, built on
`Ess.Followers._issue` plus Squad's own role bookkeeping — again, no new native calls.

```lua
Ess.Squad.Tactics.mountUp(vehGuid, targetGroup, opts) -> ok
--   opts.passengerRole: role string for non-drivers ("passenger" if omitted, e.g. "gunner" for a turret seat)
--   opts.timeout:       seconds to keep polling for "everyone seated" before giving up (default 20)

Ess.Squad.Tactics.dismountAndSecure(targetGroup, atPos, radius) -> ok
--   radius defaults to 15
```

`mountUp` is **role-aware**: within `targetGroup`, whichever guids have been `assignRole(guid, "driver")`'d
board first, issued an `"enter"` order with `role = "driver"`; everyone else boards as `opts.passengerRole`
(default `"passenger"`). Drivers are issued before everyone else specifically so a driver claims the seat
before a passenger call could otherwise take it. It then polls every 0.5s (the same poll-until-seated idiom
`queue`'s own `"enter"` step uses, just as a one-off here) until every guid in the group is seated in *some*
vehicle. Once everyone's seated, it fires `"onVehicleMounted"(vehGuid, guids)` on the shared event bus. If the
timeout elapses first, it just stops polling — **silently**, with no error and no failure event.

**A blocked or full vehicle is a real, expected outcome here, not something to treat as an error.** `mountUp`
has no way to distinguish "still boarding" from "never going to finish" other than the timeout, so a vehicle
that's out of seats, unreachable, or otherwise can't take the whole group simply times out quietly. Don't read
the absence of `"onVehicleMounted"` as a bug — check for it, or size the group to the vehicle, if a script
needs to know boarding failed.

`dismountAndSecure` disgorges whichever vehicle(s) `targetGroup` is currently riding in and then establishes
a defend perimeter at `atPos` once out:

1. Collects the distinct vehicle guid(s) the group is currently riding in (via `Ess.Object.vehicleOf`,
   deduplicated) and issues `"deploy"` on those vehicle guids — `Ess.AIOrders`' `deploy` behavior targets
   the *vehicle*, not its passengers.
2. **Confirmed live: `Ai.Deploy` only ejects passengers — a vehicle's driver stays seated straight through
   it.** In testing, the vehicle just sat there with its driver still in it after `deploy`. So
   `dismountAndSecure` also explicitly resolves each vehicle's current driver (`Vehicle.GetDriver`) and calls
   `Vehicle.Exit(veh, driver, false)` on them directly — the decompiled corpus's own
   `resident/mrxsupportcopterdelivery.lua` corroborates this exact "make the driver get out" call shape
   (`Vehicle.Exit(uHeli, uDriver, false)`), which is the confirming evidence this wrapper leans on.
3. After a 2-second settle delay (giving `deploy` a moment to actually eject riders before a `defend`/`Anchor`
   goal takes hold on guids still technically mid-exit), it issues `"defend"` at `atPos` with `radius` (default
   15) on the whole group.

## `setFormation(targetGroup, formationType, opts)` / `clearFormation(targetGroup)`

```lua
Ess.Squad.setFormation(targetGroup, formationType, opts) -> ok
--   formationType: "wedge" (default) | "column" | "line" | "diamond"
--   opts: { leader = guid (default the local player), spacing = number (default 3) }

Ess.Squad.clearFormation(targetGroup) -> ok
```

On-foot positional formations for a squad operating independently of the player, recomputed every tick as
`opts.leader` moves. **Be precise about what this is: it's deliberately opt-in and explicitly "visual sugar,"
not a precision tactical system.** Native `Ai.Role("Follow")` holds a single min/max-distance band around one
target point — it has no notion of a per-slot offset. Getting a real per-slot position means abandoning the
Role entirely for a formation member: they're driven instead by the *same* reissued-`MoveTo`-to-an-anchor
loop `Ess.Followers.startFollowLoop` already uses for vehicle escort and on-foot follow-resume (see
[Followers](followers) for that mechanism — this reuses it, it doesn't reimplement it), just with per-slot
offset math in place of that loop's hysteresis band around a moving target.

Each formation slot is computed as a **leader-local** `(right, forward)` offset — positive right is the
leader's right side, positive forward is ahead of the leader — fed through
[`Ess.Math.rotateOffset`](core#essmath) every tick to place it in world space around the leader's current
position and yaw. That's the same right/forward convention the MissionForge sample's own squad-placement grid
uses when it drops a multi-unit squad rotated to the player's facing (see
[MissionForge deep dive → "Squads: one placement, a whole formation"](../deep-dives/mission-forge#squads-one-placement-a-whole-formation)).
The four formation types differ only in how they compute that per-slot `(right, forward)` pair — `column` is
single file straight behind the leader; `line` is a horizontal wall just behind; `diamond` rings every slot
around the leader at even angles; `wedge` (the default) is the familiar V, alternating left/right and growing
behind the leader with each rank.

Each slot's loop also re-pins `Ai.Feeling` toward the leader every tick once it drops below 50 — the same
drift `Ess.Followers.startFollowLoop`'s own header documents (anything off native Follow drifts hostile toward
its target on its own within a few seconds) and fixes the same way. A small hysteresis band (0.75 units)
keeps the loop from reissuing a `MoveTo` goal every half-second once a guid has basically reached its slot.

Before starting a guid's formation-slot loop, `setFormation` first stops any existing vehicle-escort/on-foot
follow-resume loop for that guid (`Ess.Followers._stopFollowLoop`) and releases its Role/leftover Goal state —
otherwise that loop and the new formation loop would fight over the guid's movement every tick.

**Confirmed live:** a 4-unit wedge and a 4-unit diamond both converged on their expected slot positions
relative to the player's facing.

`clearFormation` stops every formation loop for the group, leaving each guid frozen wherever it currently
stands. **It deliberately does not auto-resume Follow** — unlike `cancelQueue`'s own revert-to-Follow
fallback, a formation is typically cleared to hand the group off to a *different* explicit order (an
`orderTeam` call, say), not to send everyone back to following the player. Call `orderTeam(..., "follow", {})`
(or `Ess.Followers.order("follow", ...)`) yourself if that's actually what should happen next.

## See also

- [Ess.Followers](followers) — the roster layer this whole namespace is built on: recruit/dismiss/order,
  markers, auto-resume-follow, and the `_orderScoped`/`_issue` internals `orderTeam`/`queue` reuse directly.
- [Encounter Toolkit → AIOrders](encounter-toolkit#aiorders) — the `Ai.Goal`/`Ai.Anchor`/`Ai.Deploy` layer two
  levels underneath Squad, including the `move`/`patrol` silent-`Ai.Goal`-failure fix `queue`'s own per-step
  timeout watchdog exists to guard against regardless.
- [Core Primitives → Ess.Math](core#essmath) — `rotateOffset`, the leader-local-offset math
  `setFormation` uses for every slot placement.
- [Identity & World Queries → Ess.Player](identity-query#essplayer) — `Ess.Player.character(0)`, the default
  `opts.leader` for `setFormation` when none is given.
- [MissionForge deep dive → "Squads: one placement, a whole formation"](../deep-dives/mission-forge#squads-one-placement-a-whole-formation) —
  the sample tool's own squad-grid placement, sharing the same right/forward-offset-rotated-to-facing
  convention `setFormation` uses per tick instead of at one-shot placement time.
- [Essentials (Ess)](index#the-three-tiers) — "The three tiers," for how `Ess.Easy.Squad` fits alongside the
  Core `Ess.Squad`/`Ess.Squad.Tactics` surface documented here.
