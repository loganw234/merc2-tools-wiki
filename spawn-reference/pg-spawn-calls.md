---
title: Pg.Spawn Call Sites
parent: Spawn Reference
nav_order: 4
---

# Pg.Spawn Call Sites

Every distinct string literal passed to `Pg.Spawn(...)` in the decompiled scripts (main game +
DLC), plus the `Airstrike.SpawnOrdnance(...)` ordnance strings. These are names the **shipped game
actually spawns**, so they're the highest-confidence spawn strings on the wiki.

**Template key** is the `value_hex` where the name resolves in the export; **—** means the string
wasn't in the export (usually DLC-only content, a name built at runtime, or one the hash export
didn't recover). Spawn with `Pg.Spawn("<name>", x, y, z)`.

<div class="hash-lookup-wrap" markdown="0">
<input type="text" id="hashLookupFilter" class="hash-lookup-search" placeholder="Filter spawn strings..." autocomplete="off">
<div class="hash-lookup-count" id="hashLookupCount"></div>
<div class="hash-lookup-scroll">
<table class="hash-lookup-table" id="hashLookupTable">
<thead>
<tr><th>Spawn string</th><th>Template key</th></tr>
</thead>
<tbody>
<tr><td>_global_containertransplant</td><td>0x80009F08</td></tr>
<tr><td>_global_explosivebarrel_Long_Hibernation</td><td>0x8000AB67</td></tr>
<tr><td>_pmcoutpost_statueSolanobust_lowHP</td><td>0x8000B2F9</td></tr>
<tr><td>_vzoutpost_fueltanks_PmcCon018</td><td>0x8000AB6A</td></tr>
<tr><td>Alouette3 Superiority (Driver)</td><td>0x800075E8</td></tr>
<tr><td>Ambulance (Driver)</td><td>0x80009CB8</td></tr>
<tr><td>Amx30 (Full)</td><td>0x80007254</td></tr>
<tr><td>carpetbomb_explosion</td><td>—</td></tr>
<tr><td>Cluster Bomb Projectile</td><td>0x80008459</td></tr>
<tr><td>Coanda Transport</td><td>0x800081F9</td></tr>
<tr><td>DLC Green Goblin Bomb Projectile</td><td>0x8000A94A</td></tr>
<tr><td>dlc_global_particle_explosion_pickup_timer</td><td>—</td></tr>
<tr><td>dlc_global_particle_sparks_vehicle_box_blue</td><td>—</td></tr>
<tr><td>dlc_global_particle_sparks_vehicle_box_red</td><td>—</td></tr>
<tr><td>DLC_M1A3</td><td>—</td></tr>
<tr><td>DLC_Speed_Boost_Pickup</td><td>—</td></tr>
<tr><td>DLCCon004_Cash_L_03</td><td>—</td></tr>
<tr><td>DLCCon004_Cash_S_01</td><td>—</td></tr>
<tr><td>DLCCon004_Cash_XXL_05</td><td>—</td></tr>
<tr><td>DLCCon004_Timer_Pickup</td><td>—</td></tr>
<tr><td>El Grande</td><td>0x80004F3F</td></tr>
<tr><td>El Grande (Driver)</td><td>0x80004745</td></tr>
<tr><td>Emplaced MG (VZ)</td><td>0x8000855A</td></tr>
<tr><td>Emplaced TOW (Allied) (seatbelt)</td><td>—</td></tr>
<tr><td>Explosion (Airstike Bomb Final Strike)</td><td>0x8000AF7D</td></tr>
<tr><td>Explosion (AT Mine)</td><td>0x80006B6F</td></tr>
<tr><td>Explosion (Bunker Buster Stage 1)</td><td>0x8000845F</td></tr>
<tr><td>Explosion (Bunker Buster Stage 2)</td><td>0x8000845E</td></tr>
<tr><td>Explosion (C4)</td><td>—</td></tr>
<tr><td>Explosion (Force)</td><td>0x8000A3E5</td></tr>
<tr><td>Explosion (Fuel Air Bomb)</td><td>0x80008E37</td></tr>
<tr><td>Explosion (Grenade)</td><td>0x8000568D</td></tr>
<tr><td>Explosion (MOAB)</td><td>0x80008E3C</td></tr>
<tr><td>Explosion (Rocket Artillery)</td><td>0x80008E3D</td></tr>
<tr><td>Explosion (TEST)</td><td>0x80009AF8</td></tr>
<tr><td>Explosion (Water Mine)</td><td>0x8000A274</td></tr>
<tr><td>Flare Projectile Stage 2</td><td>0x80007CCF</td></tr>
<tr><td>Fuel Air Bomb Projectile</td><td>0x80008E4D</td></tr>
<tr><td>fx_Explosion_Huge</td><td>0x80007174</td></tr>
<tr><td>global_particle_airstrike_distance</td><td>0x8000A24A</td></tr>
<tr><td>global_particle_airstrike_tactnuke</td><td>0x8000911B</td></tr>
<tr><td>global_particle_env_smokeplume_distance_tall</td><td>0x8000A251</td></tr>
<tr><td>global_particle_exp_falling_debris_airstrike</td><td>0x8000A973</td></tr>
<tr><td>global_particle_exp_shockwave_ground</td><td>0x80009129</td></tr>
<tr><td>global_particle_explosion_c4</td><td>0x80008028</td></tr>
<tr><td>global_particle_explosion_pickup_money</td><td>0x8000A932</td></tr>
<tr><td>global_particle_explosion_pickup_rocket</td><td>0x8000A937</td></tr>
<tr><td>global_particle_explosion_tankhatch</td><td>0x80007FFD</td></tr>
<tr><td>global_particle_flaresmoke_green</td><td>0x80008033</td></tr>
<tr><td>global_particle_muzzleflash_tank</td><td>0x80008021</td></tr>
<tr><td>Grenade MG Projectile</td><td>0x8000720E</td></tr>
<tr><td>Gunship Shell</td><td>0x8000AF87</td></tr>
<tr><td>Jetski (PR)</td><td>0x80008FF1</td></tr>
<tr><td>Light_airstrike_fuelairbomb_lrg_flash</td><td>0x80009120</td></tr>
<tr><td>Light_airstrike_fuelairbomb_sml</td><td>0x80009121</td></tr>
<tr><td>location</td><td>0x80005422</td></tr>
<tr><td>M113 (VZ) (Full)</td><td>0x800081F4</td></tr>
<tr><td>M151 .50Cal (VZ)</td><td>0x80006C96</td></tr>
<tr><td>M35 (Cargo) (VZ)</td><td>0x800085B9</td></tr>
<tr><td>M35 (Guntruck) (VZ) (Driver)</td><td>0x80008B88</td></tr>
<tr><td>OC Executive (OilCon002_Hostage)</td><td>0x8000B0CD</td></tr>
<tr><td>Offroad Motorcycle (AI ONLY)</td><td>0x8000A44D</td></tr>
<tr><td>Piranha</td><td>0x800075D9</td></tr>
<tr><td>Supply Drop (Blueprints)</td><td>0x8000A68D</td></tr>
<tr><td>Supply Drop (Light MG)</td><td>0x80007221</td></tr>
<tr><td>Supply Drop (Treasure)</td><td>0x8000A68C</td></tr>
<tr><td>T300 (empty)</td><td>0x800085BE</td></tr>
<tr><td>TankBuster_Instant</td><td>—</td></tr>
<tr><td>UH1 Transport (GR) (Full) (RPG)</td><td>0x8000AB75</td></tr>
<tr><td>UH1 Transport (PMC) (Driver)</td><td>0x80008208</td></tr>
<tr><td>Verification Camera</td><td>0x80007A04</td></tr>
<tr><td>Veyron</td><td>0x800085BA</td></tr>
<tr><td>VZ Deathsquad B HVT</td><td>0x8000AB74</td></tr>
<tr><td>VZ Officer</td><td>0x8000568B</td></tr>
<tr><td>VZ Soldier</td><td>0x80004385</td></tr>
<tr><td>ZTZ98</td><td>0x80006CC8</td></tr>
</tbody>
</table>
</div>
</div>

<style>
.hash-lookup-search { width: 100%; box-sizing: border-box; padding: 0.5em 0.75em;
  font-size: 1em; border: 1px solid #c3ccd6; border-radius: 6px; margin-bottom: 0.5em; }
.hash-lookup-count { font-size: 0.85em; color: #4a6fa5; margin-bottom: 0.5em; }
.hash-lookup-scroll { max-height: 70vh; overflow-y: auto; border: 1px solid #c3ccd6; border-radius: 6px; }
table.hash-lookup-table { width: 100%; border-collapse: collapse; font-size: 0.85em; }
table.hash-lookup-table th, table.hash-lookup-table td { padding: 0.3em 0.6em;
  border-bottom: 1px solid #e0e4e9; text-align: left; white-space: nowrap; }
table.hash-lookup-table td:nth-child(2) { font-family: monospace; }
table.hash-lookup-table thead th { position: sticky; top: 0; background: #f5f7fa; z-index: 1; }
table.hash-lookup-table tbody tr:nth-child(even) { background: #fafbfc; }
html.wiki-dark .hash-lookup-search { background: #1b222c; border-color: #33445c; color: #dbe4f0; }
html.wiki-dark .hash-lookup-count { color: #a9c3e8; }
html.wiki-dark .hash-lookup-scroll { border-color: #33445c; }
html.wiki-dark table.hash-lookup-table th, html.wiki-dark table.hash-lookup-table td {
  border-color: #2a3444; color: #dbe4f0; }
html.wiki-dark table.hash-lookup-table thead th { background: #1b222c; }
html.wiki-dark table.hash-lookup-table tbody tr:nth-child(even) { background: #20293a; }
</style>

<script>
(function() {
  var input = document.getElementById("hashLookupFilter");
  var table = document.getElementById("hashLookupTable");
  var countEl = document.getElementById("hashLookupCount");
  if (!input || !table) return;
  var rows = table.tBodies[0].rows;
  function updateCount(shown) { countEl.textContent = shown + " / " + rows.length + " shown"; }
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
