---
title: Spawn Reference
nav_order: 13
has_children: true
has_toc: false
---

# Spawn Reference

Name → spawn-key reference for the two engine calls you drive by *name*:
`Pg.Spawn("<name>", x, y, z[, yaw])` to spawn a template, and
`Pg.GetGuidByName("<name>")` to resolve an existing/template entity (how the shipped
scripts hand a character a weapon: `Human.Inventory.SetAllWeapons(uChar, { w })`).

These are the spawn-oriented companion to [Hash Lookup](../hash-lookup) — that page is the
complete 6119-row name→hash table (every asset, spawnable or not); the pages here are
filtered, task-focused slices. The full template list itself already lives on Hash Lookup, so
it isn't duplicated here.

**Provenance / caveats.** Names and keys come from the same `spawnable_templates.csv` export
behind Hash Lookup, cross-referenced against real `Pg.Spawn` / `Pg.GetGuidByName` call sites in
the decompiled scripts. They're **static-derived — cross-referenced, not each individually
live-tested** — except [Weapons](weapons), which is trimmed to only the subset actually
`Pg.Spawn`'d in-game and confirmed to drop as a pickup. One known data-quality gotcha: the
export's `is_vehicle` flag is unreliable for
watercraft — `LCUR`, `MarkV`, `Cutter`, and `Barco` are all flagged `is_vehicle=0` despite being
drivable boats — so the vehicle pages (built from that flag) miss some boats. For boats,
cross-check the full table on Hash Lookup.

The **Template key** column is the export's `value_hex` (the `0x8000XXXX`-shaped entity/template
key), shown here because it's the spawn-relevant key and complements Hash Lookup's name-hash column.

## Pages

| Page | Rows | What |
|---|---|---|
| [Drivable Vehicles](drivable-vehicles) | 115 | Curated, junk-filtered, variant-collapsed — the shortlist to actually drive |
| [All Vehicles](all-vehicles) | 1060 | Every `is_vehicle=1` template (variants + some non-drivable noise) |
| [Weapons](weapons) | 46 | Confirmed spawnable weapon templates (live-tested), given via `SetAllWeapons` |
| [Pg.Spawn Call Sites](pg-spawn-calls) | 76 | Every string the shipped scripts actually pass to `Pg.Spawn` / `SpawnOrdnance` |
| [Names Resolved by Name](getguidbyname) | 556 | Every `Pg.GetGuidByName` string — weapons, NPCs, vehicles, level locations |

