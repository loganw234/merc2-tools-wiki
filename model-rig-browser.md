---
title: Model Rig Browser
parent: Reference
nav_order: 5
---

# Model Rig Browser

An interactive companion to [Reading and Attaching to Any Bone](deep-dives/bone-manipulation): every bone
and hardpoint on every model in the game, browsable and searchable, with a live 2D skeleton view instead
of a flat name list.

**[Open the live tool →](https://mercs2.tools/model_rig_browser.html)**

## What it covers

329 models total — 76 characters, 168 vehicles, 85 weapons — for **16,690 bone/hardpoint slots** across
all of them. Every single one of those slots is addressable from Lua right now (see the deep dive for why:
hardpoints and skeleton bones share one hashed keyspace, and even an uncracked bone resolves through a
synthetic collision handle). What varies per bone is whether its **real name** has been recovered yet:
10,628 of the 16,690 (64%) currently have one; the rest are still only reachable through a synthetic
handle. That's the "some are opaque IDs for now" half of the picture — full coverage for *reaching* a
bone, partial coverage for *knowing what it's actually called*.

The tool classifies every named bone into one of four confidence tiers, color-coded throughout:

| Class | Meaning |
|---|---|
| **Universal** | Present (by that exact name) on essentially every model in its family — the safe bets: `Bone_Head`, `Bone_Chest`, `bone_root`, etc. on characters. |
| **Common** | Present on a meaningful subset of models in its family, not all of them. |
| **Unique** | Specific to one model or a very small handful — a particular vehicle's named turret bone, for instance. |
| **Crossref** | A name recovered on one model that turned out to also resolve correctly on a structurally-unrelated one — evidence the same rigged component (or its hash) is shared/reused across models that don't otherwise look related. |

## Using it

Pick a model on the left (searchable, filterable by Characters/Vehicles/Weapons) to see its full skeleton
projected in 2D — front/side/top or an automatic best-guess view. Solid dots are bones with a confirmed
real name; hollow ring outlines are bones that resolve fine in-game but don't have a cracked name yet.
Click any bone to see its parent/child chain; the right-hand panel lists every still-unknown bone on the
current model and flies the view to it on click. A per-model bar shows what fraction of its own bones are
named (e.g. the Allied Destroyer sits at 57/158 named, even though — per the bone-manipulation deep dive —
all 158 of its bones were confirmed reachable live).

## Where the names come from

Same methodology as the [Hash Lookup](hash-lookup) table: these are string preimages cracked against the
engine's own `pandemic_hash_m2` hash, not something read out of the model files as text (the models don't
store bone names as text at all — only the hash survives). This dataset is the bone/hardpoint-specific
slice of that same cracking effort; the two aren't the same table, but they're produced the same way and
both feed the same class of "hash back to a string" problem [World Inspector](deep-dives/world-inspector)
ran into first.

## Putting a name to use

Once you have a real (or synthetic) bone name from this tool, it works directly with everything
[Reading and Attaching to Any Bone](deep-dives/bone-manipulation) documents — `Object.GetHardpointPosition`
to read its live world position, `Object.Attach`/`Object.SetTransformToObject` to parent something to it.
Nothing else needs to change; the bone name is just a string argument to functions that already exist.
