---
title: Hash Lookup
nav_order: 7
---

# Hash Lookup

## Overview

A 6119-entry name-to-hash table, covering (per the source export) every spawnable template plus a large
number of non-spawnable assets (decals, building-HP threshold markers, internal test assets, etc.) -- this
looks to be Pandemic's own internal asset/string hash table for this game ("pandemic_hash_m2" in the
source column names), not a spawn-only list. Provided as a CSV export; the exact tool/process used to
extract it from the game isn't documented here, only what's been cross-checked against this wiki's own
already-confirmed findings below.

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

**Not yet confirmed, but worth testing:** most `value_hex` entries are `0x8000XXXX`-shaped -- the exact
address range this wiki already confirmed (via `Object.GetParent`, see the World Inspector deep dive) for
an object's own spawn-template reference. If a live `Sys.GuidToString(Object.GetParent(uGuid))` capture from
a WorldProbe detailed dump (down arrow) ever matches one of this table's `value_hex` entries, that would be
a full, live-confirmed, offline name-resolution path for template references -- not just the hashed
localized-name string. This hasn't been tested yet; worth doing on the next WorldProbe session.

## Table

Columns, straight from the CSV: `name` (the literal string, `Pg.Spawn`-able for at least the ones already
cross-referenced above), `hash` (`pandemic_hash_m2_hex` -- the 8-hex-digit key format seen in-game as
`[0xXXXXXXXX]`), `vehicle` (`is_vehicle` flag), `entry index`, `value` (`value_hex` -- see the note above),
and `aux0` (`aux0_hex`, meaning not yet confirmed; `0xFFFFFFFF` appears to be a "not set" sentinel). The
CSV's `pandemic_hash_m2_dec` and `aux1_hex` columns are omitted here -- decimal duplicates the hex hash in a
less useful form for matching against in-game bracketed hashes, and `aux1_hex` was confirmed identical to
`pandemic_hash_m2_hex` in every row of the source export, so it carries no extra information.

<div class="hash-lookup-wrap" markdown="0">
<input type="text" id="hashLookupFilter" class="hash-lookup-search"
       placeholder="Filter by name or hash (e.g. 'destroyer' or '0x02DFA76D')..." autocomplete="off">
<div class="hash-lookup-count" id="hashLookupCount"></div>
<div class="hash-lookup-scroll">
<table class="hash-lookup-table" id="hashLookupTable">
<thead>
<tr><th>Name</th><th>Hash</th><th>Vehicle</th><th>Entry Index</th><th>Value</th><th>Aux0</th></tr>
</thead>
<tbody>
<tr><td>(unnamed)</td><td>0x021F16B2</td><td>No</td><td>101</td><td>0x80004C02</td><td>0xFFFFFFFF</td></tr>
<tr><td>(unnamed)</td><td>0x816F0B0D</td><td>No</td><td>836</td><td>0x80006391</td><td>0x00000666</td></tr>
<tr><td>(unnamed)</td><td>0xA1AD5E94</td><td>No</td><td>1460</td><td>0x80006F9C</td><td>0xFFFFFFFF</td></tr>
<tr><td>(unnamed)</td><td>0xFEC25D11</td><td>No</td><td>1822</td><td>0x800076AD</td><td>0xFFFFFFFF</td></tr>
<tr><td>(unnamed)</td><td>0x699D5606</td><td>No</td><td>2644</td><td>0x80008626</td><td>0x000109D4</td></tr>
<tr><td>(unnamed)</td><td>0x4C74944F</td><td>No</td><td>2803</td><td>0x80008769</td><td>0x000091D2</td></tr>
<tr><td>(unnamed)</td><td>0xBD4DC42B</td><td>No</td><td>2943</td><td>0x800089BF</td><td>0x00004BCC</td></tr>
<tr><td>(unnamed)</td><td>0x784FCF4D</td><td>No</td><td>2969</td><td>0x800089FD</td><td>0x0000857C</td></tr>
<tr><td>(unnamed)</td><td>0xB224DB15</td><td>No</td><td>3305</td><td>0x80008F75</td><td>0x00011DD2</td></tr>
<tr><td>(unnamed)</td><td>0x2AE48660</td><td>No</td><td>4202</td><td>0x80009C2F</td><td>0x0000CAEE</td></tr>
<tr><td>(unnamed)</td><td>0x6420E4F7</td><td>No</td><td>5143</td><td>0x8000A47F</td><td>0x00003A28</td></tr>
<tr><td>(unnamed)</td><td>0x928027C1</td><td>No</td><td>5270</td><td>0x8000A7C1</td><td>0x00005827</td></tr>
<tr><td>(unnamed)</td><td>0xC6B40476</td><td>No</td><td>5387</td><td>0x8000A97B</td><td>0x00007861</td></tr>
<tr><td>(unnamed)</td><td>0x0ECB978A</td><td>No</td><td>5529</td><td>0x8000AB3F</td><td>0xFFFFFFFF</td></tr>
<tr><td>(unnamed)</td><td>0x1266E814</td><td>No</td><td>5698</td><td>0x8000ACCC</td><td>0xFFFFFFFF</td></tr>
<tr><td>(unnamed)</td><td>0xD8353CA9</td><td>No</td><td>5699</td><td>0x8000ACCD</td><td>0x00002C6F</td></tr>
<tr><td>(unnamed)</td><td>0xEDF510A0</td><td>No</td><td>5744</td><td>0x8000AD69</td><td>0x0000252C</td></tr>
<tr><td>(unnamed)</td><td>0xE19A4391</td><td>No</td><td>5755</td><td>0x8000AE05</td><td>0x00001A49</td></tr>
<tr><td>2 Seat Boat (Passenger)</td><td>0x1F3E12D3</td><td>Yes</td><td>717</td><td>0x8000617D</td><td>0x00001237</td></tr>
<tr><td>2 Seat Car (Driver)</td><td>0xF4DD3619</td><td>No</td><td>52</td><td>0x80004647</td><td>0xFFFFFFFF</td></tr>
<tr><td>2 Seat Car (Driver) (Civ)</td><td>0x148B271E</td><td>No</td><td>62</td><td>0x80004741</td><td>0x00011469</td></tr>
<tr><td>2 Seat Car (Driver) (Escort)</td><td>0x847BC256</td><td>No</td><td>4642</td><td>0x80009FC4</td><td>0x000015B4</td></tr>
<tr><td>2 Seat Car (Driver) (Police)</td><td>0x22DF2620</td><td>No</td><td>985</td><td>0x80006874</td><td>0xFFFFFFFF</td></tr>
<tr><td>2 Seat Car (Passenger)</td><td>0x90401807</td><td>No</td><td>53</td><td>0x80004648</td><td>0xFFFFFFFF</td></tr>
<tr><td>2 Seat Car (Passenger) (Escort)</td><td>0x76AED190</td><td>No</td><td>4643</td><td>0x80009FC5</td><td>0x000139FB</td></tr>
<tr><td>2 Seat Copter (Driver)</td><td>0xFDEF813A</td><td>No</td><td>12</td><td>0x80002351</td><td>0x00011829</td></tr>
<tr><td>2 Seat Copter (Driver) (Allied)</td><td>0x93EC73B4</td><td>No</td><td>36</td><td>0x80004386</td><td>0xFFFFFFFF</td></tr>
<tr><td>2 Seat Copter (Driver) (Guerilla)</td><td>0x9083B5FA</td><td>No</td><td>1026</td><td>0x800068AE</td><td>0x00006982</td></tr>
<tr><td>2 Seat Copter (Driver) (OC)</td><td>0x8CF39D8D</td><td>No</td><td>519</td><td>0x800056EA</td><td>0xFFFFFFFF</td></tr>
<tr><td>2 Seat Copter (Driver) (VZ)</td><td>0x1255524F</td><td>No</td><td>513</td><td>0x800056E2</td><td>0x00008981</td></tr>
<tr><td>2 Seat Copter (Gunner)</td><td>0x92D3A017</td><td>No</td><td>1077</td><td>0x80006A0F</td><td>0xFFFFFFFF</td></tr>
<tr><td>3 Seat Car (Driver)</td><td>0x2A00E898</td><td>No</td><td>9</td><td>0x8000234C</td><td>0x00011F1D</td></tr>
<tr><td>3 Seat Car (Driver) (Guerilla)</td><td>0xE3E5DD4C</td><td>No</td><td>59</td><td>0x80004734</td><td>0x0000A685</td></tr>
<tr><td>3 Seat Car (Gunner RightFront)</td><td>0xEAF6A00C</td><td>No</td><td>721</td><td>0x80006189</td><td>0x0000F48A</td></tr>
<tr><td>3 Seat Car (Gunner)</td><td>0x635DDFC9</td><td>No</td><td>11</td><td>0x8000234F</td><td>0x00004B5B</td></tr>
<tr><td>3 Seat Car (Passenger)</td><td>0xABE6688C</td><td>No</td><td>10</td><td>0x8000234D</td><td>0xFFFFFFFF</td></tr>
<tr><td>3ddecal_asphalt</td><td>0x29D0BDCB</td><td>No</td><td>6095</td><td>0x900001D6</td><td>0x00011FF1</td></tr>
<tr><td>3ddecal_brick</td><td>0xE893B9B5</td><td>No</td><td>6088</td><td>0x900001CF</td><td>0xFFFFFFFF</td></tr>
<tr><td>3ddecal_concrete_warm</td><td>0x3F637E01</td><td>No</td><td>6091</td><td>0x900001D2</td><td>0x00002CF4</td></tr>
<tr><td>3ddecal_dirt</td><td>0x7FFDAC69</td><td>No</td><td>6089</td><td>0x900001D0</td><td>0x0000EA17</td></tr>
<tr><td>3ddecal_metal</td><td>0xDCC30213</td><td>No</td><td>6092</td><td>0x900001D3</td><td>0x0000C774</td></tr>
<tr><td>3ddecal_rock</td><td>0x2926BC49</td><td>No</td><td>6093</td><td>0x900001D4</td><td>0x00011F5C</td></tr>
<tr><td>3ddecal_tile</td><td>0x0E8C523A</td><td>No</td><td>6090</td><td>0x900001D1</td><td>0x00008E40</td></tr>
<tr><td>3ddecal_wood</td><td>0xFBE4EEED</td><td>No</td><td>6094</td><td>0x900001D5</td><td>0x0000C980</td></tr>
<tr><td>68Valiant_Ruin</td><td>0x21C43ED9</td><td>No</td><td>1085</td><td>0x80006A30</td><td>0xFFFFFFFF</td></tr>
<tr><td>68Valiant_Ruin_fire</td><td>0x092DB194</td><td>No</td><td>2021</td><td>0x800080C4</td><td>0xFFFFFFFF</td></tr>
<tr><td>__AssetTest</td><td>0x5615C3ED</td><td>No</td><td>1557</td><td>0x8000719F</td><td>0x00006D92</td></tr>
<tr><td>__Building HP 025</td><td>0x45840CE6</td><td>No</td><td>2777</td><td>0x8000874F</td><td>0xFFFFFFFF</td></tr>
<tr><td>__Building HP 050</td><td>0x4B4189E6</td><td>No</td><td>2768</td><td>0x80008746</td><td>0x00011637</td></tr>
<tr><td>__Building HP 100</td><td>0x4E1DE140</td><td>No</td><td>2762</td><td>0x80008740</td><td>0xFFFFFFFF</td></tr>
<tr><td>__Building HP 150</td><td>0x1800E0A7</td><td>No</td><td>4068</td><td>0x80009AEE</td><td>0x000004A1</td></tr>
<tr><td>__Building HP 200</td><td>0xDAC80B8F</td><td>No</td><td>2763</td><td>0x80008741</td><td>0xFFFFFFFF</td></tr>
<tr><td>__Building HP 300</td><td>0xC867FCFA</td><td>No</td><td>2770</td><td>0x80008748</td><td>0xFFFFFFFF</td></tr>
<tr><td>__Building HP 400</td><td>0x851272D9</td><td>No</td><td>4070</td><td>0x80009AF0</td><td>0x0000317F</td></tr>
<tr><td>__Building HP 500</td><td>0x2A43B31C</td><td>No</td><td>2764</td><td>0x80008742</td><td>0x0000FA87</td></tr>
<tr><td>__Building HP 600</td><td>0x1393EC5B</td><td>No</td><td>4067</td><td>0x80009AED</td><td>0x0000E616</td></tr>
<tr><td>__Building HP 800</td><td>0xE049F895</td><td>No</td><td>4072</td><td>0x80009AF2</td><td>0x0001326D</td></tr>
<tr><td>__Building Shack</td><td>0xC33DD16B</td><td>No</td><td>2765</td><td>0x80008743</td><td>0x0000377D</td></tr>
<tr><td>__Building Skyscraper Large</td><td>0x51F35E97</td><td>No</td><td>2766</td><td>0x80008744</td><td>0x0000B978</td></tr>
<tr><td>__Building Skyscraper Medium</td><td>0x5537A857</td><td>No</td><td>1543</td><td>0x80007190</td><td>0x00003AD5</td></tr>
<tr><td>__Building Skyscraper Small</td><td>0x8CC6E63F</td><td>No</td><td>2769</td><td>0x80008747</td><td>0xFFFFFFFF</td></tr>
<tr><td>__Building Tough</td><td>0xE62D4C82</td><td>No</td><td>2767</td><td>0x80008745</td><td>0x0000EA84</td></tr>
<tr><td>__global_env_palmtree01</td><td>0x5536E844</td><td>No</td><td>2933</td><td>0x800089B4</td><td>0x0000C5AB</td></tr>
<tr><td>__global_env_palmtreebend02</td><td>0x3F5DB976</td><td>No</td><td>2944</td><td>0x800089C0</td><td>0x0000D061</td></tr>
<tr><td>__global_env_palmtreebend03</td><td>0x215FC8D3</td><td>No</td><td>2945</td><td>0x800089C1</td><td>0x000033B4</td></tr>
<tr><td>__global_env_palmtreebend04</td><td>0x1F6C91A0</td><td>No</td><td>2946</td><td>0x800089C2</td><td>0x0000E7AC</td></tr>
<tr><td>__global_env_palmtreebend05</td><td>0x496F1255</td><td>No</td><td>2947</td><td>0x800089C3</td><td>0x00010B05</td></tr>
<tr><td>__global_env_palmtreeplanted01</td><td>0x80ED4DAA</td><td>No</td><td>2948</td><td>0x800089C4</td><td>0x00009ABD</td></tr>
<tr><td>__global_env_tree01</td><td>0xF0486D5C</td><td>No</td><td>2934</td><td>0x800089B5</td><td>0xFFFFFFFF</td></tr>
<tr><td>__global_env_treeoak01</td><td>0xF26BBA79</td><td>No</td><td>2949</td><td>0x800089C5</td><td>0xFFFFFFFF</td></tr>
<tr><td>__global_env_treeplaza01</td><td>0xF394CA7C</td><td>No</td><td>2950</td><td>0x800089C6</td><td>0xFFFFFFFF</td></tr>
<tr><td>__global_env_treeplaza02</td><td>0xCD925013</td><td>No</td><td>2951</td><td>0x800089C7</td><td>0x00009464</td></tr>
<tr><td>__global_env_treeplaza03</td><td>0xEB9040B6</td><td>No</td><td>2952</td><td>0x800089C8</td><td>0x0000A53D</td></tr>
<tr><td>__global_env_treesidewalk01</td><td>0xA914401E</td><td>No</td><td>2932</td><td>0x800089B3</td><td>0xFFFFFFFF</td></tr>
<tr><td>__global_env_treespade</td><td>0xAA0976CC</td><td>No</td><td>2953</td><td>0x800089C9</td><td>0xFFFFFFFF</td></tr>
<tr><td>__global_env_treetropical01</td><td>0xEA7668B0</td><td>No</td><td>2929</td><td>0x800089B0</td><td>0xFFFFFFFF</td></tr>
<tr><td>__global_env_treetropical02</td><td>0xD4740777</td><td>No</td><td>2931</td><td>0x800089B2</td><td>0xFFFFFFFF</td></tr>
<tr><td>__jungle_env_largecanopy01</td><td>0x6694CAC1</td><td>No</td><td>2954</td><td>0x800089CA</td><td>0xFFFFFFFF</td></tr>
<tr><td>__jungle_env_smallcanopy01</td><td>0xC65D6C1D</td><td>No</td><td>2941</td><td>0x800089BC</td><td>0x00005FA5</td></tr>
<tr><td>__jungle_env_smallcanopy02</td><td>0x4455E3B2</td><td>No</td><td>3318</td><td>0x80008F82</td><td>0x0000325A</td></tr>
<tr><td>__jungle_env_treemedium01</td><td>0x7E251DAB</td><td>No</td><td>3750</td><td>0x80009712</td><td>0xFFFFFFFF</td></tr>
<tr><td>__jungle_env_treemedium03</td><td>0xFE2A6459</td><td>No</td><td>2937</td><td>0x800089B8</td><td>0x00010624</td></tr>
<tr><td>__jungle_env_treesmall01</td><td>0xBA098E81</td><td>No</td><td>2935</td><td>0x800089B6</td><td>0xFFFFFFFF</td></tr>
<tr><td>__jungle_env_treesmall02</td><td>0x38020616</td><td>No</td><td>2936</td><td>0x800089B7</td><td>0xFFFFFFFF</td></tr>
<tr><td>__jungle_env_treesmall03</td><td>0x9A04DEF3</td><td>No</td><td>3757</td><td>0x8000971F</td><td>0x0000C68C</td></tr>
<tr><td>__jungle_env_treetall01</td><td>0xC0E0D8A3</td><td>No</td><td>2963</td><td>0x800089D9</td><td>0x000039D0</td></tr>
<tr><td>__jungle_env_treetall02</td><td>0xA6E2EE4C</td><td>No</td><td>2964</td><td>0x800089DA</td><td>0x0000211D</td></tr>
<tr><td>__jungle_env_treetall03</td><td>0x20E5ECF1</td><td>No</td><td>2965</td><td>0x800089DB</td><td>0x0000C54B</td></tr>
<tr><td>__marsh_env_treewater02</td><td>0xB8F49502</td><td>No</td><td>2938</td><td>0x800089B9</td><td>0x0000D149</td></tr>
<tr><td>__placeable Environment Bush Plant</td><td>0x8F197374</td><td>No</td><td>4764</td><td>0x8000A177</td><td>0x0000DFFB</td></tr>
<tr><td>__placeable Environment Tree</td><td>0x988DDE4D</td><td>No</td><td>6079</td><td>0x900001C1</td><td>0x00005E53</td></tr>
<tr><td>__shanty_env_tree01</td><td>0x11441BFC</td><td>No</td><td>2966</td><td>0x800089E2</td><td>0x000012BC</td></tr>
<tr><td>__shanty_env_tree02</td><td>0xEB41A193</td><td>No</td><td>3751</td><td>0x80009713</td><td>0xFFFFFFFF</td></tr>
<tr><td>__shanty_env_tree03</td><td>0x093F9236</td><td>No</td><td>3752</td><td>0x80009714</td><td>0xFFFFFFFF</td></tr>
<tr><td>__Static Destructible (Crashable)</td><td>0xD192FB1F</td><td>No</td><td>2778</td><td>0x80008750</td><td>0xFFFFFFFF</td></tr>
<tr><td>__Static Destructible (Explosive)</td><td>0x66201E9B</td><td>No</td><td>4071</td><td>0x80009AF1</td><td>0x00012D44</td></tr>
<tr><td>__Static Destructible (Sandbag)</td><td>0x357D5850</td><td>No</td><td>2779</td><td>0x80008751</td><td>0xFFFFFFFF</td></tr>
<tr><td>__Static Destructible (Tower)</td><td>0x5442049D</td><td>No</td><td>2780</td><td>0x80008752</td><td>0x000011BC</td></tr>
<tr><td>__Static Destructible HP 025</td><td>0xCBFFD998</td><td>No</td><td>4069</td><td>0x80009AEF</td><td>0x0000BEFA</td></tr>
<tr><td>__Static Destructible HP 050</td><td>0x15188514</td><td>No</td><td>6080</td><td>0x900001C2</td><td>0x00012DD2</td></tr>
<tr><td>__Static Destructible HP 100</td><td>0xB5B55B0E</td><td>No</td><td>4074</td><td>0x80009AF4</td><td>0xFFFFFFFF</td></tr>
<tr><td>__Static Destructible HP 300</td><td>0x4B6B5884</td><td>No</td><td>4073</td><td>0x80009AF3</td><td>0x00013786</td></tr>
<tr><td>_airport_bld_controltower</td><td>0x5E4C3BFF</td><td>No</td><td>1837</td><td>0x800076D1</td><td>0x0000E0AB</td></tr>
<tr><td>_airport_bld_hanger01</td><td>0xEC8EFD29</td><td>No</td><td>1667</td><td>0x8000735A</td><td>0x000072A3</td></tr>
<tr><td>_airport_bld_terminal01</td><td>0x2E94EDF0</td><td>No</td><td>1836</td><td>0x800076D0</td><td>0x0000C6DB</td></tr>
<tr><td>_airport_runway1</td><td>0x677B7E05</td><td>No</td><td>1724</td><td>0x8000759F</td><td>0x0000F165</td></tr>
<tr><td>_airport_sign</td><td>0x2AF74AC3</td><td>No</td><td>5416</td><td>0x8000A9E9</td><td>0x0000D74B</td></tr>
<tr><td>_airport_whitestripe1</td><td>0x3A5EF939</td><td>No</td><td>1725</td><td>0x800075A0</td><td>0x000005B7</td></tr>
<tr><td>_aloutpost_bld_alarmtower</td><td>0x24B533CD</td><td>No</td><td>5454</td><td>0x8000AA55</td><td>0x000072D4</td></tr>
<tr><td>_aloutpost_bld_barracks01</td><td>0x67FDE537</td><td>No</td><td>6063</td><td>0x900001AF</td><td>0x000125FB</td></tr>
<tr><td>_aloutpost_bld_barracks02</td><td>0x7E004670</td><td>No</td><td>6064</td><td>0x900001B0</td><td>0x00010995</td></tr>
<tr><td>_aloutpost_bld_barracks03</td><td>0xE8032BE5</td><td>No</td><td>6065</td><td>0x900001B1</td><td>0x00013B4B</td></tr>
<tr><td>_aloutpost_bld_bunker</td><td>0xEBC079B4</td><td>No</td><td>2921</td><td>0x800089A5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_aloutpost_bld_command</td><td>0xC65DEA56</td><td>No</td><td>6066</td><td>0x900001B2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_aloutpost_bld_garage01</td><td>0x1344DF91</td><td>No</td><td>6067</td><td>0x900001B3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_aloutpost_bld_guardtowershort</td><td>0xC6F6E74D</td><td>No</td><td>282</td><td>0x80004DE2</td><td>0x00003E4D</td></tr>
<tr><td>_aloutpost_bld_guardtowertall</td><td>0xA89C2354</td><td>No</td><td>283</td><td>0x80004DE3</td><td>0x000131BA</td></tr>
<tr><td>_aloutpost_bld_hangar</td><td>0xADB07296</td><td>No</td><td>284</td><td>0x80004DE4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_aloutpost_bld_hangersmall</td><td>0x85298903</td><td>No</td><td>6068</td><td>0x900001B4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_aloutpost_bld_helipad</td><td>0x4D0BF49A</td><td>Yes</td><td>3758</td><td>0x80009720</td><td>0x0001258B</td></tr>
<tr><td>_aloutpost_bld_helipad_roof</td><td>0xE010DB4B</td><td>Yes</td><td>5476</td><td>0x8000AA6D</td><td>0x0000FB83</td></tr>
<tr><td>_aloutpost_bld_largetent</td><td>0x2EC3CB1B</td><td>No</td><td>3998</td><td>0x80009993</td><td>0x000020A8</td></tr>
<tr><td>_aloutpost_bld_largetentextensionA</td><td>0x2BBA049F</td><td>No</td><td>4512</td><td>0x80009EF8</td><td>0x000041F2</td></tr>
<tr><td>_aloutpost_bld_prison</td><td>0x6CDF420A</td><td>No</td><td>325</td><td>0x80004E17</td><td>0x0000E760</td></tr>
<tr><td>_aloutpost_bld_prison_fence</td><td>0xA82FD3E0</td><td>No</td><td>4187</td><td>0x80009C1F</td><td>0x000100C0</td></tr>
<tr><td>_aloutpost_bld_storage</td><td>0x9AC533E6</td><td>No</td><td>371</td><td>0x80005106</td><td>0x000004DA</td></tr>
<tr><td>_aloutpost_bld_storage_fence</td><td>0xDC45D2A4</td><td>No</td><td>4188</td><td>0x80009C20</td><td>0x000125C5</td></tr>
<tr><td>_aloutpost_bld_supplydepot</td><td>0x25330130</td><td>No</td><td>285</td><td>0x80004DE5</td><td>0x0000672A</td></tr>
<tr><td>_aloutpost_concretewall01</td><td>0xD0A85272</td><td>No</td><td>3762</td><td>0x80009724</td><td>0x000010FE</td></tr>
<tr><td>_aloutpost_concretewall02</td><td>0x52AFDADD</td><td>No</td><td>3763</td><td>0x80009725</td><td>0x00006F72</td></tr>
<tr><td>_aloutpost_fueltanks</td><td>0xFA4F4AB5</td><td>Yes</td><td>4544</td><td>0x80009F19</td><td>0xFFFFFFFF</td></tr>
<tr><td>_aloutpost_gateentrance</td><td>0xAD110E85</td><td>No</td><td>4784</td><td>0x8000A18D</td><td>0x00013ECF</td></tr>
<tr><td>_aloutpost_interior_herochair</td><td>0x7C809884</td><td>No</td><td>4394</td><td>0x80009DC6</td><td>0x00010335</td></tr>
<tr><td>_aloutpost_interior_job</td><td>0x4C33E8D2</td><td>No</td><td>4754</td><td>0x8000A16D</td><td>0x0001096E</td></tr>
<tr><td>_angelfalls_env_base</td><td>0xAA17FEF9</td><td>No</td><td>2051</td><td>0x80008126</td><td>0x00010B96</td></tr>
<tr><td>_angelfalls_env_basecornerupleft</td><td>0xC3B55702</td><td>No</td><td>2054</td><td>0x80008129</td><td>0xFFFFFFFF</td></tr>
<tr><td>_angelfalls_env_basecornerupright</td><td>0x47D0CE79</td><td>No</td><td>2055</td><td>0x8000812A</td><td>0x0000BE54</td></tr>
<tr><td>_angelfalls_env_canyonside</td><td>0x665452E3</td><td>No</td><td>2062</td><td>0x80008132</td><td>0xFFFFFFFF</td></tr>
<tr><td>_angelfalls_env_middle</td><td>0x65F6EFF9</td><td>No</td><td>2052</td><td>0x80008127</td><td>0x0000AB59</td></tr>
<tr><td>_angelfalls_env_middlecornerdownleft</td><td>0x0894CF99</td><td>No</td><td>2056</td><td>0x8000812B</td><td>0x000003AF</td></tr>
<tr><td>_angelfalls_env_middlecornerdownright</td><td>0xE09BE800</td><td>No</td><td>2057</td><td>0x8000812C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_angelfalls_env_middlecornerupleft</td><td>0x0ED17802</td><td>No</td><td>2059</td><td>0x8000812E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_angelfalls_env_middlecornerupright</td><td>0x8518C179</td><td>No</td><td>2058</td><td>0x8000812D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_angelfalls_env_top</td><td>0xF3BE17CF</td><td>No</td><td>2053</td><td>0x80008128</td><td>0xFFFFFFFF</td></tr>
<tr><td>_angelfalls_env_topcornerdownleft</td><td>0x509F68F3</td><td>No</td><td>2060</td><td>0x80008130</td><td>0xFFFFFFFF</td></tr>
<tr><td>_angelfalls_env_topcornerdownright</td><td>0x6E47829A</td><td>No</td><td>2061</td><td>0x80008131</td><td>0xFFFFFFFF</td></tr>
<tr><td>_angelfalls_env_topcornerupleft</td><td>0x04D0C2A8</td><td>No</td><td>2063</td><td>0x80008133</td><td>0x000036DF</td></tr>
<tr><td>_angelfalls_env_topcornerupright</td><td>0x2801FC8F</td><td>No</td><td>2064</td><td>0x80008134</td><td>0x00003CE4</td></tr>
<tr><td>_angelfalls_env_waterfallbase</td><td>0x229B202F</td><td>No</td><td>2065</td><td>0x80008135</td><td>0x0000B8EF</td></tr>
<tr><td>_angelfalls_env_waterfallbase_stream</td><td>0x2CC3211E</td><td>No</td><td>2069</td><td>0x8000813B</td><td>0x00007D62</td></tr>
<tr><td>_angelfalls_env_waterfallmiddle</td><td>0xBC41B837</td><td>No</td><td>2066</td><td>0x80008136</td><td>0x0000CA12</td></tr>
<tr><td>_angelfalls_env_waterfallmiddle_stream</td><td>0x891EE676</td><td>No</td><td>2070</td><td>0x8000813D</td><td>0x000100E3</td></tr>
<tr><td>_angelfalls_env_waterfalltop</td><td>0xD6486DDD</td><td>No</td><td>2067</td><td>0x80008137</td><td>0x0000F831</td></tr>
<tr><td>_angelfalls_env_waterfalltop_stream</td><td>0xD5381B4C</td><td>No</td><td>2071</td><td>0x8000813E</td><td>0x000136A1</td></tr>
<tr><td>_asset_building</td><td>0xC53B3283</td><td>No</td><td>1563</td><td>0x800071A5</td><td>0x000139CA</td></tr>
<tr><td>_asset_building2</td><td>0xA51C6ED3</td><td>No</td><td>1562</td><td>0x800071A4</td><td>0x0000293F</td></tr>
<tr><td>_asset_none</td><td>0xB3807B61</td><td>No</td><td>1558</td><td>0x800071A0</td><td>0x0000AD5C</td></tr>
<tr><td>_asset_none2</td><td>0x7E06E8C9</td><td>No</td><td>1556</td><td>0x8000719E</td><td>0x00010C64</td></tr>
<tr><td>_asset_prop</td><td>0x16292198</td><td>No</td><td>1560</td><td>0x800071A2</td><td>0x00003CCE</td></tr>
<tr><td>_asset_prop2</td><td>0x94D392EE</td><td>No</td><td>1561</td><td>0x800071A3</td><td>0x0000E35E</td></tr>
<tr><td>_asset_skyscraper</td><td>0x3F3FEA20</td><td>No</td><td>1559</td><td>0x800071A1</td><td>0x00003944</td></tr>
<tr><td>_asset_skyscraper2</td><td>0x1BD8CE66</td><td>No</td><td>1564</td><td>0x800071A6</td><td>0x00007358</td></tr>
<tr><td>_Car Camera Presets</td><td>0xEFBFD4DF</td><td>No</td><td>5052</td><td>0x8000A3F1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Caracas_bld_capitol</td><td>0x2500A86E</td><td>No</td><td>1368</td><td>0x80006ED6</td><td>0x000135F5</td></tr>
<tr><td>_Caracas_bld_capitol_ruined</td><td>0xC126FA94</td><td>No</td><td>4632</td><td>0x80009FB9</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_bld_cathedral</td><td>0xE33F6880</td><td>No</td><td>1295</td><td>0x80006D90</td><td>0x00008346</td></tr>
<tr><td>_caracas_bld_cathedral_ruined</td><td>0x51DD01AE</td><td>No</td><td>4631</td><td>0x80009FB8</td><td>0x00003867</td></tr>
<tr><td>_caracas_bld_cathedralstatue</td><td>0x5772D59C</td><td>No</td><td>1296</td><td>0x80006D91</td><td>0x00011586</td></tr>
<tr><td>_caracas_bld_construction01</td><td>0xF296DF56</td><td>No</td><td>1369</td><td>0x80006ED7</td><td>0x0000A690</td></tr>
<tr><td>_caracas_bld_construction01_ruined</td><td>0x1CE382DC</td><td>No</td><td>4613</td><td>0x80009FA5</td><td>0x0000CC59</td></tr>
<tr><td>_caracas_bld_firestation</td><td>0x681CB84C</td><td>No</td><td>1001</td><td>0x80006889</td><td>0x00007E90</td></tr>
<tr><td>_caracas_bld_governmentcorner01</td><td>0x04082523</td><td>No</td><td>1370</td><td>0x80006ED8</td><td>0x00011284</td></tr>
<tr><td>_caracas_bld_governmentcorner02</td><td>0xEA0A3ACC</td><td>No</td><td>1371</td><td>0x80006ED9</td><td>0x00001FB7</td></tr>
<tr><td>_caracas_bld_governmentsegment</td><td>0x1184AC2C</td><td>No</td><td>1372</td><td>0x80006EDA</td><td>0x000074C4</td></tr>
<tr><td>_caracas_bld_historical01</td><td>0xD22DFEAD</td><td>No</td><td>1387</td><td>0x80006EE9</td><td>0x000063EA</td></tr>
<tr><td>_caracas_bld_historical02</td><td>0x50267642</td><td>No</td><td>1388</td><td>0x80006EEA</td><td>0x000022BA</td></tr>
<tr><td>_caracas_bld_historical02_ruined</td><td>0x521AE9B8</td><td>No</td><td>4620</td><td>0x80009FAD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_bld_historical03</td><td>0x3228859F</td><td>No</td><td>6061</td><td>0x900001AD</td><td>0x00001EDC</td></tr>
<tr><td>_caracas_bld_historical03_ruined</td><td>0xFDE8B443</td><td>No</td><td>3271</td><td>0x80008F48</td><td>0x0000E853</td></tr>
<tr><td>_caracas_bld_historical04</td><td>0xD0212F94</td><td>No</td><td>1389</td><td>0x80006EEB</td><td>0x0000292F</td></tr>
<tr><td>_caracas_bld_historical04_ruined</td><td>0x7EA5F2A2</td><td>No</td><td>4619</td><td>0x80009FAC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_bld_historical05</td><td>0x2A23FBD9</td><td>No</td><td>1390</td><td>0x80006EEC</td><td>0x00007446</td></tr>
<tr><td>_caracas_bld_historical05_ruined</td><td>0xBCE17DED</td><td>No</td><td>4147</td><td>0x80009B4A</td><td>0x000082F8</td></tr>
<tr><td>_caracas_bld_hospitalvargas</td><td>0x5FA05820</td><td>No</td><td>1113</td><td>0x80006B47</td><td>0x0001028A</td></tr>
<tr><td>_caracas_bld_hospitalvargas_ruined</td><td>0x47BBABCE</td><td>No</td><td>4146</td><td>0x80009B49</td><td>0x00008DCB</td></tr>
<tr><td>_caracas_bld_parkingstructure01</td><td>0x65DF6146</td><td>No</td><td>1384</td><td>0x80006EE6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_bld_parquecentral01</td><td>0xEC0299F2</td><td>No</td><td>1297</td><td>0x80006D92</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_bld_parquecentral01_ruined</td><td>0x34453CE8</td><td>No</td><td>4624</td><td>0x80009FB1</td><td>0x00005633</td></tr>
<tr><td>_caracas_bld_parquecentral02</td><td>0x6E0A225D</td><td>No</td><td>1298</td><td>0x80006D93</td><td>0x00010FFB</td></tr>
<tr><td>_caracas_bld_parquecentral02_ruined</td><td>0xB90E5371</td><td>No</td><td>4622</td><td>0x80009FAF</td><td>0x0000BD17</td></tr>
<tr><td>_caracas_bld_parquecentral03</td><td>0x84080668</td><td>No</td><td>1299</td><td>0x80006D94</td><td>0x00010A50</td></tr>
<tr><td>_caracas_bld_parquecentral03_ruined</td><td>0x759901F6</td><td>No</td><td>4623</td><td>0x80009FB0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_bld_plazaparquecentral01</td><td>0xB16EB0E8</td><td>No</td><td>1300</td><td>0x80006D95</td><td>0x00002C18</td></tr>
<tr><td>_caracas_bld_plazaparquecentral02</td><td>0x3B6BB88F</td><td>No</td><td>1373</td><td>0x80006EDB</td><td>0x00006180</td></tr>
<tr><td>_caracas_bld_skyscraperblacktower01</td><td>0xB9253A62</td><td>No</td><td>1374</td><td>0x80006EDC</td><td>0x00010598</td></tr>
<tr><td>_caracas_bld_skyscraperblacktower01_ruined</td><td>0x6CF5EA58</td><td>No</td><td>4625</td><td>0x80009FB2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_bld_skyscraperbluetower01</td><td>0x8E46A4BF</td><td>No</td><td>1375</td><td>0x80006EDD</td><td>0x0000A836</td></tr>
<tr><td>_caracas_bld_skyscraperbluetower01_ruined</td><td>0xCC2E0AE3</td><td>No</td><td>4621</td><td>0x80009FAE</td><td>0x0000741E</td></tr>
<tr><td>_caracas_bld_skyscrapercollapsed01</td><td>0x9E35963F</td><td>No</td><td>1376</td><td>0x80006EDE</td><td>0x00006FF5</td></tr>
<tr><td>_caracas_bld_skyscrapercollapsed02</td><td>0x9437C518</td><td>No</td><td>1391</td><td>0x80006EED</td><td>0x0000954A</td></tr>
<tr><td>_caracas_bld_skyscraperpristine01</td><td>0x6B8C2D4E</td><td>No</td><td>1015</td><td>0x8000689F</td><td>0x00007675</td></tr>
<tr><td>_caracas_bld_skyscraperpristine02</td><td>0xCD938359</td><td>No</td><td>1107</td><td>0x80006B41</td><td>0x000008B4</td></tr>
<tr><td>_caracas_bld_skyscraperpristine02_ruined</td><td>0x0D6D586D</td><td>No</td><td>4627</td><td>0x80009FB4</td><td>0x00003AFC</td></tr>
<tr><td>_caracas_bld_skyscraperpristine03</td><td>0x7390B714</td><td>No</td><td>1114</td><td>0x80006B48</td><td>0x0000CABF</td></tr>
<tr><td>_caracas_bld_skyscraperpristine03_ruined</td><td>0xCF31CD22</td><td>No</td><td>4618</td><td>0x80009FAB</td><td>0x00009517</td></tr>
<tr><td>_caracas_bld_skytrammain</td><td>0x53EFD034</td><td>No</td><td>1377</td><td>0x80006EDF</td><td>0x00000EC5</td></tr>
<tr><td>_caracas_bld_skytrammain_ruined</td><td>0x29BD6DC2</td><td>No</td><td>4610</td><td>0x80009FA2</td><td>0x00004018</td></tr>
<tr><td>_caracas_bld_skytramshopA</td><td>0xC3132D1C</td><td>No</td><td>1003</td><td>0x8000688B</td><td>0x000071D2</td></tr>
<tr><td>_caracas_bld_skytramshopB</td><td>0x9D10B2B3</td><td>No</td><td>1002</td><td>0x8000688A</td><td>0x0000F3E0</td></tr>
<tr><td>_caracas_bld_theater01</td><td>0xF0C5FA5A</td><td>No</td><td>1392</td><td>0x80006EEE</td><td>0x000077B4</td></tr>
<tr><td>_caracas_bld_theater01_Ruined</td><td>0xF28803D0</td><td>No</td><td>4143</td><td>0x80009B46</td><td>0x000025D1</td></tr>
<tr><td>_caracas_bridgegovernment01</td><td>0x523CC48A</td><td>No</td><td>1378</td><td>0x80006EE0</td><td>0x00004CD5</td></tr>
<tr><td>_caracas_bridgeparquecentral</td><td>0x264CC375</td><td>No</td><td>1301</td><td>0x80006D96</td><td>0x000048B7</td></tr>
<tr><td>_caracas_capitolstatue</td><td>0x7BAF0531</td><td>No</td><td>6062</td><td>0x900001AE</td><td>0x000114F5</td></tr>
<tr><td>_caracas_cathedralplateau</td><td>0xF92CAE8F</td><td>No</td><td>5464</td><td>0x8000AA60</td><td>0x0000D0C5</td></tr>
<tr><td>_caracas_fountaingovernment</td><td>0x415702CC</td><td>No</td><td>1379</td><td>0x80006EE1</td><td>0x0000CC89</td></tr>
<tr><td>_caracas_fountainparquecentral</td><td>0xC1306DE0</td><td>No</td><td>1302</td><td>0x80006D97</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_lawngovernment01</td><td>0xFD46330B</td><td>No</td><td>1481</td><td>0x80007020</td><td>0x00006514</td></tr>
<tr><td>_caracas_lawngovernment02</td><td>0x2348AD74</td><td>No</td><td>1482</td><td>0x80007021</td><td>0x0000764F</td></tr>
<tr><td>_caracas_lawngovernment03</td><td>0xFD4AB039</td><td>No</td><td>1483</td><td>0x80007022</td><td>0x00009F5D</td></tr>
<tr><td>_caracas_lawnparquecentral01</td><td>0xD84A4F83</td><td>No</td><td>1484</td><td>0x80007023</td><td>0x00001B47</td></tr>
<tr><td>_caracas_lawnparquecentral02</td><td>0x3E4D2EAC</td><td>No</td><td>1485</td><td>0x80007024</td><td>0x0000A066</td></tr>
<tr><td>_caracas_lawnparquecentral03</td><td>0x384F63D1</td><td>No</td><td>1486</td><td>0x80007025</td><td>0x0000D81E</td></tr>
<tr><td>_caracas_lawnparquecentral04</td><td>0x5E51DE3A</td><td>No</td><td>1487</td><td>0x80007026</td><td>0x00012E51</td></tr>
<tr><td>_caracas_plantercapitolcenter</td><td>0xF1693392</td><td>No</td><td>1303</td><td>0x80006D98</td><td>0x00003A70</td></tr>
<tr><td>_caracas_plantercapitolleft</td><td>0x236591D6</td><td>No</td><td>1304</td><td>0x80006D99</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_plantercapitolright</td><td>0x172D7565</td><td>No</td><td>1305</td><td>0x80006D9A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_portplateau01</td><td>0x7B79F7CB</td><td>No</td><td>5458</td><td>0x8000AA59</td><td>0x0001294B</td></tr>
<tr><td>_caracas_portplateau02</td><td>0xA17C7234</td><td>No</td><td>5460</td><td>0x8000AA5C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_rampgovernment01</td><td>0xCCED9715</td><td>No</td><td>1380</td><td>0x80006EE2</td><td>0x00010E01</td></tr>
<tr><td>_caracas_rampgovernment02</td><td>0x2AE5DC4A</td><td>No</td><td>1381</td><td>0x80006EE3</td><td>0x0001148D</td></tr>
<tr><td>_caracas_rampgovernmentmid</td><td>0x711E350E</td><td>No</td><td>1382</td><td>0x80006EE4</td><td>0x00011AB8</td></tr>
<tr><td>_caracas_shoppingcenterplateau</td><td>0x18B51B98</td><td>No</td><td>5463</td><td>0x8000AA5F</td><td>0x0000792A</td></tr>
<tr><td>_caracas_sidewalk1</td><td>0x532E30A0</td><td>No</td><td>1728</td><td>0x800075A4</td><td>0x00011ABE</td></tr>
<tr><td>_caracas_sidewalk2</td><td>0xFD2B6AA7</td><td>No</td><td>1729</td><td>0x800075A5</td><td>0x00011CB0</td></tr>
<tr><td>_caracas_skyscraperplateau01</td><td>0xD5826019</td><td>No</td><td>5462</td><td>0x8000AA5E</td><td>0x000131A3</td></tr>
<tr><td>_caracas_skyscraperplateau02</td><td>0x737B0A0E</td><td>No</td><td>5461</td><td>0x8000AA5D</td><td>0x00008281</td></tr>
<tr><td>_caracas_skytramcolumn</td><td>0x51ED0322</td><td>No</td><td>1385</td><td>0x80006EE7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_skytramplateau01</td><td>0xA9043933</td><td>No</td><td>5431</td><td>0x8000A9F9</td><td>0x000102E5</td></tr>
<tr><td>_caracas_stairparquecentrallong</td><td>0x1CFEF671</td><td>No</td><td>1731</td><td>0x800075A7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_stairparquecentralshort</td><td>0x3890ADFF</td><td>No</td><td>1730</td><td>0x800075A6</td><td>0x0000B0D1</td></tr>
<tr><td>_caracas_wallcorner</td><td>0xF75A76E6</td><td>No</td><td>6081</td><td>0x900001C3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_wallcorner_pristine</td><td>0xDEBD3609</td><td>No</td><td>4192</td><td>0x80009C24</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_walllong</td><td>0xB6046123</td><td>No</td><td>1733</td><td>0x800075AB</td><td>0x000085FD</td></tr>
<tr><td>_caracas_walllong_pristine</td><td>0xA213FB4A</td><td>No</td><td>4193</td><td>0x80009C25</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracas_wallshort</td><td>0x229F1AB5</td><td>No</td><td>1732</td><td>0x800075AA</td><td>0x00008235</td></tr>
<tr><td>_caracas_wallshort_pristine</td><td>0xDBC9A110</td><td>No</td><td>4194</td><td>0x80009C26</td><td>0x0000F781</td></tr>
<tr><td>_caracasruins_bld_corner16x16A</td><td>0x96E06243</td><td>No</td><td>5477</td><td>0x8000AA6E</td><td>0x00004639</td></tr>
<tr><td>_caracasruins_bld_corner16x16B</td><td>0xFCE3416C</td><td>No</td><td>5478</td><td>0x8000AA6F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracasruins_bld_corner16x32A</td><td>0xAB6A5785</td><td>No</td><td>5479</td><td>0x8000AA70</td><td>0xFFFFFFFF</td></tr>
<tr><td>_caracasruins_bld_corner16x32B</td><td>0x4963017A</td><td>No</td><td>5480</td><td>0x8000AA71</td><td>0x0000BA7B</td></tr>
<tr><td>_caracasruins_bld_corner32x32A</td><td>0x87BCBC9B</td><td>No</td><td>5482</td><td>0x8000AA73</td><td>0x0000C4B7</td></tr>
<tr><td>_caracasruins_bld_corner32x32B</td><td>0xEDBF9BC4</td><td>No</td><td>5481</td><td>0x8000AA72</td><td>0x00001847</td></tr>
<tr><td>_chinaoutpost_bld_alarmtower</td><td>0x8324C22F</td><td>No</td><td>5455</td><td>0x8000AA56</td><td>0x0000BF35</td></tr>
<tr><td>_chinaoutpost_bld_commbunker01</td><td>0xD134C65F</td><td>No</td><td>6060</td><td>0x900001AC</td><td>0x0000F49C</td></tr>
<tr><td>_chinaoutpost_bld_commbunker01_ruined</td><td>0x52562803</td><td>No</td><td>3592</td><td>0x800093E5</td><td>0x000117F1</td></tr>
<tr><td>_chinaoutpost_bld_guardpost01</td><td>0xCC80CE0B</td><td>No</td><td>6085</td><td>0x900001C8</td><td>0x00013B91</td></tr>
<tr><td>_chinaoutpost_bld_guardpost01_gate</td><td>0xE1EE029B</td><td>No</td><td>3768</td><td>0x8000972A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_chinaoutpost_bld_guardtowershort</td><td>0xCAB1A873</td><td>No</td><td>326</td><td>0x80004E18</td><td>0x00013754</td></tr>
<tr><td>_chinaoutpost_bld_guardtowershort_ruined</td><td>0x5463E277</td><td>No</td><td>3591</td><td>0x800093E4</td><td>0x00001CF3</td></tr>
<tr><td>_chinaoutpost_bld_guardtowertall</td><td>0xE8F3EA02</td><td>No</td><td>327</td><td>0x80004E19</td><td>0xFFFFFFFF</td></tr>
<tr><td>_chinaoutpost_bld_hangar01</td><td>0x2CCE9531</td><td>No</td><td>6059</td><td>0x900001AB</td><td>0x0000DEAF</td></tr>
<tr><td>_chinaoutpost_bld_hangar01_ruined</td><td>0xA6D64645</td><td>No</td><td>3593</td><td>0x800093E6</td><td>0x00001D8A</td></tr>
<tr><td>_chinaoutpost_bld_helipad</td><td>0xD193F670</td><td>Yes</td><td>3759</td><td>0x80009721</td><td>0xFFFFFFFF</td></tr>
<tr><td>_chinaoutpost_bld_prison</td><td>0xB5E32044</td><td>No</td><td>320</td><td>0x80004E12</td><td>0x000024AF</td></tr>
<tr><td>_chinaoutpost_bld_prison_fence</td><td>0x6DAF8CD2</td><td>No</td><td>3993</td><td>0x8000998C</td><td>0x00002C12</td></tr>
<tr><td>_chinaoutpost_bld_prison_gate</td><td>0x983B00F2</td><td>No</td><td>3992</td><td>0x80009989</td><td>0x00009B0F</td></tr>
<tr><td>_chinaoutpost_bld_prison_ruined</td><td>0x3960C5D2</td><td>No</td><td>3594</td><td>0x800093E7</td><td>0x0000F28A</td></tr>
<tr><td>_chinaoutpost_bld_storage</td><td>0xD0D21854</td><td>No</td><td>319</td><td>0x80004E11</td><td>0xFFFFFFFF</td></tr>
<tr><td>_chinaoutpost_bld_tent01</td><td>0x5BE217AB</td><td>No</td><td>321</td><td>0x80004E13</td><td>0x0000D4A8</td></tr>
<tr><td>_chinaoutpost_bld_tent02</td><td>0x81E49214</td><td>No</td><td>322</td><td>0x80004E14</td><td>0x00008A3F</td></tr>
<tr><td>_chinaoutpost_bld_tent02_ruined</td><td>0xB51D8622</td><td>No</td><td>3598</td><td>0x800093EB</td><td>0x00006BB6</td></tr>
<tr><td>_chinaoutpost_concretewall01</td><td>0xD21BD8A4</td><td>No</td><td>150</td><td>0x80004CE1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_chinaoutpost_concretewall01_lowhealth</td><td>0xE5D65DB5</td><td>No</td><td>5534</td><td>0x8000AB45</td><td>0xFFFFFFFF</td></tr>
<tr><td>_chinaoutpost_concretewall02</td><td>0xEC19C2FB</td><td>No</td><td>3748</td><td>0x80009710</td><td>0x0000FF5A</td></tr>
<tr><td>_chinaoutpost_fueltanks</td><td>0xC12AD01B</td><td>Yes</td><td>4545</td><td>0x80009F1A</td><td>0x0000D3A8</td></tr>
<tr><td>_chinaoutpost_gateentrance</td><td>0x4A74B8DB</td><td>No</td><td>4783</td><td>0x8000A18C</td><td>0x0000C959</td></tr>
<tr><td>_chinaoutpost_interior_job</td><td>0x8FB388F4</td><td>No</td><td>4755</td><td>0x8000A16E</td><td>0x0001174B</td></tr>
<tr><td>_chinaoutpost_signbarrier</td><td>0x036E6494</td><td>No</td><td>3769</td><td>0x8000972B</td><td>0x0000D3DB</td></tr>
<tr><td>_city_bld_apartment01</td><td>0x8229E3DC</td><td>No</td><td>1011</td><td>0x8000689B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_apartment01_ruined</td><td>0x8697A5CA</td><td>No</td><td>4633</td><td>0x80009FBA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_apartment02</td><td>0x5C276973</td><td>No</td><td>1012</td><td>0x8000689C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_apartment02_ruined</td><td>0x59341D77</td><td>No</td><td>4634</td><td>0x80009FBB</td><td>0x0000AE72</td></tr>
<tr><td>_city_bld_apartment03</td><td>0xFA249096</td><td>No</td><td>1013</td><td>0x8000689D</td><td>0x00000ABB</td></tr>
<tr><td>_city_bld_apartment03_ruined</td><td>0xD0D8BE1C</td><td>No</td><td>4635</td><td>0x80009FBC</td><td>0x0000BA4A</td></tr>
<tr><td>_city_bld_apartment04</td><td>0x0435E975</td><td>No</td><td>1016</td><td>0x800068A0</td><td>0x0000A080</td></tr>
<tr><td>_city_bld_apartment04_ruined</td><td>0xCACDD789</td><td>No</td><td>4636</td><td>0x80009FBD</td><td>0x0000027D</td></tr>
<tr><td>_city_bld_apartment05</td><td>0xDA3368C0</td><td>No</td><td>1115</td><td>0x80006B49</td><td>0x00000758</td></tr>
<tr><td>_city_bld_apartment05_ruined</td><td>0x7C9FC0EE</td><td>No</td><td>4637</td><td>0x80009FBE</td><td>0x00003D58</td></tr>
<tr><td>_city_bld_apartment06</td><td>0x04316C47</td><td>No</td><td>786</td><td>0x8000622C</td><td>0x0000D869</td></tr>
<tr><td>_city_bld_apartment06_ruined</td><td>0x3FEE5A0B</td><td>No</td><td>4638</td><td>0x80009FBF</td><td>0x00012732</td></tr>
<tr><td>_city_bld_corner16x16a</td><td>0xAB93F71D</td><td>No</td><td>637</td><td>0x80005C44</td><td>0x000075D9</td></tr>
<tr><td>_city_bld_corner16x16a_ruined</td><td>0xF4220431</td><td>No</td><td>3569</td><td>0x800093CD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_corner16x16b</td><td>0x298C6EB2</td><td>No</td><td>900</td><td>0x800064AD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_corner16x16b_ruined</td><td>0xFDE2BCA8</td><td>No</td><td>4142</td><td>0x80009B44</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_corner16x16c</td><td>0x4B8EE2CF</td><td>No</td><td>899</td><td>0x800064AC</td><td>0x0001361A</td></tr>
<tr><td>_city_bld_corner16x16c_ruined</td><td>0x3C7D7B33</td><td>No</td><td>3570</td><td>0x800093CE</td><td>0x00006E3F</td></tr>
<tr><td>_city_bld_corner16x16d</td><td>0x2987F184</td><td>No</td><td>902</td><td>0x800064B0</td><td>0x00005328</td></tr>
<tr><td>_city_bld_corner16x16d_ruined</td><td>0x959C7012</td><td>No</td><td>4148</td><td>0x80009B4B</td><td>0x0000000C</td></tr>
<tr><td>_city_bld_corner16x32A</td><td>0x7E3F8303</td><td>No</td><td>1000</td><td>0x80006888</td><td>0x000038FB</td></tr>
<tr><td>_city_bld_corner16x32A_ruined</td><td>0xA28C3807</td><td>No</td><td>3571</td><td>0x800093CF</td><td>0x0000002E</td></tr>
<tr><td>_city_bld_corner16x32B</td><td>0xE442622C</td><td>No</td><td>1020</td><td>0x800068A4</td><td>0x000106F6</td></tr>
<tr><td>_city_bld_corner16x32B_ruined</td><td>0x69C2E41A</td><td>No</td><td>4597</td><td>0x80009F94</td><td>0x0000AC79</td></tr>
<tr><td>_city_bld_corner16x32C</td><td>0xDE449751</td><td>No</td><td>1021</td><td>0x800068A5</td><td>0x00010C17</td></tr>
<tr><td>_city_bld_corner16x32D</td><td>0x044711BA</td><td>No</td><td>1104</td><td>0x80006B3E</td><td>0x000030CD</td></tr>
<tr><td>_city_bld_corner16x32D_ruined</td><td>0x419790B0</td><td>No</td><td>4628</td><td>0x80009FB5</td><td>0x00002836</td></tr>
<tr><td>_city_bld_corner32x32A</td><td>0x4EC67AED</td><td>No</td><td>1014</td><td>0x8000689E</td><td>0x000007E0</td></tr>
<tr><td>_city_bld_corner32x32A_ruined</td><td>0x3097A1C1</td><td>No</td><td>4601</td><td>0x80009F98</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_corner32x32B</td><td>0xCCBEF282</td><td>No</td><td>1017</td><td>0x800068A1</td><td>0x0000305E</td></tr>
<tr><td>_city_bld_corner32x32B_ruined</td><td>0x036E4AF8</td><td>No</td><td>4604</td><td>0x80009F9B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_corner32x32C</td><td>0xAEC101DF</td><td>No</td><td>1018</td><td>0x800068A2</td><td>0x00004F18</td></tr>
<tr><td>_city_bld_corner32x32C_ruined</td><td>0xB1B67E83</td><td>No</td><td>2479</td><td>0x800084D4</td><td>0x0000031B</td></tr>
<tr><td>_city_bld_corner32x32D</td><td>0x4CB9ABD4</td><td>No</td><td>1019</td><td>0x800068A3</td><td>0x0000558C</td></tr>
<tr><td>_city_bld_corner32x32D_ruined</td><td>0x0AAA78E2</td><td>No</td><td>4602</td><td>0x80009F99</td><td>0x0000714B</td></tr>
<tr><td>_city_bld_segment16x16A</td><td>0x348240B3</td><td>No</td><td>468</td><td>0x800056A6</td><td>0x00011F86</td></tr>
<tr><td>_city_bld_segment16x16A_ruined</td><td>0xE1E554B7</td><td>No</td><td>3572</td><td>0x800093D0</td><td>0x00001A8C</td></tr>
<tr><td>_city_bld_segment16x16b</td><td>0x5A84BB1C</td><td>No</td><td>649</td><td>0x80005F7D</td><td>0x0000E831</td></tr>
<tr><td>_city_bld_segment16x16b_ruined</td><td>0x0C88990A</td><td>No</td><td>3573</td><td>0x800093D1</td><td>0x0000F463</td></tr>
<tr><td>_city_bld_segment16x16c</td><td>0x5486F041</td><td>No</td><td>650</td><td>0x80005F7E</td><td>0x0000E4A7</td></tr>
<tr><td>_city_bld_segment16x16c_ruined</td><td>0x3F97A995</td><td>No</td><td>3574</td><td>0x800093D2</td><td>0x00011556</td></tr>
<tr><td>_city_bld_segment16x16d</td><td>0xBA89CF6A</td><td>No</td><td>651</td><td>0x80005F7F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_segment16x16d_ruined</td><td>0x0AD328E0</td><td>No</td><td>3575</td><td>0x800093D3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_segment16x32A</td><td>0x090BD135</td><td>No</td><td>783</td><td>0x80006229</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_segment16x32A_ruined</td><td>0x6536F149</td><td>No</td><td>3576</td><td>0x800093D4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_segment16x32B</td><td>0xE704DFEA</td><td>No</td><td>1105</td><td>0x80006B3F</td><td>0x00004F9D</td></tr>
<tr><td>_city_bld_segment16x32B_ruined</td><td>0x5BEA5660</td><td>No</td><td>3577</td><td>0x800093D5</td><td>0x0001303C</td></tr>
<tr><td>_city_bld_segment16x32C</td><td>0x09075407</td><td>No</td><td>784</td><td>0x8000622A</td><td>0x00007A2F</td></tr>
<tr><td>_city_bld_segment16x32C_ruined</td><td>0xB4ABBCCB</td><td>No</td><td>3578</td><td>0x800093D6</td><td>0x0000851F</td></tr>
<tr><td>_city_bld_segment16x32D</td><td>0x86FFCB9C</td><td>No</td><td>785</td><td>0x8000622B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_segment16x32D_ruined</td><td>0x5D9FC68A</td><td>No</td><td>3579</td><td>0x800093D7</td><td>0x0000A62A</td></tr>
<tr><td>_city_bld_segment32x32A</td><td>0x1FCE92CB</td><td>No</td><td>787</td><td>0x8000622D</td><td>0x00006309</td></tr>
<tr><td>_city_bld_segment32x32A_ruined</td><td>0x3978312F</td><td>No</td><td>4617</td><td>0x80009FAA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_segment32x32B</td><td>0x45D10D34</td><td>No</td><td>1106</td><td>0x80006B40</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_segment32x32B_ruined</td><td>0x84803CC2</td><td>No</td><td>4629</td><td>0x80009FB6</td><td>0x000026E0</td></tr>
<tr><td>_city_bld_segment32x32C</td><td>0x1FD30FF9</td><td>No</td><td>1116</td><td>0x80006B4A</td><td>0x0000255F</td></tr>
<tr><td>_city_bld_segment32x32D</td><td>0x45D58A62</td><td>No</td><td>1117</td><td>0x80006B4B</td><td>0x00008B48</td></tr>
<tr><td>_city_bld_segment32x32D_ruined</td><td>0x4A945A58</td><td>No</td><td>3580</td><td>0x800093D8</td><td>0x00009808</td></tr>
<tr><td>_city_bld_skyscraper01</td><td>0xB62E683B</td><td>No</td><td>1118</td><td>0x80006B4C</td><td>0x000099F6</td></tr>
<tr><td>_city_bld_skyscraper01_ruined</td><td>0x183D33DF</td><td>No</td><td>4606</td><td>0x80009F9D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_skyscraper02</td><td>0x9C307DE4</td><td>No</td><td>1121</td><td>0x80006B4F</td><td>0x00008933</td></tr>
<tr><td>_city_bld_skyscraper02_ruined</td><td>0x39E21CF2</td><td>No</td><td>4630</td><td>0x80009FB7</td><td>0x00003284</td></tr>
<tr><td>_city_bld_skyscraper03</td><td>0xB632E569</td><td>No</td><td>1120</td><td>0x80006B4E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_skyscraper03_ruined</td><td>0x7F06D37D</td><td>No</td><td>4626</td><td>0x80009FB3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_skyscraper04</td><td>0x1C35C492</td><td>No</td><td>1119</td><td>0x80006B4D</td><td>0x0000DD52</td></tr>
<tr><td>_city_bld_standalone01</td><td>0x936B0531</td><td>No</td><td>467</td><td>0x800056A5</td><td>0x0000A7BA</td></tr>
<tr><td>_city_bld_standalone01_ruined</td><td>0xAA781645</td><td>No</td><td>5253</td><td>0x8000A7AF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_standalone02</td><td>0x11637CC6</td><td>No</td><td>652</td><td>0x80005F80</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_standalone02_ruined</td><td>0x2D6397CC</td><td>No</td><td>5254</td><td>0x8000A7B0</td><td>0x0000F523</td></tr>
<tr><td>_city_bld_standalone03</td><td>0x3365F0E3</td><td>No</td><td>653</td><td>0x80005F81</td><td>0x0000679A</td></tr>
<tr><td>_city_bld_standalone03_ruined</td><td>0xA4F2BFE7</td><td>No</td><td>5255</td><td>0x8000A7B1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_standalone04</td><td>0xB171F030</td><td>No</td><td>654</td><td>0x80005F82</td><td>0x0000B37D</td></tr>
<tr><td>_city_bld_standalone04_ruined</td><td>0x8D322A9E</td><td>No</td><td>5256</td><td>0x8000A7B2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_standalone05</td><td>0x1B74D5A5</td><td>No</td><td>655</td><td>0x80005F83</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_standalone05_ruined</td><td>0x0E0BFC39</td><td>No</td><td>5257</td><td>0x8000A7B3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_storefrontA</td><td>0x73DA352E</td><td>No</td><td>1477</td><td>0x8000701C</td><td>0x00012985</td></tr>
<tr><td>_city_bld_storefrontB</td><td>0xD5E18B39</td><td>No</td><td>1478</td><td>0x8000701D</td><td>0x00002973</td></tr>
<tr><td>_city_bld_storefrontC</td><td>0xFBDF8874</td><td>No</td><td>1479</td><td>0x8000701E</td><td>0x00000A97</td></tr>
<tr><td>_city_bld_storefrontcornerA</td><td>0xF1D108FF</td><td>No</td><td>1386</td><td>0x80006EE8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_storefrontcornerB</td><td>0xE7D337D8</td><td>No</td><td>1051</td><td>0x80006927</td><td>0x000123E2</td></tr>
<tr><td>_city_bld_storefrontcornerC</td><td>0x11D5B88D</td><td>No</td><td>1466</td><td>0x80007011</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_storefrontcornerD</td><td>0x07C45FAE</td><td>No</td><td>1502</td><td>0x80007037</td><td>0xFFFFFFFF</td></tr>
<tr><td>_city_bld_storefrontcornerE</td><td>0x69C7388B</td><td>No</td><td>1539</td><td>0x8000718C</td><td>0x00000502</td></tr>
<tr><td>_city_bld_storefrontcornerF</td><td>0x8FC9B2F4</td><td>No</td><td>1511</td><td>0x8000716E</td><td>0x00013E72</td></tr>
<tr><td>_city_bld_storefrontD</td><td>0x5DE6DE7F</td><td>No</td><td>1480</td><td>0x8000701F</td><td>0x000057BE</td></tr>
<tr><td>_city_bld_storefrontE</td><td>0xFBE405A2</td><td>No</td><td>1500</td><td>0x80007035</td><td>0x00002A67</td></tr>
<tr><td>_city_bld_storefrontF</td><td>0x7DEB8E0D</td><td>No</td><td>1501</td><td>0x80007036</td><td>0x0000E89A</td></tr>
<tr><td>_city_busstop01</td><td>0x499A441F</td><td>No</td><td>3309</td><td>0x80008F79</td><td>0xFFFFFFFF</td></tr>
<tr><td>_civilian_chaira</td><td>0x6371A6AA</td><td>No</td><td>2534</td><td>0x80008560</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_clinic</td><td>0x8D8E3BFC</td><td>No</td><td>249</td><td>0x80004DBA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_corner16x16a</td><td>0x704116CC</td><td>No</td><td>365</td><td>0x80005100</td><td>0x00008C36</td></tr>
<tr><td>_commercial_bld_corner16x16a_ruined</td><td>0xD89B2E3A</td><td>No</td><td>3272</td><td>0x80008F49</td><td>0x0001034D</td></tr>
<tr><td>_commercial_bld_corner8x16a</td><td>0xD65F4757</td><td>No</td><td>253</td><td>0x80004DBE</td><td>0x0000B75E</td></tr>
<tr><td>_commercial_bld_corner8x16a_ruined</td><td>0x67F5B75B</td><td>No</td><td>3273</td><td>0x80008F4A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_corner8x16b</td><td>0xEC61A890</td><td>No</td><td>252</td><td>0x80004DBD</td><td>0x00000F9C</td></tr>
<tr><td>_commercial_bld_corner8x16b_ruined</td><td>0x630B76FE</td><td>No</td><td>3264</td><td>0x80008F41</td><td>0x00012699</td></tr>
<tr><td>_commercial_bld_corner8x16c</td><td>0xD663C485</td><td>No</td><td>255</td><td>0x80004DC0</td><td>0x00012036</td></tr>
<tr><td>_commercial_bld_corner8x16c_ruined</td><td>0xB9430D19</td><td>No</td><td>3289</td><td>0x80008F5B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_corner8x8a</td><td>0x0394938A</td><td>No</td><td>81</td><td>0x80004B39</td><td>0x0000951E</td></tr>
<tr><td>_commercial_bld_corner8x8a_ruined</td><td>0xCDF49980</td><td>No</td><td>3267</td><td>0x80008F44</td><td>0x00003BBD</td></tr>
<tr><td>_commercial_bld_corner8x8b</td><td>0xA59C4E55</td><td>No</td><td>254</td><td>0x80004DBF</td><td>0x0000CE45</td></tr>
<tr><td>_commercial_bld_corner8x8b_ruined</td><td>0xAC5AD069</td><td>No</td><td>3285</td><td>0x80008F56</td><td>0x0001359F</td></tr>
<tr><td>_commercial_bld_firestation</td><td>0x169D4A64</td><td>No</td><td>257</td><td>0x80004DC3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_policestation</td><td>0xB885803E</td><td>No</td><td>324</td><td>0x80004E16</td><td>0x0000DC0E</td></tr>
<tr><td>_commercial_bld_ruins16x16</td><td>0xCA77D281</td><td>No</td><td>5426</td><td>0x8000A9F3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_ruins16x24</td><td>0x016F76AE</td><td>No</td><td>5424</td><td>0x8000A9F1</td><td>0x00003428</td></tr>
<tr><td>_commercial_bld_ruins16x32</td><td>0xF80C16EF</td><td>No</td><td>5425</td><td>0x8000A9F2</td><td>0x00009A04</td></tr>
<tr><td>_commercial_bld_ruins8x24</td><td>0xF381B8AF</td><td>No</td><td>5428</td><td>0x8000A9F5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_ruins8x32</td><td>0x652AE0AA</td><td>No</td><td>5427</td><td>0x8000A9F4</td><td>0x0000C133</td></tr>
<tr><td>_commercial_bld_segment16x16a</td><td>0x22F4BCBC</td><td>No</td><td>364</td><td>0x800050FF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_segment16x16a_ruined</td><td>0x586AB1AA</td><td>No</td><td>3274</td><td>0x80008F4B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_segment8x16a</td><td>0xB1EDD787</td><td>No</td><td>245</td><td>0x80004DB6</td><td>0x00009F0E</td></tr>
<tr><td>_commercial_bld_segment8x16a_ruined</td><td>0xCF70AB4B</td><td>No</td><td>3288</td><td>0x80008F5A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_segment8x16b</td><td>0x87EFD400</td><td>No</td><td>277</td><td>0x80004DDD</td><td>0x0000E56E</td></tr>
<tr><td>_commercial_bld_segment8x16c</td><td>0xB1F254B5</td><td>No</td><td>123</td><td>0x80004CC5</td><td>0x0001109A</td></tr>
<tr><td>_commercial_bld_segment8x16c_ruined</td><td>0x7FFBDFC9</td><td>No</td><td>3268</td><td>0x80008F45</td><td>0x00008421</td></tr>
<tr><td>_commercial_bld_segment8x16d</td><td>0xA7E0FBD6</td><td>No</td><td>122</td><td>0x80004CC4</td><td>0x000030D8</td></tr>
<tr><td>_commercial_bld_segment8x16d_ruined</td><td>0xF54B745C</td><td>No</td><td>3287</td><td>0x80008F59</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_segment8x16e</td><td>0x09E3D4B3</td><td>No</td><td>126</td><td>0x80004CC8</td><td>0x00001DB9</td></tr>
<tr><td>_commercial_bld_segment8x16e_ruined</td><td>0x4DC170B7</td><td>No</td><td>3265</td><td>0x80008F42</td><td>0x000006BC</td></tr>
<tr><td>_commercial_bld_segment8x8a</td><td>0xDFFE58BA</td><td>No</td><td>251</td><td>0x80004DBC</td><td>0x0000C9A2</td></tr>
<tr><td>_commercial_bld_segment8x8a_ruined</td><td>0x1ECE2DB0</td><td>No</td><td>3266</td><td>0x80008F43</td><td>0x000024DB</td></tr>
<tr><td>_commercial_bld_segment8x8b</td><td>0x4205AEC5</td><td>No</td><td>134</td><td>0x80004CD1</td><td>0x0000CF21</td></tr>
<tr><td>_commercial_bld_segment8x8b_ruined</td><td>0x50FE2759</td><td>No</td><td>3284</td><td>0x80008F55</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_bld_segment8x8c</td><td>0x580392D0</td><td>No</td><td>82</td><td>0x80004B3A</td><td>0x00002364</td></tr>
<tr><td>_commercial_bld_segment8x8c_ruined</td><td>0xBE488E3E</td><td>No</td><td>3269</td><td>0x80008F46</td><td>0x000091AC</td></tr>
<tr><td>_commercial_bld_segment8x8d</td><td>0x59F6CA03</td><td>No</td><td>250</td><td>0x80004DBB</td><td>0x00004282</td></tr>
<tr><td>_commercial_bld_segment8x8d_ruined</td><td>0x7FC2D507</td><td>No</td><td>3270</td><td>0x80008F47</td><td>0x0000AA78</td></tr>
<tr><td>_commercial_bld_supermarket</td><td>0x75BE4579</td><td>No</td><td>323</td><td>0x80004E15</td><td>0x0000335F</td></tr>
<tr><td>_commercial_bld_supermarket_ruined</td><td>0xFAACC60D</td><td>No</td><td>3286</td><td>0x80008F58</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_lightclinic</td><td>0x54BDD1B3</td><td>No</td><td>1400</td><td>0x80006EF8</td><td>0x0000605C</td></tr>
<tr><td>_commercial_merge_concrete</td><td>0x13DC322B</td><td>No</td><td>686</td><td>0x80005FA4</td><td>0x00005B18</td></tr>
<tr><td>_commercial_mergeconcrete</td><td>0x05E91342</td><td>No</td><td>3551</td><td>0x800093B9</td><td>0x0000D47C</td></tr>
<tr><td>_commercial_road10</td><td>0x81A1B270</td><td>No</td><td>275</td><td>0x80004DDA</td><td>0x0000AB54</td></tr>
<tr><td>_commercial_road10Clean</td><td>0x7BEC3EA7</td><td>No</td><td>1858</td><td>0x800076E9</td><td>0x00004A67</td></tr>
<tr><td>_commercial_road10Cleancross</td><td>0xB9509A0D</td><td>No</td><td>1859</td><td>0x800076EA</td><td>0x0000236A</td></tr>
<tr><td>_commercial_road10CleanL</td><td>0x1A808871</td><td>No</td><td>1860</td><td>0x800076EB</td><td>0x0000440A</td></tr>
<tr><td>_commercial_road10CleanT</td><td>0x3A4490A9</td><td>No</td><td>1861</td><td>0x800076EC</td><td>0x000079E4</td></tr>
<tr><td>_commercial_road10CleanT20</td><td>0x1953C29B</td><td>No</td><td>1862</td><td>0x800076ED</td><td>0x00006259</td></tr>
<tr><td>_commercial_road10CleanT5</td><td>0x42DE3E8A</td><td>No</td><td>1863</td><td>0x800076EE</td><td>0x000083EF</td></tr>
<tr><td>_commercial_road10cross</td><td>0x6A6CA690</td><td>No</td><td>261</td><td>0x80004DCB</td><td>0x00005835</td></tr>
<tr><td>_commercial_road10cross5</td><td>0xCD077E75</td><td>No</td><td>263</td><td>0x80004DCD</td><td>0x000092E4</td></tr>
<tr><td>_commercial_road10l</td><td>0xCAFC0198</td><td>No</td><td>262</td><td>0x80004DCC</td><td>0x0000661E</td></tr>
<tr><td>_commercial_road10middle</td><td>0x3BE9E69F</td><td>No</td><td>1054</td><td>0x8000692A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_road10straight</td><td>0x240E67BA</td><td>No</td><td>3315</td><td>0x80008F7F</td><td>0x000112CC</td></tr>
<tr><td>_commercial_road10t</td><td>0xCAE879E0</td><td>No</td><td>260</td><td>0x80004DCA</td><td>0x00000C79</td></tr>
<tr><td>_commercial_road10t20</td><td>0xD6A80E46</td><td>No</td><td>1034</td><td>0x80006913</td><td>0x000125E7</td></tr>
<tr><td>_commercial_road10t5</td><td>0xC0447285</td><td>No</td><td>264</td><td>0x80004DCE</td><td>0x000112DD</td></tr>
<tr><td>_commercial_road10Transparent</td><td>0xB5FEE212</td><td>No</td><td>1738</td><td>0x800075B1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_road20</td><td>0x170A6BC1</td><td>No</td><td>274</td><td>0x80004DD8</td><td>0x000123BC</td></tr>
<tr><td>_commercial_road20b</td><td>0x2FB4F779</td><td>No</td><td>1059</td><td>0x8000692F</td><td>0x000072CA</td></tr>
<tr><td>_commercial_road20Clean</td><td>0x2401AAB0</td><td>No</td><td>1864</td><td>0x800076EF</td><td>0x0000EB4D</td></tr>
<tr><td>_commercial_road20Cleanb</td><td>0x29524986</td><td>No</td><td>1865</td><td>0x800076F0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_road20Cleancross</td><td>0x0637AED0</td><td>No</td><td>1866</td><td>0x800076F1</td><td>0x00006043</td></tr>
<tr><td>_commercial_road20CleanT</td><td>0xA9397B20</td><td>No</td><td>1867</td><td>0x800076F2</td><td>0x0000809F</td></tr>
<tr><td>_commercial_road20CleanT10</td><td>0xEBAE3E4B</td><td>No</td><td>1868</td><td>0x800076F3</td><td>0x00010B44</td></tr>
<tr><td>_commercial_road20cross</td><td>0xCEA0D127</td><td>No</td><td>270</td><td>0x80004DD4</td><td>0x00000720</td></tr>
<tr><td>_commercial_road20cross10</td><td>0xEEBF26A4</td><td>No</td><td>271</td><td>0x80004DD5</td><td>0x000051F5</td></tr>
<tr><td>_commercial_road20merge10</td><td>0x54D09630</td><td>No</td><td>353</td><td>0x80004EFD</td><td>0x000100EF</td></tr>
<tr><td>_commercial_road20t</td><td>0x5792A42F</td><td>No</td><td>272</td><td>0x80004DD6</td><td>0x00007F5B</td></tr>
<tr><td>_commercial_road20t10</td><td>0xCD4AED8C</td><td>No</td><td>273</td><td>0x80004DD7</td><td>0x00008AF9</td></tr>
<tr><td>_commercial_road20t10b</td><td>0x526909CA</td><td>No</td><td>3543</td><td>0x800093B1</td><td>0x0000795C</td></tr>
<tr><td>_commercial_road5</td><td>0xDA968AB0</td><td>No</td><td>269</td><td>0x80004DD3</td><td>0x00011235</td></tr>
<tr><td>_commercial_road5cross</td><td>0x83BE4ED0</td><td>No</td><td>265</td><td>0x80004DCF</td><td>0x00007E0F</td></tr>
<tr><td>_commercial_road5l</td><td>0x15A9A2D8</td><td>No</td><td>266</td><td>0x80004DD0</td><td>0x0000DB8E</td></tr>
<tr><td>_commercial_road5t</td><td>0x15961B20</td><td>No</td><td>267</td><td>0x80004DD1</td><td>0x0000F6BC</td></tr>
<tr><td>_commercial_road5t10</td><td>0xC1EBDE4B</td><td>No</td><td>268</td><td>0x80004DD2</td><td>0x0001179B</td></tr>
<tr><td>_commercial_roadgovnt</td><td>0xACAC7E4F</td><td>No</td><td>1727</td><td>0x800075A3</td><td>0x0000DCCD</td></tr>
<tr><td>_commercial_roadstraight10</td><td>0x00AAD096</td><td>No</td><td>3257</td><td>0x80008F36</td><td>0x000057C2</td></tr>
<tr><td>_commercial_roadstraight10_crater02</td><td>0x056DA31E</td><td>No</td><td>5260</td><td>0x8000A7B7</td><td>0x000113C7</td></tr>
<tr><td>_commercial_roadstraight10_crater02_straight</td><td>0xC5D81E3F</td><td>No</td><td>5272</td><td>0x8000A7C3</td><td>0x0000770C</td></tr>
<tr><td>_commercial_roadstraight10_crater_stitcher</td><td>0xD682416D</td><td>No</td><td>5259</td><td>0x8000A7B6</td><td>0x00001230</td></tr>
<tr><td>_commercial_roadstraight20</td><td>0xC95EFD5B</td><td>No</td><td>3313</td><td>0x80008F7D</td><td>0x00001D96</td></tr>
<tr><td>_commercial_roadstraight20_crater02</td><td>0x22C44025</td><td>No</td><td>4608</td><td>0x80009FA0</td><td>0x0000D4F3</td></tr>
<tr><td>_commercial_roadstraight20_crater02_straight</td><td>0x173398F6</td><td>No</td><td>5258</td><td>0x8000A7B5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_roadstraight20_crater_stitcher</td><td>0x674EAAA8</td><td>No</td><td>4607</td><td>0x80009F9F</td><td>0x0000201D</td></tr>
<tr><td>_commercial_roadstraight20b</td><td>0xD213D90B</td><td>No</td><td>3314</td><td>0x80008F7E</td><td>0x00002334</td></tr>
<tr><td>_commercial_roadstraight5</td><td>0x6245D0CA</td><td>No</td><td>3258</td><td>0x80008F37</td><td>0x0000651A</td></tr>
<tr><td>_commercial_sidewalk</td><td>0x447A6247</td><td>No</td><td>276</td><td>0x80004DDB</td><td>0x0001307E</td></tr>
<tr><td>_commercial_sidewalk02</td><td>0x259FE84D</td><td>No</td><td>5267</td><td>0x8000A7BE</td><td>0x0001122F</td></tr>
<tr><td>_commercial_sidewalkClean</td><td>0xFC8DB1F2</td><td>No</td><td>1869</td><td>0x800076F4</td><td>0x00000425</td></tr>
<tr><td>_commercial_sidewalkCleansmall</td><td>0x19260E7B</td><td>No</td><td>1870</td><td>0x800076F5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_sidewalksmall</td><td>0x138FB724</td><td>No</td><td>367</td><td>0x80005102</td><td>0x00006BD8</td></tr>
<tr><td>_commercial_tunnelcap</td><td>0x3E06D87D</td><td>No</td><td>1067</td><td>0x80006937</td><td>0x00008CAB</td></tr>
<tr><td>_commercial_tunnelsegment</td><td>0x87B99176</td><td>No</td><td>1068</td><td>0x80006939</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_wall</td><td>0xD08A375D</td><td>No</td><td>151</td><td>0x80004CE2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_commercial_wallbeachlong</td><td>0xDB4E6594</td><td>No</td><td>1233</td><td>0x80006CE5</td><td>0x00001152</td></tr>
<tr><td>_commercial_wallbeachshort</td><td>0xA5B485E0</td><td>No</td><td>1234</td><td>0x80006CE6</td><td>0x000091E1</td></tr>
<tr><td>_commercial_wallcorner</td><td>0x9997052E</td><td>No</td><td>179</td><td>0x80004D09</td><td>0x00005109</td></tr>
<tr><td>_commercial_wallcorner_pristine</td><td>0xC1FE8321</td><td>No</td><td>4189</td><td>0x80009C21</td><td>0x000097C5</td></tr>
<tr><td>_commercial_walllong</td><td>0x7C827A9B</td><td>No</td><td>180</td><td>0x80004D0A</td><td>0x00006392</td></tr>
<tr><td>_commercial_walllong_pristine</td><td>0x5811F9D2</td><td>No</td><td>4190</td><td>0x80009C22</td><td>0x000140B8</td></tr>
<tr><td>_commercial_wallshort</td><td>0xA8BE3C0D</td><td>No</td><td>181</td><td>0x80004D0B</td><td>0x00001A5F</td></tr>
<tr><td>_commercial_wallshort_pristine</td><td>0x62E0DD58</td><td>No</td><td>4191</td><td>0x80009C23</td><td>0xFFFFFFFF</td></tr>
<tr><td>_cumana_bld_corner16x16b</td><td>0x0494455A</td><td>No</td><td>4200</td><td>0x80009C2D</td><td>0x00005384</td></tr>
<tr><td>_cumana_bld_corner16x16c</td><td>0xE69654B7</td><td>No</td><td>4201</td><td>0x80009C2E</td><td>0x00010CD1</td></tr>
<tr><td>_cumana_bld_corner32x32B</td><td>0xB5C3AE6A</td><td>No</td><td>4203</td><td>0x80009C30</td><td>0xFFFFFFFF</td></tr>
<tr><td>_cumana_bld_fortress01</td><td>0x0F46E72E</td><td>No</td><td>6056</td><td>0x900001A8</td><td>0x00007121</td></tr>
<tr><td>_cumana_bld_hotelfourstar01</td><td>0xB69BFEAC</td><td>No</td><td>6057</td><td>0x900001A9</td><td>0x00007BAD</td></tr>
<tr><td>_cumana_bld_hotelfourstar01_ruined</td><td>0xD25D559A</td><td>No</td><td>4139</td><td>0x80009B3A</td><td>0x000070DD</td></tr>
<tr><td>_cumana_bld_hoteltwostar01</td><td>0x19669520</td><td>No</td><td>6058</td><td>0x900001AA</td><td>0x0000CE97</td></tr>
<tr><td>_cumana_bld_hoteltwostar01_ruined</td><td>0xEC057ACE</td><td>No</td><td>4138</td><td>0x80009B36</td><td>0x000128A0</td></tr>
<tr><td>_cumana_bld_segment16x16a</td><td>0xC932E0EB</td><td>No</td><td>5433</td><td>0x8000A9FB</td><td>0x00002A85</td></tr>
<tr><td>_cumana_bld_segment32x32D</td><td>0x5FE42C3A</td><td>No</td><td>4204</td><td>0x80009C32</td><td>0xFFFFFFFF</td></tr>
<tr><td>_cumana_bridge_end</td><td>0xBA7B9611</td><td>No</td><td>6096</td><td>0x900001D8</td><td>0x00003E0E</td></tr>
<tr><td>_cumana_bridge_midA</td><td>0x0EC8A1C5</td><td>No</td><td>6097</td><td>0x900001D9</td><td>0x00001445</td></tr>
<tr><td>_cumana_bridge_whiteend</td><td>0x10977A0C</td><td>No</td><td>6104</td><td>0x900001E0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_cumana_bridge_whitemid</td><td>0x6B2BBDB1</td><td>No</td><td>6103</td><td>0x900001DF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_DELETE ME</td><td>0x8030427D</td><td>No</td><td>28</td><td>0x8000437D</td><td>0x0000D849</td></tr>
<tr><td>_dlc_coro_bld_motorpool</td><td>0xD2BC640A</td><td>No</td><td>5262</td><td>0x8000A7B9</td><td>0x000090C5</td></tr>
<tr><td>_DLC_global_env_treemedium02</td><td>0xFBBCD0E5</td><td>No</td><td>5265</td><td>0x8000A7BC</td><td>0x00013926</td></tr>
<tr><td>_DLC_outskirt_road10</td><td>0x5C12EFA7</td><td>No</td><td>5263</td><td>0x8000A7BA</td><td>0x00012E71</td></tr>
<tr><td>_docks_bld_bar</td><td>0x0EA28FE1</td><td>No</td><td>256</td><td>0x80004DC2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_docks_bld_booth</td><td>0x327D909A</td><td>No</td><td>139</td><td>0x80004CD6</td><td>0x0001055D</td></tr>
<tr><td>_docks_bld_toolshed</td><td>0x2DE708EA</td><td>No</td><td>135</td><td>0x80004CD2</td><td>0x0000BE89</td></tr>
<tr><td>_docks_bld_toolshed_ruined</td><td>0xBF648960</td><td>No</td><td>5560</td><td>0x8000AB61</td><td>0x0000EB25</td></tr>
<tr><td>_docks_bld_warehouse</td><td>0xEC496AA7</td><td>No</td><td>258</td><td>0x80004DC4</td><td>0x00011055</td></tr>
<tr><td>_docks_bld_warehouse_ruined</td><td>0x482909EB</td><td>No</td><td>4612</td><td>0x80009FA4</td><td>0x0000B57C</td></tr>
<tr><td>_docks_bld_warehousesmall</td><td>0x625F3B84</td><td>No</td><td>244</td><td>0x80004DB5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_docks_bld_warehousesmall_ruined</td><td>0x4149FE12</td><td>No</td><td>4611</td><td>0x80009FA3</td><td>0x000055E4</td></tr>
<tr><td>_docks_crane</td><td>0x86CC17EA</td><td>No</td><td>182</td><td>0x80004D0C</td><td>0x0000A197</td></tr>
<tr><td>_docks_dockconcrete</td><td>0x062770FF</td><td>No</td><td>183</td><td>0x80004D0D</td><td>0x0000A36D</td></tr>
<tr><td>_docks_docklarge</td><td>0x4362A993</td><td>No</td><td>184</td><td>0x80004D0E</td><td>0x0000AA50</td></tr>
<tr><td>_docks_docklarge_ruin</td><td>0x695F2284</td><td>No</td><td>5558</td><td>0x8000AB5F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_docks_dockmini</td><td>0x28F9DCE3</td><td>No</td><td>185</td><td>0x80004D0F</td><td>0x0000AE9B</td></tr>
<tr><td>_docks_dockmini_ruined</td><td>0xF1CB23E7</td><td>No</td><td>5557</td><td>0x8000AB5E</td><td>0x000079BA</td></tr>
<tr><td>_docks_dockpump</td><td>0x070941AC</td><td>No</td><td>186</td><td>0x80004D10</td><td>0x0000A549</td></tr>
<tr><td>_docks_docksmall</td><td>0x25D4384B</td><td>No</td><td>187</td><td>0x80004D11</td><td>0x0000CB35</td></tr>
<tr><td>_docks_docksmall_ruined</td><td>0x1BFB75AF</td><td>No</td><td>5559</td><td>0x8000AB60</td><td>0x00006201</td></tr>
<tr><td>_docks_fishcage</td><td>0x7E4F04F1</td><td>No</td><td>199</td><td>0x80004D1D</td><td>0x0000212A</td></tr>
<tr><td>_docks_fishingpole</td><td>0xDDECDED9</td><td>No</td><td>200</td><td>0x80004D1E</td><td>0x00012F4B</td></tr>
<tr><td>_docks_lamppost</td><td>0x77DE8FD3</td><td>No</td><td>188</td><td>0x80004D12</td><td>0x0000DF12</td></tr>
<tr><td>_docks_net</td><td>0xEDCF6DFC</td><td>No</td><td>189</td><td>0x80004D13</td><td>0x0000E4C6</td></tr>
<tr><td>_docks_netbundled</td><td>0xFEBF31EC</td><td>No</td><td>191</td><td>0x80004D15</td><td>0x0000FE9C</td></tr>
<tr><td>_docks_netoverhang</td><td>0x2D661052</td><td>No</td><td>190</td><td>0x80004D14</td><td>0x0000E876</td></tr>
<tr><td>_docks_tiredock</td><td>0xF069B3C8</td><td>No</td><td>201</td><td>0x80004D20</td><td>0x00013570</td></tr>
<tr><td>_estate_benchstone01</td><td>0xB3067FAB</td><td>No</td><td>1885</td><td>0x80007706</td><td>0xFFFFFFFF</td></tr>
<tr><td>_estate_bld_mansion01</td><td>0x61C41F60</td><td>No</td><td>670</td><td>0x80005F94</td><td>0x00012581</td></tr>
<tr><td>_estate_bld_mansion01_partialRuin</td><td>0x8271FE7C</td><td>No</td><td>4027</td><td>0x80009A0F</td><td>0x0000FBFB</td></tr>
<tr><td>_estate_bld_mansion01_ruined</td><td>0x656C4F0E</td><td>No</td><td>4145</td><td>0x80009B48</td><td>0x00007376</td></tr>
<tr><td>_estate_bld_mansion02</td><td>0x0BC15967</td><td>No</td><td>618</td><td>0x80005C2B</td><td>0x0000C7BB</td></tr>
<tr><td>_estate_bld_mansion02_ruined</td><td>0xAD2FEBAB</td><td>No</td><td>4022</td><td>0x80009A08</td><td>0x0000E712</td></tr>
<tr><td>_estate_bld_mansion03</td><td>0xE9BEE54A</td><td>No</td><td>663</td><td>0x80005F8C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_estate_bld_mansion03_ruined</td><td>0x282F7440</td><td>No</td><td>4144</td><td>0x80009B47</td><td>0x0000C3AD</td></tr>
<tr><td>_estate_bld_mansion04</td><td>0x03BCCFA1</td><td>No</td><td>788</td><td>0x8000622F</td><td>0x00008A19</td></tr>
<tr><td>_estate_bld_mansion04_ruined</td><td>0x95352BF5</td><td>No</td><td>4152</td><td>0x80009B4F</td><td>0x0000D0BA</td></tr>
<tr><td>_estate_bld_poolelevated01</td><td>0x07F13467</td><td>No</td><td>1877</td><td>0x800076FD</td><td>0x000034AE</td></tr>
<tr><td>_Estate_bld_securityshed</td><td>0xE4E141EA</td><td>No</td><td>1886</td><td>0x80007707</td><td>0x000068B7</td></tr>
<tr><td>_estate_bld_tower01</td><td>0x3AA91B50</td><td>No</td><td>1753</td><td>0x800075C2</td><td>0x00011691</td></tr>
<tr><td>_estate_bld_tower02</td><td>0x24A6BA17</td><td>No</td><td>1752</td><td>0x800075C1</td><td>0x00008E96</td></tr>
<tr><td>_estate_sidewalk</td><td>0xF92280A5</td><td>No</td><td>1749</td><td>0x800075BE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_estate_sidewalksmall</td><td>0x6F49AB3A</td><td>No</td><td>1750</td><td>0x800075BF</td><td>0x0000A2E1</td></tr>
<tr><td>_estate_stairs01</td><td>0x4CD2F7B8</td><td>No</td><td>1746</td><td>0x800075BB</td><td>0x0000499B</td></tr>
<tr><td>_estate_stairs02</td><td>0xD6CFFF5F</td><td>No</td><td>1747</td><td>0x800075BC</td><td>0x0000ED7E</td></tr>
<tr><td>_estate_stairs03</td><td>0xF4CDF002</td><td>No</td><td>615</td><td>0x80005C28</td><td>0x00007D8C</td></tr>
<tr><td>_estate_stairscenter01</td><td>0x790C8DDF</td><td>No</td><td>1748</td><td>0x800075BD</td><td>0x00001355</td></tr>
<tr><td>_estate_wallgate01</td><td>0xF6B820F7</td><td>No</td><td>1874</td><td>0x800076FA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_estate_wallgate01_ruined</td><td>0x876EDBFB</td><td>No</td><td>2522</td><td>0x80008553</td><td>0xFFFFFFFF</td></tr>
<tr><td>_estate_walllong</td><td>0x0812E7D5</td><td>No</td><td>1875</td><td>0x800076FB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_estate_walllong_pristine</td><td>0x637B5630</td><td>No</td><td>4195</td><td>0x80009C27</td><td>0x000008D9</td></tr>
<tr><td>_estate_walllong_ruined</td><td>0xCD4D50E9</td><td>No</td><td>2106</td><td>0x8000817B</td><td>0x0000034F</td></tr>
<tr><td>_estate_wallpole</td><td>0x18BE0545</td><td>No</td><td>6071</td><td>0x900001B7</td><td>0x00011B5B</td></tr>
<tr><td>_estate_wallshort</td><td>0x8639A29B</td><td>No</td><td>1876</td><td>0x800076FC</td><td>0x00005AB6</td></tr>
<tr><td>_estate_wallshort_pristine</td><td>0x2EECF1D2</td><td>No</td><td>4196</td><td>0x80009C28</td><td>0x00004042</td></tr>
<tr><td>_fueltanks parent</td><td>0x6AF39AFD</td><td>Yes</td><td>4546</td><td>0x80009F1B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_acunita</td><td>0x51FE4E53</td><td>No</td><td>156</td><td>0x80004CE9</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_acunitb</td><td>0x7800C8BC</td><td>No</td><td>157</td><td>0x80004CEA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_antennaB</td><td>0x319CC265</td><td>No</td><td>2959</td><td>0x800089D2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_antennaD</td><td>0x498DDDA3</td><td>No</td><td>2960</td><td>0x800089D3</td><td>0x00004BE2</td></tr>
<tr><td>_global_att_chandelier</td><td>0x7319C1F9</td><td>No</td><td>6106</td><td>0x900001E2</td><td>0x00000DD0</td></tr>
<tr><td>_global_att_signlanemerge</td><td>0xFFE29107</td><td>No</td><td>1062</td><td>0x80006932</td><td>0x00008267</td></tr>
<tr><td>_global_att_signnouturn</td><td>0x554211D6</td><td>No</td><td>1064</td><td>0x80006934</td><td>0x000078F1</td></tr>
<tr><td>_global_att_signoneway</td><td>0x28B81A82</td><td>No</td><td>1935</td><td>0x80007DF8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_att_signspeed</td><td>0xC78ED160</td><td>No</td><td>1063</td><td>0x80006933</td><td>0x0000C385</td></tr>
<tr><td>_global_awninga</td><td>0xDEDB3C77</td><td>No</td><td>158</td><td>0x80004CEB</td><td>0x00007054</td></tr>
<tr><td>_global_bannera</td><td>0x5C049143</td><td>No</td><td>3991</td><td>0x80009988</td><td>0x00004592</td></tr>
<tr><td>_global_barbedwirelong</td><td>0x772B42C9</td><td>No</td><td>3291</td><td>0x80008F5E</td><td>0x0000E075</td></tr>
<tr><td>_global_barbedwireshort</td><td>0x5EE0CF37</td><td>No</td><td>3292</td><td>0x80008F5F</td><td>0x00011442</td></tr>
<tr><td>_global_barbell</td><td>0xCD2A1788</td><td>No</td><td>2651</td><td>0x8000862D</td><td>0x00011938</td></tr>
<tr><td>_global_barbequea</td><td>0x84BDA044</td><td>No</td><td>2684</td><td>0x800086DA</td><td>0x00012531</td></tr>
<tr><td>_global_barrela</td><td>0x65674451</td><td>No</td><td>159</td><td>0x80004CEC</td><td>0x00000F4C</td></tr>
<tr><td>_global_barrelb</td><td>0xE35FBBE6</td><td>No</td><td>160</td><td>0x80004CED</td><td>0x00008ED3</td></tr>
<tr><td>_global_barrelc</td><td>0x05623003</td><td>No</td><td>161</td><td>0x80004CEE</td><td>0x0000D545</td></tr>
<tr><td>_global_barrelmarketa</td><td>0x373DA789</td><td>No</td><td>419</td><td>0x800055C1</td><td>0x0000C148</td></tr>
<tr><td>_global_barrelmarketb</td><td>0x9535ECBE</td><td>No</td><td>421</td><td>0x800055C3</td><td>0x0000A107</td></tr>
<tr><td>_global_barrelmarketc</td><td>0xB73860DB</td><td>No</td><td>422</td><td>0x800055C4</td><td>0x000003AC</td></tr>
<tr><td>_global_barrelmarketd</td><td>0xB54529A8</td><td>No</td><td>420</td><td>0x800055C2</td><td>0x0000F04C</td></tr>
<tr><td>_global_barreloil</td><td>0xE87C70F0</td><td>No</td><td>6110</td><td>0x900001E8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_barrelorange</td><td>0xE59AF1EA</td><td>No</td><td>958</td><td>0x800065EC</td><td>0x00011651</td></tr>
<tr><td>_global_barricadea</td><td>0xD8154C52</td><td>No</td><td>959</td><td>0x800065ED</td><td>0x00012B96</td></tr>
<tr><td>_global_barricadeb</td><td>0x5A1CD4BD</td><td>No</td><td>960</td><td>0x800065EE</td><td>0x000110DD</td></tr>
<tr><td>_global_barricadec</td><td>0xF019EF48</td><td>No</td><td>961</td><td>0x800065EF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_barricaded</td><td>0x720DEFFB</td><td>No</td><td>962</td><td>0x800065F0</td><td>0x00000CC5</td></tr>
<tr><td>_global_barrierCornerOC</td><td>0x82D32C4C</td><td>No</td><td>2739</td><td>0x80008727</td><td>0x00000CCB</td></tr>
<tr><td>_global_barrierStraightOC</td><td>0xD9EEDD1D</td><td>No</td><td>2740</td><td>0x80008728</td><td>0x00002FC6</td></tr>
<tr><td>_global_bencha</td><td>0xD2CFA533</td><td>No</td><td>162</td><td>0x80004CEF</td><td>0x000090F2</td></tr>
<tr><td>_global_benchpark</td><td>0x4F058F0E</td><td>No</td><td>2957</td><td>0x800089CE</td><td>0x000070AF</td></tr>
<tr><td>_global_billboard01</td><td>0x59FBF0E4</td><td>No</td><td>2939</td><td>0x800089BA</td><td>0x0000B15A</td></tr>
<tr><td>_global_billboard02</td><td>0x73F9DB3B</td><td>No</td><td>2928</td><td>0x800089AF</td><td>0x0000D6EF</td></tr>
<tr><td>_global_billboard03</td><td>0x51F7671E</td><td>No</td><td>2940</td><td>0x800089BB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_billboard04</td><td>0x5C08BFFD</td><td>No</td><td>3310</td><td>0x80008F7A</td><td>0x0000BCED</td></tr>
<tr><td>_global_billboard05</td><td>0xF205DA88</td><td>No</td><td>4003</td><td>0x80009998</td><td>0x00008DEA</td></tr>
<tr><td>_global_billboard06</td><td>0xFC03ABAF</td><td>No</td><td>4004</td><td>0x80009999</td><td>0x00009FBF</td></tr>
<tr><td>_global_billboard_bridge01</td><td>0x2A426AAE</td><td>No</td><td>4005</td><td>0x8000999A</td><td>0x00009B2F</td></tr>
<tr><td>_global_billboard_roof01</td><td>0x55D77BE3</td><td>No</td><td>4006</td><td>0x8000999B</td><td>0x0000C274</td></tr>
<tr><td>_global_billboard_roof02</td><td>0x3BD9918C</td><td>No</td><td>4007</td><td>0x8000999C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_billboard_wall01</td><td>0x18124D9D</td><td>No</td><td>4008</td><td>0x8000999D</td><td>0x00000A4F</td></tr>
<tr><td>_global_billboard_wall02</td><td>0x960AC532</td><td>No</td><td>4009</td><td>0x8000999E</td><td>0x000095A1</td></tr>
<tr><td>_global_billboard_wall03</td><td>0xB80D394F</td><td>No</td><td>4010</td><td>0x8000999F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_billboard_wall04</td><td>0x96064804</td><td>No</td><td>4511</td><td>0x80009EF7</td><td>0x0000C567</td></tr>
<tr><td>_global_binnoculars</td><td>0x4EB00652</td><td>No</td><td>121</td><td>0x80004C32</td><td>0x0000E8E4</td></tr>
<tr><td>_global_bld_bunkersandbag</td><td>0x6801EDCA</td><td>No</td><td>2757</td><td>0x8000873A</td><td>0x0000BED5</td></tr>
<tr><td>_global_bld_loadingdockA</td><td>0xE461FEBB</td><td>No</td><td>3765</td><td>0x80009727</td><td>0x0000D4BB</td></tr>
<tr><td>_global_bld_loadingdockB</td><td>0xCA641464</td><td>No</td><td>3766</td><td>0x80009728</td><td>0x0000A892</td></tr>
<tr><td>_global_bld_officetrailerA</td><td>0x6C1B532F</td><td>No</td><td>2730</td><td>0x8000871D</td><td>0x0000707E</td></tr>
<tr><td>_global_bld_potty0</td><td>0xF1C85BA1</td><td>No</td><td>1846</td><td>0x800076DC</td><td>0x000115AC</td></tr>
<tr><td>_global_bld_tentmarket01</td><td>0xC3B0284B</td><td>No</td><td>423</td><td>0x800055C5</td><td>0x000057BD</td></tr>
<tr><td>_global_bld_tentmarket02</td><td>0xE9B2A2B4</td><td>No</td><td>424</td><td>0x800055C6</td><td>0x000085D1</td></tr>
<tr><td>_global_blueprints</td><td>0x96398108</td><td>No</td><td>4547</td><td>0x80009F1C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_bonfire01</td><td>0x20E6E498</td><td>No</td><td>1041</td><td>0x8000691A</td><td>0x00006EF0</td></tr>
<tr><td>_global_bookshelflargea</td><td>0x7D461273</td><td>No</td><td>921</td><td>0x800064C4</td><td>0x0000956F</td></tr>
<tr><td>_global_bookshelfsmalla</td><td>0x11E449AB</td><td>No</td><td>922</td><td>0x800064C5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_boxa</td><td>0xE649C320</td><td>No</td><td>328</td><td>0x80004E1A</td><td>0x000081A0</td></tr>
<tr><td>_global_boxb</td><td>0x9046FD27</td><td>No</td><td>163</td><td>0x80004CF0</td><td>0x0000904E</td></tr>
<tr><td>_global_boxb_lowhealth</td><td>0x5B9356AE</td><td>No</td><td>5531</td><td>0x8000AB41</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_boxc</td><td>0x6E44890A</td><td>No</td><td>329</td><td>0x80004E1B</td><td>0x00000349</td></tr>
<tr><td>_global_boxc_lowhealth</td><td>0xC5269137</td><td>No</td><td>5532</td><td>0x8000AB42</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_boxd</td><td>0x88427361</td><td>No</td><td>375</td><td>0x8000510B</td><td>0x0000A35B</td></tr>
<tr><td>_global_boxd OilCon020</td><td>0xFA0EBF27</td><td>No</td><td>4020</td><td>0x80009A06</td><td>0x00003307</td></tr>
<tr><td>_global_boxholes</td><td>0xA595A40C</td><td>No</td><td>4526</td><td>0x80009F06</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_boxholes_parrot</td><td>0x8C57434F</td><td>No</td><td>4843</td><td>0x8000A226</td><td>0x00012F1B</td></tr>
<tr><td>_global_brickpile01</td><td>0x096C35F6</td><td>No</td><td>2738</td><td>0x80008725</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_bridgepedestrian01</td><td>0xD437CFA1</td><td>No</td><td>1401</td><td>0x80006EF9</td><td>0x0000FE32</td></tr>
<tr><td>_global_bridgetransition</td><td>0xA2E766F2</td><td>No</td><td>6105</td><td>0x900001E1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_cartbrick</td><td>0x953479FD</td><td>No</td><td>2759</td><td>0x8000873D</td><td>0x0000315A</td></tr>
<tr><td>_global_centerdivider_long</td><td>0x8465B4DF</td><td>No</td><td>4774</td><td>0x8000A182</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_centerdivider_middle</td><td>0xBC0059F2</td><td>No</td><td>4775</td><td>0x8000A183</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_centerdivider_short</td><td>0xF04253B9</td><td>No</td><td>4776</td><td>0x8000A184</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_chaircafe</td><td>0x0AAB62C4</td><td>No</td><td>330</td><td>0x80004E1C</td><td>0x00009413</td></tr>
<tr><td>_global_chaircomputer</td><td>0x55B1F098</td><td>No</td><td>6111</td><td>0x900001E9</td><td>0x0000D1F6</td></tr>
<tr><td>_global_chairfolding</td><td>0xFE320A4E</td><td>No</td><td>6113</td><td>0x900001EB</td><td>0x00004F93</td></tr>
<tr><td>_global_chairwooda</td><td>0x73384441</td><td>No</td><td>164</td><td>0x80004CF1</td><td>0x000098E5</td></tr>
<tr><td>_global_chairwoodb</td><td>0xF130BBD6</td><td>No</td><td>332</td><td>0x80004E1F</td><td>0x0000AE84</td></tr>
<tr><td>_global_chairwoodc</td><td>0x533394B3</td><td>No</td><td>333</td><td>0x80004E20</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_chairwoodd</td><td>0xD13F9400</td><td>No</td><td>334</td><td>0x80004E21</td><td>0x000137EE</td></tr>
<tr><td>_global_chairwoode</td><td>0xFB4214B5</td><td>No</td><td>335</td><td>0x80004E22</td><td>0x00013AB4</td></tr>
<tr><td>_global_chairwoodf</td><td>0xD93B236A</td><td>No</td><td>336</td><td>0x80004E23</td><td>0x0000598F</td></tr>
<tr><td>_global_chairyarda</td><td>0x6348F534</td><td>No</td><td>337</td><td>0x80004E24</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_checkpointA</td><td>0x5BEED12F</td><td>No</td><td>1030</td><td>0x8000690E</td><td>0x0000180A</td></tr>
<tr><td>_global_chessset</td><td>0x0D3FD180</td><td>No</td><td>417</td><td>0x800055BE</td><td>0x00006ADE</td></tr>
<tr><td>_global_clothlineshort</td><td>0xD27A01C0</td><td>No</td><td>3994</td><td>0x8000998D</td><td>0x000129CC</td></tr>
<tr><td>_global_concretebarrier01</td><td>0x94CC289F</td><td>No</td><td>6108</td><td>0x900001E6</td><td>0x0001407F</td></tr>
<tr><td>_global_concretebarrier_vz</td><td>0xF99EFFBD</td><td>No</td><td>4751</td><td>0x8000A169</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_constructionpileC</td><td>0xF46E7E2A</td><td>No</td><td>3747</td><td>0x8000970F</td><td>0x00002391</td></tr>
<tr><td>_global_containertransplant</td><td>0x90FF58B8</td><td>No</td><td>4528</td><td>0x80009F08</td><td>0x0000BC08</td></tr>
<tr><td>_global_decal_puddle01</td><td>0x5D674767</td><td>No</td><td>426</td><td>0x800055C8</td><td>0x00013143</td></tr>
<tr><td>_global_decal_puddle02</td><td>0xB36A0D60</td><td>No</td><td>427</td><td>0x800055C9</td><td>0x00009CF9</td></tr>
<tr><td>_global_decal_puddle03</td><td>0xDD6C8E15</td><td>No</td><td>428</td><td>0x800055CA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_decal_puddle04</td><td>0xD35B3536</td><td>No</td><td>429</td><td>0x800055CB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_decal_puddle05</td><td>0xB55D4493</td><td>No</td><td>430</td><td>0x800055CC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_drinkingfountain</td><td>0x31B8E0AE</td><td>No</td><td>374</td><td>0x8000510A</td><td>0x000126D9</td></tr>
<tr><td>_global_dumpstergraylong</td><td>0x8CB07ACD</td><td>No</td><td>2701</td><td>0x800086F9</td><td>0x00005C92</td></tr>
<tr><td>_global_dumpstergreenshort</td><td>0x50A3FA37</td><td>No</td><td>2703</td><td>0x800086FE</td><td>0x00013BBC</td></tr>
<tr><td>_global_dumpstergreyshort</td><td>0x39E555C7</td><td>No</td><td>2702</td><td>0x800086FD</td><td>0x00007459</td></tr>
<tr><td>_global_electricalbox01</td><td>0x82BA5A04</td><td>No</td><td>373</td><td>0x80005108</td><td>0x000031D4</td></tr>
<tr><td>_global_electricalbox02</td><td>0x1CB77ADB</td><td>No</td><td>378</td><td>0x8000510F</td><td>0x00013FC0</td></tr>
<tr><td>_global_electricboxa</td><td>0xA9CF60A1</td><td>No</td><td>166</td><td>0x80004CF3</td><td>0x0000DFAA</td></tr>
<tr><td>_global_electronicboxA</td><td>0xA766B6E6</td><td>No</td><td>2958</td><td>0x800089D1</td><td>0x00001614</td></tr>
<tr><td>_global_emptyfruitbox</td><td>0xF9DD80DE</td><td>No</td><td>2685</td><td>0x800086DC</td><td>0x0000F33E</td></tr>
<tr><td>_global_env_bush01</td><td>0x48BDE593</td><td>No</td><td>923</td><td>0x800064C6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_bushlarge01</td><td>0x79E24672</td><td>No</td><td>1047</td><td>0x80006921</td><td>0x00007BBA</td></tr>
<tr><td>_global_env_bushlarge02</td><td>0xFBE9CEDD</td><td>No</td><td>1060</td><td>0x80006930</td><td>0x0000A923</td></tr>
<tr><td>_global_env_hedgecorner</td><td>0xB595EAB0</td><td>No</td><td>5443</td><td>0x8000AA49</td><td>0x0000BD6F</td></tr>
<tr><td>_global_env_hedgelong</td><td>0xD566029D</td><td>No</td><td>5437</td><td>0x8000AA42</td><td>0x00001664</td></tr>
<tr><td>_global_env_hedgelong01</td><td>0x012CB410</td><td>No</td><td>1744</td><td>0x800075B9</td><td>0x00002230</td></tr>
<tr><td>_global_env_hedgelong02</td><td>0xEB2A52D7</td><td>No</td><td>1755</td><td>0x800075C4</td><td>0x0001330E</td></tr>
<tr><td>_global_env_hedgelong03</td><td>0x892779FA</td><td>No</td><td>1884</td><td>0x80007705</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_hedgelong04</td><td>0x6324FF91</td><td>No</td><td>2012</td><td>0x800080BB</td><td>0x0000BB3E</td></tr>
<tr><td>_global_env_hedgelowcorner</td><td>0x514366D0</td><td>No</td><td>5444</td><td>0x8000AA4A</td><td>0x0000B006</td></tr>
<tr><td>_global_env_hedgelowlong</td><td>0x1EDE6EBD</td><td>No</td><td>5440</td><td>0x8000AA46</td><td>0x00000082</td></tr>
<tr><td>_global_env_hedgelowshort</td><td>0xD07C1F63</td><td>No</td><td>5441</td><td>0x8000AA47</td><td>0x000068C3</td></tr>
<tr><td>_global_env_hedgelowsquare</td><td>0x95B702EA</td><td>No</td><td>5442</td><td>0x8000AA48</td><td>0x0000ACAE</td></tr>
<tr><td>_global_env_hedgeshort</td><td>0xB5FA41C3</td><td>No</td><td>5439</td><td>0x8000AA44</td><td>0x00004C0C</td></tr>
<tr><td>_global_env_hedgeshort01</td><td>0x073EBCBE</td><td>No</td><td>1745</td><td>0x800075BA</td><td>0x00002E1B</td></tr>
<tr><td>_global_env_hedgesquare</td><td>0x3F954CCA</td><td>No</td><td>5438</td><td>0x8000AA43</td><td>0x00011EB2</td></tr>
<tr><td>_global_env_lawnuniversity01</td><td>0x934DDD13</td><td>No</td><td>146</td><td>0x80004CDD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_lawnuniversity02</td><td>0xB950577C</td><td>No</td><td>145</td><td>0x80004CDC</td><td>0x0000F866</td></tr>
<tr><td>_global_env_palmtree01</td><td>0x347C8A5D</td><td>No</td><td>235</td><td>0x80004DAC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_palmtreebend01</td><td>0x16DD7ED0</td><td>No</td><td>964</td><td>0x800065F2</td><td>0x000066CB</td></tr>
<tr><td>_global_env_palmtreebend02</td><td>0x00DB1D97</td><td>No</td><td>999</td><td>0x80006887</td><td>0x0000CDC3</td></tr>
<tr><td>_global_env_palmtreebend03</td><td>0x9ED844BA</td><td>No</td><td>998</td><td>0x80006886</td><td>0x0000AF9C</td></tr>
<tr><td>_global_env_palmtreebend04</td><td>0x78D5CA51</td><td>No</td><td>997</td><td>0x80006885</td><td>0x00009EE2</td></tr>
<tr><td>_global_env_palmtreebend05</td><td>0x7ED3952C</td><td>No</td><td>996</td><td>0x80006884</td><td>0x00001378</td></tr>
<tr><td>_global_env_palmtreeplanted01</td><td>0x077D6479</td><td>No</td><td>418</td><td>0x800055BF</td><td>0x0000AF17</td></tr>
<tr><td>_global_env_plantersidewalk01</td><td>0x151286A9</td><td>No</td><td>1056</td><td>0x8000692C</td><td>0x00000BB0</td></tr>
<tr><td>_global_env_rockjungle01</td><td>0x0856CCDD</td><td>No</td><td>5417</td><td>0x8000A9EA</td><td>0x0001071A</td></tr>
<tr><td>_global_env_rockjungle02</td><td>0x864F4472</td><td>No</td><td>5418</td><td>0x8000A9EB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_rockjungle03</td><td>0xA851B88F</td><td>No</td><td>5419</td><td>0x8000A9EC</td><td>0x00013863</td></tr>
<tr><td>_global_env_rockjungle04</td><td>0x864AC744</td><td>No</td><td>5420</td><td>0x8000A9ED</td><td>0x000072ED</td></tr>
<tr><td>_global_env_rockjungle05</td><td>0xA04D2EC9</td><td>No</td><td>5421</td><td>0x8000A9EE</td><td>0x0000E808</td></tr>
<tr><td>_global_env_rockjungle06</td><td>0xFE4573FE</td><td>No</td><td>5422</td><td>0x8000A9EF</td><td>0x00003C15</td></tr>
<tr><td>_global_env_rocksbeach01</td><td>0x672E6A22</td><td>No</td><td>1053</td><td>0x80006929</td><td>0x00002011</td></tr>
<tr><td>_global_env_rocksbeach02</td><td>0xE935F28D</td><td>No</td><td>1052</td><td>0x80006928</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_rocksbeach03</td><td>0xBF3371D8</td><td>No</td><td>1055</td><td>0x8000692B</td><td>0x000025BE</td></tr>
<tr><td>_global_env_rocksbeach04</td><td>0x4127728B</td><td>No</td><td>1058</td><td>0x8000692E</td><td>0x00002D62</td></tr>
<tr><td>_global_env_rocksbeach05</td><td>0xDF2499AE</td><td>No</td><td>1057</td><td>0x8000692D</td><td>0x00002BBC</td></tr>
<tr><td>_global_env_rocksbeach06</td><td>0x412BEFB9</td><td>No</td><td>1061</td><td>0x80006931</td><td>0x00001BBA</td></tr>
<tr><td>_global_env_rocksmall01</td><td>0x52AD1D89</td><td>No</td><td>361</td><td>0x800050F6</td><td>0x000132BA</td></tr>
<tr><td>_global_env_rocksmine01</td><td>0x710C425A</td><td>No</td><td>1699</td><td>0x8000753B</td><td>0x0000D593</td></tr>
<tr><td>_global_env_rocksmine02</td><td>0xD3139865</td><td>No</td><td>1700</td><td>0x8000753C</td><td>0x0000902D</td></tr>
<tr><td>_global_env_rocksmine03</td><td>0x6910B2F0</td><td>No</td><td>1701</td><td>0x8000753D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_rocksmine04</td><td>0xEB04B3A3</td><td>No</td><td>1702</td><td>0x8000753E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_rocksmine05</td><td>0xC9023F86</td><td>No</td><td>1703</td><td>0x8000753F</td><td>0x0000E347</td></tr>
<tr><td>_global_env_rocksmine06</td><td>0x4B09C7F1</td><td>No</td><td>1704</td><td>0x80007540</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_rocksmoss01</td><td>0xF4D9320D</td><td>No</td><td>2717</td><td>0x80008710</td><td>0x000055B0</td></tr>
<tr><td>_global_env_rocksmoss02</td><td>0x72D1A9A2</td><td>No</td><td>2718</td><td>0x80008711</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_rocksmoss03</td><td>0xD4D4827F</td><td>No</td><td>2719</td><td>0x80008712</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_rocksmoss04</td><td>0x72CD2C74</td><td>No</td><td>2720</td><td>0x80008713</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_rocksmoss05</td><td>0x4CCF2F39</td><td>No</td><td>2721</td><td>0x80008714</td><td>0x00013A43</td></tr>
<tr><td>_global_env_rocksmoss06</td><td>0xEAC7D92E</td><td>No</td><td>2722</td><td>0x80008715</td><td>0x00003500</td></tr>
<tr><td>_global_env_rocktall01</td><td>0xE9D7D2AB</td><td>No</td><td>360</td><td>0x800050F5</td><td>0x00011703</td></tr>
<tr><td>_global_env_scrub03</td><td>0x1A855392</td><td>No</td><td>1112</td><td>0x80006B46</td><td>0x00001CDF</td></tr>
<tr><td>_global_env_tree01</td><td>0x68ECDFDD</td><td>No</td><td>233</td><td>0x80004DAA</td><td>0x000083E1</td></tr>
<tr><td>_global_env_treeoak01</td><td>0xDB65DF8E</td><td>No</td><td>925</td><td>0x800064C8</td><td>0x00007453</td></tr>
<tr><td>_global_env_treeplaza01</td><td>0x485FF5CF</td><td>No</td><td>232</td><td>0x80004DA9</td><td>0x000056D2</td></tr>
<tr><td>_global_env_treeplaza02</td><td>0xBE62EE28</td><td>No</td><td>155</td><td>0x80004CE8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_treeplaza03</td><td>0xA8650A1D</td><td>No</td><td>234</td><td>0x80004DAB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_env_treesidewalk01</td><td>0xA574991F</td><td>No</td><td>3253</td><td>0x80008F2E</td><td>0x0000D8D9</td></tr>
<tr><td>_global_env_treespade</td><td>0x7F2E10EB</td><td>No</td><td>924</td><td>0x800064C7</td><td>0x00005C8E</td></tr>
<tr><td>_global_env_treetropical01</td><td>0xA6D01109</td><td>No</td><td>359</td><td>0x800050F4</td><td>0x00003C83</td></tr>
<tr><td>_global_env_treetropical02</td><td>0x04C8563E</td><td>No</td><td>3250</td><td>0x80008F2A</td><td>0x00011914</td></tr>
<tr><td>_global_explosivebarrel</td><td>0x134DB845</td><td>No</td><td>387</td><td>0x80005489</td><td>0x00012E63</td></tr>
<tr><td>_global_explosivebarrel_crashable</td><td>0x8D42D251</td><td>No</td><td>5759</td><td>0x8000AE09</td><td>0x00009480</td></tr>
<tr><td>_global_explosivebarrel_Long_Hibernation</td><td>0x08A2350E</td><td>No</td><td>5565</td><td>0x8000AB67</td><td>0x00009CC3</td></tr>
<tr><td>_global_fencebarbed</td><td>0x826FBFF3</td><td>No</td><td>676</td><td>0x80005F9A</td><td>0x000126E4</td></tr>
<tr><td>_global_fencebarbedpole</td><td>0x554EFF2D</td><td>No</td><td>675</td><td>0x80005F99</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_fencechain</td><td>0xACCADBF6</td><td>No</td><td>338</td><td>0x80004E25</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_fencechaingate</td><td>0x18AFECBF</td><td>No</td><td>339</td><td>0x80004E26</td><td>0x00006E65</td></tr>
<tr><td>_global_fencechainlong</td><td>0xF8AF5AE4</td><td>No</td><td>2686</td><td>0x800086DD</td><td>0x000105B5</td></tr>
<tr><td>_global_fencechainpole</td><td>0xE82A3150</td><td>No</td><td>347</td><td>0x80004EF5</td><td>0x0000D3F3</td></tr>
<tr><td>_global_fencechaintarped</td><td>0x5825F792</td><td>No</td><td>346</td><td>0x80004EF4</td><td>0x0000B7FB</td></tr>
<tr><td>_global_fencechaintemp</td><td>0x1FA5C33C</td><td>No</td><td>348</td><td>0x80004EF6</td><td>0x00011260</td></tr>
<tr><td>_global_fencewoodpanel</td><td>0xF51979AE</td><td>No</td><td>434</td><td>0x800055D0</td><td>0x00010B37</td></tr>
<tr><td>_global_files</td><td>0xE6A6AA7D</td><td>No</td><td>1294</td><td>0x80006D8E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_firehydrantred01</td><td>0x114ACD2A</td><td>No</td><td>677</td><td>0x80005F9B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_firehydrantred02</td><td>0x3351BE75</td><td>No</td><td>678</td><td>0x80005F9C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_firehydrantyellow01</td><td>0x14139CEB</td><td>No</td><td>679</td><td>0x80005F9D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_fireobject</td><td>0xA19AE91D</td><td>No</td><td>4000</td><td>0x80009995</td><td>0x00000D4F</td></tr>
<tr><td>_global_flag_largeAL</td><td>0xA8B51C6D</td><td>No</td><td>2710</td><td>0x80008708</td><td>0x00010ACE</td></tr>
<tr><td>_global_flag_largeCH</td><td>0xD962EBF3</td><td>No</td><td>2711</td><td>0x80008709</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_flag_largeGR</td><td>0x16535745</td><td>No</td><td>2712</td><td>0x8000870A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_flag_largeOC</td><td>0x2317E018</td><td>No</td><td>2713</td><td>0x8000870C</td><td>0x0000E464</td></tr>
<tr><td>_global_flag_largePR</td><td>0xEA0D185C</td><td>No</td><td>2714</td><td>0x8000870D</td><td>0x00010C78</td></tr>
<tr><td>_global_flag_largeVZ</td><td>0x6FA6FBCE</td><td>No</td><td>2715</td><td>0x8000870E</td><td>0x0000A4C4</td></tr>
<tr><td>_global_flag_smallAL</td><td>0xB4AF1DE5</td><td>No</td><td>2692</td><td>0x800086EF</td><td>0x00009FB7</td></tr>
<tr><td>_global_flag_smallCH</td><td>0x85AC082B</td><td>No</td><td>2693</td><td>0x800086F0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_flag_smallGR</td><td>0xE225E48D</td><td>No</td><td>2694</td><td>0x800086F1</td><td>0x00012398</td></tr>
<tr><td>_global_flag_smallOC</td><td>0x3F313E70</td><td>No</td><td>2695</td><td>0x800086F2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_flag_smallPR</td><td>0x1354A944</td><td>No</td><td>2696</td><td>0x800086F3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_flag_smallVZ</td><td>0x99159C26</td><td>No</td><td>3791</td><td>0x800097A7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_flag_wallAL</td><td>0x06D1156A</td><td>No</td><td>2731</td><td>0x8000871E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_flag_wallCH</td><td>0x57F5D8A0</td><td>No</td><td>2732</td><td>0x8000871F</td><td>0x0000EA69</td></tr>
<tr><td>_global_flag_wallGR</td><td>0x8A13221E</td><td>No</td><td>2733</td><td>0x80008720</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_flag_wallOC</td><td>0x754E8CB3</td><td>No</td><td>2734</td><td>0x80008721</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_flag_wallPR</td><td>0x3AEA52AB</td><td>No</td><td>2735</td><td>0x80008722</td><td>0x000041EC</td></tr>
<tr><td>_global_flarestick</td><td>0x8FBC1B40</td><td>No</td><td>4002</td><td>0x80009997</td><td>0x0000B30C</td></tr>
<tr><td>_global_fountainsmall</td><td>0xF60D28CD</td><td>No</td><td>1393</td><td>0x80006EEF</td><td>0x00006956</td></tr>
<tr><td>_global_fountainsmall_ruined</td><td>0x31A393A1</td><td>No</td><td>4154</td><td>0x80009B51</td><td>0x0000F1FD</td></tr>
<tr><td>_global_freewayelevatedcurve</td><td>0x63085A76</td><td>No</td><td>2026</td><td>0x800080C9</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_freewayelevatedlong</td><td>0x0F999C87</td><td>No</td><td>1878</td><td>0x800076FF</td><td>0x00008915</td></tr>
<tr><td>_global_freewayelevatedlongramp</td><td>0x2C58D32F</td><td>No</td><td>1883</td><td>0x80007704</td><td>0x00001658</td></tr>
<tr><td>_global_freewayelevatedonofframp</td><td>0x2AA8765D</td><td>No</td><td>2025</td><td>0x800080C8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_fruita</td><td>0x5B8FE753</td><td>No</td><td>919</td><td>0x800064C2</td><td>0x00008286</td></tr>
<tr><td>_global_fruitb</td><td>0x819261BC</td><td>No</td><td>920</td><td>0x800064C3</td><td>0x00000A27</td></tr>
<tr><td>_global_fruitboxa</td><td>0x7766DA9E</td><td>No</td><td>167</td><td>0x80004CF4</td><td>0x00003F61</td></tr>
<tr><td>_global_fruitboxb</td><td>0x996DCBE9</td><td>No</td><td>168</td><td>0x80004CF6</td><td>0x00000A7E</td></tr>
<tr><td>_global_fruitboxc</td><td>0x7F6B6464</td><td>No</td><td>917</td><td>0x800064C0</td><td>0x00012405</td></tr>
<tr><td>_global_fruitboxd</td><td>0x21731F2F</td><td>No</td><td>916</td><td>0x800064BF</td><td>0x0000C3D1</td></tr>
<tr><td>_global_fruitboxe</td><td>0xFF70AB12</td><td>No</td><td>915</td><td>0x800064BE</td><td>0x0000BF3C</td></tr>
<tr><td>_global_fruitboxf</td><td>0x8178337D</td><td>No</td><td>918</td><td>0x800064C1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_gateentrance</td><td>0x7E7F8603</td><td>No</td><td>4785</td><td>0x8000A18E</td><td>0x00003DF3</td></tr>
<tr><td>_global_gunboxA</td><td>0xD9BF6376</td><td>No</td><td>5499</td><td>0x8000AAB8</td><td>0x00012279</td></tr>
<tr><td>_global_heathaze</td><td>0xDCF17894</td><td>No</td><td>5199</td><td>0x8000A558</td><td>0x000124DA</td></tr>
<tr><td>_global_intercomA</td><td>0x2C8FF4C2</td><td>No</td><td>4765</td><td>0x8000A178</td><td>0x000130BD</td></tr>
<tr><td>_global_intercomA (Invincible)</td><td>0xC8FC312A</td><td>No</td><td>5754</td><td>0x8000ADA4</td><td>0x0000F4C9</td></tr>
<tr><td>_global_jugs01</td><td>0x723D6C1C</td><td>No</td><td>4527</td><td>0x80009F07</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_junkpile01</td><td>0x0B4FA30B</td><td>No</td><td>441</td><td>0x800055DD</td><td>0x000120EF</td></tr>
<tr><td>_global_junkpile02</td><td>0x31521D74</td><td>No</td><td>442</td><td>0x800055DE</td><td>0x00011676</td></tr>
<tr><td>_global_junkpile03</td><td>0x0B542039</td><td>No</td><td>586</td><td>0x80005C04</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_junkpile04</td><td>0x31569AA2</td><td>No</td><td>585</td><td>0x80005C03</td><td>0x000098AF</td></tr>
<tr><td>_global_ladderdockmedium01</td><td>0xDE7B8271</td><td>No</td><td>4736</td><td>0x8000A158</td><td>0x0000F753</td></tr>
<tr><td>_global_ladderdocksmall01</td><td>0x82980827</td><td>No</td><td>4530</td><td>0x80009F0B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_lampcablea</td><td>0x0663672A</td><td>No</td><td>169</td><td>0x80004CF7</td><td>0x0000481F</td></tr>
<tr><td>_global_lamppostA</td><td>0x1380D52D</td><td>No</td><td>1534</td><td>0x80007185</td><td>0x0000E9D7</td></tr>
<tr><td>_global_lamppostB</td><td>0x91794CC2</td><td>No</td><td>1535</td><td>0x80007186</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_lamppostmilitary</td><td>0x511ED675</td><td>No</td><td>4786</td><td>0x8000A18F</td><td>0x0000141E</td></tr>
<tr><td>_global_landingpad</td><td>0x80EA4188</td><td>No</td><td>3996</td><td>0x8000998F</td><td>0x0000F354</td></tr>
<tr><td>_global_liftauto</td><td>0xC0D7BC8E</td><td>No</td><td>6112</td><td>0x900001EA</td><td>0x000089A6</td></tr>
<tr><td>_global_locker</td><td>0x2AA683EC</td><td>No</td><td>911</td><td>0x800064B9</td><td>0x0000D51C</td></tr>
<tr><td>_global_market01</td><td>0x0CE95815</td><td>No</td><td>2736</td><td>0x80008723</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_market02</td><td>0x6AE19D4A</td><td>No</td><td>2737</td><td>0x80008724</td><td>0x000110E3</td></tr>
<tr><td>_global_newspaperbin01</td><td>0xB8974AF5</td><td>No</td><td>680</td><td>0x80005F9E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_newspaperbin02</td><td>0x969059AA</td><td>No</td><td>681</td><td>0x80005F9F</td><td>0x0000A212</td></tr>
<tr><td>_global_newspaperstand01</td><td>0x6038DD9A</td><td>No</td><td>584</td><td>0x80005C02</td><td>0x0001376D</td></tr>
<tr><td>_global_pallet</td><td>0x70CD95C2</td><td>No</td><td>435</td><td>0x800055D1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_palletcement</td><td>0x56727392</td><td>No</td><td>436</td><td>0x800055D2</td><td>0x0000ED56</td></tr>
<tr><td>_global_paperA</td><td>0xC801CA6F</td><td>No</td><td>4852</td><td>0x8000A23B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_parkinglota</td><td>0x7D2DEB82</td><td>No</td><td>352</td><td>0x80004EFC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_parkinglotb</td><td>0xFF3573ED</td><td>No</td><td>2046</td><td>0x800080E0</td><td>0x000100AB</td></tr>
<tr><td>_global_phone1A</td><td>0x3DD6A3E6</td><td>No</td><td>1871</td><td>0x800076F6</td><td>0x000099F8</td></tr>
<tr><td>_global_phoneAhandset</td><td>0xD020AF12</td><td>No</td><td>1872</td><td>0x800076F7</td><td>0x0000578D</td></tr>
<tr><td>_global_pile01</td><td>0xFF908CCD</td><td>No</td><td>2922</td><td>0x800089A7</td><td>0x00012A5A</td></tr>
<tr><td>_global_pile02</td><td>0x7D890462</td><td>No</td><td>2923</td><td>0x800089A8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_pile03</td><td>0xDF8BDD3F</td><td>No</td><td>2924</td><td>0x800089A9</td><td>0x00000F3F</td></tr>
<tr><td>_global_pile04</td><td>0x7D848734</td><td>No</td><td>2925</td><td>0x800089AA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_pile05</td><td>0x578689F9</td><td>No</td><td>2926</td><td>0x800089AB</td><td>0x00007504</td></tr>
<tr><td>_global_pile06</td><td>0xF57F33EE</td><td>No</td><td>2927</td><td>0x800089AC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_pile07</td><td>0x57820CCB</td><td>No</td><td>3260</td><td>0x80008F3B</td><td>0x0000D824</td></tr>
<tr><td>_global_pipeunderground</td><td>0x5B8571C3</td><td>No</td><td>3563</td><td>0x800093C6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_platform01</td><td>0xE233FB3C</td><td>No</td><td>5406</td><td>0x8000A9DF</td><td>0x0000909D</td></tr>
<tr><td>_global_playgroundride01</td><td>0xA768D6C8</td><td>No</td><td>1239</td><td>0x80006CEE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_playgroundride02</td><td>0xB166A7EF</td><td>No</td><td>1238</td><td>0x80006CED</td><td>0x00011E1E</td></tr>
<tr><td>_global_playgroundride03</td><td>0x8F6433D2</td><td>No</td><td>1237</td><td>0x80006CEC</td><td>0x0000D9E7</td></tr>
<tr><td>_global_pole</td><td>0xE3CE6D3E</td><td>No</td><td>3995</td><td>0x8000998E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_portablelight</td><td>0x96279A17</td><td>No</td><td>2072</td><td>0x80008140</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_prisonpen</td><td>0xE5659BE6</td><td>No</td><td>3997</td><td>0x80009992</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_propanecannistera</td><td>0x9635E555</td><td>No</td><td>2619</td><td>0x80008604</td><td>0x0000E302</td></tr>
<tr><td>_Global_propanetanklargeA</td><td>0x78F605A5</td><td>Yes</td><td>587</td><td>0x80005C05</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_propanetanklargeB</td><td>0x16EEAF9A</td><td>Yes</td><td>2622</td><td>0x80008607</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Global_propanetanksmallA</td><td>0x31F47FC9</td><td>Yes</td><td>580</td><td>0x80005BFE</td><td>0x0001204C</td></tr>
<tr><td>_global_protestsigna</td><td>0xFF69CD8B</td><td>No</td><td>914</td><td>0x800064BD</td><td>0x0000B595</td></tr>
<tr><td>_global_pylon</td><td>0xC30AABEC</td><td>No</td><td>2826</td><td>0x80008784</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_racearrow</td><td>0xF3EF35D2</td><td>No</td><td>3987</td><td>0x80009984</td><td>0x00002ED1</td></tr>
<tr><td>_global_racecheckpoint</td><td>0x64D6F3F5</td><td>No</td><td>3988</td><td>0x80009985</td><td>0x00005C07</td></tr>
<tr><td>_global_racefinish</td><td>0x80A127A6</td><td>No</td><td>3990</td><td>0x80009987</td><td>0x0000B01D</td></tr>
<tr><td>_global_racering</td><td>0xF6DA1881</td><td>No</td><td>3989</td><td>0x80009986</td><td>0x00013647</td></tr>
<tr><td>_global_radioA</td><td>0x371216DE</td><td>No</td><td>3307</td><td>0x80008F77</td><td>0x000094F0</td></tr>
<tr><td>_global_rail01</td><td>0xCC2EF3B9</td><td>No</td><td>440</td><td>0x800055DA</td><td>0x00008474</td></tr>
<tr><td>_global_railend01</td><td>0x3CE88F26</td><td>No</td><td>444</td><td>0x800055E7</td><td>0x0000209C</td></tr>
<tr><td>_global_railend02</td><td>0xBEF01791</td><td>No</td><td>445</td><td>0x800055EA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_raillong</td><td>0xEBB2DE0E</td><td>No</td><td>3263</td><td>0x80008F40</td><td>0x00007A56</td></tr>
<tr><td>_global_railsmall</td><td>0x4F2A34BD</td><td>No</td><td>3262</td><td>0x80008F3F</td><td>0x0001298B</td></tr>
<tr><td>_global_ramp_roadlessrider</td><td>0x2769DAFA</td><td>No</td><td>4752</td><td>0x8000A16B</td><td>0x0000196C</td></tr>
<tr><td>_global_redoxytank</td><td>0xF0446A31</td><td>Yes</td><td>2620</td><td>0x80008605</td><td>0x0001160E</td></tr>
<tr><td>_global_road_parking</td><td>0x305066EF</td><td>No</td><td>3316</td><td>0x80008F80</td><td>0x00000508</td></tr>
<tr><td>_global_sandbagscornerAN</td><td>0x31AB4695</td><td>No</td><td>2742</td><td>0x8000872A</td><td>0x00009353</td></tr>
<tr><td>_global_sandbagscornerCH</td><td>0x30E42AB9</td><td>No</td><td>2741</td><td>0x80008729</td><td>0x000066D1</td></tr>
<tr><td>_global_sandbagscornerGR</td><td>0xED5410DF</td><td>No</td><td>2743</td><td>0x8000872B</td><td>0x00009F86</td></tr>
<tr><td>_global_sandbagscornerPR</td><td>0xD5E5F96A</td><td>No</td><td>2744</td><td>0x8000872C</td><td>0x0000B29A</td></tr>
<tr><td>_global_sandbagscornerVZ</td><td>0xC6E31610</td><td>No</td><td>2745</td><td>0x8000872D</td><td>0x0000B4C5</td></tr>
<tr><td>_global_sandbagscurveda</td><td>0xBB548E31</td><td>No</td><td>377</td><td>0x8000510E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_sandbagscurvedB</td><td>0x394D05C6</td><td>No</td><td>2913</td><td>0x8000899D</td><td>0x0000CD0E</td></tr>
<tr><td>_global_sandbagsendAN</td><td>0x070402EF</td><td>No</td><td>2746</td><td>0x8000872E</td><td>0x0000F799</td></tr>
<tr><td>_global_sandbagsendCH</td><td>0xD8551C43</td><td>No</td><td>2747</td><td>0x8000872F</td><td>0x00010903</td></tr>
<tr><td>_global_sandbagsendGR</td><td>0x94F69F35</td><td>No</td><td>2748</td><td>0x80008730</td><td>0x00013248</td></tr>
<tr><td>_global_sandbagsendPR</td><td>0xC62563EC</td><td>No</td><td>2749</td><td>0x80008732</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_sandbagsendVZ</td><td>0x4BBF475E</td><td>No</td><td>2750</td><td>0x80008733</td><td>0x0000A8BE</td></tr>
<tr><td>_global_sandbagsstraighta</td><td>0xF902B6F6</td><td>No</td><td>376</td><td>0x8000510D</td><td>0x00010835</td></tr>
<tr><td>_global_sandbagsstraightAN</td><td>0x32B19078</td><td>No</td><td>2751</td><td>0x80008734</td><td>0x00008BB3</td></tr>
<tr><td>_global_sandbagsstraightCH</td><td>0x0BD11998</td><td>No</td><td>2752</td><td>0x80008735</td><td>0x0000E96D</td></tr>
<tr><td>_global_sandbagsstraightGR</td><td>0xC040F326</td><td>No</td><td>2753</td><td>0x80008736</td><td>0x00010F0A</td></tr>
<tr><td>_global_sandbagsstraightPR</td><td>0xF118ED33</td><td>No</td><td>2754</td><td>0x80008737</td><td>0x0000ABFB</td></tr>
<tr><td>_global_sandbagsstraightthinCH</td><td>0x1028601D</td><td>No</td><td>4773</td><td>0x8000A181</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_sandbagsstraightVZ</td><td>0xA6C6A3ED</td><td>No</td><td>2755</td><td>0x80008738</td><td>0x000106C0</td></tr>
<tr><td>_global_satellitedishB</td><td>0xB6FE4907</td><td>No</td><td>2961</td><td>0x800089D4</td><td>0x00000067</td></tr>
<tr><td>_global_satellitedishC</td><td>0x94FBD4EA</td><td>No</td><td>2962</td><td>0x800089D5</td><td>0x00006EAB</td></tr>
<tr><td>_global_scaffold</td><td>0x574B85A2</td><td>No</td><td>3744</td><td>0x80009683</td><td>0x00012828</td></tr>
<tr><td>_global_scaffoldB</td><td>0x94958970</td><td>No</td><td>3745</td><td>0x80009684</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_scaffoldC</td><td>0xFE986EE5</td><td>No</td><td>3746</td><td>0x80009685</td><td>0x000086B6</td></tr>
<tr><td>_global_searchlighta</td><td>0x1C87FDA5</td><td>No</td><td>170</td><td>0x80004CF8</td><td>0x000064E8</td></tr>
<tr><td>_global_shoppingcartgreen</td><td>0xA52067FF</td><td>No</td><td>682</td><td>0x80005FA0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_sign_freeway</td><td>0xC96B930D</td><td>No</td><td>3771</td><td>0x8000972D</td><td>0x00000C16</td></tr>
<tr><td>_global_sign_road</td><td>0xA489AC9C</td><td>No</td><td>3772</td><td>0x8000972E</td><td>0x000009D0</td></tr>
<tr><td>_global_sign_road02</td><td>0x8E5D7DC6</td><td>No</td><td>3986</td><td>0x80009983</td><td>0x00011ECB</td></tr>
<tr><td>_global_signBar</td><td>0x212D279E</td><td>No</td><td>1857</td><td>0x800076E8</td><td>0x000028FF</td></tr>
<tr><td>_global_signcokea</td><td>0x0CFA647E</td><td>No</td><td>171</td><td>0x80004CF9</td><td>0x00001EFB</td></tr>
<tr><td>_global_signlanemerge</td><td>0xBA2C6ED7</td><td>No</td><td>4963</td><td>0x8000A38A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_signnouturn</td><td>0xD017AC86</td><td>No</td><td>4962</td><td>0x8000A389</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_signonewayleft</td><td>0x3A607295</td><td>No</td><td>6043</td><td>0x9000019B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_signspeed</td><td>0xDE7C9F10</td><td>No</td><td>4964</td><td>0x8000A38B</td><td>0x0000CB7D</td></tr>
<tr><td>_global_signstopa</td><td>0x626AC5A8</td><td>No</td><td>643</td><td>0x80005C4B</td><td>0x00012656</td></tr>
<tr><td>_global_signtaco</td><td>0x9B5C90E8</td><td>No</td><td>172</td><td>0x80004CFA</td><td>0x000091F5</td></tr>
<tr><td>_global_soccerball</td><td>0x2C83C3BA</td><td>No</td><td>913</td><td>0x800064BC</td><td>0x000025E8</td></tr>
<tr><td>_global_soccergoal</td><td>0x5F51F944</td><td>No</td><td>2050</td><td>0x80008120</td><td>0x0000C1AF</td></tr>
<tr><td>_global_spotlight</td><td>0x52D68644</td><td>No</td><td>5498</td><td>0x8000AAB7</td><td>0x000054F7</td></tr>
<tr><td>_global_stain01</td><td>0x87B54AA6</td><td>No</td><td>4514</td><td>0x80009EFA</td><td>0x000110E9</td></tr>
<tr><td>_global_stain02</td><td>0x09BCD311</td><td>No</td><td>4515</td><td>0x80009EFB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_stain03</td><td>0x0FBA9DEC</td><td>No</td><td>4516</td><td>0x80009EFC</td><td>0x00000CD1</td></tr>
<tr><td>_global_stain04</td><td>0x91C22657</td><td>No</td><td>4517</td><td>0x80009EFD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_stain05</td><td>0x2FBF4D7A</td><td>No</td><td>4518</td><td>0x80009EFE</td><td>0x0000B4C8</td></tr>
<tr><td>_global_stain06</td><td>0x91C6A385</td><td>No</td><td>4519</td><td>0x80009EFF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_stain07</td><td>0xA7C48790</td><td>No</td><td>4520</td><td>0x80009F00</td><td>0x000120E1</td></tr>
<tr><td>_global_stain08</td><td>0x89A404AB</td><td>No</td><td>4521</td><td>0x80009F01</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_stairsidewalk01</td><td>0x03CFC9A8</td><td>No</td><td>354</td><td>0x80004EFE</td><td>0x00004E13</td></tr>
<tr><td>_global_stairsidewalk02</td><td>0x8DCCD14F</td><td>No</td><td>622</td><td>0x80005C33</td><td>0x0000B045</td></tr>
<tr><td>_global_tablea</td><td>0x842866DD</td><td>No</td><td>165</td><td>0x80004CF2</td><td>0x0000DA5A</td></tr>
<tr><td>_global_tableb</td><td>0x0220DE72</td><td>No</td><td>173</td><td>0x80004CFB</td><td>0x00001B30</td></tr>
<tr><td>_global_tablecafe</td><td>0x905BA26B</td><td>No</td><td>331</td><td>0x80004E1D</td><td>0x0000A51D</td></tr>
<tr><td>_global_tablechess</td><td>0x93F543FC</td><td>No</td><td>416</td><td>0x800055BD</td><td>0x0000344F</td></tr>
<tr><td>_global_tablefolding</td><td>0xAE0AB043</td><td>No</td><td>5407</td><td>0x8000A9E0</td><td>0x00009FF7</td></tr>
<tr><td>_global_tablemarket</td><td>0x6288B184</td><td>No</td><td>912</td><td>0x800064BB</td><td>0x00000D27</td></tr>
<tr><td>_global_tableyarda</td><td>0x8B7C8BF9</td><td>No</td><td>349</td><td>0x80004EF8</td><td>0x000114C7</td></tr>
<tr><td>_global_tanktrap01</td><td>0x12DB78E4</td><td>Yes</td><td>6109</td><td>0x900001E7</td><td>0x00009619</td></tr>
<tr><td>_global_telephonebooth</td><td>0x6AD84718</td><td>No</td><td>350</td><td>0x80004EF9</td><td>0x000129F9</td></tr>
<tr><td>_global_tirelargea</td><td>0xA39928B4</td><td>No</td><td>174</td><td>0x80004CFC</td><td>0x00009F4E</td></tr>
<tr><td>_global_tiresmalla</td><td>0x2CB9FDDC</td><td>No</td><td>175</td><td>0x80004CFD</td><td>0x0000453E</td></tr>
<tr><td>_global_toolboxa</td><td>0x670CCC62</td><td>No</td><td>176</td><td>0x80004CFE</td><td>0x0000A14A</td></tr>
<tr><td>_global_toolboxb</td><td>0xE91454CD</td><td>No</td><td>177</td><td>0x80004CFF</td><td>0x00001924</td></tr>
<tr><td>_global_torchlamp</td><td>0x41DEB854</td><td>No</td><td>4001</td><td>0x80009996</td><td>0x00002603</td></tr>
<tr><td>_global_towerelectrical01</td><td>0x54D169AC</td><td>No</td><td>683</td><td>0x80005FA1</td><td>0x00000BE7</td></tr>
<tr><td>_global_towerlift</td><td>0x3722E4F0</td><td>No</td><td>684</td><td>0x80005FA2</td><td>0x000046E8</td></tr>
<tr><td>_global_towerliftend</td><td>0xB1937297</td><td>No</td><td>685</td><td>0x80005FA3</td><td>0x00001E6D</td></tr>
<tr><td>_global_trafficlight01</td><td>0x54BF448C</td><td>No</td><td>449</td><td>0x800055F1</td><td>0x0000B5A4</td></tr>
<tr><td>_global_trafficlight02</td><td>0x6EBD2EE3</td><td>No</td><td>579</td><td>0x80005BFD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_trafficpath</td><td>0x73C57156</td><td>No</td><td>3293</td><td>0x80008F64</td><td>0x0001238A</td></tr>
<tr><td>_global_trafficpathIntersection</td><td>0xE2BAE2A5</td><td>No</td><td>3294</td><td>0x80008F67</td><td>0x0000F0C6</td></tr>
<tr><td>_global_trashbag01</td><td>0x5D079001</td><td>No</td><td>578</td><td>0x80005BFC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_trashcan02</td><td>0x5FAD147A</td><td>No</td><td>2955</td><td>0x800089CC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_trashcana</td><td>0xA4CF9C81</td><td>No</td><td>178</td><td>0x80004D00</td><td>0x00003B90</td></tr>
<tr><td>_global_trashpile01</td><td>0x0669F143</td><td>No</td><td>610</td><td>0x80005C20</td><td>0x0000F1F1</td></tr>
<tr><td>_global_trashpile02</td><td>0x6C6CD06C</td><td>No</td><td>611</td><td>0x80005C21</td><td>0x0000FEEB</td></tr>
<tr><td>_global_trashpile03</td><td>0x666F0591</td><td>No</td><td>609</td><td>0x80005C1F</td><td>0x0000E3BF</td></tr>
<tr><td>_global_treasures</td><td>0x24C69082</td><td>No</td><td>4548</td><td>0x80009F1D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_vault</td><td>0x2D73145C</td><td>No</td><td>2707</td><td>0x80008705</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_vendingmachine01</td><td>0x06C8278F</td><td>No</td><td>910</td><td>0x800064B8</td><td>0x00002076</td></tr>
<tr><td>_global_vendingmachine02</td><td>0x7CCB1FE8</td><td>No</td><td>372</td><td>0x80005107</td><td>0x00012C16</td></tr>
<tr><td>_global_waterbumper</td><td>0x40CAC02C</td><td>No</td><td>6074</td><td>0x900001BA</td><td>0x00000620</td></tr>
<tr><td>_global_waterpuddle01</td><td>0x090231B4</td><td>No</td><td>3545</td><td>0x800093B3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_waterpuddle02</td><td>0xE2FFB74B</td><td>No</td><td>3546</td><td>0x800093B4</td><td>0x00008D5E</td></tr>
<tr><td>_global_waterpuddle03</td><td>0x80FCDE6E</td><td>No</td><td>3548</td><td>0x800093B6</td><td>0x00008F3A</td></tr>
<tr><td>_global_waterpuddle04</td><td>0x8B0E374D</td><td>No</td><td>3547</td><td>0x800093B5</td><td>0x0000D0E7</td></tr>
<tr><td>_global_waterpuddle05</td><td>0x610BB698</td><td>No</td><td>4531</td><td>0x80009F0C</td><td>0x0000AC01</td></tr>
<tr><td>_global_waterpuddle06</td><td>0x6B0987BF</td><td>No</td><td>4532</td><td>0x80009F0D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_waterpuddle07</td><td>0x0906AEE2</td><td>No</td><td>4533</td><td>0x80009F0E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_waterpuddle08</td><td>0x631885B1</td><td>No</td><td>4534</td><td>0x80009F0F</td><td>0x00000487</td></tr>
<tr><td>_global_watertowerA</td><td>0x4FB48B91</td><td>No</td><td>2725</td><td>0x80008718</td><td>0x00006DFA</td></tr>
<tr><td>_global_watertowerB</td><td>0xCDAD0326</td><td>No</td><td>2726</td><td>0x80008719</td><td>0x000134A1</td></tr>
<tr><td>_global_watertowerC</td><td>0xEFAF7743</td><td>No</td><td>2727</td><td>0x8000871A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_weightbench</td><td>0xC999385E</td><td>No</td><td>6086</td><td>0x900001C9</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_weightbench (Allied Users)</td><td>0x943DD17C</td><td>No</td><td>3808</td><td>0x800097C6</td><td>0x000039ED</td></tr>
<tr><td>_global_weightbench (OC Users)</td><td>0xE5B07A0D</td><td>No</td><td>2533</td><td>0x8000855F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_global_wheelbarrel</td><td>0x51E41E7D</td><td>No</td><td>3749</td><td>0x80009711</td><td>0x000107BA</td></tr>
<tr><td>_global_yellowoxytank</td><td>0xF5B44E82</td><td>Yes</td><td>2621</td><td>0x80008606</td><td>0x00013FA2</td></tr>
<tr><td>_GR_veh_truck_m151_static</td><td>0x75626E17</td><td>Yes</td><td>1087</td><td>0x80006A33</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_bld_alarmtower</td><td>0x91F09A65</td><td>No</td><td>4185</td><td>0x80009C1B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_bld_bunkerbeetle</td><td>0x235700A5</td><td>No</td><td>966</td><td>0x800065F4</td><td>0x00009F80</td></tr>
<tr><td>_groutpost_bld_bunkerconcrete</td><td>0xFCF2821D</td><td>No</td><td>967</td><td>0x800065F5</td><td>0x000108FF</td></tr>
<tr><td>_groutpost_bld_bunkersandbag01</td><td>0xC91E4FF9</td><td>No</td><td>969</td><td>0x800065F7</td><td>0x000123C6</td></tr>
<tr><td>_groutpost_bld_bunkersemitruck</td><td>0x54D6FD33</td><td>Yes</td><td>971</td><td>0x800065F9</td><td>0x00004528</td></tr>
<tr><td>_groutpost_bld_cranemining</td><td>0xCB0104A6</td><td>No</td><td>1244</td><td>0x80006CF3</td><td>0x0000442D</td></tr>
<tr><td>_groutpost_bld_earthmover</td><td>0x2546BDE8</td><td>No</td><td>1259</td><td>0x80006D03</td><td>0x000005D5</td></tr>
<tr><td>_groutpost_bld_guardtowertree01</td><td>0xB83C4D78</td><td>No</td><td>972</td><td>0x800065FA</td><td>0x00013242</td></tr>
<tr><td>_groutpost_bld_guardtowertree02</td><td>0x4239551F</td><td>No</td><td>1248</td><td>0x80006CF7</td><td>0x00004F82</td></tr>
<tr><td>_groutpost_bld_guardtowertree03</td><td>0x603745C2</td><td>No</td><td>1246</td><td>0x80006CF5</td><td>0x0000C099</td></tr>
<tr><td>_groutpost_bld_guardtowertree04</td><td>0x3A34CB59</td><td>No</td><td>1247</td><td>0x80006CF6</td><td>0x0001142C</td></tr>
<tr><td>_groutpost_bld_helipad</td><td>0x6D880D42</td><td>Yes</td><td>3760</td><td>0x80009722</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_bld_shackbus</td><td>0xF7C17325</td><td>No</td><td>973</td><td>0x800065FB</td><td>0x0000A8B9</td></tr>
<tr><td>_groutpost_bld_shackcave01</td><td>0x851B532F</td><td>No</td><td>974</td><td>0x800065FC</td><td>0x00008BAD</td></tr>
<tr><td>_groutpost_bld_shackcave01_Ruined</td><td>0x739CBF93</td><td>No</td><td>5218</td><td>0x8000A685</td><td>0x00000D15</td></tr>
<tr><td>_groutpost_bld_shackcave02</td><td>0x7B1D8208</td><td>No</td><td>1245</td><td>0x80006CF4</td><td>0x0000644E</td></tr>
<tr><td>_groutpost_bld_shackcave03</td><td>0xE520677D</td><td>No</td><td>1252</td><td>0x80006CFB</td><td>0x00007A0C</td></tr>
<tr><td>_groutpost_bld_shackcave04</td><td>0xDB0F0E9E</td><td>No</td><td>1251</td><td>0x80006CFA</td><td>0x00005A64</td></tr>
<tr><td>_groutpost_bld_shackcave05</td><td>0xFD1182BB</td><td>No</td><td>1250</td><td>0x80006CF9</td><td>0x00000855</td></tr>
<tr><td>_groutpost_bld_shackcave05_Ruined</td><td>0x02EE2F5F</td><td>No</td><td>5217</td><td>0x8000A684</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_bld_shackcave06</td><td>0xE3139864</td><td>No</td><td>1249</td><td>0x80006CF8</td><td>0x00012471</td></tr>
<tr><td>_groutpost_bld_shackfuselarge</td><td>0x50479153</td><td>No</td><td>976</td><td>0x800065FE</td><td>0x000129EB</td></tr>
<tr><td>_groutpost_bld_shackperm01</td><td>0xA199B59A</td><td>No</td><td>1242</td><td>0x80006CF1</td><td>0x0000A9F5</td></tr>
<tr><td>_groutpost_bld_shackperm02</td><td>0x03A10BA5</td><td>No</td><td>968</td><td>0x800065F6</td><td>0x00001B7E</td></tr>
<tr><td>_groutpost_bld_shackperm03</td><td>0x999E2630</td><td>No</td><td>1243</td><td>0x80006CF2</td><td>0x00004934</td></tr>
<tr><td>_groutpost_bld_shacksemiperm01</td><td>0x76EB6924</td><td>No</td><td>1241</td><td>0x80006CF0</td><td>0x000026BB</td></tr>
<tr><td>_groutpost_bld_shacktall01</td><td>0xB7801ADD</td><td>No</td><td>1254</td><td>0x80006CFD</td><td>0x00009143</td></tr>
<tr><td>_groutpost_bld_shacktall02</td><td>0x35789272</td><td>No</td><td>1253</td><td>0x80006CFC</td><td>0x000062E4</td></tr>
<tr><td>_groutpost_bld_shacktall02_Ruined</td><td>0x22BDE268</td><td>No</td><td>5219</td><td>0x8000A686</td><td>0x00002B87</td></tr>
<tr><td>_groutpost_bld_tentlargetarp</td><td>0x9D7242FA</td><td>No</td><td>970</td><td>0x800065F8</td><td>0x00013012</td></tr>
<tr><td>_groutpost_bld_tentlargetarp02</td><td>0xC8CA7210</td><td>No</td><td>2919</td><td>0x800089A3</td><td>0x0000D9D7</td></tr>
<tr><td>_groutpost_bld_tentlargetarp03</td><td>0xB2CC8E05</td><td>No</td><td>2920</td><td>0x800089A4</td><td>0x000038E5</td></tr>
<tr><td>_groutpost_bld_tentsmalltarp</td><td>0x4A0510FE</td><td>No</td><td>975</td><td>0x800065FD</td><td>0x0000E967</td></tr>
<tr><td>_groutpost_bld_tentsmalltarp02</td><td>0x271F1024</td><td>No</td><td>2917</td><td>0x800089A1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_bld_tentsmalltarp03</td><td>0x412177A9</td><td>No</td><td>2918</td><td>0x800089A2</td><td>0x00007DC7</td></tr>
<tr><td>_groutpost_bld_trailerhut01</td><td>0x7394A08A</td><td>No</td><td>977</td><td>0x800065FF</td><td>0x0000ABF5</td></tr>
<tr><td>_groutpost_bld_trailerhut02</td><td>0x159C5B55</td><td>No</td><td>1240</td><td>0x80006CEF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_env_cave</td><td>0xE9D90E55</td><td>No</td><td>1726</td><td>0x800075A1</td><td>0x00002482</td></tr>
<tr><td>_groutpost_env_junglewall</td><td>0x41175AA1</td><td>No</td><td>2036</td><td>0x800080D4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_env_junglewall02</td><td>0xC51D03BB</td><td>No</td><td>2040</td><td>0x800080D8</td><td>0x00010866</td></tr>
<tr><td>_groutpost_env_junglewallcornerleft</td><td>0x66955CED</td><td>No</td><td>2037</td><td>0x800080D5</td><td>0x00000C7F</td></tr>
<tr><td>_groutpost_env_junglewallcornerleft02</td><td>0x3F7BC827</td><td>No</td><td>2041</td><td>0x800080D9</td><td>0x00009DAE</td></tr>
<tr><td>_groutpost_env_junglewallcornerright</td><td>0x7998D38C</td><td>No</td><td>2038</td><td>0x800080D6</td><td>0x00003FE9</td></tr>
<tr><td>_groutpost_env_junglewallcornerright02</td><td>0x3489F276</td><td>No</td><td>2042</td><td>0x800080DA</td><td>0x00006129</td></tr>
<tr><td>_groutpost_env_minewall</td><td>0x324BF23F</td><td>No</td><td>1705</td><td>0x80007542</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_env_minewall6left</td><td>0x64327318</td><td>No</td><td>2788</td><td>0x8000875A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_env_minewall6right</td><td>0xEA946FBF</td><td>No</td><td>2789</td><td>0x8000875B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_env_minewallcorner16left</td><td>0x6E10B75A</td><td>No</td><td>1715</td><td>0x8000754D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_env_minewallcorner16right</td><td>0xB656FA31</td><td>No</td><td>1717</td><td>0x8000754F</td><td>0x00013B2B</td></tr>
<tr><td>_groutpost_env_minewallcorner32left</td><td>0x2C34A64C</td><td>No</td><td>1718</td><td>0x80007550</td><td>0x0000523E</td></tr>
<tr><td>_groutpost_env_minewallcorner32right</td><td>0x4FFC198B</td><td>No</td><td>1716</td><td>0x8000754E</td><td>0x00000837</td></tr>
<tr><td>_groutpost_env_minewalldrop01</td><td>0x09A03249</td><td>No</td><td>1710</td><td>0x80007548</td><td>0x0000EF94</td></tr>
<tr><td>_groutpost_env_minewalldrop02</td><td>0x6798777E</td><td>No</td><td>1711</td><td>0x80007549</td><td>0x00012203</td></tr>
<tr><td>_groutpost_env_minewallintersection16</td><td>0x31866C35</td><td>No</td><td>1714</td><td>0x8000754C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_groutpost_env_minewallintersection32</td><td>0x4F070FBB</td><td>No</td><td>1713</td><td>0x8000754B</td><td>0x00013F93</td></tr>
<tr><td>_groutpost_env_minewallrise01</td><td>0xDD1B6775</td><td>No</td><td>1709</td><td>0x80007547</td><td>0x0000C07E</td></tr>
<tr><td>_groutpost_env_minewallrise02</td><td>0xBB14762A</td><td>No</td><td>1712</td><td>0x8000754A</td><td>0x00012455</td></tr>
<tr><td>_groutpost_env_minewallshort</td><td>0x0B233177</td><td>No</td><td>2787</td><td>0x80008759</td><td>0x00007205</td></tr>
<tr><td>_groutpost_env_minewalltall</td><td>0x93BEB496</td><td>No</td><td>1708</td><td>0x80007546</td><td>0x000090C3</td></tr>
<tr><td>_groutpost_fueltanks</td><td>0xB673F35D</td><td>Yes</td><td>4768</td><td>0x8000A17C</td><td>0x00005E2E</td></tr>
<tr><td>_groutpost_interior_job</td><td>0x0441D0EA</td><td>No</td><td>4756</td><td>0x8000A16F</td><td>0x000130DF</td></tr>
<tr><td>_groutpost_mine_road10</td><td>0x4A2188EB</td><td>No</td><td>1696</td><td>0x80007536</td><td>0x0000C92B</td></tr>
<tr><td>_groutpost_mine_road10i</td><td>0x192E27FC</td><td>No</td><td>2068</td><td>0x8000813A</td><td>0x0000CCE0</td></tr>
<tr><td>_groutpost_mine_road10merge</td><td>0xD13BAE81</td><td>No</td><td>3963</td><td>0x80009953</td><td>0x00003C50</td></tr>
<tr><td>_groutpost_mine_road10T</td><td>0x1B4E7ECD</td><td>No</td><td>1697</td><td>0x80007537</td><td>0x00001587</td></tr>
<tr><td>_groutpost_mine_road20U</td><td>0x4E096A37</td><td>No</td><td>1698</td><td>0x8000753A</td><td>0x000013F8</td></tr>
<tr><td>_groutpost_podium</td><td>0x1E20A092</td><td>No</td><td>2758</td><td>0x8000873B</td><td>0x000003CE</td></tr>
<tr><td>_groutpost_podium (speaker)</td><td>0x0A17EC1A</td><td>No</td><td>3801</td><td>0x800097BE</td><td>0x00013D87</td></tr>
<tr><td>_guanare_bridgeorinoco</td><td>0x3F2D24A2</td><td>No</td><td>6054</td><td>0x900001A6</td><td>0x0000675D</td></tr>
<tr><td>_guanare_bridgeorinocosupport</td><td>0x7D29156B</td><td>No</td><td>6055</td><td>0x900001A7</td><td>0x000077FB</td></tr>
<tr><td>_guerilla_chaira</td><td>0x88AA3BDA</td><td>No</td><td>3792</td><td>0x800097AD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_guerilla_chairb</td><td>0xEAB191E5</td><td>No</td><td>3795</td><td>0x800097B0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_guerilla_chairc</td><td>0x80AEAC70</td><td>No</td><td>3796</td><td>0x800097B1</td><td>0x000109AA</td></tr>
<tr><td>_guerilla_junker</td><td>0x5DE6C75D</td><td>No</td><td>3793</td><td>0x800097AE</td><td>0x00002A20</td></tr>
<tr><td>_guerilla_junker_full</td><td>0x3E8893A7</td><td>No</td><td>3799</td><td>0x800097B6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_guerilla_junker_hood</td><td>0x50C4CEFA</td><td>No</td><td>3798</td><td>0x800097B5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_guerilla_junker_tire</td><td>0x03A2CCCE</td><td>No</td><td>3797</td><td>0x800097B4</td><td>0x000102B1</td></tr>
<tr><td>_industrial_att_pipelargeangle</td><td>0x5862432E</td><td>No</td><td>1006</td><td>0x80006896</td><td>0x00007534</td></tr>
<tr><td>_industrial_att_pipelargeangle_AllCon002</td><td>0x69EF2FEC</td><td>No</td><td>2678</td><td>0x80008680</td><td>0x00007D29</td></tr>
<tr><td>_industrial_att_pipelargecap</td><td>0x7456859B</td><td>No</td><td>1007</td><td>0x80006897</td><td>0x0000C420</td></tr>
<tr><td>_industrial_att_pipelargecap_AllCon002</td><td>0x8D26404D</td><td>No</td><td>2679</td><td>0x80008681</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_att_pipelargeL</td><td>0x005B049B</td><td>No</td><td>1008</td><td>0x80006898</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_att_pipelargeL_AllCon002</td><td>0xCAD0374D</td><td>No</td><td>2680</td><td>0x80008682</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_att_pipelargeshort</td><td>0x5D09CD45</td><td>No</td><td>1009</td><td>0x80006899</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_att_pipelargeshort_AllCon002</td><td>0x49F953DB</td><td>No</td><td>2677</td><td>0x8000867F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_att_pipelargeY</td><td>0x068A6C42</td><td>No</td><td>1010</td><td>0x8000689A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_att_pipelargeY_AllCon002</td><td>0xDF7457D8</td><td>No</td><td>2681</td><td>0x80008683</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Industrial_bld_conveyorbelt</td><td>0x1B770D31</td><td>No</td><td>2916</td><td>0x800089A0</td><td>0x00007C22</td></tr>
<tr><td>_Industrial_bld_conveyorbeltangle</td><td>0x3604CE92</td><td>No</td><td>2915</td><td>0x8000899F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Industrial_bld_conveyortransition</td><td>0x9F85B48B</td><td>No</td><td>2914</td><td>0x8000899E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_domerefinery</td><td>0x58619CC4</td><td>No</td><td>616</td><td>0x80005C29</td><td>0x0000C48E</td></tr>
<tr><td>_industrial_bld_gasstation01</td><td>0xC72905CD</td><td>No</td><td>807</td><td>0x80006243</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_gasstation01_ruined</td><td>0x9C6142A1</td><td>No</td><td>4616</td><td>0x80009FA8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_gasstation02</td><td>0x45217D62</td><td>No</td><td>808</td><td>0x80006244</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_gasstation02_ruined</td><td>0x945F9B58</td><td>No</td><td>4639</td><td>0x80009FC0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_gasstation_bathroom</td><td>0x059D6F15</td><td>No</td><td>793</td><td>0x80006234</td><td>0x000052C5</td></tr>
<tr><td>_industrial_bld_gasstationpump01</td><td>0x40B92BD7</td><td>No</td><td>792</td><td>0x80006233</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_gasstationpump01_ruined</td><td>0xDAB6C0DB</td><td>No</td><td>4615</td><td>0x80009FA7</td><td>0x00001BC3</td></tr>
<tr><td>_industrial_bld_gasstationpump02</td><td>0x56BB8D10</td><td>No</td><td>809</td><td>0x80006245</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_gasstationpump02_ruined</td><td>0xD5CC807E</td><td>No</td><td>4640</td><td>0x80009FC1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_gasstationpump03</td><td>0x40BDA905</td><td>No</td><td>1399</td><td>0x80006EF7</td><td>0x000089EC</td></tr>
<tr><td>_industrial_bld_hangar01</td><td>0x3F8A1245</td><td>No</td><td>617</td><td>0x80005C2A</td><td>0x000106CC</td></tr>
<tr><td>_industrial_bld_hangar01_ruined</td><td>0x7F0DB5D9</td><td>No</td><td>5846</td><td>0x8000AF9E</td><td>0x0000BF00</td></tr>
<tr><td>_industrial_bld_oilrig</td><td>0x69064E47</td><td>No</td><td>475</td><td>0x800056B1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_refinery01</td><td>0x77F5D454</td><td>No</td><td>1396</td><td>0x80006EF4</td><td>0x00003B13</td></tr>
<tr><td>_industrial_bld_refinery02</td><td>0x51F359EB</td><td>No</td><td>1276</td><td>0x80006D7C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_refinery03</td><td>0x6FF14A8E</td><td>No</td><td>1397</td><td>0x80006EF5</td><td>0x0000285B</td></tr>
<tr><td>_industrial_bld_refinery04</td><td>0x7A02A36D</td><td>No</td><td>1398</td><td>0x80006EF6</td><td>0x0000627F</td></tr>
<tr><td>_industrial_bld_refinery04_Ruined</td><td>0xA5A15741</td><td>No</td><td>5229</td><td>0x8000A698</td><td>0x00004D7A</td></tr>
<tr><td>_industrial_bld_refinery05</td><td>0x500022B8</td><td>No</td><td>1271</td><td>0x80006D77</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_refinery06</td><td>0xD9FD2A5F</td><td>No</td><td>1272</td><td>0x80006D78</td><td>0x000134D4</td></tr>
<tr><td>_industrial_bld_silosmall</td><td>0x2C587443</td><td>No</td><td>657</td><td>0x80005F85</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_silowide</td><td>0x4805C763</td><td>No</td><td>658</td><td>0x80005F86</td><td>0x00008686</td></tr>
<tr><td>_industrial_bld_smokestack</td><td>0x003BFA08</td><td>No</td><td>656</td><td>0x80005F84</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_towerrefinerysmall</td><td>0x9B3946BD</td><td>No</td><td>659</td><td>0x80005F87</td><td>0x0000A18A</td></tr>
<tr><td>_industrial_bld_towerrefinerytall</td><td>0xB4F3B8CD</td><td>No</td><td>660</td><td>0x80005F88</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_warehouse01</td><td>0xC9CA213B</td><td>No</td><td>661</td><td>0x80005F89</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_warehouse01_Ruined</td><td>0xB56796DF</td><td>No</td><td>5228</td><td>0x8000A697</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_warehouse02</td><td>0xAFCC36E4</td><td>No</td><td>624</td><td>0x80005C35</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_warehouse02_Ruined</td><td>0xD70C7FF2</td><td>No</td><td>5227</td><td>0x8000A696</td><td>0x00001E66</td></tr>
<tr><td>_industrial_bld_warehouse03</td><td>0xC9CE9E69</td><td>No</td><td>625</td><td>0x80005C36</td><td>0x0000DA48</td></tr>
<tr><td>_industrial_bld_warehouse03 dangerous1</td><td>0x0EBCB5A6</td><td>No</td><td>557</td><td>0x80005BAB</td><td>0x0000058E</td></tr>
<tr><td>_industrial_bld_warehouse04</td><td>0x2FD17D92</td><td>No</td><td>635</td><td>0x80005C41</td><td>0x0000589B</td></tr>
<tr><td>_industrial_bld_warehouse05</td><td>0x51D3F1AF</td><td>No</td><td>903</td><td>0x800064B1</td><td>0x0000130F</td></tr>
<tr><td>_industrial_bld_warehouse05_ruined</td><td>0x26162713</td><td>No</td><td>4151</td><td>0x80009B4E</td><td>0x00013181</td></tr>
<tr><td>_industrial_bld_warehouse06</td><td>0x47D62088</td><td>No</td><td>662</td><td>0x80005F8B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_warehouse06_ruined</td><td>0xFBF51E96</td><td>No</td><td>5224</td><td>0x8000A693</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_warehouselarge01</td><td>0x502033FA</td><td>No</td><td>901</td><td>0x800064AE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_bld_warehouselarge02</td><td>0xB2278A05</td><td>No</td><td>904</td><td>0x800064B2</td><td>0x00009E9A</td></tr>
<tr><td>_industrial_bld_warehousesmall01</td><td>0xF6CA7CC2</td><td>No</td><td>1394</td><td>0x80006EF2</td><td>0x0000BD46</td></tr>
<tr><td>_industrial_bld_warehousesmall01_ruined</td><td>0xCFC34938</td><td>No</td><td>5849</td><td>0x8000AFA1</td><td>0x00010FF6</td></tr>
<tr><td>_industrial_bld_warehousesmall02</td><td>0x78D2052D</td><td>No</td><td>1395</td><td>0x80006EF3</td><td>0x000018E8</td></tr>
<tr><td>_industrial_bld_warehousesmall02_ruined</td><td>0x817D0F01</td><td>No</td><td>4614</td><td>0x80009FA6</td><td>0x0000F089</td></tr>
<tr><td>_industrial_cart</td><td>0x0AA399A2</td><td>No</td><td>629</td><td>0x80005C3A</td><td>0x00012BFA</td></tr>
<tr><td>_industrial_cartlong</td><td>0x668B6350</td><td>No</td><td>628</td><td>0x80005C39</td><td>0x0000F2D4</td></tr>
<tr><td>_industrial_cartribbed</td><td>0x59B8430E</td><td>No</td><td>631</td><td>0x80005C3D</td><td>0x000095F6</td></tr>
<tr><td>_industrial_cartsmelting</td><td>0xFABD4EF1</td><td>No</td><td>632</td><td>0x80005C3E</td><td>0x000054CC</td></tr>
<tr><td>_industrial_catwalkangle</td><td>0x355BE790</td><td>No</td><td>905</td><td>0x800064B3</td><td>0x00001FD9</td></tr>
<tr><td>_industrial_catwalkcap</td><td>0xBE72DD61</td><td>No</td><td>906</td><td>0x800064B4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_catwalkl</td><td>0xB847F33D</td><td>No</td><td>907</td><td>0x800064B5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_catwalkshort</td><td>0x4B6F2993</td><td>No</td><td>908</td><td>0x800064B6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_catwalkstraight</td><td>0xA08E2DE9</td><td>No</td><td>909</td><td>0x800064B7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_generator01</td><td>0x86CE46A6</td><td>No</td><td>623</td><td>0x80005C34</td><td>0x00011313</td></tr>
<tr><td>_industrial_lamppost01</td><td>0xBC6A1C9D</td><td>No</td><td>641</td><td>0x80005C49</td><td>0x000008CD</td></tr>
<tr><td>_industrial_lamppost02</td><td>0x3A629432</td><td>No</td><td>664</td><td>0x80005F8E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_machineparts01</td><td>0xE63456EE</td><td>No</td><td>665</td><td>0x80005F8F</td><td>0x00007CCE</td></tr>
<tr><td>_industrial_machineparts02</td><td>0x483BACF9</td><td>No</td><td>666</td><td>0x80005F90</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_machineparts03</td><td>0x6E39AA34</td><td>No</td><td>667</td><td>0x80005F91</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_machinepartsramp01</td><td>0x4EA9DACE</td><td>No</td><td>4164</td><td>0x80009C01</td><td>0x000032A6</td></tr>
<tr><td>_Industrial_pipe12m</td><td>0x9C48CA52</td><td>No</td><td>5414</td><td>0x8000A9E7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Industrial_pipe20m</td><td>0xB55C960F</td><td>No</td><td>5415</td><td>0x8000A9E8</td><td>0x0001301C</td></tr>
<tr><td>_Industrial_pipe4m</td><td>0xE885A2ED</td><td>No</td><td>5413</td><td>0x8000A9E6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Industrial_pipecurveSide</td><td>0x5D683004</td><td>No</td><td>5409</td><td>0x8000A9E2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Industrial_pipecurveUpdown</td><td>0x8DF7DF8A</td><td>No</td><td>5408</td><td>0x8000A9E1</td><td>0x0000C050</td></tr>
<tr><td>_industrial_pipeground01</td><td>0x7B544FF0</td><td>No</td><td>668</td><td>0x80005F92</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_pipesstacked</td><td>0x9FDB14BA</td><td>No</td><td>669</td><td>0x80005F93</td><td>0x0000E04A</td></tr>
<tr><td>_Industrial_pipesupport12m</td><td>0x1978C889</td><td>No</td><td>5411</td><td>0x8000A9E4</td><td>0x0000290A</td></tr>
<tr><td>_Industrial_pipesupport16m</td><td>0x53EA4DAD</td><td>No</td><td>5410</td><td>0x8000A9E3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Industrial_pipesupport8m</td><td>0x4FE22CC0</td><td>No</td><td>5412</td><td>0x8000A9E5</td><td>0x00000B11</td></tr>
<tr><td>_industrial_signgasshort</td><td>0x6F91415C</td><td>No</td><td>1264</td><td>0x80006D6F</td><td>0x00010DA8</td></tr>
<tr><td>_industrial_signgastall</td><td>0xE8ED678B</td><td>No</td><td>1265</td><td>0x80006D70</td><td>0xFFFFFFFF</td></tr>
<tr><td>_industrial_track</td><td>0x30A9B545</td><td>No</td><td>1033</td><td>0x80006912</td><td>0x00010D9A</td></tr>
<tr><td>_industrial_trackcurve</td><td>0xCD43AA92</td><td>No</td><td>926</td><td>0x800064CA</td><td>0x0000D6D0</td></tr>
<tr><td>_industrial_trackstop</td><td>0x0C375955</td><td>No</td><td>633</td><td>0x80005C3F</td><td>0x00003F42</td></tr>
<tr><td>_industrial_trackstraight</td><td>0x3204223F</td><td>No</td><td>927</td><td>0x800064CB</td><td>0x000052FB</td></tr>
<tr><td>_island_att_battlement</td><td>0xB8E09698</td><td>No</td><td>1274</td><td>0x80006D7A</td><td>0x0000F01E</td></tr>
<tr><td>_island_bld_boothrefreshments01</td><td>0xA0EAE0E8</td><td>No</td><td>6053</td><td>0x900001A5</td><td>0x00002961</td></tr>
<tr><td>_island_bld_boothrefreshments01_ruined</td><td>0xDB0B3D76</td><td>No</td><td>2078</td><td>0x8000814D</td><td>0x00007045</td></tr>
<tr><td>_island_bld_boothrental</td><td>0xEB999BF3</td><td>No</td><td>6044</td><td>0x9000019C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_island_bld_bridge01</td><td>0xB98FEEC9</td><td>No</td><td>805</td><td>0x80006241</td><td>0xFFFFFFFF</td></tr>
<tr><td>_island_bld_bridge01_ruined</td><td>0xCACC33DD</td><td>No</td><td>5556</td><td>0x8000AB5D</td><td>0x00002314</td></tr>
<tr><td>_island_bld_fortress01</td><td>0x8A35B530</td><td>No</td><td>806</td><td>0x80006242</td><td>0x000134F1</td></tr>
<tr><td>_island_bld_fortress01_ruined</td><td>0xD8F0519E</td><td>No</td><td>5554</td><td>0x8000AB5B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_island_bld_hutmodern01</td><td>0x84ECA286</td><td>No</td><td>6045</td><td>0x9000019D</td><td>0x000100FC</td></tr>
<tr><td>_island_bld_hutmodern01_ruined</td><td>0x7E118C8C</td><td>No</td><td>2077</td><td>0x8000814C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_island_bld_tower01</td><td>0x62E28227</td><td>No</td><td>804</td><td>0x80006240</td><td>0x00012FD9</td></tr>
<tr><td>_island_bld_tower01_ruined</td><td>0x6235146B</td><td>No</td><td>5555</td><td>0x8000AB5C</td><td>0x0000CFAD</td></tr>
<tr><td>_island_wallangled</td><td>0xC0260DB5</td><td>No</td><td>1661</td><td>0x80007354</td><td>0x000133D9</td></tr>
<tr><td>_island_wallangled_ruined</td><td>0x702E42C9</td><td>No</td><td>5549</td><td>0x8000AB56</td><td>0x00004716</td></tr>
<tr><td>_island_wallcorner</td><td>0x1CA8196D</td><td>No</td><td>1662</td><td>0x80007355</td><td>0x000073ED</td></tr>
<tr><td>_island_wallcorner_ruined</td><td>0xC2440941</td><td>No</td><td>5550</td><td>0x8000AB57</td><td>0x00008790</td></tr>
<tr><td>_island_wallend</td><td>0x29A43585</td><td>No</td><td>1663</td><td>0x80007356</td><td>0x00008050</td></tr>
<tr><td>_island_wallend_ruined</td><td>0x070DD819</td><td>No</td><td>5551</td><td>0x8000AB58</td><td>0x0000C419</td></tr>
<tr><td>_island_wallstraight</td><td>0x3AC713AC</td><td>No</td><td>1664</td><td>0x80007357</td><td>0x00000D09</td></tr>
<tr><td>_island_wallstraight_ruined</td><td>0xDD26EC9A</td><td>No</td><td>5552</td><td>0x8000AB59</td><td>0xFFFFFFFF</td></tr>
<tr><td>_island_wallT</td><td>0x66D2981A</td><td>No</td><td>1665</td><td>0x80007358</td><td>0x00002B7E</td></tr>
<tr><td>_island_wallT_ruined</td><td>0x27349990</td><td>No</td><td>5553</td><td>0x8000AB5A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_bld_ruinshotelback</td><td>0x975027B3</td><td>No</td><td>1523</td><td>0x8000717A</td><td>0x000093FB</td></tr>
<tr><td>_jungle_bld_ruinshotelback_ruined</td><td>0x73CAD1B7</td><td>No</td><td>5273</td><td>0x8000A7C4</td><td>0x00008441</td></tr>
<tr><td>_Jungle_bld_ruinshotelcorner</td><td>0x1B24B935</td><td>No</td><td>1524</td><td>0x8000717B</td><td>0x0000A91B</td></tr>
<tr><td>_Jungle_bld_ruinshotelcorner_ruined</td><td>0x1F026949</td><td>No</td><td>2110</td><td>0x80008184</td><td>0x0000F6AF</td></tr>
<tr><td>_jungle_bld_ruinshotelfront</td><td>0x0A152D47</td><td>No</td><td>1525</td><td>0x8000717C</td><td>0x00012600</td></tr>
<tr><td>_jungle_bld_ruinshotelfront_ruined</td><td>0xF498950B</td><td>No</td><td>5274</td><td>0x8000A7C5</td><td>0x000092C1</td></tr>
<tr><td>_jungle_bld_ruinshotelside</td><td>0xAA42BA23</td><td>No</td><td>1526</td><td>0x8000717D</td><td>0x0000D1E5</td></tr>
<tr><td>_jungle_bld_ruinshotelside_ruined</td><td>0x15CF9127</td><td>No</td><td>5275</td><td>0x8000A7C6</td><td>0x00004884</td></tr>
<tr><td>_jungle_bridge_metalvehicleA</td><td>0x34ED110C</td><td>No</td><td>1527</td><td>0x8000717E</td><td>0x00003CA7</td></tr>
<tr><td>_jungle_bridge_woodpedestrianA</td><td>0xBF5FF99D</td><td>No</td><td>1528</td><td>0x8000717F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_background01</td><td>0x88F2A743</td><td>No</td><td>951</td><td>0x800065E5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_bushlarge01</td><td>0x933DB7B4</td><td>No</td><td>4535</td><td>0x80009F10</td><td>0x0000277E</td></tr>
<tr><td>_jungle_env_bushlarge02</td><td>0x6D3B3D4B</td><td>No</td><td>803</td><td>0x8000623E</td><td>0x0000E19D</td></tr>
<tr><td>_jungle_env_bushlarge03</td><td>0x0B38646E</td><td>No</td><td>1273</td><td>0x80006D79</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_bushmedium01</td><td>0x4215F558</td><td>No</td><td>794</td><td>0x80006235</td><td>0x0000FC03</td></tr>
<tr><td>_jungle_env_bushmedium02</td><td>0x4C13C67F</td><td>No</td><td>795</td><td>0x80006236</td><td>0x0000A4F7</td></tr>
<tr><td>_jungle_env_bushmedium03</td><td>0xEA10EDA2</td><td>No</td><td>796</td><td>0x80006237</td><td>0x00006761</td></tr>
<tr><td>_jungle_env_bushsmall01</td><td>0x86C5B570</td><td>No</td><td>797</td><td>0x80006238</td><td>0x000017BF</td></tr>
<tr><td>_jungle_env_bushsmall02</td><td>0x70C35437</td><td>No</td><td>1266</td><td>0x80006D71</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_bushsmall03</td><td>0x8EC144DA</td><td>No</td><td>929</td><td>0x800064CF</td><td>0x0001383A</td></tr>
<tr><td>_jungle_env_junglewallfoliage01</td><td>0x81B99A1B</td><td>No</td><td>3295</td><td>0x80008F68</td><td>0x00011AA8</td></tr>
<tr><td>_jungle_env_junglewallfoliage02</td><td>0xE7BC7944</td><td>No</td><td>3297</td><td>0x80008F6A</td><td>0x00006F98</td></tr>
<tr><td>_jungle_env_junglewallfoliage03</td><td>0x01BEE0C9</td><td>No</td><td>3296</td><td>0x80008F69</td><td>0x00001FF1</td></tr>
<tr><td>_jungle_env_junglewallfoliage04</td><td>0xE7C0F672</td><td>No</td><td>5266</td><td>0x8000A7BD</td><td>0x0000565A</td></tr>
<tr><td>_jungle_env_largecanopy01</td><td>0xC69265EE</td><td>No</td><td>1260</td><td>0x80006D04</td><td>0x0000E465</td></tr>
<tr><td>_jungle_env_largecanopy01_standalone</td><td>0xA6246CCC</td><td>No</td><td>4763</td><td>0x8000A176</td><td>0x00004D95</td></tr>
<tr><td>_jungle_env_plantlarge01</td><td>0xE2F627AB</td><td>No</td><td>798</td><td>0x80006239</td><td>0x0000B342</td></tr>
<tr><td>_jungle_env_plantlarge02</td><td>0x08F8A214</td><td>No</td><td>6070</td><td>0x900001B6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_plantlarge04</td><td>0x88FDE8C2</td><td>No</td><td>930</td><td>0x800064D0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_plantmed01</td><td>0xAC787460</td><td>No</td><td>1236</td><td>0x80006CEB</td><td>0x00004B92</td></tr>
<tr><td>_jungle_env_plantmed03</td><td>0x34733A4A</td><td>No</td><td>931</td><td>0x800064D1</td><td>0x00002876</td></tr>
<tr><td>_jungle_env_plantsmall02</td><td>0x90EACF9C</td><td>No</td><td>799</td><td>0x8000623A</td><td>0x00010B58</td></tr>
<tr><td>_jungle_env_plantsmall03</td><td>0x8AED04C1</td><td>No</td><td>800</td><td>0x8000623B</td><td>0x00012143</td></tr>
<tr><td>_Jungle_env_rockhuge01</td><td>0xE4600495</td><td>No</td><td>5261</td><td>0x8000A7B8</td><td>0x00011956</td></tr>
<tr><td>_Jungle_env_rockhuge02</td><td>0x425849CA</td><td>No</td><td>4979</td><td>0x8000A39A</td><td>0x0000A3A2</td></tr>
<tr><td>_jungle_env_rocklarge01</td><td>0x2165017F</td><td>No</td><td>6072</td><td>0x900001B8</td><td>0x000078CB</td></tr>
<tr><td>_jungle_env_rocklarge02</td><td>0x17673058</td><td>No</td><td>1108</td><td>0x80006B42</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_rocklarge03</td><td>0x4169B10D</td><td>No</td><td>1267</td><td>0x80006D72</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_rockmedium01</td><td>0xD7F8BD21</td><td>No</td><td>932</td><td>0x800064D2</td><td>0x000032D7</td></tr>
<tr><td>_jungle_env_rockmedium02</td><td>0x55F134B6</td><td>No</td><td>965</td><td>0x800065F3</td><td>0x0000934D</td></tr>
<tr><td>_jungle_env_rockmedium03</td><td>0x37F34413</td><td>No</td><td>933</td><td>0x800064D3</td><td>0x00003883</td></tr>
<tr><td>_jungle_env_rocksmall01</td><td>0xA158FFB7</td><td>No</td><td>934</td><td>0x800064D4</td><td>0x00010AC8</td></tr>
<tr><td>_jungle_env_rocksmall02</td><td>0xB75B60F0</td><td>No</td><td>935</td><td>0x800064D5</td><td>0x00004640</td></tr>
<tr><td>_jungle_env_rocksmall03</td><td>0x215E4665</td><td>No</td><td>936</td><td>0x800064D6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_smallcanopy01</td><td>0x4BDD9516</td><td>No</td><td>2942</td><td>0x800089BE</td><td>0x0000996D</td></tr>
<tr><td>_jungle_env_smallcanopy02</td><td>0xCDE51D81</td><td>No</td><td>3317</td><td>0x80008F81</td><td>0x0000280A</td></tr>
<tr><td>_jungle_env_treecanopy01</td><td>0x1BDD901B</td><td>No</td><td>1004</td><td>0x8000688C</td><td>0x0000187F</td></tr>
<tr><td>_jungle_env_treecanopy02</td><td>0x81E06F44</td><td>No</td><td>1275</td><td>0x80006D7B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_treemedium01</td><td>0xB5D32B06</td><td>No</td><td>801</td><td>0x8000623C</td><td>0x00010767</td></tr>
<tr><td>_jungle_env_treemedium03</td><td>0xBDD7B4CC</td><td>No</td><td>937</td><td>0x800064D7</td><td>0x0000FAF3</td></tr>
<tr><td>_jungle_env_treesmall01</td><td>0x4555E076</td><td>No</td><td>938</td><td>0x800064D8</td><td>0x0000BA82</td></tr>
<tr><td>_jungle_env_treesmall02</td><td>0xC75D68E1</td><td>No</td><td>2074</td><td>0x80008149</td><td>0x000040D0</td></tr>
<tr><td>_jungle_env_treesmall03</td><td>0x4D5A6A3C</td><td>No</td><td>3756</td><td>0x8000971E</td><td>0x00000137</td></tr>
<tr><td>_jungle_env_treetall01</td><td>0x43D0ACEE</td><td>No</td><td>939</td><td>0x800064D9</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_treetall01_standalone</td><td>0xBF94D9CC</td><td>No</td><td>4760</td><td>0x8000A173</td><td>0x00011B43</td></tr>
<tr><td>_jungle_env_treetall02</td><td>0xA5D802F9</td><td>No</td><td>942</td><td>0x800064DC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_treetall02_standalone</td><td>0x4FE46019</td><td>No</td><td>4761</td><td>0x8000A174</td><td>0x00005909</td></tr>
<tr><td>_jungle_env_treetall03</td><td>0xCBD60034</td><td>No</td><td>6069</td><td>0x900001B5</td><td>0x0000B1D8</td></tr>
<tr><td>_jungle_env_treetall03_standalone</td><td>0x8B40409A</td><td>No</td><td>4762</td><td>0x8000A175</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_treethin01</td><td>0xED2D89EA</td><td>No</td><td>956</td><td>0x800065EA</td><td>0x0000EA63</td></tr>
<tr><td>_jungle_env_treethin02</td><td>0x0F347B35</td><td>No</td><td>955</td><td>0x800065E9</td><td>0x00009B01</td></tr>
<tr><td>_jungle_env_treethin03</td><td>0xE531FA80</td><td>No</td><td>954</td><td>0x800065E8</td><td>0x00007079</td></tr>
<tr><td>_jungle_env_vines01</td><td>0xD4D2A838</td><td>No</td><td>952</td><td>0x800065E6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_env_vines02</td><td>0x5ECFAFDF</td><td>No</td><td>953</td><td>0x800065E7</td><td>0x00004567</td></tr>
<tr><td>_jungle_fountainruinshotel</td><td>0xFA7C4323</td><td>No</td><td>1529</td><td>0x80007180</td><td>0x000009E7</td></tr>
<tr><td>_jungle_fountainruinshotel_ruined</td><td>0xE874E427</td><td>No</td><td>5277</td><td>0x8000A7C8</td><td>0x00010226</td></tr>
<tr><td>_jungle_guardgate</td><td>0x259E3704</td><td>No</td><td>5457</td><td>0x8000AA58</td><td>0x00008DDE</td></tr>
<tr><td>_jungle_road10</td><td>0xDFBEBCAB</td><td>No</td><td>957</td><td>0x800065EB</td><td>0x0001156A</td></tr>
<tr><td>_jungle_road10cross</td><td>0x611C61E1</td><td>No</td><td>978</td><td>0x80006600</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_road10cross5</td><td>0x3074D9F2</td><td>No</td><td>2033</td><td>0x800080D0</td><td>0x0001203A</td></tr>
<tr><td>_jungle_road10merge</td><td>0xD963C641</td><td>No</td><td>3304</td><td>0x80008F74</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_road10mergeOutskirt</td><td>0x4D40C974</td><td>No</td><td>3557</td><td>0x800093BF</td><td>0x0000E732</td></tr>
<tr><td>_jungle_road10straight</td><td>0xD8ECD1C1</td><td>No</td><td>3306</td><td>0x80008F76</td><td>0x000009ED</td></tr>
<tr><td>_jungle_road10t</td><td>0x63042A8D</td><td>No</td><td>963</td><td>0x800065F1</td><td>0x00007293</td></tr>
<tr><td>_jungle_road10t20</td><td>0xECEC885F</td><td>No</td><td>1037</td><td>0x80006916</td><td>0x0000175C</td></tr>
<tr><td>_jungle_road10t5</td><td>0xFC426B5E</td><td>No</td><td>2032</td><td>0x800080CF</td><td>0x00010096</td></tr>
<tr><td>_jungle_road20</td><td>0x170A8FE6</td><td>No</td><td>1039</td><td>0x80006918</td><td>0x0000DB1B</td></tr>
<tr><td>_jungle_road20cross10</td><td>0x6AE0E589</td><td>No</td><td>1036</td><td>0x80006915</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_road20t10</td><td>0x5FA3BB15</td><td>No</td><td>1038</td><td>0x80006917</td><td>0x00007C72</td></tr>
<tr><td>_jungle_road5</td><td>0x03D76EA5</td><td>No</td><td>2030</td><td>0x800080CD</td><td>0x0000B764</td></tr>
<tr><td>_jungle_road5cross</td><td>0x8942178B</td><td>No</td><td>2034</td><td>0x800080D2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_road5t</td><td>0xB2B0ECC3</td><td>No</td><td>2035</td><td>0x800080D3</td><td>0x0001105B</td></tr>
<tr><td>_jungle_road5transition</td><td>0x8FEB7E30</td><td>No</td><td>2031</td><td>0x800080CE</td><td>0x0000CE4B</td></tr>
<tr><td>_jungle_ruinshotelarch</td><td>0x2DC0C04B</td><td>No</td><td>1530</td><td>0x80007181</td><td>0x000094EA</td></tr>
<tr><td>_jungle_ruinshotelarch_ruined</td><td>0x09C4CDAF</td><td>No</td><td>5276</td><td>0x8000A7C7</td><td>0x00009D90</td></tr>
<tr><td>_jungle_ruinshotelpool</td><td>0x40D01C25</td><td>No</td><td>1531</td><td>0x80007182</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_ruinsplane01_back</td><td>0x47C9ED04</td><td>No</td><td>2704</td><td>0x80008700</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_ruinsplane01_front</td><td>0xBAE40F9A</td><td>No</td><td>2705</td><td>0x80008701</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_ruinsplane01_mid</td><td>0xF85966F1</td><td>No</td><td>2706</td><td>0x80008702</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_ruinsplane01_wing</td><td>0x52D8EC44</td><td>No</td><td>3999</td><td>0x80009994</td><td>0xFFFFFFFF</td></tr>
<tr><td>_jungle_wallgate</td><td>0x0736675F</td><td>No</td><td>3558</td><td>0x800093C0</td><td>0x00012C7B</td></tr>
<tr><td>_lwcommercial_road10</td><td>0x1585ED61</td><td>No</td><td>562</td><td>0x80005BE9</td><td>0x00013C22</td></tr>
<tr><td>_lwcommercial_road10cross</td><td>0x998A7847</td><td>No</td><td>576</td><td>0x80005BF8</td><td>0x0000FF18</td></tr>
<tr><td>_lwcommercial_road10cross5</td><td>0x1FB8AA84</td><td>No</td><td>575</td><td>0x80005BF7</td><td>0x000099E4</td></tr>
<tr><td>_lwcommercial_road10l</td><td>0x35787A97</td><td>No</td><td>574</td><td>0x80005BF6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_lwcommercial_road10t</td><td>0x553C82CF</td><td>No</td><td>573</td><td>0x80005BF5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_lwcommercial_road10t5</td><td>0x3126673C</td><td>No</td><td>572</td><td>0x80005BF4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_lwcommercial_road20</td><td>0x815A6890</td><td>No</td><td>563</td><td>0x80005BEA</td><td>0x0000E133</td></tr>
<tr><td>_lwcommercial_road20cross</td><td>0xE00401B0</td><td>No</td><td>571</td><td>0x80005BF3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_lwcommercial_road20cross10</td><td>0xF9788E5B</td><td>No</td><td>570</td><td>0x80005BF2</td><td>0x000097B3</td></tr>
<tr><td>_lwcommercial_road20t10</td><td>0xAFA2E1AB</td><td>No</td><td>569</td><td>0x80005BF1</td><td>0x0000CDFB</td></tr>
<tr><td>_lwcommercial_road5</td><td>0x454AEE97</td><td>No</td><td>561</td><td>0x80005BE8</td><td>0x00003EBC</td></tr>
<tr><td>_lwcommercial_road5cross</td><td>0x79DDB93D</td><td>No</td><td>568</td><td>0x80005BF0</td><td>0x000102CC</td></tr>
<tr><td>_lwcommercial_road5l</td><td>0xC951E601</td><td>No</td><td>567</td><td>0x80005BEF</td><td>0x0000FC48</td></tr>
<tr><td>_lwcommercial_road5t</td><td>0x296604D9</td><td>No</td><td>566</td><td>0x80005BEE</td><td>0x00009711</td></tr>
<tr><td>_lwcommercial_road5t10</td><td>0xBB9E9E86</td><td>No</td><td>565</td><td>0x80005BED</td><td>0x00007FA9</td></tr>
<tr><td>_lwcommercial_wallshort</td><td>0x8536E25A</td><td>No</td><td>577</td><td>0x80005BFB</td><td>0x00003A09</td></tr>
<tr><td>_lwcommericial_sidewalk</td><td>0x09956D5D</td><td>No</td><td>564</td><td>0x80005BEB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_mar_commercial_road10</td><td>0x91F629C1</td><td>No</td><td>2474</td><td>0x800084CF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_mar_commercial_road10CleanT20</td><td>0x74DF8F86</td><td>No</td><td>2457</td><td>0x800084BD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_mar_commercial_road10CleanT20b</td><td>0x48A1801C</td><td>No</td><td>3952</td><td>0x80009940</td><td>0x0001113B</td></tr>
<tr><td>_mar_commercial_road10cross</td><td>0xC3E48B27</td><td>No</td><td>2459</td><td>0x800084BF</td><td>0x00000D6D</td></tr>
<tr><td>_mar_commercial_road10cross5</td><td>0x6B83FC64</td><td>No</td><td>2458</td><td>0x800084BE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_mar_commercial_road10L</td><td>0x38E9EC77</td><td>No</td><td>2460</td><td>0x800084C0</td><td>0x00000BED</td></tr>
<tr><td>_mar_commercial_road10middle</td><td>0x7EEB16A2</td><td>No</td><td>2461</td><td>0x800084C1</td><td>0x000046ED</td></tr>
<tr><td>_mar_commercial_road10T</td><td>0xD8AEBE2F</td><td>No</td><td>2462</td><td>0x800084C3</td><td>0x00006969</td></tr>
<tr><td>_mar_commercial_road10T5</td><td>0xBDFA441C</td><td>No</td><td>2473</td><td>0x800084CE</td><td>0x00006CD9</td></tr>
<tr><td>_mar_commercial_road20</td><td>0xFC8D7070</td><td>No</td><td>3955</td><td>0x80009943</td><td>0x0000A72D</td></tr>
<tr><td>_mar_commercial_road20b</td><td>0xCC1D6246</td><td>No</td><td>3956</td><td>0x80009944</td><td>0x0000D004</td></tr>
<tr><td>_mar_commercial_road20Clean</td><td>0x712FF8A7</td><td>No</td><td>2463</td><td>0x800084C4</td><td>0x0000C3EA</td></tr>
<tr><td>_mar_commercial_road20Cleanb</td><td>0x3C0F587F</td><td>No</td><td>2464</td><td>0x800084C5</td><td>0x000125D9</td></tr>
<tr><td>_mar_commercial_road20Cleancross</td><td>0xAA7D480D</td><td>No</td><td>2466</td><td>0x800084C7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_mar_commercial_road20Cleancross10</td><td>0x87F4A77A</td><td>No</td><td>2465</td><td>0x800084C6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_mar_commercial_road20CleanT</td><td>0x53E25EA9</td><td>No</td><td>2468</td><td>0x800084C9</td><td>0x0000798E</td></tr>
<tr><td>_mar_commercial_road20CleanT10</td><td>0xA28513D6</td><td>No</td><td>2467</td><td>0x800084C8</td><td>0x0000CF7D</td></tr>
<tr><td>_mar_commercial_road20CleanTn10</td><td>0x0B479E3A</td><td>No</td><td>4609</td><td>0x80009FA1</td><td>0x00001992</td></tr>
<tr><td>_mar_commercial_road5</td><td>0x97C83377</td><td>No</td><td>2472</td><td>0x800084CD</td><td>0x0000ECC0</td></tr>
<tr><td>_mar_commercial_road5cross</td><td>0x2EF8BE9D</td><td>No</td><td>2453</td><td>0x800084B9</td><td>0x000126E9</td></tr>
<tr><td>_mar_commercial_road5L</td><td>0xC5C2EBE1</td><td>No</td><td>2454</td><td>0x800084BA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_mar_commercial_road5T</td><td>0xA5D64139</td><td>No</td><td>2456</td><td>0x800084BC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_mar_commercial_road5T10</td><td>0x3BCB5766</td><td>No</td><td>2455</td><td>0x800084BB</td><td>0x0001273A</td></tr>
<tr><td>_mar_commercial_roadgovnt</td><td>0x3BDDA0B0</td><td>No</td><td>2469</td><td>0x800084CA</td><td>0x00013BE1</td></tr>
<tr><td>_mar_commercial_roadstraight10</td><td>0xD7555B37</td><td>No</td><td>2471</td><td>0x800084CC</td><td>0x000061D0</td></tr>
<tr><td>_mar_commercial_roadstraight10_crater02</td><td>0x29AC88F1</td><td>No</td><td>5268</td><td>0x8000A7BF</td><td>0x00000C72</td></tr>
<tr><td>_mar_commercial_roadstraight10_crater02_straight</td><td>0x92BB2EDA</td><td>No</td><td>5271</td><td>0x8000A7C2</td><td>0x000065FD</td></tr>
<tr><td>_mar_commercial_roadstraight20</td><td>0x8E524612</td><td>No</td><td>3953</td><td>0x80009941</td><td>0x0000A1AB</td></tr>
<tr><td>_mar_commercial_roadstraight20_crater02</td><td>0x406C869A</td><td>No</td><td>5269</td><td>0x8000A7C0</td><td>0x00002D66</td></tr>
<tr><td>_mar_commercial_roadstraight20b</td><td>0xA2F94540</td><td>No</td><td>3954</td><td>0x80009942</td><td>0x00012B2C</td></tr>
<tr><td>_mar_commercial_roadstraight5</td><td>0x6762E351</td><td>No</td><td>2470</td><td>0x800084CB</td><td>0x0000E22C</td></tr>
<tr><td>_mar_commercial_sidewalk</td><td>0x8B20070A</td><td>No</td><td>3950</td><td>0x8000993D</td><td>0x0000B735</td></tr>
<tr><td>_mar_commercial_sidewalksmall</td><td>0x8C838753</td><td>No</td><td>3951</td><td>0x8000993E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_mar_global_freewayelevatedcurve</td><td>0x280EE8BB</td><td>No</td><td>3959</td><td>0x80009949</td><td>0x00003FB9</td></tr>
<tr><td>_mar_global_freewayelevatedlong</td><td>0x4D4BBB94</td><td>No</td><td>3957</td><td>0x80009947</td><td>0x00000C54</td></tr>
<tr><td>_mar_global_freewayelevatedlongramp</td><td>0xB7D50350</td><td>No</td><td>3958</td><td>0x80009948</td><td>0x00001C82</td></tr>
<tr><td>_maracaibo_bld_civic02</td><td>0xA7C99C9D</td><td>No</td><td>1278</td><td>0x80006D7E</td><td>0x00002E41</td></tr>
<tr><td>_maracaibo_bld_civic02_ruined</td><td>0x77B548B1</td><td>No</td><td>3581</td><td>0x800093D9</td><td>0x00010750</td></tr>
<tr><td>_maracaibo_bld_corner16x32A</td><td>0xC62F60FD</td><td>No</td><td>1279</td><td>0x80006D7F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bld_corner16x32A_ruined</td><td>0x7F3E0211</td><td>No</td><td>3582</td><td>0x800093DA</td><td>0x0001334E</td></tr>
<tr><td>_maracaibo_bld_corner16x32B</td><td>0x4427D892</td><td>No</td><td>1280</td><td>0x80006D80</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bld_corner32x32A</td><td>0x96BE4F13</td><td>No</td><td>1287</td><td>0x80006D87</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bld_corner32x32A_ruined</td><td>0x18844117</td><td>No</td><td>3583</td><td>0x800093DB</td><td>0x00004070</td></tr>
<tr><td>_maracaibo_bld_corner32x32B</td><td>0xBCC0C97C</td><td>No</td><td>1288</td><td>0x80006D88</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bld_corner32x32B_ruined</td><td>0x45E7C96A</td><td>No</td><td>3584</td><td>0x800093DC</td><td>0x0000717E</td></tr>
<tr><td>_maracaibo_bld_firestation01</td><td>0xF46E2154</td><td>No</td><td>1281</td><td>0x80006D81</td><td>0x00004225</td></tr>
<tr><td>_maracaibo_bld_firestation01_ruined</td><td>0x5653AD62</td><td>No</td><td>3585</td><td>0x800093DD</td><td>0x00000B4D</td></tr>
<tr><td>_maracaibo_bld_gasstation02</td><td>0xDB2D4070</td><td>No</td><td>5466</td><td>0x8000AA62</td><td>0x00008D07</td></tr>
<tr><td>_maracaibo_bld_gasstationpump02</td><td>0x7AFCD1DE</td><td>No</td><td>5465</td><td>0x8000AA61</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bld_historical01</td><td>0xB884051E</td><td>No</td><td>1292</td><td>0x80006D8C</td><td>0x0000F4CB</td></tr>
<tr><td>_maracaibo_bld_historical01_ruined</td><td>0xAEB40DC4</td><td>No</td><td>3586</td><td>0x800093DE</td><td>0x000008FC</td></tr>
<tr><td>_maracaibo_bld_historical02</td><td>0xDA8AF669</td><td>No</td><td>1293</td><td>0x80006D8D</td><td>0x00011D94</td></tr>
<tr><td>_maracaibo_bld_historical02_ruined</td><td>0x6C7B7E7D</td><td>No</td><td>3587</td><td>0x800093DF</td><td>0x00009399</td></tr>
<tr><td>_maracaibo_bld_hospital01</td><td>0xFD7C87F8</td><td>No</td><td>1282</td><td>0x80006D82</td><td>0x0000ED9F</td></tr>
<tr><td>_maracaibo_bld_hospital01_ruined</td><td>0x45A39DC6</td><td>No</td><td>3588</td><td>0x800093E0</td><td>0x000028EB</td></tr>
<tr><td>_maracaibo_bld_parkingstructure01</td><td>0x3458A081</td><td>No</td><td>1283</td><td>0x80006D83</td><td>0x0000106F</td></tr>
<tr><td>_maracaibo_bld_parkingstructure01_ruined</td><td>0x9422BDD5</td><td>No</td><td>3589</td><td>0x800093E1</td><td>0x0000F7DA</td></tr>
<tr><td>_maracaibo_bld_parkingstructure02</td><td>0xB2511816</td><td>No</td><td>1289</td><td>0x80006D89</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bld_parkingstructure02_ruined</td><td>0x62B3989C</td><td>No</td><td>3590</td><td>0x800093E2</td><td>0x000116E9</td></tr>
<tr><td>_maracaibo_bld_segment16x32A</td><td>0x5BE0647B</td><td>No</td><td>1290</td><td>0x80006D8A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bld_segment16x32A_ruined</td><td>0xB6EA311F</td><td>No</td><td>4594</td><td>0x80009F90</td><td>0x00011E84</td></tr>
<tr><td>_maracaibo_bld_segment32x32A</td><td>0x8FE89365</td><td>No</td><td>1291</td><td>0x80006D8B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bld_segment32x32a_ruined</td><td>0x24A9ADF9</td><td>No</td><td>4149</td><td>0x80009B4C</td><td>0x00010CAF</td></tr>
<tr><td>_Maracaibo_bld_skyscraper01</td><td>0xEE40C9D5</td><td>No</td><td>1284</td><td>0x80006D84</td><td>0x0000D96F</td></tr>
<tr><td>_Maracaibo_bld_skyscraper01_ruined</td><td>0x0381E6E9</td><td>No</td><td>4595</td><td>0x80009F92</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bld_skyscraper02</td><td>0x4C390F0A</td><td>No</td><td>1285</td><td>0x80006D85</td><td>0x00011A0F</td></tr>
<tr><td>_maracaibo_bld_skyscraper02_ruined</td><td>0x251BB000</td><td>No</td><td>4603</td><td>0x80009F9A</td><td>0x0000E09E</td></tr>
<tr><td>_maracaibo_bld_skyscraper03</td><td>0x6E3B8327</td><td>No</td><td>1286</td><td>0x80006D86</td><td>0x0001212F</td></tr>
<tr><td>_maracaibo_bld_skyscraper03_ruined</td><td>0xD3D50F6B</td><td>No</td><td>4596</td><td>0x80009F93</td><td>0x000135C4</td></tr>
<tr><td>_maracaibo_bld_stagerepublica</td><td>0xFCC16614</td><td>No</td><td>1262</td><td>0x80006D06</td><td>0x00011CC4</td></tr>
<tr><td>_maracaibo_bld_stagerepublica_ruined</td><td>0xEBD16222</td><td>No</td><td>4598</td><td>0x80009F95</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_bridge_segmenta</td><td>0xCA48F45C</td><td>No</td><td>1042</td><td>0x8000691B</td><td>0x000099C5</td></tr>
<tr><td>_maracaibo_bridge_segmenta_ruined</td><td>0xE17AD34A</td><td>No</td><td>5848</td><td>0x8000AFA0</td><td>0x0000EF32</td></tr>
<tr><td>_maracaibo_bridge_segmentb</td><td>0xA44679F3</td><td>No</td><td>1046</td><td>0x8000691F</td><td>0x00007819</td></tr>
<tr><td>_maracaibo_fence01</td><td>0x39DE1AB0</td><td>No</td><td>3323</td><td>0x80008F88</td><td>0x0000AE64</td></tr>
<tr><td>_maracaibo_freewayascender01</td><td>0x9231CA13</td><td>No</td><td>1050</td><td>0x80006924</td><td>0x0000ECF6</td></tr>
<tr><td>_maracaibo_freewaystraight01</td><td>0x782ECFBE</td><td>No</td><td>1048</td><td>0x80006922</td><td>0x00007140</td></tr>
<tr><td>_maracaibo_freewaytrenchbridge01_overpass</td><td>0xFBDF9CB5</td><td>No</td><td>1235</td><td>0x80006CE9</td><td>0x0000B61A</td></tr>
<tr><td>_maracaibo_freewaytrenchbridge01_overpass_autobridge</td><td>0x86F4A062</td><td>No</td><td>558</td><td>0x80005BAD</td><td>0x00002444</td></tr>
<tr><td>_maracaibo_freewaytrenchbridge01_underpass</td><td>0xBC506E51</td><td>No</td><td>1049</td><td>0x80006923</td><td>0x0000DED3</td></tr>
<tr><td>_maracaibo_lampposta</td><td>0x6A5CCB23</td><td>No</td><td>1751</td><td>0x800075C0</td><td>0x0000D949</td></tr>
<tr><td>_maracaibo_lamppostb</td><td>0x505EE0CC</td><td>No</td><td>1720</td><td>0x8000759B</td><td>0x0000D76E</td></tr>
<tr><td>_maracaibo_obelisk</td><td>0x536E7991</td><td>No</td><td>1719</td><td>0x8000759A</td><td>0x000082EC</td></tr>
<tr><td>_maracaibo_obelisk_ruined</td><td>0xF6667AA5</td><td>No</td><td>4599</td><td>0x80009F96</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_outskirtbridge20cross10</td><td>0x158ABA19</td><td>No</td><td>1066</td><td>0x80006936</td><td>0x0001315A</td></tr>
<tr><td>_maracaibo_outskirtbridge20cross20</td><td>0xA0223328</td><td>No</td><td>1226</td><td>0x80006CD8</td><td>0x0000A6E0</td></tr>
<tr><td>_maracaibo_park</td><td>0x88281132</td><td>No</td><td>1263</td><td>0x80006D07</td><td>0x0000179B</td></tr>
<tr><td>_maracaibo_signgastall</td><td>0x1EFCC969</td><td>No</td><td>5467</td><td>0x8000AA63</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaibo_wall06m</td><td>0xA94F1195</td><td>No</td><td>1721</td><td>0x8000759C</td><td>0x0000487B</td></tr>
<tr><td>_maracaibo_wall10m</td><td>0xB70FB362</td><td>No</td><td>1722</td><td>0x8000759D</td><td>0x0000EB6F</td></tr>
<tr><td>_maracaibo_wall20m</td><td>0xCBC798B5</td><td>No</td><td>1723</td><td>0x8000759E</td><td>0x0000732F</td></tr>
<tr><td>_maracaiboruins_bld_govtbld</td><td>0x97B3BDF0</td><td>No</td><td>5470</td><td>0x8000AA66</td><td>0x00005ECE</td></tr>
<tr><td>_maracaiboruins_bld_historical01</td><td>0xF7373837</td><td>No</td><td>5471</td><td>0x8000AA67</td><td>0x00012E2E</td></tr>
<tr><td>_maracaiboruins_bld_historical02</td><td>0x0D399970</td><td>No</td><td>5472</td><td>0x8000AA68</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaiboruins_bld_radiotower</td><td>0x462A2536</td><td>No</td><td>5474</td><td>0x8000AA6A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaiboruins_bld_skyscraper01</td><td>0x74C3B028</td><td>No</td><td>5473</td><td>0x8000AA69</td><td>0xFFFFFFFF</td></tr>
<tr><td>_maracaiboruins_bld_skyscraper02</td><td>0xFEC0B7CF</td><td>No</td><td>5475</td><td>0x8000AA6B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_margarita_bld_bank</td><td>0x5CDA4ADE</td><td>No</td><td>2708</td><td>0x80008706</td><td>0x0000287C</td></tr>
<tr><td>_margarita_bld_club01</td><td>0xF96F58AD</td><td>No</td><td>6046</td><td>0x9000019E</td><td>0x00007C46</td></tr>
<tr><td>_margarita_bld_condo01</td><td>0x6176308A</td><td>No</td><td>6047</td><td>0x9000019F</td><td>0x0000DAFD</td></tr>
<tr><td>_margarita_bld_hotelresort01</td><td>0xC5FD29D0</td><td>No</td><td>6048</td><td>0x900001A0</td><td>0x00004BF1</td></tr>
<tr><td>_margarita_env_trench</td><td>0x39DB7CF3</td><td>No</td><td>2107</td><td>0x8000817E</td><td>0x0000AE8A</td></tr>
<tr><td>_Margarita_hotelpool</td><td>0x3116A4C3</td><td>No</td><td>6052</td><td>0x900001A4</td><td>0x0000214F</td></tr>
<tr><td>_marsh_bridge02end</td><td>0x88861CC8</td><td>No</td><td>4766</td><td>0x8000A179</td><td>0xFFFFFFFF</td></tr>
<tr><td>_marsh_bridge02end_ruined</td><td>0xA5D4FCD6</td><td>No</td><td>3562</td><td>0x800093C5</td><td>0x0000F160</td></tr>
<tr><td>_marsh_bridge02mid</td><td>0xEF0E2A55</td><td>No</td><td>4767</td><td>0x8000A17A</td><td>0x0000C520</td></tr>
<tr><td>_marsh_bridge02mid_ruined</td><td>0xA60D8469</td><td>No</td><td>3561</td><td>0x800093C4</td><td>0x0000AEB6</td></tr>
<tr><td>_marsh_bridgeend</td><td>0x65A33902</td><td>No</td><td>6050</td><td>0x900001A2</td><td>0x0000E0B4</td></tr>
<tr><td>_marsh_bridgeend_ruined</td><td>0x5D156A78</td><td>No</td><td>3559</td><td>0x800093C2</td><td>0x0000819B</td></tr>
<tr><td>_marsh_bridgemid</td><td>0xD50BB3E3</td><td>No</td><td>6049</td><td>0x900001A1</td><td>0x00006ECD</td></tr>
<tr><td>_marsh_bridgemid_AIcollision</td><td>0xB2DEFAA0</td><td>No</td><td>4769</td><td>0x8000A17D</td><td>0x0000E69F</td></tr>
<tr><td>_marsh_bridgemid_ruined</td><td>0x738CF0E7</td><td>No</td><td>3560</td><td>0x800093C3</td><td>0x00002239</td></tr>
<tr><td>_marsh_bridgerailing01</td><td>0xB94918F4</td><td>No</td><td>4777</td><td>0x8000A185</td><td>0xFFFFFFFF</td></tr>
<tr><td>_marsh_bridgerailing02</td><td>0x93469E8B</td><td>No</td><td>4778</td><td>0x8000A186</td><td>0x0000B9F6</td></tr>
<tr><td>_Marsh_env_treewater02</td><td>0xB5E63803</td><td>No</td><td>3251</td><td>0x80008F2C</td><td>0x00012E57</td></tr>
<tr><td>_merida_bld_hotel</td><td>0x37B0D170</td><td>No</td><td>80</td><td>0x80004B38</td><td>0x00007425</td></tr>
<tr><td>_merida_bld_hotel_ruined</td><td>0x680C3DDE</td><td>No</td><td>3283</td><td>0x80008F54</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_bld_lockerroom</td><td>0xB7513987</td><td>No</td><td>370</td><td>0x80005105</td><td>0x0000E65F</td></tr>
<tr><td>_merida_bld_mediabooth</td><td>0x2E14153A</td><td>No</td><td>448</td><td>0x800055F0</td><td>0x00005D73</td></tr>
<tr><td>_merida_bld_oilwellland</td><td>0x6AFE8CA5</td><td>No</td><td>351</td><td>0x80004EFB</td><td>0x0001406A</td></tr>
<tr><td>_merida_bld_oilwellland_ruined</td><td>0x4AD66939</td><td>No</td><td>5845</td><td>0x8000AF9D</td><td>0x000004A3</td></tr>
<tr><td>_merida_bld_oilwellwater</td><td>0x1ABC2EF7</td><td>No</td><td>286</td><td>0x80004DE7</td><td>0x000036D9</td></tr>
<tr><td>_merida_bld_plazachurch</td><td>0x2285EF81</td><td>No</td><td>125</td><td>0x80004CC7</td><td>0x00000966</td></tr>
<tr><td>_merida_bld_pmcautoshop</td><td>0x021C6B27</td><td>No</td><td>6107</td><td>0x900001E4</td><td>0x0000CBAF</td></tr>
<tr><td>_merida_bld_pmcautoshop_interior</td><td>0x22E0FB26</td><td>No</td><td>4759</td><td>0x8000A172</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_bld_soccerstadium</td><td>0x680E4358</td><td>No</td><td>287</td><td>0x80004DE8</td><td>0x0000B8EB</td></tr>
<tr><td>_merida_bld_tickets</td><td>0xE0439E0D</td><td>No</td><td>363</td><td>0x800050FA</td><td>0x00002582</td></tr>
<tr><td>_merida_bld_universityadmin</td><td>0x6E6D6867</td><td>No</td><td>288</td><td>0x80004DE9</td><td>0x0000CA0D</td></tr>
<tr><td>_merida_bld_universityadmin_ruined</td><td>0x3C46A0AB</td><td>No</td><td>3281</td><td>0x80008F52</td><td>0x0000360E</td></tr>
<tr><td>_merida_bld_universitycampus</td><td>0x249D52B1</td><td>No</td><td>289</td><td>0x80004DEA</td><td>0x00011F07</td></tr>
<tr><td>_merida_bld_universitycampus_ruined</td><td>0xD62412C5</td><td>No</td><td>3280</td><td>0x80008F51</td><td>0x000107DC</td></tr>
<tr><td>_merida_bld_universitydorm</td><td>0x701657EA</td><td>No</td><td>290</td><td>0x80004DEB</td><td>0x0001369B</td></tr>
<tr><td>_merida_bld_universitydorm_ruined</td><td>0xDF2AFE60</td><td>No</td><td>3282</td><td>0x80008F53</td><td>0x0000E1FF</td></tr>
<tr><td>_merida_bld_universitylibrary</td><td>0x9FC4B9D3</td><td>No</td><td>291</td><td>0x80004DEC</td><td>0x0000CCDC</td></tr>
<tr><td>_merida_busstop</td><td>0xE4BFA2F7</td><td>No</td><td>192</td><td>0x80004D16</td><td>0x00010341</td></tr>
<tr><td>_merida_env_plazabush01</td><td>0x498D0238</td><td>No</td><td>193</td><td>0x80004D17</td><td>0x000035DC</td></tr>
<tr><td>_merida_env_plazabush02</td><td>0xD38A09DF</td><td>No</td><td>194</td><td>0x80004D18</td><td>0x0000E1DF</td></tr>
<tr><td>_merida_env_plazaflowers01</td><td>0x6A3D407C</td><td>No</td><td>195</td><td>0x80004D19</td><td>0x000103C3</td></tr>
<tr><td>_merida_env_plazaflowers02</td><td>0x443AC613</td><td>No</td><td>196</td><td>0x80004D1A</td><td>0x00011E68</td></tr>
<tr><td>_merida_env_plazahedgecorner</td><td>0x7432AC69</td><td>No</td><td>197</td><td>0x80004D1B</td><td>0x0001279E</td></tr>
<tr><td>_merida_env_plazahedgestraight</td><td>0xE722F488</td><td>No</td><td>198</td><td>0x80004D1C</td><td>0x0001281C</td></tr>
<tr><td>_merida_env_plazahedgestraightlong</td><td>0x5F443962</td><td>No</td><td>369</td><td>0x80005104</td><td>0x00005DE0</td></tr>
<tr><td>_merida_env_plazalawn01</td><td>0x99831304</td><td>No</td><td>148</td><td>0x80004CDF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_env_plazalawn02</td><td>0x338033DB</td><td>No</td><td>147</td><td>0x80004CDE</td><td>0x00002F03</td></tr>
<tr><td>_merida_env_plazalawn03</td><td>0x117DBFBE</td><td>No</td><td>144</td><td>0x80004CDB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_env_plazalawn04</td><td>0x1B8F189D</td><td>No</td><td>143</td><td>0x80004CDA</td><td>0x0000B935</td></tr>
<tr><td>_merida_fencemetalgatea</td><td>0x2A7A250F</td><td>No</td><td>208</td><td>0x80004D27</td><td>0x00005B2C</td></tr>
<tr><td>_merida_fencemetallonga</td><td>0xE2687D0A</td><td>No</td><td>209</td><td>0x80004D8F</td><td>0x00006F66</td></tr>
<tr><td>_merida_fencemetalshorta</td><td>0xBF13D504</td><td>No</td><td>210</td><td>0x80004D90</td><td>0x00007B48</td></tr>
<tr><td>_merida_lawna</td><td>0x570BCE56</td><td>No</td><td>207</td><td>0x80004D26</td><td>0x00011A8B</td></tr>
<tr><td>_merida_lightstadiuma</td><td>0x4A07F687</td><td>No</td><td>446</td><td>0x800055EE</td><td>0x00000D47</td></tr>
<tr><td>_merida_lightstadiumb</td><td>0x2009F300</td><td>No</td><td>447</td><td>0x800055EF</td><td>0x00009E2F</td></tr>
<tr><td>_merida_market01</td><td>0x684D96AE</td><td>No</td><td>202</td><td>0x80004D21</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_market02</td><td>0xCA54ECB9</td><td>No</td><td>203</td><td>0x80004D22</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_market03</td><td>0xF052E9F4</td><td>No</td><td>211</td><td>0x80004D91</td><td>0x0000D4AF</td></tr>
<tr><td>_merida_market04</td><td>0x525A3FFF</td><td>No</td><td>212</td><td>0x80004D92</td><td>0x0000B558</td></tr>
<tr><td>_merida_market05</td><td>0xF0576722</td><td>No</td><td>204</td><td>0x80004D23</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_parkingplantercorner</td><td>0x24AA8196</td><td>No</td><td>149</td><td>0x80004CE0</td><td>0x0000C4A5</td></tr>
<tr><td>_merida_parkingplanterstraight</td><td>0xFA16CE7F</td><td>No</td><td>213</td><td>0x80004D93</td><td>0x0000434C</td></tr>
<tr><td>_merida_plateau01</td><td>0x05DF6F22</td><td>No</td><td>5430</td><td>0x8000A9F8</td><td>0x000085C5</td></tr>
<tr><td>_merida_plazabench</td><td>0x3D2755E3</td><td>No</td><td>205</td><td>0x80004D24</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_plazalampost</td><td>0x6A2E2FE1</td><td>No</td><td>214</td><td>0x80004D94</td><td>0x0000F99B</td></tr>
<tr><td>_merida_plazastatue</td><td>0x070CC4DF</td><td>No</td><td>215</td><td>0x80004D95</td><td>0x000021E3</td></tr>
<tr><td>_merida_plazawaterfountain</td><td>0x6C6052A8</td><td>No</td><td>216</td><td>0x80004D96</td><td>0x0000D3D5</td></tr>
<tr><td>_merida_pmcautoshop_sportscar</td><td>0xB88DBED4</td><td>No</td><td>5435</td><td>0x8000A9FD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_signa</td><td>0x1F0BBF11</td><td>No</td><td>206</td><td>0x80004D25</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_signb</td><td>0x9D0436A6</td><td>No</td><td>219</td><td>0x80004D99</td><td>0x000094C1</td></tr>
<tr><td>_merida_signc</td><td>0xBF06AAC3</td><td>No</td><td>220</td><td>0x80004D9A</td><td>0x00010975</td></tr>
<tr><td>_merida_signfolda</td><td>0xFBC54A56</td><td>No</td><td>221</td><td>0x80004D9B</td><td>0x00013390</td></tr>
<tr><td>_merida_signfoldb</td><td>0x7DCCD2C1</td><td>No</td><td>222</td><td>0x80004D9C</td><td>0x0000BCC9</td></tr>
<tr><td>_merida_signfoldc</td><td>0x83CA9D9C</td><td>No</td><td>223</td><td>0x80004D9D</td><td>0x0000BB4E</td></tr>
<tr><td>_merida_soccerfield</td><td>0xB8F19856</td><td>No</td><td>142</td><td>0x80004CD9</td><td>0x00010E6A</td></tr>
<tr><td>_merida_telephonepole</td><td>0x7586F083</td><td>No</td><td>217</td><td>0x80004D97</td><td>0x0000F4E2</td></tr>
<tr><td>_merida_universityfence</td><td>0x1EA223DA</td><td>No</td><td>218</td><td>0x80004D98</td><td>0x000009C6</td></tr>
<tr><td>_merida_universitylamppost</td><td>0x0D0323AB</td><td>No</td><td>362</td><td>0x800050F7</td><td>0x000058F4</td></tr>
<tr><td>_merida_universitylibraryplateau01</td><td>0xCD4E6943</td><td>No</td><td>5459</td><td>0x8000AA5A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_merida_universitypicnictable</td><td>0x71C293FF</td><td>No</td><td>224</td><td>0x80004DA1</td><td>0x0000F597</td></tr>
<tr><td>_merida_universitystatue</td><td>0xB5DD5B9B</td><td>No</td><td>225</td><td>0x80004DA2</td><td>0x00002CB0</td></tr>
<tr><td>_mountain_blastdoors</td><td>0xE1DF0AF5</td><td>No</td><td>2688</td><td>0x800086DF</td><td>0x0000701A</td></tr>
<tr><td>_mountain_blastdoors_invincible</td><td>0xB8FEB0DB</td><td>No</td><td>2538</td><td>0x80008565</td><td>0x0000C768</td></tr>
<tr><td>_mountain_blastdoors_stitcher</td><td>0x49BD7FB2</td><td>No</td><td>2687</td><td>0x800086DE</td><td>0x00001136</td></tr>
<tr><td>_mountain_bld_bunkerdestroyed</td><td>0x653621C7</td><td>No</td><td>2689</td><td>0x800086E0</td><td>0x00004269</td></tr>
<tr><td>_NOT YET ORGANIZED</td><td>0x90356F04</td><td>No</td><td>500</td><td>0x800056D1</td><td>0x000028D6</td></tr>
<tr><td>_ocoutpost_bench</td><td>0x5602C117</td><td>No</td><td>1845</td><td>0x800076DB</td><td>0x0001146C</td></tr>
<tr><td>_ocoutpost_bld_alarmtower</td><td>0xDDD6DD04</td><td>No</td><td>5456</td><td>0x8000AA57</td><td>0x0000C3CA</td></tr>
<tr><td>_ocoutpost_bld_guardpost01</td><td>0x9013EE16</td><td>No</td><td>2047</td><td>0x800080E1</td><td>0x000131C0</td></tr>
<tr><td>_ocoutpost_bld_guardpost01_gate</td><td>0xD6CFC6E8</td><td>No</td><td>3767</td><td>0x80009729</td><td>0xFFFFFFFF</td></tr>
<tr><td>_ocoutpost_bld_helipad</td><td>0x22C3FE09</td><td>Yes</td><td>3761</td><td>0x80009723</td><td>0x00011A92</td></tr>
<tr><td>_ocoutpost_bld_hq</td><td>0x5467DE77</td><td>No</td><td>1473</td><td>0x80007018</td><td>0x0000FEB7</td></tr>
<tr><td>_ocoutpost_bld_hq_ruined</td><td>0x7657A87B</td><td>No</td><td>5844</td><td>0x8000AF9A</td><td>0x0000E61A</td></tr>
<tr><td>_ocoutpost_bld_radiotower</td><td>0x348A63CA</td><td>No</td><td>1533</td><td>0x80007184</td><td>0x0000BCE8</td></tr>
<tr><td>_ocoutpost_bld_radiotower_ruined</td><td>0x9FAA7BC0</td><td>No</td><td>4605</td><td>0x80009F9C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_ocoutpost_bld_warehouse01</td><td>0x16A8A38A</td><td>No</td><td>1367</td><td>0x80006ED4</td><td>0x00007CFD</td></tr>
<tr><td>_ocoutpost_desklobby</td><td>0x1AE7E19C</td><td>No</td><td>1508</td><td>0x8000716B</td><td>0x0001359A</td></tr>
<tr><td>_ocoutpost_expandablevan_prop</td><td>0x8C028676</td><td>No</td><td>1947</td><td>0x80007F8D</td><td>0x0001266F</td></tr>
<tr><td>_ocoutpost_exterior_job</td><td>0xD17FCAC9</td><td>No</td><td>2378</td><td>0x80008336</td><td>0x00008CD6</td></tr>
<tr><td>_ocoutpost_fountain01</td><td>0xB6D866E6</td><td>No</td><td>1510</td><td>0x8000716D</td><td>0x00002156</td></tr>
<tr><td>_ocoutpost_fountainentrance</td><td>0x721F6649</td><td>No</td><td>1509</td><td>0x8000716C</td><td>0x0000CE9E</td></tr>
<tr><td>_ocoutpost_fueltanks</td><td>0xF00C7A06</td><td>Yes</td><td>4543</td><td>0x80009F18</td><td>0x00002F67</td></tr>
<tr><td>_ocoutpost_guardtower</td><td>0x231B6EC5</td><td>No</td><td>1841</td><td>0x800076D7</td><td>0x000013BC</td></tr>
<tr><td>_ocoutpost_hqbase</td><td>0xDB8F74AD</td><td>No</td><td>1474</td><td>0x80007019</td><td>0x000103EF</td></tr>
<tr><td>_ocoutpost_hqbaseIntersection</td><td>0x5D5506B6</td><td>No</td><td>1856</td><td>0x800076E7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_ocoutpost_hqplaza</td><td>0x5A59F8D0</td><td>No</td><td>1475</td><td>0x8000701A</td><td>0x00012AED</td></tr>
<tr><td>_ocoutpost_interior_job</td><td>0xCD2388CF</td><td>No</td><td>4757</td><td>0x8000A170</td><td>0xFFFFFFFF</td></tr>
<tr><td>_ocoutpost_planter01</td><td>0xC0A23CEA</td><td>No</td><td>1532</td><td>0x80007183</td><td>0x000099A4</td></tr>
<tr><td>_ocoutpost_statueoil</td><td>0x70364271</td><td>No</td><td>1516</td><td>0x80007173</td><td>0x00007824</td></tr>
<tr><td>_ocoutpost_tablearmwrestling</td><td>0xE91AC6DE</td><td>No</td><td>1855</td><td>0x800076E6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_ocoutpost_wallcorner</td><td>0x6960908C</td><td>No</td><td>1847</td><td>0x800076DD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_ocoutpost_wallgate</td><td>0xA893A52E</td><td>No</td><td>1842</td><td>0x800076D8</td><td>0x00006FD0</td></tr>
<tr><td>_ocoutpost_wallLong</td><td>0xF30CBF21</td><td>No</td><td>1843</td><td>0x800076D9</td><td>0x0000715D</td></tr>
<tr><td>_ocoutpost_wallShort</td><td>0x037D306F</td><td>No</td><td>1844</td><td>0x800076DA</td><td>0x0000A817</td></tr>
<tr><td>_oilrig_att_towerdrillspeakersA</td><td>0x08AA2E32</td><td>No</td><td>5423</td><td>0x8000A9F0</td><td>0x00005376</td></tr>
<tr><td>_oilrig_bld_helipadsmalla</td><td>0x30086385</td><td>Yes</td><td>947</td><td>0x800065E0</td><td>0x00006AAE</td></tr>
<tr><td>_oilrig_fueltanklargeA</td><td>0xE754321B</td><td>Yes</td><td>412</td><td>0x80005587</td><td>0xFFFFFFFF</td></tr>
<tr><td>_oilrig_tankmedA</td><td>0x268F6EBA</td><td>Yes</td><td>733</td><td>0x800061EE</td><td>0x000120DB</td></tr>
<tr><td>_oilrig_tanksmallA</td><td>0x59F415BB</td><td>Yes</td><td>407</td><td>0x8000557D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_oilrig_tanktallA</td><td>0x80FB9C09</td><td>Yes</td><td>411</td><td>0x80005583</td><td>0x0001388C</td></tr>
<tr><td>_outpost_bld_farming01</td><td>0xE680454D</td><td>No</td><td>2697</td><td>0x800086F4</td><td>0x00000A2D</td></tr>
<tr><td>_outpost_bld_farming01_true</td><td>0x12BAD0A8</td><td>No</td><td>5150</td><td>0x8000A488</td><td>0x0000FA58</td></tr>
<tr><td>_outpost_bld_govtbld</td><td>0x02B87F56</td><td>No</td><td>1277</td><td>0x80006D7D</td><td>0x00002F3F</td></tr>
<tr><td>_outpost_bld_govtbld_ruined</td><td>0x235B62DC</td><td>No</td><td>4600</td><td>0x80009F97</td><td>0xFFFFFFFF</td></tr>
<tr><td>_outpost_bld_municipal</td><td>0x6F5867C8</td><td>No</td><td>2690</td><td>0x800086EC</td><td>0x00011DED</td></tr>
<tr><td>_outpost_bld_municipal_fence</td><td>0x6E814B6E</td><td>No</td><td>4990</td><td>0x8000A3A5</td><td>0x00005D70</td></tr>
<tr><td>_outpost_bld_municipal_true</td><td>0xE8F23753</td><td>No</td><td>5151</td><td>0x8000A489</td><td>0x00003702</td></tr>
<tr><td>_outpost_bld_office</td><td>0xF4152750</td><td>No</td><td>2699</td><td>0x800086F6</td><td>0x00009575</td></tr>
<tr><td>_outpost_bld_plantation02</td><td>0x1C316850</td><td>No</td><td>2698</td><td>0x800086F5</td><td>0x000048FF</td></tr>
<tr><td>_outpost_bld_shack</td><td>0xC461646C</td><td>No</td><td>2691</td><td>0x800086ED</td><td>0x00010E1C</td></tr>
<tr><td>_outpost_bld_vzwarehouselarge</td><td>0xE5A53D46</td><td>No</td><td>2443</td><td>0x800084AE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_outpost_bld_vzwarehouselarge_Ruined</td><td>0xD589554C</td><td>No</td><td>5231</td><td>0x8000A69A</td><td>0x0000F338</td></tr>
<tr><td>_outpost_bld_warehouse01</td><td>0xBAA777CC</td><td>No</td><td>2700</td><td>0x800086F7</td><td>0x00005189</td></tr>
<tr><td>_outskirt_bld_church</td><td>0xAC945F54</td><td>No</td><td>124</td><td>0x80004CC6</td><td>0x00012B7B</td></tr>
<tr><td>_outskirt_bld_church_ruined</td><td>0x381A7762</td><td>No</td><td>3949</td><td>0x8000993B</td><td>0x0000DAEA</td></tr>
<tr><td>_outskirt_bld_house01</td><td>0x49CD0782</td><td>No</td><td>138</td><td>0x80004CD5</td><td>0x0000EC88</td></tr>
<tr><td>_outskirt_bld_house02</td><td>0xCBD48FED</td><td>No</td><td>789</td><td>0x80006230</td><td>0x00002FE6</td></tr>
<tr><td>_outskirt_bld_house03</td><td>0xA1D20F38</td><td>No</td><td>6087</td><td>0x900001CE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_outskirt_bld_house04</td><td>0xA3C5466B</td><td>No</td><td>790</td><td>0x80006231</td><td>0x000056FC</td></tr>
<tr><td>_outskirt_bld_house05</td><td>0xC1C3370E</td><td>No</td><td>791</td><td>0x80006232</td><td>0x0000A966</td></tr>
<tr><td>_outskirt_bld_house06</td><td>0x23CA8D19</td><td>No</td><td>802</td><td>0x8000623D</td><td>0x00003559</td></tr>
<tr><td>_outskirt_bld_market01</td><td>0x3B8A7310</td><td>No</td><td>137</td><td>0x80004CD4</td><td>0x0000E905</td></tr>
<tr><td>_outskirt_bld_market02</td><td>0x258811D7</td><td>No</td><td>136</td><td>0x80004CD3</td><td>0x0000275D</td></tr>
<tr><td>_outskirt_bld_market03</td><td>0xC38538FA</td><td>No</td><td>133</td><td>0x80004CD0</td><td>0x0000C1D0</td></tr>
<tr><td>_outskirt_bld_market04</td><td>0x9D82BE91</td><td>No</td><td>132</td><td>0x80004CCF</td><td>0x0000ABAA</td></tr>
<tr><td>_outskirt_bld_market05</td><td>0xA380896C</td><td>No</td><td>131</td><td>0x80004CCE</td><td>0x0000BBC7</td></tr>
<tr><td>_outskirt_bld_mercbar</td><td>0x09569D2D</td><td>No</td><td>6073</td><td>0x900001B9</td><td>0x000127CF</td></tr>
<tr><td>_outskirt_chickenfencelong</td><td>0x4E7E161A</td><td>No</td><td>433</td><td>0x800055CF</td><td>0x00010011</td></tr>
<tr><td>_outskirt_chickenfenceshort</td><td>0x68A053F2</td><td>No</td><td>432</td><td>0x800055CE</td><td>0x000000AC</td></tr>
<tr><td>_outskirt_curb</td><td>0x6A727450</td><td>No</td><td>431</td><td>0x800055CD</td><td>0x00004C20</td></tr>
<tr><td>_outskirt_road10</td><td>0xF0310CAD</td><td>No</td><td>292</td><td>0x80004DED</td><td>0xFFFFFFFF</td></tr>
<tr><td>_outskirt_road10cross</td><td>0xCB93CBD3</td><td>No</td><td>293</td><td>0x80004DEF</td><td>0x0000E21D</td></tr>
<tr><td>_outskirt_road10crossboth</td><td>0x7E4A171E</td><td>No</td><td>1224</td><td>0x80006CD6</td><td>0x000016BB</td></tr>
<tr><td>_outskirt_road10merge</td><td>0x4FEB7927</td><td>No</td><td>3312</td><td>0x80008F7C</td><td>0x0000F5A3</td></tr>
<tr><td>_outskirt_road10straight</td><td>0xBFD970C7</td><td>No</td><td>2028</td><td>0x800080CB</td><td>0x0000125C</td></tr>
<tr><td>_outskirt_road10t</td><td>0xBC8B0D5B</td><td>No</td><td>294</td><td>0x80004DF2</td><td>0x000045A1</td></tr>
<tr><td>_outskirt_road10t02</td><td>0x23D6B321</td><td>No</td><td>2039</td><td>0x800080D7</td><td>0x0000D632</td></tr>
<tr><td>_outskirt_road10t20</td><td>0xCAA2D8C9</td><td>No</td><td>2027</td><td>0x800080CA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_outskirt_road10t5</td><td>0x3DB6C788</td><td>No</td><td>3553</td><td>0x800093BB</td><td>0x00007269</td></tr>
<tr><td>_outskirt_road10tleft</td><td>0xADD46DE0</td><td>No</td><td>1070</td><td>0x8000693B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_outskirt_road10tright</td><td>0xF490DC47</td><td>No</td><td>1225</td><td>0x80006CD7</td><td>0x00007D52</td></tr>
<tr><td>_outskirt_road20</td><td>0x5AC8535C</td><td>No</td><td>437</td><td>0x800055D4</td><td>0x00001330</td></tr>
<tr><td>_outskirt_road20cross</td><td>0x97060AAC</td><td>No</td><td>439</td><td>0x800055D7</td><td>0x00002C06</td></tr>
<tr><td>_outskirt_road20cross10</td><td>0x981571F7</td><td>No</td><td>1035</td><td>0x80006914</td><td>0x00013B0E</td></tr>
<tr><td>_outskirt_road20crossboth</td><td>0xEABA162D</td><td>No</td><td>1071</td><td>0x8000693C</td><td>0x0000D5F3</td></tr>
<tr><td>_outskirt_road20straight</td><td>0x3104F53E</td><td>No</td><td>450</td><td>0x800055F2</td><td>0x0000BF5B</td></tr>
<tr><td>_outskirt_road20t</td><td>0x5FE12E9C</td><td>No</td><td>438</td><td>0x800055D6</td><td>0x00001052</td></tr>
<tr><td>_outskirt_road20t10</td><td>0xB3D1D8E7</td><td>No</td><td>443</td><td>0x800055E1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_outskirt_road20tleft</td><td>0x1CDD0373</td><td>No</td><td>1073</td><td>0x8000693E</td><td>0x00006954</td></tr>
<tr><td>_outskirt_road20tright</td><td>0x7341BA1A</td><td>No</td><td>1072</td><td>0x8000693D</td><td>0x00012DF3</td></tr>
<tr><td>_outskirt_road5</td><td>0x0D722943</td><td>No</td><td>1069</td><td>0x8000693A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_outskirt_road5T</td><td>0xBC50C2D5</td><td>No</td><td>3555</td><td>0x800093BD</td><td>0x00008FCA</td></tr>
<tr><td>_outskirt_road5T10</td><td>0x6430D3C2</td><td>No</td><td>3554</td><td>0x800093BC</td><td>0x0000332C</td></tr>
<tr><td>_outskirt_wallchurchcorner</td><td>0x973E3926</td><td>No</td><td>226</td><td>0x80004DA3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_outskirt_wallchurchlong</td><td>0x2CEA8063</td><td>No</td><td>227</td><td>0x80004DA4</td><td>0x00001DAC</td></tr>
<tr><td>_outskirt_wallchurchshort</td><td>0xE65D54F5</td><td>No</td><td>228</td><td>0x80004DA5</td><td>0x00002DDB</td></tr>
<tr><td>_pedestrian_x</td><td>0x703C9692</td><td>No</td><td>1261</td><td>0x80006D05</td><td>0x0000DCEF</td></tr>
<tr><td>_pirate_chaira</td><td>0x5D74EB8E</td><td>No</td><td>3804</td><td>0x800097C1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pirate_chairb</td><td>0xBF7C4199</td><td>No</td><td>3805</td><td>0x800097C2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pirate_chairb (Dancing)</td><td>0x7AE910C4</td><td>No</td><td>3810</td><td>0x800097CA</td><td>0x0001009C</td></tr>
<tr><td>_pmcoutpost_armyCot</td><td>0x770D34FC</td><td>No</td><td>4740</td><td>0x8000A15C</td><td>0x0000C550</td></tr>
<tr><td>_pmcoutpost_beerA</td><td>0x660F0FF8</td><td>No</td><td>4741</td><td>0x8000A15D</td><td>0x00002123</td></tr>
<tr><td>_pmcoutpost_beerB</td><td>0xF00C179F</td><td>No</td><td>4742</td><td>0x8000A15E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_beerC</td><td>0x0E0A0842</td><td>No</td><td>4743</td><td>0x8000A15F</td><td>0x000012C2</td></tr>
<tr><td>_pmcoutpost_bld_dock</td><td>0x3D56E499</td><td>No</td><td>1848</td><td>0x800076DE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_bld_fueldepot</td><td>0xF592C1D6</td><td>No</td><td>5496</td><td>0x8000AAB4</td><td>0x0000A6E5</td></tr>
<tr><td>_pmcoutpost_bld_guardpost</td><td>0xBD0F9621</td><td>No</td><td>4772</td><td>0x8000A180</td><td>0x00004A63</td></tr>
<tr><td>_pmcoutpost_bld_guardtower</td><td>0xA614A8B2</td><td>No</td><td>6102</td><td>0x900001DE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_bld_hangar</td><td>0xD4286725</td><td>No</td><td>1849</td><td>0x800076DF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_bld_hq</td><td>0xFA352751</td><td>No</td><td>1669</td><td>0x8000735C</td><td>0x0000CECC</td></tr>
<tr><td>_pmcoutpost_bld_hq_interior</td><td>0xEFF62F70</td><td>No</td><td>1850</td><td>0x800076E0</td><td>0x00002698</td></tr>
<tr><td>_pmcoutpost_bld_hq_livedin</td><td>0xAA5CF2EB</td><td>No</td><td>6101</td><td>0x900001DD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Pmcoutpost_bld_hq_livedin_pmccon003</td><td>0xE8F7513D</td><td>No</td><td>5851</td><td>0x8000AFA3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_bld_hq_stitch</td><td>0xF7137923</td><td>No</td><td>2013</td><td>0x800080BC</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_bld_hqgarage</td><td>0x0CEDB83E</td><td>No</td><td>6098</td><td>0x900001DA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_bld_hqgarage_livedin</td><td>0x4277ECA0</td><td>No</td><td>6100</td><td>0x900001DC</td><td>0x0000B64B</td></tr>
<tr><td>_pmcoutpost_bld_hqsuites</td><td>0x4D024F06</td><td>No</td><td>6099</td><td>0x900001DB</td><td>0x0000AD57</td></tr>
<tr><td>_pmcoutpost_bld_pool</td><td>0x98C100B2</td><td>No</td><td>1851</td><td>0x800076E1</td><td>0x00004750</td></tr>
<tr><td>_pmcoutpost_bld_pool_stitch</td><td>0x54C98856</td><td>No</td><td>2014</td><td>0x800080BD</td><td>0x00012F75</td></tr>
<tr><td>_pmcoutpost_bridge</td><td>0xCB1C662E</td><td>No</td><td>1734</td><td>0x800075AC</td><td>0x0000A12D</td></tr>
<tr><td>_pmcoutpost_bridge_aicollision</td><td>0xC56BCD09</td><td>No</td><td>4550</td><td>0x80009F20</td><td>0x0000CDCF</td></tr>
<tr><td>_pmcoutpost_bridgepole</td><td>0x194BCD28</td><td>No</td><td>1854</td><td>0x800076E5</td><td>0x000022A4</td></tr>
<tr><td>_pmcoutpost_carcreeper</td><td>0x3571DA99</td><td>No</td><td>4557</td><td>0x80009F27</td><td>0x000011C2</td></tr>
<tr><td>_pmcoutpost_carramp</td><td>0xA82ED4C5</td><td>No</td><td>4558</td><td>0x80009F28</td><td>0x00008EE4</td></tr>
<tr><td>_pmcoutpost_chandeliers</td><td>0x6541730F</td><td>No</td><td>1043</td><td>0x8000691C</td><td>0x0000AC6E</td></tr>
<tr><td>_pmcoutpost_column</td><td>0x148994D7</td><td>No</td><td>1873</td><td>0x800076F8</td><td>0x00012F9C</td></tr>
<tr><td>_pmcoutpost_column_noreflection</td><td>0x0F3F4CA8</td><td>No</td><td>2824</td><td>0x80008782</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_column_noreflection_large</td><td>0xC9B17DA8</td><td>No</td><td>2825</td><td>0x80008783</td><td>0x00007146</td></tr>
<tr><td>_pmcoutpost_column_noreflection_large_HighHP</td><td>0xFD46DE83</td><td>No</td><td>5575</td><td>0x8000AB73</td><td>0x000102B7</td></tr>
<tr><td>_pmcoutpost_column_noreflection_large_lowHP</td><td>0x1AF22B27</td><td>No</td><td>5570</td><td>0x8000AB6D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_column_noreflection_physics</td><td>0x26BAEADA</td><td>No</td><td>5543</td><td>0x8000AB50</td><td>0x0000A896</td></tr>
<tr><td>_pmcoutpost_coverflowerpot</td><td>0x7C8D8304</td><td>No</td><td>5434</td><td>0x8000A9FC</td><td>0x000140E6</td></tr>
<tr><td>_pmcoutpost_electricBoxA</td><td>0xEE253ECC</td><td>No</td><td>4537</td><td>0x80009F12</td><td>0x0000BEDB</td></tr>
<tr><td>_pmcoutpost_electricBoxB</td><td>0x08232923</td><td>No</td><td>4538</td><td>0x80009F13</td><td>0x000106E1</td></tr>
<tr><td>_pmcoutpost_electricBoxC</td><td>0xE620B506</td><td>No</td><td>4539</td><td>0x80009F14</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_fountain</td><td>0x2F2C856D</td><td>No</td><td>4205</td><td>0x80009C35</td><td>0x00008B7A</td></tr>
<tr><td>_pmcoutpost_gate</td><td>0xDD1CB508</td><td>No</td><td>1852</td><td>0x800076E3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_gate_open</td><td>0xBCF03323</td><td>No</td><td>2783</td><td>0x80008755</td><td>0x0000753A</td></tr>
<tr><td>_pmcoutpost_generator</td><td>0xFA076A98</td><td>No</td><td>4540</td><td>0x80009F15</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_hq_door_entrance</td><td>0x6A72B4FC</td><td>No</td><td>4522</td><td>0x80009F02</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_hq_door_entranceCollision</td><td>0x568D9ABC</td><td>No</td><td>5436</td><td>0x8000A9FE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_hq_door_garage</td><td>0x0322E7DD</td><td>No</td><td>4523</td><td>0x80009F03</td><td>0x0001324B</td></tr>
<tr><td>_pmcoutpost_hq_door_roof</td><td>0x79BABB3C</td><td>No</td><td>4513</td><td>0x80009EF9</td><td>0x000119DC</td></tr>
<tr><td>_pmcoutpost_hq_garageentrance</td><td>0xF514923E</td><td>No</td><td>5429</td><td>0x8000A9F7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_hqgarage_door_backdoor</td><td>0xA139AC30</td><td>No</td><td>4524</td><td>0x80009F04</td><td>0x00000972</td></tr>
<tr><td>_pmcoutpost_hqgarage_door_big</td><td>0x28F6E095</td><td>No</td><td>4525</td><td>0x80009F05</td><td>0x00013C31</td></tr>
<tr><td>_pmcoutpost_hqgarage_door_roof</td><td>0xA992B4C3</td><td>No</td><td>4529</td><td>0x80009F0A</td><td>0x0000E973</td></tr>
<tr><td>_pmcoutpost_icebox</td><td>0x994C22F9</td><td>No</td><td>4744</td><td>0x8000A160</td><td>0x00001023</td></tr>
<tr><td>_pmcoutpost_interior_money</td><td>0x5F83D7E4</td><td>No</td><td>4791</td><td>0x8000A194</td><td>0x00005726</td></tr>
<tr><td>_pmcoutpost_interior_money_a</td><td>0xA60DB1AC</td><td>No</td><td>4790</td><td>0x8000A193</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_interior_money_b</td><td>0x400AD283</td><td>No</td><td>4792</td><td>0x8000A195</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_interior_money_c</td><td>0x1E085E66</td><td>No</td><td>4793</td><td>0x8000A196</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_interior_money_d</td><td>0x2819B745</td><td>No</td><td>4794</td><td>0x8000A197</td><td>0x00000F97</td></tr>
<tr><td>_pmcoutpost_interior_money_e</td><td>0x3E179B50</td><td>No</td><td>4795</td><td>0x8000A198</td><td>0x000026C1</td></tr>
<tr><td>_pmcoutpost_interior_money_f</td><td>0x28153A17</td><td>No</td><td>4796</td><td>0x8000A199</td><td>0x000090D7</td></tr>
<tr><td>_pmcoutpost_interior_money_g</td><td>0xC612613A</td><td>No</td><td>4797</td><td>0x8000A19A</td><td>0x0000FA1A</td></tr>
<tr><td>_pmcoutpost_interior_money_h</td><td>0x9FFC5F19</td><td>No</td><td>4798</td><td>0x8000A19B</td><td>0x0001247C</td></tr>
<tr><td>_pmcoutpost_interior_money_i</td><td>0x45F992D4</td><td>No</td><td>4799</td><td>0x8000A19C</td><td>0x00011BD3</td></tr>
<tr><td>_pmcoutpost_interior_recruitheli</td><td>0xD148EB92</td><td>Yes</td><td>4958</td><td>0x8000A2BC</td><td>0x00003448</td></tr>
<tr><td>_pmcoutpost_interior_recruitjet</td><td>0x9F5875D3</td><td>No</td><td>4739</td><td>0x8000A15B</td><td>0x00012CBE</td></tr>
<tr><td>_pmcoutpost_interior_recruitmechanic</td><td>0x9719D1C4</td><td>No</td><td>4555</td><td>0x80009F25</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_interior_recruitmechanic_wallReplace</td><td>0x360F3129</td><td>No</td><td>4556</td><td>0x80009F26</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_interior_scaffold</td><td>0x80F17406</td><td>No</td><td>4789</td><td>0x8000A192</td><td>0x00013104</td></tr>
<tr><td>_pmcoutpost_interior_sickbay</td><td>0xF31A49D2</td><td>No</td><td>4749</td><td>0x8000A166</td><td>0x000111E7</td></tr>
<tr><td>_pmcoutpost_interior_stockpile</td><td>0x0045888E</td><td>No</td><td>4788</td><td>0x8000A191</td><td>0x0000AD4D</td></tr>
<tr><td>_pmcoutpost_IV</td><td>0x85E31274</td><td>No</td><td>4745</td><td>0x8000A161</td><td>0x00007B9F</td></tr>
<tr><td>_pmcoutpost_munitions</td><td>0xEDA24071</td><td>No</td><td>4801</td><td>0x8000A19E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_artillery_A</td><td>0x448CD8A6</td><td>No</td><td>4800</td><td>0x8000A19D</td><td>0x00013D45</td></tr>
<tr><td>_pmcoutpost_munitions_artillery_B</td><td>0xC6946111</td><td>No</td><td>4802</td><td>0x8000A19F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_artillery_C</td><td>0xCC922BEC</td><td>No</td><td>4803</td><td>0x8000A1A0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_bombingrun_A</td><td>0x11EE32DF</td><td>No</td><td>4804</td><td>0x8000A1A1</td><td>0x00000861</td></tr>
<tr><td>_pmcoutpost_munitions_bombingrun_B</td><td>0x87F12B38</td><td>No</td><td>4815</td><td>0x8000A1AC</td><td>0x0000DCFB</td></tr>
<tr><td>_pmcoutpost_munitions_bombingrun_C</td><td>0xB1F3ABED</td><td>No</td><td>4816</td><td>0x8000A1AD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_bunkerbuster_A</td><td>0x63CB97E8</td><td>No</td><td>4805</td><td>0x8000A1A2</td><td>0x0000587B</td></tr>
<tr><td>_pmcoutpost_munitions_bunkerbuster_B</td><td>0xEDC89F8F</td><td>No</td><td>4817</td><td>0x8000A1AE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_bunkerbuster_C</td><td>0xCBC62B72</td><td>No</td><td>4818</td><td>0x8000A1AF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_cap_A</td><td>0xD307BFD0</td><td>No</td><td>4806</td><td>0x8000A1A3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_cap_B</td><td>0xBD055E97</td><td>No</td><td>4819</td><td>0x8000A1B0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_cap_C</td><td>0x5B0285BA</td><td>No</td><td>4820</td><td>0x8000A1B1</td><td>0x0000825E</td></tr>
<tr><td>_pmcoutpost_munitions_clusterbomb_A</td><td>0x934AE316</td><td>No</td><td>4807</td><td>0x8000A1A4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_clusterbomb_B</td><td>0x15526B81</td><td>No</td><td>4821</td><td>0x8000A1B2</td><td>0x00008623</td></tr>
<tr><td>_pmcoutpost_munitions_clusterbomb_C</td><td>0x1B50365C</td><td>No</td><td>4822</td><td>0x8000A1B3</td><td>0x000021C5</td></tr>
<tr><td>_pmcoutpost_munitions_daisycutter_A</td><td>0x7869B7CF</td><td>No</td><td>4808</td><td>0x8000A1A5</td><td>0x0000EB91</td></tr>
<tr><td>_pmcoutpost_munitions_daisycutter_B</td><td>0xEE6CB028</td><td>No</td><td>4823</td><td>0x8000A1B4</td><td>0x0000A796</td></tr>
<tr><td>_pmcoutpost_munitions_daisycutter_C</td><td>0xD86ECC1D</td><td>No</td><td>4824</td><td>0x8000A1B5</td><td>0x00002283</td></tr>
<tr><td>_pmcoutpost_munitions_fae_A</td><td>0x724367F4</td><td>No</td><td>4809</td><td>0x8000A1A6</td><td>0x00010246</td></tr>
<tr><td>_pmcoutpost_munitions_fae_B</td><td>0x4C40ED8B</td><td>No</td><td>4825</td><td>0x8000A1B6</td><td>0x000029C7</td></tr>
<tr><td>_pmcoutpost_munitions_fae_C</td><td>0xEA3E14AE</td><td>No</td><td>4826</td><td>0x8000A1B7</td><td>0x0000C9C6</td></tr>
<tr><td>_pmcoutpost_munitions_gbu16_A</td><td>0xDE4C9A41</td><td>No</td><td>4810</td><td>0x8000A1A7</td><td>0x000132ED</td></tr>
<tr><td>_pmcoutpost_munitions_gbu16_B</td><td>0x5C4511D6</td><td>No</td><td>4827</td><td>0x8000A1B8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_gbu16_C</td><td>0xBE47EAB3</td><td>No</td><td>4828</td><td>0x8000A1B9</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_MOAB_A</td><td>0xD212950D</td><td>No</td><td>4811</td><td>0x8000A1A8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_MOAB_B</td><td>0x500B0CA2</td><td>No</td><td>4829</td><td>0x8000A1BA</td><td>0x00011F02</td></tr>
<tr><td>_pmcoutpost_munitions_MOAB_C</td><td>0xB20DE57F</td><td>No</td><td>4830</td><td>0x8000A1BB</td><td>0x00004C42</td></tr>
<tr><td>_pmcoutpost_munitions_rocketartillery_A</td><td>0x5F93B866</td><td>No</td><td>4812</td><td>0x8000A1A9</td><td>0x00000719</td></tr>
<tr><td>_pmcoutpost_munitions_rocketartillery_B</td><td>0xE19B40D1</td><td>No</td><td>4831</td><td>0x8000A1BC</td><td>0x00002F4B</td></tr>
<tr><td>_pmcoutpost_munitions_rocketartillery_C</td><td>0xE7990BAC</td><td>No</td><td>5483</td><td>0x8000AAA7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_surgicalstrike_A</td><td>0x4E1B15E8</td><td>No</td><td>4813</td><td>0x8000A1AA</td><td>0x0000ADBA</td></tr>
<tr><td>_pmcoutpost_munitions_surgicalstrike_B</td><td>0xD8181D8F</td><td>No</td><td>5484</td><td>0x8000AAA8</td><td>0x00012E66</td></tr>
<tr><td>_pmcoutpost_munitions_surgicalstrike_C</td><td>0xB615A972</td><td>No</td><td>5485</td><td>0x8000AAA9</td><td>0x0000D1C3</td></tr>
<tr><td>_pmcoutpost_munitions_tankbuster_A</td><td>0x9DE55C33</td><td>Yes</td><td>4814</td><td>0x8000A1AB</td><td>0x00008AF2</td></tr>
<tr><td>_pmcoutpost_munitions_tankbuster_B</td><td>0xC3E7D69C</td><td>Yes</td><td>5486</td><td>0x8000AAAA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_munitions_tankbuster_C</td><td>0xBDEA0BC1</td><td>Yes</td><td>5487</td><td>0x8000AAAB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_planter01</td><td>0xE873C630</td><td>No</td><td>1853</td><td>0x800076E4</td><td>0x000063C4</td></tr>
<tr><td>_pmcoutpost_plantera</td><td>0x1834E2F2</td><td>No</td><td>2016</td><td>0x800080BF</td><td>0x00001A18</td></tr>
<tr><td>_pmcoutpost_planterb</td><td>0x9A3C6B5D</td><td>No</td><td>2020</td><td>0x800080C3</td><td>0x000139A5</td></tr>
<tr><td>_pmcoutpost_planterc</td><td>0xB03A4F68</td><td>No</td><td>2019</td><td>0x800080C2</td><td>0x000109A4</td></tr>
<tr><td>_pmcoutpost_planterd</td><td>0xB22D869B</td><td>No</td><td>2018</td><td>0x800080C1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_plantere</td><td>0x902B127E</td><td>No</td><td>2017</td><td>0x800080C0</td><td>0x0000F68D</td></tr>
<tr><td>_pmcoutpost_printer</td><td>0xC936132F</td><td>No</td><td>4536</td><td>0x80009F11</td><td>0x00003160</td></tr>
<tr><td>_pmcoutpost_road_sidewalk</td><td>0x38D4A6D8</td><td>No</td><td>1743</td><td>0x800075B7</td><td>0x000000CF</td></tr>
<tr><td>_pmcoutpost_road_sidewalk01</td><td>0xE9985DDD</td><td>No</td><td>3566</td><td>0x800093C9</td><td>0x0000F640</td></tr>
<tr><td>_pmcoutpost_road_sidewalkcurve01</td><td>0xE0B079F0</td><td>No</td><td>3568</td><td>0x800093CB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_road_sidewalksmall</td><td>0x417E1A41</td><td>No</td><td>1742</td><td>0x800075B6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_road_sidewalksmall01</td><td>0xCC74F104</td><td>No</td><td>3567</td><td>0x800093CA</td><td>0x00013A88</td></tr>
<tr><td>_pmcoutpost_road_sidewalkssmcurveleft01</td><td>0xE7194906</td><td>No</td><td>3564</td><td>0x800093C7</td><td>0x00010AA6</td></tr>
<tr><td>_pmcoutpost_road_sidewalkssmcurveright01</td><td>0x49C9AA0F</td><td>No</td><td>3565</td><td>0x800093C8</td><td>0x00004B64</td></tr>
<tr><td>_pmcoutpost_shootinggallerytarget01</td><td>0x539C3F12</td><td>No</td><td>5348</td><td>0x8000A94D</td><td>0x00006E44</td></tr>
<tr><td>_pmcoutpost_sofa</td><td>0x133EC8C4</td><td>No</td><td>6084</td><td>0x900001C7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_statuecup</td><td>0x5206D86B</td><td>No</td><td>2015</td><td>0x800080BE</td><td>0x0000F8E3</td></tr>
<tr><td>_pmcoutpost_statuedavid</td><td>0x08B37231</td><td>No</td><td>1741</td><td>0x800075B5</td><td>0x00011EE1</td></tr>
<tr><td>_pmcoutpost_statuedavid_lowhealth</td><td>0x096EB764</td><td>No</td><td>5533</td><td>0x8000AB44</td><td>0x0000013D</td></tr>
<tr><td>_pmcoutpost_statuedavid_ruined</td><td>0xE0A6F545</td><td>No</td><td>2367</td><td>0x80008321</td><td>0x000072CC</td></tr>
<tr><td>_pmcoutpost_statuediscus</td><td>0xAFE5E3C2</td><td>No</td><td>1740</td><td>0x800075B4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_statueSolanobust</td><td>0xB7D02E4D</td><td>No</td><td>5432</td><td>0x8000A9FA</td><td>0x0000D3BC</td></tr>
<tr><td>_pmcoutpost_statueSolanobust_lowHP</td><td>0x484C1FA2</td><td>No</td><td>5965</td><td>0x8000B2F9</td><td>0x0001226E</td></tr>
<tr><td>_pmcoutpost_statuethinker</td><td>0x2D978172</td><td>No</td><td>1739</td><td>0x800075B3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_steamerTrunk</td><td>0xDC753284</td><td>No</td><td>4746</td><td>0x8000A162</td><td>0x0000A636</td></tr>
<tr><td>_pmcoutpost_togoBox</td><td>0xA2A8F48F</td><td>No</td><td>4541</td><td>0x80009F16</td><td>0xFFFFFFFF</td></tr>
<tr><td>_pmcoutpost_tray</td><td>0x4F0EE265</td><td>No</td><td>4747</td><td>0x8000A163</td><td>0x0000FD97</td></tr>
<tr><td>_pmcoutpost_TV</td><td>0x890C98DF</td><td>No</td><td>4748</td><td>0x8000A164</td><td>0x0000F1A8</td></tr>
<tr><td>_pmcoutpost_walla</td><td>0x51DF5BE2</td><td>No</td><td>1735</td><td>0x800075AE</td><td>0x0000A5A1</td></tr>
<tr><td>_pmcoutpost_wallb</td><td>0xD3E6E44D</td><td>No</td><td>1736</td><td>0x800075AF</td><td>0x00002ABA</td></tr>
<tr><td>_pmcoutpost_waterCooler</td><td>0x9252F580</td><td>No</td><td>4542</td><td>0x80009F17</td><td>0x0000B97D</td></tr>
<tr><td>_policeoutpost_bld_guardtower</td><td>0xA0BF3B00</td><td>No</td><td>1657</td><td>0x8000734E</td><td>0x00007B83</td></tr>
<tr><td>_policeoutpost_bld_motorpool</td><td>0xD1204EB7</td><td>No</td><td>1658</td><td>0x8000734F</td><td>0x0000FD77</td></tr>
<tr><td>_policeoutpost_bld_policeHQ</td><td>0xB0E73C59</td><td>No</td><td>1122</td><td>0x80006B50</td><td>0x00005BC6</td></tr>
<tr><td>_policeoutpost_bld_policestation01</td><td>0x7E89185D</td><td>No</td><td>1659</td><td>0x80007350</td><td>0x0000FDC0</td></tr>
<tr><td>_policeoutpost_bld_prison</td><td>0x91431313</td><td>No</td><td>1660</td><td>0x80007351</td><td>0x000114D8</td></tr>
<tr><td>_port_containera</td><td>0x545DCABE</td><td>No</td><td>612</td><td>0x80005C25</td><td>0x000120B7</td></tr>
<tr><td>_port_containera_light</td><td>0x9C19E827</td><td>No</td><td>5574</td><td>0x8000AB72</td><td>0x000088C4</td></tr>
<tr><td>_port_containerb</td><td>0xF6658589</td><td>No</td><td>613</td><td>0x80005C26</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_containerb_light</td><td>0x1F1C6F34</td><td>No</td><td>5571</td><td>0x8000AB6E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_containerc</td><td>0xDC631E04</td><td>No</td><td>614</td><td>0x80005C27</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_containerc_light</td><td>0x03DA8FBD</td><td>No</td><td>5572</td><td>0x8000AB6F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_containerd</td><td>0xFE6A0F4F</td><td>No</td><td>687</td><td>0x80005FA5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_containerd_light</td><td>0x8DF486DA</td><td>No</td><td>5573</td><td>0x8000AB70</td><td>0x00007F84</td></tr>
<tr><td>_port_crane01</td><td>0x58193AC2</td><td>No</td><td>626</td><td>0x80005C37</td><td>0x000118FF</td></tr>
<tr><td>_port_crane01_ruined</td><td>0x9A3F9338</td><td>No</td><td>5847</td><td>0x8000AF9F</td><td>0x00003185</td></tr>
<tr><td>_port_crane02</td><td>0xDA20C32D</td><td>No</td><td>627</td><td>0x80005C38</td><td>0x0001219A</td></tr>
<tr><td>_port_cranegantry01</td><td>0xAC4F5FD3</td><td>No</td><td>1005</td><td>0x8000688D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_dock_ladderlong</td><td>0x0790D4CE</td><td>No</td><td>4551</td><td>0x80009F21</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_dock_ladderlong02</td><td>0x0BDCC8F4</td><td>No</td><td>4554</td><td>0x80009F24</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_dock_laddermedium01</td><td>0x365C22D8</td><td>No</td><td>4737</td><td>0x8000A159</td><td>0x00004BE5</td></tr>
<tr><td>_port_dock_laddershort</td><td>0x39A1F0AE</td><td>No</td><td>4552</td><td>0x80009F22</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_dock_laddershort02</td><td>0x74882D54</td><td>No</td><td>4553</td><td>0x80009F23</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_dockdoorleft</td><td>0xA8B4392A</td><td>No</td><td>1513</td><td>0x80007170</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_dockdoorright</td><td>0xBDA0A581</td><td>No</td><td>1512</td><td>0x8000716F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_dockdry</td><td>0x8066913C</td><td>No</td><td>1465</td><td>0x80007010</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_dockdryendA</td><td>0x44C8B3AC</td><td>No</td><td>1488</td><td>0x80007027</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_dockdryendB</td><td>0xDEC5D483</td><td>No</td><td>1489</td><td>0x80007028</td><td>0x00003BB8</td></tr>
<tr><td>_port_dockdryT</td><td>0x36BEFCFC</td><td>No</td><td>1490</td><td>0x80007029</td><td>0x0000519D</td></tr>
<tr><td>_port_dockend</td><td>0x3B3157A0</td><td>No</td><td>1491</td><td>0x8000702A</td><td>0x000069FD</td></tr>
<tr><td>_port_dockloading</td><td>0xE0DB6447</td><td>No</td><td>1476</td><td>0x8000701B</td><td>0x0000D8D3</td></tr>
<tr><td>_port_docklong</td><td>0x185A2B9B</td><td>No</td><td>1492</td><td>0x8000702B</td><td>0x000091A7</td></tr>
<tr><td>_port_dockshort</td><td>0xFD49DF0D</td><td>No</td><td>1493</td><td>0x8000702C</td><td>0x00010D84</td></tr>
<tr><td>_port_dockT</td><td>0x26C330CB</td><td>No</td><td>1494</td><td>0x8000702D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_gangplankA</td><td>0x19F13030</td><td>No</td><td>1495</td><td>0x8000702E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_port_gangplankB</td><td>0x03EECEF7</td><td>No</td><td>1496</td><td>0x8000702F</td><td>0x000043CD</td></tr>
<tr><td>_port_scaffoldA</td><td>0xB0CE1B07</td><td>No</td><td>1497</td><td>0x80007030</td><td>0x0000A56C</td></tr>
<tr><td>_proutpost_att_neonA</td><td>0x28413890</td><td>No</td><td>1515</td><td>0x80007172</td><td>0xFFFFFFFF</td></tr>
<tr><td>_proutpost_att_neonB</td><td>0x123ED757</td><td>No</td><td>1514</td><td>0x80007171</td><td>0xFFFFFFFF</td></tr>
<tr><td>_proutpost_att_neonC</td><td>0xB03BFE7A</td><td>No</td><td>1546</td><td>0x80007193</td><td>0x0000AE5F</td></tr>
<tr><td>_proutpost_att_neonD</td><td>0x8A398411</td><td>No</td><td>1547</td><td>0x80007194</td><td>0x0000A46F</td></tr>
<tr><td>_proutpost_att_neonE</td><td>0x90374EEC</td><td>No</td><td>1548</td><td>0x80007195</td><td>0x00000255</td></tr>
<tr><td>_proutpost_att_satelitelarge</td><td>0xEF69798B</td><td>No</td><td>1549</td><td>0x80007196</td><td>0x00003D4A</td></tr>
<tr><td>_proutpost_att_satelitelarge_ruined</td><td>0x2032E9EF</td><td>No</td><td>4140</td><td>0x80009B42</td><td>0x00012EEC</td></tr>
<tr><td>_proutpost_bld_alarmtower</td><td>0x40D1E50C</td><td>No</td><td>4186</td><td>0x80009C1C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_proutpost_bld_barstand</td><td>0x9F1FD55F</td><td>No</td><td>6051</td><td>0x900001A3</td><td>0x00001AC6</td></tr>
<tr><td>_proutpost_bld_bunker</td><td>0xC27BD1A9</td><td>No</td><td>1231</td><td>0x80006CDE</td><td>0x00003DEB</td></tr>
<tr><td>_proutpost_bld_bunkersandbag</td><td>0xFBDA6937</td><td>No</td><td>2756</td><td>0x80008739</td><td>0x000078C0</td></tr>
<tr><td>_proutpost_bld_command</td><td>0xA9A06925</td><td>No</td><td>1258</td><td>0x80006D01</td><td>0x000138C0</td></tr>
<tr><td>_proutpost_bld_command_ruined</td><td>0x15479AB9</td><td>No</td><td>4150</td><td>0x80009B4D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_proutpost_bld_dormitory</td><td>0x1297A0FF</td><td>No</td><td>1257</td><td>0x80006D00</td><td>0x000045D7</td></tr>
<tr><td>_proutpost_bld_dormitory_ruined</td><td>0xBD52BE23</td><td>No</td><td>4153</td><td>0x80009B50</td><td>0xFFFFFFFF</td></tr>
<tr><td>_proutpost_bld_garageboat</td><td>0x74CEB277</td><td>Yes</td><td>1229</td><td>0x80006CDC</td><td>0x0000C94F</td></tr>
<tr><td>_proutpost_bld_garageboat_Ruined</td><td>0x9359847B</td><td>Yes</td><td>5230</td><td>0x8000A699</td><td>0x00004EE3</td></tr>
<tr><td>_proutpost_bld_gasstationpump02</td><td>0x65D06087</td><td>No</td><td>5000</td><td>0x8000A3B1</td><td>0x00008D27</td></tr>
<tr><td>_proutpost_bld_gasstationpump03</td><td>0x43CDEC6A</td><td>No</td><td>5001</td><td>0x8000A3B2</td><td>0x0000CBE4</td></tr>
<tr><td>_proutpost_bld_guardtower01</td><td>0x75662AC1</td><td>No</td><td>1230</td><td>0x80006CDD</td><td>0x00008123</td></tr>
<tr><td>_proutpost_bld_hq</td><td>0xA815D69F</td><td>No</td><td>1256</td><td>0x80006CFF</td><td>0x0001305E</td></tr>
<tr><td>_proutpost_bld_pavilion</td><td>0x54E1BE76</td><td>No</td><td>1544</td><td>0x80007191</td><td>0x0000F53D</td></tr>
<tr><td>_proutpost_bld_shacksmall01</td><td>0x6C66D3DA</td><td>No</td><td>2723</td><td>0x80008716</td><td>0x0000E180</td></tr>
<tr><td>_proutpost_bld_shacksmall02</td><td>0xCE6E29E5</td><td>No</td><td>2724</td><td>0x80008717</td><td>0x00006AB1</td></tr>
<tr><td>_proutpost_bld_shacksmall03</td><td>0x646B4470</td><td>No</td><td>2728</td><td>0x8000871B</td><td>0x0000E39F</td></tr>
<tr><td>_proutpost_bld_shacksmall03_Ruined</td><td>0x732EFEDE</td><td>No</td><td>5213</td><td>0x8000A680</td><td>0x000111C5</td></tr>
<tr><td>_proutpost_bld_shacksmall04</td><td>0xE65F4523</td><td>No</td><td>2729</td><td>0x8000871C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_proutpost_bld_surveillance</td><td>0x33A4C96D</td><td>No</td><td>1668</td><td>0x8000735B</td><td>0x0000B2D5</td></tr>
<tr><td>_proutpost_dockA</td><td>0x9F368947</td><td>No</td><td>1545</td><td>0x80007192</td><td>0xFFFFFFFF</td></tr>
<tr><td>_proutpost_dockB</td><td>0x753885C0</td><td>No</td><td>1232</td><td>0x80006CDF</td><td>0x00001414</td></tr>
<tr><td>_proutpost_fencewood01</td><td>0x8E5C1924</td><td>No</td><td>1834</td><td>0x800076CE</td><td>0x00008807</td></tr>
<tr><td>_proutpost_fencewood02</td><td>0xA85A037B</td><td>No</td><td>1835</td><td>0x800076CF</td><td>0x0000A688</td></tr>
<tr><td>_proutpost_fueltanks</td><td>0x7DD4EF9E</td><td>Yes</td><td>2991</td><td>0x80008A17</td><td>0x0000D5E8</td></tr>
<tr><td>_proutpost_helipad</td><td>0x4CE92E2A</td><td>Yes</td><td>1255</td><td>0x80006CFE</td><td>0x0000EB87</td></tr>
<tr><td>_proutpost_interior_job</td><td>0x39394E37</td><td>No</td><td>4753</td><td>0x8000A16C</td><td>0x00000B7F</td></tr>
<tr><td>_Proutpost_lampA</td><td>0x4B6D3286</td><td>No</td><td>1838</td><td>0x800076D2</td><td>0x0000C8CE</td></tr>
<tr><td>_residential_bld_corner16x16a</td><td>0xFBEE37C0</td><td>No</td><td>246</td><td>0x80004DB7</td><td>0x0000AD51</td></tr>
<tr><td>_residential_bld_corner16x16b</td><td>0x25EC3B47</td><td>No</td><td>127</td><td>0x80004CCA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_residential_bld_corner16x16c</td><td>0x03E9C72A</td><td>No</td><td>128</td><td>0x80004CCB</td><td>0xFFFFFFFF</td></tr>
<tr><td>_residential_bld_corner16x16d</td><td>0x9DE6E801</td><td>No</td><td>129</td><td>0x80004CCC</td><td>0x00004E8D</td></tr>
<tr><td>_residential_bld_corner16x16e</td><td>0xA3E4B2DC</td><td>No</td><td>130</td><td>0x80004CCD</td><td>0x0000A9A4</td></tr>
<tr><td>_residential_bld_segment16x16a</td><td>0xAB17B940</td><td>No</td><td>278</td><td>0x80004DDE</td><td>0x0000BE50</td></tr>
<tr><td>_residential_bld_segment16x16b</td><td>0xD515BCC7</td><td>No</td><td>279</td><td>0x80004DDF</td><td>0x0000A5CE</td></tr>
<tr><td>_residential_bld_segment16x16b_ruined</td><td>0xD737478B</td><td>No</td><td>3279</td><td>0x80008F50</td><td>0xFFFFFFFF</td></tr>
<tr><td>_residential_bld_segment16x16c</td><td>0xB31348AA</td><td>No</td><td>280</td><td>0x80004DE0</td><td>0x000126B5</td></tr>
<tr><td>_residential_bld_segment16x16c_ruined</td><td>0x0F313320</td><td>No</td><td>5992</td><td>0x8000B3C4</td><td>0x00001D37</td></tr>
<tr><td>_residential_bld_segment16x16d</td><td>0x4D106981</td><td>No</td><td>281</td><td>0x80004DE1</td><td>0x0000B41A</td></tr>
<tr><td>_residential_driveway</td><td>0x81AD7A10</td><td>No</td><td>366</td><td>0x80005101</td><td>0xFFFFFFFF</td></tr>
<tr><td>_residential_driveway02</td><td>0xF52D70AA</td><td>No</td><td>368</td><td>0x80005103</td><td>0x0000AC4F</td></tr>
<tr><td>_residential_road10</td><td>0xB2EDD014</td><td>No</td><td>295</td><td>0x80004DF9</td><td>0xFFFFFFFF</td></tr>
<tr><td>_residential_road10cross</td><td>0xE4F46104</td><td>No</td><td>297</td><td>0x80004DFB</td><td>0x00002B4A</td></tr>
<tr><td>_residential_road10l</td><td>0xCAF7F2CC</td><td>No</td><td>298</td><td>0x80004DFC</td><td>0x00008EB7</td></tr>
<tr><td>_residential_road10t</td><td>0x4ABC9224</td><td>No</td><td>299</td><td>0x80004DFD</td><td>0x0000EACC</td></tr>
<tr><td>_residential_road10t5</td><td>0xAEEB2BB9</td><td>No</td><td>300</td><td>0x80004DFE</td><td>0x0000F380</td></tr>
<tr><td>_residential_road5</td><td>0x8F67EE14</td><td>No</td><td>296</td><td>0x80004DFA</td><td>0x0000A31A</td></tr>
<tr><td>_residential_road5cross</td><td>0x464B3B04</td><td>No</td><td>301</td><td>0x80004DFF</td><td>0x000071B4</td></tr>
<tr><td>_residential_road5cross10</td><td>0xA714354F</td><td>No</td><td>302</td><td>0x80004E00</td><td>0x0000FFCD</td></tr>
<tr><td>_residential_road5l</td><td>0xDF352CCC</td><td>No</td><td>303</td><td>0x80004E01</td><td>0x00002635</td></tr>
<tr><td>_residential_road5t</td><td>0x5EF9CC24</td><td>No</td><td>304</td><td>0x80004E02</td><td>0x00009E36</td></tr>
<tr><td>_residential_road5t10</td><td>0x9978C5EF</td><td>No</td><td>305</td><td>0x80004E03</td><td>0x0000B5C9</td></tr>
<tr><td>_residential_sidewalk</td><td>0xFE26F5BB</td><td>No</td><td>317</td><td>0x80004E0F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_DLC_global_env_treemedium02</td><td>0x778DECED</td><td>No</td><td>5264</td><td>0x8000A7BB</td><td>0x00012B58</td></tr>
<tr><td>_scrub_env_largecanopy01</td><td>0x1BB4EE74</td><td>No</td><td>3320</td><td>0x80008F84</td><td>0x00003ADA</td></tr>
<tr><td>_scrub_env_smallcanopy</td><td>0x9265E3AD</td><td>No</td><td>3298</td><td>0x80008F6B</td><td>0x00001986</td></tr>
<tr><td>_scrub_env_smallcanopy02</td><td>0x25BA8CE7</td><td>No</td><td>3319</td><td>0x80008F83</td><td>0x00003861</td></tr>
<tr><td>_scrub_global_bananna</td><td>0x88E8C91D</td><td>No</td><td>2045</td><td>0x800080DE</td><td>0x0000A7D9</td></tr>
<tr><td>_scrub_global_env_treesidewalk01</td><td>0x547805A7</td><td>No</td><td>3303</td><td>0x80008F73</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_global_palmtree01</td><td>0xA3265679</td><td>No</td><td>2044</td><td>0x800080DD</td><td>0x0000DB94</td></tr>
<tr><td>_scrub_global_palmtreebend01</td><td>0xFD2975F4</td><td>No</td><td>2084</td><td>0x80008162</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_global_palmtreebend02</td><td>0xD726FB8B</td><td>No</td><td>2085</td><td>0x80008163</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_global_palmtreebend03</td><td>0x752422AE</td><td>No</td><td>2086</td><td>0x80008164</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_global_palmtreebend04</td><td>0x7F357B8D</td><td>No</td><td>2087</td><td>0x80008165</td><td>0x00003F24</td></tr>
<tr><td>_scrub_global_palmtreebend05</td><td>0x5532FAD8</td><td>No</td><td>2088</td><td>0x80008166</td><td>0x00000A74</td></tr>
<tr><td>_scrub_global_palmtreeMix01</td><td>0x20E2B0AB</td><td>No</td><td>2094</td><td>0x8000816D</td><td>0x00009659</td></tr>
<tr><td>_scrub_global_palmtreeMix02</td><td>0x46E52B14</td><td>No</td><td>2095</td><td>0x8000816E</td><td>0x00010BFF</td></tr>
<tr><td>_scrub_global_palmtreeplanted01</td><td>0x22B71F15</td><td>No</td><td>2091</td><td>0x80008169</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_global_treeoak01</td><td>0x2A54D6BA</td><td>No</td><td>2090</td><td>0x80008168</td><td>0x00005B1F</td></tr>
<tr><td>_scrub_global_treeplaza01</td><td>0xC9A4EC6B</td><td>No</td><td>3299</td><td>0x80008F6F</td><td>0x000072C2</td></tr>
<tr><td>_scrub_global_treeplaza02</td><td>0xEFA766D4</td><td>No</td><td>3300</td><td>0x80008F70</td><td>0x0000CC33</td></tr>
<tr><td>_scrub_global_treeplaza03</td><td>0x49AA3319</td><td>No</td><td>3301</td><td>0x80008F71</td><td>0x00004357</td></tr>
<tr><td>_scrub_global_treeplazaMix</td><td>0xA0955814</td><td>No</td><td>3302</td><td>0x80008F72</td><td>0x0000D4D5</td></tr>
<tr><td>_scrub_global_treesidewalk01</td><td>0x0720F3CB</td><td>No</td><td>3252</td><td>0x80008F2D</td><td>0x00009B77</td></tr>
<tr><td>_scrub_global_treespade</td><td>0x13E7446F</td><td>No</td><td>2089</td><td>0x80008167</td><td>0x00001827</td></tr>
<tr><td>_scrub_global_treetropical01</td><td>0x06116B5D</td><td>No</td><td>2092</td><td>0x8000816A</td><td>0x00003013</td></tr>
<tr><td>_scrub_global_treetropical02</td><td>0x8409E2F2</td><td>No</td><td>2093</td><td>0x8000816B</td><td>0x00001AFF</td></tr>
<tr><td>_scrub_global_tropicalmix</td><td>0x2AFAEC36</td><td>No</td><td>3249</td><td>0x80008F29</td><td>0x000103F5</td></tr>
<tr><td>_scrub_jungle_treemed01</td><td>0x7291BD75</td><td>No</td><td>2096</td><td>0x8000816F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_jungle_treemed03</td><td>0x728D4047</td><td>No</td><td>2076</td><td>0x8000814B</td><td>0x0000FFD3</td></tr>
<tr><td>_scrub_Jungle_treesmall01</td><td>0xD8734A7E</td><td>No</td><td>2073</td><td>0x80008146</td><td>0x0000F500</td></tr>
<tr><td>_scrub_jungle_treesmall02</td><td>0x7A7B0549</td><td>No</td><td>2075</td><td>0x8000814A</td><td>0x0000DFE8</td></tr>
<tr><td>_scrub_jungle_treesmall03</td><td>0x60789DC4</td><td>No</td><td>3322</td><td>0x80008F87</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_jungle_treetall01</td><td>0xD0CA23F6</td><td>No</td><td>3550</td><td>0x800093B8</td><td>0x00005F2B</td></tr>
<tr><td>_scrub_jungle_treetall02</td><td>0x52D1AC61</td><td>No</td><td>3549</td><td>0x800093B7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_jungle_treetall03</td><td>0xD8CEADBC</td><td>No</td><td>2097</td><td>0x80008170</td><td>0x000024B0</td></tr>
<tr><td>_scrub_Jungle_treethin01</td><td>0x9682BEE2</td><td>No</td><td>2098</td><td>0x80008171</td><td>0x00003B54</td></tr>
<tr><td>_scrub_Jungle_treethin02</td><td>0x188A474D</td><td>No</td><td>2099</td><td>0x80008172</td><td>0x00008A45</td></tr>
<tr><td>_scrub_Jungle_treethin03</td><td>0xEE87C698</td><td>No</td><td>2100</td><td>0x80008173</td><td>0x00003365</td></tr>
<tr><td>_scrub_junglemix</td><td>0x44E6AAEB</td><td>No</td><td>2048</td><td>0x800080E2</td><td>0x000051FA</td></tr>
<tr><td>_scrub_junglemix02</td><td>0xF2C6A9B1</td><td>No</td><td>3254</td><td>0x80008F32</td><td>0x00005517</td></tr>
<tr><td>_scrub_marsh_treewater02</td><td>0xCD1993FF</td><td>No</td><td>3248</td><td>0x80008F27</td><td>0x0000B6A1</td></tr>
<tr><td>_scrub_shanty_tree01</td><td>0x64B365D5</td><td>No</td><td>2101</td><td>0x80008174</td><td>0x0000F5F9</td></tr>
<tr><td>_scrub_shanty_tree02</td><td>0xC2ABAB0A</td><td>No</td><td>2102</td><td>0x80008175</td><td>0xFFFFFFFF</td></tr>
<tr><td>_scrub_shanty_tree03</td><td>0xE4AE1F27</td><td>No</td><td>2103</td><td>0x80008176</td><td>0xFFFFFFFF</td></tr>
<tr><td>_sean</td><td>0xA5960A21</td><td>No</td><td>940</td><td>0x800064DA</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_apartment01</td><td>0xFE31D148</td><td>No</td><td>692</td><td>0x80005FAB</td><td>0x00005B26</td></tr>
<tr><td>_shanty_bld_apartment01_ruined</td><td>0xA88CF656</td><td>No</td><td>2108</td><td>0x80008181</td><td>0x000017E3</td></tr>
<tr><td>_shanty_bld_apartment02</td><td>0x082FA26F</td><td>No</td><td>693</td><td>0x80005FAC</td><td>0x00007989</td></tr>
<tr><td>_shanty_bld_apartment02_ruined</td><td>0xEBFAB3D3</td><td>No</td><td>2109</td><td>0x80008182</td><td>0x0000C2ED</td></tr>
<tr><td>_shanty_bld_apartment03</td><td>0xE62D2E52</td><td>No</td><td>694</td><td>0x80005FAD</td><td>0x00003A9E</td></tr>
<tr><td>_shanty_bld_apartment04</td><td>0x802A4F29</td><td>No</td><td>898</td><td>0x800064AB</td><td>0x00011EB7</td></tr>
<tr><td>_shanty_bld_apartment04_Ruined</td><td>0xD2A16A3D</td><td>No</td><td>5232</td><td>0x8000A69B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_house01</td><td>0xA3ED4CB2</td><td>No</td><td>588</td><td>0x80005C09</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_house02</td><td>0x25F4D51D</td><td>No</td><td>589</td><td>0x80005C0A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_house02_Ruined</td><td>0x76E3AE31</td><td>No</td><td>5235</td><td>0x8000A69E</td><td>0x0000E684</td></tr>
<tr><td>_shanty_bld_house03</td><td>0x3BF2B928</td><td>No</td><td>582</td><td>0x80005C00</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_house03_Ruined</td><td>0xDAB61FB6</td><td>No</td><td>5215</td><td>0x8000A682</td><td>0x00012067</td></tr>
<tr><td>_shanty_bld_house04</td><td>0x3DE5F05B</td><td>No</td><td>581</td><td>0x80005BFF</td><td>0x00007BCA</td></tr>
<tr><td>_shanty_bld_housegroup01</td><td>0xF92264C1</td><td>No</td><td>590</td><td>0x80005C0B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Shanty_bld_housegroup02</td><td>0x771ADC56</td><td>No</td><td>671</td><td>0x80005F95</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Shanty_bld_housegroup03</td><td>0xD91DB533</td><td>No</td><td>672</td><td>0x80005F96</td><td>0x0001057B</td></tr>
<tr><td>_Shanty_bld_housegroup03_ruined</td><td>0xD2AE8E37</td><td>No</td><td>3596</td><td>0x800093E9</td><td>0x00008C05</td></tr>
<tr><td>_shanty_bld_housegroup04</td><td>0x5729B480</td><td>No</td><td>630</td><td>0x80005C3C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_housegroup05</td><td>0x812C3535</td><td>No</td><td>466</td><td>0x800056A4</td><td>0x000032FB</td></tr>
<tr><td>_shanty_bld_housegroup05_Ruined</td><td>0x04E8FD49</td><td>No</td><td>5234</td><td>0x8000A69D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_housegroup06</td><td>0x5F2543EA</td><td>No</td><td>470</td><td>0x800056A8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_housegroup06_ruined</td><td>0xFB9C6260</td><td>No</td><td>3597</td><td>0x800093EA</td><td>0x0001390C</td></tr>
<tr><td>_Shanty_bld_housegroup07</td><td>0x8127B807</td><td>No</td><td>673</td><td>0x80005F97</td><td>0x000115FC</td></tr>
<tr><td>_Shanty_bld_housegroup07_Ruined</td><td>0x545DC8CB</td><td>No</td><td>5233</td><td>0x8000A69C</td><td>0x000055FE</td></tr>
<tr><td>_Shanty_bld_housegroup08</td><td>0xDF0C7584</td><td>No</td><td>674</td><td>0x80005F98</td><td>0x00011A7C</td></tr>
<tr><td>_shanty_bld_housegroupsmall01</td><td>0xB0AB5E98</td><td>No</td><td>1383</td><td>0x80006EE5</td><td>0x000073C1</td></tr>
<tr><td>_shanty_bld_housegroupsmall01_ruined</td><td>0x193C38E6</td><td>No</td><td>3595</td><td>0x800093E8</td><td>0x000125B0</td></tr>
<tr><td>_shanty_bld_housegroupsmall02</td><td>0xBAA92FBF</td><td>No</td><td>691</td><td>0x80005FAA</td><td>0x000022E0</td></tr>
<tr><td>_shanty_bld_housegroupsmall03</td><td>0x58A656E2</td><td>No</td><td>469</td><td>0x800056A7</td><td>0x00004649</td></tr>
<tr><td>_shanty_bld_housegroupsmall04</td><td>0x32A3DC79</td><td>No</td><td>4758</td><td>0x8000A171</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_outhouse</td><td>0x9A39FC3D</td><td>No</td><td>583</td><td>0x80005C01</td><td>0x00012EE4</td></tr>
<tr><td>_shanty_bld_shack01</td><td>0xD5A65D02</td><td>No</td><td>591</td><td>0x80005C0C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_shack02</td><td>0x57ADE56D</td><td>No</td><td>592</td><td>0x80005C0D</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_shack03</td><td>0x2DAB64B8</td><td>No</td><td>593</td><td>0x80005C0E</td><td>0x000082EE</td></tr>
<tr><td>_shanty_bld_shack04</td><td>0x2F9E9BEB</td><td>No</td><td>594</td><td>0x80005C0F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_bld_shack05</td><td>0x4D9C8C8E</td><td>No</td><td>595</td><td>0x80005C10</td><td>0x00005C69</td></tr>
<tr><td>_shanty_bld_shack06</td><td>0xAFA3E299</td><td>No</td><td>596</td><td>0x80005C11</td><td>0x0000B21F</td></tr>
<tr><td>_shanty_canvaslong</td><td>0x0AEC5052</td><td>No</td><td>983</td><td>0x8000660E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_canvasshort</td><td>0x8DD8B7CA</td><td>No</td><td>982</td><td>0x8000660B</td><td>0x00003154</td></tr>
<tr><td>_shanty_clotheslinea</td><td>0x98A1BEFF</td><td>No</td><td>979</td><td>0x80006601</td><td>0x000078BA</td></tr>
<tr><td>_shanty_clotheslineb</td><td>0x8EA3EDD8</td><td>No</td><td>980</td><td>0x80006602</td><td>0x00012D23</td></tr>
<tr><td>_shanty_concreteleft</td><td>0x5886172E</td><td>No</td><td>1706</td><td>0x80007544</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_concreteright</td><td>0x3BA5C55D</td><td>No</td><td>1707</td><td>0x80007545</td><td>0x000026AA</td></tr>
<tr><td>_shanty_dockB</td><td>0xD35B1049</td><td>No</td><td>4991</td><td>0x8000A3A6</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_env_bush01</td><td>0x26FBE0CF</td><td>No</td><td>690</td><td>0x80005FA9</td><td>0x0000C5AE</td></tr>
<tr><td>_shanty_env_bush02</td><td>0x9CFED928</td><td>No</td><td>689</td><td>0x80005FA7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_env_bush03</td><td>0x8700F51D</td><td>No</td><td>688</td><td>0x80005FA6</td><td>0x0000BCA5</td></tr>
<tr><td>_shanty_env_tree01</td><td>0x1FAAA339</td><td>No</td><td>3754</td><td>0x80009718</td><td>0xFFFFFFFF</td></tr>
<tr><td>_shanty_env_tree02</td><td>0xBDA34D2E</td><td>No</td><td>3755</td><td>0x80009719</td><td>0x0000568E</td></tr>
<tr><td>_shanty_env_tree03</td><td>0x1FA6260B</td><td>No</td><td>3753</td><td>0x80009717</td><td>0x00001EC8</td></tr>
<tr><td>_shanty_fencecorner01</td><td>0xDC8E2081</td><td>No</td><td>608</td><td>0x80005C1E</td><td>0x00009932</td></tr>
<tr><td>_shanty_fencestraight01</td><td>0x1592F8F8</td><td>No</td><td>607</td><td>0x80005C1D</td><td>0x0000CBD9</td></tr>
<tr><td>_shanty_fencewood01</td><td>0xA578E4E9</td><td>No</td><td>5468</td><td>0x8000AA64</td><td>0x00006C64</td></tr>
<tr><td>_shanty_fencewood02</td><td>0x8371F39E</td><td>No</td><td>5469</td><td>0x8000AA65</td><td>0x00013836</td></tr>
<tr><td>_shanty_plankA</td><td>0xA8DA8AE1</td><td>No</td><td>4738</td><td>0x8000A15A</td><td>0x0001057A</td></tr>
<tr><td>_shanty_polepower</td><td>0x2B84DD25</td><td>No</td><td>606</td><td>0x80005C1C</td><td>0x0000C160</td></tr>
<tr><td>_shanty_shower</td><td>0xF48695FE</td><td>No</td><td>604</td><td>0x80005C1A</td><td>0x000056A5</td></tr>
<tr><td>_shanty_telephonepolepair</td><td>0xFB99B8DE</td><td>No</td><td>981</td><td>0x80006604</td><td>0x000003C8</td></tr>
<tr><td>_shanty_telephonepolesingle</td><td>0x78838436</td><td>No</td><td>1031</td><td>0x80006910</td><td>0x00007F8B</td></tr>
<tr><td>_shanty_wallcorner01</td><td>0xE092ACA2</td><td>No</td><td>605</td><td>0x80005C1B</td><td>0x00005E97</td></tr>
<tr><td>_shanty_wallcorner02</td><td>0x629A350D</td><td>No</td><td>603</td><td>0x80005C18</td><td>0x00008CD0</td></tr>
<tr><td>_shanty_wallcorner03</td><td>0x3897B458</td><td>No</td><td>602</td><td>0x80005C17</td><td>0x00002737</td></tr>
<tr><td>_shanty_walllargecorner01</td><td>0x1FF99F4F</td><td>No</td><td>601</td><td>0x80005C16</td><td>0x00003A2F</td></tr>
<tr><td>_shanty_walllargestraight01</td><td>0xA2469366</td><td>No</td><td>600</td><td>0x80005C15</td><td>0x00000657</td></tr>
<tr><td>_shanty_wallstraight01</td><td>0x7741A32B</td><td>No</td><td>599</td><td>0x80005C14</td><td>0x00009777</td></tr>
<tr><td>_shanty_wallstraight02</td><td>0x9D441D94</td><td>No</td><td>598</td><td>0x80005C13</td><td>0x00007912</td></tr>
<tr><td>_shanty_wallstraight03</td><td>0xF746E9D9</td><td>No</td><td>597</td><td>0x80005C12</td><td>0x00013175</td></tr>
<tr><td>_sign01</td><td>0xC64F2C1E</td><td>No</td><td>3770</td><td>0x8000972C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_sign02</td><td>0xE8561D69</td><td>No</td><td>3773</td><td>0x8000972F</td><td>0x00004711</td></tr>
<tr><td>_sign03</td><td>0xCE53B5E4</td><td>No</td><td>3774</td><td>0x80009730</td><td>0x0000878A</td></tr>
<tr><td>_sign04</td><td>0x705B70AF</td><td>No</td><td>3775</td><td>0x80009731</td><td>0x000094CD</td></tr>
<tr><td>_sign05</td><td>0x4E58FC92</td><td>No</td><td>3776</td><td>0x80009732</td><td>0xFFFFFFFF</td></tr>
<tr><td>_sign06</td><td>0xD06084FD</td><td>No</td><td>3777</td><td>0x80009733</td><td>0xFFFFFFFF</td></tr>
<tr><td>_sign07</td><td>0x665D9F88</td><td>No</td><td>3778</td><td>0x80009734</td><td>0x0000CFA7</td></tr>
<tr><td>_sign08</td><td>0xC864F593</td><td>No</td><td>3779</td><td>0x80009735</td><td>0x0000230E</td></tr>
<tr><td>_sign09</td><td>0xE662E636</td><td>No</td><td>3780</td><td>0x80009736</td><td>0x00002CBA</td></tr>
<tr><td>_sign10</td><td>0xDA090940</td><td>No</td><td>3781</td><td>0x80009737</td><td>0x000079B4</td></tr>
<tr><td>_sign11</td><td>0x040B89F5</td><td>No</td><td>3782</td><td>0x80009738</td><td>0x00003ABF</td></tr>
<tr><td>_sign12</td><td>0xE20498AA</td><td>No</td><td>3783</td><td>0x80009739</td><td>0x000027EE</td></tr>
<tr><td>_sign13</td><td>0x04070CC7</td><td>No</td><td>3784</td><td>0x8000973A</td><td>0x000051B0</td></tr>
<tr><td>_sign14</td><td>0x81FF845C</td><td>No</td><td>3785</td><td>0x8000973B</td><td>0x000061FB</td></tr>
<tr><td>_sign15</td><td>0x7C01B981</td><td>No</td><td>3786</td><td>0x8000973C</td><td>0x00005FF6</td></tr>
<tr><td>_sign16</td><td>0xF9FA3116</td><td>No</td><td>3787</td><td>0x8000973D</td><td>0x0000B170</td></tr>
<tr><td>_sign17</td><td>0x5BFD09F3</td><td>No</td><td>3788</td><td>0x8000973E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_sign18</td><td>0xF9F5B3E8</td><td>No</td><td>3789</td><td>0x8000973F</td><td>0x0000BB43</td></tr>
<tr><td>_sign19</td><td>0xE3F7CFDD</td><td>No</td><td>3790</td><td>0x80009740</td><td>0x0000A44F</td></tr>
<tr><td>_sign20</td><td>0x6F71C291</td><td>No</td><td>3965</td><td>0x8000996E</td><td>0x0000A7D5</td></tr>
<tr><td>_sign21</td><td>0x756F8D6C</td><td>No</td><td>3966</td><td>0x8000996F</td><td>0x00007319</td></tr>
<tr><td>_sign22</td><td>0x0F6CAE43</td><td>No</td><td>3967</td><td>0x80009970</td><td>0x00002529</td></tr>
<tr><td>_sign23</td><td>0xED6A3A26</td><td>No</td><td>3968</td><td>0x80009971</td><td>0x00002F92</td></tr>
<tr><td>_sign24</td><td>0xF77B9305</td><td>No</td><td>3969</td><td>0x80009972</td><td>0x000052E5</td></tr>
<tr><td>_sign25</td><td>0x0D797710</td><td>No</td><td>3970</td><td>0x80009973</td><td>0x00005407</td></tr>
<tr><td>_sign26</td><td>0xF77715D7</td><td>No</td><td>3971</td><td>0x80009974</td><td>0x00006AE2</td></tr>
<tr><td>_sign27</td><td>0x95743CFA</td><td>No</td><td>3972</td><td>0x80009975</td><td>0x00007F18</td></tr>
<tr><td>_sign28</td><td>0x6F5E3AD9</td><td>No</td><td>3973</td><td>0x80009976</td><td>0x00008AAA</td></tr>
<tr><td>_sign29</td><td>0x155B6E94</td><td>No</td><td>3974</td><td>0x80009977</td><td>0x000044B7</td></tr>
<tr><td>_sign30</td><td>0x1F9D7376</td><td>No</td><td>3975</td><td>0x80009978</td><td>0x00000468</td></tr>
<tr><td>_sign31</td><td>0x019F82D3</td><td>No</td><td>3976</td><td>0x80009979</td><td>0x000069C8</td></tr>
<tr><td>_sign32</td><td>0x27A1FD3C</td><td>No</td><td>3977</td><td>0x8000997A</td><td>0x00007892</td></tr>
<tr><td>_sign33</td><td>0xA1A4FBE1</td><td>No</td><td>3978</td><td>0x8000997B</td><td>0x0000AB13</td></tr>
<tr><td>_sign34</td><td>0x87A7118A</td><td>No</td><td>3979</td><td>0x8000997C</td><td>0x00002AA4</td></tr>
<tr><td>_sign35</td><td>0xA9A985A7</td><td>No</td><td>3980</td><td>0x8000997D</td><td>0x0000AF22</td></tr>
<tr><td>_sign36</td><td>0xFFAC4BA0</td><td>No</td><td>3981</td><td>0x8000997E</td><td>0x0000B114</td></tr>
<tr><td>_sign37</td><td>0x29AECC55</td><td>No</td><td>3982</td><td>0x8000997F</td><td>0x0000B401</td></tr>
<tr><td>_sign38</td><td>0xFF89B95E</td><td>No</td><td>3983</td><td>0x80009980</td><td>0x00003680</td></tr>
<tr><td>_sign39</td><td>0x218C2D7B</td><td>No</td><td>3984</td><td>0x80009981</td><td>0x0000B8B0</td></tr>
<tr><td>_sign40</td><td>0xA3EC08A7</td><td>No</td><td>3985</td><td>0x80009982</td><td>0x0000EEE5</td></tr>
<tr><td>_stealth_road10</td><td>0xA4EDCDD5</td><td>No</td><td>559</td><td>0x80005BB1</td><td>0x0000E443</td></tr>
<tr><td>_streamer_maracaibo_e</td><td>0x0A6F5B9F</td><td>No</td><td>4982</td><td>0x8000A39D</td><td>0x0000ED4F</td></tr>
<tr><td>_streamer_maracaibo_n</td><td>0xA0860E10</td><td>No</td><td>4981</td><td>0x8000A39C</td><td>0x00007ADE</td></tr>
<tr><td>_streamer_maracaibo_s</td><td>0xA2432B49</td><td>No</td><td>4980</td><td>0x8000A39B</td><td>0x0000104B</td></tr>
<tr><td>_streamer_maracaibo_w</td><td>0x0A4CC95D</td><td>No</td><td>4983</td><td>0x8000A39E</td><td>0x000119B8</td></tr>
<tr><td>_test_16x16_block</td><td>0xA48C9401</td><td>No</td><td>474</td><td>0x800056AE</td><td>0x0000C2A4</td></tr>
<tr><td>_test_32x32_block</td><td>0x64831FA5</td><td>No</td><td>465</td><td>0x800056A1</td><td>0x0000E706</td></tr>
<tr><td>_test_4x1_ramp</td><td>0x127F9387</td><td>No</td><td>457</td><td>0x80005699</td><td>0x0000F224</td></tr>
<tr><td>_test_4x1_stick</td><td>0xF58EE529</td><td>No</td><td>460</td><td>0x8000569C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_test_4x4_block</td><td>0x058B91AF</td><td>No</td><td>456</td><td>0x80005698</td><td>0x0000ECE1</td></tr>
<tr><td>_underwater_minea</td><td>0x02B39BC4</td><td>No</td><td>945</td><td>0x800065DD</td><td>0x00003E3D</td></tr>
<tr><td>_Vehicle (Immobile)</td><td>0xE538BEB5</td><td>Yes</td><td>3205</td><td>0x80008EF7</td><td>0x0000B28F</td></tr>
<tr><td>_Vehicle (Old)</td><td>0x7B6F2B60</td><td>Yes</td><td>520</td><td>0x80005722</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Vehicle (Production Ready)</td><td>0xDE2704A1</td><td>Yes</td><td>822</td><td>0x8000637D</td><td>0x0000A61E</td></tr>
<tr><td>_village_att_pierlong</td><td>0xD1ABEBB5</td><td>No</td><td>1540</td><td>0x8000718D</td><td>0x00002804</td></tr>
<tr><td>_village_att_piershort</td><td>0x755D477B</td><td>No</td><td>1541</td><td>0x8000718E</td><td>0x00003254</td></tr>
<tr><td>_village_bencha</td><td>0x12BFA394</td><td>No</td><td>1463</td><td>0x80007006</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Village_bld_cattleranch</td><td>0x15D118AB</td><td>No</td><td>1552</td><td>0x80007199</td><td>0x0000BA23</td></tr>
<tr><td>_Village_bld_docks</td><td>0xCC016B02</td><td>No</td><td>1550</td><td>0x80007197</td><td>0x00002A34</td></tr>
<tr><td>_Village_bld_docks02</td><td>0x9910FB38</td><td>No</td><td>5405</td><td>0x8000A9DE</td><td>0x00007565</td></tr>
<tr><td>_Village_bld_docks_Ruined</td><td>0x2F687078</td><td>No</td><td>5221</td><td>0x8000A688</td><td>0x0000B535</td></tr>
<tr><td>_Village_bld_farmhouse</td><td>0xD3D977BE</td><td>No</td><td>1551</td><td>0x80007198</td><td>0x000089BB</td></tr>
<tr><td>_Village_bld_farming01</td><td>0x9E59885F</td><td>No</td><td>1553</td><td>0x8000719A</td><td>0x0000CC9B</td></tr>
<tr><td>_Village_bld_farming02</td><td>0x145C80B8</td><td>No</td><td>1554</td><td>0x8000719B</td><td>0x0000D724</td></tr>
<tr><td>_Village_bld_farming03</td><td>0x3E5F016D</td><td>No</td><td>1555</td><td>0x8000719C</td><td>0x0000F8F5</td></tr>
<tr><td>_Village_bld_farming03_ruined</td><td>0x93F98141</td><td>No</td><td>2080</td><td>0x8000814F</td><td>0x00012CE1</td></tr>
<tr><td>_Village_bld_farming04</td><td>0x344DA88E</td><td>No</td><td>1633</td><td>0x80007336</td><td>0x000023E8</td></tr>
<tr><td>_Village_bld_farming05</td><td>0x164FB7EB</td><td>No</td><td>1634</td><td>0x80007337</td><td>0x00003389</td></tr>
<tr><td>_Village_bld_farming05_ruined</td><td>0x7ADBB0CF</td><td>No</td><td>2104</td><td>0x80008178</td><td>0x0000E49A</td></tr>
<tr><td>_Village_bld_food01</td><td>0xB046C41F</td><td>No</td><td>1635</td><td>0x80007338</td><td>0x00003B5E</td></tr>
<tr><td>_Village_bld_food02</td><td>0x2649BC78</td><td>No</td><td>1636</td><td>0x80007339</td><td>0x00008FF7</td></tr>
<tr><td>_Village_bld_food03</td><td>0x504C3D2D</td><td>No</td><td>1637</td><td>0x8000733A</td><td>0x0000992C</td></tr>
<tr><td>_village_bld_gasstation</td><td>0xD1928BDB</td><td>No</td><td>1521</td><td>0x80007178</td><td>0x00001984</td></tr>
<tr><td>_Village_bld_hangar</td><td>0x7EE71C1B</td><td>No</td><td>1638</td><td>0x8000733B</td><td>0x0000DC2B</td></tr>
<tr><td>_Village_bld_hangar_Ruined</td><td>0x298E1CBF</td><td>No</td><td>5226</td><td>0x8000A695</td><td>0xFFFFFFFF</td></tr>
<tr><td>_Village_bld_house01</td><td>0x4F2E5A1F</td><td>No</td><td>1640</td><td>0x8000733D</td><td>0x0000943F</td></tr>
<tr><td>_Village_bld_house01_ruined</td><td>0x197E0DC3</td><td>No</td><td>5578</td><td>0x8000ABD7</td><td>0x00013D8A</td></tr>
<tr><td>_Village_bld_house02</td><td>0xC5315278</td><td>No</td><td>1639</td><td>0x8000733C</td><td>0x00012CAA</td></tr>
<tr><td>_Village_bld_house02_ruined</td><td>0x492C2946</td><td>No</td><td>5579</td><td>0x8000ABD8</td><td>0x00008E28</td></tr>
<tr><td>_village_bld_housestilts01</td><td>0xDF865002</td><td>No</td><td>1522</td><td>0x80007179</td><td>0x0000CC2D</td></tr>
<tr><td>_village_bld_housestilts01_ruined</td><td>0x1E00F778</td><td>No</td><td>2451</td><td>0x800084B7</td><td>0x00006F4F</td></tr>
<tr><td>_village_bld_housestilts02</td><td>0x618DD86D</td><td>No</td><td>1536</td><td>0x80007187</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_bld_housestilts03</td><td>0x378B57B8</td><td>No</td><td>1537</td><td>0x80007188</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_bld_housestilts04</td><td>0x397E8EEB</td><td>No</td><td>1538</td><td>0x80007189</td><td>0x0000E6AD</td></tr>
<tr><td>_Village_bld_housestilts05</td><td>0x577C7F8E</td><td>No</td><td>1641</td><td>0x8000733E</td><td>0x00001F15</td></tr>
<tr><td>_Village_bld_housestilts05_ruined</td><td>0x8DBB3134</td><td>No</td><td>2452</td><td>0x800084B8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_bld_outhouse</td><td>0x64C2EA2E</td><td>No</td><td>950</td><td>0x800065E4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_bld_plantation01</td><td>0xC04C2E39</td><td>No</td><td>1642</td><td>0x8000733F</td><td>0x00000202</td></tr>
<tr><td>_village_bld_plantation02</td><td>0x5E44D82E</td><td>No</td><td>1643</td><td>0x80007340</td><td>0x0000A524</td></tr>
<tr><td>_village_bld_plantation03</td><td>0xC047B10B</td><td>No</td><td>1644</td><td>0x80007341</td><td>0x000021F1</td></tr>
<tr><td>_village_bld_plantationsmall01</td><td>0x0D2693B0</td><td>No</td><td>1645</td><td>0x80007342</td><td>0x0000C30E</td></tr>
<tr><td>_village_bld_plantationsmall02</td><td>0xF7243277</td><td>No</td><td>1646</td><td>0x80007343</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_bld_plantationsmall02_ruined</td><td>0x972E047B</td><td>No</td><td>5580</td><td>0x8000ABD9</td><td>0x00007C6B</td></tr>
<tr><td>_village_bld_plantationsmall03</td><td>0x1522231A</td><td>No</td><td>1647</td><td>0x80007344</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_bld_shackovergrown01</td><td>0x3E54BBB0</td><td>No</td><td>949</td><td>0x800065E3</td><td>0x0000F26B</td></tr>
<tr><td>_Village_bld_shacksmall01</td><td>0xDA4F734E</td><td>No</td><td>948</td><td>0x800065E2</td><td>0x00006DF4</td></tr>
<tr><td>_Village_bld_shacksmall01_ruined</td><td>0x656B64F4</td><td>No</td><td>2079</td><td>0x8000814E</td><td>0x00000EF9</td></tr>
<tr><td>_village_bld_shacksmall02</td><td>0x3C56C959</td><td>No</td><td>1648</td><td>0x80007345</td><td>0x00011E4E</td></tr>
<tr><td>_village_bld_shacksmall02_Ruined</td><td>0x120AFA6D</td><td>No</td><td>5220</td><td>0x8000A687</td><td>0x00004E3B</td></tr>
<tr><td>_village_bld_shacksmall03</td><td>0xE253FD14</td><td>No</td><td>1649</td><td>0x80007346</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_bld_shacksmall03_ruined</td><td>0xD3CF6F22</td><td>No</td><td>2081</td><td>0x80008151</td><td>0x0000FE63</td></tr>
<tr><td>_village_bld_shacksmall04</td><td>0x445B531F</td><td>No</td><td>1650</td><td>0x80007347</td><td>0x00006E8B</td></tr>
<tr><td>_Village_bld_toolshed</td><td>0xFF3E3C56</td><td>No</td><td>1651</td><td>0x80007348</td><td>0x0000CD45</td></tr>
<tr><td>_Village_bld_watchtower01</td><td>0x8F9B3643</td><td>No</td><td>1652</td><td>0x80007349</td><td>0x000039BE</td></tr>
<tr><td>_Village_bld_watchtower02</td><td>0xF59E156C</td><td>No</td><td>1653</td><td>0x8000734A</td><td>0x000020F1</td></tr>
<tr><td>_Village_bld_watchtower03</td><td>0xEFA04A91</td><td>No</td><td>1654</td><td>0x8000734B</td><td>0x0000CE53</td></tr>
<tr><td>_Village_bld_windmill01</td><td>0xB25A949B</td><td>No</td><td>1655</td><td>0x8000734C</td><td>0x00001292</td></tr>
<tr><td>_Village_bld_windmillbroken</td><td>0x731597AD</td><td>No</td><td>1656</td><td>0x8000734D</td><td>0x00000FF3</td></tr>
<tr><td>_village_campfire</td><td>0xF16D962C</td><td>No</td><td>1464</td><td>0x80007007</td><td>0x00007DE0</td></tr>
<tr><td>_village_cota</td><td>0xE2799EE8</td><td>No</td><td>1413</td><td>0x80006F05</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_fencewood01</td><td>0x729B9AD0</td><td>No</td><td>1411</td><td>0x80006F03</td><td>0x000034D4</td></tr>
<tr><td>_village_fencewood02</td><td>0x5C993997</td><td>No</td><td>1412</td><td>0x80006F04</td><td>0x0000E163</td></tr>
<tr><td>_village_fruitboxstacka</td><td>0x756A0B03</td><td>No</td><td>1408</td><td>0x80006F00</td><td>0x0000F69D</td></tr>
<tr><td>_village_fruitboxstackb</td><td>0xDB6CEA2C</td><td>No</td><td>1409</td><td>0x80006F01</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_fruitboxstackc</td><td>0xD56F1F51</td><td>No</td><td>1410</td><td>0x80006F02</td><td>0xFFFFFFFF</td></tr>
<tr><td>_village_fruitboxstackd</td><td>0xFB7199BA</td><td>No</td><td>1407</td><td>0x80006EFF</td><td>0x00013FFB</td></tr>
<tr><td>_village_ladderwooda</td><td>0x85A82315</td><td>No</td><td>1406</td><td>0x80006EFE</td><td>0x0000178C</td></tr>
<tr><td>_village_lampcolemana</td><td>0x855E87C3</td><td>No</td><td>1405</td><td>0x80006EFD</td><td>0x000128B9</td></tr>
<tr><td>_village_postthin</td><td>0x52A39764</td><td>No</td><td>1227</td><td>0x80006CD9</td><td>0x0001264A</td></tr>
<tr><td>_village_postwide</td><td>0x8C05E6C4</td><td>No</td><td>1228</td><td>0x80006CDA</td><td>0x00013469</td></tr>
<tr><td>_village_prop_chaira</td><td>0x4E88605B</td><td>No</td><td>1403</td><td>0x80006EFB</td><td>0x000124F1</td></tr>
<tr><td>_village_prop_tentsmallpupa</td><td>0xFFAC5A91</td><td>No</td><td>1404</td><td>0x80006EFC</td><td>0x0000A4A5</td></tr>
<tr><td>_village_stairs</td><td>0x2072AC75</td><td>No</td><td>1542</td><td>0x8000718F</td><td>0x00003860</td></tr>
<tr><td>_village_tablewooda</td><td>0x84E2E827</td><td>No</td><td>1402</td><td>0x80006EFA</td><td>0x00010D43</td></tr>
<tr><td>_vzoutpost_bld_alarmtower</td><td>0xB015A102</td><td>No</td><td>2810</td><td>0x80008773</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_alarmtower_ruined</td><td>0x00A16278</td><td>No</td><td>5547</td><td>0x8000AB54</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_barrack</td><td>0x3D078262</td><td>No</td><td>2813</td><td>0x80008776</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_barrack_ruined</td><td>0xF5B28258</td><td>No</td><td>5548</td><td>0x8000AB55</td><td>0x00000C1C</td></tr>
<tr><td>_vzoutpost_bld_barrackabandoned</td><td>0xB9BA6C86</td><td>No</td><td>4064</td><td>0x80009AEA</td><td>0x00006B96</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker</td><td>0xBF32FF01</td><td>No</td><td>2816</td><td>0x80008779</td><td>0x0000DB21</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_AL</td><td>0xCE7223B7</td><td>No</td><td>4969</td><td>0x8000A390</td><td>0x00013E12</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_CH</td><td>0x0D121909</td><td>No</td><td>5445</td><td>0x8000AA4B</td><td>0x00001309</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_GR</td><td>0x47567E8F</td><td>No</td><td>4166</td><td>0x80009C07</td><td>0x00013D10</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_OC</td><td>0x5EE52EDA</td><td>No</td><td>2827</td><td>0x80008786</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_PR</td><td>0x4D5D05FA</td><td>No</td><td>4174</td><td>0x80009C0F</td><td>0x00004B28</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker_ruined</td><td>0x92B36555</td><td>No</td><td>5561</td><td>0x8000AB63</td><td>0x0000B175</td></tr>
<tr><td>_vzoutpost_bld_barrackbunkerabandoned</td><td>0x3E81BC13</td><td>No</td><td>4065</td><td>0x80009AEB</td><td>0x000128AD</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced</td><td>0x23E4CC43</td><td>No</td><td>2819</td><td>0x8000877C</td><td>0x00011E7E</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_AL</td><td>0xCE3EDED1</td><td>No</td><td>4970</td><td>0x8000A391</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_CH</td><td>0x2F50337F</td><td>No</td><td>5446</td><td>0x8000AA4C</td><td>0x0000C5CE</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_GR</td><td>0x1268F4E9</td><td>No</td><td>4167</td><td>0x80009C08</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_OC</td><td>0x11F77F6C</td><td>No</td><td>2828</td><td>0x80008787</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforced_PR</td><td>0x4CF82448</td><td>No</td><td>4175</td><td>0x80009C10</td><td>0x00013A19</td></tr>
<tr><td>_vzoutpost_bld_barrackreinforcedabandoned</td><td>0x9FCA6061</td><td>No</td><td>4066</td><td>0x80009AEC</td><td>0x0000898D</td></tr>
<tr><td>_vzoutpost_bld_barracktent</td><td>0xBE0103C5</td><td>No</td><td>2814</td><td>0x80008777</td><td>0x00001762</td></tr>
<tr><td>_vzoutpost_bld_barracktent_AL</td><td>0xF0CBA403</td><td>No</td><td>4971</td><td>0x8000A392</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_barracktent_CH</td><td>0x7D0535FD</td><td>No</td><td>5447</td><td>0x8000AA4D</td><td>0x00002BDB</td></tr>
<tr><td>_vzoutpost_bld_barracktent_GR</td><td>0xC2DE1C0B</td><td>No</td><td>4168</td><td>0x80009C09</td><td>0x0000FAD4</td></tr>
<tr><td>_vzoutpost_bld_barracktent_OC</td><td>0x27E98286</td><td>No</td><td>2829</td><td>0x80008788</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_barracktent_PR</td><td>0x920621FE</td><td>No</td><td>4176</td><td>0x80009C11</td><td>0x0000B04C</td></tr>
<tr><td>_vzoutpost_bld_barracktent_ruined</td><td>0x6BF67E59</td><td>No</td><td>4141</td><td>0x80009B43</td><td>0x00002043</td></tr>
<tr><td>_vzoutpost_bld_bunker</td><td>0xB6AE801F</td><td>No</td><td>3764</td><td>0x80009726</td><td>0x00007B53</td></tr>
<tr><td>_vzoutpost_bld_garage</td><td>0xB90CBD9B</td><td>No</td><td>2820</td><td>0x8000877D</td><td>0x0000AC73</td></tr>
<tr><td>_vzoutpost_bld_garage_AL</td><td>0x1F388B59</td><td>No</td><td>4972</td><td>0x8000A393</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_garage_CH</td><td>0xA274C987</td><td>No</td><td>5449</td><td>0x8000AA4F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_garage_GR</td><td>0xE604E361</td><td>No</td><td>4165</td><td>0x80009C06</td><td>0x0000D2D7</td></tr>
<tr><td>_vzoutpost_bld_garage_OC</td><td>0x52C0A494</td><td>No</td><td>2831</td><td>0x8000878A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_garage_PR</td><td>0xFE197760</td><td>No</td><td>4177</td><td>0x80009C12</td><td>0x0000F07D</td></tr>
<tr><td>_vzoutpost_bld_garagebunker</td><td>0xB19DDBAC</td><td>No</td><td>2821</td><td>0x8000877E</td><td>0x00007393</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_AL</td><td>0xE49E9CBC</td><td>No</td><td>4973</td><td>0x8000A394</td><td>0x00004C1A</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_CH</td><td>0x8379C056</td><td>No</td><td>5450</td><td>0x8000AA50</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_GR</td><td>0x35F07F90</td><td>No</td><td>4179</td><td>0x80009C14</td><td>0x00006DCA</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_OC</td><td>0x866272FD</td><td>No</td><td>2832</td><td>0x8000878B</td><td>0x00002BC2</td></tr>
<tr><td>_vzoutpost_bld_garagebunker_PR</td><td>0x78D68631</td><td>No</td><td>4178</td><td>0x80009C13</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_guardtower</td><td>0xBA7BB30E</td><td>No</td><td>2812</td><td>0x80008775</td><td>0x0000E8BF</td></tr>
<tr><td>_vzoutpost_bld_guardtower_AL</td><td>0xC39B6AE6</td><td>No</td><td>4974</td><td>0x8000A395</td><td>0x0001000A</td></tr>
<tr><td>_vzoutpost_bld_guardtower_CH</td><td>0x44ACF1F4</td><td>No</td><td>5448</td><td>0x8000AA4E</td><td>0x0000ED30</td></tr>
<tr><td>_vzoutpost_bld_guardtower_GR</td><td>0x900B7B9A</td><td>No</td><td>4170</td><td>0x80009C0B</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_guardtower_OC</td><td>0x8B4ECB1F</td><td>No</td><td>2830</td><td>0x80008789</td><td>0x00002017</td></tr>
<tr><td>_vzoutpost_bld_guardtower_PR</td><td>0x8A04F42F</td><td>No</td><td>4180</td><td>0x80009C15</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_guardtower_ruined</td><td>0x6DF4AFB4</td><td>No</td><td>5563</td><td>0x8000AB65</td><td>0x000070EE</td></tr>
<tr><td>_vzoutpost_bld_hangar</td><td>0x0E8CCD09</td><td>No</td><td>2822</td><td>0x8000877F</td><td>0x00005B7F</td></tr>
<tr><td>_vzoutpost_bld_hangar_AL</td><td>0xDD1B358F</td><td>No</td><td>4975</td><td>0x8000A396</td><td>0x0000BD90</td></tr>
<tr><td>_vzoutpost_bld_hangar_CH</td><td>0xFC0AAA61</td><td>No</td><td>5451</td><td>0x8000AA51</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_hangar_GR</td><td>0x9676B677</td><td>No</td><td>4172</td><td>0x80009C0D</td><td>0x0000F744</td></tr>
<tr><td>_vzoutpost_bld_hangar_OC</td><td>0x7D5DEBB2</td><td>No</td><td>2833</td><td>0x8000878D</td><td>0x0000C38B</td></tr>
<tr><td>_vzoutpost_bld_hangar_PR</td><td>0xA1338882</td><td>No</td><td>4183</td><td>0x80009C19</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_hangarbunker</td><td>0x4C7B99C2</td><td>No</td><td>2818</td><td>0x8000877B</td><td>0x00006EF6</td></tr>
<tr><td>_vzoutpost_bld_helipad</td><td>0x7ADCACC3</td><td>Yes</td><td>2817</td><td>0x8000877A</td><td>0x0000E216</td></tr>
<tr><td>_vzoutpost_bld_pillbox</td><td>0xAF28FC30</td><td>No</td><td>2811</td><td>0x80008774</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_bld_pillbox_ruined</td><td>0x13FAEE9E</td><td>No</td><td>5564</td><td>0x8000AB66</td><td>0x0000E7CE</td></tr>
<tr><td>_vzoutpost_bld_pillboxabandoned</td><td>0xDC44B210</td><td>No</td><td>2956</td><td>0x800089CD</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_fueltanks</td><td>0xC8CA3A68</td><td>Yes</td><td>2815</td><td>0x80008778</td><td>0x00003633</td></tr>
<tr><td>_vzoutpost_fueltanks_PmcCon018</td><td>0x21A4DB9A</td><td>Yes</td><td>5567</td><td>0x8000AB6A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_fueltanks_ruined</td><td>0xEEB1FDF6</td><td>Yes</td><td>5216</td><td>0x8000A683</td><td>0x0000AD0C</td></tr>
<tr><td>_vzoutpost_gatewall_GR</td><td>0x5B462DE0</td><td>No</td><td>4173</td><td>0x80009C0E</td><td>0x000089D7</td></tr>
<tr><td>_vzoutpost_walla</td><td>0x3AF501BE</td><td>No</td><td>2709</td><td>0x80008707</td><td>0x000032DD</td></tr>
<tr><td>_vzoutpost_walla_AL</td><td>0xD3F86B56</td><td>No</td><td>4976</td><td>0x8000A397</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_walla_CH</td><td>0x15098DA4</td><td>No</td><td>5452</td><td>0x8000AA52</td><td>0x0000206F</td></tr>
<tr><td>_vzoutpost_walla_GR</td><td>0x60B7C92A</td><td>No</td><td>4169</td><td>0x80009C0A</td><td>0x0000BA60</td></tr>
<tr><td>_vzoutpost_walla_oc</td><td>0x9BABCB8F</td><td>No</td><td>2835</td><td>0x80008790</td><td>0x00008DBD</td></tr>
<tr><td>_vzoutpost_wallA_PR</td><td>0x7825E09F</td><td>No</td><td>4181</td><td>0x80009C17</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_wallb</td><td>0xDCFCBC89</td><td>No</td><td>2716</td><td>0x8000870F</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_wallb_AL</td><td>0xC95CE00F</td><td>No</td><td>4977</td><td>0x8000A398</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_wallb_CH</td><td>0xE84C54E1</td><td>No</td><td>5453</td><td>0x8000AA53</td><td>0x000059E7</td></tr>
<tr><td>_vzoutpost_wallb_GR</td><td>0x82B860F7</td><td>No</td><td>4171</td><td>0x80009C0C</td><td>0x0000559E</td></tr>
<tr><td>_vzoutpost_wallb_oc</td><td>0x699F9632</td><td>No</td><td>2836</td><td>0x80008791</td><td>0x0000A929</td></tr>
<tr><td>_vzoutpost_wallB_PR</td><td>0x8D753302</td><td>No</td><td>4182</td><td>0x80009C18</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_wallgate</td><td>0x3F5E24C4</td><td>No</td><td>4549</td><td>0x80009F1E</td><td>0xFFFFFFFF</td></tr>
<tr><td>_vzoutpost_wallgate_AL</td><td>0x093B0CE4</td><td>No</td><td>4978</td><td>0x8000A399</td><td>0x000041CC</td></tr>
<tr><td>_vzoutpost_wallgate_OC</td><td>0xFDF85725</td><td>No</td><td>2834</td><td>0x8000878E</td><td>0x0000B579</td></tr>
<tr><td>_vzoutpost_wallgate_PR</td><td>0xC25082C9</td><td>No</td><td>4184</td><td>0x80009C1A</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_corner16x16a</td><td>0x85141433</td><td>No</td><td>248</td><td>0x80004DB9</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_corner16x16a_ruined</td><td>0x8261B337</td><td>No</td><td>2105</td><td>0x8000817A</td><td>0x000081A5</td></tr>
<tr><td>_white_bld_corner16x16b</td><td>0xAB168E9C</td><td>No</td><td>239</td><td>0x80004DB0</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_corner16x16b_ruined</td><td>0xAD04F78A</td><td>No</td><td>3277</td><td>0x80008F4E</td><td>0x0000974A</td></tr>
<tr><td>_white_bld_corner8x16a</td><td>0x882C056E</td><td>No</td><td>241</td><td>0x80004DB2</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_corner8x16a_ruined</td><td>0x73172994</td><td>No</td><td>3278</td><td>0x80008F4F</td><td>0x0000E89F</td></tr>
<tr><td>_white_bld_corner8x16b</td><td>0xEA335B79</td><td>No</td><td>243</td><td>0x80004DB4</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_corner8x16b_ruined</td><td>0x8B61580D</td><td>No</td><td>2477</td><td>0x800084D2</td><td>0x00009CAD</td></tr>
<tr><td>_white_bld_corner8x8a</td><td>0x1033A6B9</td><td>No</td><td>140</td><td>0x80004CD7</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_corner8x8a_ruined</td><td>0x5EE0AE4D</td><td>No</td><td>3290</td><td>0x80008F5C</td><td>0x00009E76</td></tr>
<tr><td>_white_bld_corner8x8b</td><td>0xAE2C50AE</td><td>No</td><td>236</td><td>0x80004DAD</td><td>0x0000B9FB</td></tr>
<tr><td>_white_bld_corner8x8b_ruined</td><td>0xA8B95BD4</td><td>No</td><td>2476</td><td>0x800084D1</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_corner8x8c</td><td>0x102F298B</td><td>No</td><td>242</td><td>0x80004DB3</td><td>0x0001399F</td></tr>
<tr><td>_white_bld_corner8x8c_ruined</td><td>0xBD4679EF</td><td>No</td><td>2480</td><td>0x800084D5</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_segment16x16a</td><td>0xD04E4EBD</td><td>No</td><td>237</td><td>0x80004DAE</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_segment16x16a_ruined</td><td>0x51C256D1</td><td>No</td><td>2475</td><td>0x800084D0</td><td>0x00005FCA</td></tr>
<tr><td>_white_bld_segment8x16a</td><td>0x1784EFB8</td><td>No</td><td>238</td><td>0x80004DAF</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_segment8x16a_ruined</td><td>0x9B007386</td><td>No</td><td>3275</td><td>0x80008F4C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_segment8x16b</td><td>0xA181F75F</td><td>No</td><td>240</td><td>0x80004DB1</td><td>0x000029AC</td></tr>
<tr><td>_white_bld_segment8x16b_ruined</td><td>0x90A13303</td><td>No</td><td>2478</td><td>0x800084D3</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_segment8x8a</td><td>0x8452890B</td><td>No</td><td>247</td><td>0x80004DB8</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_bld_segment8x8a_ruined</td><td>0x07C71C6F</td><td>No</td><td>3276</td><td>0x80008F4D</td><td>0x00010DC9</td></tr>
<tr><td>_white_freewaytrenchbridge01_overpass_autobridge</td><td>0x9033E10A</td><td>No</td><td>3552</td><td>0x800093BA</td><td>0x00001C3A</td></tr>
<tr><td>_white_freewaytrenchbridge01_underpass</td><td>0x3783B2E9</td><td>No</td><td>3321</td><td>0x80008F85</td><td>0x000051B6</td></tr>
<tr><td>_white_merge_brick</td><td>0x7C671538</td><td>No</td><td>640</td><td>0x80005C48</td><td>0x0000CB14</td></tr>
<tr><td>_white_merge_dirt</td><td>0xFE900046</td><td>No</td><td>639</td><td>0x80005C47</td><td>0x00001B19</td></tr>
<tr><td>_white_mergebrick</td><td>0x0A713425</td><td>No</td><td>3311</td><td>0x80008F7B</td><td>0x00009685</td></tr>
<tr><td>_white_road10</td><td>0x402F5EAB</td><td>No</td><td>306</td><td>0x80004E04</td><td>0x0000F9CD</td></tr>
<tr><td>_white_road10cross</td><td>0xC1D5C7E1</td><td>No</td><td>308</td><td>0x80004E06</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_road10cross5</td><td>0x74506BF2</td><td>No</td><td>309</td><td>0x80004E07</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_road10l</td><td>0x343FA8D5</td><td>No</td><td>310</td><td>0x80004E08</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_road10t</td><td>0x3453308D</td><td>No</td><td>311</td><td>0x80004E09</td><td>0x00000A70</td></tr>
<tr><td>_white_road10t5</td><td>0x7BA8DD5E</td><td>No</td><td>312</td><td>0x80004E0A</td><td>0x000007AF</td></tr>
<tr><td>_white_road5</td><td>0x0B1184A5</td><td>No</td><td>307</td><td>0x80004E05</td><td>0x0000FE5D</td></tr>
<tr><td>_white_road5cross</td><td>0x809AD98B</td><td>No</td><td>316</td><td>0x80004E0E</td><td>0x00010BF9</td></tr>
<tr><td>_white_road5l</td><td>0x92E62E1B</td><td>No</td><td>313</td><td>0x80004E0B</td><td>0x00001821</td></tr>
<tr><td>_white_road5t</td><td>0x13218EC3</td><td>No</td><td>314</td><td>0x80004E0C</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_road5t10</td><td>0x238CC3E0</td><td>No</td><td>315</td><td>0x80004E0D</td><td>0x0000EE20</td></tr>
<tr><td>_white_road_merge01</td><td>0x51131270</td><td>No</td><td>634</td><td>0x80005C40</td><td>0x000047FC</td></tr>
<tr><td>_white_sidewalk</td><td>0x4DC93618</td><td>No</td><td>318</td><td>0x80004E10</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_sidewalk02</td><td>0x2AA416B2</td><td>No</td><td>3261</td><td>0x80008F3C</td><td>0x00010C08</td></tr>
<tr><td>_white_sidewalksmall</td><td>0x051DCF81</td><td>No</td><td>2029</td><td>0x800080CC</td><td>0x0000D38E</td></tr>
<tr><td>_white_wallcorner</td><td>0x275B525D</td><td>No</td><td>229</td><td>0x80004DA6</td><td>0x000027E7</td></tr>
<tr><td>_white_wallcorner_pristine</td><td>0x03131C28</td><td>No</td><td>4197</td><td>0x80009C29</td><td>0xFFFFFFFF</td></tr>
<tr><td>_white_walllong</td><td>0xE69D1104</td><td>No</td><td>230</td><td>0x80004DA7</td><td>0x0000322B</td></tr>
<tr><td>_white_walllong_pristine</td><td>0x92CDFB03</td><td>No</td><td>4199</td><td>0x80009C2B</td><td>0x0000EBF3</td></tr>
<tr><td>_white_wallshort</td><td>0x4A59C690</td><td>No</td><td>231</td><td>0x80004DA8</td><td>0x00003AB8</td></tr>
<tr><td>_white_wallshort_pristine</td><td>0x554AE977</td><td>No</td><td>4198</td><td>0x80009C2A</td><td>0x00007E75</td></tr>
<tr><td>A10</td><td>0xD035894D</td><td>No</td><td>1823</td><td>0x800076AE</td><td>0x0000B0FB</td></tr>
<tr><td>A8 15m DeadEnd</td><td>0xAB804258</td><td>No</td><td>93</td><td>0x80004BF9</td><td>0x0000A0E9</td></tr>
<tr><td>A8 15m Four</td><td>0x2721975F</td><td>No</td><td>92</td><td>0x80004BF8</td><td>0x0000041F</td></tr>
<tr><td>A8 15m L</td><td>0x457F5FFD</td><td>No</td><td>94</td><td>0x80004BFA</td><td>0x00012F99</td></tr>
<tr><td>A8 15m Road</td><td>0xAE748E09</td><td>No</td><td>95</td><td>0x80004BFB</td><td>0x0000F912</td></tr>
<tr><td>A8 15m T</td><td>0xC5BAC0A5</td><td>No</td><td>91</td><td>0x80004BF7</td><td>0x00009CD2</td></tr>
<tr><td>A8 Enemy</td><td>0xD4A0D006</td><td>No</td><td>96</td><td>0x80004BFC</td><td>0x0000B0C3</td></tr>
<tr><td>AA (Advanced)</td><td>0x6B27034E</td><td>No</td><td>2418</td><td>0x80008452</td><td>0x000008D3</td></tr>
<tr><td>AA (Basic)</td><td>0x9954F398</td><td>No</td><td>2415</td><td>0x8000844F</td><td>0x0000A1CF</td></tr>
<tr><td>AA (Jammer)</td><td>0x3A8084E0</td><td>No</td><td>2419</td><td>0x80008453</td><td>0x0000403C</td></tr>
<tr><td>AA (Medium)</td><td>0xA4045DDB</td><td>No</td><td>2417</td><td>0x80008451</td><td>0x00012854</td></tr>
<tr><td>AA Missile</td><td>0x4FCA603B</td><td>No</td><td>26</td><td>0x80004379</td><td>0x0000654D</td></tr>
<tr><td>AA Missile (amraam)</td><td>0xB4C61361</td><td>No</td><td>5511</td><td>0x8000AAC6</td><td>0xFFFFFFFF</td></tr>
<tr><td>abatters</td><td>0x695C8E03</td><td>No</td><td>391</td><td>0x8000556A</td><td>0x00005704</td></tr>
<tr><td>Action Hijack Prop (Grenade)</td><td>0x7984A387</td><td>No</td><td>1778</td><td>0x800075E4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Action Hijack Prop (Pistol)</td><td>0x456017C2</td><td>No</td><td>1777</td><td>0x800075E3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Action Hijack Prop (Rifle)</td><td>0xC736471B</td><td>No</td><td>4407</td><td>0x80009DE7</td><td>0x00010575</td></tr>
<tr><td>AH1Z</td><td>0x2FF37317</td><td>Yes</td><td>1769</td><td>0x800075DB</td><td>0x00008D58</td></tr>
<tr><td>AH1Z (Driver)</td><td>0x7337DAC2</td><td>Yes</td><td>1770</td><td>0x800075DC</td><td>0x0000D0E1</td></tr>
<tr><td>AH1Z (Ewan)</td><td>0xB8AE263B</td><td>Yes</td><td>5970</td><td>0x8000B35E</td><td>0x00000CA5</td></tr>
<tr><td>AH1Z (Full)</td><td>0x9E563131</td><td>Yes</td><td>1771</td><td>0x800075DD</td><td>0x00006C96</td></tr>
<tr><td>Aid Worker (Female)</td><td>0x8BA8A22A</td><td>No</td><td>2142</td><td>0x800081A5</td><td>0x00004EBC</td></tr>
<tr><td>Aid Worker Male</td><td>0xC53404FC</td><td>No</td><td>2141</td><td>0x800081A4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Air Boat</td><td>0xB017A293</td><td>Yes</td><td>3332</td><td>0x80008FF8</td><td>0x0000AFEE</td></tr>
<tr><td>Air Boat (Driver)</td><td>0xBDDE21EE</td><td>Yes</td><td>3335</td><td>0x80008FFB</td><td>0x0000F699</td></tr>
<tr><td>Air Boat (Driver) (Civ Poor female)</td><td>0xC71ACCBD</td><td>Yes</td><td>4666</td><td>0x80009FDC</td><td>0x00013207</td></tr>
<tr><td>Air Boat (Driver) (Civ Poor male)</td><td>0x5BB2AF10</td><td>Yes</td><td>4665</td><td>0x80009FDB</td><td>0x00011191</td></tr>
<tr><td>Air Boat (Full)</td><td>0xEB754F35</td><td>Yes</td><td>3680</td><td>0x8000952F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Airboat_Driver</td><td>0x5877732E</td><td>Yes</td><td>5079</td><td>0x8000A40E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Airstrike AA Missile</td><td>0x57A81395</td><td>No</td><td>4891</td><td>0x8000A269</td><td>0x000044E6</td></tr>
<tr><td>Airstrike AT Missile</td><td>0x99178348</td><td>No</td><td>4080</td><td>0x80009AFA</td><td>0xFFFFFFFF</td></tr>
<tr><td>AL Baseball Bat</td><td>0x8370A9EF</td><td>No</td><td>3814</td><td>0x800097CF</td><td>0xFFFFFFFF</td></tr>
<tr><td>AL Defender (AA)</td><td>0x4DB3557A</td><td>No</td><td>5020</td><td>0x8000A3C9</td><td>0x0000EC5D</td></tr>
<tr><td>AL Defender (AT)</td><td>0x60CB7BF5</td><td>No</td><td>5021</td><td>0x8000A3CA</td><td>0x0000F63A</td></tr>
<tr><td>AL Defender (AT) (Window Spawner)</td><td>0xE62D4B32</td><td>No</td><td>3003</td><td>0x80008A23</td><td>0x00000186</td></tr>
<tr><td>AL Defender (MG)</td><td>0xF2A22EA0</td><td>No</td><td>5022</td><td>0x8000A3CB</td><td>0x0001054F</td></tr>
<tr><td>AL Defender (Rifle)</td><td>0x4791BB94</td><td>No</td><td>5019</td><td>0x8000A3C8</td><td>0x0000AF3B</td></tr>
<tr><td>AL Golf Club</td><td>0x0FA8CB7A</td><td>No</td><td>3813</td><td>0x800097CE</td><td>0xFFFFFFFF</td></tr>
<tr><td>ALHQSpawnList</td><td>0xD4D6A410</td><td>No</td><td>3809</td><td>0x800097C8</td><td>0x0000CA43</td></tr>
<tr><td>AllCon003_Peng</td><td>0x55012554</td><td>No</td><td>5012</td><td>0x8000A3C0</td><td>0xFFFFFFFF</td></tr>
<tr><td>AllDbSpawner</td><td>0xDB7FA4B4</td><td>No</td><td>2382</td><td>0x8000833A</td><td>0x00005E9C</td></tr>
<tr><td>AllDbSpawner (Squad Full AT)</td><td>0x7F637141</td><td>No</td><td>3018</td><td>0x80008A32</td><td>0x000026BD</td></tr>
<tr><td>AllDbSpawner (Squad Half AT)</td><td>0x293FB845</td><td>No</td><td>3019</td><td>0x80008A33</td><td>0x0000227B</td></tr>
<tr><td>AllDbSpawner (Squad Quarter AT)</td><td>0x7FA52B06</td><td>No</td><td>5908</td><td>0x8000B03B</td><td>0xFFFFFFFF</td></tr>
<tr><td>AllDbSpawner (Squad)</td><td>0x38CF880B</td><td>No</td><td>3013</td><td>0x80008A2D</td><td>0x00010C56</td></tr>
<tr><td>AllHq_Interior</td><td>0xC8EF281E</td><td>No</td><td>2364</td><td>0x8000831E</td><td>0x0000203D</td></tr>
<tr><td>Allied</td><td>0xBBC34EF4</td><td>No</td><td>13</td><td>0x80002CF0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Allied Airborne</td><td>0xC9010376</td><td>No</td><td>1314</td><td>0x80006E3F</td><td>0x00005061</td></tr>
<tr><td>Allied Airborne (AT)</td><td>0x7F4797AA</td><td>No</td><td>4508</td><td>0x80009E66</td><td>0x00005029</td></tr>
<tr><td>Allied Airborne (Light MG)</td><td>0xC357E50F</td><td>No</td><td>4507</td><td>0x80009E65</td><td>0xFFFFFFFF</td></tr>
<tr><td>Allied Boss</td><td>0xAC3B6A63</td><td>No</td><td>2161</td><td>0x800081BB</td><td>0x00004AD4</td></tr>
<tr><td>Allied Boss (Invincible)</td><td>0xD8ABEF7D</td><td>No</td><td>5752</td><td>0x8000ADA2</td><td>0x0000046E</td></tr>
<tr><td>Allied Boss (Wheelchair)</td><td>0x28DBE71C</td><td>No</td><td>3853</td><td>0x8000980B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Allied Destroyer</td><td>0x4D9AEFA3</td><td>Yes</td><td>3206</td><td>0x80008EF8</td><td>0x000119B2</td></tr>
<tr><td>Allied Destroyer (Full)</td><td>0xEB3948C5</td><td>Yes</td><td>3220</td><td>0x80008F06</td><td>0x00005624</td></tr>
<tr><td>Allied Destroyer (Jammer)</td><td>0xA4E888AC</td><td>Yes</td><td>3235</td><td>0x80008F17</td><td>0xFFFFFFFF</td></tr>
<tr><td>Allied Heavy (AA)</td><td>0x271F10CC</td><td>No</td><td>4055</td><td>0x80009AE0</td><td>0x0000B2A9</td></tr>
<tr><td>Allied Heavy (AT Rocket)</td><td>0xD18F961F</td><td>No</td><td>1353</td><td>0x80006EC2</td><td>0x0000C896</td></tr>
<tr><td>Allied Heavy (Light MG)</td><td>0x3BC90F3E</td><td>No</td><td>1312</td><td>0x80006E3D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Allied Medic</td><td>0x2A36FD82</td><td>No</td><td>2316</td><td>0x800082D0</td><td>0x00002684</td></tr>
<tr><td>Allied Officer</td><td>0x01BDAD6E</td><td>No</td><td>1313</td><td>0x80006E3E</td><td>0x0000F890</td></tr>
<tr><td>Allied Paratrooper</td><td>0xBF4829E3</td><td>No</td><td>5007</td><td>0x8000A3BB</td><td>0x00010E98</td></tr>
<tr><td>Allied Pilot</td><td>0xACA6923E</td><td>No</td><td>1316</td><td>0x80006E42</td><td>0xFFFFFFFF</td></tr>
<tr><td>Allied Pilot (God)</td><td>0x218470B5</td><td>No</td><td>5969</td><td>0x8000B35D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Allied Prisoner</td><td>0xC526991C</td><td>No</td><td>2163</td><td>0x800081BD</td><td>0x00013943</td></tr>
<tr><td>Allied Sailor</td><td>0xE2A857D8</td><td>No</td><td>1317</td><td>0x80006E43</td><td>0x00005D91</td></tr>
<tr><td>Allied Sailor (AA)</td><td>0xBF287DA3</td><td>No</td><td>4056</td><td>0x80009AE1</td><td>0x0000F7BF</td></tr>
<tr><td>Allied Sailor (Light MG)</td><td>0xE593B215</td><td>No</td><td>4058</td><td>0x80009AE3</td><td>0x00010A00</td></tr>
<tr><td>Allied Soldier</td><td>0xC864E4A2</td><td>No</td><td>1311</td><td>0x80006E3C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Allied Soldier (Bench Press)</td><td>0x297C6502</td><td>No</td><td>3811</td><td>0x800097CC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Allied Soldier (Hip Hop Dancing)</td><td>0x68813B31</td><td>No</td><td>3812</td><td>0x800097CD</td><td>0x00011061</td></tr>
<tr><td>Allied Starter 01</td><td>0x050E6C22</td><td>No</td><td>2158</td><td>0x800081B8</td><td>0x0000F8A5</td></tr>
<tr><td>Allied Starter 02</td><td>0x8715F48D</td><td>No</td><td>2159</td><td>0x800081B9</td><td>0x000085A3</td></tr>
<tr><td>Allied Starter 03</td><td>0x5D1373D8</td><td>No</td><td>2160</td><td>0x800081BA</td><td>0x0000D58C</td></tr>
<tr><td>Allied Starter 04</td><td>0xDF07748B</td><td>No</td><td>2335</td><td>0x800082E7</td><td>0x00011C83</td></tr>
<tr><td>Allied Starter 05</td><td>0x7D049BAE</td><td>No</td><td>2336</td><td>0x800082E8</td><td>0x0000DC9F</td></tr>
<tr><td>Allied Starters</td><td>0x183F7210</td><td>No</td><td>2157</td><td>0x800081B6</td><td>0x00000211</td></tr>
<tr><td>Allied Worker</td><td>0x5AACD022</td><td>No</td><td>2162</td><td>0x800081BC</td><td>0x00012709</td></tr>
<tr><td>Allied Worker (Baseball)</td><td>0x0F837BD3</td><td>No</td><td>3816</td><td>0x800097D1</td><td>0x00006622</td></tr>
<tr><td>Allied Worker (Golf)</td><td>0xBC664A97</td><td>No</td><td>3815</td><td>0x800097D0</td><td>0x00010869</td></tr>
<tr><td>Allied Worker B</td><td>0x64B0DDB8</td><td>No</td><td>2355</td><td>0x800082FC</td><td>0x0000AC96</td></tr>
<tr><td>AlliedHQDbSpawner</td><td>0x729E051D</td><td>No</td><td>5639</td><td>0x8000AC8A</td><td>0x0000D8B9</td></tr>
<tr><td>AlliesSkirmishTest</td><td>0xD181EFFB</td><td>No</td><td>3091</td><td>0x80008BAF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Alouette 3 Transport (VZ) (Delivery)</td><td>0x76B96B2A</td><td>Yes</td><td>2225</td><td>0x800081FE</td><td>0x00010F17</td></tr>
<tr><td>Alouette3 (base)</td><td>0x725FE691</td><td>Yes</td><td>1209</td><td>0x80006CC3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Alouette3 Attack (base)</td><td>0x9217A97B</td><td>Yes</td><td>2253</td><td>0x80008227</td><td>0x0000C2A9</td></tr>
<tr><td>Alouette3 Attack (PR)</td><td>0xD944EA90</td><td>Yes</td><td>2255</td><td>0x80008229</td><td>0x0000D69A</td></tr>
<tr><td>Alouette3 Attack (PR) (Driver)</td><td>0x597C43AF</td><td>Yes</td><td>2257</td><td>0x8000822B</td><td>0x0000FBF5</td></tr>
<tr><td>Alouette3 Attack (PR) (Ewan)</td><td>0x5076A026</td><td>Yes</td><td>5971</td><td>0x8000B35F</td><td>0x0000F787</td></tr>
<tr><td>Alouette3 Attack (PR) (Full)</td><td>0x422E9BE4</td><td>Yes</td><td>2264</td><td>0x80008232</td><td>0xFFFFFFFF</td></tr>
<tr><td>Alouette3 Attack (VZ)</td><td>0x0384A0EE</td><td>Yes</td><td>2256</td><td>0x8000822A</td><td>0x0000FB19</td></tr>
<tr><td>Alouette3 Attack (VZ) (Driver)</td><td>0x10440985</td><td>Yes</td><td>2258</td><td>0x8000822C</td><td>0x00013A61</td></tr>
<tr><td>Alouette3 Attack (VZ) (Ewan)</td><td>0x76908A00</td><td>Yes</td><td>5972</td><td>0x8000B360</td><td>0x00004048</td></tr>
<tr><td>Alouette3 Attack (VZ) (Full)</td><td>0xDB44C532</td><td>Yes</td><td>2265</td><td>0x80008233</td><td>0xFFFFFFFF</td></tr>
<tr><td>Alouette3 Elite</td><td>0x3D582382</td><td>Yes</td><td>2254</td><td>0x80008228</td><td>0x00004B4E</td></tr>
<tr><td>Alouette3 Elite (Driver)</td><td>0x34CE8229</td><td>Yes</td><td>2266</td><td>0x80008234</td><td>0x00013F89</td></tr>
<tr><td>Alouette3 Elite (Ewan)</td><td>0x5F7B68E4</td><td>Yes</td><td>5973</td><td>0x8000B361</td><td>0x0000669E</td></tr>
<tr><td>Alouette3 Elite (Full)</td><td>0x4656350E</td><td>Yes</td><td>2267</td><td>0x80008235</td><td>0x000084F8</td></tr>
<tr><td>Alouette3 Superiority</td><td>0x048DB4E4</td><td>Yes</td><td>1210</td><td>0x80006CC4</td><td>0x0000DFF1</td></tr>
<tr><td>Alouette3 Superiority (Driver)</td><td>0xC3E6EDC3</td><td>Yes</td><td>1782</td><td>0x800075E8</td><td>0x0000FB39</td></tr>
<tr><td>Alouette3 Superiority (Ewan)</td><td>0x63E0E84A</td><td>Yes</td><td>5974</td><td>0x8000B362</td><td>0x00009324</td></tr>
<tr><td>Alouette3 SuperiorityElite (Base)</td><td>0xF2FF732B</td><td>Yes</td><td>3634</td><td>0x8000946E</td><td>0x00002905</td></tr>
<tr><td>Alouette3 Transport</td><td>0x4B481510</td><td>Yes</td><td>2223</td><td>0x800081FC</td><td>0x00000D4B</td></tr>
<tr><td>Alouette3 Transport (PR)</td><td>0x1C12B15F</td><td>Yes</td><td>2228</td><td>0x80008201</td><td>0x00009B2D</td></tr>
<tr><td>Alouette3 Transport (PR) (Driver)</td><td>0x8DFF774A</td><td>Yes</td><td>2230</td><td>0x80008203</td><td>0xFFFFFFFF</td></tr>
<tr><td>Alouette3 Transport (PR) (Ewan)</td><td>0x2EEC9423</td><td>Yes</td><td>5975</td><td>0x8000B363</td><td>0x000108E2</td></tr>
<tr><td>Alouette3 Transport (PR) (Extraction)</td><td>0x00DC7AB9</td><td>Yes</td><td>4409</td><td>0x80009DEE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Alouette3 Transport (PR) (Full)</td><td>0xD41A4509</td><td>Yes</td><td>2231</td><td>0x80008204</td><td>0x00000A49</td></tr>
<tr><td>Alouette3 Transport (PR) (Pursuit)</td><td>0x59787A94</td><td>Yes</td><td>4910</td><td>0x8000A281</td><td>0x00013C70</td></tr>
<tr><td>Alouette3 Transport (VZ)</td><td>0x3AAD2021</td><td>Yes</td><td>2229</td><td>0x80008202</td><td>0xFFFFFFFF</td></tr>
<tr><td>Alouette3 Transport (VZ) (Driver)</td><td>0x1A774D3C</td><td>Yes</td><td>2224</td><td>0x800081FD</td><td>0x0000B309</td></tr>
<tr><td>Alouette3 Transport (VZ) (Ewan)</td><td>0xEF9E6839</td><td>Yes</td><td>5976</td><td>0x8000B364</td><td>0xFFFFFFFF</td></tr>
<tr><td>Alouette3 Transport (VZ) (Pursuit)</td><td>0x4D3FA01E</td><td>Yes</td><td>4911</td><td>0x8000A282</td><td>0x00005DD9</td></tr>
<tr><td>Alouette3 Transport (VZA Intro) (Driver)</td><td>0x71A0FFFF</td><td>Yes</td><td>5960</td><td>0x8000B22D</td><td>0x0000E385</td></tr>
<tr><td>Altagracia Test Traffic (VZ)</td><td>0x9537357E</td><td>No</td><td>2516</td><td>0x8000854C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ambulance</td><td>0xDC065B95</td><td>Yes</td><td>2562</td><td>0x800085C2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ambulance (Driver)</td><td>0x26FA5C20</td><td>Yes</td><td>4285</td><td>0x80009CB8</td><td>0x0000610A</td></tr>
<tr><td>Ambulance (Driver) (Civ Doctor 2 female)</td><td>0x2077F55C</td><td>Yes</td><td>4287</td><td>0x80009CBA</td><td>0x0000F7F6</td></tr>
<tr><td>Ambulance (Driver) (Civ Doctor female)</td><td>0x713DE192</td><td>Yes</td><td>4286</td><td>0x80009CB9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ambulance_Driver</td><td>0xE80E4896</td><td>Yes</td><td>5054</td><td>0x8000A3F3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ammo Pickup (1xC4)</td><td>0x00C8F9AC</td><td>No</td><td>2194</td><td>0x800081DF</td><td>0x00005401</td></tr>
<tr><td>Ammo Pickup (Bullet)</td><td>0x4E3F3CE6</td><td>No</td><td>7</td><td>0x8000233E</td><td>0x00002DCC</td></tr>
<tr><td>Ammo Pickup (Full C4)</td><td>0x789E2A14</td><td>No</td><td>508</td><td>0x800056DD</td><td>0x00008BD3</td></tr>
<tr><td>Ammo Pickup (Grenades)</td><td>0xD5F15751</td><td>No</td><td>2171</td><td>0x800081C5</td><td>0x00001200</td></tr>
<tr><td>Ammo Pickup (Rocket)</td><td>0xA79D21D2</td><td>No</td><td>507</td><td>0x800056DC</td><td>0x0000D7D2</td></tr>
<tr><td>Ammo Pickup (Single Grenade)</td><td>0xC475E2EC</td><td>No</td><td>2182</td><td>0x800081D2</td><td>0x000065CB</td></tr>
<tr><td>Ammo Pickup (Small)</td><td>0x500E0DC7</td><td>No</td><td>4914</td><td>0x8000A286</td><td>0x00005C3D</td></tr>
<tr><td>ammo_designator_beacon</td><td>0xC6B65A9B</td><td>No</td><td>893</td><td>0x800063E5</td><td>0x000120A2</td></tr>
<tr><td>ammo_designator_beacon_light</td><td>0x13CC5386</td><td>No</td><td>5789</td><td>0x8000AEF5</td><td>0x0000747C</td></tr>
<tr><td>AMX30</td><td>0x36AEDE98</td><td>Yes</td><td>1615</td><td>0x80007255</td><td>0x000074E1</td></tr>
<tr><td>AMX30 (Base)</td><td>0x7D2C4AA0</td><td>Yes</td><td>3450</td><td>0x800092B8</td><td>0xFFFFFFFF</td></tr>
<tr><td>AMX30 (Driver)</td><td>0xA5572877</td><td>Yes</td><td>1613</td><td>0x80007253</td><td>0x00000F15</td></tr>
<tr><td>Amx30 (Full)</td><td>0x48B454BC</td><td>Yes</td><td>1614</td><td>0x80007254</td><td>0x0000BFC4</td></tr>
<tr><td>AMX30 (Tanks)</td><td>0x5069957C</td><td>Yes</td><td>1612</td><td>0x80007252</td><td>0x0000D51F</td></tr>
<tr><td>AMX30 AA</td><td>0x45D11D72</td><td>Yes</td><td>1617</td><td>0x80007257</td><td>0xFFFFFFFF</td></tr>
<tr><td>AMX30 AA (Driver)</td><td>0xF2A84619</td><td>Yes</td><td>1618</td><td>0x80007258</td><td>0xFFFFFFFF</td></tr>
<tr><td>AMX30 Elite</td><td>0x3F6EDBED</td><td>Yes</td><td>1616</td><td>0x80007256</td><td>0x00009BC1</td></tr>
<tr><td>AMX30 Elite (Driver)</td><td>0x6648F4F8</td><td>Yes</td><td>1619</td><td>0x80007259</td><td>0xFFFFFFFF</td></tr>
<tr><td>AMX30 Elite (Full)</td><td>0x901B8C7F</td><td>Yes</td><td>1620</td><td>0x8000725B</td><td>0xFFFFFFFF</td></tr>
<tr><td>AMX30_RUIN</td><td>0x421F2DE1</td><td>Yes</td><td>3465</td><td>0x800092C7</td><td>0x00011237</td></tr>
<tr><td>AMXFullSpawnlist</td><td>0x1AC7CF1F</td><td>No</td><td>2403</td><td>0x800083F1</td><td>0x00010E2A</td></tr>
<tr><td>Antenna</td><td>0x1D49104E</td><td>No</td><td>1908</td><td>0x80007864</td><td>0x0000C1D5</td></tr>
<tr><td>Anti-Material Rifle</td><td>0x3326597B</td><td>No</td><td>1338</td><td>0x80006EAB</td><td>0x00009256</td></tr>
<tr><td>Anti-Material Rifle (KSVK)</td><td>0x050B3C39</td><td>No</td><td>1343</td><td>0x80006EB3</td><td>0x00000919</td></tr>
<tr><td>Anti-Material Rifle Bullet</td><td>0xA4B7629D</td><td>No</td><td>1337</td><td>0x80006EAA</td><td>0x00006579</td></tr>
<tr><td>AP Autocannon Shell</td><td>0x91A508E2</td><td>No</td><td>2290</td><td>0x8000824E</td><td>0x0000E610</td></tr>
<tr><td>AP Autocannon Shell (CH)</td><td>0xF842A460</td><td>No</td><td>4093</td><td>0x80009B08</td><td>0x0000268A</td></tr>
<tr><td>APC</td><td>0x9CDBD62D</td><td>Yes</td><td>2786</td><td>0x80008758</td><td>0xFFFFFFFF</td></tr>
<tr><td>APC_Passenger</td><td>0x15D3C4A4</td><td>Yes</td><td>5096</td><td>0x8000A421</td><td>0x000056E4</td></tr>
<tr><td>Armor (Building)</td><td>0x434436BF</td><td>No</td><td>476</td><td>0x800056B2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Armor (Bunker)</td><td>0x9FA80226</td><td>No</td><td>4052</td><td>0x80009ADD</td><td>0x000023A2</td></tr>
<tr><td>Armor (Hero)</td><td>0xBFCEDA4F</td><td>No</td><td>482</td><td>0x800056BD</td><td>0x00006E14</td></tr>
<tr><td>Armor (Human)</td><td>0xC37C574A</td><td>No</td><td>481</td><td>0x800056BC</td><td>0x00006ACD</td></tr>
<tr><td>Armor (HVT)</td><td>0x12E4336D</td><td>No</td><td>4899</td><td>0x8000A273</td><td>0x0000F7EC</td></tr>
<tr><td>Armor (Light)</td><td>0x64F3FB33</td><td>No</td><td>1572</td><td>0x8000720F</td><td>0x0000F759</td></tr>
<tr><td>Armor (Medium)</td><td>0x6E97F4AC</td><td>No</td><td>4051</td><td>0x80009ADC</td><td>0x00000B27</td></tr>
<tr><td>Armor (Prop)</td><td>0x6759484A</td><td>No</td><td>477</td><td>0x800056B3</td><td>0x00004B4A</td></tr>
<tr><td>Armor (Prop.Fragile)</td><td>0xD97E8024</td><td>No</td><td>503</td><td>0x800056D7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Armor (Road)</td><td>0x0B7B8D99</td><td>No</td><td>501</td><td>0x800056D4</td><td>0x0000D337</td></tr>
<tr><td>Armor (Tank)</td><td>0x17FACC4F</td><td>Yes</td><td>479</td><td>0x800056B5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Armor (Terrain)</td><td>0x9C8D8282</td><td>No</td><td>1124</td><td>0x80006B52</td><td>0x00008662</td></tr>
<tr><td>Armor (Vegetation)</td><td>0xAE5E289B</td><td>No</td><td>6078</td><td>0x900001C0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Armor (Vehicle)</td><td>0x8260A047</td><td>No</td><td>478</td><td>0x800056B4</td><td>0x00013A5D</td></tr>
<tr><td>Armored Bank Truck</td><td>0x2F0DA5B8</td><td>Yes</td><td>1796</td><td>0x800075FA</td><td>0x0000F45F</td></tr>
<tr><td>Armored Bank Truck (driver)</td><td>0xBEB9DA97</td><td>Yes</td><td>3647</td><td>0x800094E1</td><td>0x00010B4A</td></tr>
<tr><td>Armored Bank Truck (Driver) (Civ Taxi Driver male)</td><td>0xE915BA21</td><td>Yes</td><td>4280</td><td>0x80009CB3</td><td>0x00007A7F</td></tr>
<tr><td>Armored Bank Truck_Driver</td><td>0xD3EFA565</td><td>Yes</td><td>5055</td><td>0x8000A3F4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Artillery Shell</td><td>0xC05F0F87</td><td>No</td><td>1342</td><td>0x80006EB2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Artillery Smoke Shell</td><td>0x84C5189C</td><td>No</td><td>4904</td><td>0x8000A278</td><td>0x0000803C</td></tr>
<tr><td>Assault Rifle</td><td>0x8387E850</td><td>No</td><td>22</td><td>0x8000436F</td><td>0x0000A710</td></tr>
<tr><td>Assault Rifle (VZ)</td><td>0x72DBE6E1</td><td>No</td><td>1141</td><td>0x80006B64</td><td>0x00006F2B</td></tr>
<tr><td>Assault Rifle (VZ) (Window Spawner)</td><td>0xEC1A6E46</td><td>No</td><td>2999</td><td>0x80008A1F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Assault Rifle (Window Spawner)</td><td>0x9A0D0F39</td><td>No</td><td>2998</td><td>0x80008A1E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Assault Rifle Bullet</td><td>0xA0D42D08</td><td>No</td><td>25</td><td>0x80004375</td><td>0x0000CD9A</td></tr>
<tr><td>Assault Rifle Bullet (GR)</td><td>0x6EF0F048</td><td>No</td><td>4086</td><td>0x80009B00</td><td>0x0000ACCA</td></tr>
<tr><td>AT Missile</td><td>0xFC44785E</td><td>No</td><td>1110</td><td>0x80006B44</td><td>0x00007E57</td></tr>
<tr><td>AT Missile (CH)</td><td>0x8893FB24</td><td>No</td><td>5813</td><td>0x8000AF76</td><td>0xFFFFFFFF</td></tr>
<tr><td>AT Rocket</td><td>0x1153B156</td><td>No</td><td>1130</td><td>0x80006B58</td><td>0x00008E10</td></tr>
<tr><td>Atmosphere</td><td>0x04047F6D</td><td>No</td><td>6019</td><td>0x900000CF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Atmosphere (interior)</td><td>0xDD9463C2</td><td>No</td><td>2377</td><td>0x80008333</td><td>0x0000F1F7</td></tr>
<tr><td>Audible (Vehicle HIGH)</td><td>0x1D04192A</td><td>No</td><td>3231</td><td>0x80008F12</td><td>0x0000B955</td></tr>
<tr><td>Audible (Vehicle LOW)</td><td>0x52C5A3FE</td><td>No</td><td>3229</td><td>0x80008F10</td><td>0xFFFFFFFF</td></tr>
<tr><td>Audible (Vehicle MEDIUM)</td><td>0xDED48B6D</td><td>No</td><td>3230</td><td>0x80008F11</td><td>0x00010E92</td></tr>
<tr><td>Austin (base)</td><td>0xB2CDBC45</td><td>No</td><td>2608</td><td>0x800085F7</td><td>0x0000ADF4</td></tr>
<tr><td>Austin (CIV)</td><td>0xCEBC1D68</td><td>No</td><td>1787</td><td>0x800075ED</td><td>0x00010AA1</td></tr>
<tr><td>Austin (CIV) (Driver)</td><td>0x4768D8C7</td><td>No</td><td>1789</td><td>0x800075EF</td><td>0x0001182F</td></tr>
<tr><td>Austin (CIV) (Driver) (Mechanic male)</td><td>0x6663D1C1</td><td>No</td><td>4425</td><td>0x80009E03</td><td>0x000065AB</td></tr>
<tr><td>Austin (Civ) (Full)</td><td>0x3C10400C</td><td>No</td><td>1790</td><td>0x800075F0</td><td>0x0000B070</td></tr>
<tr><td>Austin (OC)</td><td>0x99691E22</td><td>No</td><td>861</td><td>0x800063B6</td><td>0x0000DABD</td></tr>
<tr><td>Austin (OC) (Driver)</td><td>0x3A3FD9C9</td><td>No</td><td>1683</td><td>0x800074BD</td><td>0x00007254</td></tr>
<tr><td>Austin (OC) (Full)</td><td>0x59183AAE</td><td>No</td><td>1791</td><td>0x800075F1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Austin_Driver</td><td>0x5B327388</td><td>No</td><td>5075</td><td>0x8000A409</td><td>0x0000D4D6</td></tr>
<tr><td>Autocannon Shell (AL)</td><td>0xE235626F</td><td>No</td><td>4095</td><td>0x80009B0A</td><td>0x0000F9EF</td></tr>
<tr><td>Autocannon Shell (GR)</td><td>0x7638E52B</td><td>No</td><td>4094</td><td>0x80009B09</td><td>0x0000C44F</td></tr>
<tr><td>Automatic Rifle</td><td>0x388A8AE8</td><td>No</td><td>1147</td><td>0x80006B6A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Automatic Rifle (Chinese)</td><td>0x4BEC74A2</td><td>No</td><td>1143</td><td>0x80006B66</td><td>0x0000D9D1</td></tr>
<tr><td>Automatic Rifle (GR)</td><td>0xBF4E2628</td><td>No</td><td>4103</td><td>0x80009B12</td><td>0xFFFFFFFF</td></tr>
<tr><td>Automatic Rifle Bullet</td><td>0xBC623E70</td><td>No</td><td>1148</td><td>0x80006B6B</td><td>0x0000BFE6</td></tr>
<tr><td>Automatic Rifle Bullet (CH)</td><td>0x07CC98C6</td><td>No</td><td>4087</td><td>0x80009B01</td><td>0x0000D30F</td></tr>
<tr><td>Automatic Rifle Bullet (GR)</td><td>0x71DD9D80</td><td>No</td><td>4099</td><td>0x80009B0E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Autopistol Bullet</td><td>0x76146767</td><td>No</td><td>1577</td><td>0x80007215</td><td>0x0001026C</td></tr>
<tr><td>Avenger (Cargo)</td><td>0x334FCB0C</td><td>No</td><td>2615</td><td>0x800085FE</td><td>0x00002796</td></tr>
<tr><td>b52_ghost</td><td>0x8307FF04</td><td>No</td><td>381</td><td>0x8000522A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Barco</td><td>0xAC33E162</td><td>No</td><td>2280</td><td>0x80008244</td><td>0x000048A6</td></tr>
<tr><td>Barco (Driver)</td><td>0x33F98B89</td><td>No</td><td>2281</td><td>0x80008245</td><td>0x000136D9</td></tr>
<tr><td>Barco (Driver) (Civ Poor female)</td><td>0xC0AD2F6E</td><td>No</td><td>4645</td><td>0x80009FC7</td><td>0x00006DAC</td></tr>
<tr><td>Barco (Driver) (Civ Poor male)</td><td>0x551E7EA3</td><td>No</td><td>4644</td><td>0x80009FC6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Barco_Driver</td><td>0xC38D6323</td><td>No</td><td>5080</td><td>0x8000A40F</td><td>0x0000572D</td></tr>
<tr><td>Barrel_Hijack_Entrance</td><td>0x12673ECD</td><td>No</td><td>695</td><td>0x80005FB0</td><td>0x000061CA</td></tr>
<tr><td>Basic4Way</td><td>0xDE7BB098</td><td>No</td><td>89</td><td>0x80004B94</td><td>0x0000603D</td></tr>
<tr><td>basicTestRoad</td><td>0xA935C8AB</td><td>No</td><td>46</td><td>0x80004515</td><td>0xFFFFFFFF</td></tr>
<tr><td>battle_med (30x30)</td><td>0x465C372F</td><td>No</td><td>4408</td><td>0x80009DED</td><td>0x00009789</td></tr>
<tr><td>battle_med_100mRadius 0x8000a6e8</td><td>0x43B98313</td><td>No</td><td>5239</td><td>0x8000A6E8</td><td>0xFFFFFFFF</td></tr>
<tr><td>battle_med_150mRadius 0x8000a6ea</td><td>0xC9F53405</td><td>No</td><td>5241</td><td>0x8000A6EA</td><td>0xFFFFFFFF</td></tr>
<tr><td>battle_med_250mRadius 0x8000a6e9</td><td>0xA3400AE6</td><td>No</td><td>5240</td><td>0x8000A6E9</td><td>0xFFFFFFFF</td></tr>
<tr><td>battle_med_300mRadius 0x8000a6e7</td><td>0x2FDC5BEA</td><td>No</td><td>5238</td><td>0x8000A6E7</td><td>0x00003207</td></tr>
<tr><td>Beacon Designator</td><td>0x689CE209</td><td>No</td><td>894</td><td>0x800063E7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Bench Seat (Left)</td><td>0x2FEB65F0</td><td>No</td><td>107</td><td>0x80004C14</td><td>0xFFFFFFFF</td></tr>
<tr><td>Bench Seat (Right)</td><td>0x353C04FB</td><td>No</td><td>106</td><td>0x80004C13</td><td>0xFFFFFFFF</td></tr>
<tr><td>benches</td><td>0x431E175D</td><td>No</td><td>110</td><td>0x80004C1B</td><td>0x00001D5F</td></tr>
<tr><td>Binoculars</td><td>0xA0332C77</td><td>No</td><td>4048</td><td>0x80009AD8</td><td>0x0001110E</td></tr>
<tr><td>Blanco</td><td>0x5E5548C8</td><td>No</td><td>1363</td><td>0x80006ECF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Blast Cannon Shell</td><td>0x56075C12</td><td>No</td><td>4886</td><td>0x8000A264</td><td>0x0000FD5A</td></tr>
<tr><td>bld_attachTemplate</td><td>0x5487BA35</td><td>No</td><td>6117</td><td>0x900001EF</td><td>0x00010458</td></tr>
<tr><td>bld_debrisdestructTemplate</td><td>0x5F144D41</td><td>No</td><td>6118</td><td>0x900001F0</td><td>0x00013450</td></tr>
<tr><td>bld_pieceTemplate050</td><td>0x1DD7B153</td><td>No</td><td>6116</td><td>0x900001EE</td><td>0x0000A9DB</td></tr>
<tr><td>bld_pieceTemplate100</td><td>0x153BCAA1</td><td>No</td><td>2773</td><td>0x8000874B</td><td>0x0000CDC9</td></tr>
<tr><td>bld_pieceTemplate200</td><td>0xC82F8C6E</td><td>No</td><td>2775</td><td>0x8000874D</td><td>0x0000529E</td></tr>
<tr><td>bld_sliceTemplate050</td><td>0x1EDD4587</td><td>No</td><td>6115</td><td>0x900001ED</td><td>0x00000888</td></tr>
<tr><td>bld_sliceTemplate100</td><td>0x8F5A93AD</td><td>No</td><td>2774</td><td>0x8000874C</td><td>0x00009EE8</td></tr>
<tr><td>bld_sliceTemplate200</td><td>0x4160D2DA</td><td>No</td><td>2776</td><td>0x8000874E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Boat</td><td>0x45847B03</td><td>Yes</td><td>833</td><td>0x8000638E</td><td>0x00012EA8</td></tr>
<tr><td>Boat Seats (Driver) (VZ)</td><td>0x5984F529</td><td>Yes</td><td>1025</td><td>0x800068AB</td><td>0x0000340C</td></tr>
<tr><td>BoatList_Amazon_Act1</td><td>0x85405DEC</td><td>Yes</td><td>4579</td><td>0x80009F48</td><td>0x0000842C</td></tr>
<tr><td>BoatList_Amazon_Act2</td><td>0x1F3D7EC3</td><td>Yes</td><td>5940</td><td>0x8000B1E1</td><td>0xFFFFFFFF</td></tr>
<tr><td>BoatList_AngelFalls_Ac1</td><td>0xD2C7B595</td><td>Yes</td><td>5643</td><td>0x8000AC8E</td><td>0x0000AA18</td></tr>
<tr><td>BoatList_Caracas_Act1_A</td><td>0x7495A0A6</td><td>Yes</td><td>4565</td><td>0x80009F34</td><td>0x0000FEC4</td></tr>
<tr><td>BoatList_Caracas_Act1_B</td><td>0xF69D2911</td><td>Yes</td><td>4566</td><td>0x80009F35</td><td>0x00003F86</td></tr>
<tr><td>BoatList_Caracas_Act1_C</td><td>0xFC9AF3EC</td><td>Yes</td><td>4567</td><td>0x80009F37</td><td>0x00000AC6</td></tr>
<tr><td>BoatList_Caracas_Act2_ALL</td><td>0xEA2C5BC5</td><td>Yes</td><td>4568</td><td>0x80009F3A</td><td>0x00006546</td></tr>
<tr><td>BoatList_Caracas_Act2_CHI</td><td>0x4D76D8E2</td><td>Yes</td><td>5188</td><td>0x8000A4B3</td><td>0x000050DE</td></tr>
<tr><td>BoatList_Caracas_Act3_ALL</td><td>0xC7957078</td><td>Yes</td><td>4569</td><td>0x80009F3B</td><td>0x0000A08B</td></tr>
<tr><td>BoatList_Caracas_Act3_CHI</td><td>0x4E288B0F</td><td>Yes</td><td>4570</td><td>0x80009F3C</td><td>0x0000D843</td></tr>
<tr><td>BoatList_Cumana_Act1_A</td><td>0xA109E753</td><td>Yes</td><td>4572</td><td>0x80009F3E</td><td>0x0001253B</td></tr>
<tr><td>BoatList_Cumana_Act1_B</td><td>0xC70C61BC</td><td>Yes</td><td>4573</td><td>0x80009F3F</td><td>0x000129AB</td></tr>
<tr><td>BoatList_Cumana_Act1_C</td><td>0x410F6061</td><td>Yes</td><td>4574</td><td>0x80009F40</td><td>0x0000DE65</td></tr>
<tr><td>BoatList_Cumana_Act2_CHI</td><td>0x8C249C77</td><td>Yes</td><td>4575</td><td>0x80009F42</td><td>0xFFFFFFFF</td></tr>
<tr><td>BoatList_Jungle_Act1</td><td>0xCD93B7A1</td><td>Yes</td><td>4578</td><td>0x80009F47</td><td>0x0000698D</td></tr>
<tr><td>BoatList_Jungle_Act2</td><td>0x4B8C2F36</td><td>Yes</td><td>5938</td><td>0x8000B1DF</td><td>0x00005718</td></tr>
<tr><td>BoatList_Mar_City_Act1_A</td><td>0x53020772</td><td>Yes</td><td>4358</td><td>0x80009D2C</td><td>0xFFFFFFFF</td></tr>
<tr><td>BoatList_Mar_City_Act1_B</td><td>0xD5098FDD</td><td>Yes</td><td>4359</td><td>0x80009D2F</td><td>0x000029D3</td></tr>
<tr><td>BoatList_Mar_City_Act1_C</td><td>0xEB0773E8</td><td>Yes</td><td>4360</td><td>0x80009D30</td><td>0xFFFFFFFF</td></tr>
<tr><td>BoatList_Mar_City_Act1_D</td><td>0xECFAAB1B</td><td>Yes</td><td>4361</td><td>0x80009D34</td><td>0xFFFFFFFF</td></tr>
<tr><td>BoatList_Mar_City_Act2_A</td><td>0x9E0D2FC1</td><td>Yes</td><td>4563</td><td>0x80009F31</td><td>0x00009B7A</td></tr>
<tr><td>BoatList_Mar_City_Act3_A</td><td>0x123F28B4</td><td>Yes</td><td>4564</td><td>0x80009F32</td><td>0x0000A70A</td></tr>
<tr><td>BoatList_Merida_Act1</td><td>0x8D7F0FF0</td><td>Yes</td><td>4576</td><td>0x80009F43</td><td>0x000024EE</td></tr>
<tr><td>BoatList_Merida_Act2</td><td>0x777CAEB7</td><td>Yes</td><td>4577</td><td>0x80009F44</td><td>0x00003BDA</td></tr>
<tr><td>BoatList_OC_Depot</td><td>0xE4E9AEDB</td><td>Yes</td><td>5918</td><td>0x8000B1C8</td><td>0x00002049</td></tr>
<tr><td>BoatList_OC_Depot_Act1</td><td>0xC0692A6B</td><td>Yes</td><td>5633</td><td>0x8000AC83</td><td>0x0000DA1B</td></tr>
<tr><td>BoatList_PirateHQ_Cutter</td><td>0x5BCF12D6</td><td>Yes</td><td>5650</td><td>0x8000AC97</td><td>0x00005A69</td></tr>
<tr><td>BoatList_PirateHQ_Jetski</td><td>0x43943B5F</td><td>Yes</td><td>5648</td><td>0x8000AC95</td><td>0x00010A80</td></tr>
<tr><td>BoatList_PirateHQ_Jetski_Driver</td><td>0x43DE8FEC</td><td>Yes</td><td>5951</td><td>0x8000B1ED</td><td>0x00013FF4</td></tr>
<tr><td>BoatList_PirateIsles_Act1_A</td><td>0x098196E7</td><td>Yes</td><td>5962</td><td>0x8000B2D7</td><td>0x00000FBE</td></tr>
<tr><td>BoatList_PmcHQ_Act1</td><td>0xF41256D3</td><td>Yes</td><td>5642</td><td>0x8000AC8D</td><td>0x000047DB</td></tr>
<tr><td>BoatList_Simple</td><td>0x37E6A534</td><td>Yes</td><td>3100</td><td>0x80008BB8</td><td>0x0000F649</td></tr>
<tr><td>BoatList_VZCon001</td><td>0x8EC130AB</td><td>Yes</td><td>5945</td><td>0x8000B1E7</td><td>0x0000FADA</td></tr>
<tr><td>Bomb</td><td>0xA9FD3561</td><td>No</td><td>1574</td><td>0x80007211</td><td>0x00010887</td></tr>
<tr><td>Box</td><td>0xA0787FC8</td><td>No</td><td>0</td><td>0x80000002</td><td>0x00001DBB</td></tr>
<tr><td>Box Trailer</td><td>0x160D3EBD</td><td>No</td><td>1813</td><td>0x800076A4</td><td>0x00009A40</td></tr>
<tr><td>Briefing Interior</td><td>0x0B054E4B</td><td>No</td><td>1913</td><td>0x80007A02</td><td>0x00002763</td></tr>
<tr><td>Buggy</td><td>0x6AFF0875</td><td>Yes</td><td>57</td><td>0x80004730</td><td>0x00007CE0</td></tr>
<tr><td>Buggy (Guerilla driver)</td><td>0xAF3C2665</td><td>Yes</td><td>58</td><td>0x80004732</td><td>0x00008801</td></tr>
<tr><td>Buggy (Hellfire)</td><td>0x8E0908F1</td><td>Yes</td><td>4697</td><td>0x8000A000</td><td>0x000120BB</td></tr>
<tr><td>Buggy (PR)</td><td>0x86835E18</td><td>Yes</td><td>2583</td><td>0x800085DA</td><td>0x000134F7</td></tr>
<tr><td>Buggy_Driver</td><td>0x1FC07476</td><td>Yes</td><td>5070</td><td>0x8000A403</td><td>0x00011448</td></tr>
<tr><td>BuggyPR_Driver</td><td>0x42AE049C</td><td>Yes</td><td>5111</td><td>0x8000A452</td><td>0x000136D2</td></tr>
<tr><td>Building Slice Collapse</td><td>0x0007CCC4</td><td>No</td><td>83</td><td>0x80004B3D</td><td>0x00005638</td></tr>
<tr><td>Building Spawner</td><td>0x7C3107D5</td><td>No</td><td>1355</td><td>0x80006EC6</td><td>0x0000E514</td></tr>
<tr><td>Bullpup Rifle</td><td>0x3F93CEF7</td><td>No</td><td>994</td><td>0x80006881</td><td>0xFFFFFFFF</td></tr>
<tr><td>Bullpup Rifle (Window Spawner)</td><td>0x4B27AF68</td><td>No</td><td>3001</td><td>0x80008A21</td><td>0x0000E9EC</td></tr>
<tr><td>Bullpup Rifle Bullet</td><td>0xFA695BE9</td><td>No</td><td>995</td><td>0x80006882</td><td>0xFFFFFFFF</td></tr>
<tr><td>Bunker Buster Projectile</td><td>0x74C64496</td><td>No</td><td>2425</td><td>0x8000845D</td><td>0x0000CAE8</td></tr>
<tr><td>C4</td><td>0xCAF30DA8</td><td>No</td><td>707</td><td>0x80005FD3</td><td>0x0000F046</td></tr>
<tr><td>C4 Detonator</td><td>0xA5F4BC6C</td><td>No</td><td>709</td><td>0x80005FD5</td><td>0x0000F8CD</td></tr>
<tr><td>C4 Projectile</td><td>0xFC6B9E2D</td><td>No</td><td>708</td><td>0x80005FD4</td><td>0x000088A2</td></tr>
<tr><td>Car</td><td>0xCE27C791</td><td>No</td><td>499</td><td>0x800056D0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Carbine</td><td>0xDF10D765</td><td>No</td><td>1575</td><td>0x80007212</td><td>0x000121AD</td></tr>
<tr><td>Carbine (Window Spawner)</td><td>0x4EA10F02</td><td>No</td><td>3006</td><td>0x80008A26</td><td>0x0000C745</td></tr>
<tr><td>Carbine Bullet</td><td>0x73697F5F</td><td>No</td><td>5837</td><td>0x8000AF92</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cargo Ship</td><td>0x4CF6278F</td><td>Yes</td><td>3210</td><td>0x80008EFC</td><td>0x000030EC</td></tr>
<tr><td>Carmona</td><td>0xED346E8A</td><td>No</td><td>2292</td><td>0x800082B6</td><td>0x0000E98A</td></tr>
<tr><td>Carpet Bomb Projectile</td><td>0x38F6D4D5</td><td>No</td><td>383</td><td>0x8000522D</td><td>0x00005A93</td></tr>
<tr><td>Cart Worker (female)</td><td>0x80CDF678</td><td>No</td><td>2139</td><td>0x800081A2</td><td>0x00001E37</td></tr>
<tr><td>Cart Worker (male)</td><td>0x20A0AAA9</td><td>No</td><td>2134</td><td>0x8000819D</td><td>0x0000B50A</td></tr>
<tr><td>Cash (Case)</td><td>0xF6FA1AB5</td><td>No</td><td>2627</td><td>0x8000860D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cash (Large)</td><td>0xE8E9D8CA</td><td>No</td><td>2628</td><td>0x8000860E</td><td>0x0000876B</td></tr>
<tr><td>Cash (Medium)</td><td>0x1A7DE40E</td><td>No</td><td>2626</td><td>0x8000860C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cash (Small)</td><td>0xFAA7FE7E</td><td>No</td><td>2625</td><td>0x8000860B</td><td>0x0000506D</td></tr>
<tr><td>Cessna</td><td>0x3C411D08</td><td>No</td><td>1821</td><td>0x800076AC</td><td>0x00006BB0</td></tr>
<tr><td>CH Defender (AA)</td><td>0xDF26D7BC</td><td>No</td><td>5030</td><td>0x8000A3D3</td><td>0x0000D8DC</td></tr>
<tr><td>CH Defender (AT)</td><td>0xD94D6FEF</td><td>No</td><td>5029</td><td>0x8000A3D2</td><td>0xFFFFFFFF</td></tr>
<tr><td>CH Defender (AT) (Window Spawner)</td><td>0x05D217B0</td><td>No</td><td>3004</td><td>0x80008A24</td><td>0x0000015E</td></tr>
<tr><td>CH Defender (MG)</td><td>0xEA3ECB5E</td><td>No</td><td>5040</td><td>0x8000A3DD</td><td>0xFFFFFFFF</td></tr>
<tr><td>CH Defender (Rifle)</td><td>0xAF46FE02</td><td>No</td><td>5028</td><td>0x8000A3D1</td><td>0xFFFFFFFF</td></tr>
<tr><td>CH Defender (Sniper)</td><td>0x1BA70DC1</td><td>No</td><td>5031</td><td>0x8000A3D4</td><td>0x0000551D</td></tr>
<tr><td>Chain Cannon Bullet</td><td>0xA26ABEA5</td><td>No</td><td>4047</td><td>0x80009AD6</td><td>0x00011BF5</td></tr>
<tr><td>Chain Cannon Bullet (CH)</td><td>0x34067D75</td><td>No</td><td>4108</td><td>0x80009B17</td><td>0x0001384B</td></tr>
<tr><td>Chain Cannon Bullet (GR)</td><td>0x50072627</td><td>No</td><td>4115</td><td>0x80009B1E</td><td>0x000069AB</td></tr>
<tr><td>chairs</td><td>0x214F3303</td><td>No</td><td>111</td><td>0x80004C1C</td><td>0x00006D42</td></tr>
<tr><td>CheapDebrisTemplate</td><td>0x31E69F35</td><td>No</td><td>6114</td><td>0x900001EC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cheat RPG</td><td>0x49401D0B</td><td>No</td><td>4893</td><td>0x8000A26B</td><td>0x0001304C</td></tr>
<tr><td>Cheat RPG Rocket</td><td>0xBBF165B1</td><td>No</td><td>4892</td><td>0x8000A26A</td><td>0x00010759</td></tr>
<tr><td>ChiDbSpawner</td><td>0x6E0EED01</td><td>No</td><td>2381</td><td>0x80008339</td><td>0x00010D55</td></tr>
<tr><td>ChiDbSpawner (Squad Full AT)</td><td>0x54D605F4</td><td>No</td><td>5661</td><td>0x8000ACA4</td><td>0x0000BDA1</td></tr>
<tr><td>ChiDbSpawner (Squad Half AT)</td><td>0xBB7FE84C</td><td>No</td><td>5662</td><td>0x8000ACA5</td><td>0x00011CE7</td></tr>
<tr><td>ChiDbSpawner (Squad Quarter AT)</td><td>0x17419369</td><td>No</td><td>5909</td><td>0x8000B03C</td><td>0xFFFFFFFF</td></tr>
<tr><td>ChiDbSpawner (Squad)</td><td>0x2C95035A</td><td>No</td><td>3014</td><td>0x80008A2E</td><td>0x00005721</td></tr>
<tr><td>ChiHq_Interior</td><td>0xA9BF983F</td><td>No</td><td>2363</td><td>0x8000831D</td><td>0xFFFFFFFF</td></tr>
<tr><td>china</td><td>0x41359CCE</td><td>No</td><td>491</td><td>0x800056C6</td><td>0x0000CB52</td></tr>
<tr><td>ChinaSkirmishTest</td><td>0xE54C502A</td><td>No</td><td>3092</td><td>0x80008BB0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chinese Airborne</td><td>0x34DA0AF0</td><td>No</td><td>2295</td><td>0x800082B9</td><td>0x000107FE</td></tr>
<tr><td>Chinese Airborne (AT)</td><td>0x41C0EAE0</td><td>No</td><td>4509</td><td>0x80009E67</td><td>0x00002E0F</td></tr>
<tr><td>Chinese Airborne (Light MG)</td><td>0x8F248EDD</td><td>No</td><td>4510</td><td>0x80009E68</td><td>0x0000B79D</td></tr>
<tr><td>Chinese Boss</td><td>0x03393679</td><td>No</td><td>2156</td><td>0x800081B5</td><td>0x00013FC6</td></tr>
<tr><td>Chinese Boss (Invincible)</td><td>0x70F1D3BB</td><td>No</td><td>5753</td><td>0x8000ADA3</td><td>0x0000BE00</td></tr>
<tr><td>Chinese Destroyer</td><td>0x02DFA76D</td><td>Yes</td><td>3208</td><td>0x80008EFA</td><td>0x00012B8C</td></tr>
<tr><td>Chinese Destroyer (FULL)</td><td>0x4A5512FF</td><td>Yes</td><td>3219</td><td>0x80008F05</td><td>0x0000C1F9</td></tr>
<tr><td>Chinese Destroyer (Jammer)</td><td>0x0177153A</td><td>Yes</td><td>3234</td><td>0x80008F16</td><td>0x0000FB58</td></tr>
<tr><td>Chinese Elite Soldier</td><td>0xA11F6971</td><td>No</td><td>2166</td><td>0x800081C0</td><td>0x00000045</td></tr>
<tr><td>Chinese Heavy (AA)</td><td>0x8B12853E</td><td>No</td><td>4053</td><td>0x80009ADE</td><td>0x00008D73</td></tr>
<tr><td>Chinese Heavy (Light MG)</td><td>0xA7CE8B80</td><td>No</td><td>1351</td><td>0x80006EC0</td><td>0x0000E25A</td></tr>
<tr><td>Chinese Heavy (RPG)</td><td>0xDBACFF2D</td><td>No</td><td>1352</td><td>0x80006EC1</td><td>0x000005E7</td></tr>
<tr><td>Chinese Medic</td><td>0x2CCA7D48</td><td>No</td><td>2152</td><td>0x800081B1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chinese Officer</td><td>0x59ED821C</td><td>No</td><td>2296</td><td>0x800082BA</td><td>0x00012D3F</td></tr>
<tr><td>Chinese Paratrooper</td><td>0x056D6979</td><td>No</td><td>5005</td><td>0x8000A3B9</td><td>0x0000F5DB</td></tr>
<tr><td>Chinese Pilot (God)</td><td>0x7A1028CB</td><td>No</td><td>5840</td><td>0x8000AF95</td><td>0x0000AF30</td></tr>
<tr><td>Chinese Pilot A</td><td>0x579DD039</td><td>No</td><td>2148</td><td>0x800081AD</td><td>0x000004E0</td></tr>
<tr><td>Chinese Pilot B</td><td>0xF5967A2E</td><td>No</td><td>2149</td><td>0x800081AE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chinese Prisoner</td><td>0xCB0A2146</td><td>No</td><td>2151</td><td>0x800081B0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chinese Sailor</td><td>0x65C7D21A</td><td>No</td><td>2150</td><td>0x800081AF</td><td>0x000031D9</td></tr>
<tr><td>Chinese Sailor (AA)</td><td>0x272F8B51</td><td>No</td><td>4057</td><td>0x80009AE2</td><td>0x00010918</td></tr>
<tr><td>Chinese Sailor (Light MG)</td><td>0x515CFB63</td><td>No</td><td>4059</td><td>0x80009AE4</td><td>0x0000D7DC</td></tr>
<tr><td>Chinese Sniper</td><td>0x0B0A1B2B</td><td>No</td><td>1354</td><td>0x80006EC4</td><td>0x0000DD9D</td></tr>
<tr><td>Chinese Soldier</td><td>0x26EC3650</td><td>No</td><td>1350</td><td>0x80006EBF</td><td>0x0000AAD0</td></tr>
<tr><td>Chinese Starter 01</td><td>0xE515DDBC</td><td>No</td><td>2154</td><td>0x800081B3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chinese Starter 02</td><td>0xBF136353</td><td>No</td><td>2155</td><td>0x800081B4</td><td>0x00007866</td></tr>
<tr><td>Chinese Starter 03</td><td>0xDD1153F6</td><td>No</td><td>2337</td><td>0x800082E9</td><td>0x0000974C</td></tr>
<tr><td>Chinese Starter 04</td><td>0xE722ACD5</td><td>No</td><td>2338</td><td>0x800082EA</td><td>0x0000DF65</td></tr>
<tr><td>Chinese Starter 05</td><td>0xBD202C20</td><td>No</td><td>2339</td><td>0x800082EB</td><td>0x0000C11C</td></tr>
<tr><td>Chinese Starters</td><td>0x3DB9383E</td><td>No</td><td>2153</td><td>0x800081B2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chinese Tank Commander</td><td>0x70DA1B50</td><td>Yes</td><td>2297</td><td>0x800082BB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chinese VIP</td><td>0x38C5CB33</td><td>No</td><td>2391</td><td>0x80008385</td><td>0x0000FACE</td></tr>
<tr><td>Chinese Worker</td><td>0xF4D53B94</td><td>No</td><td>2147</td><td>0x800081AC</td><td>0x0000E663</td></tr>
<tr><td>Chinese Worker (Exercise)</td><td>0x38E8BC3F</td><td>No</td><td>3827</td><td>0x800097DD</td><td>0x0000C1B5</td></tr>
<tr><td>ChiVehTraffic</td><td>0x82B00835</td><td>No</td><td>2674</td><td>0x8000867B</td><td>0x00011EBD</td></tr>
<tr><td>chong</td><td>0xF856AB5E</td><td>No</td><td>67</td><td>0x800047A7</td><td>0x00004CC9</td></tr>
<tr><td>chong c1</td><td>0x6101B5F6</td><td>No</td><td>68</td><td>0x800047A9</td><td>0x0000CC60</td></tr>
<tr><td>chong c2</td><td>0xE3093E61</td><td>No</td><td>648</td><td>0x80005D82</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chopper</td><td>0x78CF64E6</td><td>Yes</td><td>2240</td><td>0x80008215</td><td>0x0000D451</td></tr>
<tr><td>Chopper (Driver)</td><td>0x714FA07D</td><td>Yes</td><td>2285</td><td>0x80008249</td><td>0x00004EA4</td></tr>
<tr><td>Chopper (Driver) (Civ Motorcycle male)</td><td>0x47F9E30C</td><td>Yes</td><td>4297</td><td>0x80009CC4</td><td>0x000132F6</td></tr>
<tr><td>Chopper_Driver</td><td>0xC532455F</td><td>Yes</td><td>5113</td><td>0x8000A457</td><td>0xFFFFFFFF</td></tr>
<tr><td>chris</td><td>0xD64BB122</td><td>No</td><td>1781</td><td>0x800075E7</td><td>0xFFFFFFFF</td></tr>
<tr><td>ChrisChickensuit</td><td>0xC2398360</td><td>No</td><td>2306</td><td>0x800082C4</td><td>0xFFFFFFFF</td></tr>
<tr><td>chrisupgrade1</td><td>0x4834745B</td><td>No</td><td>4835</td><td>0x8000A1C1</td><td>0x0000EDAB</td></tr>
<tr><td>chrisupgrade2</td><td>0xAE375384</td><td>No</td><td>4836</td><td>0x8000A1C2</td><td>0xFFFFFFFF</td></tr>
<tr><td>chrisupgrade3</td><td>0xC839BB09</td><td>No</td><td>4837</td><td>0x8000A1C3</td><td>0x0000107B</td></tr>
<tr><td>ChrisV2</td><td>0xAA1A3B0A</td><td>No</td><td>2304</td><td>0x800082C2</td><td>0x00004A3D</td></tr>
<tr><td>ChrisV3</td><td>0xCC1CAF27</td><td>No</td><td>2305</td><td>0x800082C3</td><td>0x00004AA3</td></tr>
<tr><td>Chunk</td><td>0x950E7438</td><td>No</td><td>1093</td><td>0x80006A75</td><td>0x00003969</td></tr>
<tr><td>Chunk Set</td><td>0xC06C5F3C</td><td>No</td><td>389</td><td>0x8000555C</td><td>0x00009019</td></tr>
<tr><td>Chunk Set (Tree Branches)</td><td>0xC2FA6CE5</td><td>No</td><td>1840</td><td>0x800076D5</td><td>0x0000F0F8</td></tr>
<tr><td>Chunk_aa</td><td>0x21EDB019</td><td>No</td><td>1094</td><td>0x80006A76</td><td>0x0000F41F</td></tr>
<tr><td>Chunk_ab</td><td>0xBFE65A0E</td><td>No</td><td>1095</td><td>0x80006A77</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_ac</td><td>0xA1E8696B</td><td>No</td><td>1096</td><td>0x80006A78</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_ad</td><td>0x9FF53238</td><td>No</td><td>840</td><td>0x80006397</td><td>0x000031AE</td></tr>
<tr><td>Chunk_ae</td><td>0xC9F7B2ED</td><td>No</td><td>839</td><td>0x80006396</td><td>0x00001E8F</td></tr>
<tr><td>Chunk_af</td><td>0x47F02A82</td><td>No</td><td>838</td><td>0x80006395</td><td>0x00002792</td></tr>
<tr><td>Chunk_ag</td><td>0x29F239DF</td><td>No</td><td>837</td><td>0x80006394</td><td>0x00001AE4</td></tr>
<tr><td>Chunk_ah</td><td>0x27FF02AC</td><td>No</td><td>842</td><td>0x80006399</td><td>0x0000E63F</td></tr>
<tr><td>Chunk_ai</td><td>0x220137D1</td><td>No</td><td>841</td><td>0x80006398</td><td>0x0000C199</td></tr>
<tr><td>Chunk_aj</td><td>0x9FF9AF66</td><td>No</td><td>766</td><td>0x80006217</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_ak</td><td>0xC1FC2383</td><td>No</td><td>767</td><td>0x80006218</td><td>0x00001174</td></tr>
<tr><td>Chunk_al</td><td>0xC008EC50</td><td>No</td><td>768</td><td>0x80006219</td><td>0x00000EDD</td></tr>
<tr><td>Chunk_am</td><td>0xAA0B0845</td><td>No</td><td>769</td><td>0x8000621A</td><td>0x00007C01</td></tr>
<tr><td>Chunk_asphalt_small02</td><td>0x7A81F6E2</td><td>No</td><td>2797</td><td>0x80008763</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_asphalt_small03</td><td>0xDC84CFBF</td><td>No</td><td>2798</td><td>0x80008764</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_asphalt_small04</td><td>0x7A7D79B4</td><td>No</td><td>2799</td><td>0x80008765</td><td>0x000024ED</td></tr>
<tr><td>Chunk_Branch01</td><td>0xF8EBFE62</td><td>No</td><td>3708</td><td>0x8000955A</td><td>0x0000D1BD</td></tr>
<tr><td>Chunk_Brick_Small01</td><td>0xBF25A4A7</td><td>No</td><td>84</td><td>0x80004B45</td><td>0x0000FE24</td></tr>
<tr><td>Chunk_Brick_Small02</td><td>0x15286AA0</td><td>No</td><td>85</td><td>0x80004B46</td><td>0x00006253</td></tr>
<tr><td>Chunk_Brick_Small03</td><td>0x3F2AEB55</td><td>No</td><td>87</td><td>0x80004B48</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_Brick_Small04</td><td>0x35199276</td><td>No</td><td>86</td><td>0x80004B47</td><td>0x0000283D</td></tr>
<tr><td>Chunk_Concrete_Large01</td><td>0x8B55BA93</td><td>No</td><td>1308</td><td>0x80006D9F</td><td>0x0000C182</td></tr>
<tr><td>Chunk_Concrete_Large02</td><td>0xB15834FC</td><td>No</td><td>1309</td><td>0x80006DA0</td><td>0x0000E3E8</td></tr>
<tr><td>Chunk_Concrete_Small01</td><td>0x02E016BB</td><td>No</td><td>1468</td><td>0x80007013</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_Concrete_Small02</td><td>0xE8E22C64</td><td>No</td><td>1469</td><td>0x80007014</td><td>0x0000705E</td></tr>
<tr><td>Chunk_Concrete_Small03</td><td>0x02E493E9</td><td>No</td><td>1470</td><td>0x80007015</td><td>0x00001867</td></tr>
<tr><td>Chunk_Concrete_Small04</td><td>0x68E77312</td><td>No</td><td>1471</td><td>0x80007016</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_Metal_LargeA</td><td>0x4C8224B9</td><td>No</td><td>760</td><td>0x80006210</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_Metal_LargeB</td><td>0xEA7ACEAE</td><td>No</td><td>761</td><td>0x80006211</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_Metal_LargeC</td><td>0x4C7DA78B</td><td>No</td><td>778</td><td>0x80006223</td><td>0x00006473</td></tr>
<tr><td>Chunk_Metal_LargeD</td><td>0xCA89A6D8</td><td>No</td><td>779</td><td>0x80006224</td><td>0x00007FD2</td></tr>
<tr><td>Chunk_Metal_LongA</td><td>0x17D9F02E</td><td>No</td><td>762</td><td>0x80006212</td><td>0x0000D683</td></tr>
<tr><td>Chunk_Metal_PipeA</td><td>0x16468BCC</td><td>No</td><td>763</td><td>0x80006214</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_Metal_smallA</td><td>0x7EE8355D</td><td>No</td><td>764</td><td>0x80006215</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_Metal_SmallB</td><td>0xFCE0ACF2</td><td>No</td><td>1518</td><td>0x80007175</td><td>0x00011AA5</td></tr>
<tr><td>Chunk_Metal_SmallC</td><td>0x1EE3210F</td><td>No</td><td>1519</td><td>0x80007176</td><td>0x00001FEB</td></tr>
<tr><td>Chunk_rpg</td><td>0x3341C41C</td><td>No</td><td>1976</td><td>0x80008015</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_Tile_Small01</td><td>0xBC16FBAE</td><td>No</td><td>1498</td><td>0x80007032</td><td>0xFFFFFFFF</td></tr>
<tr><td>Chunk_Tile_Small02</td><td>0x1E1E51B9</td><td>No</td><td>1499</td><td>0x80007033</td><td>0x00010DC5</td></tr>
<tr><td>Chunk_Tree_Branch</td><td>0x1EE3478A</td><td>No</td><td>1839</td><td>0x800076D4</td><td>0x0000615B</td></tr>
<tr><td>chunk_wood_beam</td><td>0xD84D272A</td><td>No</td><td>2794</td><td>0x80008760</td><td>0x00011C43</td></tr>
<tr><td>chunk_wood_panel</td><td>0xC478DD9B</td><td>No</td><td>2795</td><td>0x80008761</td><td>0x0001278D</td></tr>
<tr><td>chunk_wood_small01</td><td>0x6CA9C995</td><td>No</td><td>2792</td><td>0x8000875E</td><td>0x0000922E</td></tr>
<tr><td>chunk_wood_small02</td><td>0xCAA20ECA</td><td>No</td><td>2793</td><td>0x8000875F</td><td>0x0000A085</td></tr>
<tr><td>ChunkFlame</td><td>0x2B687AE5</td><td>No</td><td>1097</td><td>0x80006A79</td><td>0x0000F54D</td></tr>
<tr><td>ChunkFlamePersistent</td><td>0xF0325066</td><td>No</td><td>1156</td><td>0x80006BAA</td><td>0x0000C5A6</td></tr>
<tr><td>chunks_debriseffect</td><td>0xA6175DE4</td><td>No</td><td>1307</td><td>0x80006D9E</td><td>0x00005F43</td></tr>
<tr><td>chunks_rpg</td><td>0x673929DB</td><td>No</td><td>1977</td><td>0x80008016</td><td>0xFFFFFFFF</td></tr>
<tr><td>ChunkSmoke</td><td>0x4B366E23</td><td>No</td><td>1098</td><td>0x80006A7A</td><td>0x0000C0C1</td></tr>
<tr><td>Cigarette (base)</td><td>0x5809751D</td><td>No</td><td>1766</td><td>0x800075D8</td><td>0x00007956</td></tr>
<tr><td>Cigarette_Driver</td><td>0x101FD2E0</td><td>No</td><td>5081</td><td>0x8000A410</td><td>0x0000D1E6</td></tr>
<tr><td>CIV</td><td>0xDCC8B14D</td><td>No</td><td>483</td><td>0x800056BE</td><td>0x00009F20</td></tr>
<tr><td>Civ Beach A (Female)</td><td>0x42183C02</td><td>No</td><td>2115</td><td>0x80008189</td><td>0x000137F4</td></tr>
<tr><td>Civ Beach B (Female)</td><td>0x17DB1883</td><td>No</td><td>2116</td><td>0x8000818A</td><td>0x00006E6A</td></tr>
<tr><td>Civ Beach C (Female)</td><td>0x9CF92F0C</td><td>No</td><td>2345</td><td>0x800082F2</td><td>0x00002A73</td></tr>
<tr><td>Civ Beach D (Female)</td><td>0x3C2BB74D</td><td>No</td><td>2346</td><td>0x800082F3</td><td>0x0000CDFF</td></tr>
<tr><td>Civ Business (Female)</td><td>0xEAF68A6A</td><td>No</td><td>1329</td><td>0x80006E52</td><td>0x00005CE6</td></tr>
<tr><td>Civ Business (male)</td><td>0xD581782F</td><td>No</td><td>1339</td><td>0x80006EAD</td><td>0x0000981B</td></tr>
<tr><td>Civ Business B (male)</td><td>0x93B36E7D</td><td>No</td><td>2135</td><td>0x8000819E</td><td>0x0000F2B8</td></tr>
<tr><td>Civ Casual (female)</td><td>0x2A5C35C9</td><td>No</td><td>1319</td><td>0x80006E45</td><td>0xFFFFFFFF</td></tr>
<tr><td>Civ Casual (male)</td><td>0xA22617AC</td><td>No</td><td>1318</td><td>0x80006E44</td><td>0xFFFFFFFF</td></tr>
<tr><td>Civ Casual with Hat (female)</td><td>0xE1785BBC</td><td>No</td><td>2356</td><td>0x800082FD</td><td>0xFFFFFFFF</td></tr>
<tr><td>Civ Cowboy (male)</td><td>0xAA5175EE</td><td>No</td><td>1320</td><td>0x80006E46</td><td>0x0000C84E</td></tr>
<tr><td>Civ Doctor (female)</td><td>0x6837129F</td><td>No</td><td>2329</td><td>0x800082DE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Civ Doctor 2 (female)</td><td>0x6B7E69E5</td><td>No</td><td>2330</td><td>0x800082DF</td><td>0x00001CA2</td></tr>
<tr><td>Civ Fueltrailer</td><td>0x73999888</td><td>No</td><td>4012</td><td>0x800099A2</td><td>0x00002F10</td></tr>
<tr><td>Civ Fueltrailer_PmcCon018</td><td>0x022F55BA</td><td>No</td><td>5566</td><td>0x8000AB68</td><td>0xFFFFFFFF</td></tr>
<tr><td>Civ Industrial (female)</td><td>0xDFA85263</td><td>No</td><td>817</td><td>0x80006318</td><td>0x00011A35</td></tr>
<tr><td>Civ Industrial (male)</td><td>0x9B1A9B92</td><td>No</td><td>818</td><td>0x8000631A</td><td>0x00000E9D</td></tr>
<tr><td>Civ Journalist A (male)</td><td>0x6477AB1B</td><td>No</td><td>2325</td><td>0x800082DA</td><td>0x0000769D</td></tr>
<tr><td>Civ Journalist B (male)</td><td>0x48F58526</td><td>No</td><td>2326</td><td>0x800082DB</td><td>0x0001331F</td></tr>
<tr><td>Civ Journalist C (female)</td><td>0x9B77D2F0</td><td>No</td><td>2327</td><td>0x800082DC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Civ Journalist D (female)</td><td>0xC1A99029</td><td>No</td><td>2328</td><td>0x800082DD</td><td>0x00003083</td></tr>
<tr><td>Civ Motorcycle (male)</td><td>0x63825598</td><td>Yes</td><td>2358</td><td>0x800082FF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Civ Poor (female)</td><td>0x6D8CBE4C</td><td>No</td><td>2131</td><td>0x80008199</td><td>0x00004E19</td></tr>
<tr><td>Civ Poor (male)</td><td>0x26E9D55D</td><td>No</td><td>2130</td><td>0x80008198</td><td>0x000100F4</td></tr>
<tr><td>Civ Rich (female)</td><td>0x4A506AEA</td><td>No</td><td>2133</td><td>0x8000819C</td><td>0x000093D2</td></tr>
<tr><td>Civ Rich (male)</td><td>0x996B44AF</td><td>No</td><td>2132</td><td>0x8000819B</td><td>0x0000A246</td></tr>
<tr><td>Civ Taxi Driver (male)</td><td>0x7DCB768D</td><td>No</td><td>2359</td><td>0x80008300</td><td>0x0000A29B</td></tr>
<tr><td>Civilian</td><td>0xD2601C86</td><td>No</td><td>108</td><td>0x80004C15</td><td>0xFFFFFFFF</td></tr>
<tr><td>CivilianList</td><td>0x059AF94E</td><td>No</td><td>102</td><td>0x80004C05</td><td>0xFFFFFFFF</td></tr>
<tr><td>ClownCar</td><td>0x04770EA2</td><td>No</td><td>1906</td><td>0x8000780B</td><td>0x0000BBCA</td></tr>
<tr><td>Cluster Bomb Projectile</td><td>0xBEC3E888</td><td>No</td><td>2421</td><td>0x80008459</td><td>0x00006374</td></tr>
<tr><td>Cluster Bomblet Projectile</td><td>0xE9EF1357</td><td>No</td><td>2422</td><td>0x8000845A</td><td>0x0000EBEE</td></tr>
<tr><td>Coanda</td><td>0x937D0BCB</td><td>Yes</td><td>867</td><td>0x800063BF</td><td>0x0001200A</td></tr>
<tr><td>Coanda Attack</td><td>0x8FA0A591</td><td>Yes</td><td>3644</td><td>0x80009478</td><td>0x0000E802</td></tr>
<tr><td>Coanda Attack (Driver)</td><td>0xA156846C</td><td>Yes</td><td>3646</td><td>0x8000947A</td><td>0x0000042B</td></tr>
<tr><td>Coanda Attack (Ewan)</td><td>0xFDBB6BA9</td><td>Yes</td><td>5978</td><td>0x8000B366</td><td>0x00010CD7</td></tr>
<tr><td>Coanda Attack (Full)</td><td>0x7313CA1B</td><td>Yes</td><td>3654</td><td>0x80009515</td><td>0x000085C1</td></tr>
<tr><td>Coanda Gunship</td><td>0xB321082B</td><td>Yes</td><td>868</td><td>0x800063C0</td><td>0x00012380</td></tr>
<tr><td>Coanda Gunship (Delivery)</td><td>0xE998E2A4</td><td>Yes</td><td>1932</td><td>0x80007D94</td><td>0x0000D1B7</td></tr>
<tr><td>Coanda Gunship (Driver)</td><td>0x112B50C6</td><td>Yes</td><td>1776</td><td>0x800075E2</td><td>0x00012C7A</td></tr>
<tr><td>Coanda Gunship (Ewan)</td><td>0x84E5AF7F</td><td>Yes</td><td>5979</td><td>0x8000B367</td><td>0x0000CAF4</td></tr>
<tr><td>Coanda Gunship (Full)</td><td>0xF86F549D</td><td>Yes</td><td>873</td><td>0x800063C5</td><td>0x00009278</td></tr>
<tr><td>Coanda Superiority</td><td>0xECD7D340</td><td>Yes</td><td>3645</td><td>0x80009479</td><td>0x00002457</td></tr>
<tr><td>Coanda Superiority (Driver)</td><td>0x001783DF</td><td>Yes</td><td>3653</td><td>0x80009514</td><td>0x00005BB8</td></tr>
<tr><td>Coanda Superiority (Ewan)</td><td>0x011C5856</td><td>Yes</td><td>5980</td><td>0x8000B368</td><td>0x00000764</td></tr>
<tr><td>Coanda Superiority (Full)</td><td>0xF86A3C54</td><td>Yes</td><td>3655</td><td>0x80009516</td><td>0x000096BB</td></tr>
<tr><td>Coanda Transport</td><td>0x4925098C</td><td>Yes</td><td>2220</td><td>0x800081F9</td><td>0x0001167C</td></tr>
<tr><td>Coanda Transport (Driver)</td><td>0x44CF1B8B</td><td>Yes</td><td>2221</td><td>0x800081FA</td><td>0x000020A2</td></tr>
<tr><td>Coanda Transport (Ewan)</td><td>0x8642C152</td><td>Yes</td><td>5981</td><td>0x8000B369</td><td>0x000101BE</td></tr>
<tr><td>Coanda Transport (Extraction)</td><td>0xE063D388</td><td>Yes</td><td>5046</td><td>0x8000A3E3</td><td>0x00013C51</td></tr>
<tr><td>Coanda Transport (Full)</td><td>0x4DF1FD48</td><td>Yes</td><td>2222</td><td>0x800081FB</td><td>0x00013300</td></tr>
<tr><td>Coanda Transport (Pursuit)</td><td>0x46F96893</td><td>Yes</td><td>4906</td><td>0x8000A27D</td><td>0x000005F3</td></tr>
<tr><td>Coilgun</td><td>0x25A6B2FE</td><td>No</td><td>2408</td><td>0x80008448</td><td>0xFFFFFFFF</td></tr>
<tr><td>Coilgun Bullet</td><td>0xAABA7EEE</td><td>No</td><td>2412</td><td>0x8000844C</td><td>0x000075DF</td></tr>
<tr><td>coinoperated</td><td>0x6C519C7A</td><td>No</td><td>120</td><td>0x80004C26</td><td>0x0000B288</td></tr>
<tr><td>Combat Rifle</td><td>0x5E3DE643</td><td>No</td><td>988</td><td>0x80006878</td><td>0x00003777</td></tr>
<tr><td>Combat Rifle (Window Spawner)</td><td>0xDC4B09CC</td><td>No</td><td>3000</td><td>0x80008A20</td><td>0xFFFFFFFF</td></tr>
<tr><td>Combat Rifle Bullet</td><td>0xFBD57875</td><td>No</td><td>987</td><td>0x80006877</td><td>0x0000FA81</td></tr>
<tr><td>commercial_raod5</td><td>0xD2216BAD</td><td>No</td><td>153</td><td>0x80004CE6</td><td>0xFFFFFFFF</td></tr>
<tr><td>commercial_raod5t</td><td>0x69F09A5B</td><td>No</td><td>73</td><td>0x80004A42</td><td>0xFFFFFFFF</td></tr>
<tr><td>commercial_road10cross.xsi</td><td>0xA2D106BF</td><td>No</td><td>154</td><td>0x80004CE7</td><td>0x0000412F</td></tr>
<tr><td>commercial_road10cross5.xsi</td><td>0x869EAA1C</td><td>No</td><td>75</td><td>0x80004A44</td><td>0x0000474C</td></tr>
<tr><td>commercial_road5</td><td>0xBE7BE56D</td><td>No</td><td>70</td><td>0x80004A3F</td><td>0x0000466E</td></tr>
<tr><td>commercial_road5cross</td><td>0x1A98F393</td><td>No</td><td>74</td><td>0x80004A43</td><td>0x00000C29</td></tr>
<tr><td>commercial_road5L</td><td>0xBB5C6FC3</td><td>No</td><td>71</td><td>0x80004A40</td><td>0x0000D204</td></tr>
<tr><td>commercial_road5t10</td><td>0x011624D8</td><td>No</td><td>72</td><td>0x80004A41</td><td>0x00012A90</td></tr>
<tr><td>Cougar</td><td>0x7690A482</td><td>No</td><td>4017</td><td>0x800099A7</td><td>0x0000D456</td></tr>
<tr><td>Cougar (Driver) (Civ Business B Male)</td><td>0x4D32D5FB</td><td>No</td><td>4592</td><td>0x80009F5A</td><td>0x000053D1</td></tr>
<tr><td>Cover</td><td>0xBABE579E</td><td>No</td><td>2983</td><td>0x80008A0C</td><td>0x00011B3E</td></tr>
<tr><td>Cover (Barrel)</td><td>0xBACBBC6F</td><td>No</td><td>5692</td><td>0x8000ACC5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cover (Barricade)</td><td>0xEAEC1AF8</td><td>No</td><td>5684</td><td>0x8000ACBB</td><td>0x0000D9CB</td></tr>
<tr><td>Cover (Box)</td><td>0xED03DE66</td><td>No</td><td>2987</td><td>0x80008A12</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cover (Building Custom)</td><td>0x35888DF4</td><td>No</td><td>5683</td><td>0x8000ACBA</td><td>0x00007B31</td></tr>
<tr><td>Cover (Building Poor)</td><td>0x8E85833F</td><td>No</td><td>5688</td><td>0x8000ACBF</td><td>0x000136C4</td></tr>
<tr><td>Cover (Building)</td><td>0x043CB553</td><td>No</td><td>5676</td><td>0x8000ACB3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cover (Car)</td><td>0x8689C3E5</td><td>No</td><td>5687</td><td>0x8000ACBE</td><td>0x0000F98D</td></tr>
<tr><td>Cover (Container)</td><td>0xE7FF5728</td><td>No</td><td>5686</td><td>0x8000ACBD</td><td>0x0000B516</td></tr>
<tr><td>Cover (Custom)</td><td>0x7C9DFFAC</td><td>No</td><td>5691</td><td>0x8000ACC4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cover (Fence)</td><td>0x562500A6</td><td>No</td><td>5674</td><td>0x8000ACB1</td><td>0x00001498</td></tr>
<tr><td>Cover (Junk)</td><td>0xB521C7B9</td><td>No</td><td>5685</td><td>0x8000ACBC</td><td>0x0000CC14</td></tr>
<tr><td>Cover (Placeable Popup)</td><td>0xD3A761B2</td><td>No</td><td>5677</td><td>0x8000ACB4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cover (Placeable Sidestep)</td><td>0x5639C55F</td><td>No</td><td>5678</td><td>0x8000ACB5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cover (Plant)</td><td>0xE3E474B2</td><td>No</td><td>5673</td><td>0x8000ACB0</td><td>0x00007CA3</td></tr>
<tr><td>Cover (Rock)</td><td>0x5FA0B806</td><td>No</td><td>5670</td><td>0x8000ACAD</td><td>0x0000CB88</td></tr>
<tr><td>Cover (Sandbag Corner)</td><td>0x60B2EB06</td><td>No</td><td>5679</td><td>0x8000ACB6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cover (Sandbag Custom)</td><td>0xF167ED60</td><td>No</td><td>5682</td><td>0x8000ACB9</td><td>0x000010C8</td></tr>
<tr><td>Cover (Sandbag End)</td><td>0x8AA9A276</td><td>No</td><td>5680</td><td>0x8000ACB7</td><td>0x0000EDFC</td></tr>
<tr><td>Cover (Sandbag Straight)</td><td>0x7E2C94A9</td><td>No</td><td>5681</td><td>0x8000ACB8</td><td>0x00012054</td></tr>
<tr><td>Cover (Sandbag)</td><td>0xE7BD3547</td><td>No</td><td>2985</td><td>0x80008A0F</td><td>0x0000976E</td></tr>
<tr><td>Cover (Statue)</td><td>0x65B98F8B</td><td>No</td><td>5689</td><td>0x8000ACC0</td><td>0x00003113</td></tr>
<tr><td>Cover (Tree Medium)</td><td>0x51AC7CF8</td><td>No</td><td>5671</td><td>0x8000ACAE</td><td>0x00013524</td></tr>
<tr><td>Cover (Tree Small)</td><td>0xA2657DB0</td><td>No</td><td>5672</td><td>0x8000ACAF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cover (Tree)</td><td>0x56073DB3</td><td>No</td><td>2984</td><td>0x80008A0D</td><td>0x00008D9F</td></tr>
<tr><td>Cover (Vehicle)</td><td>0x0A969F1B</td><td>No</td><td>5690</td><td>0x8000ACC2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cover (Wall)</td><td>0x3E05A4CF</td><td>No</td><td>5675</td><td>0x8000ACB2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Covert Pistol</td><td>0x175AB11B</td><td>No</td><td>1142</td><td>0x80006B65</td><td>0x00004C81</td></tr>
<tr><td>Covert Pistol Bullet</td><td>0x5A8F273D</td><td>No</td><td>1146</td><td>0x80006B69</td><td>0xFFFFFFFF</td></tr>
<tr><td>Covert SMG</td><td>0x3FDF8065</td><td>No</td><td>1144</td><td>0x80006B67</td><td>0x000115E6</td></tr>
<tr><td>Covert SMG Bullet</td><td>0xBFC5325F</td><td>No</td><td>1145</td><td>0x80006B68</td><td>0xFFFFFFFF</td></tr>
<tr><td>Cruise Missile Projectile</td><td>0x39F9955D</td><td>No</td><td>3165</td><td>0x80008E40</td><td>0x000022BF</td></tr>
<tr><td>CrushingDebrisLargeTemplate</td><td>0x1E1DD33E</td><td>No</td><td>2772</td><td>0x8000874A</td><td>0xFFFFFFFF</td></tr>
<tr><td>CrushingDebrisMedTemplate</td><td>0x099867E9</td><td>No</td><td>1045</td><td>0x8000691E</td><td>0x0000E0E1</td></tr>
<tr><td>CrushingDebrisSmallTemplate</td><td>0x6986DB9A</td><td>No</td><td>1044</td><td>0x8000691D</td><td>0x0000738D</td></tr>
<tr><td>CRX</td><td>0xB67908C6</td><td>No</td><td>60</td><td>0x8000473F</td><td>0x0000C6D6</td></tr>
<tr><td>CRX (Driver)</td><td>0x0B67B3DD</td><td>No</td><td>61</td><td>0x80004740</td><td>0x0000E0A5</td></tr>
<tr><td>CRX (Driver) (Civ Business B)</td><td>0x60531464</td><td>No</td><td>4279</td><td>0x80009CB2</td><td>0x00000E41</td></tr>
<tr><td>CRX (racing)</td><td>0x03F95C1D</td><td>No</td><td>2564</td><td>0x800085C4</td><td>0x0000630F</td></tr>
<tr><td>CRX (racing) (Driver)</td><td>0x5C5AD328</td><td>No</td><td>4464</td><td>0x80009E2A</td><td>0x00007020</td></tr>
<tr><td>CRX (racing) (Driver) (Civ Motorcycle male)</td><td>0x54BAD151</td><td>Yes</td><td>4641</td><td>0x80009FC3</td><td>0x00001723</td></tr>
<tr><td>CRX_Driver</td><td>0x1C5AD3BF</td><td>No</td><td>5053</td><td>0x8000A3F2</td><td>0x00010DCD</td></tr>
<tr><td>CRX_RUIN</td><td>0xF4982A1F</td><td>No</td><td>3466</td><td>0x800092C8</td><td>0x000104EE</td></tr>
<tr><td>CRXRacing_Driver</td><td>0x44256B69</td><td>No</td><td>5105</td><td>0x8000A42A</td><td>0x0000E132</td></tr>
<tr><td>Cutter (base)</td><td>0xD156A6EC</td><td>No</td><td>2184</td><td>0x800081D4</td><td>0x00009D75</td></tr>
<tr><td>Cutter (PR)</td><td>0x6DA31E8B</td><td>No</td><td>3329</td><td>0x80008FF4</td><td>0x0000D5A5</td></tr>
<tr><td>Cutter (PR) (Driver)</td><td>0xAEB97C26</td><td>No</td><td>3684</td><td>0x80009533</td><td>0x00003E36</td></tr>
<tr><td>Cutter (PR) (Full)</td><td>0xDCAB53FD</td><td>No</td><td>3685</td><td>0x80009534</td><td>0x0000C1DA</td></tr>
<tr><td>Cutter (PR)_Ruined</td><td>0x6303B0EF</td><td>No</td><td>4155</td><td>0x80009B52</td><td>0x00008CDC</td></tr>
<tr><td>Cutter_Driver</td><td>0x83BD7A69</td><td>No</td><td>5100</td><td>0x8000A425</td><td>0x00013FED</td></tr>
<tr><td>Daisy Cutter Projectile</td><td>0x251BF46B</td><td>No</td><td>3166</td><td>0x80008E41</td><td>0xFFFFFFFF</td></tr>
<tr><td>Dance Radio</td><td>0x52F25E7F</td><td>No</td><td>4912</td><td>0x8000A283</td><td>0x000090E5</td></tr>
<tr><td>Dance Radio AL</td><td>0xDE9309A6</td><td>No</td><td>4988</td><td>0x8000A3A3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Dance Radio AL Contact</td><td>0xA6F7A1CA</td><td>No</td><td>4995</td><td>0x8000A3AB</td><td>0x00002F9C</td></tr>
<tr><td>Dance Radio CH</td><td>0x5FA490B4</td><td>No</td><td>4987</td><td>0x8000A3A2</td><td>0x000030F2</td></tr>
<tr><td>Dance Radio CH Contact</td><td>0xE621A4E0</td><td>No</td><td>4996</td><td>0x8000A3AC</td><td>0x000037FA</td></tr>
<tr><td>Dance Radio Eva</td><td>0x9A6AAB11</td><td>No</td><td>4999</td><td>0x8000A3B0</td><td>0x0000C1FF</td></tr>
<tr><td>Dance Radio GR</td><td>0xAD7D835A</td><td>No</td><td>4985</td><td>0x8000A3A0</td><td>0x00012A27</td></tr>
<tr><td>Dance Radio GR Contact</td><td>0x5318FDFE</td><td>No</td><td>4997</td><td>0x8000A3AD</td><td>0x00007937</td></tr>
<tr><td>Dance Radio OC</td><td>0xA8C0D2DF</td><td>No</td><td>4986</td><td>0x8000A3A1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Dance Radio OC Contact</td><td>0xBFA48753</td><td>No</td><td>4998</td><td>0x8000A3AE</td><td>0x000086FE</td></tr>
<tr><td>Dance Radio PR Contact</td><td>0xB6E03723</td><td>No</td><td>4989</td><td>0x8000A3A4</td><td>0x00011D56</td></tr>
<tr><td>DangerousBuildingSimpleSpawners</td><td>0xBCD05D22</td><td>No</td><td>3086</td><td>0x80008BAA</td><td>0x0000D047</td></tr>
<tr><td>DangerousBuildingTest1</td><td>0x64FA3A44</td><td>No</td><td>556</td><td>0x80005BAA</td><td>0x0000E7E8</td></tr>
<tr><td>DangerousBuildingVZBarracks</td><td>0xDE512D7A</td><td>No</td><td>2197</td><td>0x800081E2</td><td>0x00008AA4</td></tr>
<tr><td>DangerousBuildingVZBarracks_HalfSpawn</td><td>0xB7E95A1F</td><td>No</td><td>5535</td><td>0x8000AB46</td><td>0x00004A10</td></tr>
<tr><td>DangerousBuildingVZBarracks_HalfSpawn_Squad</td><td>0x211E5D68</td><td>No</td><td>2203</td><td>0x800081E8</td><td>0x000101FE</td></tr>
<tr><td>DangerousBuildingVZBarrackstent_RPG</td><td>0x85B8A191</td><td>No</td><td>5913</td><td>0x8000B0C9</td><td>0x0000A2A7</td></tr>
<tr><td>DangerousBuildingVZBunker</td><td>0x21F8F2D4</td><td>No</td><td>2986</td><td>0x80008A11</td><td>0x00004D8F</td></tr>
<tr><td>DangerousBuildingVZTower</td><td>0x57C6E44E</td><td>No</td><td>2198</td><td>0x800081E3</td><td>0x0000821D</td></tr>
<tr><td>DB VZ RPG + Rifle</td><td>0xD3AA8AE5</td><td>No</td><td>2989</td><td>0x80008A15</td><td>0x00006C1D</td></tr>
<tr><td>DB_SquadTest</td><td>0xEA87BA74</td><td>No</td><td>3096</td><td>0x80008BB4</td><td>0x000001D7</td></tr>
<tr><td>debris m151 wheel</td><td>0x72227C3D</td><td>Yes</td><td>2781</td><td>0x80008753</td><td>0xFFFFFFFF</td></tr>
<tr><td>debris m35 wheel</td><td>0xC1E768D8</td><td>Yes</td><td>2782</td><td>0x80008754</td><td>0xFFFFFFFF</td></tr>
<tr><td>debris_barreldrum</td><td>0xF2B6EB83</td><td>No</td><td>3942</td><td>0x80009869</td><td>0x00006A94</td></tr>
<tr><td>debris_metal_chainlinkfence</td><td>0xA34CF23D</td><td>No</td><td>4311</td><td>0x80009CD2</td><td>0xFFFFFFFF</td></tr>
<tr><td>debris_metal_huge</td><td>0xE347179E</td><td>No</td><td>2802</td><td>0x80008768</td><td>0x00006988</td></tr>
<tr><td>debris_metal_lrg</td><td>0xB9ED0DA8</td><td>No</td><td>3945</td><td>0x8000986D</td><td>0xFFFFFFFF</td></tr>
<tr><td>debris_metal_med</td><td>0xD3413D47</td><td>No</td><td>3943</td><td>0x8000986A</td><td>0x00012BAE</td></tr>
<tr><td>debris_metal_pipes</td><td>0xE695DCDE</td><td>No</td><td>2805</td><td>0x8000876B</td><td>0x0000C110</td></tr>
<tr><td>debris_metal_sml</td><td>0x844B57BD</td><td>No</td><td>4310</td><td>0x80009CD1</td><td>0xFFFFFFFF</td></tr>
<tr><td>debris_metalpole_lrg</td><td>0x078F8C6A</td><td>No</td><td>4308</td><td>0x80009CCF</td><td>0x00002B0C</td></tr>
<tr><td>debris_oilrig 0x8000a6f6</td><td>0x360397F2</td><td>No</td><td>5252</td><td>0x8000A6F6</td><td>0x00012BCB</td></tr>
<tr><td>debris_rubber</td><td>0x66E977B5</td><td>No</td><td>5250</td><td>0x8000A6F4</td><td>0x00011AF4</td></tr>
<tr><td>debris_sheetmetal_lrg</td><td>0xFBCCE465</td><td>No</td><td>4309</td><td>0x80009CD0</td><td>0x0000311B</td></tr>
<tr><td>debris_sheetmetal_sml</td><td>0x03CA0258</td><td>No</td><td>3944</td><td>0x8000986C</td><td>0x00013948</td></tr>
<tr><td>debris_stone_huge</td><td>0x3EBBF6D4</td><td>No</td><td>4304</td><td>0x80009CCB</td><td>0xFFFFFFFF</td></tr>
<tr><td>debris_stone_lrg</td><td>0x944C7D36</td><td>No</td><td>3947</td><td>0x8000986F</td><td>0x0000E330</td></tr>
<tr><td>debris_stone_med</td><td>0xC471EE9D</td><td>No</td><td>4305</td><td>0x80009CCC</td><td>0x00012547</td></tr>
<tr><td>debris_stone_sml</td><td>0x88F18137</td><td>No</td><td>4306</td><td>0x80009CCD</td><td>0x0000C88D</td></tr>
<tr><td>debris_veh_civ_ruin</td><td>0xE53EA0D0</td><td>Yes</td><td>4312</td><td>0x80009CD4</td><td>0x000055EE</td></tr>
<tr><td>debris_wood_sml</td><td>0xF96233D1</td><td>No</td><td>3941</td><td>0x80009866</td><td>0x000104D0</td></tr>
<tr><td>DebrisDestructTemplate</td><td>0x6729C128</td><td>No</td><td>1467</td><td>0x80007012</td><td>0x0000F3C6</td></tr>
<tr><td>DebrisTemplate</td><td>0x31EB7EA2</td><td>No</td><td>390</td><td>0x80005569</td><td>0x0000AD26</td></tr>
<tr><td>decals</td><td>0x306169B7</td><td>No</td><td>425</td><td>0x800055C7</td><td>0x00002A99</td></tr>
<tr><td>DefaultTrafficZone</td><td>0xEDD263D1</td><td>No</td><td>548</td><td>0x80005B9E</td><td>0x00002341</td></tr>
<tr><td>Destroyer_Driver</td><td>0x154B2E39</td><td>Yes</td><td>5503</td><td>0x8000AABE</td><td>0x0000A1D4</td></tr>
<tr><td>Detach</td><td>0x6A75ED48</td><td>No</td><td>15</td><td>0x800038A6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Devastator</td><td>0x4739D812</td><td>No</td><td>5497</td><td>0x8000AAB6</td><td>0x00000DF3</td></tr>
<tr><td>Devastator_Driver</td><td>0xAAA9E373</td><td>No</td><td>5403</td><td>0x8000A994</td><td>0x0001237F</td></tr>
<tr><td>Dinghy</td><td>0x6A77E320</td><td>Yes</td><td>1773</td><td>0x800075DF</td><td>0x00005F25</td></tr>
<tr><td>Dinghy (Driver)</td><td>0x23051FBF</td><td>Yes</td><td>1775</td><td>0x800075E1</td><td>0x00010B42</td></tr>
<tr><td>Dinghy (Driver) (Civ Poor female)</td><td>0x7EA81174</td><td>Yes</td><td>4647</td><td>0x80009FC9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Dinghy (Driver) (Civ Poor male)</td><td>0x6B22C245</td><td>Yes</td><td>4646</td><td>0x80009FC8</td><td>0x00010B16</td></tr>
<tr><td>Dinghy_Driver</td><td>0x3AB2899D</td><td>Yes</td><td>5082</td><td>0x8000A411</td><td>0xFFFFFFFF</td></tr>
<tr><td>Disguise Scale (Armored)</td><td>0xC0FE9DE9</td><td>No</td><td>2974</td><td>0x80008A03</td><td>0x000111E3</td></tr>
<tr><td>Disguise Scale (Boat)</td><td>0x9219DBA9</td><td>Yes</td><td>2976</td><td>0x80008A05</td><td>0x00000B7A</td></tr>
<tr><td>Disguise Scale (Car)</td><td>0xBE1726D1</td><td>No</td><td>2977</td><td>0x80008A06</td><td>0x00010968</td></tr>
<tr><td>Disguise Scale (Default)</td><td>0xF091F576</td><td>No</td><td>2200</td><td>0x800081E5</td><td>0x0000AF1C</td></tr>
<tr><td>Disguise Scale (Helicopter)</td><td>0xD88C74B2</td><td>Yes</td><td>2975</td><td>0x80008A04</td><td>0x00012A09</td></tr>
<tr><td>Disguise Scale (Motorcycle)</td><td>0xCD6D84EE</td><td>Yes</td><td>2978</td><td>0x80008A07</td><td>0x00011746</td></tr>
<tr><td>Disguise Scale (Open Boat)</td><td>0x2A685D91</td><td>Yes</td><td>2201</td><td>0x800081E6</td><td>0x0000B3FB</td></tr>
<tr><td>Disguise Scale (Open Car)</td><td>0x4F1F14D9</td><td>No</td><td>2202</td><td>0x800081E7</td><td>0x00002A9F</td></tr>
<tr><td>DLC Green Goblin Bomb Projectile</td><td>0xF65BD4CB</td><td>No</td><td>5345</td><td>0x8000A94A</td><td>0x0000E738</td></tr>
<tr><td>DLC Green Goblin Bomblet Projectile</td><td>0xE05C94CE</td><td>No</td><td>5346</td><td>0x8000A94B</td><td>0x0000F5EE</td></tr>
<tr><td>DLC_50cal</td><td>0xFA6E3CA4</td><td>No</td><td>5494</td><td>0x8000AAB2</td><td>0x0000E39C</td></tr>
<tr><td>DLC_global_particle_3d</td><td>0x2AD585BB</td><td>No</td><td>5339</td><td>0x8000A940</td><td>0x000001C3</td></tr>
<tr><td>DLC_global_particle_explosion_huge</td><td>0x647D2F0B</td><td>No</td><td>5337</td><td>0x8000A93E</td><td>0x0000A4F0</td></tr>
<tr><td>DLC_Green_Goblin_Explosion</td><td>0x42446B02</td><td>No</td><td>5340</td><td>0x8000A942</td><td>0x0000C2C5</td></tr>
<tr><td>DLC_hero</td><td>0xEDB9F3A3</td><td>No</td><td>5703</td><td>0x8000ACD5</td><td>0xFFFFFFFF</td></tr>
<tr><td>DLC_Light_explosion_huge</td><td>0x862DC7E9</td><td>No</td><td>5338</td><td>0x8000A93F</td><td>0x0000AEBC</td></tr>
<tr><td>DLC_M1A1</td><td>0x28F72787</td><td>No</td><td>5495</td><td>0x8000AAB3</td><td>0x0000F269</td></tr>
<tr><td>DLC_npc_mercenaryelite</td><td>0x8128012A</td><td>No</td><td>5704</td><td>0x8000ACD6</td><td>0x000031E5</td></tr>
<tr><td>DO NOT USE  HondaCRX Test</td><td>0x30F53A4D</td><td>No</td><td>56</td><td>0x8000464D</td><td>0x00001694</td></tr>
<tr><td>DO NOT USE (OLD police cruiser)</td><td>0xE2415973</td><td>No</td><td>644</td><td>0x80005C4E</td><td>0x0000636E</td></tr>
<tr><td>DO NOT USE Weapon Test DSHK</td><td>0x8EC416AC</td><td>No</td><td>1416</td><td>0x80006F6F</td><td>0xFFFFFFFF</td></tr>
<tr><td>DO NOT USE Weapon Test M2</td><td>0xB0AC94E5</td><td>No</td><td>1414</td><td>0x80006F6D</td><td>0xFFFFFFFF</td></tr>
<tr><td>DO NOT USE Weapon Test M60</td><td>0x3349F36B</td><td>No</td><td>1417</td><td>0x80006F70</td><td>0xFFFFFFFF</td></tr>
<tr><td>DO NOT USE Weapon Test MK19</td><td>0xC1D0275E</td><td>No</td><td>1415</td><td>0x80006F6E</td><td>0x00013E07</td></tr>
<tr><td>DO NOT USE Weapon Test TOW</td><td>0xCEEDCE4E</td><td>No</td><td>1223</td><td>0x80006CD4</td><td>0xFFFFFFFF</td></tr>
<tr><td>DONOTUSE_oc_veh_semi_fueltrailer</td><td>0xB38BF710</td><td>Yes</td><td>946</td><td>0x800065DE</td><td>0xFFFFFFFF</td></tr>
<tr><td>DropPoint (AL)</td><td>0x9FC35DA0</td><td>No</td><td>5540</td><td>0x8000AB4D</td><td>0xFFFFFFFF</td></tr>
<tr><td>DropPoint (CH)</td><td>0x0388C38E</td><td>No</td><td>5539</td><td>0x8000AB4C</td><td>0x00006F78</td></tr>
<tr><td>DropPoint (GR)</td><td>0x973E1418</td><td>No</td><td>5538</td><td>0x8000AB4A</td><td>0x00001371</td></tr>
<tr><td>DropPoint (OC)</td><td>0xEBD90A17</td><td>No</td><td>5541</td><td>0x8000AB4E</td><td>0x000118F1</td></tr>
<tr><td>DropPoint (PR)</td><td>0x32804CB7</td><td>No</td><td>5542</td><td>0x8000AB4F</td><td>0x00007E89</td></tr>
<tr><td>DropPoint (VZ)</td><td>0x839D3BC9</td><td>No</td><td>5537</td><td>0x8000AB48</td><td>0x0000F0BB</td></tr>
<tr><td>DSV Scout Vehicle</td><td>0x39870E26</td><td>No</td><td>847</td><td>0x8000639E</td><td>0x00004D1C</td></tr>
<tr><td>Dumb Rocket</td><td>0xE1B587D7</td><td>No</td><td>992</td><td>0x8000687E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Dumb Rocket (CH)</td><td>0x69C5003F</td><td>No</td><td>5507</td><td>0x8000AAC2</td><td>0xFFFFFFFF</td></tr>
<tr><td>E3 Missile Stage 1</td><td>0xEC4DB016</td><td>No</td><td>890</td><td>0x800063E0</td><td>0x0000B3D8</td></tr>
<tr><td>E3 Missile Stage 2</td><td>0x6E553881</td><td>No</td><td>891</td><td>0x800063E1</td><td>0x00010F04</td></tr>
<tr><td>E3_OC_Littlebirds</td><td>0xB5A69C43</td><td>No</td><td>1023</td><td>0x800068A9</td><td>0x000024EB</td></tr>
<tr><td>e3demo</td><td>0xDF1B9620</td><td>No</td><td>394</td><td>0x8000556F</td><td>0x0000C992</td></tr>
<tr><td>E3MeridaMedTraffic</td><td>0xDF329FB0</td><td>No</td><td>1027</td><td>0x800068B1</td><td>0x0000DC93</td></tr>
<tr><td>Effect_Impact</td><td>0x60D1B0BB</td><td>No</td><td>523</td><td>0x800057B8</td><td>0xFFFFFFFF</td></tr>
<tr><td>Effect_ParticleSmoke</td><td>0x3882A7CA</td><td>No</td><td>19</td><td>0x800038E7</td><td>0x0000F459</td></tr>
<tr><td>Effects</td><td>0xC8EA585D</td><td>No</td><td>1090</td><td>0x80006A72</td><td>0xFFFFFFFF</td></tr>
<tr><td>El Grande</td><td>0x53BAB15D</td><td>No</td><td>356</td><td>0x80004F3F</td><td>0x000093CC</td></tr>
<tr><td>El Grande (Driver)</td><td>0x9C3D99E8</td><td>No</td><td>66</td><td>0x80004745</td><td>0x0000D4F9</td></tr>
<tr><td>El Grande (Driver) (Civ Poor female)</td><td>0x126CFB2F</td><td>No</td><td>4283</td><td>0x80009CB6</td><td>0x000114EF</td></tr>
<tr><td>El Grande (Driver) (Civ Poor male)</td><td>0x98861C8E</td><td>No</td><td>4282</td><td>0x80009CB5</td><td>0x00009880</td></tr>
<tr><td>El Grande_Driver</td><td>0xCF505E8E</td><td>No</td><td>5056</td><td>0x8000A3F5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Emplaced GL</td><td>0x415B91A9</td><td>No</td><td>1357</td><td>0x80006EC8</td><td>0x0000F480</td></tr>
<tr><td>Emplaced GL (Driver)</td><td>0xA52F3DC4</td><td>No</td><td>4210</td><td>0x80009C68</td><td>0x00008956</td></tr>
<tr><td>Emplaced GL (NO Physics)</td><td>0x6B439A94</td><td>No</td><td>3346</td><td>0x80009006</td><td>0x00011218</td></tr>
<tr><td>Emplaced GL (NO Physics) (Driver)</td><td>0x1DD8B573</td><td>No</td><td>4209</td><td>0x80009C67</td><td>0x00002D26</td></tr>
<tr><td>Emplaced M101A1 (Base)</td><td>0xB3953317</td><td>No</td><td>3365</td><td>0x8000901F</td><td>0x0000E597</td></tr>
<tr><td>Emplaced M101A1 (GR)</td><td>0x3606AE5B</td><td>No</td><td>3366</td><td>0x80009020</td><td>0x0000BE73</td></tr>
<tr><td>Emplaced M101A1 (GR) (Driver)</td><td>0xFF912536</td><td>No</td><td>5640</td><td>0x8000AC8B</td><td>0x0000C0BD</td></tr>
<tr><td>Emplaced M101A1 (VZ)</td><td>0xD83A395A</td><td>No</td><td>2279</td><td>0x80008243</td><td>0x00001B84</td></tr>
<tr><td>Emplaced M101A1 (VZ) (Driver)</td><td>0x8D7E0F01</td><td>No</td><td>2530</td><td>0x8000855C</td><td>0x0000C9F7</td></tr>
<tr><td>Emplaced MG</td><td>0x0737A57C</td><td>No</td><td>1134</td><td>0x80006B5C</td><td>0x000000F0</td></tr>
<tr><td>Emplaced MG (AL)</td><td>0x87C1F1F4</td><td>No</td><td>4050</td><td>0x80009ADA</td><td>0x00000CEC</td></tr>
<tr><td>Emplaced MG (AL) (Gunner)</td><td>0x03DB8EE6</td><td>No</td><td>4560</td><td>0x80009F2C</td><td>0x0000F9E2</td></tr>
<tr><td>Emplaced MG (CH)</td><td>0xAC58DB2A</td><td>No</td><td>4559</td><td>0x80009F2B</td><td>0x0000DA87</td></tr>
<tr><td>Emplaced MG (Guerilla)</td><td>0x79156930</td><td>No</td><td>4387</td><td>0x80009D5B</td><td>0x0000C584</td></tr>
<tr><td>Emplaced MG (NO Physics)</td><td>0x24A780DF</td><td>No</td><td>3345</td><td>0x80009005</td><td>0x00002FBC</td></tr>
<tr><td>Emplaced MG (OC)</td><td>0x42C1E09B</td><td>No</td><td>4389</td><td>0x80009D5D</td><td>0x0000948F</td></tr>
<tr><td>Emplaced MG (PR)</td><td>0xB5D0D153</td><td>No</td><td>4390</td><td>0x80009D5E</td><td>0x00000672</td></tr>
<tr><td>Emplaced MG (VZ)</td><td>0xDE9A32BD</td><td>No</td><td>2528</td><td>0x8000855A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Emplaced MG DB</td><td>0x42A42946</td><td>No</td><td>1907</td><td>0x8000780D</td><td>0x00003E31</td></tr>
<tr><td>Emplaced MG3 (Allied)</td><td>0x062E7C3B</td><td>No</td><td>4368</td><td>0x80009D3F</td><td>0x00011599</td></tr>
<tr><td>Emplaced MG3 (OC)</td><td>0x15C178B6</td><td>No</td><td>2397</td><td>0x800083E9</td><td>0x0000D196</td></tr>
<tr><td>Emplaced Quad50 (Driver)</td><td>0x948AAE91</td><td>No</td><td>2529</td><td>0x8000855B</td><td>0x0000C887</td></tr>
<tr><td>Emplaced Quad50 (GR)</td><td>0x01CC3F6E</td><td>No</td><td>2871</td><td>0x80008918</td><td>0x00004E62</td></tr>
<tr><td>Emplaced Recoiless Rifle</td><td>0xCFC5EA73</td><td>No</td><td>2411</td><td>0x8000844B</td><td>0x00009B8D</td></tr>
<tr><td>Emplaced Recoiless Rifle (Allied)</td><td>0xB32356DF</td><td>No</td><td>4561</td><td>0x80009F2D</td><td>0x0000F701</td></tr>
<tr><td>Emplaced Recoiless Rifle (China)</td><td>0xF3ECF579</td><td>No</td><td>2398</td><td>0x800083EA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Emplaced Recoiless Rifle (GR)</td><td>0xC9C40571</td><td>No</td><td>4388</td><td>0x80009D5C</td><td>0x00002C47</td></tr>
<tr><td>Emplaced Recoiless Rifle (OC)</td><td>0x73341312</td><td>No</td><td>2396</td><td>0x800083E8</td><td>0x000089D2</td></tr>
<tr><td>Emplaced Recoiless Rifle (VZ)</td><td>0xED0D7950</td><td>No</td><td>2394</td><td>0x800083E6</td><td>0x0001244E</td></tr>
<tr><td>Emplaced TOW</td><td>0x9E1AF7CE</td><td>No</td><td>1206</td><td>0x80006CBE</td><td>0x00011B3B</td></tr>
<tr><td>Emplaced TOW (Allied)</td><td>0x03AB6E40</td><td>No</td><td>2402</td><td>0x800083F0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Emplaced Tripod Weapon</td><td>0x154AC16C</td><td>No</td><td>1133</td><td>0x80006B5B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Emplaced Weapon</td><td>0xB00CE408</td><td>No</td><td>4730</td><td>0x8000A024</td><td>0x0000AE9A</td></tr>
<tr><td>Emplaced ZU23</td><td>0x8A48F46A</td><td>No</td><td>2546</td><td>0x800085AC</td><td>0x0000B642</td></tr>
<tr><td>Emplaced ZU23 (Driver)</td><td>0xF239B751</td><td>No</td><td>3065</td><td>0x80008B92</td><td>0x0000D975</td></tr>
<tr><td>Emplaced ZU23 (Driver) (Seatbelted)</td><td>0x26B2F447</td><td>No</td><td>5967</td><td>0x8000B2FB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Endriago (Attack)</td><td>0x8C18A0BB</td><td>No</td><td>2172</td><td>0x800081C6</td><td>0x000113A7</td></tr>
<tr><td>Endriago (Attack) (Driver)</td><td>0xCF9CDE96</td><td>No</td><td>2188</td><td>0x800081D8</td><td>0x0000F6EB</td></tr>
<tr><td>Endriago (Attack) (Ewan)</td><td>0x373FE88F</td><td>No</td><td>5987</td><td>0x8000B36F</td><td>0x0000E5DC</td></tr>
<tr><td>Endriago (Attack) (Full)</td><td>0xAA2BBCED</td><td>No</td><td>3836</td><td>0x800097F4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Endriago (Elite)</td><td>0xF7847648</td><td>No</td><td>2177</td><td>0x800081CC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Endriago (Elite) (Driver)</td><td>0xBBD6B527</td><td>No</td><td>2189</td><td>0x800081D9</td><td>0x00007313</td></tr>
<tr><td>Endriago (Elite) (Ewan)</td><td>0x52C22EBE</td><td>No</td><td>5988</td><td>0x8000B370</td><td>0x0000D28A</td></tr>
<tr><td>Endriago (Superiority)</td><td>0x81AF7BF6</td><td>No</td><td>2175</td><td>0x800081CA</td><td>0x00011135</td></tr>
<tr><td>Endriago (Superiority) (Driver)</td><td>0xBAB8C94D</td><td>No</td><td>2190</td><td>0x800081DA</td><td>0x00002524</td></tr>
<tr><td>Endriago (Superiority) (Ewan)</td><td>0x7856D228</td><td>No</td><td>5989</td><td>0x8000B371</td><td>0x0000A60C</td></tr>
<tr><td>entrance</td><td>0x7F436ABB</td><td>No</td><td>8</td><td>0x8000234B</td><td>0x000096D7</td></tr>
<tr><td>Equipment</td><td>0xDAB653E7</td><td>No</td><td>20</td><td>0x8000436C</td><td>0x0000F705</td></tr>
<tr><td>Equipment (Pistol)</td><td>0x0EF3F28B</td><td>No</td><td>1132</td><td>0x80006B5A</td><td>0x00007CAA</td></tr>
<tr><td>escort</td><td>0x3392134D</td><td>No</td><td>1681</td><td>0x800074B3</td><td>0x0000E67A</td></tr>
<tr><td>Escort (Driver)</td><td>0xA22C2ED8</td><td>No</td><td>1682</td><td>0x800074BC</td><td>0x000068FC</td></tr>
<tr><td>Escort (Driver) (Civ Taxi Driver male)</td><td>0xCCC0ED14</td><td>No</td><td>4284</td><td>0x80009CB7</td><td>0x00012613</td></tr>
<tr><td>Escort_Driver</td><td>0x74AF4DDE</td><td>No</td><td>5057</td><td>0x8000A3F6</td><td>0xFFFFFFFF</td></tr>
<tr><td>ESV</td><td>0xE715B0A5</td><td>No</td><td>886</td><td>0x800063DB</td><td>0x0000E53A</td></tr>
<tr><td>ESV (Driver)</td><td>0xBFCEB0B0</td><td>No</td><td>1806</td><td>0x8000769D</td><td>0x0000406A</td></tr>
<tr><td>ESV (Executive Passengers)</td><td>0x231C723D</td><td>No</td><td>1808</td><td>0x8000769F</td><td>0x00000B47</td></tr>
<tr><td>ESV (Full)</td><td>0x53857247</td><td>No</td><td>1807</td><td>0x8000769E</td><td>0x00007178</td></tr>
<tr><td>Esv (lowrider)</td><td>0x45A8D20C</td><td>No</td><td>4015</td><td>0x800099A5</td><td>0x0000AFC7</td></tr>
<tr><td>ESV (Lowrider) (Civ Business (male)</td><td>0x05179C74</td><td>No</td><td>5146</td><td>0x8000A484</td><td>0x0000B42C</td></tr>
<tr><td>ESV/EXT</td><td>0x17088F3D</td><td>No</td><td>874</td><td>0x800063CA</td><td>0x0000D173</td></tr>
<tr><td>ESV_Driver</td><td>0xB9EDD606</td><td>No</td><td>5110</td><td>0x8000A451</td><td>0xFFFFFFFF</td></tr>
<tr><td>ESVLowrider_Driver</td><td>0xE53146F0</td><td>No</td><td>5104</td><td>0x8000A429</td><td>0x00002A3E</td></tr>
<tr><td>Eva</td><td>0x46D28FA9</td><td>No</td><td>504</td><td>0x800056D9</td><td>0x0001143D</td></tr>
<tr><td>Explosion</td><td>0x16930AFE</td><td>No</td><td>3</td><td>0x8000232F</td><td>0x0000465E</td></tr>
<tr><td>Explosion ( Surgical Strike Small)</td><td>0xE3C9E9B8</td><td>No</td><td>5381</td><td>0x8000A975</td><td>0x00012C06</td></tr>
<tr><td>Explosion (25mm Autocannon Shell)</td><td>0x7028DCFA</td><td>No</td><td>2864</td><td>0x80008911</td><td>0x0000171D</td></tr>
<tr><td>Explosion (AA Detonation)</td><td>0x9A4F1130</td><td>No</td><td>2430</td><td>0x80008462</td><td>0x00006B5A</td></tr>
<tr><td>Explosion (Action Hijack Grenade)</td><td>0xD1F8D673</td><td>No</td><td>1824</td><td>0x800076AF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (Airstike Bomb Final Strike)</td><td>0xCD8E9443</td><td>No</td><td>5820</td><td>0x8000AF7D</td><td>0x0000B7C2</td></tr>
<tr><td>Explosion (Airstike Bomb)</td><td>0x76647795</td><td>No</td><td>3164</td><td>0x80008E3F</td><td>0x000063F0</td></tr>
<tr><td>Explosion (Airstrike Frag)</td><td>0xB598F2B1</td><td>No</td><td>5042</td><td>0x8000A3DF</td><td>0x000028CF</td></tr>
<tr><td>Explosion (AT Mine)</td><td>0xAD41C2AF</td><td>No</td><td>1151</td><td>0x80006B6F</td><td>0x0000D6EA</td></tr>
<tr><td>Explosion (AT Missile)</td><td>0xBC2A728E</td><td>No</td><td>5786</td><td>0x8000AEF2</td><td>0x0000492D</td></tr>
<tr><td>Explosion (Bombing Run)</td><td>0xD2B69D9A</td><td>No</td><td>3169</td><td>0x80008E44</td><td>0x000077BA</td></tr>
<tr><td>Explosion (Bunker Buster Stage 1)</td><td>0xDDFC11F4</td><td>No</td><td>2427</td><td>0x8000845F</td><td>0x00004515</td></tr>
<tr><td>Explosion (Bunker Buster Stage 2)</td><td>0xAD85F5DD</td><td>No</td><td>2426</td><td>0x8000845E</td><td>0x00011530</td></tr>
<tr><td>Explosion (C4 Primary)</td><td>0x150F6CE6</td><td>No</td><td>993</td><td>0x8000687F</td><td>0x000097A8</td></tr>
<tr><td>Explosion (C4 Secondary)</td><td>0xF4A69A1E</td><td>No</td><td>4901</td><td>0x8000A275</td><td>0x00009A65</td></tr>
<tr><td>Explosion (Carpet bomb)</td><td>0x7CBBB47A</td><td>No</td><td>382</td><td>0x8000522B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (Cluster Bomb)</td><td>0x25273161</td><td>No</td><td>5281</td><td>0x8000A8AD</td><td>0x00008AD6</td></tr>
<tr><td>Explosion (Cluster Bomblet)</td><td>0x8BE95DA4</td><td>No</td><td>2423</td><td>0x8000845B</td><td>0x0000537E</td></tr>
<tr><td>Explosion (Cruise Missile)</td><td>0x4B08A278</td><td>No</td><td>3159</td><td>0x80008E3A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (Daisy Cutter)</td><td>0x34DEC7A2</td><td>No</td><td>3160</td><td>0x80008E3B</td><td>0x000073C6</td></tr>
<tr><td>Explosion (E3 Missile Strike)</td><td>0x6B6C4D1D</td><td>No</td><td>892</td><td>0x800063E2</td><td>0x00010CF4</td></tr>
<tr><td>Explosion (Force)</td><td>0xC0F7BAA4</td><td>No</td><td>5047</td><td>0x8000A3E5</td><td>0x0000AA7E</td></tr>
<tr><td>Explosion (Fuel Air Bomb)</td><td>0x834C9BF3</td><td>No</td><td>3157</td><td>0x80008E37</td><td>0x00011493</td></tr>
<tr><td>Explosion (Fuel Air Rocket Stage II)</td><td>0xC64F9AC3</td><td>No</td><td>5814</td><td>0x8000AF77</td><td>0x000134CD</td></tr>
<tr><td>Explosion (Fuel Air Rocket)</td><td>0x1500DD83</td><td>No</td><td>5792</td><td>0x8000AEF8</td><td>0x0000AFCC</td></tr>
<tr><td>Explosion (Grenade Frag)</td><td>0xF5D8EE81</td><td>No</td><td>4895</td><td>0x8000A26F</td><td>0x00004FD7</td></tr>
<tr><td>Explosion (Grenade MG)</td><td>0xE443510D</td><td>No</td><td>4079</td><td>0x80009AF9</td><td>0x00008162</td></tr>
<tr><td>Explosion (Grenade)</td><td>0x6A8141F5</td><td>No</td><td>453</td><td>0x8000568D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (Gunship Shell)</td><td>0xBF766119</td><td>Yes</td><td>5829</td><td>0x8000AF88</td><td>0x0000B2AE</td></tr>
<tr><td>Explosion (Hand Grenade Frag)</td><td>0x486B6D16</td><td>No</td><td>5209</td><td>0x8000A5F1</td><td>0x0000129E</td></tr>
<tr><td>Explosion (Hand Grenade)</td><td>0xB6393F34</td><td>No</td><td>5208</td><td>0x8000A5F0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (Handheld PEP)</td><td>0x671C7430</td><td>No</td><td>5765</td><td>0x8000AED2</td><td>0x0001364C</td></tr>
<tr><td>Explosion (Handheld RPG Frag)</td><td>0x03EAE0C8</td><td>No</td><td>5211</td><td>0x8000A5F3</td><td>0x0000B812</td></tr>
<tr><td>Explosion (Handheld RPG)</td><td>0xEB4ECA16</td><td>No</td><td>5210</td><td>0x8000A5F2</td><td>0x00009E61</td></tr>
<tr><td>Explosion (MOAB)</td><td>0xD511013C</td><td>No</td><td>3161</td><td>0x80008E3C</td><td>0x0000C064</td></tr>
<tr><td>Explosion (Munitions Laptop)</td><td>0xE7DBFE85</td><td>No</td><td>5797</td><td>0x8000AEFE</td><td>0x00002FDC</td></tr>
<tr><td>Explosion (Munitions)</td><td>0x599F00F1</td><td>No</td><td>5795</td><td>0x8000AEFC</td><td>0x00003B28</td></tr>
<tr><td>Explosion (Nil)</td><td>0xA3FB3C40</td><td>No</td><td>5832</td><td>0x8000AF8D</td><td>0x000030FF</td></tr>
<tr><td>Explosion (Practice Bomb)</td><td>0xEEC245A4</td><td>No</td><td>5838</td><td>0x8000AF93</td><td>0x0000A8ED</td></tr>
<tr><td>Explosion (Rocket Artillery)</td><td>0x985804BD</td><td>No</td><td>3162</td><td>0x80008E3D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (RPG Frag)</td><td>0x400A470A</td><td>No</td><td>4905</td><td>0x8000A27B</td><td>0x00009768</td></tr>
<tr><td>Explosion (RPG)</td><td>0xFD0F7310</td><td>No</td><td>452</td><td>0x8000568C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (Small Airstike Bomb)</td><td>0x66BA5A4E</td><td>No</td><td>5821</td><td>0x8000AF7E</td><td>0x00001F93</td></tr>
<tr><td>Explosion (Small)</td><td>0x4D62A088</td><td>No</td><td>512</td><td>0x800056E1</td><td>0x00007DA7</td></tr>
<tr><td>Explosion (Smart Bomb)</td><td>0x36BE81FC</td><td>No</td><td>3163</td><td>0x80008E3E</td><td>0x00000A0A</td></tr>
<tr><td>Explosion (Strategic Missile)</td><td>0x6D290F19</td><td>No</td><td>3158</td><td>0x80008E39</td><td>0x00012375</td></tr>
<tr><td>Explosion (Surgical Strike Invisible)</td><td>0xEDB48E74</td><td>No</td><td>1923</td><td>0x80007CD1</td><td>0x0000FB77</td></tr>
<tr><td>Explosion (Surgical Strike)</td><td>0x3219AC3B</td><td>No</td><td>1833</td><td>0x800076CD</td><td>0x00001699</td></tr>
<tr><td>Explosion (Tank Artillery)</td><td>0x35EC2FDD</td><td>Yes</td><td>4136</td><td>0x80009B34</td><td>0x0000A2A1</td></tr>
<tr><td>Explosion (Tank Shell)</td><td>0x0AB943B9</td><td>Yes</td><td>3179</td><td>0x80008E5B</td><td>0x0000EAFA</td></tr>
<tr><td>Explosion (TEST)</td><td>0x1DFA117F</td><td>No</td><td>4078</td><td>0x80009AF8</td><td>0x00004CF9</td></tr>
<tr><td>Explosion (Tiny)</td><td>0xCFC135B5</td><td>No</td><td>510</td><td>0x800056DF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (Very Small)</td><td>0xE1F3EBA4</td><td>No</td><td>511</td><td>0x800056E0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (Very Tiny)</td><td>0xCCE4F221</td><td>No</td><td>2407</td><td>0x800083F5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion (Water Mine)</td><td>0xF5E7C0D5</td><td>No</td><td>4900</td><td>0x8000A274</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion AllCon002 Pipes</td><td>0x93805F82</td><td>No</td><td>2675</td><td>0x8000867D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Explosion_Artillery</td><td>0x7B661479</td><td>No</td><td>2420</td><td>0x80008456</td><td>0x00005B4A</td></tr>
<tr><td>Explosion_Large</td><td>0x56B83982</td><td>No</td><td>1099</td><td>0x80006A7B</td><td>0x0000AA1F</td></tr>
<tr><td>Explosion_Large_OilTruck</td><td>0x23B6A048</td><td>Yes</td><td>1153</td><td>0x80006BA4</td><td>0xFFFFFFFF</td></tr>
<tr><td>explosion_rpg</td><td>0x5CDE5C1E</td><td>No</td><td>502</td><td>0x800056D6</td><td>0x00009A26</td></tr>
<tr><td>Explosion_Test</td><td>0xB6F610E5</td><td>No</td><td>2006</td><td>0x8000803A</td><td>0x00011FD5</td></tr>
<tr><td>ExplosionGrit</td><td>0xF565D29E</td><td>No</td><td>415</td><td>0x80005592</td><td>0x00008A9E</td></tr>
<tr><td>EXT</td><td>0x26308AFA</td><td>No</td><td>883</td><td>0x800063D8</td><td>0x0000E91F</td></tr>
<tr><td>EXT (Driver)</td><td>0x5BFB8AA1</td><td>No</td><td>1805</td><td>0x8000769C</td><td>0x0001129F</td></tr>
<tr><td>EXT (DriverGunner)</td><td>0xB1FC1FF2</td><td>No</td><td>3609</td><td>0x80009455</td><td>0xFFFFFFFF</td></tr>
<tr><td>EXT (Full)</td><td>0x44CD8436</td><td>No</td><td>884</td><td>0x800063D9</td><td>0x0000AAEE</td></tr>
<tr><td>EXT (GL)</td><td>0xB60CD310</td><td>No</td><td>3610</td><td>0x80009456</td><td>0x000037CC</td></tr>
<tr><td>EXT (GL) (Driver)</td><td>0xBD9DF52F</td><td>No</td><td>3611</td><td>0x80009457</td><td>0x00002DA4</td></tr>
<tr><td>EXT (GL) (DriverGunner)</td><td>0xCC757908</td><td>No</td><td>3612</td><td>0x80009458</td><td>0x000099B2</td></tr>
<tr><td>EXT (GL) (Full)</td><td>0xC43D9164</td><td>No</td><td>3613</td><td>0x80009459</td><td>0x0000A68B</td></tr>
<tr><td>EXT (monster)</td><td>0xB6D6F9F1</td><td>No</td><td>4016</td><td>0x800099A6</td><td>0xFFFFFFFF</td></tr>
<tr><td>EXT (TOW)</td><td>0xE49A8C75</td><td>No</td><td>1089</td><td>0x80006A37</td><td>0x0000B039</td></tr>
<tr><td>EXT (TOW) (Driver)</td><td>0x6D3F3C80</td><td>No</td><td>3616</td><td>0x8000945C</td><td>0x0000C8D3</td></tr>
<tr><td>EXT (TOW) (DriverGunner)</td><td>0x8C4F663F</td><td>No</td><td>3615</td><td>0x8000945B</td><td>0x000074BE</td></tr>
<tr><td>EXT (TOW) (Full)</td><td>0xD2C8CD97</td><td>No</td><td>3614</td><td>0x8000945A</td><td>0x00007758</td></tr>
<tr><td>EXT (Unarmed)</td><td>0x78C50A1D</td><td>No</td><td>1078</td><td>0x80006A13</td><td>0xFFFFFFFF</td></tr>
<tr><td>EXT (Unarmed) (Driver)</td><td>0xEC30FD28</td><td>No</td><td>5655</td><td>0x8000AC9D</td><td>0xFFFFFFFF</td></tr>
<tr><td>EXT_Driver</td><td>0x44C70BAB</td><td>No</td><td>5058</td><td>0x8000A3F7</td><td>0x00003614</td></tr>
<tr><td>EXTMonster_Driver</td><td>0x952B1D5D</td><td>No</td><td>5137</td><td>0x8000A478</td><td>0x00005C62</td></tr>
<tr><td>F35b</td><td>0x1AD49939</td><td>Yes</td><td>1199</td><td>0x80006CAF</td><td>0x00000B74</td></tr>
<tr><td>F35b (GR driver)</td><td>0x4F6B3B65</td><td>Yes</td><td>1140</td><td>0x80006B63</td><td>0x000010CF</td></tr>
<tr><td>FA Missile</td><td>0x06BFC2BE</td><td>No</td><td>5816</td><td>0x8000AF79</td><td>0xFFFFFFFF</td></tr>
<tr><td>FA RPG Rocket</td><td>0xE8279B7D</td><td>No</td><td>1365</td><td>0x80006ED1</td><td>0x00002EA0</td></tr>
<tr><td>Faction (Allied)</td><td>0x4933886F</td><td>No</td><td>485</td><td>0x800056C0</td><td>0x00004C60</td></tr>
<tr><td>Faction (China)</td><td>0x3F8DCE69</td><td>No</td><td>492</td><td>0x800056C7</td><td>0x000097F4</td></tr>
<tr><td>Faction (Civ)</td><td>0x898188A8</td><td>No</td><td>496</td><td>0x800056CB</td><td>0x00013339</td></tr>
<tr><td>Faction (Guerilla)</td><td>0x9D95C52D</td><td>No</td><td>493</td><td>0x800056C8</td><td>0x0000DE0A</td></tr>
<tr><td>Faction (OC)</td><td>0x9FE42462</td><td>No</td><td>494</td><td>0x800056C9</td><td>0x0000D1FF</td></tr>
<tr><td>Faction (Pirate)</td><td>0x4C0CB2F9</td><td>No</td><td>495</td><td>0x800056CA</td><td>0x000114BC</td></tr>
<tr><td>Faction (PMC)</td><td>0xA55FA50A</td><td>No</td><td>488</td><td>0x800056C3</td><td>0x00000FC7</td></tr>
<tr><td>Faction (Police)</td><td>0x95F6F9CE</td><td>No</td><td>486</td><td>0x800056C1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Faction (VZ)</td><td>0x8E772860</td><td>No</td><td>484</td><td>0x800056BF</td><td>0x0000EFB4</td></tr>
<tr><td>Faction Building (Allied)</td><td>0xEC7B01D9</td><td>No</td><td>2992</td><td>0x80008A18</td><td>0x00012DB9</td></tr>
<tr><td>Faction Building (China)</td><td>0xF678EBC7</td><td>No</td><td>2993</td><td>0x80008A19</td><td>0x00006924</td></tr>
<tr><td>Faction Building (Guerilla)</td><td>0xFD2D649F</td><td>No</td><td>2994</td><td>0x80008A1A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Faction Building (OC)</td><td>0x2804AA7C</td><td>No</td><td>2995</td><td>0x80008A1B</td><td>0x00012348</td></tr>
<tr><td>Faction Building (Pirate)</td><td>0xA452EC97</td><td>No</td><td>2996</td><td>0x80008A1C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Faction Building (VZ)</td><td>0xBDEDDE5A</td><td>No</td><td>2997</td><td>0x80008A1D</td><td>0x00007107</td></tr>
<tr><td>Fake Physics Prop</td><td>0x8E1BFDB8</td><td>No</td><td>3741</td><td>0x8000961B</td><td>0x0000DD86</td></tr>
<tr><td>Fake Physics Prop Destructible</td><td>0x11DCF132</td><td>No</td><td>3740</td><td>0x8000961A</td><td>0x0000BDAD</td></tr>
<tr><td>Fern01</td><td>0xA15E4C37</td><td>No</td><td>941</td><td>0x800064DB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fiona</td><td>0xC6D8FB46</td><td>No</td><td>1779</td><td>0x800075E5</td><td>0x0000229A</td></tr>
<tr><td>Fiona Taylor</td><td>0x723E34F7</td><td>No</td><td>3832</td><td>0x800097ED</td><td>0x0000BE5A</td></tr>
<tr><td>Fire</td><td>0x8A552089</td><td>No</td><td>392</td><td>0x8000556D</td><td>0x0000E324</td></tr>
<tr><td>Fire Damage (Huge)</td><td>0xD31A163A</td><td>No</td><td>4085</td><td>0x80009AFF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fire Damage (Large)</td><td>0xB85EAA42</td><td>No</td><td>4081</td><td>0x80009AFB</td><td>0x00004AA8</td></tr>
<tr><td>Fire Damage (Medium Canopy)</td><td>0xE87D41BC</td><td>No</td><td>2806</td><td>0x8000876C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fire Damage (Medium)</td><td>0x3DF67356</td><td>No</td><td>4082</td><td>0x80009AFC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fire Damage (Small)</td><td>0x11D78F96</td><td>No</td><td>4083</td><td>0x80009AFD</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fire Damage (Tiny)</td><td>0x927B288F</td><td>No</td><td>4084</td><td>0x80009AFE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fishing Boat</td><td>0x5ED1AEE5</td><td>Yes</td><td>3245</td><td>0x80008F22</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fishing Boat (Driver)</td><td>0x1C0DF270</td><td>Yes</td><td>3246</td><td>0x80008F23</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fishing Boat (Driver) (Civ Poor female)</td><td>0x75FFCB27</td><td>Yes</td><td>4649</td><td>0x80009FCB</td><td>0x0000526C</td></tr>
<tr><td>Fishing Boat (Driver) (Civ Poor male)</td><td>0x27950AA6</td><td>Yes</td><td>4648</td><td>0x80009FCA</td><td>0x00004E65</td></tr>
<tr><td>Fishing Boat_Ruined</td><td>0xEA99A479</td><td>Yes</td><td>4156</td><td>0x80009B53</td><td>0x0000BB86</td></tr>
<tr><td>FishingBoat_Driver</td><td>0x27672BF8</td><td>Yes</td><td>5083</td><td>0x8000A412</td><td>0x000087AB</td></tr>
<tr><td>Fixed Physics Prop</td><td>0x65635CE1</td><td>No</td><td>3743</td><td>0x8000961D</td><td>0x00002D39</td></tr>
<tr><td>Fixed Physics Prop Destructible</td><td>0xB0B47C61</td><td>No</td><td>3739</td><td>0x80009619</td><td>0x00000449</td></tr>
<tr><td>Fixed Physics Prop destructible chair</td><td>0x114108D2</td><td>No</td><td>2809</td><td>0x8000876F</td><td>0x000096F1</td></tr>
<tr><td>Flare</td><td>0x0DA8F2A7</td><td>No</td><td>3141</td><td>0x80008DCB</td><td>0x00013C6B</td></tr>
<tr><td>Flare Designator</td><td>0x95BBB587</td><td>No</td><td>1919</td><td>0x80007CCC</td><td>0x00010E6F</td></tr>
<tr><td>Flare Projectile</td><td>0xD2E88940</td><td>No</td><td>1918</td><td>0x80007CCB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Flare Projectile Stage 2</td><td>0x691C913C</td><td>No</td><td>1921</td><td>0x80007CCF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Flare0</td><td>0x0DBFB9FD</td><td>No</td><td>3139</td><td>0x80008DC3</td><td>0x00002F61</td></tr>
<tr><td>Flare1</td><td>0xA3BCD488</td><td>No</td><td>3140</td><td>0x80008DC6</td><td>0x0000B879</td></tr>
<tr><td>Flare2</td><td>0xADBAA5AF</td><td>No</td><td>2640</td><td>0x80008622</td><td>0x00005D09</td></tr>
<tr><td>FlareSmoke</td><td>0xE8FE3776</td><td>No</td><td>1091</td><td>0x80006A73</td><td>0xFFFFFFFF</td></tr>
<tr><td>Flatbed Trailer</td><td>0xD779F5F0</td><td>No</td><td>1815</td><td>0x800076A6</td><td>0x000117EB</td></tr>
<tr><td>Flow Control</td><td>0x00C4CFDE</td><td>No</td><td>524</td><td>0x800059E9</td><td>0x0000A66A</td></tr>
<tr><td>foliage_test</td><td>0xBC97DA6D</td><td>No</td><td>2930</td><td>0x800089B1</td><td>0xFFFFFFFF</td></tr>
<tr><td>foodcarts</td><td>0x784CDE76</td><td>No</td><td>115</td><td>0x80004C20</td><td>0x0000BD62</td></tr>
<tr><td>Ford F150</td><td>0x2874601E</td><td>No</td><td>65</td><td>0x80004744</td><td>0x00006FCB</td></tr>
<tr><td>fountains</td><td>0x1A94E908</td><td>No</td><td>113</td><td>0x80004C1E</td><td>0x00004194</td></tr>
<tr><td>Fuel Air Bomb Projectile</td><td>0x4A35D0C4</td><td>No</td><td>3177</td><td>0x80008E4D</td><td>0x00006061</td></tr>
<tr><td>Fuel Air Trail</td><td>0x13432421</td><td>No</td><td>3156</td><td>0x80008E36</td><td>0x0001128A</td></tr>
<tr><td>Fuel Pickup (Large)</td><td>0xDEE1F1F1</td><td>No</td><td>2624</td><td>0x80008609</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fuel Pickup (Small)</td><td>0x8905D2F5</td><td>No</td><td>2623</td><td>0x80008608</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fuel Trailer</td><td>0xD9B1BD84</td><td>No</td><td>1081</td><td>0x80006A1E</td><td>0x0000BA3E</td></tr>
<tr><td>Fuel-Air RPG</td><td>0x47E86EB3</td><td>No</td><td>1364</td><td>0x80006ED0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fx_CHUNKTRAIL_DUST</td><td>0x9FF3CC1A</td><td>No</td><td>3381</td><td>0x800090FD</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fx_CHUNKTRAIL_FIRE</td><td>0xB3F07C5A</td><td>No</td><td>3382</td><td>0x800090FE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Fx_CHUNKTRAIL_UNLITFIRE</td><td>0xCCF36BD2</td><td>No</td><td>3383</td><td>0x800090FF</td><td>0x00009ECA</td></tr>
<tr><td>fx_CollapseBits</td><td>0xD0BAEA4F</td><td>No</td><td>5994</td><td>0x90000066</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_CollapseBitsFort</td><td>0x4B83C230</td><td>No</td><td>5311</td><td>0x8000A923</td><td>0x00002617</td></tr>
<tr><td>fx_CollapseBitsShort</td><td>0x7CDB4407</td><td>No</td><td>5314</td><td>0x8000A927</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_CollapseBitsShortSmoke</td><td>0xEE68CDD6</td><td>No</td><td>5718</td><td>0x8000AD48</td><td>0x00012BB2</td></tr>
<tr><td>fx_CollapseBitsShortSpecial</td><td>0x96ACBE54</td><td>No</td><td>5377</td><td>0x8000A971</td><td>0x00005DB3</td></tr>
<tr><td>fx_CollapseBitsSmoke</td><td>0x93823A5E</td><td>No</td><td>5717</td><td>0x8000AD47</td><td>0x0001394E</td></tr>
<tr><td>fx_CollapseBitsSmokeSuper</td><td>0xF2E7D883</td><td>No</td><td>5716</td><td>0x8000AD46</td><td>0x00008883</td></tr>
<tr><td>fx_CollapseBitsSuper</td><td>0x5B1CB278</td><td>No</td><td>5710</td><td>0x8000AD3F</td><td>0x000002EF</td></tr>
<tr><td>fx_CollapseBitsTiny</td><td>0xD0415261</td><td>No</td><td>5335</td><td>0x8000A93C</td><td>0x00008FD0</td></tr>
<tr><td>fx_CollapseBitsTinySmoke</td><td>0x2335C668</td><td>No</td><td>5719</td><td>0x8000AD49</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_CollapseCoverDust</td><td>0x64E12D08</td><td>No</td><td>5993</td><td>0x90000065</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_CollapseCoverDust_end</td><td>0xE9421F0A</td><td>No</td><td>3113</td><td>0x80008C0B</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_CollapseCoverDust_endSuper</td><td>0xD3CAA477</td><td>No</td><td>5715</td><td>0x8000AD45</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_CollapseCoverDust_LOD0</td><td>0xBBAC3C2C</td><td>No</td><td>5309</td><td>0x8000A921</td><td>0x00013316</td></tr>
<tr><td>fx_CollapseCoverDust_LOD1</td><td>0xB5AE7151</td><td>No</td><td>5310</td><td>0x8000A922</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_CollapseCoverDust_start</td><td>0x81CEB475</td><td>No</td><td>3715</td><td>0x80009561</td><td>0x00003990</td></tr>
<tr><td>fx_CollapseCoverDust_startSuper</td><td>0x8278C062</td><td>No</td><td>5714</td><td>0x8000AD44</td><td>0x0000F8AD</td></tr>
<tr><td>fx_CollapseCoverDustBottom</td><td>0x5685D6B1</td><td>No</td><td>5317</td><td>0x8000A92A</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_CollapseCoverDustBottomSuper</td><td>0x10AC5566</td><td>No</td><td>5713</td><td>0x8000AD43</td><td>0x0000F04D</td></tr>
<tr><td>fx_CollapseCoverDustSuper</td><td>0x8D53C8C1</td><td>No</td><td>5709</td><td>0x8000AD3E</td><td>0x000104D6</td></tr>
<tr><td>fx_CollapseCoverWater</td><td>0xECC01BF5</td><td>No</td><td>3719</td><td>0x80009565</td><td>0x00012971</td></tr>
<tr><td>fx_CollapseFire</td><td>0xC60FDD97</td><td>No</td><td>3114</td><td>0x80008C0C</td><td>0x000044E0</td></tr>
<tr><td>fx_CollapseFireFull</td><td>0xA29C1DD8</td><td>No</td><td>5347</td><td>0x8000A94C</td><td>0x00002D78</td></tr>
<tr><td>fx_CollapseFireFullSuper</td><td>0x3985EFB1</td><td>No</td><td>5711</td><td>0x8000AD40</td><td>0x0000021B</td></tr>
<tr><td>fx_CollapseFireSuper</td><td>0x8994E8D0</td><td>No</td><td>5712</td><td>0x8000AD41</td><td>0x0000A432</td></tr>
<tr><td>fx_EmitChimineySmoke</td><td>0xA73AF2D6</td><td>No</td><td>745</td><td>0x800061FC</td><td>0x0000EF0B</td></tr>
<tr><td>fx_EmitFlame</td><td>0xF7505100</td><td>No</td><td>744</td><td>0x800061FB</td><td>0x0000BE2B</td></tr>
<tr><td>fx_EmitFlameOil</td><td>0x3D4CD6C0</td><td>No</td><td>3714</td><td>0x80009560</td><td>0x0000B68A</td></tr>
<tr><td>fx_EmitFlameOilrigTower</td><td>0x88237E81</td><td>No</td><td>747</td><td>0x800061FE</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_EmitFlameOilrigTower_smoke</td><td>0x7F8DC56B</td><td>No</td><td>5736</td><td>0x8000AD5C</td><td>0x00003FBC</td></tr>
<tr><td>fx_EmitFlameSmall</td><td>0x0EBC8B29</td><td>No</td><td>741</td><td>0x800061F7</td><td>0x0000524D</td></tr>
<tr><td>fx_EmitFlameTiny</td><td>0x4CB97C3A</td><td>No</td><td>742</td><td>0x800061F8</td><td>0x0000997E</td></tr>
<tr><td>fx_EmitSmokeStack</td><td>0x00A433FE</td><td>No</td><td>746</td><td>0x800061FD</td><td>0x00006836</td></tr>
<tr><td>fx_engineDamageSmoke</td><td>0x499056C2</td><td>No</td><td>1269</td><td>0x80006D74</td><td>0x00003539</td></tr>
<tr><td>fx_engineHeatHaze</td><td>0x49A06570</td><td>No</td><td>1268</td><td>0x80006D73</td><td>0x000021BE</td></tr>
<tr><td>fx_Explosion_Huge</td><td>0x09EC0A9B</td><td>No</td><td>1517</td><td>0x80007174</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_Huge_LOD0</td><td>0x6AB2FF79</td><td>No</td><td>5727</td><td>0x8000AD51</td><td>0x000053CF</td></tr>
<tr><td>fx_Explosion_Huge_LOD1</td><td>0x90B0FCB4</td><td>No</td><td>5728</td><td>0x8000AD52</td><td>0x00008FFD</td></tr>
<tr><td>fx_Explosion_HugeBoat</td><td>0x431548E1</td><td>Yes</td><td>5957</td><td>0x8000B1FA</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_HugeOil</td><td>0x78A27901</td><td>No</td><td>752</td><td>0x80006204</td><td>0x0000785F</td></tr>
<tr><td>fx_Explosion_HugeOil_LOD0</td><td>0xFC01CDB3</td><td>No</td><td>5725</td><td>0x8000AD4F</td><td>0x0000120B</td></tr>
<tr><td>fx_Explosion_HugeOil_LOD1</td><td>0x99FEF4D6</td><td>No</td><td>5726</td><td>0x8000AD50</td><td>0x000113AF</td></tr>
<tr><td>fx_Explosion_HugeOil_RigOnly</td><td>0x0B9A59F4</td><td>No</td><td>2784</td><td>0x80008756</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_HugeOilTower</td><td>0x150059D4</td><td>No</td><td>3391</td><td>0x8000910A</td><td>0x00002648</td></tr>
<tr><td>fx_Explosion_HugeOilTower_LOD0</td><td>0xF09B8A90</td><td>No</td><td>5733</td><td>0x8000AD57</td><td>0x00007A5B</td></tr>
<tr><td>fx_Explosion_HugeOilTower_LOD1</td><td>0xDA9DA685</td><td>No</td><td>5734</td><td>0x8000AD58</td><td>0x00000C59</td></tr>
<tr><td>fx_Explosion_HugeOilTower_RigOnly</td><td>0x10E37095</td><td>No</td><td>2785</td><td>0x80008757</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_HugeOilTowerBoat</td><td>0x37C5936A</td><td>Yes</td><td>5798</td><td>0x8000AF00</td><td>0x0000330D</td></tr>
<tr><td>fx_Explosion_Large</td><td>0x0538CC93</td><td>No</td><td>454</td><td>0x80005695</td><td>0x00003801</td></tr>
<tr><td>fx_Explosion_Large_LOD0</td><td>0x89DC4011</td><td>No</td><td>5721</td><td>0x8000AD4B</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_Large_LOD1</td><td>0x8FDA0AEC</td><td>No</td><td>5722</td><td>0x8000AD4C</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_Medium</td><td>0x7A757DBB</td><td>No</td><td>3111</td><td>0x80008C09</td><td>0x00000E18</td></tr>
<tr><td>fx_Explosion_Medium_LOD0</td><td>0x4087C799</td><td>No</td><td>5729</td><td>0x8000AD53</td><td>0x0000CE1A</td></tr>
<tr><td>fx_Explosion_Medium_LOD1</td><td>0xE684FB54</td><td>No</td><td>5730</td><td>0x8000AD54</td><td>0x0000A1AD</td></tr>
<tr><td>fx_Explosion_MediumBoat</td><td>0x27531981</td><td>Yes</td><td>5958</td><td>0x8000B1FB</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_MediumOil</td><td>0xD6FB13A1</td><td>No</td><td>753</td><td>0x80006205</td><td>0x0000C881</td></tr>
<tr><td>fx_Explosion_MediumOil_LOD0</td><td>0xB0987253</td><td>No</td><td>5731</td><td>0x8000AD55</td><td>0x0000F734</td></tr>
<tr><td>fx_Explosion_MediumOil_LOD1</td><td>0xCE9662F6</td><td>No</td><td>5732</td><td>0x8000AD56</td><td>0x000059DA</td></tr>
<tr><td>fx_Explosion_MediumOilPipe</td><td>0xFA3F97E5</td><td>No</td><td>3389</td><td>0x80009107</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_Small</td><td>0xE7AA5B4B</td><td>No</td><td>3112</td><td>0x80008C0A</td><td>0x0000C0DA</td></tr>
<tr><td>fx_Explosion_Small_LOD0</td><td>0x991D9B49</td><td>No</td><td>5723</td><td>0x8000AD4D</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_Small_LOD1</td><td>0x7F1B33C4</td><td>No</td><td>5724</td><td>0x8000AD4E</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_Explosion_SmallBoat</td><td>0xD96D22F1</td><td>Yes</td><td>5959</td><td>0x8000B1FC</td><td>0x0000CD5C</td></tr>
<tr><td>fx_ExplosionGrit</td><td>0x6AD474EF</td><td>No</td><td>743</td><td>0x800061FA</td><td>0x0000AB35</td></tr>
<tr><td>fx_ExplosionGritDelay3</td><td>0x9DB60747</td><td>No</td><td>1270</td><td>0x80006D76</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_ImpactShockwaveMedium</td><td>0xE10E0D0C</td><td>No</td><td>1666</td><td>0x80007359</td><td>0x00004E31</td></tr>
<tr><td>fx_OilrigDebrisDestroy</td><td>0x11199B75</td><td>No</td><td>755</td><td>0x80006207</td><td>0x0000F818</td></tr>
<tr><td>fx_OilrigDebrisDestroyExplosion</td><td>0x360357A6</td><td>No</td><td>776</td><td>0x80006221</td><td>0x000047B5</td></tr>
<tr><td>fx_ShortCollapseCoverDust</td><td>0xDCF9ED86</td><td>No</td><td>5998</td><td>0x9000006A</td><td>0x00010107</td></tr>
<tr><td>fx_ShortCollapseCoverDustBottom</td><td>0x9C913EA3</td><td>No</td><td>5315</td><td>0x8000A928</td><td>0x00010738</td></tr>
<tr><td>fx_ShortCollapseCoverDustFort</td><td>0xDC6FD589</td><td>No</td><td>5312</td><td>0x8000A924</td><td>0x0000BF8A</td></tr>
<tr><td>fx_ShortCollapseCoverDustFortStart</td><td>0x27AC0203</td><td>No</td><td>5313</td><td>0x8000A926</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_ShortCollapseCoverDustStart</td><td>0xF3D0717A</td><td>No</td><td>3701</td><td>0x80009552</td><td>0x0000FB7D</td></tr>
<tr><td>fx_ShortCollapseFire</td><td>0xFE2734ED</td><td>No</td><td>3115</td><td>0x80008C0D</td><td>0x0000657F</td></tr>
<tr><td>fx_ShortCollapseFireDelay</td><td>0x87F84666</td><td>No</td><td>5359</td><td>0x8000A95D</td><td>0x0000FCEF</td></tr>
<tr><td>fx_ShortCoverDustBottom</td><td>0x2ABC0D28</td><td>No</td><td>5316</td><td>0x8000A929</td><td>0xFFFFFFFF</td></tr>
<tr><td>fx_TinyCollapseCoverDust</td><td>0xB66CF4AA</td><td>No</td><td>5333</td><td>0x8000A93A</td><td>0x0000571A</td></tr>
<tr><td>fx_TinyCollapseCoverDustBottom</td><td>0xA126713F</td><td>No</td><td>5334</td><td>0x8000A93B</td><td>0x00005A12</td></tr>
<tr><td>fx_TinyCollapseFire</td><td>0x18281EE9</td><td>No</td><td>5358</td><td>0x8000A95C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Garbage Truck</td><td>0x1015767F</td><td>Yes</td><td>2183</td><td>0x800081D3</td><td>0x000076E6</td></tr>
<tr><td>Garbage Truck (Driver)</td><td>0xAF8AEAEA</td><td>Yes</td><td>4291</td><td>0x80009CBE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Garbage Truck (Driver) (Civ Industrial female)</td><td>0x41195AFC</td><td>Yes</td><td>4293</td><td>0x80009CC0</td><td>0x0000EFAC</td></tr>
<tr><td>Garbage Truck (Driver) (Civ Industrial male)</td><td>0xE242790D</td><td>Yes</td><td>4292</td><td>0x80009CBF</td><td>0x0000B1D2</td></tr>
<tr><td>Garbage_Driver</td><td>0xFC338953</td><td>No</td><td>5060</td><td>0x8000A3F9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Generic_Large_Interior</td><td>0x4EB64B07</td><td>No</td><td>2366</td><td>0x80008320</td><td>0x00001A23</td></tr>
<tr><td>Generic_Small_Interior</td><td>0xFDC46BF3</td><td>No</td><td>2365</td><td>0x8000831F</td><td>0xFFFFFFFF</td></tr>
<tr><td>GlassShards</td><td>0xB6655EC8</td><td>No</td><td>1100</td><td>0x80006A84</td><td>0x0001225E</td></tr>
<tr><td>gleach</td><td>0xEF44FAAB</td><td>No</td><td>895</td><td>0x80006464</td><td>0x00003662</td></tr>
<tr><td>gleach child 1</td><td>0x40537CAC</td><td>No</td><td>896</td><td>0x80006465</td><td>0x0000B890</td></tr>
<tr><td>gleach child 2</td><td>0xDA509D83</td><td>No</td><td>897</td><td>0x80006466</td><td>0x0000DB5E</td></tr>
<tr><td>global_debris_woodbeams01</td><td>0x28FCBBBB</td><td>No</td><td>525</td><td>0x80005A4F</td><td>0x0000C6B8</td></tr>
<tr><td>global_env_tree_large_debris</td><td>0xE25EA4C7</td><td>No</td><td>2800</td><td>0x80008766</td><td>0x00003BD5</td></tr>
<tr><td>global_env_tree_medium_debris</td><td>0x6F648A87</td><td>No</td><td>1946</td><td>0x80007EF4</td><td>0x000064EE</td></tr>
<tr><td>global_env_treecanopy_debris</td><td>0x5F75A3D7</td><td>No</td><td>5192</td><td>0x8000A550</td><td>0x00009193</td></tr>
<tr><td>global_particle_0x80009e34</td><td>0xE7C9E46F</td><td>No</td><td>4470</td><td>0x80009E34</td><td>0x00011DF2</td></tr>
<tr><td>global_particle_airstrike_artillery</td><td>0xF132D8D1</td><td>No</td><td>1949</td><td>0x80007FF3</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_airstrike_bunkerbuster</td><td>0xEEECE9F9</td><td>No</td><td>1975</td><td>0x80008011</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_airstrike_bunkerbuster_flash</td><td>0x1C0D7336</td><td>No</td><td>5735</td><td>0x8000AD59</td><td>0x00001C88</td></tr>
<tr><td>global_particle_airstrike_bunkerbuster_initial</td><td>0x4DCC85CC</td><td>No</td><td>4861</td><td>0x8000A245</td><td>0x00005F4E</td></tr>
<tr><td>global_particle_airstrike_carpetbomb_LOD0</td><td>0xDF505090</td><td>No</td><td>1971</td><td>0x8000800C</td><td>0x000107B8</td></tr>
<tr><td>global_particle_airstrike_carpetbomb_LOD1</td><td>0xC9526C85</td><td>No</td><td>5297</td><td>0x8000A915</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_airstrike_clusterbomb</td><td>0xBBAD61F9</td><td>No</td><td>1972</td><td>0x8000800E</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_airstrike_clusterbomb_flame</td><td>0xFDE728C5</td><td>No</td><td>3443</td><td>0x800091FF</td><td>0x000072A9</td></tr>
<tr><td>global_particle_airstrike_cruisemissile</td><td>0x3113506C</td><td>No</td><td>3433</td><td>0x800091F2</td><td>0x00007B87</td></tr>
<tr><td>global_particle_airstrike_daisycutter</td><td>0x65E42D40</td><td>No</td><td>3429</td><td>0x800091EE</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_airstrike_distance</td><td>0xA3ADF8C8</td><td>No</td><td>4865</td><td>0x8000A24A</td><td>0x00003358</td></tr>
<tr><td>global_particle_airstrike_exit_explosion</td><td>0x9EC090A1</td><td>No</td><td>1888</td><td>0x80007734</td><td>0x00002257</td></tr>
<tr><td>global_particle_airstrike_fuelairbomb</td><td>0x8B944877</td><td>No</td><td>3407</td><td>0x8000911F</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_airstrike_missile</td><td>0x5FED4B9B</td><td>No</td><td>1974</td><td>0x80008010</td><td>0x00013576</td></tr>
<tr><td>global_particle_airstrike_moab</td><td>0xC2F6DEE0</td><td>No</td><td>1994</td><td>0x8000802A</td><td>0x00000C10</td></tr>
<tr><td>global_particle_airstrike_rocket_artillery_LOD0</td><td>0xB3F67166</td><td>No</td><td>5299</td><td>0x8000A917</td><td>0x000049A4</td></tr>
<tr><td>global_particle_airstrike_rocket_artillery_LOD1</td><td>0xD5F8E583</td><td>No</td><td>5300</td><td>0x8000A918</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_airstrike_smartbomb</td><td>0x8EB9C034</td><td>No</td><td>3436</td><td>0x800091F5</td><td>0x000111BF</td></tr>
<tr><td>global_particle_airstrike_tactnuke</td><td>0x45D71EEA</td><td>No</td><td>3404</td><td>0x8000911B</td><td>0x000124D8</td></tr>
<tr><td>global_particle_airstrike_tactnuke_distance</td><td>0x14B7D77C</td><td>No</td><td>5707</td><td>0x8000AD3C</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_blastdoors_ext_smoke</td><td>0xEE56EB8F</td><td>No</td><td>3406</td><td>0x8000911D</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_blastdoors_tunnelbottom_smoke</td><td>0xCE764F3D</td><td>No</td><td>3691</td><td>0x80009548</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_blastdoors_tunneltop_smoke</td><td>0x6DF39525</td><td>No</td><td>3690</td><td>0x80009547</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_boatroostertail</td><td>0xE1FE22C4</td><td>Yes</td><td>4849</td><td>0x8000A238</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_boatroostertail_slow</td><td>0xB43ADDD0</td><td>Yes</td><td>4850</td><td>0x8000A239</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_boatroostertail_small</td><td>0x875B9010</td><td>Yes</td><td>3716</td><td>0x80009562</td><td>0x00004C57</td></tr>
<tr><td>global_particle_boatroostertail_small_drift</td><td>0xC36D5A48</td><td>Yes</td><td>3718</td><td>0x80009564</td><td>0x000103CF</td></tr>
<tr><td>global_particle_boatroostertail_small_slow</td><td>0x7601FDC4</td><td>Yes</td><td>3717</td><td>0x80009563</td><td>0x0000DFB0</td></tr>
<tr><td>global_particle_boatwake</td><td>0x33DF8EDA</td><td>Yes</td><td>3699</td><td>0x80009550</td><td>0x0000F871</td></tr>
<tr><td>global_particle_boatwake_drift</td><td>0xC92D0D2E</td><td>Yes</td><td>3704</td><td>0x80009555</td><td>0x00001842</td></tr>
<tr><td>global_particle_boatwake_drift_small</td><td>0x16141FAA</td><td>Yes</td><td>5193</td><td>0x8000A551</td><td>0x000018DD</td></tr>
<tr><td>global_particle_boatwake_point</td><td>0x8F3162A5</td><td>Yes</td><td>4848</td><td>0x8000A237</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_boatwake_point_slow</td><td>0x73BF064F</td><td>Yes</td><td>4851</td><td>0x8000A23A</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_boatwake_slow</td><td>0xEDAB7A02</td><td>Yes</td><td>3703</td><td>0x80009554</td><td>0x0000C4B1</td></tr>
<tr><td>global_particle_boatwake_slow_small</td><td>0xF1C7B02E</td><td>Yes</td><td>5194</td><td>0x8000A552</td><td>0x0000036C</td></tr>
<tr><td>global_particle_boatwake_small</td><td>0x8032FA06</td><td>Yes</td><td>5195</td><td>0x8000A554</td><td>0x0000A52C</td></tr>
<tr><td>global_particle_buildingdebrislarge</td><td>0xD1492CDA</td><td>No</td><td>1897</td><td>0x80007743</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_bunker_top_smoke</td><td>0x98EE4149</td><td>No</td><td>3692</td><td>0x80009549</td><td>0x00001A4E</td></tr>
<tr><td>global_particle_debris_rpg01</td><td>0x44576F90</td><td>No</td><td>1978</td><td>0x80008017</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_dirtexplosion</td><td>0xB7EDE5F8</td><td>No</td><td>5349</td><td>0x8000A94E</td><td>0x00001A91</td></tr>
<tr><td>global_particle_dirtexplosion_fan_large</td><td>0xDF2F904A</td><td>No</td><td>5376</td><td>0x8000A970</td><td>0x0000AC2F</td></tr>
<tr><td>global_particle_dirtexplosion_large</td><td>0x46DB9478</td><td>No</td><td>5350</td><td>0x8000A94F</td><td>0x00010AAB</td></tr>
<tr><td>global_particle_dirtexplosion_small</td><td>0xEB216074</td><td>No</td><td>5351</td><td>0x8000A950</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_dustexplosion</td><td>0x338AC051</td><td>No</td><td>1898</td><td>0x80007744</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_dustfall</td><td>0xCA4220A3</td><td>No</td><td>5336</td><td>0x8000A93D</td><td>0x0000A963</td></tr>
<tr><td>global_particle_dustshanty</td><td>0x03723F4D</td><td>No</td><td>3702</td><td>0x80009553</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_duststrike</td><td>0x26E1A04A</td><td>No</td><td>1889</td><td>0x80007736</td><td>0x00006D47</td></tr>
<tr><td>global_particle_dusttrail</td><td>0xFAB952F0</td><td>No</td><td>3119</td><td>0x80008C18</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_env_bug_swarm_placeable</td><td>0x6958E54F</td><td>No</td><td>3132</td><td>0x80008C27</td><td>0x0000EE9E</td></tr>
<tr><td>global_particle_env_firesmokeplume_infinite</td><td>0x07C664D5</td><td>No</td><td>4859</td><td>0x8000A243</td><td>0x00006CA4</td></tr>
<tr><td>global_particle_env_godray2_placeable</td><td>0x7956CD3C</td><td>No</td><td>4483</td><td>0x80009E48</td><td>0x00011890</td></tr>
<tr><td>global_particle_env_godray_placeable</td><td>0xC743959A</td><td>No</td><td>3380</td><td>0x800090FC</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_env_merida_smoke_boat</td><td>0x0A9BF54F</td><td>Yes</td><td>5769</td><td>0x8000AED6</td><td>0x00009EB1</td></tr>
<tr><td>global_particle_env_merida_smoke_infinite</td><td>0x100DAAB9</td><td>No</td><td>3117</td><td>0x80008C10</td><td>0x00006084</td></tr>
<tr><td>global_particle_env_mist_light_placeable</td><td>0xE2D5AB12</td><td>No</td><td>4858</td><td>0x8000A241</td><td>0x0000D108</td></tr>
<tr><td>global_particle_env_smokeplume_boat</td><td>0xC85169EF</td><td>Yes</td><td>5770</td><td>0x8000AED7</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_env_smokeplume_boat_LOD1</td><td>0x3F303830</td><td>Yes</td><td>5779</td><td>0x8000AEE0</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_env_smokeplume_distance</td><td>0x81B1D9D4</td><td>No</td><td>4868</td><td>0x8000A250</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_env_smokeplume_distance_light</td><td>0x68CD69CD</td><td>No</td><td>4870</td><td>0x8000A252</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_env_smokeplume_distance_light_LOD1</td><td>0x1B4B3AFA</td><td>No</td><td>5774</td><td>0x8000AEDB</td><td>0x000105E6</td></tr>
<tr><td>global_particle_env_smokeplume_distance_LOD0</td><td>0x76500A90</td><td>No</td><td>5773</td><td>0x8000AEDA</td><td>0x0000F359</td></tr>
<tr><td>global_particle_env_smokeplume_distance_LOD1</td><td>0x60522685</td><td>No</td><td>5772</td><td>0x8000AED9</td><td>0x0000811C</td></tr>
<tr><td>global_particle_env_smokeplume_distance_tall</td><td>0x0E187EA2</td><td>No</td><td>4869</td><td>0x8000A251</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_env_smokeplume_distance_tall_light</td><td>0x549CD12B</td><td>No</td><td>4871</td><td>0x8000A253</td><td>0x0000940C</td></tr>
<tr><td>global_particle_env_smokeplume_distance_tall_light_LOD1</td><td>0xB887A2A4</td><td>No</td><td>5776</td><td>0x8000AEDD</td><td>0x0000703D</td></tr>
<tr><td>global_particle_env_smokeplume_distance_tall_LOD1</td><td>0xD424C6D7</td><td>No</td><td>5775</td><td>0x8000AEDC</td><td>0x0000114B</td></tr>
<tr><td>global_particle_env_smokeplume_infinite</td><td>0x58AC1659</td><td>No</td><td>3129</td><td>0x80008C23</td><td>0x000005ED</td></tr>
<tr><td>global_particle_env_smokeplume_infinite_LOD1</td><td>0x1635366E</td><td>No</td><td>5777</td><td>0x8000AEDE</td><td>0x00011E17</td></tr>
<tr><td>global_particle_env_smokeplume_light_infinite</td><td>0x3969FD12</td><td>No</td><td>3384</td><td>0x80009100</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_env_smokeplume_light_infinite_LOD1</td><td>0x929663A7</td><td>No</td><td>5778</td><td>0x8000AEDF</td><td>0x0000CC94</td></tr>
<tr><td>global_particle_exp_falling_debris_airstrike</td><td>0xBB148FF6</td><td>No</td><td>5379</td><td>0x8000A973</td><td>0x0000E99D</td></tr>
<tr><td>global_particle_exp_falling_debris_huge</td><td>0x71186BE1</td><td>No</td><td>3432</td><td>0x800091F1</td><td>0x00001298</td></tr>
<tr><td>global_particle_exp_falling_debris_lrg</td><td>0xC0D14C79</td><td>No</td><td>3431</td><td>0x800091F0</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_exp_falling_debris_lrg_special</td><td>0x72DEAE19</td><td>No</td><td>5378</td><td>0x8000A972</td><td>0x0000E638</td></tr>
<tr><td>global_particle_exp_falling_debris_lrg_tall</td><td>0x95D31FC9</td><td>No</td><td>3434</td><td>0x800091F3</td><td>0x00005285</td></tr>
<tr><td>global_particle_exp_falling_debris_med</td><td>0xB1FE2F96</td><td>No</td><td>3442</td><td>0x800091FC</td><td>0x00002B83</td></tr>
<tr><td>global_particle_exp_falling_debris_med_tall</td><td>0x98AF6234</td><td>No</td><td>3441</td><td>0x800091FB</td><td>0x00000D0F</td></tr>
<tr><td>global_particle_exp_falling_debris_med_tall_LOD0</td><td>0x481DC970</td><td>No</td><td>5298</td><td>0x8000A916</td><td>0x00013671</td></tr>
<tr><td>global_particle_exp_shockwave_ground</td><td>0x72FDE10D</td><td>No</td><td>3417</td><td>0x80009129</td><td>0x0000036A</td></tr>
<tr><td>global_particle_exp_shockwave_ground_bunkerbuster</td><td>0x40E58CE4</td><td>No</td><td>5342</td><td>0x8000A945</td><td>0x00004B67</td></tr>
<tr><td>global_particle_exp_shockwave_ground_bunkerbuster_a</td><td>0x1162EEAC</td><td>No</td><td>5343</td><td>0x8000A946</td><td>0x0000E142</td></tr>
<tr><td>global_particle_exp_shockwave_ground_bunkerbuster_b</td><td>0xAB600F83</td><td>No</td><td>5344</td><td>0x8000A947</td><td>0x0000A8AC</td></tr>
<tr><td>global_particle_exp_shockwave_ground_lrg</td><td>0x96BEBFA1</td><td>No</td><td>3428</td><td>0x800091ED</td><td>0x00013543</td></tr>
<tr><td>global_particle_exp_shockwave_ground_moab</td><td>0xC88A5AE1</td><td>No</td><td>5341</td><td>0x8000A943</td><td>0x0000DBE9</td></tr>
<tr><td>global_particle_exp_shockwave_ground_pep</td><td>0x0B48A267</td><td>No</td><td>5746</td><td>0x8000AD6B</td><td>0x000051E7</td></tr>
<tr><td>global_particle_exp_shockwave_ground_sml</td><td>0x9042EDA4</td><td>No</td><td>3437</td><td>0x800091F6</td><td>0x00004E0E</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tactnuke</td><td>0x9590904F</td><td>No</td><td>3405</td><td>0x8000911C</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tiny</td><td>0x7DEEC326</td><td>No</td><td>3438</td><td>0x800091F7</td><td>0x000114DD</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tiny_asphalt</td><td>0x2E796D6A</td><td>No</td><td>4846</td><td>0x8000A235</td><td>0x00009E32</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tiny_concrete</td><td>0x3E3664CC</td><td>No</td><td>4847</td><td>0x8000A236</td><td>0x0000BF9D</td></tr>
<tr><td>global_particle_exp_shockwave_ground_tiny_grass</td><td>0x82186D45</td><td>No</td><td>4845</td><td>0x8000A234</td><td>0x00002630</td></tr>
<tr><td>global_particle_exp_sparks_sphere_lrg</td><td>0xA2D1A7B6</td><td>No</td><td>3430</td><td>0x800091EF</td><td>0x000020F7</td></tr>
<tr><td>global_particle_explosion</td><td>0x57F368D9</td><td>No</td><td>5997</td><td>0x90000069</td><td>0x0000FA7C</td></tr>
<tr><td>global_particle_explosion_c4</td><td>0x98FE1D7D</td><td>No</td><td>1992</td><td>0x80008028</td><td>0x0000EFA4</td></tr>
<tr><td>global_particle_explosion_canvas</td><td>0xD0329D94</td><td>No</td><td>3399</td><td>0x80009113</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_canvas_large</td><td>0x45FE04E4</td><td>No</td><td>3400</td><td>0x80009114</td><td>0x000007D6</td></tr>
<tr><td>global_particle_explosion_clothes_a</td><td>0x05F94DB0</td><td>No</td><td>5356</td><td>0x8000A956</td><td>0x00013042</td></tr>
<tr><td>global_particle_explosion_clothes_b</td><td>0xEFF6EC77</td><td>No</td><td>5357</td><td>0x8000A957</td><td>0x0000F069</td></tr>
<tr><td>global_particle_explosion_feathers</td><td>0xDFAAA9E8</td><td>No</td><td>4480</td><td>0x80009E42</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_flag_blue</td><td>0x256C3DC9</td><td>No</td><td>5794</td><td>0x8000AEFA</td><td>0x0000D45C</td></tr>
<tr><td>global_particle_explosion_flag_red</td><td>0x8221D026</td><td>No</td><td>5793</td><td>0x8000AEF9</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_flash</td><td>0x458BF396</td><td>No</td><td>1986</td><td>0x8000801F</td><td>0x00006F6C</td></tr>
<tr><td>global_particle_explosion_flash_large</td><td>0xB7C5C5FA</td><td>No</td><td>3370</td><td>0x800090F1</td><td>0x00003E72</td></tr>
<tr><td>global_particle_explosion_guts</td><td>0xA11F9967</td><td>No</td><td>5738</td><td>0x8000AD61</td><td>0x0000929C</td></tr>
<tr><td>global_particle_explosion_heli_bladeflame</td><td>0x946D93E4</td><td>Yes</td><td>1981</td><td>0x8000801A</td><td>0x00012589</td></tr>
<tr><td>global_particle_explosion_heli_bladesparks</td><td>0x0BA8DD59</td><td>Yes</td><td>1982</td><td>0x8000801B</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_heli_flame</td><td>0x0F2F66A8</td><td>Yes</td><td>2852</td><td>0x80008843</td><td>0x000026DD</td></tr>
<tr><td>global_particle_explosion_huge</td><td>0x5A8AB4FD</td><td>No</td><td>3191</td><td>0x80008E8D</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_huge_oil</td><td>0x75ED7824</td><td>No</td><td>3192</td><td>0x80008E8E</td><td>0x00013E0D</td></tr>
<tr><td>global_particle_explosion_medium</td><td>0xE5802F81</td><td>No</td><td>1989</td><td>0x80008022</td><td>0x0000A88C</td></tr>
<tr><td>global_particle_explosion_medium_oil</td><td>0x043828E0</td><td>No</td><td>3193</td><td>0x80008E8F</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_money_large</td><td>0x78311300</td><td>No</td><td>5322</td><td>0x8000A92F</td><td>0x0000D32A</td></tr>
<tr><td>global_particle_explosion_money_large_fire</td><td>0x50D6FCC3</td><td>No</td><td>5332</td><td>0x8000A939</td><td>0x000056F7</td></tr>
<tr><td>global_particle_explosion_money_small</td><td>0x2B9F96FC</td><td>No</td><td>5323</td><td>0x8000A930</td><td>0x0000EE0F</td></tr>
<tr><td>global_particle_explosion_papers</td><td>0x5E3601BD</td><td>No</td><td>5198</td><td>0x8000A557</td><td>0x00012167</td></tr>
<tr><td>global_particle_explosion_parrotfeathers</td><td>0xCE91FE1C</td><td>No</td><td>4842</td><td>0x8000A225</td><td>0x0000EAC8</td></tr>
<tr><td>global_particle_explosion_pickup_ammo</td><td>0x03451E79</td><td>No</td><td>5327</td><td>0x8000A934</td><td>0x00011C22</td></tr>
<tr><td>global_particle_explosion_pickup_c4</td><td>0x48CE797A</td><td>No</td><td>5331</td><td>0x8000A938</td><td>0x00003332</td></tr>
<tr><td>global_particle_explosion_pickup_fuel</td><td>0x170E0A0F</td><td>No</td><td>5741</td><td>0x8000AD65</td><td>0x0000985B</td></tr>
<tr><td>global_particle_explosion_pickup_grenade</td><td>0xF1C5A4D3</td><td>No</td><td>5329</td><td>0x8000A936</td><td>0x00001C3F</td></tr>
<tr><td>global_particle_explosion_pickup_health</td><td>0x25F57375</td><td>No</td><td>5328</td><td>0x8000A935</td><td>0x0000D482</td></tr>
<tr><td>global_particle_explosion_pickup_large</td><td>0x743A2AD4</td><td>No</td><td>5324</td><td>0x8000A931</td><td>0x0000D0ED</td></tr>
<tr><td>global_particle_explosion_pickup_money</td><td>0xDEF99209</td><td>No</td><td>5325</td><td>0x8000A932</td><td>0x0000536A</td></tr>
<tr><td>global_particle_explosion_pickup_money_small</td><td>0xB35F1111</td><td>No</td><td>5326</td><td>0x8000A933</td><td>0x00008F40</td></tr>
<tr><td>global_particle_explosion_pickup_rocket</td><td>0xA24B5B2B</td><td>No</td><td>5330</td><td>0x8000A937</td><td>0x000028A4</td></tr>
<tr><td>global_particle_explosion_plaster_chips</td><td>0x1B329175</td><td>No</td><td>5764</td><td>0x8000AED1</td><td>0x00012B32</td></tr>
<tr><td>global_particle_explosion_rpg</td><td>0xC2C0EEFD</td><td>No</td><td>1979</td><td>0x80008018</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_rpg_center</td><td>0xB3EE5AAB</td><td>No</td><td>1980</td><td>0x80008019</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_shockwave_ring</td><td>0x94A59F9E</td><td>No</td><td>1987</td><td>0x80008020</td><td>0x00004C8A</td></tr>
<tr><td>global_particle_explosion_shockwave_sphere</td><td>0x772FF1B7</td><td>No</td><td>1985</td><td>0x8000801E</td><td>0x000010F8</td></tr>
<tr><td>global_particle_explosion_shockwave_sphere_bunkerbuster</td><td>0xBFE62FD2</td><td>No</td><td>4860</td><td>0x8000A244</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_small</td><td>0xD21C3CE1</td><td>No</td><td>1990</td><td>0x80008026</td><td>0x0000B55E</td></tr>
<tr><td>global_particle_explosion_tankhatch</td><td>0xB334C7E6</td><td>Yes</td><td>1958</td><td>0x80007FFD</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_tankhull</td><td>0xFB159F49</td><td>Yes</td><td>1963</td><td>0x80008004</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_tankturretflame</td><td>0x1E54DCAF</td><td>Yes</td><td>1964</td><td>0x80008005</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_tankturretseam</td><td>0x590A8C40</td><td>Yes</td><td>1961</td><td>0x80008002</td><td>0x0000E4CC</td></tr>
<tr><td>global_particle_explosion_tiny</td><td>0x6335F002</td><td>No</td><td>1993</td><td>0x80008029</td><td>0x0000F99D</td></tr>
<tr><td>global_particle_explosion_treetrunk</td><td>0xC3B1D63A</td><td>No</td><td>3401</td><td>0x80009115</td><td>0x00010850</td></tr>
<tr><td>global_particle_explosion_vehicle_air</td><td>0xC6622D45</td><td>Yes</td><td>1983</td><td>0x8000801C</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosion_vehicle_ground</td><td>0xDC673342</td><td>Yes</td><td>1962</td><td>0x80008003</td><td>0x00000443</td></tr>
<tr><td>global_particle_explosion_vehicle_weakpoint</td><td>0x0544C717</td><td>Yes</td><td>5791</td><td>0x8000AEF7</td><td>0x00013BDE</td></tr>
<tr><td>global_particle_explosion_water_large</td><td>0x2438D2A1</td><td>No</td><td>4867</td><td>0x8000A24F</td><td>0x00005A2D</td></tr>
<tr><td>global_particle_explosion_waterbumper</td><td>0x71A6013C</td><td>No</td><td>3733</td><td>0x80009574</td><td>0x0000EC09</td></tr>
<tr><td>global_particle_explosion_watertower</td><td>0xA8F00200</td><td>No</td><td>3732</td><td>0x80009573</td><td>0x0000639E</td></tr>
<tr><td>global_particle_explosionhuge</td><td>0xF85E869C</td><td>No</td><td>6000</td><td>0x9000006D</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosionlarge</td><td>0x639F99B6</td><td>No</td><td>6001</td><td>0x9000006E</td><td>0x000049ED</td></tr>
<tr><td>global_particle_explosionoiltower</td><td>0x619FE42A</td><td>No</td><td>3390</td><td>0x80009109</td><td>0x00000F1B</td></tr>
<tr><td>global_particle_explosionsmall</td><td>0x840E78FE</td><td>No</td><td>6002</td><td>0x9000006F</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_explosionverysmall</td><td>0x351DD232</td><td>No</td><td>6003</td><td>0x90000070</td><td>0x00001521</td></tr>
<tr><td>global_particle_fire_armwrestling</td><td>0xD0F96D18</td><td>No</td><td>1959</td><td>0x80007FFE</td><td>0x00005245</td></tr>
<tr><td>global_particle_fire_carhood</td><td>0xC6666A25</td><td>No</td><td>3108</td><td>0x80008C06</td><td>0x00009C09</td></tr>
<tr><td>global_particle_fire_jetengine_boost_infinite</td><td>0xF8068AAD</td><td>No</td><td>5706</td><td>0x8000AD3B</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_fire_jetengine_end</td><td>0x384185DC</td><td>No</td><td>5517</td><td>0x8000AACD</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_fire_jetengine_infinite</td><td>0x5D6365F9</td><td>No</td><td>5382</td><td>0x8000A976</td><td>0x00012D57</td></tr>
<tr><td>global_particle_fire_jetengine_orange_infinite</td><td>0x69333F6E</td><td>No</td><td>5705</td><td>0x8000AD3A</td><td>0x00006CC1</td></tr>
<tr><td>global_particle_fireblue_infinite</td><td>0x791258A3</td><td>No</td><td>4486</td><td>0x80009E4C</td><td>0x0000D91D</td></tr>
<tr><td>global_particle_fireboatflamejet</td><td>0xFB1C0DB8</td><td>Yes</td><td>3724</td><td>0x8000956A</td><td>0x000084D9</td></tr>
<tr><td>global_particle_fireboatflamejet_smoke</td><td>0x54AAFB66</td><td>Yes</td><td>3736</td><td>0x80009577</td><td>0x0000AA57</td></tr>
<tr><td>global_particle_fireboatgrande</td><td>0x148F0151</td><td>Yes</td><td>3720</td><td>0x80009566</td><td>0x00000DEE</td></tr>
<tr><td>global_particle_fireboatgrande_smoke</td><td>0xBD19723B</td><td>Yes</td><td>3737</td><td>0x80009578</td><td>0x0000E838</td></tr>
<tr><td>global_particle_fireboatlarge</td><td>0x440BEA87</td><td>Yes</td><td>5197</td><td>0x8000A556</td><td>0x0000F953</td></tr>
<tr><td>global_particle_fireboatmedium</td><td>0xF05590E7</td><td>Yes</td><td>3721</td><td>0x80009567</td><td>0x0000482A</td></tr>
<tr><td>global_particle_fireboatsmall</td><td>0x798CBC2F</td><td>Yes</td><td>3722</td><td>0x80009568</td><td>0x000054F1</td></tr>
<tr><td>global_particle_fireboattiny</td><td>0x71BD9CD4</td><td>Yes</td><td>3723</td><td>0x80009569</td><td>0x000064F4</td></tr>
<tr><td>global_particle_fireflare_infinite</td><td>0xEEFB3B23</td><td>No</td><td>3726</td><td>0x8000956C</td><td>0x0000A1D1</td></tr>
<tr><td>global_particle_firegrandesmoke</td><td>0x50888846</td><td>No</td><td>1896</td><td>0x8000773F</td><td>0x00012F0A</td></tr>
<tr><td>global_particle_firegrandesmoke_infinite</td><td>0x90D31235</td><td>No</td><td>3392</td><td>0x8000910B</td><td>0x000074E7</td></tr>
<tr><td>global_particle_firegrandesmoke_infinite_smoke</td><td>0xF8C87BEF</td><td>No</td><td>4465</td><td>0x80009E2F</td><td>0x00010BED</td></tr>
<tr><td>global_particle_firegrandesmoke_smoke</td><td>0x948694F4</td><td>No</td><td>4466</td><td>0x80009E30</td><td>0x0000426D</td></tr>
<tr><td>global_particle_firehedge</td><td>0x8E87B41F</td><td>No</td><td>4497</td><td>0x80009E58</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firehydrant_spray</td><td>0x8D57E3E4</td><td>No</td><td>3725</td><td>0x8000956B</td><td>0x000097DE</td></tr>
<tr><td>global_particle_firelarge</td><td>0xF5AB345D</td><td>No</td><td>1890</td><td>0x80007737</td><td>0x0000419A</td></tr>
<tr><td>global_particle_firelarge_infinite</td><td>0xA7BD01E8</td><td>No</td><td>5296</td><td>0x8000A914</td><td>0x00011EE5</td></tr>
<tr><td>global_particle_firelarge_infinite_placeable</td><td>0x57632C60</td><td>No</td><td>5371</td><td>0x8000A96B</td><td>0x000116EC</td></tr>
<tr><td>global_particle_firelarge_smoke</td><td>0xABDE53F7</td><td>No</td><td>4467</td><td>0x80009E31</td><td>0x00004CEE</td></tr>
<tr><td>global_particle_firelargesmoke</td><td>0x749958E4</td><td>No</td><td>1895</td><td>0x8000773D</td><td>0x0000ED25</td></tr>
<tr><td>global_particle_firelargesmoke_infinite</td><td>0x8CF6A76F</td><td>No</td><td>2009</td><td>0x8000803D</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firelargesmoke_infinite_placeable</td><td>0x0D2B6E3F</td><td>No</td><td>5367</td><td>0x8000A967</td><td>0x00001B9D</td></tr>
<tr><td>global_particle_firelargesmoke_infinite_smoke</td><td>0x48974AB9</td><td>No</td><td>4469</td><td>0x80009E33</td><td>0x00009FBA</td></tr>
<tr><td>global_particle_firelargesmoke_infinite_smoke_placeable</td><td>0xA7021585</td><td>No</td><td>5368</td><td>0x8000A968</td><td>0x00001CF8</td></tr>
<tr><td>global_particle_firelargesmoke_smoke</td><td>0x271A4F42</td><td>No</td><td>4468</td><td>0x80009E32</td><td>0x0000F9C1</td></tr>
<tr><td>global_particle_firelargesmoke_smoke_vehicle</td><td>0x35F9E783</td><td>Yes</td><td>5363</td><td>0x8000A962</td><td>0x0000514C</td></tr>
<tr><td>global_particle_firelargesmoke_vehicle</td><td>0xD5624ED9</td><td>Yes</td><td>5362</td><td>0x8000A961</td><td>0x00000B53</td></tr>
<tr><td>global_particle_firemedium</td><td>0x03A9A049</td><td>No</td><td>4853</td><td>0x8000A23C</td><td>0x0000CF4C</td></tr>
<tr><td>global_particle_firemediumsmoke</td><td>0xA169E7F0</td><td>No</td><td>5996</td><td>0x90000068</td><td>0x0000374E</td></tr>
<tr><td>global_particle_firemediumsmoke_heli</td><td>0xDA1905F7</td><td>Yes</td><td>5783</td><td>0x8000AEEF</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firemediumsmoke_heli_infinite</td><td>0xF7211396</td><td>Yes</td><td>5784</td><td>0x8000AEF0</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite</td><td>0xC4858F83</td><td>No</td><td>2022</td><td>0x800080C5</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite_constant</td><td>0xB94BD146</td><td>No</td><td>5743</td><td>0x8000AD67</td><td>0x0000077F</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite_placeable</td><td>0x59DAC62B</td><td>No</td><td>5370</td><td>0x8000A96A</td><td>0x0000F290</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite_smoke</td><td>0x54D85FBD</td><td>No</td><td>4472</td><td>0x80009E36</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firemediumsmoke_infinite_smoke_placeable</td><td>0x7AD74241</td><td>No</td><td>5369</td><td>0x8000A969</td><td>0x00010A10</td></tr>
<tr><td>global_particle_firemediumsmoke_smoke</td><td>0xDEF283BE</td><td>No</td><td>4471</td><td>0x80009E35</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firemediumsmoke_smoke_vehicle</td><td>0xE4D6C747</td><td>Yes</td><td>5361</td><td>0x8000A960</td><td>0x00002B52</td></tr>
<tr><td>global_particle_firemediumsmoke_tree_box_flame</td><td>0x72AB2999</td><td>No</td><td>5787</td><td>0x8000AEF3</td><td>0x00006447</td></tr>
<tr><td>global_particle_firemediumsmoke_vehicle</td><td>0x0E54069D</td><td>Yes</td><td>5360</td><td>0x8000A95F</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firemediumsmoke_vehicle_boat_box_flame</td><td>0xF2762404</td><td>Yes</td><td>5785</td><td>0x8000AEF1</td><td>0x00000A53</td></tr>
<tr><td>global_particle_firemediumsmoke_vehicle_box_flame</td><td>0x602D65D7</td><td>Yes</td><td>4489</td><td>0x80009E4F</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firesmall</td><td>0x608D7C59</td><td>No</td><td>1893</td><td>0x8000773B</td><td>0x00000E8C</td></tr>
<tr><td>global_particle_firesmall_infinite</td><td>0x1337775C</td><td>No</td><td>3376</td><td>0x800090F8</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firesmall_infinite_constant</td><td>0x28FD3D27</td><td>No</td><td>5742</td><td>0x8000AD66</td><td>0x0000A72F</td></tr>
<tr><td>global_particle_firesmall_infinite_placeable</td><td>0xC6DB17EC</td><td>No</td><td>5372</td><td>0x8000A96C</td><td>0x00005B8E</td></tr>
<tr><td>global_particle_firesmall_infinite_smoke</td><td>0x73B0889A</td><td>No</td><td>4474</td><td>0x80009E38</td><td>0x00000A32</td></tr>
<tr><td>global_particle_firesmall_infinite_smoke_placeable</td><td>0xB31C02A6</td><td>No</td><td>5373</td><td>0x8000A96D</td><td>0x00007FEB</td></tr>
<tr><td>global_particle_firesmall_smoke</td><td>0xAB377163</td><td>No</td><td>4473</td><td>0x80009E37</td><td>0x00004777</td></tr>
<tr><td>global_particle_firesmallsmoke</td><td>0x79F41D80</td><td>No</td><td>1894</td><td>0x8000773C</td><td>0x00007ABA</td></tr>
<tr><td>global_particle_firesmallsmoke_smoke</td><td>0xD9B3670E</td><td>No</td><td>4475</td><td>0x80009E39</td><td>0x00004905</td></tr>
<tr><td>global_particle_firesmallsmoke_smoke_vehicle</td><td>0xDA5F1597</td><td>Yes</td><td>5365</td><td>0x8000A964</td><td>0x00002F19</td></tr>
<tr><td>global_particle_firesmallsmoke_vehicle</td><td>0xF46BFBAD</td><td>Yes</td><td>5364</td><td>0x8000A963</td><td>0x0000939F</td></tr>
<tr><td>global_particle_firetiny</td><td>0x92CEB6AA</td><td>No</td><td>6006</td><td>0x90000074</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firetiny_infinite</td><td>0x6FE47C31</td><td>No</td><td>1970</td><td>0x8000800B</td><td>0x000035E2</td></tr>
<tr><td>global_particle_firetiny_infinite_placeable</td><td>0xDA1AC3ED</td><td>No</td><td>5374</td><td>0x8000A96E</td><td>0x00008C0B</td></tr>
<tr><td>global_particle_firetreecanopydwarf</td><td>0xE4AF6CDC</td><td>No</td><td>4844</td><td>0x8000A227</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firetreecanopydwarf_LOD0</td><td>0x90E8C578</td><td>No</td><td>5303</td><td>0x8000A91B</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firetreecanopydwarf_LOD1</td><td>0xBAEB462D</td><td>No</td><td>5304</td><td>0x8000A91C</td><td>0x0000A2ED</td></tr>
<tr><td>global_particle_firetreecanopymedium</td><td>0x9A24C9F5</td><td>No</td><td>3695</td><td>0x8000954C</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firetreecanopymedium_LOD0</td><td>0x339C8FFF</td><td>No</td><td>5301</td><td>0x8000A919</td><td>0x000014C6</td></tr>
<tr><td>global_particle_firetreecanopymedium_LOD1</td><td>0xD199B722</td><td>No</td><td>5302</td><td>0x8000A91A</td><td>0x0000E14E</td></tr>
<tr><td>global_particle_firetreecanopymedium_static</td><td>0xB5C59F0A</td><td>No</td><td>4872</td><td>0x8000A254</td><td>0x0000185E</td></tr>
<tr><td>global_particle_firetreecanopymedium_static_smoke</td><td>0x63DA8038</td><td>No</td><td>5191</td><td>0x8000A54F</td><td>0x00008412</td></tr>
<tr><td>global_particle_firetreecanopysmall</td><td>0x6FFB154D</td><td>No</td><td>3697</td><td>0x8000954E</td><td>0x00012850</td></tr>
<tr><td>global_particle_firetreecanopysmall_LOD0</td><td>0x80283657</td><td>No</td><td>5305</td><td>0x8000A91D</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firetreecanopysmall_LOD1</td><td>0x1E255D7A</td><td>No</td><td>5306</td><td>0x8000A91E</td><td>0x00008EA0</td></tr>
<tr><td>global_particle_firetreecanopytiny</td><td>0x5617466E</td><td>No</td><td>3709</td><td>0x8000955B</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firetreecanopytiny_LOD0</td><td>0x29DA148E</td><td>No</td><td>5307</td><td>0x8000A91F</td><td>0x0001169A</td></tr>
<tr><td>global_particle_firetreecanopytiny_LOD1</td><td>0x0BDC23EB</td><td>No</td><td>5308</td><td>0x8000A920</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firetreelargesmoke</td><td>0xD223D588</td><td>No</td><td>4855</td><td>0x8000A23E</td><td>0x000122D3</td></tr>
<tr><td>global_particle_firetreemediumsmoke</td><td>0x1697661C</td><td>No</td><td>4856</td><td>0x8000A23F</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_firetreesmallsmoke</td><td>0x24986514</td><td>No</td><td>4857</td><td>0x8000A240</td><td>0x0000EE1B</td></tr>
<tr><td>global_particle_firetreetrunkA</td><td>0xB5B9E4F7</td><td>No</td><td>4476</td><td>0x80009E3D</td><td>0x0000641C</td></tr>
<tr><td>global_particle_firetreetrunkB</td><td>0xCBBC4630</td><td>No</td><td>4477</td><td>0x80009E3E</td><td>0x0000957B</td></tr>
<tr><td>global_particle_firetreetrunkC</td><td>0x35BF2BA5</td><td>No</td><td>4484</td><td>0x80009E4A</td><td>0x000062B1</td></tr>
<tr><td>global_particle_firetreetrunkD</td><td>0x2BADD2C6</td><td>No</td><td>4485</td><td>0x80009E4B</td><td>0x00010AD4</td></tr>
<tr><td>global_particle_flaresmoke</td><td>0x02F6773F</td><td>No</td><td>6005</td><td>0x90000072</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_airstrike</td><td>0x9C10F46C</td><td>No</td><td>5771</td><td>0x8000AED8</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_fail</td><td>0xA1F75A3A</td><td>No</td><td>5318</td><td>0x8000A92B</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_green</td><td>0x41675D0B</td><td>No</td><td>1999</td><td>0x80008033</td><td>0x0000BCCE</td></tr>
<tr><td>global_particle_flaresmoke_green_aristrike</td><td>0x1E31D18E</td><td>No</td><td>5780</td><td>0x8000AEEB</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_green_fail</td><td>0xF5894946</td><td>No</td><td>5319</td><td>0x8000A92C</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_green_infinite</td><td>0xC18C0252</td><td>No</td><td>3395</td><td>0x8000910F</td><td>0x000114C0</td></tr>
<tr><td>global_particle_flaresmoke_infinite</td><td>0xED6EA40E</td><td>No</td><td>3394</td><td>0x8000910E</td><td>0x00005A48</td></tr>
<tr><td>global_particle_flaresmoke_lightblue</td><td>0x6EFE9D26</td><td>No</td><td>2000</td><td>0x80008034</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_lightblue_airstrike</td><td>0xA36A90E5</td><td>No</td><td>5781</td><td>0x8000AEEC</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_lightblue_fail</td><td>0xEC738915</td><td>No</td><td>5320</td><td>0x8000A92D</td><td>0x00007FCB</td></tr>
<tr><td>global_particle_flaresmoke_lightblue_infinite</td><td>0xC6BF9415</td><td>No</td><td>3396</td><td>0x80009110</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_yellow</td><td>0xF8171566</td><td>No</td><td>2001</td><td>0x80008035</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_yellow_airstrike</td><td>0x78E50725</td><td>No</td><td>5782</td><td>0x8000AEEE</td><td>0x0000D89E</td></tr>
<tr><td>global_particle_flaresmoke_yellow_fail</td><td>0xE1DBDE55</td><td>No</td><td>5321</td><td>0x8000A92E</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flaresmoke_yellow_infinite</td><td>0xBA245355</td><td>No</td><td>3397</td><td>0x80009111</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flotsum</td><td>0xEB453E60</td><td>No</td><td>3116</td><td>0x80008C0E</td><td>0x00010DF3</td></tr>
<tr><td>global_particle_flotsum_ash</td><td>0xCA429139</td><td>No</td><td>3133</td><td>0x80008C29</td><td>0x0000F2AE</td></tr>
<tr><td>global_particle_flotsum_birds</td><td>0x6BE8743D</td><td>No</td><td>3373</td><td>0x800090F5</td><td>0x0000FA52</td></tr>
<tr><td>global_particle_flotsum_bugs</td><td>0x647189BE</td><td>No</td><td>3131</td><td>0x80008C26</td><td>0x0000DDA3</td></tr>
<tr><td>global_particle_flotsum_bugs_mosquito</td><td>0x04D89340</td><td>No</td><td>3379</td><td>0x800090FB</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flotsum_bugs_pirate</td><td>0x23CEDDB6</td><td>No</td><td>3377</td><td>0x800090F9</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_flotsum_dandy</td><td>0xEBB461C9</td><td>No</td><td>3134</td><td>0x80008C2A</td><td>0x000090DF</td></tr>
<tr><td>global_particle_flotsum_dust</td><td>0xCE4504C3</td><td>No</td><td>3135</td><td>0x80008C2B</td><td>0x00011817</td></tr>
<tr><td>global_particle_flotsum_dust_dark</td><td>0x60EBF5FE</td><td>No</td><td>5375</td><td>0x8000A96F</td><td>0x00006BBC</td></tr>
<tr><td>global_particle_flotsum_dust_ground</td><td>0x5D39458F</td><td>No</td><td>3137</td><td>0x80008C2D</td><td>0x00013716</td></tr>
<tr><td>global_particle_flotsum_leaves</td><td>0x41560073</td><td>No</td><td>3130</td><td>0x80008C25</td><td>0x0000E260</td></tr>
<tr><td>global_particle_flotsum_papers</td><td>0x0961D706</td><td>No</td><td>4854</td><td>0x8000A23D</td><td>0x0000CA18</td></tr>
<tr><td>global_particle_flotsum_smoke_ground</td><td>0x658F68B4</td><td>No</td><td>3136</td><td>0x80008C2C</td><td>0x000128E8</td></tr>
<tr><td>global_particle_fountian_a</td><td>0x35458D10</td><td>No</td><td>3120</td><td>0x80008C19</td><td>0x0000091D</td></tr>
<tr><td>global_particle_fountian_b</td><td>0x1F432BD7</td><td>No</td><td>3128</td><td>0x80008C21</td><td>0x000083B2</td></tr>
<tr><td>global_particle_fountian_drops_a</td><td>0xE146016B</td><td>No</td><td>3126</td><td>0x80008C1F</td><td>0x00001D11</td></tr>
<tr><td>global_particle_fountian_sheet_short_a</td><td>0xDC97F80B</td><td>No</td><td>3124</td><td>0x80008C1D</td><td>0x00009A61</td></tr>
<tr><td>global_particle_fountian_sheet_short_b</td><td>0x029A7274</td><td>No</td><td>3125</td><td>0x80008C1E</td><td>0x000018A4</td></tr>
<tr><td>global_particle_fountian_sheet_tall_a</td><td>0x5D77115A</td><td>No</td><td>3121</td><td>0x80008C1A</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_fountian_sheet_tall_b</td><td>0xBF7E6765</td><td>No</td><td>3122</td><td>0x80008C1B</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_fountian_sheet_tall_c</td><td>0x557B81F0</td><td>No</td><td>3127</td><td>0x80008C20</td><td>0x000077B0</td></tr>
<tr><td>global_particle_fountian_splash_a</td><td>0xD2EC0E42</td><td>No</td><td>3123</td><td>0x80008C1C</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_grenadeexplosion</td><td>0x2440B40B</td><td>No</td><td>5999</td><td>0x9000006C</td><td>0x00000120</td></tr>
<tr><td>global_particle_gritexplosion</td><td>0x314341D1</td><td>No</td><td>5995</td><td>0x90000067</td><td>0x0000F30C</td></tr>
<tr><td>global_particle_hedge_cover</td><td>0xCE8D144F</td><td>No</td><td>5739</td><td>0x8000AD62</td><td>0x000060DA</td></tr>
<tr><td>global_particle_hedge_cover_fire</td><td>0xF5481F8A</td><td>No</td><td>5740</td><td>0x8000AD63</td><td>0x00003C53</td></tr>
<tr><td>global_particle_impact_blood</td><td>0xF9AB154B</td><td>No</td><td>6014</td><td>0x9000007E</td><td>0x00009BC8</td></tr>
<tr><td>global_particle_impact_brick</td><td>0xFB787A44</td><td>No</td><td>6012</td><td>0x9000007C</td><td>0x00000F6C</td></tr>
<tr><td>global_particle_impact_brick_nodamage</td><td>0x6448B461</td><td>No</td><td>4492</td><td>0x80009E52</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_brick_point</td><td>0x1EE5B78B</td><td>No</td><td>5355</td><td>0x8000A954</td><td>0x00004F23</td></tr>
<tr><td>global_particle_impact_brickplaster_nodamage</td><td>0x9DC7132A</td><td>No</td><td>4493</td><td>0x80009E53</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_bullet_blood</td><td>0x99905F7C</td><td>No</td><td>4502</td><td>0x80009E5D</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_bullet_brick</td><td>0x79176617</td><td>No</td><td>2844</td><td>0x8000883B</td><td>0x00008CB1</td></tr>
<tr><td>global_particle_impact_bullet_dirt</td><td>0x3747110B</td><td>No</td><td>2846</td><td>0x8000883D</td><td>0x0000BD11</td></tr>
<tr><td>global_particle_impact_bullet_glass</td><td>0x4F4CAF70</td><td>No</td><td>2848</td><td>0x8000883F</td><td>0x0000D5F8</td></tr>
<tr><td>global_particle_impact_bullet_leaves</td><td>0xDD533E50</td><td>No</td><td>2847</td><td>0x8000883E</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_bullet_metal</td><td>0xEDA838E5</td><td>No</td><td>2849</td><td>0x80008840</td><td>0x0000E6D0</td></tr>
<tr><td>global_particle_impact_bullet_metal_flare</td><td>0xC410BEA4</td><td>No</td><td>4498</td><td>0x80009E59</td><td>0x000075C3</td></tr>
<tr><td>global_particle_impact_bullet_stone</td><td>0xFBA53CCB</td><td>No</td><td>2845</td><td>0x8000883C</td><td>0x0000BB6E</td></tr>
<tr><td>global_particle_impact_bullet_water</td><td>0x58A40C49</td><td>No</td><td>4501</td><td>0x80009E5C</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_bullet_wood</td><td>0xEC2E1CE7</td><td>No</td><td>2850</td><td>0x80008841</td><td>0x00010B39</td></tr>
<tr><td>global_particle_impact_concrete</td><td>0xC99D2D00</td><td>No</td><td>6008</td><td>0x90000078</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_concrete_nodamage</td><td>0xBF5270FD</td><td>No</td><td>4482</td><td>0x80009E44</td><td>0x000079EB</td></tr>
<tr><td>global_particle_impact_concrete_point</td><td>0x59938797</td><td>No</td><td>5354</td><td>0x8000A953</td><td>0x00008039</td></tr>
<tr><td>global_particle_impact_dirt</td><td>0x14CE41AA</td><td>No</td><td>6007</td><td>0x90000077</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_dirt_point</td><td>0x41B379D5</td><td>No</td><td>5353</td><td>0x8000A952</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_generic_nodamage</td><td>0xEA28E571</td><td>No</td><td>4495</td><td>0x80009E56</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_glass</td><td>0x51CCB517</td><td>No</td><td>6016</td><td>0x90000080</td><td>0x0000FEB0</td></tr>
<tr><td>global_particle_impact_glass_nodamage</td><td>0x3C0239E4</td><td>No</td><td>4491</td><td>0x80009E51</td><td>0x00010C7E</td></tr>
<tr><td>global_particle_impact_leaves</td><td>0x94171375</td><td>No</td><td>6013</td><td>0x9000007D</td><td>0x00010F40</td></tr>
<tr><td>global_particle_impact_metal</td><td>0x9386E236</td><td>No</td><td>6011</td><td>0x9000007B</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_metal_nodamage</td><td>0x279A7267</td><td>No</td><td>4481</td><td>0x80009E43</td><td>0x00003EEF</td></tr>
<tr><td>global_particle_impact_metal_nodamage_flare</td><td>0x43D6AC22</td><td>No</td><td>4499</td><td>0x80009E5A</td><td>0x00003506</td></tr>
<tr><td>global_particle_impact_metal_point</td><td>0x6A97ADC1</td><td>No</td><td>5352</td><td>0x8000A951</td><td>0x0000FD41</td></tr>
<tr><td>global_particle_impact_rocket_weakpoint</td><td>0x2C6E80E2</td><td>No</td><td>4503</td><td>0x80009E5F</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_rpg_glass</td><td>0x91BAFC77</td><td>No</td><td>1984</td><td>0x8000801D</td><td>0x00012085</td></tr>
<tr><td>global_particle_impact_slide_brick</td><td>0xE5889AD6</td><td>No</td><td>3730</td><td>0x80009571</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_slide_dirt</td><td>0xE8E827DC</td><td>No</td><td>3728</td><td>0x8000956F</td><td>0x0000CB3B</td></tr>
<tr><td>global_particle_impact_slide_leaves</td><td>0xEDBB4783</td><td>No</td><td>3731</td><td>0x80009572</td><td>0x000028BD</td></tr>
<tr><td>global_particle_impact_slide_stone</td><td>0xABFD5BDA</td><td>No</td><td>3729</td><td>0x80009570</td><td>0x00012674</td></tr>
<tr><td>global_particle_impact_stone</td><td>0x5D7A9344</td><td>No</td><td>6015</td><td>0x9000007F</td><td>0x0000C3F5</td></tr>
<tr><td>global_particle_impact_stone_nodamage</td><td>0x07066F61</td><td>No</td><td>4494</td><td>0x80009E54</td><td>0x0000539E</td></tr>
<tr><td>global_particle_impact_sweat</td><td>0x1567287F</td><td>No</td><td>4841</td><td>0x8000A223</td><td>0x0000D97B</td></tr>
<tr><td>global_particle_impact_water</td><td>0x73FD2F8A</td><td>No</td><td>6009</td><td>0x90000079</td><td>0x0000F3C1</td></tr>
<tr><td>global_particle_impact_wood</td><td>0xEC86D392</td><td>No</td><td>6010</td><td>0x9000007A</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_impact_wood_nodamage</td><td>0x773B3573</td><td>No</td><td>4488</td><td>0x80009E4E</td><td>0x000045C8</td></tr>
<tr><td>global_particle_industrial_fire_infinite</td><td>0xD60D99D3</td><td>No</td><td>1966</td><td>0x80008007</td><td>0x00005348</td></tr>
<tr><td>global_particle_industrial_firesmoke_infinite</td><td>0x0610E7B2</td><td>No</td><td>1965</td><td>0x80008006</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_industrial_smoke_infinite</td><td>0xA2227E4E</td><td>No</td><td>1967</td><td>0x80008008</td><td>0x00012822</td></tr>
<tr><td>global_particle_industrial_smokesmall_infinite</td><td>0x09CB1077</td><td>No</td><td>1969</td><td>0x8000800A</td><td>0x000086B0</td></tr>
<tr><td>global_particle_monstertruck_turbo</td><td>0x9919B4C6</td><td>Yes</td><td>5790</td><td>0x8000AEF6</td><td>0x000095A7</td></tr>
<tr><td>global_particle_muzzleflash</td><td>0x2E59B6BB</td><td>No</td><td>6004</td><td>0x90000071</td><td>0x00008487</td></tr>
<tr><td>global_particle_muzzleflash_25mm</td><td>0xE738A8AF</td><td>No</td><td>2005</td><td>0x80008039</td><td>0x00003ABA</td></tr>
<tr><td>global_particle_muzzleflash_AA</td><td>0x025925B0</td><td>No</td><td>2002</td><td>0x80008036</td><td>0x00002308</td></tr>
<tr><td>global_particle_muzzleflash_artillery</td><td>0x1433A0E8</td><td>No</td><td>5196</td><td>0x8000A555</td><td>0x0000DEEF</td></tr>
<tr><td>global_particle_muzzleflash_blue</td><td>0x341B47C6</td><td>No</td><td>5768</td><td>0x8000AED5</td><td>0x0000A6D9</td></tr>
<tr><td>global_particle_muzzleflash_grenadelauncher</td><td>0x579E9394</td><td>No</td><td>3711</td><td>0x8000955D</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_muzzleflash_handgun</td><td>0x5A1F98BD</td><td>No</td><td>1956</td><td>0x80007FFA</td><td>0x00006398</td></tr>
<tr><td>global_particle_muzzleflash_jet</td><td>0xBA8DBF73</td><td>No</td><td>4928</td><td>0x8000A296</td><td>0x0000B02B</td></tr>
<tr><td>global_particle_muzzleflash_MG</td><td>0x1E98062A</td><td>No</td><td>3694</td><td>0x8000954B</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_muzzleflash_rpg</td><td>0x00F0790B</td><td>No</td><td>1954</td><td>0x80007FF8</td><td>0x000024D2</td></tr>
<tr><td>global_particle_muzzleflash_SAM_amx30</td><td>0x157AAB71</td><td>Yes</td><td>3693</td><td>0x8000954A</td><td>0x00005EC8</td></tr>
<tr><td>global_particle_muzzleflash_shotgun</td><td>0xA45CF97C</td><td>No</td><td>1960</td><td>0x80007FFF</td><td>0x0000AA54</td></tr>
<tr><td>global_particle_muzzleflash_tank</td><td>0xDE8D74DA</td><td>Yes</td><td>1988</td><td>0x80008021</td><td>0x00007B4D</td></tr>
<tr><td>global_particle_muzzleflash_vulcan</td><td>0x0CAA3B0B</td><td>No</td><td>3713</td><td>0x8000955F</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_rotorwash</td><td>0xC05BD005</td><td>No</td><td>3700</td><td>0x80009551</td><td>0x00004635</td></tr>
<tr><td>global_particle_rotorwash_water</td><td>0xC78204C1</td><td>No</td><td>5295</td><td>0x8000A913</td><td>0x0000B8D7</td></tr>
<tr><td>global_particle_shatteringGlass_chandelier</td><td>0xDBE087CF</td><td>No</td><td>4496</td><td>0x80009E57</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_shatteringGlass_vehicle</td><td>0xD1AD89DA</td><td>Yes</td><td>1957</td><td>0x80007FFB</td><td>0x0000EC07</td></tr>
<tr><td>global_particle_shell</td><td>0x867C9756</td><td>No</td><td>6018</td><td>0x90000082</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_shellAA</td><td>0x1ECC57AC</td><td>No</td><td>2004</td><td>0x80008038</td><td>0x00001DAF</td></tr>
<tr><td>global_particle_shellAA_large</td><td>0x874AD95C</td><td>No</td><td>5708</td><td>0x8000AD3D</td><td>0x0000E425</td></tr>
<tr><td>global_particle_shellgrenade</td><td>0xA64EC344</td><td>No</td><td>1950</td><td>0x80007FF4</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_shellhandgun</td><td>0xE86E5149</td><td>No</td><td>1951</td><td>0x80007FF5</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_shellmg</td><td>0x01E51916</td><td>No</td><td>1952</td><td>0x80007FF6</td><td>0x00004544</td></tr>
<tr><td>global_particle_shellmissile</td><td>0x940A359E</td><td>No</td><td>3663</td><td>0x8000951E</td><td>0x0000007D</td></tr>
<tr><td>global_particle_shellrocket</td><td>0xA89FC596</td><td>No</td><td>3665</td><td>0x80009520</td><td>0x00002259</td></tr>
<tr><td>global_particle_shellrpg</td><td>0x2D4A6587</td><td>No</td><td>1955</td><td>0x80007FF9</td><td>0x000028BB</td></tr>
<tr><td>global_particle_shellsam</td><td>0xD4DD31D7</td><td>No</td><td>3375</td><td>0x800090F7</td><td>0x0000B913</td></tr>
<tr><td>global_particle_shellshotgun</td><td>0x55F1C5E8</td><td>No</td><td>1953</td><td>0x80007FF7</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_shellsmall</td><td>0xF7FA615F</td><td>No</td><td>6017</td><td>0x90000081</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_smoke_ac_large_infinite</td><td>0x3A737049</td><td>No</td><td>3734</td><td>0x80009575</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_smoke_ac_small_infinite</td><td>0xC38B1511</td><td>No</td><td>3735</td><td>0x80009576</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_smoke_heli_tailrotor</td><td>0xC389EFF5</td><td>Yes</td><td>1991</td><td>0x80008027</td><td>0x0000D4B5</td></tr>
<tr><td>global_particle_smokeblack</td><td>0xC1BEFB24</td><td>No</td><td>1892</td><td>0x80007739</td><td>0x00007BE7</td></tr>
<tr><td>global_particle_smokeblack_infinite</td><td>0x4F5EC3AF</td><td>No</td><td>1968</td><td>0x80008009</td><td>0x000044B4</td></tr>
<tr><td>global_particle_smokeblack_tank</td><td>0x3EBA6E4F</td><td>Yes</td><td>4479</td><td>0x80009E41</td><td>0x00013BC2</td></tr>
<tr><td>global_particle_smokeblackwide</td><td>0x7E9B9B41</td><td>No</td><td>1891</td><td>0x80007738</td><td>0x00009C30</td></tr>
<tr><td>global_particle_smokeblackwide_vehicle</td><td>0x95E10064</td><td>Yes</td><td>5366</td><td>0x8000A965</td><td>0x00010942</td></tr>
<tr><td>global_particle_smokemedium_infinite</td><td>0xD240B36D</td><td>No</td><td>1973</td><td>0x8000800F</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_sparks_rpg_decal</td><td>0xC325D0CC</td><td>No</td><td>4478</td><td>0x80009E40</td><td>0x0000745F</td></tr>
<tr><td>global_particle_sparkslarge</td><td>0x41F7E4A7</td><td>No</td><td>3398</td><td>0x80009112</td><td>0x00003F39</td></tr>
<tr><td>global_particle_sparksmedium</td><td>0x0D4B1F07</td><td>No</td><td>1948</td><td>0x80007FF1</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_splash_dive</td><td>0x1BF7AC8A</td><td>No</td><td>5720</td><td>0x8000AD4A</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_splash_huge</td><td>0x4720A979</td><td>No</td><td>3416</td><td>0x80009128</td><td>0x000081BB</td></tr>
<tr><td>global_particle_splash_lrg</td><td>0x18CBDA81</td><td>No</td><td>3415</td><td>0x80009127</td><td>0x000050D8</td></tr>
<tr><td>global_particle_splash_lrg_vehicle</td><td>0x2A7F4FA4</td><td>Yes</td><td>5737</td><td>0x8000AD5E</td><td>0x000065D7</td></tr>
<tr><td>global_particle_splash_med</td><td>0x4E210C3E</td><td>No</td><td>3414</td><td>0x80009126</td><td>0x000045F8</td></tr>
<tr><td>global_particle_splash_sml</td><td>0x79041D04</td><td>No</td><td>3413</td><td>0x80009125</td><td>0x00004398</td></tr>
<tr><td>global_particle_teargas</td><td>0xD6B6F657</td><td>No</td><td>1995</td><td>0x8000802F</td><td>0x000009CA</td></tr>
<tr><td>global_particle_test2</td><td>0x56D9F6FA</td><td>No</td><td>1887</td><td>0x80007732</td><td>0x0000BD64</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green</td><td>0x7D7470C4</td><td>No</td><td>3118</td><td>0x80008C17</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_fire</td><td>0x26240627</td><td>No</td><td>4862</td><td>0x8000A247</td><td>0x0000E759</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_large</td><td>0x651ADB14</td><td>No</td><td>3710</td><td>0x8000955C</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_large_fire</td><td>0xF6ECDD57</td><td>No</td><td>4863</td><td>0x8000A248</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_small</td><td>0xC8AF6E10</td><td>No</td><td>4490</td><td>0x80009E50</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_tree_destruction_leaves_green_small_fire</td><td>0x472B5433</td><td>No</td><td>4864</td><td>0x8000A249</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_tree_destruction_leaves_palm</td><td>0x984BE1BF</td><td>No</td><td>3402</td><td>0x80009117</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_veh_exhaust_car</td><td>0x06A262B1</td><td>Yes</td><td>2851</td><td>0x80008842</td><td>0x00012C42</td></tr>
<tr><td>global_particle_veh_exhaust_tank</td><td>0x74FE93B9</td><td>Yes</td><td>4866</td><td>0x8000A24B</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_veh_smoke_asphalt</td><td>0x49402063</td><td>Yes</td><td>3706</td><td>0x80009558</td><td>0x0000C7DE</td></tr>
<tr><td>global_particle_veh_smoke_brakes</td><td>0xB89DCE16</td><td>Yes</td><td>3411</td><td>0x80009123</td><td>0x0000338F</td></tr>
<tr><td>global_particle_veh_smoke_dust</td><td>0x52B3F712</td><td>Yes</td><td>3412</td><td>0x80009124</td><td>0x00003B63</td></tr>
<tr><td>global_particle_veh_smoke_grass</td><td>0x078B3B78</td><td>Yes</td><td>3705</td><td>0x80009557</td><td>0x00003D7D</td></tr>
<tr><td>global_particle_veh_smoke_rock</td><td>0x250CEEF1</td><td>Yes</td><td>3707</td><td>0x80009559</td><td>0x000106D8</td></tr>
<tr><td>global_particle_water_spray_fall_pmc</td><td>0x93C07918</td><td>No</td><td>5763</td><td>0x8000AED0</td><td>0x00010F68</td></tr>
<tr><td>global_particle_water_spray_pmc</td><td>0x9AFBE3BE</td><td>No</td><td>5762</td><td>0x8000AECF</td><td>0x0000F803</td></tr>
<tr><td>global_particle_waterfall_bottom</td><td>0x4C8B89AC</td><td>No</td><td>3425</td><td>0x800091E9</td><td>0x00013AD4</td></tr>
<tr><td>global_particle_waterfall_bottom_small</td><td>0x7EAD8BD8</td><td>No</td><td>3371</td><td>0x800090F2</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_waterfall_bottom_tiny</td><td>0x57F582AD</td><td>No</td><td>3372</td><td>0x800090F3</td><td>0x000080F7</td></tr>
<tr><td>global_particle_waterfall_smoke</td><td>0x385341F8</td><td>No</td><td>3388</td><td>0x80009105</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_particle_waterfall_smoke_large</td><td>0x81361078</td><td>No</td><td>4500</td><td>0x80009E5B</td><td>0x0000E184</td></tr>
<tr><td>global_particle_waterfall_wall</td><td>0xFFB152A9</td><td>No</td><td>3426</td><td>0x800091EA</td><td>0x00004BD4</td></tr>
<tr><td>global_particle_waterfall_wall_small</td><td>0x28B0D431</td><td>No</td><td>3374</td><td>0x800090F6</td><td>0x000036FC</td></tr>
<tr><td>global_ribbon_artillery</td><td>0x1CBC91C0</td><td>No</td><td>3367</td><td>0x800090ED</td><td>0x0000EF24</td></tr>
<tr><td>global_ribbon_artillery_daisy</td><td>0xA686E2FB</td><td>No</td><td>3387</td><td>0x80009103</td><td>0x0000F393</td></tr>
<tr><td>global_ribbon_artillery_moab</td><td>0x6A5FE1FA</td><td>No</td><td>3386</td><td>0x80009102</td><td>0x00012ED2</td></tr>
<tr><td>global_ribbon_artillery_slow</td><td>0xE95D53F4</td><td>No</td><td>3385</td><td>0x80009101</td><td>0x0000E11A</td></tr>
<tr><td>global_ribbon_grenade</td><td>0xA2CDC550</td><td>No</td><td>3368</td><td>0x800090EF</td><td>0xFFFFFFFF</td></tr>
<tr><td>global_ribbon_grenadelauncher</td><td>0x1482586C</td><td>No</td><td>3712</td><td>0x8000955E</td><td>0x00009BF2</td></tr>
<tr><td>global_ribbon_plane_contrail</td><td>0xAD2E0F9F</td><td>No</td><td>3369</td><td>0x800090F0</td><td>0x0000B427</td></tr>
<tr><td>global_ribbon_RPG</td><td>0xDA30DE43</td><td>No</td><td>3444</td><td>0x80009201</td><td>0x0000A255</td></tr>
<tr><td>global_strategic_missile_contrail</td><td>0x1EC9F481</td><td>No</td><td>5380</td><td>0x8000A974</td><td>0x000125B5</td></tr>
<tr><td>GR Defender (AA)</td><td>0xFF50CA66</td><td>No</td><td>5035</td><td>0x8000A3D8</td><td>0x0000CB4B</td></tr>
<tr><td>GR Defender (AT)</td><td>0x15AECCF9</td><td>No</td><td>5034</td><td>0x8000A3D7</td><td>0x00006520</td></tr>
<tr><td>GR Defender (AT) (Window Spawner)</td><td>0x502D026E</td><td>No</td><td>3005</td><td>0x80008A25</td><td>0x0000469A</td></tr>
<tr><td>GR Defender (MG)</td><td>0x6C3D798C</td><td>No</td><td>5033</td><td>0x8000A3D6</td><td>0x000057C5</td></tr>
<tr><td>GR Defender (rifle)</td><td>0xDAE42A40</td><td>No</td><td>5032</td><td>0x8000A3D5</td><td>0x0000297D</td></tr>
<tr><td>Grapple</td><td>0x25F753CA</td><td>No</td><td>943</td><td>0x80006545</td><td>0x00009CEE</td></tr>
<tr><td>Grapple Hook</td><td>0xB3AC7513</td><td>No</td><td>944</td><td>0x80006546</td><td>0xFFFFFFFF</td></tr>
<tr><td>Grass01</td><td>0x6EE5BA88</td><td>No</td><td>619</td><td>0x80005C2D</td><td>0x0000F517</td></tr>
<tr><td>Grass01_PMC</td><td>0x5EB991F1</td><td>No</td><td>3964</td><td>0x80009954</td><td>0x00010204</td></tr>
<tr><td>Grass01_Short</td><td>0x143B218F</td><td>No</td><td>638</td><td>0x80005C46</td><td>0x000097B9</td></tr>
<tr><td>Grass01_swamp</td><td>0x2513CF9D</td><td>No</td><td>3962</td><td>0x80009952</td><td>0xFFFFFFFF</td></tr>
<tr><td>Grass01_Tall</td><td>0x8EAD531E</td><td>No</td><td>928</td><td>0x800064CE</td><td>0x000096D1</td></tr>
<tr><td>Grass01_TallSwamp</td><td>0xCCE17C62</td><td>No</td><td>1695</td><td>0x80007534</td><td>0x00004AE5</td></tr>
<tr><td>GrassJungle</td><td>0x96E15D32</td><td>No</td><td>3961</td><td>0x8000994B</td><td>0x000076EB</td></tr>
<tr><td>GrassThick</td><td>0x3BE92EA4</td><td>No</td><td>1737</td><td>0x800075B0</td><td>0x0000FC80</td></tr>
<tr><td>GrassYellow</td><td>0x423C7291</td><td>No</td><td>3960</td><td>0x8000994A</td><td>0x000065D1</td></tr>
<tr><td>Grassyellowgreen</td><td>0xC61E7E9E</td><td>No</td><td>3556</td><td>0x800093BE</td><td>0x0000DBE3</td></tr>
<tr><td>Grenade</td><td>0x496D5A75</td><td>No</td><td>4</td><td>0x80002331</td><td>0xFFFFFFFF</td></tr>
<tr><td>Grenade (AI)</td><td>0x36B18E60</td><td>No</td><td>2982</td><td>0x80008A0B</td><td>0x00008FA7</td></tr>
<tr><td>Grenade Launcher</td><td>0x06332D9F</td><td>No</td><td>1333</td><td>0x80006EA4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Grenade Launcher PEP</td><td>0x7200B6C8</td><td>No</td><td>5766</td><td>0x8000AED3</td><td>0x000016B4</td></tr>
<tr><td>Grenade Launcher Projectile</td><td>0x188B0408</td><td>No</td><td>1334</td><td>0x80006EA6</td><td>0x0000C0D5</td></tr>
<tr><td>Grenade Launcher Projectile PEP</td><td>0xF50ECA0F</td><td>No</td><td>5767</td><td>0x8000AED4</td><td>0x00007D4B</td></tr>
<tr><td>Grenade MG Projectile</td><td>0x4254D63C</td><td>No</td><td>1571</td><td>0x8000720E</td><td>0x0000584A</td></tr>
<tr><td>Grenade Projectile</td><td>0xC4817A02</td><td>No</td><td>5</td><td>0x80002332</td><td>0xFFFFFFFF</td></tr>
<tr><td>Grenade Projectile (AI)</td><td>0x42E5A8F1</td><td>No</td><td>2981</td><td>0x80008A0A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Guerilla</td><td>0xB10D73CE</td><td>No</td><td>14</td><td>0x80002CF1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Guerilla Boss</td><td>0xFB56A321</td><td>No</td><td>2118</td><td>0x8000818C</td><td>0x00013AB9</td></tr>
<tr><td>Guerilla Elite Soldier</td><td>0x0FA5ED09</td><td>No</td><td>2117</td><td>0x8000818B</td><td>0x00013519</td></tr>
<tr><td>Guerilla Heavy</td><td>0x1AB98DEF</td><td>No</td><td>2125</td><td>0x80008193</td><td>0x00012440</td></tr>
<tr><td>Guerilla Heavy (Light MG)</td><td>0x954BECF8</td><td>No</td><td>1348</td><td>0x80006EBD</td><td>0x00009A5B</td></tr>
<tr><td>Guerilla Heavy (RPG)</td><td>0x90468595</td><td>No</td><td>518</td><td>0x800056E8</td><td>0x0000FF88</td></tr>
<tr><td>Guerilla Officer</td><td>0x333D82A4</td><td>No</td><td>2126</td><td>0x80008194</td><td>0x000127AD</td></tr>
<tr><td>Guerilla Officer (Female)</td><td>0x96F68841</td><td>No</td><td>2129</td><td>0x80008197</td><td>0xFFFFFFFF</td></tr>
<tr><td>Guerilla Prisoner</td><td>0xFDD26F2E</td><td>No</td><td>2371</td><td>0x80008326</td><td>0x00000008</td></tr>
<tr><td>Guerilla Soldier</td><td>0x6C42D8C8</td><td>No</td><td>31</td><td>0x80004381</td><td>0x00011038</td></tr>
<tr><td>Guerilla Soldier (Female)</td><td>0xB5DE8E35</td><td>No</td><td>515</td><td>0x800056E5</td><td>0x00007248</td></tr>
<tr><td>Guerilla Soldier (God)</td><td>0x4EAC3517</td><td>No</td><td>5841</td><td>0x8000AF96</td><td>0x0000E98C</td></tr>
<tr><td>Guerilla Soldier B</td><td>0x388DED42</td><td>No</td><td>516</td><td>0x800056E6</td><td>0x000002B5</td></tr>
<tr><td>Guerilla Soldier B (Female)</td><td>0x2FBF334F</td><td>No</td><td>517</td><td>0x800056E7</td><td>0x0000872A</td></tr>
<tr><td>Guerilla Starter 01</td><td>0xB2B19FD4</td><td>No</td><td>2121</td><td>0x8000818F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Guerilla Starter 02</td><td>0x8CAF256B</td><td>No</td><td>2122</td><td>0x80008190</td><td>0xFFFFFFFF</td></tr>
<tr><td>Guerilla Starter 03</td><td>0xAAAD160E</td><td>No</td><td>2124</td><td>0x80008192</td><td>0x0000A62E</td></tr>
<tr><td>Guerilla Starter 04</td><td>0xB4BE6EED</td><td>No</td><td>2120</td><td>0x8000818E</td><td>0x0000148C</td></tr>
<tr><td>Guerilla Starter 05</td><td>0x8ABBEE38</td><td>No</td><td>2123</td><td>0x80008191</td><td>0x00007853</td></tr>
<tr><td>Guerilla Starters</td><td>0x4EEA8396</td><td>No</td><td>2119</td><td>0x8000818D</td><td>0x000020CB</td></tr>
<tr><td>Guerilla Tank Commander</td><td>0xA20BDCE8</td><td>Yes</td><td>2127</td><td>0x80008195</td><td>0x00011A5F</td></tr>
<tr><td>Guerilla Worker</td><td>0xDCE7940C</td><td>No</td><td>2128</td><td>0x80008196</td><td>0x0000A772</td></tr>
<tr><td>Gunship Shell</td><td>0xB5434279</td><td>Yes</td><td>5828</td><td>0x8000AF87</td><td>0x00009E0D</td></tr>
<tr><td>Guntruck (OC)</td><td>0x8730B849</td><td>Yes</td><td>856</td><td>0x800063A9</td><td>0x0000001B</td></tr>
<tr><td>Guntruck (OC) (Driver)</td><td>0x1776F2E4</td><td>Yes</td><td>2268</td><td>0x80008236</td><td>0x00008E1B</td></tr>
<tr><td>Guntruck (OC) (Full)</td><td>0x6D9A82A3</td><td>Yes</td><td>2269</td><td>0x80008237</td><td>0x0000DE10</td></tr>
<tr><td>Guntruck (OC) (Gunners Only)</td><td>0xC8628708</td><td>Yes</td><td>4994</td><td>0x8000A3AA</td><td>0x0000BBEC</td></tr>
<tr><td>Guntruck (OC) (SemiFull)</td><td>0x47036AC1</td><td>Yes</td><td>5155</td><td>0x8000A48E</td><td>0xFFFFFFFF</td></tr>
<tr><td>GuntruckOC_Driver</td><td>0x07CEED75</td><td>Yes</td><td>5383</td><td>0x8000A977</td><td>0x00002287</td></tr>
<tr><td>GurDbSpawner</td><td>0x7C80110D</td><td>No</td><td>2379</td><td>0x80008337</td><td>0x0000BB80</td></tr>
<tr><td>GurDbSpawner (Squad Full AT)</td><td>0x81FE6838</td><td>No</td><td>5663</td><td>0x8000ACA6</td><td>0xFFFFFFFF</td></tr>
<tr><td>GurDbSpawner (Squad Half AT)</td><td>0x792FB590</td><td>No</td><td>5664</td><td>0x8000ACA7</td><td>0xFFFFFFFF</td></tr>
<tr><td>GurDbSpawner (Squad Quarter AT)</td><td>0x608DA4BD</td><td>No</td><td>5910</td><td>0x8000B03D</td><td>0xFFFFFFFF</td></tr>
<tr><td>GurDbSpawner (Squad)</td><td>0x01EB03A6</td><td>No</td><td>3015</td><td>0x80008A2F</td><td>0x0000427B</td></tr>
<tr><td>GurHq_Interior</td><td>0x50916633</td><td>No</td><td>2362</td><td>0x8000831C</td><td>0xFFFFFFFF</td></tr>
<tr><td>GurPedTraffic</td><td>0x0663B41F</td><td>No</td><td>1942</td><td>0x80007E0C</td><td>0x000140F1</td></tr>
<tr><td>GurVehTraffic</td><td>0x4FD073D1</td><td>No</td><td>1941</td><td>0x80007E0B</td><td>0x00012AE0</td></tr>
<tr><td>HangarTest01</td><td>0x7D7932A9</td><td>No</td><td>3079</td><td>0x80008BA3</td><td>0xFFFFFFFF</td></tr>
<tr><td>HE Autocannon Shell</td><td>0x9E32F51C</td><td>No</td><td>5825</td><td>0x8000AF84</td><td>0x0000A753</td></tr>
<tr><td>HE Autocannon Shell (CH)</td><td>0x1D6587CA</td><td>No</td><td>5827</td><td>0x8000AF86</td><td>0x00000CF2</td></tr>
<tr><td>Health Pickup</td><td>0xB8580455</td><td>No</td><td>1336</td><td>0x80006EA9</td><td>0x0000979B</td></tr>
<tr><td>Heavy MG Bullet</td><td>0x22982FBE</td><td>No</td><td>473</td><td>0x800056AD</td><td>0x0000D695</td></tr>
<tr><td>Heavy MG Bullet (AL)</td><td>0xF2677BFA</td><td>No</td><td>4090</td><td>0x80009B05</td><td>0x00004276</td></tr>
<tr><td>Heavy MG Bullet (CH)</td><td>0xD4C2BF04</td><td>No</td><td>4088</td><td>0x80009B03</td><td>0xFFFFFFFF</td></tr>
<tr><td>Heavy MG Bullet (GR)</td><td>0x8A7E6992</td><td>No</td><td>4089</td><td>0x80009B04</td><td>0x00013E25</td></tr>
<tr><td>HeavyPropTemplate</td><td>0x7C86FBD7</td><td>No</td><td>414</td><td>0x8000558E</td><td>0x00002F87</td></tr>
<tr><td>Helicopter</td><td>0x800DC82E</td><td>Yes</td><td>852</td><td>0x800063A3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Helicopter_Hijack_Entrance</td><td>0x9F874D9E</td><td>Yes</td><td>1074</td><td>0x800069A8</td><td>0xFFFFFFFF</td></tr>
<tr><td>HeliList_Caracas_Act1_A</td><td>0x582F4DB8</td><td>Yes</td><td>4585</td><td>0x80009F51</td><td>0x0000BDD2</td></tr>
<tr><td>HeliList_Caracas_Act2_ALL</td><td>0xF3A82FDB</td><td>Yes</td><td>4586</td><td>0x80009F52</td><td>0x000067D6</td></tr>
<tr><td>HeliList_Caracas_Act3ALL</td><td>0x552BB387</td><td>Yes</td><td>4587</td><td>0x80009F53</td><td>0x0000EE8B</td></tr>
<tr><td>HeliList_Caracas_Act3CHI</td><td>0x50E738C8</td><td>Yes</td><td>4588</td><td>0x80009F54</td><td>0xFFFFFFFF</td></tr>
<tr><td>HeliList_Cumana_Act1_CHI</td><td>0xF3809ADE</td><td>Yes</td><td>4589</td><td>0x80009F56</td><td>0x0000E8C5</td></tr>
<tr><td>HeliList_Cumana_Act2_CHI</td><td>0x858EDC6D</td><td>Yes</td><td>4590</td><td>0x80009F58</td><td>0x000118C1</td></tr>
<tr><td>HeliList_JungleMtn_Act1</td><td>0x254B4DAC</td><td>Yes</td><td>5629</td><td>0x8000AC7F</td><td>0x00005960</td></tr>
<tr><td>HeliList_Mar_City_Act1_A</td><td>0xCF63A97C</td><td>Yes</td><td>4580</td><td>0x80009F49</td><td>0x0000F12A</td></tr>
<tr><td>HeliList_Mar_City_Act2_A</td><td>0xA219969F</td><td>Yes</td><td>4581</td><td>0x80009F4A</td><td>0x0000AAA2</td></tr>
<tr><td>HeliList_Mar_City_Act3_A</td><td>0x30C61E5A</td><td>Yes</td><td>4582</td><td>0x80009F4B</td><td>0x0001036C</td></tr>
<tr><td>HeliList_Merida_Act1_A</td><td>0x77024A0A</td><td>Yes</td><td>4583</td><td>0x80009F4D</td><td>0x0000E4F5</td></tr>
<tr><td>HeliList_Merida_Act2_A</td><td>0x9F92D6F9</td><td>Yes</td><td>4584</td><td>0x80009F4E</td><td>0x000043E3</td></tr>
<tr><td>Hero</td><td>0x51728909</td><td>No</td><td>505</td><td>0x800056DA</td><td>0x00001D81</td></tr>
<tr><td>Hibernation Control (Building Huge)</td><td>0xBF977E5B</td><td>No</td><td>1882</td><td>0x80007703</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Building Large)</td><td>0xA6C02A91</td><td>No</td><td>1881</td><td>0x80007702</td><td>0x00013DE1</td></tr>
<tr><td>Hibernation Control (Building Medium)</td><td>0x1272156B</td><td>No</td><td>1880</td><td>0x80007701</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Building Small)</td><td>0x903C1895</td><td>No</td><td>1879</td><td>0x80007700</td><td>0x0000AFF6</td></tr>
<tr><td>Hibernation Control (Building Static Small)</td><td>0x74CA0025</td><td>No</td><td>4771</td><td>0x8000A17F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Building Streamer)</td><td>0x3E1E0B7F</td><td>No</td><td>4984</td><td>0x8000A39F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Building Super)</td><td>0x9CD0BE09</td><td>No</td><td>4770</td><td>0x8000A17E</td><td>0x00012DBE</td></tr>
<tr><td>Hibernation Control (Effects Huge)</td><td>0x23712EBB</td><td>No</td><td>4960</td><td>0x8000A387</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Effects Large)</td><td>0x01DA5C71</td><td>No</td><td>4959</td><td>0x8000A386</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Effects Medium)</td><td>0x1226B0CB</td><td>No</td><td>4781</td><td>0x8000A189</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Effects Small)</td><td>0xABFE3D75</td><td>No</td><td>4780</td><td>0x8000A188</td><td>0x0000018A</td></tr>
<tr><td>Hibernation Control (Effects Standard)</td><td>0xC2F16CC5</td><td>No</td><td>4779</td><td>0x8000A187</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Effects Super)</td><td>0x5E9D7169</td><td>No</td><td>4961</td><td>0x8000A388</td><td>0x0000C143</td></tr>
<tr><td>Hibernation Control (Environmental Huge)</td><td>0x842A9E89</td><td>No</td><td>6041</td><td>0x90000199</td><td>0x0000F961</td></tr>
<tr><td>Hibernation Control (Environmental Large)</td><td>0xA35F2AEF</td><td>No</td><td>6040</td><td>0x90000198</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Environmental Medium)</td><td>0x3B6CE98D</td><td>No</td><td>6039</td><td>0x90000197</td><td>0x000122BA</td></tr>
<tr><td>Hibernation Control (Environmental Small)</td><td>0x715BB747</td><td>No</td><td>6038</td><td>0x90000196</td><td>0x000043C9</td></tr>
<tr><td>Hibernation Control (Environmental Super)</td><td>0x23937BDF</td><td>No</td><td>2838</td><td>0x80008793</td><td>0x00001BC0</td></tr>
<tr><td>Hibernation Control (Environmental Tiny)</td><td>0x9E2783EC</td><td>No</td><td>6042</td><td>0x9000019A</td><td>0x00013AE6</td></tr>
<tr><td>Hibernation Control (Foliage Scrub Brush Assets)</td><td>0x40ED35AB</td><td>No</td><td>2823</td><td>0x80008781</td><td>0x000135BE</td></tr>
<tr><td>Hibernation Control (Prop Huge)</td><td>0x11E18E88</td><td>No</td><td>6123</td><td>0x900001F5</td><td>0x0000F083</td></tr>
<tr><td>Hibernation Control (Prop Large)</td><td>0x0DC7C248</td><td>No</td><td>6122</td><td>0x900001F4</td><td>0x0000EBB5</td></tr>
<tr><td>Hibernation Control (Prop Medium)</td><td>0xD7226CF8</td><td>No</td><td>6121</td><td>0x900001F3</td><td>0x00008F7D</td></tr>
<tr><td>Hibernation Control (Prop small)</td><td>0x048DCDB0</td><td>No</td><td>6120</td><td>0x900001F2</td><td>0x00008397</td></tr>
<tr><td>Hibernation Control (Prop Super)</td><td>0xA682B7D4</td><td>No</td><td>4734</td><td>0x8000A029</td><td>0x000070B5</td></tr>
<tr><td>Hibernation Control (Vehicle Helicopter)</td><td>0xD6D598A3</td><td>Yes</td><td>878</td><td>0x800063D2</td><td>0x000072F1</td></tr>
<tr><td>Hibernation Control (Vehicle Immobile Ship)</td><td>0x6E396D12</td><td>Yes</td><td>3207</td><td>0x80008EF9</td><td>0x000066AB</td></tr>
<tr><td>Hibernation Control (Vehicle LargeA)</td><td>0x9B0967A8</td><td>No</td><td>879</td><td>0x800063D3</td><td>0x00002510</td></tr>
<tr><td>Hibernation Control (Vehicle LargeB)</td><td>0x097E2261</td><td>No</td><td>877</td><td>0x800063D1</td><td>0x0000A7C2</td></tr>
<tr><td>Hibernation Control (Vehicle Medium)</td><td>0x35E994E5</td><td>No</td><td>875</td><td>0x800063CF</td><td>0x00011173</td></tr>
<tr><td>Hibernation Control (Vehicle Plane)</td><td>0x022C183A</td><td>No</td><td>1200</td><td>0x80006CB0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Hibernation Control (Vehicle Small) 0</td><td>0x05451017</td><td>No</td><td>880</td><td>0x800063D4</td><td>0x00003C1C</td></tr>
<tr><td>Hibernation Control (Vehicle Tiny)</td><td>0xFA430C24</td><td>No</td><td>876</td><td>0x800063D0</td><td>0x00012960</td></tr>
<tr><td>Hibernation Control (Vehicle Wheels)</td><td>0xDE606342</td><td>No</td><td>1175</td><td>0x80006C87</td><td>0x00001F30</td></tr>
<tr><td>HighDensityPedTraffic</td><td>0x782C6BF9</td><td>No</td><td>1899</td><td>0x800077FE</td><td>0xFFFFFFFF</td></tr>
<tr><td>HighRoad</td><td>0x59FE080B</td><td>No</td><td>98</td><td>0x80004BFF</td><td>0xFFFFFFFF</td></tr>
<tr><td>HMMWV (4 door base)</td><td>0x67D16052</td><td>No</td><td>3528</td><td>0x8000933C</td><td>0x0000D94F</td></tr>
<tr><td>HMMWV (Armored) (50Cal)</td><td>0x37905F6B</td><td>No</td><td>3529</td><td>0x8000933D</td><td>0x00008E9A</td></tr>
<tr><td>HMMWV (Armored) (50Cal) (Driver)</td><td>0x738B3286</td><td>No</td><td>3536</td><td>0x80009344</td><td>0xFFFFFFFF</td></tr>
<tr><td>HMMWV (Armored) (50Cal) (DriverGunner)</td><td>0x8DD3AE5D</td><td>No</td><td>3540</td><td>0x80009348</td><td>0xFFFFFFFF</td></tr>
<tr><td>HMMWV (Armored) (50Cal) (Full)</td><td>0x2E06295D</td><td>No</td><td>3601</td><td>0x8000944A</td><td>0xFFFFFFFF</td></tr>
<tr><td>HMMWV (Armored) (base)</td><td>0x91F9A7C7</td><td>No</td><td>3525</td><td>0x80009339</td><td>0x00001359</td></tr>
<tr><td>HMMWV (Armored) (GL)</td><td>0x80B1B641</td><td>No</td><td>3530</td><td>0x8000933E</td><td>0x00011696</td></tr>
<tr><td>HMMWV (Armored) (GL) (Driver)</td><td>0xD175755C</td><td>No</td><td>3534</td><td>0x80009342</td><td>0x0000BF84</td></tr>
<tr><td>HMMWV (Armored) (GL) (DriverGunner)</td><td>0xF8B8D143</td><td>No</td><td>3541</td><td>0x80009349</td><td>0xFFFFFFFF</td></tr>
<tr><td>HMMWV (Armored) (GL) (Full)</td><td>0x35921ACB</td><td>No</td><td>3602</td><td>0x8000944B</td><td>0x0000D2A5</td></tr>
<tr><td>HMMWV (Armored) (TOW)</td><td>0x9B70EDF2</td><td>No</td><td>3531</td><td>0x8000933F</td><td>0x000140EA</td></tr>
<tr><td>HMMWV (Armored) (TOW) (Driver)</td><td>0x39BB2F99</td><td>No</td><td>3535</td><td>0x80009343</td><td>0xFFFFFFFF</td></tr>
<tr><td>HMMWV (Armored) (TOW) (DriverGunner)</td><td>0xE377604A</td><td>No</td><td>3539</td><td>0x80009347</td><td>0x0000C289</td></tr>
<tr><td>HMMWV (Armored) (TOW) (Full)</td><td>0x4BFDFBBE</td><td>No</td><td>3603</td><td>0x8000944C</td><td>0xFFFFFFFF</td></tr>
<tr><td>HMMWV (Avenger)</td><td>0xAAB4BBC1</td><td>No</td><td>3524</td><td>0x80009338</td><td>0x0000E148</td></tr>
<tr><td>HMMWV (Avenger) (Driver)</td><td>0x0273ADDC</td><td>No</td><td>3533</td><td>0x80009341</td><td>0xFFFFFFFF</td></tr>
<tr><td>HMMWV (Avenger) (DriverGunner)</td><td>0xAB0145C3</td><td>No</td><td>3538</td><td>0x80009346</td><td>0x00010732</td></tr>
<tr><td>HMMWV (Avenger) (Full)</td><td>0x50027F4B</td><td>No</td><td>3600</td><td>0x80009449</td><td>0x00005DAD</td></tr>
<tr><td>HMMWV (base)</td><td>0x2CC31BFE</td><td>No</td><td>1419</td><td>0x80006F72</td><td>0x00007061</td></tr>
<tr><td>HMMWV (Softtop)</td><td>0x1D5BDF68</td><td>No</td><td>714</td><td>0x800060B1</td><td>0x0000F654</td></tr>
<tr><td>HMMWV (Softtop) (Driver)</td><td>0x4A8DFEC7</td><td>No</td><td>3537</td><td>0x80009345</td><td>0x00008E0A</td></tr>
<tr><td>HMMWV (Softtop) (Full)</td><td>0x266B760C</td><td>No</td><td>3604</td><td>0x8000944D</td><td>0xFFFFFFFF</td></tr>
<tr><td>HMMWV_Avenger_Driver</td><td>0xD3AC574E</td><td>No</td><td>5391</td><td>0x8000A982</td><td>0x00013CD9</td></tr>
<tr><td>HMMWV_Driver</td><td>0xFEFE9D0B</td><td>No</td><td>5061</td><td>0x8000A3FA</td><td>0xFFFFFFFF</td></tr>
<tr><td>HouseSpawn</td><td>0x1115537C</td><td>No</td><td>43</td><td>0x80004512</td><td>0x0000BDD9</td></tr>
<tr><td>Huangfeng</td><td>0x9119EDA6</td><td>Yes</td><td>3021</td><td>0x80008B65</td><td>0x0000A9F7</td></tr>
<tr><td>Huangfeng (Driver)</td><td>0xF21B7ABD</td><td>Yes</td><td>3040</td><td>0x80008B78</td><td>0xFFFFFFFF</td></tr>
<tr><td>Huangfeng (Jammer)</td><td>0x87BD19FF</td><td>Yes</td><td>3324</td><td>0x80008FEF</td><td>0x0000A474</td></tr>
<tr><td>Huangfeng (Jammer) (Driver)</td><td>0x7A4B1D6A</td><td>Yes</td><td>3325</td><td>0x80008FF0</td><td>0x0000025B</td></tr>
<tr><td>HuangFeng_Driver</td><td>0xD1D13A1F</td><td>Yes</td><td>5101</td><td>0x8000A426</td><td>0x0000A478</td></tr>
<tr><td>Human</td><td>0xAD431BF0</td><td>No</td><td>29</td><td>0x8000437E</td><td>0x00004064</td></tr>
<tr><td>Human Heavy MG</td><td>0x988C5BAB</td><td>No</td><td>4075</td><td>0x80009AF5</td><td>0x00007EBF</td></tr>
<tr><td>Humvee (Cargo)</td><td>0x8EE207C2</td><td>Yes</td><td>2614</td><td>0x800085FD</td><td>0x000004C4</td></tr>
<tr><td>Hunting Pistol</td><td>0x3CD65BF3</td><td>No</td><td>1362</td><td>0x80006ECE</td><td>0x0000B873</td></tr>
<tr><td>Hunting Pistol Bullet</td><td>0x67672885</td><td>No</td><td>1361</td><td>0x80006ECD</td><td>0x00005490</td></tr>
<tr><td>HVT</td><td>0xA3BAD77D</td><td>No</td><td>5871</td><td>0x8000B012</td><td>0x00006A38</td></tr>
<tr><td>impact</td><td>0xA9FC5F87</td><td>No</td><td>2574</td><td>0x800085D1</td><td>0x000017C4</td></tr>
<tr><td>Impact (base)</td><td>0x08DD0349</td><td>No</td><td>2575</td><td>0x800085D2</td><td>0x0000B348</td></tr>
<tr><td>Impact (base) (Driver)</td><td>0x7E4223E4</td><td>No</td><td>4456</td><td>0x80009E22</td><td>0xFFFFFFFF</td></tr>
<tr><td>Impact (base) (Driver) (Civ Rich female)</td><td>0xFE035BD9</td><td>No</td><td>4457</td><td>0x80009E23</td><td>0x0000A6B5</td></tr>
<tr><td>Impact (base) (Driver) (Civ Rich male)</td><td>0x110889BC</td><td>No</td><td>4458</td><td>0x80009E24</td><td>0x00009E9F</td></tr>
<tr><td>Impact (sut)</td><td>0xE9386912</td><td>No</td><td>2576</td><td>0x800085D3</td><td>0x00012FDD</td></tr>
<tr><td>Impact (sut) (Driver)</td><td>0x0B42BFB9</td><td>No</td><td>4459</td><td>0x80009E25</td><td>0x00001FE3</td></tr>
<tr><td>Impact (sut) (Driver) (Civ Rich female)</td><td>0xE381D808</td><td>No</td><td>4460</td><td>0x80009E26</td><td>0x0000C717</td></tr>
<tr><td>Impact (sut) (Driver) (Civ Rich male)</td><td>0xA583A479</td><td>No</td><td>4461</td><td>0x80009E27</td><td>0x0000EF56</td></tr>
<tr><td>Impact_Driver</td><td>0xE1F525E4</td><td>No</td><td>5062</td><td>0x8000A3FB</td><td>0x000135A3</td></tr>
<tr><td>ImpactSUT_Driver</td><td>0xE8F330F6</td><td>No</td><td>5115</td><td>0x8000A459</td><td>0xFFFFFFFF</td></tr>
<tr><td>International (subfaction)</td><td>0x73CEE4D6</td><td>No</td><td>2140</td><td>0x800081A3</td><td>0x00002588</td></tr>
<tr><td>Intersection</td><td>0xB69CE2C6</td><td>No</td><td>259</td><td>0x80004DC8</td><td>0xFFFFFFFF</td></tr>
<tr><td>Jammer</td><td>0x960171AD</td><td>No</td><td>4782</td><td>0x8000A18B</td><td>0x000029A5</td></tr>
<tr><td>Jen</td><td>0xB06FC6E8</td><td>No</td><td>1780</td><td>0x800075E6</td><td>0x0000465F</td></tr>
<tr><td>JenChickensuit</td><td>0xC3FD0436</td><td>No</td><td>2308</td><td>0x800082C6</td><td>0x00008491</td></tr>
<tr><td>jenupgrade1</td><td>0xDD2CA3B1</td><td>No</td><td>4838</td><td>0x8000A1C4</td><td>0x0000A313</td></tr>
<tr><td>jenupgrade2</td><td>0x5B251B46</td><td>No</td><td>4839</td><td>0x8000A1C5</td><td>0x0000A64E</td></tr>
<tr><td>jenupgrade3</td><td>0x7D278F63</td><td>No</td><td>4840</td><td>0x8000A1C6</td><td>0x00008EB4</td></tr>
<tr><td>JenV2</td><td>0xBE9D5CB0</td><td>No</td><td>2301</td><td>0x800082BF</td><td>0x000087E4</td></tr>
<tr><td>JenV3</td><td>0x28A04225</td><td>No</td><td>2302</td><td>0x800082C0</td><td>0x0000C6BD</td></tr>
<tr><td>JenV4</td><td>0x1E8EE946</td><td>No</td><td>2303</td><td>0x800082C1</td><td>0xFFFFFFFF</td></tr>
<tr><td>JenV5</td><td>0x40915D63</td><td>No</td><td>3833</td><td>0x800097EE</td><td>0x00002709</td></tr>
<tr><td>Jetski (Base)</td><td>0x37257397</td><td>No</td><td>3328</td><td>0x80008FF3</td><td>0x0000CCA1</td></tr>
<tr><td>Jetski (Civ)</td><td>0xA4D1B14E</td><td>No</td><td>1080</td><td>0x80006A1D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Jetski (Civ) (Driver)</td><td>0x74C91EE5</td><td>No</td><td>1601</td><td>0x80007246</td><td>0xFFFFFFFF</td></tr>
<tr><td>Jetski (Civ) (Driver) (Civ Beach A Female)</td><td>0x119ED3DC</td><td>No</td><td>4652</td><td>0x80009FCE</td><td>0x00001D58</td></tr>
<tr><td>Jetski (Civ) (Driver) (Civ Beach B Female)</td><td>0x4C55C413</td><td>No</td><td>4653</td><td>0x80009FCF</td><td>0x00004F65</td></tr>
<tr><td>Jetski (Civ) (Driver) (Civ Beach C Female)</td><td>0x44B20C8A</td><td>No</td><td>4654</td><td>0x80009FD0</td><td>0x0000DE8A</td></tr>
<tr><td>Jetski (Civ) (Driver) (Civ Beach D Female)</td><td>0x97F32909</td><td>No</td><td>4655</td><td>0x80009FD1</td><td>0x00011350</td></tr>
<tr><td>Jetski (PR)</td><td>0x19AE3DA4</td><td>No</td><td>3326</td><td>0x80008FF1</td><td>0x0000BA29</td></tr>
<tr><td>Jetski (PR) (Driver)</td><td>0xC431A403</td><td>No</td><td>3327</td><td>0x80008FF2</td><td>0x00002A38</td></tr>
<tr><td>Jetski_Driver</td><td>0x8E0E2052</td><td>No</td><td>5084</td><td>0x8000A413</td><td>0xFFFFFFFF</td></tr>
<tr><td>JetTest</td><td>0xE9037B6E</td><td>No</td><td>984</td><td>0x80006618</td><td>0x00003EAD</td></tr>
<tr><td>jnilsson</td><td>0xBEA0F5B3</td><td>No</td><td>342</td><td>0x80004E2D</td><td>0x000020C5</td></tr>
<tr><td>Journalist A (Female)</td><td>0xA8C22B68</td><td>No</td><td>2145</td><td>0x800081A8</td><td>0xFFFFFFFF</td></tr>
<tr><td>Journalist A (Male)</td><td>0xE6AD9CD9</td><td>No</td><td>2143</td><td>0x800081A6</td><td>0x0000BC7E</td></tr>
<tr><td>Journalist B (Female)</td><td>0x07BE10B5</td><td>No</td><td>2146</td><td>0x800081A9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Journalist B (Male)</td><td>0x9DBF9648</td><td>No</td><td>2144</td><td>0x800081A7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Joyce Wheelchair</td><td>0x12A4F45F</td><td>No</td><td>3852</td><td>0x8000980A</td><td>0x00008135</td></tr>
<tr><td>Jungle Elite</td><td>0x6DE626BF</td><td>No</td><td>1315</td><td>0x80006E40</td><td>0xFFFFFFFF</td></tr>
<tr><td>JustPhoenix</td><td>0x1D1A6CC8</td><td>No</td><td>550</td><td>0x80005BA4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ka29b</td><td>0xE96A0E24</td><td>Yes</td><td>1804</td><td>0x8000769A</td><td>0x0000B44B</td></tr>
<tr><td>Ka29b (base)</td><td>0x9E26024C</td><td>Yes</td><td>2598</td><td>0x800085EC</td><td>0x0000A622</td></tr>
<tr><td>Ka29b (bomber)</td><td>0xCB2041FA</td><td>Yes</td><td>2599</td><td>0x800085ED</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ka29b (Delivery)</td><td>0xB25169AD</td><td>Yes</td><td>2227</td><td>0x80008200</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ka29b (Driver)</td><td>0xF3D88D83</td><td>Yes</td><td>2226</td><td>0x800081FF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ka29b (DriverGunner)</td><td>0x008776D4</td><td>Yes</td><td>3461</td><td>0x800092C3</td><td>0x00003201</td></tr>
<tr><td>Ka29b (Ewan)</td><td>0x92265E0A</td><td>Yes</td><td>5977</td><td>0x8000B365</td><td>0x00005387</td></tr>
<tr><td>Ka29b (Extraction)</td><td>0xFF914EF0</td><td>Yes</td><td>5834</td><td>0x8000AF8F</td><td>0x00011A08</td></tr>
<tr><td>Ka29b (Full)</td><td>0x0DB71EB0</td><td>Yes</td><td>3462</td><td>0x800092C4</td><td>0x0001233A</td></tr>
<tr><td>Ka29b (pursuit)</td><td>0x0BE78C3B</td><td>Yes</td><td>4908</td><td>0x8000A27F</td><td>0x0000E266</td></tr>
<tr><td>Kodiak Ridgeline (Driver) (Mechanic (male))</td><td>0x1988CF23</td><td>No</td><td>4593</td><td>0x80009F5B</td><td>0x0000DB27</td></tr>
<tr><td>L300</td><td>0x7B978FE6</td><td>No</td><td>1799</td><td>0x800075FD</td><td>0xFFFFFFFF</td></tr>
<tr><td>L300 (base)</td><td>0x1B061B9A</td><td>No</td><td>2607</td><td>0x800085F6</td><td>0xFFFFFFFF</td></tr>
<tr><td>L300 (Driver)</td><td>0x4D90717D</td><td>No</td><td>1816</td><td>0x800076A7</td><td>0x00007793</td></tr>
<tr><td>L300 (Driver) (Cartel)</td><td>0x64834415</td><td>No</td><td>4025</td><td>0x80009A0B</td><td>0x0000FB1E</td></tr>
<tr><td>L300 (Driver) (Civ Business B Male)</td><td>0x4AF6A2D7</td><td>No</td><td>4212</td><td>0x80009C6A</td><td>0x00008691</td></tr>
<tr><td>L300 (Driver) (Civ Business female)</td><td>0x7AE87B2C</td><td>No</td><td>4213</td><td>0x80009C6B</td><td>0x00007341</td></tr>
<tr><td>L300 (Driver) (Civ Business Male)</td><td>0x2C34B9BD</td><td>No</td><td>4211</td><td>0x80009C69</td><td>0x0000D289</td></tr>
<tr><td>L300 (Driver) (Civ Rich Female)</td><td>0x464A98CC</td><td>No</td><td>4223</td><td>0x80009C75</td><td>0xFFFFFFFF</td></tr>
<tr><td>L300 (Driver) (Civ Rich Male)</td><td>0xC4548BDD</td><td>No</td><td>4222</td><td>0x80009C74</td><td>0x0000011B</td></tr>
<tr><td>L300 (Driver) (OC)</td><td>0xC9A2D430</td><td>No</td><td>1818</td><td>0x800076A9</td><td>0xFFFFFFFF</td></tr>
<tr><td>L300 (Fling Backward)</td><td>0x3901E608</td><td>No</td><td>5569</td><td>0x8000AB6C</td><td>0xFFFFFFFF</td></tr>
<tr><td>L300 (Fling Forward)</td><td>0x14692BF8</td><td>No</td><td>5545</td><td>0x8000AB52</td><td>0x000071CB</td></tr>
<tr><td>L300 (Racing)</td><td>0x9B7F14BD</td><td>No</td><td>1809</td><td>0x800076A0</td><td>0x000008F6</td></tr>
<tr><td>L300 (Racing) (Driver)</td><td>0x2F755B48</td><td>No</td><td>1810</td><td>0x800076A1</td><td>0x000116E6</td></tr>
<tr><td>L300 (Racing) (Driver) (Civ Motorcycle male)</td><td>0x3B3AEE71</td><td>Yes</td><td>4290</td><td>0x80009CBD</td><td>0xFFFFFFFF</td></tr>
<tr><td>L300 (Racing) (Driver) (OC)</td><td>0xA0F74AA7</td><td>No</td><td>1819</td><td>0x800076AA</td><td>0xFFFFFFFF</td></tr>
<tr><td>L300 (Racing) (Long Hibernation)</td><td>0x40F244BF</td><td>No</td><td>5964</td><td>0x8000B2F8</td><td>0x0001285A</td></tr>
<tr><td>L300_Driver</td><td>0xB5E86E5F</td><td>No</td><td>5063</td><td>0x8000A3FC</td><td>0xFFFFFFFF</td></tr>
<tr><td>L300Racing_Driver</td><td>0x47FEB889</td><td>No</td><td>5103</td><td>0x8000A428</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ladder Seat (Bottom A)</td><td>0x7DDE7EAD</td><td>No</td><td>3421</td><td>0x80009192</td><td>0x00009445</td></tr>
<tr><td>Ladder Seat (Bottom B)</td><td>0xEEF2D044</td><td>No</td><td>3422</td><td>0x80009193</td><td>0x0000A528</td></tr>
<tr><td>Ladder Seat (Bottom C)</td><td>0x7B72778B</td><td>No</td><td>2186</td><td>0x800081D6</td><td>0x0000EF8E</td></tr>
<tr><td>Ladder Seat (Bottom D)</td><td>0x9BBBF222</td><td>No</td><td>2761</td><td>0x8000873F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ladder Seat (Bottom E)</td><td>0xA8DA33A9</td><td>No</td><td>4703</td><td>0x8000A009</td><td>0x0000750A</td></tr>
<tr><td>Ladder Seat (Bottom F)</td><td>0x3AB52AD0</td><td>No</td><td>5488</td><td>0x8000AAAC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ladder Seat (Bottom G)</td><td>0x57D38587</td><td>No</td><td>5489</td><td>0x8000AAAD</td><td>0x00009BF6</td></tr>
<tr><td>Ladder Seat (Bottom H)</td><td>0x798AA2CE</td><td>No</td><td>5490</td><td>0x8000AAAE</td><td>0x00009F16</td></tr>
<tr><td>Ladder Seat (Bottom)</td><td>0xE17233BE</td><td>No</td><td>3418</td><td>0x80009185</td><td>0x00001F18</td></tr>
<tr><td>Ladder Seat (No Enter Top A)</td><td>0x5D20D540</td><td>No</td><td>5002</td><td>0x8000A3B3</td><td>0x0000ECE0</td></tr>
<tr><td>Ladder Seat (No Enter Top B)</td><td>0xCBE541D9</td><td>No</td><td>5003</td><td>0x8000A3B4</td><td>0x0000F21D</td></tr>
<tr><td>Ladder Seat (No Enter Top C)</td><td>0x3E286612</td><td>No</td><td>5004</td><td>0x8000A3B5</td><td>0x00005EF3</td></tr>
<tr><td>Ladder Seat (No Enter Top D)</td><td>0xDDDE86BB</td><td>No</td><td>5279</td><td>0x8000A87B</td><td>0x000051ED</td></tr>
<tr><td>Ladder Seat (No Enter Top E)</td><td>0xD0C04534</td><td>No</td><td>5280</td><td>0x8000A87C</td><td>0x00007F38</td></tr>
<tr><td>Ladder Seat (Top A)</td><td>0x4D97BE21</td><td>No</td><td>3423</td><td>0x80009194</td><td>0x0000C312</td></tr>
<tr><td>Ladder Seat (Top B)</td><td>0xDF230368</td><td>No</td><td>3424</td><td>0x80009195</td><td>0x000035AA</td></tr>
<tr><td>Ladder Seat (Top C)</td><td>0x5BA2917F</td><td>No</td><td>2187</td><td>0x800081D7</td><td>0x00004859</td></tr>
<tr><td>Ladder Seat (Top D)</td><td>0xE4B708DE</td><td>No</td><td>2760</td><td>0x8000873E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ladder Seat (Top E)</td><td>0x829B0D45</td><td>No</td><td>4702</td><td>0x8000A008</td><td>0x00002661</td></tr>
<tr><td>Ladder Seat (Top F)</td><td>0x33AFC39C</td><td>No</td><td>5491</td><td>0x8000AAAF</td><td>0x000030A3</td></tr>
<tr><td>Ladder Seat (Top G)</td><td>0xC02F6AE3</td><td>No</td><td>5492</td><td>0x8000AAB0</td><td>0x00003995</td></tr>
<tr><td>Ladder Seat (Top H)</td><td>0x08258CB2</td><td>No</td><td>5493</td><td>0x8000AAB1</td><td>0x0000DFB5</td></tr>
<tr><td>Ladder Seat (Top)</td><td>0xDADEB192</td><td>No</td><td>3419</td><td>0x80009189</td><td>0x0000840C</td></tr>
<tr><td>Landing Zone</td><td>0xA979B1A8</td><td>No</td><td>1924</td><td>0x80007CD3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Landing Zone (player 1)</td><td>0xB00D853B</td><td>No</td><td>1925</td><td>0x80007CD4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Landing Zone (player 2)</td><td>0x74E43DF6</td><td>No</td><td>1926</td><td>0x80007CD5</td><td>0x0000170D</td></tr>
<tr><td>Laser Designator</td><td>0x317226F4</td><td>No</td><td>1920</td><td>0x80007CCE</td><td>0x00009F98</td></tr>
<tr><td>Laser Guided Bomb Projectile</td><td>0x936A4827</td><td>No</td><td>1922</td><td>0x80007CD0</td><td>0x0000F86C</td></tr>
<tr><td>LAV III (Base)</td><td>0x5C6FD13B</td><td>Yes</td><td>2503</td><td>0x80008539</td><td>0x00007BA6</td></tr>
<tr><td>Lav_Driver</td><td>0x187DB76F</td><td>Yes</td><td>5077</td><td>0x8000A40B</td><td>0x000112AE</td></tr>
<tr><td>LAVIII (25mm)</td><td>0xCDC13EBD</td><td>Yes</td><td>2551</td><td>0x800085B5</td><td>0xFFFFFFFF</td></tr>
<tr><td>LAVIII (25mm) (Driver)</td><td>0x53C33948</td><td>Yes</td><td>2865</td><td>0x80008912</td><td>0x000015AE</td></tr>
<tr><td>LAVIII (25mm) (Full)</td><td>0x06CFF94F</td><td>Yes</td><td>3236</td><td>0x80008F18</td><td>0xFFFFFFFF</td></tr>
<tr><td>LAVIII (AD)</td><td>0xA7F3F42B</td><td>Yes</td><td>2550</td><td>0x800085B4</td><td>0x00012CCC</td></tr>
<tr><td>LAVIII (AD) (Driver)</td><td>0x066154C6</td><td>Yes</td><td>2866</td><td>0x80008913</td><td>0x000139F5</td></tr>
<tr><td>LAVIII (AD) (Full)</td><td>0x2C0CB89D</td><td>Yes</td><td>3238</td><td>0x80008F1A</td><td>0xFFFFFFFF</td></tr>
<tr><td>LAVIII (AT)</td><td>0x965F28DB</td><td>Yes</td><td>2552</td><td>0x800085B6</td><td>0x00000DC4</td></tr>
<tr><td>LAVIII (AT) (Driver)</td><td>0xC36D6CB6</td><td>Yes</td><td>2867</td><td>0x80008914</td><td>0xFFFFFFFF</td></tr>
<tr><td>LAVIII (AT) (Full)</td><td>0x6EDBF08D</td><td>Yes</td><td>3239</td><td>0x80008F1B</td><td>0x0000CDA7</td></tr>
<tr><td>LAVIII (Cargo)</td><td>0x6334EA20</td><td>Yes</td><td>2616</td><td>0x800085FF</td><td>0x000031B4</td></tr>
<tr><td>LAVIII (MEWSS)</td><td>0x745AEC4D</td><td>Yes</td><td>2553</td><td>0x800085B7</td><td>0x000047BB</td></tr>
<tr><td>LAVIII (MEWSS) (Driver)</td><td>0xCB9229D8</td><td>Yes</td><td>2869</td><td>0x80008916</td><td>0xFFFFFFFF</td></tr>
<tr><td>LAVIII (MEWSS) (Full)</td><td>0xBD5C1BDF</td><td>Yes</td><td>3240</td><td>0x80008F1C</td><td>0xFFFFFFFF</td></tr>
<tr><td>LAVIII (MGS)</td><td>0x7E78EA99</td><td>Yes</td><td>2549</td><td>0x800085B3</td><td>0x0000DA08</td></tr>
<tr><td>LAVIII (MGS) (Driver)</td><td>0xB4561D74</td><td>Yes</td><td>2868</td><td>0x80008915</td><td>0x00006DA6</td></tr>
<tr><td>LAVIII (MGS) (Full)</td><td>0x6ADBCCB3</td><td>Yes</td><td>3241</td><td>0x80008F1D</td><td>0xFFFFFFFF</td></tr>
<tr><td>LAVIII (Minigun)</td><td>0x7AADF15B</td><td>Yes</td><td>2547</td><td>0x800085AD</td><td>0x00004BA1</td></tr>
<tr><td>LAVIII (Minigun) (Driver)</td><td>0x7495BE36</td><td>Yes</td><td>2506</td><td>0x8000853C</td><td>0xFFFFFFFF</td></tr>
<tr><td>LAVIII (Minigun) (DriverGunner)</td><td>0xE4EA490D</td><td>Yes</td><td>5158</td><td>0x8000A491</td><td>0x00001519</td></tr>
<tr><td>LAVIII (Minigun) (Full)</td><td>0x2AA8860D</td><td>Yes</td><td>3237</td><td>0x80008F19</td><td>0x0000C4D3</td></tr>
<tr><td>LCUR</td><td>0xCAE7696F</td><td>No</td><td>3211</td><td>0x80008EFD</td><td>0xFFFFFFFF</td></tr>
<tr><td>LCUR (Driver)</td><td>0x33D54F9A</td><td>No</td><td>3212</td><td>0x80008EFE</td><td>0x00011D50</td></tr>
<tr><td>LCUR (heavy)</td><td>0x7F1DA981</td><td>No</td><td>2611</td><td>0x800085FA</td><td>0x00002C41</td></tr>
<tr><td>LCUR (light)</td><td>0xDDBBEA8E</td><td>No</td><td>2618</td><td>0x80008601</td><td>0x0000C19C</td></tr>
<tr><td>LCUR (medium)</td><td>0xF2B75B03</td><td>No</td><td>2617</td><td>0x80008600</td><td>0x0000AC3A</td></tr>
<tr><td>LCUR_Driver</td><td>0x10F465DC</td><td>No</td><td>5085</td><td>0x8000A414</td><td>0x0000F11E</td></tr>
<tr><td>Lifestyle Job ArmageddonChair</td><td>0xD92ECD54</td><td>No</td><td>1927</td><td>0x80007D2C</td><td>0x0000C4AB</td></tr>
<tr><td>Lifestyle Job Entrance (Armageddon It Minigame)</td><td>0x510DC102</td><td>No</td><td>1928</td><td>0x80007D2D</td><td>0x00012764</td></tr>
<tr><td>Lifestyle Job Entrance (High Voltage Minigame)</td><td>0x8ED2E29D</td><td>No</td><td>2390</td><td>0x80008384</td><td>0xFFFFFFFF</td></tr>
<tr><td>Lifestyle Job HighVoltage</td><td>0xD08E52E1</td><td>No</td><td>2385</td><td>0x8000837F</td><td>0x00004F42</td></tr>
<tr><td>Lifestyle OilLif001 radio</td><td>0x80BAFCB9</td><td>No</td><td>2388</td><td>0x80008382</td><td>0x00007764</td></tr>
<tr><td>Lifestyle OilLif001 Table</td><td>0xE650ED3C</td><td>No</td><td>2389</td><td>0x80008383</td><td>0x00004631</td></tr>
<tr><td>Lifestyle Seat ArmageddonChair</td><td>0xCD29A57A</td><td>No</td><td>1929</td><td>0x80007D2E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Lifestyle Seat ArmageddonChair Player</td><td>0x1A579E61</td><td>No</td><td>2384</td><td>0x8000837E</td><td>0x0000E3C5</td></tr>
<tr><td>Lifestyle Seat HIghVoltage</td><td>0xD9EDB65F</td><td>No</td><td>2387</td><td>0x80008381</td><td>0xFFFFFFFF</td></tr>
<tr><td>Lifestyle Seat HighVoltagePlayer</td><td>0xAA02452C</td><td>No</td><td>2386</td><td>0x80008380</td><td>0x00013D0A</td></tr>
<tr><td>Light (Point)</td><td>0x5DF27220</td><td>No</td><td>2839</td><td>0x800087D8</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light (Point) small orange</td><td>0xB07F4765</td><td>No</td><td>2629</td><td>0x80008613</td><td>0x00008851</td></tr>
<tr><td>Light (Spot)</td><td>0xAF211D30</td><td>No</td><td>2840</td><td>0x800087D9</td><td>0x00013160</td></tr>
<tr><td>Light MG</td><td>0x69F71F2D</td><td>No</td><td>462</td><td>0x8000569E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light MG Bullet (GR)</td><td>0x903AB295</td><td>No</td><td>4113</td><td>0x80009B1C</td><td>0x00003BF9</td></tr>
<tr><td>Light MG Bullet (OC)</td><td>0x1FF01686</td><td>No</td><td>463</td><td>0x8000569F</td><td>0x0000D44C</td></tr>
<tr><td>Light_airstrike_carpetbomb</td><td>0x49A2462E</td><td>No</td><td>3440</td><td>0x800091F9</td><td>0x00012897</td></tr>
<tr><td>Light_airstrike_clusterbomb</td><td>0xBFE3091B</td><td>No</td><td>3439</td><td>0x800091F8</td><td>0x000073F0</td></tr>
<tr><td>Light_airstrike_cruisemissile_flash</td><td>0xE4E6C0BD</td><td>No</td><td>3435</td><td>0x800091F4</td><td>0x0000B80C</td></tr>
<tr><td>Light_airstrike_fuelairbomb_lrg</td><td>0x53C24771</td><td>No</td><td>3410</td><td>0x80009122</td><td>0x000023ED</td></tr>
<tr><td>Light_airstrike_fuelairbomb_lrg_flash</td><td>0xA4B8835E</td><td>No</td><td>3408</td><td>0x80009120</td><td>0x000006A2</td></tr>
<tr><td>Light_airstrike_fuelairbomb_sml</td><td>0x6D2ABCB4</td><td>No</td><td>3409</td><td>0x80009121</td><td>0x0000054F</td></tr>
<tr><td>Light_airstrike_moab_flash</td><td>0x4E739509</td><td>No</td><td>3427</td><td>0x800091EC</td><td>0x00006E90</td></tr>
<tr><td>Light_Animation_yellow_tiny (Flicker) 0x80008623</td><td>0x5A52191C</td><td>No</td><td>2641</td><td>0x80008623</td><td>0x00009120</td></tr>
<tr><td>Light_c4</td><td>0x30B7AB37</td><td>No</td><td>2007</td><td>0x8000803B</td><td>0x00003231</td></tr>
<tr><td>Light_contrail</td><td>0xF98BAAC6</td><td>No</td><td>3110</td><td>0x80008C08</td><td>0x0000A71F</td></tr>
<tr><td>Light_enormous_whiteblue 0x8000861f</td><td>0x95D441BD</td><td>No</td><td>2639</td><td>0x8000861F</td><td>0x0000B712</td></tr>
<tr><td>Light_explosion_huge</td><td>0x4208EF77</td><td>No</td><td>3196</td><td>0x80008E92</td><td>0x00009AF9</td></tr>
<tr><td>Light_explosion_huge_oil</td><td>0x68E64D76</td><td>No</td><td>3194</td><td>0x80008E90</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_explosion_medium</td><td>0x91E7AC07</td><td>No</td><td>3195</td><td>0x80008E91</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_explosion_medium_oil</td><td>0xDD241666</td><td>No</td><td>3199</td><td>0x80008E95</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_explosion_small</td><td>0x2CE3C94F</td><td>No</td><td>3197</td><td>0x80008E93</td><td>0x000068E3</td></tr>
<tr><td>Light_explosion_tiny</td><td>0x43F3DCF4</td><td>No</td><td>3198</td><td>0x80008E94</td><td>0x0000BD8A</td></tr>
<tr><td>Light_fire_blue</td><td>0x4DCE0DB1</td><td>No</td><td>4487</td><td>0x80009E4D</td><td>0x0000388B</td></tr>
<tr><td>Light_fire_carhood</td><td>0x7C969B5B</td><td>No</td><td>3109</td><td>0x80008C07</td><td>0x0000F71D</td></tr>
<tr><td>Light_fire_flare</td><td>0x79BB13EB</td><td>No</td><td>3727</td><td>0x8000956E</td><td>0x00004FAB</td></tr>
<tr><td>Light_fire_huge</td><td>0x4BC87F94</td><td>No</td><td>3403</td><td>0x80009119</td><td>0x00011C2B</td></tr>
<tr><td>Light_fire_lamp</td><td>0xB97A6E77</td><td>No</td><td>3378</td><td>0x800090FA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_fire_large</td><td>0x428234FE</td><td>No</td><td>2008</td><td>0x8000803C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_fire_medium</td><td>0x9AA8E5C0</td><td>No</td><td>3106</td><td>0x80008C04</td><td>0x00001AA6</td></tr>
<tr><td>Light_fire_small</td><td>0xFFB554A6</td><td>No</td><td>3107</td><td>0x80008C05</td><td>0x00005ABC</td></tr>
<tr><td>Light_fire_tiny</td><td>0xF9B5B2F7</td><td>No</td><td>3105</td><td>0x80008C03</td><td>0x0000B6F1</td></tr>
<tr><td>Light_grenade</td><td>0x4441861C</td><td>No</td><td>1998</td><td>0x80008032</td><td>0x00004F6C</td></tr>
<tr><td>Light_large_blue_cumana</td><td>0x48DF4684</td><td>No</td><td>2448</td><td>0x800084B4</td><td>0x000115A3</td></tr>
<tr><td>Light_large_red 0x8000863f</td><td>0x4FCD1260</td><td>No</td><td>2664</td><td>0x8000863F</td><td>0x0000EEC0</td></tr>
<tr><td>Light_large_whiteblue 0x80008619</td><td>0x446789D3</td><td>No</td><td>2633</td><td>0x80008619</td><td>0x0000A402</td></tr>
<tr><td>Light_large_whiteblue_bright 0x8000861e</td><td>0x899ED6B8</td><td>No</td><td>2638</td><td>0x8000861E</td><td>0x0000DAC3</td></tr>
<tr><td>Light_large_whiteblue_cumana</td><td>0x580CEB11</td><td>No</td><td>2447</td><td>0x800084B3</td><td>0x000049E1</td></tr>
<tr><td>Light_large_whiteblue_dim 0x8000862b</td><td>0x4A6E7484</td><td>No</td><td>2649</td><td>0x8000862B</td><td>0x0000927E</td></tr>
<tr><td>Light_large_whiteblue_lessbright</td><td>0x666C09C3</td><td>No</td><td>2670</td><td>0x80008646</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_large_yellow 0x80008618</td><td>0x031011CB</td><td>No</td><td>2632</td><td>0x80008618</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_large_yellow_bright 0x8000861c</td><td>0x201C00B9</td><td>No</td><td>2636</td><td>0x8000861C</td><td>0x00001452</td></tr>
<tr><td>Light_large_yellow_dim</td><td>0x476E7B49</td><td>No</td><td>2668</td><td>0x80008644</td><td>0x0000F6E1</td></tr>
<tr><td>Light_med_warm_lantern 0x80008638</td><td>0x731178D0</td><td>No</td><td>2658</td><td>0x80008638</td><td>0x00008A7F</td></tr>
<tr><td>Light_medium_blue 0x8000861d</td><td>0x43E392CB</td><td>No</td><td>2637</td><td>0x8000861D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_medium_blue_dark</td><td>0x5BCB3571</td><td>No</td><td>2666</td><td>0x80008642</td><td>0x00006800</td></tr>
<tr><td>Light_medium_green 0x8000863a</td><td>0xC06EFE77</td><td>No</td><td>2660</td><td>0x8000863A</td><td>0x00009A75</td></tr>
<tr><td>Light_medium_orange_bright 0x80008639</td><td>0x2C4EE52F</td><td>No</td><td>2659</td><td>0x80008639</td><td>0x000053E1</td></tr>
<tr><td>Light_medium_yellow 0x8000861a</td><td>0xCEC820E6</td><td>No</td><td>2634</td><td>0x8000861A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_medium_yellow_bright 0x8000863c</td><td>0xAFF7260F</td><td>No</td><td>2661</td><td>0x8000863C</td><td>0x0000AAF4</td></tr>
<tr><td>Light_muzzleflash</td><td>0x9D204719</td><td>No</td><td>1997</td><td>0x80008031</td><td>0x000094C7</td></tr>
<tr><td>Light_muzzleflash_AA</td><td>0xDDF53CE6</td><td>No</td><td>2003</td><td>0x80008037</td><td>0x00002CB5</td></tr>
<tr><td>Light_rpg</td><td>0x769E762F</td><td>No</td><td>3104</td><td>0x80008BFF</td><td>0x0000DAAF</td></tr>
<tr><td>Light_small_blue</td><td>0x9DDE617A</td><td>No</td><td>2631</td><td>0x80008615</td><td>0x0000C879</td></tr>
<tr><td>Light_small_blue_dim 0x80008636</td><td>0x8E4C0966</td><td>No</td><td>2656</td><td>0x80008636</td><td>0x00002514</td></tr>
<tr><td>Light_small_blue_intense 0x80008634</td><td>0x9ADBE028</td><td>No</td><td>2654</td><td>0x80008634</td><td>0x0001186D</td></tr>
<tr><td>Light_small_darkblue 0x80008640</td><td>0xA86337B4</td><td>No</td><td>2665</td><td>0x80008640</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_small_orange</td><td>0x192CEFA8</td><td>No</td><td>2663</td><td>0x8000863E</td><td>0x0000E540</td></tr>
<tr><td>Light_small_red 0x80008635</td><td>0x5911C7EF</td><td>No</td><td>2655</td><td>0x80008635</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_small_red_dim</td><td>0x700DE444</td><td>No</td><td>2667</td><td>0x80008643</td><td>0x0000B3DE</td></tr>
<tr><td>Light_small_white 0x80008633</td><td>0xBE090CAF</td><td>No</td><td>2653</td><td>0x80008633</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_small_white_dim</td><td>0x4A35C926</td><td>No</td><td>2671</td><td>0x80008647</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_small_yellow</td><td>0xD965157E</td><td>No</td><td>2630</td><td>0x80008614</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_small_yellow_dim 0x8000862c</td><td>0x1419DF50</td><td>No</td><td>2650</td><td>0x8000862C</td><td>0x0000B45F</td></tr>
<tr><td>Light_solano_ahj</td><td>0x4B266A46</td><td>No</td><td>4414</td><td>0x80009DF3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Light_spot_enormous_yellow 0x80008637</td><td>0x1931F7EE</td><td>No</td><td>2657</td><td>0x80008637</td><td>0x00007EF7</td></tr>
<tr><td>Light_spot_large_white 0x8000863d</td><td>0x9A30F32B</td><td>No</td><td>2662</td><td>0x8000863D</td><td>0x00012E9E</td></tr>
<tr><td>Light_spot_large_yellow 0x80008627</td><td>0x29C86AD8</td><td>No</td><td>2645</td><td>0x80008627</td><td>0x00000E3E</td></tr>
<tr><td>Light_spot_medium_blue_cumana</td><td>0xB7E51F4B</td><td>No</td><td>2450</td><td>0x800084B6</td><td>0x00011601</td></tr>
<tr><td>Light_spot_medium_yellow 0x8000862e</td><td>0xC5F66F28</td><td>No</td><td>2652</td><td>0x8000862E</td><td>0x00011BB0</td></tr>
<tr><td>Light_spot_medium_yellow_cumana</td><td>0x66D3DC9B</td><td>No</td><td>2449</td><td>0x800084B5</td><td>0x00010581</td></tr>
<tr><td>Light_spot_tiny_white 0x80008629</td><td>0x1EDD0CDA</td><td>No</td><td>2647</td><td>0x80008629</td><td>0x0000D177</td></tr>
<tr><td>Light_spot_tiny_yellow 0x80008625</td><td>0x42B1C513</td><td>No</td><td>2643</td><td>0x80008625</td><td>0x000100FE</td></tr>
<tr><td>Light_tiny_blue 0x80008624</td><td>0xF6A261B5</td><td>No</td><td>2642</td><td>0x80008624</td><td>0x00010037</td></tr>
<tr><td>Light_tiny_warm_lantern 0x8000862a</td><td>0x0FD8221E</td><td>No</td><td>2648</td><td>0x8000862A</td><td>0x000065A5</td></tr>
<tr><td>Light_tiny_white_weak 0x80008628</td><td>0xD3C1A1B3</td><td>No</td><td>2646</td><td>0x80008628</td><td>0x00001C5C</td></tr>
<tr><td>Light_tiny_yellow 0x8000861b</td><td>0xB2D6402A</td><td>No</td><td>2635</td><td>0x8000861B</td><td>0xFFFFFFFF</td></tr>
<tr><td>LightAnimation (Flicker)</td><td>0x074ABA2A</td><td>No</td><td>2843</td><td>0x800087DE</td><td>0xFFFFFFFF</td></tr>
<tr><td>LightAnimation (Pulse)</td><td>0xB11604F3</td><td>No</td><td>2841</td><td>0x800087DC</td><td>0xFFFFFFFF</td></tr>
<tr><td>LightAnimation (Strobe)</td><td>0x55C70F11</td><td>No</td><td>2842</td><td>0x800087DD</td><td>0xFFFFFFFF</td></tr>
<tr><td>Lights</td><td>0xE1A18DDA</td><td>No</td><td>1996</td><td>0x80008030</td><td>0x00008784</td></tr>
<tr><td>Listening Post</td><td>0x5023CB6E</td><td>No</td><td>3178</td><td>0x80008E4F</td><td>0xFFFFFFFF</td></tr>
<tr><td>LivingWorld Objects</td><td>0x8955971E</td><td>No</td><td>103</td><td>0x80004C10</td><td>0xFFFFFFFF</td></tr>
<tr><td>LivingWorldTestParkZone</td><td>0x6F79C4D4</td><td>No</td><td>810</td><td>0x80006247</td><td>0xFFFFFFFF</td></tr>
<tr><td>LivingWorldTestZone</td><td>0x05D8E01C</td><td>No</td><td>811</td><td>0x80006248</td><td>0xFFFFFFFF</td></tr>
<tr><td>location</td><td>0x5FB9E764</td><td>No</td><td>386</td><td>0x80005422</td><td>0x0000EAB4</td></tr>
<tr><td>Lowresterrain</td><td>0x1602815C</td><td>No</td><td>2049</td><td>0x800080E4</td><td>0x00007F61</td></tr>
<tr><td>LowRoad</td><td>0x2AA7C187</td><td>No</td><td>99</td><td>0x80004C00</td><td>0xFFFFFFFF</td></tr>
<tr><td>LW_Entrance_FrontCenter</td><td>0x6ADB51C8</td><td>No</td><td>722</td><td>0x8000618D</td><td>0x00011625</td></tr>
<tr><td>LW_Seat_LR_L</td><td>0xD1DFE43A</td><td>No</td><td>118</td><td>0x80004C23</td><td>0x00001E07</td></tr>
<tr><td>LW_Seat_LR_L (Ragdoll)</td><td>0xD2D16A00</td><td>No</td><td>5747</td><td>0x8000AD71</td><td>0x0000540D</td></tr>
<tr><td>LW_Seat_LR_R</td><td>0x319FD404</td><td>No</td><td>119</td><td>0x80004C24</td><td>0x00006679</td></tr>
<tr><td>LW_Seat_LR_R (Ragdoll)</td><td>0x4D312516</td><td>No</td><td>5748</td><td>0x8000AD72</td><td>0x0000D00A</td></tr>
<tr><td>LWEntrance_Single</td><td>0x9846E607</td><td>No</td><td>4405</td><td>0x80009DD2</td><td>0x00008857</td></tr>
<tr><td>LWEntrance_Single (MercsBar)</td><td>0xFC8F5C5B</td><td>No</td><td>4406</td><td>0x80009DD3</td><td>0xFFFFFFFF</td></tr>
<tr><td>LWRoads</td><td>0x3FD5F28B</td><td>No</td><td>560</td><td>0x80005BE7</td><td>0x00011C7E</td></tr>
<tr><td>LWSeat_Single</td><td>0xB1E57184</td><td>No</td><td>117</td><td>0x80004C22</td><td>0x00000C82</td></tr>
<tr><td>LWSeat_Single (MercsBar)</td><td>0xE0B3F3AA</td><td>No</td><td>4404</td><td>0x80009DD1</td><td>0xFFFFFFFF</td></tr>
<tr><td>LWSeat_Single (No Hijack)</td><td>0x5D1CC178</td><td>No</td><td>3802</td><td>0x800097BF</td><td>0xFFFFFFFF</td></tr>
<tr><td>LWSeat_Single (No Hijack) (Ragdoll)</td><td>0xEF730982</td><td>No</td><td>5749</td><td>0x8000AD73</td><td>0x0000AB17</td></tr>
<tr><td>LWSeat_Single (Ragdoll)</td><td>0xABD76E96</td><td>No</td><td>5750</td><td>0x8000AD74</td><td>0x0000E292</td></tr>
<tr><td>LWSeats</td><td>0x12DDCF58</td><td>No</td><td>116</td><td>0x80004C21</td><td>0x00000E86</td></tr>
<tr><td>M113 (Base Passenger)</td><td>0xDD0FBB45</td><td>Yes</td><td>1784</td><td>0x800075EA</td><td>0xFFFFFFFF</td></tr>
<tr><td>M113 (Base)</td><td>0xAB5BAEF9</td><td>Yes</td><td>4256</td><td>0x80009C9B</td><td>0x000033DE</td></tr>
<tr><td>M113 (GR)</td><td>0xCE5E8D35</td><td>Yes</td><td>2206</td><td>0x800081EB</td><td>0xFFFFFFFF</td></tr>
<tr><td>M113 (GR) (Driver)</td><td>0x48FB03C0</td><td>Yes</td><td>2216</td><td>0x800081F5</td><td>0x00002C0C</td></tr>
<tr><td>M113 (GR) (DriverGunner)</td><td>0x9AF7067F</td><td>Yes</td><td>3352</td><td>0x8000900C</td><td>0x000121B3</td></tr>
<tr><td>M113 (GR) (Full)</td><td>0xD7604AD7</td><td>Yes</td><td>2217</td><td>0x800081F6</td><td>0xFFFFFFFF</td></tr>
<tr><td>M113 (VZ)</td><td>0xC9900D64</td><td>Yes</td><td>2207</td><td>0x800081EC</td><td>0xFFFFFFFF</td></tr>
<tr><td>M113 (VZ) (Driver)</td><td>0xEB80EF43</td><td>Yes</td><td>2214</td><td>0x800081F3</td><td>0x00001333</td></tr>
<tr><td>M113 (VZ) (DriverGunner)</td><td>0xDA41DF94</td><td>Yes</td><td>3353</td><td>0x8000900D</td><td>0x00007E39</td></tr>
<tr><td>M113 (VZ) (Full RPG)</td><td>0xA81BE3EB</td><td>Yes</td><td>2808</td><td>0x8000876E</td><td>0xFFFFFFFF</td></tr>
<tr><td>M113 (VZ) (Full)</td><td>0x88D24F70</td><td>Yes</td><td>2215</td><td>0x800081F4</td><td>0x00008478</td></tr>
<tr><td>M113 AA (base)</td><td>0x5266EAA9</td><td>Yes</td><td>2208</td><td>0x800081ED</td><td>0xFFFFFFFF</td></tr>
<tr><td>M113 AA (GR)</td><td>0xEBD1DEE5</td><td>Yes</td><td>1075</td><td>0x80006A0C</td><td>0x00003278</td></tr>
<tr><td>M113 AA (GR) (Driver)</td><td>0x973B8270</td><td>Yes</td><td>2210</td><td>0x800081EF</td><td>0x0000C5E6</td></tr>
<tr><td>M113 AA (GR) (DriverGunner)</td><td>0xF8B5BD2F</td><td>Yes</td><td>5925</td><td>0x8000B1CF</td><td>0xFFFFFFFF</td></tr>
<tr><td>M113 AA (GR) (Full)</td><td>0x180BD007</td><td>Yes</td><td>2211</td><td>0x800081F0</td><td>0x00013641</td></tr>
<tr><td>M113 AA (VZ)</td><td>0x26D6AE34</td><td>Yes</td><td>2209</td><td>0x800081EE</td><td>0x000000B2</td></tr>
<tr><td>M113 AA (VZ) (Driver)</td><td>0x50F46313</td><td>Yes</td><td>2212</td><td>0x800081F1</td><td>0xFFFFFFFF</td></tr>
<tr><td>M113 AA (VZ) (Full)</td><td>0xB1BC8DC0</td><td>Yes</td><td>2213</td><td>0x800081F2</td><td>0x0000B019</td></tr>
<tr><td>M113 Jammer</td><td>0xC3B398ED</td><td>Yes</td><td>2282</td><td>0x80008246</td><td>0x00007770</td></tr>
<tr><td>M113 Jammer (VZ)</td><td>0x5F15847E</td><td>Yes</td><td>2283</td><td>0x80008247</td><td>0x00002565</td></tr>
<tr><td>M113 Jammer (VZ) (Driver)</td><td>0x63E36415</td><td>Yes</td><td>2284</td><td>0x80008248</td><td>0x0000A8E1</td></tr>
<tr><td>M113 Transport</td><td>0x127C2568</td><td>Yes</td><td>2205</td><td>0x800081EA</td><td>0x00013149</td></tr>
<tr><td>M113FullSpawnList</td><td>0xF15F844D</td><td>Yes</td><td>2404</td><td>0x800083F2</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 (Base)</td><td>0x55639ADF</td><td>Yes</td><td>1083</td><td>0x80006A23</td><td>0x000001AA</td></tr>
<tr><td>M151 (MG)</td><td>0x58918BDE</td><td>Yes</td><td>1185</td><td>0x80006C98</td><td>0x0000E024</td></tr>
<tr><td>M151 (MG) (GR)</td><td>0xA72B34B2</td><td>Yes</td><td>1182</td><td>0x80006C95</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 (MG) (GR) (Driver)</td><td>0x288238D9</td><td>Yes</td><td>1825</td><td>0x800076B0</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 (MG) (GR) (DriverGunner)</td><td>0xE6A2F38A</td><td>Yes</td><td>5160</td><td>0x8000A494</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 (MG) (VZ) (Driver)</td><td>0xC26E9EFE</td><td>Yes</td><td>1826</td><td>0x800076B1</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 .50Cal (GR) (Full)</td><td>0x4F814028</td><td>Yes</td><td>1829</td><td>0x800076B4</td><td>0x0000A1C3</td></tr>
<tr><td>M151 .50Cal (VZ)</td><td>0xEEA87FED</td><td>Yes</td><td>1183</td><td>0x80006C96</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 .50Cal (VZ) (DriverGunner)</td><td>0x72A4CB37</td><td>Yes</td><td>4877</td><td>0x8000A25B</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 .50Cal (VZ) (Full)</td><td>0x888F587F</td><td>Yes</td><td>1830</td><td>0x800076B5</td><td>0x00010818</td></tr>
<tr><td>M151 Softtop</td><td>0x7260D03C</td><td>Yes</td><td>1184</td><td>0x80006C97</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 Softtop (GR)</td><td>0x4411809C</td><td>Yes</td><td>1180</td><td>0x80006C93</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 Softtop (GR) (Driver)</td><td>0x5871785B</td><td>Yes</td><td>1827</td><td>0x800076B2</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 Softtop (GR) (Full)</td><td>0xF37B0A58</td><td>Yes</td><td>1832</td><td>0x800076B7</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151 Softtop (VZ)</td><td>0xD68A30FD</td><td>Yes</td><td>1181</td><td>0x80006C94</td><td>0x0000160E</td></tr>
<tr><td>M151 Softtop (VZ) (Driver)</td><td>0x23713C08</td><td>Yes</td><td>1828</td><td>0x800076B3</td><td>0x00002F52</td></tr>
<tr><td>M151 Softtop (VZ) (Full)</td><td>0x25FE790F</td><td>Yes</td><td>1831</td><td>0x800076B6</td><td>0xFFFFFFFF</td></tr>
<tr><td>M151_Driver</td><td>0x9F163EDA</td><td>Yes</td><td>5069</td><td>0x8000A402</td><td>0x00011422</td></tr>
<tr><td>M151_Ruin</td><td>0x94F06992</td><td>Yes</td><td>6124</td><td>0x900001F6</td><td>0x00010266</td></tr>
<tr><td>M163 Driver Seat</td><td>0xB348901B</td><td>No</td><td>1076</td><td>0x80006A0D</td><td>0xFFFFFFFF</td></tr>
<tr><td>M1A2</td><td>0x0118204A</td><td>Yes</td><td>1686</td><td>0x800074C0</td><td>0x00002AEA</td></tr>
<tr><td>M1A2 (Cargo)</td><td>0x21D37A93</td><td>Yes</td><td>2613</td><td>0x800085FC</td><td>0x0000066C</td></tr>
<tr><td>M1A2 (Driver)</td><td>0x5415F131</td><td>Yes</td><td>1687</td><td>0x800074C1</td><td>0x00012758</td></tr>
<tr><td>M1A2 (Full)</td><td>0x48606406</td><td>Yes</td><td>1688</td><td>0x800074C2</td><td>0x00012D9B</td></tr>
<tr><td>M2A3</td><td>0xAE0761D0</td><td>Yes</td><td>1690</td><td>0x800074C4</td><td>0x00001E15</td></tr>
<tr><td>M2A3 (Base)</td><td>0x7B720A28</td><td>Yes</td><td>1689</td><td>0x800074C3</td><td>0xFFFFFFFF</td></tr>
<tr><td>M2A3 (Driver)</td><td>0x1DA3756F</td><td>Yes</td><td>1692</td><td>0x800074C6</td><td>0x0000B9DB</td></tr>
<tr><td>M35 (AA)</td><td>0xCF00E219</td><td>Yes</td><td>2893</td><td>0x8000892E</td><td>0x00001947</td></tr>
<tr><td>M35 (AA) (GR)</td><td>0x7E68250B</td><td>Yes</td><td>2894</td><td>0x8000892F</td><td>0x00008B4E</td></tr>
<tr><td>M35 (AA) (GR) (Driver)</td><td>0xB29EA7A6</td><td>Yes</td><td>2896</td><td>0x80008931</td><td>0x00006B3A</td></tr>
<tr><td>M35 (AA) (GR) (Full)</td><td>0x44AEB37D</td><td>Yes</td><td>2897</td><td>0x80008932</td><td>0xFFFFFFFF</td></tr>
<tr><td>M35 (AA) (VZ)</td><td>0x22A3CAEA</td><td>Yes</td><td>2895</td><td>0x80008930</td><td>0x0000DD58</td></tr>
<tr><td>M35 (AA) (VZ) (Driver)</td><td>0x855352D1</td><td>Yes</td><td>2898</td><td>0x80008933</td><td>0x00008936</td></tr>
<tr><td>M35 (AA) (VZ) (Full)</td><td>0xD34462A6</td><td>Yes</td><td>2899</td><td>0x80008934</td><td>0x00005BCB</td></tr>
<tr><td>M35 (Cargo)</td><td>0x0B3E0EEB</td><td>Yes</td><td>2873</td><td>0x8000891A</td><td>0x00008750</td></tr>
<tr><td>M35 (Cargo) (GR)</td><td>0x15A6E679</td><td>Yes</td><td>2884</td><td>0x80008925</td><td>0x000116CB</td></tr>
<tr><td>M35 (Cargo) (GR) (Driver)</td><td>0x00FB4CD4</td><td>Yes</td><td>2885</td><td>0x80008926</td><td>0x000121D7</td></tr>
<tr><td>M35 (Cargo) (GR) (Full)</td><td>0xA4F49093</td><td>Yes</td><td>2886</td><td>0x80008927</td><td>0xFFFFFFFF</td></tr>
<tr><td>M35 (Cargo) (VZ)</td><td>0x69BA71A8</td><td>Yes</td><td>2555</td><td>0x800085B9</td><td>0x00006479</td></tr>
<tr><td>M35 (Cargo) (VZ) (Driver)</td><td>0x1821E287</td><td>Yes</td><td>2874</td><td>0x8000891B</td><td>0x0000E380</td></tr>
<tr><td>M35 (Cargo) (VZ) (Full RPG)</td><td>0x0735588F</td><td>Yes</td><td>2807</td><td>0x8000876D</td><td>0x000043DD</td></tr>
<tr><td>M35 (Cargo) (VZ) (Full)</td><td>0xE0D2C7CC</td><td>Yes</td><td>2875</td><td>0x8000891C</td><td>0x00001D52</td></tr>
<tr><td>M35 (Fuel)</td><td>0x617EEDAB</td><td>Yes</td><td>3487</td><td>0x800092DF</td><td>0x0000A1B6</td></tr>
<tr><td>M35 (Fuel) (GR)</td><td>0xF351EFB9</td><td>Yes</td><td>3488</td><td>0x800092E0</td><td>0x00011BC6</td></tr>
<tr><td>M35 (Fuel) (GR) (Driver)</td><td>0xED202294</td><td>Yes</td><td>3605</td><td>0x80009451</td><td>0x0000FFA4</td></tr>
<tr><td>M35 (Fuel) (GR) (Full)</td><td>0x7A605253</td><td>Yes</td><td>3606</td><td>0x80009452</td><td>0x0000A33C</td></tr>
<tr><td>M35 (Fuel) (VZ)</td><td>0x60B22FE8</td><td>Yes</td><td>3489</td><td>0x800092E1</td><td>0x00013C50</td></tr>
<tr><td>M35 (Fuel) (VZ) (Driver)</td><td>0x15DC6847</td><td>Yes</td><td>3608</td><td>0x80009454</td><td>0xFFFFFFFF</td></tr>
<tr><td>M35 (Fuel) (VZ) (Full)</td><td>0xEB7A638C</td><td>Yes</td><td>3607</td><td>0x80009453</td><td>0x00013B8B</td></tr>
<tr><td>M35 (Guntruck)</td><td>0x5F128AE6</td><td>Yes</td><td>3049</td><td>0x80008B82</td><td>0x00009D0D</td></tr>
<tr><td>M35 (Guntruck) (GR)</td><td>0x1EB74FCA</td><td>Yes</td><td>3050</td><td>0x80008B83</td><td>0xFFFFFFFF</td></tr>
<tr><td>M35 (Guntruck) (GR) (Driver)</td><td>0xB1D007B1</td><td>Yes</td><td>3054</td><td>0x80008B87</td><td>0x00002F45</td></tr>
<tr><td>M35 (Guntruck) (GR) (Full)</td><td>0x4E05F686</td><td>Yes</td><td>3678</td><td>0x8000952D</td><td>0xFFFFFFFF</td></tr>
<tr><td>M35 (Guntruck) (VZ)</td><td>0x7BE5F40B</td><td>Yes</td><td>3051</td><td>0x80008B84</td><td>0x0000F023</td></tr>
<tr><td>M35 (Guntruck) (VZ) (Driver)</td><td>0xE44A24A6</td><td>Yes</td><td>3055</td><td>0x80008B88</td><td>0x00002E47</td></tr>
<tr><td>M35 (Guntruck) (VZ) (Full)</td><td>0xC06CA87D</td><td>Yes</td><td>3677</td><td>0x8000952C</td><td>0xFFFFFFFF</td></tr>
<tr><td>M35 (Guntruck) (VZ) (SemiFull)</td><td>0xE49CA0B7</td><td>Yes</td><td>5157</td><td>0x8000A490</td><td>0x00007D86</td></tr>
<tr><td>M35 Truck (base)</td><td>0x8FC60AB1</td><td>Yes</td><td>2554</td><td>0x800085B8</td><td>0x00004951</td></tr>
<tr><td>M35_Driver</td><td>0xBE2248D3</td><td>Yes</td><td>5064</td><td>0x8000A3FD</td><td>0xFFFFFFFF</td></tr>
<tr><td>M35_Ruin</td><td>0xE32FBDBB</td><td>Yes</td><td>6125</td><td>0x900001F7</td><td>0x0001152C</td></tr>
<tr><td>M35VZGuntruckFull_Spawnlist</td><td>0x808CADD6</td><td>Yes</td><td>5544</td><td>0x8000AB51</td><td>0xFFFFFFFF</td></tr>
<tr><td>M551</td><td>0x43C6A9CD</td><td>Yes</td><td>1756</td><td>0x800075CE</td><td>0x00014066</td></tr>
<tr><td>M551 (Driver)</td><td>0x48F70A58</td><td>Yes</td><td>1757</td><td>0x800075CF</td><td>0x00002613</td></tr>
<tr><td>M551 (Full)</td><td>0xBF98E85F</td><td>Yes</td><td>1758</td><td>0x800075D0</td><td>0x0000BF7E</td></tr>
<tr><td>M6 - DO NOT USE</td><td>0x67477F92</td><td>No</td><td>1691</td><td>0x800074C5</td><td>0x00001835</td></tr>
<tr><td>Machine Pistol</td><td>0xAB74E231</td><td>No</td><td>1125</td><td>0x80006B53</td><td>0xFFFFFFFF</td></tr>
<tr><td>Machine Pistol (PP2000)</td><td>0x8FDEFF14</td><td>No</td><td>1576</td><td>0x80007213</td><td>0xFFFFFFFF</td></tr>
<tr><td>Machine Pistol (TMP)</td><td>0x462810E1</td><td>No</td><td>1129</td><td>0x80006B57</td><td>0xFFFFFFFF</td></tr>
<tr><td>Machine Pistol (Uzi)</td><td>0x6B018DF6</td><td>No</td><td>1131</td><td>0x80006B59</td><td>0x00004980</td></tr>
<tr><td>Machine Pistol (Window Spawner)</td><td>0x9A28F0B6</td><td>No</td><td>5905</td><td>0x8000B038</td><td>0xFFFFFFFF</td></tr>
<tr><td>Machine Pistol Bullet</td><td>0x43F1553B</td><td>No</td><td>1127</td><td>0x80006B55</td><td>0xFFFFFFFF</td></tr>
<tr><td>Magazine (Assault Rifle)</td><td>0xA5BC19DF</td><td>Yes</td><td>2414</td><td>0x8000844E</td><td>0x00009B52</td></tr>
<tr><td>Magazine (RPG)</td><td>0xC6709D09</td><td>Yes</td><td>1912</td><td>0x800079FF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Magazines</td><td>0x2DE2E5AE</td><td>Yes</td><td>1911</td><td>0x800079FE</td><td>0xFFFFFFFF</td></tr>
<tr><td>MagicBarrack</td><td>0xF199D264</td><td>No</td><td>3088</td><td>0x80008BAC</td><td>0x0000E753</td></tr>
<tr><td>MagicSeat</td><td>0x5EEA3C95</td><td>No</td><td>3089</td><td>0x80008BAD</td><td>0xFFFFFFFF</td></tr>
<tr><td>MagicTurret</td><td>0x5B1E2C94</td><td>No</td><td>3090</td><td>0x80008BAE</td><td>0x00005A27</td></tr>
<tr><td>Mark (Civ)</td><td>0xDAA49C09</td><td>No</td><td>2270</td><td>0x80008239</td><td>0x00011BF1</td></tr>
<tr><td>Mark (Civ) (Driver)</td><td>0x17386824</td><td>No</td><td>2272</td><td>0x8000823B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mark (Civ) (Driver) (Mechanic male)</td><td>0xFD8DD31E</td><td>No</td><td>4426</td><td>0x80009E04</td><td>0x0000983E</td></tr>
<tr><td>Mark (Civ) (Full)</td><td>0xD2B2BCE3</td><td>No</td><td>2273</td><td>0x8000823C</td><td>0x00000CE6</td></tr>
<tr><td>Mark (PR)</td><td>0x746B03ED</td><td>No</td><td>2271</td><td>0x8000823A</td><td>0x00011108</td></tr>
<tr><td>Mark (PR) (Driver)</td><td>0x0FA2ECF8</td><td>No</td><td>2274</td><td>0x8000823D</td><td>0x00005D63</td></tr>
<tr><td>Mark (PR) (Full)</td><td>0x69B6C47F</td><td>No</td><td>2275</td><td>0x8000823E</td><td>0x00008D6D</td></tr>
<tr><td>Mark_Driver</td><td>0x75D25B87</td><td>No</td><td>5092</td><td>0x8000A41B</td><td>0xFFFFFFFF</td></tr>
<tr><td>MarkV</td><td>0xD621AED8</td><td>No</td><td>1761</td><td>0x800075D3</td><td>0xFFFFFFFF</td></tr>
<tr><td>MarkV (Driver)</td><td>0x0A0BBB37</td><td>No</td><td>1762</td><td>0x800075D4</td><td>0x0000C283</td></tr>
<tr><td>MarkV (Full)</td><td>0x2A83887C</td><td>No</td><td>1763</td><td>0x800075D5</td><td>0x00010BC1</td></tr>
<tr><td>MarkV (Full) (Allied)</td><td>0xCD4136EA</td><td>No</td><td>4362</td><td>0x80009D35</td><td>0x0000167D</td></tr>
<tr><td>MarkV (Half) (Allied)</td><td>0x8DA232F6</td><td>No</td><td>5955</td><td>0x8000B1F3</td><td>0x00009BEF</td></tr>
<tr><td>MarkV_Driver</td><td>0x05795405</td><td>No</td><td>5086</td><td>0x8000A415</td><td>0x00007388</td></tr>
<tr><td>Matches Projectile</td><td>0xD70A8661</td><td>No</td><td>710</td><td>0x80005FD6</td><td>0x00012BD1</td></tr>
<tr><td>Material Test Asset</td><td>0x304B38AA</td><td>No</td><td>1586</td><td>0x80007224</td><td>0x0000AB78</td></tr>
<tr><td>Mattias</td><td>0x030E6C38</td><td>No</td><td>1</td><td>0x80000003</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mattias Chopper</td><td>0x1ECD5E19</td><td>Yes</td><td>3244</td><td>0x80008F21</td><td>0x0001054B</td></tr>
<tr><td>MattiasChickensuit</td><td>0x98507A86</td><td>No</td><td>2300</td><td>0x800082BE</td><td>0x00003D1F</td></tr>
<tr><td>mattiasupgrade1</td><td>0x7D2EEA01</td><td>No</td><td>4832</td><td>0x8000A1BE</td><td>0x0000C621</td></tr>
<tr><td>mattiasupgrade2</td><td>0xFB276196</td><td>No</td><td>4833</td><td>0x8000A1BF</td><td>0x000049B4</td></tr>
<tr><td>mattiasupgrade3</td><td>0x5D2A3A73</td><td>No</td><td>4834</td><td>0x8000A1C0</td><td>0x00013F38</td></tr>
<tr><td>MattiasV2</td><td>0x043D0100</td><td>No</td><td>2298</td><td>0x800082BC</td><td>0x00007EBA</td></tr>
<tr><td>MattiasV3</td><td>0x2E3F81B5</td><td>No</td><td>2299</td><td>0x800082BD</td><td>0x000037A2</td></tr>
<tr><td>MD-500</td><td>0xC9B8D3D0</td><td>No</td><td>854</td><td>0x800063A6</td><td>0x0000C874</td></tr>
<tr><td>Mechanic (male)</td><td>0xA3A8AC09</td><td>No</td><td>2138</td><td>0x800081A1</td><td>0xFFFFFFFF</td></tr>
<tr><td>merida_wallchurchshort</td><td>0x5F67A1D9</td><td>No</td><td>48</td><td>0x80004578</td><td>0xFFFFFFFF</td></tr>
<tr><td>merida_wallcommercialshorta</td><td>0x6F04F6AD</td><td>No</td><td>47</td><td>0x80004577</td><td>0x000118C8</td></tr>
<tr><td>MeridaTest Allies</td><td>0x8D9D02A1</td><td>No</td><td>2515</td><td>0x8000854A</td><td>0xFFFFFFFF</td></tr>
<tr><td>MeridaTest VZ</td><td>0xF7A3427F</td><td>No</td><td>2514</td><td>0x80008549</td><td>0xFFFFFFFF</td></tr>
<tr><td>MH53J</td><td>0x83143980</td><td>Yes</td><td>3463</td><td>0x800092C5</td><td>0x00002AEE</td></tr>
<tr><td>MH53J (Driver)</td><td>0x4B5CA29F</td><td>Yes</td><td>3464</td><td>0x800092C6</td><td>0x0000B0B4</td></tr>
<tr><td>MH53J (DriverGunner)</td><td>0x859F20B8</td><td>Yes</td><td>3626</td><td>0x80009466</td><td>0xFFFFFFFF</td></tr>
<tr><td>MH53J (Ewan)</td><td>0x70719716</td><td>Yes</td><td>5982</td><td>0x8000B36A</td><td>0x00008B80</td></tr>
<tr><td>MH53J (Extraction)</td><td>0x913C4E6C</td><td>Yes</td><td>5843</td><td>0x8000AF98</td><td>0x00010F0C</td></tr>
<tr><td>MH53J (Full)</td><td>0xC97B7814</td><td>Yes</td><td>3627</td><td>0x80009467</td><td>0x000019B5</td></tr>
<tr><td>MH53J (Pursuit)</td><td>0x9964CB9F</td><td>Yes</td><td>4907</td><td>0x8000A27E</td><td>0x00008C2F</td></tr>
<tr><td>Mi26 (base)</td><td>0x9567C231</td><td>Yes</td><td>1220</td><td>0x80006CD1</td><td>0x00007101</td></tr>
<tr><td>Mi26 (CH)</td><td>0x2A46CE47</td><td>Yes</td><td>1221</td><td>0x80006CD2</td><td>0x0000F808</td></tr>
<tr><td>Mi26 (CH) (Delivery)</td><td>0xE8E09FB0</td><td>Yes</td><td>2238</td><td>0x8000820D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mi26 (CH) (Driver)</td><td>0x67B02532</td><td>Yes</td><td>2237</td><td>0x8000820C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mi26 (CH) (Ewan)</td><td>0x71CAED6B</td><td>Yes</td><td>5983</td><td>0x8000B36B</td><td>0x0000E93A</td></tr>
<tr><td>Mi26 (PMC)</td><td>0x8E30490E</td><td>Yes</td><td>1418</td><td>0x80006F71</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mi26 (PMC) (Driver)</td><td>0x9F6ADD25</td><td>Yes</td><td>2236</td><td>0x8000820B</td><td>0x0000C252</td></tr>
<tr><td>Mi26 (VZ)</td><td>0x58D6ABEC</td><td>Yes</td><td>2548</td><td>0x800085AF</td><td>0x000057A5</td></tr>
<tr><td>Mi26 (VZ) (Driver)</td><td>0x77C9BD6B</td><td>Yes</td><td>2495</td><td>0x8000852B</td><td>0x0000B0A3</td></tr>
<tr><td>Mi26 (VZ) (Ewan)</td><td>0x4AFFE432</td><td>Yes</td><td>5984</td><td>0x8000B36C</td><td>0x00006B65</td></tr>
<tr><td>Mi26 (VZA Intro) (Driver)</td><td>0xCB82945A</td><td>Yes</td><td>5961</td><td>0x8000B22E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mi35</td><td>0xD2119BCF</td><td>Yes</td><td>2497</td><td>0x80008531</td><td>0x0000F490</td></tr>
<tr><td>Mi35 (AA Driver)</td><td>0x7B286256</td><td>Yes</td><td>5850</td><td>0x8000AFA2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mi35 (AA)</td><td>0xA0D30616</td><td>Yes</td><td>2603</td><td>0x800085F1</td><td>0x0001329F</td></tr>
<tr><td>Mi35 (AA) (Ewan)</td><td>0xF31E7948</td><td>Yes</td><td>5985</td><td>0x8000B36D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mi35 (base)</td><td>0x5D916CC1</td><td>Yes</td><td>2602</td><td>0x800085F0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mi35 (Driver)</td><td>0x0EED5CFA</td><td>Yes</td><td>2498</td><td>0x80008532</td><td>0x00011FAE</td></tr>
<tr><td>Mi35 (Ewan)</td><td>0x6E0D5F93</td><td>Yes</td><td>5986</td><td>0x8000B36E</td><td>0x0000895C</td></tr>
<tr><td>Mi35 (Full)</td><td>0xCDDFDF39</td><td>Yes</td><td>2499</td><td>0x80008533</td><td>0x00012B61</td></tr>
<tr><td>Mi35 (Gunner)</td><td>0x743728D7</td><td>Yes</td><td>2500</td><td>0x80008534</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mi35 (Solano)</td><td>0xA2EFB316</td><td>Yes</td><td>3445</td><td>0x800092B3</td><td>0x0000B530</td></tr>
<tr><td>Mine (Human)</td><td>0x73FB8018</td><td>No</td><td>1332</td><td>0x80006EA3</td><td>0x00012B04</td></tr>
<tr><td>Mine (IED)</td><td>0xBE4E6E3F</td><td>No</td><td>4874</td><td>0x8000A257</td><td>0x0000AED6</td></tr>
<tr><td>Mine (Vehicle)</td><td>0xDFE0E1E1</td><td>No</td><td>1150</td><td>0x80006B6E</td><td>0x000074FE</td></tr>
<tr><td>Mine (Water)</td><td>0x3EF3D17E</td><td>No</td><td>4894</td><td>0x8000A26C</td><td>0x0000608A</td></tr>
<tr><td>Mine (Water) (Light)</td><td>0x87D2A00F</td><td>No</td><td>5968</td><td>0x8000B2FC</td><td>0x0000D03A</td></tr>
<tr><td>Minigun</td><td>0x624C0986</td><td>No</td><td>2409</td><td>0x80008449</td><td>0x000054D2</td></tr>
<tr><td>Minigun 1000</td><td>0x049CD8B9</td><td>No</td><td>4878</td><td>0x8000A25C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Minigun 1800</td><td>0x99DD73C1</td><td>No</td><td>4879</td><td>0x8000A25D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Minigun 900</td><td>0x9369BBB3</td><td>No</td><td>4880</td><td>0x8000A25E</td><td>0x00002FCF</td></tr>
<tr><td>Minigun Bullet</td><td>0xDAF903E6</td><td>No</td><td>1341</td><td>0x80006EAF</td><td>0x00010DEF</td></tr>
<tr><td>Minigun Bullet (AL)</td><td>0x7303A282</td><td>No</td><td>4123</td><td>0x80009B26</td><td>0x0000CE04</td></tr>
<tr><td>Minigun Bullet (CH)</td><td>0x0B31ED4C</td><td>No</td><td>4124</td><td>0x80009B27</td><td>0xFFFFFFFF</td></tr>
<tr><td>Minigun Bullet (GR)</td><td>0x59D47ACA</td><td>No</td><td>4125</td><td>0x80009B28</td><td>0x000058DF</td></tr>
<tr><td>Minigun Bullet (Ship)</td><td>0x18DFE609</td><td>Yes</td><td>3340</td><td>0x80009000</td><td>0x0000A0B8</td></tr>
<tr><td>MLRS Rocket</td><td>0x2560F199</td><td>No</td><td>3502</td><td>0x80009322</td><td>0x00007F32</td></tr>
<tr><td>MOAB Projectile</td><td>0xFCB92D05</td><td>No</td><td>3167</td><td>0x80008E42</td><td>0x0000744C</td></tr>
<tr><td>Monster Ridgeline</td><td>0x1D489F46</td><td>No</td><td>4014</td><td>0x800099A4</td><td>0x0000C256</td></tr>
<tr><td>Monster Truck</td><td>0xBA21D4C4</td><td>Yes</td><td>1186</td><td>0x80006C99</td><td>0x00001AB7</td></tr>
<tr><td>Monster Truck (base)</td><td>0x1000B4EC</td><td>Yes</td><td>4920</td><td>0x8000A28E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Monster truck phase1</td><td>0x9383C116</td><td>Yes</td><td>2790</td><td>0x8000875C</td><td>0x00000AC0</td></tr>
<tr><td>Monster truck phase2</td><td>0x158B4981</td><td>Yes</td><td>2791</td><td>0x8000875D</td><td>0x0000767B</td></tr>
<tr><td>Monster truck test</td><td>0x9003C228</td><td>Yes</td><td>2544</td><td>0x800085AA</td><td>0x0000117A</td></tr>
<tr><td>MonsterRidgeline_Driver</td><td>0x506C2D61</td><td>No</td><td>5098</td><td>0x8000A423</td><td>0x00010D3E</td></tr>
<tr><td>MonsterRTR_Driver</td><td>0xC091FE7C</td><td>No</td><td>5097</td><td>0x8000A422</td><td>0x00006010</td></tr>
<tr><td>monuments</td><td>0xE28D61F9</td><td>No</td><td>114</td><td>0x80004C1F</td><td>0x00009C2C</td></tr>
<tr><td>Motorcycle</td><td>0xA14A4912</td><td>Yes</td><td>3243</td><td>0x80008F1F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Motorcycle_Driver</td><td>0x6664AE73</td><td>Yes</td><td>5066</td><td>0x8000A3FF</td><td>0x0000A664</td></tr>
<tr><td>MotorcycleOld</td><td>0x25A09161</td><td>Yes</td><td>4393</td><td>0x80009D61</td><td>0x0000EC99</td></tr>
<tr><td>MotorCycleTest</td><td>0x261B03E6</td><td>Yes</td><td>340</td><td>0x80004E28</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AA Missile (1) (AMX30) A</td><td>0xABE72070</td><td>Yes</td><td>3361</td><td>0x8000901B</td><td>0x0000A981</td></tr>
<tr><td>Mounted AA Missile (1) (AMX30) B</td><td>0x95E4BF37</td><td>Yes</td><td>3362</td><td>0x8000901C</td><td>0x00006B16</td></tr>
<tr><td>Mounted AA Missile (1) (AMX30) C</td><td>0xB3E2AFDA</td><td>Yes</td><td>5509</td><td>0x8000AAC4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AA Missile (1) (AMX30) D</td><td>0x8DE03571</td><td>Yes</td><td>5510</td><td>0x8000AAC5</td><td>0x0000EC0B</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_a)</td><td>0x2069A810</td><td>No</td><td>4714</td><td>0x8000A014</td><td>0x00003045</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_b)</td><td>0x8E8EB0E9</td><td>No</td><td>4715</td><td>0x8000A015</td><td>0x0000D14F</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_c)</td><td>0x81706F62</td><td>No</td><td>4716</td><td>0x8000A016</td><td>0x0001062A</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_d)</td><td>0x6126F4CB</td><td>No</td><td>4717</td><td>0x8000A017</td><td>0x000106ED</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_e)</td><td>0xD4A74D84</td><td>No</td><td>4718</td><td>0x8000A018</td><td>0x0000A143</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_f)</td><td>0x6392FBED</td><td>No</td><td>4719</td><td>0x8000A019</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_g)</td><td>0x25FDAD86</td><td>No</td><td>4720</td><td>0x8000A01A</td><td>0x00000576</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_archer_h)</td><td>0x558C0E6F</td><td>No</td><td>4721</td><td>0x8000A01B</td><td>0x00002406</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_sidewinder_L)</td><td>0x52074186</td><td>No</td><td>4271</td><td>0x80009CAA</td><td>0x00004BED</td></tr>
<tr><td>Mounted AA Missile (1) (hp_barreltip_sidewinder_R)</td><td>0x32E24A08</td><td>No</td><td>4272</td><td>0x80009CAB</td><td>0x00006EC7</td></tr>
<tr><td>Mounted AA Missile (1) (PGZ95) A</td><td>0xB5466BDA</td><td>Yes</td><td>3036</td><td>0x80008B74</td><td>0x000005DA</td></tr>
<tr><td>Mounted AA Missile (1) (PGZ95) B</td><td>0x174DC1E5</td><td>Yes</td><td>3039</td><td>0x80008B77</td><td>0x00011CC6</td></tr>
<tr><td>Mounted AA Missile (1) (PGZ95) C</td><td>0xAD4ADC70</td><td>Yes</td><td>3038</td><td>0x80008B76</td><td>0x0000DCF5</td></tr>
<tr><td>Mounted AA Missile (1) (PGZ95) D</td><td>0x2F3EDD23</td><td>Yes</td><td>3037</td><td>0x80008B75</td><td>0x00004373</td></tr>
<tr><td>Mounted AA Missile (2) (Zu23) A</td><td>0xF03FA40A</td><td>No</td><td>4128</td><td>0x80009B2C</td><td>0x00004C04</td></tr>
<tr><td>Mounted AA Missile (2) (Zu23) B</td><td>0x92475ED5</td><td>No</td><td>4129</td><td>0x80009B2D</td><td>0x00006897</td></tr>
<tr><td>Mounted AA Missile (4)</td><td>0x9B70F72E</td><td>No</td><td>509</td><td>0x800056DE</td><td>0x000128A6</td></tr>
<tr><td>Mounted AC A (VZ)</td><td>0x8917B47D</td><td>No</td><td>5830</td><td>0x8000AF8B</td><td>0x0000EA4F</td></tr>
<tr><td>Mounted AC B (VZ)</td><td>0xC70BEFB0</td><td>No</td><td>5831</td><td>0x8000AF8C</td><td>0x000100ED</td></tr>
<tr><td>Mounted AH1Z Cannon</td><td>0xCEBA555E</td><td>Yes</td><td>3679</td><td>0x8000952E</td><td>0x00012945</td></tr>
<tr><td>Mounted AT Missile (1)  (hp_barreltip_a)</td><td>0x3016AB93</td><td>No</td><td>5810</td><td>0x8000AF73</td><td>0x00003532</td></tr>
<tr><td>Mounted AT Missile (1)  (hp_barreltip_b)</td><td>0x153D488E</td><td>No</td><td>5811</td><td>0x8000AF74</td><td>0x00007598</td></tr>
<tr><td>Mounted AT Missile (1) (Base)</td><td>0x4C9BEF00</td><td>No</td><td>4674</td><td>0x80009FE4</td><td>0x0000ABA5</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_raila)</td><td>0xA8DC9549</td><td>No</td><td>4263</td><td>0x80009CA2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railab)</td><td>0x8FCC7C4B</td><td>No</td><td>4267</td><td>0x80009CA6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railac)</td><td>0x034CD504</td><td>No</td><td>4264</td><td>0x80009CA3</td><td>0x00013AE0</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railad)</td><td>0xBD343869</td><td>No</td><td>4265</td><td>0x80009CA4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railae)</td><td>0xB015F6E2</td><td>No</td><td>4266</td><td>0x80009CA5</td><td>0x0000220B</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railaf)</td><td>0x6C2D8A47</td><td>No</td><td>4268</td><td>0x80009CA7</td><td>0x000070DB</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railag)</td><td>0x4F0F2F90</td><td>No</td><td>4269</td><td>0x80009CA8</td><td>0x0000163C</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_hellfire_railah)</td><td>0xAB2A11B5</td><td>No</td><td>4270</td><td>0x80009CA9</td><td>0x00007C40</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missile_L)</td><td>0x3060A513</td><td>No</td><td>2601</td><td>0x800085EF</td><td>0x00004FEE</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missile_la)</td><td>0x1A63F32C</td><td>No</td><td>4275</td><td>0x80009CAE</td><td>0x0000F496</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missile_R)</td><td>0xF3E10699</td><td>No</td><td>4673</td><td>0x80009FE3</td><td>0x0000A99E</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missileL_a)</td><td>0xEBA333F2</td><td>No</td><td>3668</td><td>0x80009523</td><td>0x0000ED2B</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missileL_b)</td><td>0x271C2D17</td><td>No</td><td>3669</td><td>0x80009524</td><td>0x0001198D</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missileR_a)</td><td>0xFA21F9E0</td><td>No</td><td>3660</td><td>0x8000951B</td><td>0x0000165E</td></tr>
<tr><td>Mounted AT Missile (1) (hp_barreltip_missileR_b)</td><td>0xE8E59CF9</td><td>No</td><td>3662</td><td>0x8000951D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AT Missile (2)  (hp_barreltip_c)</td><td>0x4F784B20</td><td>No</td><td>5812</td><td>0x8000AF75</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AT Missile (2) (M2A3)</td><td>0x6C8EDBAD</td><td>Yes</td><td>4116</td><td>0x80009B1F</td><td>0x0000AEF8</td></tr>
<tr><td>Mounted AT Missile (4)</td><td>0x70CB82B3</td><td>No</td><td>5809</td><td>0x8000AF72</td><td>0x00013A6A</td></tr>
<tr><td>Mounted AT Missile (4) (hp_barreltip_missile_L)</td><td>0x70478B06</td><td>No</td><td>4675</td><td>0x80009FE5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AT Missile (4) (hp_barreltip_missile_R)</td><td>0x51229388</td><td>No</td><td>4676</td><td>0x80009FE6</td><td>0x00005BD1</td></tr>
<tr><td>Mounted AT Missile (8)</td><td>0xB2FD0467</td><td>No</td><td>4042</td><td>0x80009AD0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted AT Missile (hp_barreltip_missile_lb)</td><td>0x7D548893</td><td>No</td><td>4276</td><td>0x80009CAF</td><td>0x0000F657</td></tr>
<tr><td>Mounted AT Missile (hp_barreltip_missile_ra)</td><td>0x8F08CF54</td><td>No</td><td>4278</td><td>0x80009CB1</td><td>0x00007BA9</td></tr>
<tr><td>Mounted AT Missile (hp_barreltip_missile_rb)</td><td>0xDD56483D</td><td>No</td><td>4277</td><td>0x80009CB0</td><td>0x00010085</td></tr>
<tr><td>Mounted AT Missile (Veyron)</td><td>0x5B34F448</td><td>No</td><td>5808</td><td>0x8000AF71</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Autocannon (AL)</td><td>0x6090304D</td><td>No</td><td>2289</td><td>0x8000824D</td><td>0x00008987</td></tr>
<tr><td>Mounted Autocannon (CH)</td><td>0xB17FB08B</td><td>No</td><td>4097</td><td>0x80009B0C</td><td>0x00010CE7</td></tr>
<tr><td>Mounted Autocannon (Type 14310)</td><td>0x7BC113EF</td><td>No</td><td>2185</td><td>0x800081D5</td><td>0x0000EC2E</td></tr>
<tr><td>Mounted Blast Cannon</td><td>0x37938DD0</td><td>No</td><td>4885</td><td>0x8000A263</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Chain Cannon</td><td>0x50AA1C3F</td><td>No</td><td>4046</td><td>0x80009AD5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Chain Cannon (CH)</td><td>0x7872DE87</td><td>No</td><td>4109</td><td>0x80009B18</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Chain Cannon (GR)</td><td>0xF97B07CD</td><td>No</td><td>4114</td><td>0x80009B1D</td><td>0x000051AE</td></tr>
<tr><td>Mounted Coax 20mm (OC)</td><td>0x08D57327</td><td>No</td><td>4117</td><td>0x80009B20</td><td>0x0000DCA5</td></tr>
<tr><td>Mounted Coax 20mm (VZ)</td><td>0x658DA359</td><td>No</td><td>4118</td><td>0x80009B21</td><td>0x0000786F</td></tr>
<tr><td>Mounted Coax MG (AL)</td><td>0x544E96C0</td><td>No</td><td>699</td><td>0x80005FB6</td><td>0x0000ECBA</td></tr>
<tr><td>Mounted Coax MG (CH)</td><td>0xB6D6C82E</td><td>No</td><td>4096</td><td>0x80009B0B</td><td>0x0000D37B</td></tr>
<tr><td>Mounted Coax MG (GR)</td><td>0xCBCA16B8</td><td>No</td><td>4098</td><td>0x80009B0D</td><td>0x00013E3B</td></tr>
<tr><td>Mounted Coax MG (VZ)</td><td>0x1D9E8B69</td><td>No</td><td>5013</td><td>0x8000A3C1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Cruise Missile</td><td>0x6F53A674</td><td>No</td><td>3354</td><td>0x8000900E</td><td>0x0000DBBF</td></tr>
<tr><td>Mounted Cruise Missile Projectile</td><td>0x61048FB9</td><td>No</td><td>4045</td><td>0x80009AD3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Destroyer Cannon</td><td>0xF76F060F</td><td>Yes</td><td>3355</td><td>0x80009014</td><td>0x000131EC</td></tr>
<tr><td>Mounted Destroyer Cannon (Chinese)</td><td>0x4414CCB9</td><td>Yes</td><td>3360</td><td>0x8000901A</td><td>0x00008B2A</td></tr>
<tr><td>Mounted FAE (1) (hp_barreltip_hellfire_raila)</td><td>0x1CB068A0</td><td>No</td><td>5815</td><td>0x8000AF78</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted FAE (1) (hp_barreltip_hellfire_railb)</td><td>0x0B740BB9</td><td>No</td><td>5817</td><td>0x8000AF7A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted FAE (1) (hp_barreltip_hellfire_railc)</td><td>0x7EF46472</td><td>No</td><td>5818</td><td>0x8000AF7B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted FAE (1) (hp_barreltip_hellfire_raild)</td><td>0x1EAA851B</td><td>No</td><td>5819</td><td>0x8000AF7C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Grenade Launcher</td><td>0x14DA2EDB</td><td>No</td><td>1345</td><td>0x80006EB5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Grenade Launcher (UH1 Elite)</td><td>0xD57B8791</td><td>Yes</td><td>4249</td><td>0x80009C8F</td><td>0x00010B74</td></tr>
<tr><td>Mounted Grenade Launcher Shooting Gallery</td><td>0xDE0D1378</td><td>No</td><td>5562</td><td>0x8000AB64</td><td>0x00010D36</td></tr>
<tr><td>Mounted Gun (Endriago) (Superiority) (LB)</td><td>0x3F410E0A</td><td>No</td><td>2192</td><td>0x800081DD</td><td>0x000052E1</td></tr>
<tr><td>Mounted Gun (Endriago) (Superiority) (LT)</td><td>0xA043EF7C</td><td>No</td><td>2191</td><td>0x800081DC</td><td>0x00002F8C</td></tr>
<tr><td>Mounted Gun (Endriago) (Superiority) (RB)</td><td>0x35F50D74</td><td>No</td><td>4208</td><td>0x80009C66</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Gun (Endriago) (Superiority) (RT)</td><td>0x74F194E2</td><td>No</td><td>4207</td><td>0x80009C65</td><td>0x00006B5F</td></tr>
<tr><td>Mounted Gun (Piranha) (L)</td><td>0x97AF2A8A</td><td>Yes</td><td>3203</td><td>0x80008EF5</td><td>0x000110C4</td></tr>
<tr><td>Mounted Gun (Piranha) (R)</td><td>0xDFC07DB4</td><td>Yes</td><td>3204</td><td>0x80008EF6</td><td>0x00007AD8</td></tr>
<tr><td>Mounted Gun Front (Patrol Boat VZ)</td><td>0xEAD9F069</td><td>Yes</td><td>5203</td><td>0x8000A5EB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Gunpod (L) (AL)</td><td>0x1F02D391</td><td>No</td><td>3656</td><td>0x80009517</td><td>0x000102E0</td></tr>
<tr><td>Mounted Gunpod (R) (AL)</td><td>0x6B0EC633</td><td>No</td><td>3657</td><td>0x80009518</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Heavy MG (AL)</td><td>0xB300A00E</td><td>No</td><td>6</td><td>0x80002336</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Heavy MG (Avenger)</td><td>0x1F3D06B9</td><td>No</td><td>3527</td><td>0x8000933B</td><td>0x0000A2E7</td></tr>
<tr><td>Mounted Heavy MG (Base)</td><td>0x70274A56</td><td>No</td><td>3643</td><td>0x80009477</td><td>0x00006049</td></tr>
<tr><td>Mounted Heavy MG (CH)</td><td>0x4F3B3A20</td><td>No</td><td>4091</td><td>0x80009B06</td><td>0x00011369</td></tr>
<tr><td>Mounted Heavy MG (GR)</td><td>0x54D1D516</td><td>No</td><td>4092</td><td>0x80009B07</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Heavy MG (Jeep) (AL)</td><td>0x3565F12D</td><td>Yes</td><td>5700</td><td>0x8000ACCE</td><td>0x000122FC</td></tr>
<tr><td>Mounted Heavy MG (Jeep) (GR)</td><td>0xBC105279</td><td>Yes</td><td>5701</td><td>0x8000ACCF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Heavy MG (Jeep) (OC)</td><td>0xDF170CCA</td><td>Yes</td><td>5702</td><td>0x8000ACD0</td><td>0x00003A81</td></tr>
<tr><td>Mounted Heavy MG (No Model)</td><td>0xA88E044D</td><td>No</td><td>2557</td><td>0x800085BB</td><td>0x0000BF17</td></tr>
<tr><td>Mounted Heavy MG (NOAMMO)</td><td>0xC3B9FF06</td><td>No</td><td>5612</td><td>0x8000AC5C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Heavy MG (OC)</td><td>0x21ED52B5</td><td>No</td><td>5398</td><td>0x8000A98C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Heavy MG (Tank) (AL)</td><td>0xF58133B9</td><td>Yes</td><td>5694</td><td>0x8000ACC7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Heavy MG (Tank) (CH)</td><td>0x60CFE4EF</td><td>Yes</td><td>5696</td><td>0x8000ACC9</td><td>0x0000BC8A</td></tr>
<tr><td>Mounted Heavy MG (Tank) (GR)</td><td>0x745B25A5</td><td>Yes</td><td>5695</td><td>0x8000ACC8</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Heavy MG (Tank) (OC)</td><td>0xFA33A7F6</td><td>Yes</td><td>5697</td><td>0x8000ACCA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Heavy MG (Tank) (VZ)</td><td>0x96133FF4</td><td>Yes</td><td>5693</td><td>0x8000ACC6</td><td>0x00001E42</td></tr>
<tr><td>Mounted Heavy MG (VZ)</td><td>0x08DB8417</td><td>No</td><td>1344</td><td>0x80006EB4</td><td>0x0001370B</td></tr>
<tr><td>Mounted Light MG (GR)</td><td>0x39A0741B</td><td>No</td><td>4112</td><td>0x80009B1B</td><td>0x000024FB</td></tr>
<tr><td>Mounted LockOn Missile</td><td>0xAFEB579B</td><td>No</td><td>3658</td><td>0x80009519</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted M101A1 Gun</td><td>0xD462BFB2</td><td>No</td><td>3456</td><td>0x800092BE</td><td>0x0000E9C4</td></tr>
<tr><td>Mounted MG (L)</td><td>0x285BA208</td><td>No</td><td>5514</td><td>0x8000AACA</td><td>0x00004521</td></tr>
<tr><td>Mounted MG (R)</td><td>0x47809986</td><td>No</td><td>5515</td><td>0x8000AACB</td><td>0x00001A0A</td></tr>
<tr><td>Mounted Minigun (Destroyer) (FL)</td><td>0x51AEEAC1</td><td>Yes</td><td>3356</td><td>0x80009016</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun (Destroyer) (FM)</td><td>0x4490A93A</td><td>Yes</td><td>3676</td><td>0x8000952B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun (Destroyer) (FR)</td><td>0x3C4B3A4B</td><td>Yes</td><td>3357</td><td>0x80009017</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun (Destroyer) (RL)</td><td>0xC6661465</td><td>Yes</td><td>3358</td><td>0x80009018</td><td>0x0000073B</td></tr>
<tr><td>Mounted Minigun (Destroyer) (RR)</td><td>0xD99C8DC7</td><td>Yes</td><td>3359</td><td>0x80009019</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun (Human) (AL)</td><td>0xACA58116</td><td>No</td><td>3637</td><td>0x80009471</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun (Human) (GR)</td><td>0x499A11CE</td><td>No</td><td>4126</td><td>0x80009B29</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun (Human) HelCon001</td><td>0x2F3E5314</td><td>No</td><td>4021</td><td>0x80009A07</td><td>0x000038A2</td></tr>
<tr><td>Mounted Minigun (No Model) (AL)</td><td>0x52B5AA0B</td><td>No</td><td>4127</td><td>0x80009B2A</td><td>0x00011E98</td></tr>
<tr><td>Mounted Minigun (No model) (Hind)</td><td>0x2E850373</td><td>Yes</td><td>2577</td><td>0x800085D4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun (No Model) (LAV3 AD)</td><td>0x102B093D</td><td>Yes</td><td>2596</td><td>0x800085EA</td><td>0x0000F973</td></tr>
<tr><td>Mounted Minigun (No model) (M1A2)</td><td>0xB2B5511F</td><td>Yes</td><td>3364</td><td>0x8000901E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun (No Model) (VZ)</td><td>0xFC34C616</td><td>No</td><td>1340</td><td>0x80006EAE</td><td>0x0000407A</td></tr>
<tr><td>Mounted Minigun (Remote) (AL)</td><td>0xCE7E778F</td><td>No</td><td>18</td><td>0x800038E6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun Left (No Model) (GR)</td><td>0x4F1B684C</td><td>No</td><td>857</td><td>0x800063AF</td><td>0x0000A3FC</td></tr>
<tr><td>Mounted Minigun Left (No Model) (Small) (VZ)</td><td>0xEB11BE9F</td><td>No</td><td>2589</td><td>0x800085E2</td><td>0x00002E5B</td></tr>
<tr><td>Mounted Minigun Right (No Model) (GR)</td><td>0xBDE3C1E5</td><td>No</td><td>858</td><td>0x800063B0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Minigun Right (No Model) (Small) (VZ)</td><td>0x58CF48F6</td><td>No</td><td>2590</td><td>0x800085E3</td><td>0x0000B7DF</td></tr>
<tr><td>Mounted MLRS</td><td>0xAC223AF7</td><td>No</td><td>3501</td><td>0x80009321</td><td>0x00001940</td></tr>
<tr><td>Mounted MLRS (SX2150) (01)</td><td>0x11965E4F</td><td>No</td><td>3503</td><td>0x80009323</td><td>0x00008AD0</td></tr>
<tr><td>Mounted MLRS (SX2150) (02)</td><td>0x366DAE2A</td><td>No</td><td>3504</td><td>0x80009324</td><td>0x0000AD9C</td></tr>
<tr><td>Mounted MLRS (SX2150) (03)</td><td>0xC2ED5571</td><td>No</td><td>3505</td><td>0x80009325</td><td>0x0000DCD3</td></tr>
<tr><td>Mounted MLRS (SX2150) (04)</td><td>0xA9055AEC</td><td>No</td><td>3506</td><td>0x80009326</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted MLRS (SX2150) (05)</td><td>0xB6239C73</td><td>No</td><td>3507</td><td>0x80009327</td><td>0x0000C159</td></tr>
<tr><td>Mounted MLRS (SX2150) (06)</td><td>0x1A0C3B6E</td><td>No</td><td>3508</td><td>0x80009328</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted MLRS (SX2150) (07)</td><td>0xB7526F15</td><td>No</td><td>3509</td><td>0x80009329</td><td>0x0000A133</td></tr>
<tr><td>Mounted MLRS (SX2150) (08)</td><td>0xDB36C370</td><td>No</td><td>3510</td><td>0x8000932A</td><td>0x00008603</td></tr>
<tr><td>Mounted MLRS (SX2150) (09)</td><td>0xF8551E27</td><td>No</td><td>3511</td><td>0x8000932B</td><td>0x0000A5A7</td></tr>
<tr><td>Mounted MLRS (SX2150) (10)</td><td>0x414EE8C5</td><td>No</td><td>3512</td><td>0x8000932C</td><td>0x0000FC85</td></tr>
<tr><td>Mounted MLRS (SX2150) (11)</td><td>0xA36AE45E</td><td>No</td><td>3513</td><td>0x8000932D</td><td>0x00002ABF</td></tr>
<tr><td>Mounted MLRS (SX2150) (12)</td><td>0x7EE34663</td><td>No</td><td>3514</td><td>0x8000932E</td><td>0x00013EF2</td></tr>
<tr><td>Mounted Panhard Assault Cannon</td><td>0x53E032EF</td><td>No</td><td>4729</td><td>0x8000A023</td><td>0x0000A542</td></tr>
<tr><td>Mounted PGZ95 Gun</td><td>0x06B1335C</td><td>Yes</td><td>3030</td><td>0x80008B6E</td><td>0x000062EA</td></tr>
<tr><td>Mounted PGZ95 Gun (A)</td><td>0x77662EDA</td><td>Yes</td><td>3031</td><td>0x80008B6F</td><td>0x0000EB8C</td></tr>
<tr><td>Mounted PGZ95 Gun (B)</td><td>0x928F43BF</td><td>Yes</td><td>3034</td><td>0x80008B72</td><td>0x00011507</td></tr>
<tr><td>Mounted PGZ95 Gun (C)</td><td>0x160FB5A8</td><td>Yes</td><td>3033</td><td>0x80008B71</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted PGZ95 Gun (D)</td><td>0xB987BF85</td><td>Yes</td><td>3032</td><td>0x80008B70</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Piranha Deck Cannon</td><td>0x49DEA0CC</td><td>Yes</td><td>5513</td><td>0x8000AAC9</td><td>0x0000449D</td></tr>
<tr><td>Mounted Piranha Jet Exhaust</td><td>0xEF7FFB65</td><td>Yes</td><td>3467</td><td>0x800092C9</td><td>0x0000B9E1</td></tr>
<tr><td>Mounted Quad50 Gun A (GR)</td><td>0x88A30040</td><td>No</td><td>2888</td><td>0x80008929</td><td>0x00010290</td></tr>
<tr><td>Mounted Quad50 Gun A (VZ)</td><td>0x0D76BCC1</td><td>No</td><td>4119</td><td>0x80009B22</td><td>0x00007FB5</td></tr>
<tr><td>Mounted Quad50 Gun B (GR)</td><td>0x1DECD9B5</td><td>No</td><td>2889</td><td>0x8000892A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Quad50 Gun B (VZ)</td><td>0x191E59E4</td><td>No</td><td>4120</td><td>0x80009B23</td><td>0x0000820E</td></tr>
<tr><td>Mounted Quad50 Gun C (GR)</td><td>0xD228E09E</td><td>No</td><td>2890</td><td>0x8000892B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Quad50 Gun C (VZ)</td><td>0x2DE9E22F</td><td>No</td><td>4121</td><td>0x80009B24</td><td>0x0000971D</td></tr>
<tr><td>Mounted Quad50 Gun D (GR)</td><td>0xEF6E0ED3</td><td>No</td><td>2891</td><td>0x8000892C</td><td>0x0000CAC3</td></tr>
<tr><td>Mounted Quad50 Gun D (VZ)</td><td>0x005BB6E2</td><td>No</td><td>4122</td><td>0x80009B25</td><td>0x0000DF6B</td></tr>
<tr><td>Mounted Recoiless Rifle</td><td>0xF6A450BC</td><td>No</td><td>2410</td><td>0x8000844A</td><td>0x00004802</td></tr>
<tr><td>Mounted Rocket (3)</td><td>0xBB1AA49D</td><td>No</td><td>5518</td><td>0x8000AACE</td><td>0x00006B86</td></tr>
<tr><td>Mounted Rocket Pod (10) (hp_barreltip_rocket_L)</td><td>0xEAB93289</td><td>No</td><td>4929</td><td>0x8000A297</td><td>0x000013EA</td></tr>
<tr><td>Mounted Rocket Pod (10) (hp_barreltip_rocket_R)</td><td>0x440F9F23</td><td>No</td><td>4930</td><td>0x8000A298</td><td>0x00007001</td></tr>
<tr><td>Mounted Rocket Pod (19)</td><td>0x09C80673</td><td>No</td><td>480</td><td>0x800056B6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Rocket Pod (19) (hp_barreltip_rcketlgL)</td><td>0x992241C5</td><td>No</td><td>4955</td><td>0x8000A2B7</td><td>0x00013889</td></tr>
<tr><td>Mounted Rocket Pod (19) (hp_barreltip_rcketlgR)</td><td>0xAB1B86A7</td><td>No</td><td>4956</td><td>0x8000A2B8</td><td>0x00011C9F</td></tr>
<tr><td>Mounted Rocket Pod (19) (hp_barreltip_xrocketL)</td><td>0x35E451C1</td><td>No</td><td>3666</td><td>0x80009521</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Rocket Pod (19) (hp_barreltip_xrocketR)</td><td>0x2080A14B</td><td>No</td><td>3664</td><td>0x8000951F</td><td>0x000068BD</td></tr>
<tr><td>Mounted Rocket Pod (20)</td><td>0xA5E26E43</td><td>No</td><td>4110</td><td>0x80009B19</td><td>0x000006FF</td></tr>
<tr><td>Mounted Rocket Pod (32)</td><td>0xCEC74E4C</td><td>No</td><td>2496</td><td>0x8000852D</td><td>0x0000B74F</td></tr>
<tr><td>Mounted Rocket Pod (32) (hp_barreltip_rocket_L)</td><td>0x42C03281</td><td>No</td><td>4957</td><td>0x8000A2BA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Rocket Pod (32) (hp_barreltip_rocket_R)</td><td>0x2D5C820B</td><td>No</td><td>5200</td><td>0x8000A5E8</td><td>0x00013066</td></tr>
<tr><td>Mounted Rocket Pod (6) (L)</td><td>0xDF92C81E</td><td>No</td><td>3631</td><td>0x8000946B</td><td>0x00007563</td></tr>
<tr><td>Mounted Rocket Pod (7)</td><td>0x267A1638</td><td>No</td><td>2262</td><td>0x80008230</td><td>0x0000F43A</td></tr>
<tr><td>Mounted Rocket Pod (7) (hp_barreltip_smlroktl)</td><td>0x16379B62</td><td>No</td><td>5520</td><td>0x8000AAD0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Rocket Pod (7) (hp_barreltip_smlroktr)</td><td>0xF02CA23C</td><td>No</td><td>5521</td><td>0x8000AAD1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Rocket Pod (7) (OC)</td><td>0xE4107BF7</td><td>No</td><td>5519</td><td>0x8000AACF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Rocket Pod (7) (R)</td><td>0xB3E3709B</td><td>No</td><td>3632</td><td>0x8000946C</td><td>0x0000C04A</td></tr>
<tr><td>Mounted RocketPod (Endriago) (Superiority) (L)</td><td>0x37E1FB77</td><td>No</td><td>2193</td><td>0x800081DE</td><td>0x00003454</td></tr>
<tr><td>Mounted RocketPod (Endriago) (Superiority) (R)</td><td>0x49124D35</td><td>No</td><td>2195</td><td>0x800081E0</td><td>0x00006AE0</td></tr>
<tr><td>Mounted SAM (1)</td><td>0xA6EAC7DC</td><td>No</td><td>1578</td><td>0x80007219</td><td>0x000131E6</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BA</td><td>0x704586F5</td><td>Yes</td><td>3022</td><td>0x80008B66</td><td>0x0000C09F</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BB</td><td>0x4E3E95AA</td><td>Yes</td><td>3029</td><td>0x80008B6D</td><td>0x000120D4</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BC</td><td>0x704109C7</td><td>Yes</td><td>3028</td><td>0x80008B6C</td><td>0x00007A11</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BD</td><td>0xEE39815C</td><td>Yes</td><td>3027</td><td>0x80008B6B</td><td>0x0000085B</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BE</td><td>0xE83BB681</td><td>Yes</td><td>3026</td><td>0x80008B6A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BF</td><td>0x66342E16</td><td>Yes</td><td>3025</td><td>0x80008B69</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BG</td><td>0xC83706F3</td><td>Yes</td><td>3023</td><td>0x80008B67</td><td>0x00012222</td></tr>
<tr><td>Mounted SAM (LAVIII AD) BH</td><td>0x662FB0E8</td><td>Yes</td><td>3024</td><td>0x80008B68</td><td>0x00012477</td></tr>
<tr><td>Mounted Ship Gun</td><td>0xE9291BB1</td><td>Yes</td><td>3348</td><td>0x80009008</td><td>0x00003FFC</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FA)</td><td>0x599E50E5</td><td>Yes</td><td>3347</td><td>0x80009007</td><td>0x0001133B</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FA) (AllCon002)</td><td>0xEAB0852D</td><td>Yes</td><td>4036</td><td>0x80009A21</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FB)</td><td>0x8AB23DBC</td><td>Yes</td><td>3351</td><td>0x8000900B</td><td>0x0001088D</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FB) (AllCon002)</td><td>0x4E1C02CC</td><td>Yes</td><td>4037</td><td>0x80009A22</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FC)</td><td>0x186F1983</td><td>Yes</td><td>3349</td><td>0x80009009</td><td>0x0000F75C</td></tr>
<tr><td>Mounted Ship Gun (Huangfeng) (FD)</td><td>0x98B92B3A</td><td>Yes</td><td>3350</td><td>0x8000900A</td><td>0x00006646</td></tr>
<tr><td>Mounted Ship Gun (Piranha) (JetExhaust)</td><td>0xD9268BDF</td><td>Yes</td><td>4927</td><td>0x8000A295</td><td>0x0000618C</td></tr>
<tr><td>Mounted Ship Minigun (No model)</td><td>0xDB079345</td><td>Yes</td><td>3339</td><td>0x80008FFF</td><td>0x00013FE7</td></tr>
<tr><td>Mounted SSM (Huangfeng FL)</td><td>0x5959102A</td><td>Yes</td><td>4163</td><td>0x80009BA0</td><td>0x000026F3</td></tr>
<tr><td>Mounted SSM (Huangfeng FR)</td><td>0x216999D4</td><td>Yes</td><td>4244</td><td>0x80009C8A</td><td>0x0000CF82</td></tr>
<tr><td>Mounted SSM (Huangfeng RL)</td><td>0x440319E6</td><td>Yes</td><td>4162</td><td>0x80009B9F</td><td>0x00004F45</td></tr>
<tr><td>Mounted SSM (Huangfeng RR)</td><td>0xA4DEEBE8</td><td>Yes</td><td>4161</td><td>0x80009B9E</td><td>0x000052B0</td></tr>
<tr><td>Mounted Tank Gun (Artillery)</td><td>0x4515E1EC</td><td>Yes</td><td>4134</td><td>0x80009B32</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted Tank Gun (Cannister)</td><td>0x59B859C1</td><td>Yes</td><td>5014</td><td>0x8000A3C2</td><td>0x0000C4D9</td></tr>
<tr><td>Mounted Tank Gun (Default)</td><td>0x32057B9F</td><td>Yes</td><td>698</td><td>0x80005FB5</td><td>0x00005FC4</td></tr>
<tr><td>Mounted Tank Gun (Sabot)</td><td>0xD2F93EBB</td><td>Yes</td><td>4135</td><td>0x80009B33</td><td>0x00007BCF</td></tr>
<tr><td>Mounted Tank Gun (Weak)</td><td>0x91FE83D0</td><td>Yes</td><td>4133</td><td>0x80009B31</td><td>0x0000ED06</td></tr>
<tr><td>Mounted TOW Missile</td><td>0x2E092CD1</td><td>No</td><td>1088</td><td>0x80006A35</td><td>0x000015A8</td></tr>
<tr><td>Mounted TOW Missile (1) (hp_barreltip_hellfire_A)</td><td>0x1EFACDA6</td><td>No</td><td>2592</td><td>0x800085E6</td><td>0x00004251</td></tr>
<tr><td>Mounted TOW Missile (1) (hp_barreltip_hellfire_B)</td><td>0x5A2414EB</td><td>No</td><td>2593</td><td>0x800085E7</td><td>0x0000A3F5</td></tr>
<tr><td>Mounted TOW Missile (1) (hp_barreltip_hellfire_C)</td><td>0xCC673924</td><td>No</td><td>2594</td><td>0x800085E8</td><td>0x0000EDCA</td></tr>
<tr><td>Mounted TOW Missile (1) (hp_barreltip_hellfire_D)</td><td>0x078C9A89</td><td>No</td><td>2595</td><td>0x800085E9</td><td>0x00011A3B</td></tr>
<tr><td>Mounted TOW Missile (1) (no model)</td><td>0x59CA8EC2</td><td>No</td><td>4873</td><td>0x8000A256</td><td>0x000001DB</td></tr>
<tr><td>Mounted TOW Missile (2) (hp_barrel_tip_a)</td><td>0x12477118</td><td>No</td><td>4936</td><td>0x8000A2A2</td><td>0x0000C991</td></tr>
<tr><td>Mounted TOW Missile (2) (hp_barrel_tip_b)</td><td>0x81F96051</td><td>No</td><td>4937</td><td>0x8000A2A3</td><td>0x0000D578</td></tr>
<tr><td>Mounted TOW Missile (2) (hp_barreltip_c)</td><td>0xB599A693</td><td>No</td><td>4938</td><td>0x8000A2A4</td><td>0x00000D75</td></tr>
<tr><td>Mounted TOW Missile (4) (hp_barreltip_a)</td><td>0xA2ECBCB7</td><td>No</td><td>4888</td><td>0x8000A266</td><td>0x00000E1E</td></tr>
<tr><td>Mounted TOW Missile (4) (no model)</td><td>0xE74AE3BB</td><td>No</td><td>4698</td><td>0x8000A001</td><td>0xFFFFFFFF</td></tr>
<tr><td>Mounted TOW Missile (no model)</td><td>0xFF4EC498</td><td>No</td><td>2870</td><td>0x80008917</td><td>0x0000396F</td></tr>
<tr><td>Mounted WZ10 Cannon</td><td>0xCEF89994</td><td>No</td><td>4111</td><td>0x80009B1A</td><td>0x00000599</td></tr>
<tr><td>Mounted ZU23 Gun A</td><td>0x25A78994</td><td>No</td><td>2508</td><td>0x8000853E</td><td>0x00006104</td></tr>
<tr><td>Mounted ZU23 Gun B</td><td>0xFFA50F2B</td><td>No</td><td>2509</td><td>0x8000853F</td><td>0x0000DB74</td></tr>
<tr><td>MountedM60 MG</td><td>0x709B8A92</td><td>No</td><td>49</td><td>0x80004632</td><td>0x00007834</td></tr>
<tr><td>mr_boss_test</td><td>0xE96E444B</td><td>No</td><td>2912</td><td>0x80008946</td><td>0x0000C66D</td></tr>
<tr><td>mr_boss_test2</td><td>0xD9A92C6B</td><td>No</td><td>3073</td><td>0x80008B9C</td><td>0xFFFFFFFF</td></tr>
<tr><td>MR_rd_10_1</td><td>0x4F81F793</td><td>No</td><td>2903</td><td>0x80008939</td><td>0xFFFFFFFF</td></tr>
<tr><td>MR_rd_10_2</td><td>0x758471FC</td><td>No</td><td>3074</td><td>0x80008B9E</td><td>0x0000ADDB</td></tr>
<tr><td>MR_rd_20_1</td><td>0xCBF63B36</td><td>No</td><td>2902</td><td>0x80008938</td><td>0xFFFFFFFF</td></tr>
<tr><td>mreeves</td><td>0xD4D44884</td><td>No</td><td>529</td><td>0x80005B87</td><td>0x00002244</td></tr>
<tr><td>MTV (base)</td><td>0xC0D414DC</td><td>No</td><td>3470</td><td>0x800092CC</td><td>0xFFFFFFFF</td></tr>
<tr><td>MTV (Cargo)</td><td>0xDE067C2D</td><td>No</td><td>3471</td><td>0x800092CD</td><td>0x00013EC0</td></tr>
<tr><td>MTV (Cargo) (Driver)</td><td>0x142EB3B8</td><td>No</td><td>3495</td><td>0x8000931B</td><td>0x0000C370</td></tr>
<tr><td>MTV (Cargo) (Full)</td><td>0x73BDBE3F</td><td>No</td><td>3498</td><td>0x8000931E</td><td>0x00004881</td></tr>
<tr><td>MTV (Expandible Van)</td><td>0xB7495554</td><td>No</td><td>3475</td><td>0x800092D1</td><td>0x000084AA</td></tr>
<tr><td>MTV (Expandible Van) (Driver)</td><td>0x5ECC34B3</td><td>No</td><td>3496</td><td>0x8000931C</td><td>0x0000D774</td></tr>
<tr><td>MTV (Expandible Van) (Full)</td><td>0xD61300E0</td><td>No</td><td>3499</td><td>0x8000931F</td><td>0x0001339D</td></tr>
<tr><td>MTV (Fuel)</td><td>0xDB734B8D</td><td>No</td><td>3472</td><td>0x800092CE</td><td>0xFFFFFFFF</td></tr>
<tr><td>MTV (Fuel) (Driver)</td><td>0x770C9A98</td><td>No</td><td>3497</td><td>0x8000931D</td><td>0x00010221</td></tr>
<tr><td>MTV (Fuel) (Full)</td><td>0x694EB79F</td><td>No</td><td>3500</td><td>0x80009320</td><td>0x000138AB</td></tr>
<tr><td>MTV (semi)</td><td>0xA3D40E0B</td><td>No</td><td>4013</td><td>0x800099A3</td><td>0x00005CAE</td></tr>
<tr><td>MTV (semi) (Driver)</td><td>0xAECCD2A6</td><td>No</td><td>3085</td><td>0x80008BA9</td><td>0x0000C188</td></tr>
<tr><td>MTV_Driver</td><td>0x6B984FB9</td><td>No</td><td>5076</td><td>0x8000A40A</td><td>0x0000CC37</td></tr>
<tr><td>MTVExpandibleVan_Driver</td><td>0x43570A2C</td><td>No</td><td>5388</td><td>0x8000A97C</td><td>0x0000880E</td></tr>
<tr><td>Munitions (Artillery Ch)</td><td>0x048E9847</td><td>No</td><td>5877</td><td>0x8000B019</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions (Artillery Gr)</td><td>0x8596C18D</td><td>No</td><td>5876</td><td>0x8000B018</td><td>0x00013E3C</td></tr>
<tr><td>Munitions (Artillery Laptop)</td><td>0x4C7050FC</td><td>No</td><td>5796</td><td>0x8000AEFD</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions (Artillery VZ)</td><td>0x331E75EC</td><td>No</td><td>5872</td><td>0x8000B014</td><td>0x00008E1D</td></tr>
<tr><td>Munitions (Artillery)</td><td>0x65BFA29A</td><td>No</td><td>2442</td><td>0x80008471</td><td>0x000095E0</td></tr>
<tr><td>Munitions (Bombing Run Al)</td><td>0xFAEE8B68</td><td>No</td><td>5886</td><td>0x8000B022</td><td>0x00010708</td></tr>
<tr><td>Munitions (Bombing Run Ch)</td><td>0xDA9C40F6</td><td>No</td><td>5878</td><td>0x8000B01A</td><td>0x00000AF1</td></tr>
<tr><td>Munitions (Bombing Run OC)</td><td>0x8A4F9C3F</td><td>No</td><td>5894</td><td>0x8000B02A</td><td>0x0000DF71</td></tr>
<tr><td>Munitions (Bombing Run VZ)</td><td>0x848DCD31</td><td>No</td><td>5873</td><td>0x8000B015</td><td>0x00009FDE</td></tr>
<tr><td>Munitions (Bombing Run)</td><td>0xE9B43425</td><td>No</td><td>3142</td><td>0x80008E28</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions (Bunker Buster Al)</td><td>0xFBA255D9</td><td>No</td><td>5887</td><td>0x8000B023</td><td>0x000024FE</td></tr>
<tr><td>Munitions (Bunker Buster)</td><td>0xF38C2502</td><td>No</td><td>2432</td><td>0x80008465</td><td>0x00002D20</td></tr>
<tr><td>Munitions (Carpet Bomb)</td><td>0x3724C6AD</td><td>No</td><td>3150</td><td>0x80008E30</td><td>0x00006186</td></tr>
<tr><td>Munitions (Cluster Bomb OC)</td><td>0x6904D454</td><td>No</td><td>5895</td><td>0x8000B02B</td><td>0x0000E50E</td></tr>
<tr><td>Munitions (Cluster Bomb VZ)</td><td>0x446E9D12</td><td>No</td><td>5874</td><td>0x8000B016</td><td>0x0000F714</td></tr>
<tr><td>Munitions (Cluster Bomb)</td><td>0x768E6A44</td><td>No</td><td>3143</td><td>0x80008E29</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions (Combat Air Patrol Al)</td><td>0x4DBD93DD</td><td>No</td><td>5888</td><td>0x8000B024</td><td>0x0000244B</td></tr>
<tr><td>Munitions (Combat Air Patrol Ch)</td><td>0x77F9645B</td><td>No</td><td>5879</td><td>0x8000B01B</td><td>0x00006572</td></tr>
<tr><td>Munitions (Combat Air Patrol)</td><td>0x47590DD6</td><td>No</td><td>2433</td><td>0x80008468</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions (Cruise Missile)</td><td>0x2B8222D5</td><td>No</td><td>3151</td><td>0x80008E31</td><td>0x0000C8F6</td></tr>
<tr><td>Munitions (Daisy Cutter Al)</td><td>0x456B6262</td><td>No</td><td>5889</td><td>0x8000B025</td><td>0x00003BFE</td></tr>
<tr><td>Munitions (Daisy Cutter)</td><td>0x7D29FEE3</td><td>No</td><td>3144</td><td>0x80008E2A</td><td>0x00007D03</td></tr>
<tr><td>Munitions (Fuel-Air Bomb Ch)</td><td>0x839F8C84</td><td>No</td><td>5880</td><td>0x8000B01C</td><td>0x000076A6</td></tr>
<tr><td>Munitions (Fuel-Air Bomb)</td><td>0xC55F371B</td><td>No</td><td>3145</td><td>0x80008E2B</td><td>0x00008828</td></tr>
<tr><td>Munitions (HARM)</td><td>0x8977BD24</td><td>No</td><td>3153</td><td>0x80008E33</td><td>0x00006FFB</td></tr>
<tr><td>Munitions (Laptop)</td><td>0x5DFA6876</td><td>No</td><td>5043</td><td>0x8000A3E0</td><td>0x000091B2</td></tr>
<tr><td>Munitions (Laser Guided Bomb Al)</td><td>0xA4056FFE</td><td>No</td><td>5890</td><td>0x8000B026</td><td>0x000051DB</td></tr>
<tr><td>Munitions (Laser Guided Bomb Ch)</td><td>0x47323650</td><td>No</td><td>5881</td><td>0x8000B01D</td><td>0x0000924F</td></tr>
<tr><td>Munitions (Laser Guided Bomb)</td><td>0xA1FEDF6F</td><td>No</td><td>2434</td><td>0x80008469</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions (MOAB)</td><td>0xCF23B9A5</td><td>No</td><td>3146</td><td>0x80008E2C</td><td>0x0000A695</td></tr>
<tr><td>Munitions (Rocket Artillery Ch)</td><td>0xBF0E49A1</td><td>No</td><td>5883</td><td>0x8000B01F</td><td>0x00003C43</td></tr>
<tr><td>Munitions (Rocket Artillery)</td><td>0x98EA2ECC</td><td>No</td><td>3147</td><td>0x80008E2D</td><td>0x00009E80</td></tr>
<tr><td>Munitions (Smart Bomb)</td><td>0x67D0E315</td><td>No</td><td>3154</td><td>0x80008E34</td><td>0x0001059D</td></tr>
<tr><td>Munitions (Strategic Missile)</td><td>0x3BCF38A2</td><td>No</td><td>3152</td><td>0x80008E32</td><td>0x000013E6</td></tr>
<tr><td>Munitions (Surgical Strike Al)</td><td>0x62C3BD57</td><td>No</td><td>5891</td><td>0x8000B027</td><td>0x000069B1</td></tr>
<tr><td>Munitions (Surgical Strike Ch)</td><td>0xC8602D19</td><td>No</td><td>5884</td><td>0x8000B020</td><td>0x00001CAE</td></tr>
<tr><td>Munitions (Surgical Strike)</td><td>0xB4F78D44</td><td>No</td><td>3148</td><td>0x80008E2E</td><td>0x00001FBC</td></tr>
<tr><td>Munitions (Tank Buster Al)</td><td>0xC17825EC</td><td>Yes</td><td>5892</td><td>0x8000B028</td><td>0x00008430</td></tr>
<tr><td>Munitions (Tank Buster Ch)</td><td>0xA80BDD22</td><td>Yes</td><td>5885</td><td>0x8000B021</td><td>0x0000D859</td></tr>
<tr><td>Munitions (Tank Buster VZ)</td><td>0x5B3B80D5</td><td>Yes</td><td>5875</td><td>0x8000B017</td><td>0x0001103F</td></tr>
<tr><td>Munitions (Tank Buster)</td><td>0x57EBF5C9</td><td>Yes</td><td>3149</td><td>0x80008E2F</td><td>0x000074C7</td></tr>
<tr><td>Munitions Spawner (Al Passcodes)</td><td>0x81BF38EA</td><td>No</td><td>3190</td><td>0x80008E66</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions Spawner (Al)</td><td>0x21104E27</td><td>No</td><td>3186</td><td>0x80008E62</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions Spawner (Ch)</td><td>0x86ACBDE9</td><td>No</td><td>3187</td><td>0x80008E63</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions Spawner (Default)</td><td>0xBDC66D51</td><td>No</td><td>2436</td><td>0x8000846B</td><td>0x0000868B</td></tr>
<tr><td>Munitions Spawner (Gr)</td><td>0x4CBD7F53</td><td>No</td><td>3188</td><td>0x80008E64</td><td>0x000034DA</td></tr>
<tr><td>Munitions Spawner (OC)</td><td>0xA5980AE4</td><td>No</td><td>5896</td><td>0x8000B02C</td><td>0x00013EAF</td></tr>
<tr><td>Munitions Spawner (VZ)</td><td>0x5DAB2762</td><td>No</td><td>3189</td><td>0x80008E65</td><td>0x0000E169</td></tr>
<tr><td>Munitions Spawnlist (Al Passcodes)</td><td>0x917C7A09</td><td>No</td><td>3185</td><td>0x80008E61</td><td>0x0000F6A1</td></tr>
<tr><td>Munitions Spawnlist (Al)</td><td>0xBED90AC0</td><td>No</td><td>3183</td><td>0x80008E5F</td><td>0x00001792</td></tr>
<tr><td>Munitions Spawnlist (Ch)</td><td>0x21613C2E</td><td>No</td><td>3182</td><td>0x80008E5E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions Spawnlist (Gr)</td><td>0x36548AB8</td><td>No</td><td>3184</td><td>0x80008E60</td><td>0xFFFFFFFF</td></tr>
<tr><td>Munitions Spawnlist (OC)</td><td>0x09B182B7</td><td>No</td><td>5893</td><td>0x8000B029</td><td>0x000091DD</td></tr>
<tr><td>Munitions Spawnlist (Test)</td><td>0x7FE13D29</td><td>No</td><td>2435</td><td>0x8000846A</td><td>0x0000567B</td></tr>
<tr><td>Munitions Spawnlist (VZ)</td><td>0x8828FF69</td><td>No</td><td>3180</td><td>0x80008E5C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Muzzle Flash (RR)</td><td>0x7EAC3B61</td><td>No</td><td>5826</td><td>0x8000AF85</td><td>0x00011114</td></tr>
<tr><td>New Template 0x80008a02</td><td>0x4E62D16C</td><td>No</td><td>2973</td><td>0x80008A02</td><td>0x0000FD92</td></tr>
<tr><td>New Template 0x80008a09</td><td>0xC84C382B</td><td>No</td><td>2980</td><td>0x80008A09</td><td>0xFFFFFFFF</td></tr>
<tr><td>New Template 0x800097ff</td><td>0xB8307A83</td><td>No</td><td>3845</td><td>0x800097FF</td><td>0xFFFFFFFF</td></tr>
<tr><td>New Template 0x8000b01e</td><td>0xF06FFCAF</td><td>No</td><td>5882</td><td>0x8000B01E</td><td>0x0000308F</td></tr>
<tr><td>New Terrain</td><td>0xC221E8F2</td><td>No</td><td>1032</td><td>0x80006911</td><td>0x000096EB</td></tr>
<tr><td>New Terrain (Large)</td><td>0x479273EC</td><td>No</td><td>1765</td><td>0x800075D7</td><td>0x000082AD</td></tr>
<tr><td>New Terrain (medium)</td><td>0xA40E7C64</td><td>No</td><td>1065</td><td>0x80006935</td><td>0x0000D08F</td></tr>
<tr><td>New Terrain (Small)</td><td>0x7B8D4CA4</td><td>No</td><td>780</td><td>0x80006226</td><td>0x0000D330</td></tr>
<tr><td>NGLV</td><td>0xAEE02F3A</td><td>No</td><td>3052</td><td>0x80008B85</td><td>0x00013F32</td></tr>
<tr><td>NGLV (GL)</td><td>0xD2EA92D0</td><td>No</td><td>3056</td><td>0x80008B89</td><td>0x0000C61B</td></tr>
<tr><td>NGLV (GL) (Driver)</td><td>0x4E0AF86F</td><td>No</td><td>3058</td><td>0x80008B8B</td><td>0x0000EDA5</td></tr>
<tr><td>NGLV (GL) (DriverGunner)</td><td>0x27A05248</td><td>No</td><td>3060</td><td>0x80008B8D</td><td>0x00001075</td></tr>
<tr><td>NGLV (GL) (Full)</td><td>0x782AE2A4</td><td>No</td><td>3064</td><td>0x80008B91</td><td>0x0000A860</td></tr>
<tr><td>NGLV (MG)</td><td>0xDBDEC16F</td><td>No</td><td>3053</td><td>0x80008B86</td><td>0x0001189D</td></tr>
<tr><td>NGLV (MG) (Driver)</td><td>0x909DD79A</td><td>No</td><td>3057</td><td>0x80008B8A</td><td>0x00010BB8</td></tr>
<tr><td>NGLV (MG) (DriverGunner)</td><td>0x69264E99</td><td>No</td><td>3059</td><td>0x80008B8C</td><td>0x000136ED</td></tr>
<tr><td>NGLV (MG) (Full)</td><td>0x48E47D59</td><td>No</td><td>3063</td><td>0x80008B90</td><td>0x0000A64A</td></tr>
<tr><td>NGLV_Driver</td><td>0x2EB0A1EB</td><td>No</td><td>5065</td><td>0x8000A3FE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Night Vision Elite</td><td>0xCF703D6A</td><td>No</td><td>2293</td><td>0x800082B7</td><td>0x000002B8</td></tr>
<tr><td>NM SS</td><td>0xC353AD20</td><td>No</td><td>2904</td><td>0x8000893B</td><td>0x00003E8E</td></tr>
<tr><td>Nuclear Bunker Buster Projectile</td><td>0x4BBAE398</td><td>No</td><td>4875</td><td>0x8000A258</td><td>0x00013D73</td></tr>
<tr><td>OC</td><td>0xE947B797</td><td>No</td><td>490</td><td>0x800056C5</td><td>0x000084F2</td></tr>
<tr><td>OC Board Member</td><td>0x164999FF</td><td>No</td><td>2311</td><td>0x800082CA</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Boss</td><td>0x5885B432</td><td>No</td><td>820</td><td>0x80006323</td><td>0x00010948</td></tr>
<tr><td>OC Boss (phone)</td><td>0xBD427E13</td><td>No</td><td>816</td><td>0x80006254</td><td>0x0000F19C</td></tr>
<tr><td>OC Boss Phone</td><td>0x4FF6C2FE</td><td>No</td><td>1943</td><td>0x80007E8F</td><td>0x00000DE8</td></tr>
<tr><td>OC Defender (AA)</td><td>0xE6653D0B</td><td>No</td><td>5041</td><td>0x8000A3DE</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Defender (AT)</td><td>0x5412C040</td><td>No</td><td>5024</td><td>0x8000A3CD</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Defender (AT) (Window Spawner)</td><td>0x5D885C09</td><td>No</td><td>3007</td><td>0x80008A27</td><td>0x00013EC9</td></tr>
<tr><td>OC Defender (MG)</td><td>0xA8573F8D</td><td>No</td><td>5025</td><td>0x8000A3CE</td><td>0x0000B6A5</td></tr>
<tr><td>OC Defender (Rifle)</td><td>0x5F9983AF</td><td>No</td><td>5023</td><td>0x8000A3CC</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Defender (Sniper)</td><td>0x02CC7BAE</td><td>No</td><td>5026</td><td>0x8000A3CF</td><td>0x0000EACD</td></tr>
<tr><td>OC Elite</td><td>0x3225BF3A</td><td>No</td><td>990</td><td>0x8000687B</td><td>0x00011632</td></tr>
<tr><td>OC Exec Box</td><td>0x997A0FF5</td><td>No</td><td>2673</td><td>0x80008679</td><td>0x0000B894</td></tr>
<tr><td>OC Executive</td><td>0xE0428861</td><td>No</td><td>1327</td><td>0x80006E50</td><td>0x00011372</td></tr>
<tr><td>OC Executive (Armed)</td><td>0x8962059B</td><td>No</td><td>2542</td><td>0x8000856B</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Executive (Box)</td><td>0x31A786AD</td><td>No</td><td>2672</td><td>0x80008678</td><td>0x00003668</td></tr>
<tr><td>OC Executive (Crying)</td><td>0xD3817D3E</td><td>No</td><td>1945</td><td>0x80007E91</td><td>0x000054EB</td></tr>
<tr><td>OC Executive (Female)</td><td>0xDDAF8A12</td><td>No</td><td>1328</td><td>0x80006E51</td><td>0x0000B6EB</td></tr>
<tr><td>OC Executive (OilCon002_Hostage)</td><td>0xA25CDC6C</td><td>No</td><td>5915</td><td>0x8000B0CD</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Executive (Phone)</td><td>0x8B29C584</td><td>No</td><td>1938</td><td>0x80007E02</td><td>0x0000DFAD</td></tr>
<tr><td>OC Executive (Shredder)</td><td>0x76B9F9CF</td><td>No</td><td>1944</td><td>0x80007E90</td><td>0x00004825</td></tr>
<tr><td>OC Firefighter</td><td>0xF63D05CC</td><td>No</td><td>2315</td><td>0x800082CF</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Heavy (Grenade Launcher)</td><td>0x4A53C685</td><td>No</td><td>1346</td><td>0x80006EBB</td><td>0x000051DD</td></tr>
<tr><td>OC Heavy (Light MG)</td><td>0x15348807</td><td>No</td><td>989</td><td>0x80006879</td><td>0x0000B973</td></tr>
<tr><td>OC Heavy (RPG)</td><td>0x35DF2250</td><td>No</td><td>1103</td><td>0x80006AD9</td><td>0x00009B43</td></tr>
<tr><td>OC Lifestyle Starter</td><td>0x77547833</td><td>No</td><td>2165</td><td>0x800081BF</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Officer</td><td>0xA68AA209</td><td>No</td><td>1326</td><td>0x80006E4D</td><td>0x000011E8</td></tr>
<tr><td>OC Pilot</td><td>0x42552FF1</td><td>No</td><td>2314</td><td>0x800082CE</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Prisoner</td><td>0x0F073CB1</td><td>No</td><td>2368</td><td>0x80008323</td><td>0x00007372</td></tr>
<tr><td>OC Sniper</td><td>0x07E46DF4</td><td>No</td><td>1347</td><td>0x80006EBC</td><td>0x00007ED3</td></tr>
<tr><td>OC Soldier</td><td>0x07B00AAD</td><td>No</td><td>514</td><td>0x800056E4</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Soldier (Bench Press)</td><td>0xBB217A61</td><td>No</td><td>2532</td><td>0x8000855E</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Soldier (God)</td><td>0xEDD00DA2</td><td>No</td><td>5839</td><td>0x8000AF94</td><td>0x00004EA6</td></tr>
<tr><td>OC Soldier (Saunter)</td><td>0x8E0FD15E</td><td>No</td><td>1937</td><td>0x80007E01</td><td>0x0000B684</td></tr>
<tr><td>OC Starter 1</td><td>0x05323547</td><td>No</td><td>2331</td><td>0x800082E2</td><td>0x00013845</td></tr>
<tr><td>OC Starter 2</td><td>0xDB3431C0</td><td>No</td><td>2332</td><td>0x800082E3</td><td>0x0000601D</td></tr>
<tr><td>OC Starter 3</td><td>0x0536B275</td><td>No</td><td>2333</td><td>0x800082E4</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Starter 4</td><td>0xFB255996</td><td>No</td><td>2334</td><td>0x800082E5</td><td>0x00000593</td></tr>
<tr><td>OC Starters</td><td>0x10120EDD</td><td>No</td><td>2164</td><td>0x800081BE</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Tank Commander</td><td>0xD0F85B6F</td><td>Yes</td><td>2313</td><td>0x800082CD</td><td>0xFFFFFFFF</td></tr>
<tr><td>OC Worker</td><td>0x2D571F27</td><td>No</td><td>2312</td><td>0x800082CC</td><td>0x0000F3EC</td></tr>
<tr><td>OCDepotWarehouseSpawner</td><td>0x2D530F48</td><td>No</td><td>5149</td><td>0x8000A487</td><td>0xFFFFFFFF</td></tr>
<tr><td>OCHQ Paper</td><td>0xAA9D345C</td><td>No</td><td>2291</td><td>0x8000824F</td><td>0x0000D29E</td></tr>
<tr><td>OCHQSpawnList</td><td>0x6C57EA0B</td><td>No</td><td>1507</td><td>0x80007042</td><td>0xFFFFFFFF</td></tr>
<tr><td>OCHQVehicleSpawnList</td><td>0xCC4C5D33</td><td>No</td><td>1934</td><td>0x80007DF7</td><td>0x000084CF</td></tr>
<tr><td>OCMercSpawnList</td><td>0x134119C9</td><td>No</td><td>1940</td><td>0x80007E06</td><td>0x00009054</td></tr>
<tr><td>OCPedTraffic</td><td>0x3A988AAD</td><td>No</td><td>2082</td><td>0x80008153</td><td>0xFFFFFFFF</td></tr>
<tr><td>OCVehTraffic</td><td>0xAFD1C1E3</td><td>No</td><td>2083</td><td>0x80008154</td><td>0x0000AE58</td></tr>
<tr><td>Offroad Motorcycle (AI ONLY)</td><td>0xF6B714A8</td><td>Yes</td><td>5106</td><td>0x8000A44D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Offroad Motorcycle (AL)</td><td>0xA52A5783</td><td>Yes</td><td>824</td><td>0x8000637F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Offroad Motorcycle (AL) (Driver)</td><td>0x3975175E</td><td>Yes</td><td>830</td><td>0x80006385</td><td>0xFFFFFFFF</td></tr>
<tr><td>Offroad Motorcycle (GR)</td><td>0xFE3B86CF</td><td>Yes</td><td>825</td><td>0x80006380</td><td>0xFFFFFFFF</td></tr>
<tr><td>Offroad Motorcycle (GR) (Driver)</td><td>0x82F76DFA</td><td>Yes</td><td>828</td><td>0x80006383</td><td>0xFFFFFFFF</td></tr>
<tr><td>OffroadMotorcycle_Driver</td><td>0x1E0A049E</td><td>Yes</td><td>5385</td><td>0x8000A979</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ofroad Motorcycle</td><td>0x1AE863DB</td><td>Yes</td><td>823</td><td>0x8000637E</td><td>0x0000B4E9</td></tr>
<tr><td>Oil Tanker (OC)</td><td>0x73554933</td><td>Yes</td><td>3209</td><td>0x80008EFB</td><td>0xFFFFFFFF</td></tr>
<tr><td>OilCon020_Carbine</td><td>0x768BB7FE</td><td>No</td><td>4029</td><td>0x80009A16</td><td>0x0001402A</td></tr>
<tr><td>OilCon020_Carbine_b</td><td>0x2DEED175</td><td>No</td><td>4032</td><td>0x80009A1C</td><td>0x00013A64</td></tr>
<tr><td>OilDbSpawner</td><td>0xF10AD117</td><td>No</td><td>2380</td><td>0x80008338</td><td>0x00006C4C</td></tr>
<tr><td>OilDbSpawner (Squad Full AT)</td><td>0x9EC1D98A</td><td>No</td><td>5665</td><td>0x8000ACA8</td><td>0xFFFFFFFF</td></tr>
<tr><td>OilDbSpawner (Squad Half AT)</td><td>0xE672B662</td><td>No</td><td>5666</td><td>0x8000ACA9</td><td>0x0000865D</td></tr>
<tr><td>OilDbSpawner (Squad Quarter AT)</td><td>0xA4607BBF</td><td>No</td><td>5911</td><td>0x8000B03E</td><td>0xFFFFFFFF</td></tr>
<tr><td>OilDbSpawner (Squad)</td><td>0x5F97BBDC</td><td>No</td><td>3016</td><td>0x80008A30</td><td>0xFFFFFFFF</td></tr>
<tr><td>OilHq_Interior</td><td>0x3FAAFEE5</td><td>No</td><td>1914</td><td>0x80007A03</td><td>0x00006C5F</td></tr>
<tr><td>oilrig</td><td>0x7ED017FB</td><td>No</td><td>393</td><td>0x8000556E</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig buildings</td><td>0x8ED2A0D4</td><td>No</td><td>395</td><td>0x80005570</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_att_anchorlinegrillA</td><td>0x9D98438E</td><td>No</td><td>726</td><td>0x800061E5</td><td>0x0000582B</td></tr>
<tr><td>oilrig_att_anchorlinespindleA</td><td>0x3C05E445</td><td>No</td><td>403</td><td>0x80005579</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_att_BuildingDpipe</td><td>0x2CC316D6</td><td>No</td><td>773</td><td>0x8000621E</td><td>0x00012019</td></tr>
<tr><td>oilrig_att_dockingrampA</td><td>0x7B5578A2</td><td>No</td><td>399</td><td>0x80005575</td><td>0x000095D9</td></tr>
<tr><td>oilrig_att_dockingrampB</td><td>0xFD5D010D</td><td>No</td><td>754</td><td>0x80006206</td><td>0x0000C9F1</td></tr>
<tr><td>oilrig_att_ductdisposalA</td><td>0x2C874C90</td><td>No</td><td>408</td><td>0x80005580</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_att_pipeblowout</td><td>0x8E4E954A</td><td>No</td><td>740</td><td>0x800061F6</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_att_towerdrillpipesA</td><td>0xF021B3A4</td><td>No</td><td>770</td><td>0x8000621B</td><td>0x0000B63D</td></tr>
<tr><td>oilrig_att_towerdrillpipesB</td><td>0x0A1F9DFB</td><td>No</td><td>771</td><td>0x8000621C</td><td>0x0000CD23</td></tr>
<tr><td>oilrig_bld_buildingA</td><td>0xD23F52FC</td><td>No</td><td>406</td><td>0x8000557C</td><td>0x000076E0</td></tr>
<tr><td>oilrig_bld_buildingB</td><td>0xAC3CD893</td><td>No</td><td>409</td><td>0x80005581</td><td>0x0000EB55</td></tr>
<tr><td>oilrig_bld_buildingBB</td><td>0x3D7B1AD3</td><td>No</td><td>404</td><td>0x8000557A</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_bld_buildingC</td><td>0xCA3AC936</td><td>No</td><td>400</td><td>0x80005576</td><td>0x0001112F</td></tr>
<tr><td>oilrig_bld_buildingD</td><td>0xD44C2215</td><td>No</td><td>396</td><td>0x80005571</td><td>0x00000D7C</td></tr>
<tr><td>oilrig_bld_helipadlargeA</td><td>0x4DDC8DF8</td><td>Yes</td><td>398</td><td>0x80005573</td><td>0x00007586</td></tr>
<tr><td>oilrig_catwalkA</td><td>0xC2EEF876</td><td>No</td><td>725</td><td>0x800061E4</td><td>0x00007A74</td></tr>
<tr><td>oilrig_catwalkB</td><td>0x44F680E1</td><td>No</td><td>402</td><td>0x80005578</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_catwalkC</td><td>0xCAF3823C</td><td>No</td><td>410</td><td>0x80005582</td><td>0x00004853</td></tr>
<tr><td>oilrig_catwalkD</td><td>0x4CFB0AA7</td><td>No</td><td>727</td><td>0x800061E6</td><td>0x0001177E</td></tr>
<tr><td>oilrig_cranelargeA</td><td>0x16970F43</td><td>No</td><td>729</td><td>0x800061E9</td><td>0x00009877</td></tr>
<tr><td>oilrig_cranesmallA</td><td>0x3925E07B</td><td>No</td><td>728</td><td>0x800061E8</td><td>0x00006604</td></tr>
<tr><td>oilrig_radiojammer</td><td>0x786ECF9F</td><td>No</td><td>732</td><td>0x800061ED</td><td>0x0000D619</td></tr>
<tr><td>oilrig_radiojammer_ruined</td><td>0xB96B4243</td><td>No</td><td>5225</td><td>0x8000A694</td><td>0x00010D0A</td></tr>
<tr><td>oilrig_scaffold</td><td>0x68B59E68</td><td>No</td><td>405</td><td>0x8000557B</td><td>0x0000081B</td></tr>
<tr><td>oilrig_simple</td><td>0x618526A4</td><td>No</td><td>748</td><td>0x800061FF</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_simple_ruined</td><td>0x9C06A4B2</td><td>No</td><td>4137</td><td>0x80009B35</td><td>0x00004C6E</td></tr>
<tr><td>oilrig_smokestack</td><td>0x9A6F6587</td><td>No</td><td>734</td><td>0x800061EF</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_stairwellA</td><td>0xFA1394CE</td><td>No</td><td>735</td><td>0x800061F0</td><td>0x0001213F</td></tr>
<tr><td>oilrig_stairwellB</td><td>0x5C1AEAD9</td><td>No</td><td>736</td><td>0x800061F1</td><td>0x00012195</td></tr>
<tr><td>oilrig_stairwellC</td><td>0x02181E94</td><td>No</td><td>737</td><td>0x800061F2</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_stairwellD</td><td>0x641F749F</td><td>No</td><td>738</td><td>0x800061F3</td><td>0x0000BBB9</td></tr>
<tr><td>oilrig_stairwellE</td><td>0x821D6542</td><td>No</td><td>749</td><td>0x80006201</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_stairwellF</td><td>0x0424EDAD</td><td>No</td><td>750</td><td>0x80006202</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_stairwellG</td><td>0xDA226CF8</td><td>No</td><td>751</td><td>0x80006203</td><td>0xFFFFFFFF</td></tr>
<tr><td>oilrig_stairwellH</td><td>0xFC295E43</td><td>No</td><td>731</td><td>0x800061EB</td><td>0x0000B499</td></tr>
<tr><td>oilrig_towerblowoutdiagonal</td><td>0x8566262E</td><td>No</td><td>397</td><td>0x80005572</td><td>0x000026A5</td></tr>
<tr><td>oilrig_towerblowoutlargeA</td><td>0xBD858E29</td><td>No</td><td>739</td><td>0x800061F4</td><td>0x0000542F</td></tr>
<tr><td>oilrig_towerblowoutsmallA</td><td>0xE85D130D</td><td>No</td><td>730</td><td>0x800061EA</td><td>0x00009D96</td></tr>
<tr><td>oilrig_towerdrill</td><td>0x299798D8</td><td>No</td><td>401</td><td>0x80005577</td><td>0x000121F3</td></tr>
<tr><td>OilrigDebris</td><td>0x2E56EC4A</td><td>No</td><td>413</td><td>0x80005589</td><td>0x0000251E</td></tr>
<tr><td>OilrigDebrisLarge</td><td>0x6A3605FB</td><td>No</td><td>756</td><td>0x8000620C</td><td>0xFFFFFFFF</td></tr>
<tr><td>OilrigDebrisLong</td><td>0xA301CD08</td><td>No</td><td>777</td><td>0x80006222</td><td>0x00009FFF</td></tr>
<tr><td>OilrigDebrisMedium</td><td>0xA53995D3</td><td>No</td><td>759</td><td>0x8000620F</td><td>0x000014CD</td></tr>
<tr><td>OilrigDebrisMediumFloat</td><td>0x29DF5B4F</td><td>No</td><td>757</td><td>0x8000620D</td><td>0xFFFFFFFF</td></tr>
<tr><td>OilrigDebrisSmall</td><td>0xEFD97A93</td><td>No</td><td>758</td><td>0x8000620E</td><td>0x000016DA</td></tr>
<tr><td>OLD DO NOT USE gr_veh_tank_m551sheridan</td><td>0x22682C0C</td><td>Yes</td><td>1079</td><td>0x80006A1A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Omen</td><td>0xCB516D9C</td><td>No</td><td>835</td><td>0x80006390</td><td>0x0000E2FE</td></tr>
<tr><td>Omen (Driver)</td><td>0x53DF6F5B</td><td>No</td><td>1764</td><td>0x800075D6</td><td>0x00002FA1</td></tr>
<tr><td>Omen (Full)</td><td>0x39546958</td><td>No</td><td>3683</td><td>0x80009532</td><td>0xFFFFFFFF</td></tr>
<tr><td>Omen (Full) (OC)</td><td>0x195C2497</td><td>No</td><td>4363</td><td>0x80009D37</td><td>0x00007C87</td></tr>
<tr><td>Omen (OC) (DriverGunner)</td><td>0xA6E1016D</td><td>No</td><td>4030</td><td>0x80009A19</td><td>0xFFFFFFFF</td></tr>
<tr><td>Opentop Trailer</td><td>0x6F4EE91B</td><td>No</td><td>4011</td><td>0x800099A1</td><td>0xFFFFFFFF</td></tr>
<tr><td>OutskirtsTraffic</td><td>0x3ED61736</td><td>No</td><td>1503</td><td>0x8000703A</td><td>0x000058CC</td></tr>
<tr><td>OutskirtTrafficZone</td><td>0x7582021D</td><td>No</td><td>547</td><td>0x80005B9C</td><td>0x0000CFD7</td></tr>
<tr><td>PalmTreeDebrisTemplate</td><td>0x53FE886A</td><td>No</td><td>3698</td><td>0x8000954F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Panel Damage (Car)</td><td>0x18D60B8B</td><td>No</td><td>55</td><td>0x8000464C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Panhard</td><td>0x47924871</td><td>No</td><td>4691</td><td>0x80009FF8</td><td>0x000109B0</td></tr>
<tr><td>Panhard (Assault)</td><td>0x449BB52B</td><td>No</td><td>2587</td><td>0x800085E0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Panhard (base)</td><td>0xD3D29EAF</td><td>No</td><td>2545</td><td>0x800085AB</td><td>0x00007C07</td></tr>
<tr><td>Panhard_Driver</td><td>0xDBCF4D8A</td><td>No</td><td>5114</td><td>0x8000A458</td><td>0xFFFFFFFF</td></tr>
<tr><td>ParachuteA</td><td>0x61024957</td><td>No</td><td>5500</td><td>0x8000AAB9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Paradrop Location (AL)</td><td>0xA34D87BB</td><td>No</td><td>5010</td><td>0x8000A3BE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Paradrop Location (CH)</td><td>0x2BEE94C5</td><td>No</td><td>5009</td><td>0x8000A3BD</td><td>0xFFFFFFFF</td></tr>
<tr><td>ParkedCarList</td><td>0x7901B2E0</td><td>No</td><td>3098</td><td>0x80008BB6</td><td>0x00013D6D</td></tr>
<tr><td>ParkingSpawner</td><td>0x361E6E2D</td><td>No</td><td>3097</td><td>0x80008BB5</td><td>0x0000C854</td></tr>
<tr><td>PathSpawner1</td><td>0x107FF8ED</td><td>No</td><td>3099</td><td>0x80008BB7</td><td>0x0000AF64</td></tr>
<tr><td>PathSpawner_AlliedHQ_PedList</td><td>0x5A4D3ABD</td><td>No</td><td>5638</td><td>0x8000AC88</td><td>0x0000EF58</td></tr>
<tr><td>PathSpawner_Boat_Amazon_Act1</td><td>0xEA6FF3F2</td><td>Yes</td><td>5632</td><td>0x8000AC82</td><td>0x0000704F</td></tr>
<tr><td>PathSpawner_Boat_Amazon_Act2</td><td>0x6C777C5D</td><td>Yes</td><td>5939</td><td>0x8000B1E0</td><td>0x00012E10</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act1_A</td><td>0xD326695A</td><td>Yes</td><td>5182</td><td>0x8000A4AD</td><td>0x00005564</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act1_B</td><td>0x352DBF65</td><td>Yes</td><td>5183</td><td>0x8000A4AE</td><td>0x00012400</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act1_C</td><td>0xCB2AD9F0</td><td>Yes</td><td>5184</td><td>0x8000A4AF</td><td>0x000072E7</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act2_Allied</td><td>0xD9C80A41</td><td>Yes</td><td>5186</td><td>0x8000A4B1</td><td>0x0000191C</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act2_China</td><td>0xDEF109A9</td><td>Yes</td><td>5189</td><td>0x8000A4B4</td><td>0x00006367</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act3_Allied</td><td>0x4F90EB72</td><td>Yes</td><td>5614</td><td>0x8000AC6F</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_Boat_Car_City_Act3_China</td><td>0x93E6C2C0</td><td>Yes</td><td>5190</td><td>0x8000A4B5</td><td>0x000045FE</td></tr>
<tr><td>PathSpawner_Boat_Cumana_Act1_A</td><td>0xC234DE49</td><td>Yes</td><td>5617</td><td>0x8000AC72</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_Boat_Cumana_Act1_B</td><td>0x202D237E</td><td>Yes</td><td>5618</td><td>0x8000AC73</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_Boat_Cumana_Act1_C</td><td>0x422F979B</td><td>Yes</td><td>5619</td><td>0x8000AC74</td><td>0x00013B2E</td></tr>
<tr><td>PathSpawner_Boat_Cumana_Act2_China</td><td>0xB5651806</td><td>Yes</td><td>5622</td><td>0x8000AC77</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_Boat_JungleMtn_Act1</td><td>0xF7D0FF94</td><td>Yes</td><td>5631</td><td>0x8000AC81</td><td>0x000084C0</td></tr>
<tr><td>PathSpawner_Boat_JungleMtn_Act2</td><td>0xD1CE852B</td><td>Yes</td><td>5937</td><td>0x8000B1DE</td><td>0x0000531E</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act1_A</td><td>0x2C56E3D4</td><td>Yes</td><td>3101</td><td>0x80008BB9</td><td>0x00011850</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act1_B</td><td>0x0654696B</td><td>Yes</td><td>5176</td><td>0x8000A4A7</td><td>0x000047F5</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act1_C</td><td>0x24525A0E</td><td>Yes</td><td>5177</td><td>0x8000A4A8</td><td>0x000064BC</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act1_D</td><td>0x2E63B2ED</td><td>Yes</td><td>5178</td><td>0x8000A4A9</td><td>0x00010856</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act2</td><td>0x82E10253</td><td>Yes</td><td>5175</td><td>0x8000A4A6</td><td>0x00003F3E</td></tr>
<tr><td>PathSpawner_Boat_Mar_City_Act3</td><td>0xA0DEF2F6</td><td>Yes</td><td>5180</td><td>0x8000A4AB</td><td>0x00011C31</td></tr>
<tr><td>PathSpawner_Boat_Merida_Act1</td><td>0x2783AD86</td><td>Yes</td><td>5624</td><td>0x8000AC79</td><td>0x0000EA37</td></tr>
<tr><td>PathSpawner_Boat_Merida_Act2</td><td>0xA98B35F1</td><td>Yes</td><td>5628</td><td>0x8000AC7E</td><td>0x000040DC</td></tr>
<tr><td>PathSpawner_Boat_OC_Depot_Act1</td><td>0x49FFA4B5</td><td>Yes</td><td>5634</td><td>0x8000AC84</td><td>0x0000B662</td></tr>
<tr><td>PathSpawner_Boat_PirateIsles_Act1_A</td><td>0xD45B17A5</td><td>Yes</td><td>5963</td><td>0x8000B2D8</td><td>0x0000CED9</td></tr>
<tr><td>PathSpawner_ChiHQ_PedList</td><td>0x34E8DA10</td><td>No</td><td>5933</td><td>0x8000B1DA</td><td>0x0000D6A9</td></tr>
<tr><td>PathSpawner_GurHQ_PedList</td><td>0x2E9E9CD8</td><td>No</td><td>5930</td><td>0x8000B1D4</td><td>0x0000FE2C</td></tr>
<tr><td>PathSpawner_GurHQ_VehList</td><td>0x76FC6D8A</td><td>Yes</td><td>5929</td><td>0x8000B1D3</td><td>0x00009543</td></tr>
<tr><td>PathSpawner_Heli_Car_City_Act1</td><td>0x502D8994</td><td>Yes</td><td>5185</td><td>0x8000A4B0</td><td>0x000006A8</td></tr>
<tr><td>PathSpawner_Heli_Car_City_Act2</td><td>0x2A2B0F2B</td><td>Yes</td><td>5187</td><td>0x8000A4B2</td><td>0x00003B69</td></tr>
<tr><td>PathSpawner_Heli_Car_City_Act3_Allied</td><td>0x1B4FA27C</td><td>Yes</td><td>5615</td><td>0x8000AC70</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_Heli_Car_City_Act3_China</td><td>0x05CC2646</td><td>Yes</td><td>5616</td><td>0x8000AC71</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_Heli_Cumana_Act1_China</td><td>0xE03AF933</td><td>Yes</td><td>5620</td><td>0x8000AC75</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_Heli_Cumana_Act2_China</td><td>0xF217B55C</td><td>Yes</td><td>5621</td><td>0x8000AC76</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_Heli_JungleMtn_Act1</td><td>0xB17B15DE</td><td>Yes</td><td>5630</td><td>0x8000AC80</td><td>0x0000B033</td></tr>
<tr><td>PathSpawner_Heli_Mar_City_Act1</td><td>0xA0B53D36</td><td>Yes</td><td>3103</td><td>0x80008BBB</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_Heli_Mar_City_Act2</td><td>0x22BCC5A1</td><td>Yes</td><td>5179</td><td>0x8000A4AA</td><td>0x00012F2D</td></tr>
<tr><td>PathSpawner_Heli_Mar_City_Act3</td><td>0xA8B9C6FC</td><td>Yes</td><td>5181</td><td>0x8000A4AC</td><td>0x00001B15</td></tr>
<tr><td>PathSpawner_Heli_Merida_Act1</td><td>0x51B9C050</td><td>Yes</td><td>5623</td><td>0x8000AC78</td><td>0x00007D69</td></tr>
<tr><td>PathSpawner_Heli_Merida_Act2</td><td>0x3BB75F17</td><td>Yes</td><td>5625</td><td>0x8000AC7A</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_OCHQ_Depot_PedList</td><td>0x50B01295</td><td>No</td><td>5644</td><td>0x8000AC8F</td><td>0x0000D628</td></tr>
<tr><td>PathSpawner_Pirate_Jetski</td><td>0x4D147C27</td><td>No</td><td>5952</td><td>0x8000B1EE</td><td>0x00013A1E</td></tr>
<tr><td>PathSpawner_Pirate_VehList</td><td>0x8EC67A18</td><td>Yes</td><td>5950</td><td>0x8000B1EC</td><td>0x0000F74A</td></tr>
<tr><td>PathSpawner_PirateHQ_PedList</td><td>0x6B567E2B</td><td>No</td><td>5645</td><td>0x8000AC92</td><td>0x0000FBE1</td></tr>
<tr><td>PathSpawner_PMC001_Stairs01</td><td>0x4811DE86</td><td>No</td><td>2539</td><td>0x80008566</td><td>0x00008ECC</td></tr>
<tr><td>PathSpawner_VZCon001_M151</td><td>0x351C54B5</td><td>Yes</td><td>5944</td><td>0x8000B1E6</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawner_VZCon001_PedList</td><td>0xF61AA94C</td><td>No</td><td>5942</td><td>0x8000B1E4</td><td>0xFFFFFFFF</td></tr>
<tr><td>PathSpawners</td><td>0xEFDBE59F</td><td>No</td><td>3102</td><td>0x80008BBA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Patrol Boat (base)</td><td>0x74FC9169</td><td>Yes</td><td>4687</td><td>0x80009FF3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Patrol Boat (PMC)</td><td>0x1D9FC746</td><td>Yes</td><td>2584</td><td>0x800085DD</td><td>0xFFFFFFFF</td></tr>
<tr><td>Patrol Boat (PMC) (Driver)</td><td>0x180E875D</td><td>Yes</td><td>4682</td><td>0x80009FED</td><td>0xFFFFFFFF</td></tr>
<tr><td>Patrol Boat (VZ)</td><td>0xBB5331F4</td><td>Yes</td><td>2586</td><td>0x800085DF</td><td>0x00013F58</td></tr>
<tr><td>Patrol Boat (VZ) (Driver)</td><td>0x9D326D53</td><td>Yes</td><td>4705</td><td>0x8000A00B</td><td>0x0000D6F5</td></tr>
<tr><td>Patrol Boat (VZ) (DriverGunners)</td><td>0xD749939B</td><td>Yes</td><td>5536</td><td>0x8000AB47</td><td>0x0001258F</td></tr>
<tr><td>Patrol Boat (VZ) (Full)</td><td>0x26BC0400</td><td>Yes</td><td>4713</td><td>0x8000A013</td><td>0xFFFFFFFF</td></tr>
<tr><td>Patrolboat_Driver</td><td>0x918E1442</td><td>Yes</td><td>5087</td><td>0x8000A416</td><td>0x0000BCF3</td></tr>
<tr><td>PatrolboatVZ_Driver</td><td>0x915322FE</td><td>Yes</td><td>5102</td><td>0x8000A427</td><td>0xFFFFFFFF</td></tr>
<tr><td>PatrolSpawner</td><td>0xD7D9C119</td><td>No</td><td>3081</td><td>0x80008BA5</td><td>0xFFFFFFFF</td></tr>
<tr><td>PD Soldier</td><td>0xD18E58CB</td><td>No</td><td>34</td><td>0x80004384</td><td>0x000019E4</td></tr>
<tr><td>PDA</td><td>0xFA62754E</td><td>No</td><td>4049</td><td>0x80009AD9</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_AllCon002_Traffic</td><td>0x94BDB230</td><td>No</td><td>4366</td><td>0x80009D3D</td><td>0x00002E61</td></tr>
<tr><td>PedList_AlliedHQ_Paths</td><td>0xA9BB4F26</td><td>No</td><td>5637</td><td>0x8000AC87</td><td>0x00009042</td></tr>
<tr><td>PedList_AllJob001</td><td>0x28D493F2</td><td>No</td><td>4367</td><td>0x80009D3E</td><td>0x0000C646</td></tr>
<tr><td>PedList_Amazon_Act1</td><td>0xAE54EA83</td><td>No</td><td>4349</td><td>0x80009D21</td><td>0x0000DD1F</td></tr>
<tr><td>PedList_Amazon_AllJob002_i_Act1</td><td>0xE634825C</td><td>No</td><td>4351</td><td>0x80009D23</td><td>0x0000B34E</td></tr>
<tr><td>PedList_Blank</td><td>0x2C5096CB</td><td>No</td><td>2393</td><td>0x80008387</td><td>0x000106D2</td></tr>
<tr><td>PedList_Car_Big_Act1</td><td>0xBCFC6CE6</td><td>No</td><td>4344</td><td>0x80009D1C</td><td>0x0000EBAF</td></tr>
<tr><td>PedList_Car_City_Act1</td><td>0xE27F610F</td><td>No</td><td>4336</td><td>0x80009D13</td><td>0x0000BF1D</td></tr>
<tr><td>PedList_Car_City_Act2ALL</td><td>0xF3F707B9</td><td>No</td><td>5170</td><td>0x8000A49F</td><td>0x0000F2CE</td></tr>
<tr><td>PedList_Car_City_Act2CHI</td><td>0x52E973E6</td><td>No</td><td>5171</td><td>0x8000A4A0</td><td>0x00009047</td></tr>
<tr><td>PedList_Car_City_Act3ALL</td><td>0x36FED14A</td><td>No</td><td>4373</td><td>0x80009D49</td><td>0x0000D99F</td></tr>
<tr><td>PedList_Car_City_Act3CHI</td><td>0x7581CD7D</td><td>No</td><td>4391</td><td>0x80009D5F</td><td>0x00001AEB</td></tr>
<tr><td>PedList_Car_Dock_Act1</td><td>0x4C179CFF</td><td>No</td><td>4337</td><td>0x80009D14</td><td>0x000124A0</td></tr>
<tr><td>PedList_Car_Estate_Act1</td><td>0x5A8CF76C</td><td>No</td><td>4333</td><td>0x80009D10</td><td>0x0000647F</td></tr>
<tr><td>PedList_Car_Shanty_Act1</td><td>0xAD11F307</td><td>No</td><td>4331</td><td>0x80009D0E</td><td>0x00004957</td></tr>
<tr><td>PedList_ChiHQ_Paths</td><td>0x6E079873</td><td>No</td><td>5931</td><td>0x8000B1D8</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_Cumana_act1ALL</td><td>0x5E724CE9</td><td>No</td><td>5173</td><td>0x8000A4A2</td><td>0x000118F9</td></tr>
<tr><td>PedList_Cumana_Act1CHI</td><td>0xBD64B916</td><td>No</td><td>5174</td><td>0x8000A4A3</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_Cumana_act2ALL</td><td>0x17B486D0</td><td>No</td><td>4376</td><td>0x80009D4C</td><td>0x00012A46</td></tr>
<tr><td>PedList_Cumana_act2CHI</td><td>0x19426E67</td><td>No</td><td>4377</td><td>0x80009D4D</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_Cumana_City_Act1</td><td>0xE591C396</td><td>No</td><td>4357</td><td>0x80009D2A</td><td>0x000094B6</td></tr>
<tr><td>PedList_Cumana_Outskirts_Act1</td><td>0x23D326B7</td><td>No</td><td>4355</td><td>0x80009D27</td><td>0x00012FE3</td></tr>
<tr><td>PedList_Guanare_Act1</td><td>0xAD750756</td><td>No</td><td>4346</td><td>0x80009D1E</td><td>0x00013B88</td></tr>
<tr><td>PedList_Guanare_Big_Act1</td><td>0x20BCB8BB</td><td>No</td><td>4347</td><td>0x80009D1F</td><td>0x00009CE4</td></tr>
<tr><td>PedList_GurHQ_Paths</td><td>0xDFDBF3CB</td><td>No</td><td>3794</td><td>0x800097AF</td><td>0x0000E122</td></tr>
<tr><td>PedList_JungleMtnA_Act1</td><td>0x00E37D92</td><td>No</td><td>4329</td><td>0x80009D0C</td><td>0x00000DCA</td></tr>
<tr><td>PedList_JungleMtnB_Act1</td><td>0x32B64927</td><td>No</td><td>4330</td><td>0x80009D0D</td><td>0x000047C0</td></tr>
<tr><td>PedList_Mar_Altagracia_Act1</td><td>0x94F73793</td><td>No</td><td>4321</td><td>0x80009D04</td><td>0x0000117D</td></tr>
<tr><td>PedList_Mar_Altagracia_Act2</td><td>0xBAF9B1FC</td><td>No</td><td>5166</td><td>0x8000A49B</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_Mar_Big_Act1</td><td>0xE0A7B124</td><td>No</td><td>4339</td><td>0x80009D16</td><td>0x00007A3A</td></tr>
<tr><td>PedList_Mar_City_Act1</td><td>0x950F6EE5</td><td>No</td><td>4314</td><td>0x80009CFD</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_Mar_City_Act2</td><td>0x330818DA</td><td>No</td><td>2446</td><td>0x800084B2</td><td>0x0000E050</td></tr>
<tr><td>PedList_Mar_City_Act3</td><td>0x150A2837</td><td>No</td><td>4370</td><td>0x80009D41</td><td>0x00011A41</td></tr>
<tr><td>PedList_Mar_City_Act4</td><td>0x93029FCC</td><td>No</td><td>4372</td><td>0x80009D44</td><td>0x00007B1D</td></tr>
<tr><td>PedList_Mar_Industrial_Act1</td><td>0xE2755041</td><td>No</td><td>4323</td><td>0x80009D06</td><td>0x0000D24B</td></tr>
<tr><td>PedList_Mar_Industrial_Act2</td><td>0x606DC7D6</td><td>No</td><td>4383</td><td>0x80009D56</td><td>0x000104CD</td></tr>
<tr><td>PedList_Mar_Industrial_Act3</td><td>0xC270A0B3</td><td>No</td><td>4384</td><td>0x80009D57</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_Mar_Outskirt_Act1</td><td>0x6E384A11</td><td>No</td><td>4319</td><td>0x80009D02</td><td>0x00005304</td></tr>
<tr><td>PedList_Mar_Village_Act1</td><td>0x1EA86682</td><td>No</td><td>4317</td><td>0x80009D00</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_Margarita_Act1</td><td>0x983F54CB</td><td>No</td><td>4364</td><td>0x80009D3B</td><td>0x00013F5E</td></tr>
<tr><td>PedList_Mer_Big_Act1</td><td>0xC137BD20</td><td>No</td><td>4341</td><td>0x80009D18</td><td>0x00006315</td></tr>
<tr><td>PedList_Mer_City_Act1</td><td>0x22F441D9</td><td>No</td><td>2523</td><td>0x80008554</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_Mer_City_Act2</td><td>0xC0ECEBCE</td><td>No</td><td>4379</td><td>0x80009D50</td><td>0xFFFFFFFF</td></tr>
<tr><td>PedList_Mer_City_Act3</td><td>0xA2EEFB2B</td><td>No</td><td>4380</td><td>0x80009D51</td><td>0x00005BAF</td></tr>
<tr><td>PedList_Mer_City_Act4</td><td>0xA0FBC3F8</td><td>No</td><td>4381</td><td>0x80009D52</td><td>0x00000993</td></tr>
<tr><td>PedList_Mer_Outskirt_Act1</td><td>0x3F8CEA6D</td><td>No</td><td>4325</td><td>0x80009D08</td><td>0x00012CD2</td></tr>
<tr><td>PedList_OilDepot_Paths</td><td>0xBA16CBA0</td><td>No</td><td>4315</td><td>0x80009CFE</td><td>0x0000C76E</td></tr>
<tr><td>PedList_PirateHQ_Paths</td><td>0xA3DA8CA4</td><td>No</td><td>5646</td><td>0x8000AC93</td><td>0x0001064C</td></tr>
<tr><td>PedList_Protester</td><td>0xAD0D6299</td><td>No</td><td>2406</td><td>0x800083F4</td><td>0x00012AD5</td></tr>
<tr><td>PedList_VZCon001</td><td>0xB9445ADE</td><td>No</td><td>5941</td><td>0x8000B1E2</td><td>0x000056F1</td></tr>
<tr><td>PEP Rocket</td><td>0x642E5554</td><td>No</td><td>5745</td><td>0x8000AD6A</td><td>0x00002F96</td></tr>
<tr><td>PGZ95</td><td>0x76BE6D86</td><td>Yes</td><td>1629</td><td>0x80007265</td><td>0xFFFFFFFF</td></tr>
<tr><td>PGZ95 (base)</td><td>0x2213B43A</td><td>Yes</td><td>1627</td><td>0x80007262</td><td>0x0000555F</td></tr>
<tr><td>PGZ95 (Driver)</td><td>0x2157351D</td><td>Yes</td><td>1628</td><td>0x80007263</td><td>0x0000D125</td></tr>
<tr><td>PGZ95 Command</td><td>0x19CCC8A1</td><td>Yes</td><td>1630</td><td>0x80007266</td><td>0x0000995C</td></tr>
<tr><td>PGZ95 Command (Driver)</td><td>0x87E43EBC</td><td>Yes</td><td>1631</td><td>0x80007267</td><td>0x0000069F</td></tr>
<tr><td>Phoenix</td><td>0xA516ABB2</td><td>No</td><td>645</td><td>0x80005C55</td><td>0x0000EBE9</td></tr>
<tr><td>Phoenix (crappy)</td><td>0xCA2E0D98</td><td>No</td><td>2561</td><td>0x800085C1</td><td>0x00007A35</td></tr>
<tr><td>Phoenix (crappy) (Driver) (Civ Poor female)</td><td>0x5B8D933C</td><td>No</td><td>4415</td><td>0x80009DF9</td><td>0x0000DAC9</td></tr>
<tr><td>Phoenix (crappy) (Driver) (Civ Poor male)</td><td>0x9794874D</td><td>No</td><td>4416</td><td>0x80009DFA</td><td>0x0000CB95</td></tr>
<tr><td>Phoenix (Driver)</td><td>0x40442DD9</td><td>No</td><td>718</td><td>0x80006181</td><td>0xFFFFFFFF</td></tr>
<tr><td>Phoenix (Driver) (Civ Poor female)</td><td>0xB76B085E</td><td>No</td><td>4301</td><td>0x80009CC8</td><td>0xFFFFFFFF</td></tr>
<tr><td>Phoenix (Driver) (Civ Poor male)</td><td>0xCCD52953</td><td>No</td><td>4300</td><td>0x80009CC7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Phoenix (racing)</td><td>0x753E9DA1</td><td>No</td><td>2568</td><td>0x800085CB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Phoenix (racing) (Driver)</td><td>0x9CB16DBC</td><td>No</td><td>4417</td><td>0x80009DFB</td><td>0x00005D0F</td></tr>
<tr><td>Phoenix (racing) (Driver) (Civ Motorcycle male)</td><td>0x21FF7645</td><td>Yes</td><td>4418</td><td>0x80009DFC</td><td>0x0001003D</td></tr>
<tr><td>Phoenix_Driver</td><td>0x8B4A7993</td><td>No</td><td>5073</td><td>0x8000A407</td><td>0x0000111A</td></tr>
<tr><td>Phoenix_Driver (tight)</td><td>0xF765B0B2</td><td>No</td><td>5138</td><td>0x8000A47A</td><td>0x0000A986</td></tr>
<tr><td>Phoenix_Ruin</td><td>0x9F2A637B</td><td>No</td><td>1084</td><td>0x80006A2F</td><td>0x00005B84</td></tr>
<tr><td>Phoenix_Ruin_Fire</td><td>0xE80D5226</td><td>No</td><td>2023</td><td>0x800080C6</td><td>0x0000F536</td></tr>
<tr><td>PhoenixTestRoad20m</td><td>0x87040FE3</td><td>No</td><td>551</td><td>0x80005BA5</td><td>0x00004F1A</td></tr>
<tr><td>Physics Crashable (car)</td><td>0x677F3B2A</td><td>No</td><td>4504</td><td>0x80009E61</td><td>0xFFFFFFFF</td></tr>
<tr><td>Physics Crashable (tank)</td><td>0x0C30201A</td><td>Yes</td><td>4506</td><td>0x80009E63</td><td>0xFFFFFFFF</td></tr>
<tr><td>Physics Crashable (truck)</td><td>0xDC31BC5F</td><td>Yes</td><td>4505</td><td>0x80009E62</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pickup (Cash)</td><td>0x5BF2AB21</td><td>No</td><td>4903</td><td>0x8000A277</td><td>0x00001D17</td></tr>
<tr><td>PickupList1</td><td>0x07D0880E</td><td>No</td><td>41</td><td>0x8000450D</td><td>0x0000530C</td></tr>
<tr><td>piece_building2x2x2</td><td>0x8E32F426</td><td>No</td><td>782</td><td>0x80006228</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pirahna (GurCon003)</td><td>0x2D1EEE58</td><td>No</td><td>4031</td><td>0x80009A1A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Piranha</td><td>0x42C221BA</td><td>Yes</td><td>1767</td><td>0x800075D9</td><td>0x00009639</td></tr>
<tr><td>Piranha (Driver)</td><td>0xB4B4BCE1</td><td>Yes</td><td>1768</td><td>0x800075DA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Piranha (DriverGunner)</td><td>0xFB99B032</td><td>Yes</td><td>5626</td><td>0x8000AC7B</td><td>0x0000C795</td></tr>
<tr><td>Piranha (Full)</td><td>0x9CA00276</td><td>Yes</td><td>3681</td><td>0x80009530</td><td>0x00008312</td></tr>
<tr><td>Piranha Jet Exhaust ammo</td><td>0x75E63C99</td><td>Yes</td><td>3468</td><td>0x800092CA</td><td>0x00001838</td></tr>
<tr><td>Piranha_Driver</td><td>0xE4DF656B</td><td>Yes</td><td>5389</td><td>0x8000A980</td><td>0x00004D15</td></tr>
<tr><td>Pirate</td><td>0xC18215FE</td><td>No</td><td>487</td><td>0x800056C2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pirate Officer</td><td>0x07E00634</td><td>No</td><td>1323</td><td>0x80006E4A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pirate Officer (RPG)</td><td>0xBA29E876</td><td>No</td><td>2521</td><td>0x80008552</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pirate Pilot</td><td>0x5E78D2CC</td><td>No</td><td>2323</td><td>0x800082D8</td><td>0x000082CF</td></tr>
<tr><td>Pirate Prisoner</td><td>0x76A386FE</td><td>No</td><td>2370</td><td>0x80008325</td><td>0x000082F2</td></tr>
<tr><td>Pirate Sailor</td><td>0xFCE48F72</td><td>No</td><td>1322</td><td>0x80006E49</td><td>0x0000AF60</td></tr>
<tr><td>Pirate Sailor (Drinker)</td><td>0xD776EAD6</td><td>No</td><td>3806</td><td>0x800097C4</td><td>0x0000A09F</td></tr>
<tr><td>Pirate Starter 01</td><td>0x10855284</td><td>No</td><td>2321</td><td>0x800082D6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pirate Starter 02</td><td>0xAA82735B</td><td>No</td><td>2322</td><td>0x800082D7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pirate Starter 03</td><td>0x887FFF3E</td><td>No</td><td>2340</td><td>0x800082EC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pirate Starter 04</td><td>0x9291581D</td><td>No</td><td>2341</td><td>0x800082ED</td><td>0x00010EED</td></tr>
<tr><td>Pirate Starter 05</td><td>0xA88F3C28</td><td>No</td><td>1325</td><td>0x80006E4C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pirate Thug</td><td>0x9DC036EA</td><td>No</td><td>1321</td><td>0x80006E48</td><td>0x00013D68</td></tr>
<tr><td>Pirate Thug (AA)</td><td>0x91188C81</td><td>No</td><td>2519</td><td>0x80008550</td><td>0x00013486</td></tr>
<tr><td>Pirate Thug (Female AA)</td><td>0x6B347CE1</td><td>No</td><td>2520</td><td>0x80008551</td><td>0x0000EF11</td></tr>
<tr><td>Pirate Thug (Female)</td><td>0xD1FEF2C7</td><td>No</td><td>1324</td><td>0x80006E4B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pirate Thug (God)</td><td>0x70CC53F9</td><td>No</td><td>5842</td><td>0x8000AF97</td><td>0x0000AC17</td></tr>
<tr><td>Pirate Thug (RPG)</td><td>0x28CF4EB4</td><td>No</td><td>2518</td><td>0x8000854F</td><td>0x0000AB3B</td></tr>
<tr><td>Pirate Thug (Shotgun)</td><td>0x136BD415</td><td>No</td><td>1366</td><td>0x80006ED2</td><td>0x00005A85</td></tr>
<tr><td>Pirate Traffic</td><td>0xCA85ABA9</td><td>No</td><td>1506</td><td>0x80007041</td><td>0x0000B83B</td></tr>
<tr><td>Pirate Worker</td><td>0x226333BC</td><td>No</td><td>2324</td><td>0x800082D9</td><td>0x00000AE5</td></tr>
<tr><td>Pirate Worker (Cell Phone)</td><td>0xA6B03989</td><td>No</td><td>3817</td><td>0x800097D2</td><td>0xFFFFFFFF</td></tr>
<tr><td>PirDbSpawner</td><td>0x95E72680</td><td>No</td><td>2383</td><td>0x8000833B</td><td>0x0001317B</td></tr>
<tr><td>PirDbSpawner (Squad Full AT)</td><td>0x23A81C25</td><td>No</td><td>5667</td><td>0x8000ACAA</td><td>0x0000358B</td></tr>
<tr><td>PirDbSpawner (Squad Half AT)</td><td>0x98ED8089</td><td>No</td><td>5668</td><td>0x8000ACAB</td><td>0x000073F9</td></tr>
<tr><td>PirDbSpawner (Squad Quarter AT)</td><td>0x9653836A</td><td>No</td><td>5912</td><td>0x8000B03F</td><td>0xFFFFFFFF</td></tr>
<tr><td>PirDbSpawner (Squad)</td><td>0xB1E30047</td><td>No</td><td>3017</td><td>0x80008A31</td><td>0x00000F91</td></tr>
<tr><td>Pistol</td><td>0xD48C7D34</td><td>No</td><td>1111</td><td>0x80006B45</td><td>0x0000EBC9</td></tr>
<tr><td>Pistol (AL)</td><td>0xF7D358AC</td><td>No</td><td>4106</td><td>0x80009B15</td><td>0x0000EF88</td></tr>
<tr><td>Pistol (CH)</td><td>0xDE670FE2</td><td>No</td><td>4104</td><td>0x80009B13</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pistol (GR)</td><td>0x8C9B1E24</td><td>No</td><td>4105</td><td>0x80009B14</td><td>0x00003089</td></tr>
<tr><td>Pistol (silver)</td><td>0x4A02D924</td><td>No</td><td>358</td><td>0x8000508E</td><td>0x0000B504</td></tr>
<tr><td>Pistol Bullet</td><td>0xA9F6A3BC</td><td>No</td><td>1123</td><td>0x80006B51</td><td>0x0000B0E5</td></tr>
<tr><td>Pistol Bullet (CH)</td><td>0x819173EA</td><td>No</td><td>4101</td><td>0x80009B10</td><td>0x00000AEB</td></tr>
<tr><td>Pistol Bullet (GR)</td><td>0x215A1B1C</td><td>No</td><td>4100</td><td>0x80009B0F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pistol Bullet (OC)</td><td>0x31472E5B</td><td>No</td><td>4102</td><td>0x80009B11</td><td>0x000076A2</td></tr>
<tr><td>placeable Building</td><td>0x8DC14572</td><td>No</td><td>77</td><td>0x80004B30</td><td>0x000022A2</td></tr>
<tr><td>placeable Constrained</td><td>0x8850798A</td><td>No</td><td>1472</td><td>0x80007017</td><td>0x00006A1F</td></tr>
<tr><td>placeable Environment</td><td>0x0F3754C5</td><td>No</td><td>79</td><td>0x80004B32</td><td>0x000063BE</td></tr>
<tr><td>placeable Fence</td><td>0xFF05D325</td><td>No</td><td>6076</td><td>0x900001BC</td><td>0x0000E9D1</td></tr>
<tr><td>placeable Prop</td><td>0xE8CB9DED</td><td>No</td><td>78</td><td>0x80004B31</td><td>0x000019ED</td></tr>
<tr><td>placeable Prop Destructible</td><td>0xF82EF36D</td><td>No</td><td>6075</td><td>0x900001BB</td><td>0x00008C86</td></tr>
<tr><td>placeable Static</td><td>0xE8137428</td><td>No</td><td>141</td><td>0x80004CD8</td><td>0xFFFFFFFF</td></tr>
<tr><td>placeable Static Destructible</td><td>0x88BDAEE2</td><td>No</td><td>152</td><td>0x80004CE3</td><td>0x0000C7D4</td></tr>
<tr><td>placeable Wall</td><td>0xDFA3C5B6</td><td>No</td><td>69</td><td>0x80004A17</td><td>0x00013CA1</td></tr>
<tr><td>Planes (as Buildings)</td><td>0xFFD23808</td><td>No</td><td>1820</td><td>0x800076AB</td><td>0xFFFFFFFF</td></tr>
<tr><td>PLZ45</td><td>0x4515E6E4</td><td>Yes</td><td>1632</td><td>0x80007268</td><td>0x0000054A</td></tr>
<tr><td>PLZ45 (Driver)</td><td>0x3AAE63C3</td><td>Yes</td><td>1670</td><td>0x8000749B</td><td>0xFFFFFFFF</td></tr>
<tr><td>PLZ45 (Full)</td><td>0xF6B88FF0</td><td>Yes</td><td>4728</td><td>0x8000A022</td><td>0x0000946A</td></tr>
<tr><td>pMc</td><td>0x30E4A26F</td><td>No</td><td>489</td><td>0x800056C4</td><td>0xFFFFFFFF</td></tr>
<tr><td>PmcHq_Interior</td><td>0x1EEE05C1</td><td>No</td><td>2376</td><td>0x8000832C</td><td>0x0000D0B4</td></tr>
<tr><td>PmcSeat</td><td>0x78EBB784</td><td>No</td><td>1916</td><td>0x80007A14</td><td>0x00010FA8</td></tr>
<tr><td>PointTraffic</td><td>0x3C55A4B8</td><td>No</td><td>3080</td><td>0x80008BA4</td><td>0xFFFFFFFF</td></tr>
<tr><td>PointTraffic_AlliedHQ_AA</td><td>0x5775B480</td><td>No</td><td>5635</td><td>0x8000AC85</td><td>0x00001F70</td></tr>
<tr><td>PointTraffic_AlliedHQ_HMMWV</td><td>0x45833FC3</td><td>No</td><td>5922</td><td>0x8000B1CC</td><td>0x0000B58E</td></tr>
<tr><td>PointTraffic_ChiHQ_AA</td><td>0x5FE4A4E3</td><td>No</td><td>5936</td><td>0x8000B1DD</td><td>0xFFFFFFFF</td></tr>
<tr><td>PointTraffic_ChiHQ_Soldiers</td><td>0x1E2C21E4</td><td>No</td><td>5932</td><td>0x8000B1D9</td><td>0x0000BD3F</td></tr>
<tr><td>PointTraffic_ChiHQ_Vehicles</td><td>0xB2CC6B46</td><td>Yes</td><td>5934</td><td>0x8000B1DB</td><td>0xFFFFFFFF</td></tr>
<tr><td>PointTraffic_GurHQ_AA</td><td>0xB6CEC6BB</td><td>No</td><td>5926</td><td>0x8000B1D0</td><td>0x00003CBA</td></tr>
<tr><td>PointTraffic_GurHQ_Soldiers</td><td>0x53A2E42C</td><td>No</td><td>5923</td><td>0x8000B1CD</td><td>0x0000C3B3</td></tr>
<tr><td>PointTraffic_GurHQ_Vehicles</td><td>0xD1F25B0E</td><td>Yes</td><td>5927</td><td>0x8000B1D1</td><td>0xFFFFFFFF</td></tr>
<tr><td>PointTraffic_OC_EXT</td><td>0xC63DB251</td><td>No</td><td>5653</td><td>0x8000AC9B</td><td>0x00009172</td></tr>
<tr><td>PointTraffic_OC_GunTrucks</td><td>0x3ECEC776</td><td>Yes</td><td>5656</td><td>0x8000AC9E</td><td>0x00005243</td></tr>
<tr><td>PointTraffic_OC_Omen</td><td>0xEA0B050D</td><td>No</td><td>5919</td><td>0x8000B1C9</td><td>0x00000EBE</td></tr>
<tr><td>PointTraffic_OC_Soldiers</td><td>0x1BB1F43D</td><td>No</td><td>5920</td><td>0x8000B1CA</td><td>0x00001DC6</td></tr>
<tr><td>PointTraffic_OC_Stingray</td><td>0xC39AAE15</td><td>Yes</td><td>5917</td><td>0x8000B1C7</td><td>0xFFFFFFFF</td></tr>
<tr><td>PointTraffic_Pirate_T300DriverGunner</td><td>0xD5D0C497</td><td>No</td><td>5953</td><td>0x8000B1EF</td><td>0xFFFFFFFF</td></tr>
<tr><td>PointTraffic_PirateHQ_Cutter</td><td>0x72792695</td><td>No</td><td>5649</td><td>0x8000AC96</td><td>0x000008AD</td></tr>
<tr><td>PointTraffic_PirateHQ_Jetski</td><td>0xBC5A7380</td><td>No</td><td>5647</td><td>0x8000AC94</td><td>0x00001B05</td></tr>
<tr><td>PointTraffic_PirateHQ_LandVehicle</td><td>0xCD67CB21</td><td>No</td><td>5651</td><td>0x8000AC98</td><td>0x00012AC2</td></tr>
<tr><td>PointTraffic_Pmc_Boats</td><td>0xD4783061</td><td>Yes</td><td>5641</td><td>0x8000AC8C</td><td>0x00000C42</td></tr>
<tr><td>PointTraffic_Roadblock_CHINGLV50Spawn</td><td>0xD6B41900</td><td>No</td><td>5163</td><td>0x8000A498</td><td>0x000038DE</td></tr>
<tr><td>PointTraffic_Roadblock_GunTrucksOC</td><td>0xF1340AC9</td><td>Yes</td><td>4992</td><td>0x8000A3A7</td><td>0x000018C8</td></tr>
<tr><td>PointTraffic_Roadblock_Gur50JeepSpawn</td><td>0xA57EA2D9</td><td>Yes</td><td>5164</td><td>0x8000A499</td><td>0x0000F399</td></tr>
<tr><td>PointTraffic_Roadblock_HMMVSpawn</td><td>0x5F997554</td><td>No</td><td>5167</td><td>0x8000A49C</td><td>0x00000F20</td></tr>
<tr><td>PointTraffic_Roadblock_VZ50jeepSpawn</td><td>0xDC5C7AB5</td><td>Yes</td><td>5161</td><td>0x8000A495</td><td>0x00007DB3</td></tr>
<tr><td>PointTraffic_VZCon001_Dirtbike</td><td>0xF770D59D</td><td>No</td><td>5947</td><td>0x8000B1E9</td><td>0x00003D6E</td></tr>
<tr><td>PointTraffic_VZCon001_PBoat</td><td>0x3E6A6B05</td><td>Yes</td><td>5946</td><td>0x8000B1E8</td><td>0x0000A49E</td></tr>
<tr><td>Police</td><td>0xC6FBA403</td><td>No</td><td>33</td><td>0x80004383</td><td>0xFFFFFFFF</td></tr>
<tr><td>Police (Gasmask)</td><td>0xA9352497</td><td>No</td><td>522</td><td>0x80005726</td><td>0x000087DE</td></tr>
<tr><td>Police (Riot)</td><td>0x02CC0CC2</td><td>No</td><td>521</td><td>0x80005725</td><td>0x00007EB4</td></tr>
<tr><td>Police car (Police driver)</td><td>0xB40344EC</td><td>No</td><td>986</td><td>0x80006875</td><td>0xFFFFFFFF</td></tr>
<tr><td>Police Cruiser</td><td>0xB6A5ED4A</td><td>No</td><td>1187</td><td>0x80006C9E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Police Cruiser (Driver)</td><td>0xAB6F8831</td><td>No</td><td>1188</td><td>0x80006C9F</td><td>0x00013C7F</td></tr>
<tr><td>police cruiser With Civ Driver</td><td>0x351B674A</td><td>No</td><td>719</td><td>0x80006182</td><td>0x0000B74B</td></tr>
<tr><td>Police Helicopter</td><td>0xDC56A3AA</td><td>Yes</td><td>1191</td><td>0x80006CA3</td><td>0x00007A62</td></tr>
<tr><td>Police Helicopter (Delivery)</td><td>0x3FAD763F</td><td>Yes</td><td>2219</td><td>0x800081F8</td><td>0x0000F34E</td></tr>
<tr><td>Police Helicopter (Driver)</td><td>0x03E72111</td><td>Yes</td><td>1192</td><td>0x80006CA4</td><td>0x00007B94</td></tr>
<tr><td>Pony (base)</td><td>0x14B85D27</td><td>No</td><td>2179</td><td>0x800081CF</td><td>0x0001337E</td></tr>
<tr><td>Pony (crappy)</td><td>0x3957B519</td><td>No</td><td>2180</td><td>0x800081D0</td><td>0x00000C4E</td></tr>
<tr><td>Pony (Crappy) (Driver)</td><td>0xA1B054F4</td><td>No</td><td>3083</td><td>0x80008BA7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pony (crappy) (Driver) (Civ Poor female)</td><td>0x3E6DC31B</td><td>No</td><td>4281</td><td>0x80009CB4</td><td>0x000113D6</td></tr>
<tr><td>Pony (crappy) (Driver) (Civ Poor male)</td><td>0x1AF7A1CA</td><td>No</td><td>4252</td><td>0x80009C97</td><td>0x00005FD0</td></tr>
<tr><td>Pony (normal)</td><td>0x89A24815</td><td>No</td><td>2181</td><td>0x800081D1</td><td>0x00003FB4</td></tr>
<tr><td>Pony (Normal) (black)</td><td>0xD727254F</td><td>No</td><td>5596</td><td>0x8000AC4B</td><td>0x00006134</td></tr>
<tr><td>Pony (Normal) (blue)</td><td>0xFD344F9A</td><td>No</td><td>5597</td><td>0x8000AC4C</td><td>0x0000DBA0</td></tr>
<tr><td>Pony (Normal) (Driver)</td><td>0xE75BD9A0</td><td>No</td><td>3084</td><td>0x80008BA8</td><td>0x00005F49</td></tr>
<tr><td>Pony (Normal) (Driver) (Civ Poor female)</td><td>0x2E0C2837</td><td>No</td><td>4420</td><td>0x80009DFE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pony (Normal) (Driver) (Civ Poor male)</td><td>0x308AC676</td><td>No</td><td>4419</td><td>0x80009DFD</td><td>0x0001193C</td></tr>
<tr><td>Pony (Normal) (green)</td><td>0xDB96D9D7</td><td>No</td><td>5601</td><td>0x8000AC50</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pony (Normal) (lightblue)</td><td>0x93EB015C</td><td>No</td><td>5602</td><td>0x8000AC51</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pony (Normal) (orange)</td><td>0xA6C359DC</td><td>No</td><td>5599</td><td>0x8000AC4E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pony (Normal) (red)</td><td>0xB9844A27</td><td>No</td><td>5598</td><td>0x8000AC4D</td><td>0x00000BAA</td></tr>
<tr><td>Pony (Normal) (white)</td><td>0xA3C23DFD</td><td>No</td><td>5600</td><td>0x8000AC4F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Pony_Driver</td><td>0xA0E58342</td><td>No</td><td>5091</td><td>0x8000A41A</td><td>0x0000233A</td></tr>
<tr><td>PopulationRegions</td><td>0x9DB5BF57</td><td>No</td><td>97</td><td>0x80004BFE</td><td>0xFFFFFFFF</td></tr>
<tr><td>PR buggy (Gunner RightFront)</td><td>0xD4C38954</td><td>Yes</td><td>5613</td><td>0x8000AC5D</td><td>0xFFFFFFFF</td></tr>
<tr><td>PR Cup</td><td>0xD236C9FF</td><td>No</td><td>3807</td><td>0x800097C5</td><td>0x00004DBB</td></tr>
<tr><td>PR Defender (AA)</td><td>0xEA15496B</td><td>No</td><td>5038</td><td>0x8000A3DB</td><td>0x00001B4F</td></tr>
<tr><td>PR Defender (AT)</td><td>0xD68661A0</td><td>No</td><td>5037</td><td>0x8000A3DA</td><td>0x0000D829</td></tr>
<tr><td>PR Defender (AT) (Window Spawner)</td><td>0x2A580369</td><td>No</td><td>3009</td><td>0x80008A29</td><td>0x00001419</td></tr>
<tr><td>PR Defender (MG)</td><td>0x2C08156D</td><td>No</td><td>5039</td><td>0x8000A3DC</td><td>0x00012991</td></tr>
<tr><td>PR Defender (Rifle)</td><td>0xFB7ED48F</td><td>No</td><td>5036</td><td>0x8000A3D9</td><td>0x0000D35D</td></tr>
<tr><td>PR HQ Cell Phone</td><td>0x1A4F5240</td><td>No</td><td>3818</td><td>0x800097D3</td><td>0x00009DB4</td></tr>
<tr><td>Practice LGB Projectile</td><td>0x041F899E</td><td>No</td><td>4881</td><td>0x8000A25F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Primary Equipment</td><td>0xDFCF027D</td><td>No</td><td>705</td><td>0x80005FD0</td><td>0x0000A43D</td></tr>
<tr><td>Programmer Test Template</td><td>0x89923DE7</td><td>No</td><td>341</td><td>0x80004E2C</td><td>0xFFFFFFFF</td></tr>
<tr><td>ProgrammerBlueRoad10</td><td>0xE6BA19F8</td><td>No</td><td>541</td><td>0x80005B95</td><td>0x000087B2</td></tr>
<tr><td>ProgrammerBlueRoad20</td><td>0x1AE507A9</td><td>No</td><td>545</td><td>0x80005B9A</td><td>0x00010CE5</td></tr>
<tr><td>ProgrammerBlueZone</td><td>0xAEB500CF</td><td>No</td><td>535</td><td>0x80005B8F</td><td>0xFFFFFFFF</td></tr>
<tr><td>ProgrammerGreenRoad10</td><td>0x62C45ABB</td><td>No</td><td>542</td><td>0x80005B96</td><td>0x0000C022</td></tr>
<tr><td>ProgrammerGreenZone</td><td>0x02A13980</td><td>No</td><td>538</td><td>0x80005B92</td><td>0x000073A7</td></tr>
<tr><td>ProgrammerRedHDTemplate</td><td>0x02F37108</td><td>No</td><td>544</td><td>0x80005B98</td><td>0x0000EE62</td></tr>
<tr><td>ProgrammerRedRoad10</td><td>0xD81F2DDB</td><td>No</td><td>540</td><td>0x80005B94</td><td>0x0000754D</td></tr>
<tr><td>ProgrammerRedRoad20</td><td>0x0F6B0116</td><td>No</td><td>543</td><td>0x80005B97</td><td>0x0000C445</td></tr>
<tr><td>ProgrammerRedZone</td><td>0x4235BFA0</td><td>No</td><td>536</td><td>0x80005B90</td><td>0xFFFFFFFF</td></tr>
<tr><td>ProgrammerTest10Cross</td><td>0xED2056E2</td><td>No</td><td>528</td><td>0x80005B86</td><td>0xFFFFFFFF</td></tr>
<tr><td>ProgrammerTestRoad10w</td><td>0xEF2A1E77</td><td>No</td><td>527</td><td>0x80005B85</td><td>0x00004A38</td></tr>
<tr><td>ProgrammerTestRoad20c</td><td>0xCFA7AD64</td><td>No</td><td>533</td><td>0x80005B8B</td><td>0x00004CA8</td></tr>
<tr><td>ProgrammerTestZone</td><td>0x590C0497</td><td>No</td><td>526</td><td>0x80005B84</td><td>0xFFFFFFFF</td></tr>
<tr><td>ProgrammerYellowRoad10</td><td>0x9D8FABBC</td><td>No</td><td>539</td><td>0x80005B93</td><td>0x00002680</td></tr>
<tr><td>ProgrammerYellowZone</td><td>0x48A5E12B</td><td>No</td><td>537</td><td>0x80005B91</td><td>0xFFFFFFFF</td></tr>
<tr><td>Projectile</td><td>0xBD8C6F10</td><td>No</td><td>23</td><td>0x80004372</td><td>0x00005542</td></tr>
<tr><td>prop_metal_lrg</td><td>0x30E6DADE</td><td>No</td><td>3946</td><td>0x8000986E</td><td>0x00009C5A</td></tr>
<tr><td>prop_stone_lrg</td><td>0x8A394748</td><td>No</td><td>4307</td><td>0x80009CCE</td><td>0xFFFFFFFF</td></tr>
<tr><td>PropDestructTemplate</td><td>0x56C61F52</td><td>No</td><td>6037</td><td>0x90000195</td><td>0x00010D23</td></tr>
<tr><td>PropTemplate</td><td>0x6A5C2678</td><td>No</td><td>388</td><td>0x8000555B</td><td>0x0001393D</td></tr>
<tr><td>PropTemplate_chandellier</td><td>0xFDF1F196</td><td>No</td><td>4302</td><td>0x80009CC9</td><td>0x0000D5EF</td></tr>
<tr><td>Protester (female)</td><td>0x43DD69DC</td><td>No</td><td>2137</td><td>0x800081A0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Protester (male)</td><td>0x1EA64DED</td><td>No</td><td>2136</td><td>0x8000819F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Proximity Mine</td><td>0x0C1E83CD</td><td>No</td><td>1331</td><td>0x80006EA2</td><td>0x00007366</td></tr>
<tr><td>Proximity Mine (Planted)</td><td>0xDF14909C</td><td>No</td><td>1149</td><td>0x80006B6C</td><td>0x000046CA</td></tr>
<tr><td>Proximity Mine Projectile</td><td>0x8557688A</td><td>No</td><td>1330</td><td>0x80006EA1</td><td>0x0000F718</td></tr>
<tr><td>QuotaObject</td><td>0x15D0D35E</td><td>No</td><td>44</td><td>0x80004513</td><td>0x000067DD</td></tr>
<tr><td>R90</td><td>0xCA5BBA82</td><td>No</td><td>1792</td><td>0x800075F2</td><td>0xFFFFFFFF</td></tr>
<tr><td>R90 (Driver)</td><td>0x3876D729</td><td>No</td><td>1794</td><td>0x800075F8</td><td>0x000098BE</td></tr>
<tr><td>R90 (Driver) (Civ Business B Male)</td><td>0x209227FB</td><td>No</td><td>4215</td><td>0x80009C6D</td><td>0x0000FF3D</td></tr>
<tr><td>R90 (Driver) (Civ Business Female)</td><td>0xE594BA20</td><td>No</td><td>4216</td><td>0x80009C6E</td><td>0x000029EF</td></tr>
<tr><td>R90 (Driver) (Civ Business Male)</td><td>0xDC9E9AD1</td><td>No</td><td>4214</td><td>0x80009C6C</td><td>0x0000A606</td></tr>
<tr><td>R90 (Driver) (Civ Rich Female)</td><td>0x1F49A5F8</td><td>No</td><td>4225</td><td>0x80009C77</td><td>0xFFFFFFFF</td></tr>
<tr><td>R90 (Driver) (Civ Rich Male)</td><td>0x258DEE29</td><td>No</td><td>4224</td><td>0x80009C76</td><td>0x000049E7</td></tr>
<tr><td>R90 (Driver) (OC)</td><td>0x219BDAFC</td><td>No</td><td>1817</td><td>0x800076A8</td><td>0x0001154A</td></tr>
<tr><td>R90 (Fling Left)</td><td>0x4F977B9C</td><td>No</td><td>5568</td><td>0x8000AB6B</td><td>0xFFFFFFFF</td></tr>
<tr><td>R90 (Fling Right)</td><td>0x8FD76CCF</td><td>No</td><td>5546</td><td>0x8000AB53</td><td>0xFFFFFFFF</td></tr>
<tr><td>R90 Limo</td><td>0x50390CFF</td><td>No</td><td>2610</td><td>0x800085F9</td><td>0xFFFFFFFF</td></tr>
<tr><td>R90 Taxi</td><td>0x1D022366</td><td>No</td><td>1793</td><td>0x800075F5</td><td>0xFFFFFFFF</td></tr>
<tr><td>R90 Taxi (Driver)</td><td>0x705A73FD</td><td>No</td><td>1795</td><td>0x800075F9</td><td>0x00005CCE</td></tr>
<tr><td>R90 Taxi (Driver) (Civ Taxi Driver male)</td><td>0xF93E8587</td><td>No</td><td>4421</td><td>0x80009DFF</td><td>0x000109DA</td></tr>
<tr><td>R90_Driver</td><td>0xD19ED643</td><td>No</td><td>5071</td><td>0x8000A404</td><td>0x0000F0CC</td></tr>
<tr><td>Real Physics Prop</td><td>0xFFE5624D</td><td>No</td><td>3742</td><td>0x8000961C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Real Physics Prop Destructible</td><td>0x12C5BACD</td><td>No</td><td>3738</td><td>0x80009618</td><td>0x00008E75</td></tr>
<tr><td>Recruit Eva Navarro</td><td>0x262B9048</td><td>No</td><td>2278</td><td>0x80008242</td><td>0xFFFFFFFF</td></tr>
<tr><td>Recruit Ewen Garret</td><td>0x9C5DD2A9</td><td>No</td><td>2276</td><td>0x80008240</td><td>0x00009373</td></tr>
<tr><td>Recruit Ewen Garret (Invincible)</td><td>0x5C54C46B</td><td>No</td><td>5751</td><td>0x8000ADA1</td><td>0x0000EC38</td></tr>
<tr><td>Recruit Misha Milanich</td><td>0xD777E8A2</td><td>No</td><td>2277</td><td>0x80008241</td><td>0x0000F7BC</td></tr>
<tr><td>RIB36</td><td>0xDB1BF61F</td><td>No</td><td>834</td><td>0x8000638F</td><td>0x00002C3B</td></tr>
<tr><td>RIB36 (DEPRECIATED)</td><td>0x1E169152</td><td>No</td><td>355</td><td>0x80004F3D</td><td>0x0000A240</td></tr>
<tr><td>RIB36 (VZ Driver)</td><td>0x4FAAE964</td><td>No</td><td>1024</td><td>0x800068AA</td><td>0x00003BD0</td></tr>
<tr><td>RIB36_Driver</td><td>0x7ADD14AC</td><td>No</td><td>5088</td><td>0x8000A417</td><td>0x0000CCC6</td></tr>
<tr><td>Ridgeline</td><td>0x4C5D7A00</td><td>No</td><td>2560</td><td>0x800085C0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Ridgeline (Driver)</td><td>0xF044DC1F</td><td>No</td><td>4294</td><td>0x80009CC1</td><td>0x00011B55</td></tr>
<tr><td>Ridgeline (Driver) (Civ Poor female)</td><td>0xA10E5854</td><td>No</td><td>4296</td><td>0x80009CC3</td><td>0x000127CD</td></tr>
<tr><td>Ridgeline (Driver) (Civ Poor male)</td><td>0x29012425</td><td>No</td><td>4295</td><td>0x80009CC2</td><td>0x0000D07B</td></tr>
<tr><td>Ridgeline_Driver</td><td>0x32561F7D</td><td>No</td><td>5090</td><td>0x8000A419</td><td>0x00001D9C</td></tr>
<tr><td>rifle</td><td>0xD0459A41</td><td>No</td><td>472</td><td>0x800056AC</td><td>0x0001401E</td></tr>
<tr><td>Riot Gun</td><td>0x2531D295</td><td>No</td><td>1349</td><td>0x80006EBE</td><td>0x0000E90A</td></tr>
<tr><td>Riot Gun Projectile</td><td>0x3C45B6A2</td><td>No</td><td>2413</td><td>0x8000844D</td><td>0x000097BF</td></tr>
<tr><td>Road</td><td>0xEA0F3AA3</td><td>No</td><td>45</td><td>0x80004514</td><td>0x00012506</td></tr>
<tr><td>Rocket</td><td>0x5434C7ED</td><td>No</td><td>5207</td><td>0x8000A5EF</td><td>0x000020FD</td></tr>
<tr><td>Rocket Artillery Projectile</td><td>0x908FB818</td><td>No</td><td>3168</td><td>0x80008E43</td><td>0xFFFFFFFF</td></tr>
<tr><td>Rocks01</td><td>0xB8822B30</td><td>No</td><td>621</td><td>0x80005C2F</td><td>0x0000D191</td></tr>
<tr><td>RPG</td><td>0x60437246</td><td>No</td><td>27</td><td>0x8000437B</td><td>0x00009800</td></tr>
<tr><td>RPG (Window Spawner)</td><td>0xC507000B</td><td>No</td><td>5669</td><td>0x8000ACAC</td><td>0x0001077A</td></tr>
<tr><td>RPG Rocket</td><td>0xEFEB3916</td><td>No</td><td>24</td><td>0x80004373</td><td>0x00008515</td></tr>
<tr><td>rpglauncher</td><td>0xEB8404E6</td><td>No</td><td>471</td><td>0x800056AB</td><td>0x0000FB13</td></tr>
<tr><td>RTR</td><td>0xCFCAA9FB</td><td>No</td><td>647</td><td>0x80005C61</td><td>0xFFFFFFFF</td></tr>
<tr><td>RTR (Civ)</td><td>0x23322390</td><td>No</td><td>1196</td><td>0x80006CA8</td><td>0xFFFFFFFF</td></tr>
<tr><td>RTR (Civ) (black)</td><td>0x72D8A062</td><td>No</td><td>5585</td><td>0x8000AC40</td><td>0x000039F1</td></tr>
<tr><td>RTR (Civ) (blue)</td><td>0x95CAF8C1</td><td>No</td><td>5584</td><td>0x8000AC3F</td><td>0x0000E0DA</td></tr>
<tr><td>RTR (Civ) (Driver)</td><td>0x78695EAF</td><td>No</td><td>812</td><td>0x8000624A</td><td>0x00005611</td></tr>
<tr><td>RTR (Civ) (Driver) (Civ Business B male)</td><td>0x3CEF5959</td><td>No</td><td>4422</td><td>0x80009E00</td><td>0x00013375</td></tr>
<tr><td>RTR (Civ) (Driver) (Civ Poor Male)</td><td>0xE4B8C995</td><td>No</td><td>5954</td><td>0x8000B1F0</td><td>0xFFFFFFFF</td></tr>
<tr><td>RTR (Civ) (green)</td><td>0x251C7E1A</td><td>No</td><td>5588</td><td>0x8000AC43</td><td>0x00007812</td></tr>
<tr><td>RTR (Civ) (lightblue)</td><td>0x8E43E67D</td><td>No</td><td>5586</td><td>0x8000AC41</td><td>0x000100A1</td></tr>
<tr><td>RTR (Civ) (orange)</td><td>0xC729455F</td><td>No</td><td>5587</td><td>0x8000AC42</td><td>0xFFFFFFFF</td></tr>
<tr><td>RTR (Civ) (red)</td><td>0xFA5106B6</td><td>No</td><td>5583</td><td>0x8000AC3E</td><td>0x000099BF</td></tr>
<tr><td>RTR (Civ) (white)</td><td>0x1FA88138</td><td>No</td><td>5582</td><td>0x8000AC3D</td><td>0x00004BFB</td></tr>
<tr><td>RTR (crappy)</td><td>0x2C14011F</td><td>No</td><td>2565</td><td>0x800085C5</td><td>0x00008A1F</td></tr>
<tr><td>RTR (crappy) (driver)</td><td>0x8FDA008A</td><td>No</td><td>4228</td><td>0x80009C7A</td><td>0x000010D9</td></tr>
<tr><td>RTR (crappy) (Driver) (Civ Casual female)</td><td>0x3C608342</td><td>No</td><td>4230</td><td>0x80009C7C</td><td>0xFFFFFFFF</td></tr>
<tr><td>RTR (crappy) (Driver) (Civ Casual male)</td><td>0x54C270E7</td><td>No</td><td>4229</td><td>0x80009C7B</td><td>0x0000AF8C</td></tr>
<tr><td>RTR (crappy) (Driver) (Civ Poor female)</td><td>0xF1076039</td><td>No</td><td>4232</td><td>0x80009C7E</td><td>0x0000A87E</td></tr>
<tr><td>RTR (crappy) (Driver) (Civ Poor male)</td><td>0x8AA5FB1C</td><td>No</td><td>4231</td><td>0x80009C7D</td><td>0x000123B2</td></tr>
<tr><td>RTR (racing)</td><td>0x928B459E</td><td>No</td><td>2567</td><td>0x800085CA</td><td>0xFFFFFFFF</td></tr>
<tr><td>RTR (racing) (Driver)</td><td>0x892F2F35</td><td>No</td><td>4423</td><td>0x80009E01</td><td>0x00003FA8</td></tr>
<tr><td>RTR (racing) (Driver) (Civ Motorcycle male)</td><td>0x78551744</td><td>Yes</td><td>4424</td><td>0x80009E02</td><td>0x00008565</td></tr>
<tr><td>RTR_Driver</td><td>0xD9EAD870</td><td>No</td><td>5112</td><td>0x8000A456</td><td>0x00013DAE</td></tr>
<tr><td>RTRCrappy_Driver</td><td>0xF4C1E9A3</td><td>No</td><td>5141</td><td>0x8000A47D</td><td>0xFFFFFFFF</td></tr>
<tr><td>RTRRacing_Driver</td><td>0x9D5D27A2</td><td>No</td><td>5142</td><td>0x8000A47E</td><td>0x00000651</td></tr>
<tr><td>RuinDebris01</td><td>0x5D3EC19B</td><td>No</td><td>3255</td><td>0x80008F33</td><td>0x00002977</td></tr>
<tr><td>RuinDebris02</td><td>0xC341A0C4</td><td>No</td><td>3256</td><td>0x80008F34</td><td>0x00000A9C</td></tr>
<tr><td>RuinDebris_concrete</td><td>0x6AC06304</td><td>No</td><td>3308</td><td>0x80008F78</td><td>0xFFFFFFFF</td></tr>
<tr><td>Salamander</td><td>0x91C6BF01</td><td>No</td><td>832</td><td>0x8000638D</td><td>0x0000BC56</td></tr>
<tr><td>Salton Seahorse (base)</td><td>0xF41431F6</td><td>Yes</td><td>3343</td><td>0x80009003</td><td>0x0000FA2E</td></tr>
<tr><td>Salton Seahorse (Civ)</td><td>0xBE7BD515</td><td>Yes</td><td>1197</td><td>0x80006CAD</td><td>0x000060E1</td></tr>
<tr><td>Salton Seahorse (Civ) (Driver)</td><td>0xE39CB0A0</td><td>Yes</td><td>3686</td><td>0x80009535</td><td>0x0000CF2B</td></tr>
<tr><td>Salton Seahorse (Civ) (Driver) (Civ Poor female)</td><td>0xE5841737</td><td>Yes</td><td>4651</td><td>0x80009FCD</td><td>0x0000F425</td></tr>
<tr><td>Salton Seahorse (Civ) (Driver) (Civ Poor male)</td><td>0x972F5D76</td><td>Yes</td><td>4650</td><td>0x80009FCC</td><td>0x00008756</td></tr>
<tr><td>Salton Seahorse (PR)</td><td>0x860D8FF9</td><td>Yes</td><td>3344</td><td>0x80009004</td><td>0x00004161</td></tr>
<tr><td>Salton Seahorse (PR) (Driver)</td><td>0xDD8E3154</td><td>Yes</td><td>3687</td><td>0x80009536</td><td>0x0001319D</td></tr>
<tr><td>Salton Seahorse (PR) (Full)</td><td>0x0606C113</td><td>Yes</td><td>3689</td><td>0x80009538</td><td>0x00008D01</td></tr>
<tr><td>Salton_Driver</td><td>0x654931B3</td><td>No</td><td>5089</td><td>0x8000A418</td><td>0x0000CFD0</td></tr>
<tr><td>Satellite Designator</td><td>0x9ADAB72A</td><td>No</td><td>385</td><td>0x800052F3</td><td>0x00007761</td></tr>
<tr><td>Scooter</td><td>0x5EAC70AA</td><td>No</td><td>2239</td><td>0x8000820E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Scooter (Driver)</td><td>0xBD18B811</td><td>No</td><td>2286</td><td>0x8000824A</td><td>0x00008BD9</td></tr>
<tr><td>Scooter (Driver) (Civ casual female)</td><td>0x40048AA9</td><td>No</td><td>4241</td><td>0x80009C87</td><td>0x0000C3EF</td></tr>
<tr><td>Scooter (Driver) (Civ casual male)</td><td>0x0FD71A8C</td><td>No</td><td>4240</td><td>0x80009C86</td><td>0x00007527</td></tr>
<tr><td>Scooter (Driver) (Civ poor female)</td><td>0xAD797E46</td><td>No</td><td>4243</td><td>0x80009C89</td><td>0x000082BE</td></tr>
<tr><td>Scooter (Driver) (Civ poor male)</td><td>0x0850EC7B</td><td>No</td><td>4242</td><td>0x80009C88</td><td>0x00010F3A</td></tr>
<tr><td>Scooter (Driver) (Civ rich female)</td><td>0x62202290</td><td>No</td><td>4298</td><td>0x80009CC5</td><td>0x00008C80</td></tr>
<tr><td>Scooter_Driver</td><td>0xE5EC037B</td><td>No</td><td>5107</td><td>0x8000A44E</td><td>0x000088E5</td></tr>
<tr><td>Scooter_OC021</td><td>0x5D965E06</td><td>No</td><td>5128</td><td>0x8000A46D</td><td>0x000098AB</td></tr>
<tr><td>Scorpion90</td><td>0x46E480D9</td><td>Yes</td><td>1198</td><td>0x80006CAE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Scorpion90 (Driver)</td><td>0xC08A6A34</td><td>Yes</td><td>1610</td><td>0x8000724F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Scorpion90 (Driver) (PMC001)</td><td>0xF44925BE</td><td>Yes</td><td>2543</td><td>0x8000856C</td><td>0x00001439</td></tr>
<tr><td>Scorpion90 (Full)</td><td>0x4504E573</td><td>Yes</td><td>1137</td><td>0x80006B60</td><td>0xFFFFFFFF</td></tr>
<tr><td>Scrubs</td><td>0xB099EE89</td><td>No</td><td>620</td><td>0x80005C2E</td><td>0x00004109</td></tr>
<tr><td>Secondary Equipment</td><td>0x904302A5</td><td>No</td><td>706</td><td>0x80005FD1</td><td>0x0000BB17</td></tr>
<tr><td>Semi (Base)</td><td>0x1077B77D</td><td>No</td><td>1788</td><td>0x800075EE</td><td>0x00004B5E</td></tr>
<tr><td>SF LowRoad</td><td>0xB9A67D1A</td><td>No</td><td>100</td><td>0x80004C01</td><td>0x000034A8</td></tr>
<tr><td>Shockwave_C4</td><td>0x42A66B28</td><td>No</td><td>2011</td><td>0x80008041</td><td>0xFFFFFFFF</td></tr>
<tr><td>Shockwaves</td><td>0x963C4A61</td><td>No</td><td>2010</td><td>0x80008040</td><td>0xFFFFFFFF</td></tr>
<tr><td>Shotgun</td><td>0xFA8FBA6D</td><td>No</td><td>461</td><td>0x8000569D</td><td>0x0001383B</td></tr>
<tr><td>Shotgun (Window Spawner)</td><td>0x230B031A</td><td>No</td><td>3002</td><td>0x80008A22</td><td>0x0001270F</td></tr>
<tr><td>Shotgun Bullet</td><td>0xC846C397</td><td>No</td><td>464</td><td>0x800056A0</td><td>0x0000D2EA</td></tr>
<tr><td>Sidecar Motorcycle</td><td>0x07856105</td><td>Yes</td><td>2597</td><td>0x800085EB</td><td>0x0000FE41</td></tr>
<tr><td>Sidecar Motorcycle (Driver)</td><td>0xA9456B10</td><td>Yes</td><td>3843</td><td>0x800097FD</td><td>0x0000F835</td></tr>
<tr><td>Sidecar Motorcycle (Full)</td><td>0x74651AA7</td><td>Yes</td><td>3844</td><td>0x800097FE</td><td>0xFFFFFFFF</td></tr>
<tr><td>SideCarMotorcycle_Driver</td><td>0x9C5FC386</td><td>Yes</td><td>5386</td><td>0x8000A97A</td><td>0xFFFFFFFF</td></tr>
<tr><td>SimplePointSpawner</td><td>0x639DA6DD</td><td>No</td><td>90</td><td>0x80004B95</td><td>0xFFFFFFFF</td></tr>
<tr><td>skyscraper2x4</td><td>0x27737148</td><td>No</td><td>781</td><td>0x80006227</td><td>0xFFFFFFFF</td></tr>
<tr><td>Small Fishing Boat</td><td>0xA18CEEA2</td><td>Yes</td><td>1772</td><td>0x800075DE</td><td>0x0000B151</td></tr>
<tr><td>Small Fishing Boat (Driver)</td><td>0xF49EC349</td><td>Yes</td><td>1774</td><td>0x800075E0</td><td>0x0000E72C</td></tr>
<tr><td>Small Fishing Boat (Driver) (Civ Poor female)</td><td>0x4CC307AE</td><td>Yes</td><td>4657</td><td>0x80009FD3</td><td>0x00009B49</td></tr>
<tr><td>Small Fishing Boat (Driver) (Civ Poor male)</td><td>0xC94477E3</td><td>Yes</td><td>4656</td><td>0x80009FD2</td><td>0xFFFFFFFF</td></tr>
<tr><td>small_boats</td><td>0xFA95731A</td><td>Yes</td><td>5512</td><td>0x8000AAC7</td><td>0x00011AD1</td></tr>
<tr><td>SmallFishingBoat_Driver</td><td>0x2ADA33A7</td><td>Yes</td><td>5144</td><td>0x8000A480</td><td>0x0000EF29</td></tr>
<tr><td>SmallFlame</td><td>0x7E73F9C7</td><td>No</td><td>1101</td><td>0x80006A86</td><td>0x0001373F</td></tr>
<tr><td>Smart Bomb Projectile</td><td>0x5755AD55</td><td>No</td><td>3170</td><td>0x80008E45</td><td>0x0000695C</td></tr>
<tr><td>smg</td><td>0x858035CC</td><td>No</td><td>1126</td><td>0x80006B54</td><td>0xFFFFFFFF</td></tr>
<tr><td>SMG Bullet</td><td>0x17D01624</td><td>No</td><td>1128</td><td>0x80006B56</td><td>0x0000CE12</td></tr>
<tr><td>Smoke Designator</td><td>0xCA109D56</td><td>No</td><td>384</td><td>0x800052F2</td><td>0x00004AD1</td></tr>
<tr><td>Smoke Grenade Projectile</td><td>0xF7208F3F</td><td>No</td><td>1933</td><td>0x80007D95</td><td>0x00010523</td></tr>
<tr><td>SndEmitter_ShantyRadio</td><td>0x09BEF713</td><td>No</td><td>1155</td><td>0x80006BA8</td><td>0xFFFFFFFF</td></tr>
<tr><td>Sniper Rifle</td><td>0xEA4DEF62</td><td>No</td><td>458</td><td>0x8000569A</td><td>0x00008D2E</td></tr>
<tr><td>Sniper Rifle (AA Backup)</td><td>0x2AF0A2AB</td><td>No</td><td>5903</td><td>0x8000B036</td><td>0x0000DB34</td></tr>
<tr><td>Sniper Rifle (SVD)</td><td>0x4D3161D0</td><td>No</td><td>1109</td><td>0x80006B43</td><td>0xFFFFFFFF</td></tr>
<tr><td>Sniper Rifle Bullet</td><td>0xCD44A052</td><td>No</td><td>459</td><td>0x8000569B</td><td>0x0000D0D5</td></tr>
<tr><td>SoccerBallProp</td><td>0x68632398</td><td>No</td><td>3948</td><td>0x80009872</td><td>0x00001206</td></tr>
<tr><td>Solano</td><td>0xA69995AF</td><td>No</td><td>821</td><td>0x80006324</td><td>0x00005153</td></tr>
<tr><td>soldier</td><td>0x75E8C74D</td><td>No</td><td>30</td><td>0x8000437F</td><td>0x00007172</td></tr>
<tr><td>SoundEmitter</td><td>0x08E7BCC8</td><td>No</td><td>1154</td><td>0x80006BA7</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial</td><td>0x3CB9AED5</td><td>No</td><td>6021</td><td>0x9000012F</td><td>0x00000A92</td></tr>
<tr><td>SoundMaterial ((veh_motorcycl</td><td>0x6A0DB29F</td><td>Yes</td><td>3923</td><td>0x80009854</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (ArmoredVehicle)</td><td>0xCDEC35F0</td><td>No</td><td>6034</td><td>0x9000013C</td><td>0x0000B23B</td></tr>
<tr><td>SoundMaterial (bldg_bunker)</td><td>0x42246AB5</td><td>No</td><td>3855</td><td>0x8000980E</td><td>0x00007049</td></tr>
<tr><td>SoundMaterial (bldg_default)</td><td>0xB78AC49F</td><td>No</td><td>6022</td><td>0x90000130</td><td>0x00007648</td></tr>
<tr><td>SoundMaterial (bldg_glass)</td><td>0x2A04FAA6</td><td>No</td><td>3856</td><td>0x8000980F</td><td>0x00000EFC</td></tr>
<tr><td>SoundMaterial (bldg_metal)</td><td>0x683F901D</td><td>No</td><td>6032</td><td>0x9000013A</td><td>0x00003BB1</td></tr>
<tr><td>SoundMaterial (bldg_stone)</td><td>0xB414CABB</td><td>No</td><td>6031</td><td>0x90000139</td><td>0x00002421</td></tr>
<tr><td>SoundMaterial (bldg_stone_large)</td><td>0x29A327A7</td><td>No</td><td>2801</td><td>0x80008767</td><td>0x000051A8</td></tr>
<tr><td>SoundMaterial (bldg_wood)</td><td>0xD608DEC9</td><td>No</td><td>6033</td><td>0x9000013B</td><td>0x000033E4</td></tr>
<tr><td>SoundMaterial (BrickProp)</td><td>0xD9A26AA4</td><td>No</td><td>6030</td><td>0x90000138</td><td>0x0000E7BE</td></tr>
<tr><td>SoundMaterial (debris_oilrig) 0x8000a6f5</td><td>0xA0616178</td><td>No</td><td>5251</td><td>0x8000A6F5</td><td>0x00013973</td></tr>
<tr><td>SoundMaterial (hum_civ)</td><td>0xF21BD6EB</td><td>No</td><td>3857</td><td>0x80009810</td><td>0x0000DA15</td></tr>
<tr><td>SoundMaterial (hum_hero_chris)</td><td>0xA4CCA57D</td><td>No</td><td>3938</td><td>0x80009863</td><td>0x0000D592</td></tr>
<tr><td>SoundMaterial (hum_hero_jen)</td><td>0x6A4B7D7B</td><td>No</td><td>3939</td><td>0x80009864</td><td>0x0000887D</td></tr>
<tr><td>SoundMaterial (hum_hero_mattias)</td><td>0x99BB8D1F</td><td>No</td><td>3940</td><td>0x80009865</td><td>0x0000F8A7</td></tr>
<tr><td>SoundMaterial (hum_soldier)</td><td>0x2069C0EF</td><td>No</td><td>6036</td><td>0x9000013E</td><td>0x0000DC6D</td></tr>
<tr><td>SoundMaterial (Human)</td><td>0x7D2D50F1</td><td>No</td><td>6026</td><td>0x90000134</td><td>0x0000674C</td></tr>
<tr><td>SoundMaterial (Projectile)</td><td>0xDD1AECD1</td><td>No</td><td>6025</td><td>0x90000133</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (projectile_bullet_heavyMG)</td><td>0x8366D4FC</td><td>No</td><td>3858</td><td>0x80009811</td><td>0x0000CD27</td></tr>
<tr><td>SoundMaterial (projectile_bullet_rifle)</td><td>0xC181A3C5</td><td>No</td><td>3859</td><td>0x80009812</td><td>0x0000FE69</td></tr>
<tr><td>SoundMaterial (projectile_grapple)</td><td>0x197888C1</td><td>No</td><td>6035</td><td>0x9000013D</td><td>0x0000D070</td></tr>
<tr><td>SoundMaterial (projectile_rocket)</td><td>0x3DA89DF0</td><td>No</td><td>3860</td><td>0x80009813</td><td>0x00012575</td></tr>
<tr><td>SoundMaterial (Prop)</td><td>0x944539D3</td><td>No</td><td>6024</td><td>0x90000132</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_barreldrum)</td><td>0xDC7B841E</td><td>No</td><td>3854</td><td>0x8000980C</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_fabric)</td><td>0xD0D32A77</td><td>No</td><td>3876</td><td>0x80009824</td><td>0x0000633B</td></tr>
<tr><td>SoundMaterial (prop_fabric_lrg)</td><td>0x4F3E72AB</td><td>No</td><td>3863</td><td>0x80009816</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_fabric_sml)</td><td>0xEC0900A0</td><td>No</td><td>3864</td><td>0x80009817</td><td>0x000047D9</td></tr>
<tr><td>SoundMaterial (prop_foliage)</td><td>0xF0083103</td><td>No</td><td>3875</td><td>0x80009823</td><td>0x00003B5A</td></tr>
<tr><td>SoundMaterial (prop_foliage_lrg)</td><td>0x2E032F8F</td><td>No</td><td>3865</td><td>0x80009818</td><td>0x00000A7A</td></tr>
<tr><td>SoundMaterial (prop_foliage_med)</td><td>0x0433A3C6</td><td>No</td><td>3867</td><td>0x8000981A</td><td>0x0000FBDC</td></tr>
<tr><td>SoundMaterial (prop_foliage_sml)</td><td>0x1D4D54A4</td><td>No</td><td>3866</td><td>0x80009819</td><td>0x00009627</td></tr>
<tr><td>SoundMaterial (prop_glass)</td><td>0x7C81F92C</td><td>No</td><td>4303</td><td>0x80009CCA</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_metal)</td><td>0x3BBA0CD7</td><td>No</td><td>6027</td><td>0x90000135</td><td>0x00010D81</td></tr>
<tr><td>SoundMaterial (prop_metal_chainlinkfence)</td><td>0xC85544D4</td><td>No</td><td>3868</td><td>0x8000981B</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_metal_lrg)</td><td>0xFF9FB98B</td><td>No</td><td>3870</td><td>0x8000981E</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_metal_med)</td><td>0x041639AA</td><td>No</td><td>3869</td><td>0x8000981D</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_metal_sml)</td><td>0x1DA6B280</td><td>No</td><td>3871</td><td>0x8000981F</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_metalpole_lrg)</td><td>0xF0ECD9CD</td><td>No</td><td>3872</td><td>0x80009820</td><td>0x00005B3A</td></tr>
<tr><td>SoundMaterial (prop_metalpole_sml)</td><td>0x71CD1C76</td><td>No</td><td>3873</td><td>0x80009821</td><td>0x00007A49</td></tr>
<tr><td>SoundMaterial (prop_rubber_tire)</td><td>0x4AAF9A99</td><td>No</td><td>3874</td><td>0x80009822</td><td>0x00001912</td></tr>
<tr><td>SoundMaterial (prop_sandbag)</td><td>0x9B218104</td><td>No</td><td>3877</td><td>0x80009825</td><td>0x00002FF5</td></tr>
<tr><td>SoundMaterial (prop_sheetmetal_lrg)</td><td>0x7291193C</td><td>No</td><td>3878</td><td>0x80009826</td><td>0x00008A4B</td></tr>
<tr><td>SoundMaterial (prop_sheetmetal_med)</td><td>0xAFBBFD71</td><td>No</td><td>3879</td><td>0x80009827</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_sheetmetal_sml)</td><td>0x7F4D9347</td><td>No</td><td>6028</td><td>0x90000136</td><td>0x00011028</td></tr>
<tr><td>SoundMaterial (prop_stone)</td><td>0xF0344971</td><td>No</td><td>3880</td><td>0x80009828</td><td>0x00012429</td></tr>
<tr><td>SoundMaterial (prop_stone_lrg)</td><td>0x778E81E9</td><td>No</td><td>3881</td><td>0x80009829</td><td>0x00008E70</td></tr>
<tr><td>SoundMaterial (prop_stone_med)</td><td>0x89D18648</td><td>No</td><td>3882</td><td>0x8000982A</td><td>0x0000AE90</td></tr>
<tr><td>SoundMaterial (prop_stone_sml)</td><td>0xB3467632</td><td>No</td><td>3883</td><td>0x8000982B</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_tree)</td><td>0xF97D8862</td><td>No</td><td>3884</td><td>0x8000982C</td><td>0x00006778</td></tr>
<tr><td>SoundMaterial (prop_tree_lrg)</td><td>0xCADD03AE</td><td>No</td><td>3885</td><td>0x8000982D</td><td>0x000017E9</td></tr>
<tr><td>SoundMaterial (prop_tree_med)</td><td>0xABBA1A3B</td><td>No</td><td>3886</td><td>0x8000982E</td><td>0x0000F94D</td></tr>
<tr><td>SoundMaterial (prop_tree_sml)</td><td>0xFD72BA2D</td><td>No</td><td>3887</td><td>0x8000982F</td><td>0x00010DB3</td></tr>
<tr><td>SoundMaterial (prop_wood)</td><td>0x80FE5283</td><td>No</td><td>6029</td><td>0x90000137</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_wood_crate)</td><td>0x24D65F3B</td><td>No</td><td>3888</td><td>0x80009830</td><td>0x000137FA</td></tr>
<tr><td>SoundMaterial (prop_wood_lrg)</td><td>0x2299E90F</td><td>No</td><td>3889</td><td>0x80009831</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (prop_wood_med)</td><td>0xF8CA5D46</td><td>No</td><td>3890</td><td>0x80009832</td><td>0x00003587</td></tr>
<tr><td>SoundMaterial (prop_wood_sml)</td><td>0x11E40E24</td><td>No</td><td>3891</td><td>0x80009833</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (SheetMetalProp)</td><td>0xBCBA4A55</td><td>No</td><td>5249</td><td>0x8000A6F2</td><td>0x000104F4</td></tr>
<tr><td>SoundMaterial (terrain)</td><td>0x0C9229E5</td><td>No</td><td>3892</td><td>0x80009834</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (terrain_asphalt)</td><td>0x9353CDF9</td><td>No</td><td>3893</td><td>0x80009835</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (terrain_dirt)</td><td>0x0069F079</td><td>No</td><td>3895</td><td>0x80009837</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (terrain_grass)</td><td>0x64D2EB70</td><td>No</td><td>3894</td><td>0x80009836</td><td>0x0001351F</td></tr>
<tr><td>SoundMaterial (terrain_sand)</td><td>0x99787256</td><td>No</td><td>3896</td><td>0x80009838</td><td>0x000020D1</td></tr>
<tr><td>SoundMaterial (veh)</td><td>0xA240211F</td><td>No</td><td>3897</td><td>0x80009839</td><td>0x00001492</td></tr>
<tr><td>SoundMaterial (veh_armored)</td><td>0xBE063886</td><td>Yes</td><td>3898</td><td>0x8000983A</td><td>0x00009B0B</td></tr>
<tr><td>SoundMaterial (veh_armored_bottom_skids)</td><td>0xBDE9EC61</td><td>Yes</td><td>3899</td><td>0x8000983B</td><td>0x00009E51</td></tr>
<tr><td>SoundMaterial (veh_armored_bottom_tracked)</td><td>0x72550BFB</td><td>Yes</td><td>3900</td><td>0x8000983C</td><td>0x0000A283</td></tr>
<tr><td>SoundMaterial (veh_armored_bottom_wheeled)</td><td>0xF6EC0973</td><td>Yes</td><td>3901</td><td>0x8000983D</td><td>0x0001340B</td></tr>
<tr><td>SoundMaterial (veh_armored_heli_rotor)</td><td>0xD748B4E6</td><td>Yes</td><td>3902</td><td>0x8000983F</td><td>0x00013F84</td></tr>
<tr><td>SoundMaterial (veh_armored_light)</td><td>0x6C91197D</td><td>Yes</td><td>3903</td><td>0x80009840</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (veh_armored_med)</td><td>0x29575C2F</td><td>Yes</td><td>3904</td><td>0x80009841</td><td>0x00011A65</td></tr>
<tr><td>SoundMaterial (veh_armored_ruin)</td><td>0x20792A2F</td><td>Yes</td><td>3905</td><td>0x80009842</td><td>0x0000688B</td></tr>
<tr><td>SoundMaterial (veh_armored_tank)</td><td>0x338C6E41</td><td>Yes</td><td>3906</td><td>0x80009843</td><td>0x000073DC</td></tr>
<tr><td>SoundMaterial (veh_armored_tank_turret)</td><td>0x825464A6</td><td>Yes</td><td>3907</td><td>0x80009844</td><td>0x0000B2BF</td></tr>
<tr><td>SoundMaterial (veh_boat_lrg)</td><td>0xFD1F4378</td><td>Yes</td><td>3908</td><td>0x80009845</td><td>0x00004E1C</td></tr>
<tr><td>SoundMaterial (veh_boat_med)</td><td>0xBD5F1525</td><td>Yes</td><td>3909</td><td>0x80009846</td><td>0x0000A24C</td></tr>
<tr><td>SoundMaterial (veh_boat_sml)</td><td>0x2A14BE53</td><td>Yes</td><td>3910</td><td>0x80009847</td><td>0x0000B510</td></tr>
<tr><td>SoundMaterial (veh_civ)</td><td>0x075715DE</td><td>Yes</td><td>3911</td><td>0x80009848</td><td>0x0000EF75</td></tr>
<tr><td>SoundMaterial (veh_civ_bottom)</td><td>0xEBED61C6</td><td>Yes</td><td>3912</td><td>0x80009849</td><td>0x0000F2BB</td></tr>
<tr><td>SoundMaterial (veh_civ_bumper)</td><td>0xC8EDEBBA</td><td>Yes</td><td>3913</td><td>0x8000984A</td><td>0x000136BE</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg)</td><td>0xAAC80002</td><td>Yes</td><td>3914</td><td>0x8000984B</td><td>0x000132C0</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_bottom)</td><td>0x00881382</td><td>Yes</td><td>3915</td><td>0x8000984C</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_bumper)</td><td>0xD160FF96</td><td>Yes</td><td>3916</td><td>0x8000984D</td><td>0x00001E3D</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_ruin)</td><td>0xFDAED94B</td><td>Yes</td><td>3917</td><td>0x8000984E</td><td>0x0000FDE8</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_sides)</td><td>0x641AE6C1</td><td>Yes</td><td>3918</td><td>0x8000984F</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (veh_civ_lrg_top)</td><td>0x7619BA46</td><td>Yes</td><td>3919</td><td>0x80009850</td><td>0x0000AE1A</td></tr>
<tr><td>SoundMaterial (veh_civ_ruin)</td><td>0xFA79D447</td><td>Yes</td><td>3920</td><td>0x80009851</td><td>0x0000BC84</td></tr>
<tr><td>SoundMaterial (veh_civ_sides)</td><td>0x2651CC55</td><td>Yes</td><td>3921</td><td>0x80009852</td><td>0x000124B8</td></tr>
<tr><td>SoundMaterial (veh_civ_top)</td><td>0x3A81BB2A</td><td>Yes</td><td>3922</td><td>0x80009853</td><td>0x00002C69</td></tr>
<tr><td>SoundMaterial (veh_motorcycle)</td><td>0x1A68F603</td><td>Yes</td><td>3924</td><td>0x80009855</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (veh_motorcycle_ruin)</td><td>0xD3DBAF10</td><td>Yes</td><td>3925</td><td>0x80009856</td><td>0x000004E6</td></tr>
<tr><td>SoundMaterial (veh_motorcycle_wheels)</td><td>0xBEC0535A</td><td>Yes</td><td>3926</td><td>0x80009857</td><td>0x000027BE</td></tr>
<tr><td>SoundMaterial (Vehicle)</td><td>0xE1E412C0</td><td>No</td><td>6023</td><td>0x90000131</td><td>0x0000CA54</td></tr>
<tr><td>SoundMaterial (water)</td><td>0xC95CA2AB</td><td>No</td><td>3927</td><td>0x80009858</td><td>0x000031DF</td></tr>
<tr><td>SoundMaterial (water_deep)</td><td>0x325ADAA8</td><td>No</td><td>3928</td><td>0x80009859</td><td>0x00003A7B</td></tr>
<tr><td>SoundMaterial (water_puddle)</td><td>0x60C7DECE</td><td>No</td><td>3929</td><td>0x8000985A</td><td>0x00012C17</td></tr>
<tr><td>SoundMaterial (water_shallow)</td><td>0xB010267C</td><td>No</td><td>3930</td><td>0x8000985B</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (Weapon)</td><td>0x17688DCE</td><td>No</td><td>3861</td><td>0x80009814</td><td>0x00012CE7</td></tr>
<tr><td>SoundMaterial (wpn_c4)</td><td>0x65D717CD</td><td>No</td><td>3931</td><td>0x8000985C</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (wpn_clip)</td><td>0xFB97ACE0</td><td>No</td><td>3932</td><td>0x8000985D</td><td>0x0000BAF1</td></tr>
<tr><td>SoundMaterial (wpn_designator)</td><td>0x5E83C924</td><td>No</td><td>3933</td><td>0x8000985E</td><td>0x000002EA</td></tr>
<tr><td>SoundMaterial (wpn_emplacedgun)</td><td>0xA5909613</td><td>No</td><td>3934</td><td>0x8000985F</td><td>0x00000216</td></tr>
<tr><td>SoundMaterial (wpn_grenade)</td><td>0xAE30CA36</td><td>No</td><td>3862</td><td>0x80009815</td><td>0xFFFFFFFF</td></tr>
<tr><td>SoundMaterial (wpn_pistol)</td><td>0x7A95CCE1</td><td>No</td><td>3935</td><td>0x80009860</td><td>0x0000A42D</td></tr>
<tr><td>SoundMaterial (wpn_rifle)</td><td>0x641CD0EA</td><td>No</td><td>3936</td><td>0x80009861</td><td>0x000085A9</td></tr>
<tr><td>SoundMaterial (wpn_rocket)</td><td>0x45C9DAE6</td><td>No</td><td>3937</td><td>0x80009862</td><td>0x0000B9BD</td></tr>
<tr><td>Spawnable</td><td>0xE2B0DE0E</td><td>No</td><td>39</td><td>0x8000450B</td><td>0x0000778E</td></tr>
<tr><td>Spawners</td><td>0x2FEE679A</td><td>No</td><td>37</td><td>0x80004509</td><td>0x00001CEC</td></tr>
<tr><td>Spawnlist (Allied AA)</td><td>0xAA950B00</td><td>No</td><td>4054</td><td>0x80009ADF</td><td>0x00009379</td></tr>
<tr><td>Spawnlist (Allied Balcony)</td><td>0x90093EB0</td><td>No</td><td>1570</td><td>0x8000720D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (Allied Destroyer Crew)</td><td>0x40EA8E78</td><td>Yes</td><td>4060</td><td>0x80009AE5</td><td>0x00002568</td></tr>
<tr><td>Spawnlist (Allied Ground)</td><td>0x66BAA21D</td><td>No</td><td>1569</td><td>0x8000720C</td><td>0x0001106B</td></tr>
<tr><td>Spawnlist (Allied Prisoner)</td><td>0xCF53FF46</td><td>No</td><td>2372</td><td>0x80008327</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (Allied Tower AA)</td><td>0x56C3EB9F</td><td>No</td><td>5869</td><td>0x8000B010</td><td>0x00001882</td></tr>
<tr><td>Spawnlist (Allied Tower AT)</td><td>0x3F28B48C</td><td>No</td><td>5868</td><td>0x8000B00E</td><td>0x000011E2</td></tr>
<tr><td>Spawnlist (Allied Tower)</td><td>0x08150331</td><td>No</td><td>5867</td><td>0x8000B00D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (Allied Window)</td><td>0x2073D612</td><td>No</td><td>5898</td><td>0x8000B02F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (CHI BasePeds)</td><td>0x380C69EA</td><td>No</td><td>3077</td><td>0x80008BA1</td><td>0x00002C1E</td></tr>
<tr><td>Spawnlist (CHI BaseTanks)</td><td>0x8F9CCA13</td><td>Yes</td><td>3078</td><td>0x80008BA2</td><td>0x00010A52</td></tr>
<tr><td>Spawnlist (CHI BaseVehicles)</td><td>0xBB23D451</td><td>No</td><td>3076</td><td>0x80008BA0</td><td>0x0000CF46</td></tr>
<tr><td>Spawnlist (ChiCon002)</td><td>0x48AC633B</td><td>No</td><td>2401</td><td>0x800083EF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (China AA)</td><td>0x84DAB5CC</td><td>No</td><td>3176</td><td>0x80008E4C</td><td>0x0000B1AD</td></tr>
<tr><td>Spawnlist (China Balcony)</td><td>0xE63107BC</td><td>No</td><td>3174</td><td>0x80008E49</td><td>0x000089F1</td></tr>
<tr><td>Spawnlist (China Destroyer Crew)</td><td>0xFC902B0C</td><td>Yes</td><td>4061</td><td>0x80009AE6</td><td>0x0000A8E7</td></tr>
<tr><td>Spawnlist (China Ground)</td><td>0xC6B39751</td><td>No</td><td>3175</td><td>0x80008E4B</td><td>0x00006D20</td></tr>
<tr><td>Spawnlist (China Tower AA)</td><td>0xF6C4622B</td><td>No</td><td>5866</td><td>0x8000B00C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (China Tower RPG)</td><td>0x1F6DA07A</td><td>No</td><td>5865</td><td>0x8000B00B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (China Tower)</td><td>0x214FB215</td><td>No</td><td>5864</td><td>0x8000B00A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (China Window)</td><td>0x64BF7076</td><td>No</td><td>5899</td><td>0x8000B030</td><td>0x00002A78</td></tr>
<tr><td>Spawnlist (Chinese Prisoner)</td><td>0xACEDECCA</td><td>No</td><td>2373</td><td>0x80008328</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (Civilian Default)</td><td>0x665509FB</td><td>No</td><td>1573</td><td>0x80007210</td><td>0x00006640</td></tr>
<tr><td>Spawnlist (Guerilla AA)</td><td>0x517C4F32</td><td>No</td><td>5904</td><td>0x8000B037</td><td>0x00011E9B</td></tr>
<tr><td>Spawnlist (Guerilla Balcony)</td><td>0x42167CDE</td><td>No</td><td>1568</td><td>0x8000720B</td><td>0x00013FE1</td></tr>
<tr><td>Spawnlist (Guerilla Ground)</td><td>0x9AFAD237</td><td>No</td><td>1567</td><td>0x8000720A</td><td>0x000133EA</td></tr>
<tr><td>Spawnlist (Guerilla Prisoner)</td><td>0x56B94A1C</td><td>No</td><td>2374</td><td>0x8000832A</td><td>0x00010A2F</td></tr>
<tr><td>Spawnlist (Guerilla Tower RPG)</td><td>0x7DE5C088</td><td>No</td><td>5863</td><td>0x8000B009</td><td>0x00002197</td></tr>
<tr><td>Spawnlist (Guerilla Tower)</td><td>0x1A0B5733</td><td>No</td><td>5862</td><td>0x8000B008</td><td>0x00006A80</td></tr>
<tr><td>Spawnlist (Guerilla Window)</td><td>0xCD6A29CC</td><td>No</td><td>5900</td><td>0x8000B032</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (M1A2 (Full))</td><td>0x62946724</td><td>Yes</td><td>5530</td><td>0x8000AB40</td><td>0x00001ECE</td></tr>
<tr><td>Spawnlist (OC AA)</td><td>0x6E25992F</td><td>No</td><td>5897</td><td>0x8000B02E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (OC Balcony)</td><td>0x51866F91</td><td>No</td><td>1360</td><td>0x80006ECB</td><td>0x000086EC</td></tr>
<tr><td>Spawnlist (OC Ground)</td><td>0x31E2D3EE</td><td>No</td><td>1356</td><td>0x80006EC7</td><td>0x0000EE98</td></tr>
<tr><td>Spawnlist (OC Prisoner)</td><td>0x65CFF4F9</td><td>No</td><td>2369</td><td>0x80008324</td><td>0x0000C3A7</td></tr>
<tr><td>Spawnlist (OC Tower Elite)</td><td>0x746381A3</td><td>No</td><td>2535</td><td>0x80008562</td><td>0x000016DF</td></tr>
<tr><td>Spawnlist (OC Tower GL)</td><td>0xAA726291</td><td>No</td><td>5861</td><td>0x8000B007</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (OC Tower)</td><td>0x736F058C</td><td>No</td><td>5860</td><td>0x8000B006</td><td>0x00001541</td></tr>
<tr><td>Spawnlist (OC Window)</td><td>0x77C26C99</td><td>No</td><td>5901</td><td>0x8000B033</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (Pirate AA)</td><td>0x9A3367B2</td><td>No</td><td>5906</td><td>0x8000B039</td><td>0x00006F1A</td></tr>
<tr><td>Spawnlist (Pirate Balcony)</td><td>0x68D9A65E</td><td>No</td><td>1566</td><td>0x80007209</td><td>0x00011335</td></tr>
<tr><td>Spawnlist (Pirate Ground)</td><td>0xB42AF2B7</td><td>No</td><td>1565</td><td>0x80007208</td><td>0x0001372B</td></tr>
<tr><td>Spawnlist (Pirate Prisoner)</td><td>0xDBF39E9C</td><td>No</td><td>2375</td><td>0x8000832B</td><td>0x0000CBDF</td></tr>
<tr><td>Spawnlist (Pirate Tower)</td><td>0x70D104B3</td><td>No</td><td>5859</td><td>0x8000B005</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (Pirate Window)</td><td>0xE69A4A4C</td><td>No</td><td>5902</td><td>0x8000B034</td><td>0x000058E4</td></tr>
<tr><td>Spawnlist (VZ AA)</td><td>0xF9ADB995</td><td>No</td><td>2416</td><td>0x80008450</td><td>0x000100BA</td></tr>
<tr><td>Spawnlist (VZ Balcony AT)</td><td>0x932DE232</td><td>No</td><td>3010</td><td>0x80008A2A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ Balcony)</td><td>0x1E14B42B</td><td>No</td><td>1358</td><td>0x80006EC9</td><td>0x00011811</td></tr>
<tr><td>Spawnlist (VZ Barracks Ground)</td><td>0x9A7C5879</td><td>No</td><td>2199</td><td>0x800081E4</td><td>0x0000A10B</td></tr>
<tr><td>Spawnlist (VZ Barracks Ground_wRPG)</td><td>0xB0223410</td><td>No</td><td>5914</td><td>0x8000B0CB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ BaseVehicles)</td><td>0xFA9BF1C7</td><td>No</td><td>3075</td><td>0x80008B9F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ Elite)</td><td>0x7C903D04</td><td>No</td><td>2399</td><td>0x800083EC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ Ground)</td><td>0x7B4587E4</td><td>No</td><td>1022</td><td>0x800068A7</td><td>0x000006D6</td></tr>
<tr><td>Spawnlist (VZ Mixed Patrol)</td><td>0x8F2DBB04</td><td>No</td><td>2541</td><td>0x80008568</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ RPG + Rifle)</td><td>0x47E72343</td><td>No</td><td>2990</td><td>0x80008A16</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ RPG Patrol)</td><td>0xAE49DABC</td><td>No</td><td>2537</td><td>0x80008564</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ RPG)</td><td>0xC8F924D8</td><td>No</td><td>2395</td><td>0x800083E7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ Tower AA)</td><td>0xC26D48FE</td><td>No</td><td>5858</td><td>0x8000B004</td><td>0x00004AAD</td></tr>
<tr><td>Spawnlist (VZ Tower RPG)</td><td>0x32E8CBED</td><td>No</td><td>5857</td><td>0x8000B003</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ Tower RPG) 0x8000b2fa</td><td>0xBBA759B4</td><td>No</td><td>5966</td><td>0x8000B2FA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Spawnlist (VZ Tower)</td><td>0xEE307A42</td><td>No</td><td>5856</td><td>0x8000B001</td><td>0x0000505A</td></tr>
<tr><td>Spawnlist (VZ Window)</td><td>0x5C4ACD6F</td><td>No</td><td>4077</td><td>0x80009AF7</td><td>0x00003D25</td></tr>
<tr><td>Speed Boat</td><td>0xF6515BBC</td><td>Yes</td><td>1082</td><td>0x80006A22</td><td>0x00008E4F</td></tr>
<tr><td>Speed Boat (Driver)</td><td>0xF3EEE47B</td><td>Yes</td><td>1609</td><td>0x8000724E</td><td>0x000038D6</td></tr>
<tr><td>Speed Boat (Driver) (Civ Beach A Female)</td><td>0x4FE1C572</td><td>Yes</td><td>4658</td><td>0x80009FD4</td><td>0x0000CA86</td></tr>
<tr><td>Speed Boat (Driver) (Civ Beach B Female)</td><td>0xBB059AF5</td><td>Yes</td><td>4659</td><td>0x80009FD5</td><td>0x0000B282</td></tr>
<tr><td>Speed Boat (Driver) (Civ Beach C Female)</td><td>0xFFFAB0A4</td><td>Yes</td><td>4660</td><td>0x80009FD6</td><td>0x000108B8</td></tr>
<tr><td>Speed Boat (Driver) (Civ Beach D Female)</td><td>0xC5C88D67</td><td>Yes</td><td>4661</td><td>0x80009FD7</td><td>0x00006672</td></tr>
<tr><td>Speed Boat (Full)</td><td>0x69A995F8</td><td>Yes</td><td>3682</td><td>0x80009531</td><td>0x000104A1</td></tr>
<tr><td>Sportbike (Civ)</td><td>0x2F26B7F9</td><td>No</td><td>2241</td><td>0x80008216</td><td>0x0000D7C7</td></tr>
<tr><td>Sportbike (Civ) (black)</td><td>0x2CA1CF5B</td><td>No</td><td>5590</td><td>0x8000AC45</td><td>0xFFFFFFFF</td></tr>
<tr><td>Sportbike (Civ) (blue)</td><td>0x705901CE</td><td>No</td><td>5589</td><td>0x8000AC44</td><td>0x00007BB7</td></tr>
<tr><td>Sportbike (Civ) (Driver)</td><td>0x7E6F2954</td><td>No</td><td>2287</td><td>0x8000824B</td><td>0x0000AF29</td></tr>
<tr><td>Sportbike (Civ) (Driver) (Civ casual female)</td><td>0x64C5B500</td><td>No</td><td>4239</td><td>0x80009C85</td><td>0x000048C2</td></tr>
<tr><td>Sportbike (Civ) (Driver) (Civ casual male)</td><td>0x824548B1</td><td>No</td><td>4238</td><td>0x80009C84</td><td>0x000046F2</td></tr>
<tr><td>Sportbike (Civ) (Driver) (Civ Motorcycle male)</td><td>0xFB5D55FD</td><td>Yes</td><td>4299</td><td>0x80009CC6</td><td>0x000130D9</td></tr>
<tr><td>Sportbike (Civ) (green)</td><td>0x0821B58B</td><td>No</td><td>5595</td><td>0x8000AC4A</td><td>0x0000D200</td></tr>
<tr><td>Sportbike (Civ) (lightblue)</td><td>0xC30D7E10</td><td>No</td><td>5592</td><td>0x8000AC47</td><td>0x00012884</td></tr>
<tr><td>Sportbike (Civ) (orange)</td><td>0x80DCCB08</td><td>No</td><td>5593</td><td>0x8000AC48</td><td>0xFFFFFFFF</td></tr>
<tr><td>Sportbike (Civ) (red)</td><td>0x48B303BB</td><td>No</td><td>5591</td><td>0x8000AC46</td><td>0x000123DB</td></tr>
<tr><td>Sportbike (Civ) (white)</td><td>0x67ADC189</td><td>No</td><td>5594</td><td>0x8000AC49</td><td>0xFFFFFFFF</td></tr>
<tr><td>Sportbike_Driver</td><td>0x0DC17FF7</td><td>No</td><td>5095</td><td>0x8000A420</td><td>0x00006227</td></tr>
<tr><td>Squad</td><td>0x9788C501</td><td>No</td><td>2204</td><td>0x800081E9</td><td>0x00009CFF</td></tr>
<tr><td>SquadSpawner</td><td>0xFC55E3A3</td><td>No</td><td>3094</td><td>0x80008BB2</td><td>0x00005D97</td></tr>
<tr><td>SquadTest</td><td>0x63BEDB59</td><td>No</td><td>3093</td><td>0x80008BB1</td><td>0xFFFFFFFF</td></tr>
<tr><td>SquadTest 2</td><td>0xEE5C5203</td><td>No</td><td>3095</td><td>0x80008BB3</td><td>0x00002DCE</td></tr>
<tr><td>Stinger</td><td>0xABF77BF9</td><td>No</td><td>506</td><td>0x800056DB</td><td>0x00002564</td></tr>
<tr><td>Stingray II</td><td>0xF7E45E52</td><td>Yes</td><td>16</td><td>0x800038B2</td><td>0x0000DA8E</td></tr>
<tr><td>Stingray II (Civ driver)</td><td>0x8B638C7F</td><td>Yes</td><td>697</td><td>0x80005FB3</td><td>0x000083DF</td></tr>
<tr><td>Stingray II (Driver)</td><td>0x7FE89779</td><td>Yes</td><td>498</td><td>0x800056CF</td><td>0x00011CFE</td></tr>
<tr><td>Stingray II (Full)</td><td>0x9635391E</td><td>Yes</td><td>1611</td><td>0x80007250</td><td>0xFFFFFFFF</td></tr>
<tr><td>Stingray II (VZ driver)</td><td>0xC7BFD691</td><td>Yes</td><td>1310</td><td>0x80006E3B</td><td>0x0000BAC4</td></tr>
<tr><td>StingrayFullSpawnList</td><td>0xFB6E6930</td><td>Yes</td><td>2405</td><td>0x800083F3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Strategic Missile Projectile</td><td>0xE6B58FBE</td><td>No</td><td>3171</td><td>0x80008E46</td><td>0x00011889</td></tr>
<tr><td>Strategic Missile Projectile Launch</td><td>0x0462B13B</td><td>No</td><td>5788</td><td>0x8000AEF4</td><td>0x00008358</td></tr>
<tr><td>Strategic Missile Shrapnel</td><td>0x6CF337B8</td><td>No</td><td>3155</td><td>0x80008E35</td><td>0x00004CDB</td></tr>
<tr><td>Supply Drop (AA)</td><td>0x371641A6</td><td>No</td><td>1583</td><td>0x8000721F</td><td>0x00008B24</td></tr>
<tr><td>Supply Drop (AL Ammo)</td><td>0x9AD7F8C3</td><td>No</td><td>5757</td><td>0x8000AE07</td><td>0x0000B407</td></tr>
<tr><td>Supply Drop (AL Grenade)</td><td>0xD6EB5CBF</td><td>No</td><td>5758</td><td>0x8000AE08</td><td>0x00010063</td></tr>
<tr><td>Supply Drop (AL Health)</td><td>0x69A74BC7</td><td>No</td><td>5756</td><td>0x8000AE06</td><td>0x00001C03</td></tr>
<tr><td>Supply Drop (Allied)</td><td>0xBCE8CF73</td><td>No</td><td>815</td><td>0x80006252</td><td>0x0000424B</td></tr>
<tr><td>Supply Drop (AM AL)</td><td>0x2975CD61</td><td>No</td><td>5044</td><td>0x8000A3E1</td><td>0x00009A20</td></tr>
<tr><td>Supply Drop (AM CH)</td><td>0xF19A1E77</td><td>No</td><td>5045</td><td>0x8000A3E2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (AT AL)</td><td>0x90ED447C</td><td>No</td><td>5803</td><td>0x8000AF6B</td><td>0x0001402F</td></tr>
<tr><td>Supply Drop (AT CH)</td><td>0xB8BE94F2</td><td>No</td><td>5802</td><td>0x8000AF6A</td><td>0x0000FC01</td></tr>
<tr><td>Supply Drop (Base)</td><td>0xA0C609B1</td><td>No</td><td>5822</td><td>0x8000AF81</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (Blanco)</td><td>0x9283570F</td><td>No</td><td>5823</td><td>0x8000AF82</td><td>0x0000421E</td></tr>
<tr><td>Supply Drop (Blueprints)</td><td>0xD4ED05B4</td><td>No</td><td>5223</td><td>0x8000A68D</td><td>0x0000A20C</td></tr>
<tr><td>Supply Drop (C4)</td><td>0x92AC6643</td><td>No</td><td>1582</td><td>0x8000721E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (C4) (VZ)</td><td>0x55F3D8C0</td><td>No</td><td>2540</td><td>0x80008567</td><td>0x0000C976</td></tr>
<tr><td>Supply Drop (Chinese)</td><td>0x86D23BC9</td><td>No</td><td>1930</td><td>0x80007D92</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (Covert)</td><td>0xD2DF8435</td><td>No</td><td>4062</td><td>0x80009AE8</td><td>0x00008BDF</td></tr>
<tr><td>Supply Drop (CQB)</td><td>0x6C9225B0</td><td>No</td><td>5801</td><td>0x8000AF69</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (FIona)</td><td>0x28CF74B9</td><td>No</td><td>5824</td><td>0x8000AF83</td><td>0x00004DF9</td></tr>
<tr><td>Supply Drop (GL)</td><td>0xC2CA593F</td><td>No</td><td>4063</td><td>0x80009AE9</td><td>0x00011D05</td></tr>
<tr><td>Supply Drop (Guerilla)</td><td>0xB1A00939</td><td>No</td><td>1579</td><td>0x8000721B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (Guerilla) (Sniper)</td><td>0x508A7D49</td><td>No</td><td>2536</td><td>0x80008563</td><td>0x0000EA0D</td></tr>
<tr><td>Supply Drop (Health)</td><td>0x87B6441E</td><td>No</td><td>2531</td><td>0x8000855D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (Light MG)</td><td>0xF5FA7F08</td><td>No</td><td>1584</td><td>0x80007221</td><td>0x0000A97B</td></tr>
<tr><td>Supply Drop (Light MG) (AL)</td><td>0x558DE1B0</td><td>No</td><td>4876</td><td>0x8000A259</td><td>0x00011856</td></tr>
<tr><td>Supply Drop (OC)</td><td>0x81B20DAE</td><td>No</td><td>1580</td><td>0x8000721C</td><td>0x00012E89</td></tr>
<tr><td>Supply Drop (Pirate)</td><td>0x5EEB052D</td><td>No</td><td>814</td><td>0x80006251</td><td>0x0000B7DA</td></tr>
<tr><td>Supply Drop (RPG)</td><td>0xC22DA165</td><td>No</td><td>5806</td><td>0x8000AF6F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (Sniper CH)</td><td>0x52D9BD68</td><td>No</td><td>5799</td><td>0x8000AF67</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (Sniper RU)</td><td>0xA924BBE2</td><td>No</td><td>5800</td><td>0x8000AF68</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (Sniper)</td><td>0xFCC499E7</td><td>No</td><td>1581</td><td>0x8000721D</td><td>0x00000735</td></tr>
<tr><td>Supply Drop (Support)</td><td>0x9282B9C9</td><td>No</td><td>1585</td><td>0x80007223</td><td>0x00006B10</td></tr>
<tr><td>Supply Drop (Treasure)</td><td>0x3227E7D1</td><td>No</td><td>5222</td><td>0x8000A68C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Supply Drop (VZ)</td><td>0xCF4EC76C</td><td>No</td><td>3181</td><td>0x80008E5D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Support Vehicle (727)</td><td>0x017141B5</td><td>No</td><td>4896</td><td>0x8000A270</td><td>0x0000D1D1</td></tr>
<tr><td>Support Vehicle (727) low altitude</td><td>0xFC0FFB37</td><td>No</td><td>5282</td><td>0x8000A8AE</td><td>0x00006AEE</td></tr>
<tr><td>Support Vehicle (A10)</td><td>0xFC0C8C31</td><td>No</td><td>2424</td><td>0x8000845C</td><td>0x000140B2</td></tr>
<tr><td>Support Vehicle (A10) low altitude</td><td>0x1067B683</td><td>No</td><td>5283</td><td>0x8000A8AF</td><td>0x0000A7A7</td></tr>
<tr><td>Support Vehicle (AC130)</td><td>0x5676F5D3</td><td>Yes</td><td>2582</td><td>0x800085D9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Support Vehicle (Autogunship)</td><td>0xE76E828E</td><td>Yes</td><td>5011</td><td>0x8000A3BF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Support Vehicle (B2)</td><td>0x3B379C6F</td><td>No</td><td>2578</td><td>0x800085D5</td><td>0x0001076D</td></tr>
<tr><td>Support Vehicle (B2) low altitude</td><td>0x406CAF95</td><td>No</td><td>5284</td><td>0x8000A8B0</td><td>0x0000AB30</td></tr>
<tr><td>Support Vehicle (Base)</td><td>0xC421D9BA</td><td>No</td><td>4898</td><td>0x8000A272</td><td>0x0000F4C2</td></tr>
<tr><td>Support Vehicle (C130)</td><td>0xA4FEAE5C</td><td>Yes</td><td>2581</td><td>0x800085D8</td><td>0x0000E1A3</td></tr>
<tr><td>Support Vehicle (C130) low altitude</td><td>0xDD6E1014</td><td>Yes</td><td>5293</td><td>0x8000A8B9</td><td>0x00006714</td></tr>
<tr><td>Support Vehicle (Cessna)</td><td>0x31DDDFC8</td><td>No</td><td>4897</td><td>0x8000A271</td><td>0x00000922</td></tr>
<tr><td>Support Vehicle (Cessna) low altitude</td><td>0x3115FAD0</td><td>No</td><td>5285</td><td>0x8000A8B1</td><td>0x0000ADA2</td></tr>
<tr><td>Support Vehicle (Cruise Missile)</td><td>0x7FEE61A0</td><td>No</td><td>3173</td><td>0x80008E48</td><td>0x00006285</td></tr>
<tr><td>Support Vehicle (F117)</td><td>0x70C3E492</td><td>No</td><td>3172</td><td>0x80008E47</td><td>0x0000248B</td></tr>
<tr><td>Support Vehicle (F117) low altitude</td><td>0x2717978E</td><td>No</td><td>5286</td><td>0x8000A8B2</td><td>0x0000BE25</td></tr>
<tr><td>Support Vehicle (F35)</td><td>0xE616BA41</td><td>Yes</td><td>2428</td><td>0x80008460</td><td>0xFFFFFFFF</td></tr>
<tr><td>Support Vehicle (F35) low altitude</td><td>0x648C7473</td><td>Yes</td><td>5287</td><td>0x8000A8B3</td><td>0x0000A5AD</td></tr>
<tr><td>Support Vehicle (Mig27)</td><td>0xE74AC2EB</td><td>No</td><td>4044</td><td>0x80009AD2</td><td>0x00013341</td></tr>
<tr><td>Support Vehicle (Mig27) low altitude</td><td>0x41B5E531</td><td>No</td><td>5288</td><td>0x8000A8B4</td><td>0x000120D7</td></tr>
<tr><td>Support Vehicle (OV10)</td><td>0x55CCD133</td><td>No</td><td>4043</td><td>0x80009AD1</td><td>0x0000408C</td></tr>
<tr><td>Support Vehicle (OV10) low altitude</td><td>0x69308989</td><td>No</td><td>5289</td><td>0x8000A8B5</td><td>0x0001251A</td></tr>
<tr><td>Support Vehicle (Paradrop_AL)</td><td>0xCD6B7326</td><td>No</td><td>5008</td><td>0x8000A3BC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Support Vehicle (Paradrop_ch)</td><td>0xEC808918</td><td>No</td><td>5006</td><td>0x8000A3BA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Support Vehicle (Predator)</td><td>0xB81F9838</td><td>No</td><td>4787</td><td>0x8000A190</td><td>0x00009F08</td></tr>
<tr><td>Support Vehicle (Predator) low altitude</td><td>0x5BCCABA0</td><td>No</td><td>5290</td><td>0x8000A8B6</td><td>0x00002AC2</td></tr>
<tr><td>Support Vehicle (Q5)</td><td>0xD78EE851</td><td>No</td><td>2580</td><td>0x800085D7</td><td>0x00004406</td></tr>
<tr><td>Support Vehicle (Q5) low altitude</td><td>0xBE7DE823</td><td>No</td><td>5291</td><td>0x8000A8B7</td><td>0x00013EF8</td></tr>
<tr><td>Support Vehicle (Transport)</td><td>0x6BF9A5EA</td><td>No</td><td>2609</td><td>0x800085F8</td><td>0x0000BC5C</td></tr>
<tr><td>Support Vehicle (Tucano)</td><td>0x03501723</td><td>No</td><td>2579</td><td>0x800085D6</td><td>0x0000355F</td></tr>
<tr><td>Support Vehicle (Tucano) low altitude</td><td>0x89AB7899</td><td>No</td><td>5292</td><td>0x8000A8B8</td><td>0xFFFFFFFF</td></tr>
<tr><td>Surgical Strike Projectile</td><td>0xDB16CC58</td><td>No</td><td>1909</td><td>0x800078CA</td><td>0x0000CF26</td></tr>
<tr><td>Surgical Strike Shrapnel</td><td>0xF791712E</td><td>No</td><td>1910</td><td>0x800078CC</td><td>0xFFFFFFFF</td></tr>
<tr><td>SX2150 (Base)</td><td>0x75BC4C18</td><td>No</td><td>3478</td><td>0x800092D5</td><td>0x00009032</td></tr>
<tr><td>SX2150 (Cargo)</td><td>0xCA6EEAB9</td><td>No</td><td>3481</td><td>0x800092D8</td><td>0xFFFFFFFF</td></tr>
<tr><td>SX2150 (Cargo) (Driver)</td><td>0x71E26394</td><td>No</td><td>3515</td><td>0x8000932F</td><td>0x00009D05</td></tr>
<tr><td>SX2150 (Cargo) (Full)</td><td>0x24FE6B53</td><td>No</td><td>3519</td><td>0x80009333</td><td>0xFFFFFFFF</td></tr>
<tr><td>SX2150 (Fuel)</td><td>0x4778F921</td><td>No</td><td>3484</td><td>0x800092DB</td><td>0x000019C6</td></tr>
<tr><td>SX2150 (Fuel) (Driver)</td><td>0x2AB6483C</td><td>No</td><td>3516</td><td>0x80009330</td><td>0x0000670E</td></tr>
<tr><td>SX2150 (Fuel) (Full)</td><td>0x07BA4D2B</td><td>No</td><td>3520</td><td>0x80009334</td><td>0x0000C5F9</td></tr>
<tr><td>SX2150 (MLRS)</td><td>0xFBDC7E43</td><td>No</td><td>3483</td><td>0x800092DA</td><td>0xFFFFFFFF</td></tr>
<tr><td>SX2150 (MLRS) (Driver)</td><td>0xADD73D9E</td><td>No</td><td>3517</td><td>0x80009331</td><td>0x000036A6</td></tr>
<tr><td>SX2150 (MLRS) (Full)</td><td>0x648129E5</td><td>No</td><td>3521</td><td>0x80009335</td><td>0x0001366B</td></tr>
<tr><td>SX2150 (Semi)</td><td>0x71470A0F</td><td>No</td><td>3482</td><td>0x800092D9</td><td>0xFFFFFFFF</td></tr>
<tr><td>SX2150 (Semi) (Driver)</td><td>0xD92DEBBA</td><td>No</td><td>3518</td><td>0x80009332</td><td>0x00003CD0</td></tr>
<tr><td>SX2150 (Semi) (Full)</td><td>0xAE08EBF9</td><td>No</td><td>3522</td><td>0x80009336</td><td>0x0000499F</td></tr>
<tr><td>SX2150_Driver</td><td>0xE489AB3D</td><td>No</td><td>5074</td><td>0x8000A408</td><td>0x00006F9E</td></tr>
<tr><td>T300 (base)</td><td>0x273374D2</td><td>No</td><td>3476</td><td>0x800092D2</td><td>0x00010144</td></tr>
<tr><td>T300 (Driver)</td><td>0x239E95E5</td><td>No</td><td>3490</td><td>0x800092E2</td><td>0x0000607A</td></tr>
<tr><td>T300 (empty)</td><td>0x8F3EC4FE</td><td>No</td><td>2559</td><td>0x800085BE</td><td>0xFFFFFFFF</td></tr>
<tr><td>T300 (Full)</td><td>0x8270C192</td><td>No</td><td>3491</td><td>0x800092E3</td><td>0x00004F7B</td></tr>
<tr><td>T300 (M60)</td><td>0x9A974376</td><td>No</td><td>3477</td><td>0x800092D3</td><td>0x0000004A</td></tr>
<tr><td>T300 (M60) (Driver)</td><td>0xD05B27CD</td><td>No</td><td>3492</td><td>0x800092E4</td><td>0xFFFFFFFF</td></tr>
<tr><td>T300 (M60) (DriverGunner)</td><td>0x19C77906</td><td>No</td><td>3493</td><td>0x80009319</td><td>0x00007706</td></tr>
<tr><td>T300 (M60) (Full)</td><td>0xD68EDD6A</td><td>No</td><td>3494</td><td>0x8000931A</td><td>0x000092BB</td></tr>
<tr><td>Tank</td><td>0xC686AE99</td><td>Yes</td><td>831</td><td>0x8000638A</td><td>0x00004EBA</td></tr>
<tr><td>Tank Bike</td><td>0x0ADFFAD4</td><td>Yes</td><td>2585</td><td>0x800085DE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Tank Commander</td><td>0x413AB10F</td><td>Yes</td><td>2294</td><td>0x800082B8</td><td>0x000128A9</td></tr>
<tr><td>Tank Seat (Driver) (Civ)</td><td>0xBF349994</td><td>Yes</td><td>696</td><td>0x80005FB2</td><td>0x00006CD5</td></tr>
<tr><td>Tank Seat (Driver) (VZ)</td><td>0x0A5CB4A4</td><td>Yes</td><td>497</td><td>0x800056CE</td><td>0x0000F7B6</td></tr>
<tr><td>Tank Seat (Gunner) (VZ)</td><td>0xF2E099CF</td><td>Yes</td><td>1205</td><td>0x80006CBD</td><td>0xFFFFFFFF</td></tr>
<tr><td>Tank Shell (Artillery)</td><td>0x724BBEC8</td><td>Yes</td><td>4132</td><td>0x80009B30</td><td>0xFFFFFFFF</td></tr>
<tr><td>Tank Shell (Default)</td><td>0xAB81CFDB</td><td>Yes</td><td>455</td><td>0x80005696</td><td>0x00008704</td></tr>
<tr><td>Tank Shell (Sabot)</td><td>0x5FB2FB87</td><td>Yes</td><td>4131</td><td>0x80009B2F</td><td>0x0000AC98</td></tr>
<tr><td>Tank Shell (Weak)</td><td>0x3AC5E254</td><td>Yes</td><td>4130</td><td>0x80009B2E</td><td>0x00006F18</td></tr>
<tr><td>TankBike_Driver</td><td>0xF04D95EB</td><td>Yes</td><td>5384</td><td>0x8000A978</td><td>0x00013294</td></tr>
<tr><td>Taxi (Tercel)</td><td>0x3D094D4F</td><td>No</td><td>3639</td><td>0x80009473</td><td>0x0000625F</td></tr>
<tr><td>Taxi (Tercel) (Driver)</td><td>0xC92AD97A</td><td>No</td><td>4462</td><td>0x80009E28</td><td>0x0000F344</td></tr>
<tr><td>Taxi (Tercel) (Driver) (Civ Taxi Driver male)</td><td>0x7808D20E</td><td>No</td><td>4463</td><td>0x80009E29</td><td>0x000105BB</td></tr>
<tr><td>TCTest1</td><td>0x201CAADF</td><td>No</td><td>530</td><td>0x80005B88</td><td>0x00001398</td></tr>
<tr><td>TCTest2</td><td>0x961FA338</td><td>No</td><td>531</td><td>0x80005B89</td><td>0x0000F0D3</td></tr>
<tr><td>Telephone Pole Test</td><td>0x56607881</td><td>No</td><td>380</td><td>0x800051C0</td><td>0x0000B9B4</td></tr>
<tr><td>telephone wire</td><td>0xE631DF46</td><td>No</td><td>1040</td><td>0x80006919</td><td>0xFFFFFFFF</td></tr>
<tr><td>telephones</td><td>0xA4D5C112</td><td>No</td><td>112</td><td>0x80004C1D</td><td>0x0000B799</td></tr>
<tr><td>Teleporter</td><td>0x60A7C059</td><td>No</td><td>549</td><td>0x80005B9F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Tercel_Driver</td><td>0xB97625FF</td><td>No</td><td>5127</td><td>0x8000A46B</td><td>0x0000664C</td></tr>
<tr><td>terrain</td><td>0x19FC10AC</td><td>No</td><td>2</td><td>0x8000232D</td><td>0x00002294</td></tr>
<tr><td>Terrain_128</td><td>0x0729ED62</td><td>No</td><td>343</td><td>0x80004E8F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Terrain_512</td><td>0xF3D1E031</td><td>No</td><td>642</td><td>0x80005C4A</td><td>0x00005B44</td></tr>
<tr><td>Test Explosion Large</td><td>0xEAC413B5</td><td>No</td><td>1801</td><td>0x80007634</td><td>0x00008519</td></tr>
<tr><td>Test Explosion Medium</td><td>0xCC1BDA91</td><td>No</td><td>3138</td><td>0x80008CFA</td><td>0x00005496</td></tr>
<tr><td>TestBossBattle</td><td>0xF1D8C824</td><td>No</td><td>2909</td><td>0x80008940</td><td>0x00004986</td></tr>
<tr><td>testdust</td><td>0x9623D53D</td><td>No</td><td>1802</td><td>0x80007635</td><td>0x0000DE2E</td></tr>
<tr><td>testPris</td><td>0xEF2CD5E3</td><td>No</td><td>3069</td><td>0x80008B98</td><td>0x00011D99</td></tr>
<tr><td>testPris2</td><td>0x4C8103B3</td><td>No</td><td>3070</td><td>0x80008B99</td><td>0x00009B7F</td></tr>
<tr><td>testPris3</td><td>0xEA7E2AD6</td><td>No</td><td>3071</td><td>0x80008B9A</td><td>0x00012F15</td></tr>
<tr><td>testPris4</td><td>0xF48F83B5</td><td>No</td><td>3072</td><td>0x80008B9B</td><td>0xFFFFFFFF</td></tr>
<tr><td>TestSingleSpawn</td><td>0x535D2B8A</td><td>No</td><td>546</td><td>0x80005B9B</td><td>0xFFFFFFFF</td></tr>
<tr><td>TestSkirmish</td><td>0xE7A37705</td><td>No</td><td>3087</td><td>0x80008BAB</td><td>0x0000E3ED</td></tr>
<tr><td>TestSpawn1</td><td>0x858B4C93</td><td>No</td><td>38</td><td>0x8000450A</td><td>0x000117E5</td></tr>
<tr><td>TestSpawn2</td><td>0xAB8DC6FC</td><td>No</td><td>42</td><td>0x8000450E</td><td>0x00005B88</td></tr>
<tr><td>TestTree</td><td>0xD5A65B0D</td><td>No</td><td>636</td><td>0x80005C42</td><td>0x000064C2</td></tr>
<tr><td>ThirstyFountain</td><td>0xD9EC1F0A</td><td>No</td><td>104</td><td>0x80004C11</td><td>0x00013DDB</td></tr>
<tr><td>Thunder</td><td>0x5404A661</td><td>No</td><td>1679</td><td>0x800074A8</td><td>0x0000F6D8</td></tr>
<tr><td>Thunder (black)</td><td>0xB32B3EC3</td><td>No</td><td>5603</td><td>0x8000AC52</td><td>0x0000B1F5</td></tr>
<tr><td>Thunder (blue)</td><td>0xB2373196</td><td>No</td><td>5606</td><td>0x8000AC55</td><td>0x00004E46</td></tr>
<tr><td>Thunder (Driver)</td><td>0x41BC9AFC</td><td>No</td><td>1680</td><td>0x800074A9</td><td>0x00005E0C</td></tr>
<tr><td>Thunder (Driver) (Civ Business B Male)</td><td>0x0B421BB2</td><td>No</td><td>4218</td><td>0x80009C70</td><td>0x0000673A</td></tr>
<tr><td>Thunder (Driver) (Civ Business Female)</td><td>0x4112D58D</td><td>No</td><td>4219</td><td>0x80009C71</td><td>0x000095E5</td></tr>
<tr><td>Thunder (Driver) (Civ Business Male)</td><td>0xBAA9A0A0</td><td>No</td><td>4217</td><td>0x80009C6F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Thunder (Driver) (Civ Poor female)</td><td>0x7FB36213</td><td>No</td><td>4289</td><td>0x80009CBC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Thunder (Driver) (Civ Poor Male)</td><td>0x39F4B542</td><td>No</td><td>4288</td><td>0x80009CBB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Thunder (Driver) (Civ Rich Female)</td><td>0xEBF64761</td><td>No</td><td>4221</td><td>0x80009C73</td><td>0x0000568D</td></tr>
<tr><td>Thunder (Driver) (Civ Rich Male)</td><td>0x0F9A0C04</td><td>No</td><td>4220</td><td>0x80009C72</td><td>0xFFFFFFFF</td></tr>
<tr><td>Thunder (green)</td><td>0xB2F606A3</td><td>No</td><td>5607</td><td>0x8000AC56</td><td>0x0000D088</td></tr>
<tr><td>Thunder (lightblue)</td><td>0x7ED17AF8</td><td>No</td><td>5609</td><td>0x8000AC58</td><td>0xFFFFFFFF</td></tr>
<tr><td>Thunder (orange)</td><td>0x29654040</td><td>No</td><td>5608</td><td>0x8000AC57</td><td>0x0000F611</td></tr>
<tr><td>Thunder (red)</td><td>0x17EDC823</td><td>No</td><td>5604</td><td>0x8000AC53</td><td>0xFFFFFFFF</td></tr>
<tr><td>Thunder (white)</td><td>0x23FCA7D1</td><td>No</td><td>5605</td><td>0x8000AC54</td><td>0xFFFFFFFF</td></tr>
<tr><td>Thunder_Driver</td><td>0x56146B5A</td><td>No</td><td>5059</td><td>0x8000A3F8</td><td>0x0000D3BB</td></tr>
<tr><td>Tiny Geometry Component Master</td><td>0x3A5B45C2</td><td>No</td><td>4750</td><td>0x8000A168</td><td>0x0000806E</td></tr>
<tr><td>TinyFlame</td><td>0x4FD293F4</td><td>No</td><td>1102</td><td>0x80006A87</td><td>0x0001409C</td></tr>
<tr><td>TinyGeometry</td><td>0xA5D1E0AB</td><td>No</td><td>1917</td><td>0x80007B94</td><td>0xFFFFFFFF</td></tr>
<tr><td>TinyGeometryHowto</td><td>0x0F613E38</td><td>No</td><td>5528</td><td>0x8000AADA</td><td>0xFFFFFFFF</td></tr>
<tr><td>TinyGeometryVZ</td><td>0xD1B92D9F</td><td>No</td><td>1754</td><td>0x800075C3</td><td>0x00012115</td></tr>
<tr><td>TinyGeometryVZ_064</td><td>0x811764F8</td><td>No</td><td>4968</td><td>0x8000A38F</td><td>0xFFFFFFFF</td></tr>
<tr><td>TinyGeometryVZ_128</td><td>0x5853A8E1</td><td>No</td><td>4967</td><td>0x8000A38E</td><td>0xFFFFFFFF</td></tr>
<tr><td>TinyGeometryVZ_2048</td><td>0x18EA2F8C</td><td>No</td><td>2837</td><td>0x80008792</td><td>0x0000CC53</td></tr>
<tr><td>TinyGeometryVZ_256</td><td>0xF10D0A65</td><td>No</td><td>4966</td><td>0x8000A38D</td><td>0x00010307</td></tr>
<tr><td>TinyGeometryVZ_512</td><td>0x0C21C446</td><td>No</td><td>4965</td><td>0x8000A38C</td><td>0x000034E0</td></tr>
<tr><td>TiredBench</td><td>0x461B2F79</td><td>No</td><td>105</td><td>0x80004C12</td><td>0x00013EBD</td></tr>
<tr><td>TiredBenchSpawner</td><td>0x4DC7CB7B</td><td>No</td><td>1936</td><td>0x80007DFF</td><td>0xFFFFFFFF</td></tr>
<tr><td>TiredBenchSpawner (Crying)</td><td>0x065DF86C</td><td>No</td><td>1939</td><td>0x80007E03</td><td>0x000103C9</td></tr>
<tr><td>TOW Missile</td><td>0xE744DC15</td><td>No</td><td>1135</td><td>0x80006B5E</td><td>0x0000003E</td></tr>
<tr><td>TOW Missile (Hellfire)</td><td>0x415A7711</td><td>No</td><td>5508</td><td>0x8000AAC3</td><td>0x000028C0</td></tr>
<tr><td>TowerDestructTemplate</td><td>0xF25CC7D0</td><td>No</td><td>2771</td><td>0x80008749</td><td>0xFFFFFFFF</td></tr>
<tr><td>Traffic Gur HQ List</td><td>0x976BBEE1</td><td>No</td><td>2517</td><td>0x8000854E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Traffic Zones</td><td>0x13EEFF25</td><td>No</td><td>344</td><td>0x80004E90</td><td>0xFFFFFFFF</td></tr>
<tr><td>TrafficLight_2</td><td>0xD2CEA177</td><td>No</td><td>532</td><td>0x80005B8A</td><td>0x000066DB</td></tr>
<tr><td>TrafficLight__</td><td>0x694D0AAE</td><td>No</td><td>534</td><td>0x80005B8D</td><td>0x000128B8</td></tr>
<tr><td>Trailer</td><td>0x8D3354FE</td><td>No</td><td>1814</td><td>0x800076A5</td><td>0x00001CF0</td></tr>
<tr><td>Trailer_Driver</td><td>0x8F5AF747</td><td>No</td><td>5116</td><td>0x8000A45A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Transport Truck</td><td>0x190F4FD9</td><td>Yes</td><td>716</td><td>0x800060B7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Transport Truck (Driver)</td><td>0x926CE734</td><td>Yes</td><td>1591</td><td>0x8000723B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Transport Truck (Driver) (Mechanic male)</td><td>0x3847E5AE</td><td>Yes</td><td>4427</td><td>0x80009E05</td><td>0x0000D17D</td></tr>
<tr><td>Transport Truck_Ruined</td><td>0x73CCD9ED</td><td>Yes</td><td>5214</td><td>0x8000A681</td><td>0xFFFFFFFF</td></tr>
<tr><td>Transport_Ruin</td><td>0x459EA631</td><td>No</td><td>1086</td><td>0x80006A32</td><td>0x00004B04</td></tr>
<tr><td>Transport_Ruin_Fire</td><td>0x063B655C</td><td>No</td><td>2024</td><td>0x800080C7</td><td>0xFFFFFFFF</td></tr>
<tr><td>TransportTruck_Driver</td><td>0x20A97A76</td><td>Yes</td><td>5068</td><td>0x8000A401</td><td>0x0000E07B</td></tr>
<tr><td>trash01</td><td>0x33859570</td><td>No</td><td>3259</td><td>0x80008F39</td><td>0x00009213</td></tr>
<tr><td>Tree_Scrub</td><td>0x170A44B5</td><td>No</td><td>2043</td><td>0x800080DB</td><td>0x00009B26</td></tr>
<tr><td>TreeTrunkDebrisTemplate</td><td>0x5280B8DA</td><td>No</td><td>3696</td><td>0x8000954D</td><td>0xFFFFFFFF</td></tr>
<tr><td>TriggerTimer AllCon002 Pipes</td><td>0xB50876EA</td><td>No</td><td>2676</td><td>0x8000867E</td><td>0x00002EB6</td></tr>
<tr><td>TriggerTimer AllCon002 Pipes Effect</td><td>0x7921548D</td><td>No</td><td>3393</td><td>0x8000910D</td><td>0x0000FE74</td></tr>
<tr><td>TrooperPooper</td><td>0x1A037D7D</td><td>No</td><td>1905</td><td>0x80007807</td><td>0x0001049B</td></tr>
<tr><td>Turbosquid</td><td>0x072C3307</td><td>No</td><td>713</td><td>0x800060AF</td><td>0x0000F526</td></tr>
<tr><td>Turbosquid (CIV)</td><td>0x5C820F44</td><td>No</td><td>1595</td><td>0x80007240</td><td>0xFFFFFFFF</td></tr>
<tr><td>Turbosquid (CIV) (Driver)</td><td>0x26AF3A23</td><td>No</td><td>4662</td><td>0x80009FD8</td><td>0x00011093</td></tr>
<tr><td>Turbosquid (CIV) (Driver) (Civ Poor female)</td><td>0xE6C337D8</td><td>No</td><td>4664</td><td>0x80009FDA</td><td>0x000121DB</td></tr>
<tr><td>Turbosquid (CIV) (Driver) (Civ Poor male)</td><td>0x24098509</td><td>No</td><td>4663</td><td>0x80009FD9</td><td>0x00009DC4</td></tr>
<tr><td>Turbosquid (CIV) (Driver) DEPRECATED</td><td>0xAF9255AE</td><td>No</td><td>1598</td><td>0x80007243</td><td>0x0000593B</td></tr>
<tr><td>Turbosquid (GR)</td><td>0x25588685</td><td>No</td><td>1596</td><td>0x80007241</td><td>0x0000F301</td></tr>
<tr><td>Turbosquid (GR) (Driver)</td><td>0x60D20390</td><td>No</td><td>1599</td><td>0x80007244</td><td>0x0000B90D</td></tr>
<tr><td>Turbosquid (GR) (DriverGunner)</td><td>0xB868CBCF</td><td>No</td><td>5627</td><td>0x8000AC7C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Turbosquid (GR) (Full)</td><td>0x0764DF27</td><td>No</td><td>5148</td><td>0x8000A486</td><td>0xFFFFFFFF</td></tr>
<tr><td>Turbosquid (OC)</td><td>0xAB3108D6</td><td>No</td><td>1597</td><td>0x80007242</td><td>0x000036F6</td></tr>
<tr><td>Turbosquid (OC) (Driver)</td><td>0xCDE44AAD</td><td>No</td><td>1600</td><td>0x80007245</td><td>0x0000FA4C</td></tr>
<tr><td>Turbosquid (OC) (Full)</td><td>0x41E6A84A</td><td>No</td><td>3840</td><td>0x800097F8</td><td>0x00010E4B</td></tr>
<tr><td>Type 14310</td><td>0xB68095D8</td><td>No</td><td>2218</td><td>0x800081F7</td><td>0x00013CBA</td></tr>
<tr><td>Type 14310 (Driver)</td><td>0x29610037</td><td>No</td><td>2252</td><td>0x80008226</td><td>0x00002A4C</td></tr>
<tr><td>Type 14310 (Full)</td><td>0xF594057C</td><td>No</td><td>3688</td><td>0x80009537</td><td>0x0000F213</td></tr>
<tr><td>Type 14310 (Non AA)</td><td>0x611DF226</td><td>No</td><td>5204</td><td>0x8000A5EC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Type 14310 (Non AA) (Driver)</td><td>0x2D4BC03D</td><td>No</td><td>5205</td><td>0x8000A5ED</td><td>0x00013549</td></tr>
<tr><td>Type 14310 (Non AA) (Full)</td><td>0xE646A49A</td><td>No</td><td>5206</td><td>0x8000A5EE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Type14310_Driver</td><td>0xCD6B097F</td><td>No</td><td>5099</td><td>0x8000A424</td><td>0xFFFFFFFF</td></tr>
<tr><td>U1 Transport (PMC) (AL Insertion)</td><td>0x2FB13A66</td><td>No</td><td>2439</td><td>0x8000846E</td><td>0x000029E9</td></tr>
<tr><td>U1 Transport (PMC) (CH Insertion)</td><td>0xEF50F86C</td><td>No</td><td>2441</td><td>0x80008470</td><td>0x00006736</td></tr>
<tr><td>U1 Transport (PMC) (GR Insertion)</td><td>0x964AB6EA</td><td>No</td><td>2437</td><td>0x8000846C</td><td>0x0000D3C1</td></tr>
<tr><td>U1 Transport (PMC) (OC Insertion)</td><td>0x3A0624A1</td><td>No</td><td>2438</td><td>0x8000846D</td><td>0xFFFFFFFF</td></tr>
<tr><td>U1 Transport (PMC) (PR Insertion)</td><td>0xA71C3C19</td><td>No</td><td>2440</td><td>0x8000846F</td><td>0xFFFFFFFF</td></tr>
<tr><td>UH1</td><td>0x218895A3</td><td>Yes</td><td>853</td><td>0x800063A5</td><td>0xFFFFFFFF</td></tr>
<tr><td>UH1 Attack</td><td>0xEE6C2DE9</td><td>Yes</td><td>2173</td><td>0x800081C8</td><td>0x00011948</td></tr>
<tr><td>UH1 Attack (PMC)</td><td>0x89FBE62C</td><td>Yes</td><td>2242</td><td>0x80008217</td><td>0x0000E70C</td></tr>
<tr><td>UH1 Attack (PMC) (Driver)</td><td>0x9FECF32B</td><td>Yes</td><td>2247</td><td>0x8000821D</td><td>0xFFFFFFFF</td></tr>
<tr><td>UH1 Attack (PMC) (Driver) (Railshooter)</td><td>0x548C503E</td><td>Yes</td><td>4935</td><td>0x8000A29D</td><td>0x00011497</td></tr>
<tr><td>UH1 Attack (PMC) HelCon</td><td>0xE8ED7D25</td><td>Yes</td><td>2682</td><td>0x80008684</td><td>0x00001FDF</td></tr>
<tr><td>UH1 Elite</td><td>0xA9674B56</td><td>Yes</td><td>2176</td><td>0x800081CB</td><td>0x0000A1A6</td></tr>
<tr><td>UH1 Superiority</td><td>0x4015A778</td><td>Yes</td><td>2174</td><td>0x800081C9</td><td>0x0000758C</td></tr>
<tr><td>UH1 Transport</td><td>0xCA1D5C24</td><td>Yes</td><td>855</td><td>0x800063A8</td><td>0xFFFFFFFF</td></tr>
<tr><td>UH1 Transport (GR)</td><td>0x7EECCD94</td><td>Yes</td><td>2232</td><td>0x80008205</td><td>0x0000959B</td></tr>
<tr><td>UH1 Transport (GR) (Delivery)</td><td>0xAEF1F11D</td><td>Yes</td><td>1931</td><td>0x80007D93</td><td>0x00004135</td></tr>
<tr><td>UH1 Transport (GR) (Driver)</td><td>0x05B41E73</td><td>Yes</td><td>2234</td><td>0x80008207</td><td>0xFFFFFFFF</td></tr>
<tr><td>UH1 Transport (GR) (Ewan)</td><td>0x0CF7687A</td><td>Yes</td><td>5990</td><td>0x8000B372</td><td>0xFFFFFFFF</td></tr>
<tr><td>UH1 Transport (GR) (Extraction)</td><td>0x76D9AD80</td><td>Yes</td><td>5833</td><td>0x8000AF8E</td><td>0x0001091D</td></tr>
<tr><td>UH1 Transport (GR) (Full)</td><td>0x1BAAE2A0</td><td>Yes</td><td>2494</td><td>0x80008529</td><td>0x00009C05</td></tr>
<tr><td>UH1 Transport (GR) (Full) (RPG)</td><td>0xDBFA90EA</td><td>Yes</td><td>5577</td><td>0x8000AB75</td><td>0x0000619E</td></tr>
<tr><td>UH1 Transport (PMC)</td><td>0x79415FA1</td><td>Yes</td><td>2233</td><td>0x80008206</td><td>0xFFFFFFFF</td></tr>
<tr><td>UH1 Transport (PMC) (Driver)</td><td>0x0CCF93BC</td><td>Yes</td><td>2235</td><td>0x80008208</td><td>0x00002F0A</td></tr>
<tr><td>UH1 Transport (PMC) (Extraction)</td><td>0x1CB07287</td><td>Yes</td><td>2683</td><td>0x80008686</td><td>0x000114B5</td></tr>
<tr><td>UH1 Transport (PMC) (Ghost)</td><td>0xECB8938F</td><td>Yes</td><td>4902</td><td>0x8000A276</td><td>0x000018A9</td></tr>
<tr><td>UH1 Transport (Pursuit)</td><td>0x81C04A3B</td><td>Yes</td><td>4909</td><td>0x8000A280</td><td>0x00011B05</td></tr>
<tr><td>UH1 Transport (Transit)</td><td>0xAC41D6F2</td><td>Yes</td><td>5807</td><td>0x8000AF70</td><td>0xFFFFFFFF</td></tr>
<tr><td>UnitList1</td><td>0xEFBB2A10</td><td>No</td><td>40</td><td>0x8000450C</td><td>0x0000AAA7</td></tr>
<tr><td>UnlockableAbel</td><td>0x2D666C6B</td><td>No</td><td>2352</td><td>0x800082F9</td><td>0x00006F13</td></tr>
<tr><td>UnlockableBlanco</td><td>0x82AEA2E8</td><td>No</td><td>2349</td><td>0x800082F6</td><td>0xFFFFFFFF</td></tr>
<tr><td>UnlockableCarlos</td><td>0x8F185DB1</td><td>No</td><td>2353</td><td>0x800082FA</td><td>0x000030AC</td></tr>
<tr><td>UnlockableDiablo</td><td>0x26E87C5A</td><td>No</td><td>2342</td><td>0x800082EE</td><td>0x00007FAF</td></tr>
<tr><td>UnlockableEva</td><td>0xB5471149</td><td>No</td><td>2310</td><td>0x800082C8</td><td>0x0000ACC4</td></tr>
<tr><td>UnlockableEwan</td><td>0x47966194</td><td>No</td><td>2307</td><td>0x800082C5</td><td>0x0000139E</td></tr>
<tr><td>UnlockableFiona</td><td>0x84E26766</td><td>No</td><td>2357</td><td>0x800082FE</td><td>0xFFFFFFFF</td></tr>
<tr><td>UnlockableFire</td><td>0x9E408529</td><td>No</td><td>2348</td><td>0x800082F5</td><td>0xFFFFFFFF</td></tr>
<tr><td>UnlockableGauge</td><td>0x6CD8F24E</td><td>No</td><td>2347</td><td>0x800082F4</td><td>0xFFFFFFFF</td></tr>
<tr><td>UnlockableGhost</td><td>0x025545AE</td><td>No</td><td>2344</td><td>0x800082F0</td><td>0x000102D2</td></tr>
<tr><td>UnlockableHoang</td><td>0xC0D17EC6</td><td>No</td><td>2350</td><td>0x800082F7</td><td>0xFFFFFFFF</td></tr>
<tr><td>UnlockableMisha</td><td>0xB74302B3</td><td>No</td><td>2309</td><td>0x800082C7</td><td>0x00009BDC</td></tr>
<tr><td>UnlockableVasquez</td><td>0x8EE21A12</td><td>No</td><td>2351</td><td>0x800082F8</td><td>0xFFFFFFFF</td></tr>
<tr><td>UnlockableWingman</td><td>0xA944E334</td><td>No</td><td>2354</td><td>0x800082FB</td><td>0x00003A0B</td></tr>
<tr><td>UrbanCarList</td><td>0xD8C4E86B</td><td>No</td><td>88</td><td>0x80004B91</td><td>0xFFFFFFFF</td></tr>
<tr><td>V22 (Delivery)</td><td>0xA4F6D8C6</td><td>No</td><td>889</td><td>0x800063DF</td><td>0x0000EEBB</td></tr>
<tr><td>V22 (Driver)</td><td>0x65E28854</td><td>No</td><td>1783</td><td>0x800075E9</td><td>0x0000C509</td></tr>
<tr><td>V22 - DO NOT USE</td><td>0x18EBA05D</td><td>No</td><td>76</td><td>0x80004A60</td><td>0x000048DA</td></tr>
<tr><td>Valiant</td><td>0x540A0D66</td><td>No</td><td>357</td><td>0x80004F44</td><td>0x0000A626</td></tr>
<tr><td>Valiant (4door)</td><td>0x92CDA237</td><td>No</td><td>2563</td><td>0x800085C3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Valiant (4door) (Driver)</td><td>0x89EFADE2</td><td>No</td><td>4237</td><td>0x80009C83</td><td>0x00000BF3</td></tr>
<tr><td>Valiant (4door) (Driver) (Civ Business B male)</td><td>0xC78FAA18</td><td>No</td><td>4428</td><td>0x80009E06</td><td>0x000060AF</td></tr>
<tr><td>Valiant (base)</td><td>0x23E1281A</td><td>No</td><td>63</td><td>0x80004742</td><td>0x0000F0F2</td></tr>
<tr><td>Valiant (crappy)</td><td>0x1E22A2D4</td><td>No</td><td>2566</td><td>0x800085C9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Valiant (crappy) (Driver)</td><td>0x4530C533</td><td>No</td><td>4429</td><td>0x80009E07</td><td>0xFFFFFFFF</td></tr>
<tr><td>Valiant (crappy) (Driver) (Civ Poor female)</td><td>0xD0A49A88</td><td>No</td><td>4431</td><td>0x80009E09</td><td>0xFFFFFFFF</td></tr>
<tr><td>Valiant (crappy) (Driver) (Civ Poor male)</td><td>0xF47F02F9</td><td>No</td><td>4430</td><td>0x80009E08</td><td>0xFFFFFFFF</td></tr>
<tr><td>Valiant (Driver)</td><td>0x6C5D91FD</td><td>No</td><td>64</td><td>0x80004743</td><td>0x000115A6</td></tr>
<tr><td>Valiant (Driver) (Civ Business B male)</td><td>0x7D56DF57</td><td>No</td><td>4432</td><td>0x80009E0A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Valiant (Driver) (Civ casual female)</td><td>0x3A038FA5</td><td>No</td><td>4234</td><td>0x80009C80</td><td>0xFFFFFFFF</td></tr>
<tr><td>Valiant (Driver) (Civ casual male)</td><td>0x38F88238</td><td>No</td><td>4233</td><td>0x80009C7F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Valiant (Driver) (Civ poor female)</td><td>0x6F9DCC92</td><td>No</td><td>4236</td><td>0x80009C82</td><td>0x00000D72</td></tr>
<tr><td>Valiant (Driver) (Civ poor male)</td><td>0xD8A843B7</td><td>No</td><td>4235</td><td>0x80009C81</td><td>0xFFFFFFFF</td></tr>
<tr><td>Valiant (Python)</td><td>0xCF4FA909</td><td>No</td><td>4019</td><td>0x800099AA</td><td>0x00003B25</td></tr>
<tr><td>Valiant (Python) (Mechanic male)</td><td>0xEE96CC27</td><td>No</td><td>5147</td><td>0x8000A485</td><td>0x0000B116</td></tr>
<tr><td>Valiant_Driver</td><td>0xBEC37ADF</td><td>No</td><td>5072</td><td>0x8000A405</td><td>0x00012095</td></tr>
<tr><td>ValiantCrappy_Driver</td><td>0xE0580DA0</td><td>No</td><td>5139</td><td>0x8000A47B</td><td>0xFFFFFFFF</td></tr>
<tr><td>ValiantPython_Driver</td><td>0xCB03BAA5</td><td>No</td><td>5145</td><td>0x8000A482</td><td>0xFFFFFFFF</td></tr>
<tr><td>Van (base)</td><td>0x07A72F20</td><td>No</td><td>1674</td><td>0x800074A3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Van (Commercial)</td><td>0x1410F16F</td><td>No</td><td>3640</td><td>0x80009474</td><td>0x00010716</td></tr>
<tr><td>Van (Commercial) (Driver)</td><td>0x0C41679A</td><td>No</td><td>3642</td><td>0x80009476</td><td>0x0001385D</td></tr>
<tr><td>Van (Commercial) (Driver) (Civ Casual female)</td><td>0x12368D32</td><td>No</td><td>4227</td><td>0x80009C79</td><td>0xFFFFFFFF</td></tr>
<tr><td>Van (Commercial) (Driver) (Civ Casual male)</td><td>0x0A2B92D7</td><td>No</td><td>4226</td><td>0x80009C78</td><td>0x00010587</td></tr>
<tr><td>Van (Commercial) (Driver) (Civ Industrial female)</td><td>0x1F02BD0C</td><td>No</td><td>4433</td><td>0x80009E0B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Van (Commercial) (Driver) (Civ Industrial male)</td><td>0xE34E881D</td><td>No</td><td>4434</td><td>0x80009E0C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Van (Crappy)</td><td>0x1405526A</td><td>No</td><td>1675</td><td>0x800074A4</td><td>0x00004D6F</td></tr>
<tr><td>Van (Crappy) (Driver)</td><td>0x6686F151</td><td>No</td><td>1676</td><td>0x800074A5</td><td>0x00004EDA</td></tr>
<tr><td>Van (Crappy) (Driver) (Civ Poor female)</td><td>0xC4CDF206</td><td>No</td><td>4436</td><td>0x80009E0E</td><td>0x000053E6</td></tr>
<tr><td>Van (Crappy) (Driver) (Civ Poor male)</td><td>0xAB04BE3B</td><td>No</td><td>4435</td><td>0x80009E0D</td><td>0x00009A7B</td></tr>
<tr><td>Van (Green)</td><td>0x4CD82092</td><td>No</td><td>646</td><td>0x80005C5A</td><td>0x000083A7</td></tr>
<tr><td>Van (Green) (Driver)</td><td>0x817DEE39</td><td>No</td><td>813</td><td>0x8000624B</td><td>0x00004F27</td></tr>
<tr><td>Van (Green) (Driver) (Civ Poor female)</td><td>0xB4B2273E</td><td>No</td><td>4438</td><td>0x80009E10</td><td>0x00008D79</td></tr>
<tr><td>Van (Green) (Driver) (Civ Poor male)</td><td>0x50C518B3</td><td>No</td><td>4437</td><td>0x80009E0F</td><td>0x0000B1B3</td></tr>
<tr><td>Van (Racing)</td><td>0xB3F6FAA3</td><td>No</td><td>1677</td><td>0x800074A6</td><td>0x00008C5F</td></tr>
<tr><td>Van (Racing) (Driver)</td><td>0xF9CEA07E</td><td>No</td><td>1678</td><td>0x800074A7</td><td>0x00006BF7</td></tr>
<tr><td>Van (Racing) (Driver) (Civ Motorcycle male)</td><td>0x6970528B</td><td>Yes</td><td>4439</td><td>0x80009E11</td><td>0x0000AAF9</td></tr>
<tr><td>Van (Taxi)</td><td>0x89323325</td><td>No</td><td>3638</td><td>0x80009472</td><td>0xFFFFFFFF</td></tr>
<tr><td>Van (Taxi) (Driver)</td><td>0x36BE9030</td><td>No</td><td>3641</td><td>0x80009475</td><td>0x00001CCA</td></tr>
<tr><td>Van (Taxi) (Driver) (Civ Taxi Driver male)</td><td>0x1073BB1C</td><td>No</td><td>4440</td><td>0x80009E12</td><td>0x00000616</td></tr>
<tr><td>Van_Driver</td><td>0x35634C45</td><td>No</td><td>5067</td><td>0x8000A400</td><td>0x000133A2</td></tr>
<tr><td>Vanquish</td><td>0x7E6FC182</td><td>No</td><td>2250</td><td>0x80008220</td><td>0x00003DA3</td></tr>
<tr><td>Vanquish (base)</td><td>0xCA4FDA36</td><td>No</td><td>2605</td><td>0x800085F3</td><td>0x000077E7</td></tr>
<tr><td>Vanquish (Racing)</td><td>0x1B533F71</td><td>No</td><td>2604</td><td>0x800085F2</td><td>0x0000098D</td></tr>
<tr><td>Vanquish_Driver</td><td>0xE6C5B343</td><td>No</td><td>5397</td><td>0x8000A989</td><td>0x00001D6E</td></tr>
<tr><td>VanRacing_Driver</td><td>0x491C15DF</td><td>No</td><td>5140</td><td>0x8000A47C</td><td>0x0000AB84</td></tr>
<tr><td>Vehicle A12ATGM Missile</td><td>0x8D37601C</td><td>No</td><td>2600</td><td>0x800085EE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle AA Missile</td><td>0x64008733</td><td>No</td><td>2429</td><td>0x80008461</td><td>0x0000DD66</td></tr>
<tr><td>Vehicle AA Missile (sidewinder)</td><td>0x5996DDFE</td><td>No</td><td>5504</td><td>0x8000AABF</td><td>0x00004FB0</td></tr>
<tr><td>Vehicle AA Missile (stinger)</td><td>0xA7913CBC</td><td>No</td><td>5505</td><td>0x8000AAC0</td><td>0x00011CFA</td></tr>
<tr><td>Vehicle AT Missile</td><td>0xDCAE66D6</td><td>No</td><td>2431</td><td>0x80008463</td><td>0x00013765</td></tr>
<tr><td>Vehicle AT Missile (Hellfire)</td><td>0x6951B31C</td><td>No</td><td>4107</td><td>0x80009B16</td><td>0x00001CA8</td></tr>
<tr><td>Vehicle AT Missile (mi35)</td><td>0x655324B9</td><td>Yes</td><td>5506</td><td>0x8000AAC1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Camera (LargeA) (Driver)</td><td>0x2F044516</td><td>No</td><td>1439</td><td>0x80006F87</td><td>0x000101C5</td></tr>
<tr><td>Vehicle Camera (LargeA) (front_right)</td><td>0x175A6E7C</td><td>No</td><td>1440</td><td>0x80006F88</td><td>0x0000BBE3</td></tr>
<tr><td>Vehicle Camera (LargeA) (rear_left)</td><td>0x7A697900</td><td>No</td><td>1456</td><td>0x80006F98</td><td>0x00010E8D</td></tr>
<tr><td>Vehicle Camera (LargeA) (rear_right)</td><td>0x84E1DA0B</td><td>No</td><td>1455</td><td>0x80006F97</td><td>0x00010D4B</td></tr>
<tr><td>Vehicle Camera (LargeB) (Driver)</td><td>0x85DF704D</td><td>No</td><td>1451</td><td>0x80006F93</td><td>0x0000A407</td></tr>
<tr><td>Vehicle Camera (LargeB) (front_right)</td><td>0x0595F839</td><td>No</td><td>1452</td><td>0x80006F94</td><td>0x0000E5E1</td></tr>
<tr><td>Vehicle Camera (LargeB) (rear_left)</td><td>0xFD105EC9</td><td>No</td><td>1462</td><td>0x80006F9E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Camera (LargeB) (rear_right)</td><td>0x6FA03DD0</td><td>No</td><td>1461</td><td>0x80006F9D</td><td>0x00001528</td></tr>
<tr><td>Vehicle Camera (LargeC) (Driver)</td><td>0xA2DB7EA8</td><td>No</td><td>1427</td><td>0x80006F7B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Camera (LargeC) (front_right)</td><td>0x3DD6087A</td><td>No</td><td>1430</td><td>0x80006F7E</td><td>0x000066A5</td></tr>
<tr><td>Vehicle Camera (Medium) (Driver)</td><td>0x5903B001</td><td>No</td><td>1443</td><td>0x80006F8B</td><td>0x0000ABD2</td></tr>
<tr><td>Vehicle Camera (Medium) (front_right)</td><td>0x39D3E695</td><td>No</td><td>1444</td><td>0x80006F8C</td><td>0x00010564</td></tr>
<tr><td>Vehicle Camera (Medium) (Rear Gunner)</td><td>0x16A4173E</td><td>No</td><td>1445</td><td>0x80006F8D</td><td>0x000078B4</td></tr>
<tr><td>Vehicle Camera (Small) (Driver)</td><td>0xDF62F009</td><td>No</td><td>1435</td><td>0x80006F83</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Camera (Small) (front_right)</td><td>0x6A536B0D</td><td>No</td><td>1436</td><td>0x80006F84</td><td>0x0000A7F2</td></tr>
<tr><td>Vehicle Cargo (DoNotUse)</td><td>0x732BFA4D</td><td>No</td><td>2612</td><td>0x800085FB</td><td>0x00009489</td></tr>
<tr><td>Vehicle Chunk Set (Armored)</td><td>0x77C213C7</td><td>No</td><td>6083</td><td>0x900001C5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Chunk Set (Extra Large)</td><td>0x117A6C04</td><td>No</td><td>845</td><td>0x8000639C</td><td>0x0000B99E</td></tr>
<tr><td>Vehicle Chunk Set (LargeA)</td><td>0xF11CF3BB</td><td>No</td><td>844</td><td>0x8000639B</td><td>0x0000817E</td></tr>
<tr><td>Vehicle Chunk Set (LargeB)</td><td>0xB5F3AC76</td><td>No</td><td>860</td><td>0x800063B5</td><td>0x00011392</td></tr>
<tr><td>Vehicle Chunk Set (Medium)</td><td>0xF85207DA</td><td>No</td><td>1202</td><td>0x80006CB2</td><td>0x000042C3</td></tr>
<tr><td>Vehicle Chunk Set (Motorcycle)</td><td>0xF21E5DF8</td><td>Yes</td><td>846</td><td>0x8000639D</td><td>0x00003D28</td></tr>
<tr><td>Vehicle Chunk Set (Small)</td><td>0xA545B962</td><td>No</td><td>843</td><td>0x8000639A</td><td>0x00011608</td></tr>
<tr><td>Vehicle Class (2seat w/ Rear Gunner)</td><td>0x1CAA032A</td><td>No</td><td>882</td><td>0x800063D7</td><td>0x00007EF2</td></tr>
<tr><td>Vehicle Class (2seat)</td><td>0xB40E7285</td><td>No</td><td>704</td><td>0x80005FBB</td><td>0x0000177F</td></tr>
<tr><td>Vehicle Class (4seat w/ Rear Gunner)</td><td>0x17745348</td><td>No</td><td>885</td><td>0x800063DA</td><td>0x00011867</td></tr>
<tr><td>Vehicle Class (4seat w/ Rear Gunner) (Full) (GR)</td><td>0xA56A034C</td><td>No</td><td>1168</td><td>0x80006C80</td><td>0x000033AE</td></tr>
<tr><td>Vehicle Class (4seat w/ Rear Gunner) (Full) (OC)</td><td>0x991FAC2B</td><td>No</td><td>1173</td><td>0x80006C85</td><td>0x00012F65</td></tr>
<tr><td>Vehicle Class (4seat)</td><td>0x57931C4F</td><td>No</td><td>881</td><td>0x800063D6</td><td>0x00005136</td></tr>
<tr><td>Vehicle Class (Buggy)</td><td>0x0F495930</td><td>Yes</td><td>848</td><td>0x8000639F</td><td>0x0000506A</td></tr>
<tr><td>Vehicle Class (LargeB)</td><td>0xA1E06D53</td><td>No</td><td>715</td><td>0x800060B6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Class (Medium)</td><td>0xE0E69EBB</td><td>No</td><td>703</td><td>0x80005FBA</td><td>0x00009DE4</td></tr>
<tr><td>Vehicle Class (Small)</td><td>0x0B561C45</td><td>No</td><td>702</td><td>0x80005FB9</td><td>0x00000315</td></tr>
<tr><td>Vehicle Entrance</td><td>0x7A4310F3</td><td>No</td><td>54</td><td>0x80004649</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (_Default Boat)</td><td>0x2FAE9FA6</td><td>Yes</td><td>4735</td><td>0x8000A092</td><td>0x00001619</td></tr>
<tr><td>Vehicle Entrance (_Default Boat) Small Radius</td><td>0x130EE163</td><td>Yes</td><td>5390</td><td>0x8000A981</td><td>0x0000EA8A</td></tr>
<tr><td>Vehicle Entrance (_Default)</td><td>0x1E6DF616</td><td>No</td><td>1212</td><td>0x80006CC6</td><td>0x00006C17</td></tr>
<tr><td>Vehicle Entrance (_Default) MatchSpeedonExit</td><td>0x01E97725</td><td>No</td><td>5404</td><td>0x8000A995</td><td>0x000019B7</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (AH1Z)</td><td>0x155792CB</td><td>Yes</td><td>3224</td><td>0x80008F0A</td><td>0x0000E2BF</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (AMX30 AA)</td><td>0x38EDD3EC</td><td>Yes</td><td>2971</td><td>0x800089FF</td><td>0x000044A9</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (AMX30)</td><td>0x098E2A74</td><td>Yes</td><td>1684</td><td>0x800074BE</td><td>0x0000FCCC</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Armored Bank Truck)</td><td>0xD8F3BB56</td><td>Yes</td><td>3648</td><td>0x800094E2</td><td>0x000099FE</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (F35b)</td><td>0x522A4BA1</td><td>Yes</td><td>1139</td><td>0x80006B62</td><td>0x00007C1C</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Ka29b)</td><td>0x3F3A3CE4</td><td>Yes</td><td>3650</td><td>0x800094E6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (M113)</td><td>0xE2CF0943</td><td>Yes</td><td>3227</td><td>0x80008F0E</td><td>0x000129E4</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (M1A2)</td><td>0x6A680ECC</td><td>Yes</td><td>3062</td><td>0x80008B8F</td><td>0x0000A30D</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (M2A3)</td><td>0xA17E6C56</td><td>Yes</td><td>2872</td><td>0x80008919</td><td>0x000042A8</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (M551)</td><td>0x518B06ED</td><td>Yes</td><td>3452</td><td>0x800092BA</td><td>0x00004D74</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (MD500)</td><td>0xD2D32C0D</td><td>Yes</td><td>1138</td><td>0x80006B61</td><td>0x0000EE03</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (MH53J Pavelow)</td><td>0xF2DA1950</td><td>Yes</td><td>2970</td><td>0x800089FE</td><td>0x0000CE6D</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Mi26)</td><td>0xB5F3795B</td><td>Yes</td><td>3454</td><td>0x800092BC</td><td>0x00008C65</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Mi35 Solano)</td><td>0x7F1FFF69</td><td>Yes</td><td>3446</td><td>0x800092B4</td><td>0x00012A07</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Mi35)</td><td>0xE5E8BF9F</td><td>Yes</td><td>3223</td><td>0x80008F09</td><td>0x000054B2</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (PGZ95)</td><td>0xD7ADF06A</td><td>Yes</td><td>2967</td><td>0x800089EE</td><td>0x0000101E</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (PLZ45)</td><td>0x3E083794</td><td>Yes</td><td>3449</td><td>0x800092B7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Scorpion90)</td><td>0xADC54D35</td><td>Yes</td><td>1136</td><td>0x80006B5F</td><td>0x0000C667</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (Stingray II)</td><td>0x3DFDEBAA</td><td>Yes</td><td>1213</td><td>0x80006CC7</td><td>0x00001A4D</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (UH1)</td><td>0x546B7A35</td><td>Yes</td><td>2972</td><td>0x80008A00</td><td>0x0000F1A4</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (WZ10)</td><td>0x9E49FA89</td><td>No</td><td>3066</td><td>0x80008B93</td><td>0x000106C5</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (WZ551)</td><td>0x81D36417</td><td>Yes</td><td>3453</td><td>0x800092BB</td><td>0x00004EDE</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (ZBD2000)</td><td>0x9D58E683</td><td>No</td><td>2968</td><td>0x800089F0</td><td>0x00007B99</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (ZTZ63a)</td><td>0x4D4A5673</td><td>Yes</td><td>1685</td><td>0x800074BF</td><td>0x00012338</td></tr>
<tr><td>Vehicle Entrance (Action Hijack) (ZTZ98)</td><td>0xB990D3B0</td><td>Yes</td><td>1215</td><td>0x80006CC9</td><td>0x00005E28</td></tr>
<tr><td>Vehicle Entrance (Airboat Entrance Left)</td><td>0xAE0D5BA3</td><td>Yes</td><td>5392</td><td>0x8000A984</td><td>0x0000C8D8</td></tr>
<tr><td>Vehicle Entrance (Airboat Entrance Right)</td><td>0x1F3E218A</td><td>Yes</td><td>5393</td><td>0x8000A985</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Alouette3 Driver)</td><td>0x790EC576</td><td>Yes</td><td>1211</td><td>0x80006CC5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (APC Rear Hatch)</td><td>0x147B03C6</td><td>Yes</td><td>3228</td><td>0x80008F0F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Armored Bank Truck Rear)</td><td>0x6FF33079</td><td>Yes</td><td>3042</td><td>0x80008B7B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Barco) (Driver)</td><td>0x84CC9268</td><td>No</td><td>3847</td><td>0x80009802</td><td>0x0000EA31</td></tr>
<tr><td>Vehicle Entrance (Boarding Entrance)</td><td>0xBC368B84</td><td>No</td><td>711</td><td>0x80005FDA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Boarding Entrance) Speedboat</td><td>0xB60128C3</td><td>Yes</td><td>5132</td><td>0x8000A473</td><td>0x00010893</td></tr>
<tr><td>Vehicle Entrance (Boarding Exit)</td><td>0x2BB6EBA2</td><td>No</td><td>3222</td><td>0x80008F08</td><td>0x0000ABD8</td></tr>
<tr><td>Vehicle Entrance (CH Destroyer) (Driver)</td><td>0x2014C719</td><td>Yes</td><td>5502</td><td>0x8000AABD</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Cutter Rear Top)</td><td>0x3E64FABE</td><td>No</td><td>4934</td><td>0x8000A29C</td><td>0x0000C8FC</td></tr>
<tr><td>Vehicle Entrance (Dinghy Entrance Left)</td><td>0x97E00B58</td><td>Yes</td><td>5395</td><td>0x8000A987</td><td>0x000013C8</td></tr>
<tr><td>Vehicle Entrance (Dinghy Entrance Right)</td><td>0xEC65DEE3</td><td>Yes</td><td>5394</td><td>0x8000A986</td><td>0x00001564</td></tr>
<tr><td>Vehicle Entrance (Entrance Front Left)</td><td>0x531E3F0C</td><td>No</td><td>700</td><td>0x80005FB7</td><td>0x00010D6A</td></tr>
<tr><td>Vehicle Entrance (Entrance Front Right)</td><td>0xD23F20BF</td><td>No</td><td>701</td><td>0x80005FB8</td><td>0x000003F8</td></tr>
<tr><td>Vehicle Entrance (Entrance Middle Left)</td><td>0x22F97470</td><td>No</td><td>3621</td><td>0x80009461</td><td>0x0001010E</td></tr>
<tr><td>Vehicle Entrance (Entrance Middle Right)</td><td>0x545CD87B</td><td>No</td><td>3622</td><td>0x80009462</td><td>0x000038FF</td></tr>
<tr><td>Vehicle Entrance (Entrance Rear Gunner)</td><td>0x19550473</td><td>No</td><td>4398</td><td>0x80009DCA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Entrance Rear Left)</td><td>0x69E8FD09</td><td>No</td><td>1163</td><td>0x80006C76</td><td>0x0000B154</td></tr>
<tr><td>Vehicle Entrance (Entrance Rear Middle)</td><td>0x096397DD</td><td>No</td><td>3061</td><td>0x80008B8E</td><td>0x00007B0A</td></tr>
<tr><td>Vehicle Entrance (Entrance Rear Right)</td><td>0x4CFBAD10</td><td>No</td><td>1162</td><td>0x80006C75</td><td>0x00006CC7</td></tr>
<tr><td>Vehicle Entrance (EXT Rear Hatch)</td><td>0x5BA9046D</td><td>No</td><td>4672</td><td>0x80009FE2</td><td>0x00008B54</td></tr>
<tr><td>Vehicle Entrance (Extraction) (Entrance Rear Left)</td><td>0x879E8BBB</td><td>No</td><td>4410</td><td>0x80009DEF</td><td>0x0000A406</td></tr>
<tr><td>Vehicle Entrance (Extraction) (Entrance Rear Right)</td><td>0x54E244E2</td><td>No</td><td>4413</td><td>0x80009DF2</td><td>0x00001458</td></tr>
<tr><td>Vehicle Entrance (Fishing Boat Driver)</td><td>0x1CFCEF3C</td><td>Yes</td><td>4948</td><td>0x8000A2AE</td><td>0x0000DE35</td></tr>
<tr><td>Vehicle Entrance (Guntruck Rear Middle)</td><td>0x4AF3110E</td><td>Yes</td><td>5212</td><td>0x8000A5F4</td><td>0x00004F2E</td></tr>
<tr><td>Vehicle Entrance (Huangfeng Driver)</td><td>0x89262A07</td><td>Yes</td><td>4949</td><td>0x8000A2AF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Jetski Entrance Left)</td><td>0xDCE5469B</td><td>No</td><td>4395</td><td>0x80009DC7</td><td>0x00005F74</td></tr>
<tr><td>Vehicle Entrance (Jetski Entrance Right)</td><td>0xCDC4C1C2</td><td>No</td><td>4396</td><td>0x80009DC8</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Jetski Entrance Top)</td><td>0x599BB107</td><td>No</td><td>4397</td><td>0x80009DC9</td><td>0x0000D04D</td></tr>
<tr><td>Vehicle Entrance (Ka29b Driver)</td><td>0x2C59AD71</td><td>Yes</td><td>3649</td><td>0x800094E5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Ka29b Rear Left)</td><td>0xF9E85EFC</td><td>Yes</td><td>3459</td><td>0x800092C1</td><td>0x0000F336</td></tr>
<tr><td>Vehicle Entrance (Ka29b Rear Right)</td><td>0x193FA42F</td><td>Yes</td><td>3460</td><td>0x800092C2</td><td>0x0000FCD0</td></tr>
<tr><td>Vehicle Entrance (Ladder)</td><td>0xA5E62C0C</td><td>No</td><td>3420</td><td>0x80009190</td><td>0x0000918E</td></tr>
<tr><td>Vehicle Entrance (Ladder) (Boat)</td><td>0xFC1AFCB7</td><td>Yes</td><td>4273</td><td>0x80009CAC</td><td>0x0000B0A4</td></tr>
<tr><td>Vehicle Entrance (Ladder) Boat</td><td>0xD0CCBF76</td><td>Yes</td><td>5402</td><td>0x8000A991</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Ladder) Long</td><td>0x34975F2A</td><td>No</td><td>5131</td><td>0x8000A472</td><td>0x0000DBC5</td></tr>
<tr><td>Vehicle Entrance (Ladder) Long Boat</td><td>0x86D24820</td><td>Yes</td><td>5401</td><td>0x8000A990</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Ladder) Small Radius</td><td>0x11CF9D89</td><td>No</td><td>5278</td><td>0x8000A87A</td><td>0x00001941</td></tr>
<tr><td>Vehicle Entrance (LAVIII 25 Gunner)</td><td>0xA6C26784</td><td>Yes</td><td>5202</td><td>0x8000A5EA</td><td>0x0000599D</td></tr>
<tr><td>Vehicle Entrance (LAVIII Driver)</td><td>0x44554A38</td><td>Yes</td><td>2504</td><td>0x8000853A</td><td>0x0000CB6A</td></tr>
<tr><td>Vehicle Entrance (LAVIII Gunner)</td><td>0xBD7BD769</td><td>Yes</td><td>4733</td><td>0x8000A027</td><td>0x0000E86F</td></tr>
<tr><td>Vehicle Entrance (LAVIII MGS Driver)</td><td>0x3A01CD63</td><td>Yes</td><td>4952</td><td>0x8000A2B2</td><td>0x00006D26</td></tr>
<tr><td>Vehicle Entrance (LAVIII MGS Gunner)</td><td>0xFBA91556</td><td>Yes</td><td>4950</td><td>0x8000A2B0</td><td>0x0000628B</td></tr>
<tr><td>Vehicle Entrance (LAVIII MGS Rear Left)</td><td>0xD26C0F5A</td><td>Yes</td><td>4951</td><td>0x8000A2B1</td><td>0x0000EB52</td></tr>
<tr><td>Vehicle Entrance (LAVIII Rear Left)</td><td>0x4CC53CB7</td><td>Yes</td><td>2511</td><td>0x80008541</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (LAVIII Rear Right)</td><td>0x0FAEE3B6</td><td>Yes</td><td>2512</td><td>0x80008542</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (LCUR Driver)</td><td>0xD24BFD9A</td><td>No</td><td>4931</td><td>0x8000A299</td><td>0x00009012</td></tr>
<tr><td>Vehicle Entrance (M113 Driver Hatch)</td><td>0x59E11458</td><td>Yes</td><td>1176</td><td>0x80006C88</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (M2A3 Gunner)</td><td>0x0D310FF4</td><td>Yes</td><td>4941</td><td>0x8000A2A7</td><td>0x000063F6</td></tr>
<tr><td>Vehicle Entrance (M2A3 Rear Hatch)</td><td>0xC9CF6F4B</td><td>Yes</td><td>2485</td><td>0x80008517</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (MD500 Driver)</td><td>0x45A81402</td><td>Yes</td><td>4667</td><td>0x80009FDD</td><td>0x00013C3E</td></tr>
<tr><td>Vehicle Entrance (MH53J Driver)</td><td>0x5B32A391</td><td>Yes</td><td>3652</td><td>0x800094EE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (MH53J Rear Doors)</td><td>0xF55ABB04</td><td>Yes</td><td>4253</td><td>0x80009C98</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Mi26) (seat_rear_right)</td><td>0x21905F76</td><td>Yes</td><td>4924</td><td>0x8000A292</td><td>0x0000C6FA</td></tr>
<tr><td>Vehicle Entrance (Omen Entrance Rear)</td><td>0xC9266137</td><td>No</td><td>5396</td><td>0x8000A988</td><td>0x00008499</td></tr>
<tr><td>Vehicle Entrance (Patrol Boat) (Driver)</td><td>0x1D7B69B5</td><td>Yes</td><td>4399</td><td>0x80009DCB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Patrol Boat) (Gunner)</td><td>0x5195583C</td><td>Yes</td><td>4400</td><td>0x80009DCC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Patrol Boat) (Passenger)</td><td>0xD1549593</td><td>Yes</td><td>4401</td><td>0x80009DCD</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Piranha Gunner)</td><td>0xCA0E1D72</td><td>Yes</td><td>5400</td><td>0x8000A98F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Piranha MKII Driver)</td><td>0x56D56C95</td><td>Yes</td><td>4679</td><td>0x80009FEA</td><td>0x0000EC81</td></tr>
<tr><td>Vehicle Entrance (PLZ45 Rear Hatch)</td><td>0x9419A4C7</td><td>Yes</td><td>3803</td><td>0x800097C0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Salton Seahorse Front Left)</td><td>0x3BDF5031</td><td>Yes</td><td>4932</td><td>0x8000A29A</td><td>0x00004CE1</td></tr>
<tr><td>Vehicle Entrance (Salton Seahorse Front Left) Long</td><td>0xB7524A65</td><td>Yes</td><td>5129</td><td>0x8000A470</td><td>0x00009DC0</td></tr>
<tr><td>Vehicle Entrance (Salton Seahorse Front Right)</td><td>0xB9C424B8</td><td>Yes</td><td>4933</td><td>0x8000A29B</td><td>0x0000A83E</td></tr>
<tr><td>Vehicle Entrance (Salton Seahorse Front Right) Long</td><td>0x02282B6E</td><td>Yes</td><td>5130</td><td>0x8000A471</td><td>0x00009DFB</td></tr>
<tr><td>Vehicle Entrance (Scorpion90 Driver)</td><td>0x74D04970</td><td>Yes</td><td>1203</td><td>0x80006CBA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Tank Hatch Driver)</td><td>0xDFF538EE</td><td>Yes</td><td>1174</td><td>0x80006C86</td><td>0x0000945F</td></tr>
<tr><td>Vehicle Entrance (Tank Hatch Gunner)</td><td>0xC824D93B</td><td>Yes</td><td>1434</td><td>0x80006F82</td><td>0x000108E3</td></tr>
<tr><td>Vehicle Entrance (Turbosquid Driver)</td><td>0x64883B22</td><td>No</td><td>3838</td><td>0x800097F6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Turbosquid Gunner)</td><td>0x61B2C88F</td><td>No</td><td>3839</td><td>0x800097F7</td><td>0x0000FA4A</td></tr>
<tr><td>Vehicle Entrance (Turbosquid Passenger)</td><td>0xE6A83572</td><td>No</td><td>3841</td><td>0x800097F9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (Type 14130 Gunner Front)</td><td>0x5F2D17AB</td><td>No</td><td>4692</td><td>0x80009FF9</td><td>0x0000EA8E</td></tr>
<tr><td>Vehicle Entrance (Type 14310 Driver)</td><td>0xF35695E1</td><td>No</td><td>4704</td><td>0x8000A00A</td><td>0x0000FE95</td></tr>
<tr><td>Vehicle Entrance (UH1 Back Left)</td><td>0x553F473E</td><td>Yes</td><td>4260</td><td>0x80009C9F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (UH1 Back Right)</td><td>0xF0C093A9</td><td>Yes</td><td>4259</td><td>0x80009C9E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (UH1 Driver)</td><td>0xC826006A</td><td>Yes</td><td>3651</td><td>0x800094ED</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (UH1 Middle Left)</td><td>0x2F06893C</td><td>Yes</td><td>4261</td><td>0x80009CA0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (UH1 Middle Right)</td><td>0x3C16776F</td><td>Yes</td><td>4262</td><td>0x80009CA1</td><td>0x000122B4</td></tr>
<tr><td>Vehicle Entrance (UH1 Rear Left)</td><td>0x9B0B2435</td><td>Yes</td><td>4257</td><td>0x80009C9C</td><td>0x0000DC67</td></tr>
<tr><td>Vehicle Entrance (UH1 Rear Right)</td><td>0xCEF29274</td><td>Yes</td><td>4258</td><td>0x80009C9D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (WZ551 Driver)</td><td>0xC61B3E1C</td><td>Yes</td><td>1693</td><td>0x800074CA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (WZ551 Gunner)</td><td>0x8A95B25D</td><td>Yes</td><td>1694</td><td>0x800074CB</td><td>0x000074DD</td></tr>
<tr><td>Vehicle Entrance (WZ551 Passenger)</td><td>0x1CC7AB30</td><td>Yes</td><td>3819</td><td>0x800097D4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (ZBD2000 Driver)</td><td>0x9C406008</td><td>No</td><td>3821</td><td>0x800097D6</td><td>0x000131C6</td></tr>
<tr><td>Vehicle Entrance (ZBD2000 Gunner)</td><td>0x3C2CC799</td><td>No</td><td>3822</td><td>0x800097D7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Entrance (ZBD2000 Passenger)</td><td>0xC09352FC</td><td>No</td><td>3823</td><td>0x800097D8</td><td>0x00010CE9</td></tr>
<tr><td>Vehicle Entrance M35 Boarding Left</td><td>0xABC61C29</td><td>Yes</td><td>5134</td><td>0x8000A475</td><td>0x0001260C</td></tr>
<tr><td>Vehicle Entrance M35 Boarding Right</td><td>0xF49CD850</td><td>Yes</td><td>5136</td><td>0x8000A477</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle LockOn Missile</td><td>0x49F1FC77</td><td>No</td><td>3659</td><td>0x8000951A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Repair Pad</td><td>0xBDB19EB9</td><td>No</td><td>4913</td><td>0x8000A284</td><td>0x00009C83</td></tr>
<tr><td>Vehicle Repair Pickup</td><td>0x1CAB20C6</td><td>No</td><td>6020</td><td>0x900000D4</td><td>0x000082C2</td></tr>
<tr><td>Vehicle Rider Setup (HMMWV) (Soldiers)</td><td>0xDC158E0C</td><td>No</td><td>3542</td><td>0x8000934A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Rider Setup (LAVIII) (Soldiers)</td><td>0xF3E353B1</td><td>Yes</td><td>3242</td><td>0x80008F1E</td><td>0x0000EC57</td></tr>
<tr><td>Vehicle Rider Setup (SX2150) (Soldiers)</td><td>0x4974993C</td><td>No</td><td>3523</td><td>0x80009337</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Ruins</td><td>0xAA5A7CD2</td><td>No</td><td>6119</td><td>0x900001F1</td><td>0x0000686D</td></tr>
<tr><td>Vehicle Seat</td><td>0xB6A14F9E</td><td>No</td><td>51</td><td>0x80004646</td><td>0x00010E3E</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver)</td><td>0x4B53001D</td><td>No</td><td>1189</td><td>0x80006CA0</td><td>0x0000FD8E</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera LargeA)</td><td>0x134CB5CF</td><td>No</td><td>1441</td><td>0x80006F89</td><td>0x0000C1F3</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera LargeB)</td><td>0x382405AA</td><td>No</td><td>1453</td><td>0x80006F95</td><td>0x0000EF65</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera LargeC)</td><td>0xC4A3ACF1</td><td>No</td><td>1428</td><td>0x80006F7C</td><td>0x00009E0A</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera Medium)</td><td>0x28BEE44E</td><td>No</td><td>1449</td><td>0x80006F91</td><td>0x00006838</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_driver) (Camera Small)</td><td>0x74CA85BE</td><td>No</td><td>1437</td><td>0x80006F85</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right)</td><td>0xCE7B0729</td><td>No</td><td>1190</td><td>0x80006CA1</td><td>0x00001018</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera LargeA)</td><td>0x03E38293</td><td>No</td><td>1442</td><td>0x80006F8A</td><td>0x0000E941</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera LargeB)</td><td>0xE90A1F8E</td><td>No</td><td>1454</td><td>0x80006F96</td><td>0x00003755</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera LargeC)</td><td>0x064F89B5</td><td>No</td><td>1429</td><td>0x80006F7D</td><td>0x0000B28E</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera Medium)</td><td>0x1F337852</td><td>No</td><td>1450</td><td>0x80006F92</td><td>0x00005365</td></tr>
<tr><td>Vehicle Seat (2 Seat) (seat_front_right) (Camera Small)</td><td>0xD7C54BAA</td><td>No</td><td>1438</td><td>0x80006F86</td><td>0x000104AA</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_driver)</td><td>0x3E3B9634</td><td>No</td><td>1177</td><td>0x80006C89</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_driver) (Camera Medium)</td><td>0x3BE093CB</td><td>No</td><td>1446</td><td>0x80006F8E</td><td>0x00003A54</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_front_right)</td><td>0x1769414E</td><td>No</td><td>1179</td><td>0x80006C8B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_front_right) (Camera Medium)</td><td>0x426A8A05</td><td>No</td><td>1447</td><td>0x80006F8F</td><td>0x0000BEAE</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_gunner_rearcenter)</td><td>0x13ADE31B</td><td>No</td><td>1178</td><td>0x80006C8A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (3 Seat) (seat_gunner_rearcenter) (Camera Medium)</td><td>0x617799CC</td><td>No</td><td>1448</td><td>0x80006F90</td><td>0x00003136</td></tr>
<tr><td>Vehicle Seat (4 seat Car w/Gunner) (seat_gunner)</td><td>0x1F789BEF</td><td>No</td><td>1159</td><td>0x80006C72</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_left)</td><td>0xB90AAC3C</td><td>No</td><td>1160</td><td>0x80006C73</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_left) (GR)</td><td>0xB778149C</td><td>No</td><td>1164</td><td>0x80006C7C</td><td>0x00005F9F</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_left) (OC)</td><td>0xC76527DB</td><td>No</td><td>1171</td><td>0x80006C83</td><td>0x0001041E</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_right)</td><td>0x8099906F</td><td>No</td><td>1161</td><td>0x80006C74</td><td>0x0000D143</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_right) (GR)</td><td>0x619A4BFD</td><td>No</td><td>1165</td><td>0x80006C7D</td><td>0x0000CC0C</td></tr>
<tr><td>Vehicle Seat (4 Seat Car w/Gunner) (seat_rear_right) (OC)</td><td>0xDEF9E57E</td><td>No</td><td>1172</td><td>0x80006C84</td><td>0x00012CB7</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_driver)</td><td>0xDDCB911D</td><td>No</td><td>887</td><td>0x800063DC</td><td>0x0000C8A7</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_driver) (GR)</td><td>0xCA5B7F8F</td><td>No</td><td>1167</td><td>0x80006C7F</td><td>0x0000727B</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_driver) (OC)</td><td>0x1385A3D0</td><td>No</td><td>1169</td><td>0x80006C81</td><td>0x0000D05B</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_front_right)</td><td>0x67887A29</td><td>No</td><td>888</td><td>0x800063DD</td><td>0x0000038A</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_front_right) (GR)</td><td>0x28F5ACDB</td><td>No</td><td>1166</td><td>0x80006C7E</td><td>0x0000056C</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_front_right) (OC)</td><td>0x354003FC</td><td>No</td><td>1170</td><td>0x80006C82</td><td>0x0000E7A9</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_rear_left)</td><td>0x06FBE959</td><td>No</td><td>1157</td><td>0x80006C70</td><td>0x00012300</td></tr>
<tr><td>Vehicle Seat (4 Seat Car) (seat_rear_right)</td><td>0x784C2E20</td><td>No</td><td>1158</td><td>0x80006C71</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_driver) (Camera LargeA)</td><td>0xD29D48B5</td><td>No</td><td>1587</td><td>0x80007237</td><td>0x00013089</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_driver) (Camera LargeB)</td><td>0xC313000C</td><td>No</td><td>1457</td><td>0x80006F99</td><td>0x0000FB52</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_front_right) (Camera LargeA)</td><td>0x55975DF5</td><td>No</td><td>1588</td><td>0x80007238</td><td>0x0000E591</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_front_right) (Camera LargeB)</td><td>0x460D154C</td><td>No</td><td>1458</td><td>0x80006F9A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_rear_left) (Camera LargeA)</td><td>0xABBC57E1</td><td>No</td><td>1589</td><td>0x80007239</td><td>0x0000BE71</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_rear_right) (Camera LargeA)</td><td>0x309750F0</td><td>No</td><td>1590</td><td>0x8000723A</td><td>0x0000A5EC</td></tr>
<tr><td>Vehicle Seat (4 Seat) (seat_rear_right) (Camera LargeB)</td><td>0x1FFA57C9</td><td>No</td><td>1459</td><td>0x80006F9B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (AH1Z) (Driver)</td><td>0xECFE5E30</td><td>Yes</td><td>3828</td><td>0x800097DE</td><td>0x0000C5BC</td></tr>
<tr><td>Vehicle Seat (AH1Z) (Driver) (Gunner)</td><td>0xBDB52E02</td><td>Yes</td><td>3831</td><td>0x800097E1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (AH1Z) (Driver) (Pilot)</td><td>0x439B9663</td><td>Yes</td><td>3829</td><td>0x800097DF</td><td>0x0000AB5F</td></tr>
<tr><td>Vehicle Seat (AH1Z) (Gunner)</td><td>0x71727191</td><td>Yes</td><td>3830</td><td>0x800097E0</td><td>0x0000EA6D</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_front_left)</td><td>0x36BA6EF0</td><td>Yes</td><td>3630</td><td>0x8000946A</td><td>0x000063CA</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_rear_left)</td><td>0x178C3E7F</td><td>Yes</td><td>3628</td><td>0x80009468</td><td>0x00000C2E</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_rear_left) (Extraction)</td><td>0xE8D77659</td><td>Yes</td><td>4411</td><td>0x80009DF0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_rear_right)</td><td>0xFF7FB3BE</td><td>Yes</td><td>3629</td><td>0x80009469</td><td>0x00004754</td></tr>
<tr><td>Vehicle Seat (Alouette3 Transport) (seat_rear_right) (Extraction)</td><td>0xF54C005E</td><td>Yes</td><td>4412</td><td>0x80009DF1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Alouette3) (Attack) (seat_driver)</td><td>0x30ED76D1</td><td>Yes</td><td>2259</td><td>0x8000822D</td><td>0x00006E1A</td></tr>
<tr><td>Vehicle Seat (Alouette3) (Attack) (seat_rear_left)</td><td>0x007D931D</td><td>Yes</td><td>2261</td><td>0x8000822F</td><td>0x00014024</td></tr>
<tr><td>Vehicle Seat (Alouette3) (seat_front_right)</td><td>0xC2D02F20</td><td>Yes</td><td>2260</td><td>0x8000822E</td><td>0x0000EFBA</td></tr>
<tr><td>Vehicle Seat (Alouette3) (SuperiorityElite) (seat_driver)</td><td>0x94B00D81</td><td>Yes</td><td>3633</td><td>0x8000946D</td><td>0x0000C45D</td></tr>
<tr><td>Vehicle Seat (Alouette3) (Transport) (seat_driver)</td><td>0x48654DF2</td><td>Yes</td><td>2263</td><td>0x80008231</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (AMX30 AA) (seat_driver)</td><td>0xF3170687</td><td>Yes</td><td>3363</td><td>0x8000901D</td><td>0x0000AB7E</td></tr>
<tr><td>Vehicle Seat (APC 4 Rear Seats) (ML)</td><td>0x1664E2C3</td><td>Yes</td><td>3225</td><td>0x80008F0B</td><td>0x0000313C</td></tr>
<tr><td>Vehicle Seat (APC 4 Rear Seats) (MR)</td><td>0xBBD141A9</td><td>Yes</td><td>3226</td><td>0x80008F0C</td><td>0x0000683D</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (BL)</td><td>0xE878771A</td><td>Yes</td><td>2880</td><td>0x80008921</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (BR)</td><td>0xD3B29764</td><td>Yes</td><td>2881</td><td>0x80008922</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (ML)</td><td>0x3BE891A9</td><td>Yes</td><td>2876</td><td>0x8000891D</td><td>0x0000227C</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (MR)</td><td>0x967C32C3</td><td>Yes</td><td>2877</td><td>0x8000891E</td><td>0x00008147</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (RL)</td><td>0x5F60F40A</td><td>Yes</td><td>2878</td><td>0x8000891F</td><td>0x0000F193</td></tr>
<tr><td>Vehicle Seat (APC 6 Rear Seats) (RR)</td><td>0xA7724734</td><td>Yes</td><td>2879</td><td>0x80008920</td><td>0x00011BE0</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (ML)</td><td>0xA4AAFFAE</td><td>Yes</td><td>3043</td><td>0x80008B7C</td><td>0x00008258</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (MR)</td><td>0x94412120</td><td>Yes</td><td>3044</td><td>0x80008B7D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (RL)</td><td>0x55445E25</td><td>Yes</td><td>3045</td><td>0x80008B7E</td><td>0x000021C0</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (RR)</td><td>0x687AD787</td><td>Yes</td><td>3046</td><td>0x80008B7F</td><td>0x0001032F</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (seat_driver)</td><td>0xC5884BDF</td><td>Yes</td><td>3047</td><td>0x80008B80</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Armored Bank Truck Seats) (seat_front_right)</td><td>0x9F5D7DC7</td><td>Yes</td><td>3048</td><td>0x80008B81</td><td>0x0000D5B5</td></tr>
<tr><td>Vehicle Seat (Avenger) (seat_gunner_rearcenter)</td><td>0x698C1C57</td><td>No</td><td>3526</td><td>0x8000933A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Barco) (Driver)</td><td>0x4A6A0527</td><td>No</td><td>3846</td><td>0x80009801</td><td>0x00007D68</td></tr>
<tr><td>Vehicle Seat (Boarding) (FL)</td><td>0xC439F216</td><td>No</td><td>4402</td><td>0x80009DCE</td><td>0x00005070</td></tr>
<tr><td>Vehicle Seat (Boarding) (FR)</td><td>0x483F5AB8</td><td>No</td><td>4403</td><td>0x80009DCF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Boarding) (ML)</td><td>0xF57886F9</td><td>No</td><td>1432</td><td>0x80006F80</td><td>0x0000B4A2</td></tr>
<tr><td>Vehicle Seat (Boarding) (MR)</td><td>0xB3362373</td><td>No</td><td>1433</td><td>0x80006F81</td><td>0x0000F171</td></tr>
<tr><td>Vehicle Seat (Boarding) (MR) AI</td><td>0xF9CA8163</td><td>No</td><td>5399</td><td>0x8000A98D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Boarding) (RL)</td><td>0x58C4387A</td><td>No</td><td>3336</td><td>0x80008FFC</td><td>0x000139D0</td></tr>
<tr><td>Vehicle Seat (Boarding) (RM)</td><td>0x65E27A01</td><td>No</td><td>712</td><td>0x80005FDB</td><td>0x00007DB0</td></tr>
<tr><td>Vehicle Seat (Boarding) (RR)</td><td>0xC3FF2244</td><td>No</td><td>3337</td><td>0x80008FFD</td><td>0x0000E362</td></tr>
<tr><td>Vehicle Seat (Boarding) M35 Left</td><td>0x7F1435B1</td><td>Yes</td><td>5133</td><td>0x8000A474</td><td>0x000121B9</td></tr>
<tr><td>Vehicle Seat (Boarding) M35 Right</td><td>0xEFBFB218</td><td>Yes</td><td>5135</td><td>0x8000A476</td><td>0x000131ED</td></tr>
<tr><td>Vehicle Seat (Boat) (Driver)</td><td>0xB6E19000</td><td>Yes</td><td>3067</td><td>0x80008B94</td><td>0x000116B0</td></tr>
<tr><td>Vehicle Seat (Boat) (FL)</td><td>0x30A035F0</td><td>Yes</td><td>3200</td><td>0x80008EF2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Buggy Hellfire) (seat_driver)</td><td>0x1748A3D7</td><td>Yes</td><td>4695</td><td>0x80009FFC</td><td>0x00005294</td></tr>
<tr><td>Vehicle Seat (Buggy Hellfire) (seat_gunner_rightfront)</td><td>0x657F3EAC</td><td>Yes</td><td>4696</td><td>0x80009FFD</td><td>0x00007DCD</td></tr>
<tr><td>Vehicle Seat (Buggy PR) (seat_driver)</td><td>0xC57D72D2</td><td>Yes</td><td>4683</td><td>0x80009FEE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Buggy PR) (seat_gunner_rightfront)</td><td>0xF12BA63F</td><td>Yes</td><td>4684</td><td>0x80009FEF</td><td>0x0000FA61</td></tr>
<tr><td>Vehicle Seat (CH Destroyer) (Driver)</td><td>0x002D65CC</td><td>Yes</td><td>5501</td><td>0x8000AABC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Chopper) (Driver)</td><td>0xF119BF93</td><td>Yes</td><td>5117</td><td>0x8000A45B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Chopper) (Passenger)</td><td>0x003A6B55</td><td>Yes</td><td>5125</td><td>0x8000A468</td><td>0x00004002</td></tr>
<tr><td>Vehicle Seat (Cigarette) (Driver)</td><td>0x2496653E</td><td>No</td><td>4723</td><td>0x8000A01D</td><td>0x00003B8A</td></tr>
<tr><td>Vehicle Seat (Cigarette) (front_left)</td><td>0x8367AFB5</td><td>No</td><td>4724</td><td>0x8000A01E</td><td>0x00005102</td></tr>
<tr><td>Vehicle Seat (Coanda Attack) (seat_driver)</td><td>0x4A89AC20</td><td>Yes</td><td>3661</td><td>0x8000951C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Coanda Attack) (seat_front_right)</td><td>0x7302BC82</td><td>Yes</td><td>3672</td><td>0x80009527</td><td>0x00012F0F</td></tr>
<tr><td>Vehicle Seat (Coanda Gunship) (seat_driver)</td><td>0xD20C2B1C</td><td>Yes</td><td>869</td><td>0x800063C1</td><td>0x00001802</td></tr>
<tr><td>Vehicle Seat (Coanda Gunship) (seat_front_right)</td><td>0xD4BBE626</td><td>Yes</td><td>3671</td><td>0x80009526</td><td>0x00007AC0</td></tr>
<tr><td>Vehicle Seat (Coanda Superiority) (seat_driver)</td><td>0x462FBFF1</td><td>Yes</td><td>3667</td><td>0x80009522</td><td>0x00009C34</td></tr>
<tr><td>Vehicle Seat (Coanda Superiority) (seat_front_right)</td><td>0x88FF4AA5</td><td>Yes</td><td>3670</td><td>0x80009525</td><td>0x00000E91</td></tr>
<tr><td>Vehicle Seat (Cutter) (Driver)</td><td>0x81A9DBAB</td><td>No</td><td>4706</td><td>0x8000A00C</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Destroyer) (cannon)</td><td>0x6D71738E</td><td>Yes</td><td>3213</td><td>0x80008EFF</td><td>0x0000A7F8</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsFL)</td><td>0xF4A5C4B7</td><td>Yes</td><td>3215</td><td>0x80008F01</td><td>0x000018C2</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsFM)</td><td>0x58260440</td><td>Yes</td><td>3675</td><td>0x8000952A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsFR)</td><td>0x05D61675</td><td>Yes</td><td>3214</td><td>0x80008F00</td><td>0x00013225</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsRL)</td><td>0x43E413F3</td><td>Yes</td><td>3217</td><td>0x80008F03</td><td>0x0000BBE9</td></tr>
<tr><td>Vehicle Seat (Destroyer) (ciwsRR)</td><td>0x86267779</td><td>Yes</td><td>3216</td><td>0x80008F02</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Destroyer) (sam)</td><td>0xF17A1EF4</td><td>Yes</td><td>3218</td><td>0x80008F04</td><td>0x0000441F</td></tr>
<tr><td>Vehicle Seat (Destroyer) (samFM)</td><td>0x7D81090D</td><td>Yes</td><td>3673</td><td>0x80009528</td><td>0x00004387</td></tr>
<tr><td>Vehicle Seat (Destroyer) (samRR)</td><td>0x1E8F6F14</td><td>Yes</td><td>3674</td><td>0x80009529</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Dinghy) (Driver)</td><td>0xDBA6E97F</td><td>Yes</td><td>4711</td><td>0x8000A011</td><td>0x00012F44</td></tr>
<tr><td>Vehicle Seat (Dinghy) (seat_front_middle)</td><td>0x99AE114A</td><td>Yes</td><td>3848</td><td>0x80009803</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Dinghy) (seat_front_right)</td><td>0x31571E01</td><td>Yes</td><td>4712</td><td>0x8000A012</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Dinghy) (seat_middle_middle)</td><td>0x0D679B4C</td><td>Yes</td><td>3849</td><td>0x80009804</td><td>0x0000C78F</td></tr>
<tr><td>Vehicle Seat (Emplaced GL)</td><td>0x7D98A565</td><td>No</td><td>5049</td><td>0x8000A3E7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Emplaced GR M101A1)</td><td>0x99FDFDE4</td><td>No</td><td>5804</td><td>0x8000AF6C</td><td>0x00012FC9</td></tr>
<tr><td>Vehicle Seat (Emplaced MG)</td><td>0x1E90C3AA</td><td>No</td><td>5048</td><td>0x8000A3E6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Emplaced Quad50) (seat)</td><td>0x1F71439C</td><td>No</td><td>2887</td><td>0x80008928</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Emplaced RR)</td><td>0x4B079BF2</td><td>No</td><td>5050</td><td>0x8000A3E8</td><td>0x0000BDB1</td></tr>
<tr><td>Vehicle Seat (Emplaced TOW)</td><td>0xE445A226</td><td>No</td><td>5805</td><td>0x8000AF6E</td><td>0x0000F92D</td></tr>
<tr><td>Vehicle Seat (Emplaced VZ M101A1)</td><td>0x3A1F881F</td><td>No</td><td>3455</td><td>0x800092BD</td><td>0x00006BFA</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (FL)</td><td>0xBD9E64C1</td><td>No</td><td>3330</td><td>0x80008FF6</td><td>0x000088E0</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (FR)</td><td>0xA83AB44B</td><td>No</td><td>3331</td><td>0x80008FF7</td><td>0x00003477</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (RL)</td><td>0x32558E65</td><td>No</td><td>3341</td><td>0x80009001</td><td>0x0000735A</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (RR)</td><td>0x458C07C7</td><td>No</td><td>3342</td><td>0x80009002</td><td>0x0000B784</td></tr>
<tr><td>Vehicle Seat (Emplaced Weapon) (seat)</td><td>0x92362DDE</td><td>No</td><td>1207</td><td>0x80006CBF</td><td>0x00008D9A</td></tr>
<tr><td>Vehicle Seat (Emplaced ZU)</td><td>0x15BB2093</td><td>No</td><td>5051</td><td>0x8000A3E9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Emplaced ZU23) (seat)</td><td>0x75E5FF88</td><td>No</td><td>2507</td><td>0x8000853D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Fishing Boat) (Driver)</td><td>0x22BA2666</td><td>Yes</td><td>4708</td><td>0x8000A00E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Garbage Truck) (seat_driver)</td><td>0x10D3CD2E</td><td>Yes</td><td>4731</td><td>0x8000A025</td><td>0x00002A58</td></tr>
<tr><td>Vehicle Seat (Garbage Truck) (seat_front_right)</td><td>0x7CCED684</td><td>Yes</td><td>4732</td><td>0x8000A026</td><td>0x0000C333</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_driver)</td><td>0x1ADCBF03</td><td>Yes</td><td>1604</td><td>0x80007249</td><td>0x00001510</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_front_right)</td><td>0xD877A843</td><td>Yes</td><td>1605</td><td>0x8000724A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_rear_left)</td><td>0xB7D62217</td><td>Yes</td><td>1606</td><td>0x8000724B</td><td>0x00009EC8</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_rear_middle)</td><td>0xFD932DB7</td><td>Yes</td><td>1608</td><td>0x8000724D</td><td>0x0000E114</td></tr>
<tr><td>Vehicle Seat (Guntruck) (seat_rear_right)</td><td>0xD4944A16</td><td>Yes</td><td>1607</td><td>0x8000724C</td><td>0x000040AA</td></tr>
<tr><td>Vehicle Seat (HMMWV) (Gunner)</td><td>0x20D696B2</td><td>No</td><td>3532</td><td>0x80009340</td><td>0x00013312</td></tr>
<tr><td>Vehicle Seat (HMMWV) (seat_driver)</td><td>0x4789A0A5</td><td>No</td><td>4670</td><td>0x80009FE0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (HMMWV) (seat_front_right)</td><td>0x873C2B61</td><td>No</td><td>4671</td><td>0x80009FE1</td><td>0x00004E88</td></tr>
<tr><td>Vehicle Seat (HMMWV) (seat_rear_left)</td><td>0x480A0A21</td><td>No</td><td>4668</td><td>0x80009FDE</td><td>0x0000CAC9</td></tr>
<tr><td>Vehicle Seat (HMMWV) (seat_rear_right)</td><td>0x48A5BDE8</td><td>No</td><td>4669</td><td>0x80009FDF</td><td>0x0000194C</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (Driver AI)</td><td>0x6A677421</td><td>Yes</td><td>4160</td><td>0x80009B9D</td><td>0x00012E0A</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (Driver)</td><td>0xEA4D87CF</td><td>Yes</td><td>3221</td><td>0x80008F07</td><td>0x000086F8</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (hp_seat_turret_f)</td><td>0x9B252E6B</td><td>Yes</td><td>4158</td><td>0x80009B9B</td><td>0x0000D6A3</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (hp_seat_turret_r)</td><td>0x25533B97</td><td>Yes</td><td>4159</td><td>0x80009B9C</td><td>0x00005EA2</td></tr>
<tr><td>Vehicle Seat (Huangfeng) (seat_missle)</td><td>0xA9158F4C</td><td>Yes</td><td>4157</td><td>0x80009B9A</td><td>0x00006C4D</td></tr>
<tr><td>Vehicle Seat (Jetski)</td><td>0x1FAD5417</td><td>No</td><td>1602</td><td>0x80007247</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Jetski) (CIV)</td><td>0x3FEF4BF4</td><td>No</td><td>1603</td><td>0x80007248</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Jetski) (Passenger)</td><td>0x9BC90912</td><td>No</td><td>4678</td><td>0x80009FE9</td><td>0x0000E5B8</td></tr>
<tr><td>Vehicle Seat (Ka29b) (Driver)</td><td>0xF57F9271</td><td>Yes</td><td>3458</td><td>0x800092C0</td><td>0x0000E67E</td></tr>
<tr><td>Vehicle Seat (Ka29b) (Gunner)</td><td>0x2095DDC8</td><td>Yes</td><td>3457</td><td>0x800092BF</td><td>0x00005E12</td></tr>
<tr><td>Vehicle Seat (Ka29b) (ML)</td><td>0x2448A7D2</td><td>Yes</td><td>4245</td><td>0x80009C8B</td><td>0x000022E9</td></tr>
<tr><td>Vehicle Seat (Ka29b) (MR)</td><td>0xE166E08C</td><td>Yes</td><td>4246</td><td>0x80009C8C</td><td>0x00007994</td></tr>
<tr><td>Vehicle Seat (Ka29b) (RL)</td><td>0x4D6079E1</td><td>Yes</td><td>4248</td><td>0x80009C8E</td><td>0x000061D6</td></tr>
<tr><td>Vehicle Seat (Ka29b) (RR)</td><td>0xB939346B</td><td>Yes</td><td>4247</td><td>0x80009C8D</td><td>0x0000ECC6</td></tr>
<tr><td>Vehicle Seat (LAVIII 25) (Driver)</td><td>0x987066D9</td><td>Yes</td><td>2860</td><td>0x8000890D</td><td>0x000001B0</td></tr>
<tr><td>Vehicle Seat (LAVIII 25) (Gunner)</td><td>0xA1C2CDC0</td><td>Yes</td><td>4916</td><td>0x8000A28A</td><td>0x0000C350</td></tr>
<tr><td>Vehicle Seat (LAVIII 50Cal) (Driver)</td><td>0x90E88163</td><td>Yes</td><td>2505</td><td>0x8000853B</td><td>0x0000987C</td></tr>
<tr><td>Vehicle Seat (LAVIII 50Cal) (Gunner)</td><td>0x528FC956</td><td>Yes</td><td>4915</td><td>0x8000A289</td><td>0x0000549C</td></tr>
<tr><td>Vehicle Seat (LAVIII AD) (Driver)</td><td>0x9D5C52A5</td><td>Yes</td><td>2863</td><td>0x80008910</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (LAVIII AD) (Gunner)</td><td>0x418B280C</td><td>Yes</td><td>4917</td><td>0x8000A28B</td><td>0x00001F9F</td></tr>
<tr><td>Vehicle Seat (LAVIII AT) (Driver)</td><td>0x1B00CF15</td><td>Yes</td><td>2861</td><td>0x8000890E</td><td>0x0000BA44</td></tr>
<tr><td>Vehicle Seat (LAVIII AT) (Gunner)</td><td>0xFA5FF91C</td><td>Yes</td><td>4918</td><td>0x8000A28C</td><td>0x000127AA</td></tr>
<tr><td>Vehicle Seat (LAVIII MEWSS) (Driver)</td><td>0x61B393E1</td><td>Yes</td><td>2510</td><td>0x80008540</td><td>0x00009AA1</td></tr>
<tr><td>Vehicle Seat (LAVIII MEWSS) (Passenger)</td><td>0x8F75135F</td><td>Yes</td><td>5201</td><td>0x8000A5E9</td><td>0x000035B0</td></tr>
<tr><td>Vehicle Seat (LAVIII MGS) (Driver)</td><td>0xBB9DB579</td><td>Yes</td><td>2862</td><td>0x8000890F</td><td>0x0000F73E</td></tr>
<tr><td>Vehicle Seat (LAVIII MGS) (Gunner)</td><td>0x6A019EE0</td><td>Yes</td><td>4919</td><td>0x8000A28D</td><td>0x000128ED</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger BL)</td><td>0xDC40374E</td><td>Yes</td><td>2855</td><td>0x80008908</td><td>0x00012DF9</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger BR)</td><td>0x4BD58F40</td><td>Yes</td><td>2854</td><td>0x80008906</td><td>0x000120B0</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger FL)</td><td>0x23EA9762</td><td>Yes</td><td>2513</td><td>0x80008543</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger FR)</td><td>0xFDDF9E3C</td><td>Yes</td><td>2853</td><td>0x80008905</td><td>0x0000327E</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger ML)</td><td>0x42582D55</td><td>Yes</td><td>2859</td><td>0x8000890C</td><td>0x00000278</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger MR)</td><td>0x32651017</td><td>Yes</td><td>2858</td><td>0x8000890B</td><td>0x0000A489</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger RL)</td><td>0x0CD586FE</td><td>Yes</td><td>2857</td><td>0x8000890A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (LAVIII) (Passenger RR)</td><td>0x1F953F10</td><td>Yes</td><td>2856</td><td>0x80008909</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (LCUR) (Driver)</td><td>0xEEB97B68</td><td>No</td><td>4722</td><td>0x8000A01C</td><td>0x000033BA</td></tr>
<tr><td>Vehicle Seat (LCUR) (Front)</td><td>0xCDABB81B</td><td>No</td><td>3635</td><td>0x8000946F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (LCUR) (Rear)</td><td>0xD9C6456C</td><td>No</td><td>3636</td><td>0x80009470</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (M113 50Cal) (Driver)</td><td>0xAB30D575</td><td>Yes</td><td>3232</td><td>0x80008F13</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (M113 AA) (Driver)</td><td>0x58A10B26</td><td>Yes</td><td>1786</td><td>0x800075EC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (M113 AA) (Gunner)</td><td>0x8589CA63</td><td>Yes</td><td>4255</td><td>0x80009C9A</td><td>0x00009DE6</td></tr>
<tr><td>Vehicle Seat (M113) (Driver)</td><td>0xF94F2200</td><td>Yes</td><td>1785</td><td>0x800075EB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (M113) (Gunner)</td><td>0x449FD1C1</td><td>Yes</td><td>3233</td><td>0x80008F14</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (M2A3) (Driver)</td><td>0x2893392B</td><td>Yes</td><td>2288</td><td>0x8000824C</td><td>0x0000D7D8</td></tr>
<tr><td>Vehicle Seat (M2A3) (Gunner)</td><td>0x0183D30E</td><td>Yes</td><td>4940</td><td>0x8000A2A6</td><td>0x0000757F</td></tr>
<tr><td>Vehicle Seat (M2A3) (Passenger ML)</td><td>0x8DC46964</td><td>Yes</td><td>2481</td><td>0x80008512</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (M2A3) (Passenger MR)</td><td>0xA28A491A</td><td>Yes</td><td>2484</td><td>0x80008516</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (M2A3) (Passenger RL)</td><td>0x197C1A8F</td><td>Yes</td><td>2483</td><td>0x80008515</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (M2A3) (Passenger RR)</td><td>0x54B16CFD</td><td>Yes</td><td>2482</td><td>0x80008514</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (M35 AA) (seat_driver)</td><td>0x9F53C839</td><td>Yes</td><td>2901</td><td>0x80008936</td><td>0x0000E5B3</td></tr>
<tr><td>Vehicle Seat (M35 AA) (seat_front_right)</td><td>0xF706779D</td><td>Yes</td><td>3020</td><td>0x80008B64</td><td>0x000047A2</td></tr>
<tr><td>Vehicle Seat (M35 AA) (seat_rear_middle)</td><td>0x07B485B1</td><td>Yes</td><td>2900</td><td>0x80008935</td><td>0x00009C6F</td></tr>
<tr><td>Vehicle Seat (M35 Cargo) (seat_driver)</td><td>0x412C70A1</td><td>Yes</td><td>2882</td><td>0x80008923</td><td>0x0000D802</td></tr>
<tr><td>Vehicle Seat (M35 Cargo) (seat_front_right)</td><td>0xBC1FC3B5</td><td>Yes</td><td>2883</td><td>0x80008924</td><td>0x000108B2</td></tr>
<tr><td>Vehicle Seat (M35) (seat_front_right)</td><td>0xD990B985</td><td>Yes</td><td>4922</td><td>0x8000A290</td><td>0x0000882E</td></tr>
<tr><td>Vehicle Seat (Main Gun Only) (seat_driver)</td><td>0x214E1119</td><td>No</td><td>1204</td><td>0x80006CBB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (MarkV) (Driver)</td><td>0xFF4D0DA9</td><td>No</td><td>4707</td><td>0x8000A00D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Mattias Chopper) (Driver)</td><td>0x14A645D8</td><td>Yes</td><td>5120</td><td>0x8000A45E</td><td>0x00011341</td></tr>
<tr><td>Vehicle Seat (Mattias Chopper) (Passenger)</td><td>0xF27E45CC</td><td>Yes</td><td>5126</td><td>0x8000A469</td><td>0x00007AB5</td></tr>
<tr><td>Vehicle Seat (MD500 Gunship) (Driver) (Manned)</td><td>0xDF4BDEF4</td><td>Yes</td><td>872</td><td>0x800063C4</td><td>0x000076CF</td></tr>
<tr><td>Vehicle Seat (MD500 Gunship) (Gunner) (Manned)</td><td>0xC8F6FAC7</td><td>Yes</td><td>871</td><td>0x800063C3</td><td>0x0000659F</td></tr>
<tr><td>Vehicle Seat (MD500 Gunship) (seat_front_right)</td><td>0x5A2C4CBC</td><td>Yes</td><td>870</td><td>0x800063C2</td><td>0x00003FA4</td></tr>
<tr><td>Vehicle Seat (MD500) (Driver) (Manned)</td><td>0xEA2730AC</td><td>Yes</td><td>1194</td><td>0x80006CA6</td><td>0x00010F6F</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_driver)</td><td>0x6D139EEE</td><td>Yes</td><td>1193</td><td>0x80006CA5</td><td>0x00009B99</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_front_right)</td><td>0xC1645444</td><td>Yes</td><td>1195</td><td>0x80006CA7</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_rear_left)</td><td>0xA26D7638</td><td>Yes</td><td>2249</td><td>0x8000821F</td><td>0x0000A4E7</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_rear_left) (Stowable)</td><td>0x5EAD8CC8</td><td>Yes</td><td>5835</td><td>0x8000AF90</td><td>0x00013273</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_rear_right)</td><td>0x5543C9C3</td><td>Yes</td><td>2248</td><td>0x8000821E</td><td>0x00009082</td></tr>
<tr><td>Vehicle Seat (MD500) (seat_rear_right) (stowable)</td><td>0x47C1B025</td><td>Yes</td><td>5836</td><td>0x8000AF91</td><td>0x0001378A</td></tr>
<tr><td>Vehicle Seat (MH53J) (Gunner ML)</td><td>0x2A6738C3</td><td>Yes</td><td>3618</td><td>0x8000945E</td><td>0x000013C2</td></tr>
<tr><td>Vehicle Seat (MH53J) (Gunner MR)</td><td>0xCFD397A9</td><td>Yes</td><td>3619</td><td>0x8000945F</td><td>0x0000A81D</td></tr>
<tr><td>Vehicle Seat (MH53J) (Gunner RM)</td><td>0x09406D97</td><td>Yes</td><td>3620</td><td>0x80009460</td><td>0x00007163</td></tr>
<tr><td>Vehicle Seat (MH53J) (Passenger L)</td><td>0x79639EA7</td><td>Yes</td><td>3623</td><td>0x80009463</td><td>0x00013CD3</td></tr>
<tr><td>Vehicle Seat (MH53J) (Passenger R)</td><td>0x676A59C5</td><td>Yes</td><td>3624</td><td>0x80009464</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (MH53J) (Passenger) (base)</td><td>0xCA9FA295</td><td>Yes</td><td>3625</td><td>0x80009465</td><td>0x0000F0A3</td></tr>
<tr><td>Vehicle Seat (MH53J) (seat_driver)</td><td>0x6A8E9A7F</td><td>Yes</td><td>3617</td><td>0x8000945D</td><td>0x0000155F</td></tr>
<tr><td>Vehicle Seat (MH53J) (seat_front_right)</td><td>0x19BB3A67</td><td>Yes</td><td>4254</td><td>0x80009C99</td><td>0x00011C5E</td></tr>
<tr><td>Vehicle Seat (Mi26) (Driver)</td><td>0xD5B19DDC</td><td>Yes</td><td>2892</td><td>0x8000892D</td><td>0x0000075E</td></tr>
<tr><td>Vehicle Seat (Mi26) (seat_front_right)</td><td>0x9C4D6D46</td><td>Yes</td><td>4923</td><td>0x8000A291</td><td>0x0000A698</td></tr>
<tr><td>Vehicle Seat (Mi35 Solano) (seat_driver)</td><td>0xED34AE16</td><td>Yes</td><td>3447</td><td>0x800092B5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Mi35 Solano) (seat_solano_back)</td><td>0xCF1D1942</td><td>Yes</td><td>3800</td><td>0x800097BA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Mi35 Solano) (seat_solano_front)</td><td>0x55F8595E</td><td>Yes</td><td>3448</td><td>0x800092B6</td><td>0x00010D04</td></tr>
<tr><td>Vehicle Seat (Mi35) (Driver)</td><td>0xF1AACA6C</td><td>Yes</td><td>4274</td><td>0x80009CAD</td><td>0x00001AC1</td></tr>
<tr><td>Vehicle Seat (Mi35) (seat_rearleft)</td><td>0xBE3022CD</td><td>Yes</td><td>3834</td><td>0x800097EF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Mi35) (seat_rearright)</td><td>0xD33D7B6C</td><td>Yes</td><td>3835</td><td>0x800097F0</td><td>0x0000B41E</td></tr>
<tr><td>Vehicle Seat (Motorcycle)</td><td>0x7CD4FB1A</td><td>Yes</td><td>826</td><td>0x80006381</td><td>0x00013299</td></tr>
<tr><td>Vehicle Seat (Motorcycle) (Passenger)</td><td>0x6BEB413F</td><td>Yes</td><td>4677</td><td>0x80009FE7</td><td>0x0000BE85</td></tr>
<tr><td>Vehicle Seat (Motorcycle)(AL)</td><td>0xE69A320E</td><td>Yes</td><td>829</td><td>0x80006384</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Motorcycle)(GR)</td><td>0x886B6716</td><td>Yes</td><td>827</td><td>0x80006382</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (MTV) (seat_driver)</td><td>0xC71EA19B</td><td>No</td><td>3473</td><td>0x800092CF</td><td>0x0001396D</td></tr>
<tr><td>Vehicle Seat (MTV) (seat_gunner)</td><td>0x1D81309E</td><td>No</td><td>3474</td><td>0x800092D0</td><td>0x0000158C</td></tr>
<tr><td>Vehicle Seat (Offroad Motorcycle) (Driver)</td><td>0xE8D4945E</td><td>Yes</td><td>5121</td><td>0x8000A45F</td><td>0x00004167</td></tr>
<tr><td>Vehicle Seat (Offroad Motorcycle) (Passenger)</td><td>0xD8AAD71E</td><td>Yes</td><td>5124</td><td>0x8000A467</td><td>0x00000E68</td></tr>
<tr><td>Vehicle Seat (Omen) (Driver)</td><td>0x18915DB3</td><td>No</td><td>850</td><td>0x800063A1</td><td>0x00012C09</td></tr>
<tr><td>Vehicle Seat (Omen) (front_left)</td><td>0x590899C8</td><td>No</td><td>851</td><td>0x800063A2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Omen) (gunner_front)</td><td>0x273A48C2</td><td>No</td><td>849</td><td>0x800063A0</td><td>0x0000BAD8</td></tr>
<tr><td>Vehicle Seat (Omen) (gunner_rear)</td><td>0x39AA5A63</td><td>No</td><td>5516</td><td>0x8000AACC</td><td>0x0000E83E</td></tr>
<tr><td>Vehicle Seat (Panhard Assault) (Driver)</td><td>0x05FB8185</td><td>No</td><td>4925</td><td>0x8000A293</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Panhard Assault) (seat_front_right)</td><td>0x4D50A977</td><td>No</td><td>4926</td><td>0x8000A294</td><td>0x000074CB</td></tr>
<tr><td>Vehicle Seat (Patrol Boat PMC) (Driver)</td><td>0xA44241C2</td><td>Yes</td><td>4681</td><td>0x80009FEC</td><td>0x00003E93</td></tr>
<tr><td>Vehicle Seat (Patrol Boat PMC) (gunner)</td><td>0xA02F9AAF</td><td>Yes</td><td>4680</td><td>0x80009FEB</td><td>0x0001217B</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (Driver)</td><td>0x24CA200E</td><td>Yes</td><td>4686</td><td>0x80009FF2</td><td>0x0000B933</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (seat_gunner_front)</td><td>0x5D009117</td><td>Yes</td><td>4688</td><td>0x80009FF4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (seat_gunner_rear)</td><td>0x7E9AC3F8</td><td>Yes</td><td>4689</td><td>0x80009FF6</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (seat_passenger_front)</td><td>0x8B5360A6</td><td>Yes</td><td>4693</td><td>0x80009FFA</td><td>0x00007C28</td></tr>
<tr><td>Vehicle Seat (Patrol Boat VZ) (seat_passenger_rear)</td><td>0xE4110427</td><td>Yes</td><td>4694</td><td>0x80009FFB</td><td>0x000113E6</td></tr>
<tr><td>Vehicle Seat (PGZ95 Command) (Driver)</td><td>0x129A8750</td><td>Yes</td><td>3041</td><td>0x80008B7A</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (PGZ95) (Driver)</td><td>0x5086BE7B</td><td>Yes</td><td>3035</td><td>0x80008B73</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Piranha) (gunner)</td><td>0x94700BBE</td><td>Yes</td><td>3202</td><td>0x80008EF4</td><td>0x00009C3C</td></tr>
<tr><td>Vehicle Seat (Pirhana) (Driver)</td><td>0xDB2C558D</td><td>No</td><td>3068</td><td>0x80008B95</td><td>0x00011F99</td></tr>
<tr><td>Vehicle Seat (Pirhana) (FL)</td><td>0x75AB3A99</td><td>No</td><td>3201</td><td>0x80008EF3</td><td>0x000041C6</td></tr>
<tr><td>Vehicle Seat (PLZ45) (Driver)</td><td>0x5CB0BA91</td><td>Yes</td><td>3451</td><td>0x800092B9</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (PMC Copter) (Driver)</td><td>0xA16C6B11</td><td>No</td><td>4883</td><td>0x8000A261</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (PMC Mi26) (Driver)</td><td>0x6DFB1320</td><td>Yes</td><td>4884</td><td>0x8000A262</td><td>0x0000F470</td></tr>
<tr><td>Vehicle Seat (PMC UH1) (Attack) (seat_rear_left)</td><td>0x47FC3D75</td><td>Yes</td><td>4889</td><td>0x8000A267</td><td>0x0000C0E0</td></tr>
<tr><td>Vehicle Seat (PMC UH1) (Attack) (seat_rear_right)</td><td>0xDB23ACB4</td><td>Yes</td><td>4890</td><td>0x8000A268</td><td>0x0001125B</td></tr>
<tr><td>Vehicle Seat (Salton Seahorse) (Driver)</td><td>0x17A37E07</td><td>Yes</td><td>1431</td><td>0x80006F7F</td><td>0x000023D6</td></tr>
<tr><td>Vehicle Seat (Scooter) (Driver)</td><td>0xC0DAF4A7</td><td>No</td><td>5119</td><td>0x8000A45D</td><td>0x0000B789</td></tr>
<tr><td>Vehicle Seat (Scooter) (Passenger)</td><td>0xB513F829</td><td>No</td><td>5123</td><td>0x8000A466</td><td>0x00011966</td></tr>
<tr><td>Vehicle Seat (Sidecar Motorcycle) (Driver)</td><td>0xB511913E</td><td>Yes</td><td>4725</td><td>0x8000A01F</td><td>0x0000DC42</td></tr>
<tr><td>Vehicle Seat (Sidecar Motorcycle) (Gunner)</td><td>0xA8D2CD6B</td><td>Yes</td><td>4727</td><td>0x8000A021</td><td>0x000081CA</td></tr>
<tr><td>Vehicle Seat (Sidecar Motorcycle) (Passenger)</td><td>0x5368117E</td><td>Yes</td><td>4726</td><td>0x8000A020</td><td>0x0000DF0B</td></tr>
<tr><td>Vehicle Seat (Small Fishing Boat) (Driver)</td><td>0x37EADD61</td><td>Yes</td><td>4709</td><td>0x8000A00F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Small Fishing Boat) (seat_front_middle)</td><td>0xD4941458</td><td>Yes</td><td>3851</td><td>0x80009807</td><td>0x000040D6</td></tr>
<tr><td>Vehicle Seat (Small Fishing Boat) (seat_front_right)</td><td>0xFBA3E88B</td><td>Yes</td><td>4710</td><td>0x8000A010</td><td>0x0000A044</td></tr>
<tr><td>Vehicle Seat (Small Fishing Boat) (seat_middle_middle)</td><td>0xA5FE7FE6</td><td>Yes</td><td>3850</td><td>0x80009806</td><td>0x0000F506</td></tr>
<tr><td>Vehicle Seat (Sportbike) (Driver)</td><td>0xB70951A7</td><td>No</td><td>5118</td><td>0x8000A45C</td><td>0x0000A26A</td></tr>
<tr><td>Vehicle Seat (Sportbike) (Passenger)</td><td>0xCDB03729</td><td>No</td><td>5122</td><td>0x8000A465</td><td>0x0000F187</td></tr>
<tr><td>Vehicle Seat (Swamp Boat) (Driver)</td><td>0x03F7DF54</td><td>Yes</td><td>3334</td><td>0x80008FFA</td><td>0x00006D98</td></tr>
<tr><td>Vehicle Seat (Swamp Boat) (Front)</td><td>0xE8141EC7</td><td>Yes</td><td>3333</td><td>0x80008FF9</td><td>0x00006AA9</td></tr>
<tr><td>Vehicle Seat (SX2150 MLRS) (seat_driver)</td><td>0xCCB4A13D</td><td>No</td><td>3486</td><td>0x800092DD</td><td>0x00012351</td></tr>
<tr><td>Vehicle Seat (SX2150 MLRS) (seat_front_right)</td><td>0xA4359D49</td><td>No</td><td>3485</td><td>0x800092DC</td><td>0x00006A58</td></tr>
<tr><td>Vehicle Seat (T300) (seat_gunner_rearcenter)</td><td>0xACC9774E</td><td>No</td><td>4939</td><td>0x8000A2A5</td><td>0x00004766</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Driver)</td><td>0x408C6051</td><td>Yes</td><td>17</td><td>0x800038B4</td><td>0x0000B6C0</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Driver) (CH)</td><td>0x27211509</td><td>Yes</td><td>1218</td><td>0x80006CCF</td><td>0x0000D926</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Driver) (OC)</td><td>0x2CBFAD04</td><td>Yes</td><td>1029</td><td>0x800068C4</td><td>0x0000E7D5</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Gunner)</td><td>0xBC092228</td><td>Yes</td><td>720</td><td>0x80006186</td><td>0x0000CE34</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Gunner) (AL)</td><td>0xBDE27A50</td><td>Yes</td><td>4921</td><td>0x8000A28F</td><td>0x00007D09</td></tr>
<tr><td>Vehicle Seat (Tank Default) (Gunner) (CH)</td><td>0x1AB5B3FE</td><td>Yes</td><td>1219</td><td>0x80006CD0</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (TankBike) (AL)</td><td>0x170947AE</td><td>Yes</td><td>2588</td><td>0x800085E1</td><td>0x00006A64</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (Driver)</td><td>0x47E90920</td><td>No</td><td>379</td><td>0x800051BF</td><td>0x000037D6</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (Driver) (CIV)</td><td>0x8448045B</td><td>No</td><td>1594</td><td>0x8000723F</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (Driver) (GR)</td><td>0x1250B030</td><td>No</td><td>1593</td><td>0x8000723E</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (Driver) (OC)</td><td>0xF6063FDF</td><td>No</td><td>1592</td><td>0x8000723D</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (seat_front_left)</td><td>0x6C0EAFAB</td><td>No</td><td>3842</td><td>0x800097FB</td><td>0x0000CEC9</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (seat_front_right)</td><td>0x3FD999D2</td><td>No</td><td>4685</td><td>0x80009FF1</td><td>0x00003727</td></tr>
<tr><td>Vehicle Seat (Turbosquid) (seat_gunner)</td><td>0x7B04A1B1</td><td>No</td><td>3837</td><td>0x800097F5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Type14310) (Driver)</td><td>0xCAB22D13</td><td>No</td><td>3338</td><td>0x80008FFE</td><td>0x00013DA8</td></tr>
<tr><td>Vehicle Seat (Type14310) (seat_gunner_FM)</td><td>0xBFE5906A</td><td>No</td><td>4690</td><td>0x80009FF7</td><td>0x0000CD12</td></tr>
<tr><td>Vehicle Seat (UH1 PMC) (seat_driver)</td><td>0xF0F25EDA</td><td>Yes</td><td>4953</td><td>0x8000A2B5</td><td>0x0000A8AF</td></tr>
<tr><td>Vehicle Seat (UH1 PMC) (Transport) (Driver)</td><td>0xCEEC2586</td><td>Yes</td><td>4954</td><td>0x8000A2B6</td><td>0x00006067</td></tr>
<tr><td>Vehicle Seat (UH1) (Attack) (seat_driver)</td><td>0xB644E3BD</td><td>Yes</td><td>2245</td><td>0x8000821A</td><td>0x00011F8C</td></tr>
<tr><td>Vehicle Seat (UH1) (Attack) (seat_front_right)</td><td>0xF109C4C9</td><td>Yes</td><td>2246</td><td>0x8000821B</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (UH1) (Attack) (seat_rear_left)</td><td>0x1E4712F9</td><td>Yes</td><td>2243</td><td>0x80008218</td><td>0x00003301</td></tr>
<tr><td>Vehicle Seat (UH1) (Attack) (seat_rear_right)</td><td>0x84DB84C0</td><td>Yes</td><td>2244</td><td>0x80008219</td><td>0x0000389F</td></tr>
<tr><td>Vehicle Seat (UH1) (Elite) (seat_driver)</td><td>0xB5EB4A8C</td><td>Yes</td><td>4250</td><td>0x80009C90</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (UH1) (Elite) (seat_front_right)</td><td>0xAD74DC36</td><td>Yes</td><td>4251</td><td>0x80009C92</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (UH1) (Gunship) (Driver)</td><td>0xBFEFDE85</td><td>Yes</td><td>859</td><td>0x800063B2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (UH1) (Gunship) (Driver) (GR pilot)</td><td>0xF21A9A49</td><td>Yes</td><td>862</td><td>0x800063B8</td><td>0x0000B70C</td></tr>
<tr><td>Vehicle Seat (UH1) (Superiority) (seat_driver)</td><td>0x06A7D30E</td><td>Yes</td><td>4206</td><td>0x80009C64</td><td>0x0000DD6C</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (Driver)</td><td>0x28A02742</td><td>Yes</td><td>2486</td><td>0x80008518</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_back_left)</td><td>0xA1538617</td><td>Yes</td><td>2491</td><td>0x80008525</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_back_right)</td><td>0x64F8B616</td><td>Yes</td><td>2488</td><td>0x80008522</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_front_right)</td><td>0xBFBD3CFC</td><td>Yes</td><td>2487</td><td>0x80008519</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_middle_left)</td><td>0xFD696D59</td><td>Yes</td><td>2492</td><td>0x80008527</td><td>0x00001638</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_middle_left) (Non-Stowable)</td><td>0x26D2E819</td><td>Yes</td><td>5852</td><td>0x8000AFA5</td><td>0x0000BAC1</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_middle_right)</td><td>0x66B2FA20</td><td>Yes</td><td>2489</td><td>0x80008523</td><td>0x00001F63</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_middle_right) (Non-Stowable)</td><td>0x84E8B4C2</td><td>Yes</td><td>5853</td><td>0x8000AFA6</td><td>0x000037AE</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_rear_left)</td><td>0x432B0380</td><td>Yes</td><td>2493</td><td>0x80008528</td><td>0x00007C3A</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_rear_left) (Non-Stowable)</td><td>0xCC342DA2</td><td>Yes</td><td>5854</td><td>0x8000AFA7</td><td>0x0000B989</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_rear_right)</td><td>0x0D8EE18B</td><td>Yes</td><td>2490</td><td>0x80008524</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (UH1) (Transport) (seat_rear_right) (Non-Stowable)</td><td>0xD4E3E583</td><td>Yes</td><td>5855</td><td>0x8000AFA8</td><td>0x00004CFB</td></tr>
<tr><td>Vehicle Seat (Veyron Assault) (seat_driver)</td><td>0xE6DF4C82</td><td>No</td><td>4699</td><td>0x8000A002</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (Veyron Assault) (seat_front_right)</td><td>0x4DF7DF30</td><td>No</td><td>4701</td><td>0x8000A006</td><td>0x00000F45</td></tr>
<tr><td>Vehicle Seat (WZ10) (Driver)</td><td>0x4BEEFBB2</td><td>No</td><td>863</td><td>0x800063BB</td><td>0x00009A94</td></tr>
<tr><td>Vehicle Seat (WZ10) (Driver) (Gunner)</td><td>0x64EA84C0</td><td>No</td><td>866</td><td>0x800063BE</td><td>0x00011937</td></tr>
<tr><td>Vehicle Seat (WZ10) (Driver) (Pilot)</td><td>0x60BCE9C1</td><td>No</td><td>865</td><td>0x800063BD</td><td>0x0000F9FC</td></tr>
<tr><td>Vehicle Seat (WZ10) (Gunner)</td><td>0x3F13DD3F</td><td>No</td><td>864</td><td>0x800063BC</td><td>0x0000F728</td></tr>
<tr><td>Vehicle Seat (WZ551) (Driver)</td><td>0xC0DA4364</td><td>Yes</td><td>1672</td><td>0x800074A1</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (WZ551) (Driver) (Amphibious)</td><td>0x2435A3EC</td><td>Yes</td><td>4945</td><td>0x8000A2AB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (WZ551) (Gunner)</td><td>0xA4249BD5</td><td>Yes</td><td>1673</td><td>0x800074A2</td><td>0x000058FB</td></tr>
<tr><td>Vehicle Seat (WZ551) (Passenger)</td><td>0xDA43E5E8</td><td>Yes</td><td>3820</td><td>0x800097D5</td><td>0x0000DB9A</td></tr>
<tr><td>Vehicle Seat (ZBD2000) (Driver)</td><td>0xAE03AE54</td><td>No</td><td>3824</td><td>0x800097DA</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (ZBD2000) (Driver) (Amphibious)</td><td>0x9B4EA59C</td><td>No</td><td>4943</td><td>0x8000A2A9</td><td>0x000095D2</td></tr>
<tr><td>Vehicle Seat (ZBD2000) (Gunner)</td><td>0x1447EFE5</td><td>No</td><td>3825</td><td>0x800097DB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Vehicle Seat (ZBD2000) (Passenger)</td><td>0xAC69DE18</td><td>No</td><td>3826</td><td>0x800097DC</td><td>0x0000B1EF</td></tr>
<tr><td>Vehicle Seat (ZTZ63a) (Driver)</td><td>0xBC9F3F14</td><td>Yes</td><td>1671</td><td>0x800074A0</td><td>0x0000E8F4</td></tr>
<tr><td>Vehicle Seat (ZTZ63A) (Driver) (Amphibious)</td><td>0xFA0CDCDC</td><td>Yes</td><td>4946</td><td>0x8000A2AC</td><td>0x0000ACE6</td></tr>
<tr><td>Vehicle SS Missile</td><td>0x91A6456F</td><td>No</td><td>4882</td><td>0x8000A260</td><td>0x0000A17C</td></tr>
<tr><td>vehicleHealthTemplate</td><td>0x5474E03F</td><td>No</td><td>2796</td><td>0x80008762</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_AllCon002_AN</td><td>0x9321474A</td><td>No</td><td>4033</td><td>0x80009A1D</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_AllCon002_Traffic</td><td>0xFB5D703A</td><td>No</td><td>4365</td><td>0x80009D3C</td><td>0x00006A67</td></tr>
<tr><td>VehList_AllCon003_Allies</td><td>0xDEB07C96</td><td>No</td><td>2196</td><td>0x800081E1</td><td>0x00007F12</td></tr>
<tr><td>VehList_AllCon003_Chinese</td><td>0x865E9911</td><td>No</td><td>2170</td><td>0x800081C4</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_ALLHQ</td><td>0x976B90A3</td><td>No</td><td>2444</td><td>0x800084B0</td><td>0x0000568B</td></tr>
<tr><td>VehList_ALLHQ_AA</td><td>0x1F5AD598</td><td>No</td><td>5636</td><td>0x8000AC86</td><td>0x00004BAF</td></tr>
<tr><td>VehList_ALLHQ_HMMWV</td><td>0x44CF107B</td><td>No</td><td>5921</td><td>0x8000B1CB</td><td>0x000025D4</td></tr>
<tr><td>VehList_AllJob001</td><td>0x588481FC</td><td>No</td><td>4562</td><td>0x80009F30</td><td>0x0000991B</td></tr>
<tr><td>VehList_Amazon_Act1</td><td>0x2DDBE815</td><td>No</td><td>4350</td><td>0x80009D22</td><td>0x0000676B</td></tr>
<tr><td>VehList_Amazon_Act2</td><td>0x8BD42D4A</td><td>No</td><td>5152</td><td>0x8000A48A</td><td>0x0000B918</td></tr>
<tr><td>VehList_Amazon_AllJob002_i_Act1</td><td>0x30A59D56</td><td>No</td><td>4352</td><td>0x80009D24</td><td>0x00002D0C</td></tr>
<tr><td>VehList_Angel_Falls_Act1</td><td>0x4F2BC6FB</td><td>No</td><td>4353</td><td>0x80009D25</td><td>0x00008088</td></tr>
<tr><td>VehList_Blank</td><td>0x263CFCE5</td><td>No</td><td>2392</td><td>0x80008386</td><td>0x0000C494</td></tr>
<tr><td>VehList_Car_Big_Act1</td><td>0x61FA32CC</td><td>No</td><td>4343</td><td>0x80009D1B</td><td>0x00008F77</td></tr>
<tr><td>VehList_Car_City_Act1</td><td>0xC1152F0D</td><td>No</td><td>4335</td><td>0x80009D12</td><td>0x000089A0</td></tr>
<tr><td>VehList_Car_City_Act1ContestedAL</td><td>0x365E148B</td><td>No</td><td>5168</td><td>0x8000A49D</td><td>0x0000DA41</td></tr>
<tr><td>VehList_Car_City_Act2ALL</td><td>0xC53AD1D7</td><td>No</td><td>5169</td><td>0x8000A49E</td><td>0x00004BBE</td></tr>
<tr><td>VehList_Car_City_Act2CHI</td><td>0xC0F65718</td><td>No</td><td>5172</td><td>0x8000A4A1</td><td>0x0000FE7A</td></tr>
<tr><td>VehList_Car_City_Act3ALL</td><td>0x98A524B0</td><td>No</td><td>4374</td><td>0x80009D4A</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_Car_City_Act3CHI</td><td>0x036189C7</td><td>No</td><td>4375</td><td>0x80009D4B</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_Car_Dock_Act1</td><td>0x508F6095</td><td>No</td><td>4338</td><td>0x80009D15</td><td>0x00000882</td></tr>
<tr><td>VehList_Car_Estate_Act1</td><td>0x2DFAD29A</td><td>No</td><td>4334</td><td>0x80009D11</td><td>0x00009613</td></tr>
<tr><td>VehList_Car_Shanty_Act1</td><td>0xE1BC5559</td><td>No</td><td>4332</td><td>0x80009D0F</td><td>0x0000588F</td></tr>
<tr><td>VehList_CHIHQ</td><td>0xF1C5A9BC</td><td>No</td><td>2445</td><td>0x800084B1</td><td>0x00000115</td></tr>
<tr><td>VehList_CHIHQ_AA</td><td>0x39D7B4CD</td><td>No</td><td>5935</td><td>0x8000B1DC</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_Cumana_Act1ALL</td><td>0x7248D833</td><td>No</td><td>4356</td><td>0x80009D29</td><td>0x000021D8</td></tr>
<tr><td>VehList_Cumana_Act1CHI</td><td>0xD27C4934</td><td>No</td><td>4354</td><td>0x80009D26</td><td>0x00008265</td></tr>
<tr><td>VehList_Cumana_act2CHI</td><td>0xF6F0C349</td><td>No</td><td>4378</td><td>0x80009D4E</td><td>0x00004FF4</td></tr>
<tr><td>VehList_Cumana_Fort_AllJob002B</td><td>0x9D0EE581</td><td>No</td><td>4392</td><td>0x80009D60</td><td>0x0000279B</td></tr>
<tr><td>VehList_Guanare_Act1</td><td>0xCAF91A4C</td><td>No</td><td>4345</td><td>0x80009D1D</td><td>0x00011526</td></tr>
<tr><td>VehList_Guanare_Big_Act1</td><td>0x0138AD75</td><td>No</td><td>4348</td><td>0x80009D20</td><td>0x00011CDA</td></tr>
<tr><td>VehList_Guanare_MecCon</td><td>0xF9A68CC6</td><td>No</td><td>2804</td><td>0x8000876A</td><td>0x00010366</td></tr>
<tr><td>VehList_GurHQ_AA</td><td>0xA3CA0241</td><td>No</td><td>5924</td><td>0x8000B1CE</td><td>0x0000CC82</td></tr>
<tr><td>VehList_GurHQ_Traffic</td><td>0x13AC24F2</td><td>No</td><td>5928</td><td>0x8000B1D2</td><td>0x00000A00</td></tr>
<tr><td>VehList_GurHQ_Vehicles</td><td>0x5785F7C8</td><td>Yes</td><td>2527</td><td>0x80008558</td><td>0x000080E2</td></tr>
<tr><td>VehList_JungleMtn_GurCon052</td><td>0x9AE66CBB</td><td>No</td><td>5870</td><td>0x8000B011</td><td>0x0001136F</td></tr>
<tr><td>VehList_JungleMtnA_Act1</td><td>0x97D9B7F0</td><td>No</td><td>4327</td><td>0x80009D0A</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_JungleMtnB_Act1</td><td>0x173E2151</td><td>No</td><td>4328</td><td>0x80009D0B</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_JungleMtnC_Act1</td><td>0xB0DFA0E2</td><td>No</td><td>5956</td><td>0x8000B1F5</td><td>0x00006DD0</td></tr>
<tr><td>VehList_Mar_Altagracia_Act1</td><td>0xAC551BFD</td><td>No</td><td>4322</td><td>0x80009D05</td><td>0x000084B7</td></tr>
<tr><td>VehList_Mar_Altagracia_Act2</td><td>0x2A4D9392</td><td>No</td><td>4591</td><td>0x80009F59</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_Mar_Big_Act1</td><td>0x0C46D0FE</td><td>No</td><td>4340</td><td>0x80009D17</td><td>0x0001344A</td></tr>
<tr><td>VehList_Mar_City_OilCon020Cartel</td><td>0x8B9CECFD</td><td>No</td><td>4026</td><td>0x80009A0C</td><td>0x0000BA9A</td></tr>
<tr><td>VehList_Mar_City_OilCon021</td><td>0x4B792311</td><td>No</td><td>4023</td><td>0x80009A09</td><td>0x00010AF6</td></tr>
<tr><td>VehList_Mar_Industrial_Act1</td><td>0x1B9159B3</td><td>No</td><td>4324</td><td>0x80009D07</td><td>0x00004BA5</td></tr>
<tr><td>VehList_Mar_Industrial_Act2</td><td>0x4193D41C</td><td>No</td><td>4385</td><td>0x80009D58</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_Mar_Industrial_Act3</td><td>0x3B960941</td><td>No</td><td>4386</td><td>0x80009D59</td><td>0x00011002</td></tr>
<tr><td>VehList_Mar_Outskirt_Act1</td><td>0x713CEEC7</td><td>No</td><td>4320</td><td>0x80009D03</td><td>0x0000143F</td></tr>
<tr><td>VehList_Mar_Outskirt_Act1VZ</td><td>0x61676513</td><td>No</td><td>5156</td><td>0x8000A48F</td><td>0x0000CCF9</td></tr>
<tr><td>VehList_Mar_Outskirt_OilCon020Cartel</td><td>0xA455C57D</td><td>No</td><td>4024</td><td>0x80009A0A</td><td>0x00012C70</td></tr>
<tr><td>VehList_Mar_Village_Act1</td><td>0x43DC42A4</td><td>No</td><td>4318</td><td>0x80009D01</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_Mar_Village_Act1_PirCon2</td><td>0xC5D8015E</td><td>No</td><td>4034</td><td>0x80009A1E</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_MarCity_Act1</td><td>0xF1274DA4</td><td>No</td><td>4313</td><td>0x80009CFC</td><td>0x00011FEC</td></tr>
<tr><td>VehList_MarCity_Act1Contested</td><td>0x26D3E1F3</td><td>No</td><td>5153</td><td>0x8000A48C</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_MarCity_Act1ContestedVZ</td><td>0x014B5D57</td><td>No</td><td>5159</td><td>0x8000A493</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_MarCity_Act1OC_R</td><td>0x2A3920CD</td><td>No</td><td>4993</td><td>0x8000A3A9</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_MarCity_Act1UP</td><td>0xCB42F663</td><td>No</td><td>5154</td><td>0x8000A48D</td><td>0x0000D3A6</td></tr>
<tr><td>VehList_MarCity_Act1UP_PirCon02</td><td>0x3594D7FF</td><td>No</td><td>4035</td><td>0x80009A20</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_MarCity_Act2</td><td>0x0B2537FB</td><td>No</td><td>4369</td><td>0x80009D40</td><td>0x0000EDD0</td></tr>
<tr><td>VehList_MarCity_Act2ContestedCH</td><td>0x614F0283</td><td>No</td><td>5162</td><td>0x8000A496</td><td>0x00004102</td></tr>
<tr><td>VehList_MarCity_Act3</td><td>0xE922C3DE</td><td>No</td><td>4371</td><td>0x80009D42</td><td>0x0000109C</td></tr>
<tr><td>VehList_Margarita_Act1</td><td>0x8F68C771</td><td>No</td><td>4571</td><td>0x80009F3D</td><td>0x00003064</td></tr>
<tr><td>VehList_Mer_Big_Act1</td><td>0xE3E52CAA</td><td>No</td><td>4342</td><td>0x80009D1A</td><td>0x00006867</td></tr>
<tr><td>VehList_Mer_City_Act1</td><td>0xBEF61B6B</td><td>No</td><td>2524</td><td>0x80008555</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_Mer_City_Act1ContestedGR</td><td>0x50175F85</td><td>No</td><td>5165</td><td>0x8000A49A</td><td>0x0000F516</td></tr>
<tr><td>VehList_Mer_City_Act2</td><td>0xE4F895D4</td><td>No</td><td>4382</td><td>0x80009D53</td><td>0x00005B08</td></tr>
<tr><td>VehList_Mer_Outskirt_Act1</td><td>0x3AD48073</td><td>No</td><td>4326</td><td>0x80009D09</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_Merida_GurOutskirts</td><td>0xB9FB2202</td><td>No</td><td>2525</td><td>0x80008556</td><td>0x00003E16</td></tr>
<tr><td>VehList_Merida_VZOutskirts</td><td>0xBFF35910</td><td>No</td><td>2526</td><td>0x80008557</td><td>0x0001293A</td></tr>
<tr><td>VehList_OilDepot_Act1</td><td>0x1FC7641F</td><td>No</td><td>4316</td><td>0x80009CFF</td><td>0x0000F4F7</td></tr>
<tr><td>VehList_OilDepot_EXT</td><td>0xCF6DC9F3</td><td>No</td><td>5654</td><td>0x8000AC9C</td><td>0x00012CED</td></tr>
<tr><td>VehList_OilDepot_GunTrucks</td><td>0x801BCAD0</td><td>Yes</td><td>5657</td><td>0x8000AC9F</td><td>0xFFFFFFFF</td></tr>
<tr><td>VehList_OilDepot_Stingray</td><td>0x5F265AC3</td><td>Yes</td><td>5658</td><td>0x8000ACA0</td><td>0x000044F5</td></tr>
<tr><td>VehList_Pir_T300Driver</td><td>0x0BC6FDB8</td><td>No</td><td>5949</td><td>0x8000B1EB</td><td>0x0000BA66</td></tr>
<tr><td>VehList_PirCon003</td><td>0xE9FBB0B1</td><td>No</td><td>4028</td><td>0x80009A11</td><td>0x0000F929</td></tr>
<tr><td>VehList_PirHQ</td><td>0x0BD071F7</td><td>No</td><td>5652</td><td>0x8000AC99</td><td>0x00006341</td></tr>
<tr><td>VehList_VZCon001_Dirtbike</td><td>0xA3901E57</td><td>No</td><td>5948</td><td>0x8000B1EA</td><td>0x000055A4</td></tr>
<tr><td>VehList_VZCon001_M151</td><td>0x963817EF</td><td>Yes</td><td>5943</td><td>0x8000B1E5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Verification Camera</td><td>0xF182CA19</td><td>No</td><td>1915</td><td>0x80007A04</td><td>0x0000EC8E</td></tr>
<tr><td>verify flash</td><td>0xB9F5A2CC</td><td>No</td><td>5294</td><td>0x8000A912</td><td>0x000036AC</td></tr>
<tr><td>Veyron</td><td>0xDE0208C0</td><td>No</td><td>2556</td><td>0x800085BA</td><td>0x0000960E</td></tr>
<tr><td>Veyron (as a building)</td><td>0x5E327E60</td><td>No</td><td>2251</td><td>0x80008225</td><td>0x0000BA95</td></tr>
<tr><td>Veyron (Assault)</td><td>0x046E1AA2</td><td>No</td><td>2591</td><td>0x800085E5</td><td>0xFFFFFFFF</td></tr>
<tr><td>Veyron (Assault) (Driver)</td><td>0x115B8749</td><td>No</td><td>4700</td><td>0x8000A005</td><td>0xFFFFFFFF</td></tr>
<tr><td>Veyron (base)</td><td>0x33588F18</td><td>No</td><td>2606</td><td>0x800085F4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Veyron (Cannon)</td><td>0xCB562B84</td><td>No</td><td>4887</td><td>0x8000A265</td><td>0xFFFFFFFF</td></tr>
<tr><td>Veyron (Driver)</td><td>0x1F484C5F</td><td>No</td><td>4441</td><td>0x80009E13</td><td>0x0000C8B1</td></tr>
<tr><td>Veyron (Driver) (Civ Rich female)</td><td>0x903B0452</td><td>No</td><td>4443</td><td>0x80009E15</td><td>0x0000E546</td></tr>
<tr><td>Veyron (Driver) (Civ Rich male)</td><td>0x66CFAD77</td><td>No</td><td>4442</td><td>0x80009E14</td><td>0x0000DDC0</td></tr>
<tr><td>Veyron_Driver</td><td>0xA225EE3D</td><td>No</td><td>5093</td><td>0x8000A41C</td><td>0x00003AE0</td></tr>
<tr><td>VeyronAssault_Driver</td><td>0xC9AC1A8E</td><td>No</td><td>5109</td><td>0x8000A450</td><td>0x0000AFF1</td></tr>
<tr><td>VZ</td><td>0xB4420059</td><td>No</td><td>32</td><td>0x80004382</td><td>0x00005B5C</td></tr>
<tr><td>VZ Allied Defector</td><td>0x6A0568F2</td><td>No</td><td>4038</td><td>0x80009A6B</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Antenna</td><td>0x963EF124</td><td>No</td><td>2558</td><td>0x800085BD</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Captain</td><td>0x06F7E45D</td><td>No</td><td>2319</td><td>0x800082D4</td><td>0x0000C449</td></tr>
<tr><td>VZ Chinese Defector</td><td>0x8253CF38</td><td>No</td><td>3599</td><td>0x800093EC</td><td>0x00013C64</td></tr>
<tr><td>VZ Deathsquad</td><td>0xAF46A983</td><td>No</td><td>2112</td><td>0x80008186</td><td>0x00010DAF</td></tr>
<tr><td>VZ Deathsquad (Mook)</td><td>0xC964419E</td><td>No</td><td>2167</td><td>0x800081C1</td><td>0x0000AD2C</td></tr>
<tr><td>VZ Deathsquad (Mook) w/ LMG</td><td>0x8D27323C</td><td>No</td><td>2169</td><td>0x800081C3</td><td>0x0000E32A</td></tr>
<tr><td>VZ Deathsquad (Mook) w/ RPG</td><td>0xA75BF6B5</td><td>No</td><td>2168</td><td>0x800081C2</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Deathsquad B</td><td>0x7082C649</td><td>No</td><td>2360</td><td>0x80008319</td><td>0x00012EE8</td></tr>
<tr><td>VZ Deathsquad B HVT</td><td>0xDBCDEE03</td><td>No</td><td>5576</td><td>0x8000AB74</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Deathsquad C</td><td>0x56805EC4</td><td>No</td><td>2361</td><td>0x8000831A</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Defender (AA)</td><td>0x68071939</td><td>No</td><td>5017</td><td>0x8000A3C6</td><td>0x0000C7FF</td></tr>
<tr><td>VZ Defender (AT)</td><td>0x51A916A6</td><td>No</td><td>5016</td><td>0x8000A3C5</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Defender (AT) (Window Spawner)</td><td>0x50E1E3EB</td><td>No</td><td>3008</td><td>0x80008A28</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Defender (MG)</td><td>0x0CF90747</td><td>No</td><td>5018</td><td>0x8000A3C7</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Defender (Rifle)</td><td>0x8F5E7B99</td><td>No</td><td>5015</td><td>0x8000A3C4</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Defender (Sniper)</td><td>0x5F9AF5A8</td><td>No</td><td>5027</td><td>0x8000A3D0</td><td>0x0000910B</td></tr>
<tr><td>VZ Elite</td><td>0xE0C2BA3C</td><td>No</td><td>2111</td><td>0x80008185</td><td>0x0000F948</td></tr>
<tr><td>VZ Guerilla Defector</td><td>0x0075BAE0</td><td>No</td><td>4040</td><td>0x80009A6D</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Heavy (AA Missile)</td><td>0x4F07A507</td><td>No</td><td>1335</td><td>0x80006EA8</td><td>0x000057F7</td></tr>
<tr><td>VZ Heavy (Heavy MG)</td><td>0x405F7B3C</td><td>No</td><td>4076</td><td>0x80009AF6</td><td>0x000037A8</td></tr>
<tr><td>VZ Heavy (Light MG)</td><td>0xBA7B1711</td><td>No</td><td>1028</td><td>0x800068B3</td><td>0x0000DF4A</td></tr>
<tr><td>VZ Heavy (RPG + Rifle)</td><td>0xBAC092CD</td><td>No</td><td>2988</td><td>0x80008A13</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Heavy (RPG)</td><td>0x82CF86E6</td><td>No</td><td>991</td><td>0x8000687C</td><td>0x00013C10</td></tr>
<tr><td>VZ HeliPatrol</td><td>0x8E7B1B61</td><td>Yes</td><td>3082</td><td>0x80008BA6</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ HVT01</td><td>0x3CF53B8E</td><td>No</td><td>819</td><td>0x80006322</td><td>0x0000F970</td></tr>
<tr><td>VZ HVT02</td><td>0x9EFC9199</td><td>No</td><td>2317</td><td>0x800082D2</td><td>0x00004734</td></tr>
<tr><td>VZ HVT03</td><td>0x44F9C554</td><td>No</td><td>2318</td><td>0x800082D3</td><td>0x0000C027</td></tr>
<tr><td>VZ HVT04</td><td>0xA7011B5F</td><td>No</td><td>2320</td><td>0x800082D5</td><td>0x0000EE68</td></tr>
<tr><td>VZ Jet Pilot</td><td>0xFDAD5ECA</td><td>No</td><td>2343</td><td>0x800082EF</td><td>0x00009717</td></tr>
<tr><td>VZ MinerUnionBoss</td><td>0x6C9E6F52</td><td>No</td><td>4039</td><td>0x80009A6C</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Officer</td><td>0x238E6A57</td><td>No</td><td>451</td><td>0x8000568B</td><td>0x00011D5B</td></tr>
<tr><td>VZ Oil Company Defector</td><td>0x4DE8C1C4</td><td>No</td><td>4041</td><td>0x80009A6E</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Riot Soldier</td><td>0x63B075BF</td><td>No</td><td>2113</td><td>0x80008187</td><td>0x00003581</td></tr>
<tr><td>VZ Sniper</td><td>0xAC1CBADE</td><td>No</td><td>1359</td><td>0x80006ECA</td><td>0x00013CC7</td></tr>
<tr><td>VZ Soldier</td><td>0x5FFB1CB3</td><td>No</td><td>35</td><td>0x80004385</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Soldier (Crash Repro)</td><td>0xE7813B45</td><td>No</td><td>2979</td><td>0x80008A08</td><td>0x00013C84</td></tr>
<tr><td>VZ Soldier (Mook)</td><td>0xA22B422E</td><td>No</td><td>2178</td><td>0x800081CE</td><td>0x0000CFFE</td></tr>
<tr><td>VZ Soldier (Seatbelted)</td><td>0xFF5C6CC5</td><td>No</td><td>5916</td><td>0x8000B0CE</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Soldier (stowed)</td><td>0xE913C87C</td><td>No</td><td>1201</td><td>0x80006CB1</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZ Tank Commander</td><td>0xD94E10C5</td><td>Yes</td><td>2114</td><td>0x80008188</td><td>0x0000CDEC</td></tr>
<tr><td>VZBaseTemp</td><td>0xCD89AD48</td><td>No</td><td>1505</td><td>0x8000703F</td><td>0x000059AC</td></tr>
<tr><td>VZBaseTrafficZone</td><td>0xD21D8AAF</td><td>No</td><td>1504</td><td>0x8000703C</td><td>0x00003608</td></tr>
<tr><td>VzDbSpawner</td><td>0x3CFFE175</td><td>No</td><td>3011</td><td>0x80008A2B</td><td>0x0000D9EB</td></tr>
<tr><td>VzDbSpawner (Squad Full AT)</td><td>0xEF3E1340</td><td>No</td><td>5659</td><td>0x8000ACA2</td><td>0x00000437</td></tr>
<tr><td>VzDbSpawner (Squad Half AT)</td><td>0xFC034558</td><td>No</td><td>5660</td><td>0x8000ACA3</td><td>0x00004F61</td></tr>
<tr><td>VzDbSpawner (Squad Quarter AT)</td><td>0x291F2235</td><td>No</td><td>5907</td><td>0x8000B03A</td><td>0x000135EE</td></tr>
<tr><td>VzDbSpawner (Squad)</td><td>0x260CAACE</td><td>No</td><td>3012</td><td>0x80008A2C</td><td>0x0000B620</td></tr>
<tr><td>VZGurTankSpawnlist</td><td>0x8609B23A</td><td>Yes</td><td>2400</td><td>0x800083ED</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZHealthBucket</td><td>0x2BE4C7F1</td><td>No</td><td>553</td><td>0x80005BA7</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZHealthList</td><td>0x00F5431B</td><td>No</td><td>552</td><td>0x80005BA6</td><td>0x0000622E</td></tr>
<tr><td>VZRareHeavy</td><td>0x737DB7D2</td><td>No</td><td>554</td><td>0x80005BA8</td><td>0xFFFFFFFF</td></tr>
<tr><td>VZRockets</td><td>0x02E06A24</td><td>No</td><td>555</td><td>0x80005BA9</td><td>0x00006017</td></tr>
<tr><td>VzTestTrafficZone</td><td>0x7F9379B2</td><td>No</td><td>345</td><td>0x80004E91</td><td>0x00000FCB</td></tr>
<tr><td>VZWindowList</td><td>0xFDE30AFD</td><td>No</td><td>2911</td><td>0x80008944</td><td>0x000000F6</td></tr>
<tr><td>W series</td><td>0xAA8FE983</td><td>No</td><td>2569</td><td>0x800085CC</td><td>0xFFFFFFFF</td></tr>
<tr><td>W12 (normal)</td><td>0xB9D23751</td><td>No</td><td>2573</td><td>0x800085D0</td><td>0x00006765</td></tr>
<tr><td>W12 (normal) (black)</td><td>0xDEBDCC33</td><td>No</td><td>5523</td><td>0x8000AAD4</td><td>0x000086BC</td></tr>
<tr><td>W12 (normal) (blue)</td><td>0x5FBC7946</td><td>No</td><td>5522</td><td>0x8000AAD3</td><td>0xFFFFFFFF</td></tr>
<tr><td>W12 (normal) (bronze)</td><td>0x4A9BCCFA</td><td>No</td><td>5610</td><td>0x8000AC59</td><td>0x0000270F</td></tr>
<tr><td>W12 (normal) (Driver)</td><td>0x7076E2AC</td><td>No</td><td>4444</td><td>0x80009E16</td><td>0x0000B3E2</td></tr>
<tr><td>W12 (normal) (Driver) (Civ Rich female)</td><td>0x6D615051</td><td>No</td><td>4445</td><td>0x80009E17</td><td>0x0000EEC5</td></tr>
<tr><td>W12 (normal) (Driver) (Civ Rich male)</td><td>0x9801E1F4</td><td>No</td><td>4446</td><td>0x80009E18</td><td>0x0000FD12</td></tr>
<tr><td>W12 (normal) (green)</td><td>0x0EDF2B73</td><td>No</td><td>5581</td><td>0x8000AC3C</td><td>0x0000145E</td></tr>
<tr><td>W12 (normal) (lightblue)</td><td>0x83C91BE8</td><td>No</td><td>5527</td><td>0x8000AAD8</td><td>0xFFFFFFFF</td></tr>
<tr><td>W12 (normal) (orange)</td><td>0x2C3451F0</td><td>No</td><td>5525</td><td>0x8000AAD6</td><td>0x00002393</td></tr>
<tr><td>W12 (normal) (paleblue)</td><td>0x4239EE46</td><td>No</td><td>5611</td><td>0x8000AC5A</td><td>0x00006C39</td></tr>
<tr><td>W12 (normal) (red)</td><td>0x0011FF73</td><td>No</td><td>5526</td><td>0x8000AAD7</td><td>0x00003EA6</td></tr>
<tr><td>W12 (normal) (white)</td><td>0xF1254381</td><td>No</td><td>5524</td><td>0x8000AAD5</td><td>0x0000028B</td></tr>
<tr><td>W12 (sprint)</td><td>0xFBCDEEBA</td><td>No</td><td>2571</td><td>0x800085CE</td><td>0xFFFFFFFF</td></tr>
<tr><td>W12 (sprint) (Driver)</td><td>0xDCA853E1</td><td>No</td><td>4447</td><td>0x80009E19</td><td>0x0000EF41</td></tr>
<tr><td>W12 (sprint) (Driver) (Civ Rich female)</td><td>0x3FAFE7A0</td><td>No</td><td>4448</td><td>0x80009E1A</td><td>0x00011F2F</td></tr>
<tr><td>W12 (sprint) (Driver) (Civ Rich male)</td><td>0x1BD3AC51</td><td>No</td><td>4449</td><td>0x80009E1B</td><td>0x00005D2D</td></tr>
<tr><td>W12 (Z12)</td><td>0x5DE0BD51</td><td>No</td><td>2570</td><td>0x800085CD</td><td>0x00010B5E</td></tr>
<tr><td>W12 (Z12) (Driver)</td><td>0xBEC014AC</td><td>No</td><td>4450</td><td>0x80009E1C</td><td>0x0000B896</td></tr>
<tr><td>W12 (Z12) (Driver) (Civ Rich female)</td><td>0xEF9F5251</td><td>No</td><td>4451</td><td>0x80009E1D</td><td>0x00012901</td></tr>
<tr><td>W12 (Z12) (Driver) (Civ Rich male)</td><td>0x69FB93F4</td><td>No</td><td>4452</td><td>0x80009E1E</td><td>0x00013124</td></tr>
<tr><td>W12 (Z12) Racer</td><td>0x82E9924A</td><td>No</td><td>4018</td><td>0x800099A8</td><td>0x00000522</td></tr>
<tr><td>W12_Driver</td><td>0xA1E5243E</td><td>No</td><td>5094</td><td>0x8000A41D</td><td>0x00002810</td></tr>
<tr><td>W8 (normal)</td><td>0x717E21E6</td><td>No</td><td>2572</td><td>0x800085CF</td><td>0xFFFFFFFF</td></tr>
<tr><td>W8 (normal) (Driver)</td><td>0xB4ED077D</td><td>No</td><td>4453</td><td>0x80009E1F</td><td>0x00005BE6</td></tr>
<tr><td>W8 (normal) (Driver) (Civ Rich female)</td><td>0x642D9ECC</td><td>No</td><td>4454</td><td>0x80009E20</td><td>0xFFFFFFFF</td></tr>
<tr><td>W8 (normal) (Driver) (Civ Rich male)</td><td>0x5902A1DD</td><td>No</td><td>4455</td><td>0x80009E21</td><td>0x00007D2F</td></tr>
<tr><td>W8_Driver</td><td>0x941202DD</td><td>No</td><td>5108</td><td>0x8000A44F</td><td>0x0000347D</td></tr>
<tr><td>wallace_testcube01</td><td>0xF703083B</td><td>No</td><td>723</td><td>0x800061E2</td><td>0xFFFFFFFF</td></tr>
<tr><td>wallace_testrig</td><td>0xC5FFFE39</td><td>No</td><td>724</td><td>0x800061E3</td><td>0x00004A6E</td></tr>
<tr><td>water_template</td><td>0x14AEF06B</td><td>No</td><td>3247</td><td>0x80008F25</td><td>0x0000186B</td></tr>
<tr><td>waterpuddle01</td><td>0xB91F2097</td><td>No</td><td>3544</td><td>0x800093B2</td><td>0x00013C35</td></tr>
<tr><td>waterShore100mTemplate</td><td>0xD29684C1</td><td>No</td><td>5236</td><td>0x8000A6E5</td><td>0x00003A99</td></tr>
<tr><td>waterShore150mTemplate 0x8000a6f1</td><td>0xEB4D47F6</td><td>No</td><td>5248</td><td>0x8000A6F1</td><td>0x0000D599</td></tr>
<tr><td>waterShore200mTemplate 0x8000a6eb</td><td>0xDE398D90</td><td>No</td><td>5242</td><td>0x8000A6EB</td><td>0xFFFFFFFF</td></tr>
<tr><td>waterShore25mTemplate 0x8000a6ed</td><td>0xF9861505</td><td>No</td><td>5244</td><td>0x8000A6ED</td><td>0x00005675</td></tr>
<tr><td>waterShore300mTemplate 0x8000a6ef</td><td>0x179D9769</td><td>No</td><td>5246</td><td>0x8000A6EF</td><td>0x00004D3F</td></tr>
<tr><td>waterShore400mTemplate 0x8000a6ee</td><td>0x91A3F6DD</td><td>No</td><td>5245</td><td>0x8000A6EE</td><td>0x0000B9E7</td></tr>
<tr><td>waterShore50mTemplate 0x8000a6ec</td><td>0x7AFA4926</td><td>No</td><td>5243</td><td>0x8000A6EC</td><td>0x0000BB11</td></tr>
<tr><td>waterShore75mTemplate 0x8000a6f0</td><td>0x253B5EDB</td><td>No</td><td>5247</td><td>0x8000A6F0</td><td>0x0000F03F</td></tr>
<tr><td>waterShore_open</td><td>0x16A64C2C</td><td>No</td><td>5760</td><td>0x8000AE6A</td><td>0x00003686</td></tr>
<tr><td>waterShore_small</td><td>0x883609C5</td><td>No</td><td>5761</td><td>0x8000AE6B</td><td>0x0000B8B6</td></tr>
<tr><td>waterShore_tiny</td><td>0x93827ED6</td><td>No</td><td>5237</td><td>0x8000A6E6</td><td>0x000027CC</td></tr>
<tr><td>Weapon (Human)</td><td>0xE6466F25</td><td>No</td><td>21</td><td>0x8000436E</td><td>0x00012B00</td></tr>
<tr><td>Weapon (TESTS for Art)</td><td>0xEF416863</td><td>No</td><td>1222</td><td>0x80006CD3</td><td>0xFFFFFFFF</td></tr>
<tr><td>WeaponMagDebrisTemplate</td><td>0x4E68D76D</td><td>No</td><td>6082</td><td>0x900001C4</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel (Rear)</td><td>0xE2460FC9</td><td>No</td><td>50</td><td>0x80004643</td><td>0x0000FF2C</td></tr>
<tr><td>Wheel Armored Bank Truck (L)</td><td>0x6F630E42</td><td>Yes</td><td>1797</td><td>0x800075FB</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel Armored Bank Truck (R)</td><td>0x4958151C</td><td>Yes</td><td>1798</td><td>0x800075FC</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel Health</td><td>0x80D436B8</td><td>No</td><td>1900</td><td>0x800077FF</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel Health RL</td><td>0x2E0FD24E</td><td>No</td><td>1904</td><td>0x80007806</td><td>0x0000830C</td></tr>
<tr><td>Wheel Health RR</td><td>0x8E0A5940</td><td>No</td><td>1903</td><td>0x80007805</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel Health XL</td><td>0xD063D4B8</td><td>No</td><td>1901</td><td>0x80007801</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel Health XR</td><td>0x7040AB56</td><td>No</td><td>1902</td><td>0x80007804</td><td>0x00012940</td></tr>
<tr><td>Wheel L300 (L)</td><td>0xDEFDC8E8</td><td>No</td><td>1800</td><td>0x800075FE</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel L300 (R)</td><td>0x7E21F6E6</td><td>No</td><td>1803</td><td>0x80007699</td><td>0x00009805</td></tr>
<tr><td>Wheel L300 (Racing) (L)</td><td>0xA2E7C1D9</td><td>No</td><td>1811</td><td>0x800076A2</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel L300 (Racing) (R)</td><td>0xDF676053</td><td>No</td><td>1812</td><td>0x800076A3</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel SX2150 (L)</td><td>0x3CB0AB26</td><td>No</td><td>3479</td><td>0x800092D6</td><td>0x00003910</td></tr>
<tr><td>Wheel SX2150 (R)</td><td>0x9D8C7D28</td><td>No</td><td>3480</td><td>0x800092D7</td><td>0x00001BDA</td></tr>
<tr><td>Wheel WZ551 (L)</td><td>0xF7B9DCA5</td><td>Yes</td><td>1421</td><td>0x80006F74</td><td>0x0000CEE0</td></tr>
<tr><td>Wheel WZ551 (ML)</td><td>0xB0654998</td><td>Yes</td><td>1426</td><td>0x80006F79</td><td>0x000110BF</td></tr>
<tr><td>Wheel WZ551 (MR)</td><td>0xAC60AA76</td><td>Yes</td><td>1425</td><td>0x80006F78</td><td>0x000119AD</td></tr>
<tr><td>Wheel WZ551 (R)</td><td>0x0AF05607</td><td>Yes</td><td>1422</td><td>0x80006F75</td><td>0xFFFFFFFF</td></tr>
<tr><td>Wheel WZ551 (RL)</td><td>0x026A840B</td><td>Yes</td><td>1424</td><td>0x80006F77</td><td>0x000041C0</td></tr>
<tr><td>Wheel WZ551 (RR)</td><td>0x17CE3481</td><td>Yes</td><td>1423</td><td>0x80006F76</td><td>0xFFFFFFFF</td></tr>
<tr><td>WheelFlame</td><td>0xC614F6F7</td><td>No</td><td>1092</td><td>0x80006A74</td><td>0xFFFFFFFF</td></tr>
<tr><td>Will_atmospheres</td><td>0xADC27D93</td><td>No</td><td>2669</td><td>0x80008645</td><td>0x00010CF8</td></tr>
<tr><td>WindowSeat</td><td>0xFBD5485E</td><td>No</td><td>2907</td><td>0x8000893E</td><td>0xFFFFFFFF</td></tr>
<tr><td>WindowSpawnerTest</td><td>0xEF14D2FB</td><td>No</td><td>2905</td><td>0x8000893C</td><td>0xFFFFFFFF</td></tr>
<tr><td>WindowSpawnerTest2</td><td>0xAE8C7E5B</td><td>No</td><td>2906</td><td>0x8000893D</td><td>0xFFFFFFFF</td></tr>
<tr><td>WindowSpawnerTurret</td><td>0x2A8EFC41</td><td>No</td><td>2908</td><td>0x8000893F</td><td>0x00003722</td></tr>
<tr><td>WorldExit</td><td>0xAA9975CB</td><td>No</td><td>109</td><td>0x80004C17</td><td>0xFFFFFFFF</td></tr>
<tr><td>WS Test</td><td>0x783A7745</td><td>No</td><td>2910</td><td>0x80008942</td><td>0xFFFFFFFF</td></tr>
<tr><td>WZ10</td><td>0x02661E85</td><td>No</td><td>1208</td><td>0x80006CC2</td><td>0x0000976B</td></tr>
<tr><td>WZ10 (Driver)</td><td>0x26B94B90</td><td>No</td><td>2501</td><td>0x80008535</td><td>0x00001038</td></tr>
<tr><td>WZ10 (Ewan)</td><td>0x73EF463D</td><td>No</td><td>5991</td><td>0x8000B373</td><td>0x0000FF43</td></tr>
<tr><td>WZ10 (Full)</td><td>0x1E58E727</td><td>No</td><td>2502</td><td>0x80008536</td><td>0x00007A7A</td></tr>
<tr><td>WZ551</td><td>0xCC9CEB99</td><td>Yes</td><td>1420</td><td>0x80006F73</td><td>0xFFFFFFFF</td></tr>
<tr><td>WZ551 (Amphibious) (DoNotUse)</td><td>0xB17A4B69</td><td>Yes</td><td>4944</td><td>0x8000A2AA</td><td>0x0000C06A</td></tr>
<tr><td>WZ551 (Driver)</td><td>0x29431074</td><td>Yes</td><td>1759</td><td>0x800075D1</td><td>0xFFFFFFFF</td></tr>
<tr><td>WZ551 (Full)</td><td>0x4D84C7B3</td><td>Yes</td><td>1760</td><td>0x800075D2</td><td>0xFFFFFFFF</td></tr>
<tr><td>WZ551_Driver</td><td>0x17FC2D22</td><td>Yes</td><td>5078</td><td>0x8000A40D</td><td>0x00009FAD</td></tr>
<tr><td>ZBD2000</td><td>0x58827779</td><td>No</td><td>1624</td><td>0x8000725F</td><td>0x0000762B</td></tr>
<tr><td>ZBD2000 (Amphibious) (DoNotUse)</td><td>0xD6A07C49</td><td>No</td><td>4942</td><td>0x8000A2A8</td><td>0x000022C4</td></tr>
<tr><td>ZBD2000 (Driver)</td><td>0xEC25EFD4</td><td>No</td><td>1625</td><td>0x80007260</td><td>0xFFFFFFFF</td></tr>
<tr><td>ZBD2000 (DriverGunner)</td><td>0xD745179B</td><td>No</td><td>3469</td><td>0x800092CB</td><td>0x00012DA0</td></tr>
<tr><td>ZBD2000 (Full)</td><td>0x3F57BB93</td><td>No</td><td>1626</td><td>0x80007261</td><td>0x0000302D</td></tr>
<tr><td>ZippoFlame</td><td>0x90BF5C72</td><td>No</td><td>1152</td><td>0x80006B70</td><td>0xFFFFFFFF</td></tr>
<tr><td>ZTZ63a</td><td>0xC36271CF</td><td>Yes</td><td>1621</td><td>0x8000725C</td><td>0xFFFFFFFF</td></tr>
<tr><td>ZTZ63a (Amphibious) (DoNotUse)</td><td>0xE6739AD3</td><td>Yes</td><td>4947</td><td>0x8000A2AD</td><td>0x00006962</td></tr>
<tr><td>ZTZ63a (Driver)</td><td>0xEF287EFA</td><td>Yes</td><td>1622</td><td>0x8000725D</td><td>0xFFFFFFFF</td></tr>
<tr><td>ZTZ63a (Full)</td><td>0x8309B139</td><td>Yes</td><td>1623</td><td>0x8000725E</td><td>0x000007D0</td></tr>
<tr><td>ZTZ98</td><td>0x28CFA508</td><td>Yes</td><td>1214</td><td>0x80006CC8</td><td>0x00001C0A</td></tr>
<tr><td>ZTZ98 (Driver)</td><td>0x33DF6767</td><td>Yes</td><td>1216</td><td>0x80006CCD</td><td>0x00012928</td></tr>
<tr><td>ZTZ98 (Full)</td><td>0xC1F56AAC</td><td>Yes</td><td>1217</td><td>0x80006CCE</td><td>0xFFFFFFFF</td></tr>
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
table.hash-lookup-table td:nth-child(2),
table.hash-lookup-table td:nth-child(4),
table.hash-lookup-table td:nth-child(5),
table.hash-lookup-table td:nth-child(6) {
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
