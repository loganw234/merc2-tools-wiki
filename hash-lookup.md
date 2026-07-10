---
title: Hash Lookup
parent: Reference
nav_order: 2
---

# Hash Lookup

## Overview

A 6119-entry name-to-hash table, covering (per the source export) every spawnable template plus a large
number of non-spawnable assets (decals, building-HP threshold markers, internal test assets, etc.) -- this
looks to be Pandemic's own internal asset/string hash table for this game ("pandemic_hash_m2" in the
source column names), not a spawn-only list. Provided as a CSV export; the exact tool/process used to
extract it from the game isn't documented here, only what's been cross-checked against this wiki's own
already-confirmed findings below.

**Looking for something more specific than the full table?** [Spawn Reference](spawn-reference/) has
task-focused, pre-filtered slices of this same data — drivable vehicles, the full vehicle set,
confirmed-spawnable weapons, and every real `Pg.Spawn` / `Pg.GetGuidByName` call-site string actually
used by the shipped scripts.

## Why this matters

Throughout this wiki's live-testing notes (see the
[World Inspector deep dive](deep-dives/world-inspector)), `Object.GetLocalizedName(uGuid)` was repeatedly
confirmed to return a hashed key in `[0xXXXXXXXX]` form for objects with no custom display name, with no
way found to resolve that hash back to a real name from anywhere reachable in Lua. The `pandemic_hash_m2_hex`
column below is in exactly that 8-hex-digit format -- this table is very likely the missing piece needed to
resolve those hashes back to literal names.

**Confirmed by direct cross-reference**, not just format matching: several template name strings already
used and confirmed working elsewhere on this wiki appear in this table under their exact expected name --
`Veyron` (the [Custom Contract deep dive](deep-dives/custom-contract)'s test-mission spawn), `Supply Drop
(Blueprints)` / `Supply Drop (Treasure)` / `Supply Drop (Light MG)` (confirmed real `Pg.Spawn` call sites in
`resident/bountycopter.lua`), and `Chinese Destroyer` (the destroyer spawn built for the World Inspector
follow-up work). That's about as strong a confirmation as static cross-referencing can give without a live
in-game test.

**Confirmed scope limit:** this table only resolves *spawn/asset template* name hashes, not
`Object.GetLocalizedName`'s hashes in general. Three real hashes pulled from a live WAILA session (a
Human/Hero/PMC character, an Allied vehicle, an unfactioned vehicle) were checked against every column of
the source CSV and matched nothing at all, even though the lookup method itself was re-verified against a
known-good hash (`Chinese Destroyer`) in the same pass. `Object.GetLocalizedName` appears to key into a
separate localization-string table -- same hash algorithm, different dictionary of source strings -- that
this export doesn't cover. This table is the right tool for resolving a spawn-template reference (e.g. via
`Object.GetParent`), not for resolving an arbitrary object's display-name hash.

Only `name`, `hash` (`pandemic_hash_m2_hex` -- the 8-hex-digit key format seen in-game as `[0xXXXXXXXX]`),
and `vehicle` (`is_vehicle`) are published in the table below -- the source CSV also has `entry_index`,
`value_hex`, and `aux0_hex` columns (plus a decimal duplicate of the hash and an `aux1_hex` confirmed
identical to the hash column), but none of those have a confirmed use yet, so they're left out of the
page for now. They're still in `spawnable_templates.csv` itself if a future test needs them -- e.g. the
still-untested theory that `value_hex` (mostly `0x8000XXXX`-shaped, matching the address range already
confirmed for `Object.GetParent`'s template reference) might resolve template references directly.

## Table

<div class="hash-lookup-wrap" markdown="0">
<input type="text" id="hashLookupFilter" class="hash-lookup-search"
       placeholder="Filter by name or hash (e.g. 'destroyer' or '0x02DFA76D')..." autocomplete="off">
<div class="hash-lookup-count" id="hashLookupCount"></div>
<div class="hash-lookup-scroll">
<table class="hash-lookup-table" id="hashLookupTable">
<thead>
<tr><th>Name</th><th>Hash</th><th>Vehicle</th></tr>
</thead>
<tbody>
<tr><td>(unnamed)</td><td>0x021F16B2</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0x816F0B0D</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0xA1AD5E94</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0xFEC25D11</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0x699D5606</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0x4C74944F</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0xBD4DC42B</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0x784FCF4D</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0xB224DB15</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0x2AE48660</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0x6420E4F7</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0x928027C1</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0xC6B40476</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0x0ECB978A</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0x1266E814</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0xD8353CA9</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0xEDF510A0</td><td>No</td></tr>
<tr><td>(unnamed)</td><td>0xE19A4391</td><td>No</td></tr>
<tr><td>2 Seat Boat (Passenger)</td><td>0x1F3E12D3</td><td>Yes</td></tr>
<tr><td>2 Seat Car (Driver)</td><td>0xF4DD3619</td><td>No</td></tr>
<tr><td>2 Seat Car (Driver) (Civ)</td><td>0x148B271E</td><td>No</td></tr>
<tr><td>2 Seat Car (Driver) (Escort)</td><td>0x847BC256</td><td>No</td></tr>
<tr><td>2 Seat Car (Driver) (Police)</td><td>0x22DF2620</td><td>No</td></tr>
<tr><td>2 Seat Car (Passenger)</td><td>0x90401807</td><td>No</td></tr>
<tr><td>2 Seat Car (Passenger) (Escort)</td><td>0x76AED190</td><td>No</td></tr>
<tr><td>2 Seat Copter (Driver)</td><td>0xFDEF813A</td><td>No</td></tr>
<tr><td>2 Seat Copter (Driver) (Allied)</td><td>0x93EC73B4</td><td>No</td></tr>
<tr><td>2 Seat Copter (Driver) (Guerilla)</td><td>0x9083B5FA</td><td>No</td></tr>
<tr><td>2 Seat Copter (Driver) (OC)</td><td>0x8CF39D8D</td><td>No</td></tr>
<tr><td>2 Seat Copter (Driver) (VZ)</td><td>0x1255524F</td><td>No</td></tr>
<tr><td>2 Seat Copter (Gunner)</td><td>0x92D3A017</td><td>No</td></tr>
<tr><td>3 Seat Car (Driver)</td><td>0x2A00E898</td><td>No</td></tr>
<tr><td>3 Seat Car (Driver) (Guerilla)</td><td>0xE3E5DD4C</td><td>No</td></tr>
<tr><td>3 Seat Car (Gunner RightFront)</td><td>0xEAF6A00C</td><td>No</td></tr>
<tr><td>3 Seat Car (Gunner)</td><td>0x635DDFC9</td><td>No</td></tr>
<tr><td>3 Seat Car (Passenger)</td><td>0xABE6688C</td><td>No</td></tr>
<tr><td>3ddecal_asphalt</td><td>0x29D0BDCB</td><td>No</td></tr>
<tr><td>3ddecal_brick</td><td>0xE893B9B5</td><td>No</td></tr>
<tr><td>3ddecal_concrete_warm</td><td>0x3F637E01</td><td>No</td></tr>
<tr><td>3ddecal_dirt</td><td>0x7FFDAC69</td><td>No</td></tr>
<tr><td>3ddecal_metal</td><td>0xDCC30213</td><td>No</td></tr>
<tr><td>3ddecal_rock</td><td>0x2926BC49</td><td>No</td></tr>
<tr><td>3ddecal_tile</td><td>0x0E8C523A</td><td>No</td></tr>
<tr><td>3ddecal_wood</td><td>0xFBE4EEED</td><td>No</td></tr>
<tr><td>68Valiant_Ruin</td><td>0x21C43ED9</td><td>No</td></tr>
<tr><td>68Valiant_Ruin_fire</td><td>0x092DB194</td><td>No</td></tr>
<tr><td>__AssetTest</td><td>0x5615C3ED</td><td>No</td></tr>
<tr><td>__Building HP 025</td><td>0x45840CE6</td><td>No</td></tr>
<tr><td>__Building HP 050</td><td>0x4B4189E6</td><td>No</td></tr>
<tr><td>__Building HP 100</td><td>0x4E1DE140</td><td>No</td></tr>
<tr><td>__Building HP 150</td><td>0x1800E0A7</td><td>No</td></tr>
<tr><td>__Building HP 200</td><td>0xDAC80B8F</td><td>No</td></tr>
<tr><td>__Building HP 300</td><td>0xC867FCFA</td><td>No</td></tr>
<tr><td>__Building HP 400</td><td>0x851272D9</td><td>No</td></tr>
<tr><td>__Building HP 500</td><td>0x2A43B31C</td><td>No</td></tr>
<tr><td>__Building HP 600</td><td>0x1393EC5B</td><td>No</td></tr>
<tr><td>__Building HP 800</td><td>0xE049F895</td><td>No</td></tr>
<tr><td>__Building Shack</td><td>0xC33DD16B</td><td>No</td></tr>
<tr><td>__Building Skyscraper Large</td><td>0x51F35E97</td><td>No</td></tr>
<tr><td>__Building Skyscraper Medium</td><td>0x5537A857</td><td>No</td></tr>
<tr><td>__Building Skyscraper Small</td><td>0x8CC6E63F</td><td>No</td></tr>
<tr><td>__Building Tough</td><td>0xE62D4C82</td><td>No</td></tr>
<tr><td>__global_env_palmtree01</td><td>0x5536E844</td><td>No</td></tr>
<tr><td>__global_env_palmtreebend02</td><td>0x3F5DB976</td><td>No</td></tr>
<tr><td>__global_env_palmtreebend03</td><td>0x215FC8D3</td><td>No</td></tr>
<tr><td>__global_env_palmtreebend04</td><td>0x1F6C91A0</td><td>No</td></tr>
<tr><td>__global_env_palmtreebend05</td><td>0x496F1255</td><td>No</td></tr>
<tr><td>__global_env_palmtreeplanted01</td><td>0x80ED4DAA</td><td>No</td></tr>
<tr><td>__global_env_tree01</td><td>0xF0486D5C</td><td>No</td></tr>
<tr><td>__global_env_treeoak01</td><td>0xF26BBA79</td><td>No</td></tr>
<tr><td>__global_env_treeplaza01</td><td>0xF394CA7C</td><td>No</td></tr>
<tr><td>__global_env_treeplaza02</td><td>0xCD925013</td><td>No</td></tr>
<tr><td>__global_env_treeplaza03</td><td>0xEB9040B6</td><td>No</td></tr>
<tr><td>__global_env_treesidewalk01</td><td>0xA914401E</td><td>No</td></tr>
<tr><td>__global_env_treespade</td><td>0xAA0976CC</td><td>No</td></tr>
<tr><td>__global_env_treetropical01</td><td>0xEA7668B0</td><td>No</td></tr>
<tr><td>__global_env_treetropical02</td><td>0xD4740777</td><td>No</td></tr>
<tr><td>__jungle_env_largecanopy01</td><td>0x6694CAC1</td><td>No</td></tr>
<tr><td>__jungle_env_smallcanopy01</td><td>0xC65D6C1D</td><td>No</td></tr>
<tr><td>__jungle_env_smallcanopy02</td><td>0x4455E3B2</td><td>No</td></tr>
<tr><td>__jungle_env_treemedium01</td><td>0x7E251DAB</td><td>No</td></tr>
<tr><td>__jungle_env_treemedium03</td><td>0xFE2A6459</td><td>No</td></tr>
<tr><td>__jungle_env_treesmall01</td><td>0xBA098E81</td><td>No</td></tr>
<tr><td>__jungle_env_treesmall02</td><td>0x38020616</td><td>No</td></tr>
<tr><td>__jungle_env_treesmall03</td><td>0x9A04DEF3</td><td>No</td></tr>
<tr><td>__jungle_env_treetall01</td><td>0xC0E0D8A3</td><td>No</td></tr>
<tr><td>__jungle_env_treetall02</td><td>0xA6E2EE4C</td><td>No</td></tr>
<tr><td>__jungle_env_treetall03</td><td>0x20E5ECF1</td><td>No</td></tr>
<tr><td>__marsh_env_treewater02</td><td>0xB8F49502</td><td>No</td></tr>
<tr><td>__placeable Environment Bush Plant</td><td>0x8F197374</td><td>No</td></tr>
<tr><td>__placeable Environment Tree</td><td>0x988DDE4D</td><td>No</td></tr>
<tr><td>__shanty_env_tree01</td><td>0x11441BFC</td><td>No</td></tr>
<tr><td>__shanty_env_tree02</td><td>0xEB41A193</td><td>No</td></tr>
<tr><td>__shanty_env_tree03</td><td>0x093F9236</td><td>No</td></tr>
<tr><td>__Static Destructible (Crashable)</td><td>0xD192FB1F</td><td>No</td></tr>
<tr><td>__Static Destructible (Explosive)</td><td>0x66201E9B</td><td>No</td></tr>
<tr><td>__Static Destructible (Sandbag)</td><td>0x357D5850</td><td>No</td></tr>
<tr><td>__Static Destructible (Tower)</td><td>0x5442049D</td><td>No</td></tr>
<tr><td>__Static Destructible HP 025</td><td>0xCBFFD998</td><td>No</td></tr>
<tr><td>__Static Destructible HP 050</td><td>0x15188514</td><td>No</td></tr>
<tr><td>__Static Destructible HP 100</td><td>0xB5B55B0E</td><td>No</td></tr>
<tr><td>__Static Destructible HP 300</td><td>0x4B6B5884</td><td>No</td></tr>
<tr><td>_airport_bld_controltower</td><td>0x5E4C3BFF</td><td>No</td></tr>
<tr><td>_airport_bld_hanger01</td><td>0xEC8EFD29</td><td>No</td></tr>
<tr><td>_airport_bld_terminal01</td><td>0x2E94EDF0</td><td>No</td></tr>
<tr><td>_airport_runway1</td><td>0x677B7E05</td><td>No</td></tr>
<tr><td>_airport_sign</td><td>0x2AF74AC3</td><td>No</td></tr>
<tr><td>_airport_whitestripe1</td><td>0x3A5EF939</td><td>No</td></tr>
<tr><td>_aloutpost_bld_alarmtower</td><td>0x24B533CD</td><td>No</td></tr>
<tr><td>_aloutpost_bld_barracks01</td><td>0x67FDE537</td><td>No</td></tr>
<tr><td>_aloutpost_bld_barracks02</td><td>0x7E004670</td><td>No</td></tr>
<tr><td>_aloutpost_bld_barracks03</td><td>0xE8032BE5</td><td>No</td></tr>
<tr><td>_aloutpost_bld_bunker</td><td>0xEBC079B4</td><td>No</td></tr>
<tr><td>_aloutpost_bld_command</td><td>0xC65DEA56</td><td>No</td></tr>
<tr><td>_aloutpost_bld_garage01</td><td>0x1344DF91</td><td>No</td></tr>
<tr><td>_aloutpost_bld_guardtowershort</td><td>0xC6F6E74D</td><td>No</td></tr>
<tr><td>_aloutpost_bld_guardtowertall</td><td>0xA89C2354</td><td>No</td></tr>
<tr><td>_aloutpost_bld_hangar</td><td>0xADB07296</td><td>No</td></tr>
<tr><td>_aloutpost_bld_hangersmall</td><td>0x85298903</td><td>No</td></tr>
<tr><td>_aloutpost_bld_helipad</td><td>0x4D0BF49A</td><td>Yes</td></tr>
<tr><td>_aloutpost_bld_helipad_roof</td><td>0xE010DB4B</td><td>Yes</td></tr>
<tr><td>_aloutpost_bld_largetent</td><td>0x2EC3CB1B</td><td>No</td></tr>
<tr><td>_aloutpost_bld_largetentextensionA</td><td>0x2BBA049F</td><td>No</td></tr>
<tr><td>_aloutpost_bld_prison</td><td>0x6CDF420A</td><td>No</td></tr>
<tr><td>_aloutpost_bld_prison_fence</td><td>0xA82FD3E0</td><td>No</td></tr>
<tr><td>_aloutpost_bld_storage</td><td>0x9AC533E6</td><td>No</td></tr>
<tr><td>_aloutpost_bld_storage_fence</td><td>0xDC45D2A4</td><td>No</td></tr>
<tr><td>_aloutpost_bld_supplydepot</td><td>0x25330130</td><td>No</td></tr>
<tr><td>_aloutpost_concretewall01</td><td>0xD0A85272</td><td>No</td></tr>
<tr><td>_aloutpost_concretewall02</td><td>0x52AFDADD</td><td>No</td></tr>
<tr><td>_aloutpost_fueltanks</td><td>0xFA4F4AB5</td><td>Yes</td></tr>
<tr><td>_aloutpost_gateentrance</td><td>0xAD110E85</td><td>No</td></tr>
<tr><td>_aloutpost_interior_herochair</td><td>0x7C809884</td><td>No</td></tr>
<tr><td>_aloutpost_interior_job</td><td>0x4C33E8D2</td><td>No</td></tr>
<tr><td>_angelfalls_env_base</td><td>0xAA17FEF9</td><td>No</td></tr>
<tr><td>_angelfalls_env_basecornerupleft</td><td>0xC3B55702</td><td>No</td></tr>
<tr><td>_angelfalls_env_basecornerupright</td><td>0x47D0CE79</td><td>No</td></tr>
<tr><td>_angelfalls_env_canyonside</td><td>0x665452E3</td><td>No</td></tr>
<tr><td>_angelfalls_env_middle</td><td>0x65F6EFF9</td><td>No</td></tr>
<tr><td>_angelfalls_env_middlecornerdownleft</td><td>0x0894CF99</td><td>No</td></tr>
<tr><td>_angelfalls_env_middlecornerdownright</td><td>0xE09BE800</td><td>No</td></tr>
<tr><td>_angelfalls_env_middlecornerupleft</td><td>0x0ED17802</td><td>No</td></tr>
<tr><td>_angelfalls_env_middlecornerupright</td><td>0x8518C179</td><td>No</td></tr>
<tr><td>_angelfalls_env_top</td><td>0xF3BE17CF</td><td>No</td></tr>
<tr><td>_angelfalls_env_topcornerdownleft</td><td>0x509F68F3</td><td>No</td></tr>
<tr><td>_angelfalls_env_topcornerdownright</td><td>0x6E47829A</td><td>No</td></tr>
<tr><td>_angelfalls_env_topcornerupleft</td><td>0x04D0C2A8</td><td>No</td></tr>
<tr><td>_angelfalls_env_topcornerupright</td><td>0x2801FC8F</td><td>No</td></tr>
<tr><td>_angelfalls_env_waterfallbase</td><td>0x229B202F</td><td>No</td></tr>
<tr><td>_angelfalls_env_waterfallbase_stream</td><td>0x2CC3211E</td><td>No</td></tr>
<tr><td>_angelfalls_env_waterfallmiddle</td><td>0xBC41B837</td><td>No</td></tr>
<tr><td>_angelfalls_env_waterfallmiddle_stream</td><td>0x891EE676</td><td>No</td></tr>
<tr><td>_angelfalls_env_waterfalltop</td><td>0xD6486DDD</td><td>No</td></tr>
<tr><td>_angelfalls_env_waterfalltop_stream</td><td>0xD5381B4C</td><td>No</td></tr>
<tr><td>_asset_building</td><td>0xC53B3283</td><td>No</td></tr>
<tr><td>_asset_building2</td><td>0xA51C6ED3</td><td>No</td></tr>
<tr><td>_asset_none</td><td>0xB3807B61</td><td>No</td></tr>
<tr><td>_asset_none2</td><td>0x7E06E8C9</td><td>No</td></tr>
<tr><td>_asset_prop</td><td>0x16292198</td><td>No</td></tr>
<tr><td>_asset_prop2</td><td>0x94D392EE</td><td>No</td></tr>
<tr><td>_asset_skyscraper</td><td>0x3F3FEA20</td><td>No</td></tr>
<tr><td>_asset_skyscraper2</td><td>0x1BD8CE66</td><td>No</td></tr>
<tr><td>_Car Camera Presets</td><td>0xEFBFD4DF</td><td>No</td></tr>
<tr><td>_Caracas_bld_capitol</td><td>0x2500A86E</td><td>No</td></tr>
<tr><td>_Caracas_bld_capitol_ruined</td><td>0xC126FA94</td><td>No</td></tr>
<tr><td>_caracas_bld_cathedral</td><td>0xE33F6880</td><td>No</td></tr>
<tr><td>_caracas_bld_cathedral_ruined</td><td>0x51DD01AE</td><td>No</td></tr>
<tr><td>_caracas_bld_cathedralstatue</td><td>0x5772D59C</td><td>No</td></tr>
<tr><td>_caracas_bld_construction01</td><td>0xF296DF56</td><td>No</td></tr>
<tr><td>_caracas_bld_construction01_ruined</td><td>0x1CE382DC</td><td>No</td></tr>
<tr><td>_caracas_bld_firestation</td><td>0x681CB84C</td><td>No</td></tr>
<tr><td>_caracas_bld_governmentcorner01</td><td>0x04082523</td><td>No</td></tr>
<tr><td>_caracas_bld_governmentcorner02</td><td>0xEA0A3ACC</td><td>No</td></tr>
<tr><td>_caracas_bld_governmentsegment</td><td>0x1184AC2C</td><td>No</td></tr>
<tr><td>_caracas_bld_historical01</td><td>0xD22DFEAD</td><td>No</td></tr>
<tr><td>_caracas_bld_historical02</td><td>0x50267642</td><td>No</td></tr>
<tr><td>_caracas_bld_historical02_ruined</td><td>0x521AE9B8</td><td>No</td></tr>
<tr><td>_caracas_bld_historical03</td><td>0x3228859F</td><td>No</td></tr>
<tr><td>_caracas_bld_historical03_ruined</td><td>0xFDE8B443</td><td>No</td></tr>
<tr><td>_caracas_bld_historical04</td><td>0xD0212F94</td><td>No</td></tr>
<tr><td>_caracas_bld_historical04_ruined</td><td>0x7EA5F2A2</td><td>No</td></tr>
<tr><td>_caracas_bld_historical05</td><td>0x2A23FBD9</td><td>No</td></tr>
<tr><td>_caracas_bld_historical05_ruined</td><td>0xBCE17DED</td><td>No</td></tr>
<tr><td>_caracas_bld_hospitalvargas</td><td>0x5FA05820</td><td>No</td></tr>
<tr><td>_caracas_bld_hospitalvargas_ruined</td><td>0x47BBABCE</td><td>No</td></tr>
<tr><td>_caracas_bld_parkingstructure01</td><td>0x65DF6146</td><td>No</td></tr>
<tr><td>_caracas_bld_parquecentral01</td><td>0xEC0299F2</td><td>No</td></tr>
<tr><td>_caracas_bld_parquecentral01_ruined</td><td>0x34453CE8</td><td>No</td></tr>
<tr><td>_caracas_bld_parquecentral02</td><td>0x6E0A225D</td><td>No</td></tr>
<tr><td>_caracas_bld_parquecentral02_ruined</td><td>0xB90E5371</td><td>No</td></tr>
<tr><td>_caracas_bld_parquecentral03</td><td>0x84080668</td><td>No</td></tr>
<tr><td>_caracas_bld_parquecentral03_ruined</td><td>0x759901F6</td><td>No</td></tr>
<tr><td>_caracas_bld_plazaparquecentral01</td><td>0xB16EB0E8</td><td>No</td></tr>
<tr><td>_caracas_bld_plazaparquecentral02</td><td>0x3B6BB88F</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscraperblacktower01</td><td>0xB9253A62</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscraperblacktower01_ruined</td><td>0x6CF5EA58</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscraperbluetower01</td><td>0x8E46A4BF</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscraperbluetower01_ruined</td><td>0xCC2E0AE3</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscrapercollapsed01</td><td>0x9E35963F</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscrapercollapsed02</td><td>0x9437C518</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscraperpristine01</td><td>0x6B8C2D4E</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscraperpristine02</td><td>0xCD938359</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscraperpristine02_ruined</td><td>0x0D6D586D</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscraperpristine03</td><td>0x7390B714</td><td>No</td></tr>
<tr><td>_caracas_bld_skyscraperpristine03_ruined</td><td>0xCF31CD22</td><td>No</td></tr>
<tr><td>_caracas_bld_skytrammain</td><td>0x53EFD034</td><td>No</td></tr>
<tr><td>_caracas_bld_skytrammain_ruined</td><td>0x29BD6DC2</td><td>No</td></tr>
<tr><td>_caracas_bld_skytramshopA</td><td>0xC3132D1C</td><td>No</td></tr>
<tr><td>_caracas_bld_skytramshopB</td><td>0x9D10B2B3</td><td>No</td></tr>
<tr><td>_caracas_bld_theater01</td><td>0xF0C5FA5A</td><td>No</td></tr>
<tr><td>_caracas_bld_theater01_Ruined</td><td>0xF28803D0</td><td>No</td></tr>
<tr><td>_caracas_bridgegovernment01</td><td>0x523CC48A</td><td>No</td></tr>
<tr><td>_caracas_bridgeparquecentral</td><td>0x264CC375</td><td>No</td></tr>
<tr><td>_caracas_capitolstatue</td><td>0x7BAF0531</td><td>No</td></tr>
<tr><td>_caracas_cathedralplateau</td><td>0xF92CAE8F</td><td>No</td></tr>
<tr><td>_caracas_fountaingovernment</td><td>0x415702CC</td><td>No</td></tr>
<tr><td>_caracas_fountainparquecentral</td><td>0xC1306DE0</td><td>No</td></tr>
<tr><td>_caracas_lawngovernment01</td><td>0xFD46330B</td><td>No</td></tr>
<tr><td>_caracas_lawngovernment02</td><td>0x2348AD74</td><td>No</td></tr>
<tr><td>_caracas_lawngovernment03</td><td>0xFD4AB039</td><td>No</td></tr>
<tr><td>_caracas_lawnparquecentral01</td><td>0xD84A4F83</td><td>No</td></tr>
<tr><td>_caracas_lawnparquecentral02</td><td>0x3E4D2EAC</td><td>No</td></tr>
<tr><td>_caracas_lawnparquecentral03</td><td>0x384F63D1</td><td>No</td></tr>
<tr><td>_caracas_lawnparquecentral04</td><td>0x5E51DE3A</td><td>No</td></tr>
<tr><td>_caracas_plantercapitolcenter</td><td>0xF1693392</td><td>No</td></tr>
<tr><td>_caracas_plantercapitolleft</td><td>0x236591D6</td><td>No</td></tr>
<tr><td>_caracas_plantercapitolright</td><td>0x172D7565</td><td>No</td></tr>
<tr><td>_caracas_portplateau01</td><td>0x7B79F7CB</td><td>No</td></tr>
<tr><td>_caracas_portplateau02</td><td>0xA17C7234</td><td>No</td></tr>
<tr><td>_caracas_rampgovernment01</td><td>0xCCED9715</td><td>No</td></tr>
<tr><td>_caracas_rampgovernment02</td><td>0x2AE5DC4A</td><td>No</td></tr>
<tr><td>_caracas_rampgovernmentmid</td><td>0x711E350E</td><td>No</td></tr>
<tr><td>_caracas_shoppingcenterplateau</td><td>0x18B51B98</td><td>No</td></tr>
<tr><td>_caracas_sidewalk1</td><td>0x532E30A0</td><td>No</td></tr>
<tr><td>_caracas_sidewalk2</td><td>0xFD2B6AA7</td><td>No</td></tr>
<tr><td>_caracas_skyscraperplateau01</td><td>0xD5826019</td><td>No</td></tr>
<tr><td>_caracas_skyscraperplateau02</td><td>0x737B0A0E</td><td>No</td></tr>
<tr><td>_caracas_skytramcolumn</td><td>0x51ED0322</td><td>No</td></tr>
<tr><td>_caracas_skytramplateau01</td><td>0xA9043933</td><td>No</td></tr>
<tr><td>_caracas_stairparquecentrallong</td><td>0x1CFEF671</td><td>No</td></tr>
<tr><td>_caracas_stairparquecentralshort</td><td>0x3890ADFF</td><td>No</td></tr>
<tr><td>_caracas_wallcorner</td><td>0xF75A76E6</td><td>No</td></tr>
<tr><td>_caracas_wallcorner_pristine</td><td>0xDEBD3609</td><td>No</td></tr>
<tr><td>_caracas_walllong</td><td>0xB6046123</td><td>No</td></tr>
<tr><td>_caracas_walllong_pristine</td><td>0xA213FB4A</td><td>No</td></tr>
<tr><td>_caracas_wallshort</td><td>0x229F1AB5</td><td>No</td></tr>
<tr><td>_caracas_wallshort_pristine</td><td>0xDBC9A110</td><td>No</td></tr>
<tr><td>_caracasruins_bld_corner16x16A</td><td>0x96E06243</td><td>No</td></tr>
<tr><td>_caracasruins_bld_corner16x16B</td><td>0xFCE3416C</td><td>No</td></tr>
<tr><td>_caracasruins_bld_corner16x32A</td><td>0xAB6A5785</td><td>No</td></tr>
<tr><td>_caracasruins_bld_corner16x32B</td><td>0x4963017A</td><td>No</td></tr>
<tr><td>_caracasruins_bld_corner32x32A</td><td>0x87BCBC9B</td><td>No</td></tr>
<tr><td>_caracasruins_bld_corner32x32B</td><td>0xEDBF9BC4</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_alarmtower</td><td>0x8324C22F</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_commbunker01</td><td>0xD134C65F</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_commbunker01_ruined</td><td>0x52562803</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_guardpost01</td><td>0xCC80CE0B</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_guardpost01_gate</td><td>0xE1EE029B</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_guardtowershort</td><td>0xCAB1A873</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_guardtowershort_ruined</td><td>0x5463E277</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_guardtowertall</td><td>0xE8F3EA02</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_hangar01</td><td>0x2CCE9531</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_hangar01_ruined</td><td>0xA6D64645</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_helipad</td><td>0xD193F670</td><td>Yes</td></tr>
<tr><td>_chinaoutpost_bld_prison</td><td>0xB5E32044</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_prison_fence</td><td>0x6DAF8CD2</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_prison_gate</td><td>0x983B00F2</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_prison_ruined</td><td>0x3960C5D2</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_storage</td><td>0xD0D21854</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_tent01</td><td>0x5BE217AB</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_tent02</td><td>0x81E49214</td><td>No</td></tr>
<tr><td>_chinaoutpost_bld_tent02_ruined</td><td>0xB51D8622</td><td>No</td></tr>
<tr><td>_chinaoutpost_concretewall01</td><td>0xD21BD8A4</td><td>No</td></tr>
<tr><td>_chinaoutpost_concretewall01_lowhealth</td><td>0xE5D65DB5</td><td>No</td></tr>
<tr><td>_chinaoutpost_concretewall02</td><td>0xEC19C2FB</td><td>No</td></tr>
<tr><td>_chinaoutpost_fueltanks</td><td>0xC12AD01B</td><td>Yes</td></tr>
<tr><td>_chinaoutpost_gateentrance</td><td>0x4A74B8DB</td><td>No</td></tr>
<tr><td>_chinaoutpost_interior_job</td><td>0x8FB388F4</td><td>No</td></tr>
<tr><td>_chinaoutpost_signbarrier</td><td>0x036E6494</td><td>No</td></tr>
<tr><td>_city_bld_apartment01</td><td>0x8229E3DC</td><td>No</td></tr>
<tr><td>_city_bld_apartment01_ruined</td><td>0x8697A5CA</td><td>No</td></tr>
<tr><td>_city_bld_apartment02</td><td>0x5C276973</td><td>No</td></tr>
<tr><td>_city_bld_apartment02_ruined</td><td>0x59341D77</td><td>No</td></tr>
<tr><td>_city_bld_apartment03</td><td>0xFA249096</td><td>No</td></tr>
<tr><td>_city_bld_apartment03_ruined</td><td>0xD0D8BE1C</td><td>No</td></tr>
<tr><td>_city_bld_apartment04</td><td>0x0435E975</td><td>No</td></tr>
<tr><td>_city_bld_apartment04_ruined</td><td>0xCACDD789</td><td>No</td></tr>
<tr><td>_city_bld_apartment05</td><td>0xDA3368C0</td><td>No</td></tr>
<tr><td>_city_bld_apartment05_ruined</td><td>0x7C9FC0EE</td><td>No</td></tr>
<tr><td>_city_bld_apartment06</td><td>0x04316C47</td><td>No</td></tr>
<tr><td>_city_bld_apartment06_ruined</td><td>0x3FEE5A0B</td><td>No</td></tr>
<tr><td>_city_bld_corner16x16a</td><td>0xAB93F71D</td><td>No</td></tr>
<tr><td>_city_bld_corner16x16a_ruined</td><td>0xF4220431</td><td>No</td></tr>
<tr><td>_city_bld_corner16x16b</td><td>0x298C6EB2</td><td>No</td></tr>
<tr><td>_city_bld_corner16x16b_ruined</td><td>0xFDE2BCA8</td><td>No</td></tr>
<tr><td>_city_bld_corner16x16c</td><td>0x4B8EE2CF</td><td>No</td></tr>
<tr><td>_city_bld_corner16x16c_ruined</td><td>0x3C7D7B33</td><td>No</td></tr>
<tr><td>_city_bld_corner16x16d</td><td>0x2987F184</td><td>No</td></tr>
<tr><td>_city_bld_corner16x16d_ruined</td><td>0x959C7012</td><td>No</td></tr>
<tr><td>_city_bld_corner16x32A</td><td>0x7E3F8303</td><td>No</td></tr>
<tr><td>_city_bld_corner16x32A_ruined</td><td>0xA28C3807</td><td>No</td></tr>
<tr><td>_city_bld_corner16x32B</td><td>0xE442622C</td><td>No</td></tr>
<tr><td>_city_bld_corner16x32B_ruined</td><td>0x69C2E41A</td><td>No</td></tr>
<tr><td>_city_bld_corner16x32C</td><td>0xDE449751</td><td>No</td></tr>
<tr><td>_city_bld_corner16x32D</td><td>0x044711BA</td><td>No</td></tr>
<tr><td>_city_bld_corner16x32D_ruined</td><td>0x419790B0</td><td>No</td></tr>
<tr><td>_city_bld_corner32x32A</td><td>0x4EC67AED</td><td>No</td></tr>
<tr><td>_city_bld_corner32x32A_ruined</td><td>0x3097A1C1</td><td>No</td></tr>
<tr><td>_city_bld_corner32x32B</td><td>0xCCBEF282</td><td>No</td></tr>
<tr><td>_city_bld_corner32x32B_ruined</td><td>0x036E4AF8</td><td>No</td></tr>
<tr><td>_city_bld_corner32x32C</td><td>0xAEC101DF</td><td>No</td></tr>
<tr><td>_city_bld_corner32x32C_ruined</td><td>0xB1B67E83</td><td>No</td></tr>
<tr><td>_city_bld_corner32x32D</td><td>0x4CB9ABD4</td><td>No</td></tr>
<tr><td>_city_bld_corner32x32D_ruined</td><td>0x0AAA78E2</td><td>No</td></tr>
<tr><td>_city_bld_segment16x16A</td><td>0x348240B3</td><td>No</td></tr>
<tr><td>_city_bld_segment16x16A_ruined</td><td>0xE1E554B7</td><td>No</td></tr>
<tr><td>_city_bld_segment16x16b</td><td>0x5A84BB1C</td><td>No</td></tr>
<tr><td>_city_bld_segment16x16b_ruined</td><td>0x0C88990A</td><td>No</td></tr>
<tr><td>_city_bld_segment16x16c</td><td>0x5486F041</td><td>No</td></tr>
<tr><td>_city_bld_segment16x16c_ruined</td><td>0x3F97A995</td><td>No</td></tr>
<tr><td>_city_bld_segment16x16d</td><td>0xBA89CF6A</td><td>No</td></tr>
<tr><td>_city_bld_segment16x16d_ruined</td><td>0x0AD328E0</td><td>No</td></tr>
<tr><td>_city_bld_segment16x32A</td><td>0x090BD135</td><td>No</td></tr>
<tr><td>_city_bld_segment16x32A_ruined</td><td>0x6536F149</td><td>No</td></tr>
<tr><td>_city_bld_segment16x32B</td><td>0xE704DFEA</td><td>No</td></tr>
<tr><td>_city_bld_segment16x32B_ruined</td><td>0x5BEA5660</td><td>No</td></tr>
<tr><td>_city_bld_segment16x32C</td><td>0x09075407</td><td>No</td></tr>
<tr><td>_city_bld_segment16x32C_ruined</td><td>0xB4ABBCCB</td><td>No</td></tr>
<tr><td>_city_bld_segment16x32D</td><td>0x86FFCB9C</td><td>No</td></tr>
<tr><td>_city_bld_segment16x32D_ruined</td><td>0x5D9FC68A</td><td>No</td></tr>
<tr><td>_city_bld_segment32x32A</td><td>0x1FCE92CB</td><td>No</td></tr>
<tr><td>_city_bld_segment32x32A_ruined</td><td>0x3978312F</td><td>No</td></tr>
<tr><td>_city_bld_segment32x32B</td><td>0x45D10D34</td><td>No</td></tr>
<tr><td>_city_bld_segment32x32B_ruined</td><td>0x84803CC2</td><td>No</td></tr>
<tr><td>_city_bld_segment32x32C</td><td>0x1FD30FF9</td><td>No</td></tr>
<tr><td>_city_bld_segment32x32D</td><td>0x45D58A62</td><td>No</td></tr>
<tr><td>_city_bld_segment32x32D_ruined</td><td>0x4A945A58</td><td>No</td></tr>
<tr><td>_city_bld_skyscraper01</td><td>0xB62E683B</td><td>No</td></tr>
<tr><td>_city_bld_skyscraper01_ruined</td><td>0x183D33DF</td><td>No</td></tr>
<tr><td>_city_bld_skyscraper02</td><td>0x9C307DE4</td><td>No</td></tr>
<tr><td>_city_bld_skyscraper02_ruined</td><td>0x39E21CF2</td><td>No</td></tr>
<tr><td>_city_bld_skyscraper03</td><td>0xB632E569</td><td>No</td></tr>
<tr><td>_city_bld_skyscraper03_ruined</td><td>0x7F06D37D</td><td>No</td></tr>
<tr><td>_city_bld_skyscraper04</td><td>0x1C35C492</td><td>No</td></tr>
<tr><td>_city_bld_standalone01</td><td>0x936B0531</td><td>No</td></tr>
<tr><td>_city_bld_standalone01_ruined</td><td>0xAA781645</td><td>No</td></tr>
<tr><td>_city_bld_standalone02</td><td>0x11637CC6</td><td>No</td></tr>
<tr><td>_city_bld_standalone02_ruined</td><td>0x2D6397CC</td><td>No</td></tr>
<tr><td>_city_bld_standalone03</td><td>0x3365F0E3</td><td>No</td></tr>
<tr><td>_city_bld_standalone03_ruined</td><td>0xA4F2BFE7</td><td>No</td></tr>
<tr><td>_city_bld_standalone04</td><td>0xB171F030</td><td>No</td></tr>
<tr><td>_city_bld_standalone04_ruined</td><td>0x8D322A9E</td><td>No</td></tr>
<tr><td>_city_bld_standalone05</td><td>0x1B74D5A5</td><td>No</td></tr>
<tr><td>_city_bld_standalone05_ruined</td><td>0x0E0BFC39</td><td>No</td></tr>
<tr><td>_city_bld_storefrontA</td><td>0x73DA352E</td><td>No</td></tr>
<tr><td>_city_bld_storefrontB</td><td>0xD5E18B39</td><td>No</td></tr>
<tr><td>_city_bld_storefrontC</td><td>0xFBDF8874</td><td>No</td></tr>
<tr><td>_city_bld_storefrontcornerA</td><td>0xF1D108FF</td><td>No</td></tr>
<tr><td>_city_bld_storefrontcornerB</td><td>0xE7D337D8</td><td>No</td></tr>
<tr><td>_city_bld_storefrontcornerC</td><td>0x11D5B88D</td><td>No</td></tr>
<tr><td>_city_bld_storefrontcornerD</td><td>0x07C45FAE</td><td>No</td></tr>
<tr><td>_city_bld_storefrontcornerE</td><td>0x69C7388B</td><td>No</td></tr>
<tr><td>_city_bld_storefrontcornerF</td><td>0x8FC9B2F4</td><td>No</td></tr>
<tr><td>_city_bld_storefrontD</td><td>0x5DE6DE7F</td><td>No</td></tr>
<tr><td>_city_bld_storefrontE</td><td>0xFBE405A2</td><td>No</td></tr>
<tr><td>_city_bld_storefrontF</td><td>0x7DEB8E0D</td><td>No</td></tr>
<tr><td>_city_busstop01</td><td>0x499A441F</td><td>No</td></tr>
<tr><td>_civilian_chaira</td><td>0x6371A6AA</td><td>No</td></tr>
<tr><td>_commercial_bld_clinic</td><td>0x8D8E3BFC</td><td>No</td></tr>
<tr><td>_commercial_bld_corner16x16a</td><td>0x704116CC</td><td>No</td></tr>
<tr><td>_commercial_bld_corner16x16a_ruined</td><td>0xD89B2E3A</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x16a</td><td>0xD65F4757</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x16a_ruined</td><td>0x67F5B75B</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x16b</td><td>0xEC61A890</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x16b_ruined</td><td>0x630B76FE</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x16c</td><td>0xD663C485</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x16c_ruined</td><td>0xB9430D19</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x8a</td><td>0x0394938A</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x8a_ruined</td><td>0xCDF49980</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x8b</td><td>0xA59C4E55</td><td>No</td></tr>
<tr><td>_commercial_bld_corner8x8b_ruined</td><td>0xAC5AD069</td><td>No</td></tr>
<tr><td>_commercial_bld_firestation</td><td>0x169D4A64</td><td>No</td></tr>
<tr><td>_commercial_bld_policestation</td><td>0xB885803E</td><td>No</td></tr>
<tr><td>_commercial_bld_ruins16x16</td><td>0xCA77D281</td><td>No</td></tr>
<tr><td>_commercial_bld_ruins16x24</td><td>0x016F76AE</td><td>No</td></tr>
<tr><td>_commercial_bld_ruins16x32</td><td>0xF80C16EF</td><td>No</td></tr>
<tr><td>_commercial_bld_ruins8x24</td><td>0xF381B8AF</td><td>No</td></tr>
<tr><td>_commercial_bld_ruins8x32</td><td>0x652AE0AA</td><td>No</td></tr>
<tr><td>_commercial_bld_segment16x16a</td><td>0x22F4BCBC</td><td>No</td></tr>
<tr><td>_commercial_bld_segment16x16a_ruined</td><td>0x586AB1AA</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x16a</td><td>0xB1EDD787</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x16a_ruined</td><td>0xCF70AB4B</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x16b</td><td>0x87EFD400</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x16c</td><td>0xB1F254B5</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x16c_ruined</td><td>0x7FFBDFC9</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x16d</td><td>0xA7E0FBD6</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x16d_ruined</td><td>0xF54B745C</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x16e</td><td>0x09E3D4B3</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x16e_ruined</td><td>0x4DC170B7</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x8a</td><td>0xDFFE58BA</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x8a_ruined</td><td>0x1ECE2DB0</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x8b</td><td>0x4205AEC5</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x8b_ruined</td><td>0x50FE2759</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x8c</td><td>0x580392D0</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x8c_ruined</td><td>0xBE488E3E</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x8d</td><td>0x59F6CA03</td><td>No</td></tr>
<tr><td>_commercial_bld_segment8x8d_ruined</td><td>0x7FC2D507</td><td>No</td></tr>
<tr><td>_commercial_bld_supermarket</td><td>0x75BE4579</td><td>No</td></tr>
<tr><td>_commercial_bld_supermarket_ruined</td><td>0xFAACC60D</td><td>No</td></tr>
<tr><td>_commercial_lightclinic</td><td>0x54BDD1B3</td><td>No</td></tr>
<tr><td>_commercial_merge_concrete</td><td>0x13DC322B</td><td>No</td></tr>
<tr><td>_commercial_mergeconcrete</td><td>0x05E91342</td><td>No</td></tr>
<tr><td>_commercial_road10</td><td>0x81A1B270</td><td>No</td></tr>
<tr><td>_commercial_road10Clean</td><td>0x7BEC3EA7</td><td>No</td></tr>
<tr><td>_commercial_road10Cleancross</td><td>0xB9509A0D</td><td>No</td></tr>
<tr><td>_commercial_road10CleanL</td><td>0x1A808871</td><td>No</td></tr>
<tr><td>_commercial_road10CleanT</td><td>0x3A4490A9</td><td>No</td></tr>
<tr><td>_commercial_road10CleanT20</td><td>0x1953C29B</td><td>No</td></tr>
<tr><td>_commercial_road10CleanT5</td><td>0x42DE3E8A</td><td>No</td></tr>
<tr><td>_commercial_road10cross</td><td>0x6A6CA690</td><td>No</td></tr>
<tr><td>_commercial_road10cross5</td><td>0xCD077E75</td><td>No</td></tr>
<tr><td>_commercial_road10l</td><td>0xCAFC0198</td><td>No</td></tr>
<tr><td>_commercial_road10middle</td><td>0x3BE9E69F</td><td>No</td></tr>
<tr><td>_commercial_road10straight</td><td>0x240E67BA</td><td>No</td></tr>
<tr><td>_commercial_road10t</td><td>0xCAE879E0</td><td>No</td></tr>
<tr><td>_commercial_road10t20</td><td>0xD6A80E46</td><td>No</td></tr>
<tr><td>_commercial_road10t5</td><td>0xC0447285</td><td>No</td></tr>
<tr><td>_commercial_road10Transparent</td><td>0xB5FEE212</td><td>No</td></tr>
<tr><td>_commercial_road20</td><td>0x170A6BC1</td><td>No</td></tr>
<tr><td>_commercial_road20b</td><td>0x2FB4F779</td><td>No</td></tr>
<tr><td>_commercial_road20Clean</td><td>0x2401AAB0</td><td>No</td></tr>
<tr><td>_commercial_road20Cleanb</td><td>0x29524986</td><td>No</td></tr>
<tr><td>_commercial_road20Cleancross</td><td>0x0637AED0</td><td>No</td></tr>
<tr><td>_commercial_road20CleanT</td><td>0xA9397B20</td><td>No</td></tr>
<tr><td>_commercial_road20CleanT10</td><td>0xEBAE3E4B</td><td>No</td></tr>
<tr><td>_commercial_road20cross</td><td>0xCEA0D127</td><td>No</td></tr>
<tr><td>_commercial_road20cross10</td><td>0xEEBF26A4</td><td>No</td></tr>
<tr><td>_commercial_road20merge10</td><td>0x54D09630</td><td>No</td></tr>
<tr><td>_commercial_road20t</td><td>0x5792A42F</td><td>No</td></tr>
<tr><td>_commercial_road20t10</td><td>0xCD4AED8C</td><td>No</td></tr>
<tr><td>_commercial_road20t10b</td><td>0x526909CA</td><td>No</td></tr>
<tr><td>_commercial_road5</td><td>0xDA968AB0</td><td>No</td></tr>
<tr><td>_commercial_road5cross</td><td>0x83BE4ED0</td><td>No</td></tr>
<tr><td>_commercial_road5l</td><td>0x15A9A2D8</td><td>No</td></tr>
<tr><td>_commercial_road5t</td><td>0x15961B20</td><td>No</td></tr>
<tr><td>_commercial_road5t10</td><td>0xC1EBDE4B</td><td>No</td></tr>
<tr><td>_commercial_roadgovnt</td><td>0xACAC7E4F</td><td>No</td></tr>
<tr><td>_commercial_roadstraight10</td><td>0x00AAD096</td><td>No</td></tr>
<tr><td>_commercial_roadstraight10_crater02</td><td>0x056DA31E</td><td>No</td></tr>
<tr><td>_commercial_roadstraight10_crater02_straight</td><td>0xC5D81E3F</td><td>No</td></tr>
<tr><td>_commercial_roadstraight10_crater_stitcher</td><td>0xD682416D</td><td>No</td></tr>
<tr><td>_commercial_roadstraight20</td><td>0xC95EFD5B</td><td>No</td></tr>
<tr><td>_commercial_roadstraight20_crater02</td><td>0x22C44025</td><td>No</td></tr>
<tr><td>_commercial_roadstraight20_crater02_straight</td><td>0x173398F6</td><td>No</td></tr>
<tr><td>_commercial_roadstraight20_crater_stitcher</td><td>0x674EAAA8</td><td>No</td></tr>
<tr><td>_commercial_roadstraight20b</td><td>0xD213D90B</td><td>No</td></tr>
<tr><td>_commercial_roadstraight5</td><td>0x6245D0CA</td><td>No</td></tr>
<tr><td>_commercial_sidewalk</td><td>0x447A6247</td><td>No</td></tr>
<tr><td>_commercial_sidewalk02</td><td>0x259FE84D</td><td>No</td></tr>
<tr><td>_commercial_sidewalkClean</td><td>0xFC8DB1F2</td><td>No</td></tr>
<tr><td>_commercial_sidewalkCleansmall</td><td>0x19260E7B</td><td>No</td></tr>
<tr><td>_commercial_sidewalksmall</td><td>0x138FB724</td><td>No</td></tr>
<tr><td>_commercial_tunnelcap</td><td>0x3E06D87D</td><td>No</td></tr>
<tr><td>_commercial_tunnelsegment</td><td>0x87B99176</td><td>No</td></tr>
<tr><td>_commercial_wall</td><td>0xD08A375D</td><td>No</td></tr>
<tr><td>_commercial_wallbeachlong</td><td>0xDB4E6594</td><td>No</td></tr>
<tr><td>_commercial_wallbeachshort</td><td>0xA5B485E0</td><td>No</td></tr>
<tr><td>_commercial_wallcorner</td><td>0x9997052E</td><td>No</td></tr>
<tr><td>_commercial_wallcorner_pristine</td><td>0xC1FE8321</td><td>No</td></tr>
<tr><td>_commercial_walllong</td><td>0x7C827A9B</td><td>No</td></tr>
<tr><td>_commercial_walllong_pristine</td><td>0x5811F9D2</td><td>No</td></tr>
<tr><td>_commercial_wallshort</td><td>0xA8BE3C0D</td><td>No</td></tr>
<tr><td>_commercial_wallshort_pristine</td><td>0x62E0DD58</td><td>No</td></tr>
<tr><td>_cumana_bld_corner16x16b</td><td>0x0494455A</td><td>No</td></tr>
<tr><td>_cumana_bld_corner16x16c</td><td>0xE69654B7</td><td>No</td></tr>
<tr><td>_cumana_bld_corner32x32B</td><td>0xB5C3AE6A</td><td>No</td></tr>
<tr><td>_cumana_bld_fortress01</td><td>0x0F46E72E</td><td>No</td></tr>
<tr><td>_cumana_bld_hotelfourstar01</td><td>0xB69BFEAC</td><td>No</td></tr>
<tr><td>_cumana_bld_hotelfourstar01_ruined</td><td>0xD25D559A</td><td>No</td></tr>
<tr><td>_cumana_bld_hoteltwostar01</td><td>0x19669520</td><td>No</td></tr>
<tr><td>_cumana_bld_hoteltwostar01_ruined</td><td>0xEC057ACE</td><td>No</td></tr>
<tr><td>_cumana_bld_segment16x16a</td><td>0xC932E0EB</td><td>No</td></tr>
<tr><td>_cumana_bld_segment32x32D</td><td>0x5FE42C3A</td><td>No</td></tr>
<tr><td>_cumana_bridge_end</td><td>0xBA7B9611</td><td>No</td></tr>
<tr><td>_cumana_bridge_midA</td><td>0x0EC8A1C5</td><td>No</td></tr>
<tr><td>_cumana_bridge_whiteend</td><td>0x10977A0C</td><td>No</td></tr>
<tr><td>_cumana_bridge_whitemid</td><td>0x6B2BBDB1</td><td>No</td></tr>
<tr><td>_DELETE ME</td><td>0x8030427D</td><td>No</td></tr>
<tr><td>_dlc_coro_bld_motorpool</td><td>0xD2BC640A</td><td>No</td></tr>
<tr><td>_DLC_global_env_treemedium02</td><td>0xFBBCD0E5</td><td>No</td></tr>
<tr><td>_DLC_outskirt_road10</td><td>0x5C12EFA7</td><td>No</td></tr>
<tr><td>_docks_bld_bar</td><td>0x0EA28FE1</td><td>No</td></tr>
<tr><td>_docks_bld_booth</td><td>0x327D909A</td><td>No</td></tr>
<tr><td>_docks_bld_toolshed</td><td>0x2DE708EA</td><td>No</td></tr>
<tr><td>_docks_bld_toolshed_ruined</td><td>0xBF648960</td><td>No</td></tr>
<tr><td>_docks_bld_warehouse</td><td>0xEC496AA7</td><td>No</td></tr>
<tr><td>_docks_bld_warehouse_ruined</td><td>0x482909EB</td><td>No</td></tr>
<tr><td>_docks_bld_warehousesmall</td><td>0x625F3B84</td><td>No</td></tr>
<tr><td>_docks_bld_warehousesmall_ruined</td><td>0x4149FE12</td><td>No</td></tr>
<tr><td>_docks_crane</td><td>0x86CC17EA</td><td>No</td></tr>
<tr><td>_docks_dockconcrete</td><td>0x062770FF</td><td>No</td></tr>
<tr><td>_docks_docklarge</td><td>0x4362A993</td><td>No</td></tr>
<tr><td>_docks_docklarge_ruin</td><td>0x695F2284</td><td>No</td></tr>
<tr><td>_docks_dockmini</td><td>0x28F9DCE3</td><td>No</td></tr>
<tr><td>_docks_dockmini_ruined</td><td>0xF1CB23E7</td><td>No</td></tr>
<tr><td>_docks_dockpump</td><td>0x070941AC</td><td>No</td></tr>
<tr><td>_docks_docksmall</td><td>0x25D4384B</td><td>No</td></tr>
<tr><td>_docks_docksmall_ruined</td><td>0x1BFB75AF</td><td>No</td></tr>
<tr><td>_docks_fishcage</td><td>0x7E4F04F1</td><td>No</td></tr>
<tr><td>_docks_fishingpole</td><td>0xDDECDED9</td><td>No</td></tr>
<tr><td>_docks_lamppost</td><td>0x77DE8FD3</td><td>No</td></tr>
<tr><td>_docks_net</td><td>0xEDCF6DFC</td><td>No</td></tr>
<tr><td>_docks_netbundled</td><td>0xFEBF31EC</td><td>No</td></tr>
<tr><td>_docks_netoverhang</td><td>0x2D661052</td><td>No</td></tr>
<tr><td>_docks_tiredock</td><td>0xF069B3C8</td><td>No</td></tr>
<tr><td>_estate_benchstone01</td><td>0xB3067FAB</td><td>No</td></tr>
<tr><td>_estate_bld_mansion01</td><td>0x61C41F60</td><td>No</td></tr>
<tr><td>_estate_bld_mansion01_partialRuin</td><td>0x8271FE7C</td><td>No</td></tr>
<tr><td>_estate_bld_mansion01_ruined</td><td>0x656C4F0E</td><td>No</td></tr>
<tr><td>_estate_bld_mansion02</td><td>0x0BC15967</td><td>No</td></tr>
<tr><td>_estate_bld_mansion02_ruined</td><td>0xAD2FEBAB</td><td>No</td></tr>
<tr><td>_estate_bld_mansion03</td><td>0xE9BEE54A</td><td>No</td></tr>
<tr><td>_estate_bld_mansion03_ruined</td><td>0x282F7440</td><td>No</td></tr>
<tr><td>_estate_bld_mansion04</td><td>0x03BCCFA1</td><td>No</td></tr>
<tr><td>_estate_bld_mansion04_ruined</td><td>0x95352BF5</td><td>No</td></tr>
<tr><td>_estate_bld_poolelevated01</td><td>0x07F13467</td><td>No</td></tr>
<tr><td>_Estate_bld_securityshed</td><td>0xE4E141EA</td><td>No</td></tr>
<tr><td>_estate_bld_tower01</td><td>0x3AA91B50</td><td>No</td></tr>
<tr><td>_estate_bld_tower02</td><td>0x24A6BA17</td><td>No</td></tr>
<tr><td>_estate_sidewalk</td><td>0xF92280A5</td><td>No</td></tr>
<tr><td>_estate_sidewalksmall</td><td>0x6F49AB3A</td><td>No</td></tr>
<tr><td>_estate_stairs01</td><td>0x4CD2F7B8</td><td>No</td></tr>
<tr><td>_estate_stairs02</td><td>0xD6CFFF5F</td><td>No</td></tr>
<tr><td>_estate_stairs03</td><td>0xF4CDF002</td><td>No</td></tr>
<tr><td>_estate_stairscenter01</td><td>0x790C8DDF</td><td>No</td></tr>
<tr><td>_estate_wallgate01</td><td>0xF6B820F7</td><td>No</td></tr>
<tr><td>_estate_wallgate01_ruined</td><td>0x876EDBFB</td><td>No</td></tr>
<tr><td>_estate_walllong</td><td>0x0812E7D5</td><td>No</td></tr>
<tr><td>_estate_walllong_pristine</td><td>0x637B5630</td><td>No</td></tr>
<tr><td>_estate_walllong_ruined</td><td>0xCD4D50E9</td><td>No</td></tr>
<tr><td>_estate_wallpole</td><td>0x18BE0545</td><td>No</td></tr>
<tr><td>_estate_wallshort</td><td>0x8639A29B</td><td>No</td></tr>
<tr><td>_estate_wallshort_pristine</td><td>0x2EECF1D2</td><td>No</td></tr>
<tr><td>_fueltanks parent</td><td>0x6AF39AFD</td><td>Yes</td></tr>
<tr><td>_global_acunita</td><td>0x51FE4E53</td><td>No</td></tr>
<tr><td>_global_acunitb</td><td>0x7800C8BC</td><td>No</td></tr>
<tr><td>_global_antennaB</td><td>0x319CC265</td><td>No</td></tr>
<tr><td>_global_antennaD</td><td>0x498DDDA3</td><td>No</td></tr>
<tr><td>_global_att_chandelier</td><td>0x7319C1F9</td><td>No</td></tr>
<tr><td>_global_att_signlanemerge</td><td>0xFFE29107</td><td>No</td></tr>
<tr><td>_global_att_signnouturn</td><td>0x554211D6</td><td>No</td></tr>
<tr><td>_global_att_signoneway</td><td>0x28B81A82</td><td>No</td></tr>
<tr><td>_global_att_signspeed</td><td>0xC78ED160</td><td>No</td></tr>
<tr><td>_global_awninga</td><td>0xDEDB3C77</td><td>No</td></tr>
<tr><td>_global_bannera</td><td>0x5C049143</td><td>No</td></tr>
<tr><td>_global_barbedwirelong</td><td>0x772B42C9</td><td>No</td></tr>
<tr><td>_global_barbedwireshort</td><td>0x5EE0CF37</td><td>No</td></tr>
<tr><td>_global_barbell</td><td>0xCD2A1788</td><td>No</td></tr>
<tr><td>_global_barbequea</td><td>0x84BDA044</td><td>No</td></tr>
<tr><td>_global_barrela</td><td>0x65674451</td><td>No</td></tr>
<tr><td>_global_barrelb</td><td>0xE35FBBE6</td><td>No</td></tr>
<tr><td>_global_barrelc</td><td>0x05623003</td><td>No</td></tr>
<tr><td>_global_barrelmarketa</td><td>0x373DA789</td><td>No</td></tr>
<tr><td>_global_barrelmarketb</td><td>0x9535ECBE</td><td>No</td></tr>
<tr><td>_global_barrelmarketc</td><td>0xB73860DB</td><td>No</td></tr>
<tr><td>_global_barrelmarketd</td><td>0xB54529A8</td><td>No</td></tr>
<tr><td>_global_barreloil</td><td>0xE87C70F0</td><td>No</td></tr>
<tr><td>_global_barrelorange</td><td>0xE59AF1EA</td><td>No</td></tr>
<tr><td>_global_barricadea</td><td>0xD8154C52</td><td>No</td></tr>
<tr><td>_global_barricadeb</td><td>0x5A1CD4BD</td><td>No</td></tr>
<tr><td>_global_barricadec</td><td>0xF019EF48</td><td>No</td></tr>
<tr><td>_global_barricaded</td><td>0x720DEFFB</td><td>No</td></tr>
<tr><td>_global_barrierCornerOC</td><td>0x82D32C4C</td><td>No</td></tr>
<tr><td>_global_barrierStraightOC</td><td>0xD9EEDD1D</td><td>No</td></tr>
<tr><td>_global_bencha</td><td>0xD2CFA533</td><td>No</td></tr>
<tr><td>_global_benchpark</td><td>0x4F058F0E</td><td>No</td></tr>
<tr><td>_global_billboard01</td><td>0x59FBF0E4</td><td>No</td></tr>
<tr><td>_global_billboard02</td><td>0x73F9DB3B</td><td>No</td></tr>
<tr><td>_global_billboard03</td><td>0x51F7671E</td><td>No</td></tr>
<tr><td>_global_billboard04</td><td>0x5C08BFFD</td><td>No</td></tr>
<tr><td>_global_billboard05</td><td>0xF205DA88</td><td>No</td></tr>
<tr><td>_global_billboard06</td><td>0xFC03ABAF</td><td>No</td></tr>
<tr><td>_global_billboard_bridge01</td><td>0x2A426AAE</td><td>No</td></tr>
<tr><td>_global_billboard_roof01</td><td>0x55D77BE3</td><td>No</td></tr>
<tr><td>_global_billboard_roof02</td><td>0x3BD9918C</td><td>No</td></tr>
<tr><td>_global_billboard_wall01</td><td>0x18124D9D</td><td>No</td></tr>
<tr><td>_global_billboard_wall02</td><td>0x960AC532</td><td>No</td></tr>
<tr><td>_global_billboard_wall03</td><td>0xB80D394F</td><td>No</td></tr>
<tr><td>_global_billboard_wall04</td><td>0x96064804</td><td>No</td></tr>
<tr><td>_global_binnoculars</td><td>0x4EB00652</td><td>No</td></tr>
<tr><td>_global_bld_bunkersandbag</td><td>0x6801EDCA</td><td>No</td></tr>
<tr><td>_global_bld_loadingdockA</td><td>0xE461FEBB</td><td>No</td></tr>
<tr><td>_global_bld_loadingdockB</td><td>0xCA641464</td><td>No</td></tr>
<tr><td>_global_bld_officetrailerA</td><td>0x6C1B532F</td><td>No</td></tr>
<tr><td>_global_bld_potty0</td><td>0xF1C85BA1</td><td>No</td></tr>
<tr><td>_global_bld_tentmarket01</td><td>0xC3B0284B</td><td>No</td></tr>
<tr><td>_global_bld_tentmarket02</td><td>0xE9B2A2B4</td><td>No</td></tr>
<tr><td>_global_blueprints</td><td>0x96398108</td><td>No</td></tr>
<tr><td>_global_bonfire01</td><td>0x20E6E498</td><td>No</td></tr>
<tr><td>_global_bookshelflargea</td><td>0x7D461273</td><td>No</td></tr>
<tr><td>_global_bookshelfsmalla</td><td>0x11E449AB</td><td>No</td></tr>
<tr><td>_global_boxa</td><td>0xE649C320</td><td>No</td></tr>
<tr><td>_global_boxb</td><td>0x9046FD27</td><td>No</td></tr>
<tr><td>_global_boxb_lowhealth</td><td>0x5B9356AE</td><td>No</td></tr>
<tr><td>_global_boxc</td><td>0x6E44890A</td><td>No</td></tr>
<tr><td>_global_boxc_lowhealth</td><td>0xC5269137</td><td>No</td></tr>
<tr><td>_global_boxd</td><td>0x88427361</td><td>No</td></tr>
<tr><td>_global_boxd OilCon020</td><td>0xFA0EBF27</td><td>No</td></tr>
<tr><td>_global_boxholes</td><td>0xA595A40C</td><td>No</td></tr>
<tr><td>_global_boxholes_parrot</td><td>0x8C57434F</td><td>No</td></tr>
<tr><td>_global_brickpile01</td><td>0x096C35F6</td><td>No</td></tr>
<tr><td>_global_bridgepedestrian01</td><td>0xD437CFA1</td><td>No</td></tr>
<tr><td>_global_bridgetransition</td><td>0xA2E766F2</td><td>No</td></tr>
<tr><td>_global_cartbrick</td><td>0x953479FD</td><td>No</td></tr>
<tr><td>_global_centerdivider_long</td><td>0x8465B4DF</td><td>No</td></tr>
<tr><td>_global_centerdivider_middle</td><td>0xBC0059F2</td><td>No</td></tr>
<tr><td>_global_centerdivider_short</td><td>0xF04253B9</td><td>No</td></tr>
<tr><td>_global_chaircafe</td><td>0x0AAB62C4</td><td>No</td></tr>
<tr><td>_global_chaircomputer</td><td>0x55B1F098</td><td>No</td></tr>
<tr><td>_global_chairfolding</td><td>0xFE320A4E</td><td>No</td></tr>
<tr><td>_global_chairwooda</td><td>0x73384441</td><td>No</td></tr>
<tr><td>_global_chairwoodb</td><td>0xF130BBD6</td><td>No</td></tr>
<tr><td>_global_chairwoodc</td><td>0x533394B3</td><td>No</td></tr>
<tr><td>_global_chairwoodd</td><td>0xD13F9400</td><td>No</td></tr>
<tr><td>_global_chairwoode</td><td>0xFB4214B5</td><td>No</td></tr>
<tr><td>_global_chairwoodf</td><td>0xD93B236A</td><td>No</td></tr>
<tr><td>_global_chairyarda</td><td>0x6348F534</td><td>No</td></tr>
<tr><td>_global_checkpointA</td><td>0x5BEED12F</td><td>No</td></tr>
<tr><td>_global_chessset</td><td>0x0D3FD180</td><td>No</td></tr>
<tr><td>_global_clothlineshort</td><td>0xD27A01C0</td><td>No</td></tr>
<tr><td>_global_concretebarrier01</td><td>0x94CC289F</td><td>No</td></tr>
<tr><td>_global_concretebarrier_vz</td><td>0xF99EFFBD</td><td>No</td></tr>
<tr><td>_global_constructionpileC</td><td>0xF46E7E2A</td><td>No</td></tr>
<tr><td>_global_containertransplant</td><td>0x90FF58B8</td><td>No</td></tr>
<tr><td>_global_decal_puddle01</td><td>0x5D674767</td><td>No</td></tr>
<tr><td>_global_decal_puddle02</td><td>0xB36A0D60</td><td>No</td></tr>
<tr><td>_global_decal_puddle03</td><td>0xDD6C8E15</td><td>No</td></tr>
<tr><td>_global_decal_puddle04</td><td>0xD35B3536</td><td>No</td></tr>
<tr><td>_global_decal_puddle05</td><td>0xB55D4493</td><td>No</td></tr>
<tr><td>_global_drinkingfountain</td><td>0x31B8E0AE</td><td>No</td></tr>
<tr><td>_global_dumpstergraylong</td><td>0x8CB07ACD</td><td>No</td></tr>
<tr><td>_global_dumpstergreenshort</td><td>0x50A3FA37</td><td>No</td></tr>
<tr><td>_global_dumpstergreyshort</td><td>0x39E555C7</td><td>No</td></tr>
<tr><td>_global_electricalbox01</td><td>0x82BA5A04</td><td>No</td></tr>
<tr><td>_global_electricalbox02</td><td>0x1CB77ADB</td><td>No</td></tr>
<tr><td>_global_electricboxa</td><td>0xA9CF60A1</td><td>No</td></tr>
<tr><td>_global_electronicboxA</td><td>0xA766B6E6</td><td>No</td></tr>
<tr><td>_global_emptyfruitbox</td><td>0xF9DD80DE</td><td>No</td></tr>
<tr><td>_global_env_bush01</td><td>0x48BDE593</td><td>No</td></tr>
<tr><td>_global_env_bushlarge01</td><td>0x79E24672</td><td>No</td></tr>
<tr><td>_global_env_bushlarge02</td><td>0xFBE9CEDD</td><td>No</td></tr>
<tr><td>_global_env_hedgecorner</td><td>0xB595EAB0</td><td>No</td></tr>
<tr><td>_global_env_hedgelong</td><td>0xD566029D</td><td>No</td></tr>
<tr><td>_global_env_hedgelong01</td><td>0x012CB410</td><td>No</td></tr>
<tr><td>_global_env_hedgelong02</td><td>0xEB2A52D7</td><td>No</td></tr>
<tr><td>_global_env_hedgelong03</td><td>0x892779FA</td><td>No</td></tr>
<tr><td>_global_env_hedgelong04</td><td>0x6324FF91</td><td>No</td></tr>
<tr><td>_global_env_hedgelowcorner</td><td>0x514366D0</td><td>No</td></tr>
<tr><td>_global_env_hedgelowlong</td><td>0x1EDE6EBD</td><td>No</td></tr>
<tr><td>_global_env_hedgelowshort</td><td>0xD07C1F63</td><td>No</td></tr>
<tr><td>_global_env_hedgelowsquare</td><td>0x95B702EA</td><td>No</td></tr>
<tr><td>_global_env_hedgeshort</td><td>0xB5FA41C3</td><td>No</td></tr>
<tr><td>_global_env_hedgeshort01</td><td>0x073EBCBE</td><td>No</td></tr>
<tr><td>_global_env_hedgesquare</td><td>0x3F954CCA</td><td>No</td></tr>
<tr><td>_global_env_lawnuniversity01</td><td>0x934DDD13</td><td>No</td></tr>
<tr><td>_global_env_lawnuniversity02</td><td>0xB950577C</td><td>No</td></tr>
<tr><td>_global_env_palmtree01</td><td>0x347C8A5D</td><td>No</td></tr>
<tr><td>_global_env_palmtreebend01</td><td>0x16DD7ED0</td><td>No</td></tr>
<tr><td>_global_env_palmtreebend02</td><td>0x00DB1D97</td><td>No</td></tr>
<tr><td>_global_env_palmtreebend03</td><td>0x9ED844BA</td><td>No</td></tr>
<tr><td>_global_env_palmtreebend04</td><td>0x78D5CA51</td><td>No</td></tr>
<tr><td>_global_env_palmtreebend05</td><td>0x7ED3952C</td><td>No</td></tr>
<tr><td>_global_env_palmtreeplanted01</td><td>0x077D6479</td><td>No</td></tr>
<tr><td>_global_env_plantersidewalk01</td><td>0x151286A9</td><td>No</td></tr>
<tr><td>_global_env_rockjungle01</td><td>0x0856CCDD</td><td>No</td></tr>
<tr><td>_global_env_rockjungle02</td><td>0x864F4472</td><td>No</td></tr>
<tr><td>_global_env_rockjungle03</td><td>0xA851B88F</td><td>No</td></tr>
<tr><td>_global_env_rockjungle04</td><td>0x864AC744</td><td>No</td></tr>
<tr><td>_global_env_rockjungle05</td><td>0xA04D2EC9</td><td>No</td></tr>
<tr><td>_global_env_rockjungle06</td><td>0xFE4573FE</td><td>No</td></tr>
<tr><td>_global_env_rocksbeach01</td><td>0x672E6A22</td><td>No</td></tr>
<tr><td>_global_env_rocksbeach02</td><td>0xE935F28D</td><td>No</td></tr>
<tr><td>_global_env_rocksbeach03</td><td>0xBF3371D8</td><td>No</td></tr>
<tr><td>_global_env_rocksbeach04</td><td>0x4127728B</td><td>No</td></tr>
<tr><td>_global_env_rocksbeach05</td><td>0xDF2499AE</td><td>No</td></tr>
<tr><td>_global_env_rocksbeach06</td><td>0x412BEFB9</td><td>No</td></tr>
<tr><td>_global_env_rocksmall01</td><td>0x52AD1D89</td><td>No</td></tr>
<tr><td>_global_env_rocksmine01</td><td>0x710C425A</td><td>No</td></tr>
<tr><td>_global_env_rocksmine02</td><td>0xD3139865</td><td>No</td></tr>
<tr><td>_global_env_rocksmine03</td><td>0x6910B2F0</td><td>No</td></tr>
<tr><td>_global_env_rocksmine04</td><td>0xEB04B3A3</td><td>No</td></tr>
<tr><td>_global_env_rocksmine05</td><td>0xC9023F86</td><td>No</td></tr>
<tr><td>_global_env_rocksmine06</td><td>0x4B09C7F1</td><td>No</td></tr>
<tr><td>_global_env_rocksmoss01</td><td>0xF4D9320D</td><td>No</td></tr>
<tr><td>_global_env_rocksmoss02</td><td>0x72D1A9A2</td><td>No</td></tr>
<tr><td>_global_env_rocksmoss03</td><td>0xD4D4827F</td><td>No</td></tr>
<tr><td>_global_env_rocksmoss04</td><td>0x72CD2C74</td><td>No</td></tr>
<tr><td>_global_env_rocksmoss05</td><td>0x4CCF2F39</td><td>No</td></tr>
<tr><td>_global_env_rocksmoss06</td><td>0xEAC7D92E</td><td>No</td></tr>
<tr><td>_global_env_rocktall01</td><td>0xE9D7D2AB</td><td>No</td></tr>
<tr><td>_global_env_scrub03</td><td>0x1A855392</td><td>No</td></tr>
<tr><td>_global_env_tree01</td><td>0x68ECDFDD</td><td>No</td></tr>
<tr><td>_global_env_treeoak01</td><td>0xDB65DF8E</td><td>No</td></tr>
<tr><td>_global_env_treeplaza01</td><td>0x485FF5CF</td><td>No</td></tr>
<tr><td>_global_env_treeplaza02</td><td>0xBE62EE28</td><td>No</td></tr>
<tr><td>_global_env_treeplaza03</td><td>0xA8650A1D</td><td>No</td></tr>
<tr><td>_global_env_treesidewalk01</td><td>0xA574991F</td><td>No</td></tr>
<tr><td>_global_env_treespade</td><td>0x7F2E10EB</td><td>No</td></tr>
<tr><td>_global_env_treetropical01</td><td>0xA6D01109</td><td>No</td></tr>
<tr><td>_global_env_treetropical02</td><td>0x04C8563E</td><td>No</td></tr>
<tr><td>_global_explosivebarrel</td><td>0x134DB845</td><td>No</td></tr>
<tr><td>_global_explosivebarrel_crashable</td><td>0x8D42D251</td><td>No</td></tr>
<tr><td>_global_explosivebarrel_Long_Hibernation</td><td>0x08A2350E</td><td>No</td></tr>
<tr><td>_global_fencebarbed</td><td>0x826FBFF3</td><td>No</td></tr>
<tr><td>_global_fencebarbedpole</td><td>0x554EFF2D</td><td>No</td></tr>
<tr><td>_global_fencechain</td><td>0xACCADBF6</td><td>No</td></tr>
<tr><td>_global_fencechaingate</td><td>0x18AFECBF</td><td>No</td></tr>
<tr><td>_global_fencechainlong</td><td>0xF8AF5AE4</td><td>No</td></tr>
<tr><td>_global_fencechainpole</td><td>0xE82A3150</td><td>No</td></tr>
<tr><td>_global_fencechaintarped</td><td>0x5825F792</td><td>No</td></tr>
<tr><td>_global_fencechaintemp</td><td>0x1FA5C33C</td><td>No</td></tr>
<tr><td>_global_fencewoodpanel</td><td>0xF51979AE</td><td>No</td></tr>
<tr><td>_global_files</td><td>0xE6A6AA7D</td><td>No</td></tr>
<tr><td>_global_firehydrantred01</td><td>0x114ACD2A</td><td>No</td></tr>
<tr><td>_global_firehydrantred02</td><td>0x3351BE75</td><td>No</td></tr>
<tr><td>_global_firehydrantyellow01</td><td>0x14139CEB</td><td>No</td></tr>
<tr><td>_global_fireobject</td><td>0xA19AE91D</td><td>No</td></tr>
<tr><td>_global_flag_largeAL</td><td>0xA8B51C6D</td><td>No</td></tr>
<tr><td>_global_flag_largeCH</td><td>0xD962EBF3</td><td>No</td></tr>
<tr><td>_global_flag_largeGR</td><td>0x16535745</td><td>No</td></tr>
<tr><td>_global_flag_largeOC</td><td>0x2317E018</td><td>No</td></tr>
<tr><td>_global_flag_largePR</td><td>0xEA0D185C</td><td>No</td></tr>
<tr><td>_global_flag_largeVZ</td><td>0x6FA6FBCE</td><td>No</td></tr>
<tr><td>_global_flag_smallAL</td><td>0xB4AF1DE5</td><td>No</td></tr>
<tr><td>_global_flag_smallCH</td><td>0x85AC082B</td><td>No</td></tr>
<tr><td>_global_flag_smallGR</td><td>0xE225E48D</td><td>No</td></tr>
<tr><td>_global_flag_smallOC</td><td>0x3F313E70</td><td>No</td></tr>
<tr><td>_global_flag_smallPR</td><td>0x1354A944</td><td>No</td></tr>
<tr><td>_global_flag_smallVZ</td><td>0x99159C26</td><td>No</td></tr>
<tr><td>_global_flag_wallAL</td><td>0x06D1156A</td><td>No</td></tr>
<tr><td>_global_flag_wallCH</td><td>0x57F5D8A0</td><td>No</td></tr>
<tr><td>_global_flag_wallGR</td><td>0x8A13221E</td><td>No</td></tr>
<tr><td>_global_flag_wallOC</td><td>0x754E8CB3</td><td>No</td></tr>
<tr><td>_global_flag_wallPR</td><td>0x3AEA52AB</td><td>No</td></tr>
<tr><td>_global_flarestick</td><td>0x8FBC1B40</td><td>No</td></tr>
<tr><td>_global_fountainsmall</td><td>0xF60D28CD</td><td>No</td></tr>
<tr><td>_global_fountainsmall_ruined</td><td>0x31A393A1</td><td>No</td></tr>
<tr><td>_global_freewayelevatedcurve</td><td>0x63085A76</td><td>No</td></tr>
<tr><td>_global_freewayelevatedlong</td><td>0x0F999C87</td><td>No</td></tr>
<tr><td>_global_freewayelevatedlongramp</td><td>0x2C58D32F</td><td>No</td></tr>
<tr><td>_global_freewayelevatedonofframp</td><td>0x2AA8765D</td><td>No</td></tr>
<tr><td>_global_fruita</td><td>0x5B8FE753</td><td>No</td></tr>
<tr><td>_global_fruitb</td><td>0x819261BC</td><td>No</td></tr>
<tr><td>_global_fruitboxa</td><td>0x7766DA9E</td><td>No</td></tr>
<tr><td>_global_fruitboxb</td><td>0x996DCBE9</td><td>No</td></tr>
<tr><td>_global_fruitboxc</td><td>0x7F6B6464</td><td>No</td></tr>
<tr><td>_global_fruitboxd</td><td>0x21731F2F</td><td>No</td></tr>
<tr><td>_global_fruitboxe</td><td>0xFF70AB12</td><td>No</td></tr>
<tr><td>_global_fruitboxf</td><td>0x8178337D</td><td>No</td></tr>
<tr><td>_global_gateentrance</td><td>0x7E7F8603</td><td>No</td></tr>
<tr><td>_global_gunboxA</td><td>0xD9BF6376</td><td>No</td></tr>
<tr><td>_global_heathaze</td><td>0xDCF17894</td><td>No</td></tr>
<tr><td>_global_intercomA</td><td>0x2C8FF4C2</td><td>No</td></tr>
<tr><td>_global_intercomA (Invincible)</td><td>0xC8FC312A</td><td>No</td></tr>
<tr><td>_global_jugs01</td><td>0x723D6C1C</td><td>No</td></tr>
<tr><td>_global_junkpile01</td><td>0x0B4FA30B</td><td>No</td></tr>
<tr><td>_global_junkpile02</td><td>0x31521D74</td><td>No</td></tr>
<tr><td>_global_junkpile03</td><td>0x0B542039</td><td>No</td></tr>
<tr><td>_global_junkpile04</td><td>0x31569AA2</td><td>No</td></tr>
<tr><td>_global_ladderdockmedium01</td><td>0xDE7B8271</td><td>No</td></tr>
<tr><td>_global_ladderdocksmall01</td><td>0x82980827</td><td>No</td></tr>
<tr><td>_global_lampcablea</td><td>0x0663672A</td><td>No</td></tr>
<tr><td>_global_lamppostA</td><td>0x1380D52D</td><td>No</td></tr>
<tr><td>_global_lamppostB</td><td>0x91794CC2</td><td>No</td></tr>
<tr><td>_global_lamppostmilitary</td><td>0x511ED675</td><td>No</td></tr>
<tr><td>_global_landingpad</td><td>0x80EA4188</td><td>No</td></tr>
<tr><td>_global_liftauto</td><td>0xC0D7BC8E</td><td>No</td></tr>
<tr><td>_global_locker</td><td>0x2AA683EC</td><td>No</td></tr>
<tr><td>_global_market01</td><td>0x0CE95815</td><td>No</td></tr>
<tr><td>_global_market02</td><td>0x6AE19D4A</td><td>No</td></tr>
<tr><td>_global_newspaperbin01</td><td>0xB8974AF5</td><td>No</td></tr>
<tr><td>_global_newspaperbin02</td><td>0x969059AA</td><td>No</td></tr>
<tr><td>_global_newspaperstand01</td><td>0x6038DD9A</td><td>No</td></tr>
<tr><td>_global_pallet</td><td>0x70CD95C2</td><td>No</td></tr>
<tr><td>_global_palletcement</td><td>0x56727392</td><td>No</td></tr>
<tr><td>_global_paperA</td><td>0xC801CA6F</td><td>No</td></tr>
<tr><td>_global_parkinglota</td><td>0x7D2DEB82</td><td>No</td></tr>
<tr><td>_global_parkinglotb</td><td>0xFF3573ED</td><td>No</td></tr>
<tr><td>_global_phone1A</td><td>0x3DD6A3E6</td><td>No</td></tr>
<tr><td>_global_phoneAhandset</td><td>0xD020AF12</td><td>No</td></tr>
<tr><td>_global_pile01</td><td>0xFF908CCD</td><td>No</td></tr>
<tr><td>_global_pile02</td><td>0x7D890462</td><td>No</td></tr>
<tr><td>_global_pile03</td><td>0xDF8BDD3F</td><td>No</td></tr>
<tr><td>_global_pile04</td><td>0x7D848734</td><td>No</td></tr>
<tr><td>_global_pile05</td><td>0x578689F9</td><td>No</td></tr>
<tr><td>_global_pile06</td><td>0xF57F33EE</td><td>No</td></tr>
<tr><td>_global_pile07</td><td>0x57820CCB</td><td>No</td></tr>
<tr><td>_global_pipeunderground</td><td>0x5B8571C3</td><td>No</td></tr>
<tr><td>_global_platform01</td><td>0xE233FB3C</td><td>No</td></tr>
<tr><td>_global_playgroundride01</td><td>0xA768D6C8</td><td>No</td></tr>
<tr><td>_global_playgroundride02</td><td>0xB166A7EF</td><td>No</td></tr>
<tr><td>_global_playgroundride03</td><td>0x8F6433D2</td><td>No</td></tr>
<tr><td>_global_pole</td><td>0xE3CE6D3E</td><td>No</td></tr>
<tr><td>_global_portablelight</td><td>0x96279A17</td><td>No</td></tr>
<tr><td>_global_prisonpen</td><td>0xE5659BE6</td><td>No</td></tr>
<tr><td>_global_propanecannistera</td><td>0x9635E555</td><td>No</td></tr>
<tr><td>_Global_propanetanklargeA</td><td>0x78F605A5</td><td>Yes</td></tr>
<tr><td>_global_propanetanklargeB</td><td>0x16EEAF9A</td><td>Yes</td></tr>
<tr><td>_Global_propanetanksmallA</td><td>0x31F47FC9</td><td>Yes</td></tr>
<tr><td>_global_protestsigna</td><td>0xFF69CD8B</td><td>No</td></tr>
<tr><td>_global_pylon</td><td>0xC30AABEC</td><td>No</td></tr>
<tr><td>_global_racearrow</td><td>0xF3EF35D2</td><td>No</td></tr>
<tr><td>_global_racecheckpoint</td><td>0x64D6F3F5</td><td>No</td></tr>
<tr><td>_global_racefinish</td><td>0x80A127A6</td><td>No</td></tr>
<tr><td>_global_racering</td><td>0xF6DA1881</td><td>No</td></tr>
<tr><td>_global_radioA</td><td>0x371216DE</td><td>No</td></tr>
<tr><td>_global_rail01</td><td>0xCC2EF3B9</td><td>No</td></tr>
<tr><td>_global_railend01</td><td>0x3CE88F26</td><td>No</td></tr>
<tr><td>_global_railend02</td><td>0xBEF01791</td><td>No</td></tr>
<tr><td>_global_raillong</td><td>0xEBB2DE0E</td><td>No</td></tr>
<tr><td>_global_railsmall</td><td>0x4F2A34BD</td><td>No</td></tr>
<tr><td>_global_ramp_roadlessrider</td><td>0x2769DAFA</td><td>No</td></tr>
<tr><td>_global_redoxytank</td><td>0xF0446A31</td><td>Yes</td></tr>
<tr><td>_global_road_parking</td><td>0x305066EF</td><td>No</td></tr>
<tr><td>_global_sandbagscornerAN</td><td>0x31AB4695</td><td>No</td></tr>
<tr><td>_global_sandbagscornerCH</td><td>0x30E42AB9</td><td>No</td></tr>
<tr><td>_global_sandbagscornerGR</td><td>0xED5410DF</td><td>No</td></tr>
<tr><td>_global_sandbagscornerPR</td><td>0xD5E5F96A</td><td>No</td></tr>
<tr><td>_global_sandbagscornerVZ</td><td>0xC6E31610</td><td>No</td></tr>
<tr><td>_global_sandbagscurveda</td><td>0xBB548E31</td><td>No</td></tr>
<tr><td>_global_sandbagscurvedB</td><td>0x394D05C6</td><td>No</td></tr>
<tr><td>_global_sandbagsendAN</td><td>0x070402EF</td><td>No</td></tr>
<tr><td>_global_sandbagsendCH</td><td>0xD8551C43</td><td>No</td></tr>
<tr><td>_global_sandbagsendGR</td><td>0x94F69F35</td><td>No</td></tr>
<tr><td>_global_sandbagsendPR</td><td>0xC62563EC</td><td>No</td></tr>
<tr><td>_global_sandbagsendVZ</td><td>0x4BBF475E</td><td>No</td></tr>
<tr><td>_global_sandbagsstraighta</td><td>0xF902B6F6</td><td>No</td></tr>
<tr><td>_global_sandbagsstraightAN</td><td>0x32B19078</td><td>No</td></tr>
<tr><td>_global_sandbagsstraightCH</td><td>0x0BD11998</td><td>No</td></tr>
<tr><td>_global_sandbagsstraightGR</td><td>0xC040F326</td><td>No</td></tr>
<tr><td>_global_sandbagsstraightPR</td><td>0xF118ED33</td><td>No</td></tr>
<tr><td>_global_sandbagsstraightthinCH</td><td>0x1028601D</td><td>No</td></tr>
<tr><td>_global_sandbagsstraightVZ</td><td>0xA6C6A3ED</td><td>No</td></tr>
<tr><td>_global_satellitedishB</td><td>0xB6FE4907</td><td>No</td></tr>
<tr><td>_global_satellitedishC</td><td>0x94FBD4EA</td><td>No</td></tr>
<tr><td>_global_scaffold</td><td>0x574B85A2</td><td>No</td></tr>
<tr><td>_global_scaffoldB</td><td>0x94958970</td><td>No</td></tr>
<tr><td>_global_scaffoldC</td><td>0xFE986EE5</td><td>No</td></tr>
<tr><td>_global_searchlighta</td><td>0x1C87FDA5</td><td>No</td></tr>
<tr><td>_global_shoppingcartgreen</td><td>0xA52067FF</td><td>No</td></tr>
<tr><td>_global_sign_freeway</td><td>0xC96B930D</td><td>No</td></tr>
<tr><td>_global_sign_road</td><td>0xA489AC9C</td><td>No</td></tr>
<tr><td>_global_sign_road02</td><td>0x8E5D7DC6</td><td>No</td></tr>
<tr><td>_global_signBar</td><td>0x212D279E</td><td>No</td></tr>
<tr><td>_global_signcokea</td><td>0x0CFA647E</td><td>No</td></tr>
<tr><td>_global_signlanemerge</td><td>0xBA2C6ED7</td><td>No</td></tr>
<tr><td>_global_signnouturn</td><td>0xD017AC86</td><td>No</td></tr>
<tr><td>_global_signonewayleft</td><td>0x3A607295</td><td>No</td></tr>
<tr><td>_global_signspeed</td><td>0xDE7C9F10</td><td>No</td></tr>
<tr><td>_global_signstopa</td><td>0x626AC5A8</td><td>No</td></tr>
<tr><td>_global_signtaco</td><td>0x9B5C90E8</td><td>No</td></tr>
<tr><td>_global_soccerball</td><td>0x2C83C3BA</td><td>No</td></tr>
<tr><td>_global_soccergoal</td><td>0x5F51F944</td><td>No</td></tr>
<tr><td>_global_spotlight</td><td>0x52D68644</td><td>No</td></tr>
<tr><td>_global_stain01</td><td>0x87B54AA6</td><td>No</td></tr>
<tr><td>_global_stain02</td><td>0x09BCD311</td><td>No</td></tr>
<tr><td>_global_stain03</td><td>0x0FBA9DEC</td><td>No</td></tr>
<tr><td>_global_stain04</td><td>0x91C22657</td><td>No</td></tr>
<tr><td>_global_stain05</td><td>0x2FBF4D7A</td><td>No</td></tr>
<tr><td>_global_stain06</td><td>0x91C6A385</td><td>No</td></tr>
<tr><td>_global_stain07</td><td>0xA7C48790</td><td>No</td></tr>
<tr><td>_global_stain08</td><td>0x89A404AB</td><td>No</td></tr>
<tr><td>_global_stairsidewalk01</td><td>0x03CFC9A8</td><td>No</td></tr>
<tr><td>_global_stairsidewalk02</td><td>0x8DCCD14F</td><td>No</td></tr>
<tr><td>_global_tablea</td><td>0x842866DD</td><td>No</td></tr>
<tr><td>_global_tableb</td><td>0x0220DE72</td><td>No</td></tr>
<tr><td>_global_tablecafe</td><td>0x905BA26B</td><td>No</td></tr>
<tr><td>_global_tablechess</td><td>0x93F543FC</td><td>No</td></tr>
<tr><td>_global_tablefolding</td><td>0xAE0AB043</td><td>No</td></tr>
<tr><td>_global_tablemarket</td><td>0x6288B184</td><td>No</td></tr>
<tr><td>_global_tableyarda</td><td>0x8B7C8BF9</td><td>No</td></tr>
<tr><td>_global_tanktrap01</td><td>0x12DB78E4</td><td>Yes</td></tr>
<tr><td>_global_telephonebooth</td><td>0x6AD84718</td><td>No</td></tr>
<tr><td>_global_tirelargea</td><td>0xA39928B4</td><td>No</td></tr>
<tr><td>_global_tiresmalla</td><td>0x2CB9FDDC</td><td>No</td></tr>
<tr><td>_global_toolboxa</td><td>0x670CCC62</td><td>No</td></tr>
<tr><td>_global_toolboxb</td><td>0xE91454CD</td><td>No</td></tr>
<tr><td>_global_torchlamp</td><td>0x41DEB854</td><td>No</td></tr>
<tr><td>_global_towerelectrical01</td><td>0x54D169AC</td><td>No</td></tr>
<tr><td>_global_towerlift</td><td>0x3722E4F0</td><td>No</td></tr>
<tr><td>_global_towerliftend</td><td>0xB1937297</td><td>No</td></tr>
<tr><td>_global_trafficlight01</td><td>0x54BF448C</td><td>No</td></tr>
<tr><td>_global_trafficlight02</td><td>0x6EBD2EE3</td><td>No</td></tr>
<tr><td>_global_trafficpath</td><td>0x73C57156</td><td>No</td></tr>
<tr><td>_global_trafficpathIntersection</td><td>0xE2BAE2A5</td><td>No</td></tr>
<tr><td>_global_trashbag01</td><td>0x5D079001</td><td>No</td></tr>
<tr><td>_global_trashcan02</td><td>0x5FAD147A</td><td>No</td></tr>
<tr><td>_global_trashcana</td><td>0xA4CF9C81</td><td>No</td></tr>
<tr><td>_global_trashpile01</td><td>0x0669F143</td><td>No</td></tr>
<tr><td>_global_trashpile02</td><td>0x6C6CD06C</td><td>No</td></tr>
<tr><td>_global_trashpile03</td><td>0x666F0591</td><td>No</td></tr>
<tr><td>_global_treasures</td><td>0x24C69082</td><td>No</td></tr>
<tr><td>_global_vault</td><td>0x2D73145C</td><td>No</td></tr>
<tr><td>_global_vendingmachine01</td><td>0x06C8278F</td><td>No</td></tr>
<tr><td>_global_vendingmachine02</td><td>0x7CCB1FE8</td><td>No</td></tr>
<tr><td>_global_waterbumper</td><td>0x40CAC02C</td><td>No</td></tr>
<tr><td>_global_waterpuddle01</td><td>0x090231B4</td><td>No</td></tr>
<tr><td>_global_waterpuddle02</td><td>0xE2FFB74B</td><td>No</td></tr>
<tr><td>_global_waterpuddle03</td><td>0x80FCDE6E</td><td>No</td></tr>
<tr><td>_global_waterpuddle04</td><td>0x8B0E374D</td><td>No</td></tr>
<tr><td>_global_waterpuddle05</td><td>0x610BB698</td><td>No</td></tr>
<tr><td>_global_waterpuddle06</td><td>0x6B0987BF</td><td>No</td></tr>
<tr><td>_global_waterpuddle07</td><td>0x0906AEE2</td><td>No</td></tr>
<tr><td>_global_waterpuddle08</td><td>0x631885B1</td><td>No</td></tr>
<tr><td>_global_watertowerA</td><td>0x4FB48B91</td><td>No</td></tr>
<tr><td>_global_watertowerB</td><td>0xCDAD0326</td><td>No</td></tr>
<tr><td>_global_watertowerC</td><td>0xEFAF7743</td><td>No</td></tr>
<tr><td>_global_weightbench</td><td>0xC999385E</td><td>No</td></tr>
<tr><td>_global_weightbench (Allied Users)</td><td>0x943DD17C</td><td>No</td></tr>
<tr><td>_global_weightbench (OC Users)</td><td>0xE5B07A0D</td><td>No</td></tr>
<tr><td>_global_wheelbarrel</td><td>0x51E41E7D</td><td>No</td></tr>
<tr><td>_global_yellowoxytank</td><td>0xF5B44E82</td><td>Yes</td></tr>
<tr><td>_GR_veh_truck_m151_static</td><td>0x75626E17</td><td>Yes</td></tr>
<tr><td>_groutpost_bld_alarmtower</td><td>0x91F09A65</td><td>No</td></tr>
<tr><td>_groutpost_bld_bunkerbeetle</td><td>0x235700A5</td><td>No</td></tr>
<tr><td>_groutpost_bld_bunkerconcrete</td><td>0xFCF2821D</td><td>No</td></tr>
<tr><td>_groutpost_bld_bunkersandbag01</td><td>0xC91E4FF9</td><td>No</td></tr>
<tr><td>_groutpost_bld_bunkersemitruck</td><td>0x54D6FD33</td><td>Yes</td></tr>
<tr><td>_groutpost_bld_cranemining</td><td>0xCB0104A6</td><td>No</td></tr>
<tr><td>_groutpost_bld_earthmover</td><td>0x2546BDE8</td><td>No</td></tr>
<tr><td>_groutpost_bld_guardtowertree01</td><td>0xB83C4D78</td><td>No</td></tr>
<tr><td>_groutpost_bld_guardtowertree02</td><td>0x4239551F</td><td>No</td></tr>
<tr><td>_groutpost_bld_guardtowertree03</td><td>0x603745C2</td><td>No</td></tr>
<tr><td>_groutpost_bld_guardtowertree04</td><td>0x3A34CB59</td><td>No</td></tr>
<tr><td>_groutpost_bld_helipad</td><td>0x6D880D42</td><td>Yes</td></tr>
<tr><td>_groutpost_bld_shackbus</td><td>0xF7C17325</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackcave01</td><td>0x851B532F</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackcave01_Ruined</td><td>0x739CBF93</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackcave02</td><td>0x7B1D8208</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackcave03</td><td>0xE520677D</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackcave04</td><td>0xDB0F0E9E</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackcave05</td><td>0xFD1182BB</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackcave05_Ruined</td><td>0x02EE2F5F</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackcave06</td><td>0xE3139864</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackfuselarge</td><td>0x50479153</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackperm01</td><td>0xA199B59A</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackperm02</td><td>0x03A10BA5</td><td>No</td></tr>
<tr><td>_groutpost_bld_shackperm03</td><td>0x999E2630</td><td>No</td></tr>
<tr><td>_groutpost_bld_shacksemiperm01</td><td>0x76EB6924</td><td>No</td></tr>
<tr><td>_groutpost_bld_shacktall01</td><td>0xB7801ADD</td><td>No</td></tr>
<tr><td>_groutpost_bld_shacktall02</td><td>0x35789272</td><td>No</td></tr>
<tr><td>_groutpost_bld_shacktall02_Ruined</td><td>0x22BDE268</td><td>No</td></tr>
<tr><td>_groutpost_bld_tentlargetarp</td><td>0x9D7242FA</td><td>No</td></tr>
<tr><td>_groutpost_bld_tentlargetarp02</td><td>0xC8CA7210</td><td>No</td></tr>
<tr><td>_groutpost_bld_tentlargetarp03</td><td>0xB2CC8E05</td><td>No</td></tr>
<tr><td>_groutpost_bld_tentsmalltarp</td><td>0x4A0510FE</td><td>No</td></tr>
<tr><td>_groutpost_bld_tentsmalltarp02</td><td>0x271F1024</td><td>No</td></tr>
<tr><td>_groutpost_bld_tentsmalltarp03</td><td>0x412177A9</td><td>No</td></tr>
<tr><td>_groutpost_bld_trailerhut01</td><td>0x7394A08A</td><td>No</td></tr>
<tr><td>_groutpost_bld_trailerhut02</td><td>0x159C5B55</td><td>No</td></tr>
<tr><td>_groutpost_env_cave</td><td>0xE9D90E55</td><td>No</td></tr>
<tr><td>_groutpost_env_junglewall</td><td>0x41175AA1</td><td>No</td></tr>
<tr><td>_groutpost_env_junglewall02</td><td>0xC51D03BB</td><td>No</td></tr>
<tr><td>_groutpost_env_junglewallcornerleft</td><td>0x66955CED</td><td>No</td></tr>
<tr><td>_groutpost_env_junglewallcornerleft02</td><td>0x3F7BC827</td><td>No</td></tr>
<tr><td>_groutpost_env_junglewallcornerright</td><td>0x7998D38C</td><td>No</td></tr>
<tr><td>_groutpost_env_junglewallcornerright02</td><td>0x3489F276</td><td>No</td></tr>
<tr><td>_groutpost_env_minewall</td><td>0x324BF23F</td><td>No</td></tr>
<tr><td>_groutpost_env_minewall6left</td><td>0x64327318</td><td>No</td></tr>
<tr><td>_groutpost_env_minewall6right</td><td>0xEA946FBF</td><td>No</td></tr>
<tr><td>_groutpost_env_minewallcorner16left</td><td>0x6E10B75A</td><td>No</td></tr>
<tr><td>_groutpost_env_minewallcorner16right</td><td>0xB656FA31</td><td>No</td></tr>
<tr><td>_groutpost_env_minewallcorner32left</td><td>0x2C34A64C</td><td>No</td></tr>
<tr><td>_groutpost_env_minewallcorner32right</td><td>0x4FFC198B</td><td>No</td></tr>
<tr><td>_groutpost_env_minewalldrop01</td><td>0x09A03249</td><td>No</td></tr>
<tr><td>_groutpost_env_minewalldrop02</td><td>0x6798777E</td><td>No</td></tr>
<tr><td>_groutpost_env_minewallintersection16</td><td>0x31866C35</td><td>No</td></tr>
<tr><td>_groutpost_env_minewallintersection32</td><td>0x4F070FBB</td><td>No</td></tr>
<tr><td>_groutpost_env_minewallrise01</td><td>0xDD1B6775</td><td>No</td></tr>
<tr><td>_groutpost_env_minewallrise02</td><td>0xBB14762A</td><td>No</td></tr>
<tr><td>_groutpost_env_minewallshort</td><td>0x0B233177</td><td>No</td></tr>
<tr><td>_groutpost_env_minewalltall</td><td>0x93BEB496</td><td>No</td></tr>
<tr><td>_groutpost_fueltanks</td><td>0xB673F35D</td><td>Yes</td></tr>
<tr><td>_groutpost_interior_job</td><td>0x0441D0EA</td><td>No</td></tr>
<tr><td>_groutpost_mine_road10</td><td>0x4A2188EB</td><td>No</td></tr>
<tr><td>_groutpost_mine_road10i</td><td>0x192E27FC</td><td>No</td></tr>
<tr><td>_groutpost_mine_road10merge</td><td>0xD13BAE81</td><td>No</td></tr>
<tr><td>_groutpost_mine_road10T</td><td>0x1B4E7ECD</td><td>No</td></tr>
<tr><td>_groutpost_mine_road20U</td><td>0x4E096A37</td><td>No</td></tr>
<tr><td>_groutpost_podium</td><td>0x1E20A092</td><td>No</td></tr>
<tr><td>_groutpost_podium (speaker)</td><td>0x0A17EC1A</td><td>No</td></tr>
<tr><td>_guanare_bridgeorinoco</td><td>0x3F2D24A2</td><td>No</td></tr>
<tr><td>_guanare_bridgeorinocosupport</td><td>0x7D29156B</td><td>No</td></tr>
<tr><td>_guerilla_chaira</td><td>0x88AA3BDA</td><td>No</td></tr>
<tr><td>_guerilla_chairb</td><td>0xEAB191E5</td><td>No</td></tr>
<tr><td>_guerilla_chairc</td><td>0x80AEAC70</td><td>No</td></tr>
<tr><td>_guerilla_junker</td><td>0x5DE6C75D</td><td>No</td></tr>
<tr><td>_guerilla_junker_full</td><td>0x3E8893A7</td><td>No</td></tr>
<tr><td>_guerilla_junker_hood</td><td>0x50C4CEFA</td><td>No</td></tr>
<tr><td>_guerilla_junker_tire</td><td>0x03A2CCCE</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargeangle</td><td>0x5862432E</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargeangle_AllCon002</td><td>0x69EF2FEC</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargecap</td><td>0x7456859B</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargecap_AllCon002</td><td>0x8D26404D</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargeL</td><td>0x005B049B</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargeL_AllCon002</td><td>0xCAD0374D</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargeshort</td><td>0x5D09CD45</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargeshort_AllCon002</td><td>0x49F953DB</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargeY</td><td>0x068A6C42</td><td>No</td></tr>
<tr><td>_industrial_att_pipelargeY_AllCon002</td><td>0xDF7457D8</td><td>No</td></tr>
<tr><td>_Industrial_bld_conveyorbelt</td><td>0x1B770D31</td><td>No</td></tr>
<tr><td>_Industrial_bld_conveyorbeltangle</td><td>0x3604CE92</td><td>No</td></tr>
<tr><td>_Industrial_bld_conveyortransition</td><td>0x9F85B48B</td><td>No</td></tr>
<tr><td>_industrial_bld_domerefinery</td><td>0x58619CC4</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstation01</td><td>0xC72905CD</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstation01_ruined</td><td>0x9C6142A1</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstation02</td><td>0x45217D62</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstation02_ruined</td><td>0x945F9B58</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstation_bathroom</td><td>0x059D6F15</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstationpump01</td><td>0x40B92BD7</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstationpump01_ruined</td><td>0xDAB6C0DB</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstationpump02</td><td>0x56BB8D10</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstationpump02_ruined</td><td>0xD5CC807E</td><td>No</td></tr>
<tr><td>_industrial_bld_gasstationpump03</td><td>0x40BDA905</td><td>No</td></tr>
<tr><td>_industrial_bld_hangar01</td><td>0x3F8A1245</td><td>No</td></tr>
<tr><td>_industrial_bld_hangar01_ruined</td><td>0x7F0DB5D9</td><td>No</td></tr>
<tr><td>_industrial_bld_oilrig</td><td>0x69064E47</td><td>No</td></tr>
<tr><td>_industrial_bld_refinery01</td><td>0x77F5D454</td><td>No</td></tr>
<tr><td>_industrial_bld_refinery02</td><td>0x51F359EB</td><td>No</td></tr>
<tr><td>_industrial_bld_refinery03</td><td>0x6FF14A8E</td><td>No</td></tr>
<tr><td>_industrial_bld_refinery04</td><td>0x7A02A36D</td><td>No</td></tr>
<tr><td>_industrial_bld_refinery04_Ruined</td><td>0xA5A15741</td><td>No</td></tr>
<tr><td>_industrial_bld_refinery05</td><td>0x500022B8</td><td>No</td></tr>
<tr><td>_industrial_bld_refinery06</td><td>0xD9FD2A5F</td><td>No</td></tr>
<tr><td>_industrial_bld_silosmall</td><td>0x2C587443</td><td>No</td></tr>
<tr><td>_industrial_bld_silowide</td><td>0x4805C763</td><td>No</td></tr>
<tr><td>_industrial_bld_smokestack</td><td>0x003BFA08</td><td>No</td></tr>
<tr><td>_industrial_bld_towerrefinerysmall</td><td>0x9B3946BD</td><td>No</td></tr>
<tr><td>_industrial_bld_towerrefinerytall</td><td>0xB4F3B8CD</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse01</td><td>0xC9CA213B</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse01_Ruined</td><td>0xB56796DF</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse02</td><td>0xAFCC36E4</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse02_Ruined</td><td>0xD70C7FF2</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse03</td><td>0xC9CE9E69</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse03 dangerous1</td><td>0x0EBCB5A6</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse04</td><td>0x2FD17D92</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse05</td><td>0x51D3F1AF</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse05_ruined</td><td>0x26162713</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse06</td><td>0x47D62088</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouse06_ruined</td><td>0xFBF51E96</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouselarge01</td><td>0x502033FA</td><td>No</td></tr>
<tr><td>_industrial_bld_warehouselarge02</td><td>0xB2278A05</td><td>No</td></tr>
<tr><td>_industrial_bld_warehousesmall01</td><td>0xF6CA7CC2</td><td>No</td></tr>
<tr><td>_industrial_bld_warehousesmall01_ruined</td><td>0xCFC34938</td><td>No</td></tr>
<tr><td>_industrial_bld_warehousesmall02</td><td>0x78D2052D</td><td>No</td></tr>
<tr><td>_industrial_bld_warehousesmall02_ruined</td><td>0x817D0F01</td><td>No</td></tr>
<tr><td>_industrial_cart</td><td>0x0AA399A2</td><td>No</td></tr>
<tr><td>_industrial_cartlong</td><td>0x668B6350</td><td>No</td></tr>
<tr><td>_industrial_cartribbed</td><td>0x59B8430E</td><td>No</td></tr>
<tr><td>_industrial_cartsmelting</td><td>0xFABD4EF1</td><td>No</td></tr>
<tr><td>_industrial_catwalkangle</td><td>0x355BE790</td><td>No</td></tr>
<tr><td>_industrial_catwalkcap</td><td>0xBE72DD61</td><td>No</td></tr>
<tr><td>_industrial_catwalkl</td><td>0xB847F33D</td><td>No</td></tr>
<tr><td>_industrial_catwalkshort</td><td>0x4B6F2993</td><td>No</td></tr>
<tr><td>_industrial_catwalkstraight</td><td>0xA08E2DE9</td><td>No</td></tr>
<tr><td>_industrial_generator01</td><td>0x86CE46A6</td><td>No</td></tr>
<tr><td>_industrial_lamppost01</td><td>0xBC6A1C9D</td><td>No</td></tr>
<tr><td>_industrial_lamppost02</td><td>0x3A629432</td><td>No</td></tr>
<tr><td>_industrial_machineparts01</td><td>0xE63456EE</td><td>No</td></tr>
<tr><td>_industrial_machineparts02</td><td>0x483BACF9</td><td>No</td></tr>
<tr><td>_industrial_machineparts03</td><td>0x6E39AA34</td><td>No</td></tr>
<tr><td>_industrial_machinepartsramp01</td><td>0x4EA9DACE</td><td>No</td></tr>
<tr><td>_Industrial_pipe12m</td><td>0x9C48CA52</td><td>No</td></tr>
<tr><td>_Industrial_pipe20m</td><td>0xB55C960F</td><td>No</td></tr>
<tr><td>_Industrial_pipe4m</td><td>0xE885A2ED</td><td>No</td></tr>
<tr><td>_Industrial_pipecurveSide</td><td>0x5D683004</td><td>No</td></tr>
<tr><td>_Industrial_pipecurveUpdown</td><td>0x8DF7DF8A</td><td>No</td></tr>
<tr><td>_industrial_pipeground01</td><td>0x7B544FF0</td><td>No</td></tr>
<tr><td>_industrial_pipesstacked</td><td>0x9FDB14BA</td><td>No</td></tr>
<tr><td>_Industrial_pipesupport12m</td><td>0x1978C889</td><td>No</td></tr>
<tr><td>_Industrial_pipesupport16m</td><td>0x53EA4DAD</td><td>No</td></tr>
<tr><td>_Industrial_pipesupport8m</td><td>0x4FE22CC0</td><td>No</td></tr>
<tr><td>_industrial_signgasshort</td><td>0x6F91415C</td><td>No</td></tr>
<tr><td>_industrial_signgastall</td><td>0xE8ED678B</td><td>No</td></tr>
<tr><td>_industrial_track</td><td>0x30A9B545</td><td>No</td></tr>
<tr><td>_industrial_trackcurve</td><td>0xCD43AA92</td><td>No</td></tr>
<tr><td>_industrial_trackstop</td><td>0x0C375955</td><td>No</td></tr>
<tr><td>_industrial_trackstraight</td><td>0x3204223F</td><td>No</td></tr>
<tr><td>_island_att_battlement</td><td>0xB8E09698</td><td>No</td></tr>
<tr><td>_island_bld_boothrefreshments01</td><td>0xA0EAE0E8</td><td>No</td></tr>
<tr><td>_island_bld_boothrefreshments01_ruined</td><td>0xDB0B3D76</td><td>No</td></tr>
<tr><td>_island_bld_boothrental</td><td>0xEB999BF3</td><td>No</td></tr>
<tr><td>_island_bld_bridge01</td><td>0xB98FEEC9</td><td>No</td></tr>
<tr><td>_island_bld_bridge01_ruined</td><td>0xCACC33DD</td><td>No</td></tr>
<tr><td>_island_bld_fortress01</td><td>0x8A35B530</td><td>No</td></tr>
<tr><td>_island_bld_fortress01_ruined</td><td>0xD8F0519E</td><td>No</td></tr>
<tr><td>_island_bld_hutmodern01</td><td>0x84ECA286</td><td>No</td></tr>
<tr><td>_island_bld_hutmodern01_ruined</td><td>0x7E118C8C</td><td>No</td></tr>
<tr><td>_island_bld_tower01</td><td>0x62E28227</td><td>No</td></tr>
<tr><td>_island_bld_tower01_ruined</td><td>0x6235146B</td><td>No</td></tr>
<tr><td>_island_wallangled</td><td>0xC0260DB5</td><td>No</td></tr>
<tr><td>_island_wallangled_ruined</td><td>0x702E42C9</td><td>No</td></tr>
<tr><td>_island_wallcorner</td><td>0x1CA8196D</td><td>No</td></tr>
<tr><td>_island_wallcorner_ruined</td><td>0xC2440941</td><td>No</td></tr>
<tr><td>_island_wallend</td><td>0x29A43585</td><td>No</td></tr>
<tr><td>_island_wallend_ruined</td><td>0x070DD819</td><td>No</td></tr>
<tr><td>_island_wallstraight</td><td>0x3AC713AC</td><td>No</td></tr>
<tr><td>_island_wallstraight_ruined</td><td>0xDD26EC9A</td><td>No</td></tr>
<tr><td>_island_wallT</td><td>0x66D2981A</td><td>No</td></tr>
<tr><td>_island_wallT_ruined</td><td>0x27349990</td><td>No</td></tr>
<tr><td>_jungle_bld_ruinshotelback</td><td>0x975027B3</td><td>No</td></tr>
<tr><td>_jungle_bld_ruinshotelback_ruined</td><td>0x73CAD1B7</td><td>No</td></tr>
<tr><td>_Jungle_bld_ruinshotelcorner</td><td>0x1B24B935</td><td>No</td></tr>
<tr><td>_Jungle_bld_ruinshotelcorner_ruined</td><td>0x1F026949</td><td>No</td></tr>
<tr><td>_jungle_bld_ruinshotelfront</td><td>0x0A152D47</td><td>No</td></tr>
<tr><td>_jungle_bld_ruinshotelfront_ruined</td><td>0xF498950B</td><td>No</td></tr>
<tr><td>_jungle_bld_ruinshotelside</td><td>0xAA42BA23</td><td>No</td></tr>
<tr><td>_jungle_bld_ruinshotelside_ruined</td><td>0x15CF9127</td><td>No</td></tr>
<tr><td>_jungle_bridge_metalvehicleA</td><td>0x34ED110C</td><td>No</td></tr>
<tr><td>_jungle_bridge_woodpedestrianA</td><td>0xBF5FF99D</td><td>No</td></tr>
<tr><td>_jungle_env_background01</td><td>0x88F2A743</td><td>No</td></tr>
<tr><td>_jungle_env_bushlarge01</td><td>0x933DB7B4</td><td>No</td></tr>
<tr><td>_jungle_env_bushlarge02</td><td>0x6D3B3D4B</td><td>No</td></tr>
<tr><td>_jungle_env_bushlarge03</td><td>0x0B38646E</td><td>No</td></tr>
<tr><td>_jungle_env_bushmedium01</td><td>0x4215F558</td><td>No</td></tr>
<tr><td>_jungle_env_bushmedium02</td><td>0x4C13C67F</td><td>No</td></tr>
<tr><td>_jungle_env_bushmedium03</td><td>0xEA10EDA2</td><td>No</td></tr>
<tr><td>_jungle_env_bushsmall01</td><td>0x86C5B570</td><td>No</td></tr>
<tr><td>_jungle_env_bushsmall02</td><td>0x70C35437</td><td>No</td></tr>
<tr><td>_jungle_env_bushsmall03</td><td>0x8EC144DA</td><td>No</td></tr>
<tr><td>_jungle_env_junglewallfoliage01</td><td>0x81B99A1B</td><td>No</td></tr>
<tr><td>_jungle_env_junglewallfoliage02</td><td>0xE7BC7944</td><td>No</td></tr>
<tr><td>_jungle_env_junglewallfoliage03</td><td>0x01BEE0C9</td><td>No</td></tr>
<tr><td>_jungle_env_junglewallfoliage04</td><td>0xE7C0F672</td><td>No</td></tr>
<tr><td>_jungle_env_largecanopy01</td><td>0xC69265EE</td><td>No</td></tr>
<tr><td>_jungle_env_largecanopy01_standalone</td><td>0xA6246CCC</td><td>No</td></tr>
<tr><td>_jungle_env_plantlarge01</td><td>0xE2F627AB</td><td>No</td></tr>
<tr><td>_jungle_env_plantlarge02</td><td>0x08F8A214</td><td>No</td></tr>
<tr><td>_jungle_env_plantlarge04</td><td>0x88FDE8C2</td><td>No</td></tr>
<tr><td>_jungle_env_plantmed01</td><td>0xAC787460</td><td>No</td></tr>
<tr><td>_jungle_env_plantmed03</td><td>0x34733A4A</td><td>No</td></tr>
<tr><td>_jungle_env_plantsmall02</td><td>0x90EACF9C</td><td>No</td></tr>
<tr><td>_jungle_env_plantsmall03</td><td>0x8AED04C1</td><td>No</td></tr>
<tr><td>_Jungle_env_rockhuge01</td><td>0xE4600495</td><td>No</td></tr>
<tr><td>_Jungle_env_rockhuge02</td><td>0x425849CA</td><td>No</td></tr>
<tr><td>_jungle_env_rocklarge01</td><td>0x2165017F</td><td>No</td></tr>
<tr><td>_jungle_env_rocklarge02</td><td>0x17673058</td><td>No</td></tr>
<tr><td>_jungle_env_rocklarge03</td><td>0x4169B10D</td><td>No</td></tr>
<tr><td>_jungle_env_rockmedium01</td><td>0xD7F8BD21</td><td>No</td></tr>
<tr><td>_jungle_env_rockmedium02</td><td>0x55F134B6</td><td>No</td></tr>
<tr><td>_jungle_env_rockmedium03</td><td>0x37F34413</td><td>No</td></tr>
<tr><td>_jungle_env_rocksmall01</td><td>0xA158FFB7</td><td>No</td></tr>
<tr><td>_jungle_env_rocksmall02</td><td>0xB75B60F0</td><td>No</td></tr>
<tr><td>_jungle_env_rocksmall03</td><td>0x215E4665</td><td>No</td></tr>
<tr><td>_jungle_env_smallcanopy01</td><td>0x4BDD9516</td><td>No</td></tr>
<tr><td>_jungle_env_smallcanopy02</td><td>0xCDE51D81</td><td>No</td></tr>
<tr><td>_jungle_env_treecanopy01</td><td>0x1BDD901B</td><td>No</td></tr>
<tr><td>_jungle_env_treecanopy02</td><td>0x81E06F44</td><td>No</td></tr>
<tr><td>_jungle_env_treemedium01</td><td>0xB5D32B06</td><td>No</td></tr>
<tr><td>_jungle_env_treemedium03</td><td>0xBDD7B4CC</td><td>No</td></tr>
<tr><td>_jungle_env_treesmall01</td><td>0x4555E076</td><td>No</td></tr>
<tr><td>_jungle_env_treesmall02</td><td>0xC75D68E1</td><td>No</td></tr>
<tr><td>_jungle_env_treesmall03</td><td>0x4D5A6A3C</td><td>No</td></tr>
<tr><td>_jungle_env_treetall01</td><td>0x43D0ACEE</td><td>No</td></tr>
<tr><td>_jungle_env_treetall01_standalone</td><td>0xBF94D9CC</td><td>No</td></tr>
<tr><td>_jungle_env_treetall02</td><td>0xA5D802F9</td><td>No</td></tr>
<tr><td>_jungle_env_treetall02_standalone</td><td>0x4FE46019</td><td>No</td></tr>
<tr><td>_jungle_env_treetall03</td><td>0xCBD60034</td><td>No</td></tr>
<tr><td>_jungle_env_treetall03_standalone</td><td>0x8B40409A</td><td>No</td></tr>
<tr><td>_jungle_env_treethin01</td><td>0xED2D89EA</td><td>No</td></tr>
<tr><td>_jungle_env_treethin02</td><td>0x0F347B35</td><td>No</td></tr>
<tr><td>_jungle_env_treethin03</td><td>0xE531FA80</td><td>No</td></tr>
<tr><td>_jungle_env_vines01</td><td>0xD4D2A838</td><td>No</td></tr>
<tr><td>_jungle_env_vines02</td><td>0x5ECFAFDF</td><td>No</td></tr>
<tr><td>_jungle_fountainruinshotel</td><td>0xFA7C4323</td><td>No</td></tr>
<tr><td>_jungle_fountainruinshotel_ruined</td><td>0xE874E427</td><td>No</td></tr>
<tr><td>_jungle_guardgate</td><td>0x259E3704</td><td>No</td></tr>
<tr><td>_jungle_road10</td><td>0xDFBEBCAB</td><td>No</td></tr>
<tr><td>_jungle_road10cross</td><td>0x611C61E1</td><td>No</td></tr>
<tr><td>_jungle_road10cross5</td><td>0x3074D9F2</td><td>No</td></tr>
<tr><td>_jungle_road10merge</td><td>0xD963C641</td><td>No</td></tr>
<tr><td>_jungle_road10mergeOutskirt</td><td>0x4D40C974</td><td>No</td></tr>
<tr><td>_jungle_road10straight</td><td>0xD8ECD1C1</td><td>No</td></tr>
<tr><td>_jungle_road10t</td><td>0x63042A8D</td><td>No</td></tr>
<tr><td>_jungle_road10t20</td><td>0xECEC885F</td><td>No</td></tr>
<tr><td>_jungle_road10t5</td><td>0xFC426B5E</td><td>No</td></tr>
<tr><td>_jungle_road20</td><td>0x170A8FE6</td><td>No</td></tr>
<tr><td>_jungle_road20cross10</td><td>0x6AE0E589</td><td>No</td></tr>
<tr><td>_jungle_road20t10</td><td>0x5FA3BB15</td><td>No</td></tr>
<tr><td>_jungle_road5</td><td>0x03D76EA5</td><td>No</td></tr>
<tr><td>_jungle_road5cross</td><td>0x8942178B</td><td>No</td></tr>
<tr><td>_jungle_road5t</td><td>0xB2B0ECC3</td><td>No</td></tr>
<tr><td>_jungle_road5transition</td><td>0x8FEB7E30</td><td>No</td></tr>
<tr><td>_jungle_ruinshotelarch</td><td>0x2DC0C04B</td><td>No</td></tr>
<tr><td>_jungle_ruinshotelarch_ruined</td><td>0x09C4CDAF</td><td>No</td></tr>
<tr><td>_jungle_ruinshotelpool</td><td>0x40D01C25</td><td>No</td></tr>
<tr><td>_jungle_ruinsplane01_back</td><td>0x47C9ED04</td><td>No</td></tr>
<tr><td>_jungle_ruinsplane01_front</td><td>0xBAE40F9A</td><td>No</td></tr>
<tr><td>_jungle_ruinsplane01_mid</td><td>0xF85966F1</td><td>No</td></tr>
<tr><td>_jungle_ruinsplane01_wing</td><td>0x52D8EC44</td><td>No</td></tr>
<tr><td>_jungle_wallgate</td><td>0x0736675F</td><td>No</td></tr>
<tr><td>_lwcommercial_road10</td><td>0x1585ED61</td><td>No</td></tr>
<tr><td>_lwcommercial_road10cross</td><td>0x998A7847</td><td>No</td></tr>
<tr><td>_lwcommercial_road10cross5</td><td>0x1FB8AA84</td><td>No</td></tr>
<tr><td>_lwcommercial_road10l</td><td>0x35787A97</td><td>No</td></tr>
<tr><td>_lwcommercial_road10t</td><td>0x553C82CF</td><td>No</td></tr>
<tr><td>_lwcommercial_road10t5</td><td>0x3126673C</td><td>No</td></tr>
<tr><td>_lwcommercial_road20</td><td>0x815A6890</td><td>No</td></tr>
<tr><td>_lwcommercial_road20cross</td><td>0xE00401B0</td><td>No</td></tr>
<tr><td>_lwcommercial_road20cross10</td><td>0xF9788E5B</td><td>No</td></tr>
<tr><td>_lwcommercial_road20t10</td><td>0xAFA2E1AB</td><td>No</td></tr>
<tr><td>_lwcommercial_road5</td><td>0x454AEE97</td><td>No</td></tr>
<tr><td>_lwcommercial_road5cross</td><td>0x79DDB93D</td><td>No</td></tr>
<tr><td>_lwcommercial_road5l</td><td>0xC951E601</td><td>No</td></tr>
<tr><td>_lwcommercial_road5t</td><td>0x296604D9</td><td>No</td></tr>
<tr><td>_lwcommercial_road5t10</td><td>0xBB9E9E86</td><td>No</td></tr>
<tr><td>_lwcommercial_wallshort</td><td>0x8536E25A</td><td>No</td></tr>
<tr><td>_lwcommericial_sidewalk</td><td>0x09956D5D</td><td>No</td></tr>
<tr><td>_mar_commercial_road10</td><td>0x91F629C1</td><td>No</td></tr>
<tr><td>_mar_commercial_road10CleanT20</td><td>0x74DF8F86</td><td>No</td></tr>
<tr><td>_mar_commercial_road10CleanT20b</td><td>0x48A1801C</td><td>No</td></tr>
<tr><td>_mar_commercial_road10cross</td><td>0xC3E48B27</td><td>No</td></tr>
<tr><td>_mar_commercial_road10cross5</td><td>0x6B83FC64</td><td>No</td></tr>
<tr><td>_mar_commercial_road10L</td><td>0x38E9EC77</td><td>No</td></tr>
<tr><td>_mar_commercial_road10middle</td><td>0x7EEB16A2</td><td>No</td></tr>
<tr><td>_mar_commercial_road10T</td><td>0xD8AEBE2F</td><td>No</td></tr>
<tr><td>_mar_commercial_road10T5</td><td>0xBDFA441C</td><td>No</td></tr>
<tr><td>_mar_commercial_road20</td><td>0xFC8D7070</td><td>No</td></tr>
<tr><td>_mar_commercial_road20b</td><td>0xCC1D6246</td><td>No</td></tr>
<tr><td>_mar_commercial_road20Clean</td><td>0x712FF8A7</td><td>No</td></tr>
<tr><td>_mar_commercial_road20Cleanb</td><td>0x3C0F587F</td><td>No</td></tr>
<tr><td>_mar_commercial_road20Cleancross</td><td>0xAA7D480D</td><td>No</td></tr>
<tr><td>_mar_commercial_road20Cleancross10</td><td>0x87F4A77A</td><td>No</td></tr>
<tr><td>_mar_commercial_road20CleanT</td><td>0x53E25EA9</td><td>No</td></tr>
<tr><td>_mar_commercial_road20CleanT10</td><td>0xA28513D6</td><td>No</td></tr>
<tr><td>_mar_commercial_road20CleanTn10</td><td>0x0B479E3A</td><td>No</td></tr>
<tr><td>_mar_commercial_road5</td><td>0x97C83377</td><td>No</td></tr>
<tr><td>_mar_commercial_road5cross</td><td>0x2EF8BE9D</td><td>No</td></tr>
<tr><td>_mar_commercial_road5L</td><td>0xC5C2EBE1</td><td>No</td></tr>
<tr><td>_mar_commercial_road5T</td><td>0xA5D64139</td><td>No</td></tr>
<tr><td>_mar_commercial_road5T10</td><td>0x3BCB5766</td><td>No</td></tr>
<tr><td>_mar_commercial_roadgovnt</td><td>0x3BDDA0B0</td><td>No</td></tr>
<tr><td>_mar_commercial_roadstraight10</td><td>0xD7555B37</td><td>No</td></tr>
<tr><td>_mar_commercial_roadstraight10_crater02</td><td>0x29AC88F1</td><td>No</td></tr>
<tr><td>_mar_commercial_roadstraight10_crater02_straight</td><td>0x92BB2EDA</td><td>No</td></tr>
<tr><td>_mar_commercial_roadstraight20</td><td>0x8E524612</td><td>No</td></tr>
<tr><td>_mar_commercial_roadstraight20_crater02</td><td>0x406C869A</td><td>No</td></tr>
<tr><td>_mar_commercial_roadstraight20b</td><td>0xA2F94540</td><td>No</td></tr>
<tr><td>_mar_commercial_roadstraight5</td><td>0x6762E351</td><td>No</td></tr>
<tr><td>_mar_commercial_sidewalk</td><td>0x8B20070A</td><td>No</td></tr>
<tr><td>_mar_commercial_sidewalksmall</td><td>0x8C838753</td><td>No</td></tr>
<tr><td>_mar_global_freewayelevatedcurve</td><td>0x280EE8BB</td><td>No</td></tr>
<tr><td>_mar_global_freewayelevatedlong</td><td>0x4D4BBB94</td><td>No</td></tr>
<tr><td>_mar_global_freewayelevatedlongramp</td><td>0xB7D50350</td><td>No</td></tr>
<tr><td>_maracaibo_bld_civic02</td><td>0xA7C99C9D</td><td>No</td></tr>
<tr><td>_maracaibo_bld_civic02_ruined</td><td>0x77B548B1</td><td>No</td></tr>
<tr><td>_maracaibo_bld_corner16x32A</td><td>0xC62F60FD</td><td>No</td></tr>
<tr><td>_maracaibo_bld_corner16x32A_ruined</td><td>0x7F3E0211</td><td>No</td></tr>
<tr><td>_maracaibo_bld_corner16x32B</td><td>0x4427D892</td><td>No</td></tr>
<tr><td>_maracaibo_bld_corner32x32A</td><td>0x96BE4F13</td><td>No</td></tr>
<tr><td>_maracaibo_bld_corner32x32A_ruined</td><td>0x18844117</td><td>No</td></tr>
<tr><td>_maracaibo_bld_corner32x32B</td><td>0xBCC0C97C</td><td>No</td></tr>
<tr><td>_maracaibo_bld_corner32x32B_ruined</td><td>0x45E7C96A</td><td>No</td></tr>
<tr><td>_maracaibo_bld_firestation01</td><td>0xF46E2154</td><td>No</td></tr>
<tr><td>_maracaibo_bld_firestation01_ruined</td><td>0x5653AD62</td><td>No</td></tr>
<tr><td>_maracaibo_bld_gasstation02</td><td>0xDB2D4070</td><td>No</td></tr>
<tr><td>_maracaibo_bld_gasstationpump02</td><td>0x7AFCD1DE</td><td>No</td></tr>
<tr><td>_maracaibo_bld_historical01</td><td>0xB884051E</td><td>No</td></tr>
<tr><td>_maracaibo_bld_historical01_ruined</td><td>0xAEB40DC4</td><td>No</td></tr>
<tr><td>_maracaibo_bld_historical02</td><td>0xDA8AF669</td><td>No</td></tr>
<tr><td>_maracaibo_bld_historical02_ruined</td><td>0x6C7B7E7D</td><td>No</td></tr>
<tr><td>_maracaibo_bld_hospital01</td><td>0xFD7C87F8</td><td>No</td></tr>
<tr><td>_maracaibo_bld_hospital01_ruined</td><td>0x45A39DC6</td><td>No</td></tr>
<tr><td>_maracaibo_bld_parkingstructure01</td><td>0x3458A081</td><td>No</td></tr>
<tr><td>_maracaibo_bld_parkingstructure01_ruined</td><td>0x9422BDD5</td><td>No</td></tr>
<tr><td>_maracaibo_bld_parkingstructure02</td><td>0xB2511816</td><td>No</td></tr>
<tr><td>_maracaibo_bld_parkingstructure02_ruined</td><td>0x62B3989C</td><td>No</td></tr>
<tr><td>_maracaibo_bld_segment16x32A</td><td>0x5BE0647B</td><td>No</td></tr>
<tr><td>_maracaibo_bld_segment16x32A_ruined</td><td>0xB6EA311F</td><td>No</td></tr>
<tr><td>_maracaibo_bld_segment32x32A</td><td>0x8FE89365</td><td>No</td></tr>
<tr><td>_maracaibo_bld_segment32x32a_ruined</td><td>0x24A9ADF9</td><td>No</td></tr>
<tr><td>_Maracaibo_bld_skyscraper01</td><td>0xEE40C9D5</td><td>No</td></tr>
<tr><td>_Maracaibo_bld_skyscraper01_ruined</td><td>0x0381E6E9</td><td>No</td></tr>
<tr><td>_maracaibo_bld_skyscraper02</td><td>0x4C390F0A</td><td>No</td></tr>
<tr><td>_maracaibo_bld_skyscraper02_ruined</td><td>0x251BB000</td><td>No</td></tr>
<tr><td>_maracaibo_bld_skyscraper03</td><td>0x6E3B8327</td><td>No</td></tr>
<tr><td>_maracaibo_bld_skyscraper03_ruined</td><td>0xD3D50F6B</td><td>No</td></tr>
<tr><td>_maracaibo_bld_stagerepublica</td><td>0xFCC16614</td><td>No</td></tr>
<tr><td>_maracaibo_bld_stagerepublica_ruined</td><td>0xEBD16222</td><td>No</td></tr>
<tr><td>_maracaibo_bridge_segmenta</td><td>0xCA48F45C</td><td>No</td></tr>
<tr><td>_maracaibo_bridge_segmenta_ruined</td><td>0xE17AD34A</td><td>No</td></tr>
<tr><td>_maracaibo_bridge_segmentb</td><td>0xA44679F3</td><td>No</td></tr>
<tr><td>_maracaibo_fence01</td><td>0x39DE1AB0</td><td>No</td></tr>
<tr><td>_maracaibo_freewayascender01</td><td>0x9231CA13</td><td>No</td></tr>
<tr><td>_maracaibo_freewaystraight01</td><td>0x782ECFBE</td><td>No</td></tr>
<tr><td>_maracaibo_freewaytrenchbridge01_overpass</td><td>0xFBDF9CB5</td><td>No</td></tr>
<tr><td>_maracaibo_freewaytrenchbridge01_overpass_autobridge</td><td>0x86F4A062</td><td>No</td></tr>
<tr><td>_maracaibo_freewaytrenchbridge01_underpass</td><td>0xBC506E51</td><td>No</td></tr>
<tr><td>_maracaibo_lampposta</td><td>0x6A5CCB23</td><td>No</td></tr>
<tr><td>_maracaibo_lamppostb</td><td>0x505EE0CC</td><td>No</td></tr>
<tr><td>_maracaibo_obelisk</td><td>0x536E7991</td><td>No</td></tr>
<tr><td>_maracaibo_obelisk_ruined</td><td>0xF6667AA5</td><td>No</td></tr>
<tr><td>_maracaibo_outskirtbridge20cross10</td><td>0x158ABA19</td><td>No</td></tr>
<tr><td>_maracaibo_outskirtbridge20cross20</td><td>0xA0223328</td><td>No</td></tr>
<tr><td>_maracaibo_park</td><td>0x88281132</td><td>No</td></tr>
<tr><td>_maracaibo_signgastall</td><td>0x1EFCC969</td><td>No</td></tr>
<tr><td>_maracaibo_wall06m</td><td>0xA94F1195</td><td>No</td></tr>
<tr><td>_maracaibo_wall10m</td><td>0xB70FB362</td><td>No</td></tr>
<tr><td>_maracaibo_wall20m</td><td>0xCBC798B5</td><td>No</td></tr>
<tr><td>_maracaiboruins_bld_govtbld</td><td>0x97B3BDF0</td><td>No</td></tr>
<tr><td>_maracaiboruins_bld_historical01</td><td>0xF7373837</td><td>No</td></tr>
<tr><td>_maracaiboruins_bld_historical02</td><td>0x0D399970</td><td>No</td></tr>
<tr><td>_maracaiboruins_bld_radiotower</td><td>0x462A2536</td><td>No</td></tr>
<tr><td>_maracaiboruins_bld_skyscraper01</td><td>0x74C3B028</td><td>No</td></tr>
<tr><td>_maracaiboruins_bld_skyscraper02</td><td>0xFEC0B7CF</td><td>No</td></tr>
<tr><td>_margarita_bld_bank</td><td>0x5CDA4ADE</td><td>No</td></tr>
<tr><td>_margarita_bld_club01</td><td>0xF96F58AD</td><td>No</td></tr>
<tr><td>_margarita_bld_condo01</td><td>0x6176308A</td><td>No</td></tr>
<tr><td>_margarita_bld_hotelresort01</td><td>0xC5FD29D0</td><td>No</td></tr>
<tr><td>_margarita_env_trench</td><td>0x39DB7CF3</td><td>No</td></tr>
<tr><td>_Margarita_hotelpool</td><td>0x3116A4C3</td><td>No</td></tr>
<tr><td>_marsh_bridge02end</td><td>0x88861CC8</td><td>No</td></tr>
<tr><td>_marsh_bridge02end_ruined</td><td>0xA5D4FCD6</td><td>No</td></tr>
<tr><td>_marsh_bridge02mid</td><td>0xEF0E2A55</td><td>No</td></tr>
<tr><td>_marsh_bridge02mid_ruined</td><td>0xA60D8469</td><td>No</td></tr>
<tr><td>_marsh_bridgeend</td><td>0x65A33902</td><td>No</td></tr>
<tr><td>_marsh_bridgeend_ruined</td><td>0x5D156A78</td><td>No</td></tr>
<tr><td>_marsh_bridgemid</td><td>0xD50BB3E3</td><td>No</td></tr>
<tr><td>_marsh_bridgemid_AIcollision</td><td>0xB2DEFAA0</td><td>No</td></tr>
<tr><td>_marsh_bridgemid_ruined</td><td>0x738CF0E7</td><td>No</td></tr>
<tr><td>_marsh_bridgerailing01</td><td>0xB94918F4</td><td>No</td></tr>
<tr><td>_marsh_bridgerailing02</td><td>0x93469E8B</td><td>No</td></tr>
<tr><td>_Marsh_env_treewater02</td><td>0xB5E63803</td><td>No</td></tr>
<tr><td>_merida_bld_hotel</td><td>0x37B0D170</td><td>No</td></tr>
<tr><td>_merida_bld_hotel_ruined</td><td>0x680C3DDE</td><td>No</td></tr>
<tr><td>_merida_bld_lockerroom</td><td>0xB7513987</td><td>No</td></tr>
<tr><td>_merida_bld_mediabooth</td><td>0x2E14153A</td><td>No</td></tr>
<tr><td>_merida_bld_oilwellland</td><td>0x6AFE8CA5</td><td>No</td></tr>
<tr><td>_merida_bld_oilwellland_ruined</td><td>0x4AD66939</td><td>No</td></tr>
<tr><td>_merida_bld_oilwellwater</td><td>0x1ABC2EF7</td><td>No</td></tr>
<tr><td>_merida_bld_plazachurch</td><td>0x2285EF81</td><td>No</td></tr>
<tr><td>_merida_bld_pmcautoshop</td><td>0x021C6B27</td><td>No</td></tr>
<tr><td>_merida_bld_pmcautoshop_interior</td><td>0x22E0FB26</td><td>No</td></tr>
<tr><td>_merida_bld_soccerstadium</td><td>0x680E4358</td><td>No</td></tr>
<tr><td>_merida_bld_tickets</td><td>0xE0439E0D</td><td>No</td></tr>
<tr><td>_merida_bld_universityadmin</td><td>0x6E6D6867</td><td>No</td></tr>
<tr><td>_merida_bld_universityadmin_ruined</td><td>0x3C46A0AB</td><td>No</td></tr>
<tr><td>_merida_bld_universitycampus</td><td>0x249D52B1</td><td>No</td></tr>
<tr><td>_merida_bld_universitycampus_ruined</td><td>0xD62412C5</td><td>No</td></tr>
<tr><td>_merida_bld_universitydorm</td><td>0x701657EA</td><td>No</td></tr>
<tr><td>_merida_bld_universitydorm_ruined</td><td>0xDF2AFE60</td><td>No</td></tr>
<tr><td>_merida_bld_universitylibrary</td><td>0x9FC4B9D3</td><td>No</td></tr>
<tr><td>_merida_busstop</td><td>0xE4BFA2F7</td><td>No</td></tr>
<tr><td>_merida_env_plazabush01</td><td>0x498D0238</td><td>No</td></tr>
<tr><td>_merida_env_plazabush02</td><td>0xD38A09DF</td><td>No</td></tr>
<tr><td>_merida_env_plazaflowers01</td><td>0x6A3D407C</td><td>No</td></tr>
<tr><td>_merida_env_plazaflowers02</td><td>0x443AC613</td><td>No</td></tr>
<tr><td>_merida_env_plazahedgecorner</td><td>0x7432AC69</td><td>No</td></tr>
<tr><td>_merida_env_plazahedgestraight</td><td>0xE722F488</td><td>No</td></tr>
<tr><td>_merida_env_plazahedgestraightlong</td><td>0x5F443962</td><td>No</td></tr>
<tr><td>_merida_env_plazalawn01</td><td>0x99831304</td><td>No</td></tr>
<tr><td>_merida_env_plazalawn02</td><td>0x338033DB</td><td>No</td></tr>
<tr><td>_merida_env_plazalawn03</td><td>0x117DBFBE</td><td>No</td></tr>
<tr><td>_merida_env_plazalawn04</td><td>0x1B8F189D</td><td>No</td></tr>
<tr><td>_merida_fencemetalgatea</td><td>0x2A7A250F</td><td>No</td></tr>
<tr><td>_merida_fencemetallonga</td><td>0xE2687D0A</td><td>No</td></tr>
<tr><td>_merida_fencemetalshorta</td><td>0xBF13D504</td><td>No</td></tr>
<tr><td>_merida_lawna</td><td>0x570BCE56</td><td>No</td></tr>
<tr><td>_merida_lightstadiuma</td><td>0x4A07F687</td><td>No</td></tr>
<tr><td>_merida_lightstadiumb</td><td>0x2009F300</td><td>No</td></tr>
<tr><td>_merida_market01</td><td>0x684D96AE</td><td>No</td></tr>
<tr><td>_merida_market02</td><td>0xCA54ECB9</td><td>No</td></tr>
<tr><td>_merida_market03</td><td>0xF052E9F4</td><td>No</td></tr>
<tr><td>_merida_market04</td><td>0x525A3FFF</td><td>No</td></tr>
<tr><td>_merida_market05</td><td>0xF0576722</td><td>No</td></tr>
<tr><td>_merida_parkingplantercorner</td><td>0x24AA8196</td><td>No</td></tr>
<tr><td>_merida_parkingplanterstraight</td><td>0xFA16CE7F</td><td>No</td></tr>
<tr><td>_merida_plateau01</td><td>0x05DF6F22</td><td>No</td></tr>
<tr><td>_merida_plazabench</td><td>0x3D2755E3</td><td>No</td></tr>
<tr><td>_merida_plazalampost</td><td>0x6A2E2FE1</td><td>No</td></tr>
<tr><td>_merida_plazastatue</td><td>0x070CC4DF</td><td>No</td></tr>
<tr><td>_merida_plazawaterfountain</td><td>0x6C6052A8</td><td>No</td></tr>
<tr><td>_merida_pmcautoshop_sportscar</td><td>0xB88DBED4</td><td>No</td></tr>
<tr><td>_merida_signa</td><td>0x1F0BBF11</td><td>No</td></tr>
<tr><td>_merida_signb</td><td>0x9D0436A6</td><td>No</td></tr>
<tr><td>_merida_signc</td><td>0xBF06AAC3</td><td>No</td></tr>
<tr><td>_merida_signfolda</td><td>0xFBC54A56</td><td>No</td></tr>
<tr><td>_merida_signfoldb</td><td>0x7DCCD2C1</td><td>No</td></tr>
<tr><td>_merida_signfoldc</td><td>0x83CA9D9C</td><td>No</td></tr>
<tr><td>_merida_soccerfield</td><td>0xB8F19856</td><td>No</td></tr>
<tr><td>_merida_telephonepole</td><td>0x7586F083</td><td>No</td></tr>
<tr><td>_merida_universityfence</td><td>0x1EA223DA</td><td>No</td></tr>
<tr><td>_merida_universitylamppost</td><td>0x0D0323AB</td><td>No</td></tr>
<tr><td>_merida_universitylibraryplateau01</td><td>0xCD4E6943</td><td>No</td></tr>
<tr><td>_merida_universitypicnictable</td><td>0x71C293FF</td><td>No</td></tr>
<tr><td>_merida_universitystatue</td><td>0xB5DD5B9B</td><td>No</td></tr>
<tr><td>_mountain_blastdoors</td><td>0xE1DF0AF5</td><td>No</td></tr>
<tr><td>_mountain_blastdoors_invincible</td><td>0xB8FEB0DB</td><td>No</td></tr>
<tr><td>_mountain_blastdoors_stitcher</td><td>0x49BD7FB2</td><td>No</td></tr>
<tr><td>_mountain_bld_bunkerdestroyed</td><td>0x653621C7</td><td>No</td></tr>
<tr><td>_NOT YET ORGANIZED</td><td>0x90356F04</td><td>No</td></tr>
<tr><td>_ocoutpost_bench</td><td>0x5602C117</td><td>No</td></tr>
<tr><td>_ocoutpost_bld_alarmtower</td><td>0xDDD6DD04</td><td>No</td></tr>
<tr><td>_ocoutpost_bld_guardpost01</td><td>0x9013EE16</td><td>No</td></tr>
<tr><td>_ocoutpost_bld_guardpost01_gate</td><td>0xD6CFC6E8</td><td>No</td></tr>
<tr><td>_ocoutpost_bld_helipad</td><td>0x22C3FE09</td><td>Yes</td></tr>
<tr><td>_ocoutpost_bld_hq</td><td>0x5467DE77</td><td>No</td></tr>
<tr><td>_ocoutpost_bld_hq_ruined</td><td>0x7657A87B</td><td>No</td></tr>
<tr><td>_ocoutpost_bld_radiotower</td><td>0x348A63CA</td><td>No</td></tr>
<tr><td>_ocoutpost_bld_radiotower_ruined</td><td>0x9FAA7BC0</td><td>No</td></tr>
<tr><td>_ocoutpost_bld_warehouse01</td><td>0x16A8A38A</td><td>No</td></tr>
<tr><td>_ocoutpost_desklobby</td><td>0x1AE7E19C</td><td>No</td></tr>
<tr><td>_ocoutpost_expandablevan_prop</td><td>0x8C028676</td><td>No</td></tr>
<tr><td>_ocoutpost_exterior_job</td><td>0xD17FCAC9</td><td>No</td></tr>
<tr><td>_ocoutpost_fountain01</td><td>0xB6D866E6</td><td>No</td></tr>
<tr><td>_ocoutpost_fountainentrance</td><td>0x721F6649</td><td>No</td></tr>
<tr><td>_ocoutpost_fueltanks</td><td>0xF00C7A06</td><td>Yes</td></tr>
<tr><td>_ocoutpost_guardtower</td><td>0x231B6EC5</td><td>No</td></tr>
<tr><td>_ocoutpost_hqbase</td><td>0xDB8F74AD</td><td>No</td></tr>
<tr><td>_ocoutpost_hqbaseIntersection</td><td>0x5D5506B6</td><td>No</td></tr>
<tr><td>_ocoutpost_hqplaza</td><td>0x5A59F8D0</td><td>No</td></tr>
<tr><td>_ocoutpost_interior_job</td><td>0xCD2388CF</td><td>No</td></tr>
<tr><td>_ocoutpost_planter01</td><td>0xC0A23CEA</td><td>No</td></tr>
<tr><td>_ocoutpost_statueoil</td><td>0x70364271</td><td>No</td></tr>
<tr><td>_ocoutpost_tablearmwrestling</td><td>0xE91AC6DE</td><td>No</td></tr>
<tr><td>_ocoutpost_wallcorner</td><td>0x6960908C</td><td>No</td></tr>
<tr><td>_ocoutpost_wallgate</td><td>0xA893A52E</td><td>No</td></tr>
<tr><td>_ocoutpost_wallLong</td><td>0xF30CBF21</td><td>No</td></tr>
<tr><td>_ocoutpost_wallShort</td><td>0x037D306F</td><td>No</td></tr>
<tr><td>_oilrig_att_towerdrillspeakersA</td><td>0x08AA2E32</td><td>No</td></tr>
<tr><td>_oilrig_bld_helipadsmalla</td><td>0x30086385</td><td>Yes</td></tr>
<tr><td>_oilrig_fueltanklargeA</td><td>0xE754321B</td><td>Yes</td></tr>
<tr><td>_oilrig_tankmedA</td><td>0x268F6EBA</td><td>Yes</td></tr>
<tr><td>_oilrig_tanksmallA</td><td>0x59F415BB</td><td>Yes</td></tr>
<tr><td>_oilrig_tanktallA</td><td>0x80FB9C09</td><td>Yes</td></tr>
<tr><td>_outpost_bld_farming01</td><td>0xE680454D</td><td>No</td></tr>
<tr><td>_outpost_bld_farming01_true</td><td>0x12BAD0A8</td><td>No</td></tr>
<tr><td>_outpost_bld_govtbld</td><td>0x02B87F56</td><td>No</td></tr>
<tr><td>_outpost_bld_govtbld_ruined</td><td>0x235B62DC</td><td>No</td></tr>
<tr><td>_outpost_bld_municipal</td><td>0x6F5867C8</td><td>No</td></tr>
<tr><td>_outpost_bld_municipal_fence</td><td>0x6E814B6E</td><td>No</td></tr>
<tr><td>_outpost_bld_municipal_true</td><td>0xE8F23753</td><td>No</td></tr>
<tr><td>_outpost_bld_office</td><td>0xF4152750</td><td>No</td></tr>
<tr><td>_outpost_bld_plantation02</td><td>0x1C316850</td><td>No</td></tr>
<tr><td>_outpost_bld_shack</td><td>0xC461646C</td><td>No</td></tr>
<tr><td>_outpost_bld_vzwarehouselarge</td><td>0xE5A53D46</td><td>No</td></tr>
<tr><td>_outpost_bld_vzwarehouselarge_Ruined</td><td>0xD589554C</td><td>No</td></tr>
<tr><td>_outpost_bld_warehouse01</td><td>0xBAA777CC</td><td>No</td></tr>
<tr><td>_outskirt_bld_church</td><td>0xAC945F54</td><td>No</td></tr>
<tr><td>_outskirt_bld_church_ruined</td><td>0x381A7762</td><td>No</td></tr>
<tr><td>_outskirt_bld_house01</td><td>0x49CD0782</td><td>No</td></tr>
<tr><td>_outskirt_bld_house02</td><td>0xCBD48FED</td><td>No</td></tr>
<tr><td>_outskirt_bld_house03</td><td>0xA1D20F38</td><td>No</td></tr>
<tr><td>_outskirt_bld_house04</td><td>0xA3C5466B</td><td>No</td></tr>
<tr><td>_outskirt_bld_house05</td><td>0xC1C3370E</td><td>No</td></tr>
<tr><td>_outskirt_bld_house06</td><td>0x23CA8D19</td><td>No</td></tr>
<tr><td>_outskirt_bld_market01</td><td>0x3B8A7310</td><td>No</td></tr>
<tr><td>_outskirt_bld_market02</td><td>0x258811D7</td><td>No</td></tr>
<tr><td>_outskirt_bld_market03</td><td>0xC38538FA</td><td>No</td></tr>
<tr><td>_outskirt_bld_market04</td><td>0x9D82BE91</td><td>No</td></tr>
<tr><td>_outskirt_bld_market05</td><td>0xA380896C</td><td>No</td></tr>
<tr><td>_outskirt_bld_mercbar</td><td>0x09569D2D</td><td>No</td></tr>
<tr><td>_outskirt_chickenfencelong</td><td>0x4E7E161A</td><td>No</td></tr>
<tr><td>_outskirt_chickenfenceshort</td><td>0x68A053F2</td><td>No</td></tr>
<tr><td>_outskirt_curb</td><td>0x6A727450</td><td>No</td></tr>
<tr><td>_outskirt_road10</td><td>0xF0310CAD</td><td>No</td></tr>
<tr><td>_outskirt_road10cross</td><td>0xCB93CBD3</td><td>No</td></tr>
<tr><td>_outskirt_road10crossboth</td><td>0x7E4A171E</td><td>No</td></tr>
<tr><td>_outskirt_road10merge</td><td>0x4FEB7927</td><td>No</td></tr>
<tr><td>_outskirt_road10straight</td><td>0xBFD970C7</td><td>No</td></tr>
<tr><td>_outskirt_road10t</td><td>0xBC8B0D5B</td><td>No</td></tr>
<tr><td>_outskirt_road10t02</td><td>0x23D6B321</td><td>No</td></tr>
<tr><td>_outskirt_road10t20</td><td>0xCAA2D8C9</td><td>No</td></tr>
<tr><td>_outskirt_road10t5</td><td>0x3DB6C788</td><td>No</td></tr>
<tr><td>_outskirt_road10tleft</td><td>0xADD46DE0</td><td>No</td></tr>
<tr><td>_outskirt_road10tright</td><td>0xF490DC47</td><td>No</td></tr>
<tr><td>_outskirt_road20</td><td>0x5AC8535C</td><td>No</td></tr>
<tr><td>_outskirt_road20cross</td><td>0x97060AAC</td><td>No</td></tr>
<tr><td>_outskirt_road20cross10</td><td>0x981571F7</td><td>No</td></tr>
<tr><td>_outskirt_road20crossboth</td><td>0xEABA162D</td><td>No</td></tr>
<tr><td>_outskirt_road20straight</td><td>0x3104F53E</td><td>No</td></tr>
<tr><td>_outskirt_road20t</td><td>0x5FE12E9C</td><td>No</td></tr>
<tr><td>_outskirt_road20t10</td><td>0xB3D1D8E7</td><td>No</td></tr>
<tr><td>_outskirt_road20tleft</td><td>0x1CDD0373</td><td>No</td></tr>
<tr><td>_outskirt_road20tright</td><td>0x7341BA1A</td><td>No</td></tr>
<tr><td>_outskirt_road5</td><td>0x0D722943</td><td>No</td></tr>
<tr><td>_outskirt_road5T</td><td>0xBC50C2D5</td><td>No</td></tr>
<tr><td>_outskirt_road5T10</td><td>0x6430D3C2</td><td>No</td></tr>
<tr><td>_outskirt_wallchurchcorner</td><td>0x973E3926</td><td>No</td></tr>
<tr><td>_outskirt_wallchurchlong</td><td>0x2CEA8063</td><td>No</td></tr>
<tr><td>_outskirt_wallchurchshort</td><td>0xE65D54F5</td><td>No</td></tr>
<tr><td>_pedestrian_x</td><td>0x703C9692</td><td>No</td></tr>
<tr><td>_pirate_chaira</td><td>0x5D74EB8E</td><td>No</td></tr>
<tr><td>_pirate_chairb</td><td>0xBF7C4199</td><td>No</td></tr>
<tr><td>_pirate_chairb (Dancing)</td><td>0x7AE910C4</td><td>No</td></tr>
<tr><td>_pmcoutpost_armyCot</td><td>0x770D34FC</td><td>No</td></tr>
<tr><td>_pmcoutpost_beerA</td><td>0x660F0FF8</td><td>No</td></tr>
<tr><td>_pmcoutpost_beerB</td><td>0xF00C179F</td><td>No</td></tr>
<tr><td>_pmcoutpost_beerC</td><td>0x0E0A0842</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_dock</td><td>0x3D56E499</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_fueldepot</td><td>0xF592C1D6</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_guardpost</td><td>0xBD0F9621</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_guardtower</td><td>0xA614A8B2</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_hangar</td><td>0xD4286725</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_hq</td><td>0xFA352751</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_hq_interior</td><td>0xEFF62F70</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_hq_livedin</td><td>0xAA5CF2EB</td><td>No</td></tr>
<tr><td>_Pmcoutpost_bld_hq_livedin_pmccon003</td><td>0xE8F7513D</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_hq_stitch</td><td>0xF7137923</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_hqgarage</td><td>0x0CEDB83E</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_hqgarage_livedin</td><td>0x4277ECA0</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_hqsuites</td><td>0x4D024F06</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_pool</td><td>0x98C100B2</td><td>No</td></tr>
<tr><td>_pmcoutpost_bld_pool_stitch</td><td>0x54C98856</td><td>No</td></tr>
<tr><td>_pmcoutpost_bridge</td><td>0xCB1C662E</td><td>No</td></tr>
<tr><td>_pmcoutpost_bridge_aicollision</td><td>0xC56BCD09</td><td>No</td></tr>
<tr><td>_pmcoutpost_bridgepole</td><td>0x194BCD28</td><td>No</td></tr>
<tr><td>_pmcoutpost_carcreeper</td><td>0x3571DA99</td><td>No</td></tr>
<tr><td>_pmcoutpost_carramp</td><td>0xA82ED4C5</td><td>No</td></tr>
<tr><td>_pmcoutpost_chandeliers</td><td>0x6541730F</td><td>No</td></tr>
<tr><td>_pmcoutpost_column</td><td>0x148994D7</td><td>No</td></tr>
<tr><td>_pmcoutpost_column_noreflection</td><td>0x0F3F4CA8</td><td>No</td></tr>
<tr><td>_pmcoutpost_column_noreflection_large</td><td>0xC9B17DA8</td><td>No</td></tr>
<tr><td>_pmcoutpost_column_noreflection_large_HighHP</td><td>0xFD46DE83</td><td>No</td></tr>
<tr><td>_pmcoutpost_column_noreflection_large_lowHP</td><td>0x1AF22B27</td><td>No</td></tr>
<tr><td>_pmcoutpost_column_noreflection_physics</td><td>0x26BAEADA</td><td>No</td></tr>
<tr><td>_pmcoutpost_coverflowerpot</td><td>0x7C8D8304</td><td>No</td></tr>
<tr><td>_pmcoutpost_electricBoxA</td><td>0xEE253ECC</td><td>No</td></tr>
<tr><td>_pmcoutpost_electricBoxB</td><td>0x08232923</td><td>No</td></tr>
<tr><td>_pmcoutpost_electricBoxC</td><td>0xE620B506</td><td>No</td></tr>
<tr><td>_pmcoutpost_fountain</td><td>0x2F2C856D</td><td>No</td></tr>
<tr><td>_pmcoutpost_gate</td><td>0xDD1CB508</td><td>No</td></tr>
<tr><td>_pmcoutpost_gate_open</td><td>0xBCF03323</td><td>No</td></tr>
<tr><td>_pmcoutpost_generator</td><td>0xFA076A98</td><td>No</td></tr>
<tr><td>_pmcoutpost_hq_door_entrance</td><td>0x6A72B4FC</td><td>No</td></tr>
<tr><td>_pmcoutpost_hq_door_entranceCollision</td><td>0x568D9ABC</td><td>No</td></tr>
<tr><td>_pmcoutpost_hq_door_garage</td><td>0x0322E7DD</td><td>No</td></tr>
<tr><td>_pmcoutpost_hq_door_roof</td><td>0x79BABB3C</td><td>No</td></tr>
<tr><td>_pmcoutpost_hq_garageentrance</td><td>0xF514923E</td><td>No</td></tr>
<tr><td>_pmcoutpost_hqgarage_door_backdoor</td><td>0xA139AC30</td><td>No</td></tr>
<tr><td>_pmcoutpost_hqgarage_door_big</td><td>0x28F6E095</td><td>No</td></tr>
<tr><td>_pmcoutpost_hqgarage_door_roof</td><td>0xA992B4C3</td><td>No</td></tr>
<tr><td>_pmcoutpost_icebox</td><td>0x994C22F9</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money</td><td>0x5F83D7E4</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money_a</td><td>0xA60DB1AC</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money_b</td><td>0x400AD283</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money_c</td><td>0x1E085E66</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money_d</td><td>0x2819B745</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money_e</td><td>0x3E179B50</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money_f</td><td>0x28153A17</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money_g</td><td>0xC612613A</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money_h</td><td>0x9FFC5F19</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_money_i</td><td>0x45F992D4</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_recruitheli</td><td>0xD148EB92</td><td>Yes</td></tr>
<tr><td>_pmcoutpost_interior_recruitjet</td><td>0x9F5875D3</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_recruitmechanic</td><td>0x9719D1C4</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_recruitmechanic_wallReplace</td><td>0x360F3129</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_scaffold</td><td>0x80F17406</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_sickbay</td><td>0xF31A49D2</td><td>No</td></tr>
<tr><td>_pmcoutpost_interior_stockpile</td><td>0x0045888E</td><td>No</td></tr>
<tr><td>_pmcoutpost_IV</td><td>0x85E31274</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions</td><td>0xEDA24071</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_artillery_A</td><td>0x448CD8A6</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_artillery_B</td><td>0xC6946111</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_artillery_C</td><td>0xCC922BEC</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_bombingrun_A</td><td>0x11EE32DF</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_bombingrun_B</td><td>0x87F12B38</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_bombingrun_C</td><td>0xB1F3ABED</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_bunkerbuster_A</td><td>0x63CB97E8</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_bunkerbuster_B</td><td>0xEDC89F8F</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_bunkerbuster_C</td><td>0xCBC62B72</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_cap_A</td><td>0xD307BFD0</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_cap_B</td><td>0xBD055E97</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_cap_C</td><td>0x5B0285BA</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_clusterbomb_A</td><td>0x934AE316</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_clusterbomb_B</td><td>0x15526B81</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_clusterbomb_C</td><td>0x1B50365C</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_daisycutter_A</td><td>0x7869B7CF</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_daisycutter_B</td><td>0xEE6CB028</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_daisycutter_C</td><td>0xD86ECC1D</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_fae_A</td><td>0x724367F4</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_fae_B</td><td>0x4C40ED8B</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_fae_C</td><td>0xEA3E14AE</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_gbu16_A</td><td>0xDE4C9A41</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_gbu16_B</td><td>0x5C4511D6</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_gbu16_C</td><td>0xBE47EAB3</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_MOAB_A</td><td>0xD212950D</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_MOAB_B</td><td>0x500B0CA2</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_MOAB_C</td><td>0xB20DE57F</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_rocketartillery_A</td><td>0x5F93B866</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_rocketartillery_B</td><td>0xE19B40D1</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_rocketartillery_C</td><td>0xE7990BAC</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_surgicalstrike_A</td><td>0x4E1B15E8</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_surgicalstrike_B</td><td>0xD8181D8F</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_surgicalstrike_C</td><td>0xB615A972</td><td>No</td></tr>
<tr><td>_pmcoutpost_munitions_tankbuster_A</td><td>0x9DE55C33</td><td>Yes</td></tr>
<tr><td>_pmcoutpost_munitions_tankbuster_B</td><td>0xC3E7D69C</td><td>Yes</td></tr>
<tr><td>_pmcoutpost_munitions_tankbuster_C</td><td>0xBDEA0BC1</td><td>Yes</td></tr>
<tr><td>_pmcoutpost_planter01</td><td>0xE873C630</td><td>No</td></tr>
<tr><td>_pmcoutpost_plantera</td><td>0x1834E2F2</td><td>No</td></tr>
<tr><td>_pmcoutpost_planterb</td><td>0x9A3C6B5D</td><td>No</td></tr>
<tr><td>_pmcoutpost_planterc</td><td>0xB03A4F68</td><td>No</td></tr>
<tr><td>_pmcoutpost_planterd</td><td>0xB22D869B</td><td>No</td></tr>
<tr><td>_pmcoutpost_plantere</td><td>0x902B127E</td><td>No</td></tr>
<tr><td>_pmcoutpost_printer</td><td>0xC936132F</td><td>No</td></tr>
<tr><td>_pmcoutpost_road_sidewalk</td><td>0x38D4A6D8</td><td>No</td></tr>
<tr><td>_pmcoutpost_road_sidewalk01</td><td>0xE9985DDD</td><td>No</td></tr>
<tr><td>_pmcoutpost_road_sidewalkcurve01</td><td>0xE0B079F0</td><td>No</td></tr>
<tr><td>_pmcoutpost_road_sidewalksmall</td><td>0x417E1A41</td><td>No</td></tr>
<tr><td>_pmcoutpost_road_sidewalksmall01</td><td>0xCC74F104</td><td>No</td></tr>
<tr><td>_pmcoutpost_road_sidewalkssmcurveleft01</td><td>0xE7194906</td><td>No</td></tr>
<tr><td>_pmcoutpost_road_sidewalkssmcurveright01</td><td>0x49C9AA0F</td><td>No</td></tr>
<tr><td>_pmcoutpost_shootinggallerytarget01</td><td>0x539C3F12</td><td>No</td></tr>
<tr><td>_pmcoutpost_sofa</td><td>0x133EC8C4</td><td>No</td></tr>
<tr><td>_pmcoutpost_statuecup</td><td>0x5206D86B</td><td>No</td></tr>
<tr><td>_pmcoutpost_statuedavid</td><td>0x08B37231</td><td>No</td></tr>
<tr><td>_pmcoutpost_statuedavid_lowhealth</td><td>0x096EB764</td><td>No</td></tr>
<tr><td>_pmcoutpost_statuedavid_ruined</td><td>0xE0A6F545</td><td>No</td></tr>
<tr><td>_pmcoutpost_statuediscus</td><td>0xAFE5E3C2</td><td>No</td></tr>
<tr><td>_pmcoutpost_statueSolanobust</td><td>0xB7D02E4D</td><td>No</td></tr>
<tr><td>_pmcoutpost_statueSolanobust_lowHP</td><td>0x484C1FA2</td><td>No</td></tr>
<tr><td>_pmcoutpost_statuethinker</td><td>0x2D978172</td><td>No</td></tr>
<tr><td>_pmcoutpost_steamerTrunk</td><td>0xDC753284</td><td>No</td></tr>
<tr><td>_pmcoutpost_togoBox</td><td>0xA2A8F48F</td><td>No</td></tr>
<tr><td>_pmcoutpost_tray</td><td>0x4F0EE265</td><td>No</td></tr>
<tr><td>_pmcoutpost_TV</td><td>0x890C98DF</td><td>No</td></tr>
<tr><td>_pmcoutpost_walla</td><td>0x51DF5BE2</td><td>No</td></tr>
<tr><td>_pmcoutpost_wallb</td><td>0xD3E6E44D</td><td>No</td></tr>
<tr><td>_pmcoutpost_waterCooler</td><td>0x9252F580</td><td>No</td></tr>
<tr><td>_policeoutpost_bld_guardtower</td><td>0xA0BF3B00</td><td>No</td></tr>
<tr><td>_policeoutpost_bld_motorpool</td><td>0xD1204EB7</td><td>No</td></tr>
<tr><td>_policeoutpost_bld_policeHQ</td><td>0xB0E73C59</td><td>No</td></tr>
<tr><td>_policeoutpost_bld_policestation01</td><td>0x7E89185D</td><td>No</td></tr>
<tr><td>_policeoutpost_bld_prison</td><td>0x91431313</td><td>No</td></tr>
<tr><td>_port_containera</td><td>0x545DCABE</td><td>No</td></tr>
<tr><td>_port_containera_light</td><td>0x9C19E827</td><td>No</td></tr>
<tr><td>_port_containerb</td><td>0xF6658589</td><td>No</td></tr>
<tr><td>_port_containerb_light</td><td>0x1F1C6F34</td><td>No</td></tr>
<tr><td>_port_containerc</td><td>0xDC631E04</td><td>No</td></tr>
<tr><td>_port_containerc_light</td><td>0x03DA8FBD</td><td>No</td></tr>
<tr><td>_port_containerd</td><td>0xFE6A0F4F</td><td>No</td></tr>
<tr><td>_port_containerd_light</td><td>0x8DF486DA</td><td>No</td></tr>
<tr><td>_port_crane01</td><td>0x58193AC2</td><td>No</td></tr>
<tr><td>_port_crane01_ruined</td><td>0x9A3F9338</td><td>No</td></tr>
<tr><td>_port_crane02</td><td>0xDA20C32D</td><td>No</td></tr>
<tr><td>_port_cranegantry01</td><td>0xAC4F5FD3</td><td>No</td></tr>
<tr><td>_port_dock_ladderlong</td><td>0x0790D4CE</td><td>No</td></tr>
<tr><td>_port_dock_ladderlong02</td><td>0x0BDCC8F4</td><td>No</td></tr>
<tr><td>_port_dock_laddermedium01</td><td>0x365C22D8</td><td>No</td></tr>
<tr><td>_port_dock_laddershort</td><td>0x39A1F0AE</td><td>No</td></tr>
<tr><td>_port_dock_laddershort02</td><td>0x74882D54</td><td>No</td></tr>
<tr><td>_port_dockdoorleft</td><td>0xA8B4392A</td><td>No</td></tr>
<tr><td>_port_dockdoorright</td><td>0xBDA0A581</td><td>No</td></tr>
<tr><td>_port_dockdry</td><td>0x8066913C</td><td>No</td></tr>
<tr><td>_port_dockdryendA</td><td>0x44C8B3AC</td><td>No</td></tr>
<tr><td>_port_dockdryendB</td><td>0xDEC5D483</td><td>No</td></tr>
<tr><td>_port_dockdryT</td><td>0x36BEFCFC</td><td>No</td></tr>
<tr><td>_port_dockend</td><td>0x3B3157A0</td><td>No</td></tr>
<tr><td>_port_dockloading</td><td>0xE0DB6447</td><td>No</td></tr>
<tr><td>_port_docklong</td><td>0x185A2B9B</td><td>No</td></tr>
<tr><td>_port_dockshort</td><td>0xFD49DF0D</td><td>No</td></tr>
<tr><td>_port_dockT</td><td>0x26C330CB</td><td>No</td></tr>
<tr><td>_port_gangplankA</td><td>0x19F13030</td><td>No</td></tr>
<tr><td>_port_gangplankB</td><td>0x03EECEF7</td><td>No</td></tr>
<tr><td>_port_scaffoldA</td><td>0xB0CE1B07</td><td>No</td></tr>
<tr><td>_proutpost_att_neonA</td><td>0x28413890</td><td>No</td></tr>
<tr><td>_proutpost_att_neonB</td><td>0x123ED757</td><td>No</td></tr>
<tr><td>_proutpost_att_neonC</td><td>0xB03BFE7A</td><td>No</td></tr>
<tr><td>_proutpost_att_neonD</td><td>0x8A398411</td><td>No</td></tr>
<tr><td>_proutpost_att_neonE</td><td>0x90374EEC</td><td>No</td></tr>
<tr><td>_proutpost_att_satelitelarge</td><td>0xEF69798B</td><td>No</td></tr>
<tr><td>_proutpost_att_satelitelarge_ruined</td><td>0x2032E9EF</td><td>No</td></tr>
<tr><td>_proutpost_bld_alarmtower</td><td>0x40D1E50C</td><td>No</td></tr>
<tr><td>_proutpost_bld_barstand</td><td>0x9F1FD55F</td><td>No</td></tr>
<tr><td>_proutpost_bld_bunker</td><td>0xC27BD1A9</td><td>No</td></tr>
<tr><td>_proutpost_bld_bunkersandbag</td><td>0xFBDA6937</td><td>No</td></tr>
<tr><td>_proutpost_bld_command</td><td>0xA9A06925</td><td>No</td></tr>
<tr><td>_proutpost_bld_command_ruined</td><td>0x15479AB9</td><td>No</td></tr>
<tr><td>_proutpost_bld_dormitory</td><td>0x1297A0FF</td><td>No</td></tr>
<tr><td>_proutpost_bld_dormitory_ruined</td><td>0xBD52BE23</td><td>No</td></tr>
<tr><td>_proutpost_bld_garageboat</td><td>0x74CEB277</td><td>Yes</td></tr>
<tr><td>_proutpost_bld_garageboat_Ruined</td><td>0x9359847B</td><td>Yes</td></tr>
<tr><td>_proutpost_bld_gasstationpump02</td><td>0x65D06087</td><td>No</td></tr>
<tr><td>_proutpost_bld_gasstationpump03</td><td>0x43CDEC6A</td><td>No</td></tr>
<tr><td>_proutpost_bld_guardtower01</td><td>0x75662AC1</td><td>No</td></tr>
<tr><td>_proutpost_bld_hq</td><td>0xA815D69F</td><td>No</td></tr>
<tr><td>_proutpost_bld_pavilion</td><td>0x54E1BE76</td><td>No</td></tr>
<tr><td>_proutpost_bld_shacksmall01</td><td>0x6C66D3DA</td><td>No</td></tr>
<tr><td>_proutpost_bld_shacksmall02</td><td>0xCE6E29E5</td><td>No</td></tr>
<tr><td>_proutpost_bld_shacksmall03</td><td>0x646B4470</td><td>No</td></tr>
<tr><td>_proutpost_bld_shacksmall03_Ruined</td><td>0x732EFEDE</td><td>No</td></tr>
<tr><td>_proutpost_bld_shacksmall04</td><td>0xE65F4523</td><td>No</td></tr>
<tr><td>_proutpost_bld_surveillance</td><td>0x33A4C96D</td><td>No</td></tr>
<tr><td>_proutpost_dockA</td><td>0x9F368947</td><td>No</td></tr>
<tr><td>_proutpost_dockB</td><td>0x753885C0</td><td>No</td></tr>
<tr><td>_proutpost_fencewood01</td><td>0x8E5C1924</td><td>No</td></tr>
<tr><td>_proutpost_fencewood02</td><td>0xA85A037B</td><td>No</td></tr>
<tr><td>_proutpost_fueltanks</td><td>0x7DD4EF9E</td><td>Yes</td></tr>
<tr><td>_proutpost_helipad</td><td>0x4CE92E2A</td><td>Yes</td></tr>
<tr><td>_proutpost_interior_job</td><td>0x39394E37</td><td>No</td></tr>
<tr><td>_Proutpost_lampA</td><td>0x4B6D3286</td><td>No</td></tr>
<tr><td>_residential_bld_corner16x16a</td><td>0xFBEE37C0</td><td>No</td></tr>
<tr><td>_residential_bld_corner16x16b</td><td>0x25EC3B47</td><td>No</td></tr>
<tr><td>_residential_bld_corner16x16c</td><td>0x03E9C72A</td><td>No</td></tr>
<tr><td>_residential_bld_corner16x16d</td><td>0x9DE6E801</td><td>No</td></tr>
<tr><td>_residential_bld_corner16x16e</td><td>0xA3E4B2DC</td><td>No</td></tr>
<tr><td>_residential_bld_segment16x16a</td><td>0xAB17B940</td><td>No</td></tr>
<tr><td>_residential_bld_segment16x16b</td><td>0xD515BCC7</td><td>No</td></tr>
<tr><td>_residential_bld_segment16x16b_ruined</td><td>0xD737478B</td><td>No</td></tr>
<tr><td>_residential_bld_segment16x16c</td><td>0xB31348AA</td><td>No</td></tr>
<tr><td>_residential_bld_segment16x16c_ruined</td><td>0x0F313320</td><td>No</td></tr>
<tr><td>_residential_bld_segment16x16d</td><td>0x4D106981</td><td>No</td></tr>
<tr><td>_residential_driveway</td><td>0x81AD7A10</td><td>No</td></tr>
<tr><td>_residential_driveway02</td><td>0xF52D70AA</td><td>No</td></tr>
<tr><td>_residential_road10</td><td>0xB2EDD014</td><td>No</td></tr>
<tr><td>_residential_road10cross</td><td>0xE4F46104</td><td>No</td></tr>
<tr><td>_residential_road10l</td><td>0xCAF7F2CC</td><td>No</td></tr>
<tr><td>_residential_road10t</td><td>0x4ABC9224</td><td>No</td></tr>
<tr><td>_residential_road10t5</td><td>0xAEEB2BB9</td><td>No</td></tr>
<tr><td>_residential_road5</td><td>0x8F67EE14</td><td>No</td></tr>
<tr><td>_residential_road5cross</td><td>0x464B3B04</td><td>No</td></tr>
<tr><td>_residential_road5cross10</td><td>0xA714354F</td><td>No</td></tr>
<tr><td>_residential_road5l</td><td>0xDF352CCC</td><td>No</td></tr>
<tr><td>_residential_road5t</td><td>0x5EF9CC24</td><td>No</td></tr>
<tr><td>_residential_road5t10</td><td>0x9978C5EF</td><td>No</td></tr>
<tr><td>_residential_sidewalk</td><td>0xFE26F5BB</td><td>No</td></tr>
<tr><td>_scrub_DLC_global_env_treemedium02</td><td>0x778DECED</td><td>No</td></tr>
<tr><td>_scrub_env_largecanopy01</td><td>0x1BB4EE74</td><td>No</td></tr>
<tr><td>_scrub_env_smallcanopy</td><td>0x9265E3AD</td><td>No</td></tr>
<tr><td>_scrub_env_smallcanopy02</td><td>0x25BA8CE7</td><td>No</td></tr>
<tr><td>_scrub_global_bananna</td><td>0x88E8C91D</td><td>No</td></tr>
<tr><td>_scrub_global_env_treesidewalk01</td><td>0x547805A7</td><td>No</td></tr>
<tr><td>_scrub_global_palmtree01</td><td>0xA3265679</td><td>No</td></tr>
<tr><td>_scrub_global_palmtreebend01</td><td>0xFD2975F4</td><td>No</td></tr>
<tr><td>_scrub_global_palmtreebend02</td><td>0xD726FB8B</td><td>No</td></tr>
<tr><td>_scrub_global_palmtreebend03</td><td>0x752422AE</td><td>No</td></tr>
<tr><td>_scrub_global_palmtreebend04</td><td>0x7F357B8D</td><td>No</td></tr>
<tr><td>_scrub_global_palmtreebend05</td><td>0x5532FAD8</td><td>No</td></tr>
<tr><td>_scrub_global_palmtreeMix01</td><td>0x20E2B0AB</td><td>No</td></tr>
<tr><td>_scrub_global_palmtreeMix02</td><td>0x46E52B14</td><td>No</td></tr>
<tr><td>_scrub_global_palmtreeplanted01</td><td>0x22B71F15</td><td>No</td></tr>
<tr><td>_scrub_global_treeoak01</td><td>0x2A54D6BA</td><td>No</td></tr>
<tr><td>_scrub_global_treeplaza01</td><td>0xC9A4EC6B</td><td>No</td></tr>
<tr><td>_scrub_global_treeplaza02</td><td>0xEFA766D4</td><td>No</td></tr>
<tr><td>_scrub_global_treeplaza03</td><td>0x49AA3319</td><td>No</td></tr>
<tr><td>_scrub_global_treeplazaMix</td><td>0xA0955814</td><td>No</td></tr>
<tr><td>_scrub_global_treesidewalk01</td><td>0x0720F3CB</td><td>No</td></tr>
<tr><td>_scrub_global_treespade</td><td>0x13E7446F</td><td>No</td></tr>
<tr><td>_scrub_global_treetropical01</td><td>0x06116B5D</td><td>No</td></tr>
<tr><td>_scrub_global_treetropical02</td><td>0x8409E2F2</td><td>No</td></tr>
<tr><td>_scrub_global_tropicalmix</td><td>0x2AFAEC36</td><td>No</td></tr>
<tr><td>_scrub_jungle_treemed01</td><td>0x7291BD75</td><td>No</td></tr>
<tr><td>_scrub_jungle_treemed03</td><td>0x728D4047</td><td>No</td></tr>
<tr><td>_scrub_Jungle_treesmall01</td><td>0xD8734A7E</td><td>No</td></tr>
<tr><td>_scrub_jungle_treesmall02</td><td>0x7A7B0549</td><td>No</td></tr>
<tr><td>_scrub_jungle_treesmall03</td><td>0x60789DC4</td><td>No</td></tr>
<tr><td>_scrub_jungle_treetall01</td><td>0xD0CA23F6</td><td>No</td></tr>
<tr><td>_scrub_jungle_treetall02</td><td>0x52D1AC61</td><td>No</td></tr>
<tr><td>_scrub_jungle_treetall03</td><td>0xD8CEADBC</td><td>No</td></tr>
<tr><td>_scrub_Jungle_treethin01</td><td>0x9682BEE2</td><td>No</td></tr>
<tr><td>_scrub_Jungle_treethin02</td><td>0x188A474D</td><td>No</td></tr>
<tr><td>_scrub_Jungle_treethin03</td><td>0xEE87C698</td><td>No</td></tr>
<tr><td>_scrub_junglemix</td><td>0x44E6AAEB</td><td>No</td></tr>
<tr><td>_scrub_junglemix02</td><td>0xF2C6A9B1</td><td>No</td></tr>
<tr><td>_scrub_marsh_treewater02</td><td>0xCD1993FF</td><td>No</td></tr>
<tr><td>_scrub_shanty_tree01</td><td>0x64B365D5</td><td>No</td></tr>
<tr><td>_scrub_shanty_tree02</td><td>0xC2ABAB0A</td><td>No</td></tr>
<tr><td>_scrub_shanty_tree03</td><td>0xE4AE1F27</td><td>No</td></tr>
<tr><td>_sean</td><td>0xA5960A21</td><td>No</td></tr>
<tr><td>_shanty_bld_apartment01</td><td>0xFE31D148</td><td>No</td></tr>
<tr><td>_shanty_bld_apartment01_ruined</td><td>0xA88CF656</td><td>No</td></tr>
<tr><td>_shanty_bld_apartment02</td><td>0x082FA26F</td><td>No</td></tr>
<tr><td>_shanty_bld_apartment02_ruined</td><td>0xEBFAB3D3</td><td>No</td></tr>
<tr><td>_shanty_bld_apartment03</td><td>0xE62D2E52</td><td>No</td></tr>
<tr><td>_shanty_bld_apartment04</td><td>0x802A4F29</td><td>No</td></tr>
<tr><td>_shanty_bld_apartment04_Ruined</td><td>0xD2A16A3D</td><td>No</td></tr>
<tr><td>_shanty_bld_house01</td><td>0xA3ED4CB2</td><td>No</td></tr>
<tr><td>_shanty_bld_house02</td><td>0x25F4D51D</td><td>No</td></tr>
<tr><td>_shanty_bld_house02_Ruined</td><td>0x76E3AE31</td><td>No</td></tr>
<tr><td>_shanty_bld_house03</td><td>0x3BF2B928</td><td>No</td></tr>
<tr><td>_shanty_bld_house03_Ruined</td><td>0xDAB61FB6</td><td>No</td></tr>
<tr><td>_shanty_bld_house04</td><td>0x3DE5F05B</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroup01</td><td>0xF92264C1</td><td>No</td></tr>
<tr><td>_Shanty_bld_housegroup02</td><td>0x771ADC56</td><td>No</td></tr>
<tr><td>_Shanty_bld_housegroup03</td><td>0xD91DB533</td><td>No</td></tr>
<tr><td>_Shanty_bld_housegroup03_ruined</td><td>0xD2AE8E37</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroup04</td><td>0x5729B480</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroup05</td><td>0x812C3535</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroup05_Ruined</td><td>0x04E8FD49</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroup06</td><td>0x5F2543EA</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroup06_ruined</td><td>0xFB9C6260</td><td>No</td></tr>
<tr><td>_Shanty_bld_housegroup07</td><td>0x8127B807</td><td>No</td></tr>
<tr><td>_Shanty_bld_housegroup07_Ruined</td><td>0x545DC8CB</td><td>No</td></tr>
<tr><td>_Shanty_bld_housegroup08</td><td>0xDF0C7584</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroupsmall01</td><td>0xB0AB5E98</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroupsmall01_ruined</td><td>0x193C38E6</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroupsmall02</td><td>0xBAA92FBF</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroupsmall03</td><td>0x58A656E2</td><td>No</td></tr>
<tr><td>_shanty_bld_housegroupsmall04</td><td>0x32A3DC79</td><td>No</td></tr>
<tr><td>_shanty_bld_outhouse</td><td>0x9A39FC3D</td><td>No</td></tr>
<tr><td>_shanty_bld_shack01</td><td>0xD5A65D02</td><td>No</td></tr>
<tr><td>_shanty_bld_shack02</td><td>0x57ADE56D</td><td>No</td></tr>
<tr><td>_shanty_bld_shack03</td><td>0x2DAB64B8</td><td>No</td></tr>
<tr><td>_shanty_bld_shack04</td><td>0x2F9E9BEB</td><td>No</td></tr>
<tr><td>_shanty_bld_shack05</td><td>0x4D9C8C8E</td><td>No</td></tr>
<tr><td>_shanty_bld_shack06</td><td>0xAFA3E299</td><td>No</td></tr>
<tr><td>_shanty_canvaslong</td><td>0x0AEC5052</td><td>No</td></tr>
<tr><td>_shanty_canvasshort</td><td>0x8DD8B7CA</td><td>No</td></tr>
<tr><td>_shanty_clotheslinea</td><td>0x98A1BEFF</td><td>No</td></tr>
<tr><td>_shanty_clotheslineb</td><td>0x8EA3EDD8</td><td>No</td></tr>
<tr><td>_shanty_concreteleft</td><td>0x5886172E</td><td>No</td></tr>
<tr><td>_shanty_concreteright</td><td>0x3BA5C55D</td><td>No</td></tr>
<tr><td>_shanty_dockB</td><td>0xD35B1049</td><td>No</td></tr>
<tr><td>_shanty_env_bush01</td><td>0x26FBE0CF</td><td>No</td></tr>
<tr><td>_shanty_env_bush02</td><td>0x9CFED928</td><td>No</td></tr>
<tr><td>_shanty_env_bush03</td><td>0x8700F51D</td><td>No</td></tr>
<tr><td>_shanty_env_tree01</td><td>0x1FAAA339</td><td>No</td></tr>
<tr><td>_shanty_env_tree02</td><td>0xBDA34D2E</td><td>No</td></tr>
<tr><td>_shanty_env_tree03</td><td>0x1FA6260B</td><td>No</td></tr>
<tr><td>_shanty_fencecorner01</td><td>0xDC8E2081</td><td>No</td></tr>
<tr><td>_shanty_fencestraight01</td><td>0x1592F8F8</td><td>No</td></tr>
<tr><td>_shanty_fencewood01</td><td>0xA578E4E9</td><td>No</td></tr>
<tr><td>_shanty_fencewood02</td><td>0x8371F39E</td><td>No</td></tr>
<tr><td>_shanty_plankA</td><td>0xA8DA8AE1</td><td>No</td></tr>
<tr><td>_shanty_polepower</td><td>0x2B84DD25</td><td>No</td></tr>
<tr><td>_shanty_shower</td><td>0xF48695FE</td><td>No</td></tr>
<tr><td>_shanty_telephonepolepair</td><td>0xFB99B8DE</td><td>No</td></tr>
<tr><td>_shanty_telephonepolesingle</td><td>0x78838436</td><td>No</td></tr>
<tr><td>_shanty_wallcorner01</td><td>0xE092ACA2</td><td>No</td></tr>
<tr><td>_shanty_wallcorner02</td><td>0x629A350D</td><td>No</td></tr>
<tr><td>_shanty_wallcorner03</td><td>0x3897B458</td><td>No</td></tr>
<tr><td>_shanty_walllargecorner01</td><td>0x1FF99F4F</td><td>No</td></tr>
<tr><td>_shanty_walllargestraight01</td><td>0xA2469366</td><td>No</td></tr>
<tr><td>_shanty_wallstraight01</td><td>0x7741A32B</td><td>No</td></tr>
<tr><td>_shanty_wallstraight02</td><td>0x9D441D94</td><td>No</td></tr>
<tr><td>_shanty_wallstraight03</td><td>0xF746E9D9</td><td>No</td></tr>
<tr><td>_sign01</td><td>0xC64F2C1E</td><td>No</td></tr>
<tr><td>_sign02</td><td>0xE8561D69</td><td>No</td></tr>
<tr><td>_sign03</td><td>0xCE53B5E4</td><td>No</td></tr>
<tr><td>_sign04</td><td>0x705B70AF</td><td>No</td></tr>
<tr><td>_sign05</td><td>0x4E58FC92</td><td>No</td></tr>
<tr><td>_sign06</td><td>0xD06084FD</td><td>No</td></tr>
<tr><td>_sign07</td><td>0x665D9F88</td><td>No</td></tr>
<tr><td>_sign08</td><td>0xC864F593</td><td>No</td></tr>
<tr><td>_sign09</td><td>0xE662E636</td><td>No</td></tr>
<tr><td>_sign10</td><td>0xDA090940</td><td>No</td></tr>
<tr><td>_sign11</td><td>0x040B89F5</td><td>No</td></tr>
<tr><td>_sign12</td><td>0xE20498AA</td><td>No</td></tr>
<tr><td>_sign13</td><td>0x04070CC7</td><td>No</td></tr>
<tr><td>_sign14</td><td>0x81FF845C</td><td>No</td></tr>
<tr><td>_sign15</td><td>0x7C01B981</td><td>No</td></tr>
<tr><td>_sign16</td><td>0xF9FA3116</td><td>No</td></tr>
<tr><td>_sign17</td><td>0x5BFD09F3</td><td>No</td></tr>
<tr><td>_sign18</td><td>0xF9F5B3E8</td><td>No</td></tr>
<tr><td>_sign19</td><td>0xE3F7CFDD</td><td>No</td></tr>
<tr><td>_sign20</td><td>0x6F71C291</td><td>No</td></tr>
<tr><td>_sign21</td><td>0x756F8D6C</td><td>No</td></tr>
<tr><td>_sign22</td><td>0x0F6CAE43</td><td>No</td></tr>
<tr><td>_sign23</td><td>0xED6A3A26</td><td>No</td></tr>
<tr><td>_sign24</td><td>0xF77B9305</td><td>No</td></tr>
<tr><td>_sign25</td><td>0x0D797710</td><td>No</td></tr>
<tr><td>_sign26</td><td>0xF77715D7</td><td>No</td></tr>
<tr><td>_sign27</td><td>0x95743CFA</td><td>No</td></tr>
<tr><td>_sign28</td><td>0x6F5E3AD9</td><td>No</td></tr>
<tr><td>_sign29</td><td>0x155B6E94</td><td>No</td></tr>
<tr><td>_sign30</td><td>0x1F9D7376</td><td>No</td></tr>
<tr><td>_sign31</td><td>0x019F82D3</td><td>No</td></tr>
<tr><td>_sign32</td><td>0x27A1FD3C</td><td>No</td></tr>
<tr><td>_sign33</td><td>0xA1A4FBE1</td><td>No</td></tr>
<tr><td>_sign34</td><td>0x87A7118A</td><td>No</td></tr>
<tr><td>_sign35</td><td>0xA9A985A7</td><td>No</td></tr>
<tr><td>_sign36</td><td>0xFFAC4BA0</td><td>No</td></tr>
<tr><td>_sign37</td><td>0x29AECC55</td><td>No</td></tr>
<tr><td>_sign38</td><td>0xFF89B95E</td><td>No</td></tr>
<tr><td>_sign39</td><td>0x218C2D7B</td><td>No</td></tr>
<tr><td>_sign40</td><td>0xA3EC08A7</td><td>No</td></tr>
<tr><td>_stealth_road10</td><td>0xA4EDCDD5</td><td>No</td></tr>
<tr><td>_streamer_maracaibo_e</td><td>0x0A6F5B9F</td><td>No</td></tr>
<tr><td>_streamer_maracaibo_n</td><td>0xA0860E10</td><td>No</td></tr>
<tr><td>_streamer_maracaibo_s</td><td>0xA2432B49</td><td>No</td></tr>
<tr><td>_streamer_maracaibo_w</td><td>0x0A4CC95D</td><td>No</td></tr>
<tr><td>_test_16x16_block</td><td>0xA48C9401</td><td>No</td></tr>
<tr><td>_test_32x32_block</td><td>0x64831FA5</td><td>No</td></tr>
<tr><td>_test_4x1_ramp</td><td>0x127F9387</td><td>No</td></tr>
<tr><td>_test_4x1_stick</td><td>0xF58EE529</td><td>No</td></tr>
<tr><td>_test_4x4_block</td><td>0x058B91AF</td><td>No</td></tr>
<tr><td>_underwater_minea</td><td>0x02B39BC4</td><td>No</td></tr>
<tr><td>_Vehicle (Immobile)</td><td>0xE538BEB5</td><td>Yes</td></tr>
<tr><td>_Vehicle (Old)</td><td>0x7B6F2B60</td><td>Yes</td></tr>
<tr><td>_Vehicle (Production Ready)</td><td>0xDE2704A1</td><td>Yes</td></tr>
<tr><td>_village_att_pierlong</td><td>0xD1ABEBB5</td><td>No</td></tr>
<tr><td>_village_att_piershort</td><td>0x755D477B</td><td>No</td></tr>
<tr><td>_village_bencha</td><td>0x12BFA394</td><td>No</td></tr>
<tr><td>_Village_bld_cattleranch</td><td>0x15D118AB</td><td>No</td></tr>
<tr><td>_Village_bld_docks</td><td>0xCC016B02</td><td>No</td></tr>
<tr><td>_Village_bld_docks02</td><td>0x9910FB38</td><td>No</td></tr>
<tr><td>_Village_bld_docks_Ruined</td><td>0x2F687078</td><td>No</td></tr>
<tr><td>_Village_bld_farmhouse</td><td>0xD3D977BE</td><td>No</td></tr>
<tr><td>_Village_bld_farming01</td><td>0x9E59885F</td><td>No</td></tr>
<tr><td>_Village_bld_farming02</td><td>0x145C80B8</td><td>No</td></tr>
<tr><td>_Village_bld_farming03</td><td>0x3E5F016D</td><td>No</td></tr>
<tr><td>_Village_bld_farming03_ruined</td><td>0x93F98141</td><td>No</td></tr>
<tr><td>_Village_bld_farming04</td><td>0x344DA88E</td><td>No</td></tr>
<tr><td>_Village_bld_farming05</td><td>0x164FB7EB</td><td>No</td></tr>
<tr><td>_Village_bld_farming05_ruined</td><td>0x7ADBB0CF</td><td>No</td></tr>
<tr><td>_Village_bld_food01</td><td>0xB046C41F</td><td>No</td></tr>
<tr><td>_Village_bld_food02</td><td>0x2649BC78</td><td>No</td></tr>
<tr><td>_Village_bld_food03</td><td>0x504C3D2D</td><td>No</td></tr>
<tr><td>_village_bld_gasstation</td><td>0xD1928BDB</td><td>No</td></tr>
<tr><td>_Village_bld_hangar</td><td>0x7EE71C1B</td><td>No</td></tr>
<tr><td>_Village_bld_hangar_Ruined</td><td>0x298E1CBF</td><td>No</td></tr>
<tr><td>_Village_bld_house01</td><td>0x4F2E5A1F</td><td>No</td></tr>
<tr><td>_Village_bld_house01_ruined</td><td>0x197E0DC3</td><td>No</td></tr>
<tr><td>_Village_bld_house02</td><td>0xC5315278</td><td>No</td></tr>
<tr><td>_Village_bld_house02_ruined</td><td>0x492C2946</td><td>No</td></tr>
<tr><td>_village_bld_housestilts01</td><td>0xDF865002</td><td>No</td></tr>
<tr><td>_village_bld_housestilts01_ruined</td><td>0x1E00F778</td><td>No</td></tr>
<tr><td>_village_bld_housestilts02</td><td>0x618DD86D</td><td>No</td></tr>
<tr><td>_village_bld_housestilts03</td><td>0x378B57B8</td><td>No</td></tr>
<tr><td>_village_bld_housestilts04</td><td>0x397E8EEB</td><td>No</td></tr>
<tr><td>_Village_bld_housestilts05</td><td>0x577C7F8E</td><td>No</td></tr>
<tr><td>_Village_bld_housestilts05_ruined</td><td>0x8DBB3134</td><td>No</td></tr>
<tr><td>_village_bld_outhouse</td><td>0x64C2EA2E</td><td>No</td></tr>
<tr><td>_village_bld_plantation01</td><td>0xC04C2E39</td><td>No</td></tr>
<tr><td>_village_bld_plantation02</td><td>0x5E44D82E</td><td>No</td></tr>
<tr><td>_village_bld_plantation03</td><td>0xC047B10B</td><td>No</td></tr>
<tr><td>_village_bld_plantationsmall01</td><td>0x0D2693B0</td><td>No</td></tr>
<tr><td>_village_bld_plantationsmall02</td><td>0xF7243277</td><td>No</td></tr>
<tr><td>_village_bld_plantationsmall02_ruined</td><td>0x972E047B</td><td>No</td></tr>
<tr><td>_village_bld_plantationsmall03</td><td>0x1522231A</td><td>No</td></tr>
<tr><td>_village_bld_shackovergrown01</td><td>0x3E54BBB0</td><td>No</td></tr>
<tr><td>_Village_bld_shacksmall01</td><td>0xDA4F734E</td><td>No</td></tr>
<tr><td>_Village_bld_shacksmall01_ruined</td><td>0x656B64F4</td><td>No</td></tr>
<tr><td>_village_bld_shacksmall02</td><td>0x3C56C959</td><td>No</td></tr>
<tr><td>_village_bld_shacksmall02_Ruined</td><td>0x120AFA6D</td><td>No</td></tr>
<tr><td>_village_bld_shacksmall03</td><td>0xE253FD14</td><td>No</td></tr>
<tr><td>_village_bld_shacksmall03_ruined</td><td>0xD3CF6F22</td><td>No</td></tr>
<tr><td>_village_bld_shacksmall04</td><td>0x445B531F</td><td>No</td></tr>
<tr><td>_Village_bld_toolshed</td><td>0xFF3E3C56</td><td>No</td></tr>
<tr><td>_Village_bld_watchtower01</td><td>0x8F9B3643</td><td>No</td></tr>
<tr><td>_Village_bld_watchtower02</td><td>0xF59E156C</td><td>No</td></tr>
<tr><td>_Village_bld_watchtower03</td><td>0xEFA04A91</td><td>No</td></tr>
<tr><td>_Village_bld_windmill01</td><td>0xB25A949B</td><td>No</td></tr>
<tr><td>_Village_bld_windmillbroken</td><td>0x731597AD</td><td>No</td></tr>
<tr><td>_village_campfire</td><td>0xF16D962C</td><td>No</td></tr>
<tr><td>_village_cota</td><td>0xE2799EE8</td><td>No</td></tr>
<tr><td>_village_fencewood01</td><td>0x729B9AD0</td><td>No</td></tr>
<tr><td>_village_fencewood02</td><td>0x5C993997</td><td>No</td></tr>
<tr><td>_village_fruitboxstacka</td><td>0x756A0B03</td><td>No</td></tr>
<tr><td>_village_fruitboxstackb</td><td>0xDB6CEA2C</td><td>No</td></tr>
<tr><td>_village_fruitboxstackc</td><td>0xD56F1F51</td><td>No</td></tr>
<tr><td>_village_fruitboxstackd</td><td>0xFB7199BA</td><td>No</td></tr>
<tr><td>_village_ladderwooda</td><td>0x85A82315</td><td>No</td></tr>
<tr><td>_village_lampcolemana</td><td>0x855E87C3</td><td>No</td></tr>
<tr><td>_village_postthin</td><td>0x52A39764</td><td>No</td></tr>
<tr><td>_village_postwide</td><td>0x8C05E6C4</td><td>No</td></tr>
<tr><td>_village_prop_chaira</td><td>0x4E88605B</td><td>No</td></tr>
<tr><td>_village_prop_tentsmallpupa</td><td>0xFFAC5A91</td><td>No</td></tr>
<tr><td>_village_stairs</td><td>0x2072AC75</td><td>No</td></tr>
<tr><td>_village_tablewooda</td><td>0x84E2E827</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_alarmtower</td><td>0xB015A102</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_alarmtower_ruined</td><td>0x00A16278</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrack</td><td>0x3D078262</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrack_ruined</td><td>0xF5B28258</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackabandoned</td><td>0xB9BA6C86</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker</td><td>0xBF32FF01</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_AL</td><td>0xCE7223B7</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_CH</td><td>0x0D121909</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_GR</td><td>0x47567E8F</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_OC</td><td>0x5EE52EDA</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_PR</td><td>0x4D5D05FA</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_ruined</td><td>0x92B36555</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackbunkerabandoned</td><td>0x3E81BC13</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced</td><td>0x23E4CC43</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_AL</td><td>0xCE3EDED1</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_CH</td><td>0x2F50337F</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_GR</td><td>0x1268F4E9</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_OC</td><td>0x11F77F6C</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_PR</td><td>0x4CF82448</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforcedabandoned</td><td>0x9FCA6061</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barracktent</td><td>0xBE0103C5</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barracktent_AL</td><td>0xF0CBA403</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barracktent_CH</td><td>0x7D0535FD</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barracktent_GR</td><td>0xC2DE1C0B</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barracktent_OC</td><td>0x27E98286</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barracktent_PR</td><td>0x920621FE</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_barracktent_ruined</td><td>0x6BF67E59</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_bunker</td><td>0xB6AE801F</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garage</td><td>0xB90CBD9B</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garage_AL</td><td>0x1F388B59</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garage_CH</td><td>0xA274C987</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garage_GR</td><td>0xE604E361</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garage_OC</td><td>0x52C0A494</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garage_PR</td><td>0xFE197760</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garagebunker</td><td>0xB19DDBAC</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_AL</td><td>0xE49E9CBC</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_CH</td><td>0x8379C056</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_GR</td><td>0x35F07F90</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_OC</td><td>0x866272FD</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_PR</td><td>0x78D68631</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_guardtower</td><td>0xBA7BB30E</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_guardtower_AL</td><td>0xC39B6AE6</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_guardtower_CH</td><td>0x44ACF1F4</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_guardtower_GR</td><td>0x900B7B9A</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_guardtower_OC</td><td>0x8B4ECB1F</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_guardtower_PR</td><td>0x8A04F42F</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_guardtower_ruined</td><td>0x6DF4AFB4</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_hangar</td><td>0x0E8CCD09</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_hangar_AL</td><td>0xDD1B358F</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_hangar_CH</td><td>0xFC0AAA61</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_hangar_GR</td><td>0x9676B677</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_hangar_OC</td><td>0x7D5DEBB2</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_hangar_PR</td><td>0xA1338882</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_hangarbunker</td><td>0x4C7B99C2</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_helipad</td><td>0x7ADCACC3</td><td>Yes</td></tr>
<tr><td>_vzoutpost_bld_pillbox</td><td>0xAF28FC30</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_pillbox_ruined</td><td>0x13FAEE9E</td><td>No</td></tr>
<tr><td>_vzoutpost_bld_pillboxabandoned</td><td>0xDC44B210</td><td>No</td></tr>
<tr><td>_vzoutpost_fueltanks</td><td>0xC8CA3A68</td><td>Yes</td></tr>
<tr><td>_vzoutpost_fueltanks_PmcCon018</td><td>0x21A4DB9A</td><td>Yes</td></tr>
<tr><td>_vzoutpost_fueltanks_ruined</td><td>0xEEB1FDF6</td><td>Yes</td></tr>
<tr><td>_vzoutpost_gatewall_GR</td><td>0x5B462DE0</td><td>No</td></tr>
<tr><td>_vzoutpost_walla</td><td>0x3AF501BE</td><td>No</td></tr>
<tr><td>_vzoutpost_walla_AL</td><td>0xD3F86B56</td><td>No</td></tr>
<tr><td>_vzoutpost_walla_CH</td><td>0x15098DA4</td><td>No</td></tr>
<tr><td>_vzoutpost_walla_GR</td><td>0x60B7C92A</td><td>No</td></tr>
<tr><td>_vzoutpost_walla_oc</td><td>0x9BABCB8F</td><td>No</td></tr>
<tr><td>_vzoutpost_wallA_PR</td><td>0x7825E09F</td><td>No</td></tr>
<tr><td>_vzoutpost_wallb</td><td>0xDCFCBC89</td><td>No</td></tr>
<tr><td>_vzoutpost_wallb_AL</td><td>0xC95CE00F</td><td>No</td></tr>
<tr><td>_vzoutpost_wallb_CH</td><td>0xE84C54E1</td><td>No</td></tr>
<tr><td>_vzoutpost_wallb_GR</td><td>0x82B860F7</td><td>No</td></tr>
<tr><td>_vzoutpost_wallb_oc</td><td>0x699F9632</td><td>No</td></tr>
<tr><td>_vzoutpost_wallB_PR</td><td>0x8D753302</td><td>No</td></tr>
<tr><td>_vzoutpost_wallgate</td><td>0x3F5E24C4</td><td>No</td></tr>
<tr><td>_vzoutpost_wallgate_AL</td><td>0x093B0CE4</td><td>No</td></tr>
<tr><td>_vzoutpost_wallgate_OC</td><td>0xFDF85725</td><td>No</td></tr>
<tr><td>_vzoutpost_wallgate_PR</td><td>0xC25082C9</td><td>No</td></tr>
<tr><td>_white_bld_corner16x16a</td><td>0x85141433</td><td>No</td></tr>
<tr><td>_white_bld_corner16x16a_ruined</td><td>0x8261B337</td><td>No</td></tr>
<tr><td>_white_bld_corner16x16b</td><td>0xAB168E9C</td><td>No</td></tr>
<tr><td>_white_bld_corner16x16b_ruined</td><td>0xAD04F78A</td><td>No</td></tr>
<tr><td>_white_bld_corner8x16a</td><td>0x882C056E</td><td>No</td></tr>
<tr><td>_white_bld_corner8x16a_ruined</td><td>0x73172994</td><td>No</td></tr>
<tr><td>_white_bld_corner8x16b</td><td>0xEA335B79</td><td>No</td></tr>
<tr><td>_white_bld_corner8x16b_ruined</td><td>0x8B61580D</td><td>No</td></tr>
<tr><td>_white_bld_corner8x8a</td><td>0x1033A6B9</td><td>No</td></tr>
<tr><td>_white_bld_corner8x8a_ruined</td><td>0x5EE0AE4D</td><td>No</td></tr>
<tr><td>_white_bld_corner8x8b</td><td>0xAE2C50AE</td><td>No</td></tr>
<tr><td>_white_bld_corner8x8b_ruined</td><td>0xA8B95BD4</td><td>No</td></tr>
<tr><td>_white_bld_corner8x8c</td><td>0x102F298B</td><td>No</td></tr>
<tr><td>_white_bld_corner8x8c_ruined</td><td>0xBD4679EF</td><td>No</td></tr>
<tr><td>_white_bld_segment16x16a</td><td>0xD04E4EBD</td><td>No</td></tr>
<tr><td>_white_bld_segment16x16a_ruined</td><td>0x51C256D1</td><td>No</td></tr>
<tr><td>_white_bld_segment8x16a</td><td>0x1784EFB8</td><td>No</td></tr>
<tr><td>_white_bld_segment8x16a_ruined</td><td>0x9B007386</td><td>No</td></tr>
<tr><td>_white_bld_segment8x16b</td><td>0xA181F75F</td><td>No</td></tr>
<tr><td>_white_bld_segment8x16b_ruined</td><td>0x90A13303</td><td>No</td></tr>
<tr><td>_white_bld_segment8x8a</td><td>0x8452890B</td><td>No</td></tr>
<tr><td>_white_bld_segment8x8a_ruined</td><td>0x07C71C6F</td><td>No</td></tr>
<tr><td>_white_freewaytrenchbridge01_overpass_autobridge</td><td>0x9033E10A</td><td>No</td></tr>
<tr><td>_white_freewaytrenchbridge01_underpass</td><td>0x3783B2E9</td><td>No</td></tr>
<tr><td>_white_merge_brick</td><td>0x7C671538</td><td>No</td></tr>
<tr><td>_white_merge_dirt</td><td>0xFE900046</td><td>No</td></tr>
<tr><td>_white_mergebrick</td><td>0x0A713425</td><td>No</td></tr>
<tr><td>_white_road10</td><td>0x402F5EAB</td><td>No</td></tr>
<tr><td>_white_road10cross</td><td>0xC1D5C7E1</td><td>No</td></tr>
<tr><td>_white_road10cross5</td><td>0x74506BF2</td><td>No</td></tr>
<tr><td>_white_road10l</td><td>0x343FA8D5</td><td>No</td></tr>
<tr><td>_white_road10t</td><td>0x3453308D</td><td>No</td></tr>
<tr><td>_white_road10t5</td><td>0x7BA8DD5E</td><td>No</td></tr>
<tr><td>_white_road5</td><td>0x0B1184A5</td><td>No</td></tr>
<tr><td>_white_road5cross</td><td>0x809AD98B</td><td>No</td></tr>
<tr><td>_white_road5l</td><td>0x92E62E1B</td><td>No</td></tr>
<tr><td>_white_road5t</td><td>0x13218EC3</td><td>No</td></tr>
<tr><td>_white_road5t10</td><td>0x238CC3E0</td><td>No</td></tr>
<tr><td>_white_road_merge01</td><td>0x51131270</td><td>No</td></tr>
<tr><td>_white_sidewalk</td><td>0x4DC93618</td><td>No</td></tr>
<tr><td>_white_sidewalk02</td><td>0x2AA416B2</td><td>No</td></tr>
<tr><td>_white_sidewalksmall</td><td>0x051DCF81</td><td>No</td></tr>
<tr><td>_white_wallcorner</td><td>0x275B525D</td><td>No</td></tr>
<tr><td>_white_wallcorner_pristine</td><td>0x03131C28</td><td>No</td></tr>
<tr><td>_white_walllong</td><td>0xE69D1104</td><td>No</td></tr>
<tr><td>_white_walllong_pristine</td><td>0x92CDFB03</td><td>No</td></tr>
<tr><td>_white_wallshort</td><td>0x4A59C690</td><td>No</td></tr>
<tr><td>_white_wallshort_pristine</td><td>0x554AE977</td><td>No</td></tr>
<tr><td>A10</td><td>0xD035894D</td><td>No</td></tr>
<tr><td>A8 15m DeadEnd</td><td>0xAB804258</td><td>No</td></tr>
<tr><td>A8 15m Four</td><td>0x2721975F</td><td>No</td></tr>
<tr><td>A8 15m L</td><td>0x457F5FFD</td><td>No</td></tr>
<tr><td>A8 15m Road</td><td>0xAE748E09</td><td>No</td></tr>
<tr><td>A8 15m T</td><td>0xC5BAC0A5</td><td>No</td></tr>
<tr><td>A8 Enemy</td><td>0xD4A0D006</td><td>No</td></tr>
<tr><td>AA (Advanced)</td><td>0x6B27034E</td><td>No</td></tr>
<tr><td>AA (Basic)</td><td>0x9954F398</td><td>No</td></tr>
<tr><td>AA (Jammer)</td><td>0x3A8084E0</td><td>No</td></tr>
<tr><td>AA (Medium)</td><td>0xA4045DDB</td><td>No</td></tr>
<tr><td>AA Missile</td><td>0x4FCA603B</td><td>No</td></tr>
<tr><td>AA Missile (amraam)</td><td>0xB4C61361</td><td>No</td></tr>
<tr><td>abatters</td><td>0x695C8E03</td><td>No</td></tr>
<tr><td>Action Hijack Prop (Grenade)</td><td>0x7984A387</td><td>No</td></tr>
<tr><td>Action Hijack Prop (Pistol)</td><td>0x456017C2</td><td>No</td></tr>
<tr><td>Action Hijack Prop (Rifle)</td><td>0xC736471B</td><td>No</td></tr>
<tr><td>AH1Z</td><td>0x2FF37317</td><td>Yes</td></tr>
<tr><td>AH1Z (Driver)</td><td>0x7337DAC2</td><td>Yes</td></tr>
<tr><td>AH1Z (Ewan)</td><td>0xB8AE263B</td><td>Yes</td></tr>
<tr><td>AH1Z (Full)</td><td>0x9E563131</td><td>Yes</td></tr>
<tr><td>Aid Worker (Female)</td><td>0x8BA8A22A</td><td>No</td></tr>
<tr><td>Aid Worker Male</td><td>0xC53404FC</td><td>No</td></tr>
<tr><td>Air Boat</td><td>0xB017A293</td><td>Yes</td></tr>
<tr><td>Air Boat (Driver)</td><td>0xBDDE21EE</td><td>Yes</td></tr>
<tr><td>Air Boat (Driver) (Civ Poor female)</td><td>0xC71ACCBD</td><td>Yes</td></tr>
<tr><td>Air Boat (Driver) (Civ Poor male)</td><td>0x5BB2AF10</td><td>Yes</td></tr>
<tr><td>Air Boat (Full)</td><td>0xEB754F35</td><td>Yes</td></tr>
<tr><td>Airboat_Driver</td><td>0x5877732E</td><td>Yes</td></tr>
<tr><td>Airstrike AA Missile</td><td>0x57A81395</td><td>No</td></tr>
<tr><td>Airstrike AT Missile</td><td>0x99178348</td><td>No</td></tr>
<tr><td>AL Baseball Bat</td><td>0x8370A9EF</td><td>No</td></tr>
<tr><td>AL Defender (AA)</td><td>0x4DB3557A</td><td>No</td></tr>
<tr><td>AL Defender (AT)</td><td>0x60CB7BF5</td><td>No</td></tr>
<tr><td>AL Defender (AT) (Window Spawner)</td><td>0xE62D4B32</td><td>No</td></tr>
<tr><td>AL Defender (MG)</td><td>0xF2A22EA0</td><td>No</td></tr>
<tr><td>AL Defender (Rifle)</td><td>0x4791BB94</td><td>No</td></tr>
<tr><td>AL Golf Club</td><td>0x0FA8CB7A</td><td>No</td></tr>
<tr><td>ALHQSpawnList</td><td>0xD4D6A410</td><td>No</td></tr>
<tr><td>AllCon003_Peng</td><td>0x55012554</td><td>No</td></tr>
<tr><td>AllDbSpawner</td><td>0xDB7FA4B4</td><td>No</td></tr>
<tr><td>AllDbSpawner (Squad Full AT)</td><td>0x7F637141</td><td>No</td></tr>
<tr><td>AllDbSpawner (Squad Half AT)</td><td>0x293FB845</td><td>No</td></tr>
<tr><td>AllDbSpawner (Squad Quarter AT)</td><td>0x7FA52B06</td><td>No</td></tr>
<tr><td>AllDbSpawner (Squad)</td><td>0x38CF880B</td><td>No</td></tr>
<tr><td>AllHq_Interior</td><td>0xC8EF281E</td><td>No</td></tr>
<tr><td>Allied</td><td>0xBBC34EF4</td><td>No</td></tr>
<tr><td>Allied Airborne</td><td>0xC9010376</td><td>No</td></tr>
<tr><td>Allied Airborne (AT)</td><td>0x7F4797AA</td><td>No</td></tr>
<tr><td>Allied Airborne (Light MG)</td><td>0xC357E50F</td><td>No</td></tr>
<tr><td>Allied Boss</td><td>0xAC3B6A63</td><td>No</td></tr>
<tr><td>Allied Boss (Invincible)</td><td>0xD8ABEF7D</td><td>No</td></tr>
<tr><td>Allied Boss (Wheelchair)</td><td>0x28DBE71C</td><td>No</td></tr>
<tr><td>Allied Destroyer</td><td>0x4D9AEFA3</td><td>Yes</td></tr>
<tr><td>Allied Destroyer (Full)</td><td>0xEB3948C5</td><td>Yes</td></tr>
<tr><td>Allied Destroyer (Jammer)</td><td>0xA4E888AC</td><td>Yes</td></tr>
<tr><td>Allied Heavy (AA)</td><td>0x271F10CC</td><td>No</td></tr>
<tr><td>Allied Heavy (AT Rocket)</td><td>0xD18F961F</td><td>No</td></tr>
<tr><td>Allied Heavy (Light MG)</td><td>0x3BC90F3E</td><td>No</td></tr>
<tr><td>Allied Medic</td><td>0x2A36FD82</td><td>No</td></tr>
<tr><td>Allied Officer</td><td>0x01BDAD6E</td><td>No</td></tr>
<tr><td>Allied Paratrooper</td><td>0xBF4829E3</td><td>No</td></tr>
<tr><td>Allied Pilot</td><td>0xACA6923E</td><td>No</td></tr>
<tr><td>Allied Pilot (God)</td><td>0x218470B5</td><td>No</td></tr>
<tr><td>Allied Prisoner</td><td>0xC526991C</td><td>No</td></tr>
<tr><td>Allied Sailor</td><td>0xE2A857D8</td><td>No</td></tr>
<tr><td>Allied Sailor (AA)</td><td>0xBF287DA3</td><td>No</td></tr>
<tr><td>Allied Sailor (Light MG)</td><td>0xE593B215</td><td>No</td></tr>
<tr><td>Allied Soldier</td><td>0xC864E4A2</td><td>No</td></tr>
<tr><td>Allied Soldier (Bench Press)</td><td>0x297C6502</td><td>No</td></tr>
<tr><td>Allied Soldier (Hip Hop Dancing)</td><td>0x68813B31</td><td>No</td></tr>
<tr><td>Allied Starter 01</td><td>0x050E6C22</td><td>No</td></tr>
<tr><td>Allied Starter 02</td><td>0x8715F48D</td><td>No</td></tr>
<tr><td>Allied Starter 03</td><td>0x5D1373D8</td><td>No</td></tr>
<tr><td>Allied Starter 04</td><td>0xDF07748B</td><td>No</td></tr>
<tr><td>Allied Starter 05</td><td>0x7D049BAE</td><td>No</td></tr>
<tr><td>Allied Starters</td><td>0x183F7210</td><td>No</td></tr>
<tr><td>Allied Worker</td><td>0x5AACD022</td><td>No</td></tr>
<tr><td>Allied Worker (Baseball)</td><td>0x0F837BD3</td><td>No</td></tr>
<tr><td>Allied Worker (Golf)</td><td>0xBC664A97</td><td>No</td></tr>
<tr><td>Allied Worker B</td><td>0x64B0DDB8</td><td>No</td></tr>
<tr><td>AlliedHQDbSpawner</td><td>0x729E051D</td><td>No</td></tr>
<tr><td>AlliesSkirmishTest</td><td>0xD181EFFB</td><td>No</td></tr>
<tr><td>Alouette 3 Transport (VZ) (Delivery)</td><td>0x76B96B2A</td><td>Yes</td></tr>
<tr><td>Alouette3 (base)</td><td>0x725FE691</td><td>Yes</td></tr>
<tr><td>Alouette3 Attack (base)</td><td>0x9217A97B</td><td>Yes</td></tr>
<tr><td>Alouette3 Attack (PR)</td><td>0xD944EA90</td><td>Yes</td></tr>
<tr><td>Alouette3 Attack (PR) (Driver)</td><td>0x597C43AF</td><td>Yes</td></tr>
<tr><td>Alouette3 Attack (PR) (Ewan)</td><td>0x5076A026</td><td>Yes</td></tr>
<tr><td>Alouette3 Attack (PR) (Full)</td><td>0x422E9BE4</td><td>Yes</td></tr>
<tr><td>Alouette3 Attack (VZ)</td><td>0x0384A0EE</td><td>Yes</td></tr>
<tr><td>Alouette3 Attack (VZ) (Driver)</td><td>0x10440985</td><td>Yes</td></tr>
<tr><td>Alouette3 Attack (VZ) (Ewan)</td><td>0x76908A00</td><td>Yes</td></tr>
<tr><td>Alouette3 Attack (VZ) (Full)</td><td>0xDB44C532</td><td>Yes</td></tr>
<tr><td>Alouette3 Elite</td><td>0x3D582382</td><td>Yes</td></tr>
<tr><td>Alouette3 Elite (Driver)</td><td>0x34CE8229</td><td>Yes</td></tr>
<tr><td>Alouette3 Elite (Ewan)</td><td>0x5F7B68E4</td><td>Yes</td></tr>
<tr><td>Alouette3 Elite (Full)</td><td>0x4656350E</td><td>Yes</td></tr>
<tr><td>Alouette3 Superiority</td><td>0x048DB4E4</td><td>Yes</td></tr>
<tr><td>Alouette3 Superiority (Driver)</td><td>0xC3E6EDC3</td><td>Yes</td></tr>
<tr><td>Alouette3 Superiority (Ewan)</td><td>0x63E0E84A</td><td>Yes</td></tr>
<tr><td>Alouette3 SuperiorityElite (Base)</td><td>0xF2FF732B</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport</td><td>0x4B481510</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (PR)</td><td>0x1C12B15F</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (PR) (Driver)</td><td>0x8DFF774A</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (PR) (Ewan)</td><td>0x2EEC9423</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (PR) (Extraction)</td><td>0x00DC7AB9</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (PR) (Full)</td><td>0xD41A4509</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (PR) (Pursuit)</td><td>0x59787A94</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (VZ)</td><td>0x3AAD2021</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (VZ) (Driver)</td><td>0x1A774D3C</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (VZ) (Ewan)</td><td>0xEF9E6839</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (VZ) (Pursuit)</td><td>0x4D3FA01E</td><td>Yes</td></tr>
<tr><td>Alouette3 Transport (VZA Intro) (Driver)</td><td>0x71A0FFFF</td><td>Yes</td></tr>
<tr><td>Altagracia Test Traffic (VZ)</td><td>0x9537357E</td><td>No</td></tr>
<tr><td>Ambulance</td><td>0xDC065B95</td><td>Yes</td></tr>
<tr><td>Ambulance (Driver)</td><td>0x26FA5C20</td><td>Yes</td></tr>
<tr><td>Ambulance (Driver) (Civ Doctor 2 female)</td><td>0x2077F55C</td><td>Yes</td></tr>
<tr><td>Ambulance (Driver) (Civ Doctor female)</td><td>0x713DE192</td><td>Yes</td></tr>
<tr><td>Ambulance_Driver</td><td>0xE80E4896</td><td>Yes</td></tr>
<tr><td>Ammo Pickup (1xC4)</td><td>0x00C8F9AC</td><td>No</td></tr>
<tr><td>Ammo Pickup (Bullet)</td><td>0x4E3F3CE6</td><td>No</td></tr>
<tr><td>Ammo Pickup (Full C4)</td><td>0x789E2A14</td><td>No</td></tr>
<tr><td>Ammo Pickup (Grenades)</td><td>0xD5F15751</td><td>No</td></tr>
<tr><td>Ammo Pickup (Rocket)</td><td>0xA79D21D2</td><td>No</td></tr>
<tr><td>Ammo Pickup (Single Grenade)</td><td>0xC475E2EC</td><td>No</td></tr>
<tr><td>Ammo Pickup (Small)</td><td>0x500E0DC7</td><td>No</td></tr>
<tr><td>ammo_designator_beacon</td><td>0xC6B65A9B</td><td>No</td></tr>
<tr><td>ammo_designator_beacon_light</td><td>0x13CC5386</td><td>No</td></tr>
<tr><td>AMX30</td><td>0x36AEDE98</td><td>Yes</td></tr>
<tr><td>AMX30 (Base)</td><td>0x7D2C4AA0</td><td>Yes</td></tr>
<tr><td>AMX30 (Driver)</td><td>0xA5572877</td><td>Yes</td></tr>
<tr><td>Amx30 (Full)</td><td>0x48B454BC</td><td>Yes</td></tr>
<tr><td>AMX30 (Tanks)</td><td>0x5069957C</td><td>Yes</td></tr>
<tr><td>AMX30 AA</td><td>0x45D11D72</td><td>Yes</td></tr>
<tr><td>AMX30 AA (Driver)</td><td>0xF2A84619</td><td>Yes</td></tr>
<tr><td>AMX30 Elite</td><td>0x3F6EDBED</td><td>Yes</td></tr>
<tr><td>AMX30 Elite (Driver)</td><td>0x6648F4F8</td><td>Yes</td></tr>
<tr><td>AMX30 Elite (Full)</td><td>0x901B8C7F</td><td>Yes</td></tr>
<tr><td>AMX30_RUIN</td><td>0x421F2DE1</td><td>Yes</td></tr>
<tr><td>AMXFullSpawnlist</td><td>0x1AC7CF1F</td><td>No</td></tr>
<tr><td>Antenna</td><td>0x1D49104E</td><td>No</td></tr>
<tr><td>Anti-Material Rifle</td><td>0x3326597B</td><td>No</td></tr>
<tr><td>Anti-Material Rifle (KSVK)</td><td>0x050B3C39</td><td>No</td></tr>
<tr><td>Anti-Material Rifle Bullet</td><td>0xA4B7629D</td><td>No</td></tr>
<tr><td>AP Autocannon Shell</td><td>0x91A508E2</td><td>No</td></tr>
<tr><td>AP Autocannon Shell (CH)</td><td>0xF842A460</td><td>No</td></tr>
<tr><td>APC</td><td>0x9CDBD62D</td><td>Yes</td></tr>
<tr><td>APC_Passenger</td><td>0x15D3C4A4</td><td>Yes</td></tr>
<tr><td>Armor (Building)</td><td>0x434436BF</td><td>No</td></tr>
<tr><td>Armor (Bunker)</td><td>0x9FA80226</td><td>No</td></tr>
<tr><td>Armor (Hero)</td><td>0xBFCEDA4F</td><td>No</td></tr>
<tr><td>Armor (Human)</td><td>0xC37C574A</td><td>No</td></tr>
<tr><td>Armor (HVT)</td><td>0x12E4336D</td><td>No</td></tr>
<tr><td>Armor (Light)</td><td>0x64F3FB33</td><td>No</td></tr>
<tr><td>Armor (Medium)</td><td>0x6E97F4AC</td><td>No</td></tr>
<tr><td>Armor (Prop)</td><td>0x6759484A</td><td>No</td></tr>
<tr><td>Armor (Prop.Fragile)</td><td>0xD97E8024</td><td>No</td></tr>
<tr><td>Armor (Road)</td><td>0x0B7B8D99</td><td>No</td></tr>
<tr><td>Armor (Tank)</td><td>0x17FACC4F</td><td>Yes</td></tr>
<tr><td>Armor (Terrain)</td><td>0x9C8D8282</td><td>No</td></tr>
<tr><td>Armor (Vegetation)</td><td>0xAE5E289B</td><td>No</td></tr>
<tr><td>Armor (Vehicle)</td><td>0x8260A047</td><td>No</td></tr>
<tr><td>Armored Bank Truck</td><td>0x2F0DA5B8</td><td>Yes</td></tr>
<tr><td>Armored Bank Truck (driver)</td><td>0xBEB9DA97</td><td>Yes</td></tr>
<tr><td>Armored Bank Truck (Driver) (Civ Taxi Driver male)</td><td>0xE915BA21</td><td>Yes</td></tr>
<tr><td>Armored Bank Truck_Driver</td><td>0xD3EFA565</td><td>Yes</td></tr>
<tr><td>Artillery Shell</td><td>0xC05F0F87</td><td>No</td></tr>
<tr><td>Artillery Smoke Shell</td><td>0x84C5189C</td><td>No</td></tr>
<tr><td>Assault Rifle</td><td>0x8387E850</td><td>No</td></tr>
<tr><td>Assault Rifle (VZ)</td><td>0x72DBE6E1</td><td>No</td></tr>
<tr><td>Assault Rifle (VZ) (Window Spawner)</td><td>0xEC1A6E46</td><td>No</td></tr>
<tr><td>Assault Rifle (Window Spawner)</td><td>0x9A0D0F39</td><td>No</td></tr>
<tr><td>Assault Rifle Bullet</td><td>0xA0D42D08</td><td>No</td></tr>
<tr><td>Assault Rifle Bullet (GR)</td><td>0x6EF0F048</td><td>No</td></tr>
<tr><td>AT Missile</td><td>0xFC44785E</td><td>No</td></tr>
<tr><td>AT Missile (CH)</td><td>0x8893FB24</td><td>No</td></tr>
<tr><td>AT Rocket</td><td>0x1153B156</td><td>No</td></tr>
<tr><td>Atmosphere</td><td>0x04047F6D</td><td>No</td></tr>
<tr><td>Atmosphere (interior)</td><td>0xDD9463C2</td><td>No</td></tr>
<tr><td>Audible (Vehicle HIGH)</td><td>0x1D04192A</td><td>No</td></tr>
<tr><td>Audible (Vehicle LOW)</td><td>0x52C5A3FE</td><td>No</td></tr>
<tr><td>Audible (Vehicle MEDIUM)</td><td>0xDED48B6D</td><td>No</td></tr>
<tr><td>Austin (base)</td><td>0xB2CDBC45</td><td>No</td></tr>
<tr><td>Austin (CIV)</td><td>0xCEBC1D68</td><td>No</td></tr>
<tr><td>Austin (CIV) (Driver)</td><td>0x4768D8C7</td><td>No</td></tr>
<tr><td>Austin (CIV) (Driver) (Mechanic male)</td><td>0x6663D1C1</td><td>No</td></tr>
<tr><td>Austin (Civ) (Full)</td><td>0x3C10400C</td><td>No</td></tr>
<tr><td>Austin (OC)</td><td>0x99691E22</td><td>No</td></tr>
<tr><td>Austin (OC) (Driver)</td><td>0x3A3FD9C9</td><td>No</td></tr>
<tr><td>Austin (OC) (Full)</td><td>0x59183AAE</td><td>No</td></tr>
<tr><td>Austin_Driver</td><td>0x5B327388</td><td>No</td></tr>
<tr><td>Autocannon Shell (AL)</td><td>0xE235626F</td><td>No</td></tr>
<tr><td>Autocannon Shell (GR)</td><td>0x7638E52B</td><td>No</td></tr>
<tr><td>Automatic Rifle</td><td>0x388A8AE8</td><td>No</td></tr>
<tr><td>Automatic Rifle (Chinese)</td><td>0x4BEC74A2</td><td>No</td></tr>
<tr><td>Automatic Rifle (GR)</td><td>0xBF4E2628</td><td>No</td></tr>
<tr><td>Automatic Rifle Bullet</td><td>0xBC623E70</td><td>No</td></tr>
<tr><td>Automatic Rifle Bullet (CH)</td><td>0x07CC98C6</td><td>No</td></tr>
<tr><td>Automatic Rifle Bullet (GR)</td><td>0x71DD9D80</td><td>No</td></tr>
<tr><td>Autopistol Bullet</td><td>0x76146767</td><td>No</td></tr>
<tr><td>Avenger (Cargo)</td><td>0x334FCB0C</td><td>No</td></tr>
<tr><td>b52_ghost</td><td>0x8307FF04</td><td>No</td></tr>
<tr><td>Barco</td><td>0xAC33E162</td><td>No</td></tr>
<tr><td>Barco (Driver)</td><td>0x33F98B89</td><td>No</td></tr>
<tr><td>Barco (Driver) (Civ Poor female)</td><td>0xC0AD2F6E</td><td>No</td></tr>
<tr><td>Barco (Driver) (Civ Poor male)</td><td>0x551E7EA3</td><td>No</td></tr>
<tr><td>Barco_Driver</td><td>0xC38D6323</td><td>No</td></tr>
<tr><td>Barrel_Hijack_Entrance</td><td>0x12673ECD</td><td>No</td></tr>
<tr><td>Basic4Way</td><td>0xDE7BB098</td><td>No</td></tr>
<tr><td>basicTestRoad</td><td>0xA935C8AB</td><td>No</td></tr>
<tr><td>battle_med (30x30)</td><td>0x465C372F</td><td>No</td></tr>
<tr><td>battle_med_100mRadius 0x8000a6e8</td><td>0x43B98313</td><td>No</td></tr>
<tr><td>battle_med_150mRadius 0x8000a6ea</td><td>0xC9F53405</td><td>No</td></tr>
<tr><td>battle_med_250mRadius 0x8000a6e9</td><td>0xA3400AE6</td><td>No</td></tr>
<tr><td>battle_med_300mRadius 0x8000a6e7</td><td>0x2FDC5BEA</td><td>No</td></tr>
<tr><td>Beacon Designator</td><td>0x689CE209</td><td>No</td></tr>
<tr><td>Bench Seat (Left)</td><td>0x2FEB65F0</td><td>No</td></tr>
<tr><td>Bench Seat (Right)</td><td>0x353C04FB</td><td>No</td></tr>
<tr><td>benches</td><td>0x431E175D</td><td>No</td></tr>
<tr><td>Binoculars</td><td>0xA0332C77</td><td>No</td></tr>
<tr><td>Blanco</td><td>0x5E5548C8</td><td>No</td></tr>
<tr><td>Blast Cannon Shell</td><td>0x56075C12</td><td>No</td></tr>
<tr><td>bld_attachTemplate</td><td>0x5487BA35</td><td>No</td></tr>
<tr><td>bld_debrisdestructTemplate</td><td>0x5F144D41</td><td>No</td></tr>
<tr><td>bld_pieceTemplate050</td><td>0x1DD7B153</td><td>No</td></tr>
<tr><td>bld_pieceTemplate100</td><td>0x153BCAA1</td><td>No</td></tr>
<tr><td>bld_pieceTemplate200</td><td>0xC82F8C6E</td><td>No</td></tr>
<tr><td>bld_sliceTemplate050</td><td>0x1EDD4587</td><td>No</td></tr>
<tr><td>bld_sliceTemplate100</td><td>0x8F5A93AD</td><td>No</td></tr>
<tr><td>bld_sliceTemplate200</td><td>0x4160D2DA</td><td>No</td></tr>
<tr><td>Boat</td><td>0x45847B03</td><td>Yes</td></tr>
<tr><td>Boat Seats (Driver) (VZ)</td><td>0x5984F529</td><td>Yes</td></tr>
<tr><td>BoatList_Amazon_Act1</td><td>0x85405DEC</td><td>Yes</td></tr>
<tr><td>BoatList_Amazon_Act2</td><td>0x1F3D7EC3</td><td>Yes</td></tr>
<tr><td>BoatList_AngelFalls_Ac1</td><td>0xD2C7B595</td><td>Yes</td></tr>
<tr><td>BoatList_Caracas_Act1_A</td><td>0x7495A0A6</td><td>Yes</td></tr>
<tr><td>BoatList_Caracas_Act1_B</td><td>0xF69D2911</td><td>Yes</td></tr>
<tr><td>BoatList_Caracas_Act1_C</td><td>0xFC9AF3EC</td><td>Yes</td></tr>
<tr><td>BoatList_Caracas_Act2_ALL</td><td>0xEA2C5BC5</td><td>Yes</td></tr>
<tr><td>BoatList_Caracas_Act2_CHI</td><td>0x4D76D8E2</td><td>Yes</td></tr>
<tr><td>BoatList_Caracas_Act3_ALL</td><td>0xC7957078</td><td>Yes</td></tr>
<tr><td>BoatList_Caracas_Act3_CHI</td><td>0x4E288B0F</td><td>Yes</td></tr>
<tr><td>BoatList_Cumana_Act1_A</td><td>0xA109E753</td><td>Yes</td></tr>
<tr><td>BoatList_Cumana_Act1_B</td><td>0xC70C61BC</td><td>Yes</td></tr>
<tr><td>BoatList_Cumana_Act1_C</td><td>0x410F6061</td><td>Yes</td></tr>
<tr><td>BoatList_Cumana_Act2_CHI</td><td>0x8C249C77</td><td>Yes</td></tr>
<tr><td>BoatList_Jungle_Act1</td><td>0xCD93B7A1</td><td>Yes</td></tr>
<tr><td>BoatList_Jungle_Act2</td><td>0x4B8C2F36</td><td>Yes</td></tr>
<tr><td>BoatList_Mar_City_Act1_A</td><td>0x53020772</td><td>Yes</td></tr>
<tr><td>BoatList_Mar_City_Act1_B</td><td>0xD5098FDD</td><td>Yes</td></tr>
<tr><td>BoatList_Mar_City_Act1_C</td><td>0xEB0773E8</td><td>Yes</td></tr>
<tr><td>BoatList_Mar_City_Act1_D</td><td>0xECFAAB1B</td><td>Yes</td></tr>
<tr><td>BoatList_Mar_City_Act2_A</td><td>0x9E0D2FC1</td><td>Yes</td></tr>
<tr><td>BoatList_Mar_City_Act3_A</td><td>0x123F28B4</td><td>Yes</td></tr>
<tr><td>BoatList_Merida_Act1</td><td>0x8D7F0FF0</td><td>Yes</td></tr>
<tr><td>BoatList_Merida_Act2</td><td>0x777CAEB7</td><td>Yes</td></tr>
<tr><td>BoatList_OC_Depot</td><td>0xE4E9AEDB</td><td>Yes</td></tr>
<tr><td>BoatList_OC_Depot_Act1</td><td>0xC0692A6B</td><td>Yes</td></tr>
<tr><td>BoatList_PirateHQ_Cutter</td><td>0x5BCF12D6</td><td>Yes</td></tr>
<tr><td>BoatList_PirateHQ_Jetski</td><td>0x43943B5F</td><td>Yes</td></tr>
<tr><td>BoatList_PirateHQ_Jetski_Driver</td><td>0x43DE8FEC</td><td>Yes</td></tr>
<tr><td>BoatList_PirateIsles_Act1_A</td><td>0x098196E7</td><td>Yes</td></tr>
<tr><td>BoatList_PmcHQ_Act1</td><td>0xF41256D3</td><td>Yes</td></tr>
<tr><td>BoatList_Simple</td><td>0x37E6A534</td><td>Yes</td></tr>
<tr><td>BoatList_VZCon001</td><td>0x8EC130AB</td><td>Yes</td></tr>
<tr><td>Bomb</td><td>0xA9FD3561</td><td>No</td></tr>
<tr><td>Box</td><td>0xA0787FC8</td><td>No</td></tr>
<tr><td>Box Trailer</td><td>0x160D3EBD</td><td>No</td></tr>
<tr><td>Briefing Interior</td><td>0x0B054E4B</td><td>No</td></tr>
<tr><td>Buggy</td><td>0x6AFF0875</td><td>Yes</td></tr>
<tr><td>Buggy (Guerilla driver)</td><td>0xAF3C2665</td><td>Yes</td></tr>
<tr><td>Buggy (Hellfire)</td><td>0x8E0908F1</td><td>Yes</td></tr>
<tr><td>Buggy (PR)</td><td>0x86835E18</td><td>Yes</td></tr>
<tr><td>Buggy_Driver</td><td>0x1FC07476</td><td>Yes</td></tr>
<tr><td>BuggyPR_Driver</td><td>0x42AE049C</td><td>Yes</td></tr>
<tr><td>Building Slice Collapse</td><td>0x0007CCC4</td><td>No</td></tr>
<tr><td>Building Spawner</td><td>0x7C3107D5</td><td>No</td></tr>
<tr><td>Bullpup Rifle</td><td>0x3F93CEF7</td><td>No</td></tr>
<tr><td>Bullpup Rifle (Window Spawner)</td><td>0x4B27AF68</td><td>No</td></tr>
<tr><td>Bullpup Rifle Bullet</td><td>0xFA695BE9</td><td>No</td></tr>
<tr><td>Bunker Buster Projectile</td><td>0x74C64496</td><td>No</td></tr>
<tr><td>C4</td><td>0xCAF30DA8</td><td>No</td></tr>
<tr><td>C4 Detonator</td><td>0xA5F4BC6C</td><td>No</td></tr>
<tr><td>C4 Projectile</td><td>0xFC6B9E2D</td><td>No</td></tr>
<tr><td>Car</td><td>0xCE27C791</td><td>No</td></tr>
<tr><td>Carbine</td><td>0xDF10D765</td><td>No</td></tr>
<tr><td>Carbine (Window Spawner)</td><td>0x4EA10F02</td><td>No</td></tr>
<tr><td>Carbine Bullet</td><td>0x73697F5F</td><td>No</td></tr>
<tr><td>Cargo Ship</td><td>0x4CF6278F</td><td>Yes</td></tr>
<tr><td>Carmona</td><td>0xED346E8A</td><td>No</td></tr>
<tr><td>Carpet Bomb Projectile</td><td>0x38F6D4D5</td><td>No</td></tr>
<tr><td>Cart Worker (female)</td><td>0x80CDF678</td><td>No</td></tr>
<tr><td>Cart Worker (male)</td><td>0x20A0AAA9</td><td>No</td></tr>
<tr><td>Cash (Case)</td><td>0xF6FA1AB5</td><td>No</td></tr>
<tr><td>Cash (Large)</td><td>0xE8E9D8CA</td><td>No</td></tr>
<tr><td>Cash (Medium)</td><td>0x1A7DE40E</td><td>No</td></tr>
<tr><td>Cash (Small)</td><td>0xFAA7FE7E</td><td>No</td></tr>
<tr><td>Cessna</td><td>0x3C411D08</td><td>No</td></tr>
<tr><td>CH Defender (AA)</td><td>0xDF26D7BC</td><td>No</td></tr>
<tr><td>CH Defender (AT)</td><td>0xD94D6FEF</td><td>No</td></tr>
<tr><td>CH Defender (AT) (Window Spawner)</td><td>0x05D217B0</td><td>No</td></tr>
<tr><td>CH Defender (MG)</td><td>0xEA3ECB5E</td><td>No</td></tr>
<tr><td>CH Defender (Rifle)</td><td>0xAF46FE02</td><td>No</td></tr>
<tr><td>CH Defender (Sniper)</td><td>0x1BA70DC1</td><td>No</td></tr>
<tr><td>Chain Cannon Bullet</td><td>0xA26ABEA5</td><td>No</td></tr>
<tr><td>Chain Cannon Bullet (CH)</td><td>0x34067D75</td><td>No</td></tr>
<tr><td>Chain Cannon Bullet (GR)</td><td>0x50072627</td><td>No</td></tr>
<tr><td>chairs</td><td>0x214F3303</td><td>No</td></tr>
<tr><td>CheapDebrisTemplate</td><td>0x31E69F35</td><td>No</td></tr>
<tr><td>Cheat RPG</td><td>0x49401D0B</td><td>No</td></tr>
<tr><td>Cheat RPG Rocket</td><td>0xBBF165B1</td><td>No</td></tr>
<tr><td>ChiDbSpawner</td><td>0x6E0EED01</td><td>No</td></tr>
<tr><td>ChiDbSpawner (Squad Full AT)</td><td>0x54D605F4</td><td>No</td></tr>
<tr><td>ChiDbSpawner (Squad Half AT)</td><td>0xBB7FE84C</td><td>No</td></tr>
<tr><td>ChiDbSpawner (Squad Quarter AT)</td><td>0x17419369</td><td>No</td></tr>
<tr><td>ChiDbSpawner (Squad)</td><td>0x2C95035A</td><td>No</td></tr>
<tr><td>ChiHq_Interior</td><td>0xA9BF983F</td><td>No</td></tr>
<tr><td>china</td><td>0x41359CCE</td><td>No</td></tr>
<tr><td>ChinaSkirmishTest</td><td>0xE54C502A</td><td>No</td></tr>
<tr><td>Chinese Airborne</td><td>0x34DA0AF0</td><td>No</td></tr>
<tr><td>Chinese Airborne (AT)</td><td>0x41C0EAE0</td><td>No</td></tr>
<tr><td>Chinese Airborne (Light MG)</td><td>0x8F248EDD</td><td>No</td></tr>
<tr><td>Chinese Boss</td><td>0x03393679</td><td>No</td></tr>
<tr><td>Chinese Boss (Invincible)</td><td>0x70F1D3BB</td><td>No</td></tr>
<tr><td>Chinese Destroyer</td><td>0x02DFA76D</td><td>Yes</td></tr>
<tr><td>Chinese Destroyer (FULL)</td><td>0x4A5512FF</td><td>Yes</td></tr>
<tr><td>Chinese Destroyer (Jammer)</td><td>0x0177153A</td><td>Yes</td></tr>
<tr><td>Chinese Elite Soldier</td><td>0xA11F6971</td><td>No</td></tr>
<tr><td>Chinese Heavy (AA)</td><td>0x8B12853E</td><td>No</td></tr>
<tr><td>Chinese Heavy (Light MG)</td><td>0xA7CE8B80</td><td>No</td></tr>
<tr><td>Chinese Heavy (RPG)</td><td>0xDBACFF2D</td><td>No</td></tr>
<tr><td>Chinese Medic</td><td>0x2CCA7D48</td><td>No</td></tr>
<tr><td>Chinese Officer</td><td>0x59ED821C</td><td>No</td></tr>
<tr><td>Chinese Paratrooper</td><td>0x056D6979</td><td>No</td></tr>
<tr><td>Chinese Pilot (God)</td><td>0x7A1028CB</td><td>No</td></tr>
<tr><td>Chinese Pilot A</td><td>0x579DD039</td><td>No</td></tr>
<tr><td>Chinese Pilot B</td><td>0xF5967A2E</td><td>No</td></tr>
<tr><td>Chinese Prisoner</td><td>0xCB0A2146</td><td>No</td></tr>
<tr><td>Chinese Sailor</td><td>0x65C7D21A</td><td>No</td></tr>
<tr><td>Chinese Sailor (AA)</td><td>0x272F8B51</td><td>No</td></tr>
<tr><td>Chinese Sailor (Light MG)</td><td>0x515CFB63</td><td>No</td></tr>
<tr><td>Chinese Sniper</td><td>0x0B0A1B2B</td><td>No</td></tr>
<tr><td>Chinese Soldier</td><td>0x26EC3650</td><td>No</td></tr>
<tr><td>Chinese Starter 01</td><td>0xE515DDBC</td><td>No</td></tr>
<tr><td>Chinese Starter 02</td><td>0xBF136353</td><td>No</td></tr>
<tr><td>Chinese Starter 03</td><td>0xDD1153F6</td><td>No</td></tr>
<tr><td>Chinese Starter 04</td><td>0xE722ACD5</td><td>No</td></tr>
<tr><td>Chinese Starter 05</td><td>0xBD202C20</td><td>No</td></tr>
<tr><td>Chinese Starters</td><td>0x3DB9383E</td><td>No</td></tr>
<tr><td>Chinese Tank Commander</td><td>0x70DA1B50</td><td>Yes</td></tr>
<tr><td>Chinese VIP</td><td>0x38C5CB33</td><td>No</td></tr>
<tr><td>Chinese Worker</td><td>0xF4D53B94</td><td>No</td></tr>
<tr><td>Chinese Worker (Exercise)</td><td>0x38E8BC3F</td><td>No</td></tr>
<tr><td>ChiVehTraffic</td><td>0x82B00835</td><td>No</td></tr>
<tr><td>chong</td><td>0xF856AB5E</td><td>No</td></tr>
<tr><td>chong c1</td><td>0x6101B5F6</td><td>No</td></tr>
<tr><td>chong c2</td><td>0xE3093E61</td><td>No</td></tr>
<tr><td>Chopper</td><td>0x78CF64E6</td><td>Yes</td></tr>
<tr><td>Chopper (Driver)</td><td>0x714FA07D</td><td>Yes</td></tr>
<tr><td>Chopper (Driver) (Civ Motorcycle male)</td><td>0x47F9E30C</td><td>Yes</td></tr>
<tr><td>Chopper_Driver</td><td>0xC532455F</td><td>Yes</td></tr>
<tr><td>chris</td><td>0xD64BB122</td><td>No</td></tr>
<tr><td>ChrisChickensuit</td><td>0xC2398360</td><td>No</td></tr>
<tr><td>chrisupgrade1</td><td>0x4834745B</td><td>No</td></tr>
<tr><td>chrisupgrade2</td><td>0xAE375384</td><td>No</td></tr>
<tr><td>chrisupgrade3</td><td>0xC839BB09</td><td>No</td></tr>
<tr><td>ChrisV2</td><td>0xAA1A3B0A</td><td>No</td></tr>
<tr><td>ChrisV3</td><td>0xCC1CAF27</td><td>No</td></tr>
<tr><td>Chunk</td><td>0x950E7438</td><td>No</td></tr>
<tr><td>Chunk Set</td><td>0xC06C5F3C</td><td>No</td></tr>
<tr><td>Chunk Set (Tree Branches)</td><td>0xC2FA6CE5</td><td>No</td></tr>
<tr><td>Chunk_aa</td><td>0x21EDB019</td><td>No</td></tr>
<tr><td>Chunk_ab</td><td>0xBFE65A0E</td><td>No</td></tr>
<tr><td>Chunk_ac</td><td>0xA1E8696B</td><td>No</td></tr>
<tr><td>Chunk_ad</td><td>0x9FF53238</td><td>No</td></tr>
<tr><td>Chunk_ae</td><td>0xC9F7B2ED</td><td>No</td></tr>
<tr><td>Chunk_af</td><td>0x47F02A82</td><td>No</td></tr>
<tr><td>Chunk_ag</td><td>0x29F239DF</td><td>No</td></tr>
<tr><td>Chunk_ah</td><td>0x27FF02AC</td><td>No</td></tr>
<tr><td>Chunk_ai</td><td>0x220137D1</td><td>No</td></tr>
<tr><td>Chunk_aj</td><td>0x9FF9AF66</td><td>No</td></tr>
<tr><td>Chunk_ak</td><td>0xC1FC2383</td><td>No</td></tr>
<tr><td>Chunk_al</td><td>0xC008EC50</td><td>No</td></tr>
<tr><td>Chunk_am</td><td>0xAA0B0845</td><td>No</td></tr>
<tr><td>Chunk_asphalt_small02</td><td>0x7A81F6E2</td><td>No</td></tr>
<tr><td>Chunk_asphalt_small03</td><td>0xDC84CFBF</td><td>No</td></tr>
<tr><td>Chunk_asphalt_small04</td><td>0x7A7D79B4</td><td>No</td></tr>
<tr><td>Chunk_Branch01</td><td>0xF8EBFE62</td><td>No</td></tr>
<tr><td>Chunk_Brick_Small01</td><td>0xBF25A4A7</td><td>No</td></tr>
<tr><td>Chunk_Brick_Small02</td><td>0x15286AA0</td><td>No</td></tr>
<tr><td>Chunk_Brick_Small03</td><td>0x3F2AEB55</td><td>No</td></tr>
<tr><td>Chunk_Brick_Small04</td><td>0x35199276</td><td>No</td></tr>
<tr><td>Chunk_Concrete_Large01</td><td>0x8B55BA93</td><td>No</td></tr>
<tr><td>Chunk_Concrete_Large02</td><td>0xB15834FC</td><td>No</td></tr>
<tr><td>Chunk_Concrete_Small01</td><td>0x02E016BB</td><td>No</td></tr>
<tr><td>Chunk_Concrete_Small02</td><td>0xE8E22C64</td><td>No</td></tr>
<tr><td>Chunk_Concrete_Small03</td><td>0x02E493E9</td><td>No</td></tr>
<tr><td>Chunk_Concrete_Small04</td><td>0x68E77312</td><td>No</td></tr>
<tr><td>Chunk_Metal_LargeA</td><td>0x4C8224B9</td><td>No</td></tr>
<tr><td>Chunk_Metal_LargeB</td><td>0xEA7ACEAE</td><td>No</td></tr>
<tr><td>Chunk_Metal_LargeC</td><td>0x4C7DA78B</td><td>No</td></tr>
<tr><td>Chunk_Metal_LargeD</td><td>0xCA89A6D8</td><td>No</td></tr>
<tr><td>Chunk_Metal_LongA</td><td>0x17D9F02E</td><td>No</td></tr>
<tr><td>Chunk_Metal_PipeA</td><td>0x16468BCC</td><td>No</td></tr>
<tr><td>Chunk_Metal_smallA</td><td>0x7EE8355D</td><td>No</td></tr>
<tr><td>Chunk_Metal_SmallB</td><td>0xFCE0ACF2</td><td>No</td></tr>
<tr><td>Chunk_Metal_SmallC</td><td>0x1EE3210F</td><td>No</td></tr>
<tr><td>Chunk_rpg</td><td>0x3341C41C</td><td>No</td></tr>
<tr><td>Chunk_Tile_Small01</td><td>0xBC16FBAE</td><td>No</td></tr>
<tr><td>Chunk_Tile_Small02</td><td>0x1E1E51B9</td><td>No</td></tr>
<tr><td>Chunk_Tree_Branch</td><td>0x1EE3478A</td><td>No</td></tr>
<tr><td>chunk_wood_beam</td><td>0xD84D272A</td><td>No</td></tr>
<tr><td>chunk_wood_panel</td><td>0xC478DD9B</td><td>No</td></tr>
<tr><td>chunk_wood_small01</td><td>0x6CA9C995</td><td>No</td></tr>
<tr><td>chunk_wood_small02</td><td>0xCAA20ECA</td><td>No</td></tr>
<tr><td>ChunkFlame</td><td>0x2B687AE5</td><td>No</td></tr>
<tr><td>ChunkFlamePersistent</td><td>0xF0325066</td><td>No</td></tr>
<tr><td>chunks_debriseffect</td><td>0xA6175DE4</td><td>No</td></tr>
<tr><td>chunks_rpg</td><td>0x673929DB</td><td>No</td></tr>
<tr><td>ChunkSmoke</td><td>0x4B366E23</td><td>No</td></tr>
<tr><td>Cigarette (base)</td><td>0x5809751D</td><td>No</td></tr>
<tr><td>Cigarette_Driver</td><td>0x101FD2E0</td><td>No</td></tr>
<tr><td>CIV</td><td>0xDCC8B14D</td><td>No</td></tr>
<tr><td>Civ Beach A (Female)</td><td>0x42183C02</td><td>No</td></tr>
<tr><td>Civ Beach B (Female)</td><td>0x17DB1883</td><td>No</td></tr>
<tr><td>Civ Beach C (Female)</td><td>0x9CF92F0C</td><td>No</td></tr>
<tr><td>Civ Beach D (Female)</td><td>0x3C2BB74D</td><td>No</td></tr>
<tr><td>Civ Business (Female)</td><td>0xEAF68A6A</td><td>No</td></tr>
<tr><td>Civ Business (male)</td><td>0xD581782F</td><td>No</td></tr>
<tr><td>Civ Business B (male)</td><td>0x93B36E7D</td><td>No</td></tr>
<tr><td>Civ Casual (female)</td><td>0x2A5C35C9</td><td>No</td></tr>
<tr><td>Civ Casual (male)</td><td>0xA22617AC</td><td>No</td></tr>
<tr><td>Civ Casual with Hat (female)</td><td>0xE1785BBC</td><td>No</td></tr>
<tr><td>Civ Cowboy (male)</td><td>0xAA5175EE</td><td>No</td></tr>
<tr><td>Civ Doctor (female)</td><td>0x6837129F</td><td>No</td></tr>
<tr><td>Civ Doctor 2 (female)</td><td>0x6B7E69E5</td><td>No</td></tr>
<tr><td>Civ Fueltrailer</td><td>0x73999888</td><td>No</td></tr>
<tr><td>Civ Fueltrailer_PmcCon018</td><td>0x022F55BA</td><td>No</td></tr>
<tr><td>Civ Industrial (female)</td><td>0xDFA85263</td><td>No</td></tr>
<tr><td>Civ Industrial (male)</td><td>0x9B1A9B92</td><td>No</td></tr>
<tr><td>Civ Journalist A (male)</td><td>0x6477AB1B</td><td>No</td></tr>
<tr><td>Civ Journalist B (male)</td><td>0x48F58526</td><td>No</td></tr>
<tr><td>Civ Journalist C (female)</td><td>0x9B77D2F0</td><td>No</td></tr>
<tr><td>Civ Journalist D (female)</td><td>0xC1A99029</td><td>No</td></tr>
<tr><td>Civ Motorcycle (male)</td><td>0x63825598</td><td>Yes</td></tr>
<tr><td>Civ Poor (female)</td><td>0x6D8CBE4C</td><td>No</td></tr>
<tr><td>Civ Poor (male)</td><td>0x26E9D55D</td><td>No</td></tr>
<tr><td>Civ Rich (female)</td><td>0x4A506AEA</td><td>No</td></tr>
<tr><td>Civ Rich (male)</td><td>0x996B44AF</td><td>No</td></tr>
<tr><td>Civ Taxi Driver (male)</td><td>0x7DCB768D</td><td>No</td></tr>
<tr><td>Civilian</td><td>0xD2601C86</td><td>No</td></tr>
<tr><td>CivilianList</td><td>0x059AF94E</td><td>No</td></tr>
<tr><td>ClownCar</td><td>0x04770EA2</td><td>No</td></tr>
<tr><td>Cluster Bomb Projectile</td><td>0xBEC3E888</td><td>No</td></tr>
<tr><td>Cluster Bomblet Projectile</td><td>0xE9EF1357</td><td>No</td></tr>
<tr><td>Coanda</td><td>0x937D0BCB</td><td>Yes</td></tr>
<tr><td>Coanda Attack</td><td>0x8FA0A591</td><td>Yes</td></tr>
<tr><td>Coanda Attack (Driver)</td><td>0xA156846C</td><td>Yes</td></tr>
<tr><td>Coanda Attack (Ewan)</td><td>0xFDBB6BA9</td><td>Yes</td></tr>
<tr><td>Coanda Attack (Full)</td><td>0x7313CA1B</td><td>Yes</td></tr>
<tr><td>Coanda Gunship</td><td>0xB321082B</td><td>Yes</td></tr>
<tr><td>Coanda Gunship (Delivery)</td><td>0xE998E2A4</td><td>Yes</td></tr>
<tr><td>Coanda Gunship (Driver)</td><td>0x112B50C6</td><td>Yes</td></tr>
<tr><td>Coanda Gunship (Ewan)</td><td>0x84E5AF7F</td><td>Yes</td></tr>
<tr><td>Coanda Gunship (Full)</td><td>0xF86F549D</td><td>Yes</td></tr>
<tr><td>Coanda Superiority</td><td>0xECD7D340</td><td>Yes</td></tr>
<tr><td>Coanda Superiority (Driver)</td><td>0x001783DF</td><td>Yes</td></tr>
<tr><td>Coanda Superiority (Ewan)</td><td>0x011C5856</td><td>Yes</td></tr>
<tr><td>Coanda Superiority (Full)</td><td>0xF86A3C54</td><td>Yes</td></tr>
<tr><td>Coanda Transport</td><td>0x4925098C</td><td>Yes</td></tr>
<tr><td>Coanda Transport (Driver)</td><td>0x44CF1B8B</td><td>Yes</td></tr>
<tr><td>Coanda Transport (Ewan)</td><td>0x8642C152</td><td>Yes</td></tr>
<tr><td>Coanda Transport (Extraction)</td><td>0xE063D388</td><td>Yes</td></tr>
<tr><td>Coanda Transport (Full)</td><td>0x4DF1FD48</td><td>Yes</td></tr>
<tr><td>Coanda Transport (Pursuit)</td><td>0x46F96893</td><td>Yes</td></tr>
<tr><td>Coilgun</td><td>0x25A6B2FE</td><td>No</td></tr>
<tr><td>Coilgun Bullet</td><td>0xAABA7EEE</td><td>No</td></tr>
<tr><td>coinoperated</td><td>0x6C519C7A</td><td>No</td></tr>
<tr><td>Combat Rifle</td><td>0x5E3DE643</td><td>No</td></tr>
<tr><td>Combat Rifle (Window Spawner)</td><td>0xDC4B09CC</td><td>No</td></tr>
<tr><td>Combat Rifle Bullet</td><td>0xFBD57875</td><td>No</td></tr>
<tr><td>commercial_raod5</td><td>0xD2216BAD</td><td>No</td></tr>
<tr><td>commercial_raod5t</td><td>0x69F09A5B</td><td>No</td></tr>
<tr><td>commercial_road10cross.xsi</td><td>0xA2D106BF</td><td>No</td></tr>
<tr><td>commercial_road10cross5.xsi</td><td>0x869EAA1C</td><td>No</td></tr>
<tr><td>commercial_road5</td><td>0xBE7BE56D</td><td>No</td></tr>
<tr><td>commercial_road5cross</td><td>0x1A98F393</td><td>No</td></tr>
<tr><td>commercial_road5L</td><td>0xBB5C6FC3</td><td>No</td></tr>
<tr><td>commercial_road5t10</td><td>0x011624D8</td><td>No</td></tr>
<tr><td>Cougar</td><td>0x7690A482</td><td>No</td></tr>
<tr><td>Cougar (Driver) (Civ Business B Male)</td><td>0x4D32D5FB</td><td>No</td></tr>
<tr><td>Cover</td><td>0xBABE579E</td><td>No</td></tr>
<tr><td>Cover (Barrel)</td><td>0xBACBBC6F</td><td>No</td></tr>
<tr><td>Cover (Barricade)</td><td>0xEAEC1AF8</td><td>No</td></tr>
<tr><td>Cover (Box)</td><td>0xED03DE66</td><td>No</td></tr>
<tr><td>Cover (Building Custom)</td><td>0x35888DF4</td><td>No</td></tr>
<tr><td>Cover (Building Poor)</td><td>0x8E85833F</td><td>No</td></tr>
<tr><td>Cover (Building)</td><td>0x043CB553</td><td>No</td></tr>
<tr><td>Cover (Car)</td><td>0x8689C3E5</td><td>No</td></tr>
<tr><td>Cover (Container)</td><td>0xE7FF5728</td><td>No</td></tr>
<tr><td>Cover (Custom)</td><td>0x7C9DFFAC</td><td>No</td></tr>
<tr><td>Cover (Fence)</td><td>0x562500A6</td><td>No</td></tr>
<tr><td>Cover (Junk)</td><td>0xB521C7B9</td><td>No</td></tr>
<tr><td>Cover (Placeable Popup)</td><td>0xD3A761B2</td><td>No</td></tr>
<tr><td>Cover (Placeable Sidestep)</td><td>0x5639C55F</td><td>No</td></tr>
<tr><td>Cover (Plant)</td><td>0xE3E474B2</td><td>No</td></tr>
<tr><td>Cover (Rock)</td><td>0x5FA0B806</td><td>No</td></tr>
<tr><td>Cover (Sandbag Corner)</td><td>0x60B2EB06</td><td>No</td></tr>
<tr><td>Cover (Sandbag Custom)</td><td>0xF167ED60</td><td>No</td></tr>
<tr><td>Cover (Sandbag End)</td><td>0x8AA9A276</td><td>No</td></tr>
<tr><td>Cover (Sandbag Straight)</td><td>0x7E2C94A9</td><td>No</td></tr>
<tr><td>Cover (Sandbag)</td><td>0xE7BD3547</td><td>No</td></tr>
<tr><td>Cover (Statue)</td><td>0x65B98F8B</td><td>No</td></tr>
<tr><td>Cover (Tree Medium)</td><td>0x51AC7CF8</td><td>No</td></tr>
<tr><td>Cover (Tree Small)</td><td>0xA2657DB0</td><td>No</td></tr>
<tr><td>Cover (Tree)</td><td>0x56073DB3</td><td>No</td></tr>
<tr><td>Cover (Vehicle)</td><td>0x0A969F1B</td><td>No</td></tr>
<tr><td>Cover (Wall)</td><td>0x3E05A4CF</td><td>No</td></tr>
<tr><td>Covert Pistol</td><td>0x175AB11B</td><td>No</td></tr>
<tr><td>Covert Pistol Bullet</td><td>0x5A8F273D</td><td>No</td></tr>
<tr><td>Covert SMG</td><td>0x3FDF8065</td><td>No</td></tr>
<tr><td>Covert SMG Bullet</td><td>0xBFC5325F</td><td>No</td></tr>
<tr><td>Cruise Missile Projectile</td><td>0x39F9955D</td><td>No</td></tr>
<tr><td>CrushingDebrisLargeTemplate</td><td>0x1E1DD33E</td><td>No</td></tr>
<tr><td>CrushingDebrisMedTemplate</td><td>0x099867E9</td><td>No</td></tr>
<tr><td>CrushingDebrisSmallTemplate</td><td>0x6986DB9A</td><td>No</td></tr>
<tr><td>CRX</td><td>0xB67908C6</td><td>No</td></tr>
<tr><td>CRX (Driver)</td><td>0x0B67B3DD</td><td>No</td></tr>
<tr><td>CRX (Driver) (Civ Business B)</td><td>0x60531464</td><td>No</td></tr>
<tr><td>CRX (racing)</td><td>0x03F95C1D</td><td>No</td></tr>
<tr><td>CRX (racing) (Driver)</td><td>0x5C5AD328</td><td>No</td></tr>
<tr><td>CRX (racing) (Driver) (Civ Motorcycle male)</td><td>0x54BAD151</td><td>Yes</td></tr>
<tr><td>CRX_Driver</td><td>0x1C5AD3BF</td><td>No</td></tr>
<tr><td>CRX_RUIN</td><td>0xF4982A1F</td><td>No</td></tr>
<tr><td>CRXRacing_Driver</td><td>0x44256B69</td><td>No</td></tr>
<tr><td>Cutter (base)</td><td>0xD156A6EC</td><td>No</td></tr>
<tr><td>Cutter (PR)</td><td>0x6DA31E8B</td><td>No</td></tr>
<tr><td>Cutter (PR) (Driver)</td><td>0xAEB97C26</td><td>No</td></tr>
<tr><td>Cutter (PR) (Full)</td><td>0xDCAB53FD</td><td>No</td></tr>
<tr><td>Cutter (PR)_Ruined</td><td>0x6303B0EF</td><td>No</td></tr>
<tr><td>Cutter_Driver</td><td>0x83BD7A69</td><td>No</td></tr>
<tr><td>Daisy Cutter Projectile</td><td>0x251BF46B</td><td>No</td></tr>
<tr><td>Dance Radio</td><td>0x52F25E7F</td><td>No</td></tr>
<tr><td>Dance Radio AL</td><td>0xDE9309A6</td><td>No</td></tr>
<tr><td>Dance Radio AL Contact</td><td>0xA6F7A1CA</td><td>No</td></tr>
<tr><td>Dance Radio CH</td><td>0x5FA490B4</td><td>No</td></tr>
<tr><td>Dance Radio CH Contact</td><td>0xE621A4E0</td><td>No</td></tr>
<tr><td>Dance Radio Eva</td><td>0x9A6AAB11</td><td>No</td></tr>
<tr><td>Dance Radio GR</td><td>0xAD7D835A</td><td>No</td></tr>
<tr><td>Dance Radio GR Contact</td><td>0x5318FDFE</td><td>No</td></tr>
<tr><td>Dance Radio OC</td><td>0xA8C0D2DF</td><td>No</td></tr>
<tr><td>Dance Radio OC Contact</td><td>0xBFA48753</td><td>No</td></tr>
<tr><td>Dance Radio PR Contact</td><td>0xB6E03723</td><td>No</td></tr>
<tr><td>DangerousBuildingSimpleSpawners</td><td>0xBCD05D22</td><td>No</td></tr>
<tr><td>DangerousBuildingTest1</td><td>0x64FA3A44</td><td>No</td></tr>
<tr><td>DangerousBuildingVZBarracks</td><td>0xDE512D7A</td><td>No</td></tr>
<tr><td>DangerousBuildingVZBarracks_HalfSpawn</td><td>0xB7E95A1F</td><td>No</td></tr>
<tr><td>DangerousBuildingVZBarracks_HalfSpawn_Squad</td><td>0x211E5D68</td><td>No</td></tr>
<tr><td>DangerousBuildingVZBarrackstent_RPG</td><td>0x85B8A191</td><td>No</td></tr>
<tr><td>DangerousBuildingVZBunker</td><td>0x21F8F2D4</td><td>No</td></tr>
<tr><td>DangerousBuildingVZTower</td><td>0x57C6E44E</td><td>No</td></tr>
<tr><td>DB VZ RPG + Rifle</td><td>0xD3AA8AE5</td><td>No</td></tr>
<tr><td>DB_SquadTest</td><td>0xEA87BA74</td><td>No</td></tr>
<tr><td>debris m151 wheel</td><td>0x72227C3D</td><td>Yes</td></tr>
<tr><td>debris m35 wheel</td><td>0xC1E768D8</td><td>Yes</td></tr>
<tr><td>debris_barreldrum</td><td>0xF2B6EB83</td><td>No</td></tr>
<tr><td>debris_metal_chainlinkfence</td><td>0xA34CF23D</td><td>No</td></tr>
<tr><td>debris_metal_huge</td><td>0xE347179E</td><td>No</td></tr>
<tr><td>debris_metal_lrg</td><td>0xB9ED0DA8</td><td>No</td></tr>
<tr><td>debris_metal_med</td><td>0xD3413D47</td><td>No</td></tr>
<tr><td>debris_metal_pipes</td><td>0xE695DCDE</td><td>No</td></tr>
<tr><td>debris_metal_sml</td><td>0x844B57BD</td><td>No</td></tr>
<tr><td>debris_metalpole_lrg</td><td>0x078F8C6A</td><td>No</td></tr>
<tr><td>debris_oilrig 0x8000a6f6</td><td>0x360397F2</td><td>No</td></tr>
<tr><td>debris_rubber</td><td>0x66E977B5</td><td>No</td></tr>
<tr><td>debris_sheetmetal_lrg</td><td>0xFBCCE465</td><td>No</td></tr>
<tr><td>debris_sheetmetal_sml</td><td>0x03CA0258</td><td>No</td></tr>
<tr><td>debris_stone_huge</td><td>0x3EBBF6D4</td><td>No</td></tr>
<tr><td>debris_stone_lrg</td><td>0x944C7D36</td><td>No</td></tr>
<tr><td>debris_stone_med</td><td>0xC471EE9D</td><td>No</td></tr>
<tr><td>debris_stone_sml</td><td>0x88F18137</td><td>No</td></tr>
<tr><td>debris_veh_civ_ruin</td><td>0xE53EA0D0</td><td>Yes</td></tr>
<tr><td>debris_wood_sml</td><td>0xF96233D1</td><td>No</td></tr>
<tr><td>DebrisDestructTemplate</td><td>0x6729C128</td><td>No</td></tr>
<tr><td>DebrisTemplate</td><td>0x31EB7EA2</td><td>No</td></tr>
<tr><td>decals</td><td>0x306169B7</td><td>No</td></tr>
<tr><td>DefaultTrafficZone</td><td>0xEDD263D1</td><td>No</td></tr>
<tr><td>Destroyer_Driver</td><td>0x154B2E39</td><td>Yes</td></tr>
<tr><td>Detach</td><td>0x6A75ED48</td><td>No</td></tr>
<tr><td>Devastator</td><td>0x4739D812</td><td>No</td></tr>
<tr><td>Devastator_Driver</td><td>0xAAA9E373</td><td>No</td></tr>
<tr><td>Dinghy</td><td>0x6A77E320</td><td>Yes</td></tr>
<tr><td>Dinghy (Driver)</td><td>0x23051FBF</td><td>Yes</td></tr>
<tr><td>Dinghy (Driver) (Civ Poor female)</td><td>0x7EA81174</td><td>Yes</td></tr>
<tr><td>Dinghy (Driver) (Civ Poor male)</td><td>0x6B22C245</td><td>Yes</td></tr>
<tr><td>Dinghy_Driver</td><td>0x3AB2899D</td><td>Yes</td></tr>
<tr><td>Disguise Scale (Armored)</td><td>0xC0FE9DE9</td><td>No</td></tr>
<tr><td>Disguise Scale (Boat)</td><td>0x9219DBA9</td><td>Yes</td></tr>
<tr><td>Disguise Scale (Car)</td><td>0xBE1726D1</td><td>No</td></tr>
<tr><td>Disguise Scale (Default)</td><td>0xF091F576</td><td>No</td></tr>
<tr><td>Disguise Scale (Helicopter)</td><td>0xD88C74B2</td><td>Yes</td></tr>
<tr><td>Disguise Scale (Motorcycle)</td><td>0xCD6D84EE</td><td>Yes</td></tr>
<tr><td>Disguise Scale (Open Boat)</td><td>0x2A685D91</td><td>Yes</td></tr>
<tr><td>Disguise Scale (Open Car)</td><td>0x4F1F14D9</td><td>No</td></tr>
<tr><td>DLC Green Goblin Bomb Projectile</td><td>0xF65BD4CB</td><td>No</td></tr>
<tr><td>DLC Green Goblin Bomblet Projectile</td><td>0xE05C94CE</td><td>No</td></tr>
<tr><td>DLC_50cal</td><td>0xFA6E3CA4</td><td>No</td></tr>
<tr><td>DLC_global_particle_3d</td><td>0x2AD585BB</td><td>No</td></tr>
<tr><td>DLC_global_particle_explosion_huge</td><td>0x647D2F0B</td><td>No</td></tr>
<tr><td>DLC_Green_Goblin_Explosion</td><td>0x42446B02</td><td>No</td></tr>
<tr><td>DLC_hero</td><td>0xEDB9F3A3</td><td>No</td></tr>
<tr><td>DLC_Light_explosion_huge</td><td>0x862DC7E9</td><td>No</td></tr>
<tr><td>DLC_M1A1</td><td>0x28F72787</td><td>No</td></tr>
<tr><td>DLC_npc_mercenaryelite</td><td>0x8128012A</td><td>No</td></tr>
<tr><td>DO NOT USE  HondaCRX Test</td><td>0x30F53A4D</td><td>No</td></tr>
<tr><td>DO NOT USE (OLD police cruiser)</td><td>0xE2415973</td><td>No</td></tr>
<tr><td>DO NOT USE Weapon Test DSHK</td><td>0x8EC416AC</td><td>No</td></tr>
<tr><td>DO NOT USE Weapon Test M2</td><td>0xB0AC94E5</td><td>No</td></tr>
<tr><td>DO NOT USE Weapon Test M60</td><td>0x3349F36B</td><td>No</td></tr>
<tr><td>DO NOT USE Weapon Test MK19</td><td>0xC1D0275E</td><td>No</td></tr>
<tr><td>DO NOT USE Weapon Test TOW</td><td>0xCEEDCE4E</td><td>No</td></tr>
<tr><td>DONOTUSE_oc_veh_semi_fueltrailer</td><td>0xB38BF710</td><td>Yes</td></tr>
<tr><td>DropPoint (AL)</td><td>0x9FC35DA0</td><td>No</td></tr>
<tr><td>DropPoint (CH)</td><td>0x0388C38E</td><td>No</td></tr>
<tr><td>DropPoint (GR)</td><td>0x973E1418</td><td>No</td></tr>
<tr><td>DropPoint (OC)</td><td>0xEBD90A17</td><td>No</td></tr>
<tr><td>DropPoint (PR)</td><td>0x32804CB7</td><td>No</td></tr>
<tr><td>DropPoint (VZ)</td><td>0x839D3BC9</td><td>No</td></tr>
<tr><td>DSV Scout Vehicle</td><td>0x39870E26</td><td>No</td></tr>
<tr><td>Dumb Rocket</td><td>0xE1B587D7</td><td>No</td></tr>
<tr><td>Dumb Rocket (CH)</td><td>0x69C5003F</td><td>No</td></tr>
<tr><td>E3 Missile Stage 1</td><td>0xEC4DB016</td><td>No</td></tr>
<tr><td>E3 Missile Stage 2</td><td>0x6E553881</td><td>No</td></tr>
<tr><td>E3_OC_Littlebirds</td><td>0xB5A69C43</td><td>No</td></tr>
<tr><td>e3demo</td><td>0xDF1B9620</td><td>No</td></tr>
<tr><td>E3MeridaMedTraffic</td><td>0xDF329FB0</td><td>No</td></tr>
<tr><td>Effect_Impact</td><td>0x60D1B0BB</td><td>No</td></tr>
<tr><td>Effect_ParticleSmoke</td><td>0x3882A7CA</td><td>No</td></tr>
<tr><td>Effects</td><td>0xC8EA585D</td><td>No</td></tr>
<tr><td>El Grande</td><td>0x53BAB15D</td><td>No</td></tr>
<tr><td>El Grande (Driver)</td><td>0x9C3D99E8</td><td>No</td></tr>
<tr><td>El Grande (Driver) (Civ Poor female)</td><td>0x126CFB2F</td><td>No</td></tr>
<tr><td>El Grande (Driver) (Civ Poor male)</td><td>0x98861C8E</td><td>No</td></tr>
<tr><td>El Grande_Driver</td><td>0xCF505E8E</td><td>No</td></tr>
<tr><td>Emplaced GL</td><td>0x415B91A9</td><td>No</td></tr>
<tr><td>Emplaced GL (Driver)</td><td>0xA52F3DC4</td><td>No</td></tr>
<tr><td>Emplaced GL (NO Physics)</td><td>0x6B439A94</td><td>No</td></tr>
<tr><td>Emplaced GL (NO Physics) (Driver)</td><td>0x1DD8B573</td><td>No</td></tr>
<tr><td>Emplaced M101A1 (Base)</td><td>0xB3953317</td><td>No</td></tr>
<tr><td>Emplaced M101A1 (GR)</td><td>0x3606AE5B</td><td>No</td></tr>
<tr><td>Emplaced M101A1 (GR) (Driver)</td><td>0xFF912536</td><td>No</td></tr>
<tr><td>Emplaced M101A1 (VZ)</td><td>0xD83A395A</td><td>No</td></tr>
<tr><td>Emplaced M101A1 (VZ) (Driver)</td><td>0x8D7E0F01</td><td>No</td></tr>
<tr><td>Emplaced MG</td><td>0x0737A57C</td><td>No</td></tr>
<tr><td>Emplaced MG (AL)</td><td>0x87C1F1F4</td><td>No</td></tr>
<tr><td>Emplaced MG (AL) (Gunner)</td><td>0x03DB8EE6</td><td>No</td></tr>
<tr><td>Emplaced MG (CH)</td><td>0xAC58DB2A</td><td>No</td></tr>
<tr><td>Emplaced MG (Guerilla)</td><td>0x79156930</td><td>No</td></tr>
<tr><td>Emplaced MG (NO Physics)</td><td>0x24A780DF</td><td>No</td></tr>
<tr><td>Emplaced MG (OC)</td><td>0x42C1E09B</td><td>No</td></tr>
<tr><td>Emplaced MG (PR)</td><td>0xB5D0D153</td><td>No</td></tr>
<tr><td>Emplaced MG (VZ)</td><td>0xDE9A32BD</td><td>No</td></tr>
<tr><td>Emplaced MG DB</td><td>0x42A42946</td><td>No</td></tr>
<tr><td>Emplaced MG3 (Allied)</td><td>0x062E7C3B</td><td>No</td></tr>
<tr><td>Emplaced MG3 (OC)</td><td>0x15C178B6</td><td>No</td></tr>
<tr><td>Emplaced Quad50 (Driver)</td><td>0x948AAE91</td><td>No</td></tr>
<tr><td>Emplaced Quad50 (GR)</td><td>0x01CC3F6E</td><td>No</td></tr>
<tr><td>Emplaced Recoiless Rifle</td><td>0xCFC5EA73</td><td>No</td></tr>
<tr><td>Emplaced Recoiless Rifle (Allied)</td><td>0xB32356DF</td><td>No</td></tr>
<tr><td>Emplaced Recoiless Rifle (China)</td><td>0xF3ECF579</td><td>No</td></tr>
<tr><td>Emplaced Recoiless Rifle (GR)</td><td>0xC9C40571</td><td>No</td></tr>
<tr><td>Emplaced Recoiless Rifle (OC)</td><td>0x73341312</td><td>No</td></tr>
<tr><td>Emplaced Recoiless Rifle (VZ)</td><td>0xED0D7950</td><td>No</td></tr>
<tr><td>Emplaced TOW</td><td>0x9E1AF7CE</td><td>No</td></tr>
<tr><td>Emplaced TOW (Allied)</td><td>0x03AB6E40</td><td>No</td></tr>
<tr><td>Emplaced Tripod Weapon</td><td>0x154AC16C</td><td>No</td></tr>
<tr><td>Emplaced Weapon</td><td>0xB00CE408</td><td>No</td></tr>
<tr><td>Emplaced ZU23</td><td>0x8A48F46A</td><td>No</td></tr>
<tr><td>Emplaced ZU23 (Driver)</td><td>0xF239B751</td><td>No</td></tr>
<tr><td>Emplaced ZU23 (Driver) (Seatbelted)</td><td>0x26B2F447</td><td>No</td></tr>
<tr><td>Endriago (Attack)</td><td>0x8C18A0BB</td><td>No</td></tr>
<tr><td>Endriago (Attack) (Driver)</td><td>0xCF9CDE96</td><td>No</td></tr>
<tr><td>Endriago (Attack) (Ewan)</td><td>0x373FE88F</td><td>No</td></tr>
<tr><td>Endriago (Attack) (Full)</td><td>0xAA2BBCED</td><td>No</td></tr>
<tr><td>Endriago (Elite)</td><td>0xF7847648</td><td>No</td></tr>
<tr><td>Endriago (Elite) (Driver)</td><td>0xBBD6B527</td><td>No</td></tr>
<tr><td>Endriago (Elite) (Ewan)</td><td>0x52C22EBE</td><td>No</td></tr>
<tr><td>Endriago (Superiority)</td><td>0x81AF7BF6</td><td>No</td></tr>
<tr><td>Endriago (Superiority) (Driver)</td><td>0xBAB8C94D</td><td>No</td></tr>
<tr><td>Endriago (Superiority) (Ewan)</td><td>0x7856D228</td><td>No</td></tr>
<tr><td>entrance</td><td>0x7F436ABB</td><td>No</td></tr>
<tr><td>Equipment</td><td>0xDAB653E7</td><td>No</td></tr>
<tr><td>Equipment (Pistol)</td><td>0x0EF3F28B</td><td>No</td></tr>
<tr><td>escort</td><td>0x3392134D</td><td>No</td></tr>
<tr><td>Escort (Driver)</td><td>0xA22C2ED8</td><td>No</td></tr>
<tr><td>Escort (Driver) (Civ Taxi Driver male)</td><td>0xCCC0ED14</td><td>No</td></tr>
<tr><td>Escort_Driver</td><td>0x74AF4DDE</td><td>No</td></tr>
<tr><td>ESV</td><td>0xE715B0A5</td><td>No</td></tr>
<tr><td>ESV (Driver)</td><td>0xBFCEB0B0</td><td>No</td></tr>
<tr><td>ESV (Executive Passengers)</td><td>0x231C723D</td><td>No</td></tr>
<tr><td>ESV (Full)</td><td>0x53857247</td><td>No</td></tr>
<tr><td>Esv (lowrider)</td><td>0x45A8D20C</td><td>No</td></tr>
<tr><td>ESV (Lowrider) (Civ Business (male)</td><td>0x05179C74</td><td>No</td></tr>
<tr><td>ESV/EXT</td><td>0x17088F3D</td><td>No</td></tr>
<tr><td>ESV_Driver</td><td>0xB9EDD606</td><td>No</td></tr>
<tr><td>ESVLowrider_Driver</td><td>0xE53146F0</td><td>No</td></tr>
<tr><td>Eva</td><td>0x46D28FA9</td><td>No</td></tr>
<tr><td>Explosion</td><td>0x16930AFE</td><td>No</td></tr>
<tr><td>Explosion ( Surgical Strike Small)</td><td>0xE3C9E9B8</td><td>No</td></tr>
<tr><td>Explosion (25mm Autocannon Shell)</td><td>0x7028DCFA</td><td>No</td></tr>
<tr><td>Explosion (AA Detonation)</td><td>0x9A4F1130</td><td>No</td></tr>
<tr><td>Explosion (Action Hijack Grenade)</td><td>0xD1F8D673</td><td>No</td></tr>
<tr><td>Explosion (Airstike Bomb Final Strike)</td><td>0xCD8E9443</td><td>No</td></tr>
<tr><td>Explosion (Airstike Bomb)</td><td>0x76647795</td><td>No</td></tr>
<tr><td>Explosion (Airstrike Frag)</td><td>0xB598F2B1</td><td>No</td></tr>
<tr><td>Explosion (AT Mine)</td><td>0xAD41C2AF</td><td>No</td></tr>
<tr><td>Explosion (AT Missile)</td><td>0xBC2A728E</td><td>No</td></tr>
<tr><td>Explosion (Bombing Run)</td><td>0xD2B69D9A</td><td>No</td></tr>
<tr><td>Explosion (Bunker Buster Stage 1)</td><td>0xDDFC11F4</td><td>No</td></tr>
<tr><td>Explosion (Bunker Buster Stage 2)</td><td>0xAD85F5DD</td><td>No</td></tr>
<tr><td>Explosion (C4 Primary)</td><td>0x150F6CE6</td><td>No</td></tr>
<tr><td>Explosion (C4 Secondary)</td><td>0xF4A69A1E</td><td>No</td></tr>
<tr><td>Explosion (Carpet bomb)</td><td>0x7CBBB47A</td><td>No</td></tr>
<tr><td>Explosion (Cluster Bomb)</td><td>0x25273161</td><td>No</td></tr>
<tr><td>Explosion (Cluster Bomblet)</td><td>0x8BE95DA4</td><td>No</td></tr>
<tr><td>Explosion (Cruise Missile)</td><td>0x4B08A278</td><td>No</td></tr>
<tr><td>Explosion (Daisy Cutter)</td><td>0x34DEC7A2</td><td>No</td></tr>
<tr><td>Explosion (E3 Missile Strike)</td><td>0x6B6C4D1D</td><td>No</td></tr>
<tr><td>Explosion (Force)</td><td>0xC0F7BAA4</td><td>No</td></tr>
<tr><td>Explosion (Fuel Air Bomb)</td><td>0x834C9BF3</td><td>No</td></tr>
<tr><td>Explosion (Fuel Air Rocket Stage II)</td><td>0xC64F9AC3</td><td>No</td></tr>
<tr><td>Explosion (Fuel Air Rocket)</td><td>0x1500DD83</td><td>No</td></tr>
<tr><td>Explosion (Grenade Frag)</td><td>0xF5D8EE81</td><td>No</td></tr>
<tr><td>Explosion (Grenade MG)</td><td>0xE443510D</td><td>No</td></tr>
<tr><td>Explosion (Grenade)</td><td>0x6A8141F5</td><td>No</td></tr>
<tr><td>Explosion (Gunship Shell)</td><td>0xBF766119</td><td>Yes</td></tr>
<tr><td>Explosion (Hand Grenade Frag)</td><td>0x486B6D16</td><td>No</td></tr>
<tr><td>Explosion (Hand Grenade)</td><td>0xB6393F34</td><td>No</td></tr>
<tr><td>Explosion (Handheld PEP)</td><td>0x671C7430</td><td>No</td></tr>
<tr><td>Explosion (Handheld RPG Frag)</td><td>0x03EAE0C8</td><td>No</td></tr>
<tr><td>Explosion (Handheld RPG)</td><td>0xEB4ECA16</td><td>No</td></tr>
<tr><td>Explosion (MOAB)</td><td>0xD511013C</td><td>No</td></tr>
<tr><td>Explosion (Munitions Laptop)</td><td>0xE7DBFE85</td><td>No</td></tr>
<tr><td>Explosion (Munitions)</td><td>0x599F00F1</td><td>No</td></tr>
<tr><td>Explosion (Nil)</td><td>0xA3FB3C40</td><td>No</td></tr>
<tr><td>Explosion (Practice Bomb)</td><td>0xEEC245A4</td><td>No</td></tr>
<tr><td>Explosion (Rocket Artillery)</td><td>0x985804BD</td><td>No</td></tr>
<tr><td>Explosion (RPG Frag)</td><td>0x400A470A</td><td>No</td></tr>
<tr><td>Explosion (RPG)</td><td>0xFD0F7310</td><td>No</td></tr>
<tr><td>Explosion (Small Airstike Bomb)</td><td>0x66BA5A4E</td><td>No</td></tr>
<tr><td>Explosion (Small)</td><td>0x4D62A088</td><td>No</td></tr>
<tr><td>Explosion (Smart Bomb)</td><td>0x36BE81FC</td><td>No</td></tr>
<tr><td>Explosion (Strategic Missile)</td><td>0x6D290F19</td><td>No</td></tr>
<tr><td>Explosion (Surgical Strike Invisible)</td><td>0xEDB48E74</td><td>No</td></tr>
<tr><td>Explosion (Surgical Strike)</td><td>0x3219AC3B</td><td>No</td></tr>
<tr><td>Explosion (Tank Artillery)</td><td>0x35EC2FDD</td><td>Yes</td></tr>
<tr><td>Explosion (Tank Shell)</td><td>0x0AB943B9</td><td>Yes</td></tr>
<tr><td>Explosion (TEST)</td><td>0x1DFA117F</td><td>No</td></tr>
<tr><td>Explosion (Tiny)</td><td>0xCFC135B5</td><td>No</td></tr>
<tr><td>Explosion (Very Small)</td><td>0xE1F3EBA4</td><td>No</td></tr>
<tr><td>Explosion (Very Tiny)</td><td>0xCCE4F221</td><td>No</td></tr>
<tr><td>Explosion (Water Mine)</td><td>0xF5E7C0D5</td><td>No</td></tr>
<tr><td>Explosion AllCon002 Pipes</td><td>0x93805F82</td><td>No</td></tr>
<tr><td>Explosion_Artillery</td><td>0x7B661479</td><td>No</td></tr>
<tr><td>Explosion_Large</td><td>0x56B83982</td><td>No</td></tr>
<tr><td>Explosion_Large_OilTruck</td><td>0x23B6A048</td><td>Yes</td></tr>
<tr><td>explosion_rpg</td><td>0x5CDE5C1E</td><td>No</td></tr>
<tr><td>Explosion_Test</td><td>0xB6F610E5</td><td>No</td></tr>
<tr><td>ExplosionGrit</td><td>0xF565D29E</td><td>No</td></tr>
<tr><td>EXT</td><td>0x26308AFA</td><td>No</td></tr>
<tr><td>EXT (Driver)</td><td>0x5BFB8AA1</td><td>No</td></tr>
<tr><td>EXT (DriverGunner)</td><td>0xB1FC1FF2</td><td>No</td></tr>
<tr><td>EXT (Full)</td><td>0x44CD8436</td><td>No</td></tr>
<tr><td>EXT (GL)</td><td>0xB60CD310</td><td>No</td></tr>
<tr><td>EXT (GL) (Driver)</td><td>0xBD9DF52F</td><td>No</td></tr>
<tr><td>EXT (GL) (DriverGunner)</td><td>0xCC757908</td><td>No</td></tr>
<tr><td>EXT (GL) (Full)</td><td>0xC43D9164</td><td>No</td></tr>
<tr><td>EXT (monster)</td><td>0xB6D6F9F1</td><td>No</td></tr>
<tr><td>EXT (TOW)</td><td>0xE49A8C75</td><td>No</td></tr>
<tr><td>EXT (TOW) (Driver)</td><td>0x6D3F3C80</td><td>No</td></tr>
<tr><td>EXT (TOW) (DriverGunner)</td><td>0x8C4F663F</td><td>No</td></tr>
<tr><td>EXT (TOW) (Full)</td><td>0xD2C8CD97</td><td>No</td></tr>
<tr><td>EXT (Unarmed)</td><td>0x78C50A1D</td><td>No</td></tr>
<tr><td>EXT (Unarmed) (Driver)</td><td>0xEC30FD28</td><td>No</td></tr>
<tr><td>EXT_Driver</td><td>0x44C70BAB</td><td>No</td></tr>
<tr><td>EXTMonster_Driver</td><td>0x952B1D5D</td><td>No</td></tr>
<tr><td>F35b</td><td>0x1AD49939</td><td>Yes</td></tr>
<tr><td>F35b (GR driver)</td><td>0x4F6B3B65</td><td>Yes</td></tr>
<tr><td>FA Missile</td><td>0x06BFC2BE</td><td>No</td></tr>
<tr><td>FA RPG Rocket</td><td>0xE8279B7D</td><td>No</td></tr>
<tr><td>Faction (Allied)</td><td>0x4933886F</td><td>No</td></tr>
<tr><td>Faction (China)</td><td>0x3F8DCE69</td><td>No</td></tr>
<tr><td>Faction (Civ)</td><td>0x898188A8</td><td>No</td></tr>
<tr><td>Faction (Guerilla)</td><td>0x9D95C52D</td><td>No</td></tr>
<tr><td>Faction (OC)</td><td>0x9FE42462</td><td>No</td></tr>
<tr><td>Faction (Pirate)</td><td>0x4C0CB2F9</td><td>No</td></tr>
<tr><td>Faction (PMC)</td><td>0xA55FA50A</td><td>No</td></tr>
<tr><td>Faction (Police)</td><td>0x95F6F9CE</td><td>No</td></tr>
<tr><td>Faction (VZ)</td><td>0x8E772860</td><td>No</td></tr>
<tr><td>Faction Building (Allied)</td><td>0xEC7B01D9</td><td>No</td></tr>
<tr><td>Faction Building (China)</td><td>0xF678EBC7</td><td>No</td></tr>
<tr><td>Faction Building (Guerilla)</td><td>0xFD2D649F</td><td>No</td></tr>
<tr><td>Faction Building (OC)</td><td>0x2804AA7C</td><td>No</td></tr>
<tr><td>Faction Building (Pirate)</td><td>0xA452EC97</td><td>No</td></tr>
<tr><td>Faction Building (VZ)</td><td>0xBDEDDE5A</td><td>No</td></tr>
<tr><td>Fake Physics Prop</td><td>0x8E1BFDB8</td><td>No</td></tr>
<tr><td>Fake Physics Prop Destructible</td><td>0x11DCF132</td><td>No</td></tr>
<tr><td>Fern01</td><td>0xA15E4C37</td><td>No</td></tr>
<tr><td>Fiona</td><td>0xC6D8FB46</td><td>No</td></tr>
<tr><td>Fiona Taylor</td><td>0x723E34F7</td><td>No</td></tr>
<tr><td>Fire</td><td>0x8A552089</td><td>No</td></tr>
<tr><td>Fire Damage (Huge)</td><td>0xD31A163A</td><td>No</td></tr>
<tr><td>Fire Damage (Large)</td><td>0xB85EAA42</td><td>No</td></tr>
<tr><td>Fire Damage (Medium Canopy)</td><td>0xE87D41BC</td><td>No</td></tr>
<tr><td>Fire Damage (Medium)</td><td>0x3DF67356</td><td>No</td></tr>
<tr><td>Fire Damage (Small)</td><td>0x11D78F96</td><td>No</td></tr>
<tr><td>Fire Damage (Tiny)</td><td>0x927B288F</td><td>No</td></tr>
<tr><td>Fishing Boat</td><td>0x5ED1AEE5</td><td>Yes</td></tr>
<tr><td>Fishing Boat (Driver)</td><td>0x1C0DF270</td><td>Yes</td></tr>
<tr><td>Fishing Boat (Driver) (Civ Poor female)</td><td>0x75FFCB27</td><td>Yes</td></tr>
<tr><td>Fishing Boat (Driver) (Civ Poor male)</td><td>0x27950AA6</td><td>Yes</td></tr>
<tr><td>Fishing Boat_Ruined</td><td>0xEA99A479</td><td>Yes</td></tr>
<tr><td>FishingBoat_Driver</td><td>0x27672BF8</td><td>Yes</td></tr>
<tr><td>Fixed Physics Prop</td><td>0x65635CE1</td><td>No</td></tr>
<tr><td>Fixed Physics Prop Destructible</td><td>0xB0B47C61</td><td>No</td></tr>
<tr><td>Fixed Physics Prop destructible chair</td><td>0x114108D2</td><td>No</td></tr>
<tr><td>Flare</td><td>0x0DA8F2A7</td><td>No</td></tr>
<tr><td>Flare Designator</td><td>0x95BBB587</td><td>No</td></tr>
<tr><td>Flare Projectile</td><td>0xD2E88940</td><td>No</td></tr>
<tr><td>Flare Projectile Stage 2</td><td>0x691C913C</td><td>No</td></tr>
<tr><td>Flare0</td><td>0x0DBFB9FD</td><td>No</td></tr>
<tr><td>Flare1</td><td>0xA3BCD488</td><td>No</td></tr>
<tr><td>Flare2</td><td>0xADBAA5AF</td><td>No</td></tr>
<tr><td>FlareSmoke</td><td>0xE8FE3776</td><td>No</td></tr>
<tr><td>Flatbed Trailer</td><td>0xD779F5F0</td><td>No</td></tr>
<tr><td>Flow Control</td><td>0x00C4CFDE</td><td>No</td></tr>
<tr><td>foliage_test</td><td>0xBC97DA6D</td><td>No</td></tr>
<tr><td>foodcarts</td><td>0x784CDE76</td><td>No</td></tr>
<tr><td>Ford F150</td><td>0x2874601E</td><td>No</td></tr>
<tr><td>fountains</td><td>0x1A94E908</td><td>No</td></tr>
<tr><td>Fuel Air Bomb Projectile</td><td>0x4A35D0C4</td><td>No</td></tr>
<tr><td>Fuel Air Trail</td><td>0x13432421</td><td>No</td></tr>
<tr><td>Fuel Pickup (Large)</td><td>0xDEE1F1F1</td><td>No</td></tr>
<tr><td>Fuel Pickup (Small)</td><td>0x8905D2F5</td><td>No</td></tr>
<tr><td>Fuel Trailer</td><td>0xD9B1BD84</td><td>No</td></tr>
<tr><td>Fuel-Air RPG</td><td>0x47E86EB3</td><td>No</td></tr>
<tr><td>Fx_CHUNKTRAIL_DUST</td><td>0x9FF3CC1A</td><td>No</td></tr>
<tr><td>Fx_CHUNKTRAIL_FIRE</td><td>0xB3F07C5A</td><td>No</td></tr>
<tr><td>Fx_CHUNKTRAIL_UNLITFIRE</td><td>0xCCF36BD2</td><td>No</td></tr>
<tr><td>fx_CollapseBits</td><td>0xD0BAEA4F</td><td>No</td></tr>
<tr><td>fx_CollapseBitsFort</td><td>0x4B83C230</td><td>No</td></tr>
<tr><td>fx_CollapseBitsShort</td><td>0x7CDB4407</td><td>No</td></tr>
<tr><td>fx_CollapseBitsShortSmoke</td><td>0xEE68CDD6</td><td>No</td></tr>
<tr><td>fx_CollapseBitsShortSpecial</td><td>0x96ACBE54</td><td>No</td></tr>
<tr><td>fx_CollapseBitsSmoke</td><td>0x93823A5E</td><td>No</td></tr>
<tr><td>fx_CollapseBitsSmokeSuper</td><td>0xF2E7D883</td><td>No</td></tr>
<tr><td>fx_CollapseBitsSuper</td><td>0x5B1CB278</td><td>No</td></tr>
<tr><td>fx_CollapseBitsTiny</td><td>0xD0415261</td><td>No</td></tr>
<tr><td>fx_CollapseBitsTinySmoke</td><td>0x2335C668</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDust</td><td>0x64E12D08</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDust_end</td><td>0xE9421F0A</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDust_endSuper</td><td>0xD3CAA477</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDust_LOD0</td><td>0xBBAC3C2C</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDust_LOD1</td><td>0xB5AE7151</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDust_start</td><td>0x81CEB475</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDust_startSuper</td><td>0x8278C062</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDustBottom</td><td>0x5685D6B1</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDustBottomSuper</td><td>0x10AC5566</td><td>No</td></tr>
<tr><td>fx_CollapseCoverDustSuper</td><td>0x8D53C8C1</td><td>No</td></tr>
<tr><td>fx_CollapseCoverWater</td><td>0xECC01BF5</td><td>No</td></tr>
<tr><td>fx_CollapseFire</td><td>0xC60FDD97</td><td>No</td></tr>
<tr><td>fx_CollapseFireFull</td><td>0xA29C1DD8</td><td>No</td></tr>
<tr><td>fx_CollapseFireFullSuper</td><td>0x3985EFB1</td><td>No</td></tr>
<tr><td>fx_CollapseFireSuper</td><td>0x8994E8D0</td><td>No</td></tr>
<tr><td>fx_EmitChimineySmoke</td><td>0xA73AF2D6</td><td>No</td></tr>
<tr><td>fx_EmitFlame</td><td>0xF7505100</td><td>No</td></tr>
<tr><td>fx_EmitFlameOil</td><td>0x3D4CD6C0</td><td>No</td></tr>
<tr><td>fx_EmitFlameOilrigTower</td><td>0x88237E81</td><td>No</td></tr>
<tr><td>fx_EmitFlameOilrigTower_smoke</td><td>0x7F8DC56B</td><td>No</td></tr>
<tr><td>fx_EmitFlameSmall</td><td>0x0EBC8B29</td><td>No</td></tr>
<tr><td>fx_EmitFlameTiny</td><td>0x4CB97C3A</td><td>No</td></tr>
<tr><td>fx_EmitSmokeStack</td><td>0x00A433FE</td><td>No</td></tr>
<tr><td>fx_engineDamageSmoke</td><td>0x499056C2</td><td>No</td></tr>
<tr><td>fx_engineHeatHaze</td><td>0x49A06570</td><td>No</td></tr>
<tr><td>fx_Explosion_Huge</td><td>0x09EC0A9B</td><td>No</td></tr>
<tr><td>fx_Explosion_Huge_LOD0</td><td>0x6AB2FF79</td><td>No</td></tr>
<tr><td>fx_Explosion_Huge_LOD1</td><td>0x90B0FCB4</td><td>No</td></tr>
<tr><td>fx_Explosion_HugeBoat</td><td>0x431548E1</td><td>Yes</td></tr>
<tr><td>fx_Explosion_HugeOil</td><td>0x78A27901</td><td>No</td></tr>
<tr><td>fx_Explosion_HugeOil_LOD0</td><td>0xFC01CDB3</td><td>No</td></tr>
<tr><td>fx_Explosion_HugeOil_LOD1</td><td>0x99FEF4D6</td><td>No</td></tr>
<tr><td>fx_Explosion_HugeOil_RigOnly</td><td>0x0B9A59F4</td><td>No</td></tr>
<tr><td>fx_Explosion_HugeOilTower</td><td>0x150059D4</td><td>No</td></tr>
<tr><td>fx_Explosion_HugeOilTower_LOD0</td><td>0xF09B8A90</td><td>No</td></tr>
<tr><td>fx_Explosion_HugeOilTower_LOD1</td><td>0xDA9DA685</td><td>No</td></tr>
<tr><td>fx_Explosion_HugeOilTower_RigOnly</td><td>0x10E37095</td><td>No</td></tr>
<tr><td>fx_Explosion_HugeOilTowerBoat</td><td>0x37C5936A</td><td>Yes</td></tr>
<tr><td>fx_Explosion_Large</td><td>0x0538CC93</td><td>No</td></tr>
<tr><td>fx_Explosion_Large_LOD0</td><td>0x89DC4011</td><td>No</td></tr>
<tr><td>fx_Explosion_Large_LOD1</td><td>0x8FDA0AEC</td><td>No</td></tr>
<tr><td>fx_Explosion_Medium</td><td>0x7A757DBB</td><td>No</td></tr>
<tr><td>fx_Explosion_Medium_LOD0</td><td>0x4087C799</td><td>No</td></tr>
<tr><td>fx_Explosion_Medium_LOD1</td><td>0xE684FB54</td><td>No</td></tr>
<tr><td>fx_Explosion_MediumBoat</td><td>0x27531981</td><td>Yes</td></tr>
<tr><td>fx_Explosion_MediumOil</td><td>0xD6FB13A1</td><td>No</td></tr>
<tr><td>fx_Explosion_MediumOil_LOD0</td><td>0xB0987253</td><td>No</td></tr>
<tr><td>fx_Explosion_MediumOil_LOD1</td><td>0xCE9662F6</td><td>No</td></tr>
<tr><td>fx_Explosion_MediumOilPipe</td><td>0xFA3F97E5</td><td>No</td></tr>
<tr><td>fx_Explosion_Small</td><td>0xE7AA5B4B</td><td>No</td></tr>
<tr><td>fx_Explosion_Small_LOD0</td><td>0x991D9B49</td><td>No</td></tr>
<tr><td>fx_Explosion_Small_LOD1</td><td>0x7F1B33C4</td><td>No</td></tr>
<tr><td>fx_Explosion_SmallBoat</td><td>0xD96D22F1</td><td>Yes</td></tr>
<tr><td>fx_ExplosionGrit</td><td>0x6AD474EF</td><td>No</td></tr>
<tr><td>fx_ExplosionGritDelay3</td><td>0x9DB60747</td><td>No</td></tr>
<tr><td>fx_ImpactShockwaveMedium</td><td>0xE10E0D0C</td><td>No</td></tr>
<tr><td>fx_OilrigDebrisDestroy</td><td>0x11199B75</td><td>No</td></tr>
<tr><td>fx_OilrigDebrisDestroyExplosion</td><td>0x360357A6</td><td>No</td></tr>
<tr><td>fx_ShortCollapseCoverDust</td><td>0xDCF9ED86</td><td>No</td></tr>
<tr><td>fx_ShortCollapseCoverDustBottom</td><td>0x9C913EA3</td><td>No</td></tr>
<tr><td>fx_ShortCollapseCoverDustFort</td><td>0xDC6FD589</td><td>No</td></tr>
<tr><td>fx_ShortCollapseCoverDustFortStart</td><td>0x27AC0203</td><td>No</td></tr>
<tr><td>fx_ShortCollapseCoverDustStart</td><td>0xF3D0717A</td><td>No</td></tr>
<tr><td>fx_ShortCollapseFire</td><td>0xFE2734ED</td><td>No</td></tr>
<tr><td>fx_ShortCollapseFireDelay</td><td>0x87F84666</td><td>No</td></tr>
<tr><td>fx_ShortCoverDustBottom</td><td>0x2ABC0D28</td><td>No</td></tr>
<tr><td>fx_TinyCollapseCoverDust</td><td>0xB66CF4AA</td><td>No</td></tr>
<tr><td>fx_TinyCollapseCoverDustBottom</td><td>0xA126713F</td><td>No</td></tr>
<tr><td>fx_TinyCollapseFire</td><td>0x18281EE9</td><td>No</td></tr>
<tr><td>Garbage Truck</td><td>0x1015767F</td><td>Yes</td></tr>
<tr><td>Garbage Truck (Driver)</td><td>0xAF8AEAEA</td><td>Yes</td></tr>
<tr><td>Garbage Truck (Driver) (Civ Industrial female)</td><td>0x41195AFC</td><td>Yes</td></tr>
<tr><td>Garbage Truck (Driver) (Civ Industrial male)</td><td>0xE242790D</td><td>Yes</td></tr>
<tr><td>Garbage_Driver</td><td>0xFC338953</td><td>No</td></tr>
<tr><td>Generic_Large_Interior</td><td>0x4EB64B07</td><td>No</td></tr>
<tr><td>Generic_Small_Interior</td><td>0xFDC46BF3</td><td>No</td></tr>
<tr><td>GlassShards</td><td>0xB6655EC8</td><td>No</td></tr>
<tr><td>gleach</td><td>0xEF44FAAB</td><td>No</td></tr>
<tr><td>gleach child 1</td><td>0x40537CAC</td><td>No</td></tr>
<tr><td>gleach child 2</td><td>0xDA509D83</td><td>No</td></tr>
<tr><td>global_debris_woodbeams01</td><td>0x28FCBBBB</td><td>No</td></tr>
<tr><td>global_env_tree_large_debris</td><td>0xE25EA4C7</td><td>No</td></tr>
<tr><td>global_env_tree_medium_debris</td><td>0x6F648A87</td><td>No</td></tr>
<tr><td>global_env_treecanopy_debris</td><td>0x5F75A3D7</td><td>No</td></tr>
<tr><td>global_particle_0x80009e34</td><td>0xE7C9E46F</td><td>No</td></tr>
<tr><td>global_particle_airstrike_artillery</td><td>0xF132D8D1</td><td>No</td></tr>
<tr><td>global_particle_airstrike_bunkerbuster</td><td>0xEEECE9F9</td><td>No</td></tr>
<tr><td>global_particle_airstrike_bunkerbuster_flash</td><td>0x1C0D7336</td><td>No</td></tr>
<tr><td>global_particle_airstrike_bunkerbuster_initial</td><td>0x4DCC85CC</td><td>No</td></tr>
<tr><td>global_particle_airstrike_carpetbomb_LOD0</td><td>0xDF505090</td><td>No</td></tr>
<tr><td>global_particle_airstrike_carpetbomb_LOD1</td><td>0xC9526C85</td><td>No</td></tr>
<tr><td>global_particle_airstrike_clusterbomb</td><td>0xBBAD61F9</td><td>No</td></tr>
<tr><td>global_particle_airstrike_clusterbomb_flame</td><td>0xFDE728C5</td><td>No</td></tr>
<tr><td>global_particle_airstrike_cruisemissile</td><td>0x3113506C</td><td>No</td></tr>
<tr><td>global_particle_airstrike_daisycutter</td><td>0x65E42D40</td><td>No</td></tr>
<tr><td>global_particle_airstrike_distance</td><td>0xA3ADF8C8</td><td>No</td></tr>
<tr><td>global_particle_airstrike_exit_explosion</td><td>0x9EC090A1</td><td>No</td></tr>
<tr><td>global_particle_airstrike_fuelairbomb</td><td>0x8B944877</td><td>No</td></tr>
<tr><td>global_particle_airstrike_missile</td><td>0x5FED4B9B</td><td>No</td></tr>
<tr><td>global_particle_airstrike_moab</td><td>0xC2F6DEE0</td><td>No</td></tr>
<tr><td>global_particle_airstrike_rocket_artillery_LOD0</td><td>0xB3F67166</td><td>No</td></tr>
<tr><td>global_particle_airstrike_rocket_artillery_LOD1</td><td>0xD5F8E583</td><td>No</td></tr>
<tr><td>global_particle_airstrike_smartbomb</td><td>0x8EB9C034</td><td>No</td></tr>
<tr><td>global_particle_airstrike_tactnuke</td><td>0x45D71EEA</td><td>No</td></tr>
<tr><td>global_particle_airstrike_tactnuke_distance</td><td>0x14B7D77C</td><td>No</td></tr>
<tr><td>global_particle_blastdoors_ext_smoke</td><td>0xEE56EB8F</td><td>No</td></tr>
<tr><td>global_particle_blastdoors_tunnelbottom_smoke</td><td>0xCE764F3D</td><td>No</td></tr>
<tr><td>global_particle_blastdoors_tunneltop_smoke</td><td>0x6DF39525</td><td>No</td></tr>
<tr><td>global_particle_boatroostertail</td><td>0xE1FE22C4</td><td>Yes</td></tr>
<tr><td>global_particle_boatroostertail_slow</td><td>0xB43ADDD0</td><td>Yes</td></tr>
<tr><td>global_particle_boatroostertail_small</td><td>0x875B9010</td><td>Yes</td></tr>
<tr><td>global_particle_boatroostertail_small_drift</td><td>0xC36D5A48</td><td>Yes</td></tr>
<tr><td>global_particle_boatroostertail_small_slow</td><td>0x7601FDC4</td><td>Yes</td></tr>
<tr><td>global_particle_boatwake</td><td>0x33DF8EDA</td><td>Yes</td></tr>
<tr><td>global_particle_boatwake_drift</td><td>0xC92D0D2E</td><td>Yes</td></tr>
<tr><td>global_particle_boatwake_drift_small</td><td>0x16141FAA</td><td>Yes</td></tr>
<tr><td>global_particle_boatwake_point</td><td>0x8F3162A5</td><td>Yes</td></tr>
<tr><td>global_particle_boatwake_point_slow</td><td>0x73BF064F</td><td>Yes</td></tr>
<tr><td>global_particle_boatwake_slow</td><td>0xEDAB7A02</td><td>Yes</td></tr>
<tr><td>global_particle_boatwake_slow_small</td><td>0xF1C7B02E</td><td>Yes</td></tr>
<tr><td>global_particle_boatwake_small</td><td>0x8032FA06</td><td>Yes</td></tr>
<tr><td>global_particle_buildingdebrislarge</td><td>0xD1492CDA</td><td>No</td></tr>
<tr><td>global_particle_bunker_top_smoke</td><td>0x98EE4149</td><td>No</td></tr>
<tr><td>global_particle_debris_rpg01</td><td>0x44576F90</td><td>No</td></tr>
<tr><td>global_particle_dirtexplosion</td><td>0xB7EDE5F8</td><td>No</td></tr>
<tr><td>global_particle_dirtexplosion_fan_large</td><td>0xDF2F904A</td><td>No</td></tr>
<tr><td>global_particle_dirtexplosion_large</td><td>0x46DB9478</td><td>No</td></tr>
<tr><td>global_particle_dirtexplosion_small</td><td>0xEB216074</td><td>No</td></tr>
<tr><td>global_particle_dustexplosion</td><td>0x338AC051</td><td>No</td></tr>
<tr><td>global_particle_dustfall</td><td>0xCA4220A3</td><td>No</td></tr>
<tr><td>global_particle_dustshanty</td><td>0x03723F4D</td><td>No</td></tr>
<tr><td>global_particle_duststrike</td><td>0x26E1A04A</td><td>No</td></tr>
<tr><td>global_particle_dusttrail</td><td>0xFAB952F0</td><td>No</td></tr>
<tr><td>global_particle_env_bug_swarm_placeable</td><td>0x6958E54F</td><td>No</td></tr>
<tr><td>global_particle_env_firesmokeplume_infinite</td><td>0x07C664D5</td><td>No</td></tr>
<tr><td>global_particle_env_godray2_placeable</td><td>0x7956CD3C</td><td>No</td></tr>
<tr><td>global_particle_env_godray_placeable</td><td>0xC743959A</td><td>No</td></tr>
<tr><td>global_particle_env_merida_smoke_boat</td><td>0x0A9BF54F</td><td>Yes</td></tr>
<tr><td>global_particle_env_merida_smoke_infinite</td><td>0x100DAAB9</td><td>No</td></tr>
<tr><td>global_particle_env_mist_light_placeable</td><td>0xE2D5AB12</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_boat</td><td>0xC85169EF</td><td>Yes</td></tr>
<tr><td>global_particle_env_smokeplume_boat_LOD1</td><td>0x3F303830</td><td>Yes</td></tr>
<tr><td>global_particle_env_smokeplume_distance</td><td>0x81B1D9D4</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_distance_light</td><td>0x68CD69CD</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_distance_light_LOD1</td><td>0x1B4B3AFA</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_distance_LOD0</td><td>0x76500A90</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_distance_LOD1</td><td>0x60522685</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_distance_tall</td><td>0x0E187EA2</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_distance_tall_light</td><td>0x549CD12B</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_distance_tall_light_LOD1</td><td>0xB887A2A4</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_distance_tall_LOD1</td><td>0xD424C6D7</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_infinite</td><td>0x58AC1659</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_infinite_LOD1</td><td>0x1635366E</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_light_infinite</td><td>0x3969FD12</td><td>No</td></tr>
<tr><td>global_particle_env_smokeplume_light_infinite_LOD1</td><td>0x929663A7</td><td>No</td></tr>
<tr><td>global_particle_exp_falling_debris_airstrike</td><td>0xBB148FF6</td><td>No</td></tr>
<tr><td>global_particle_exp_falling_debris_huge</td><td>0x71186BE1</td><td>No</td></tr>
<tr><td>global_particle_exp_falling_debris_lrg</td><td>0xC0D14C79</td><td>No</td></tr>
<tr><td>global_particle_exp_falling_debris_lrg_special</td><td>0x72DEAE19</td><td>No</td></tr>
<tr><td>global_particle_exp_falling_debris_lrg_tall</td><td>0x95D31FC9</td><td>No</td></tr>
<tr><td>global_particle_exp_falling_debris_med</td><td>0xB1FE2F96</td><td>No</td></tr>
<tr><td>global_particle_exp_falling_debris_med_tall</td><td>0x98AF6234</td><td>No</td></tr>
<tr><td>global_particle_exp_falling_debris_med_tall_LOD0</td><td>0x481DC970</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground</td><td>0x72FDE10D</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_bunkerbuster</td><td>0x40E58CE4</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_bunkerbuster_a</td><td>0x1162EEAC</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_bunkerbuster_b</td><td>0xAB600F83</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_lrg</td><td>0x96BEBFA1</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_moab</td><td>0xC88A5AE1</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_pep</td><td>0x0B48A267</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_sml</td><td>0x9042EDA4</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tactnuke</td><td>0x9590904F</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tiny</td><td>0x7DEEC326</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tiny_asphalt</td><td>0x2E796D6A</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tiny_concrete</td><td>0x3E3664CC</td><td>No</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tiny_grass</td><td>0x82186D45</td><td>No</td></tr>
<tr><td>global_particle_exp_sparks_sphere_lrg</td><td>0xA2D1A7B6</td><td>No</td></tr>
<tr><td>global_particle_explosion</td><td>0x57F368D9</td><td>No</td></tr>
<tr><td>global_particle_explosion_c4</td><td>0x98FE1D7D</td><td>No</td></tr>
<tr><td>global_particle_explosion_canvas</td><td>0xD0329D94</td><td>No</td></tr>
<tr><td>global_particle_explosion_canvas_large</td><td>0x45FE04E4</td><td>No</td></tr>
<tr><td>global_particle_explosion_clothes_a</td><td>0x05F94DB0</td><td>No</td></tr>
<tr><td>global_particle_explosion_clothes_b</td><td>0xEFF6EC77</td><td>No</td></tr>
<tr><td>global_particle_explosion_feathers</td><td>0xDFAAA9E8</td><td>No</td></tr>
<tr><td>global_particle_explosion_flag_blue</td><td>0x256C3DC9</td><td>No</td></tr>
<tr><td>global_particle_explosion_flag_red</td><td>0x8221D026</td><td>No</td></tr>
<tr><td>global_particle_explosion_flash</td><td>0x458BF396</td><td>No</td></tr>
<tr><td>global_particle_explosion_flash_large</td><td>0xB7C5C5FA</td><td>No</td></tr>
<tr><td>global_particle_explosion_guts</td><td>0xA11F9967</td><td>No</td></tr>
<tr><td>global_particle_explosion_heli_bladeflame</td><td>0x946D93E4</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_heli_bladesparks</td><td>0x0BA8DD59</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_heli_flame</td><td>0x0F2F66A8</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_huge</td><td>0x5A8AB4FD</td><td>No</td></tr>
<tr><td>global_particle_explosion_huge_oil</td><td>0x75ED7824</td><td>No</td></tr>
<tr><td>global_particle_explosion_medium</td><td>0xE5802F81</td><td>No</td></tr>
<tr><td>global_particle_explosion_medium_oil</td><td>0x043828E0</td><td>No</td></tr>
<tr><td>global_particle_explosion_money_large</td><td>0x78311300</td><td>No</td></tr>
<tr><td>global_particle_explosion_money_large_fire</td><td>0x50D6FCC3</td><td>No</td></tr>
<tr><td>global_particle_explosion_money_small</td><td>0x2B9F96FC</td><td>No</td></tr>
<tr><td>global_particle_explosion_papers</td><td>0x5E3601BD</td><td>No</td></tr>
<tr><td>global_particle_explosion_parrotfeathers</td><td>0xCE91FE1C</td><td>No</td></tr>
<tr><td>global_particle_explosion_pickup_ammo</td><td>0x03451E79</td><td>No</td></tr>
<tr><td>global_particle_explosion_pickup_c4</td><td>0x48CE797A</td><td>No</td></tr>
<tr><td>global_particle_explosion_pickup_fuel</td><td>0x170E0A0F</td><td>No</td></tr>
<tr><td>global_particle_explosion_pickup_grenade</td><td>0xF1C5A4D3</td><td>No</td></tr>
<tr><td>global_particle_explosion_pickup_health</td><td>0x25F57375</td><td>No</td></tr>
<tr><td>global_particle_explosion_pickup_large</td><td>0x743A2AD4</td><td>No</td></tr>
<tr><td>global_particle_explosion_pickup_money</td><td>0xDEF99209</td><td>No</td></tr>
<tr><td>global_particle_explosion_pickup_money_small</td><td>0xB35F1111</td><td>No</td></tr>
<tr><td>global_particle_explosion_pickup_rocket</td><td>0xA24B5B2B</td><td>No</td></tr>
<tr><td>global_particle_explosion_plaster_chips</td><td>0x1B329175</td><td>No</td></tr>
<tr><td>global_particle_explosion_rpg</td><td>0xC2C0EEFD</td><td>No</td></tr>
<tr><td>global_particle_explosion_rpg_center</td><td>0xB3EE5AAB</td><td>No</td></tr>
<tr><td>global_particle_explosion_shockwave_ring</td><td>0x94A59F9E</td><td>No</td></tr>
<tr><td>global_particle_explosion_shockwave_sphere</td><td>0x772FF1B7</td><td>No</td></tr>
<tr><td>global_particle_explosion_shockwave_sphere_bunkerbuster</td><td>0xBFE62FD2</td><td>No</td></tr>
<tr><td>global_particle_explosion_small</td><td>0xD21C3CE1</td><td>No</td></tr>
<tr><td>global_particle_explosion_tankhatch</td><td>0xB334C7E6</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_tankhull</td><td>0xFB159F49</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_tankturretflame</td><td>0x1E54DCAF</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_tankturretseam</td><td>0x590A8C40</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_tiny</td><td>0x6335F002</td><td>No</td></tr>
<tr><td>global_particle_explosion_treetrunk</td><td>0xC3B1D63A</td><td>No</td></tr>
<tr><td>global_particle_explosion_vehicle_air</td><td>0xC6622D45</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_vehicle_ground</td><td>0xDC673342</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_vehicle_weakpoint</td><td>0x0544C717</td><td>Yes</td></tr>
<tr><td>global_particle_explosion_water_large</td><td>0x2438D2A1</td><td>No</td></tr>
<tr><td>global_particle_explosion_waterbumper</td><td>0x71A6013C</td><td>No</td></tr>
<tr><td>global_particle_explosion_watertower</td><td>0xA8F00200</td><td>No</td></tr>
<tr><td>global_particle_explosionhuge</td><td>0xF85E869C</td><td>No</td></tr>
<tr><td>global_particle_explosionlarge</td><td>0x639F99B6</td><td>No</td></tr>
<tr><td>global_particle_explosionoiltower</td><td>0x619FE42A</td><td>No</td></tr>
<tr><td>global_particle_explosionsmall</td><td>0x840E78FE</td><td>No</td></tr>
<tr><td>global_particle_explosionverysmall</td><td>0x351DD232</td><td>No</td></tr>
<tr><td>global_particle_fire_armwrestling</td><td>0xD0F96D18</td><td>No</td></tr>
<tr><td>global_particle_fire_carhood</td><td>0xC6666A25</td><td>No</td></tr>
<tr><td>global_particle_fire_jetengine_boost_infinite</td><td>0xF8068AAD</td><td>No</td></tr>
<tr><td>global_particle_fire_jetengine_end</td><td>0x384185DC</td><td>No</td></tr>
<tr><td>global_particle_fire_jetengine_infinite</td><td>0x5D6365F9</td><td>No</td></tr>
<tr><td>global_particle_fire_jetengine_orange_infinite</td><td>0x69333F6E</td><td>No</td></tr>
<tr><td>global_particle_fireblue_infinite</td><td>0x791258A3</td><td>No</td></tr>
<tr><td>global_particle_fireboatflamejet</td><td>0xFB1C0DB8</td><td>Yes</td></tr>
<tr><td>global_particle_fireboatflamejet_smoke</td><td>0x54AAFB66</td><td>Yes</td></tr>
<tr><td>global_particle_fireboatgrande</td><td>0x148F0151</td><td>Yes</td></tr>
<tr><td>global_particle_fireboatgrande_smoke</td><td>0xBD19723B</td><td>Yes</td></tr>
<tr><td>global_particle_fireboatlarge</td><td>0x440BEA87</td><td>Yes</td></tr>
<tr><td>global_particle_fireboatmedium</td><td>0xF05590E7</td><td>Yes</td></tr>
<tr><td>global_particle_fireboatsmall</td><td>0x798CBC2F</td><td>Yes</td></tr>
<tr><td>global_particle_fireboattiny</td><td>0x71BD9CD4</td><td>Yes</td></tr>
<tr><td>global_particle_fireflare_infinite</td><td>0xEEFB3B23</td><td>No</td></tr>
<tr><td>global_particle_firegrandesmoke</td><td>0x50888846</td><td>No</td></tr>
<tr><td>global_particle_firegrandesmoke_infinite</td><td>0x90D31235</td><td>No</td></tr>
<tr><td>global_particle_firegrandesmoke_infinite_smoke</td><td>0xF8C87BEF</td><td>No</td></tr>
<tr><td>global_particle_firegrandesmoke_smoke</td><td>0x948694F4</td><td>No</td></tr>
<tr><td>global_particle_firehedge</td><td>0x8E87B41F</td><td>No</td></tr>
<tr><td>global_particle_firehydrant_spray</td><td>0x8D57E3E4</td><td>No</td></tr>
<tr><td>global_particle_firelarge</td><td>0xF5AB345D</td><td>No</td></tr>
<tr><td>global_particle_firelarge_infinite</td><td>0xA7BD01E8</td><td>No</td></tr>
<tr><td>global_particle_firelarge_infinite_placeable</td><td>0x57632C60</td><td>No</td></tr>
<tr><td>global_particle_firelarge_smoke</td><td>0xABDE53F7</td><td>No</td></tr>
<tr><td>global_particle_firelargesmoke</td><td>0x749958E4</td><td>No</td></tr>
<tr><td>global_particle_firelargesmoke_infinite</td><td>0x8CF6A76F</td><td>No</td></tr>
<tr><td>global_particle_firelargesmoke_infinite_placeable</td><td>0x0D2B6E3F</td><td>No</td></tr>
<tr><td>global_particle_firelargesmoke_infinite_smoke</td><td>0x48974AB9</td><td>No</td></tr>
<tr><td>global_particle_firelargesmoke_infinite_smoke_placeable</td><td>0xA7021585</td><td>No</td></tr>
<tr><td>global_particle_firelargesmoke_smoke</td><td>0x271A4F42</td><td>No</td></tr>
<tr><td>global_particle_firelargesmoke_smoke_vehicle</td><td>0x35F9E783</td><td>Yes</td></tr>
<tr><td>global_particle_firelargesmoke_vehicle</td><td>0xD5624ED9</td><td>Yes</td></tr>
<tr><td>global_particle_firemedium</td><td>0x03A9A049</td><td>No</td></tr>
<tr><td>global_particle_firemediumsmoke</td><td>0xA169E7F0</td><td>No</td></tr>
<tr><td>global_particle_firemediumsmoke_heli</td><td>0xDA1905F7</td><td>Yes</td></tr>
<tr><td>global_particle_firemediumsmoke_heli_infinite</td><td>0xF7211396</td><td>Yes</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite</td><td>0xC4858F83</td><td>No</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite_constant</td><td>0xB94BD146</td><td>No</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite_placeable</td><td>0x59DAC62B</td><td>No</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite_smoke</td><td>0x54D85FBD</td><td>No</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite_smoke_placeable</td><td>0x7AD74241</td><td>No</td></tr>
<tr><td>global_particle_firemediumsmoke_smoke</td><td>0xDEF283BE</td><td>No</td></tr>
<tr><td>global_particle_firemediumsmoke_smoke_vehicle</td><td>0xE4D6C747</td><td>Yes</td></tr>
<tr><td>global_particle_firemediumsmoke_tree_box_flame</td><td>0x72AB2999</td><td>No</td></tr>
<tr><td>global_particle_firemediumsmoke_vehicle</td><td>0x0E54069D</td><td>Yes</td></tr>
<tr><td>global_particle_firemediumsmoke_vehicle_boat_box_flame</td><td>0xF2762404</td><td>Yes</td></tr>
<tr><td>global_particle_firemediumsmoke_vehicle_box_flame</td><td>0x602D65D7</td><td>Yes</td></tr>
<tr><td>global_particle_firesmall</td><td>0x608D7C59</td><td>No</td></tr>
<tr><td>global_particle_firesmall_infinite</td><td>0x1337775C</td><td>No</td></tr>
<tr><td>global_particle_firesmall_infinite_constant</td><td>0x28FD3D27</td><td>No</td></tr>
<tr><td>global_particle_firesmall_infinite_placeable</td><td>0xC6DB17EC</td><td>No</td></tr>
<tr><td>global_particle_firesmall_infinite_smoke</td><td>0x73B0889A</td><td>No</td></tr>
<tr><td>global_particle_firesmall_infinite_smoke_placeable</td><td>0xB31C02A6</td><td>No</td></tr>
<tr><td>global_particle_firesmall_smoke</td><td>0xAB377163</td><td>No</td></tr>
<tr><td>global_particle_firesmallsmoke</td><td>0x79F41D80</td><td>No</td></tr>
<tr><td>global_particle_firesmallsmoke_smoke</td><td>0xD9B3670E</td><td>No</td></tr>
<tr><td>global_particle_firesmallsmoke_smoke_vehicle</td><td>0xDA5F1597</td><td>Yes</td></tr>
<tr><td>global_particle_firesmallsmoke_vehicle</td><td>0xF46BFBAD</td><td>Yes</td></tr>
<tr><td>global_particle_firetiny</td><td>0x92CEB6AA</td><td>No</td></tr>
<tr><td>global_particle_firetiny_infinite</td><td>0x6FE47C31</td><td>No</td></tr>
<tr><td>global_particle_firetiny_infinite_placeable</td><td>0xDA1AC3ED</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopydwarf</td><td>0xE4AF6CDC</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopydwarf_LOD0</td><td>0x90E8C578</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopydwarf_LOD1</td><td>0xBAEB462D</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopymedium</td><td>0x9A24C9F5</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopymedium_LOD0</td><td>0x339C8FFF</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopymedium_LOD1</td><td>0xD199B722</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopymedium_static</td><td>0xB5C59F0A</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopymedium_static_smoke</td><td>0x63DA8038</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopysmall</td><td>0x6FFB154D</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopysmall_LOD0</td><td>0x80283657</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopysmall_LOD1</td><td>0x1E255D7A</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopytiny</td><td>0x5617466E</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopytiny_LOD0</td><td>0x29DA148E</td><td>No</td></tr>
<tr><td>global_particle_firetreecanopytiny_LOD1</td><td>0x0BDC23EB</td><td>No</td></tr>
<tr><td>global_particle_firetreelargesmoke</td><td>0xD223D588</td><td>No</td></tr>
<tr><td>global_particle_firetreemediumsmoke</td><td>0x1697661C</td><td>No</td></tr>
<tr><td>global_particle_firetreesmallsmoke</td><td>0x24986514</td><td>No</td></tr>
<tr><td>global_particle_firetreetrunkA</td><td>0xB5B9E4F7</td><td>No</td></tr>
<tr><td>global_particle_firetreetrunkB</td><td>0xCBBC4630</td><td>No</td></tr>
<tr><td>global_particle_firetreetrunkC</td><td>0x35BF2BA5</td><td>No</td></tr>
<tr><td>global_particle_firetreetrunkD</td><td>0x2BADD2C6</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke</td><td>0x02F6773F</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_airstrike</td><td>0x9C10F46C</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_fail</td><td>0xA1F75A3A</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_green</td><td>0x41675D0B</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_green_aristrike</td><td>0x1E31D18E</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_green_fail</td><td>0xF5894946</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_green_infinite</td><td>0xC18C0252</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_infinite</td><td>0xED6EA40E</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_lightblue</td><td>0x6EFE9D26</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_lightblue_airstrike</td><td>0xA36A90E5</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_lightblue_fail</td><td>0xEC738915</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_lightblue_infinite</td><td>0xC6BF9415</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_yellow</td><td>0xF8171566</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_yellow_airstrike</td><td>0x78E50725</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_yellow_fail</td><td>0xE1DBDE55</td><td>No</td></tr>
<tr><td>global_particle_flaresmoke_yellow_infinite</td><td>0xBA245355</td><td>No</td></tr>
<tr><td>global_particle_flotsum</td><td>0xEB453E60</td><td>No</td></tr>
<tr><td>global_particle_flotsum_ash</td><td>0xCA429139</td><td>No</td></tr>
<tr><td>global_particle_flotsum_birds</td><td>0x6BE8743D</td><td>No</td></tr>
<tr><td>global_particle_flotsum_bugs</td><td>0x647189BE</td><td>No</td></tr>
<tr><td>global_particle_flotsum_bugs_mosquito</td><td>0x04D89340</td><td>No</td></tr>
<tr><td>global_particle_flotsum_bugs_pirate</td><td>0x23CEDDB6</td><td>No</td></tr>
<tr><td>global_particle_flotsum_dandy</td><td>0xEBB461C9</td><td>No</td></tr>
<tr><td>global_particle_flotsum_dust</td><td>0xCE4504C3</td><td>No</td></tr>
<tr><td>global_particle_flotsum_dust_dark</td><td>0x60EBF5FE</td><td>No</td></tr>
<tr><td>global_particle_flotsum_dust_ground</td><td>0x5D39458F</td><td>No</td></tr>
<tr><td>global_particle_flotsum_leaves</td><td>0x41560073</td><td>No</td></tr>
<tr><td>global_particle_flotsum_papers</td><td>0x0961D706</td><td>No</td></tr>
<tr><td>global_particle_flotsum_smoke_ground</td><td>0x658F68B4</td><td>No</td></tr>
<tr><td>global_particle_fountian_a</td><td>0x35458D10</td><td>No</td></tr>
<tr><td>global_particle_fountian_b</td><td>0x1F432BD7</td><td>No</td></tr>
<tr><td>global_particle_fountian_drops_a</td><td>0xE146016B</td><td>No</td></tr>
<tr><td>global_particle_fountian_sheet_short_a</td><td>0xDC97F80B</td><td>No</td></tr>
<tr><td>global_particle_fountian_sheet_short_b</td><td>0x029A7274</td><td>No</td></tr>
<tr><td>global_particle_fountian_sheet_tall_a</td><td>0x5D77115A</td><td>No</td></tr>
<tr><td>global_particle_fountian_sheet_tall_b</td><td>0xBF7E6765</td><td>No</td></tr>
<tr><td>global_particle_fountian_sheet_tall_c</td><td>0x557B81F0</td><td>No</td></tr>
<tr><td>global_particle_fountian_splash_a</td><td>0xD2EC0E42</td><td>No</td></tr>
<tr><td>global_particle_grenadeexplosion</td><td>0x2440B40B</td><td>No</td></tr>
<tr><td>global_particle_gritexplosion</td><td>0x314341D1</td><td>No</td></tr>
<tr><td>global_particle_hedge_cover</td><td>0xCE8D144F</td><td>No</td></tr>
<tr><td>global_particle_hedge_cover_fire</td><td>0xF5481F8A</td><td>No</td></tr>
<tr><td>global_particle_impact_blood</td><td>0xF9AB154B</td><td>No</td></tr>
<tr><td>global_particle_impact_brick</td><td>0xFB787A44</td><td>No</td></tr>
<tr><td>global_particle_impact_brick_nodamage</td><td>0x6448B461</td><td>No</td></tr>
<tr><td>global_particle_impact_brick_point</td><td>0x1EE5B78B</td><td>No</td></tr>
<tr><td>global_particle_impact_brickplaster_nodamage</td><td>0x9DC7132A</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_blood</td><td>0x99905F7C</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_brick</td><td>0x79176617</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_dirt</td><td>0x3747110B</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_glass</td><td>0x4F4CAF70</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_leaves</td><td>0xDD533E50</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_metal</td><td>0xEDA838E5</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_metal_flare</td><td>0xC410BEA4</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_stone</td><td>0xFBA53CCB</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_water</td><td>0x58A40C49</td><td>No</td></tr>
<tr><td>global_particle_impact_bullet_wood</td><td>0xEC2E1CE7</td><td>No</td></tr>
<tr><td>global_particle_impact_concrete</td><td>0xC99D2D00</td><td>No</td></tr>
<tr><td>global_particle_impact_concrete_nodamage</td><td>0xBF5270FD</td><td>No</td></tr>
<tr><td>global_particle_impact_concrete_point</td><td>0x59938797</td><td>No</td></tr>
<tr><td>global_particle_impact_dirt</td><td>0x14CE41AA</td><td>No</td></tr>
<tr><td>global_particle_impact_dirt_point</td><td>0x41B379D5</td><td>No</td></tr>
<tr><td>global_particle_impact_generic_nodamage</td><td>0xEA28E571</td><td>No</td></tr>
<tr><td>global_particle_impact_glass</td><td>0x51CCB517</td><td>No</td></tr>
<tr><td>global_particle_impact_glass_nodamage</td><td>0x3C0239E4</td><td>No</td></tr>
<tr><td>global_particle_impact_leaves</td><td>0x94171375</td><td>No</td></tr>
<tr><td>global_particle_impact_metal</td><td>0x9386E236</td><td>No</td></tr>
<tr><td>global_particle_impact_metal_nodamage</td><td>0x279A7267</td><td>No</td></tr>
<tr><td>global_particle_impact_metal_nodamage_flare</td><td>0x43D6AC22</td><td>No</td></tr>
<tr><td>global_particle_impact_metal_point</td><td>0x6A97ADC1</td><td>No</td></tr>
<tr><td>global_particle_impact_rocket_weakpoint</td><td>0x2C6E80E2</td><td>No</td></tr>
<tr><td>global_particle_impact_rpg_glass</td><td>0x91BAFC77</td><td>No</td></tr>
<tr><td>global_particle_impact_slide_brick</td><td>0xE5889AD6</td><td>No</td></tr>
<tr><td>global_particle_impact_slide_dirt</td><td>0xE8E827DC</td><td>No</td></tr>
<tr><td>global_particle_impact_slide_leaves</td><td>0xEDBB4783</td><td>No</td></tr>
<tr><td>global_particle_impact_slide_stone</td><td>0xABFD5BDA</td><td>No</td></tr>
<tr><td>global_particle_impact_stone</td><td>0x5D7A9344</td><td>No</td></tr>
<tr><td>global_particle_impact_stone_nodamage</td><td>0x07066F61</td><td>No</td></tr>
<tr><td>global_particle_impact_sweat</td><td>0x1567287F</td><td>No</td></tr>
<tr><td>global_particle_impact_water</td><td>0x73FD2F8A</td><td>No</td></tr>
<tr><td>global_particle_impact_wood</td><td>0xEC86D392</td><td>No</td></tr>
<tr><td>global_particle_impact_wood_nodamage</td><td>0x773B3573</td><td>No</td></tr>
<tr><td>global_particle_industrial_fire_infinite</td><td>0xD60D99D3</td><td>No</td></tr>
<tr><td>global_particle_industrial_firesmoke_infinite</td><td>0x0610E7B2</td><td>No</td></tr>
<tr><td>global_particle_industrial_smoke_infinite</td><td>0xA2227E4E</td><td>No</td></tr>
<tr><td>global_particle_industrial_smokesmall_infinite</td><td>0x09CB1077</td><td>No</td></tr>
<tr><td>global_particle_monstertruck_turbo</td><td>0x9919B4C6</td><td>Yes</td></tr>
<tr><td>global_particle_muzzleflash</td><td>0x2E59B6BB</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_25mm</td><td>0xE738A8AF</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_AA</td><td>0x025925B0</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_artillery</td><td>0x1433A0E8</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_blue</td><td>0x341B47C6</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_grenadelauncher</td><td>0x579E9394</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_handgun</td><td>0x5A1F98BD</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_jet</td><td>0xBA8DBF73</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_MG</td><td>0x1E98062A</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_rpg</td><td>0x00F0790B</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_SAM_amx30</td><td>0x157AAB71</td><td>Yes</td></tr>
<tr><td>global_particle_muzzleflash_shotgun</td><td>0xA45CF97C</td><td>No</td></tr>
<tr><td>global_particle_muzzleflash_tank</td><td>0xDE8D74DA</td><td>Yes</td></tr>
<tr><td>global_particle_muzzleflash_vulcan</td><td>0x0CAA3B0B</td><td>No</td></tr>
<tr><td>global_particle_rotorwash</td><td>0xC05BD005</td><td>No</td></tr>
<tr><td>global_particle_rotorwash_water</td><td>0xC78204C1</td><td>No</td></tr>
<tr><td>global_particle_shatteringGlass_chandelier</td><td>0xDBE087CF</td><td>No</td></tr>
<tr><td>global_particle_shatteringGlass_vehicle</td><td>0xD1AD89DA</td><td>Yes</td></tr>
<tr><td>global_particle_shell</td><td>0x867C9756</td><td>No</td></tr>
<tr><td>global_particle_shellAA</td><td>0x1ECC57AC</td><td>No</td></tr>
<tr><td>global_particle_shellAA_large</td><td>0x874AD95C</td><td>No</td></tr>
<tr><td>global_particle_shellgrenade</td><td>0xA64EC344</td><td>No</td></tr>
<tr><td>global_particle_shellhandgun</td><td>0xE86E5149</td><td>No</td></tr>
<tr><td>global_particle_shellmg</td><td>0x01E51916</td><td>No</td></tr>
<tr><td>global_particle_shellmissile</td><td>0x940A359E</td><td>No</td></tr>
<tr><td>global_particle_shellrocket</td><td>0xA89FC596</td><td>No</td></tr>
<tr><td>global_particle_shellrpg</td><td>0x2D4A6587</td><td>No</td></tr>
<tr><td>global_particle_shellsam</td><td>0xD4DD31D7</td><td>No</td></tr>
<tr><td>global_particle_shellshotgun</td><td>0x55F1C5E8</td><td>No</td></tr>
<tr><td>global_particle_shellsmall</td><td>0xF7FA615F</td><td>No</td></tr>
<tr><td>global_particle_smoke_ac_large_infinite</td><td>0x3A737049</td><td>No</td></tr>
<tr><td>global_particle_smoke_ac_small_infinite</td><td>0xC38B1511</td><td>No</td></tr>
<tr><td>global_particle_smoke_heli_tailrotor</td><td>0xC389EFF5</td><td>Yes</td></tr>
<tr><td>global_particle_smokeblack</td><td>0xC1BEFB24</td><td>No</td></tr>
<tr><td>global_particle_smokeblack_infinite</td><td>0x4F5EC3AF</td><td>No</td></tr>
<tr><td>global_particle_smokeblack_tank</td><td>0x3EBA6E4F</td><td>Yes</td></tr>
<tr><td>global_particle_smokeblackwide</td><td>0x7E9B9B41</td><td>No</td></tr>
<tr><td>global_particle_smokeblackwide_vehicle</td><td>0x95E10064</td><td>Yes</td></tr>
<tr><td>global_particle_smokemedium_infinite</td><td>0xD240B36D</td><td>No</td></tr>
<tr><td>global_particle_sparks_rpg_decal</td><td>0xC325D0CC</td><td>No</td></tr>
<tr><td>global_particle_sparkslarge</td><td>0x41F7E4A7</td><td>No</td></tr>
<tr><td>global_particle_sparksmedium</td><td>0x0D4B1F07</td><td>No</td></tr>
<tr><td>global_particle_splash_dive</td><td>0x1BF7AC8A</td><td>No</td></tr>
<tr><td>global_particle_splash_huge</td><td>0x4720A979</td><td>No</td></tr>
<tr><td>global_particle_splash_lrg</td><td>0x18CBDA81</td><td>No</td></tr>
<tr><td>global_particle_splash_lrg_vehicle</td><td>0x2A7F4FA4</td><td>Yes</td></tr>
<tr><td>global_particle_splash_med</td><td>0x4E210C3E</td><td>No</td></tr>
<tr><td>global_particle_splash_sml</td><td>0x79041D04</td><td>No</td></tr>
<tr><td>global_particle_teargas</td><td>0xD6B6F657</td><td>No</td></tr>
<tr><td>global_particle_test2</td><td>0x56D9F6FA</td><td>No</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green</td><td>0x7D7470C4</td><td>No</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_fire</td><td>0x26240627</td><td>No</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_large</td><td>0x651ADB14</td><td>No</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_large_fire</td><td>0xF6ECDD57</td><td>No</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_small</td><td>0xC8AF6E10</td><td>No</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_small_fire</td><td>0x472B5433</td><td>No</td></tr>
<tr><td>global_particle_tree_destruction_leaves_palm</td><td>0x984BE1BF</td><td>No</td></tr>
<tr><td>global_particle_veh_exhaust_car</td><td>0x06A262B1</td><td>Yes</td></tr>
<tr><td>global_particle_veh_exhaust_tank</td><td>0x74FE93B9</td><td>Yes</td></tr>
<tr><td>global_particle_veh_smoke_asphalt</td><td>0x49402063</td><td>Yes</td></tr>
<tr><td>global_particle_veh_smoke_brakes</td><td>0xB89DCE16</td><td>Yes</td></tr>
<tr><td>global_particle_veh_smoke_dust</td><td>0x52B3F712</td><td>Yes</td></tr>
<tr><td>global_particle_veh_smoke_grass</td><td>0x078B3B78</td><td>Yes</td></tr>
<tr><td>global_particle_veh_smoke_rock</td><td>0x250CEEF1</td><td>Yes</td></tr>
<tr><td>global_particle_water_spray_fall_pmc</td><td>0x93C07918</td><td>No</td></tr>
<tr><td>global_particle_water_spray_pmc</td><td>0x9AFBE3BE</td><td>No</td></tr>
<tr><td>global_particle_waterfall_bottom</td><td>0x4C8B89AC</td><td>No</td></tr>
<tr><td>global_particle_waterfall_bottom_small</td><td>0x7EAD8BD8</td><td>No</td></tr>
<tr><td>global_particle_waterfall_bottom_tiny</td><td>0x57F582AD</td><td>No</td></tr>
<tr><td>global_particle_waterfall_smoke</td><td>0x385341F8</td><td>No</td></tr>
<tr><td>global_particle_waterfall_smoke_large</td><td>0x81361078</td><td>No</td></tr>
<tr><td>global_particle_waterfall_wall</td><td>0xFFB152A9</td><td>No</td></tr>
<tr><td>global_particle_waterfall_wall_small</td><td>0x28B0D431</td><td>No</td></tr>
<tr><td>global_ribbon_artillery</td><td>0x1CBC91C0</td><td>No</td></tr>
<tr><td>global_ribbon_artillery_daisy</td><td>0xA686E2FB</td><td>No</td></tr>
<tr><td>global_ribbon_artillery_moab</td><td>0x6A5FE1FA</td><td>No</td></tr>
<tr><td>global_ribbon_artillery_slow</td><td>0xE95D53F4</td><td>No</td></tr>
<tr><td>global_ribbon_grenade</td><td>0xA2CDC550</td><td>No</td></tr>
<tr><td>global_ribbon_grenadelauncher</td><td>0x1482586C</td><td>No</td></tr>
<tr><td>global_ribbon_plane_contrail</td><td>0xAD2E0F9F</td><td>No</td></tr>
<tr><td>global_ribbon_RPG</td><td>0xDA30DE43</td><td>No</td></tr>
<tr><td>global_strategic_missile_contrail</td><td>0x1EC9F481</td><td>No</td></tr>
<tr><td>GR Defender (AA)</td><td>0xFF50CA66</td><td>No</td></tr>
<tr><td>GR Defender (AT)</td><td>0x15AECCF9</td><td>No</td></tr>
<tr><td>GR Defender (AT) (Window Spawner)</td><td>0x502D026E</td><td>No</td></tr>
<tr><td>GR Defender (MG)</td><td>0x6C3D798C</td><td>No</td></tr>
<tr><td>GR Defender (rifle)</td><td>0xDAE42A40</td><td>No</td></tr>
<tr><td>Grapple</td><td>0x25F753CA</td><td>No</td></tr>
<tr><td>Grapple Hook</td><td>0xB3AC7513</td><td>No</td></tr>
<tr><td>Grass01</td><td>0x6EE5BA88</td><td>No</td></tr>
<tr><td>Grass01_PMC</td><td>0x5EB991F1</td><td>No</td></tr>
<tr><td>Grass01_Short</td><td>0x143B218F</td><td>No</td></tr>
<tr><td>Grass01_swamp</td><td>0x2513CF9D</td><td>No</td></tr>
<tr><td>Grass01_Tall</td><td>0x8EAD531E</td><td>No</td></tr>
<tr><td>Grass01_TallSwamp</td><td>0xCCE17C62</td><td>No</td></tr>
<tr><td>GrassJungle</td><td>0x96E15D32</td><td>No</td></tr>
<tr><td>GrassThick</td><td>0x3BE92EA4</td><td>No</td></tr>
<tr><td>GrassYellow</td><td>0x423C7291</td><td>No</td></tr>
<tr><td>Grassyellowgreen</td><td>0xC61E7E9E</td><td>No</td></tr>
<tr><td>Grenade</td><td>0x496D5A75</td><td>No</td></tr>
<tr><td>Grenade (AI)</td><td>0x36B18E60</td><td>No</td></tr>
<tr><td>Grenade Launcher</td><td>0x06332D9F</td><td>No</td></tr>
<tr><td>Grenade Launcher PEP</td><td>0x7200B6C8</td><td>No</td></tr>
<tr><td>Grenade Launcher Projectile</td><td>0x188B0408</td><td>No</td></tr>
<tr><td>Grenade Launcher Projectile PEP</td><td>0xF50ECA0F</td><td>No</td></tr>
<tr><td>Grenade MG Projectile</td><td>0x4254D63C</td><td>No</td></tr>
<tr><td>Grenade Projectile</td><td>0xC4817A02</td><td>No</td></tr>
<tr><td>Grenade Projectile (AI)</td><td>0x42E5A8F1</td><td>No</td></tr>
<tr><td>Guerilla</td><td>0xB10D73CE</td><td>No</td></tr>
<tr><td>Guerilla Boss</td><td>0xFB56A321</td><td>No</td></tr>
<tr><td>Guerilla Elite Soldier</td><td>0x0FA5ED09</td><td>No</td></tr>
<tr><td>Guerilla Heavy</td><td>0x1AB98DEF</td><td>No</td></tr>
<tr><td>Guerilla Heavy (Light MG)</td><td>0x954BECF8</td><td>No</td></tr>
<tr><td>Guerilla Heavy (RPG)</td><td>0x90468595</td><td>No</td></tr>
<tr><td>Guerilla Officer</td><td>0x333D82A4</td><td>No</td></tr>
<tr><td>Guerilla Officer (Female)</td><td>0x96F68841</td><td>No</td></tr>
<tr><td>Guerilla Prisoner</td><td>0xFDD26F2E</td><td>No</td></tr>
<tr><td>Guerilla Soldier</td><td>0x6C42D8C8</td><td>No</td></tr>
<tr><td>Guerilla Soldier (Female)</td><td>0xB5DE8E35</td><td>No</td></tr>
<tr><td>Guerilla Soldier (God)</td><td>0x4EAC3517</td><td>No</td></tr>
<tr><td>Guerilla Soldier B</td><td>0x388DED42</td><td>No</td></tr>
<tr><td>Guerilla Soldier B (Female)</td><td>0x2FBF334F</td><td>No</td></tr>
<tr><td>Guerilla Starter 01</td><td>0xB2B19FD4</td><td>No</td></tr>
<tr><td>Guerilla Starter 02</td><td>0x8CAF256B</td><td>No</td></tr>
<tr><td>Guerilla Starter 03</td><td>0xAAAD160E</td><td>No</td></tr>
<tr><td>Guerilla Starter 04</td><td>0xB4BE6EED</td><td>No</td></tr>
<tr><td>Guerilla Starter 05</td><td>0x8ABBEE38</td><td>No</td></tr>
<tr><td>Guerilla Starters</td><td>0x4EEA8396</td><td>No</td></tr>
<tr><td>Guerilla Tank Commander</td><td>0xA20BDCE8</td><td>Yes</td></tr>
<tr><td>Guerilla Worker</td><td>0xDCE7940C</td><td>No</td></tr>
<tr><td>Gunship Shell</td><td>0xB5434279</td><td>Yes</td></tr>
<tr><td>Guntruck (OC)</td><td>0x8730B849</td><td>Yes</td></tr>
<tr><td>Guntruck (OC) (Driver)</td><td>0x1776F2E4</td><td>Yes</td></tr>
<tr><td>Guntruck (OC) (Full)</td><td>0x6D9A82A3</td><td>Yes</td></tr>
<tr><td>Guntruck (OC) (Gunners Only)</td><td>0xC8628708</td><td>Yes</td></tr>
<tr><td>Guntruck (OC) (SemiFull)</td><td>0x47036AC1</td><td>Yes</td></tr>
<tr><td>GuntruckOC_Driver</td><td>0x07CEED75</td><td>Yes</td></tr>
<tr><td>GurDbSpawner</td><td>0x7C80110D</td><td>No</td></tr>
<tr><td>GurDbSpawner (Squad Full AT)</td><td>0x81FE6838</td><td>No</td></tr>
<tr><td>GurDbSpawner (Squad Half AT)</td><td>0x792FB590</td><td>No</td></tr>
<tr><td>GurDbSpawner (Squad Quarter AT)</td><td>0x608DA4BD</td><td>No</td></tr>
<tr><td>GurDbSpawner (Squad)</td><td>0x01EB03A6</td><td>No</td></tr>
<tr><td>GurHq_Interior</td><td>0x50916633</td><td>No</td></tr>
<tr><td>GurPedTraffic</td><td>0x0663B41F</td><td>No</td></tr>
<tr><td>GurVehTraffic</td><td>0x4FD073D1</td><td>No</td></tr>
<tr><td>HangarTest01</td><td>0x7D7932A9</td><td>No</td></tr>
<tr><td>HE Autocannon Shell</td><td>0x9E32F51C</td><td>No</td></tr>
<tr><td>HE Autocannon Shell (CH)</td><td>0x1D6587CA</td><td>No</td></tr>
<tr><td>Health Pickup</td><td>0xB8580455</td><td>No</td></tr>
<tr><td>Heavy MG Bullet</td><td>0x22982FBE</td><td>No</td></tr>
<tr><td>Heavy MG Bullet (AL)</td><td>0xF2677BFA</td><td>No</td></tr>
<tr><td>Heavy MG Bullet (CH)</td><td>0xD4C2BF04</td><td>No</td></tr>
<tr><td>Heavy MG Bullet (GR)</td><td>0x8A7E6992</td><td>No</td></tr>
<tr><td>HeavyPropTemplate</td><td>0x7C86FBD7</td><td>No</td></tr>
<tr><td>Helicopter</td><td>0x800DC82E</td><td>Yes</td></tr>
<tr><td>Helicopter_Hijack_Entrance</td><td>0x9F874D9E</td><td>Yes</td></tr>
<tr><td>HeliList_Caracas_Act1_A</td><td>0x582F4DB8</td><td>Yes</td></tr>
<tr><td>HeliList_Caracas_Act2_ALL</td><td>0xF3A82FDB</td><td>Yes</td></tr>
<tr><td>HeliList_Caracas_Act3ALL</td><td>0x552BB387</td><td>Yes</td></tr>
<tr><td>HeliList_Caracas_Act3CHI</td><td>0x50E738C8</td><td>Yes</td></tr>
<tr><td>HeliList_Cumana_Act1_CHI</td><td>0xF3809ADE</td><td>Yes</td></tr>
<tr><td>HeliList_Cumana_Act2_CHI</td><td>0x858EDC6D</td><td>Yes</td></tr>
<tr><td>HeliList_JungleMtn_Act1</td><td>0x254B4DAC</td><td>Yes</td></tr>
<tr><td>HeliList_Mar_City_Act1_A</td><td>0xCF63A97C</td><td>Yes</td></tr>
<tr><td>HeliList_Mar_City_Act2_A</td><td>0xA219969F</td><td>Yes</td></tr>
<tr><td>HeliList_Mar_City_Act3_A</td><td>0x30C61E5A</td><td>Yes</td></tr>
<tr><td>HeliList_Merida_Act1_A</td><td>0x77024A0A</td><td>Yes</td></tr>
<tr><td>HeliList_Merida_Act2_A</td><td>0x9F92D6F9</td><td>Yes</td></tr>
<tr><td>Hero</td><td>0x51728909</td><td>No</td></tr>
<tr><td>Hibernation Control (Building Huge)</td><td>0xBF977E5B</td><td>No</td></tr>
<tr><td>Hibernation Control (Building Large)</td><td>0xA6C02A91</td><td>No</td></tr>
<tr><td>Hibernation Control (Building Medium)</td><td>0x1272156B</td><td>No</td></tr>
<tr><td>Hibernation Control (Building Small)</td><td>0x903C1895</td><td>No</td></tr>
<tr><td>Hibernation Control (Building Static Small)</td><td>0x74CA0025</td><td>No</td></tr>
<tr><td>Hibernation Control (Building Streamer)</td><td>0x3E1E0B7F</td><td>No</td></tr>
<tr><td>Hibernation Control (Building Super)</td><td>0x9CD0BE09</td><td>No</td></tr>
<tr><td>Hibernation Control (Effects Huge)</td><td>0x23712EBB</td><td>No</td></tr>
<tr><td>Hibernation Control (Effects Large)</td><td>0x01DA5C71</td><td>No</td></tr>
<tr><td>Hibernation Control (Effects Medium)</td><td>0x1226B0CB</td><td>No</td></tr>
<tr><td>Hibernation Control (Effects Small)</td><td>0xABFE3D75</td><td>No</td></tr>
<tr><td>Hibernation Control (Effects Standard)</td><td>0xC2F16CC5</td><td>No</td></tr>
<tr><td>Hibernation Control (Effects Super)</td><td>0x5E9D7169</td><td>No</td></tr>
<tr><td>Hibernation Control (Environmental Huge)</td><td>0x842A9E89</td><td>No</td></tr>
<tr><td>Hibernation Control (Environmental Large)</td><td>0xA35F2AEF</td><td>No</td></tr>
<tr><td>Hibernation Control (Environmental Medium)</td><td>0x3B6CE98D</td><td>No</td></tr>
<tr><td>Hibernation Control (Environmental Small)</td><td>0x715BB747</td><td>No</td></tr>
<tr><td>Hibernation Control (Environmental Super)</td><td>0x23937BDF</td><td>No</td></tr>
<tr><td>Hibernation Control (Environmental Tiny)</td><td>0x9E2783EC</td><td>No</td></tr>
<tr><td>Hibernation Control (Foliage Scrub Brush Assets)</td><td>0x40ED35AB</td><td>No</td></tr>
<tr><td>Hibernation Control (Prop Huge)</td><td>0x11E18E88</td><td>No</td></tr>
<tr><td>Hibernation Control (Prop Large)</td><td>0x0DC7C248</td><td>No</td></tr>
<tr><td>Hibernation Control (Prop Medium)</td><td>0xD7226CF8</td><td>No</td></tr>
<tr><td>Hibernation Control (Prop small)</td><td>0x048DCDB0</td><td>No</td></tr>
<tr><td>Hibernation Control (Prop Super)</td><td>0xA682B7D4</td><td>No</td></tr>
<tr><td>Hibernation Control (Vehicle Helicopter)</td><td>0xD6D598A3</td><td>Yes</td></tr>
<tr><td>Hibernation Control (Vehicle Immobile Ship)</td><td>0x6E396D12</td><td>Yes</td></tr>
<tr><td>Hibernation Control (Vehicle LargeA)</td><td>0x9B0967A8</td><td>No</td></tr>
<tr><td>Hibernation Control (Vehicle LargeB)</td><td>0x097E2261</td><td>No</td></tr>
<tr><td>Hibernation Control (Vehicle Medium)</td><td>0x35E994E5</td><td>No</td></tr>
<tr><td>Hibernation Control (Vehicle Plane)</td><td>0x022C183A</td><td>No</td></tr>
<tr><td>Hibernation Control (Vehicle Small) 0</td><td>0x05451017</td><td>No</td></tr>
<tr><td>Hibernation Control (Vehicle Tiny)</td><td>0xFA430C24</td><td>No</td></tr>
<tr><td>Hibernation Control (Vehicle Wheels)</td><td>0xDE606342</td><td>No</td></tr>
<tr><td>HighDensityPedTraffic</td><td>0x782C6BF9</td><td>No</td></tr>
<tr><td>HighRoad</td><td>0x59FE080B</td><td>No</td></tr>
<tr><td>HMMWV (4 door base)</td><td>0x67D16052</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (50Cal)</td><td>0x37905F6B</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (50Cal) (Driver)</td><td>0x738B3286</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (50Cal) (DriverGunner)</td><td>0x8DD3AE5D</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (50Cal) (Full)</td><td>0x2E06295D</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (base)</td><td>0x91F9A7C7</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (GL)</td><td>0x80B1B641</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (GL) (Driver)</td><td>0xD175755C</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (GL) (DriverGunner)</td><td>0xF8B8D143</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (GL) (Full)</td><td>0x35921ACB</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (TOW)</td><td>0x9B70EDF2</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (TOW) (Driver)</td><td>0x39BB2F99</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (TOW) (DriverGunner)</td><td>0xE377604A</td><td>No</td></tr>
<tr><td>HMMWV (Armored) (TOW) (Full)</td><td>0x4BFDFBBE</td><td>No</td></tr>
<tr><td>HMMWV (Avenger)</td><td>0xAAB4BBC1</td><td>No</td></tr>
<tr><td>HMMWV (Avenger) (Driver)</td><td>0x0273ADDC</td><td>No</td></tr>
<tr><td>HMMWV (Avenger) (DriverGunner)</td><td>0xAB0145C3</td><td>No</td></tr>
<tr><td>HMMWV (Avenger) (Full)</td><td>0x50027F4B</td><td>No</td></tr>
<tr><td>HMMWV (base)</td><td>0x2CC31BFE</td><td>No</td></tr>
<tr><td>HMMWV (Softtop)</td><td>0x1D5BDF68</td><td>No</td></tr>
<tr><td>HMMWV (Softtop) (Driver)</td><td>0x4A8DFEC7</td><td>No</td></tr>
<tr><td>HMMWV (Softtop) (Full)</td><td>0x266B760C</td><td>No</td></tr>
<tr><td>HMMWV_Avenger_Driver</td><td>0xD3AC574E</td><td>No</td></tr>
<tr><td>HMMWV_Driver</td><td>0xFEFE9D0B</td><td>No</td></tr>
<tr><td>HouseSpawn</td><td>0x1115537C</td><td>No</td></tr>
<tr><td>Huangfeng</td><td>0x9119EDA6</td><td>Yes</td></tr>
<tr><td>Huangfeng (Driver)</td><td>0xF21B7ABD</td><td>Yes</td></tr>
<tr><td>Huangfeng (Jammer)</td><td>0x87BD19FF</td><td>Yes</td></tr>
<tr><td>Huangfeng (Jammer) (Driver)</td><td>0x7A4B1D6A</td><td>Yes</td></tr>
<tr><td>HuangFeng_Driver</td><td>0xD1D13A1F</td><td>Yes</td></tr>
<tr><td>Human</td><td>0xAD431BF0</td><td>No</td></tr>
<tr><td>Human Heavy MG</td><td>0x988C5BAB</td><td>No</td></tr>
<tr><td>Humvee (Cargo)</td><td>0x8EE207C2</td><td>Yes</td></tr>
<tr><td>Hunting Pistol</td><td>0x3CD65BF3</td><td>No</td></tr>
<tr><td>Hunting Pistol Bullet</td><td>0x67672885</td><td>No</td></tr>
<tr><td>HVT</td><td>0xA3BAD77D</td><td>No</td></tr>
<tr><td>impact</td><td>0xA9FC5F87</td><td>No</td></tr>
<tr><td>Impact (base)</td><td>0x08DD0349</td><td>No</td></tr>
<tr><td>Impact (base) (Driver)</td><td>0x7E4223E4</td><td>No</td></tr>
<tr><td>Impact (base) (Driver) (Civ Rich female)</td><td>0xFE035BD9</td><td>No</td></tr>
<tr><td>Impact (base) (Driver) (Civ Rich male)</td><td>0x110889BC</td><td>No</td></tr>
<tr><td>Impact (sut)</td><td>0xE9386912</td><td>No</td></tr>
<tr><td>Impact (sut) (Driver)</td><td>0x0B42BFB9</td><td>No</td></tr>
<tr><td>Impact (sut) (Driver) (Civ Rich female)</td><td>0xE381D808</td><td>No</td></tr>
<tr><td>Impact (sut) (Driver) (Civ Rich male)</td><td>0xA583A479</td><td>No</td></tr>
<tr><td>Impact_Driver</td><td>0xE1F525E4</td><td>No</td></tr>
<tr><td>ImpactSUT_Driver</td><td>0xE8F330F6</td><td>No</td></tr>
<tr><td>International (subfaction)</td><td>0x73CEE4D6</td><td>No</td></tr>
<tr><td>Intersection</td><td>0xB69CE2C6</td><td>No</td></tr>
<tr><td>Jammer</td><td>0x960171AD</td><td>No</td></tr>
<tr><td>Jen</td><td>0xB06FC6E8</td><td>No</td></tr>
<tr><td>JenChickensuit</td><td>0xC3FD0436</td><td>No</td></tr>
<tr><td>jenupgrade1</td><td>0xDD2CA3B1</td><td>No</td></tr>
<tr><td>jenupgrade2</td><td>0x5B251B46</td><td>No</td></tr>
<tr><td>jenupgrade3</td><td>0x7D278F63</td><td>No</td></tr>
<tr><td>JenV2</td><td>0xBE9D5CB0</td><td>No</td></tr>
<tr><td>JenV3</td><td>0x28A04225</td><td>No</td></tr>
<tr><td>JenV4</td><td>0x1E8EE946</td><td>No</td></tr>
<tr><td>JenV5</td><td>0x40915D63</td><td>No</td></tr>
<tr><td>Jetski (Base)</td><td>0x37257397</td><td>No</td></tr>
<tr><td>Jetski (Civ)</td><td>0xA4D1B14E</td><td>No</td></tr>
<tr><td>Jetski (Civ) (Driver)</td><td>0x74C91EE5</td><td>No</td></tr>
<tr><td>Jetski (Civ) (Driver) (Civ Beach A Female)</td><td>0x119ED3DC</td><td>No</td></tr>
<tr><td>Jetski (Civ) (Driver) (Civ Beach B Female)</td><td>0x4C55C413</td><td>No</td></tr>
<tr><td>Jetski (Civ) (Driver) (Civ Beach C Female)</td><td>0x44B20C8A</td><td>No</td></tr>
<tr><td>Jetski (Civ) (Driver) (Civ Beach D Female)</td><td>0x97F32909</td><td>No</td></tr>
<tr><td>Jetski (PR)</td><td>0x19AE3DA4</td><td>No</td></tr>
<tr><td>Jetski (PR) (Driver)</td><td>0xC431A403</td><td>No</td></tr>
<tr><td>Jetski_Driver</td><td>0x8E0E2052</td><td>No</td></tr>
<tr><td>JetTest</td><td>0xE9037B6E</td><td>No</td></tr>
<tr><td>jnilsson</td><td>0xBEA0F5B3</td><td>No</td></tr>
<tr><td>Journalist A (Female)</td><td>0xA8C22B68</td><td>No</td></tr>
<tr><td>Journalist A (Male)</td><td>0xE6AD9CD9</td><td>No</td></tr>
<tr><td>Journalist B (Female)</td><td>0x07BE10B5</td><td>No</td></tr>
<tr><td>Journalist B (Male)</td><td>0x9DBF9648</td><td>No</td></tr>
<tr><td>Joyce Wheelchair</td><td>0x12A4F45F</td><td>No</td></tr>
<tr><td>Jungle Elite</td><td>0x6DE626BF</td><td>No</td></tr>
<tr><td>JustPhoenix</td><td>0x1D1A6CC8</td><td>No</td></tr>
<tr><td>Ka29b</td><td>0xE96A0E24</td><td>Yes</td></tr>
<tr><td>Ka29b (base)</td><td>0x9E26024C</td><td>Yes</td></tr>
<tr><td>Ka29b (bomber)</td><td>0xCB2041FA</td><td>Yes</td></tr>
<tr><td>Ka29b (Delivery)</td><td>0xB25169AD</td><td>Yes</td></tr>
<tr><td>Ka29b (Driver)</td><td>0xF3D88D83</td><td>Yes</td></tr>
<tr><td>Ka29b (DriverGunner)</td><td>0x008776D4</td><td>Yes</td></tr>
<tr><td>Ka29b (Ewan)</td><td>0x92265E0A</td><td>Yes</td></tr>
<tr><td>Ka29b (Extraction)</td><td>0xFF914EF0</td><td>Yes</td></tr>
<tr><td>Ka29b (Full)</td><td>0x0DB71EB0</td><td>Yes</td></tr>
<tr><td>Ka29b (pursuit)</td><td>0x0BE78C3B</td><td>Yes</td></tr>
<tr><td>Kodiak Ridgeline (Driver) (Mechanic (male))</td><td>0x1988CF23</td><td>No</td></tr>
<tr><td>L300</td><td>0x7B978FE6</td><td>No</td></tr>
<tr><td>L300 (base)</td><td>0x1B061B9A</td><td>No</td></tr>
<tr><td>L300 (Driver)</td><td>0x4D90717D</td><td>No</td></tr>
<tr><td>L300 (Driver) (Cartel)</td><td>0x64834415</td><td>No</td></tr>
<tr><td>L300 (Driver) (Civ Business B Male)</td><td>0x4AF6A2D7</td><td>No</td></tr>
<tr><td>L300 (Driver) (Civ Business female)</td><td>0x7AE87B2C</td><td>No</td></tr>
<tr><td>L300 (Driver) (Civ Business Male)</td><td>0x2C34B9BD</td><td>No</td></tr>
<tr><td>L300 (Driver) (Civ Rich Female)</td><td>0x464A98CC</td><td>No</td></tr>
<tr><td>L300 (Driver) (Civ Rich Male)</td><td>0xC4548BDD</td><td>No</td></tr>
<tr><td>L300 (Driver) (OC)</td><td>0xC9A2D430</td><td>No</td></tr>
<tr><td>L300 (Fling Backward)</td><td>0x3901E608</td><td>No</td></tr>
<tr><td>L300 (Fling Forward)</td><td>0x14692BF8</td><td>No</td></tr>
<tr><td>L300 (Racing)</td><td>0x9B7F14BD</td><td>No</td></tr>
<tr><td>L300 (Racing) (Driver)</td><td>0x2F755B48</td><td>No</td></tr>
<tr><td>L300 (Racing) (Driver) (Civ Motorcycle male)</td><td>0x3B3AEE71</td><td>Yes</td></tr>
<tr><td>L300 (Racing) (Driver) (OC)</td><td>0xA0F74AA7</td><td>No</td></tr>
<tr><td>L300 (Racing) (Long Hibernation)</td><td>0x40F244BF</td><td>No</td></tr>
<tr><td>L300_Driver</td><td>0xB5E86E5F</td><td>No</td></tr>
<tr><td>L300Racing_Driver</td><td>0x47FEB889</td><td>No</td></tr>
<tr><td>Ladder Seat (Bottom A)</td><td>0x7DDE7EAD</td><td>No</td></tr>
<tr><td>Ladder Seat (Bottom B)</td><td>0xEEF2D044</td><td>No</td></tr>
<tr><td>Ladder Seat (Bottom C)</td><td>0x7B72778B</td><td>No</td></tr>
<tr><td>Ladder Seat (Bottom D)</td><td>0x9BBBF222</td><td>No</td></tr>
<tr><td>Ladder Seat (Bottom E)</td><td>0xA8DA33A9</td><td>No</td></tr>
<tr><td>Ladder Seat (Bottom F)</td><td>0x3AB52AD0</td><td>No</td></tr>
<tr><td>Ladder Seat (Bottom G)</td><td>0x57D38587</td><td>No</td></tr>
<tr><td>Ladder Seat (Bottom H)</td><td>0x798AA2CE</td><td>No</td></tr>
<tr><td>Ladder Seat (Bottom)</td><td>0xE17233BE</td><td>No</td></tr>
<tr><td>Ladder Seat (No Enter Top A)</td><td>0x5D20D540</td><td>No</td></tr>
<tr><td>Ladder Seat (No Enter Top B)</td><td>0xCBE541D9</td><td>No</td></tr>
<tr><td>Ladder Seat (No Enter Top C)</td><td>0x3E286612</td><td>No</td></tr>
<tr><td>Ladder Seat (No Enter Top D)</td><td>0xDDDE86BB</td><td>No</td></tr>
<tr><td>Ladder Seat (No Enter Top E)</td><td>0xD0C04534</td><td>No</td></tr>
<tr><td>Ladder Seat (Top A)</td><td>0x4D97BE21</td><td>No</td></tr>
<tr><td>Ladder Seat (Top B)</td><td>0xDF230368</td><td>No</td></tr>
<tr><td>Ladder Seat (Top C)</td><td>0x5BA2917F</td><td>No</td></tr>
<tr><td>Ladder Seat (Top D)</td><td>0xE4B708DE</td><td>No</td></tr>
<tr><td>Ladder Seat (Top E)</td><td>0x829B0D45</td><td>No</td></tr>
<tr><td>Ladder Seat (Top F)</td><td>0x33AFC39C</td><td>No</td></tr>
<tr><td>Ladder Seat (Top G)</td><td>0xC02F6AE3</td><td>No</td></tr>
<tr><td>Ladder Seat (Top H)</td><td>0x08258CB2</td><td>No</td></tr>
<tr><td>Ladder Seat (Top)</td><td>0xDADEB192</td><td>No</td></tr>
<tr><td>Landing Zone</td><td>0xA979B1A8</td><td>No</td></tr>
<tr><td>Landing Zone (player 1)</td><td>0xB00D853B</td><td>No</td></tr>
<tr><td>Landing Zone (player 2)</td><td>0x74E43DF6</td><td>No</td></tr>
<tr><td>Laser Designator</td><td>0x317226F4</td><td>No</td></tr>
<tr><td>Laser Guided Bomb Projectile</td><td>0x936A4827</td><td>No</td></tr>
<tr><td>LAV III (Base)</td><td>0x5C6FD13B</td><td>Yes</td></tr>
<tr><td>Lav_Driver</td><td>0x187DB76F</td><td>Yes</td></tr>
<tr><td>LAVIII (25mm)</td><td>0xCDC13EBD</td><td>Yes</td></tr>
<tr><td>LAVIII (25mm) (Driver)</td><td>0x53C33948</td><td>Yes</td></tr>
<tr><td>LAVIII (25mm) (Full)</td><td>0x06CFF94F</td><td>Yes</td></tr>
<tr><td>LAVIII (AD)</td><td>0xA7F3F42B</td><td>Yes</td></tr>
<tr><td>LAVIII (AD) (Driver)</td><td>0x066154C6</td><td>Yes</td></tr>
<tr><td>LAVIII (AD) (Full)</td><td>0x2C0CB89D</td><td>Yes</td></tr>
<tr><td>LAVIII (AT)</td><td>0x965F28DB</td><td>Yes</td></tr>
<tr><td>LAVIII (AT) (Driver)</td><td>0xC36D6CB6</td><td>Yes</td></tr>
<tr><td>LAVIII (AT) (Full)</td><td>0x6EDBF08D</td><td>Yes</td></tr>
<tr><td>LAVIII (Cargo)</td><td>0x6334EA20</td><td>Yes</td></tr>
<tr><td>LAVIII (MEWSS)</td><td>0x745AEC4D</td><td>Yes</td></tr>
<tr><td>LAVIII (MEWSS) (Driver)</td><td>0xCB9229D8</td><td>Yes</td></tr>
<tr><td>LAVIII (MEWSS) (Full)</td><td>0xBD5C1BDF</td><td>Yes</td></tr>
<tr><td>LAVIII (MGS)</td><td>0x7E78EA99</td><td>Yes</td></tr>
<tr><td>LAVIII (MGS) (Driver)</td><td>0xB4561D74</td><td>Yes</td></tr>
<tr><td>LAVIII (MGS) (Full)</td><td>0x6ADBCCB3</td><td>Yes</td></tr>
<tr><td>LAVIII (Minigun)</td><td>0x7AADF15B</td><td>Yes</td></tr>
<tr><td>LAVIII (Minigun) (Driver)</td><td>0x7495BE36</td><td>Yes</td></tr>
<tr><td>LAVIII (Minigun) (DriverGunner)</td><td>0xE4EA490D</td><td>Yes</td></tr>
<tr><td>LAVIII (Minigun) (Full)</td><td>0x2AA8860D</td><td>Yes</td></tr>
<tr><td>LCUR</td><td>0xCAE7696F</td><td>No</td></tr>
<tr><td>LCUR (Driver)</td><td>0x33D54F9A</td><td>No</td></tr>
<tr><td>LCUR (heavy)</td><td>0x7F1DA981</td><td>No</td></tr>
<tr><td>LCUR (light)</td><td>0xDDBBEA8E</td><td>No</td></tr>
<tr><td>LCUR (medium)</td><td>0xF2B75B03</td><td>No</td></tr>
<tr><td>LCUR_Driver</td><td>0x10F465DC</td><td>No</td></tr>
<tr><td>Lifestyle Job ArmageddonChair</td><td>0xD92ECD54</td><td>No</td></tr>
<tr><td>Lifestyle Job Entrance (Armageddon It Minigame)</td><td>0x510DC102</td><td>No</td></tr>
<tr><td>Lifestyle Job Entrance (High Voltage Minigame)</td><td>0x8ED2E29D</td><td>No</td></tr>
<tr><td>Lifestyle Job HighVoltage</td><td>0xD08E52E1</td><td>No</td></tr>
<tr><td>Lifestyle OilLif001 radio</td><td>0x80BAFCB9</td><td>No</td></tr>
<tr><td>Lifestyle OilLif001 Table</td><td>0xE650ED3C</td><td>No</td></tr>
<tr><td>Lifestyle Seat ArmageddonChair</td><td>0xCD29A57A</td><td>No</td></tr>
<tr><td>Lifestyle Seat ArmageddonChair Player</td><td>0x1A579E61</td><td>No</td></tr>
<tr><td>Lifestyle Seat HIghVoltage</td><td>0xD9EDB65F</td><td>No</td></tr>
<tr><td>Lifestyle Seat HighVoltagePlayer</td><td>0xAA02452C</td><td>No</td></tr>
<tr><td>Light (Point)</td><td>0x5DF27220</td><td>No</td></tr>
<tr><td>Light (Point) small orange</td><td>0xB07F4765</td><td>No</td></tr>
<tr><td>Light (Spot)</td><td>0xAF211D30</td><td>No</td></tr>
<tr><td>Light MG</td><td>0x69F71F2D</td><td>No</td></tr>
<tr><td>Light MG Bullet (GR)</td><td>0x903AB295</td><td>No</td></tr>
<tr><td>Light MG Bullet (OC)</td><td>0x1FF01686</td><td>No</td></tr>
<tr><td>Light_airstrike_carpetbomb</td><td>0x49A2462E</td><td>No</td></tr>
<tr><td>Light_airstrike_clusterbomb</td><td>0xBFE3091B</td><td>No</td></tr>
<tr><td>Light_airstrike_cruisemissile_flash</td><td>0xE4E6C0BD</td><td>No</td></tr>
<tr><td>Light_airstrike_fuelairbomb_lrg</td><td>0x53C24771</td><td>No</td></tr>
<tr><td>Light_airstrike_fuelairbomb_lrg_flash</td><td>0xA4B8835E</td><td>No</td></tr>
<tr><td>Light_airstrike_fuelairbomb_sml</td><td>0x6D2ABCB4</td><td>No</td></tr>
<tr><td>Light_airstrike_moab_flash</td><td>0x4E739509</td><td>No</td></tr>
<tr><td>Light_Animation_yellow_tiny (Flicker) 0x80008623</td><td>0x5A52191C</td><td>No</td></tr>
<tr><td>Light_c4</td><td>0x30B7AB37</td><td>No</td></tr>
<tr><td>Light_contrail</td><td>0xF98BAAC6</td><td>No</td></tr>
<tr><td>Light_enormous_whiteblue 0x8000861f</td><td>0x95D441BD</td><td>No</td></tr>
<tr><td>Light_explosion_huge</td><td>0x4208EF77</td><td>No</td></tr>
<tr><td>Light_explosion_huge_oil</td><td>0x68E64D76</td><td>No</td></tr>
<tr><td>Light_explosion_medium</td><td>0x91E7AC07</td><td>No</td></tr>
<tr><td>Light_explosion_medium_oil</td><td>0xDD241666</td><td>No</td></tr>
<tr><td>Light_explosion_small</td><td>0x2CE3C94F</td><td>No</td></tr>
<tr><td>Light_explosion_tiny</td><td>0x43F3DCF4</td><td>No</td></tr>
<tr><td>Light_fire_blue</td><td>0x4DCE0DB1</td><td>No</td></tr>
<tr><td>Light_fire_carhood</td><td>0x7C969B5B</td><td>No</td></tr>
<tr><td>Light_fire_flare</td><td>0x79BB13EB</td><td>No</td></tr>
<tr><td>Light_fire_huge</td><td>0x4BC87F94</td><td>No</td></tr>
<tr><td>Light_fire_lamp</td><td>0xB97A6E77</td><td>No</td></tr>
<tr><td>Light_fire_large</td><td>0x428234FE</td><td>No</td></tr>
<tr><td>Light_fire_medium</td><td>0x9AA8E5C0</td><td>No</td></tr>
<tr><td>Light_fire_small</td><td>0xFFB554A6</td><td>No</td></tr>
<tr><td>Light_fire_tiny</td><td>0xF9B5B2F7</td><td>No</td></tr>
<tr><td>Light_grenade</td><td>0x4441861C</td><td>No</td></tr>
<tr><td>Light_large_blue_cumana</td><td>0x48DF4684</td><td>No</td></tr>
<tr><td>Light_large_red 0x8000863f</td><td>0x4FCD1260</td><td>No</td></tr>
<tr><td>Light_large_whiteblue 0x80008619</td><td>0x446789D3</td><td>No</td></tr>
<tr><td>Light_large_whiteblue_bright 0x8000861e</td><td>0x899ED6B8</td><td>No</td></tr>
<tr><td>Light_large_whiteblue_cumana</td><td>0x580CEB11</td><td>No</td></tr>
<tr><td>Light_large_whiteblue_dim 0x8000862b</td><td>0x4A6E7484</td><td>No</td></tr>
<tr><td>Light_large_whiteblue_lessbright</td><td>0x666C09C3</td><td>No</td></tr>
<tr><td>Light_large_yellow 0x80008618</td><td>0x031011CB</td><td>No</td></tr>
<tr><td>Light_large_yellow_bright 0x8000861c</td><td>0x201C00B9</td><td>No</td></tr>
<tr><td>Light_large_yellow_dim</td><td>0x476E7B49</td><td>No</td></tr>
<tr><td>Light_med_warm_lantern 0x80008638</td><td>0x731178D0</td><td>No</td></tr>
<tr><td>Light_medium_blue 0x8000861d</td><td>0x43E392CB</td><td>No</td></tr>
<tr><td>Light_medium_blue_dark</td><td>0x5BCB3571</td><td>No</td></tr>
<tr><td>Light_medium_green 0x8000863a</td><td>0xC06EFE77</td><td>No</td></tr>
<tr><td>Light_medium_orange_bright 0x80008639</td><td>0x2C4EE52F</td><td>No</td></tr>
<tr><td>Light_medium_yellow 0x8000861a</td><td>0xCEC820E6</td><td>No</td></tr>
<tr><td>Light_medium_yellow_bright 0x8000863c</td><td>0xAFF7260F</td><td>No</td></tr>
<tr><td>Light_muzzleflash</td><td>0x9D204719</td><td>No</td></tr>
<tr><td>Light_muzzleflash_AA</td><td>0xDDF53CE6</td><td>No</td></tr>
<tr><td>Light_rpg</td><td>0x769E762F</td><td>No</td></tr>
<tr><td>Light_small_blue</td><td>0x9DDE617A</td><td>No</td></tr>
<tr><td>Light_small_blue_dim 0x80008636</td><td>0x8E4C0966</td><td>No</td></tr>
<tr><td>Light_small_blue_intense 0x80008634</td><td>0x9ADBE028</td><td>No</td></tr>
<tr><td>Light_small_darkblue 0x80008640</td><td>0xA86337B4</td><td>No</td></tr>
<tr><td>Light_small_orange</td><td>0x192CEFA8</td><td>No</td></tr>
<tr><td>Light_small_red 0x80008635</td><td>0x5911C7EF</td><td>No</td></tr>
<tr><td>Light_small_red_dim</td><td>0x700DE444</td><td>No</td></tr>
<tr><td>Light_small_white 0x80008633</td><td>0xBE090CAF</td><td>No</td></tr>
<tr><td>Light_small_white_dim</td><td>0x4A35C926</td><td>No</td></tr>
<tr><td>Light_small_yellow</td><td>0xD965157E</td><td>No</td></tr>
<tr><td>Light_small_yellow_dim 0x8000862c</td><td>0x1419DF50</td><td>No</td></tr>
<tr><td>Light_solano_ahj</td><td>0x4B266A46</td><td>No</td></tr>
<tr><td>Light_spot_enormous_yellow 0x80008637</td><td>0x1931F7EE</td><td>No</td></tr>
<tr><td>Light_spot_large_white 0x8000863d</td><td>0x9A30F32B</td><td>No</td></tr>
<tr><td>Light_spot_large_yellow 0x80008627</td><td>0x29C86AD8</td><td>No</td></tr>
<tr><td>Light_spot_medium_blue_cumana</td><td>0xB7E51F4B</td><td>No</td></tr>
<tr><td>Light_spot_medium_yellow 0x8000862e</td><td>0xC5F66F28</td><td>No</td></tr>
<tr><td>Light_spot_medium_yellow_cumana</td><td>0x66D3DC9B</td><td>No</td></tr>
<tr><td>Light_spot_tiny_white 0x80008629</td><td>0x1EDD0CDA</td><td>No</td></tr>
<tr><td>Light_spot_tiny_yellow 0x80008625</td><td>0x42B1C513</td><td>No</td></tr>
<tr><td>Light_tiny_blue 0x80008624</td><td>0xF6A261B5</td><td>No</td></tr>
<tr><td>Light_tiny_warm_lantern 0x8000862a</td><td>0x0FD8221E</td><td>No</td></tr>
<tr><td>Light_tiny_white_weak 0x80008628</td><td>0xD3C1A1B3</td><td>No</td></tr>
<tr><td>Light_tiny_yellow 0x8000861b</td><td>0xB2D6402A</td><td>No</td></tr>
<tr><td>LightAnimation (Flicker)</td><td>0x074ABA2A</td><td>No</td></tr>
<tr><td>LightAnimation (Pulse)</td><td>0xB11604F3</td><td>No</td></tr>
<tr><td>LightAnimation (Strobe)</td><td>0x55C70F11</td><td>No</td></tr>
<tr><td>Lights</td><td>0xE1A18DDA</td><td>No</td></tr>
<tr><td>Listening Post</td><td>0x5023CB6E</td><td>No</td></tr>
<tr><td>LivingWorld Objects</td><td>0x8955971E</td><td>No</td></tr>
<tr><td>LivingWorldTestParkZone</td><td>0x6F79C4D4</td><td>No</td></tr>
<tr><td>LivingWorldTestZone</td><td>0x05D8E01C</td><td>No</td></tr>
<tr><td>location</td><td>0x5FB9E764</td><td>No</td></tr>
<tr><td>Lowresterrain</td><td>0x1602815C</td><td>No</td></tr>
<tr><td>LowRoad</td><td>0x2AA7C187</td><td>No</td></tr>
<tr><td>LW_Entrance_FrontCenter</td><td>0x6ADB51C8</td><td>No</td></tr>
<tr><td>LW_Seat_LR_L</td><td>0xD1DFE43A</td><td>No</td></tr>
<tr><td>LW_Seat_LR_L (Ragdoll)</td><td>0xD2D16A00</td><td>No</td></tr>
<tr><td>LW_Seat_LR_R</td><td>0x319FD404</td><td>No</td></tr>
<tr><td>LW_Seat_LR_R (Ragdoll)</td><td>0x4D312516</td><td>No</td></tr>
<tr><td>LWEntrance_Single</td><td>0x9846E607</td><td>No</td></tr>
<tr><td>LWEntrance_Single (MercsBar)</td><td>0xFC8F5C5B</td><td>No</td></tr>
<tr><td>LWRoads</td><td>0x3FD5F28B</td><td>No</td></tr>
<tr><td>LWSeat_Single</td><td>0xB1E57184</td><td>No</td></tr>
<tr><td>LWSeat_Single (MercsBar)</td><td>0xE0B3F3AA</td><td>No</td></tr>
<tr><td>LWSeat_Single (No Hijack)</td><td>0x5D1CC178</td><td>No</td></tr>
<tr><td>LWSeat_Single (No Hijack) (Ragdoll)</td><td>0xEF730982</td><td>No</td></tr>
<tr><td>LWSeat_Single (Ragdoll)</td><td>0xABD76E96</td><td>No</td></tr>
<tr><td>LWSeats</td><td>0x12DDCF58</td><td>No</td></tr>
<tr><td>M113 (Base Passenger)</td><td>0xDD0FBB45</td><td>Yes</td></tr>
<tr><td>M113 (Base)</td><td>0xAB5BAEF9</td><td>Yes</td></tr>
<tr><td>M113 (GR)</td><td>0xCE5E8D35</td><td>Yes</td></tr>
<tr><td>M113 (GR) (Driver)</td><td>0x48FB03C0</td><td>Yes</td></tr>
<tr><td>M113 (GR) (DriverGunner)</td><td>0x9AF7067F</td><td>Yes</td></tr>
<tr><td>M113 (GR) (Full)</td><td>0xD7604AD7</td><td>Yes</td></tr>
<tr><td>M113 (VZ)</td><td>0xC9900D64</td><td>Yes</td></tr>
<tr><td>M113 (VZ) (Driver)</td><td>0xEB80EF43</td><td>Yes</td></tr>
<tr><td>M113 (VZ) (DriverGunner)</td><td>0xDA41DF94</td><td>Yes</td></tr>
<tr><td>M113 (VZ) (Full RPG)</td><td>0xA81BE3EB</td><td>Yes</td></tr>
<tr><td>M113 (VZ) (Full)</td><td>0x88D24F70</td><td>Yes</td></tr>
<tr><td>M113 AA (base)</td><td>0x5266EAA9</td><td>Yes</td></tr>
<tr><td>M113 AA (GR)</td><td>0xEBD1DEE5</td><td>Yes</td></tr>
<tr><td>M113 AA (GR) (Driver)</td><td>0x973B8270</td><td>Yes</td></tr>
<tr><td>M113 AA (GR) (DriverGunner)</td><td>0xF8B5BD2F</td><td>Yes</td></tr>
<tr><td>M113 AA (GR) (Full)</td><td>0x180BD007</td><td>Yes</td></tr>
<tr><td>M113 AA (VZ)</td><td>0x26D6AE34</td><td>Yes</td></tr>
<tr><td>M113 AA (VZ) (Driver)</td><td>0x50F46313</td><td>Yes</td></tr>
<tr><td>M113 AA (VZ) (Full)</td><td>0xB1BC8DC0</td><td>Yes</td></tr>
<tr><td>M113 Jammer</td><td>0xC3B398ED</td><td>Yes</td></tr>
<tr><td>M113 Jammer (VZ)</td><td>0x5F15847E</td><td>Yes</td></tr>
<tr><td>M113 Jammer (VZ) (Driver)</td><td>0x63E36415</td><td>Yes</td></tr>
<tr><td>M113 Transport</td><td>0x127C2568</td><td>Yes</td></tr>
<tr><td>M113FullSpawnList</td><td>0xF15F844D</td><td>Yes</td></tr>
<tr><td>M151 (Base)</td><td>0x55639ADF</td><td>Yes</td></tr>
<tr><td>M151 (MG)</td><td>0x58918BDE</td><td>Yes</td></tr>
<tr><td>M151 (MG) (GR)</td><td>0xA72B34B2</td><td>Yes</td></tr>
<tr><td>M151 (MG) (GR) (Driver)</td><td>0x288238D9</td><td>Yes</td></tr>
<tr><td>M151 (MG) (GR) (DriverGunner)</td><td>0xE6A2F38A</td><td>Yes</td></tr>
<tr><td>M151 (MG) (VZ) (Driver)</td><td>0xC26E9EFE</td><td>Yes</td></tr>
<tr><td>M151 .50Cal (GR) (Full)</td><td>0x4F814028</td><td>Yes</td></tr>
<tr><td>M151 .50Cal (VZ)</td><td>0xEEA87FED</td><td>Yes</td></tr>
<tr><td>M151 .50Cal (VZ) (DriverGunner)</td><td>0x72A4CB37</td><td>Yes</td></tr>
<tr><td>M151 .50Cal (VZ) (Full)</td><td>0x888F587F</td><td>Yes</td></tr>
<tr><td>M151 Softtop</td><td>0x7260D03C</td><td>Yes</td></tr>
<tr><td>M151 Softtop (GR)</td><td>0x4411809C</td><td>Yes</td></tr>
<tr><td>M151 Softtop (GR) (Driver)</td><td>0x5871785B</td><td>Yes</td></tr>
<tr><td>M151 Softtop (GR) (Full)</td><td>0xF37B0A58</td><td>Yes</td></tr>
<tr><td>M151 Softtop (VZ)</td><td>0xD68A30FD</td><td>Yes</td></tr>
<tr><td>M151 Softtop (VZ) (Driver)</td><td>0x23713C08</td><td>Yes</td></tr>
<tr><td>M151 Softtop (VZ) (Full)</td><td>0x25FE790F</td><td>Yes</td></tr>
<tr><td>M151_Driver</td><td>0x9F163EDA</td><td>Yes</td></tr>
<tr><td>M151_Ruin</td><td>0x94F06992</td><td>Yes</td></tr>
<tr><td>M163 Driver Seat</td><td>0xB348901B</td><td>No</td></tr>
<tr><td>M1A2</td><td>0x0118204A</td><td>Yes</td></tr>
<tr><td>M1A2 (Cargo)</td><td>0x21D37A93</td><td>Yes</td></tr>
<tr><td>M1A2 (Driver)</td><td>0x5415F131</td><td>Yes</td></tr>
<tr><td>M1A2 (Full)</td><td>0x48606406</td><td>Yes</td></tr>
<tr><td>M2A3</td><td>0xAE0761D0</td><td>Yes</td></tr>
<tr><td>M2A3 (Base)</td><td>0x7B720A28</td><td>Yes</td></tr>
<tr><td>M2A3 (Driver)</td><td>0x1DA3756F</td><td>Yes</td></tr>
<tr><td>M35 (AA)</td><td>0xCF00E219</td><td>Yes</td></tr>
<tr><td>M35 (AA) (GR)</td><td>0x7E68250B</td><td>Yes</td></tr>
<tr><td>M35 (AA) (GR) (Driver)</td><td>0xB29EA7A6</td><td>Yes</td></tr>
<tr><td>M35 (AA) (GR) (Full)</td><td>0x44AEB37D</td><td>Yes</td></tr>
<tr><td>M35 (AA) (VZ)</td><td>0x22A3CAEA</td><td>Yes</td></tr>
<tr><td>M35 (AA) (VZ) (Driver)</td><td>0x855352D1</td><td>Yes</td></tr>
<tr><td>M35 (AA) (VZ) (Full)</td><td>0xD34462A6</td><td>Yes</td></tr>
<tr><td>M35 (Cargo)</td><td>0x0B3E0EEB</td><td>Yes</td></tr>
<tr><td>M35 (Cargo) (GR)</td><td>0x15A6E679</td><td>Yes</td></tr>
<tr><td>M35 (Cargo) (GR) (Driver)</td><td>0x00FB4CD4</td><td>Yes</td></tr>
<tr><td>M35 (Cargo) (GR) (Full)</td><td>0xA4F49093</td><td>Yes</td></tr>
<tr><td>M35 (Cargo) (VZ)</td><td>0x69BA71A8</td><td>Yes</td></tr>
<tr><td>M35 (Cargo) (VZ) (Driver)</td><td>0x1821E287</td><td>Yes</td></tr>
<tr><td>M35 (Cargo) (VZ) (Full RPG)</td><td>0x0735588F</td><td>Yes</td></tr>
<tr><td>M35 (Cargo) (VZ) (Full)</td><td>0xE0D2C7CC</td><td>Yes</td></tr>
<tr><td>M35 (Fuel)</td><td>0x617EEDAB</td><td>Yes</td></tr>
<tr><td>M35 (Fuel) (GR)</td><td>0xF351EFB9</td><td>Yes</td></tr>
<tr><td>M35 (Fuel) (GR) (Driver)</td><td>0xED202294</td><td>Yes</td></tr>
<tr><td>M35 (Fuel) (GR) (Full)</td><td>0x7A605253</td><td>Yes</td></tr>
<tr><td>M35 (Fuel) (VZ)</td><td>0x60B22FE8</td><td>Yes</td></tr>
<tr><td>M35 (Fuel) (VZ) (Driver)</td><td>0x15DC6847</td><td>Yes</td></tr>
<tr><td>M35 (Fuel) (VZ) (Full)</td><td>0xEB7A638C</td><td>Yes</td></tr>
<tr><td>M35 (Guntruck)</td><td>0x5F128AE6</td><td>Yes</td></tr>
<tr><td>M35 (Guntruck) (GR)</td><td>0x1EB74FCA</td><td>Yes</td></tr>
<tr><td>M35 (Guntruck) (GR) (Driver)</td><td>0xB1D007B1</td><td>Yes</td></tr>
<tr><td>M35 (Guntruck) (GR) (Full)</td><td>0x4E05F686</td><td>Yes</td></tr>
<tr><td>M35 (Guntruck) (VZ)</td><td>0x7BE5F40B</td><td>Yes</td></tr>
<tr><td>M35 (Guntruck) (VZ) (Driver)</td><td>0xE44A24A6</td><td>Yes</td></tr>
<tr><td>M35 (Guntruck) (VZ) (Full)</td><td>0xC06CA87D</td><td>Yes</td></tr>
<tr><td>M35 (Guntruck) (VZ) (SemiFull)</td><td>0xE49CA0B7</td><td>Yes</td></tr>
<tr><td>M35 Truck (base)</td><td>0x8FC60AB1</td><td>Yes</td></tr>
<tr><td>M35_Driver</td><td>0xBE2248D3</td><td>Yes</td></tr>
<tr><td>M35_Ruin</td><td>0xE32FBDBB</td><td>Yes</td></tr>
<tr><td>M35VZGuntruckFull_Spawnlist</td><td>0x808CADD6</td><td>Yes</td></tr>
<tr><td>M551</td><td>0x43C6A9CD</td><td>Yes</td></tr>
<tr><td>M551 (Driver)</td><td>0x48F70A58</td><td>Yes</td></tr>
<tr><td>M551 (Full)</td><td>0xBF98E85F</td><td>Yes</td></tr>
<tr><td>M6 - DO NOT USE</td><td>0x67477F92</td><td>No</td></tr>
<tr><td>Machine Pistol</td><td>0xAB74E231</td><td>No</td></tr>
<tr><td>Machine Pistol (PP2000)</td><td>0x8FDEFF14</td><td>No</td></tr>
<tr><td>Machine Pistol (TMP)</td><td>0x462810E1</td><td>No</td></tr>
<tr><td>Machine Pistol (Uzi)</td><td>0x6B018DF6</td><td>No</td></tr>
<tr><td>Machine Pistol (Window Spawner)</td><td>0x9A28F0B6</td><td>No</td></tr>
<tr><td>Machine Pistol Bullet</td><td>0x43F1553B</td><td>No</td></tr>
<tr><td>Magazine (Assault Rifle)</td><td>0xA5BC19DF</td><td>Yes</td></tr>
<tr><td>Magazine (RPG)</td><td>0xC6709D09</td><td>Yes</td></tr>
<tr><td>Magazines</td><td>0x2DE2E5AE</td><td>Yes</td></tr>
<tr><td>MagicBarrack</td><td>0xF199D264</td><td>No</td></tr>
<tr><td>MagicSeat</td><td>0x5EEA3C95</td><td>No</td></tr>
<tr><td>MagicTurret</td><td>0x5B1E2C94</td><td>No</td></tr>
<tr><td>Mark (Civ)</td><td>0xDAA49C09</td><td>No</td></tr>
<tr><td>Mark (Civ) (Driver)</td><td>0x17386824</td><td>No</td></tr>
<tr><td>Mark (Civ) (Driver) (Mechanic male)</td><td>0xFD8DD31E</td><td>No</td></tr>
<tr><td>Mark (Civ) (Full)</td><td>0xD2B2BCE3</td><td>No</td></tr>
<tr><td>Mark (PR)</td><td>0x746B03ED</td><td>No</td></tr>
<tr><td>Mark (PR) (Driver)</td><td>0x0FA2ECF8</td><td>No</td></tr>
<tr><td>Mark (PR) (Full)</td><td>0x69B6C47F</td><td>No</td></tr>
<tr><td>Mark_Driver</td><td>0x75D25B87</td><td>No</td></tr>
<tr><td>MarkV</td><td>0xD621AED8</td><td>No</td></tr>
<tr><td>MarkV (Driver)</td><td>0x0A0BBB37</td><td>No</td></tr>
<tr><td>MarkV (Full)</td><td>0x2A83887C</td><td>No</td></tr>
<tr><td>MarkV (Full) (Allied)</td><td>0xCD4136EA</td><td>No</td></tr>
<tr><td>MarkV (Half) (Allied)</td><td>0x8DA232F6</td><td>No</td></tr>
<tr><td>MarkV_Driver</td><td>0x05795405</td><td>No</td></tr>
<tr><td>Matches Projectile</td><td>0xD70A8661</td><td>No</td></tr>
<tr><td>Material Test Asset</td><td>0x304B38AA</td><td>No</td></tr>
<tr><td>Mattias</td><td>0x030E6C38</td><td>No</td></tr>
<tr><td>Mattias Chopper</td><td>0x1ECD5E19</td><td>Yes</td></tr>
<tr><td>MattiasChickensuit</td><td>0x98507A86</td><td>No</td></tr>
<tr><td>mattiasupgrade1</td><td>0x7D2EEA01</td><td>No</td></tr>
<tr><td>mattiasupgrade2</td><td>0xFB276196</td><td>No</td></tr>
<tr><td>mattiasupgrade3</td><td>0x5D2A3A73</td><td>No</td></tr>
<tr><td>MattiasV2</td><td>0x043D0100</td><td>No</td></tr>
<tr><td>MattiasV3</td><td>0x2E3F81B5</td><td>No</td></tr>
<tr><td>MD-500</td><td>0xC9B8D3D0</td><td>No</td></tr>
<tr><td>Mechanic (male)</td><td>0xA3A8AC09</td><td>No</td></tr>
<tr><td>merida_wallchurchshort</td><td>0x5F67A1D9</td><td>No</td></tr>
<tr><td>merida_wallcommercialshorta</td><td>0x6F04F6AD</td><td>No</td></tr>
<tr><td>MeridaTest Allies</td><td>0x8D9D02A1</td><td>No</td></tr>
<tr><td>MeridaTest VZ</td><td>0xF7A3427F</td><td>No</td></tr>
<tr><td>MH53J</td><td>0x83143980</td><td>Yes</td></tr>
<tr><td>MH53J (Driver)</td><td>0x4B5CA29F</td><td>Yes</td></tr>
<tr><td>MH53J (DriverGunner)</td><td>0x859F20B8</td><td>Yes</td></tr>
<tr><td>MH53J (Ewan)</td><td>0x70719716</td><td>Yes</td></tr>
<tr><td>MH53J (Extraction)</td><td>0x913C4E6C</td><td>Yes</td></tr>
<tr><td>MH53J (Full)</td><td>0xC97B7814</td><td>Yes</td></tr>
<tr><td>MH53J (Pursuit)</td><td>0x9964CB9F</td><td>Yes</td></tr>
<tr><td>Mi26 (base)</td><td>0x9567C231</td><td>Yes</td></tr>
<tr><td>Mi26 (CH)</td><td>0x2A46CE47</td><td>Yes</td></tr>
<tr><td>Mi26 (CH) (Delivery)</td><td>0xE8E09FB0</td><td>Yes</td></tr>
<tr><td>Mi26 (CH) (Driver)</td><td>0x67B02532</td><td>Yes</td></tr>
<tr><td>Mi26 (CH) (Ewan)</td><td>0x71CAED6B</td><td>Yes</td></tr>
<tr><td>Mi26 (PMC)</td><td>0x8E30490E</td><td>Yes</td></tr>
<tr><td>Mi26 (PMC) (Driver)</td><td>0x9F6ADD25</td><td>Yes</td></tr>
<tr><td>Mi26 (VZ)</td><td>0x58D6ABEC</td><td>Yes</td></tr>
<tr><td>Mi26 (VZ) (Driver)</td><td>0x77C9BD6B</td><td>Yes</td></tr>
<tr><td>Mi26 (VZ) (Ewan)</td><td>0x4AFFE432</td><td>Yes</td></tr>
<tr><td>Mi26 (VZA Intro) (Driver)</td><td>0xCB82945A</td><td>Yes</td></tr>
<tr><td>Mi35</td><td>0xD2119BCF</td><td>Yes</td></tr>
<tr><td>Mi35 (AA Driver)</td><td>0x7B286256</td><td>Yes</td></tr>
<tr><td>Mi35 (AA)</td><td>0xA0D30616</td><td>Yes</td></tr>
<tr><td>Mi35 (AA) (Ewan)</td><td>0xF31E7948</td><td>Yes</td></tr>
<tr><td>Mi35 (base)</td><td>0x5D916CC1</td><td>Yes</td></tr>
<tr><td>Mi35 (Driver)</td><td>0x0EED5CFA</td><td>Yes</td></tr>
<tr><td>Mi35 (Ewan)</td><td>0x6E0D5F93</td><td>Yes</td></tr>
<tr><td>Mi35 (Full)</td><td>0xCDDFDF39</td><td>Yes</td></tr>
<tr><td>Mi35 (Gunner)</td><td>0x743728D7</td><td>Yes</td></tr>
<tr><td>Mi35 (Solano)</td><td>0xA2EFB316</td><td>Yes</td></tr>
<tr><td>Mine (Human)</td><td>0x73FB8018</td><td>No</td></tr>
<tr><td>Mine (IED)</td><td>0xBE4E6E3F</td><td>No</td></tr>
<tr><td>Mine (Vehicle)</td><td>0xDFE0E1E1</td><td>No</td></tr>
<tr><td>Mine (Water)</td><td>0x3EF3D17E</td><td>No</td></tr>
<tr><td>Mine (Water) (Light)</td><td>0x87D2A00F</td><td>No</td></tr>
<tr><td>Minigun</td><td>0x624C0986</td><td>No</td></tr>
<tr><td>Minigun 1000</td><td>0x049CD8B9</td><td>No</td></tr>
<tr><td>Minigun 1800</td><td>0x99DD73C1</td><td>No</td></tr>
<tr><td>Minigun 900</td><td>0x9369BBB3</td><td>No</td></tr>
<tr><td>Minigun Bullet</td><td>0xDAF903E6</td><td>No</td></tr>
<tr><td>Minigun Bullet (AL)</td><td>0x7303A282</td><td>No</td></tr>
<tr><td>Minigun Bullet (CH)</td><td>0x0B31ED4C</td><td>No</td></tr>
<tr><td>Minigun Bullet (GR)</td><td>0x59D47ACA</td><td>No</td></tr>
<tr><td>Minigun Bullet (Ship)</td><td>0x18DFE609</td><td>Yes</td></tr>
<tr><td>MLRS Rocket</td><td>0x2560F199</td><td>No</td></tr>
<tr><td>MOAB Projectile</td><td>0xFCB92D05</td><td>No</td></tr>
<tr><td>Monster Ridgeline</td><td>0x1D489F46</td><td>No</td></tr>
<tr><td>Monster Truck</td><td>0xBA21D4C4</td><td>Yes</td></tr>
<tr><td>Monster Truck (base)</td><td>0x1000B4EC</td><td>Yes</td></tr>
<tr><td>Monster truck phase1</td><td>0x9383C116</td><td>Yes</td></tr>
<tr><td>Monster truck phase2</td><td>0x158B4981</td><td>Yes</td></tr>
<tr><td>Monster truck test</td><td>0x9003C228</td><td>Yes</td></tr>
<tr><td>MonsterRidgeline_Driver</td><td>0x506C2D61</td><td>No</td></tr>
<tr><td>MonsterRTR_Driver</td><td>0xC091FE7C</td><td>No</td></tr>
<tr><td>monuments</td><td>0xE28D61F9</td><td>No</td></tr>
<tr><td>Motorcycle</td><td>0xA14A4912</td><td>Yes</td></tr>
<tr><td>Motorcycle_Driver</td><td>0x6664AE73</td><td>Yes</td></tr>
<tr><td>MotorcycleOld</td><td>0x25A09161</td><td>Yes</td></tr>
<tr><td>MotorCycleTest</td><td>0x261B03E6</td><td>Yes</td></tr>
<tr><td>Mounted AA Missile (1) (AMX30) A</td><td>0xABE72070</td><td>Yes</td></tr>
<tr><td>Mounted AA Missile (1) (AMX30) B</td><td>0x95E4BF37</td><td>Yes</td></tr>
<tr><td>Mounted AA Missile (1) (AMX30) C</td><td>0xB3E2AFDA</td><td>Yes</td></tr>
<tr><td>Mounted AA Missile (1) (AMX30) D</td><td>0x8DE03571</td><td>Yes</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_a)</td><td>0x2069A810</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_b)</td><td>0x8E8EB0E9</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_c)</td><td>0x81706F62</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_d)</td><td>0x6126F4CB</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_e)</td><td>0xD4A74D84</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_f)</td><td>0x6392FBED</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_g)</td><td>0x25FDAD86</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_h)</td><td>0x558C0E6F</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_sidewinder_L)</td><td>0x52074186</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_sidewinder_R)</td><td>0x32E24A08</td><td>No</td></tr>
<tr><td>Mounted AA Missile (1) (PGZ95) A</td><td>0xB5466BDA</td><td>Yes</td></tr>
<tr><td>Mounted AA Missile (1) (PGZ95) B</td><td>0x174DC1E5</td><td>Yes</td></tr>
<tr><td>Mounted AA Missile (1) (PGZ95) C</td><td>0xAD4ADC70</td><td>Yes</td></tr>
<tr><td>Mounted AA Missile (1) (PGZ95) D</td><td>0x2F3EDD23</td><td>Yes</td></tr>
<tr><td>Mounted AA Missile (2) (Zu23) A</td><td>0xF03FA40A</td><td>No</td></tr>
<tr><td>Mounted AA Missile (2) (Zu23) B</td><td>0x92475ED5</td><td>No</td></tr>
<tr><td>Mounted AA Missile (4)</td><td>0x9B70F72E</td><td>No</td></tr>
<tr><td>Mounted AC A (VZ)</td><td>0x8917B47D</td><td>No</td></tr>
<tr><td>Mounted AC B (VZ)</td><td>0xC70BEFB0</td><td>No</td></tr>
<tr><td>Mounted AH1Z Cannon</td><td>0xCEBA555E</td><td>Yes</td></tr>
<tr><td>Mounted AT Missile (1)  (hp_barreltip_a)</td><td>0x3016AB93</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1)  (hp_barreltip_b)</td><td>0x153D488E</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (Base)</td><td>0x4C9BEF00</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_raila)</td><td>0xA8DC9549</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railab)</td><td>0x8FCC7C4B</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railac)</td><td>0x034CD504</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railad)</td><td>0xBD343869</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railae)</td><td>0xB015F6E2</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railaf)</td><td>0x6C2D8A47</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railag)</td><td>0x4F0F2F90</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railah)</td><td>0xAB2A11B5</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missile_L)</td><td>0x3060A513</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missile_la)</td><td>0x1A63F32C</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missile_R)</td><td>0xF3E10699</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missileL_a)</td><td>0xEBA333F2</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missileL_b)</td><td>0x271C2D17</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missileR_a)</td><td>0xFA21F9E0</td><td>No</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missileR_b)</td><td>0xE8E59CF9</td><td>No</td></tr>
<tr><td>Mounted AT Missile (2)  (hp_barreltip_c)</td><td>0x4F784B20</td><td>No</td></tr>
<tr><td>Mounted AT Missile (2) (M2A3)</td><td>0x6C8EDBAD</td><td>Yes</td></tr>
<tr><td>Mounted AT Missile (4)</td><td>0x70CB82B3</td><td>No</td></tr>
<tr><td>Mounted AT Missile (4) (hp_barreltip_missile_L)</td><td>0x70478B06</td><td>No</td></tr>
<tr><td>Mounted AT Missile (4) (hp_barreltip_missile_R)</td><td>0x51229388</td><td>No</td></tr>
<tr><td>Mounted AT Missile (8)</td><td>0xB2FD0467</td><td>No</td></tr>
<tr><td>Mounted AT Missile (hp_barreltip_missile_lb)</td><td>0x7D548893</td><td>No</td></tr>
<tr><td>Mounted AT Missile (hp_barreltip_missile_ra)</td><td>0x8F08CF54</td><td>No</td></tr>
<tr><td>Mounted AT Missile (hp_barreltip_missile_rb)</td><td>0xDD56483D</td><td>No</td></tr>
<tr><td>Mounted AT Missile (Veyron)</td><td>0x5B34F448</td><td>No</td></tr>
<tr><td>Mounted Autocannon (AL)</td><td>0x6090304D</td><td>No</td></tr>
<tr><td>Mounted Autocannon (CH)</td><td>0xB17FB08B</td><td>No</td></tr>
<tr><td>Mounted Autocannon (Type 14310)</td><td>0x7BC113EF</td><td>No</td></tr>
<tr><td>Mounted Blast Cannon</td><td>0x37938DD0</td><td>No</td></tr>
<tr><td>Mounted Chain Cannon</td><td>0x50AA1C3F</td><td>No</td></tr>
<tr><td>Mounted Chain Cannon (CH)</td><td>0x7872DE87</td><td>No</td></tr>
<tr><td>Mounted Chain Cannon (GR)</td><td>0xF97B07CD</td><td>No</td></tr>
<tr><td>Mounted Coax 20mm (OC)</td><td>0x08D57327</td><td>No</td></tr>
<tr><td>Mounted Coax 20mm (VZ)</td><td>0x658DA359</td><td>No</td></tr>
<tr><td>Mounted Coax MG (AL)</td><td>0x544E96C0</td><td>No</td></tr>
<tr><td>Mounted Coax MG (CH)</td><td>0xB6D6C82E</td><td>No</td></tr>
<tr><td>Mounted Coax MG (GR)</td><td>0xCBCA16B8</td><td>No</td></tr>
<tr><td>Mounted Coax MG (VZ)</td><td>0x1D9E8B69</td><td>No</td></tr>
<tr><td>Mounted Cruise Missile</td><td>0x6F53A674</td><td>No</td></tr>
<tr><td>Mounted Cruise Missile Projectile</td><td>0x61048FB9</td><td>No</td></tr>
<tr><td>Mounted Destroyer Cannon</td><td>0xF76F060F</td><td>Yes</td></tr>
<tr><td>Mounted Destroyer Cannon (Chinese)</td><td>0x4414CCB9</td><td>Yes</td></tr>
<tr><td>Mounted FAE (1) (hp_barreltip_hellfire_raila)</td><td>0x1CB068A0</td><td>No</td></tr>
<tr><td>Mounted FAE (1) (hp_barreltip_hellfire_railb)</td><td>0x0B740BB9</td><td>No</td></tr>
<tr><td>Mounted FAE (1) (hp_barreltip_hellfire_railc)</td><td>0x7EF46472</td><td>No</td></tr>
<tr><td>Mounted FAE (1) (hp_barreltip_hellfire_raild)</td><td>0x1EAA851B</td><td>No</td></tr>
<tr><td>Mounted Grenade Launcher</td><td>0x14DA2EDB</td><td>No</td></tr>
<tr><td>Mounted Grenade Launcher (UH1 Elite)</td><td>0xD57B8791</td><td>Yes</td></tr>
<tr><td>Mounted Grenade Launcher Shooting Gallery</td><td>0xDE0D1378</td><td>No</td></tr>
<tr><td>Mounted Gun (Endriago) (Superiority) (LB)</td><td>0x3F410E0A</td><td>No</td></tr>
<tr><td>Mounted Gun (Endriago) (Superiority) (LT)</td><td>0xA043EF7C</td><td>No</td></tr>
<tr><td>Mounted Gun (Endriago) (Superiority) (RB)</td><td>0x35F50D74</td><td>No</td></tr>
<tr><td>Mounted Gun (Endriago) (Superiority) (RT)</td><td>0x74F194E2</td><td>No</td></tr>
<tr><td>Mounted Gun (Piranha) (L)</td><td>0x97AF2A8A</td><td>Yes</td></tr>
<tr><td>Mounted Gun (Piranha) (R)</td><td>0xDFC07DB4</td><td>Yes</td></tr>
<tr><td>Mounted Gun Front (Patrol Boat VZ)</td><td>0xEAD9F069</td><td>Yes</td></tr>
<tr><td>Mounted Gunpod (L) (AL)</td><td>0x1F02D391</td><td>No</td></tr>
<tr><td>Mounted Gunpod (R) (AL)</td><td>0x6B0EC633</td><td>No</td></tr>
<tr><td>Mounted Heavy MG (AL)</td><td>0xB300A00E</td><td>No</td></tr>
<tr><td>Mounted Heavy MG (Avenger)</td><td>0x1F3D06B9</td><td>No</td></tr>
<tr><td>Mounted Heavy MG (Base)</td><td>0x70274A56</td><td>No</td></tr>
<tr><td>Mounted Heavy MG (CH)</td><td>0x4F3B3A20</td><td>No</td></tr>
<tr><td>Mounted Heavy MG (GR)</td><td>0x54D1D516</td><td>No</td></tr>
<tr><td>Mounted Heavy MG (Jeep) (AL)</td><td>0x3565F12D</td><td>Yes</td></tr>
<tr><td>Mounted Heavy MG (Jeep) (GR)</td><td>0xBC105279</td><td>Yes</td></tr>
<tr><td>Mounted Heavy MG (Jeep) (OC)</td><td>0xDF170CCA</td><td>Yes</td></tr>
<tr><td>Mounted Heavy MG (No Model)</td><td>0xA88E044D</td><td>No</td></tr>
<tr><td>Mounted Heavy MG (NOAMMO)</td><td>0xC3B9FF06</td><td>No</td></tr>
<tr><td>Mounted Heavy MG (OC)</td><td>0x21ED52B5</td><td>No</td></tr>
<tr><td>Mounted Heavy MG (Tank) (AL)</td><td>0xF58133B9</td><td>Yes</td></tr>
<tr><td>Mounted Heavy MG (Tank) (CH)</td><td>0x60CFE4EF</td><td>Yes</td></tr>
<tr><td>Mounted Heavy MG (Tank) (GR)</td><td>0x745B25A5</td><td>Yes</td></tr>
<tr><td>Mounted Heavy MG (Tank) (OC)</td><td>0xFA33A7F6</td><td>Yes</td></tr>
<tr><td>Mounted Heavy MG (Tank) (VZ)</td><td>0x96133FF4</td><td>Yes</td></tr>
<tr><td>Mounted Heavy MG (VZ)</td><td>0x08DB8417</td><td>No</td></tr>
<tr><td>Mounted Light MG (GR)</td><td>0x39A0741B</td><td>No</td></tr>
<tr><td>Mounted LockOn Missile</td><td>0xAFEB579B</td><td>No</td></tr>
<tr><td>Mounted M101A1 Gun</td><td>0xD462BFB2</td><td>No</td></tr>
<tr><td>Mounted MG (L)</td><td>0x285BA208</td><td>No</td></tr>
<tr><td>Mounted MG (R)</td><td>0x47809986</td><td>No</td></tr>
<tr><td>Mounted Minigun (Destroyer) (FL)</td><td>0x51AEEAC1</td><td>Yes</td></tr>
<tr><td>Mounted Minigun (Destroyer) (FM)</td><td>0x4490A93A</td><td>Yes</td></tr>
<tr><td>Mounted Minigun (Destroyer) (FR)</td><td>0x3C4B3A4B</td><td>Yes</td></tr>
<tr><td>Mounted Minigun (Destroyer) (RL)</td><td>0xC6661465</td><td>Yes</td></tr>
<tr><td>Mounted Minigun (Destroyer) (RR)</td><td>0xD99C8DC7</td><td>Yes</td></tr>
<tr><td>Mounted Minigun (Human) (AL)</td><td>0xACA58116</td><td>No</td></tr>
<tr><td>Mounted Minigun (Human) (GR)</td><td>0x499A11CE</td><td>No</td></tr>
<tr><td>Mounted Minigun (Human) HelCon001</td><td>0x2F3E5314</td><td>No</td></tr>
<tr><td>Mounted Minigun (No Model) (AL)</td><td>0x52B5AA0B</td><td>No</td></tr>
<tr><td>Mounted Minigun (No model) (Hind)</td><td>0x2E850373</td><td>Yes</td></tr>
<tr><td>Mounted Minigun (No Model) (LAV3 AD)</td><td>0x102B093D</td><td>Yes</td></tr>
<tr><td>Mounted Minigun (No model) (M1A2)</td><td>0xB2B5511F</td><td>Yes</td></tr>
<tr><td>Mounted Minigun (No Model) (VZ)</td><td>0xFC34C616</td><td>No</td></tr>
<tr><td>Mounted Minigun (Remote) (AL)</td><td>0xCE7E778F</td><td>No</td></tr>
<tr><td>Mounted Minigun Left (No Model) (GR)</td><td>0x4F1B684C</td><td>No</td></tr>
<tr><td>Mounted Minigun Left (No Model) (Small) (VZ)</td><td>0xEB11BE9F</td><td>No</td></tr>
<tr><td>Mounted Minigun Right (No Model) (GR)</td><td>0xBDE3C1E5</td><td>No</td></tr>
<tr><td>Mounted Minigun Right (No Model) (Small) (VZ)</td><td>0x58CF48F6</td><td>No</td></tr>
<tr><td>Mounted MLRS</td><td>0xAC223AF7</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (01)</td><td>0x11965E4F</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (02)</td><td>0x366DAE2A</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (03)</td><td>0xC2ED5571</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (04)</td><td>0xA9055AEC</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (05)</td><td>0xB6239C73</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (06)</td><td>0x1A0C3B6E</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (07)</td><td>0xB7526F15</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (08)</td><td>0xDB36C370</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (09)</td><td>0xF8551E27</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (10)</td><td>0x414EE8C5</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (11)</td><td>0xA36AE45E</td><td>No</td></tr>
<tr><td>Mounted MLRS (SX2150) (12)</td><td>0x7EE34663</td><td>No</td></tr>
<tr><td>Mounted Panhard Assault Cannon</td><td>0x53E032EF</td><td>No</td></tr>
<tr><td>Mounted PGZ95 Gun</td><td>0x06B1335C</td><td>Yes</td></tr>
<tr><td>Mounted PGZ95 Gun (A)</td><td>0x77662EDA</td><td>Yes</td></tr>
<tr><td>Mounted PGZ95 Gun (B)</td><td>0x928F43BF</td><td>Yes</td></tr>
<tr><td>Mounted PGZ95 Gun (C)</td><td>0x160FB5A8</td><td>Yes</td></tr>
<tr><td>Mounted PGZ95 Gun (D)</td><td>0xB987BF85</td><td>Yes</td></tr>
<tr><td>Mounted Piranha Deck Cannon</td><td>0x49DEA0CC</td><td>Yes</td></tr>
<tr><td>Mounted Piranha Jet Exhaust</td><td>0xEF7FFB65</td><td>Yes</td></tr>
<tr><td>Mounted Quad50 Gun A (GR)</td><td>0x88A30040</td><td>No</td></tr>
<tr><td>Mounted Quad50 Gun A (VZ)</td><td>0x0D76BCC1</td><td>No</td></tr>
<tr><td>Mounted Quad50 Gun B (GR)</td><td>0x1DECD9B5</td><td>No</td></tr>
<tr><td>Mounted Quad50 Gun B (VZ)</td><td>0x191E59E4</td><td>No</td></tr>
<tr><td>Mounted Quad50 Gun C (GR)</td><td>0xD228E09E</td><td>No</td></tr>
<tr><td>Mounted Quad50 Gun C (VZ)</td><td>0x2DE9E22F</td><td>No</td></tr>
<tr><td>Mounted Quad50 Gun D (GR)</td><td>0xEF6E0ED3</td><td>No</td></tr>
<tr><td>Mounted Quad50 Gun D (VZ)</td><td>0x005BB6E2</td><td>No</td></tr>
<tr><td>Mounted Recoiless Rifle</td><td>0xF6A450BC</td><td>No</td></tr>
<tr><td>Mounted Rocket (3)</td><td>0xBB1AA49D</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (10) (hp_barreltip_rocket_L)</td><td>0xEAB93289</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (10) (hp_barreltip_rocket_R)</td><td>0x440F9F23</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (19)</td><td>0x09C80673</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (19) (hp_barreltip_rcketlgL)</td><td>0x992241C5</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (19) (hp_barreltip_rcketlgR)</td><td>0xAB1B86A7</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (19) (hp_barreltip_xrocketL)</td><td>0x35E451C1</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (19) (hp_barreltip_xrocketR)</td><td>0x2080A14B</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (20)</td><td>0xA5E26E43</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (32)</td><td>0xCEC74E4C</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (32) (hp_barreltip_rocket_L)</td><td>0x42C03281</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (32) (hp_barreltip_rocket_R)</td><td>0x2D5C820B</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (6) (L)</td><td>0xDF92C81E</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (7)</td><td>0x267A1638</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (7) (hp_barreltip_smlroktl)</td><td>0x16379B62</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (7) (hp_barreltip_smlroktr)</td><td>0xF02CA23C</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (7) (OC)</td><td>0xE4107BF7</td><td>No</td></tr>
<tr><td>Mounted Rocket Pod (7) (R)</td><td>0xB3E3709B</td><td>No</td></tr>
<tr><td>Mounted RocketPod (Endriago) (Superiority) (L)</td><td>0x37E1FB77</td><td>No</td></tr>
<tr><td>Mounted RocketPod (Endriago) (Superiority) (R)</td><td>0x49124D35</td><td>No</td></tr>
<tr><td>Mounted SAM (1)</td><td>0xA6EAC7DC</td><td>No</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BA</td><td>0x704586F5</td><td>Yes</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BB</td><td>0x4E3E95AA</td><td>Yes</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BC</td><td>0x704109C7</td><td>Yes</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BD</td><td>0xEE39815C</td><td>Yes</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BE</td><td>0xE83BB681</td><td>Yes</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BF</td><td>0x66342E16</td><td>Yes</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BG</td><td>0xC83706F3</td><td>Yes</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BH</td><td>0x662FB0E8</td><td>Yes</td></tr>
<tr><td>Mounted Ship Gun</td><td>0xE9291BB1</td><td>Yes</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FA)</td><td>0x599E50E5</td><td>Yes</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FA) (AllCon002)</td><td>0xEAB0852D</td><td>Yes</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FB)</td><td>0x8AB23DBC</td><td>Yes</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FB) (AllCon002)</td><td>0x4E1C02CC</td><td>Yes</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FC)</td><td>0x186F1983</td><td>Yes</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FD)</td><td>0x98B92B3A</td><td>Yes</td></tr>
<tr><td>Mounted Ship Gun (Piranha) (JetExhaust)</td><td>0xD9268BDF</td><td>Yes</td></tr>
<tr><td>Mounted Ship Minigun (No model)</td><td>0xDB079345</td><td>Yes</td></tr>
<tr><td>Mounted SSM (Huangfeng FL)</td><td>0x5959102A</td><td>Yes</td></tr>
<tr><td>Mounted SSM (Huangfeng FR)</td><td>0x216999D4</td><td>Yes</td></tr>
<tr><td>Mounted SSM (Huangfeng RL)</td><td>0x440319E6</td><td>Yes</td></tr>
<tr><td>Mounted SSM (Huangfeng RR)</td><td>0xA4DEEBE8</td><td>Yes</td></tr>
<tr><td>Mounted Tank Gun (Artillery)</td><td>0x4515E1EC</td><td>Yes</td></tr>
<tr><td>Mounted Tank Gun (Cannister)</td><td>0x59B859C1</td><td>Yes</td></tr>
<tr><td>Mounted Tank Gun (Default)</td><td>0x32057B9F</td><td>Yes</td></tr>
<tr><td>Mounted Tank Gun (Sabot)</td><td>0xD2F93EBB</td><td>Yes</td></tr>
<tr><td>Mounted Tank Gun (Weak)</td><td>0x91FE83D0</td><td>Yes</td></tr>
<tr><td>Mounted TOW Missile</td><td>0x2E092CD1</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (1) (hp_barreltip_hellfire_A)</td><td>0x1EFACDA6</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (1) (hp_barreltip_hellfire_B)</td><td>0x5A2414EB</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (1) (hp_barreltip_hellfire_C)</td><td>0xCC673924</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (1) (hp_barreltip_hellfire_D)</td><td>0x078C9A89</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (1) (no model)</td><td>0x59CA8EC2</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (2) (hp_barrel_tip_a)</td><td>0x12477118</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (2) (hp_barrel_tip_b)</td><td>0x81F96051</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (2) (hp_barreltip_c)</td><td>0xB599A693</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (4) (hp_barreltip_a)</td><td>0xA2ECBCB7</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (4) (no model)</td><td>0xE74AE3BB</td><td>No</td></tr>
<tr><td>Mounted TOW Missile (no model)</td><td>0xFF4EC498</td><td>No</td></tr>
<tr><td>Mounted WZ10 Cannon</td><td>0xCEF89994</td><td>No</td></tr>
<tr><td>Mounted ZU23 Gun A</td><td>0x25A78994</td><td>No</td></tr>
<tr><td>Mounted ZU23 Gun B</td><td>0xFFA50F2B</td><td>No</td></tr>
<tr><td>MountedM60 MG</td><td>0x709B8A92</td><td>No</td></tr>
<tr><td>mr_boss_test</td><td>0xE96E444B</td><td>No</td></tr>
<tr><td>mr_boss_test2</td><td>0xD9A92C6B</td><td>No</td></tr>
<tr><td>MR_rd_10_1</td><td>0x4F81F793</td><td>No</td></tr>
<tr><td>MR_rd_10_2</td><td>0x758471FC</td><td>No</td></tr>
<tr><td>MR_rd_20_1</td><td>0xCBF63B36</td><td>No</td></tr>
<tr><td>mreeves</td><td>0xD4D44884</td><td>No</td></tr>
<tr><td>MTV (base)</td><td>0xC0D414DC</td><td>No</td></tr>
<tr><td>MTV (Cargo)</td><td>0xDE067C2D</td><td>No</td></tr>
<tr><td>MTV (Cargo) (Driver)</td><td>0x142EB3B8</td><td>No</td></tr>
<tr><td>MTV (Cargo) (Full)</td><td>0x73BDBE3F</td><td>No</td></tr>
<tr><td>MTV (Expandible Van)</td><td>0xB7495554</td><td>No</td></tr>
<tr><td>MTV (Expandible Van) (Driver)</td><td>0x5ECC34B3</td><td>No</td></tr>
<tr><td>MTV (Expandible Van) (Full)</td><td>0xD61300E0</td><td>No</td></tr>
<tr><td>MTV (Fuel)</td><td>0xDB734B8D</td><td>No</td></tr>
<tr><td>MTV (Fuel) (Driver)</td><td>0x770C9A98</td><td>No</td></tr>
<tr><td>MTV (Fuel) (Full)</td><td>0x694EB79F</td><td>No</td></tr>
<tr><td>MTV (semi)</td><td>0xA3D40E0B</td><td>No</td></tr>
<tr><td>MTV (semi) (Driver)</td><td>0xAECCD2A6</td><td>No</td></tr>
<tr><td>MTV_Driver</td><td>0x6B984FB9</td><td>No</td></tr>
<tr><td>MTVExpandibleVan_Driver</td><td>0x43570A2C</td><td>No</td></tr>
<tr><td>Munitions (Artillery Ch)</td><td>0x048E9847</td><td>No</td></tr>
<tr><td>Munitions (Artillery Gr)</td><td>0x8596C18D</td><td>No</td></tr>
<tr><td>Munitions (Artillery Laptop)</td><td>0x4C7050FC</td><td>No</td></tr>
<tr><td>Munitions (Artillery VZ)</td><td>0x331E75EC</td><td>No</td></tr>
<tr><td>Munitions (Artillery)</td><td>0x65BFA29A</td><td>No</td></tr>
<tr><td>Munitions (Bombing Run Al)</td><td>0xFAEE8B68</td><td>No</td></tr>
<tr><td>Munitions (Bombing Run Ch)</td><td>0xDA9C40F6</td><td>No</td></tr>
<tr><td>Munitions (Bombing Run OC)</td><td>0x8A4F9C3F</td><td>No</td></tr>
<tr><td>Munitions (Bombing Run VZ)</td><td>0x848DCD31</td><td>No</td></tr>
<tr><td>Munitions (Bombing Run)</td><td>0xE9B43425</td><td>No</td></tr>
<tr><td>Munitions (Bunker Buster Al)</td><td>0xFBA255D9</td><td>No</td></tr>
<tr><td>Munitions (Bunker Buster)</td><td>0xF38C2502</td><td>No</td></tr>
<tr><td>Munitions (Carpet Bomb)</td><td>0x3724C6AD</td><td>No</td></tr>
<tr><td>Munitions (Cluster Bomb OC)</td><td>0x6904D454</td><td>No</td></tr>
<tr><td>Munitions (Cluster Bomb VZ)</td><td>0x446E9D12</td><td>No</td></tr>
<tr><td>Munitions (Cluster Bomb)</td><td>0x768E6A44</td><td>No</td></tr>
<tr><td>Munitions (Combat Air Patrol Al)</td><td>0x4DBD93DD</td><td>No</td></tr>
<tr><td>Munitions (Combat Air Patrol Ch)</td><td>0x77F9645B</td><td>No</td></tr>
<tr><td>Munitions (Combat Air Patrol)</td><td>0x47590DD6</td><td>No</td></tr>
<tr><td>Munitions (Cruise Missile)</td><td>0x2B8222D5</td><td>No</td></tr>
<tr><td>Munitions (Daisy Cutter Al)</td><td>0x456B6262</td><td>No</td></tr>
<tr><td>Munitions (Daisy Cutter)</td><td>0x7D29FEE3</td><td>No</td></tr>
<tr><td>Munitions (Fuel-Air Bomb Ch)</td><td>0x839F8C84</td><td>No</td></tr>
<tr><td>Munitions (Fuel-Air Bomb)</td><td>0xC55F371B</td><td>No</td></tr>
<tr><td>Munitions (HARM)</td><td>0x8977BD24</td><td>No</td></tr>
<tr><td>Munitions (Laptop)</td><td>0x5DFA6876</td><td>No</td></tr>
<tr><td>Munitions (Laser Guided Bomb Al)</td><td>0xA4056FFE</td><td>No</td></tr>
<tr><td>Munitions (Laser Guided Bomb Ch)</td><td>0x47323650</td><td>No</td></tr>
<tr><td>Munitions (Laser Guided Bomb)</td><td>0xA1FEDF6F</td><td>No</td></tr>
<tr><td>Munitions (MOAB)</td><td>0xCF23B9A5</td><td>No</td></tr>
<tr><td>Munitions (Rocket Artillery Ch)</td><td>0xBF0E49A1</td><td>No</td></tr>
<tr><td>Munitions (Rocket Artillery)</td><td>0x98EA2ECC</td><td>No</td></tr>
<tr><td>Munitions (Smart Bomb)</td><td>0x67D0E315</td><td>No</td></tr>
<tr><td>Munitions (Strategic Missile)</td><td>0x3BCF38A2</td><td>No</td></tr>
<tr><td>Munitions (Surgical Strike Al)</td><td>0x62C3BD57</td><td>No</td></tr>
<tr><td>Munitions (Surgical Strike Ch)</td><td>0xC8602D19</td><td>No</td></tr>
<tr><td>Munitions (Surgical Strike)</td><td>0xB4F78D44</td><td>No</td></tr>
<tr><td>Munitions (Tank Buster Al)</td><td>0xC17825EC</td><td>Yes</td></tr>
<tr><td>Munitions (Tank Buster Ch)</td><td>0xA80BDD22</td><td>Yes</td></tr>
<tr><td>Munitions (Tank Buster VZ)</td><td>0x5B3B80D5</td><td>Yes</td></tr>
<tr><td>Munitions (Tank Buster)</td><td>0x57EBF5C9</td><td>Yes</td></tr>
<tr><td>Munitions Spawner (Al Passcodes)</td><td>0x81BF38EA</td><td>No</td></tr>
<tr><td>Munitions Spawner (Al)</td><td>0x21104E27</td><td>No</td></tr>
<tr><td>Munitions Spawner (Ch)</td><td>0x86ACBDE9</td><td>No</td></tr>
<tr><td>Munitions Spawner (Default)</td><td>0xBDC66D51</td><td>No</td></tr>
<tr><td>Munitions Spawner (Gr)</td><td>0x4CBD7F53</td><td>No</td></tr>
<tr><td>Munitions Spawner (OC)</td><td>0xA5980AE4</td><td>No</td></tr>
<tr><td>Munitions Spawner (VZ)</td><td>0x5DAB2762</td><td>No</td></tr>
<tr><td>Munitions Spawnlist (Al Passcodes)</td><td>0x917C7A09</td><td>No</td></tr>
<tr><td>Munitions Spawnlist (Al)</td><td>0xBED90AC0</td><td>No</td></tr>
<tr><td>Munitions Spawnlist (Ch)</td><td>0x21613C2E</td><td>No</td></tr>
<tr><td>Munitions Spawnlist (Gr)</td><td>0x36548AB8</td><td>No</td></tr>
<tr><td>Munitions Spawnlist (OC)</td><td>0x09B182B7</td><td>No</td></tr>
<tr><td>Munitions Spawnlist (Test)</td><td>0x7FE13D29</td><td>No</td></tr>
<tr><td>Munitions Spawnlist (VZ)</td><td>0x8828FF69</td><td>No</td></tr>
<tr><td>Muzzle Flash (RR)</td><td>0x7EAC3B61</td><td>No</td></tr>
<tr><td>New Template 0x80008a02</td><td>0x4E62D16C</td><td>No</td></tr>
<tr><td>New Template 0x80008a09</td><td>0xC84C382B</td><td>No</td></tr>
<tr><td>New Template 0x800097ff</td><td>0xB8307A83</td><td>No</td></tr>
<tr><td>New Template 0x8000b01e</td><td>0xF06FFCAF</td><td>No</td></tr>
<tr><td>New Terrain</td><td>0xC221E8F2</td><td>No</td></tr>
<tr><td>New Terrain (Large)</td><td>0x479273EC</td><td>No</td></tr>
<tr><td>New Terrain (medium)</td><td>0xA40E7C64</td><td>No</td></tr>
<tr><td>New Terrain (Small)</td><td>0x7B8D4CA4</td><td>No</td></tr>
<tr><td>NGLV</td><td>0xAEE02F3A</td><td>No</td></tr>
<tr><td>NGLV (GL)</td><td>0xD2EA92D0</td><td>No</td></tr>
<tr><td>NGLV (GL) (Driver)</td><td>0x4E0AF86F</td><td>No</td></tr>
<tr><td>NGLV (GL) (DriverGunner)</td><td>0x27A05248</td><td>No</td></tr>
<tr><td>NGLV (GL) (Full)</td><td>0x782AE2A4</td><td>No</td></tr>
<tr><td>NGLV (MG)</td><td>0xDBDEC16F</td><td>No</td></tr>
<tr><td>NGLV (MG) (Driver)</td><td>0x909DD79A</td><td>No</td></tr>
<tr><td>NGLV (MG) (DriverGunner)</td><td>0x69264E99</td><td>No</td></tr>
<tr><td>NGLV (MG) (Full)</td><td>0x48E47D59</td><td>No</td></tr>
<tr><td>NGLV_Driver</td><td>0x2EB0A1EB</td><td>No</td></tr>
<tr><td>Night Vision Elite</td><td>0xCF703D6A</td><td>No</td></tr>
<tr><td>NM SS</td><td>0xC353AD20</td><td>No</td></tr>
<tr><td>Nuclear Bunker Buster Projectile</td><td>0x4BBAE398</td><td>No</td></tr>
<tr><td>OC</td><td>0xE947B797</td><td>No</td></tr>
<tr><td>OC Board Member</td><td>0x164999FF</td><td>No</td></tr>
<tr><td>OC Boss</td><td>0x5885B432</td><td>No</td></tr>
<tr><td>OC Boss (phone)</td><td>0xBD427E13</td><td>No</td></tr>
<tr><td>OC Boss Phone</td><td>0x4FF6C2FE</td><td>No</td></tr>
<tr><td>OC Defender (AA)</td><td>0xE6653D0B</td><td>No</td></tr>
<tr><td>OC Defender (AT)</td><td>0x5412C040</td><td>No</td></tr>
<tr><td>OC Defender (AT) (Window Spawner)</td><td>0x5D885C09</td><td>No</td></tr>
<tr><td>OC Defender (MG)</td><td>0xA8573F8D</td><td>No</td></tr>
<tr><td>OC Defender (Rifle)</td><td>0x5F9983AF</td><td>No</td></tr>
<tr><td>OC Defender (Sniper)</td><td>0x02CC7BAE</td><td>No</td></tr>
<tr><td>OC Elite</td><td>0x3225BF3A</td><td>No</td></tr>
<tr><td>OC Exec Box</td><td>0x997A0FF5</td><td>No</td></tr>
<tr><td>OC Executive</td><td>0xE0428861</td><td>No</td></tr>
<tr><td>OC Executive (Armed)</td><td>0x8962059B</td><td>No</td></tr>
<tr><td>OC Executive (Box)</td><td>0x31A786AD</td><td>No</td></tr>
<tr><td>OC Executive (Crying)</td><td>0xD3817D3E</td><td>No</td></tr>
<tr><td>OC Executive (Female)</td><td>0xDDAF8A12</td><td>No</td></tr>
<tr><td>OC Executive (OilCon002_Hostage)</td><td>0xA25CDC6C</td><td>No</td></tr>
<tr><td>OC Executive (Phone)</td><td>0x8B29C584</td><td>No</td></tr>
<tr><td>OC Executive (Shredder)</td><td>0x76B9F9CF</td><td>No</td></tr>
<tr><td>OC Firefighter</td><td>0xF63D05CC</td><td>No</td></tr>
<tr><td>OC Heavy (Grenade Launcher)</td><td>0x4A53C685</td><td>No</td></tr>
<tr><td>OC Heavy (Light MG)</td><td>0x15348807</td><td>No</td></tr>
<tr><td>OC Heavy (RPG)</td><td>0x35DF2250</td><td>No</td></tr>
<tr><td>OC Lifestyle Starter</td><td>0x77547833</td><td>No</td></tr>
<tr><td>OC Officer</td><td>0xA68AA209</td><td>No</td></tr>
<tr><td>OC Pilot</td><td>0x42552FF1</td><td>No</td></tr>
<tr><td>OC Prisoner</td><td>0x0F073CB1</td><td>No</td></tr>
<tr><td>OC Sniper</td><td>0x07E46DF4</td><td>No</td></tr>
<tr><td>OC Soldier</td><td>0x07B00AAD</td><td>No</td></tr>
<tr><td>OC Soldier (Bench Press)</td><td>0xBB217A61</td><td>No</td></tr>
<tr><td>OC Soldier (God)</td><td>0xEDD00DA2</td><td>No</td></tr>
<tr><td>OC Soldier (Saunter)</td><td>0x8E0FD15E</td><td>No</td></tr>
<tr><td>OC Starter 1</td><td>0x05323547</td><td>No</td></tr>
<tr><td>OC Starter 2</td><td>0xDB3431C0</td><td>No</td></tr>
<tr><td>OC Starter 3</td><td>0x0536B275</td><td>No</td></tr>
<tr><td>OC Starter 4</td><td>0xFB255996</td><td>No</td></tr>
<tr><td>OC Starters</td><td>0x10120EDD</td><td>No</td></tr>
<tr><td>OC Tank Commander</td><td>0xD0F85B6F</td><td>Yes</td></tr>
<tr><td>OC Worker</td><td>0x2D571F27</td><td>No</td></tr>
<tr><td>OCDepotWarehouseSpawner</td><td>0x2D530F48</td><td>No</td></tr>
<tr><td>OCHQ Paper</td><td>0xAA9D345C</td><td>No</td></tr>
<tr><td>OCHQSpawnList</td><td>0x6C57EA0B</td><td>No</td></tr>
<tr><td>OCHQVehicleSpawnList</td><td>0xCC4C5D33</td><td>No</td></tr>
<tr><td>OCMercSpawnList</td><td>0x134119C9</td><td>No</td></tr>
<tr><td>OCPedTraffic</td><td>0x3A988AAD</td><td>No</td></tr>
<tr><td>OCVehTraffic</td><td>0xAFD1C1E3</td><td>No</td></tr>
<tr><td>Offroad Motorcycle (AI ONLY)</td><td>0xF6B714A8</td><td>Yes</td></tr>
<tr><td>Offroad Motorcycle (AL)</td><td>0xA52A5783</td><td>Yes</td></tr>
<tr><td>Offroad Motorcycle (AL) (Driver)</td><td>0x3975175E</td><td>Yes</td></tr>
<tr><td>Offroad Motorcycle (GR)</td><td>0xFE3B86CF</td><td>Yes</td></tr>
<tr><td>Offroad Motorcycle (GR) (Driver)</td><td>0x82F76DFA</td><td>Yes</td></tr>
<tr><td>OffroadMotorcycle_Driver</td><td>0x1E0A049E</td><td>Yes</td></tr>
<tr><td>Ofroad Motorcycle</td><td>0x1AE863DB</td><td>Yes</td></tr>
<tr><td>Oil Tanker (OC)</td><td>0x73554933</td><td>Yes</td></tr>
<tr><td>OilCon020_Carbine</td><td>0x768BB7FE</td><td>No</td></tr>
<tr><td>OilCon020_Carbine_b</td><td>0x2DEED175</td><td>No</td></tr>
<tr><td>OilDbSpawner</td><td>0xF10AD117</td><td>No</td></tr>
<tr><td>OilDbSpawner (Squad Full AT)</td><td>0x9EC1D98A</td><td>No</td></tr>
<tr><td>OilDbSpawner (Squad Half AT)</td><td>0xE672B662</td><td>No</td></tr>
<tr><td>OilDbSpawner (Squad Quarter AT)</td><td>0xA4607BBF</td><td>No</td></tr>
<tr><td>OilDbSpawner (Squad)</td><td>0x5F97BBDC</td><td>No</td></tr>
<tr><td>OilHq_Interior</td><td>0x3FAAFEE5</td><td>No</td></tr>
<tr><td>oilrig</td><td>0x7ED017FB</td><td>No</td></tr>
<tr><td>oilrig buildings</td><td>0x8ED2A0D4</td><td>No</td></tr>
<tr><td>oilrig_att_anchorlinegrillA</td><td>0x9D98438E</td><td>No</td></tr>
<tr><td>oilrig_att_anchorlinespindleA</td><td>0x3C05E445</td><td>No</td></tr>
<tr><td>oilrig_att_BuildingDpipe</td><td>0x2CC316D6</td><td>No</td></tr>
<tr><td>oilrig_att_dockingrampA</td><td>0x7B5578A2</td><td>No</td></tr>
<tr><td>oilrig_att_dockingrampB</td><td>0xFD5D010D</td><td>No</td></tr>
<tr><td>oilrig_att_ductdisposalA</td><td>0x2C874C90</td><td>No</td></tr>
<tr><td>oilrig_att_pipeblowout</td><td>0x8E4E954A</td><td>No</td></tr>
<tr><td>oilrig_att_towerdrillpipesA</td><td>0xF021B3A4</td><td>No</td></tr>
<tr><td>oilrig_att_towerdrillpipesB</td><td>0x0A1F9DFB</td><td>No</td></tr>
<tr><td>oilrig_bld_buildingA</td><td>0xD23F52FC</td><td>No</td></tr>
<tr><td>oilrig_bld_buildingB</td><td>0xAC3CD893</td><td>No</td></tr>
<tr><td>oilrig_bld_buildingBB</td><td>0x3D7B1AD3</td><td>No</td></tr>
<tr><td>oilrig_bld_buildingC</td><td>0xCA3AC936</td><td>No</td></tr>
<tr><td>oilrig_bld_buildingD</td><td>0xD44C2215</td><td>No</td></tr>
<tr><td>oilrig_bld_helipadlargeA</td><td>0x4DDC8DF8</td><td>Yes</td></tr>
<tr><td>oilrig_catwalkA</td><td>0xC2EEF876</td><td>No</td></tr>
<tr><td>oilrig_catwalkB</td><td>0x44F680E1</td><td>No</td></tr>
<tr><td>oilrig_catwalkC</td><td>0xCAF3823C</td><td>No</td></tr>
<tr><td>oilrig_catwalkD</td><td>0x4CFB0AA7</td><td>No</td></tr>
<tr><td>oilrig_cranelargeA</td><td>0x16970F43</td><td>No</td></tr>
<tr><td>oilrig_cranesmallA</td><td>0x3925E07B</td><td>No</td></tr>
<tr><td>oilrig_radiojammer</td><td>0x786ECF9F</td><td>No</td></tr>
<tr><td>oilrig_radiojammer_ruined</td><td>0xB96B4243</td><td>No</td></tr>
<tr><td>oilrig_scaffold</td><td>0x68B59E68</td><td>No</td></tr>
<tr><td>oilrig_simple</td><td>0x618526A4</td><td>No</td></tr>
<tr><td>oilrig_simple_ruined</td><td>0x9C06A4B2</td><td>No</td></tr>
<tr><td>oilrig_smokestack</td><td>0x9A6F6587</td><td>No</td></tr>
<tr><td>oilrig_stairwellA</td><td>0xFA1394CE</td><td>No</td></tr>
<tr><td>oilrig_stairwellB</td><td>0x5C1AEAD9</td><td>No</td></tr>
<tr><td>oilrig_stairwellC</td><td>0x02181E94</td><td>No</td></tr>
<tr><td>oilrig_stairwellD</td><td>0x641F749F</td><td>No</td></tr>
<tr><td>oilrig_stairwellE</td><td>0x821D6542</td><td>No</td></tr>
<tr><td>oilrig_stairwellF</td><td>0x0424EDAD</td><td>No</td></tr>
<tr><td>oilrig_stairwellG</td><td>0xDA226CF8</td><td>No</td></tr>
<tr><td>oilrig_stairwellH</td><td>0xFC295E43</td><td>No</td></tr>
<tr><td>oilrig_towerblowoutdiagonal</td><td>0x8566262E</td><td>No</td></tr>
<tr><td>oilrig_towerblowoutlargeA</td><td>0xBD858E29</td><td>No</td></tr>
<tr><td>oilrig_towerblowoutsmallA</td><td>0xE85D130D</td><td>No</td></tr>
<tr><td>oilrig_towerdrill</td><td>0x299798D8</td><td>No</td></tr>
<tr><td>OilrigDebris</td><td>0x2E56EC4A</td><td>No</td></tr>
<tr><td>OilrigDebrisLarge</td><td>0x6A3605FB</td><td>No</td></tr>
<tr><td>OilrigDebrisLong</td><td>0xA301CD08</td><td>No</td></tr>
<tr><td>OilrigDebrisMedium</td><td>0xA53995D3</td><td>No</td></tr>
<tr><td>OilrigDebrisMediumFloat</td><td>0x29DF5B4F</td><td>No</td></tr>
<tr><td>OilrigDebrisSmall</td><td>0xEFD97A93</td><td>No</td></tr>
<tr><td>OLD DO NOT USE gr_veh_tank_m551sheridan</td><td>0x22682C0C</td><td>Yes</td></tr>
<tr><td>Omen</td><td>0xCB516D9C</td><td>No</td></tr>
<tr><td>Omen (Driver)</td><td>0x53DF6F5B</td><td>No</td></tr>
<tr><td>Omen (Full)</td><td>0x39546958</td><td>No</td></tr>
<tr><td>Omen (Full) (OC)</td><td>0x195C2497</td><td>No</td></tr>
<tr><td>Omen (OC) (DriverGunner)</td><td>0xA6E1016D</td><td>No</td></tr>
<tr><td>Opentop Trailer</td><td>0x6F4EE91B</td><td>No</td></tr>
<tr><td>OutskirtsTraffic</td><td>0x3ED61736</td><td>No</td></tr>
<tr><td>OutskirtTrafficZone</td><td>0x7582021D</td><td>No</td></tr>
<tr><td>PalmTreeDebrisTemplate</td><td>0x53FE886A</td><td>No</td></tr>
<tr><td>Panel Damage (Car)</td><td>0x18D60B8B</td><td>No</td></tr>
<tr><td>Panhard</td><td>0x47924871</td><td>No</td></tr>
<tr><td>Panhard (Assault)</td><td>0x449BB52B</td><td>No</td></tr>
<tr><td>Panhard (base)</td><td>0xD3D29EAF</td><td>No</td></tr>
<tr><td>Panhard_Driver</td><td>0xDBCF4D8A</td><td>No</td></tr>
<tr><td>ParachuteA</td><td>0x61024957</td><td>No</td></tr>
<tr><td>Paradrop Location (AL)</td><td>0xA34D87BB</td><td>No</td></tr>
<tr><td>Paradrop Location (CH)</td><td>0x2BEE94C5</td><td>No</td></tr>
<tr><td>ParkedCarList</td><td>0x7901B2E0</td><td>No</td></tr>
<tr><td>ParkingSpawner</td><td>0x361E6E2D</td><td>No</td></tr>
<tr><td>PathSpawner1</td><td>0x107FF8ED</td><td>No</td></tr>
<tr><td>PathSpawner_AlliedHQ_PedList</td><td>0x5A4D3ABD</td><td>No</td></tr>
<tr><td>PathSpawner_Boat_Amazon_Act1</td><td>0xEA6FF3F2</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Amazon_Act2</td><td>0x6C777C5D</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act1_A</td><td>0xD326695A</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act1_B</td><td>0x352DBF65</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act1_C</td><td>0xCB2AD9F0</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act2_Allied</td><td>0xD9C80A41</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act2_China</td><td>0xDEF109A9</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act3_Allied</td><td>0x4F90EB72</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act3_China</td><td>0x93E6C2C0</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Cumana_Act1_A</td><td>0xC234DE49</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Cumana_Act1_B</td><td>0x202D237E</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Cumana_Act1_C</td><td>0x422F979B</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Cumana_Act2_China</td><td>0xB5651806</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_JungleMtn_Act1</td><td>0xF7D0FF94</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_JungleMtn_Act2</td><td>0xD1CE852B</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act1_A</td><td>0x2C56E3D4</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act1_B</td><td>0x0654696B</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act1_C</td><td>0x24525A0E</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act1_D</td><td>0x2E63B2ED</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act2</td><td>0x82E10253</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act3</td><td>0xA0DEF2F6</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Merida_Act1</td><td>0x2783AD86</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_Merida_Act2</td><td>0xA98B35F1</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_OC_Depot_Act1</td><td>0x49FFA4B5</td><td>Yes</td></tr>
<tr><td>PathSpawner_Boat_PirateIsles_Act1_A</td><td>0xD45B17A5</td><td>Yes</td></tr>
<tr><td>PathSpawner_ChiHQ_PedList</td><td>0x34E8DA10</td><td>No</td></tr>
<tr><td>PathSpawner_GurHQ_PedList</td><td>0x2E9E9CD8</td><td>No</td></tr>
<tr><td>PathSpawner_GurHQ_VehList</td><td>0x76FC6D8A</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Car_City_Act1</td><td>0x502D8994</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Car_City_Act2</td><td>0x2A2B0F2B</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Car_City_Act3_Allied</td><td>0x1B4FA27C</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Car_City_Act3_China</td><td>0x05CC2646</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Cumana_Act1_China</td><td>0xE03AF933</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Cumana_Act2_China</td><td>0xF217B55C</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_JungleMtn_Act1</td><td>0xB17B15DE</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Mar_City_Act1</td><td>0xA0B53D36</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Mar_City_Act2</td><td>0x22BCC5A1</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Mar_City_Act3</td><td>0xA8B9C6FC</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Merida_Act1</td><td>0x51B9C050</td><td>Yes</td></tr>
<tr><td>PathSpawner_Heli_Merida_Act2</td><td>0x3BB75F17</td><td>Yes</td></tr>
<tr><td>PathSpawner_OCHQ_Depot_PedList</td><td>0x50B01295</td><td>No</td></tr>
<tr><td>PathSpawner_Pirate_Jetski</td><td>0x4D147C27</td><td>No</td></tr>
<tr><td>PathSpawner_Pirate_VehList</td><td>0x8EC67A18</td><td>Yes</td></tr>
<tr><td>PathSpawner_PirateHQ_PedList</td><td>0x6B567E2B</td><td>No</td></tr>
<tr><td>PathSpawner_PMC001_Stairs01</td><td>0x4811DE86</td><td>No</td></tr>
<tr><td>PathSpawner_VZCon001_M151</td><td>0x351C54B5</td><td>Yes</td></tr>
<tr><td>PathSpawner_VZCon001_PedList</td><td>0xF61AA94C</td><td>No</td></tr>
<tr><td>PathSpawners</td><td>0xEFDBE59F</td><td>No</td></tr>
<tr><td>Patrol Boat (base)</td><td>0x74FC9169</td><td>Yes</td></tr>
<tr><td>Patrol Boat (PMC)</td><td>0x1D9FC746</td><td>Yes</td></tr>
<tr><td>Patrol Boat (PMC) (Driver)</td><td>0x180E875D</td><td>Yes</td></tr>
<tr><td>Patrol Boat (VZ)</td><td>0xBB5331F4</td><td>Yes</td></tr>
<tr><td>Patrol Boat (VZ) (Driver)</td><td>0x9D326D53</td><td>Yes</td></tr>
<tr><td>Patrol Boat (VZ) (DriverGunners)</td><td>0xD749939B</td><td>Yes</td></tr>
<tr><td>Patrol Boat (VZ) (Full)</td><td>0x26BC0400</td><td>Yes</td></tr>
<tr><td>Patrolboat_Driver</td><td>0x918E1442</td><td>Yes</td></tr>
<tr><td>PatrolboatVZ_Driver</td><td>0x915322FE</td><td>Yes</td></tr>
<tr><td>PatrolSpawner</td><td>0xD7D9C119</td><td>No</td></tr>
<tr><td>PD Soldier</td><td>0xD18E58CB</td><td>No</td></tr>
<tr><td>PDA</td><td>0xFA62754E</td><td>No</td></tr>
<tr><td>PedList_AllCon002_Traffic</td><td>0x94BDB230</td><td>No</td></tr>
<tr><td>PedList_AlliedHQ_Paths</td><td>0xA9BB4F26</td><td>No</td></tr>
<tr><td>PedList_AllJob001</td><td>0x28D493F2</td><td>No</td></tr>
<tr><td>PedList_Amazon_Act1</td><td>0xAE54EA83</td><td>No</td></tr>
<tr><td>PedList_Amazon_AllJob002_i_Act1</td><td>0xE634825C</td><td>No</td></tr>
<tr><td>PedList_Blank</td><td>0x2C5096CB</td><td>No</td></tr>
<tr><td>PedList_Car_Big_Act1</td><td>0xBCFC6CE6</td><td>No</td></tr>
<tr><td>PedList_Car_City_Act1</td><td>0xE27F610F</td><td>No</td></tr>
<tr><td>PedList_Car_City_Act2ALL</td><td>0xF3F707B9</td><td>No</td></tr>
<tr><td>PedList_Car_City_Act2CHI</td><td>0x52E973E6</td><td>No</td></tr>
<tr><td>PedList_Car_City_Act3ALL</td><td>0x36FED14A</td><td>No</td></tr>
<tr><td>PedList_Car_City_Act3CHI</td><td>0x7581CD7D</td><td>No</td></tr>
<tr><td>PedList_Car_Dock_Act1</td><td>0x4C179CFF</td><td>No</td></tr>
<tr><td>PedList_Car_Estate_Act1</td><td>0x5A8CF76C</td><td>No</td></tr>
<tr><td>PedList_Car_Shanty_Act1</td><td>0xAD11F307</td><td>No</td></tr>
<tr><td>PedList_ChiHQ_Paths</td><td>0x6E079873</td><td>No</td></tr>
<tr><td>PedList_Cumana_act1ALL</td><td>0x5E724CE9</td><td>No</td></tr>
<tr><td>PedList_Cumana_Act1CHI</td><td>0xBD64B916</td><td>No</td></tr>
<tr><td>PedList_Cumana_act2ALL</td><td>0x17B486D0</td><td>No</td></tr>
<tr><td>PedList_Cumana_act2CHI</td><td>0x19426E67</td><td>No</td></tr>
<tr><td>PedList_Cumana_City_Act1</td><td>0xE591C396</td><td>No</td></tr>
<tr><td>PedList_Cumana_Outskirts_Act1</td><td>0x23D326B7</td><td>No</td></tr>
<tr><td>PedList_Guanare_Act1</td><td>0xAD750756</td><td>No</td></tr>
<tr><td>PedList_Guanare_Big_Act1</td><td>0x20BCB8BB</td><td>No</td></tr>
<tr><td>PedList_GurHQ_Paths</td><td>0xDFDBF3CB</td><td>No</td></tr>
<tr><td>PedList_JungleMtnA_Act1</td><td>0x00E37D92</td><td>No</td></tr>
<tr><td>PedList_JungleMtnB_Act1</td><td>0x32B64927</td><td>No</td></tr>
<tr><td>PedList_Mar_Altagracia_Act1</td><td>0x94F73793</td><td>No</td></tr>
<tr><td>PedList_Mar_Altagracia_Act2</td><td>0xBAF9B1FC</td><td>No</td></tr>
<tr><td>PedList_Mar_Big_Act1</td><td>0xE0A7B124</td><td>No</td></tr>
<tr><td>PedList_Mar_City_Act1</td><td>0x950F6EE5</td><td>No</td></tr>
<tr><td>PedList_Mar_City_Act2</td><td>0x330818DA</td><td>No</td></tr>
<tr><td>PedList_Mar_City_Act3</td><td>0x150A2837</td><td>No</td></tr>
<tr><td>PedList_Mar_City_Act4</td><td>0x93029FCC</td><td>No</td></tr>
<tr><td>PedList_Mar_Industrial_Act1</td><td>0xE2755041</td><td>No</td></tr>
<tr><td>PedList_Mar_Industrial_Act2</td><td>0x606DC7D6</td><td>No</td></tr>
<tr><td>PedList_Mar_Industrial_Act3</td><td>0xC270A0B3</td><td>No</td></tr>
<tr><td>PedList_Mar_Outskirt_Act1</td><td>0x6E384A11</td><td>No</td></tr>
<tr><td>PedList_Mar_Village_Act1</td><td>0x1EA86682</td><td>No</td></tr>
<tr><td>PedList_Margarita_Act1</td><td>0x983F54CB</td><td>No</td></tr>
<tr><td>PedList_Mer_Big_Act1</td><td>0xC137BD20</td><td>No</td></tr>
<tr><td>PedList_Mer_City_Act1</td><td>0x22F441D9</td><td>No</td></tr>
<tr><td>PedList_Mer_City_Act2</td><td>0xC0ECEBCE</td><td>No</td></tr>
<tr><td>PedList_Mer_City_Act3</td><td>0xA2EEFB2B</td><td>No</td></tr>
<tr><td>PedList_Mer_City_Act4</td><td>0xA0FBC3F8</td><td>No</td></tr>
<tr><td>PedList_Mer_Outskirt_Act1</td><td>0x3F8CEA6D</td><td>No</td></tr>
<tr><td>PedList_OilDepot_Paths</td><td>0xBA16CBA0</td><td>No</td></tr>
<tr><td>PedList_PirateHQ_Paths</td><td>0xA3DA8CA4</td><td>No</td></tr>
<tr><td>PedList_Protester</td><td>0xAD0D6299</td><td>No</td></tr>
<tr><td>PedList_VZCon001</td><td>0xB9445ADE</td><td>No</td></tr>
<tr><td>PEP Rocket</td><td>0x642E5554</td><td>No</td></tr>
<tr><td>PGZ95</td><td>0x76BE6D86</td><td>Yes</td></tr>
<tr><td>PGZ95 (base)</td><td>0x2213B43A</td><td>Yes</td></tr>
<tr><td>PGZ95 (Driver)</td><td>0x2157351D</td><td>Yes</td></tr>
<tr><td>PGZ95 Command</td><td>0x19CCC8A1</td><td>Yes</td></tr>
<tr><td>PGZ95 Command (Driver)</td><td>0x87E43EBC</td><td>Yes</td></tr>
<tr><td>Phoenix</td><td>0xA516ABB2</td><td>No</td></tr>
<tr><td>Phoenix (crappy)</td><td>0xCA2E0D98</td><td>No</td></tr>
<tr><td>Phoenix (crappy) (Driver) (Civ Poor female)</td><td>0x5B8D933C</td><td>No</td></tr>
<tr><td>Phoenix (crappy) (Driver) (Civ Poor male)</td><td>0x9794874D</td><td>No</td></tr>
<tr><td>Phoenix (Driver)</td><td>0x40442DD9</td><td>No</td></tr>
<tr><td>Phoenix (Driver) (Civ Poor female)</td><td>0xB76B085E</td><td>No</td></tr>
<tr><td>Phoenix (Driver) (Civ Poor male)</td><td>0xCCD52953</td><td>No</td></tr>
<tr><td>Phoenix (racing)</td><td>0x753E9DA1</td><td>No</td></tr>
<tr><td>Phoenix (racing) (Driver)</td><td>0x9CB16DBC</td><td>No</td></tr>
<tr><td>Phoenix (racing) (Driver) (Civ Motorcycle male)</td><td>0x21FF7645</td><td>Yes</td></tr>
<tr><td>Phoenix_Driver</td><td>0x8B4A7993</td><td>No</td></tr>
<tr><td>Phoenix_Driver (tight)</td><td>0xF765B0B2</td><td>No</td></tr>
<tr><td>Phoenix_Ruin</td><td>0x9F2A637B</td><td>No</td></tr>
<tr><td>Phoenix_Ruin_Fire</td><td>0xE80D5226</td><td>No</td></tr>
<tr><td>PhoenixTestRoad20m</td><td>0x87040FE3</td><td>No</td></tr>
<tr><td>Physics Crashable (car)</td><td>0x677F3B2A</td><td>No</td></tr>
<tr><td>Physics Crashable (tank)</td><td>0x0C30201A</td><td>Yes</td></tr>
<tr><td>Physics Crashable (truck)</td><td>0xDC31BC5F</td><td>Yes</td></tr>
<tr><td>Pickup (Cash)</td><td>0x5BF2AB21</td><td>No</td></tr>
<tr><td>PickupList1</td><td>0x07D0880E</td><td>No</td></tr>
<tr><td>piece_building2x2x2</td><td>0x8E32F426</td><td>No</td></tr>
<tr><td>Pirahna (GurCon003)</td><td>0x2D1EEE58</td><td>No</td></tr>
<tr><td>Piranha</td><td>0x42C221BA</td><td>Yes</td></tr>
<tr><td>Piranha (Driver)</td><td>0xB4B4BCE1</td><td>Yes</td></tr>
<tr><td>Piranha (DriverGunner)</td><td>0xFB99B032</td><td>Yes</td></tr>
<tr><td>Piranha (Full)</td><td>0x9CA00276</td><td>Yes</td></tr>
<tr><td>Piranha Jet Exhaust ammo</td><td>0x75E63C99</td><td>Yes</td></tr>
<tr><td>Piranha_Driver</td><td>0xE4DF656B</td><td>Yes</td></tr>
<tr><td>Pirate</td><td>0xC18215FE</td><td>No</td></tr>
<tr><td>Pirate Officer</td><td>0x07E00634</td><td>No</td></tr>
<tr><td>Pirate Officer (RPG)</td><td>0xBA29E876</td><td>No</td></tr>
<tr><td>Pirate Pilot</td><td>0x5E78D2CC</td><td>No</td></tr>
<tr><td>Pirate Prisoner</td><td>0x76A386FE</td><td>No</td></tr>
<tr><td>Pirate Sailor</td><td>0xFCE48F72</td><td>No</td></tr>
<tr><td>Pirate Sailor (Drinker)</td><td>0xD776EAD6</td><td>No</td></tr>
<tr><td>Pirate Starter 01</td><td>0x10855284</td><td>No</td></tr>
<tr><td>Pirate Starter 02</td><td>0xAA82735B</td><td>No</td></tr>
<tr><td>Pirate Starter 03</td><td>0x887FFF3E</td><td>No</td></tr>
<tr><td>Pirate Starter 04</td><td>0x9291581D</td><td>No</td></tr>
<tr><td>Pirate Starter 05</td><td>0xA88F3C28</td><td>No</td></tr>
<tr><td>Pirate Thug</td><td>0x9DC036EA</td><td>No</td></tr>
<tr><td>Pirate Thug (AA)</td><td>0x91188C81</td><td>No</td></tr>
<tr><td>Pirate Thug (Female AA)</td><td>0x6B347CE1</td><td>No</td></tr>
<tr><td>Pirate Thug (Female)</td><td>0xD1FEF2C7</td><td>No</td></tr>
<tr><td>Pirate Thug (God)</td><td>0x70CC53F9</td><td>No</td></tr>
<tr><td>Pirate Thug (RPG)</td><td>0x28CF4EB4</td><td>No</td></tr>
<tr><td>Pirate Thug (Shotgun)</td><td>0x136BD415</td><td>No</td></tr>
<tr><td>Pirate Traffic</td><td>0xCA85ABA9</td><td>No</td></tr>
<tr><td>Pirate Worker</td><td>0x226333BC</td><td>No</td></tr>
<tr><td>Pirate Worker (Cell Phone)</td><td>0xA6B03989</td><td>No</td></tr>
<tr><td>PirDbSpawner</td><td>0x95E72680</td><td>No</td></tr>
<tr><td>PirDbSpawner (Squad Full AT)</td><td>0x23A81C25</td><td>No</td></tr>
<tr><td>PirDbSpawner (Squad Half AT)</td><td>0x98ED8089</td><td>No</td></tr>
<tr><td>PirDbSpawner (Squad Quarter AT)</td><td>0x9653836A</td><td>No</td></tr>
<tr><td>PirDbSpawner (Squad)</td><td>0xB1E30047</td><td>No</td></tr>
<tr><td>Pistol</td><td>0xD48C7D34</td><td>No</td></tr>
<tr><td>Pistol (AL)</td><td>0xF7D358AC</td><td>No</td></tr>
<tr><td>Pistol (CH)</td><td>0xDE670FE2</td><td>No</td></tr>
<tr><td>Pistol (GR)</td><td>0x8C9B1E24</td><td>No</td></tr>
<tr><td>Pistol (silver)</td><td>0x4A02D924</td><td>No</td></tr>
<tr><td>Pistol Bullet</td><td>0xA9F6A3BC</td><td>No</td></tr>
<tr><td>Pistol Bullet (CH)</td><td>0x819173EA</td><td>No</td></tr>
<tr><td>Pistol Bullet (GR)</td><td>0x215A1B1C</td><td>No</td></tr>
<tr><td>Pistol Bullet (OC)</td><td>0x31472E5B</td><td>No</td></tr>
<tr><td>placeable Building</td><td>0x8DC14572</td><td>No</td></tr>
<tr><td>placeable Constrained</td><td>0x8850798A</td><td>No</td></tr>
<tr><td>placeable Environment</td><td>0x0F3754C5</td><td>No</td></tr>
<tr><td>placeable Fence</td><td>0xFF05D325</td><td>No</td></tr>
<tr><td>placeable Prop</td><td>0xE8CB9DED</td><td>No</td></tr>
<tr><td>placeable Prop Destructible</td><td>0xF82EF36D</td><td>No</td></tr>
<tr><td>placeable Static</td><td>0xE8137428</td><td>No</td></tr>
<tr><td>placeable Static Destructible</td><td>0x88BDAEE2</td><td>No</td></tr>
<tr><td>placeable Wall</td><td>0xDFA3C5B6</td><td>No</td></tr>
<tr><td>Planes (as Buildings)</td><td>0xFFD23808</td><td>No</td></tr>
<tr><td>PLZ45</td><td>0x4515E6E4</td><td>Yes</td></tr>
<tr><td>PLZ45 (Driver)</td><td>0x3AAE63C3</td><td>Yes</td></tr>
<tr><td>PLZ45 (Full)</td><td>0xF6B88FF0</td><td>Yes</td></tr>
<tr><td>pMc</td><td>0x30E4A26F</td><td>No</td></tr>
<tr><td>PmcHq_Interior</td><td>0x1EEE05C1</td><td>No</td></tr>
<tr><td>PmcSeat</td><td>0x78EBB784</td><td>No</td></tr>
<tr><td>PointTraffic</td><td>0x3C55A4B8</td><td>No</td></tr>
<tr><td>PointTraffic_AlliedHQ_AA</td><td>0x5775B480</td><td>No</td></tr>
<tr><td>PointTraffic_AlliedHQ_HMMWV</td><td>0x45833FC3</td><td>No</td></tr>
<tr><td>PointTraffic_ChiHQ_AA</td><td>0x5FE4A4E3</td><td>No</td></tr>
<tr><td>PointTraffic_ChiHQ_Soldiers</td><td>0x1E2C21E4</td><td>No</td></tr>
<tr><td>PointTraffic_ChiHQ_Vehicles</td><td>0xB2CC6B46</td><td>Yes</td></tr>
<tr><td>PointTraffic_GurHQ_AA</td><td>0xB6CEC6BB</td><td>No</td></tr>
<tr><td>PointTraffic_GurHQ_Soldiers</td><td>0x53A2E42C</td><td>No</td></tr>
<tr><td>PointTraffic_GurHQ_Vehicles</td><td>0xD1F25B0E</td><td>Yes</td></tr>
<tr><td>PointTraffic_OC_EXT</td><td>0xC63DB251</td><td>No</td></tr>
<tr><td>PointTraffic_OC_GunTrucks</td><td>0x3ECEC776</td><td>Yes</td></tr>
<tr><td>PointTraffic_OC_Omen</td><td>0xEA0B050D</td><td>No</td></tr>
<tr><td>PointTraffic_OC_Soldiers</td><td>0x1BB1F43D</td><td>No</td></tr>
<tr><td>PointTraffic_OC_Stingray</td><td>0xC39AAE15</td><td>Yes</td></tr>
<tr><td>PointTraffic_Pirate_T300DriverGunner</td><td>0xD5D0C497</td><td>No</td></tr>
<tr><td>PointTraffic_PirateHQ_Cutter</td><td>0x72792695</td><td>No</td></tr>
<tr><td>PointTraffic_PirateHQ_Jetski</td><td>0xBC5A7380</td><td>No</td></tr>
<tr><td>PointTraffic_PirateHQ_LandVehicle</td><td>0xCD67CB21</td><td>No</td></tr>
<tr><td>PointTraffic_Pmc_Boats</td><td>0xD4783061</td><td>Yes</td></tr>
<tr><td>PointTraffic_Roadblock_CHINGLV50Spawn</td><td>0xD6B41900</td><td>No</td></tr>
<tr><td>PointTraffic_Roadblock_GunTrucksOC</td><td>0xF1340AC9</td><td>Yes</td></tr>
<tr><td>PointTraffic_Roadblock_Gur50JeepSpawn</td><td>0xA57EA2D9</td><td>Yes</td></tr>
<tr><td>PointTraffic_Roadblock_HMMVSpawn</td><td>0x5F997554</td><td>No</td></tr>
<tr><td>PointTraffic_Roadblock_VZ50jeepSpawn</td><td>0xDC5C7AB5</td><td>Yes</td></tr>
<tr><td>PointTraffic_VZCon001_Dirtbike</td><td>0xF770D59D</td><td>No</td></tr>
<tr><td>PointTraffic_VZCon001_PBoat</td><td>0x3E6A6B05</td><td>Yes</td></tr>
<tr><td>Police</td><td>0xC6FBA403</td><td>No</td></tr>
<tr><td>Police (Gasmask)</td><td>0xA9352497</td><td>No</td></tr>
<tr><td>Police (Riot)</td><td>0x02CC0CC2</td><td>No</td></tr>
<tr><td>Police car (Police driver)</td><td>0xB40344EC</td><td>No</td></tr>
<tr><td>Police Cruiser</td><td>0xB6A5ED4A</td><td>No</td></tr>
<tr><td>Police Cruiser (Driver)</td><td>0xAB6F8831</td><td>No</td></tr>
<tr><td>police cruiser With Civ Driver</td><td>0x351B674A</td><td>No</td></tr>
<tr><td>Police Helicopter</td><td>0xDC56A3AA</td><td>Yes</td></tr>
<tr><td>Police Helicopter (Delivery)</td><td>0x3FAD763F</td><td>Yes</td></tr>
<tr><td>Police Helicopter (Driver)</td><td>0x03E72111</td><td>Yes</td></tr>
<tr><td>Pony (base)</td><td>0x14B85D27</td><td>No</td></tr>
<tr><td>Pony (crappy)</td><td>0x3957B519</td><td>No</td></tr>
<tr><td>Pony (Crappy) (Driver)</td><td>0xA1B054F4</td><td>No</td></tr>
<tr><td>Pony (crappy) (Driver) (Civ Poor female)</td><td>0x3E6DC31B</td><td>No</td></tr>
<tr><td>Pony (crappy) (Driver) (Civ Poor male)</td><td>0x1AF7A1CA</td><td>No</td></tr>
<tr><td>Pony (normal)</td><td>0x89A24815</td><td>No</td></tr>
<tr><td>Pony (Normal) (black)</td><td>0xD727254F</td><td>No</td></tr>
<tr><td>Pony (Normal) (blue)</td><td>0xFD344F9A</td><td>No</td></tr>
<tr><td>Pony (Normal) (Driver)</td><td>0xE75BD9A0</td><td>No</td></tr>
<tr><td>Pony (Normal) (Driver) (Civ Poor female)</td><td>0x2E0C2837</td><td>No</td></tr>
<tr><td>Pony (Normal) (Driver) (Civ Poor male)</td><td>0x308AC676</td><td>No</td></tr>
<tr><td>Pony (Normal) (green)</td><td>0xDB96D9D7</td><td>No</td></tr>
<tr><td>Pony (Normal) (lightblue)</td><td>0x93EB015C</td><td>No</td></tr>
<tr><td>Pony (Normal) (orange)</td><td>0xA6C359DC</td><td>No</td></tr>
<tr><td>Pony (Normal) (red)</td><td>0xB9844A27</td><td>No</td></tr>
<tr><td>Pony (Normal) (white)</td><td>0xA3C23DFD</td><td>No</td></tr>
<tr><td>Pony_Driver</td><td>0xA0E58342</td><td>No</td></tr>
<tr><td>PopulationRegions</td><td>0x9DB5BF57</td><td>No</td></tr>
<tr><td>PR buggy (Gunner RightFront)</td><td>0xD4C38954</td><td>Yes</td></tr>
<tr><td>PR Cup</td><td>0xD236C9FF</td><td>No</td></tr>
<tr><td>PR Defender (AA)</td><td>0xEA15496B</td><td>No</td></tr>
<tr><td>PR Defender (AT)</td><td>0xD68661A0</td><td>No</td></tr>
<tr><td>PR Defender (AT) (Window Spawner)</td><td>0x2A580369</td><td>No</td></tr>
<tr><td>PR Defender (MG)</td><td>0x2C08156D</td><td>No</td></tr>
<tr><td>PR Defender (Rifle)</td><td>0xFB7ED48F</td><td>No</td></tr>
<tr><td>PR HQ Cell Phone</td><td>0x1A4F5240</td><td>No</td></tr>
<tr><td>Practice LGB Projectile</td><td>0x041F899E</td><td>No</td></tr>
<tr><td>Primary Equipment</td><td>0xDFCF027D</td><td>No</td></tr>
<tr><td>Programmer Test Template</td><td>0x89923DE7</td><td>No</td></tr>
<tr><td>ProgrammerBlueRoad10</td><td>0xE6BA19F8</td><td>No</td></tr>
<tr><td>ProgrammerBlueRoad20</td><td>0x1AE507A9</td><td>No</td></tr>
<tr><td>ProgrammerBlueZone</td><td>0xAEB500CF</td><td>No</td></tr>
<tr><td>ProgrammerGreenRoad10</td><td>0x62C45ABB</td><td>No</td></tr>
<tr><td>ProgrammerGreenZone</td><td>0x02A13980</td><td>No</td></tr>
<tr><td>ProgrammerRedHDTemplate</td><td>0x02F37108</td><td>No</td></tr>
<tr><td>ProgrammerRedRoad10</td><td>0xD81F2DDB</td><td>No</td></tr>
<tr><td>ProgrammerRedRoad20</td><td>0x0F6B0116</td><td>No</td></tr>
<tr><td>ProgrammerRedZone</td><td>0x4235BFA0</td><td>No</td></tr>
<tr><td>ProgrammerTest10Cross</td><td>0xED2056E2</td><td>No</td></tr>
<tr><td>ProgrammerTestRoad10w</td><td>0xEF2A1E77</td><td>No</td></tr>
<tr><td>ProgrammerTestRoad20c</td><td>0xCFA7AD64</td><td>No</td></tr>
<tr><td>ProgrammerTestZone</td><td>0x590C0497</td><td>No</td></tr>
<tr><td>ProgrammerYellowRoad10</td><td>0x9D8FABBC</td><td>No</td></tr>
<tr><td>ProgrammerYellowZone</td><td>0x48A5E12B</td><td>No</td></tr>
<tr><td>Projectile</td><td>0xBD8C6F10</td><td>No</td></tr>
<tr><td>prop_metal_lrg</td><td>0x30E6DADE</td><td>No</td></tr>
<tr><td>prop_stone_lrg</td><td>0x8A394748</td><td>No</td></tr>
<tr><td>PropDestructTemplate</td><td>0x56C61F52</td><td>No</td></tr>
<tr><td>PropTemplate</td><td>0x6A5C2678</td><td>No</td></tr>
<tr><td>PropTemplate_chandellier</td><td>0xFDF1F196</td><td>No</td></tr>
<tr><td>Protester (female)</td><td>0x43DD69DC</td><td>No</td></tr>
<tr><td>Protester (male)</td><td>0x1EA64DED</td><td>No</td></tr>
<tr><td>Proximity Mine</td><td>0x0C1E83CD</td><td>No</td></tr>
<tr><td>Proximity Mine (Planted)</td><td>0xDF14909C</td><td>No</td></tr>
<tr><td>Proximity Mine Projectile</td><td>0x8557688A</td><td>No</td></tr>
<tr><td>QuotaObject</td><td>0x15D0D35E</td><td>No</td></tr>
<tr><td>R90</td><td>0xCA5BBA82</td><td>No</td></tr>
<tr><td>R90 (Driver)</td><td>0x3876D729</td><td>No</td></tr>
<tr><td>R90 (Driver) (Civ Business B Male)</td><td>0x209227FB</td><td>No</td></tr>
<tr><td>R90 (Driver) (Civ Business Female)</td><td>0xE594BA20</td><td>No</td></tr>
<tr><td>R90 (Driver) (Civ Business Male)</td><td>0xDC9E9AD1</td><td>No</td></tr>
<tr><td>R90 (Driver) (Civ Rich Female)</td><td>0x1F49A5F8</td><td>No</td></tr>
<tr><td>R90 (Driver) (Civ Rich Male)</td><td>0x258DEE29</td><td>No</td></tr>
<tr><td>R90 (Driver) (OC)</td><td>0x219BDAFC</td><td>No</td></tr>
<tr><td>R90 (Fling Left)</td><td>0x4F977B9C</td><td>No</td></tr>
<tr><td>R90 (Fling Right)</td><td>0x8FD76CCF</td><td>No</td></tr>
<tr><td>R90 Limo</td><td>0x50390CFF</td><td>No</td></tr>
<tr><td>R90 Taxi</td><td>0x1D022366</td><td>No</td></tr>
<tr><td>R90 Taxi (Driver)</td><td>0x705A73FD</td><td>No</td></tr>
<tr><td>R90 Taxi (Driver) (Civ Taxi Driver male)</td><td>0xF93E8587</td><td>No</td></tr>
<tr><td>R90_Driver</td><td>0xD19ED643</td><td>No</td></tr>
<tr><td>Real Physics Prop</td><td>0xFFE5624D</td><td>No</td></tr>
<tr><td>Real Physics Prop Destructible</td><td>0x12C5BACD</td><td>No</td></tr>
<tr><td>Recruit Eva Navarro</td><td>0x262B9048</td><td>No</td></tr>
<tr><td>Recruit Ewen Garret</td><td>0x9C5DD2A9</td><td>No</td></tr>
<tr><td>Recruit Ewen Garret (Invincible)</td><td>0x5C54C46B</td><td>No</td></tr>
<tr><td>Recruit Misha Milanich</td><td>0xD777E8A2</td><td>No</td></tr>
<tr><td>RIB36</td><td>0xDB1BF61F</td><td>No</td></tr>
<tr><td>RIB36 (DEPRECIATED)</td><td>0x1E169152</td><td>No</td></tr>
<tr><td>RIB36 (VZ Driver)</td><td>0x4FAAE964</td><td>No</td></tr>
<tr><td>RIB36_Driver</td><td>0x7ADD14AC</td><td>No</td></tr>
<tr><td>Ridgeline</td><td>0x4C5D7A00</td><td>No</td></tr>
<tr><td>Ridgeline (Driver)</td><td>0xF044DC1F</td><td>No</td></tr>
<tr><td>Ridgeline (Driver) (Civ Poor female)</td><td>0xA10E5854</td><td>No</td></tr>
<tr><td>Ridgeline (Driver) (Civ Poor male)</td><td>0x29012425</td><td>No</td></tr>
<tr><td>Ridgeline_Driver</td><td>0x32561F7D</td><td>No</td></tr>
<tr><td>rifle</td><td>0xD0459A41</td><td>No</td></tr>
<tr><td>Riot Gun</td><td>0x2531D295</td><td>No</td></tr>
<tr><td>Riot Gun Projectile</td><td>0x3C45B6A2</td><td>No</td></tr>
<tr><td>Road</td><td>0xEA0F3AA3</td><td>No</td></tr>
<tr><td>Rocket</td><td>0x5434C7ED</td><td>No</td></tr>
<tr><td>Rocket Artillery Projectile</td><td>0x908FB818</td><td>No</td></tr>
<tr><td>Rocks01</td><td>0xB8822B30</td><td>No</td></tr>
<tr><td>RPG</td><td>0x60437246</td><td>No</td></tr>
<tr><td>RPG (Window Spawner)</td><td>0xC507000B</td><td>No</td></tr>
<tr><td>RPG Rocket</td><td>0xEFEB3916</td><td>No</td></tr>
<tr><td>rpglauncher</td><td>0xEB8404E6</td><td>No</td></tr>
<tr><td>RTR</td><td>0xCFCAA9FB</td><td>No</td></tr>
<tr><td>RTR (Civ)</td><td>0x23322390</td><td>No</td></tr>
<tr><td>RTR (Civ) (black)</td><td>0x72D8A062</td><td>No</td></tr>
<tr><td>RTR (Civ) (blue)</td><td>0x95CAF8C1</td><td>No</td></tr>
<tr><td>RTR (Civ) (Driver)</td><td>0x78695EAF</td><td>No</td></tr>
<tr><td>RTR (Civ) (Driver) (Civ Business B male)</td><td>0x3CEF5959</td><td>No</td></tr>
<tr><td>RTR (Civ) (Driver) (Civ Poor Male)</td><td>0xE4B8C995</td><td>No</td></tr>
<tr><td>RTR (Civ) (green)</td><td>0x251C7E1A</td><td>No</td></tr>
<tr><td>RTR (Civ) (lightblue)</td><td>0x8E43E67D</td><td>No</td></tr>
<tr><td>RTR (Civ) (orange)</td><td>0xC729455F</td><td>No</td></tr>
<tr><td>RTR (Civ) (red)</td><td>0xFA5106B6</td><td>No</td></tr>
<tr><td>RTR (Civ) (white)</td><td>0x1FA88138</td><td>No</td></tr>
<tr><td>RTR (crappy)</td><td>0x2C14011F</td><td>No</td></tr>
<tr><td>RTR (crappy) (driver)</td><td>0x8FDA008A</td><td>No</td></tr>
<tr><td>RTR (crappy) (Driver) (Civ Casual female)</td><td>0x3C608342</td><td>No</td></tr>
<tr><td>RTR (crappy) (Driver) (Civ Casual male)</td><td>0x54C270E7</td><td>No</td></tr>
<tr><td>RTR (crappy) (Driver) (Civ Poor female)</td><td>0xF1076039</td><td>No</td></tr>
<tr><td>RTR (crappy) (Driver) (Civ Poor male)</td><td>0x8AA5FB1C</td><td>No</td></tr>
<tr><td>RTR (racing)</td><td>0x928B459E</td><td>No</td></tr>
<tr><td>RTR (racing) (Driver)</td><td>0x892F2F35</td><td>No</td></tr>
<tr><td>RTR (racing) (Driver) (Civ Motorcycle male)</td><td>0x78551744</td><td>Yes</td></tr>
<tr><td>RTR_Driver</td><td>0xD9EAD870</td><td>No</td></tr>
<tr><td>RTRCrappy_Driver</td><td>0xF4C1E9A3</td><td>No</td></tr>
<tr><td>RTRRacing_Driver</td><td>0x9D5D27A2</td><td>No</td></tr>
<tr><td>RuinDebris01</td><td>0x5D3EC19B</td><td>No</td></tr>
<tr><td>RuinDebris02</td><td>0xC341A0C4</td><td>No</td></tr>
<tr><td>RuinDebris_concrete</td><td>0x6AC06304</td><td>No</td></tr>
<tr><td>Salamander</td><td>0x91C6BF01</td><td>No</td></tr>
<tr><td>Salton Seahorse (base)</td><td>0xF41431F6</td><td>Yes</td></tr>
<tr><td>Salton Seahorse (Civ)</td><td>0xBE7BD515</td><td>Yes</td></tr>
<tr><td>Salton Seahorse (Civ) (Driver)</td><td>0xE39CB0A0</td><td>Yes</td></tr>
<tr><td>Salton Seahorse (Civ) (Driver) (Civ Poor female)</td><td>0xE5841737</td><td>Yes</td></tr>
<tr><td>Salton Seahorse (Civ) (Driver) (Civ Poor male)</td><td>0x972F5D76</td><td>Yes</td></tr>
<tr><td>Salton Seahorse (PR)</td><td>0x860D8FF9</td><td>Yes</td></tr>
<tr><td>Salton Seahorse (PR) (Driver)</td><td>0xDD8E3154</td><td>Yes</td></tr>
<tr><td>Salton Seahorse (PR) (Full)</td><td>0x0606C113</td><td>Yes</td></tr>
<tr><td>Salton_Driver</td><td>0x654931B3</td><td>No</td></tr>
<tr><td>Satellite Designator</td><td>0x9ADAB72A</td><td>No</td></tr>
<tr><td>Scooter</td><td>0x5EAC70AA</td><td>No</td></tr>
<tr><td>Scooter (Driver)</td><td>0xBD18B811</td><td>No</td></tr>
<tr><td>Scooter (Driver) (Civ casual female)</td><td>0x40048AA9</td><td>No</td></tr>
<tr><td>Scooter (Driver) (Civ casual male)</td><td>0x0FD71A8C</td><td>No</td></tr>
<tr><td>Scooter (Driver) (Civ poor female)</td><td>0xAD797E46</td><td>No</td></tr>
<tr><td>Scooter (Driver) (Civ poor male)</td><td>0x0850EC7B</td><td>No</td></tr>
<tr><td>Scooter (Driver) (Civ rich female)</td><td>0x62202290</td><td>No</td></tr>
<tr><td>Scooter_Driver</td><td>0xE5EC037B</td><td>No</td></tr>
<tr><td>Scooter_OC021</td><td>0x5D965E06</td><td>No</td></tr>
<tr><td>Scorpion90</td><td>0x46E480D9</td><td>Yes</td></tr>
<tr><td>Scorpion90 (Driver)</td><td>0xC08A6A34</td><td>Yes</td></tr>
<tr><td>Scorpion90 (Driver) (PMC001)</td><td>0xF44925BE</td><td>Yes</td></tr>
<tr><td>Scorpion90 (Full)</td><td>0x4504E573</td><td>Yes</td></tr>
<tr><td>Scrubs</td><td>0xB099EE89</td><td>No</td></tr>
<tr><td>Secondary Equipment</td><td>0x904302A5</td><td>No</td></tr>
<tr><td>Semi (Base)</td><td>0x1077B77D</td><td>No</td></tr>
<tr><td>SF LowRoad</td><td>0xB9A67D1A</td><td>No</td></tr>
<tr><td>Shockwave_C4</td><td>0x42A66B28</td><td>No</td></tr>
<tr><td>Shockwaves</td><td>0x963C4A61</td><td>No</td></tr>
<tr><td>Shotgun</td><td>0xFA8FBA6D</td><td>No</td></tr>
<tr><td>Shotgun (Window Spawner)</td><td>0x230B031A</td><td>No</td></tr>
<tr><td>Shotgun Bullet</td><td>0xC846C397</td><td>No</td></tr>
<tr><td>Sidecar Motorcycle</td><td>0x07856105</td><td>Yes</td></tr>
<tr><td>Sidecar Motorcycle (Driver)</td><td>0xA9456B10</td><td>Yes</td></tr>
<tr><td>Sidecar Motorcycle (Full)</td><td>0x74651AA7</td><td>Yes</td></tr>
<tr><td>SideCarMotorcycle_Driver</td><td>0x9C5FC386</td><td>Yes</td></tr>
<tr><td>SimplePointSpawner</td><td>0x639DA6DD</td><td>No</td></tr>
<tr><td>skyscraper2x4</td><td>0x27737148</td><td>No</td></tr>
<tr><td>Small Fishing Boat</td><td>0xA18CEEA2</td><td>Yes</td></tr>
<tr><td>Small Fishing Boat (Driver)</td><td>0xF49EC349</td><td>Yes</td></tr>
<tr><td>Small Fishing Boat (Driver) (Civ Poor female)</td><td>0x4CC307AE</td><td>Yes</td></tr>
<tr><td>Small Fishing Boat (Driver) (Civ Poor male)</td><td>0xC94477E3</td><td>Yes</td></tr>
<tr><td>small_boats</td><td>0xFA95731A</td><td>Yes</td></tr>
<tr><td>SmallFishingBoat_Driver</td><td>0x2ADA33A7</td><td>Yes</td></tr>
<tr><td>SmallFlame</td><td>0x7E73F9C7</td><td>No</td></tr>
<tr><td>Smart Bomb Projectile</td><td>0x5755AD55</td><td>No</td></tr>
<tr><td>smg</td><td>0x858035CC</td><td>No</td></tr>
<tr><td>SMG Bullet</td><td>0x17D01624</td><td>No</td></tr>
<tr><td>Smoke Designator</td><td>0xCA109D56</td><td>No</td></tr>
<tr><td>Smoke Grenade Projectile</td><td>0xF7208F3F</td><td>No</td></tr>
<tr><td>SndEmitter_ShantyRadio</td><td>0x09BEF713</td><td>No</td></tr>
<tr><td>Sniper Rifle</td><td>0xEA4DEF62</td><td>No</td></tr>
<tr><td>Sniper Rifle (AA Backup)</td><td>0x2AF0A2AB</td><td>No</td></tr>
<tr><td>Sniper Rifle (SVD)</td><td>0x4D3161D0</td><td>No</td></tr>
<tr><td>Sniper Rifle Bullet</td><td>0xCD44A052</td><td>No</td></tr>
<tr><td>SoccerBallProp</td><td>0x68632398</td><td>No</td></tr>
<tr><td>Solano</td><td>0xA69995AF</td><td>No</td></tr>
<tr><td>soldier</td><td>0x75E8C74D</td><td>No</td></tr>
<tr><td>SoundEmitter</td><td>0x08E7BCC8</td><td>No</td></tr>
<tr><td>SoundMaterial</td><td>0x3CB9AED5</td><td>No</td></tr>
<tr><td>SoundMaterial ((veh_motorcycl</td><td>0x6A0DB29F</td><td>Yes</td></tr>
<tr><td>SoundMaterial (ArmoredVehicle)</td><td>0xCDEC35F0</td><td>No</td></tr>
<tr><td>SoundMaterial (bldg_bunker)</td><td>0x42246AB5</td><td>No</td></tr>
<tr><td>SoundMaterial (bldg_default)</td><td>0xB78AC49F</td><td>No</td></tr>
<tr><td>SoundMaterial (bldg_glass)</td><td>0x2A04FAA6</td><td>No</td></tr>
<tr><td>SoundMaterial (bldg_metal)</td><td>0x683F901D</td><td>No</td></tr>
<tr><td>SoundMaterial (bldg_stone)</td><td>0xB414CABB</td><td>No</td></tr>
<tr><td>SoundMaterial (bldg_stone_large)</td><td>0x29A327A7</td><td>No</td></tr>
<tr><td>SoundMaterial (bldg_wood)</td><td>0xD608DEC9</td><td>No</td></tr>
<tr><td>SoundMaterial (BrickProp)</td><td>0xD9A26AA4</td><td>No</td></tr>
<tr><td>SoundMaterial (debris_oilrig) 0x8000a6f5</td><td>0xA0616178</td><td>No</td></tr>
<tr><td>SoundMaterial (hum_civ)</td><td>0xF21BD6EB</td><td>No</td></tr>
<tr><td>SoundMaterial (hum_hero_chris)</td><td>0xA4CCA57D</td><td>No</td></tr>
<tr><td>SoundMaterial (hum_hero_jen)</td><td>0x6A4B7D7B</td><td>No</td></tr>
<tr><td>SoundMaterial (hum_hero_mattias)</td><td>0x99BB8D1F</td><td>No</td></tr>
<tr><td>SoundMaterial (hum_soldier)</td><td>0x2069C0EF</td><td>No</td></tr>
<tr><td>SoundMaterial (Human)</td><td>0x7D2D50F1</td><td>No</td></tr>
<tr><td>SoundMaterial (Projectile)</td><td>0xDD1AECD1</td><td>No</td></tr>
<tr><td>SoundMaterial (projectile_bullet_heavyMG)</td><td>0x8366D4FC</td><td>No</td></tr>
<tr><td>SoundMaterial (projectile_bullet_rifle)</td><td>0xC181A3C5</td><td>No</td></tr>
<tr><td>SoundMaterial (projectile_grapple)</td><td>0x197888C1</td><td>No</td></tr>
<tr><td>SoundMaterial (projectile_rocket)</td><td>0x3DA89DF0</td><td>No</td></tr>
<tr><td>SoundMaterial (Prop)</td><td>0x944539D3</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_barreldrum)</td><td>0xDC7B841E</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_fabric)</td><td>0xD0D32A77</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_fabric_lrg)</td><td>0x4F3E72AB</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_fabric_sml)</td><td>0xEC0900A0</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_foliage)</td><td>0xF0083103</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_foliage_lrg)</td><td>0x2E032F8F</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_foliage_med)</td><td>0x0433A3C6</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_foliage_sml)</td><td>0x1D4D54A4</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_glass)</td><td>0x7C81F92C</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_metal)</td><td>0x3BBA0CD7</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_metal_chainlinkfence)</td><td>0xC85544D4</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_metal_lrg)</td><td>0xFF9FB98B</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_metal_med)</td><td>0x041639AA</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_metal_sml)</td><td>0x1DA6B280</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_metalpole_lrg)</td><td>0xF0ECD9CD</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_metalpole_sml)</td><td>0x71CD1C76</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_rubber_tire)</td><td>0x4AAF9A99</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_sandbag)</td><td>0x9B218104</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_sheetmetal_lrg)</td><td>0x7291193C</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_sheetmetal_med)</td><td>0xAFBBFD71</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_sheetmetal_sml)</td><td>0x7F4D9347</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_stone)</td><td>0xF0344971</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_stone_lrg)</td><td>0x778E81E9</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_stone_med)</td><td>0x89D18648</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_stone_sml)</td><td>0xB3467632</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_tree)</td><td>0xF97D8862</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_tree_lrg)</td><td>0xCADD03AE</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_tree_med)</td><td>0xABBA1A3B</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_tree_sml)</td><td>0xFD72BA2D</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_wood)</td><td>0x80FE5283</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_wood_crate)</td><td>0x24D65F3B</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_wood_lrg)</td><td>0x2299E90F</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_wood_med)</td><td>0xF8CA5D46</td><td>No</td></tr>
<tr><td>SoundMaterial (prop_wood_sml)</td><td>0x11E40E24</td><td>No</td></tr>
<tr><td>SoundMaterial (SheetMetalProp)</td><td>0xBCBA4A55</td><td>No</td></tr>
<tr><td>SoundMaterial (terrain)</td><td>0x0C9229E5</td><td>No</td></tr>
<tr><td>SoundMaterial (terrain_asphalt)</td><td>0x9353CDF9</td><td>No</td></tr>
<tr><td>SoundMaterial (terrain_dirt)</td><td>0x0069F079</td><td>No</td></tr>
<tr><td>SoundMaterial (terrain_grass)</td><td>0x64D2EB70</td><td>No</td></tr>
<tr><td>SoundMaterial (terrain_sand)</td><td>0x99787256</td><td>No</td></tr>
<tr><td>SoundMaterial (veh)</td><td>0xA240211F</td><td>No</td></tr>
<tr><td>SoundMaterial (veh_armored)</td><td>0xBE063886</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_armored_bottom_skids)</td><td>0xBDE9EC61</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_armored_bottom_tracked)</td><td>0x72550BFB</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_armored_bottom_wheeled)</td><td>0xF6EC0973</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_armored_heli_rotor)</td><td>0xD748B4E6</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_armored_light)</td><td>0x6C91197D</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_armored_med)</td><td>0x29575C2F</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_armored_ruin)</td><td>0x20792A2F</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_armored_tank)</td><td>0x338C6E41</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_armored_tank_turret)</td><td>0x825464A6</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_boat_lrg)</td><td>0xFD1F4378</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_boat_med)</td><td>0xBD5F1525</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_boat_sml)</td><td>0x2A14BE53</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ)</td><td>0x075715DE</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_bottom)</td><td>0xEBED61C6</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_bumper)</td><td>0xC8EDEBBA</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg)</td><td>0xAAC80002</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_bottom)</td><td>0x00881382</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_bumper)</td><td>0xD160FF96</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_ruin)</td><td>0xFDAED94B</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_sides)</td><td>0x641AE6C1</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_top)</td><td>0x7619BA46</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_ruin)</td><td>0xFA79D447</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_sides)</td><td>0x2651CC55</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_civ_top)</td><td>0x3A81BB2A</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_motorcycle)</td><td>0x1A68F603</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_motorcycle_ruin)</td><td>0xD3DBAF10</td><td>Yes</td></tr>
<tr><td>SoundMaterial (veh_motorcycle_wheels)</td><td>0xBEC0535A</td><td>Yes</td></tr>
<tr><td>SoundMaterial (Vehicle)</td><td>0xE1E412C0</td><td>No</td></tr>
<tr><td>SoundMaterial (water)</td><td>0xC95CA2AB</td><td>No</td></tr>
<tr><td>SoundMaterial (water_deep)</td><td>0x325ADAA8</td><td>No</td></tr>
<tr><td>SoundMaterial (water_puddle)</td><td>0x60C7DECE</td><td>No</td></tr>
<tr><td>SoundMaterial (water_shallow)</td><td>0xB010267C</td><td>No</td></tr>
<tr><td>SoundMaterial (Weapon)</td><td>0x17688DCE</td><td>No</td></tr>
<tr><td>SoundMaterial (wpn_c4)</td><td>0x65D717CD</td><td>No</td></tr>
<tr><td>SoundMaterial (wpn_clip)</td><td>0xFB97ACE0</td><td>No</td></tr>
<tr><td>SoundMaterial (wpn_designator)</td><td>0x5E83C924</td><td>No</td></tr>
<tr><td>SoundMaterial (wpn_emplacedgun)</td><td>0xA5909613</td><td>No</td></tr>
<tr><td>SoundMaterial (wpn_grenade)</td><td>0xAE30CA36</td><td>No</td></tr>
<tr><td>SoundMaterial (wpn_pistol)</td><td>0x7A95CCE1</td><td>No</td></tr>
<tr><td>SoundMaterial (wpn_rifle)</td><td>0x641CD0EA</td><td>No</td></tr>
<tr><td>SoundMaterial (wpn_rocket)</td><td>0x45C9DAE6</td><td>No</td></tr>
<tr><td>Spawnable</td><td>0xE2B0DE0E</td><td>No</td></tr>
<tr><td>Spawners</td><td>0x2FEE679A</td><td>No</td></tr>
<tr><td>Spawnlist (Allied AA)</td><td>0xAA950B00</td><td>No</td></tr>
<tr><td>Spawnlist (Allied Balcony)</td><td>0x90093EB0</td><td>No</td></tr>
<tr><td>Spawnlist (Allied Destroyer Crew)</td><td>0x40EA8E78</td><td>Yes</td></tr>
<tr><td>Spawnlist (Allied Ground)</td><td>0x66BAA21D</td><td>No</td></tr>
<tr><td>Spawnlist (Allied Prisoner)</td><td>0xCF53FF46</td><td>No</td></tr>
<tr><td>Spawnlist (Allied Tower AA)</td><td>0x56C3EB9F</td><td>No</td></tr>
<tr><td>Spawnlist (Allied Tower AT)</td><td>0x3F28B48C</td><td>No</td></tr>
<tr><td>Spawnlist (Allied Tower)</td><td>0x08150331</td><td>No</td></tr>
<tr><td>Spawnlist (Allied Window)</td><td>0x2073D612</td><td>No</td></tr>
<tr><td>Spawnlist (CHI BasePeds)</td><td>0x380C69EA</td><td>No</td></tr>
<tr><td>Spawnlist (CHI BaseTanks)</td><td>0x8F9CCA13</td><td>Yes</td></tr>
<tr><td>Spawnlist (CHI BaseVehicles)</td><td>0xBB23D451</td><td>No</td></tr>
<tr><td>Spawnlist (ChiCon002)</td><td>0x48AC633B</td><td>No</td></tr>
<tr><td>Spawnlist (China AA)</td><td>0x84DAB5CC</td><td>No</td></tr>
<tr><td>Spawnlist (China Balcony)</td><td>0xE63107BC</td><td>No</td></tr>
<tr><td>Spawnlist (China Destroyer Crew)</td><td>0xFC902B0C</td><td>Yes</td></tr>
<tr><td>Spawnlist (China Ground)</td><td>0xC6B39751</td><td>No</td></tr>
<tr><td>Spawnlist (China Tower AA)</td><td>0xF6C4622B</td><td>No</td></tr>
<tr><td>Spawnlist (China Tower RPG)</td><td>0x1F6DA07A</td><td>No</td></tr>
<tr><td>Spawnlist (China Tower)</td><td>0x214FB215</td><td>No</td></tr>
<tr><td>Spawnlist (China Window)</td><td>0x64BF7076</td><td>No</td></tr>
<tr><td>Spawnlist (Chinese Prisoner)</td><td>0xACEDECCA</td><td>No</td></tr>
<tr><td>Spawnlist (Civilian Default)</td><td>0x665509FB</td><td>No</td></tr>
<tr><td>Spawnlist (Guerilla AA)</td><td>0x517C4F32</td><td>No</td></tr>
<tr><td>Spawnlist (Guerilla Balcony)</td><td>0x42167CDE</td><td>No</td></tr>
<tr><td>Spawnlist (Guerilla Ground)</td><td>0x9AFAD237</td><td>No</td></tr>
<tr><td>Spawnlist (Guerilla Prisoner)</td><td>0x56B94A1C</td><td>No</td></tr>
<tr><td>Spawnlist (Guerilla Tower RPG)</td><td>0x7DE5C088</td><td>No</td></tr>
<tr><td>Spawnlist (Guerilla Tower)</td><td>0x1A0B5733</td><td>No</td></tr>
<tr><td>Spawnlist (Guerilla Window)</td><td>0xCD6A29CC</td><td>No</td></tr>
<tr><td>Spawnlist (M1A2 (Full))</td><td>0x62946724</td><td>Yes</td></tr>
<tr><td>Spawnlist (OC AA)</td><td>0x6E25992F</td><td>No</td></tr>
<tr><td>Spawnlist (OC Balcony)</td><td>0x51866F91</td><td>No</td></tr>
<tr><td>Spawnlist (OC Ground)</td><td>0x31E2D3EE</td><td>No</td></tr>
<tr><td>Spawnlist (OC Prisoner)</td><td>0x65CFF4F9</td><td>No</td></tr>
<tr><td>Spawnlist (OC Tower Elite)</td><td>0x746381A3</td><td>No</td></tr>
<tr><td>Spawnlist (OC Tower GL)</td><td>0xAA726291</td><td>No</td></tr>
<tr><td>Spawnlist (OC Tower)</td><td>0x736F058C</td><td>No</td></tr>
<tr><td>Spawnlist (OC Window)</td><td>0x77C26C99</td><td>No</td></tr>
<tr><td>Spawnlist (Pirate AA)</td><td>0x9A3367B2</td><td>No</td></tr>
<tr><td>Spawnlist (Pirate Balcony)</td><td>0x68D9A65E</td><td>No</td></tr>
<tr><td>Spawnlist (Pirate Ground)</td><td>0xB42AF2B7</td><td>No</td></tr>
<tr><td>Spawnlist (Pirate Prisoner)</td><td>0xDBF39E9C</td><td>No</td></tr>
<tr><td>Spawnlist (Pirate Tower)</td><td>0x70D104B3</td><td>No</td></tr>
<tr><td>Spawnlist (Pirate Window)</td><td>0xE69A4A4C</td><td>No</td></tr>
<tr><td>Spawnlist (VZ AA)</td><td>0xF9ADB995</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Balcony AT)</td><td>0x932DE232</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Balcony)</td><td>0x1E14B42B</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Barracks Ground)</td><td>0x9A7C5879</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Barracks Ground_wRPG)</td><td>0xB0223410</td><td>No</td></tr>
<tr><td>Spawnlist (VZ BaseVehicles)</td><td>0xFA9BF1C7</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Elite)</td><td>0x7C903D04</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Ground)</td><td>0x7B4587E4</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Mixed Patrol)</td><td>0x8F2DBB04</td><td>No</td></tr>
<tr><td>Spawnlist (VZ RPG + Rifle)</td><td>0x47E72343</td><td>No</td></tr>
<tr><td>Spawnlist (VZ RPG Patrol)</td><td>0xAE49DABC</td><td>No</td></tr>
<tr><td>Spawnlist (VZ RPG)</td><td>0xC8F924D8</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Tower AA)</td><td>0xC26D48FE</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Tower RPG)</td><td>0x32E8CBED</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Tower RPG) 0x8000b2fa</td><td>0xBBA759B4</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Tower)</td><td>0xEE307A42</td><td>No</td></tr>
<tr><td>Spawnlist (VZ Window)</td><td>0x5C4ACD6F</td><td>No</td></tr>
<tr><td>Speed Boat</td><td>0xF6515BBC</td><td>Yes</td></tr>
<tr><td>Speed Boat (Driver)</td><td>0xF3EEE47B</td><td>Yes</td></tr>
<tr><td>Speed Boat (Driver) (Civ Beach A Female)</td><td>0x4FE1C572</td><td>Yes</td></tr>
<tr><td>Speed Boat (Driver) (Civ Beach B Female)</td><td>0xBB059AF5</td><td>Yes</td></tr>
<tr><td>Speed Boat (Driver) (Civ Beach C Female)</td><td>0xFFFAB0A4</td><td>Yes</td></tr>
<tr><td>Speed Boat (Driver) (Civ Beach D Female)</td><td>0xC5C88D67</td><td>Yes</td></tr>
<tr><td>Speed Boat (Full)</td><td>0x69A995F8</td><td>Yes</td></tr>
<tr><td>Sportbike (Civ)</td><td>0x2F26B7F9</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (black)</td><td>0x2CA1CF5B</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (blue)</td><td>0x705901CE</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (Driver)</td><td>0x7E6F2954</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (Driver) (Civ casual female)</td><td>0x64C5B500</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (Driver) (Civ casual male)</td><td>0x824548B1</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (Driver) (Civ Motorcycle male)</td><td>0xFB5D55FD</td><td>Yes</td></tr>
<tr><td>Sportbike (Civ) (green)</td><td>0x0821B58B</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (lightblue)</td><td>0xC30D7E10</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (orange)</td><td>0x80DCCB08</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (red)</td><td>0x48B303BB</td><td>No</td></tr>
<tr><td>Sportbike (Civ) (white)</td><td>0x67ADC189</td><td>No</td></tr>
<tr><td>Sportbike_Driver</td><td>0x0DC17FF7</td><td>No</td></tr>
<tr><td>Squad</td><td>0x9788C501</td><td>No</td></tr>
<tr><td>SquadSpawner</td><td>0xFC55E3A3</td><td>No</td></tr>
<tr><td>SquadTest</td><td>0x63BEDB59</td><td>No</td></tr>
<tr><td>SquadTest 2</td><td>0xEE5C5203</td><td>No</td></tr>
<tr><td>Stinger</td><td>0xABF77BF9</td><td>No</td></tr>
<tr><td>Stingray II</td><td>0xF7E45E52</td><td>Yes</td></tr>
<tr><td>Stingray II (Civ driver)</td><td>0x8B638C7F</td><td>Yes</td></tr>
<tr><td>Stingray II (Driver)</td><td>0x7FE89779</td><td>Yes</td></tr>
<tr><td>Stingray II (Full)</td><td>0x9635391E</td><td>Yes</td></tr>
<tr><td>Stingray II (VZ driver)</td><td>0xC7BFD691</td><td>Yes</td></tr>
<tr><td>StingrayFullSpawnList</td><td>0xFB6E6930</td><td>Yes</td></tr>
<tr><td>Strategic Missile Projectile</td><td>0xE6B58FBE</td><td>No</td></tr>
<tr><td>Strategic Missile Projectile Launch</td><td>0x0462B13B</td><td>No</td></tr>
<tr><td>Strategic Missile Shrapnel</td><td>0x6CF337B8</td><td>No</td></tr>
<tr><td>Supply Drop (AA)</td><td>0x371641A6</td><td>No</td></tr>
<tr><td>Supply Drop (AL Ammo)</td><td>0x9AD7F8C3</td><td>No</td></tr>
<tr><td>Supply Drop (AL Grenade)</td><td>0xD6EB5CBF</td><td>No</td></tr>
<tr><td>Supply Drop (AL Health)</td><td>0x69A74BC7</td><td>No</td></tr>
<tr><td>Supply Drop (Allied)</td><td>0xBCE8CF73</td><td>No</td></tr>
<tr><td>Supply Drop (AM AL)</td><td>0x2975CD61</td><td>No</td></tr>
<tr><td>Supply Drop (AM CH)</td><td>0xF19A1E77</td><td>No</td></tr>
<tr><td>Supply Drop (AT AL)</td><td>0x90ED447C</td><td>No</td></tr>
<tr><td>Supply Drop (AT CH)</td><td>0xB8BE94F2</td><td>No</td></tr>
<tr><td>Supply Drop (Base)</td><td>0xA0C609B1</td><td>No</td></tr>
<tr><td>Supply Drop (Blanco)</td><td>0x9283570F</td><td>No</td></tr>
<tr><td>Supply Drop (Blueprints)</td><td>0xD4ED05B4</td><td>No</td></tr>
<tr><td>Supply Drop (C4)</td><td>0x92AC6643</td><td>No</td></tr>
<tr><td>Supply Drop (C4) (VZ)</td><td>0x55F3D8C0</td><td>No</td></tr>
<tr><td>Supply Drop (Chinese)</td><td>0x86D23BC9</td><td>No</td></tr>
<tr><td>Supply Drop (Covert)</td><td>0xD2DF8435</td><td>No</td></tr>
<tr><td>Supply Drop (CQB)</td><td>0x6C9225B0</td><td>No</td></tr>
<tr><td>Supply Drop (FIona)</td><td>0x28CF74B9</td><td>No</td></tr>
<tr><td>Supply Drop (GL)</td><td>0xC2CA593F</td><td>No</td></tr>
<tr><td>Supply Drop (Guerilla)</td><td>0xB1A00939</td><td>No</td></tr>
<tr><td>Supply Drop (Guerilla) (Sniper)</td><td>0x508A7D49</td><td>No</td></tr>
<tr><td>Supply Drop (Health)</td><td>0x87B6441E</td><td>No</td></tr>
<tr><td>Supply Drop (Light MG)</td><td>0xF5FA7F08</td><td>No</td></tr>
<tr><td>Supply Drop (Light MG) (AL)</td><td>0x558DE1B0</td><td>No</td></tr>
<tr><td>Supply Drop (OC)</td><td>0x81B20DAE</td><td>No</td></tr>
<tr><td>Supply Drop (Pirate)</td><td>0x5EEB052D</td><td>No</td></tr>
<tr><td>Supply Drop (RPG)</td><td>0xC22DA165</td><td>No</td></tr>
<tr><td>Supply Drop (Sniper CH)</td><td>0x52D9BD68</td><td>No</td></tr>
<tr><td>Supply Drop (Sniper RU)</td><td>0xA924BBE2</td><td>No</td></tr>
<tr><td>Supply Drop (Sniper)</td><td>0xFCC499E7</td><td>No</td></tr>
<tr><td>Supply Drop (Support)</td><td>0x9282B9C9</td><td>No</td></tr>
<tr><td>Supply Drop (Treasure)</td><td>0x3227E7D1</td><td>No</td></tr>
<tr><td>Supply Drop (VZ)</td><td>0xCF4EC76C</td><td>No</td></tr>
<tr><td>Support Vehicle (727)</td><td>0x017141B5</td><td>No</td></tr>
<tr><td>Support Vehicle (727) low altitude</td><td>0xFC0FFB37</td><td>No</td></tr>
<tr><td>Support Vehicle (A10)</td><td>0xFC0C8C31</td><td>No</td></tr>
<tr><td>Support Vehicle (A10) low altitude</td><td>0x1067B683</td><td>No</td></tr>
<tr><td>Support Vehicle (AC130)</td><td>0x5676F5D3</td><td>Yes</td></tr>
<tr><td>Support Vehicle (Autogunship)</td><td>0xE76E828E</td><td>Yes</td></tr>
<tr><td>Support Vehicle (B2)</td><td>0x3B379C6F</td><td>No</td></tr>
<tr><td>Support Vehicle (B2) low altitude</td><td>0x406CAF95</td><td>No</td></tr>
<tr><td>Support Vehicle (Base)</td><td>0xC421D9BA</td><td>No</td></tr>
<tr><td>Support Vehicle (C130)</td><td>0xA4FEAE5C</td><td>Yes</td></tr>
<tr><td>Support Vehicle (C130) low altitude</td><td>0xDD6E1014</td><td>Yes</td></tr>
<tr><td>Support Vehicle (Cessna)</td><td>0x31DDDFC8</td><td>No</td></tr>
<tr><td>Support Vehicle (Cessna) low altitude</td><td>0x3115FAD0</td><td>No</td></tr>
<tr><td>Support Vehicle (Cruise Missile)</td><td>0x7FEE61A0</td><td>No</td></tr>
<tr><td>Support Vehicle (F117)</td><td>0x70C3E492</td><td>No</td></tr>
<tr><td>Support Vehicle (F117) low altitude</td><td>0x2717978E</td><td>No</td></tr>
<tr><td>Support Vehicle (F35)</td><td>0xE616BA41</td><td>Yes</td></tr>
<tr><td>Support Vehicle (F35) low altitude</td><td>0x648C7473</td><td>Yes</td></tr>
<tr><td>Support Vehicle (Mig27)</td><td>0xE74AC2EB</td><td>No</td></tr>
<tr><td>Support Vehicle (Mig27) low altitude</td><td>0x41B5E531</td><td>No</td></tr>
<tr><td>Support Vehicle (OV10)</td><td>0x55CCD133</td><td>No</td></tr>
<tr><td>Support Vehicle (OV10) low altitude</td><td>0x69308989</td><td>No</td></tr>
<tr><td>Support Vehicle (Paradrop_AL)</td><td>0xCD6B7326</td><td>No</td></tr>
<tr><td>Support Vehicle (Paradrop_ch)</td><td>0xEC808918</td><td>No</td></tr>
<tr><td>Support Vehicle (Predator)</td><td>0xB81F9838</td><td>No</td></tr>
<tr><td>Support Vehicle (Predator) low altitude</td><td>0x5BCCABA0</td><td>No</td></tr>
<tr><td>Support Vehicle (Q5)</td><td>0xD78EE851</td><td>No</td></tr>
<tr><td>Support Vehicle (Q5) low altitude</td><td>0xBE7DE823</td><td>No</td></tr>
<tr><td>Support Vehicle (Transport)</td><td>0x6BF9A5EA</td><td>No</td></tr>
<tr><td>Support Vehicle (Tucano)</td><td>0x03501723</td><td>No</td></tr>
<tr><td>Support Vehicle (Tucano) low altitude</td><td>0x89AB7899</td><td>No</td></tr>
<tr><td>Surgical Strike Projectile</td><td>0xDB16CC58</td><td>No</td></tr>
<tr><td>Surgical Strike Shrapnel</td><td>0xF791712E</td><td>No</td></tr>
<tr><td>SX2150 (Base)</td><td>0x75BC4C18</td><td>No</td></tr>
<tr><td>SX2150 (Cargo)</td><td>0xCA6EEAB9</td><td>No</td></tr>
<tr><td>SX2150 (Cargo) (Driver)</td><td>0x71E26394</td><td>No</td></tr>
<tr><td>SX2150 (Cargo) (Full)</td><td>0x24FE6B53</td><td>No</td></tr>
<tr><td>SX2150 (Fuel)</td><td>0x4778F921</td><td>No</td></tr>
<tr><td>SX2150 (Fuel) (Driver)</td><td>0x2AB6483C</td><td>No</td></tr>
<tr><td>SX2150 (Fuel) (Full)</td><td>0x07BA4D2B</td><td>No</td></tr>
<tr><td>SX2150 (MLRS)</td><td>0xFBDC7E43</td><td>No</td></tr>
<tr><td>SX2150 (MLRS) (Driver)</td><td>0xADD73D9E</td><td>No</td></tr>
<tr><td>SX2150 (MLRS) (Full)</td><td>0x648129E5</td><td>No</td></tr>
<tr><td>SX2150 (Semi)</td><td>0x71470A0F</td><td>No</td></tr>
<tr><td>SX2150 (Semi) (Driver)</td><td>0xD92DEBBA</td><td>No</td></tr>
<tr><td>SX2150 (Semi) (Full)</td><td>0xAE08EBF9</td><td>No</td></tr>
<tr><td>SX2150_Driver</td><td>0xE489AB3D</td><td>No</td></tr>
<tr><td>T300 (base)</td><td>0x273374D2</td><td>No</td></tr>
<tr><td>T300 (Driver)</td><td>0x239E95E5</td><td>No</td></tr>
<tr><td>T300 (empty)</td><td>0x8F3EC4FE</td><td>No</td></tr>
<tr><td>T300 (Full)</td><td>0x8270C192</td><td>No</td></tr>
<tr><td>T300 (M60)</td><td>0x9A974376</td><td>No</td></tr>
<tr><td>T300 (M60) (Driver)</td><td>0xD05B27CD</td><td>No</td></tr>
<tr><td>T300 (M60) (DriverGunner)</td><td>0x19C77906</td><td>No</td></tr>
<tr><td>T300 (M60) (Full)</td><td>0xD68EDD6A</td><td>No</td></tr>
<tr><td>Tank</td><td>0xC686AE99</td><td>Yes</td></tr>
<tr><td>Tank Bike</td><td>0x0ADFFAD4</td><td>Yes</td></tr>
<tr><td>Tank Commander</td><td>0x413AB10F</td><td>Yes</td></tr>
<tr><td>Tank Seat (Driver) (Civ)</td><td>0xBF349994</td><td>Yes</td></tr>
<tr><td>Tank Seat (Driver) (VZ)</td><td>0x0A5CB4A4</td><td>Yes</td></tr>
<tr><td>Tank Seat (Gunner) (VZ)</td><td>0xF2E099CF</td><td>Yes</td></tr>
<tr><td>Tank Shell (Artillery)</td><td>0x724BBEC8</td><td>Yes</td></tr>
<tr><td>Tank Shell (Default)</td><td>0xAB81CFDB</td><td>Yes</td></tr>
<tr><td>Tank Shell (Sabot)</td><td>0x5FB2FB87</td><td>Yes</td></tr>
<tr><td>Tank Shell (Weak)</td><td>0x3AC5E254</td><td>Yes</td></tr>
<tr><td>TankBike_Driver</td><td>0xF04D95EB</td><td>Yes</td></tr>
<tr><td>Taxi (Tercel)</td><td>0x3D094D4F</td><td>No</td></tr>
<tr><td>Taxi (Tercel) (Driver)</td><td>0xC92AD97A</td><td>No</td></tr>
<tr><td>Taxi (Tercel) (Driver) (Civ Taxi Driver male)</td><td>0x7808D20E</td><td>No</td></tr>
<tr><td>TCTest1</td><td>0x201CAADF</td><td>No</td></tr>
<tr><td>TCTest2</td><td>0x961FA338</td><td>No</td></tr>
<tr><td>Telephone Pole Test</td><td>0x56607881</td><td>No</td></tr>
<tr><td>telephone wire</td><td>0xE631DF46</td><td>No</td></tr>
<tr><td>telephones</td><td>0xA4D5C112</td><td>No</td></tr>
<tr><td>Teleporter</td><td>0x60A7C059</td><td>No</td></tr>
<tr><td>Tercel_Driver</td><td>0xB97625FF</td><td>No</td></tr>
<tr><td>terrain</td><td>0x19FC10AC</td><td>No</td></tr>
<tr><td>Terrain_128</td><td>0x0729ED62</td><td>No</td></tr>
<tr><td>Terrain_512</td><td>0xF3D1E031</td><td>No</td></tr>
<tr><td>Test Explosion Large</td><td>0xEAC413B5</td><td>No</td></tr>
<tr><td>Test Explosion Medium</td><td>0xCC1BDA91</td><td>No</td></tr>
<tr><td>TestBossBattle</td><td>0xF1D8C824</td><td>No</td></tr>
<tr><td>testdust</td><td>0x9623D53D</td><td>No</td></tr>
<tr><td>testPris</td><td>0xEF2CD5E3</td><td>No</td></tr>
<tr><td>testPris2</td><td>0x4C8103B3</td><td>No</td></tr>
<tr><td>testPris3</td><td>0xEA7E2AD6</td><td>No</td></tr>
<tr><td>testPris4</td><td>0xF48F83B5</td><td>No</td></tr>
<tr><td>TestSingleSpawn</td><td>0x535D2B8A</td><td>No</td></tr>
<tr><td>TestSkirmish</td><td>0xE7A37705</td><td>No</td></tr>
<tr><td>TestSpawn1</td><td>0x858B4C93</td><td>No</td></tr>
<tr><td>TestSpawn2</td><td>0xAB8DC6FC</td><td>No</td></tr>
<tr><td>TestTree</td><td>0xD5A65B0D</td><td>No</td></tr>
<tr><td>ThirstyFountain</td><td>0xD9EC1F0A</td><td>No</td></tr>
<tr><td>Thunder</td><td>0x5404A661</td><td>No</td></tr>
<tr><td>Thunder (black)</td><td>0xB32B3EC3</td><td>No</td></tr>
<tr><td>Thunder (blue)</td><td>0xB2373196</td><td>No</td></tr>
<tr><td>Thunder (Driver)</td><td>0x41BC9AFC</td><td>No</td></tr>
<tr><td>Thunder (Driver) (Civ Business B Male)</td><td>0x0B421BB2</td><td>No</td></tr>
<tr><td>Thunder (Driver) (Civ Business Female)</td><td>0x4112D58D</td><td>No</td></tr>
<tr><td>Thunder (Driver) (Civ Business Male)</td><td>0xBAA9A0A0</td><td>No</td></tr>
<tr><td>Thunder (Driver) (Civ Poor female)</td><td>0x7FB36213</td><td>No</td></tr>
<tr><td>Thunder (Driver) (Civ Poor Male)</td><td>0x39F4B542</td><td>No</td></tr>
<tr><td>Thunder (Driver) (Civ Rich Female)</td><td>0xEBF64761</td><td>No</td></tr>
<tr><td>Thunder (Driver) (Civ Rich Male)</td><td>0x0F9A0C04</td><td>No</td></tr>
<tr><td>Thunder (green)</td><td>0xB2F606A3</td><td>No</td></tr>
<tr><td>Thunder (lightblue)</td><td>0x7ED17AF8</td><td>No</td></tr>
<tr><td>Thunder (orange)</td><td>0x29654040</td><td>No</td></tr>
<tr><td>Thunder (red)</td><td>0x17EDC823</td><td>No</td></tr>
<tr><td>Thunder (white)</td><td>0x23FCA7D1</td><td>No</td></tr>
<tr><td>Thunder_Driver</td><td>0x56146B5A</td><td>No</td></tr>
<tr><td>Tiny Geometry Component Master</td><td>0x3A5B45C2</td><td>No</td></tr>
<tr><td>TinyFlame</td><td>0x4FD293F4</td><td>No</td></tr>
<tr><td>TinyGeometry</td><td>0xA5D1E0AB</td><td>No</td></tr>
<tr><td>TinyGeometryHowto</td><td>0x0F613E38</td><td>No</td></tr>
<tr><td>TinyGeometryVZ</td><td>0xD1B92D9F</td><td>No</td></tr>
<tr><td>TinyGeometryVZ_064</td><td>0x811764F8</td><td>No</td></tr>
<tr><td>TinyGeometryVZ_128</td><td>0x5853A8E1</td><td>No</td></tr>
<tr><td>TinyGeometryVZ_2048</td><td>0x18EA2F8C</td><td>No</td></tr>
<tr><td>TinyGeometryVZ_256</td><td>0xF10D0A65</td><td>No</td></tr>
<tr><td>TinyGeometryVZ_512</td><td>0x0C21C446</td><td>No</td></tr>
<tr><td>TiredBench</td><td>0x461B2F79</td><td>No</td></tr>
<tr><td>TiredBenchSpawner</td><td>0x4DC7CB7B</td><td>No</td></tr>
<tr><td>TiredBenchSpawner (Crying)</td><td>0x065DF86C</td><td>No</td></tr>
<tr><td>TOW Missile</td><td>0xE744DC15</td><td>No</td></tr>
<tr><td>TOW Missile (Hellfire)</td><td>0x415A7711</td><td>No</td></tr>
<tr><td>TowerDestructTemplate</td><td>0xF25CC7D0</td><td>No</td></tr>
<tr><td>Traffic Gur HQ List</td><td>0x976BBEE1</td><td>No</td></tr>
<tr><td>Traffic Zones</td><td>0x13EEFF25</td><td>No</td></tr>
<tr><td>TrafficLight_2</td><td>0xD2CEA177</td><td>No</td></tr>
<tr><td>TrafficLight__</td><td>0x694D0AAE</td><td>No</td></tr>
<tr><td>Trailer</td><td>0x8D3354FE</td><td>No</td></tr>
<tr><td>Trailer_Driver</td><td>0x8F5AF747</td><td>No</td></tr>
<tr><td>Transport Truck</td><td>0x190F4FD9</td><td>Yes</td></tr>
<tr><td>Transport Truck (Driver)</td><td>0x926CE734</td><td>Yes</td></tr>
<tr><td>Transport Truck (Driver) (Mechanic male)</td><td>0x3847E5AE</td><td>Yes</td></tr>
<tr><td>Transport Truck_Ruined</td><td>0x73CCD9ED</td><td>Yes</td></tr>
<tr><td>Transport_Ruin</td><td>0x459EA631</td><td>No</td></tr>
<tr><td>Transport_Ruin_Fire</td><td>0x063B655C</td><td>No</td></tr>
<tr><td>TransportTruck_Driver</td><td>0x20A97A76</td><td>Yes</td></tr>
<tr><td>trash01</td><td>0x33859570</td><td>No</td></tr>
<tr><td>Tree_Scrub</td><td>0x170A44B5</td><td>No</td></tr>
<tr><td>TreeTrunkDebrisTemplate</td><td>0x5280B8DA</td><td>No</td></tr>
<tr><td>TriggerTimer AllCon002 Pipes</td><td>0xB50876EA</td><td>No</td></tr>
<tr><td>TriggerTimer AllCon002 Pipes Effect</td><td>0x7921548D</td><td>No</td></tr>
<tr><td>TrooperPooper</td><td>0x1A037D7D</td><td>No</td></tr>
<tr><td>Turbosquid</td><td>0x072C3307</td><td>No</td></tr>
<tr><td>Turbosquid (CIV)</td><td>0x5C820F44</td><td>No</td></tr>
<tr><td>Turbosquid (CIV) (Driver)</td><td>0x26AF3A23</td><td>No</td></tr>
<tr><td>Turbosquid (CIV) (Driver) (Civ Poor female)</td><td>0xE6C337D8</td><td>No</td></tr>
<tr><td>Turbosquid (CIV) (Driver) (Civ Poor male)</td><td>0x24098509</td><td>No</td></tr>
<tr><td>Turbosquid (CIV) (Driver) DEPRECATED</td><td>0xAF9255AE</td><td>No</td></tr>
<tr><td>Turbosquid (GR)</td><td>0x25588685</td><td>No</td></tr>
<tr><td>Turbosquid (GR) (Driver)</td><td>0x60D20390</td><td>No</td></tr>
<tr><td>Turbosquid (GR) (DriverGunner)</td><td>0xB868CBCF</td><td>No</td></tr>
<tr><td>Turbosquid (GR) (Full)</td><td>0x0764DF27</td><td>No</td></tr>
<tr><td>Turbosquid (OC)</td><td>0xAB3108D6</td><td>No</td></tr>
<tr><td>Turbosquid (OC) (Driver)</td><td>0xCDE44AAD</td><td>No</td></tr>
<tr><td>Turbosquid (OC) (Full)</td><td>0x41E6A84A</td><td>No</td></tr>
<tr><td>Type 14310</td><td>0xB68095D8</td><td>No</td></tr>
<tr><td>Type 14310 (Driver)</td><td>0x29610037</td><td>No</td></tr>
<tr><td>Type 14310 (Full)</td><td>0xF594057C</td><td>No</td></tr>
<tr><td>Type 14310 (Non AA)</td><td>0x611DF226</td><td>No</td></tr>
<tr><td>Type 14310 (Non AA) (Driver)</td><td>0x2D4BC03D</td><td>No</td></tr>
<tr><td>Type 14310 (Non AA) (Full)</td><td>0xE646A49A</td><td>No</td></tr>
<tr><td>Type14310_Driver</td><td>0xCD6B097F</td><td>No</td></tr>
<tr><td>U1 Transport (PMC) (AL Insertion)</td><td>0x2FB13A66</td><td>No</td></tr>
<tr><td>U1 Transport (PMC) (CH Insertion)</td><td>0xEF50F86C</td><td>No</td></tr>
<tr><td>U1 Transport (PMC) (GR Insertion)</td><td>0x964AB6EA</td><td>No</td></tr>
<tr><td>U1 Transport (PMC) (OC Insertion)</td><td>0x3A0624A1</td><td>No</td></tr>
<tr><td>U1 Transport (PMC) (PR Insertion)</td><td>0xA71C3C19</td><td>No</td></tr>
<tr><td>UH1</td><td>0x218895A3</td><td>Yes</td></tr>
<tr><td>UH1 Attack</td><td>0xEE6C2DE9</td><td>Yes</td></tr>
<tr><td>UH1 Attack (PMC)</td><td>0x89FBE62C</td><td>Yes</td></tr>
<tr><td>UH1 Attack (PMC) (Driver)</td><td>0x9FECF32B</td><td>Yes</td></tr>
<tr><td>UH1 Attack (PMC) (Driver) (Railshooter)</td><td>0x548C503E</td><td>Yes</td></tr>
<tr><td>UH1 Attack (PMC) HelCon</td><td>0xE8ED7D25</td><td>Yes</td></tr>
<tr><td>UH1 Elite</td><td>0xA9674B56</td><td>Yes</td></tr>
<tr><td>UH1 Superiority</td><td>0x4015A778</td><td>Yes</td></tr>
<tr><td>UH1 Transport</td><td>0xCA1D5C24</td><td>Yes</td></tr>
<tr><td>UH1 Transport (GR)</td><td>0x7EECCD94</td><td>Yes</td></tr>
<tr><td>UH1 Transport (GR) (Delivery)</td><td>0xAEF1F11D</td><td>Yes</td></tr>
<tr><td>UH1 Transport (GR) (Driver)</td><td>0x05B41E73</td><td>Yes</td></tr>
<tr><td>UH1 Transport (GR) (Ewan)</td><td>0x0CF7687A</td><td>Yes</td></tr>
<tr><td>UH1 Transport (GR) (Extraction)</td><td>0x76D9AD80</td><td>Yes</td></tr>
<tr><td>UH1 Transport (GR) (Full)</td><td>0x1BAAE2A0</td><td>Yes</td></tr>
<tr><td>UH1 Transport (GR) (Full) (RPG)</td><td>0xDBFA90EA</td><td>Yes</td></tr>
<tr><td>UH1 Transport (PMC)</td><td>0x79415FA1</td><td>Yes</td></tr>
<tr><td>UH1 Transport (PMC) (Driver)</td><td>0x0CCF93BC</td><td>Yes</td></tr>
<tr><td>UH1 Transport (PMC) (Extraction)</td><td>0x1CB07287</td><td>Yes</td></tr>
<tr><td>UH1 Transport (PMC) (Ghost)</td><td>0xECB8938F</td><td>Yes</td></tr>
<tr><td>UH1 Transport (Pursuit)</td><td>0x81C04A3B</td><td>Yes</td></tr>
<tr><td>UH1 Transport (Transit)</td><td>0xAC41D6F2</td><td>Yes</td></tr>
<tr><td>UnitList1</td><td>0xEFBB2A10</td><td>No</td></tr>
<tr><td>UnlockableAbel</td><td>0x2D666C6B</td><td>No</td></tr>
<tr><td>UnlockableBlanco</td><td>0x82AEA2E8</td><td>No</td></tr>
<tr><td>UnlockableCarlos</td><td>0x8F185DB1</td><td>No</td></tr>
<tr><td>UnlockableDiablo</td><td>0x26E87C5A</td><td>No</td></tr>
<tr><td>UnlockableEva</td><td>0xB5471149</td><td>No</td></tr>
<tr><td>UnlockableEwan</td><td>0x47966194</td><td>No</td></tr>
<tr><td>UnlockableFiona</td><td>0x84E26766</td><td>No</td></tr>
<tr><td>UnlockableFire</td><td>0x9E408529</td><td>No</td></tr>
<tr><td>UnlockableGauge</td><td>0x6CD8F24E</td><td>No</td></tr>
<tr><td>UnlockableGhost</td><td>0x025545AE</td><td>No</td></tr>
<tr><td>UnlockableHoang</td><td>0xC0D17EC6</td><td>No</td></tr>
<tr><td>UnlockableMisha</td><td>0xB74302B3</td><td>No</td></tr>
<tr><td>UnlockableVasquez</td><td>0x8EE21A12</td><td>No</td></tr>
<tr><td>UnlockableWingman</td><td>0xA944E334</td><td>No</td></tr>
<tr><td>UrbanCarList</td><td>0xD8C4E86B</td><td>No</td></tr>
<tr><td>V22 (Delivery)</td><td>0xA4F6D8C6</td><td>No</td></tr>
<tr><td>V22 (Driver)</td><td>0x65E28854</td><td>No</td></tr>
<tr><td>V22 - DO NOT USE</td><td>0x18EBA05D</td><td>No</td></tr>
<tr><td>Valiant</td><td>0x540A0D66</td><td>No</td></tr>
<tr><td>Valiant (4door)</td><td>0x92CDA237</td><td>No</td></tr>
<tr><td>Valiant (4door) (Driver)</td><td>0x89EFADE2</td><td>No</td></tr>
<tr><td>Valiant (4door) (Driver) (Civ Business B male)</td><td>0xC78FAA18</td><td>No</td></tr>
<tr><td>Valiant (base)</td><td>0x23E1281A</td><td>No</td></tr>
<tr><td>Valiant (crappy)</td><td>0x1E22A2D4</td><td>No</td></tr>
<tr><td>Valiant (crappy) (Driver)</td><td>0x4530C533</td><td>No</td></tr>
<tr><td>Valiant (crappy) (Driver) (Civ Poor female)</td><td>0xD0A49A88</td><td>No</td></tr>
<tr><td>Valiant (crappy) (Driver) (Civ Poor male)</td><td>0xF47F02F9</td><td>No</td></tr>
<tr><td>Valiant (Driver)</td><td>0x6C5D91FD</td><td>No</td></tr>
<tr><td>Valiant (Driver) (Civ Business B male)</td><td>0x7D56DF57</td><td>No</td></tr>
<tr><td>Valiant (Driver) (Civ casual female)</td><td>0x3A038FA5</td><td>No</td></tr>
<tr><td>Valiant (Driver) (Civ casual male)</td><td>0x38F88238</td><td>No</td></tr>
<tr><td>Valiant (Driver) (Civ poor female)</td><td>0x6F9DCC92</td><td>No</td></tr>
<tr><td>Valiant (Driver) (Civ poor male)</td><td>0xD8A843B7</td><td>No</td></tr>
<tr><td>Valiant (Python)</td><td>0xCF4FA909</td><td>No</td></tr>
<tr><td>Valiant (Python) (Mechanic male)</td><td>0xEE96CC27</td><td>No</td></tr>
<tr><td>Valiant_Driver</td><td>0xBEC37ADF</td><td>No</td></tr>
<tr><td>ValiantCrappy_Driver</td><td>0xE0580DA0</td><td>No</td></tr>
<tr><td>ValiantPython_Driver</td><td>0xCB03BAA5</td><td>No</td></tr>
<tr><td>Van (base)</td><td>0x07A72F20</td><td>No</td></tr>
<tr><td>Van (Commercial)</td><td>0x1410F16F</td><td>No</td></tr>
<tr><td>Van (Commercial) (Driver)</td><td>0x0C41679A</td><td>No</td></tr>
<tr><td>Van (Commercial) (Driver) (Civ Casual female)</td><td>0x12368D32</td><td>No</td></tr>
<tr><td>Van (Commercial) (Driver) (Civ Casual male)</td><td>0x0A2B92D7</td><td>No</td></tr>
<tr><td>Van (Commercial) (Driver) (Civ Industrial female)</td><td>0x1F02BD0C</td><td>No</td></tr>
<tr><td>Van (Commercial) (Driver) (Civ Industrial male)</td><td>0xE34E881D</td><td>No</td></tr>
<tr><td>Van (Crappy)</td><td>0x1405526A</td><td>No</td></tr>
<tr><td>Van (Crappy) (Driver)</td><td>0x6686F151</td><td>No</td></tr>
<tr><td>Van (Crappy) (Driver) (Civ Poor female)</td><td>0xC4CDF206</td><td>No</td></tr>
<tr><td>Van (Crappy) (Driver) (Civ Poor male)</td><td>0xAB04BE3B</td><td>No</td></tr>
<tr><td>Van (Green)</td><td>0x4CD82092</td><td>No</td></tr>
<tr><td>Van (Green) (Driver)</td><td>0x817DEE39</td><td>No</td></tr>
<tr><td>Van (Green) (Driver) (Civ Poor female)</td><td>0xB4B2273E</td><td>No</td></tr>
<tr><td>Van (Green) (Driver) (Civ Poor male)</td><td>0x50C518B3</td><td>No</td></tr>
<tr><td>Van (Racing)</td><td>0xB3F6FAA3</td><td>No</td></tr>
<tr><td>Van (Racing) (Driver)</td><td>0xF9CEA07E</td><td>No</td></tr>
<tr><td>Van (Racing) (Driver) (Civ Motorcycle male)</td><td>0x6970528B</td><td>Yes</td></tr>
<tr><td>Van (Taxi)</td><td>0x89323325</td><td>No</td></tr>
<tr><td>Van (Taxi) (Driver)</td><td>0x36BE9030</td><td>No</td></tr>
<tr><td>Van (Taxi) (Driver) (Civ Taxi Driver male)</td><td>0x1073BB1C</td><td>No</td></tr>
<tr><td>Van_Driver</td><td>0x35634C45</td><td>No</td></tr>
<tr><td>Vanquish</td><td>0x7E6FC182</td><td>No</td></tr>
<tr><td>Vanquish (base)</td><td>0xCA4FDA36</td><td>No</td></tr>
<tr><td>Vanquish (Racing)</td><td>0x1B533F71</td><td>No</td></tr>
<tr><td>Vanquish_Driver</td><td>0xE6C5B343</td><td>No</td></tr>
<tr><td>VanRacing_Driver</td><td>0x491C15DF</td><td>No</td></tr>
<tr><td>Vehicle A12ATGM Missile</td><td>0x8D37601C</td><td>No</td></tr>
<tr><td>Vehicle AA Missile</td><td>0x64008733</td><td>No</td></tr>
<tr><td>Vehicle AA Missile (sidewinder)</td><td>0x5996DDFE</td><td>No</td></tr>
<tr><td>Vehicle AA Missile (stinger)</td><td>0xA7913CBC</td><td>No</td></tr>
<tr><td>Vehicle AT Missile</td><td>0xDCAE66D6</td><td>No</td></tr>
<tr><td>Vehicle AT Missile (Hellfire)</td><td>0x6951B31C</td><td>No</td></tr>
<tr><td>Vehicle AT Missile (mi35)</td><td>0x655324B9</td><td>Yes</td></tr>
<tr><td>Vehicle Camera (LargeA) (Driver)</td><td>0x2F044516</td><td>No</td></tr>
<tr><td>Vehicle Camera (LargeA) (front_right)</td><td>0x175A6E7C</td><td>No</td></tr>
<tr><td>Vehicle Camera (LargeA) (rear_left)</td><td>0x7A697900</td><td>No</td></tr>
<tr><td>Vehicle Camera (LargeA) (rear_right)</td><td>0x84E1DA0B</td><td>No</td></tr>
<tr><td>Vehicle Camera (LargeB) (Driver)</td><td>0x85DF704D</td><td>No</td></tr>
<tr><td>Vehicle Camera (LargeB) (front_right)</td><td>0x0595F839</td><td>No</td></tr>
<tr><td>Vehicle Camera (LargeB) (rear_left)</td><td>0xFD105EC9</td><td>No</td></tr>
<tr><td>Vehicle Camera (LargeB) (rear_right)</td><td>0x6FA03DD0</td><td>No</td></tr>
<tr><td>Vehicle Camera (LargeC) (Driver)</td><td>0xA2DB7EA8</td><td>No</td></tr>
<tr><td>Vehicle Camera (LargeC) (front_right)</td><td>0x3DD6087A</td><td>No</td></tr>
<tr><td>Vehicle Camera (Medium) (Driver)</td><td>0x5903B001</td><td>No</td></tr>
<tr><td>Vehicle Camera (Medium) (front_right)</td><td>0x39D3E695</td><td>No</td></tr>
<tr><td>Vehicle Camera (Medium) (Rear Gunner)</td><td>0x16A4173E</td><td>No</td></tr>
<tr><td>Vehicle Camera (Small) (Driver)</td><td>0xDF62F009</td><td>No</td></tr>
<tr><td>Vehicle Camera (Small) (front_right)</td><td>0x6A536B0D</td><td>No</td></tr>
<tr><td>Vehicle Cargo (DoNotUse)</td><td>0x732BFA4D</td><td>No</td></tr>
<tr><td>Vehicle Chunk Set (Armored)</td><td>0x77C213C7</td><td>No</td></tr>
<tr><td>Vehicle Chunk Set (Extra Large)</td><td>0x117A6C04</td><td>No</td></tr>
<tr><td>Vehicle Chunk Set (LargeA)</td><td>0xF11CF3BB</td><td>No</td></tr>
<tr><td>Vehicle Chunk Set (LargeB)</td><td>0xB5F3AC76</td><td>No</td></tr>
<tr><td>Vehicle Chunk Set (Medium)</td><td>0xF85207DA</td><td>No</td></tr>
<tr><td>Vehicle Chunk Set (Motorcycle)</td><td>0xF21E5DF8</td><td>Yes</td></tr>
<tr><td>Vehicle Chunk Set (Small)</td><td>0xA545B962</td><td>No</td></tr>
<tr><td>Vehicle Class (2seat w/ Rear Gunner)</td><td>0x1CAA032A</td><td>No</td></tr>
<tr><td>Vehicle Class (2seat)</td><td>0xB40E7285</td><td>No</td></tr>
<tr><td>Vehicle Class (4seat w/ Rear Gunner)</td><td>0x17745348</td><td>No</td></tr>
<tr><td>Vehicle Class (4seat w/ Rear Gunner) (Full) (GR)</td><td>0xA56A034C</td><td>No</td></tr>
<tr><td>Vehicle Class (4seat w/ Rear Gunner) (Full) (OC)</td><td>0x991FAC2B</td><td>No</td></tr>
<tr><td>Vehicle Class (4seat)</td><td>0x57931C4F</td><td>No</td></tr>
<tr><td>Vehicle Class (Buggy)</td><td>0x0F495930</td><td>Yes</td></tr>
<tr><td>Vehicle Class (LargeB)</td><td>0xA1E06D53</td><td>No</td></tr>
<tr><td>Vehicle Class (Medium)</td><td>0xE0E69EBB</td><td>No</td></tr>
<tr><td>Vehicle Class (Small)</td><td>0x0B561C45</td><td>No</td></tr>
<tr><td>Vehicle Entrance</td><td>0x7A4310F3</td><td>No</td></tr>
<tr><td>Vehicle Entrance (_Default Boat)</td><td>0x2FAE9FA6</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (_Default Boat) Small Radius</td><td>0x130EE163</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (_Default)</td><td>0x1E6DF616</td><td>No</td></tr>
<tr><td>Vehicle Entrance (_Default) MatchSpeedonExit</td><td>0x01E97725</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (AH1Z)</td><td>0x155792CB</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (AMX30 AA)</td><td>0x38EDD3EC</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (AMX30)</td><td>0x098E2A74</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Armored Bank Truck)</td><td>0xD8F3BB56</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (F35b)</td><td>0x522A4BA1</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Ka29b)</td><td>0x3F3A3CE4</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (M113)</td><td>0xE2CF0943</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (M1A2)</td><td>0x6A680ECC</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (M2A3)</td><td>0xA17E6C56</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (M551)</td><td>0x518B06ED</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (MD500)</td><td>0xD2D32C0D</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (MH53J Pavelow)</td><td>0xF2DA1950</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Mi26)</td><td>0xB5F3795B</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Mi35 Solano)</td><td>0x7F1FFF69</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Mi35)</td><td>0xE5E8BF9F</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (PGZ95)</td><td>0xD7ADF06A</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (PLZ45)</td><td>0x3E083794</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Scorpion90)</td><td>0xADC54D35</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Stingray II)</td><td>0x3DFDEBAA</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (UH1)</td><td>0x546B7A35</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (WZ10)</td><td>0x9E49FA89</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (WZ551)</td><td>0x81D36417</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (ZBD2000)</td><td>0x9D58E683</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (ZTZ63a)</td><td>0x4D4A5673</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (ZTZ98)</td><td>0xB990D3B0</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Airboat Entrance Left)</td><td>0xAE0D5BA3</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Airboat Entrance Right)</td><td>0x1F3E218A</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Alouette3 Driver)</td><td>0x790EC576</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (APC Rear Hatch)</td><td>0x147B03C6</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Armored Bank Truck Rear)</td><td>0x6FF33079</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Barco) (Driver)</td><td>0x84CC9268</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Boarding Entrance)</td><td>0xBC368B84</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Boarding Entrance) Speedboat</td><td>0xB60128C3</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Boarding Exit)</td><td>0x2BB6EBA2</td><td>No</td></tr>
<tr><td>Vehicle Entrance (CH Destroyer) (Driver)</td><td>0x2014C719</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Cutter Rear Top)</td><td>0x3E64FABE</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Dinghy Entrance Left)</td><td>0x97E00B58</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Dinghy Entrance Right)</td><td>0xEC65DEE3</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Entrance Front Left)</td><td>0x531E3F0C</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Entrance Front Right)</td><td>0xD23F20BF</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Entrance Middle Left)</td><td>0x22F97470</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Entrance Middle Right)</td><td>0x545CD87B</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Entrance Rear Gunner)</td><td>0x19550473</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Entrance Rear Left)</td><td>0x69E8FD09</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Entrance Rear Middle)</td><td>0x096397DD</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Entrance Rear Right)</td><td>0x4CFBAD10</td><td>No</td></tr>
<tr><td>Vehicle Entrance (EXT Rear Hatch)</td><td>0x5BA9046D</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Extraction) (Entrance Rear Left)</td><td>0x879E8BBB</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Extraction) (Entrance Rear Right)</td><td>0x54E244E2</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Fishing Boat Driver)</td><td>0x1CFCEF3C</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Guntruck Rear Middle)</td><td>0x4AF3110E</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Huangfeng Driver)</td><td>0x89262A07</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Jetski Entrance Left)</td><td>0xDCE5469B</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Jetski Entrance Right)</td><td>0xCDC4C1C2</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Jetski Entrance Top)</td><td>0x599BB107</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Ka29b Driver)</td><td>0x2C59AD71</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Ka29b Rear Left)</td><td>0xF9E85EFC</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Ka29b Rear Right)</td><td>0x193FA42F</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Ladder)</td><td>0xA5E62C0C</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Ladder) (Boat)</td><td>0xFC1AFCB7</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Ladder) Boat</td><td>0xD0CCBF76</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Ladder) Long</td><td>0x34975F2A</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Ladder) Long Boat</td><td>0x86D24820</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Ladder) Small Radius</td><td>0x11CF9D89</td><td>No</td></tr>
<tr><td>Vehicle Entrance (LAVIII 25 Gunner)</td><td>0xA6C26784</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (LAVIII Driver)</td><td>0x44554A38</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (LAVIII Gunner)</td><td>0xBD7BD769</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (LAVIII MGS Driver)</td><td>0x3A01CD63</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (LAVIII MGS Gunner)</td><td>0xFBA91556</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (LAVIII MGS Rear Left)</td><td>0xD26C0F5A</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (LAVIII Rear Left)</td><td>0x4CC53CB7</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (LAVIII Rear Right)</td><td>0x0FAEE3B6</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (LCUR Driver)</td><td>0xD24BFD9A</td><td>No</td></tr>
<tr><td>Vehicle Entrance (M113 Driver Hatch)</td><td>0x59E11458</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (M2A3 Gunner)</td><td>0x0D310FF4</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (M2A3 Rear Hatch)</td><td>0xC9CF6F4B</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (MD500 Driver)</td><td>0x45A81402</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (MH53J Driver)</td><td>0x5B32A391</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (MH53J Rear Doors)</td><td>0xF55ABB04</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Mi26) (seat_rear_right)</td><td>0x21905F76</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Omen Entrance Rear)</td><td>0xC9266137</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Patrol Boat) (Driver)</td><td>0x1D7B69B5</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Patrol Boat) (Gunner)</td><td>0x5195583C</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Patrol Boat) (Passenger)</td><td>0xD1549593</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Piranha Gunner)</td><td>0xCA0E1D72</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Piranha MKII Driver)</td><td>0x56D56C95</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (PLZ45 Rear Hatch)</td><td>0x9419A4C7</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Salton Seahorse Front Left)</td><td>0x3BDF5031</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Salton Seahorse Front Left) Long</td><td>0xB7524A65</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Salton Seahorse Front Right)</td><td>0xB9C424B8</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Salton Seahorse Front Right) Long</td><td>0x02282B6E</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Scorpion90 Driver)</td><td>0x74D04970</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Tank Hatch Driver)</td><td>0xDFF538EE</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Tank Hatch Gunner)</td><td>0xC824D93B</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (Turbosquid Driver)</td><td>0x64883B22</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Turbosquid Gunner)</td><td>0x61B2C88F</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Turbosquid Passenger)</td><td>0xE6A83572</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Type 14130 Gunner Front)</td><td>0x5F2D17AB</td><td>No</td></tr>
<tr><td>Vehicle Entrance (Type 14310 Driver)</td><td>0xF35695E1</td><td>No</td></tr>
<tr><td>Vehicle Entrance (UH1 Back Left)</td><td>0x553F473E</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (UH1 Back Right)</td><td>0xF0C093A9</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (UH1 Driver)</td><td>0xC826006A</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (UH1 Middle Left)</td><td>0x2F06893C</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (UH1 Middle Right)</td><td>0x3C16776F</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (UH1 Rear Left)</td><td>0x9B0B2435</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (UH1 Rear Right)</td><td>0xCEF29274</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (WZ551 Driver)</td><td>0xC61B3E1C</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (WZ551 Gunner)</td><td>0x8A95B25D</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (WZ551 Passenger)</td><td>0x1CC7AB30</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance (ZBD2000 Driver)</td><td>0x9C406008</td><td>No</td></tr>
<tr><td>Vehicle Entrance (ZBD2000 Gunner)</td><td>0x3C2CC799</td><td>No</td></tr>
<tr><td>Vehicle Entrance (ZBD2000 Passenger)</td><td>0xC09352FC</td><td>No</td></tr>
<tr><td>Vehicle Entrance M35 Boarding Left</td><td>0xABC61C29</td><td>Yes</td></tr>
<tr><td>Vehicle Entrance M35 Boarding Right</td><td>0xF49CD850</td><td>Yes</td></tr>
<tr><td>Vehicle LockOn Missile</td><td>0x49F1FC77</td><td>No</td></tr>
<tr><td>Vehicle Repair Pad</td><td>0xBDB19EB9</td><td>No</td></tr>
<tr><td>Vehicle Repair Pickup</td><td>0x1CAB20C6</td><td>No</td></tr>
<tr><td>Vehicle Rider Setup (HMMWV) (Soldiers)</td><td>0xDC158E0C</td><td>No</td></tr>
<tr><td>Vehicle Rider Setup (LAVIII) (Soldiers)</td><td>0xF3E353B1</td><td>Yes</td></tr>
<tr><td>Vehicle Rider Setup (SX2150) (Soldiers)</td><td>0x4974993C</td><td>No</td></tr>
<tr><td>Vehicle Ruins</td><td>0xAA5A7CD2</td><td>No</td></tr>
<tr><td>Vehicle Seat</td><td>0xB6A14F9E</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver)</td><td>0x4B53001D</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera LargeA)</td><td>0x134CB5CF</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera LargeB)</td><td>0x382405AA</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera LargeC)</td><td>0xC4A3ACF1</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera Medium)</td><td>0x28BEE44E</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera Small)</td><td>0x74CA85BE</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right)</td><td>0xCE7B0729</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera LargeA)</td><td>0x03E38293</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera LargeB)</td><td>0xE90A1F8E</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera LargeC)</td><td>0x064F89B5</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera Medium)</td><td>0x1F337852</td><td>No</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera Small)</td><td>0xD7C54BAA</td><td>No</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_driver)</td><td>0x3E3B9634</td><td>No</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_driver) (Camera Medium)</td><td>0x3BE093CB</td><td>No</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_front_right)</td><td>0x1769414E</td><td>No</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_front_right) (Camera Medium)</td><td>0x426A8A05</td><td>No</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_gunner_rearcenter)</td><td>0x13ADE31B</td><td>No</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_gunner_rearcenter) (Camera Medium)</td><td>0x617799CC</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 seat Car w/Gunner) (seat_gunner)</td><td>0x1F789BEF</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_left)</td><td>0xB90AAC3C</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_left) (GR)</td><td>0xB778149C</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_left) (OC)</td><td>0xC76527DB</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_right)</td><td>0x8099906F</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_right) (GR)</td><td>0x619A4BFD</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_right) (OC)</td><td>0xDEF9E57E</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_driver)</td><td>0xDDCB911D</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_driver) (GR)</td><td>0xCA5B7F8F</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_driver) (OC)</td><td>0x1385A3D0</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_front_right)</td><td>0x67887A29</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_front_right) (GR)</td><td>0x28F5ACDB</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_front_right) (OC)</td><td>0x354003FC</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_rear_left)</td><td>0x06FBE959</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_rear_right)</td><td>0x784C2E20</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_driver) (Camera LargeA)</td><td>0xD29D48B5</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_driver) (Camera LargeB)</td><td>0xC313000C</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_front_right) (Camera LargeA)</td><td>0x55975DF5</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_front_right) (Camera LargeB)</td><td>0x460D154C</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_rear_left) (Camera LargeA)</td><td>0xABBC57E1</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_rear_right) (Camera LargeA)</td><td>0x309750F0</td><td>No</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_rear_right) (Camera LargeB)</td><td>0x1FFA57C9</td><td>No</td></tr>
<tr><td>Vehicle Seat (AH1Z) (Driver)</td><td>0xECFE5E30</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (AH1Z) (Driver) (Gunner)</td><td>0xBDB52E02</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (AH1Z) (Driver) (Pilot)</td><td>0x439B9663</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (AH1Z) (Gunner)</td><td>0x71727191</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_front_left)</td><td>0x36BA6EF0</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_rear_left)</td><td>0x178C3E7F</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_rear_left) (Extraction)</td><td>0xE8D77659</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_rear_right)</td><td>0xFF7FB3BE</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_rear_right) (Extraction)</td><td>0xF54C005E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3) (Attack) (seat_driver)</td><td>0x30ED76D1</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3) (Attack) (seat_rear_left)</td><td>0x007D931D</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3) (seat_front_right)</td><td>0xC2D02F20</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3) (SuperiorityElite) (seat_driver)</td><td>0x94B00D81</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Alouette3) (Transport) (seat_driver)</td><td>0x48654DF2</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (AMX30 AA) (seat_driver)</td><td>0xF3170687</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (APC 4 Rear Seats) (ML)</td><td>0x1664E2C3</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (APC 4 Rear Seats) (MR)</td><td>0xBBD141A9</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (BL)</td><td>0xE878771A</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (BR)</td><td>0xD3B29764</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (ML)</td><td>0x3BE891A9</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (MR)</td><td>0x967C32C3</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (RL)</td><td>0x5F60F40A</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (RR)</td><td>0xA7724734</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (ML)</td><td>0xA4AAFFAE</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (MR)</td><td>0x94412120</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (RL)</td><td>0x55445E25</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (RR)</td><td>0x687AD787</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (seat_driver)</td><td>0xC5884BDF</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (seat_front_right)</td><td>0x9F5D7DC7</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Avenger) (seat_gunner_rearcenter)</td><td>0x698C1C57</td><td>No</td></tr>
<tr><td>Vehicle Seat (Barco) (Driver)</td><td>0x4A6A0527</td><td>No</td></tr>
<tr><td>Vehicle Seat (Boarding) (FL)</td><td>0xC439F216</td><td>No</td></tr>
<tr><td>Vehicle Seat (Boarding) (FR)</td><td>0x483F5AB8</td><td>No</td></tr>
<tr><td>Vehicle Seat (Boarding) (ML)</td><td>0xF57886F9</td><td>No</td></tr>
<tr><td>Vehicle Seat (Boarding) (MR)</td><td>0xB3362373</td><td>No</td></tr>
<tr><td>Vehicle Seat (Boarding) (MR) AI</td><td>0xF9CA8163</td><td>No</td></tr>
<tr><td>Vehicle Seat (Boarding) (RL)</td><td>0x58C4387A</td><td>No</td></tr>
<tr><td>Vehicle Seat (Boarding) (RM)</td><td>0x65E27A01</td><td>No</td></tr>
<tr><td>Vehicle Seat (Boarding) (RR)</td><td>0xC3FF2244</td><td>No</td></tr>
<tr><td>Vehicle Seat (Boarding) M35 Left</td><td>0x7F1435B1</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Boarding) M35 Right</td><td>0xEFBFB218</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Boat) (Driver)</td><td>0xB6E19000</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Boat) (FL)</td><td>0x30A035F0</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Buggy Hellfire) (seat_driver)</td><td>0x1748A3D7</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Buggy Hellfire) (seat_gunner_rightfront)</td><td>0x657F3EAC</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Buggy PR) (seat_driver)</td><td>0xC57D72D2</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Buggy PR) (seat_gunner_rightfront)</td><td>0xF12BA63F</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (CH Destroyer) (Driver)</td><td>0x002D65CC</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Chopper) (Driver)</td><td>0xF119BF93</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Chopper) (Passenger)</td><td>0x003A6B55</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Cigarette) (Driver)</td><td>0x2496653E</td><td>No</td></tr>
<tr><td>Vehicle Seat (Cigarette) (front_left)</td><td>0x8367AFB5</td><td>No</td></tr>
<tr><td>Vehicle Seat (Coanda Attack) (seat_driver)</td><td>0x4A89AC20</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Coanda Attack) (seat_front_right)</td><td>0x7302BC82</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Coanda Gunship) (seat_driver)</td><td>0xD20C2B1C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Coanda Gunship) (seat_front_right)</td><td>0xD4BBE626</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Coanda Superiority) (seat_driver)</td><td>0x462FBFF1</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Coanda Superiority) (seat_front_right)</td><td>0x88FF4AA5</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Cutter) (Driver)</td><td>0x81A9DBAB</td><td>No</td></tr>
<tr><td>Vehicle Seat (Destroyer) (cannon)</td><td>0x6D71738E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsFL)</td><td>0xF4A5C4B7</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsFM)</td><td>0x58260440</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsFR)</td><td>0x05D61675</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsRL)</td><td>0x43E413F3</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsRR)</td><td>0x86267779</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Destroyer) (sam)</td><td>0xF17A1EF4</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Destroyer) (samFM)</td><td>0x7D81090D</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Destroyer) (samRR)</td><td>0x1E8F6F14</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Dinghy) (Driver)</td><td>0xDBA6E97F</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Dinghy) (seat_front_middle)</td><td>0x99AE114A</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Dinghy) (seat_front_right)</td><td>0x31571E01</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Dinghy) (seat_middle_middle)</td><td>0x0D679B4C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Emplaced GL)</td><td>0x7D98A565</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced GR M101A1)</td><td>0x99FDFDE4</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced MG)</td><td>0x1E90C3AA</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced Quad50) (seat)</td><td>0x1F71439C</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced RR)</td><td>0x4B079BF2</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced TOW)</td><td>0xE445A226</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced VZ M101A1)</td><td>0x3A1F881F</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (FL)</td><td>0xBD9E64C1</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (FR)</td><td>0xA83AB44B</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (RL)</td><td>0x32558E65</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (RR)</td><td>0x458C07C7</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (seat)</td><td>0x92362DDE</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced ZU)</td><td>0x15BB2093</td><td>No</td></tr>
<tr><td>Vehicle Seat (Emplaced ZU23) (seat)</td><td>0x75E5FF88</td><td>No</td></tr>
<tr><td>Vehicle Seat (Fishing Boat) (Driver)</td><td>0x22BA2666</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Garbage Truck) (seat_driver)</td><td>0x10D3CD2E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Garbage Truck) (seat_front_right)</td><td>0x7CCED684</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_driver)</td><td>0x1ADCBF03</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_front_right)</td><td>0xD877A843</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_rear_left)</td><td>0xB7D62217</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_rear_middle)</td><td>0xFD932DB7</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_rear_right)</td><td>0xD4944A16</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (HMMWV) (Gunner)</td><td>0x20D696B2</td><td>No</td></tr>
<tr><td>Vehicle Seat (HMMWV) (seat_driver)</td><td>0x4789A0A5</td><td>No</td></tr>
<tr><td>Vehicle Seat (HMMWV) (seat_front_right)</td><td>0x873C2B61</td><td>No</td></tr>
<tr><td>Vehicle Seat (HMMWV) (seat_rear_left)</td><td>0x480A0A21</td><td>No</td></tr>
<tr><td>Vehicle Seat (HMMWV) (seat_rear_right)</td><td>0x48A5BDE8</td><td>No</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (Driver AI)</td><td>0x6A677421</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (Driver)</td><td>0xEA4D87CF</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (hp_seat_turret_f)</td><td>0x9B252E6B</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (hp_seat_turret_r)</td><td>0x25533B97</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (seat_missle)</td><td>0xA9158F4C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Jetski)</td><td>0x1FAD5417</td><td>No</td></tr>
<tr><td>Vehicle Seat (Jetski) (CIV)</td><td>0x3FEF4BF4</td><td>No</td></tr>
<tr><td>Vehicle Seat (Jetski) (Passenger)</td><td>0x9BC90912</td><td>No</td></tr>
<tr><td>Vehicle Seat (Ka29b) (Driver)</td><td>0xF57F9271</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Ka29b) (Gunner)</td><td>0x2095DDC8</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Ka29b) (ML)</td><td>0x2448A7D2</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Ka29b) (MR)</td><td>0xE166E08C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Ka29b) (RL)</td><td>0x4D6079E1</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Ka29b) (RR)</td><td>0xB939346B</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII 25) (Driver)</td><td>0x987066D9</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII 25) (Gunner)</td><td>0xA1C2CDC0</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII 50Cal) (Driver)</td><td>0x90E88163</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII 50Cal) (Gunner)</td><td>0x528FC956</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII AD) (Driver)</td><td>0x9D5C52A5</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII AD) (Gunner)</td><td>0x418B280C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII AT) (Driver)</td><td>0x1B00CF15</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII AT) (Gunner)</td><td>0xFA5FF91C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII MEWSS) (Driver)</td><td>0x61B393E1</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII MEWSS) (Passenger)</td><td>0x8F75135F</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII MGS) (Driver)</td><td>0xBB9DB579</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII MGS) (Gunner)</td><td>0x6A019EE0</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger BL)</td><td>0xDC40374E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger BR)</td><td>0x4BD58F40</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger FL)</td><td>0x23EA9762</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger FR)</td><td>0xFDDF9E3C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger ML)</td><td>0x42582D55</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger MR)</td><td>0x32651017</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger RL)</td><td>0x0CD586FE</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger RR)</td><td>0x1F953F10</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (LCUR) (Driver)</td><td>0xEEB97B68</td><td>No</td></tr>
<tr><td>Vehicle Seat (LCUR) (Front)</td><td>0xCDABB81B</td><td>No</td></tr>
<tr><td>Vehicle Seat (LCUR) (Rear)</td><td>0xD9C6456C</td><td>No</td></tr>
<tr><td>Vehicle Seat (M113 50Cal) (Driver)</td><td>0xAB30D575</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M113 AA) (Driver)</td><td>0x58A10B26</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M113 AA) (Gunner)</td><td>0x8589CA63</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M113) (Driver)</td><td>0xF94F2200</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M113) (Gunner)</td><td>0x449FD1C1</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M2A3) (Driver)</td><td>0x2893392B</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M2A3) (Gunner)</td><td>0x0183D30E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M2A3) (Passenger ML)</td><td>0x8DC46964</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M2A3) (Passenger MR)</td><td>0xA28A491A</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M2A3) (Passenger RL)</td><td>0x197C1A8F</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M2A3) (Passenger RR)</td><td>0x54B16CFD</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M35 AA) (seat_driver)</td><td>0x9F53C839</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M35 AA) (seat_front_right)</td><td>0xF706779D</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M35 AA) (seat_rear_middle)</td><td>0x07B485B1</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M35 Cargo) (seat_driver)</td><td>0x412C70A1</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M35 Cargo) (seat_front_right)</td><td>0xBC1FC3B5</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (M35) (seat_front_right)</td><td>0xD990B985</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Main Gun Only) (seat_driver)</td><td>0x214E1119</td><td>No</td></tr>
<tr><td>Vehicle Seat (MarkV) (Driver)</td><td>0xFF4D0DA9</td><td>No</td></tr>
<tr><td>Vehicle Seat (Mattias Chopper) (Driver)</td><td>0x14A645D8</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Mattias Chopper) (Passenger)</td><td>0xF27E45CC</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500 Gunship) (Driver) (Manned)</td><td>0xDF4BDEF4</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500 Gunship) (Gunner) (Manned)</td><td>0xC8F6FAC7</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500 Gunship) (seat_front_right)</td><td>0x5A2C4CBC</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500) (Driver) (Manned)</td><td>0xEA2730AC</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_driver)</td><td>0x6D139EEE</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_front_right)</td><td>0xC1645444</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_rear_left)</td><td>0xA26D7638</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_rear_left) (Stowable)</td><td>0x5EAD8CC8</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_rear_right)</td><td>0x5543C9C3</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_rear_right) (stowable)</td><td>0x47C1B025</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MH53J) (Gunner ML)</td><td>0x2A6738C3</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MH53J) (Gunner MR)</td><td>0xCFD397A9</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MH53J) (Gunner RM)</td><td>0x09406D97</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MH53J) (Passenger L)</td><td>0x79639EA7</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MH53J) (Passenger R)</td><td>0x676A59C5</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MH53J) (Passenger) (base)</td><td>0xCA9FA295</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MH53J) (seat_driver)</td><td>0x6A8E9A7F</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MH53J) (seat_front_right)</td><td>0x19BB3A67</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Mi26) (Driver)</td><td>0xD5B19DDC</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Mi26) (seat_front_right)</td><td>0x9C4D6D46</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Mi35 Solano) (seat_driver)</td><td>0xED34AE16</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Mi35 Solano) (seat_solano_back)</td><td>0xCF1D1942</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Mi35 Solano) (seat_solano_front)</td><td>0x55F8595E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Mi35) (Driver)</td><td>0xF1AACA6C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Mi35) (seat_rearleft)</td><td>0xBE3022CD</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Mi35) (seat_rearright)</td><td>0xD33D7B6C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Motorcycle)</td><td>0x7CD4FB1A</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Motorcycle) (Passenger)</td><td>0x6BEB413F</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Motorcycle)(AL)</td><td>0xE69A320E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Motorcycle)(GR)</td><td>0x886B6716</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (MTV) (seat_driver)</td><td>0xC71EA19B</td><td>No</td></tr>
<tr><td>Vehicle Seat (MTV) (seat_gunner)</td><td>0x1D81309E</td><td>No</td></tr>
<tr><td>Vehicle Seat (Offroad Motorcycle) (Driver)</td><td>0xE8D4945E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Offroad Motorcycle) (Passenger)</td><td>0xD8AAD71E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Omen) (Driver)</td><td>0x18915DB3</td><td>No</td></tr>
<tr><td>Vehicle Seat (Omen) (front_left)</td><td>0x590899C8</td><td>No</td></tr>
<tr><td>Vehicle Seat (Omen) (gunner_front)</td><td>0x273A48C2</td><td>No</td></tr>
<tr><td>Vehicle Seat (Omen) (gunner_rear)</td><td>0x39AA5A63</td><td>No</td></tr>
<tr><td>Vehicle Seat (Panhard Assault) (Driver)</td><td>0x05FB8185</td><td>No</td></tr>
<tr><td>Vehicle Seat (Panhard Assault) (seat_front_right)</td><td>0x4D50A977</td><td>No</td></tr>
<tr><td>Vehicle Seat (Patrol Boat PMC) (Driver)</td><td>0xA44241C2</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Patrol Boat PMC) (gunner)</td><td>0xA02F9AAF</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (Driver)</td><td>0x24CA200E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (seat_gunner_front)</td><td>0x5D009117</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (seat_gunner_rear)</td><td>0x7E9AC3F8</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (seat_passenger_front)</td><td>0x8B5360A6</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (seat_passenger_rear)</td><td>0xE4110427</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (PGZ95 Command) (Driver)</td><td>0x129A8750</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (PGZ95) (Driver)</td><td>0x5086BE7B</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Piranha) (gunner)</td><td>0x94700BBE</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Pirhana) (Driver)</td><td>0xDB2C558D</td><td>No</td></tr>
<tr><td>Vehicle Seat (Pirhana) (FL)</td><td>0x75AB3A99</td><td>No</td></tr>
<tr><td>Vehicle Seat (PLZ45) (Driver)</td><td>0x5CB0BA91</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (PMC Copter) (Driver)</td><td>0xA16C6B11</td><td>No</td></tr>
<tr><td>Vehicle Seat (PMC Mi26) (Driver)</td><td>0x6DFB1320</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (PMC UH1) (Attack) (seat_rear_left)</td><td>0x47FC3D75</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (PMC UH1) (Attack) (seat_rear_right)</td><td>0xDB23ACB4</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Salton Seahorse) (Driver)</td><td>0x17A37E07</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Scooter) (Driver)</td><td>0xC0DAF4A7</td><td>No</td></tr>
<tr><td>Vehicle Seat (Scooter) (Passenger)</td><td>0xB513F829</td><td>No</td></tr>
<tr><td>Vehicle Seat (Sidecar Motorcycle) (Driver)</td><td>0xB511913E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Sidecar Motorcycle) (Gunner)</td><td>0xA8D2CD6B</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Sidecar Motorcycle) (Passenger)</td><td>0x5368117E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Small Fishing Boat) (Driver)</td><td>0x37EADD61</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Small Fishing Boat) (seat_front_middle)</td><td>0xD4941458</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Small Fishing Boat) (seat_front_right)</td><td>0xFBA3E88B</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Small Fishing Boat) (seat_middle_middle)</td><td>0xA5FE7FE6</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Sportbike) (Driver)</td><td>0xB70951A7</td><td>No</td></tr>
<tr><td>Vehicle Seat (Sportbike) (Passenger)</td><td>0xCDB03729</td><td>No</td></tr>
<tr><td>Vehicle Seat (Swamp Boat) (Driver)</td><td>0x03F7DF54</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Swamp Boat) (Front)</td><td>0xE8141EC7</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (SX2150 MLRS) (seat_driver)</td><td>0xCCB4A13D</td><td>No</td></tr>
<tr><td>Vehicle Seat (SX2150 MLRS) (seat_front_right)</td><td>0xA4359D49</td><td>No</td></tr>
<tr><td>Vehicle Seat (T300) (seat_gunner_rearcenter)</td><td>0xACC9774E</td><td>No</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Driver)</td><td>0x408C6051</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Driver) (CH)</td><td>0x27211509</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Driver) (OC)</td><td>0x2CBFAD04</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Gunner)</td><td>0xBC092228</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Gunner) (AL)</td><td>0xBDE27A50</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Gunner) (CH)</td><td>0x1AB5B3FE</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (TankBike) (AL)</td><td>0x170947AE</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (Driver)</td><td>0x47E90920</td><td>No</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (Driver) (CIV)</td><td>0x8448045B</td><td>No</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (Driver) (GR)</td><td>0x1250B030</td><td>No</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (Driver) (OC)</td><td>0xF6063FDF</td><td>No</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (seat_front_left)</td><td>0x6C0EAFAB</td><td>No</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (seat_front_right)</td><td>0x3FD999D2</td><td>No</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (seat_gunner)</td><td>0x7B04A1B1</td><td>No</td></tr>
<tr><td>Vehicle Seat (Type14310) (Driver)</td><td>0xCAB22D13</td><td>No</td></tr>
<tr><td>Vehicle Seat (Type14310) (seat_gunner_FM)</td><td>0xBFE5906A</td><td>No</td></tr>
<tr><td>Vehicle Seat (UH1 PMC) (seat_driver)</td><td>0xF0F25EDA</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1 PMC) (Transport) (Driver)</td><td>0xCEEC2586</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Attack) (seat_driver)</td><td>0xB644E3BD</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Attack) (seat_front_right)</td><td>0xF109C4C9</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Attack) (seat_rear_left)</td><td>0x1E4712F9</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Attack) (seat_rear_right)</td><td>0x84DB84C0</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Elite) (seat_driver)</td><td>0xB5EB4A8C</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Elite) (seat_front_right)</td><td>0xAD74DC36</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Gunship) (Driver)</td><td>0xBFEFDE85</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Gunship) (Driver) (GR pilot)</td><td>0xF21A9A49</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Superiority) (seat_driver)</td><td>0x06A7D30E</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (Driver)</td><td>0x28A02742</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_back_left)</td><td>0xA1538617</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_back_right)</td><td>0x64F8B616</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_front_right)</td><td>0xBFBD3CFC</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_middle_left)</td><td>0xFD696D59</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_middle_left) (Non-Stowable)</td><td>0x26D2E819</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_middle_right)</td><td>0x66B2FA20</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_middle_right) (Non-Stowable)</td><td>0x84E8B4C2</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_rear_left)</td><td>0x432B0380</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_rear_left) (Non-Stowable)</td><td>0xCC342DA2</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_rear_right)</td><td>0x0D8EE18B</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_rear_right) (Non-Stowable)</td><td>0xD4E3E583</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (Veyron Assault) (seat_driver)</td><td>0xE6DF4C82</td><td>No</td></tr>
<tr><td>Vehicle Seat (Veyron Assault) (seat_front_right)</td><td>0x4DF7DF30</td><td>No</td></tr>
<tr><td>Vehicle Seat (WZ10) (Driver)</td><td>0x4BEEFBB2</td><td>No</td></tr>
<tr><td>Vehicle Seat (WZ10) (Driver) (Gunner)</td><td>0x64EA84C0</td><td>No</td></tr>
<tr><td>Vehicle Seat (WZ10) (Driver) (Pilot)</td><td>0x60BCE9C1</td><td>No</td></tr>
<tr><td>Vehicle Seat (WZ10) (Gunner)</td><td>0x3F13DD3F</td><td>No</td></tr>
<tr><td>Vehicle Seat (WZ551) (Driver)</td><td>0xC0DA4364</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (WZ551) (Driver) (Amphibious)</td><td>0x2435A3EC</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (WZ551) (Gunner)</td><td>0xA4249BD5</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (WZ551) (Passenger)</td><td>0xDA43E5E8</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (ZBD2000) (Driver)</td><td>0xAE03AE54</td><td>No</td></tr>
<tr><td>Vehicle Seat (ZBD2000) (Driver) (Amphibious)</td><td>0x9B4EA59C</td><td>No</td></tr>
<tr><td>Vehicle Seat (ZBD2000) (Gunner)</td><td>0x1447EFE5</td><td>No</td></tr>
<tr><td>Vehicle Seat (ZBD2000) (Passenger)</td><td>0xAC69DE18</td><td>No</td></tr>
<tr><td>Vehicle Seat (ZTZ63a) (Driver)</td><td>0xBC9F3F14</td><td>Yes</td></tr>
<tr><td>Vehicle Seat (ZTZ63A) (Driver) (Amphibious)</td><td>0xFA0CDCDC</td><td>Yes</td></tr>
<tr><td>Vehicle SS Missile</td><td>0x91A6456F</td><td>No</td></tr>
<tr><td>vehicleHealthTemplate</td><td>0x5474E03F</td><td>No</td></tr>
<tr><td>VehList_AllCon002_AN</td><td>0x9321474A</td><td>No</td></tr>
<tr><td>VehList_AllCon002_Traffic</td><td>0xFB5D703A</td><td>No</td></tr>
<tr><td>VehList_AllCon003_Allies</td><td>0xDEB07C96</td><td>No</td></tr>
<tr><td>VehList_AllCon003_Chinese</td><td>0x865E9911</td><td>No</td></tr>
<tr><td>VehList_ALLHQ</td><td>0x976B90A3</td><td>No</td></tr>
<tr><td>VehList_ALLHQ_AA</td><td>0x1F5AD598</td><td>No</td></tr>
<tr><td>VehList_ALLHQ_HMMWV</td><td>0x44CF107B</td><td>No</td></tr>
<tr><td>VehList_AllJob001</td><td>0x588481FC</td><td>No</td></tr>
<tr><td>VehList_Amazon_Act1</td><td>0x2DDBE815</td><td>No</td></tr>
<tr><td>VehList_Amazon_Act2</td><td>0x8BD42D4A</td><td>No</td></tr>
<tr><td>VehList_Amazon_AllJob002_i_Act1</td><td>0x30A59D56</td><td>No</td></tr>
<tr><td>VehList_Angel_Falls_Act1</td><td>0x4F2BC6FB</td><td>No</td></tr>
<tr><td>VehList_Blank</td><td>0x263CFCE5</td><td>No</td></tr>
<tr><td>VehList_Car_Big_Act1</td><td>0x61FA32CC</td><td>No</td></tr>
<tr><td>VehList_Car_City_Act1</td><td>0xC1152F0D</td><td>No</td></tr>
<tr><td>VehList_Car_City_Act1ContestedAL</td><td>0x365E148B</td><td>No</td></tr>
<tr><td>VehList_Car_City_Act2ALL</td><td>0xC53AD1D7</td><td>No</td></tr>
<tr><td>VehList_Car_City_Act2CHI</td><td>0xC0F65718</td><td>No</td></tr>
<tr><td>VehList_Car_City_Act3ALL</td><td>0x98A524B0</td><td>No</td></tr>
<tr><td>VehList_Car_City_Act3CHI</td><td>0x036189C7</td><td>No</td></tr>
<tr><td>VehList_Car_Dock_Act1</td><td>0x508F6095</td><td>No</td></tr>
<tr><td>VehList_Car_Estate_Act1</td><td>0x2DFAD29A</td><td>No</td></tr>
<tr><td>VehList_Car_Shanty_Act1</td><td>0xE1BC5559</td><td>No</td></tr>
<tr><td>VehList_CHIHQ</td><td>0xF1C5A9BC</td><td>No</td></tr>
<tr><td>VehList_CHIHQ_AA</td><td>0x39D7B4CD</td><td>No</td></tr>
<tr><td>VehList_Cumana_Act1ALL</td><td>0x7248D833</td><td>No</td></tr>
<tr><td>VehList_Cumana_Act1CHI</td><td>0xD27C4934</td><td>No</td></tr>
<tr><td>VehList_Cumana_act2CHI</td><td>0xF6F0C349</td><td>No</td></tr>
<tr><td>VehList_Cumana_Fort_AllJob002B</td><td>0x9D0EE581</td><td>No</td></tr>
<tr><td>VehList_Guanare_Act1</td><td>0xCAF91A4C</td><td>No</td></tr>
<tr><td>VehList_Guanare_Big_Act1</td><td>0x0138AD75</td><td>No</td></tr>
<tr><td>VehList_Guanare_MecCon</td><td>0xF9A68CC6</td><td>No</td></tr>
<tr><td>VehList_GurHQ_AA</td><td>0xA3CA0241</td><td>No</td></tr>
<tr><td>VehList_GurHQ_Traffic</td><td>0x13AC24F2</td><td>No</td></tr>
<tr><td>VehList_GurHQ_Vehicles</td><td>0x5785F7C8</td><td>Yes</td></tr>
<tr><td>VehList_JungleMtn_GurCon052</td><td>0x9AE66CBB</td><td>No</td></tr>
<tr><td>VehList_JungleMtnA_Act1</td><td>0x97D9B7F0</td><td>No</td></tr>
<tr><td>VehList_JungleMtnB_Act1</td><td>0x173E2151</td><td>No</td></tr>
<tr><td>VehList_JungleMtnC_Act1</td><td>0xB0DFA0E2</td><td>No</td></tr>
<tr><td>VehList_Mar_Altagracia_Act1</td><td>0xAC551BFD</td><td>No</td></tr>
<tr><td>VehList_Mar_Altagracia_Act2</td><td>0x2A4D9392</td><td>No</td></tr>
<tr><td>VehList_Mar_Big_Act1</td><td>0x0C46D0FE</td><td>No</td></tr>
<tr><td>VehList_Mar_City_OilCon020Cartel</td><td>0x8B9CECFD</td><td>No</td></tr>
<tr><td>VehList_Mar_City_OilCon021</td><td>0x4B792311</td><td>No</td></tr>
<tr><td>VehList_Mar_Industrial_Act1</td><td>0x1B9159B3</td><td>No</td></tr>
<tr><td>VehList_Mar_Industrial_Act2</td><td>0x4193D41C</td><td>No</td></tr>
<tr><td>VehList_Mar_Industrial_Act3</td><td>0x3B960941</td><td>No</td></tr>
<tr><td>VehList_Mar_Outskirt_Act1</td><td>0x713CEEC7</td><td>No</td></tr>
<tr><td>VehList_Mar_Outskirt_Act1VZ</td><td>0x61676513</td><td>No</td></tr>
<tr><td>VehList_Mar_Outskirt_OilCon020Cartel</td><td>0xA455C57D</td><td>No</td></tr>
<tr><td>VehList_Mar_Village_Act1</td><td>0x43DC42A4</td><td>No</td></tr>
<tr><td>VehList_Mar_Village_Act1_PirCon2</td><td>0xC5D8015E</td><td>No</td></tr>
<tr><td>VehList_MarCity_Act1</td><td>0xF1274DA4</td><td>No</td></tr>
<tr><td>VehList_MarCity_Act1Contested</td><td>0x26D3E1F3</td><td>No</td></tr>
<tr><td>VehList_MarCity_Act1ContestedVZ</td><td>0x014B5D57</td><td>No</td></tr>
<tr><td>VehList_MarCity_Act1OC_R</td><td>0x2A3920CD</td><td>No</td></tr>
<tr><td>VehList_MarCity_Act1UP</td><td>0xCB42F663</td><td>No</td></tr>
<tr><td>VehList_MarCity_Act1UP_PirCon02</td><td>0x3594D7FF</td><td>No</td></tr>
<tr><td>VehList_MarCity_Act2</td><td>0x0B2537FB</td><td>No</td></tr>
<tr><td>VehList_MarCity_Act2ContestedCH</td><td>0x614F0283</td><td>No</td></tr>
<tr><td>VehList_MarCity_Act3</td><td>0xE922C3DE</td><td>No</td></tr>
<tr><td>VehList_Margarita_Act1</td><td>0x8F68C771</td><td>No</td></tr>
<tr><td>VehList_Mer_Big_Act1</td><td>0xE3E52CAA</td><td>No</td></tr>
<tr><td>VehList_Mer_City_Act1</td><td>0xBEF61B6B</td><td>No</td></tr>
<tr><td>VehList_Mer_City_Act1ContestedGR</td><td>0x50175F85</td><td>No</td></tr>
<tr><td>VehList_Mer_City_Act2</td><td>0xE4F895D4</td><td>No</td></tr>
<tr><td>VehList_Mer_Outskirt_Act1</td><td>0x3AD48073</td><td>No</td></tr>
<tr><td>VehList_Merida_GurOutskirts</td><td>0xB9FB2202</td><td>No</td></tr>
<tr><td>VehList_Merida_VZOutskirts</td><td>0xBFF35910</td><td>No</td></tr>
<tr><td>VehList_OilDepot_Act1</td><td>0x1FC7641F</td><td>No</td></tr>
<tr><td>VehList_OilDepot_EXT</td><td>0xCF6DC9F3</td><td>No</td></tr>
<tr><td>VehList_OilDepot_GunTrucks</td><td>0x801BCAD0</td><td>Yes</td></tr>
<tr><td>VehList_OilDepot_Stingray</td><td>0x5F265AC3</td><td>Yes</td></tr>
<tr><td>VehList_Pir_T300Driver</td><td>0x0BC6FDB8</td><td>No</td></tr>
<tr><td>VehList_PirCon003</td><td>0xE9FBB0B1</td><td>No</td></tr>
<tr><td>VehList_PirHQ</td><td>0x0BD071F7</td><td>No</td></tr>
<tr><td>VehList_VZCon001_Dirtbike</td><td>0xA3901E57</td><td>No</td></tr>
<tr><td>VehList_VZCon001_M151</td><td>0x963817EF</td><td>Yes</td></tr>
<tr><td>Verification Camera</td><td>0xF182CA19</td><td>No</td></tr>
<tr><td>verify flash</td><td>0xB9F5A2CC</td><td>No</td></tr>
<tr><td>Veyron</td><td>0xDE0208C0</td><td>No</td></tr>
<tr><td>Veyron (as a building)</td><td>0x5E327E60</td><td>No</td></tr>
<tr><td>Veyron (Assault)</td><td>0x046E1AA2</td><td>No</td></tr>
<tr><td>Veyron (Assault) (Driver)</td><td>0x115B8749</td><td>No</td></tr>
<tr><td>Veyron (base)</td><td>0x33588F18</td><td>No</td></tr>
<tr><td>Veyron (Cannon)</td><td>0xCB562B84</td><td>No</td></tr>
<tr><td>Veyron (Driver)</td><td>0x1F484C5F</td><td>No</td></tr>
<tr><td>Veyron (Driver) (Civ Rich female)</td><td>0x903B0452</td><td>No</td></tr>
<tr><td>Veyron (Driver) (Civ Rich male)</td><td>0x66CFAD77</td><td>No</td></tr>
<tr><td>Veyron_Driver</td><td>0xA225EE3D</td><td>No</td></tr>
<tr><td>VeyronAssault_Driver</td><td>0xC9AC1A8E</td><td>No</td></tr>
<tr><td>VZ</td><td>0xB4420059</td><td>No</td></tr>
<tr><td>VZ Allied Defector</td><td>0x6A0568F2</td><td>No</td></tr>
<tr><td>VZ Antenna</td><td>0x963EF124</td><td>No</td></tr>
<tr><td>VZ Captain</td><td>0x06F7E45D</td><td>No</td></tr>
<tr><td>VZ Chinese Defector</td><td>0x8253CF38</td><td>No</td></tr>
<tr><td>VZ Deathsquad</td><td>0xAF46A983</td><td>No</td></tr>
<tr><td>VZ Deathsquad (Mook)</td><td>0xC964419E</td><td>No</td></tr>
<tr><td>VZ Deathsquad (Mook) w/ LMG</td><td>0x8D27323C</td><td>No</td></tr>
<tr><td>VZ Deathsquad (Mook) w/ RPG</td><td>0xA75BF6B5</td><td>No</td></tr>
<tr><td>VZ Deathsquad B</td><td>0x7082C649</td><td>No</td></tr>
<tr><td>VZ Deathsquad B HVT</td><td>0xDBCDEE03</td><td>No</td></tr>
<tr><td>VZ Deathsquad C</td><td>0x56805EC4</td><td>No</td></tr>
<tr><td>VZ Defender (AA)</td><td>0x68071939</td><td>No</td></tr>
<tr><td>VZ Defender (AT)</td><td>0x51A916A6</td><td>No</td></tr>
<tr><td>VZ Defender (AT) (Window Spawner)</td><td>0x50E1E3EB</td><td>No</td></tr>
<tr><td>VZ Defender (MG)</td><td>0x0CF90747</td><td>No</td></tr>
<tr><td>VZ Defender (Rifle)</td><td>0x8F5E7B99</td><td>No</td></tr>
<tr><td>VZ Defender (Sniper)</td><td>0x5F9AF5A8</td><td>No</td></tr>
<tr><td>VZ Elite</td><td>0xE0C2BA3C</td><td>No</td></tr>
<tr><td>VZ Guerilla Defector</td><td>0x0075BAE0</td><td>No</td></tr>
<tr><td>VZ Heavy (AA Missile)</td><td>0x4F07A507</td><td>No</td></tr>
<tr><td>VZ Heavy (Heavy MG)</td><td>0x405F7B3C</td><td>No</td></tr>
<tr><td>VZ Heavy (Light MG)</td><td>0xBA7B1711</td><td>No</td></tr>
<tr><td>VZ Heavy (RPG + Rifle)</td><td>0xBAC092CD</td><td>No</td></tr>
<tr><td>VZ Heavy (RPG)</td><td>0x82CF86E6</td><td>No</td></tr>
<tr><td>VZ HeliPatrol</td><td>0x8E7B1B61</td><td>Yes</td></tr>
<tr><td>VZ HVT01</td><td>0x3CF53B8E</td><td>No</td></tr>
<tr><td>VZ HVT02</td><td>0x9EFC9199</td><td>No</td></tr>
<tr><td>VZ HVT03</td><td>0x44F9C554</td><td>No</td></tr>
<tr><td>VZ HVT04</td><td>0xA7011B5F</td><td>No</td></tr>
<tr><td>VZ Jet Pilot</td><td>0xFDAD5ECA</td><td>No</td></tr>
<tr><td>VZ MinerUnionBoss</td><td>0x6C9E6F52</td><td>No</td></tr>
<tr><td>VZ Officer</td><td>0x238E6A57</td><td>No</td></tr>
<tr><td>VZ Oil Company Defector</td><td>0x4DE8C1C4</td><td>No</td></tr>
<tr><td>VZ Riot Soldier</td><td>0x63B075BF</td><td>No</td></tr>
<tr><td>VZ Sniper</td><td>0xAC1CBADE</td><td>No</td></tr>
<tr><td>VZ Soldier</td><td>0x5FFB1CB3</td><td>No</td></tr>
<tr><td>VZ Soldier (Crash Repro)</td><td>0xE7813B45</td><td>No</td></tr>
<tr><td>VZ Soldier (Mook)</td><td>0xA22B422E</td><td>No</td></tr>
<tr><td>VZ Soldier (Seatbelted)</td><td>0xFF5C6CC5</td><td>No</td></tr>
<tr><td>VZ Soldier (stowed)</td><td>0xE913C87C</td><td>No</td></tr>
<tr><td>VZ Tank Commander</td><td>0xD94E10C5</td><td>Yes</td></tr>
<tr><td>VZBaseTemp</td><td>0xCD89AD48</td><td>No</td></tr>
<tr><td>VZBaseTrafficZone</td><td>0xD21D8AAF</td><td>No</td></tr>
<tr><td>VzDbSpawner</td><td>0x3CFFE175</td><td>No</td></tr>
<tr><td>VzDbSpawner (Squad Full AT)</td><td>0xEF3E1340</td><td>No</td></tr>
<tr><td>VzDbSpawner (Squad Half AT)</td><td>0xFC034558</td><td>No</td></tr>
<tr><td>VzDbSpawner (Squad Quarter AT)</td><td>0x291F2235</td><td>No</td></tr>
<tr><td>VzDbSpawner (Squad)</td><td>0x260CAACE</td><td>No</td></tr>
<tr><td>VZGurTankSpawnlist</td><td>0x8609B23A</td><td>Yes</td></tr>
<tr><td>VZHealthBucket</td><td>0x2BE4C7F1</td><td>No</td></tr>
<tr><td>VZHealthList</td><td>0x00F5431B</td><td>No</td></tr>
<tr><td>VZRareHeavy</td><td>0x737DB7D2</td><td>No</td></tr>
<tr><td>VZRockets</td><td>0x02E06A24</td><td>No</td></tr>
<tr><td>VzTestTrafficZone</td><td>0x7F9379B2</td><td>No</td></tr>
<tr><td>VZWindowList</td><td>0xFDE30AFD</td><td>No</td></tr>
<tr><td>W series</td><td>0xAA8FE983</td><td>No</td></tr>
<tr><td>W12 (normal)</td><td>0xB9D23751</td><td>No</td></tr>
<tr><td>W12 (normal) (black)</td><td>0xDEBDCC33</td><td>No</td></tr>
<tr><td>W12 (normal) (blue)</td><td>0x5FBC7946</td><td>No</td></tr>
<tr><td>W12 (normal) (bronze)</td><td>0x4A9BCCFA</td><td>No</td></tr>
<tr><td>W12 (normal) (Driver)</td><td>0x7076E2AC</td><td>No</td></tr>
<tr><td>W12 (normal) (Driver) (Civ Rich female)</td><td>0x6D615051</td><td>No</td></tr>
<tr><td>W12 (normal) (Driver) (Civ Rich male)</td><td>0x9801E1F4</td><td>No</td></tr>
<tr><td>W12 (normal) (green)</td><td>0x0EDF2B73</td><td>No</td></tr>
<tr><td>W12 (normal) (lightblue)</td><td>0x83C91BE8</td><td>No</td></tr>
<tr><td>W12 (normal) (orange)</td><td>0x2C3451F0</td><td>No</td></tr>
<tr><td>W12 (normal) (paleblue)</td><td>0x4239EE46</td><td>No</td></tr>
<tr><td>W12 (normal) (red)</td><td>0x0011FF73</td><td>No</td></tr>
<tr><td>W12 (normal) (white)</td><td>0xF1254381</td><td>No</td></tr>
<tr><td>W12 (sprint)</td><td>0xFBCDEEBA</td><td>No</td></tr>
<tr><td>W12 (sprint) (Driver)</td><td>0xDCA853E1</td><td>No</td></tr>
<tr><td>W12 (sprint) (Driver) (Civ Rich female)</td><td>0x3FAFE7A0</td><td>No</td></tr>
<tr><td>W12 (sprint) (Driver) (Civ Rich male)</td><td>0x1BD3AC51</td><td>No</td></tr>
<tr><td>W12 (Z12)</td><td>0x5DE0BD51</td><td>No</td></tr>
<tr><td>W12 (Z12) (Driver)</td><td>0xBEC014AC</td><td>No</td></tr>
<tr><td>W12 (Z12) (Driver) (Civ Rich female)</td><td>0xEF9F5251</td><td>No</td></tr>
<tr><td>W12 (Z12) (Driver) (Civ Rich male)</td><td>0x69FB93F4</td><td>No</td></tr>
<tr><td>W12 (Z12) Racer</td><td>0x82E9924A</td><td>No</td></tr>
<tr><td>W12_Driver</td><td>0xA1E5243E</td><td>No</td></tr>
<tr><td>W8 (normal)</td><td>0x717E21E6</td><td>No</td></tr>
<tr><td>W8 (normal) (Driver)</td><td>0xB4ED077D</td><td>No</td></tr>
<tr><td>W8 (normal) (Driver) (Civ Rich female)</td><td>0x642D9ECC</td><td>No</td></tr>
<tr><td>W8 (normal) (Driver) (Civ Rich male)</td><td>0x5902A1DD</td><td>No</td></tr>
<tr><td>W8_Driver</td><td>0x941202DD</td><td>No</td></tr>
<tr><td>wallace_testcube01</td><td>0xF703083B</td><td>No</td></tr>
<tr><td>wallace_testrig</td><td>0xC5FFFE39</td><td>No</td></tr>
<tr><td>water_template</td><td>0x14AEF06B</td><td>No</td></tr>
<tr><td>waterpuddle01</td><td>0xB91F2097</td><td>No</td></tr>
<tr><td>waterShore100mTemplate</td><td>0xD29684C1</td><td>No</td></tr>
<tr><td>waterShore150mTemplate 0x8000a6f1</td><td>0xEB4D47F6</td><td>No</td></tr>
<tr><td>waterShore200mTemplate 0x8000a6eb</td><td>0xDE398D90</td><td>No</td></tr>
<tr><td>waterShore25mTemplate 0x8000a6ed</td><td>0xF9861505</td><td>No</td></tr>
<tr><td>waterShore300mTemplate 0x8000a6ef</td><td>0x179D9769</td><td>No</td></tr>
<tr><td>waterShore400mTemplate 0x8000a6ee</td><td>0x91A3F6DD</td><td>No</td></tr>
<tr><td>waterShore50mTemplate 0x8000a6ec</td><td>0x7AFA4926</td><td>No</td></tr>
<tr><td>waterShore75mTemplate 0x8000a6f0</td><td>0x253B5EDB</td><td>No</td></tr>
<tr><td>waterShore_open</td><td>0x16A64C2C</td><td>No</td></tr>
<tr><td>waterShore_small</td><td>0x883609C5</td><td>No</td></tr>
<tr><td>waterShore_tiny</td><td>0x93827ED6</td><td>No</td></tr>
<tr><td>Weapon (Human)</td><td>0xE6466F25</td><td>No</td></tr>
<tr><td>Weapon (TESTS for Art)</td><td>0xEF416863</td><td>No</td></tr>
<tr><td>WeaponMagDebrisTemplate</td><td>0x4E68D76D</td><td>No</td></tr>
<tr><td>Wheel (Rear)</td><td>0xE2460FC9</td><td>No</td></tr>
<tr><td>Wheel Armored Bank Truck (L)</td><td>0x6F630E42</td><td>Yes</td></tr>
<tr><td>Wheel Armored Bank Truck (R)</td><td>0x4958151C</td><td>Yes</td></tr>
<tr><td>Wheel Health</td><td>0x80D436B8</td><td>No</td></tr>
<tr><td>Wheel Health RL</td><td>0x2E0FD24E</td><td>No</td></tr>
<tr><td>Wheel Health RR</td><td>0x8E0A5940</td><td>No</td></tr>
<tr><td>Wheel Health XL</td><td>0xD063D4B8</td><td>No</td></tr>
<tr><td>Wheel Health XR</td><td>0x7040AB56</td><td>No</td></tr>
<tr><td>Wheel L300 (L)</td><td>0xDEFDC8E8</td><td>No</td></tr>
<tr><td>Wheel L300 (R)</td><td>0x7E21F6E6</td><td>No</td></tr>
<tr><td>Wheel L300 (Racing) (L)</td><td>0xA2E7C1D9</td><td>No</td></tr>
<tr><td>Wheel L300 (Racing) (R)</td><td>0xDF676053</td><td>No</td></tr>
<tr><td>Wheel SX2150 (L)</td><td>0x3CB0AB26</td><td>No</td></tr>
<tr><td>Wheel SX2150 (R)</td><td>0x9D8C7D28</td><td>No</td></tr>
<tr><td>Wheel WZ551 (L)</td><td>0xF7B9DCA5</td><td>Yes</td></tr>
<tr><td>Wheel WZ551 (ML)</td><td>0xB0654998</td><td>Yes</td></tr>
<tr><td>Wheel WZ551 (MR)</td><td>0xAC60AA76</td><td>Yes</td></tr>
<tr><td>Wheel WZ551 (R)</td><td>0x0AF05607</td><td>Yes</td></tr>
<tr><td>Wheel WZ551 (RL)</td><td>0x026A840B</td><td>Yes</td></tr>
<tr><td>Wheel WZ551 (RR)</td><td>0x17CE3481</td><td>Yes</td></tr>
<tr><td>WheelFlame</td><td>0xC614F6F7</td><td>No</td></tr>
<tr><td>Will_atmospheres</td><td>0xADC27D93</td><td>No</td></tr>
<tr><td>WindowSeat</td><td>0xFBD5485E</td><td>No</td></tr>
<tr><td>WindowSpawnerTest</td><td>0xEF14D2FB</td><td>No</td></tr>
<tr><td>WindowSpawnerTest2</td><td>0xAE8C7E5B</td><td>No</td></tr>
<tr><td>WindowSpawnerTurret</td><td>0x2A8EFC41</td><td>No</td></tr>
<tr><td>WorldExit</td><td>0xAA9975CB</td><td>No</td></tr>
<tr><td>WS Test</td><td>0x783A7745</td><td>No</td></tr>
<tr><td>WZ10</td><td>0x02661E85</td><td>No</td></tr>
<tr><td>WZ10 (Driver)</td><td>0x26B94B90</td><td>No</td></tr>
<tr><td>WZ10 (Ewan)</td><td>0x73EF463D</td><td>No</td></tr>
<tr><td>WZ10 (Full)</td><td>0x1E58E727</td><td>No</td></tr>
<tr><td>WZ551</td><td>0xCC9CEB99</td><td>Yes</td></tr>
<tr><td>WZ551 (Amphibious) (DoNotUse)</td><td>0xB17A4B69</td><td>Yes</td></tr>
<tr><td>WZ551 (Driver)</td><td>0x29431074</td><td>Yes</td></tr>
<tr><td>WZ551 (Full)</td><td>0x4D84C7B3</td><td>Yes</td></tr>
<tr><td>WZ551_Driver</td><td>0x17FC2D22</td><td>Yes</td></tr>
<tr><td>ZBD2000</td><td>0x58827779</td><td>No</td></tr>
<tr><td>ZBD2000 (Amphibious) (DoNotUse)</td><td>0xD6A07C49</td><td>No</td></tr>
<tr><td>ZBD2000 (Driver)</td><td>0xEC25EFD4</td><td>No</td></tr>
<tr><td>ZBD2000 (DriverGunner)</td><td>0xD745179B</td><td>No</td></tr>
<tr><td>ZBD2000 (Full)</td><td>0x3F57BB93</td><td>No</td></tr>
<tr><td>ZippoFlame</td><td>0x90BF5C72</td><td>No</td></tr>
<tr><td>ZTZ63a</td><td>0xC36271CF</td><td>Yes</td></tr>
<tr><td>ZTZ63a (Amphibious) (DoNotUse)</td><td>0xE6739AD3</td><td>Yes</td></tr>
<tr><td>ZTZ63a (Driver)</td><td>0xEF287EFA</td><td>Yes</td></tr>
<tr><td>ZTZ63a (Full)</td><td>0x8309B139</td><td>Yes</td></tr>
<tr><td>ZTZ98</td><td>0x28CFA508</td><td>Yes</td></tr>
<tr><td>ZTZ98 (Driver)</td><td>0x33DF6767</td><td>Yes</td></tr>
<tr><td>ZTZ98 (Full)</td><td>0xC1F56AAC</td><td>Yes</td></tr>
</tbody>
</table>
</div>
</div>

<style>
.hash-lookup-search {
  width: 100%;
  box-sizing: border-box;
  padding: 0.5em 0.75em;
  font-size: 1em;
  border: 1px solid #c3ccd6;
  border-radius: 6px;
  margin-bottom: 0.5em;
}
.hash-lookup-count {
  font-size: 0.85em;
  color: #4a6fa5;
  margin-bottom: 0.5em;
}
.hash-lookup-scroll {
  max-height: 70vh;
  overflow-y: auto;
  border: 1px solid #c3ccd6;
  border-radius: 6px;
}
table.hash-lookup-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85em;
}
table.hash-lookup-table th, table.hash-lookup-table td {
  padding: 0.3em 0.6em;
  border-bottom: 1px solid #e0e4e9;
  text-align: left;
  white-space: nowrap;
}
table.hash-lookup-table td:nth-child(2) {
  font-family: monospace;
}
table.hash-lookup-table thead th {
  position: sticky;
  top: 0;
  background: #f5f7fa;
  z-index: 1;
}
table.hash-lookup-table tbody tr:nth-child(even) {
  background: #fafbfc;
}
html.wiki-dark .hash-lookup-search {
  background: #1b222c;
  border-color: #33445c;
  color: #dbe4f0;
}
html.wiki-dark .hash-lookup-count {
  color: #a9c3e8;
}
html.wiki-dark .hash-lookup-scroll {
  border-color: #33445c;
}
html.wiki-dark table.hash-lookup-table th,
html.wiki-dark table.hash-lookup-table td {
  border-color: #2a3444;
  color: #dbe4f0;
}
html.wiki-dark table.hash-lookup-table thead th {
  background: #1b222c;
}
html.wiki-dark table.hash-lookup-table tbody tr:nth-child(even) {
  background: #20293a;
}
</style>

<script>
(function() {
  var input = document.getElementById("hashLookupFilter");
  var table = document.getElementById("hashLookupTable");
  var countEl = document.getElementById("hashLookupCount");
  if (!input || !table) return;
  var rows = table.tBodies[0].rows;
  function updateCount(shown) {
    countEl.textContent = shown + " / " + rows.length + " shown";
  }
  updateCount(rows.length);
  input.addEventListener("input", function() {
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    for (var i = 0; i < rows.length; i++) {
      var match = q === "" || rows[i].textContent.toLowerCase().indexOf(q) !== -1;
      rows[i].style.display = match ? "" : "none";
      if (match) shown++;
    }
    updateCount(shown);
  });
})();
</script>
