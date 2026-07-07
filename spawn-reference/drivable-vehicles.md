---
title: Drivable Vehicles
parent: Spawn Reference
nav_order: 1
---

# Drivable Vehicles

The `is_vehicle=1` set with the obvious non-vehicles removed (particles, spawn-lists,
path-spawners, mounted guns, seats, wrecks/debris) and variants collapsed to their base family —
the shortlist to actually try driving. Spawn with `Pg.Spawn("<name>", x, y, z)`.

**Variants** counts how many source rows share that base name (driver / full / jammer / faction
skins); the full per-variant list is on [All Vehicles](all-vehicles). Boats need water under the
spawn point.

> **Boat caveat.** This page is filtered from `is_vehicle=1`, and several real boats — `LCUR`,
> `MarkV`, `Cutter`, `Barco` — are flagged `is_vehicle=0` in the source export, so they are **not
> listed here**. Find them via [Hash Lookup](../hash-lookup). Boats that *are* here (flagged
> correctly): `Huangfeng`, `Patrol Boat`, `Piranha`, `Dinghy`, `Speed Boat`, `Fishing Boat`,
> `Air Boat`, `Salton Seahorse`, `Cargo Ship`, `Oil Tanker`, both `Destroyer`s.

<div class="hash-lookup-wrap" markdown="0">
<input type="text" id="hashLookupFilter" class="hash-lookup-search" placeholder="Filter drivable vehicles..." autocomplete="off">
<div class="hash-lookup-count" id="hashLookupCount"></div>
<div class="hash-lookup-scroll">
<table class="hash-lookup-table" id="hashLookupTable">
<thead>
<tr><th>Name</th><th>Template key</th><th>Variants</th></tr>
</thead>
<tbody>
<tr><td>AH1Z</td><td>0x800075DB</td><td>4</td></tr>
<tr><td>Air Boat</td><td>0x80008FF8</td><td>5</td></tr>
<tr><td>Airboat</td><td>0x8000A40E</td><td>1</td></tr>
<tr><td>Allied Destroyer</td><td>0x80008EF8</td><td>3</td></tr>
<tr><td>Alouette 3 Transport</td><td>0x800081FE</td><td>1</td></tr>
<tr><td>Alouette3</td><td>0x80006CC3</td><td>1</td></tr>
<tr><td>Alouette3 Attack</td><td>0x80008227</td><td>9</td></tr>
<tr><td>Alouette3 Elite</td><td>0x80008228</td><td>4</td></tr>
<tr><td>Alouette3 Superiority</td><td>0x80006CC4</td><td>3</td></tr>
<tr><td>Alouette3 SuperiorityElite</td><td>0x8000946E</td><td>1</td></tr>
<tr><td>Alouette3 Transport</td><td>0x800081FC</td><td>12</td></tr>
<tr><td>Ambulance</td><td>0x800085C2</td><td>5</td></tr>
<tr><td>AMX30</td><td>0x80007255</td><td>4</td></tr>
<tr><td>Amx30</td><td>0x80007254</td><td>1</td></tr>
<tr><td>AMX30 AA</td><td>0x80007257</td><td>2</td></tr>
<tr><td>AMX30 Elite</td><td>0x80007256</td><td>3</td></tr>
<tr><td>AMX30_RUIN</td><td>0x800092C7</td><td>1</td></tr>
<tr><td>APC</td><td>0x80008758</td><td>1</td></tr>
<tr><td>APC_Passenger</td><td>0x8000A421</td><td>1</td></tr>
<tr><td>Boat</td><td>0x8000638E</td><td>1</td></tr>
<tr><td>Buggy</td><td>0x80004730</td><td>5</td></tr>
<tr><td>BuggyPR</td><td>0x8000A452</td><td>1</td></tr>
<tr><td>Cargo Ship</td><td>0x80008EFC</td><td>1</td></tr>
<tr><td>Chinese Destroyer</td><td>0x80008EFA</td><td>3</td></tr>
<tr><td>Chopper</td><td>0x80008215</td><td>4</td></tr>
<tr><td>Civ Motorcycle</td><td>0x800082FF</td><td>1</td></tr>
<tr><td>Coanda</td><td>0x800063BF</td><td>1</td></tr>
<tr><td>Coanda Attack</td><td>0x80009478</td><td>4</td></tr>
<tr><td>Coanda Gunship</td><td>0x800063C0</td><td>5</td></tr>
<tr><td>Coanda Superiority</td><td>0x80009479</td><td>4</td></tr>
<tr><td>Coanda Transport</td><td>0x800081F9</td><td>6</td></tr>
<tr><td>CRX</td><td>0x80009FC3</td><td>1</td></tr>
<tr><td>Destroyer</td><td>0x8000AABE</td><td>1</td></tr>
<tr><td>Dinghy</td><td>0x800075DF</td><td>5</td></tr>
<tr><td>F35b</td><td>0x80006CAF</td><td>2</td></tr>
<tr><td>Fishing Boat</td><td>0x80008F22</td><td>5</td></tr>
<tr><td>FishingBoat</td><td>0x8000A412</td><td>1</td></tr>
<tr><td>Garbage Truck</td><td>0x800081D3</td><td>4</td></tr>
<tr><td>Guntruck</td><td>0x800063A9</td><td>5</td></tr>
<tr><td>GuntruckOC</td><td>0x8000A977</td><td>1</td></tr>
<tr><td>Helicopter</td><td>0x800063A3</td><td>1</td></tr>
<tr><td>Huangfeng</td><td>0x80008B65</td><td>4</td></tr>
<tr><td>HuangFeng</td><td>0x8000A426</td><td>1</td></tr>
<tr><td>Humvee</td><td>0x800085FD</td><td>1</td></tr>
<tr><td>Ka29b</td><td>0x8000769A</td><td>10</td></tr>
<tr><td>L300</td><td>0x80009CBD</td><td>1</td></tr>
<tr><td>Lav</td><td>0x8000A40B</td><td>1</td></tr>
<tr><td>LAV III</td><td>0x80008539</td><td>1</td></tr>
<tr><td>LAVIII</td><td>0x800085B5</td><td>20</td></tr>
<tr><td>M113</td><td>0x800075EA</td><td>11</td></tr>
<tr><td>M113 AA</td><td>0x800081ED</td><td>8</td></tr>
<tr><td>M113 Jammer</td><td>0x80008246</td><td>3</td></tr>
<tr><td>M113 Transport</td><td>0x800081EA</td><td>1</td></tr>
<tr><td>M151</td><td>0x80006A23</td><td>7</td></tr>
<tr><td>M151 .50Cal</td><td>0x800076B4</td><td>4</td></tr>
<tr><td>M151 Softtop</td><td>0x80006C97</td><td>7</td></tr>
<tr><td>M151_Ruin</td><td>0x900001F6</td><td>1</td></tr>
<tr><td>M1A2</td><td>0x800074C0</td><td>4</td></tr>
<tr><td>M2A3</td><td>0x800074C4</td><td>3</td></tr>
<tr><td>M35</td><td>0x8000892E</td><td>31</td></tr>
<tr><td>M35 Truck</td><td>0x800085B8</td><td>1</td></tr>
<tr><td>M35_Ruin</td><td>0x900001F7</td><td>1</td></tr>
<tr><td>M551</td><td>0x800075CE</td><td>3</td></tr>
<tr><td>Mattias Chopper</td><td>0x80008F21</td><td>1</td></tr>
<tr><td>MH53J</td><td>0x800092C5</td><td>7</td></tr>
<tr><td>Mi26</td><td>0x80006CD1</td><td>11</td></tr>
<tr><td>Mi35</td><td>0x80008531</td><td>10</td></tr>
<tr><td>Monster Truck</td><td>0x80006C99</td><td>2</td></tr>
<tr><td>Monster truck phase1</td><td>0x8000875C</td><td>1</td></tr>
<tr><td>Monster truck phase2</td><td>0x8000875D</td><td>1</td></tr>
<tr><td>Monster truck test</td><td>0x800085AA</td><td>1</td></tr>
<tr><td>Motorcycle</td><td>0x80008F1F</td><td>2</td></tr>
<tr><td>MotorcycleOld</td><td>0x80009D61</td><td>1</td></tr>
<tr><td>MotorCycleTest</td><td>0x80004E28</td><td>1</td></tr>
<tr><td>Offroad Motorcycle</td><td>0x8000A44D</td><td>5</td></tr>
<tr><td>OffroadMotorcycle</td><td>0x8000A979</td><td>1</td></tr>
<tr><td>Ofroad Motorcycle</td><td>0x8000637E</td><td>1</td></tr>
<tr><td>Oil Tanker</td><td>0x80008EFB</td><td>1</td></tr>
<tr><td>Patrol Boat</td><td>0x80009FF3</td><td>7</td></tr>
<tr><td>Patrolboat</td><td>0x8000A416</td><td>1</td></tr>
<tr><td>PatrolboatVZ</td><td>0x8000A427</td><td>1</td></tr>
<tr><td>PGZ95</td><td>0x80007265</td><td>3</td></tr>
<tr><td>PGZ95 Command</td><td>0x80007266</td><td>2</td></tr>
<tr><td>Phoenix</td><td>0x80009DFC</td><td>1</td></tr>
<tr><td>Piranha</td><td>0x800075D9</td><td>5</td></tr>
<tr><td>PLZ45</td><td>0x80007268</td><td>3</td></tr>
<tr><td>Police Helicopter</td><td>0x80006CA3</td><td>3</td></tr>
<tr><td>PR buggy</td><td>0x8000AC5D</td><td>1</td></tr>
<tr><td>RTR</td><td>0x80009E02</td><td>1</td></tr>
<tr><td>Salton Seahorse</td><td>0x80009003</td><td>8</td></tr>
<tr><td>Scorpion90</td><td>0x80006CAE</td><td>4</td></tr>
<tr><td>Sidecar Motorcycle</td><td>0x800085EB</td><td>3</td></tr>
<tr><td>SideCarMotorcycle</td><td>0x8000A97A</td><td>1</td></tr>
<tr><td>Small Fishing Boat</td><td>0x800075DE</td><td>4</td></tr>
<tr><td>SmallFishingBoat</td><td>0x8000A480</td><td>1</td></tr>
<tr><td>Speed Boat</td><td>0x80006A22</td><td>7</td></tr>
<tr><td>Sportbike</td><td>0x80009CC6</td><td>1</td></tr>
<tr><td>Stingray II</td><td>0x800038B2</td><td>5</td></tr>
<tr><td>Support Vehicle</td><td>0x800085D9</td><td>6</td></tr>
<tr><td>Tank</td><td>0x8000638A</td><td>1</td></tr>
<tr><td>Tank Bike</td><td>0x800085DE</td><td>1</td></tr>
<tr><td>TankBike</td><td>0x8000A978</td><td>1</td></tr>
<tr><td>Transport Truck</td><td>0x800060B7</td><td>4</td></tr>
<tr><td>TransportTruck</td><td>0x8000A401</td><td>1</td></tr>
<tr><td>UH1</td><td>0x800063A5</td><td>1</td></tr>
<tr><td>UH1 Attack</td><td>0x800081C8</td><td>5</td></tr>
<tr><td>UH1 Elite</td><td>0x800081CB</td><td>1</td></tr>
<tr><td>UH1 Superiority</td><td>0x800081C9</td><td>1</td></tr>
<tr><td>UH1 Transport</td><td>0x800063A8</td><td>14</td></tr>
<tr><td>Van</td><td>0x80009E11</td><td>1</td></tr>
<tr><td>Vehicle AT Missile</td><td>0x8000AAC1</td><td>1</td></tr>
<tr><td>Wheel WZ551</td><td>0x80006F74</td><td>6</td></tr>
<tr><td>WZ551</td><td>0x80006F73</td><td>5</td></tr>
<tr><td>ZTZ63a</td><td>0x8000725C</td><td>4</td></tr>
<tr><td>ZTZ98</td><td>0x80006CC8</td><td>3</td></tr>
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
