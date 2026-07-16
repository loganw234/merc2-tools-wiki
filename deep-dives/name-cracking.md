---
title: "Cracking the Bone-Name Hashes"
parent: Deep Dives
nav_order: 16
---

# Deep Dive: Cracking the Bone-Name Hashes

> **Status: method proven, results delivered and cross-validated.** This is the story of where the bone and
> hardpoint *names* on the rest of the wiki actually came from. It starts with an in-game Lua probe brute-forcing
> strings against a Transport Truck parked in the PMC HQ overnight, and ends with a pair of GPUs solving the last
> character of a hash algebraically at ~17 trillion candidates a second. Along the way: the exact hash function,
> the single piece of math that caps the whole problem, three collision blunders that had to be caught and undone,
> and the hard wall that a large chunk of the names sit permanently behind. Final tally — of the ~10,199 distinct
> bone/hardpoint hashes, **~47.5% now carry a real or best-effort name** (the game's own dev shipped **6%**), and
> **100% are addressable** through either a real name or a synthetic hash-matching handle. If you just want to
> *use* the names, read [Reading and Attaching to Any Bone](bone-manipulation) instead — this page is how they were
> recovered.

## The problem: a model stores hashes, not names

A Mercenaries 2 model doesn't carry its bone names as text. Each skeleton node is stored as a 32-bit hash, and
every engine function that takes a "hardpoint name" — `Object.GetHardpointPosition`, `Object.Attach`,
`Vehicle.SetParts`, `Camera.SetLookAt` — hashes the string you pass and matches it against those node hashes (the
[bone-manipulation dive](bone-manipulation) documents that lookup in detail). So to address a bone by name you first
have to *have* the name, and the name isn't in the file. It has to be recovered from the outside by inverting the
hash — finding a string that hashes to the node's value. That inversion is what this whole effort is.

Two facts about the hash make this both possible and frustrating, and both were discovered the same night:

1. **It's a plain 32-bit hash, so preimages exist and are findable.** You can brute-force strings and check.
2. **It's a plain 32-bit hash, so preimages are not unique.** Roughly 2³² strings of a given shape all collide into
   the same 32-bit space. Most strings that hash to a node's value are *not* the dev's authored name — they're
   coincidences. Separating the one real name from its ocean of collisions is the entire difficulty, and for a
   large fraction of the names it turns out to be impossible.

## Genesis: the overnight probe against a truck in the HQ

The effort didn't start on a GPU. It started as an OnKey Lua script running *inside the game*.

The setup was deliberately dumb: spawn (or walk up to) a **Transport Truck** sitting in the PMC HQ, then have a Lua
script march an odometer through candidate strings — `a`, `b`, … `aa`, `ab`, … — hashing nothing itself, just
handing each candidate to `Object.GetHardpointPosition(truck, candidate)` and logging any call that came back with a
real world position instead of `nil`. Batched and streamed, in-engine Lua managed roughly a couple hundred thousand
candidates a second. It ran overnight and logged **262 hits** before the game was closed and the log archived.

262 "hits" against one truck is, on its face, almost nothing. But the probe wasn't really there to enumerate a
truck's hardpoints — it was there to answer one structural question, and it answered it decisively:

**The engine never compares your string as text. It hashes it and matches the hash.** That's why junk strings kept
"resolving" — a meaningless candidate that happens to hash to the same 32-bit value as a real node returns that
node's position, indistinguishable from the real name. Two consequences fell straight out of that observation, and
both shaped everything after:

- **The names are recoverable offline.** If the lookup is "hash the string, compare 32 bits," then the names can be
  cracked away from the game entirely — no need to keep a truck loaded and poll a Lua function. You just need the
  hash function and the list of target hashes.
- **A collision is a usable handle.** Because the engine can't tell a real name from a colliding junk string, *any*
  string that hashes to a node is a valid alias for it. Even a bone whose real name is never recovered stays fully
  addressable, as long as you can manufacture *some* string that collides to its hash. (This is the property the
  [bone-manipulation dive](bone-manipulation) leans on to reach all 158 destroyer bones when only 57 have real
  names.)

The probe also proved its own obsolescence. A couple hundred thousand candidates a second, tying up the whole game
to do it, is hopeless against a 32-bit keyspace — you'd be there for millennia, and you can only probe one loaded
model at a time. The obvious move was to take the hash out of the engine and run it somewhere fast.

## Step one off the console: recovering `pandemic_hash_m2`

To crack the hashes offline you need a byte-exact copy of the hash function. The source column names in the game's
own data label it `pandemic_hash_m2`, and it turns out to be **FNV-1a, 32-bit, with two twists**:

```
h = 0x811C9DC5                            # FNV offset basis
for each byte b of the name:
    h = (h XOR (b | 0x20)) * 0x01000193   (mod 2^32)   # twist 1: OR 0x20 on every byte
h = (h XOR 0x2A) * 0x01000193             (mod 2^32)   # twist 2: the "m2" finalize
```

- **Twist 1 — `| 0x20` on every byte — makes the hash case-insensitive.** `'A'` (0x41) and `'a'` (0x61) differ only
  in bit 5, so OR-ing 0x20 folds them together; `bone_chest` and `BONE_CHEST` hash identically. (A side effect worth
  knowing: any two characters differing only in bit 5 become aliases — `[` folds onto `{`, `\` onto `|` — so those
  never need to be in the search alphabet separately.)
- **Twist 2 — the extra `XOR 0x2A` then multiply at the end — is the "m2" finalize** that distinguishes this from a
  textbook FNV-1a.

The working alphabet is **`a-z 0-9 _ .`** — 38 characters. The dot is not decoration: Mercenaries 2's
total-destructibility system names destruction fragments with dotted paths like `floor01.piece1a_propattach11_ruin`,
and a search alphabet without `.` structurally cannot find them. (Missing that dot cost real recoveries for a
while — see [The dot we were missing](#the-dot-we-were-missing) below.)

The reference implementation lives in one file (`fnv.py`) as both a scalar Python function and the CUDA-C source
string the GPU kernels compile — one source of truth, so the GPU can never silently disagree with the CPU. Every
kernel built later is validated byte-exact against it before it's trusted.

## Onto the GPU

From there it was a straight climb in throughput:

- **Lua in-engine:** ~2×10⁵ candidates/s.
- **CPU, NumPy-vectorized:** ~150× the Lua probe.
- **GPU, CuPy `RawKernel`:** the naive kernel hit **~7×10⁹ candidates/s combined** across the two cards in this
  machine — an **RTX 4070** (Ada, sm_89) and an **RTX 5060 Ti** (Blackwell, sm_120). That's roughly **35,000× the
  in-game probe.**

Worth a note for anyone reproducing it: there's no CUDA toolkit or `nvcc` on this box. CuPy's `cupy-cuda12x` bundles
NVRTC, which compiles the kernel source for both architectures at runtime; Numba's CUDA path, by contrast, needs a
toolkit it can't find and won't run. The multi-GPU code has to allocate every device array inside
`with cp.cuda.Device(d)` and launch on that device's default stream — an early bug where a non-blocking stream raced
the target-set upload produced silent zero-hit runs that took a full validation pass to track down.

But raw speed, it turned out, was never going to be the thing that mattered.

## The one piece of math that shapes the entire problem

Here is the number the whole project orbits around:

> **precision = keyspace / 2³² = the expected number of coincidental collisions per target bone.**

If your search enumerates a keyspace of *K* candidate strings against the ~10,000 target hashes, then for any one
target you expect about *K*/2³² of your candidates to hash to it *by chance*. Push *K* past 2³² ≈ 4.3 billion and
every target is buried under more than one collision on average; the real name, if it's even in your keyspace, is no
longer distinguishable from the noise. **You cannot out-brute a 32-bit hash.** A faster GPU doesn't fix this — it
just reaches the noise floor sooner.

Each unknown character you wildcard multiplies the keyspace by 38. So a blind 8-character brute (38⁸ ≈ 4×10¹²) is
~1000× past the collision floor — pure noise. But a *known* character costs nothing: if you already know a name
starts `hp_fx_` and ends `_a`, you're only searching the middle. Fix the prefix and suffix and a 15-character name
becomes a 5-character search, comfortably *below* the floor.

That reframes the whole effort away from "search deeper" and toward **"search a smarter, smaller space."** The
budget isn't GPU-hours spent on one deep wildcard; it's *breadth* — assembling many well-scaffolded candidate
templates, each shallow enough to stay under the collision floor. Almost everything that worked is an application of
this principle.

## The easy wins: conventions

A large share of the names follow human conventions, and conventions are cheap to enumerate.

- **The biped rig.** Characters share one skeleton — the *same hashes* appear on every human model — so it only has
  to be solved once. The convention is regular: `bone_<side><part>`, `bone_<side><finger><1-3>` for the 30 finger
  joints, `bone_<feature>_<vpos>_<side>` for the face. Hashing that grammar recovered the whole standard skeleton;
  the [89-bone base set](bone-manipulation#the-base-human-skeleton-89-bones) is the result.
- **The vehicle rig.** `wheel / hub / axle / suspension / shock / strut / brake / door / hatch / piston / exhaust /
  steering / propeller / rudder / seat / barreltip / …` crossed with positions `fl / fr / rl / rr / ml / mr / …`.
- **Mirror pairs.** A left/right pair's two names differ only by the side marker, and their bones sit at mirrored
  world positions (x ↔ −x, same y/z). One overnight autonomous run leaned entirely on this and produced **269 new
  high-confidence names**, 93 of them near-certain L/R pairs proven by mirrored geometry alone —
  `bone_axle/shock/strut/brake_fl/fr/rl/rr`, `bone_door/rudder/propeller_l/r`, `hp_antenna/barreltip/dock_l/r`.
- **Family completion.** A trailing number is a family marker; one hit like `hp_fx_light1` implies the run, and you
  complete `hp_fx_light2..N` by enumeration.

The first offline catalog, before any of the clever stuff, recovered 21 real dev names *exactly* — `Bone_Head`,
`Bone_Spine2`, `HP_INT_A`, `Hp_starter`, `HP_Truckbed` — which was the "it actually works" moment that justified the
rest.

## Collisions, and the corroboration principle

Conventions get you the parts a human named by hand. The hard majority is everything else, and the enemy there is
always the same: **the hash gives you zero information for choosing the real preimage out of its collisions.** A
single hit proves nothing.

The escape is to require *multiple, independent* hash constraints to agree — because while a single 32-bit collision
is common, two independent ones agreeing is astronomically rare:

- **A mirror pair.** If a shared part `X` has to satisfy `m2("bone_l"+X) == Lhash` *and* `m2("bone_r"+X) == Rhash`,
  a coincidence has to hit two independent targets at once — probability ~ (T/2³²)², around 10⁻⁹. Even an *opaque*
  shared part is uniquely pinned this way.
- **A ≥3-consecutive family.** Three consecutive indices of one stem all hitting real bones is ~ (T/2³²)³ — call it
  10⁻¹⁹. Real dev sequences are consecutive; chance ones scatter.
- **A joint id.** If two different rig words share one id on one model — `bone_pitch_<X>` *and* `bone_yaw_<X>` both
  resolve — then `X` satisfies two independent 32-bit constraints from two different prefix states: a ~64-bit lock.
  This is what cracked opaque weapon-system ids that no dictionary could touch — the destroyer's CIWS array
  (`ciwsfl/fm/fr/rl/rr` × `pitch/roll/yaw/seat`), turret and sensor gimbals, the AC-130's `maingun/minigun/sidegun`.

This principle — **constrain the target set, constrain the candidate space, and demand corroboration** — is the one
durable lesson of the whole project. It's also what three separate wrong turns violated.

### Three collisions we had to catch and undo

The wiki's deep dives are supposed to include the dead ends, and this project had instructive ones — each a case of
trusting a hit that corroboration would have rejected. All three were caught in live review.

- **Circular mining.** An early tool "recovered" 538 wheel-child names by harvesting recurring opaque *stems* and
  enumerating indices off them. The stems, though, had been mined from strings that *already hashed to wheel
  children* — the sweep's own collision artifacts plus the dev's 733k real game strings. A real game string plus a
  brute-forced index is a perfectly valid preimage but is **not the authored bone name**; enumerating it just
  manufactures more collisions. The "538 can't be chance" statistic was wrong because the draws weren't independent.
  Reverted.
- **"64-bit" that was really 32-bit.** The dual-constraint L/R solver was first justified as a 64-bit lock. It isn't:
  for `bone_ + W + _l/_r` both sides share the intermediate state after `bone_+W`, and the suffix fold is
  invertible, so the two constraints collapse to a *single* 32-bit collision on that shared state. At depth that
  produces ~21 colliding `W` per pair, mostly junk. The fix was to stop trusting a lone pair and require the whole
  numbered *family* to corroborate.
- **The coherence quarantine.** Because one hash maps to one authored string reused across every model that has that
  part, a candidate's implied asset-type must match the models the hash actually lives on. An audit of an
  already-shipped 4,271-name deliverable found **570+ names that failed this** — a `village_bld_*` string sitting on
  a tank bone, a character id (`vz_hum_blanco_v6r12`) landing on HQ-interior fan bones. They hashed correctly and
  were still wrong. Quarantined, and the check baked in as a permanent second anti-collision layer.

### The dot we were missing

For a long stretch the search alphabet was `a-z 0-9 _` — no dot — and a whole class of names was therefore
*structurally* unreachable: the destruction fragments named `floor01.piece1a_propattach11_ruin`, with a literal `.`
and a `_ruin`/`_pristine` state suffix. Adding `.` to the alphabet and anchoring on the destruction grammar (only
accepting a variant when a sibling of that exact piece is already known — collision-proof) recovered **~160 more**
building fragments, including a `_lod`/`_lod0..2` level-of-detail axis nobody had noticed.

## The CUDA ladder — and the trick at the top of it

Throughput never solved the collision problem, but it did decide *how much* corroboration-gated space you could
sweep in a sitting, so the kernel got optimized hard. The ladder, each rung a specific lesson:

1. **`GpuCracker` — global bitmap (~3.7 G/s, memory-bound).** Targets in a 512 MB bitmap in global memory. Correct,
   but the per-candidate membership test thrashes memory. The lesson: this kernel was never compute-bound, so
   "optimize the hash" was optimizing the wrong thing.
2. **`FastWild` — on-chip targets (~1.9×).** Put the sorted target set in shared memory and binary-search it on-chip
   with a persistent grid-stride loop. The real win was on-chip membership, not a faster hash.
3. **`FastOdo` — odometer + prefilter (~190 G/s combined).** The optimized true-brute: each thread walks a
   *contiguous* range of the wild digits with a **rolling FNV state stack** (recompute only from the digit that
   changed) instead of re-hashing every candidate; an **inner-digit unroll** amortizes the prefix hash over all 38
   last-character values; and a **shared-memory bitmap prefilter** rejects ~97% of candidates with one on-chip bit
   test, so only survivors pay the (L2-cached) confirm. Measured dead ends worth *not* repeating: a bloom prefilter
   (its extra multiplies cost more than the confirms it saved) and putting the full sorted targets in shared for the
   confirm (it collapsed occupancy). The winning shape was the cheap bitmap plus a rare global confirm.
4. **`BruteSolve` — the last character is *solved*, not searched (~15–17 T/s per card).** This is the crown jewel,
   and it comes straight out of the hash's structure. The finalize multiply is by an odd constant, so it's
   **invertible mod 2³²**. Precompute the inverse once and you can run the finalize *backwards* from the target:

   ```
   PINV = 0x359C449B                          # 0x01000193^-1 mod 2^32
   NEED = ((target * PINV) XOR 0x2A) * PINV    # per target, computed once

   # given the running hash state S after every character but the last:
   want = S XOR NEED                           # one XOR
   # if `want` is a valid alphabet byte, it is the ONLY last character that
   # completes the string to `target`; if it isn't, this prefix has no hit.
   ```

   The inner 38-way loop over the last character — the hottest loop in any brute — collapses to **one XOR and a
   128-entry table lookup**, and the last character is effectively free. That single algebraic move took the
   single-target rate from 543 G/s (a stripped compare-only kernel) to **17.3 T/s on the Blackwell card and 15.0
   T/s on the Ada card** — about a 30× jump, and enough that every string up to 10 characters for a given target is
   exhausted in ~7 minutes. Because the two cards differ in speed, each one runs its *own* full target end-to-end
   rather than sharding one hash between them, so the fast card never waits on the slow one.
5. **`HyperGen` — the solve, multi-target (~1.2M collisions/s combined).** For generating a large *labeled* collision
   corpus at once, the trick is that a candidate can only complete to target *t* when its state and `NEED[t]` share
   their top 25 bits (the solved byte is < 128). Sort the `NEED`s and each candidate does one O(log N) binary search
   instead of N linear checks, so throughput scales ~linearly with target count.

A companion kernel, `LabelWild`, runs the same machinery with the underscore dropped from the alphabet to *mint*
clean `a-z0-9` collision handles on demand — the mechanism behind the synthetic `_gen_` labels every otherwise-blank
bone falls back to.

## The wall: opaque procedural ids

For all that, a large fraction of the bones cannot be recovered by any of this, and it's worth being precise about
why, because it's a property of the data and not a limit of the method.

Many nodes — the sub-bones of every wheel, most gear-mount points, the "universal" interned rigs shared across
vehicles and buildings — were never named by a human at all. They were auto-generated by the modeling/rigging tools
as opaque ids: `att_hwz7k`, `amcrr49`, `cc06s7p`, `vz_chi_job001_c`, `Y7EzN3L7`. These aren't words, they don't
follow a convention, and — critically — a lone one has **no second constraint** to corroborate against. It was
proven unrecoverable every way it could be:

- A 2.1-million-word dictionary sweep: **zero** wheel-child names.
- Every delimiter, every convention scaffold, wildcards to L≤6: only junk, no scaffold beating the chance floor.
- And the decisive one — **the game's own dev, with his own extraction, has a real name for only 1 of 592
  wheel-children, and it's garbage** (`xZIQDWw\VZ` on a stingray wheel). The strings simply aren't in the extracted
  binary; they're procedural or were never exported.

The statistical reason is clean, and it's the same reason the [collision minter](https://mercs2.tools/minter.html)
can't double as a recovery tool: an opaque id is itself a near-random string, so it sits *inside* the distribution of
random collisions. A real word-name stands out from the collision cloud — real ids are ~77% dictionary-coverable and start
with a consonant ~90% of the time, versus ~21% and ~55% for collisions — but an opaque id is indistinguishable from
the noise by any statistic on the string itself. The only thing that can supply these names is the retail string
export, if it ever surfaces; the hash cannot give them back.

That's not a failure so much as a boundary: everything with structure to exploit — descriptive rig words, mirror
pairs, consecutive families, destruction fragments, the joint-id weapon systems — was recovered; everything without
it is addressed by a synthetic handle instead.

## Cross-checking against the other dev

This work ran alongside another developer maintaining an independent `rainbow_table.json` (his own extraction) and,
later, a `bone_census.csv` with structural telemetry we didn't have — per-bone model counts, root/leaf roles, an
`anim_skel` flag, bounding boxes, and the destruction `states`. Two rules governed the interaction, and the first is
absolute: **his files were treated as strictly read-only.** Everything we produced was written to our own
`merged_rainbow.json`; his originals were never touched.

The cross-check was strong external validation. Where both sides had independently named the same bone, they
**agreed on 1,690 of 1,716 (98.5%)**. The 26 disagreements were, on inspection, cases where *our* name was the
collision and his was right — a handful of Tier-A entries that were opaque hash-collisions (`ss_ragdoll_551` was
really `slice1b_propattach02`; `bone_dhm9x5m_left` was really `bone_chestleft`). The census's telemetry also turned
out to be a far stronger anchor than owner-model inference alone, and it drove the highest-yield collision-proof
recovery in the whole project: **model-scoped family completion** (accept a generated variant only when it hashes to
another *unnamed* bone *on the same model*) plus **per-model wildcards on the opaque-id segment** (tiny target set →
low collision, kept only when the id-stem forms a ≥2 cluster). Those two alone added ~1,500 clean names.

## The result

Where it landed, against the game's own dev shipping **578 named bones (6%)**:

- **Of the ~10,199 distinct bone/hardpoint hashes, ~47.5% now carry a real or best-effort name**, and **100% are
  addressable** — every bone has either a recovered name or a synthetic, hash-matching handle, so nothing in any
  skeleton is unreachable.
- Handed back to the other dev: **2,326 names his table lacked**, each with the census columns to verify it.
- Browsed per-model, that's **329 models / 16,690 skeleton slots, ~64% with a real name** (common bones are named
  once and recur across models). The human rig is effectively complete — most individual characters resolve
  100% of their bones.

The deeper takeaway was a reframe of what "recovery" even is. Late in the project it became clear that the
productive lever was never a bigger brute — it was **graph completion**. Given the skeleton's topology and a set of
verified anchors, the blanks are *implied* by structure (a mirror partner, a family index, a shared joint id), and
the hash is only there to *confirm* a guess, never to generate it. That's collision-proof by construction and it
scales with how many anchors you have, which is exactly backwards from brute force. The opaque ids resist it for the
one reason nothing can fix: they have no structure to complete from.

## Using the result

The names this produced are what the rest of the wiki consumes:

- **[Reading and Attaching to Any Bone](bone-manipulation)** — the sequel: what you can *do* once you have the names
  (read any bone's live position, parent effects to it), including the point that a synthetic collision handle works
  just as well as a real name for addressing a bone.
- **[Model Rig Browser](../model-rig-browser)** — every model's skeleton, browsable, with the real-name-vs-synthetic
  status shown per bone.
- **[Hash Lookup](../hash-lookup)** — the name→hash table for spawn/asset templates (the same hash, a different
  dictionary of source strings).
- **[Making the Destroyer Driveable](destroyer-vehicle)** — where the destroyer's 158 bones first came up, and the
  turret-aim vector the [bone dive](bone-manipulation) later closed out with the recovered `hp_seat_cannon` /
  `hp_barreltip_cannon`.

And if you just need a colliding handle for a bone whose real name is one of the unrecoverable opaque ids, you don't
need any of this infrastructure — the last-character solve is small enough to run in a browser. A pure-JavaScript
minter (`minter.html` / `minter.js` in the cracker toolkit) will hand you the shortest colliding string, or one
under a prefix/suffix you choose, in milliseconds — the same algebraic trick from the top of the CUDA ladder, no GPU
required.
