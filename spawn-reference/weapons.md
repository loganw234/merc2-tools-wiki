---
title: Weapons
parent: Spawn Reference
nav_order: 3
---

# Weapons

Weapon-type templates. In the shipped scripts a weapon is handed to a character *by name*:

```lua
local w = Pg.GetGuidByName("Assault Rifle")
Human.Inventory.SetAllWeapons(uChar, { w })
```

(real call sites: `resident/hero.lua`, `vz/pmccon001.lua`, `vz/pmccon033.lua` — the last uses
`Pistol (silver)`.) The player arsenal: `Pistol`, `Pistol (silver)`, `Covert Pistol`,
`Assault Rifle`, `Sniper Rifle`, `Anti-Material Rifle`, `RPG`, `Grenade Launcher`, `C4`, `Shotgun`,
`Minigun`, `Light MG` (for a grenade pickup specifically, use `Supply Drop (AL Grenade)` below — the
bare `Grenade` template resolves to the thrown projectile entity, not an inventory item).

> **On "Blanco" and other shop names.** The fancy in-game shop/display names are **localized
> strings in the stringdb**, mapped onto these generic template names — they are *not* the template
> names and won't resolve via `GetGuidByName`. ("Blanco" itself is the PmcCon002 mission NPC, not a
> weapon.) Use the generic names below to spawn/give a weapon.

Every name below is **confirmed** — live spawn-tested (`Pg.Spawn`'d as a ground pickup, one at a
time) and verified to actually drop. For the broader weapon-adjacent template list — including
untested names, vehicle-mounted-weapon variants, and entries that turned out not to be pickups at
all (projectile/ammo entities, NPC archetype names) — see [Hash Lookup](../hash-lookup).

<div class="hash-lookup-wrap" markdown="0">
<input type="text" id="hashLookupFilter" class="hash-lookup-search" placeholder="Filter weapons..." autocomplete="off">
<div class="hash-lookup-count" id="hashLookupCount"></div>
<div class="hash-lookup-scroll">
<table class="hash-lookup-table" id="hashLookupTable">
<thead>
<tr><th>Name</th><th>Template key</th></tr>
</thead>
<tbody>
<tr><td>Anti-Material Rifle</td><td>0x80006EAB</td></tr>
<tr><td>Anti-Material Rifle (KSVK)</td><td>0x80006EB3</td></tr>
<tr><td>Assault Rifle</td><td>0x8000436F</td></tr>
<tr><td>AT Rocket</td><td>0x80006B58</td></tr>
<tr><td>Automatic Rifle</td><td>0x80006B6A</td></tr>
<tr><td>Bullpup Rifle</td><td>0x80006881</td></tr>
<tr><td>C4</td><td>0x80005FD3</td></tr>
<tr><td>Carbine</td><td>0x80007212</td></tr>
<tr><td>Cheat RPG</td><td>0x8000A26B</td></tr>
<tr><td>Combat Rifle</td><td>0x80006878</td></tr>
<tr><td>Covert Pistol</td><td>0x80006B65</td></tr>
<tr><td>Covert SMG</td><td>0x80006B67</td></tr>
<tr><td>Fuel-Air RPG</td><td>0x80006ED0</td></tr>
<tr><td>Grenade Launcher</td><td>0x80006EA4</td></tr>
<tr><td>Grenade Launcher PEP</td><td>0x8000AED3</td></tr>
<tr><td>Hunting Pistol</td><td>0x80006ECE</td></tr>
<tr><td>Light MG</td><td>0x8000569E</td></tr>
<tr><td>Machine Pistol</td><td>0x80006B53</td></tr>
<tr><td>Machine Pistol (PP2000)</td><td>0x80007213</td></tr>
<tr><td>Machine Pistol (TMP)</td><td>0x80006B57</td></tr>
<tr><td>Machine Pistol (Uzi)</td><td>0x80006B59</td></tr>
<tr><td>Minigun</td><td>0x80008449</td></tr>
<tr><td>Minigun 1000</td><td>0x8000A25C</td></tr>
<tr><td>Pistol</td><td>0x80006B45</td></tr>
<tr><td>Pistol (AL)</td><td>0x80009B15</td></tr>
<tr><td>Pistol (CH)</td><td>0x80009B13</td></tr>
<tr><td>Pistol (GR)</td><td>0x80009B14</td></tr>
<tr><td>Pistol (silver)</td><td>0x8000508E</td></tr>
<tr><td>rifle</td><td>0x800056AC</td></tr>
<tr><td>RPG</td><td>0x8000437B</td></tr>
<tr><td>rpglauncher</td><td>0x800056AB</td></tr>
<tr><td>Shotgun</td><td>0x8000569D</td></tr>
<tr><td>smg</td><td>0x80006B54</td></tr>
<tr><td>Sniper Rifle</td><td>0x8000569A</td></tr>
<tr><td>Sniper Rifle (AA Backup)</td><td>0x8000B036</td></tr>
<tr><td>Sniper Rifle (SVD)</td><td>0x80006B43</td></tr>
<tr><td>Supply Drop (AL Grenade)</td><td>0x8000AE08</td></tr>
<tr><td>Supply Drop (C4)</td><td>0x8000721E</td></tr>
<tr><td>Supply Drop (C4) (VZ)</td><td>0x80008567</td></tr>
<tr><td>Supply Drop (Guerilla) (Sniper)</td><td>0x80008563</td></tr>
<tr><td>Supply Drop (Light MG)</td><td>0x80007221</td></tr>
<tr><td>Supply Drop (Light MG) (AL)</td><td>0x8000A259</td></tr>
<tr><td>Supply Drop (RPG)</td><td>0x8000AF6F</td></tr>
<tr><td>Supply Drop (Sniper CH)</td><td>0x8000AF67</td></tr>
<tr><td>Supply Drop (Sniper RU)</td><td>0x8000AF68</td></tr>
<tr><td>Supply Drop (Sniper)</td><td>0x8000721D</td></tr>
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
