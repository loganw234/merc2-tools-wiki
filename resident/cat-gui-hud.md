---
title: GUI & HUD
parent: Resident Modules
nav_order: 5
has_children: true
has_toc: false
---

# GUI & HUD

The Scaleform-backed GUI/HUD toolkit: widget base classes, HUD elements (ammo counter, radar, objective tray, ...), menus, and screen layouts. `MrxGuiBase` is the foundation almost every page here inherits from or imports.

## Modules in this category

- **[MrxGui](mrxgui)** — The `MrxGui` module serves as a facade/alias for the Scaleform-based GUI/HUD system in Mercenaries 2.
- **[MrxGuiAttractLayout](mrxguiattractlayout)** — The `MrxGuiAttractLayout` module defines the layout and initialization of a GUI attract mode screen.
- **[MrxGuiAttractMode](mrxguiattractmode)** — The `MrxGuiAttractMode` module is responsible for managing the attract mode screen in the game.
- **[MrxGuiBase](mrxguibase)** — The `MrxGuiBase` module is a foundational component for managing graphical user interface (GUI) elements in the game.
- **[MrxGuiBinoculars](mrxguibinoculars)** — The `MrxGuiBinoculars` module manages the behavior of the binoculars GUI in the game.
- **[MrxGuiBootstrap](mrxguibootstrap)** — The `MrxGuiBootstrap` module is responsible for initializing and managing the Scaleform GUI/HUD system in the game.
- **[MrxGuiCinematic](mrxguicinematic)** — The `MrxGuiCinematic` module is responsible for managing the display of cinematic movies and subtitles within the game's GUI.
- **[MrxGuiCinematicLayout](mrxguicinematiclayout)** — The `MrxGuiCinematicLayout` module is responsible for managing the layout and initialization of widgets used in cinematic sequences within the game.
- **[MrxGuiDialogBox](mrxguidialogbox)** — The `MrxGuiDialogBox` module is responsible for creating and managing graphical user interface (GUI) dialog boxes in the game.
- **[MrxGuiGarage](mrxguigarage)** — The `MrxGuiGarage` module is responsible for managing the garage screen in the game's user interface.
- **[MrxGuiHudActionHijack](mrxguihudactionhijack)** — The `MrxGuiHudActionHijack` module is responsible for managing the action hijack HUD elements in the game.
- **[MrxGuiHudAmmoCountersNew](mrxguihudammocountersnew)** — The `MrxGuiHudAmmoCountersNew` module is responsible for managing the display and animation of ammo counters in the HUD.
- **[MrxGuiHudDamageIndicator](mrxguihuddamageindicator)** — The `MrxGuiHudDamageIndicator` module is responsible for displaying directional "took damage" fading arcs on the HUD, centered on the reticle widget.
- **[MrxGuiHudFactionBuffer](mrxguihudfactionbuffer)** — The `MrxGuiHudFactionBuffer` module is a manager for up to two on-screen faction gauges.
- **[MrxGuiHudFactionGauge](mrxguihudfactiongauge)** — The `MrxGuiHudFactionGauge` module is responsible for managing the graphical representation of faction gauges in the game's HUD.
- **[MrxGuiHudHealthCounter](mrxguihudhealthcounter)** — The `MrxGuiHudHealthCounter` module is responsible for managing the health counter display on the HUD.
- **[MrxGuiHudMelee](mrxguihudmelee)** — The `MrxGuiHudMelee` module is responsible for managing the melee and context-action HUD prompts in the game.
- **[MrxGuiHudMessage](mrxguihudmessage)** — The `MrxGuiHudMessage` module is responsible for managing various types of HUD messages and fanfares in the game.
- **[MrxGuiHudObjectiveTray](mrxguihudobjectivetray)** — The `MrxGuiHudObjectiveTray` module is responsible for managing a 3-slot vertical tray on the HUD that can display text or image objective entries.
- **[MrxGuiHudRadar](mrxguihudradar)** — The `MrxGuiHudRadar` module is responsible for managing the minimap and its various components such as faction-zone region overlays, GPS markers, target markers, and map-label flashes.
- **[MrxGuiHudResourceCounter](mrxguihudresourcecounter)** — The `MrxGuiHudResourceCounter` module is responsible for managing and displaying a resource counter on the HUD.
- **[MrxGuiHudReticle](mrxguihudreticle)** — The `MrxGuiHudReticle` module is responsible for managing the various types of reticles used in the game's heads-up display (HUD).
- **[MrxGuiHudSupportMenu](mrxguihudsupportmenu)** — The `MrxGuiHudSupportMenu` module is responsible for managing the in-game HUD support menu.
- **[MrxGuiHudVehicleDisguise](mrxguihudvehicledisguise)** — The `MrxGuiHudVehicleDisguise` module is responsible for managing the vehicle disguise display on the HUD.
- **[MrxGuiInterface](mrxguiinterface)** — The `MrxGuiInterface` module is a comprehensive interface for managing various aspects of the game's user interface (UI), including the Heads-Up Display (HUD) and the Personal Digital Assistant (PDA).
- **[MrxGuiLoadLayout](mrxguiloadlayout)** — The `MrxGuiLoadLayout` module is responsible for defining and managing the layout of the loading screen GUI.
- **[MrxGuiLoadScreen](mrxguiloadscreen)** — The `MrxGuiLoadScreen` module is responsible for managing the loading screen GUI in the game.
- **[MrxGuiLTIPrecache](mrxguiltiprecache)** — The `MrxGuiLTIPrecache` module is responsible for managing the pre-cache loading screen in the game.
- **[MrxGuilTiprecachelayout](mrxguiltiprecachelayout)** — The `MrxGuilTiprecachelayout` module defines a layout for a GUI widget used in the game's interface.
- **[MrxGuiManager](mrxguimanager)** — The `MrxGuiManager` module is responsible for managing the creation, duplication, and lifecycle of various GUI layouts in the game.
- **[MrxGuiNumericBox](mrxguinumericbox)** — The `MrxGuiNumericBox` module is responsible for creating and managing a numeric input box GUI widget.
- **[MrxGuiPauseLayout](mrxguipauselayout)** — The `MrxGuiPauseLayout` module is responsible for managing the layout and behavior of the pause screen in the game.
- **[MrxGuiPauseScreen](mrxguipausescreen)** — The `MrxGuiPauseScreen` module is responsible for managing the pause screen in the game.
- **[MrxGuiPda](mrxguipda)** — The `MrxGuiPda` module is responsible for managing the Player Data Assistant (PDA) interface in the game.
- **[MrxGuiSatellite](mrxguisatellite)** — The `MrxGuiSatellite` module is responsible for managing the satellite GUI overlay in the game.
- **[mrxguishell](mrxguishell)** — The `mrxguishell` module is responsible for managing the GUI shell in the game.
- **[MrxGuiShellBootstrap](mrxguishellbootstrap)** — The `MrxGuiShellBootstrap` module is responsible for managing the loading and display of various GUI layouts in the game's front-end, including the main shell interface, precache screen, and attract/cinematic screens.
- **[MrxGuiShellLayout](mrxguishelllayout)** — The `MrxGuiShellLayout` module defines the layout and event handling for a GUI shell in the game.
- **[MrxGuiSniperscope](mrxguisniperscope)** — The `MrxGuiSniperscope` module is responsible for managing the sniper scope GUI elements in the game.
- **[MrxGuiSupportShop](mrxguisupportshop)** — The `MrxGuiSupportShop` module is responsible for managing the in-game support shop interface.
- **[MrxGuiTextBuffer](mrxguitextbuffer)** — The `MrxGuiTextBuffer` module is responsible for managing text buffers in the game's GUI system.
- **[mrxguitutorial](mrxguitutorial)** — The `mrxguitutorial` module is responsible for managing in-game tutorials that guide players through various game elements.
- **[MrxMultipageMenu](mrxmultipagemenu)** — The `MrxMultipageMenu` module is responsible for managing a paginated menu system in the game's user interface.
