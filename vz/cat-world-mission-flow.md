---
title: World & Mission Flow
parent: VZ Modules
nav_order: 9
has_children: true
has_toc: false
---

# World & Mission Flow

The core, non-faction-specific data and flow modules that tie a level together: save/load
(`wifbriefingdata.lua`, `wifmissiondata.lua`), the PMC HQ/garage/interior systems
(`wifhqdata.lua`, `wifpmcgarage.lua`, `wifpmcinterior.lua`), starter/recommendation/equipment data,
freeplay/hints (`wiffreeplay.lua`, `wifhints.lua`), world ambience/boundary data, and
[`xQ!L`](xql) — the boot-time streaming/save-load conductor everything else here ultimately routes
through. 18 files total.

## Modules in this category

- **[WifBios](wifbios)** — `WifBios` tracks which character/faction dossier entries the player has unlocked for the in-game PDA database, and holds the static text (title/body/icon key) for each of the game's 22 named dossiers plus a default placeholder.
- **[WifBriefingData](wifbriefingdata)** — `wifbriefingdata.lua` is 16,445 lines long and almost none of it is logic — confirmed by grep, the entire file contains exactly two functions (`GetIntroIdByIndex`, `GetIntroIndexById`) and no `import()`/`inherit()` at all.
- **[WifCheatStockpile](wifcheatstockpile)** — `WifCheatStockpile` is a flat lookup table of "expected resources at this point in the campaign" — support charges, equipment, cash, and fuel — keyed directly by mission id.
- **[WifEquipmentData](wifequipmentdata)** — `WifEquipmentData` is the static registry of purchasable/ownable PMC equipment — 14 numbered fuel tanks plus the grappling hook — along with per-faction unlock-state tracking (new/viewed) layered directly onto that same table at runtime.
- **[WifFreePlay](wiffreeplay)** — `WifFreePlay` is Fiona's freeplay "idle nag" system — a repeating, self-rescheduling timer that, once armed, periodically checks whether the player is idling in freeplay with an available hint queued up, and if so, plays a short VO line prompting them to go check it out.
- **[WifHints](wifhints)** — `WifHints` is the contextual "ambient VO hint" system for the game's four commentary characters (Fiona, Ewan, Eva, Misha) — a static pool of one-off VO lines per speaker, each optionally gated by a faction-attitude condition, plus per-speaker "currently active/unlocked" queues that story/mission code adds to and removes from as the campaign progresses.
- **[WifHqData](wifhqdata)** — `WifHqData` is the static per-HQ/outpost configuration table for every faction base in the game — interior template, portal/entrance points, PDA and radar icon sets, atmosphere, landing zone, and parking lot — plus three small getter/index functions.
- **[WifMissionData](wifmissiondata)** — `WifMissionData` is the game's native mission/contract registry — a single large table (`tMissionData`) with one entry per contract or job across every faction (69 entries total), giving each a stable identity, unlock/starter wiring, a critical-path flag, milestone thresholds for repeatable "job" types, and PDA/journal display metadata.
- **[WifMissionFlow](wifmissionflow)** — `WifMissionFlow` is the single-player campaign's critical-path controller — a save-driven "key" graph where completing one contract awards a key, which satisfies another entry's prerequisite, which runs that entry's consequence (unlock the next contract(s), play a cutscene, swap world-state layers, grant an achievement, adjust Fiona's hint pool, and so on).
- **[WifPmcGarage](wifpmcgarage)** — `WifPmcGarage` manages the player's PMC-HQ vehicle storage across three physical regions — the garage (cars/tanks), the helipad (helicopters), and the dock (boats).
- **[WifPmcInterior](wifpmcinterior)** — The PMC HQ job-board/menu system — the indoor space the player teleports into to see the four PMC-faction starters, pick a contract, change outfits, and check owned support-item stock.
- **[WifRecommendationData](wifrecommendationdata)** — A static per-mission "recommended loadout" catalog — for about 25 contracts across every faction, a small table of support-item id -> suggested quantity (e.g.
- **[WifStarterData](wifstarterdata)** — The static per-faction catalog of every "starter" NPC in the game — the mission-giving character standing at each faction HQ/outpost who hands out that faction's contracts (distinct from the four PMC-specific bosses, whose runtime behavior lives in [`WifPmcInterior`](wifpmcinterior) but whose catalog entries are still defined here alongside everyone else's). ~30 entries total: 5 for Allied Nation, 5 for China, 5 for Guerilla, 6 for Oil Company, 3 for Pirates, plus the Jet/Mec recruitment bosses and the four PMC starters.
- **[WifVzAmbience](wifvzambience)** — A small, generic boundary-triggered ambient-sound-cue system: cross into a named world boundary volume and it cues an ambience sound stream; cross back out and it stops that stream.
- **[WifVzAtmosphere](wifvzatmosphere)** — Drives the open-world sky/weather preset (`Graphics.Atmosphere.SetSky`) based on which named atmosphere boundary region the local player is currently standing inside — e.g. an underground cave gets an `"afternoon"` sky override, Caracas gets its own `"Maracaibo"` preset, and leaving every configured region reverts to a hardcoded default.
- **[WifVzBoundary](wifvzboundary)** — Owns the single "world boundary" that fences the player into whatever portion of the map the story has currently unlocked — the invisible wall (plus a Fiona-voiced warning line and static/radio noise) that keeps you from wandering into content you haven't reached yet.
- **[WifVzRegionNames](wifvzregionnames)** — Despite the filename, this isn't a plain name/label lookup table — it's the point-of-interest (POI) system that shows a map-label popup (`Hud.MapLabel`) the first time the player enters any of ~38 named world regions (Caracas, Maracaibo, Angel Falls, the various faction HQs, etc.), and for about half of them, plays one of Fiona's one-time descriptive VO lines the first time you arrive.
- **[xQ!L](xql)** — The game's boot-time streaming/save-load conductor — the single module that decides what a new session actually boots into (a fresh campaign start, a loaded save, a checkpoint retry, or a debug mission-skip), drives the whole level-streaming handshake from "nothing loaded" to "player has control," and owns the master save-data table that every other persisted subsystem's own `SaveSingleton`/`LoadSingleton` feeds into.
