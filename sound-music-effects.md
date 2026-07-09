---
title: "Sound, Music & Effects"
nav_order: 10
---

# Sound, Music & Effects

A reference sheet of the **named cues** you drop into a mission's audio-visual moments — music tracks, explosion/particle effects, and voice-over lines. Everything here is a plain **string name**: pass it as the relevant field, or type it into the web tool's **`custom…`** box.

These pair with the custom contract framework's support effects (`music` / `vfx` / `vo`) and the raw engine calls the shipped missions use: [`MrxMusic.PlaySpecialMusic`](resident/mrxmusic), [`Airstrike.SpawnDirectedObject`](namespaces/airstrike), and [`MrxVoSequence.Start`](resident/mrxvosequence).

**On this page:** [Music cues](#music-cues) · [Explosions & particles](#explosions--particle-effects) · [Voice-over](#voice-over-lines) · [Audio state](#audio-state-mrxsound) · [Which field takes which](#which-field-takes-which-name)

---

## Music cues

Played with `MrxMusic.PlaySpecialMusic("<cue>")`, stopped with `MrxMusic.StopSpecialMusic()`. In the framework this is the **`music`** support effect: `effect="music", cue="<cue>"` (or `cue="stop"` to return to the normal soundtrack).

### Faction mood loops — `mu_fac_<faction>_<mood>_01`

The bread-and-butter combat/tension music, keyed by faction × mood. **Any mission can use any of these.**

| faction code | who |
|---|---|
| `an` | Allied (used by the Allied missions) |
| `ch` | China |
| `gr` | Guerilla |
| `oc` | OC / Universal Petroleum |
| `pmc` | PMC (you) |

| mood | feel |
|---|---|
| `explore` | calm / ambient |
| `threat` | enemies near, rising tension |
| `kickass` | full combat |
| `win` | victory loop |
| `fail` | defeat |
| `hijack_01` / `_02` / `_03` | vehicle-theft stings |

**Examples:** `mu_fac_ch_kickass_01`, `mu_fac_gr_threat_01`, `mu_fac_oc_explore_01`, `mu_fac_pmc_win_01`, `mu_fac_an_hijack_02`.

### Ambient world music — `mu_nomission_<terrain>_<mood>`

Terrain: `city` / `jungle` / `water` &nbsp;·&nbsp; mood: `explore` / `threat_01` / `threat_02` / `fail`.
e.g. `mu_nomission_jungle_threat_01`, `mu_nomission_water_explore_01`.

### PMC / special

`mu_pmc_panicloop_01` &nbsp;·&nbsp; `mu_pmc_006_01` &nbsp;·&nbsp; `mu_pmc_006_02` &nbsp;·&nbsp; `mu_maintheme` &nbsp;·&nbsp; `mu_shell_01`

### Mission-specific (tied to a shipped mission, but still callable)

`mu_mission_meccon001_01` · `mu_mission_meccon001_02` · `mu_mission_chicon008_01` · `mu_mission_chicon009_01` · `mu_mission_allcon008_01` · `mu_mission_oilcon005_01` · `mu_mission_oilcon021_01` · `mu_mission_pircon001_01` · `mu_mission_pircon002_02` · `mu_mission_pircon002_03` · `mu_mission_pircon003_02` · `mu_mission_pircon004_02` · `mu_mission_pmccon013_01` · `mu_mission_pmccon031_01`..`_02` · `mu_mission_pmccon032_01`..`_02` · `mu_mission_pmccon033_01`..`_02` · `mu_mission_pmccon034_01`..`_02` · `mu_PmcCon016_01`

### Source / HQ music (`mu_src_*`)

The base-game faction-region music system (HQ + op tracks), e.g. `mu_src_al_hq_01`, `mu_src_ch_op_05`, `mu_src_up_op_02_contact`. These are wired through the music-**source** system rather than `PlaySpecialMusic`; listed for completeness.

### The `MrxMusic` API

| function | does |
|---|---|
| `PlaySpecialMusic(cue)` | play a special-music cue over the normal track |
| `StopSpecialMusic()` | stop it, return to normal |
| `PlayFanfare(bWin)` | the win/lose sting (the framework uses this on complete) |
| `EnterContractMusic()` / `EnterFreeplayMusic()` | switch the whole music context |
| `Reset()` | reset the music state |
| `BindMusicCue(...)` / `AddMusicPlaylist(...)` / `ClearMusicPlaylist()` | playlist plumbing |

---

## Explosions & particle effects

Spawned with `Airstrike.SpawnDirectedObject("<particle>", x, y, z, dirX, dirY, dirZ)` — the framework's **`vfx`** support effect: `effect="vfx", particle="<name>", count=N`. **Purely cosmetic (no damage).** Names ending `_infinite` or `_placeable` **persist** (great for a burning wreck / smoke column); the rest are one-shots.

### Airstrike blasts — the biggest bangs

| particle | note |
|---|---|
| `global_particle_airstrike_moab` | huge |
| `global_particle_airstrike_tactnuke` | tactical nuke |
| `global_particle_airstrike_daisycutter` | |
| `global_particle_airstrike_fuelairbomb` | thermobaric |
| `global_particle_airstrike_cruisemissile` | |
| `global_particle_airstrike_carpetbomb_LOD0` | |
| `global_particle_airstrike_clusterbomb` | |
| `global_particle_airstrike_bunkerbuster` | (+ `_flash`, `_initial`) |
| `global_particle_airstrike_smartbomb` | |
| `global_particle_airstrike_missile` | |
| `global_particle_airstrike_artillery` | |
| `global_particle_airstrike_rocket_artillery_LOD0` | |

Ground shockwaves: `global_particle_exp_shockwave_ground_moab` · `_tactnuke` · `_bunkerbuster` · `_lrg` · `_sml` · `_tiny`
Flash: `global_particle_explosion_flash_large` · `global_particle_explosion_flash`

### Generic explosions

`global_particle_explosion` · `_huge` · `_large` · `_medium` · `_small` · `_tiny` · `_huge_oil` · `_medium_oil` · `_c4` · `_rpg` · `_rpg_center` · `_grenade` · `_shockwave_ring` · `_shockwave_sphere`
Also: `global_particle_grenadeexplosion` · `global_particle_gritexplosion` · `global_particle_explosionhuge` / `explosionlarge` / `explosionsmall` / `explosionverysmall` / `explosionoiltower`
Vehicle kills: `global_particle_explosion_vehicle_air` · `_vehicle_ground` · `_vehicle_weakpoint` · `_tankhull` · `_tankhatch` · `_tankturretflame` · `_watertower`

### Fire — persistent (burning wrecks & scenery)

Use an `_infinite` / `_placeable` variant so it keeps burning:
`global_particle_env_firesmokeplume_infinite` · `global_particle_firelargesmoke_infinite_placeable` · `global_particle_firemediumsmoke_infinite_placeable` · `global_particle_firesmall_infinite_placeable` · `global_particle_industrial_fire_infinite` · `global_particle_fireblue_infinite`
Sizes (one-shot + `_infinite` variants exist for each): `global_particle_fire{tiny,small,medium,large}` and `...firesmall/medium/large smoke`

### Smoke columns & signals

`global_particle_env_smokeplume_distance_tall` · `_distance` · `_infinite` · `global_particle_smokeblack` · `_smokeblack_infinite` · `_smokeblackwide` · `global_particle_industrial_smoke_infinite`
Coloured signal smoke: `global_particle_flaresmoke` · `_green` · `_yellow` · `_lightblue` (each with `_infinite`)

### Dirt / dust / debris

`global_particle_dirtexplosion` · `_large` · `_small` · `_fan_large` · `global_particle_dustexplosion` · `global_particle_buildingdebrislarge` · `global_particle_exp_falling_debris_huge` / `_lrg` / `_med`

### Water

`global_particle_explosion_water_large` · `global_particle_splash_huge` / `_lrg` / `_med` / `_sml` / `_dive` · `global_particle_waterfall_bottom` · `global_particle_boatwake` / `boatroostertail`

<details markdown="1">
<summary><strong>Full particle set</strong> — impacts, muzzle flashes, shell casings, ambient, vehicle FX (click to expand)</summary>

**Muzzle flashes:** `global_particle_muzzleflash` · `_25mm` · `_AA` · `_MG` · `_artillery` · `_grenadelauncher` · `_handgun` · `_jet` · `_rpg` · `_shotgun` · `_tank` · `_vulcan` · `_blue`

**Shell casings:** `global_particle_shell` · `_shellAA` · `_shellAA_large` · `_shellgrenade` · `_shellhandgun` · `_shellmg` · `_shellmissile` · `_shellrocket` · `_shellrpg` · `_shellsam` · `_shellshotgun` · `_shellsmall`

**Impacts** (`global_particle_impact_*`): `blood` · `brick` · `concrete` · `dirt` · `glass` · `leaves` · `metal` · `stone` · `water` · `wood` (each with `_nodamage` / `_point` variants); bullet variants `impact_bullet_{blood,brick,dirt,glass,leaves,metal,stone,water,wood}`; slides `impact_slide_{brick,dirt,leaves,stone}`.

**Sparks:** `global_particle_sparkslarge` · `_sparksmedium` · `_exp_sparks_sphere_lrg`

**Vehicle FX:** `global_particle_veh_exhaust_car` · `_veh_exhaust_tank` · `_veh_smoke_{asphalt,brakes,dust,grass,rock}` · `global_particle_rotorwash` · `_rotorwash_water` · `global_particle_dusttrail` · `_duststrike`

**Trees / destruction:** `global_particle_tree_destruction_leaves_green{,_large,_small}{,_fire}` · `global_particle_firetreecanopy{tiny,small,medium,dwarf}` · `global_particle_firetreetrunk{A,B,C,D}`

**Ambient / flotsam:** `global_particle_env_godray_placeable` · `_env_godray2_placeable` · `_env_mist_light_placeable` · `_env_bug_swarm_placeable` · `global_particle_flotsum` (+ `_ash,_birds,_bugs,_dust,_leaves,_papers,_dandy`) · `global_particle_teargas`

**Fountains / water detail:** `global_particle_fountian_{a,b,drops_a,splash_a,sheet_*}` · `global_particle_water_spray_pmc` · `_waterfall_{wall,smoke,bottom_small,bottom_tiny}`

</details>

### Named explosion definitions (`Explosion (…)`)

These are the game's explosion **definitions** (with real damage/force) that ordnance detonates as — a different system from the cosmetic particles above. Handy to know what each strike looks like:

`Explosion (MOAB)` · `(Daisy Cutter)` · `(Fuel Air Bomb)` · `(Cluster Bomb)` · `(Cluster Bomblet)` · `(Carpet bomb)` · `(Cruise Missile)` · `(Bombing Run)` · `(Gunship Shell)` · `(Rocket Artillery)` · `(Tank Shell)` · `(Tank Artillery)` · `(RPG)` · `(RPG Frag)` · `(Grenade)` · `(Grenade Frag)` · `(C4 Primary)` · `(C4 Secondary)` · `(Bunker Buster Stage 1/2)` · `(Strategic Missile)` · `(AT Missile)` · `(AA Detonation)` · `(Surgical Strike)` · `(Smart Bomb)` · `(Small)` · `(Tiny)` · `(Very Small)` · `(Water Mine)` · `(AT Mine)`

### Lights & contrails

Point lights: `Light_explosion_{huge,medium,small,tiny}` · `Light_fire_{huge,large,medium,small,tiny}` · `Light_airstrike_moab_flash` · `Light_airstrike_cruisemissile_flash` · `Light_c4` · `Light_grenade` · `Light_rpg` · `Light_muzzleflash`
Contrails / ribbons: `global_ribbon_plane_contrail` · `global_ribbon_artillery` (+ `_moab`, `_daisy`, `_slow`) · `global_ribbon_RPG` · `Light_contrail`

---

## Voice-over lines

Played with `MrxVoSequence.Start({ "<key>", <gapSeconds>, "<key>", ... })` — the framework's **`vo`** effect: `effect="vo", lines={ "<key>", "<key>" }` (it inserts the gap between lines for you). VO keys are **mission-authored strings**, so you reuse the game's existing ones (there is no way to add new audio without WAD work).

### Key pattern

`<Speaker>-<Context>-<Type>-<Mission><NN>` — e.g. `Fiona-In-Mission-Contract-Chi01-07`, `Misha-None-Freeplay-Support-01`.

### Speakers (by how many lines they have)

**Fiona** (by far the most — your handler) · **Mattias** · **Jennifer** · **Chris** · **OilExec** · **Parrot** · **Eva** · **Ewan** · **Misha** · **Blanco** · **Rubin**; generic troops **`AlliedSoldier`** · **`ChinaSoldier`** · **`VZSoldier`** · **`PirThug`** · **`OCMerc`**.

### Most reusable (generic freeplay support chatter — not tied to a story mission)

- `Misha-None-Freeplay-Support-01` … `-20` — support-call chatter
- `Ewan-None-Freeplay-Support-10` · `-28` · `-38` · `-73` · `-89` · `-90` · `-91` · `-99`
- `Fiona-None-Freeplay-None-01` · `-02` · `-07` · `-08` · `-12` · `-14` · `-15`

Any `<Speaker>-In-Mission-Contract-<Mission><NN>` line also works if you don't mind mission-specific dialogue.

---

## Audio state ([`MrxSound`](resident/mrxsound))

Not individual sounds — these switch the whole audio **mood/mix**. Call the matching Begin/End (or Enter/Exit) pair around a moment:

| pair | effect |
|---|---|
| `BeginSurvivalMode()` / `EndSurvivalMode()` | tense "last-stand" mix (great around a `survive` objective) |
| `EnterCinematicState()` / `ExitCinematicState()` | cinematic mix (muffles gameplay audio) |
| `BeginActionHijack()` / `EndActionHijack()` | hijack-sequence audio |
| `BeginTransit()` / `EndTransit()` | vehicle-transit audio |

---

## Which field takes which name

| Framework support field | Names come from |
|---|---|
| `music` → `cue` | **Music cues** (this page) |
| `vfx` → `particle` | **Particle effects** (this page) |
| `vo` → `lines` | **Voice-over lines** (this page) |
| `artillery` / `bombingrun` → `ammo` | ordnance templates (see the Spawn Reference / [Hash Lookup]) |
| `flyby` / `bombingrun` → `vehicle` | `Support Vehicle (…)` aircraft (see [Hash Lookup]) |

Names not listed here can still be used — every field in the web tool has a **`custom…`** option, and any string from the [Hash Lookup] master table is fair game.

[Hash Lookup]: hash-lookup
