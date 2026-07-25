---
title: "Followers Roster"
parent: Essentials (Ess)
nav_order: 20
---

# Followers Roster

## Overview

`Ess.Followers` (`src/66_followers.lua`, Core; `src/66_followers_easy.lua`, Easy) is a lifecycle-aware
"who's currently assigned to me" roster sitting on top of stateless [`Ess.AIOrders`](encounter-toolkit#aiorders).
Per its own source header, it is built **entirely** on `Ess.AIOrders` (specifically `BEHAVIORS.follow`),
[`Ess.On.death`](reactive-hotkeys), and [`Ess.Mark`](mark) — no new native calls of its own. There is no
`Ess.Raw.Followers`; the native primitives it composes are the same `Ai.Role`/`Ai.Goal`/`Ai.Feeling`/
`Ai.LivingWorld`/`Ai.SetState` calls `Ess.AIOrders`' own Raw tier already exposes.

The gap it closes: `Ess.AIOrders.command` re-passes an explicit guid list on **every** call and remembers
nothing between calls — not who you recruited, and not the `Ai.Feeling`/`Ai.LivingWorld`/`Vip` state
`BEHAVIORS.follow` sets when following starts (its own header admits it never reverts any of that).
`Ess.Followers.recruit`/`.dismiss` run that state sequence **and** track membership; a dead follower prunes
itself automatically via `Ess.On.death`, no polling; and [`.order()`](#orderbehavior-opts--command-the-whole-roster)
is the actual payoff — command the whole current roster, any of `Ess.AIOrders`' 11 behaviors, without
re-threading a guid list through your own script every time.

**New in 0.3.3**, then substantially extended in **0.3.4** — the two releases changed different things, and
this page is careful to say which. See [Status](#status) below for the precise, dated account: some of what
0.3.3 shipped (specifically, how a follower *resumes* Follow) was already superseded within the same source
file by the time 0.3.4 released.

[`Ess.Squad`](squad) — also new in 0.3.4, its own page — layers named teams, roles, a step queue, and
formations on top of this exact roster (reusing `Ess.Followers`' own internal `_orderScoped`/`_issue` seams
rather than duplicating them). This page covers `Ess.Followers`/`Ess.Easy.Followers` only; see
[Ess.Squad — team and role management on top](#esssquad--team-and-role-management-on-top) below for the
pointer.

## Status

Two layers, worth separating the way [Pursuit & Wanted System](pursuit#status) does for its own namespace:

1. **The native layer.** `Ai.Role("Follow")`, `Ai.Feeling`, `Ai.LivingWorld`, `Ai.SetState("Vip")`,
   `Ai.Goal`/`Ai.RemoveGoal` — the primitives underneath everything on this page — are the same ones
   `Ess.AIOrders` already wraps and [Encounter Toolkit's AIOrders section](encounter-toolkit#aiorders)
   documents. That page (and `60_aiorders.lua`'s own header) is the ground truth for those calls; this page
   doesn't re-derive them.
2. **This wrapper's own confirmation.** Unlike `Ess.Pursuit`'s dedicated `control_pursuit` smoke recipe,
   `Ess.Followers` does not yet have a recipe of its own under `samples/recipes/` (checked directly — no file
   there references `Ess.Followers`). Its confirmation instead comes from dated `CONFIRMED LIVE` notes written
   directly into `66_followers.lua`'s own header and function comments, cross-referenced by `CHANGELOG.md`'s
   `[0.3.3]`/`[0.3.4]` `Added`/`Fixed` entries. Neither version's changelog entry carries a separate
   "Verification status" block the way `[0.3.1]` did — the live-test evidence is folded into each bullet
   instead, so that's what this page cites, bullet by bullet, rather than one summary claim.

The dated timeline, because it matters for which behavior is current:

- **2026-07-24** — the pass that produced 0.3.3: the `recruit()` sequence (feeling neutralize → `LivingWorld`
  off → `Ai.SetState("Vip", true)`, with `Vip` confirmed live as the one *missing* piece — without it,
  `Ai.Role` still returns a truthy handle but the unit never follows), the `Ai.RemoveGoal({Handle=0})` fix,
  the `"hi"`-priority-default fix, and natural-completion-only auto-resume-follow.
- **Also 2026-07-24, same pass** — the vehicle-aware-follow work (`orderEnter`, the driver-escort loop,
  `vehicleRoleOf`/`smartFollow`). `CHANGELOG.md`'s own `[0.3.4]` preface says this was "already sitting
  unreleased from the previous pass" — written and live-tested the same day as 0.3.3's own pass, but not
  shipped until 0.3.4.
- **2026-07-25** — a day later, a second and more fundamental finding: the Follow-role-drift bug (see
  [Vehicle-aware follow and the Follow-role-drift fix](#vehicle-aware-follow-and-the-follow-role-drift-fix)
  below), confirmed live side-by-side against an untouched control follower who stayed on native Follow the
  whole time and never drifted. This is the fix that generalized the reissued-`MoveTo` loop from
  "vehicle-driver-escort only" to "every resume, on-foot included" — **superseding** 0.3.4's own first-cut
  vehicle-aware-follow work from the day before, which still left on-foot resume on the native Role unchanged.

Read that last point plainly: if you've seen an earlier description of this namespace saying a resumed
on-foot follower just gets the native `Ai.Role("Follow")` reissued, that was true for a few hours of 0.3.4's
own development and is **not** what ships. The current behavior is in
[Vehicle-aware follow and the Follow-role-drift fix](#vehicle-aware-follow-and-the-follow-role-drift-fix).

## Ess.Followers (Core)

| Function | Signature | Notes |
|---|---|---|
| `recruit` | `Ess.Followers.recruit(guid, opts) -> ok` | See [below](#recruitguid-opts--bring-a-guid-onto-the-roster). Idempotent — recruiting an already-rostered guid is a no-op returning `true`. |
| `dismiss` | `Ess.Followers.dismiss(guid) -> ok` | See [below](#dismissguid-and-dismissall). A guid that was never recruited is a safe no-op returning `false`. |
| `dismissAll` | `Ess.Followers.dismissAll()` | `dismiss()` on every current follower. |
| `list` | `Ess.Followers.list() -> guids` | The current roster, insertion order. Self-healing — see [below](#list-count-and-isfollowerguid). |
| `count` | `Ess.Followers.count() -> n` | `#Ess.Followers.list()`. |
| `isFollower` | `Ess.Followers.isFollower(guid) -> bool` | Plain roster membership check. |
| `order` | `Ess.Followers.order(behavior, opts) -> ok` | See [below](#orderbehavior-opts--command-the-whole-roster). The actual payoff — any of `Ess.AIOrders`' 11 behaviors against the whole roster at once. |
| `on` | `Ess.Followers.on(eventName, fn) -> stop()` | **New in 0.3.4.** See [Ess.Followers.on — the event bus](#essfollowerson--the-event-bus). |
| `setMarkersEnabled` | `Ess.Followers.setMarkersEnabled(bOn)` | See [Markers](#markers-on-by-default). |
| `markersEnabled` | `Ess.Followers.markersEnabled() -> bool` | |

Three more functions are exposed on the `Ess` table but are internal, underscore-prefixed, and not meant to
be called directly by mod code: `_orderScoped(scope, guids, behavior, opts)` (the scoped core `order()`
itself calls with `scope = "__all__"` — `Ess.Squad.orderTeam` reuses it directly to command a subset without
racing `order()`'s own whole-roster calls), `_issue(guids, behavior, opts)` (the raw issuing primitive
`_orderScoped` layers marker-tracking and auto-resume-follow on top of — `Ess.Squad.queue` reuses this
instead, since it needs its own per-step completion signal rather than auto-resume-follow firing mid-sequence),
and `_stopFollowLoop(guid)` (lets `Ess.Squad.Tactics`/formation code cleanly hand a guid's movement off from
one reissued-`MoveTo` loop to another without both fighting for control). They're documented here only so a
reference to them elsewhere on the wiki (chiefly [Ess.Squad](squad)) isn't a dead end.

### `recruit(guid, opts)` — bring a guid onto the roster

`opts` accepts the same `target`/`minDistance`/`maxDistance`/`moveDistance`/`speed` fields
`BEHAVIORS.follow` does (see [Ess.AIOrders](encounter-toolkit#aiorders)), plus two fields specific to
`Ess.Followers` itself: `opts.escortMinDistance`/`opts.escortMaxDistance` — the hold-off distances used only
by the vehicle-driver-escort/on-foot-resume loop described below, distinct from `minDistance`/`maxDistance`,
which the native Follow Role consumes on a fresh `recruit()`. `opts.target` defaults to
`Ess.Player.character(0)`, same default `Ess.AIOrders`' own `follow` behavior uses.

For an **on-foot** guid (unchanged since 0.3.3), `recruit()` runs the confirmed sequence in order — each
step confirmed live to be load-bearing, not decorative:

1. Neutralize a hostile `Ai.Feeling` toward the target.
2. `Ai.LivingWorld(..., "LivingWorldBehaviour", false)` — the unit's ambient background AI otherwise fights
   the Follow role for control.
3. `Ai.SetState(..., "Vip", true)` — confirmed live 2026-07-24 as the one **missing** piece: without it,
   `Ai.Role("Follow")` still returns a truthy handle (looks accepted) but the unit never actually follows.
4. `Ai.Role({Role = "Follow", ...})` itself.

Then it remembers the guid (`roster[key]`, `order_` list), wires `Ess.On.death(guid, function() Ess.Followers.dismiss(guid) end)`
so a dead follower prunes itself with no polling, places a marker if markers are on (see
[Markers](#markers-on-by-default)), and fires the `"onRecruit"` event.

**Vehicle-aware since 0.3.4.** `recruit()` now checks `vehicleRoleOf(guid)` up front. A guid already sitting
in a vehicle at recruit time — real game state, which can be true even right after a fresh Lua-side reload —
used to get the native Follow role applied while seated, which was wrong (confirmed live, same bug class as
the resume-side fix below). Now: a **driver** skips the Follow-role prerequisites entirely (they're specific
to `Ai.Role("Follow")`, which the escort path never uses) and only gets the feeling-neutralize step, then
goes straight to the same escort loop [described below](#vehicle-aware-follow-and-the-follow-role-drift-fix);
a **passenger/gunner** is registered as-is with nothing touched; **on-foot** is the unchanged sequence above.

### `dismiss(guid)` and `dismissAll()`

`dismiss()` reverts exactly what `recruit()`'s sequence set — `Ai.Role` back to `"Idle"`, `LivingWorld` back
on, `Vip` off — stops any active follow loop, clears the guid's marker, and forgets it. It also distinguishes
**why**: `Object.IsAlive(guid)` is checked **before** any teardown happens (checking after would trivially
read `false` regardless of cause), so a death-triggered auto-dismiss (`wasKilled = true`) fires both
`"onFollowerDown"` and `"onDismiss"(guid, true)`, while a manual dismiss on a still-living follower fires only
`"onDismiss"(guid, false)`. `dismissAll()` iterates a snapshot of the roster, not the live table — `dismiss()`
mutates the same list it would be walking, which would otherwise skip entries the same way removing from an
array mid-iteration always does.

### `list()`, `count()`, and `isFollower(guid)`

`list()` is self-healing as of a 0.3.4 fix: confirmed live 2026-07-25, a death-triggered auto-dismiss racing
a manual `dismissAll()` call left the ordered roster list holding guids whose actual roster entry was already
gone — no further `dismiss()` call could clear them, since `dismiss()` only ever removes an entry it can still
find. `list()` now prunes the ordered list in place of any such guid on every read (the same lazy-prune-on-read
idiom `Ess.Squad.team()` uses over this identical roster). `count()` is just `#list()`, so it inherits the
same self-healing for free.

### `order(behavior, opts)` — command the whole roster

Any of `Ess.AIOrders`' 11 behaviors (`move`/`face`/`hold`/`defend`/`attack`/`patrol`/`follow`/`flee`/`enter`/
`deploy`/`animate`) against the entire current roster at once, same `opts` shape
[Ess.AIOrders.command](encounter-toolkit#aiorders) takes — this page doesn't re-document that opts table,
see that page for it. An empty roster is a safe no-op. Internally this is just
`_orderScoped("__all__", Ess.Followers.list(), behavior, opts)`.

Two fixes here are specific to ordering an **already-following** unit onto something else, both confirmed
live 2026-07-24, both applied on every call regardless of behavior:

1. **`Ai.RemoveGoal({Handle = 0})` is issued first**, for every guid in the list — a follower can still be
   mid-goal from a *prior* `order()` call when a new one comes in, and `Force = true` alone didn't reliably
   preempt it. `Handle = 0` is the confirmed "whatever's current" wildcard (matches how the decompiled game
   corpus itself uses it, e.g. `allcon002.lua`).
2. **`opts.priority` defaults to `"hi"` here** — not changed in `Ess.AIOrders.command` itself, whose other
   callers never have a Follow Role to preempt in the first place. The root cause of an intermittent "order
   does nothing" bug during testing turned out to be priority, not timing: `Ess.AIOrders`' own per-behavior
   defaults (attack's `"med"`, for instance) aren't reliably high enough to override a just-released Follow
   Role's leftover state, even with `Force = true` — only `"hi"`/`HiPri` worked consistently.

A non-`"follow"` order also releases the Role (`Ai.Role({Role = "Idle"})`) and then waits **1.5 seconds**
(`Event.TimerRelative`) before actually issuing the new goal — confirmed live that both 0.1s and 0.5s were
unreliable settle time between releasing the Role and the deferred goal actually taking; every manually
reissued order several real seconds later worked, the short deferred ones intermittently didn't.

`order()`'s destination also gets a temporary marker — see [Markers](#markers-on-by-default) — and,
depending on the behavior, automatically resumes Follow once it naturally completes — see
[Vehicle-aware follow and the Follow-role-drift fix](#vehicle-aware-follow-and-the-follow-role-drift-fix),
which is also where auto-resume's own natural-completion rules live.

## Markers (on by default)

`Ess.Followers.setMarkersEnabled(bOn)` / `.markersEnabled()` toggle a module-wide default that starts **on**.
While enabled, every current *and future* follower gets a floating world-space icon over its head
([`Ess.Mark.object`](mark#essmark-core), `world = true`, `radar`/`pda` both off), each in its own color —
picked by stepping the HSL hue wheel by the **golden angle** (137.508°, saturation 0.85, lightness 0.55) so
any number of followers stay evenly spread with no fixed palette to run out of and no two consecutive picks
landing close together. Turning markers on retroactively marks the *current* roster; turning them off clears
every marker this module placed and nothing else's.

`order()`'s own destination — `opts.at` for `move`/`defend`, each point in `opts.points` for `patrol`, or
`opts.target` for `attack` (only when it's an actual object guid, not an unresolved group name) — also gets a
temporary neutral-white ground marker ([`Ess.Mark.zone`](mark#essmark-core) for a point, `Ess.Mark.object`
for an attack target), distinct from any follower's own cycled color. It's cleared the moment a *newer* order
in the same scope supersedes it, or the current one naturally completes — "where did I just tell them to go,"
not just "where are they now." Order-destination marks are tracked per **scope** (`"__all__"` for
`Ess.Followers.order()`'s own whole-roster case, or a team name for `Ess.Squad.orderTeam`), specifically so
one team's in-flight order can't clear or resume-follow another team's still-in-flight one.

## Vehicle-aware follow and the Follow-role-drift fix

This is the section [Status](#status) above points to — it changed twice within the same 0.3.4 release cycle,
and the final shape is meaningfully different from either earlier cut.

**0.3.3 baseline.** Auto-resume-follow fires only on a **natural completion signal**, never on a timer:
`attack` resumes the instant its target dies (`Ess.On.death` on the target); a non-looping `move`/`patrol`
resumes once every follower in the order finishes its route (`onComplete`). `guard`/`hold`/a looping `patrol`
have no natural "done" and stay on that order until you explicitly call `order("follow", opts)` again. In
0.3.3, "resume" meant one thing: reissue the native `Ai.Role("Follow")`, same as `recruit()` itself does.

**0.3.4, first cut (2026-07-24): vehicle awareness.** The native `Ai.Role("Follow")` wants its subject to
board a vehicle *with* the target — reissuing it on a follower currently **driving** their own vehicle (after
[`orderEnter`](#esseasyfollowers), say) made them climb back out to go do that instead, the "gunner runs out
the instant an order finishes" bug this closes. Fix: a `vehicleRoleOf(guid)` check (`Ess.Object.vehicleOf`
plus `Vehicle.GetDriver` — see [Vehicle-entry watch](identity-query#vehicle-entry-watch) for the underlying
call; no separate "who's driving what" tracker needed) dispatches through `smartFollow`:

- **Driver** → a reissued-`MoveTo` escort loop (`startFollowLoop`/`startEscort`) instead of the Role: a
  disposable `TinyGeometry` anchor is repositioned every tick to a stand-off point `minDist` out from the
  target along the driver's current heading, and re-targeted with `Ai.Goal{Goal="MoveTo", Priority="HiPri", Force=true}`.
  Holds **10–20 units off by default** (`minDist`/`maxDist`, overridable via `recruit()`'s own
  `opts.escortMinDistance`/`opts.escortMaxDistance`), with hysteresis — idle once within `minDist`, only
  starts closing again once past `maxDist` — so it doesn't twitch at the boundary. A raw `"MoveToPos"` toward
  the stand-off coordinate was tried first (a vehicle driver was the corpus's one confirmed use of that goal)
  but confirmed live to return `nil` from a bare `Ai.Goal` call anyway; the anchor-plus-`"MoveTo"` trick
  `move`/`defend`/`patrol`/`flee` already use was substituted instead. The loop's own "has the driver left?"
  check is **debounced to 3 consecutive misses**, not a single reading — confirmed live that a single
  transient bad read (e.g. right as another follower was recruited or spawned nearby) was otherwise enough to
  permanently kill a perfectly good loop, since a loop tick returning `false` is treated as final by
  `Ess.Loop`, not "retry me."
- **Passenger/gunner** → left completely alone. They already go wherever the vehicle goes, and touching their
  Role/Goal at all risks ejecting them for nothing.
- **On foot** → in this first cut, the unchanged native Role. (Superseded the next day — see below.)

**0.3.4, second cut (confirmed live 2026-07-25): the Follow-role-drift fix.** A separate, more fundamental bug
surfaced: a follower taken off native `Ai.Role("Follow")` for **any** order — even a plain `move` — had its
`Ai.Feeling` toward the follow target snap back hostile within 1–3 seconds on its own, and reissuing
`Ai.Role("Follow")` afterward returned a valid handle but never actually moved the unit again. Both confirmed
live side-by-side against an untouched follower who stayed on native Follow the whole time and never drifted
at all — proving the native Role itself is what suppresses the drift, not the one-time feeling/LivingWorld/Vip
setup `recruit()` does. Native Follow, it turns out, is reliable **only on its first engagement**, straight
from `recruit()` — left unchanged, it's the one confirmed-good path.

The fix: every **resume** — `order("follow", ...)`, auto-resume-follow, or `Ess.Squad.orderTeam` (a sibling
namespace, not covered on this page) — now routes through the *same* reissued-`MoveTo`-plus-hysteresis loop
the vehicle-driver escort above already used, generalized to on-foot followers too, with a per-tick feeling
re-pin added (re-asserting `Ai.SetFeeling(guid, target, 100)` whenever a read drops below 50, thresholded so
it never fights a caller's own deliberate negative-feeling change toward some *other* guid) to stop the drift
from recurring. This is the change that makes the 0.3.4-first-cut's "on foot is the unchanged Role" line above
stale — on-foot resume no longer touches the Role at all.

**Accepted tradeoff, stated plainly (from the source's own comment):** a *resumed* follower loses native
Follow's own free vehicle-boarding-with-you convenience — the context-action prompt is tied to the Role —
until explicitly [`orderEnter()`](#esseasyfollowers)'d again. A fresh `recruit()` still gets that convenience;
only a guid that has since been taken off Follow for some other order and resumed does not.

## Ess.Followers.on — the event bus

**New in 0.3.4.** `Ess.Followers.on(eventName, fn) -> stop()` is a generic string-keyed pub/sub — the one
piece neither [`Ess.On`](reactive-hotkeys#esson--reactive-world-hooks) (engine-signal-specific: death, area,
health, vehicle, tick, labeled) nor `Ess.Event` (raw engine `Event` handles) provides. Unknown event names are
harmless — they simply never fire, so there's no fixed registry to keep in sync as new events get added
elsewhere. Three fire today:

| Event | Fired as | When |
|---|---|---|
| `"onRecruit"` | `fn(guid)` | Every successful `recruit()`. |
| `"onDismiss"` | `fn(guid, wasKilled)` | Every `dismiss()`, manual or death-triggered — see [dismiss(guid) and dismissAll()](#dismissguid-and-dismissall) for how `wasKilled` is determined. |
| `"onFollowerDown"` | `fn(guid)` | Only when `dismiss()` was itself triggered by the guid's death — fired immediately alongside `"onDismiss"` for that same call, not as a separate later event. |

`Ess.Squad.on(...)` ([Ess.Squad](squad)) forwards to this exact same bus rather than standing up a second one,
so its own higher-level events (`"onStepComplete"`, `"onVehicleMounted"`, …) fire through the identical
mechanism.

## Ess.Easy.Followers

`src/66_followers_easy.lua` — named one-liners over the whole current roster, mirroring
[`Ess.Easy.AIOrders`](encounter-toolkit#aiorders)' own `attack`/`patrol`/`guard` shape but with no `guids`
parameter, since `Ess.Followers` already knows who.

| Function | Signature | Notes |
|---|---|---|
| `recruit` | `Ess.Easy.Followers.recruit(guid) -> ok` | `Ess.Followers.recruit(guid, { target = Ess.Player.character(0) })`. |
| `orderAttack` | `Ess.Easy.Followers.orderAttack(target)` | `order("attack", { target = target })`. |
| `orderPatrol` | `Ess.Easy.Followers.orderPatrol(points)` | `order("patrol", { points = points })`. |
| `orderGuard` | `Ess.Easy.Followers.orderGuard(at)` | `order("defend", { at = at })`. |
| `orderEnter` | `Ess.Easy.Followers.orderEnter(vehicleGuid, role)` | **New in 0.3.4.** `order("enter", { target = vehicleGuid, role = role or "driver" })`. See below. |
| `showMarkers` / `hideMarkers` | `Ess.Easy.Followers.showMarkers()` / `.hideMarkers()` | Named aliases for `setMarkersEnabled(true)`/`(false)`. |

`orderEnter`'s `role` defaults to `"driver"` — deliberately **not** `Ess.AIOrders`' own `"passenger"`
default for the underlying `enter` behavior — specifically so a lone follower boards the one seat that keeps
every later order (`move`/`attack`/`guard`/…) still working through the same guid already on the roster.
Confirmed live 2026-07-24: no secondary "who's currently driving which vehicle" tracker is needed for this to
work — a follower who's currently driving *is already* the correct `AIGuid` for a later `order()` to steer the
vehicle through, since `Ess.Raw.AIOrders.actor()`
([Ess.AIOrders Raw tier](encounter-toolkit#aiorders)) already implements the established "target the driver,
not the hull" rule. (Bonus confirmed behavior from the same test: once a subsequent `move` order finished, the
usual auto-resume-follow fired — the follower got back out of the car and returned to following on foot, same
as from any other order.) A follower who enters as a passenger/gunner instead is still recruited and orderable
as themselves, just not "the vehicle."

## Ess.Squad — team and role management on top

[`Ess.Squad`](squad) is also new in 0.3.4 and gets its own page — a full team/role/queue/tactics/formation
layer for scripts managing enough followers that "the whole roster" stops being the right unit of command
(`createTeam`/`assignRole`/`orderTeam`, an async step `queue`, role-aware vehicle `Tactics`, on-foot
`setFormation`). It's built entirely on `Ess.Followers` — specifically the internal `_orderScoped`/`_issue`
seams mentioned in [Ess.Followers (Core)](#essfollowers-core) above — with no new roster and no new native
calls of its own. This page doesn't document `Ess.Squad`'s own functions; see its page for the full API.

## See also

- [Encounter Toolkit — AIOrders](encounter-toolkit#aiorders) — the stateless group-command layer
  `Ess.Followers` is built on: the 11 behaviors, their `opts`, and `Ess.Raw.AIOrders.actor()`'s
  driver-not-hull rule.
- [Markers](mark) — `Ess.Mark.object`/`Ess.Mark.zone`, what this namespace's follower-head icons and
  order-destination markers are built from.
- [Reactive Hooks & Hotkeys](reactive-hotkeys) — `Ess.On.death`, the hook `recruit()` wires for automatic
  roster pruning; `Ess.On`/`Ess.Event`, the two things `Ess.Followers.on`'s own event bus deliberately doesn't
  duplicate.
- [Identity & World Query — Vehicle-entry watch](identity-query#vehicle-entry-watch) — `Ess.Object.vehicleOf`,
  the no-separate-tracker-needed call the vehicle-aware follow logic above is built on.
- [Ess.Squad](squad) — team/role/queue/tactics/formation management built on top of this exact roster.
- [Ess.Easy](easy) — the full one-liner catalog, including `Ess.Easy.Followers` above.
- [Essentials (Ess)](index#the-three-tiers) — "The three tiers," for why this namespace has no `Ess.Raw.Followers`.
