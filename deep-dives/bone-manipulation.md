---
title: "Reading and Attaching to Any Bone"
parent: Deep Dives
nav_order: 14
---

# Deep Dive: Reading and Attaching to Any Bone

> **Status: confirmed working live.** Every bone on a character *and* on a vehicle is reachable from Lua
> by name: `Object.GetHardpointPosition` returns any bone's live world position, and `Object.Attach`
> parents a spawned object or particle effect to any bone so it follows the skeleton as it animates.
> Confirmed in-engine on the player character (85 of the 89 base human bones), on a spawned Allied
> Destroyer (all 158 bones), and by gluing fire/smoke/flare effects onto hands, fingers, feet, head, and
> back — they track the bones as you move. The one thing this does **not** unlock is the vehicle
> gunning camera; that stays a hard native wall (see [Making the Destroyer Driveable](destroyer-vehicle)).

## The goal

Two capabilities that had never been confirmed from Lua: **read** where any bone on a model is in the
world right now, and **attach** your own object to a specific bone so it rides along. Not just the handful
of declared hardpoints that happen to appear in the decompiled scripts (`hp_seat_lt`, `HP_Truckbed`,
`bone_attach_lhand`), but *any* bone in a model's skeleton — every finger joint, every turret pivot.

## The one insight that makes it work: it's all one hashed keyspace

The engine functions that take a "hardpoint name" — `Object.GetHardpointPosition`, `Object.Attach`,
`Object.SetTransformToObject`, `Camera.SetPosition`/`SetLookAt`, `Vehicle.SetParts` — do **not** look the
string up as text. They hash it (`pandemic_hash_m2`) and match against the model's node hashes. Two
consequences fall out of that, and both are load-bearing here:

1. **Hardpoints and skeleton bones share the same namespace.** A `hp_*` declared hardpoint and a `bone_*`
   skeleton joint resolve through the exact same lookup. The corpus already proves this if you look: the
   same `sHardpoint` argument is fed a declared hardpoint in one place (`Object.GetHardpointPosition(self._vehicle, "hp_seat_lt")`,
   `resident/mrxactionhijack.lua:149`) and a raw skeleton bone in another (`Object.Attach(uActioner, "bone_attach_lhand", uCamera)`,
   `resident/mrxtaskobjectiveverify.lua:284`; `Camera.SetLookAt(uCamera, self._hijacker, "bone_chest")`,
   `resident/mrxactionhijack.lua:916`). So a recovered skeleton bone name is a first-class target for all of
   these functions — not just the declared attach points.

2. **Any string that hashes to a bone's node hash works** — including a synthetic one. If you never
   recovered a bone's real dev name but you *do* have a manufactured string that collides to the same hash,
   the engine can't tell the difference. That means every bone in a model is addressable even where the
   true name was never cracked (more on this below).

Where do the names come from? Bone/hardpoint strings aren't stored in the model as text — only their
hashes are. They're recovered externally by cracking those hashes back to a preimage (see the
[Hash Lookup](../hash-lookup) reference). This page is about what you can *do* once you have them.

## The core API

All of these are on the always-global [`Object`](../namespaces/object) namespace (no `import` needed) and
take a `uGuid` first. Every one below is confirmed at a real call site in the decompiled corpus.

| Function | Signature | What it does |
|---|---|---|
| `GetHardpointPosition` | `x, y, z = Object.GetHardpointPosition(uGuid, sBone)` | World position of a named bone/hardpoint; `nil` if the model has no such node. |
| `Attach` | `bOk, uInst = Object.Attach(uParent, sBone, uChild)` | Parents `uChild` to the named bone on `uParent`; the child then follows the bone. Returns success + an attachment handle. |
| `Detach` | `bOk = Object.Detach(uParent, uInst)` | Undoes an `Attach`, by the handle it returned. |
| `SetTransformToObject` | `Object.SetTransformToObject(uObj, uTarget, sBone)` | Snaps `uObj`'s transform onto the named bone (used right after `Attach` to seat it). |

`Attach`/`Detach` are confirmed together in `resident/mrxactionhijack.lua:363-365` (a VFX ribbon glued to
a bone) and `resident/mrxbriefing.lua:2734-2735` (an actor parented to a hardpoint, then seated with
`SetTransformToObject`).

## Reading: the whole character skeleton is live-readable

The open question going in was that every `GetHardpointPosition` call in the corpus targets a *vehicle* —
whether it reads a *character's* skeleton was unproven. It does. Probing all 89 base human bones against
`Player.GetLocalCharacter()` returned **85 distinct, anatomically-correct world positions** — face bones
~1.7 m up, finger joints ~0.8–1.5 m, feet ~0.2–0.5 m, root at the origin. The 4 misses were exactly the
rare gear bones this particular model doesn't carry (see the percentages below), which is the correct
result, not a failure: the probe distinguishes bones the model *has* from bones it doesn't.

### The base human skeleton (89 bones)

Percentage = share of known human models that carry that bone (100% = every human has it). The core is
universal; the face and gear mounts are near-universal; a few are rare.

```
SPINE / CORE (11)   Bone_Attach_Root 100  Bone_Chest 100  Bone_Head 100  Bone_Hips 100
                    Bone_Spine2 100  GlobalSRT 100  bone_attach_chest 100  bone_neck 100
                    bone_root 100  bone_spine1 100  bone_attach_root_b 32
LEGS (8)            Bone_LFootBone1/2 100  Bone_LShin 100  Bone_LThigh 100
                    Bone_RFootBone1/2 100  Bone_RShin 100  Bone_RThigh 100
ARMS (12)           Bone_LBicep 100  Bone_LForearm 100  Bone_RBicep 100  Bone_RForearm 100
                    bone_attach_lhand 100  bone_attach_rhand 100  bone_lforearmroll 100
                    bone_lhand 100  bone_lshoulder 100  bone_rforearmroll 100  bone_rhand 100  bone_rshoulder 100
HANDS (30)          bone_[l/r][index/middle/pinky/ring/thumb][1/2/3] 100  (all five fingers, both hands, 3 joints each)
FACE (20)           bone_brow_center, bone_cheek_left/right, bone_eyeball_left/right,
                    bone_eyebrow_center/left/right, bone_eyelid_top_left/right, bone_jaw,
                    bone_mouth_bottom_left/right, bone_mouth_corner_left/right, bone_mouth_top_left/right,
                    bone_nose_left/right, bone_tongue_tip   (all 88)
ATTACH (gear) (4)   bone_attach_backleft 89  bone_attach_backright 89  bone_attach_hipleft 88  bone_attach_hipright 88
OTHER (rare) (4)    bone_cc06s7p_left/right 12  bone_amcrr49_left/right 11
```

The `bone_attach_*` points (hands, back, hips) are the game's own "put gear here" mounts and are the
natural first targets for anything cosmetic.

## Every vehicle bone is addressable too — even without the real name

Spawning an Allied Destroyer and probing its full 158-node skeleton resolved **all 158, zero misses**.
That breaks into 57 nodes with a recovered real dev name (the meaningful ones: `bone_yaw_bowgun`,
`bone_pitch_bowgun`, the SAM and CIWS `bone_yaw/pitch/roll_*` turret bones, `hp_seat_cannon`,
`hp_barreltip_cannon`, `hp_ladder_*`, `bone_hatch_*`) and 101 nodes addressed only by a **synthetic
collision handle** — a manufactured string that hashes to the node's hash. Both groups resolved
identically. That's consequence #2 from above, confirmed on a real model: you can read and attach to a
bone you never cracked the true name for, as long as you have any string that collides to its hash.

One caveat worth repeating from the naming work: a few "real" labels are themselves collisions rather than
the true bone name (the destroyer surfaces some `civ_veh_boat_oiltanker_orientation_*` handles, for
instance). They still resolve — the string is a valid alias — but don't read semantic meaning into every
recovered label. The genuinely meaningful reals are the weapon/structure bones.

## Attaching: the recipe

Spawn something, attach it to the bone, seat it. Confirmed live gluing effects to character bones:

```lua
local sBone = "bone_attach_rhand"                 -- right-hand gear mount
local x, y, z = Object.GetHardpointPosition(uChar, sBone)
local uFx = Pg.Spawn("global_particle_firelargesmoke_infinite", x, y, z, 0)   -- fire + smoke, infinite
if uFx then
  Object.Attach(uChar, sBone, uFx)                -- parent it to the bone
  Object.SetTransformToObject(uFx, uChar, sBone)  -- seat it exactly on the bone
end
-- later, to remove:  Object.Detach(uChar, uFx);  Object.Remove(uFx)
```

Particle templates confirmed to spawn and attach this way: `global_particle_firelargesmoke_infinite`
(fire + smoke, persistent), `global_particle_env_smokeplume_distance_tall` (smoke), `_global_flarestick`
(flare). Effects follow the bone through animation — attach fire to `Bone_Head` and both
`bone_attach_back*` and walk around, and it tracks. A flare on all 30 finger joints plus both feet and the
head all attached and tracked simultaneously. In practice almost any spawnable object attaches — physical
props included, though spawned *vehicles* and *characters* attached to a bone behave erratically (their own
physics/AI fights the parent transform), so stick to props and particle effects.

### Gotcha: a freshly spawned model isn't ready for ~0.3 s

If you `Pg.Spawn` the target and immediately read its hardpoints, they come back `nil` — the model's
skeleton hasn't initialized yet. The player character is always ready (it already exists), but a
just-spawned vehicle needs a beat. Either delay ~0.3 s with `Event.Create(Event.TimerRelative, {0.3}, …)`
before reading, or poll `GetHardpointPosition` each tick until it first returns non-`nil`. This was a real
bug: v1 of the destroyer camera test read the barrel bones synchronously at spawn and logged "unresolved,"
when they resolve fine a fraction of a second later.

## Bonus: you can now read a turret's real aim direction

The [destroyer deep dive](destroyer-vehicle) noted that a turret's actual aim direction "isn't
Lua-readable." With the real bones it is — two points on the same gun define its axis. On the Allied
Destroyer's cannon, `hp_seat_cannon` (breech) and `hp_barreltip_cannon` (muzzle) both resolve, and the
vector between them is the barrel line:

```lua
local sx, sy, sz = Object.GetHardpointPosition(uBoat, "hp_seat_cannon")
local mx, my, mz = Object.GetHardpointPosition(uBoat, "hp_barreltip_cannon")
local ax, ay, az = mx - sx, my - sy, mz - sz    -- the barrel's world-space aim vector
```

That's enough to spawn tracers or effects down the real barrel line, or drive any aim-aware logic — even
though, as covered next, you can't point the *camera* down it.

## What this does NOT unlock: the gunning camera

Being able to read the barrel and attach to the turret is not the same as controlling the view while
gunning. That was retested here with the confirmed turret bones and it stays a hard wall. Boarding the
destroyer's cannon seat and running the full camera battery on `Player.GetCamera(player)` —
`SetPosition`/`SetLookAt`/`Hold` *and* the never-before-tried `Shake` (with a known-good preset),
`SetFOV`, `SetYaw`, `SetPitch`, and `Follow` — moved the view **not at all**. Notably, even `Camera.Shake`
did nothing, which points past "position is locked" to "the active gunning camera isn't the object
`Player.GetCamera` hands you." Vehicle gunning-camera control remains in the same no-Lua-touchpoint
category as turret firing itself; see the [destroyer deep dive](destroyer-vehicle) for the full history.
Bone **read** and **attach** are the wins here — the camera is not one of them.

## Quick reference

```lua
-- READ any bone's live world position (nil if the model lacks that node)
local x, y, z = Object.GetHardpointPosition(uGuid, "bone_attach_rhand")

-- ATTACH a spawned object/effect to a bone so it follows the skeleton
local uFx = Pg.Spawn("global_particle_firelargesmoke_infinite", x, y, z, 0)
Object.Attach(uGuid, "bone_attach_rhand", uFx)
Object.SetTransformToObject(uFx, uGuid, "bone_attach_rhand")

-- REMOVE it
Object.Detach(uGuid, uFx)
Object.Remove(uFx)
```

- Character bones are ready immediately; a freshly `Pg.Spawn`'d model's bones need ~0.3 s.
- `hp_*` and `bone_*` names resolve through the same hashed lookup — both are valid targets.
- Wrap engine calls in `pcall` and report failures with `Loader.Printf` (see the [AI Primer](../ai-primer)).
