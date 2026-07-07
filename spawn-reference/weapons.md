---
title: Weapons
parent: Spawn Reference
nav_order: 3
---

# Weapons

Weapon-type templates, filtered from the full table by name. In the shipped scripts a weapon is
handed to a character *by name*:

```lua
local w = Pg.GetGuidByName("Assault Rifle")
Human.Inventory.SetAllWeapons(uChar, { w })
```

(real call sites: `resident/hero.lua`, `vz/pmccon001.lua`, `vz/pmccon033.lua` — the last uses
`Pistol (silver)`.) The player arsenal is all in here: `Pistol`, `Pistol (silver)`,
`Covert Pistol`, `Assault Rifle`, `Sniper Rifle`, `Anti-Material Rifle`, `RPG`, `Grenade Launcher`,
`Grenade`, `C4`, `Shotgun`, `Minigun`, `Light MG`.

> **On "Blanco" and other shop names.** The fancy in-game shop/display names are **localized
> strings in the stringdb**, mapped onto these generic template names — they are *not* the template
> names and won't resolve via `GetGuidByName`. ("Blanco" itself is the PmcCon002 mission NPC, not a
> weapon.) Use the generic names below to spawn/give a weapon.

This is a keyword filter, so it also sweeps in vehicle-mounted weapons (e.g. `LAVIII (Minigun)`)
and airstrike designators — filter the table to narrow it.

## Live spawn-test

A 60-template subset was spawn-tested in-game — `Pg.Spawn`'d as a ground pickup, one per second —
and the **Spawns** column records the outcome: **Yes** = confirmed drops as a pickup, **No** = did
not, **—** = not yet tested. **46 of 60 passed.** Every base player weapon works (Pistol, Assault
Rifle, Sniper Rifle, RPG, Shotgun, Minigun, C4, Grenade Launcher, the Machine Pistols — even the
lowercase internal names `rifle` / `smg` / `rpglauncher`).

The 14 failures group into clear *not-a-pickup* kinds, which is itself useful — it tells you what a
name actually is:

- **Projectile / ammo entities** (they fly, they don't drop): `Dumb Rocket`, `Dumb Rocket (CH)`,
  `FA RPG Rocket`.
- **NPC / soldier archetype names**, not weapons: `Chinese Sniper`, `Human Heavy MG`.
- **A vehicle template** the keyword filter caught on "bomb": `Ka29b (bomber)` (a helicopter).
- **Faction / numbered variants** that don't resolve standalone: `Assault Rifle (VZ)`,
  `Automatic Rifle (Chinese)`, `Automatic Rifle (GR)`, `Minigun 900`, `Minigun 1800`.
- **Component / internal names**: `Light_grenade`, `Equipment (Pistol)`.
- The base **`Grenade`** name also didn't drop as a pickup — it appears to resolve to the thrown
  projectile entity rather than an inventory grenade (use `Supply Drop (AL Grenade)` for a pickup).

<div class="hash-lookup-wrap" markdown="0">
<input type="text" id="hashLookupFilter" class="hash-lookup-search" placeholder="Filter weapons..." autocomplete="off">
<div class="hash-lookup-count" id="hashLookupCount"></div>
<div class="hash-lookup-scroll">
<table class="hash-lookup-table" id="hashLookupTable">
<thead>
<tr><th>Name</th><th>Template key</th><th>Spawns</th></tr>
</thead>
<tbody>
<tr><td>Action Hijack Prop (Grenade)</td><td>0x800075E4</td><td>—</td></tr>
<tr><td>Action Hijack Prop (Pistol)</td><td>0x800075E3</td><td>—</td></tr>
<tr><td>Action Hijack Prop (Rifle)</td><td>0x80009DE7</td><td>—</td></tr>
<tr><td>AL Defender (MG)</td><td>0x8000A3CB</td><td>—</td></tr>
<tr><td>AL Defender (Rifle)</td><td>0x8000A3C8</td><td>—</td></tr>
<tr><td>Allied Airborne (Light MG)</td><td>0x80009E65</td><td>—</td></tr>
<tr><td>Allied Heavy (AT Rocket)</td><td>0x80006EC2</td><td>—</td></tr>
<tr><td>Allied Heavy (Light MG)</td><td>0x80006E3D</td><td>—</td></tr>
<tr><td>Allied Sailor (Light MG)</td><td>0x80009AE3</td><td>—</td></tr>
<tr><td>ammo_designator_beacon</td><td>0x800063E5</td><td>—</td></tr>
<tr><td>ammo_designator_beacon_light</td><td>0x8000AEF5</td><td>—</td></tr>
<tr><td>Anti-Material Rifle</td><td>0x80006EAB</td><td>Yes</td></tr>
<tr><td>Anti-Material Rifle (KSVK)</td><td>0x80006EB3</td><td>Yes</td></tr>
<tr><td>Assault Rifle</td><td>0x8000436F</td><td>Yes</td></tr>
<tr><td>Assault Rifle (VZ)</td><td>0x80006B64</td><td>No</td></tr>
<tr><td>AT Rocket</td><td>0x80006B58</td><td>Yes</td></tr>
<tr><td>Automatic Rifle</td><td>0x80006B6A</td><td>Yes</td></tr>
<tr><td>Automatic Rifle (Chinese)</td><td>0x80006B66</td><td>No</td></tr>
<tr><td>Automatic Rifle (GR)</td><td>0x80009B12</td><td>No</td></tr>
<tr><td>Beacon Designator</td><td>0x800063E7</td><td>—</td></tr>
<tr><td>Bomb</td><td>0x80007211</td><td>—</td></tr>
<tr><td>Bullpup Rifle</td><td>0x80006881</td><td>Yes</td></tr>
<tr><td>C4</td><td>0x80005FD3</td><td>Yes</td></tr>
<tr><td>Carbine</td><td>0x80007212</td><td>Yes</td></tr>
<tr><td>CH Defender (MG)</td><td>0x8000A3DD</td><td>—</td></tr>
<tr><td>CH Defender (Rifle)</td><td>0x8000A3D1</td><td>—</td></tr>
<tr><td>CH Defender (Sniper)</td><td>0x8000A3D4</td><td>—</td></tr>
<tr><td>Cheat RPG</td><td>0x8000A26B</td><td>Yes</td></tr>
<tr><td>Cheat RPG Rocket</td><td>0x8000A26A</td><td>—</td></tr>
<tr><td>Chinese Airborne (Light MG)</td><td>0x80009E68</td><td>—</td></tr>
<tr><td>Chinese Heavy (Light MG)</td><td>0x80006EC0</td><td>—</td></tr>
<tr><td>Chinese Heavy (RPG)</td><td>0x80006EC1</td><td>—</td></tr>
<tr><td>Chinese Sailor (Light MG)</td><td>0x80009AE4</td><td>—</td></tr>
<tr><td>Chinese Sniper</td><td>0x80006EC4</td><td>No</td></tr>
<tr><td>Combat Rifle</td><td>0x80006878</td><td>Yes</td></tr>
<tr><td>Covert Pistol</td><td>0x80006B65</td><td>Yes</td></tr>
<tr><td>Covert SMG</td><td>0x80006B67</td><td>Yes</td></tr>
<tr><td>DB VZ RPG + Rifle</td><td>0x80008A15</td><td>—</td></tr>
<tr><td>Dumb Rocket</td><td>0x8000687E</td><td>No</td></tr>
<tr><td>Dumb Rocket (CH)</td><td>0x8000AAC2</td><td>No</td></tr>
<tr><td>Equipment (Pistol)</td><td>0x80006B5A</td><td>No</td></tr>
<tr><td>FA RPG Rocket</td><td>0x80006ED1</td><td>No</td></tr>
<tr><td>Flare Designator</td><td>0x80007CCC</td><td>—</td></tr>
<tr><td>Fuel-Air RPG</td><td>0x80006ED0</td><td>Yes</td></tr>
<tr><td>global_particle_airstrike_carpetbomb_LOD0</td><td>0x8000800C</td><td>—</td></tr>
<tr><td>global_particle_airstrike_carpetbomb_LOD1</td><td>0x8000A915</td><td>—</td></tr>
<tr><td>global_particle_airstrike_clusterbomb</td><td>0x8000800E</td><td>—</td></tr>
<tr><td>global_particle_airstrike_clusterbomb_flame</td><td>0x800091FF</td><td>—</td></tr>
<tr><td>global_particle_airstrike_fuelairbomb</td><td>0x8000911F</td><td>—</td></tr>
<tr><td>global_particle_airstrike_smartbomb</td><td>0x800091F5</td><td>—</td></tr>
<tr><td>global_particle_muzzleflash_grenadelauncher</td><td>0x8000955D</td><td>—</td></tr>
<tr><td>global_particle_muzzleflash_shotgun</td><td>0x80007FFF</td><td>—</td></tr>
<tr><td>global_ribbon_grenade</td><td>0x800090EF</td><td>—</td></tr>
<tr><td>global_ribbon_grenadelauncher</td><td>0x8000955E</td><td>—</td></tr>
<tr><td>GR Defender (MG)</td><td>0x8000A3D6</td><td>—</td></tr>
<tr><td>GR Defender (rifle)</td><td>0x8000A3D5</td><td>—</td></tr>
<tr><td>Grenade</td><td>0x80002331</td><td>No</td></tr>
<tr><td>Grenade (AI)</td><td>0x80008A0B</td><td>—</td></tr>
<tr><td>Grenade Launcher</td><td>0x80006EA4</td><td>Yes</td></tr>
<tr><td>Grenade Launcher PEP</td><td>0x8000AED3</td><td>Yes</td></tr>
<tr><td>Guerilla Heavy (Light MG)</td><td>0x80006EBD</td><td>—</td></tr>
<tr><td>Guerilla Heavy (RPG)</td><td>0x800056E8</td><td>—</td></tr>
<tr><td>Human Heavy MG</td><td>0x80009AF5</td><td>No</td></tr>
<tr><td>Hunting Pistol</td><td>0x80006ECE</td><td>Yes</td></tr>
<tr><td>Ka29b (bomber)</td><td>0x800085ED</td><td>No</td></tr>
<tr><td>Laser Designator</td><td>0x80007CCE</td><td>—</td></tr>
<tr><td>LAVIII (Minigun)</td><td>0x800085AD</td><td>—</td></tr>
<tr><td>LAVIII (Minigun) (Driver)</td><td>0x8000853C</td><td>—</td></tr>
<tr><td>LAVIII (Minigun) (DriverGunner)</td><td>0x8000A491</td><td>—</td></tr>
<tr><td>LAVIII (Minigun) (Full)</td><td>0x80008F19</td><td>—</td></tr>
<tr><td>Light MG</td><td>0x8000569E</td><td>Yes</td></tr>
<tr><td>Light_airstrike_carpetbomb</td><td>0x800091F9</td><td>—</td></tr>
<tr><td>Light_airstrike_clusterbomb</td><td>0x800091F8</td><td>—</td></tr>
<tr><td>Light_airstrike_fuelairbomb_lrg</td><td>0x80009122</td><td>—</td></tr>
<tr><td>Light_airstrike_fuelairbomb_lrg_flash</td><td>0x80009120</td><td>—</td></tr>
<tr><td>Light_airstrike_fuelairbomb_sml</td><td>0x80009121</td><td>—</td></tr>
<tr><td>Light_grenade</td><td>0x80008032</td><td>No</td></tr>
<tr><td>M113 (VZ) (Full RPG)</td><td>0x8000876E</td><td>—</td></tr>
<tr><td>M151 (MG)</td><td>0x80006C98</td><td>—</td></tr>
<tr><td>M151 (MG) (GR)</td><td>0x80006C95</td><td>—</td></tr>
<tr><td>M151 (MG) (GR) (Driver)</td><td>0x800076B0</td><td>—</td></tr>
<tr><td>M151 (MG) (GR) (DriverGunner)</td><td>0x8000A494</td><td>—</td></tr>
<tr><td>M151 (MG) (VZ) (Driver)</td><td>0x800076B1</td><td>—</td></tr>
<tr><td>M35 (Cargo) (VZ) (Full RPG)</td><td>0x8000876D</td><td>—</td></tr>
<tr><td>Machine Pistol</td><td>0x80006B53</td><td>Yes</td></tr>
<tr><td>Machine Pistol (PP2000)</td><td>0x80007213</td><td>Yes</td></tr>
<tr><td>Machine Pistol (TMP)</td><td>0x80006B57</td><td>Yes</td></tr>
<tr><td>Machine Pistol (Uzi)</td><td>0x80006B59</td><td>Yes</td></tr>
<tr><td>Magazine (Assault Rifle)</td><td>0x8000844E</td><td>—</td></tr>
<tr><td>Magazine (RPG)</td><td>0x800079FF</td><td>—</td></tr>
<tr><td>Minigun</td><td>0x80008449</td><td>Yes</td></tr>
<tr><td>Minigun 1000</td><td>0x8000A25C</td><td>Yes</td></tr>
<tr><td>Minigun 1800</td><td>0x8000A25D</td><td>No</td></tr>
<tr><td>Minigun 900</td><td>0x8000A25E</td><td>No</td></tr>
<tr><td>MLRS Rocket</td><td>0x80009322</td><td>—</td></tr>
<tr><td>NGLV (MG)</td><td>0x80008B86</td><td>—</td></tr>
<tr><td>NGLV (MG) (Driver)</td><td>0x80008B8A</td><td>—</td></tr>
<tr><td>NGLV (MG) (DriverGunner)</td><td>0x80008B8C</td><td>—</td></tr>
<tr><td>NGLV (MG) (Full)</td><td>0x80008B90</td><td>—</td></tr>
<tr><td>OC Defender (MG)</td><td>0x8000A3CE</td><td>—</td></tr>
<tr><td>OC Defender (Rifle)</td><td>0x8000A3CC</td><td>—</td></tr>
<tr><td>OC Defender (Sniper)</td><td>0x8000A3CF</td><td>—</td></tr>
<tr><td>OC Heavy (Grenade Launcher)</td><td>0x80006EBB</td><td>—</td></tr>
<tr><td>OC Heavy (Light MG)</td><td>0x80006879</td><td>—</td></tr>
<tr><td>OC Heavy (RPG)</td><td>0x80006AD9</td><td>—</td></tr>
<tr><td>OC Sniper</td><td>0x80006EBC</td><td>—</td></tr>
<tr><td>OilCon020_Carbine</td><td>0x80009A16</td><td>—</td></tr>
<tr><td>OilCon020_Carbine_b</td><td>0x80009A1C</td><td>—</td></tr>
<tr><td>PEP Rocket</td><td>0x8000AD6A</td><td>—</td></tr>
<tr><td>Pirate Officer (RPG)</td><td>0x80008552</td><td>—</td></tr>
<tr><td>Pirate Thug (RPG)</td><td>0x8000854F</td><td>—</td></tr>
<tr><td>Pirate Thug (Shotgun)</td><td>0x80006ED2</td><td>—</td></tr>
<tr><td>Pistol</td><td>0x80006B45</td><td>Yes</td></tr>
<tr><td>Pistol (AL)</td><td>0x80009B15</td><td>Yes</td></tr>
<tr><td>Pistol (CH)</td><td>0x80009B13</td><td>Yes</td></tr>
<tr><td>Pistol (GR)</td><td>0x80009B14</td><td>Yes</td></tr>
<tr><td>Pistol (silver)</td><td>0x8000508E</td><td>Yes</td></tr>
<tr><td>PR Defender (MG)</td><td>0x8000A3DC</td><td>—</td></tr>
<tr><td>PR Defender (Rifle)</td><td>0x8000A3D9</td><td>—</td></tr>
<tr><td>rifle</td><td>0x800056AC</td><td>Yes</td></tr>
<tr><td>Rocket</td><td>0x8000A5EF</td><td>—</td></tr>
<tr><td>RPG</td><td>0x8000437B</td><td>Yes</td></tr>
<tr><td>RPG Rocket</td><td>0x80004373</td><td>—</td></tr>
<tr><td>rpglauncher</td><td>0x800056AB</td><td>Yes</td></tr>
<tr><td>Satellite Designator</td><td>0x800052F3</td><td>—</td></tr>
<tr><td>Shotgun</td><td>0x8000569D</td><td>Yes</td></tr>
<tr><td>smg</td><td>0x80006B54</td><td>Yes</td></tr>
<tr><td>Smoke Designator</td><td>0x800052F2</td><td>—</td></tr>
<tr><td>Sniper Rifle</td><td>0x8000569A</td><td>Yes</td></tr>
<tr><td>Sniper Rifle (AA Backup)</td><td>0x8000B036</td><td>Yes</td></tr>
<tr><td>Sniper Rifle (SVD)</td><td>0x80006B43</td><td>Yes</td></tr>
<tr><td>SoundMaterial (wpn_designator)</td><td>0x8000985E</td><td>—</td></tr>
<tr><td>SoundMaterial (wpn_grenade)</td><td>0x80009815</td><td>—</td></tr>
<tr><td>SoundMaterial (wpn_pistol)</td><td>0x80009860</td><td>—</td></tr>
<tr><td>SoundMaterial (wpn_rifle)</td><td>0x80009861</td><td>—</td></tr>
<tr><td>SoundMaterial (wpn_rocket)</td><td>0x80009862</td><td>—</td></tr>
<tr><td>Spawnlist (China Tower RPG)</td><td>0x8000B00B</td><td>—</td></tr>
<tr><td>Spawnlist (Guerilla Tower RPG)</td><td>0x8000B009</td><td>—</td></tr>
<tr><td>Spawnlist (VZ RPG + Rifle)</td><td>0x80008A16</td><td>—</td></tr>
<tr><td>Spawnlist (VZ RPG Patrol)</td><td>0x80008564</td><td>—</td></tr>
<tr><td>Spawnlist (VZ RPG)</td><td>0x800083E7</td><td>—</td></tr>
<tr><td>Spawnlist (VZ Tower RPG)</td><td>0x8000B003</td><td>—</td></tr>
<tr><td>Spawnlist (VZ Tower RPG) 0x8000b2fa</td><td>0x8000B2FA</td><td>—</td></tr>
<tr><td>Supply Drop (AL Grenade)</td><td>0x8000AE08</td><td>Yes</td></tr>
<tr><td>Supply Drop (C4)</td><td>0x8000721E</td><td>Yes</td></tr>
<tr><td>Supply Drop (C4) (VZ)</td><td>0x80008567</td><td>Yes</td></tr>
<tr><td>Supply Drop (Guerilla) (Sniper)</td><td>0x80008563</td><td>Yes</td></tr>
<tr><td>Supply Drop (Light MG)</td><td>0x80007221</td><td>Yes</td></tr>
<tr><td>Supply Drop (Light MG) (AL)</td><td>0x8000A259</td><td>Yes</td></tr>
<tr><td>Supply Drop (RPG)</td><td>0x8000AF6F</td><td>Yes</td></tr>
<tr><td>Supply Drop (Sniper CH)</td><td>0x8000AF67</td><td>Yes</td></tr>
<tr><td>Supply Drop (Sniper RU)</td><td>0x8000AF68</td><td>Yes</td></tr>
<tr><td>Supply Drop (Sniper)</td><td>0x8000721D</td><td>Yes</td></tr>
<tr><td>UH1 Transport (GR) (Full) (RPG)</td><td>0x8000AB75</td><td>—</td></tr>
<tr><td>VZ Deathsquad (Mook) w/ LMG</td><td>0x800081C3</td><td>—</td></tr>
<tr><td>VZ Deathsquad (Mook) w/ RPG</td><td>0x800081C2</td><td>—</td></tr>
<tr><td>VZ Defender (MG)</td><td>0x8000A3C7</td><td>—</td></tr>
<tr><td>VZ Defender (Rifle)</td><td>0x8000A3C4</td><td>—</td></tr>
<tr><td>VZ Defender (Sniper)</td><td>0x8000A3D0</td><td>—</td></tr>
<tr><td>VZ Heavy (Heavy MG)</td><td>0x80009AF6</td><td>—</td></tr>
<tr><td>VZ Heavy (Light MG)</td><td>0x800068B3</td><td>—</td></tr>
<tr><td>VZ Heavy (RPG + Rifle)</td><td>0x80008A13</td><td>—</td></tr>
<tr><td>VZ Heavy (RPG)</td><td>0x8000687C</td><td>—</td></tr>
<tr><td>VZ Sniper</td><td>0x80006ECA</td><td>—</td></tr>
<tr><td>VZRockets</td><td>0x80005BA9</td><td>—</td></tr>
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
