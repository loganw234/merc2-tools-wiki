---
title: Names Resolved by Name
parent: Spawn Reference
nav_order: 5
---

# Names Resolved by Name

Every distinct string passed to `Pg.GetGuidByName(...)` in the decompiled scripts — the names the
game resolves to already-placed or template entities: weapons (given via `SetAllWeapons`), named
NPCs, vehicles, and level locations.

**Template** means the name is in the spawn-template export (a real template you can also
`Pg.Spawn`, key shown); **level-instance** means it's a placed-object name that only exists inside
a specific loaded mission/layer (a trailing `0x…` instance id was stripped for readability, and the
name only resolves while that layer is loaded).

<div class="hash-lookup-wrap" markdown="0">
<input type="text" id="hashLookupFilter" class="hash-lookup-search" placeholder="Filter names..." autocomplete="off">
<div class="hash-lookup-count" id="hashLookupCount"></div>
<div class="hash-lookup-scroll">
<table class="hash-lookup-table" id="hashLookupTable">
<thead>
<tr><th>Name</th><th>Template key / kind</th></tr>
</thead>
<tbody>
<tr><td>01_pmc_hq_lz_playerone</td><td>level-instance</td></tr>
<tr><td>01_pmc_hq_parking</td><td>level-instance</td></tr>
<tr><td>1stmine</td><td>level-instance</td></tr>
<tr><td>\t</td><td>level-instance</td></tr>
<tr><td>_caracas_bld_historical04</td><td>0x80006EEB</td></tr>
<tr><td>_cumana_bld_corner32x32B</td><td>0x80009C30</td></tr>
<tr><td>_DLC_vzoutpost_bld_guardtower</td><td>level-instance</td></tr>
<tr><td>_global_bencha</td><td>0x80004CEF</td></tr>
<tr><td>_global_soccergoal</td><td>0x80008120</td></tr>
<tr><td>_industrial_att_pipelargeshort</td><td>0x80006899</td></tr>
<tr><td>_maracaibo_bridge_segmenta</td><td>0x8000691B</td></tr>
<tr><td>_maracaibo_bridge_segmentb</td><td>0x8000691F</td></tr>
<tr><td>_merida_bld_lockerroom</td><td>0x80005105</td></tr>
<tr><td>_merida_bld_lockerroom 0</td><td>level-instance</td></tr>
<tr><td>_merida_bld_mediabooth</td><td>0x800055F0</td></tr>
<tr><td>_merida_bld_oilwellland</td><td>0x80004EFB</td></tr>
<tr><td>_merida_bld_plazachurch 0</td><td>level-instance</td></tr>
<tr><td>_merida_bld_universitycampus</td><td>0x80004DEA</td></tr>
<tr><td>_merida_bld_universitydorm</td><td>0x80004DEB</td></tr>
<tr><td>_merida_bld_universitydorm 0</td><td>level-instance</td></tr>
<tr><td>_merida_bld_universitylibrary 1</td><td>level-instance</td></tr>
<tr><td>_ocoutpost_bld_hq</td><td>0x80007018</td></tr>
<tr><td>_ocoutpost_wallgate</td><td>0x800076D8</td></tr>
<tr><td>_pmcoutpost_bld_hq_livedin</td><td>0x900001DD</td></tr>
<tr><td>_Pmcoutpost_bld_hq_livedin_pmccon003</td><td>0x8000AFA3</td></tr>
<tr><td>_pmcoutpost_bld_hqsuites</td><td>0x900001DB</td></tr>
<tr><td>_pmcoutpost_column</td><td>0x800076F8</td></tr>
<tr><td>_pmcoutpost_shootinggallerytarget01</td><td>0x8000A94D</td></tr>
<tr><td>_port_crane01</td><td>0x80005C37</td></tr>
<tr><td>_vzoutpost_bld_barrackbunker</td><td>0x80008779</td></tr>
<tr><td>_vzoutpost_bld_barracktent</td><td>0x80008777</td></tr>
<tr><td>activateActionHijack_Lineregion</td><td>level-instance</td></tr>
<tr><td>AllCon008_SpawnCopter01</td><td>level-instance</td></tr>
<tr><td>AllCon008_SpawnCopter02</td><td>level-instance</td></tr>
<tr><td>Allied</td><td>0x80002CF0</td></tr>
<tr><td>AllJob001_02_Outpost</td><td>level-instance</td></tr>
<tr><td>AllJob002_04_Jeep01</td><td>level-instance</td></tr>
<tr><td>Alouette3 Attack (VZ)</td><td>0x8000822A</td></tr>
<tr><td>Alouette3 Elite (Driver)</td><td>0x80008234</td></tr>
<tr><td>Anti-Material Rifle</td><td>0x80006EAB</td></tr>
<tr><td>Arena_01</td><td>level-instance</td></tr>
<tr><td>Assault Rifle</td><td>0x8000436F</td></tr>
<tr><td>BoatBlock_</td><td>level-instance</td></tr>
<tr><td>BoatGunnerMan</td><td>level-instance</td></tr>
<tr><td>BombCar</td><td>level-instance</td></tr>
<tr><td>bottom01</td><td>level-instance</td></tr>
<tr><td>bottom02</td><td>level-instance</td></tr>
<tr><td>brokenbridge_mook</td><td>level-instance</td></tr>
<tr><td>Bunker Buster Projectile</td><td>0x8000845D</td></tr>
<tr><td>C4</td><td>0x80005FD3</td></tr>
<tr><td>Carbine</td><td>0x80007212</td></tr>
<tr><td>Carmona_VzaCon001</td><td>level-instance</td></tr>
<tr><td>CarmonaHeli</td><td>level-instance</td></tr>
<tr><td>CarmonaJeep</td><td>level-instance</td></tr>
<tr><td>CarmonaTarget</td><td>level-instance</td></tr>
<tr><td>CartelBlock_</td><td>level-instance</td></tr>
<tr><td>check0a</td><td>level-instance</td></tr>
<tr><td>check11</td><td>level-instance</td></tr>
<tr><td>check2</td><td>level-instance</td></tr>
<tr><td>check29</td><td>level-instance</td></tr>
<tr><td>check35</td><td>level-instance</td></tr>
<tr><td>ChiCon008_Checkpoint04</td><td>level-instance</td></tr>
<tr><td>ChiCon008_Checkpoint07</td><td>level-instance</td></tr>
<tr><td>ChiCon008_ZTZ98</td><td>level-instance</td></tr>
<tr><td>ChiCon009_ZBD2000</td><td>level-instance</td></tr>
<tr><td>China</td><td>level-instance</td></tr>
<tr><td>ChinaContact</td><td>level-instance</td></tr>
<tr><td>ChinaDriver</td><td>level-instance</td></tr>
<tr><td>ChineseSkirmish2</td><td>level-instance</td></tr>
<tr><td>ChineseSkirmish3</td><td>level-instance</td></tr>
<tr><td>ChineseSkirmish4</td><td>level-instance</td></tr>
<tr><td>Chopper_PmcCon003_Bunker_ApproachEnc01</td><td>level-instance</td></tr>
<tr><td>Civ</td><td>level-instance</td></tr>
<tr><td>Civ_VIP_1</td><td>level-instance</td></tr>
<tr><td>Civ_VIP_2</td><td>level-instance</td></tr>
<tr><td>CliffyA</td><td>level-instance</td></tr>
<tr><td>CliffyB</td><td>level-instance</td></tr>
<tr><td>Combat Rifle</td><td>0x80006878</td></tr>
<tr><td>CommercialBuildingGurcon002</td><td>level-instance</td></tr>
<tr><td>Custom Outfit Location</td><td>level-instance</td></tr>
<tr><td>DisableDBs</td><td>level-instance</td></tr>
<tr><td>DLC_AT Rocket</td><td>level-instance</td></tr>
<tr><td>DLC_Explosion (Daisy Cutter)</td><td>level-instance</td></tr>
<tr><td>dlc_global_particle_airstrike_distance</td><td>level-instance</td></tr>
<tr><td>dlc_global_particle_tracer_AA</td><td>level-instance</td></tr>
<tr><td>DLC_M1A3</td><td>level-instance</td></tr>
<tr><td>DLCCon003_overpass_a</td><td>level-instance</td></tr>
<tr><td>DLCCON004_UberPanhard_01</td><td>level-instance</td></tr>
<tr><td>Dumb Bomb Projectile</td><td>level-instance</td></tr>
<tr><td>Emplaced GL</td><td>0x80006EC8</td></tr>
<tr><td>Emplaced MG</td><td>0x80006B5C</td></tr>
<tr><td>Emplaced Recoiless Rifle</td><td>0x8000844B</td></tr>
<tr><td>Finder_</td><td>level-instance</td></tr>
<tr><td>Fiona</td><td>0x800075E5</td></tr>
<tr><td>Fuel-Air RPG</td><td>0x80006ED0</td></tr>
<tr><td>garage02</td><td>level-instance</td></tr>
<tr><td>Grenade</td><td>0x80002331</td></tr>
<tr><td>Grenade Launcher</td><td>0x80006EA4</td></tr>
<tr><td>Guerilla</td><td>0x80002CF1</td></tr>
<tr><td>Guerilla_Earthmover_Patrol</td><td>level-instance</td></tr>
<tr><td>Guerilla_Moverarm_Patrol</td><td>level-instance</td></tr>
<tr><td>Guerilla_Patrol_FrontOne</td><td>level-instance</td></tr>
<tr><td>Guerilla_Patrol_RoadOne</td><td>level-instance</td></tr>
<tr><td>Guerilla_Patrol_RoadTwo</td><td>level-instance</td></tr>
<tr><td>Guerilla_Trailer_Patrol</td><td>level-instance</td></tr>
<tr><td>GunningBoat</td><td>level-instance</td></tr>
<tr><td>GunPickup</td><td>level-instance</td></tr>
<tr><td>GunPickup_2</td><td>level-instance</td></tr>
<tr><td>gurcon001.barracks.003</td><td>level-instance</td></tr>
<tr><td>gurcon001.barracks.004</td><td>level-instance</td></tr>
<tr><td>gurcon001.barracks.005</td><td>level-instance</td></tr>
<tr><td>gurcon001.barracks.006</td><td>level-instance</td></tr>
<tr><td>gurcon001.barracks.007</td><td>level-instance</td></tr>
<tr><td>gurcon001.barracks.008</td><td>level-instance</td></tr>
<tr><td>gurcon001.barracks.01</td><td>level-instance</td></tr>
<tr><td>GurCon001_Checkpoint</td><td>level-instance</td></tr>
<tr><td>GurCon001_ChurchHoverPath1</td><td>level-instance</td></tr>
<tr><td>GurCon001_ChurchHoverPath2</td><td>level-instance</td></tr>
<tr><td>GurCon001HeloDropPoint1</td><td>level-instance</td></tr>
<tr><td>GurCon001HeloDropPoint2</td><td>level-instance</td></tr>
<tr><td>GurCon002_Soccer_Music_Border</td><td>level-instance</td></tr>
<tr><td>GurCon002HeloPath1</td><td>level-instance</td></tr>
<tr><td>GurCon003_deliv</td><td>level-instance</td></tr>
<tr><td>GurCon003_deliv_2</td><td>level-instance</td></tr>
<tr><td>GurCon003_dest</td><td>level-instance</td></tr>
<tr><td>GurCon3_gate_20</td><td>level-instance</td></tr>
<tr><td>GurCon3_gate_40</td><td>level-instance</td></tr>
<tr><td>GurJob008_02_Outpost</td><td>level-instance</td></tr>
<tr><td>HqInterior</td><td>level-instance</td></tr>
<tr><td>intercom_locked</td><td>level-instance</td></tr>
<tr><td>jail_</td><td>level-instance</td></tr>
<tr><td>jail_11_</td><td>level-instance</td></tr>
<tr><td>JetCon001_AASite01_Jeep_Path</td><td>level-instance</td></tr>
<tr><td>JetCon001_AttackCopter</td><td>level-instance</td></tr>
<tr><td>JetCon001_BeachAssault_Tank01</td><td>level-instance</td></tr>
<tr><td>JetCon001_Bunker</td><td>level-instance</td></tr>
<tr><td>JetCon001_BunkerBuster0</td><td>level-instance</td></tr>
<tr><td>JetCon001_BunkerBuster01</td><td>level-instance</td></tr>
<tr><td>JetCon001_BunkerBuster02</td><td>level-instance</td></tr>
<tr><td>JetCon001_BunkerBuster03</td><td>level-instance</td></tr>
<tr><td>JetCon001_Jeep_BunkerIsland</td><td>level-instance</td></tr>
<tr><td>JetCon001_ScrambleCopter</td><td>level-instance</td></tr>
<tr><td>JetCon001_Supply_AAJeep01</td><td>level-instance</td></tr>
<tr><td>JugPickup_1</td><td>level-instance</td></tr>
<tr><td>JugPickup_2</td><td>level-instance</td></tr>
<tr><td>Ka29b (Driver)</td><td>0x800081FF</td></tr>
<tr><td>Laser Guided Bomb Projectile</td><td>0x80007CD0</td></tr>
<tr><td>LineRegion_Firefights</td><td>level-instance</td></tr>
<tr><td>lnrg_destroybridge1</td><td>level-instance</td></tr>
<tr><td>lnrg_destroybridge2</td><td>level-instance</td></tr>
<tr><td>lnrgn_apcdrop1</td><td>level-instance</td></tr>
<tr><td>lnrgn_apcdrop2</td><td>level-instance</td></tr>
<tr><td>lnrgn_apcdrop3</td><td>level-instance</td></tr>
<tr><td>lnrgn_CompoundMusic</td><td>level-instance</td></tr>
<tr><td>lnrgn_explosion1</td><td>level-instance</td></tr>
<tr><td>lnrgn_explosion2_3</td><td>level-instance</td></tr>
<tr><td>lnrgn_helicheck1</td><td>level-instance</td></tr>
<tr><td>lnrgn_helicheck2</td><td>level-instance</td></tr>
<tr><td>loc_AmbulanceDropoff</td><td>level-instance</td></tr>
<tr><td>loc_AmbulanceRendezvous</td><td>level-instance</td></tr>
<tr><td>loc_ChiCon008_ZTZ98</td><td>level-instance</td></tr>
<tr><td>loc_ChopperDropoff_P1</td><td>level-instance</td></tr>
<tr><td>loc_CliffyA</td><td>level-instance</td></tr>
<tr><td>loc_DeliverStart</td><td>level-instance</td></tr>
<tr><td>loc_DeliverySpot</td><td>level-instance</td></tr>
<tr><td>loc_DeliverySpot_end</td><td>level-instance</td></tr>
<tr><td>loc_EntourageFleePoint</td><td>level-instance</td></tr>
<tr><td>loc_explosion1</td><td>level-instance</td></tr>
<tr><td>loc_explosion2</td><td>level-instance</td></tr>
<tr><td>loc_explosion3</td><td>level-instance</td></tr>
<tr><td>loc_fake_cantina</td><td>level-instance</td></tr>
<tr><td>loc_FireTgt_</td><td>level-instance</td></tr>
<tr><td>loc_FireTgt_Boat</td><td>level-instance</td></tr>
<tr><td>loc_GunDrop</td><td>level-instance</td></tr>
<tr><td>loc_MailDrop</td><td>level-instance</td></tr>
<tr><td>loc_PirCon002deliver</td><td>level-instance</td></tr>
<tr><td>loc_playerStart</td><td>level-instance</td></tr>
<tr><td>LOC_PMC</td><td>level-instance</td></tr>
<tr><td>loc_PmcCon015_RaceCar_MP</td><td>level-instance</td></tr>
<tr><td>loc_PmcCon015_RaceCar_SP</td><td>level-instance</td></tr>
<tr><td>loc_pmccon016_005</td><td>level-instance</td></tr>
<tr><td>loc_PmcCon016_Racer</td><td>level-instance</td></tr>
<tr><td>loc_Rockets_</td><td>level-instance</td></tr>
<tr><td>loc_Rockets_see_</td><td>level-instance</td></tr>
<tr><td>loc_shockwave</td><td>level-instance</td></tr>
<tr><td>Loc_Smoke_</td><td>level-instance</td></tr>
<tr><td>loc_solattack1</td><td>level-instance</td></tr>
<tr><td>loc_solattack2</td><td>level-instance</td></tr>
<tr><td>loc_solattack3</td><td>level-instance</td></tr>
<tr><td>loc_solattack4</td><td>level-instance</td></tr>
<tr><td>loc_SpawnAmbulance</td><td>level-instance</td></tr>
<tr><td>loc_spawnmans</td><td>level-instance</td></tr>
<tr><td>loc_StartOCBoats</td><td>level-instance</td></tr>
<tr><td>loc_VehDisTalk</td><td>level-instance</td></tr>
<tr><td>loc_vza_amxdrop</td><td>level-instance</td></tr>
<tr><td>loc_vza_cardrop</td><td>level-instance</td></tr>
<tr><td>loc_vza_helispawn1</td><td>level-instance</td></tr>
<tr><td>loc_vza_helispawn2</td><td>level-instance</td></tr>
<tr><td>loc_vza_helispawn3</td><td>level-instance</td></tr>
<tr><td>loc_vza_weapondrop</td><td>level-instance</td></tr>
<tr><td>loc_vzAttack</td><td>level-instance</td></tr>
<tr><td>location</td><td>0x80005422</td></tr>
<tr><td>LR_CastleGR2</td><td>level-instance</td></tr>
<tr><td>LR_Church_Abandon</td><td>level-instance</td></tr>
<tr><td>LR_Goal</td><td>level-instance</td></tr>
<tr><td>LR_PMCOOB</td><td>level-instance</td></tr>
<tr><td>LR_TowerBase</td><td>level-instance</td></tr>
<tr><td>LR_VZGurAttack_GC2</td><td>level-instance</td></tr>
<tr><td>LRGurcon001Shore</td><td>level-instance</td></tr>
<tr><td>M113 Jammer (VZ) (Driver)</td><td>0x80008248</td></tr>
<tr><td>M151 .50Cal (VZ) (Full)</td><td>0x800076B5</td></tr>
<tr><td>M35 (Cargo) (VZ) (Full)</td><td>0x8000891C</td></tr>
<tr><td>MailTalk</td><td>level-instance</td></tr>
<tr><td>MailTruck</td><td>level-instance</td></tr>
<tr><td>mc001.bridgeBomb.tigger</td><td>level-instance</td></tr>
<tr><td>mc001.loc.tutorialtrigger</td><td>level-instance</td></tr>
<tr><td>mechanicHQ</td><td>level-instance</td></tr>
<tr><td>mechanicHQ.rgn.inside</td><td>level-instance</td></tr>
<tr><td>mechanicHQ.rgn.outside</td><td>level-instance</td></tr>
<tr><td>Mi35 (AA Driver)</td><td>0x8000AFA2</td></tr>
<tr><td>Mi35 (Solano Hijack)</td><td>level-instance</td></tr>
<tr><td>Monster1</td><td>level-instance</td></tr>
<tr><td>Munitions (Rocket Artillery)</td><td>0x80008E2D</td></tr>
<tr><td>Nuclear Bunker Buster Projectile</td><td>0x8000A258</td></tr>
<tr><td>Obj1_</td><td>level-instance</td></tr>
<tr><td>Obj1_A</td><td>level-instance</td></tr>
<tr><td>Obj1_B</td><td>level-instance</td></tr>
<tr><td>Obj1_C</td><td>level-instance</td></tr>
<tr><td>OBJ_Wave02_APC01</td><td>level-instance</td></tr>
<tr><td>OBJ_Wave02_APC02</td><td>level-instance</td></tr>
<tr><td>OBJ_Wave02_Tank01</td><td>level-instance</td></tr>
<tr><td>OBJ_Wave02_Tank02</td><td>level-instance</td></tr>
<tr><td>OBJ_Wave02_Tank03</td><td>level-instance</td></tr>
<tr><td>OBJ_Wave02_Tank04</td><td>level-instance</td></tr>
<tr><td>OC</td><td>0x800056C5</td></tr>
<tr><td>oc001.loc.finish</td><td>level-instance</td></tr>
<tr><td>oc001.loc.stagedEnc</td><td>level-instance</td></tr>
<tr><td>oc001.loc.stagedExp</td><td>level-instance</td></tr>
<tr><td>oc001.obj1.ocsquad2</td><td>level-instance</td></tr>
<tr><td>oc001.obj1.vzsquad1</td><td>level-instance</td></tr>
<tr><td>oc001.obj2.loc.supplyDrop</td><td>level-instance</td></tr>
<tr><td>oc001.obj3.pth.pipe1</td><td>level-instance</td></tr>
<tr><td>oc001.oc.boatrunner</td><td>level-instance</td></tr>
<tr><td>oc001.pth.rabbit</td><td>level-instance</td></tr>
<tr><td>oc001.pth.ship_patrol</td><td>level-instance</td></tr>
<tr><td>oc001.rgn.boundary</td><td>level-instance</td></tr>
<tr><td>oc001.rgn.warehouse01</td><td>level-instance</td></tr>
<tr><td>oc001_exec</td><td>level-instance</td></tr>
<tr><td>OilCon002_Entrance2Helipad</td><td>level-instance</td></tr>
<tr><td>OilCon002_EpiEwan</td><td>level-instance</td></tr>
<tr><td>OilCon002_EwanHoldingPath</td><td>level-instance</td></tr>
<tr><td>OilCon002_HeliTele</td><td>level-instance</td></tr>
<tr><td>oilcon002_loc_postA</td><td>level-instance</td></tr>
<tr><td>oilcon002_loc_postB</td><td>level-instance</td></tr>
<tr><td>oilcon002_loc_postC</td><td>level-instance</td></tr>
<tr><td>OilCon002_ParkingStructure01(critical)</td><td>level-instance</td></tr>
<tr><td>OilCon002_RescueSite</td><td>level-instance</td></tr>
<tr><td>OilCon002_VZAirportHeli01</td><td>level-instance</td></tr>
<tr><td>OilCon002_VZAirportHeli02</td><td>level-instance</td></tr>
<tr><td>OilCon002_VZAirportHeliPath</td><td>level-instance</td></tr>
<tr><td>OilCon002_VZHeliPilot</td><td>level-instance</td></tr>
<tr><td>OilCon003_deliv</td><td>level-instance</td></tr>
<tr><td>OilCon005_SpawnSportscar01</td><td>level-instance</td></tr>
<tr><td>OilCon005_SpawnSportscar02</td><td>level-instance</td></tr>
<tr><td>OilCon020_endTalk</td><td>level-instance</td></tr>
<tr><td>OilCon020_takesTruck</td><td>level-instance</td></tr>
<tr><td>OilCon021_deadblocker</td><td>level-instance</td></tr>
<tr><td>OilCon021_Laugher_</td><td>level-instance</td></tr>
<tr><td>OilCon021_Laugher_3</td><td>level-instance</td></tr>
<tr><td>OilCon021_Laugher_4</td><td>level-instance</td></tr>
<tr><td>OilCon3_start</td><td>level-instance</td></tr>
<tr><td>OilJob001_Outpost</td><td>level-instance</td></tr>
<tr><td>OilLif001 Table</td><td>level-instance</td></tr>
<tr><td>oilrig_alarm</td><td>level-instance</td></tr>
<tr><td>OrganBox_02</td><td>level-instance</td></tr>
<tr><td>OrganBox_02b</td><td>level-instance</td></tr>
<tr><td>OrganBox_03</td><td>level-instance</td></tr>
<tr><td>OrganBox_03b</td><td>level-instance</td></tr>
<tr><td>OrganBox_04</td><td>level-instance</td></tr>
<tr><td>OrganBox_04b</td><td>level-instance</td></tr>
<tr><td>OrganBox_05</td><td>level-instance</td></tr>
<tr><td>OrganBox_05b</td><td>level-instance</td></tr>
<tr><td>OrganBox_08</td><td>level-instance</td></tr>
<tr><td>OrganBox_08b</td><td>level-instance</td></tr>
<tr><td>OrganBox_09</td><td>level-instance</td></tr>
<tr><td>OrganBox_09b</td><td>level-instance</td></tr>
<tr><td>OrganBox_10</td><td>level-instance</td></tr>
<tr><td>OrganBox_10b</td><td>level-instance</td></tr>
<tr><td>OrganBox_11</td><td>level-instance</td></tr>
<tr><td>OrganBox_11b</td><td>level-instance</td></tr>
<tr><td>OrganBox_12</td><td>level-instance</td></tr>
<tr><td>OrganBox_12b</td><td>level-instance</td></tr>
<tr><td>OrganBox_13</td><td>level-instance</td></tr>
<tr><td>OrganBox_13b</td><td>level-instance</td></tr>
<tr><td>OrganBox_14</td><td>level-instance</td></tr>
<tr><td>OrganBox_14b</td><td>level-instance</td></tr>
<tr><td>OrganBox_15</td><td>level-instance</td></tr>
<tr><td>OrganBox_15b</td><td>level-instance</td></tr>
<tr><td>OrganBox_16</td><td>level-instance</td></tr>
<tr><td>OrganBox_16b</td><td>level-instance</td></tr>
<tr><td>OrganBox_17</td><td>level-instance</td></tr>
<tr><td>OrganBox_17b</td><td>level-instance</td></tr>
<tr><td>OrganBox_18</td><td>level-instance</td></tr>
<tr><td>OrganBox_18b</td><td>level-instance</td></tr>
<tr><td>OrganBox_19</td><td>level-instance</td></tr>
<tr><td>OrganBox_19b</td><td>level-instance</td></tr>
<tr><td>OrganBox_20</td><td>level-instance</td></tr>
<tr><td>OrganBox_20b</td><td>level-instance</td></tr>
<tr><td>OrganBox_21</td><td>level-instance</td></tr>
<tr><td>OrganBox_21b</td><td>level-instance</td></tr>
<tr><td>OrganBox_22</td><td>level-instance</td></tr>
<tr><td>OrganBox_22b</td><td>level-instance</td></tr>
<tr><td>OrganBox_23</td><td>level-instance</td></tr>
<tr><td>OrganBox_23b</td><td>level-instance</td></tr>
<tr><td>OrganBox_24</td><td>level-instance</td></tr>
<tr><td>OrganBox_24b</td><td>level-instance</td></tr>
<tr><td>OrganBox_25</td><td>level-instance</td></tr>
<tr><td>OrganBox_25b</td><td>level-instance</td></tr>
<tr><td>OrganBox_26</td><td>level-instance</td></tr>
<tr><td>OrganBox_26b</td><td>level-instance</td></tr>
<tr><td>OrganBox_27</td><td>level-instance</td></tr>
<tr><td>OrganBox_27b</td><td>level-instance</td></tr>
<tr><td>OrganBox_28</td><td>level-instance</td></tr>
<tr><td>OrganBox_28b</td><td>level-instance</td></tr>
<tr><td>OrganBox_29</td><td>level-instance</td></tr>
<tr><td>OrganBox_29b</td><td>level-instance</td></tr>
<tr><td>OrganBox_31</td><td>level-instance</td></tr>
<tr><td>OrganBox_31b</td><td>level-instance</td></tr>
<tr><td>OrganBox_32</td><td>level-instance</td></tr>
<tr><td>OrganBox_32b</td><td>level-instance</td></tr>
<tr><td>OrganBox_33</td><td>level-instance</td></tr>
<tr><td>OrganBox_33b</td><td>level-instance</td></tr>
<tr><td>OrganBox_34</td><td>level-instance</td></tr>
<tr><td>OrganBox_34b</td><td>level-instance</td></tr>
<tr><td>Pa_Boat_</td><td>level-instance</td></tr>
<tr><td>Pa_BoatBlock_3</td><td>level-instance</td></tr>
<tr><td>Pa_CartelBlock_</td><td>level-instance</td></tr>
<tr><td>Pa_CliffyA</td><td>level-instance</td></tr>
<tr><td>Pa_CliffyB</td><td>level-instance</td></tr>
<tr><td>Pa_Finder_</td><td>level-instance</td></tr>
<tr><td>Pa_OCTakes</td><td>level-instance</td></tr>
<tr><td>Pa_RunMan_</td><td>level-instance</td></tr>
<tr><td>Pa_stager</td><td>level-instance</td></tr>
<tr><td>Panhard (DLCCON004)</td><td>level-instance</td></tr>
<tr><td>ParrotPickup</td><td>level-instance</td></tr>
<tr><td>ParrotPickup_2</td><td>level-instance</td></tr>
<tr><td>PartyOfficial</td><td>level-instance</td></tr>
<tr><td>Path</td><td>level-instance</td></tr>
<tr><td>Path_AllJob002_Jeep01</td><td>level-instance</td></tr>
<tr><td>Path_Ambulance</td><td>level-instance</td></tr>
<tr><td>Path_Bottom01</td><td>level-instance</td></tr>
<tr><td>path_brokenbridge</td><td>level-instance</td></tr>
<tr><td>Path_EarthMover_Patrol</td><td>level-instance</td></tr>
<tr><td>path_firefight2</td><td>level-instance</td></tr>
<tr><td>path_firefight3</td><td>level-instance</td></tr>
<tr><td>path_firefight4</td><td>level-instance</td></tr>
<tr><td>path_gate_patrol</td><td>level-instance</td></tr>
<tr><td>Path_GurBase_Front_PatrolOne</td><td>level-instance</td></tr>
<tr><td>Path_GurBase_MoverArm</td><td>level-instance</td></tr>
<tr><td>Path_GurBase_RoadOne</td><td>level-instance</td></tr>
<tr><td>Path_GurBase_RoadTwo</td><td>level-instance</td></tr>
<tr><td>Path_JetCon001_Bunker_JeepPatrol01</td><td>level-instance</td></tr>
<tr><td>Path_JetCon001_CopterAttack</td><td>level-instance</td></tr>
<tr><td>Path_JetCon001_SupplyBeachAmbush_Tank01</td><td>level-instance</td></tr>
<tr><td>Path_PMC001_GarageSmash</td><td>level-instance</td></tr>
<tr><td>Path_PMC001_WaveTwo_BottomLeft</td><td>level-instance</td></tr>
<tr><td>Path_PMC001_WaveTwo_TopLeft</td><td>level-instance</td></tr>
<tr><td>Path_PMC001_WaveTwo_TopRight</td><td>level-instance</td></tr>
<tr><td>Path_Pmc003_Bunker_TankAmbush01</td><td>level-instance</td></tr>
<tr><td>Path_PMC003_CarmonaFlee</td><td>level-instance</td></tr>
<tr><td>Path_PmcCon003_AngelFallsBridge</td><td>level-instance</td></tr>
<tr><td>Path_PmcCon003_Bunker_ApproachEnc01</td><td>level-instance</td></tr>
<tr><td>Path_Squad_PatrolOne</td><td>level-instance</td></tr>
<tr><td>Path_top02</td><td>level-instance</td></tr>
<tr><td>Path_top03</td><td>level-instance</td></tr>
<tr><td>Path_top04</td><td>level-instance</td></tr>
<tr><td>Path_Trailer_Loop</td><td>level-instance</td></tr>
<tr><td>Path_VZGurAttackJeep1_GC2</td><td>level-instance</td></tr>
<tr><td>Path_VZGurAttackJeep2_GC2</td><td>level-instance</td></tr>
<tr><td>Path_VZGurAttackTruck_GC2</td><td>level-instance</td></tr>
<tr><td>Patrol_GurBase_Gate</td><td>level-instance</td></tr>
<tr><td>patrolBoat_2</td><td>level-instance</td></tr>
<tr><td>patrolBoat_3</td><td>level-instance</td></tr>
<tr><td>patrolBoat_4</td><td>level-instance</td></tr>
<tr><td>patrolBoat_west2</td><td>level-instance</td></tr>
<tr><td>Pirate</td><td>0x800056C2</td></tr>
<tr><td>PirCon001_ConvergeTrigger_Loc</td><td>level-instance</td></tr>
<tr><td>PirCon001_SpawnJetski01</td><td>level-instance</td></tr>
<tr><td>PirCon001_SpawnJetski02</td><td>level-instance</td></tr>
<tr><td>PirCon002_endTalk</td><td>level-instance</td></tr>
<tr><td>PirCon003_endTalk</td><td>level-instance</td></tr>
<tr><td>PirCon004_DeliveryRecipient</td><td>level-instance</td></tr>
<tr><td>PirCon004_DelStart_loc</td><td>level-instance</td></tr>
<tr><td>PirCon004_Dest_Location</td><td>level-instance</td></tr>
<tr><td>PirCon004_EndPursuit_region</td><td>level-instance</td></tr>
<tr><td>PirCon004_OrganTruck</td><td>level-instance</td></tr>
<tr><td>PirCon004_PipeObst01</td><td>level-instance</td></tr>
<tr><td>PirCon004_PipeObst02</td><td>level-instance</td></tr>
<tr><td>PirCon004_Player2Truck</td><td>level-instance</td></tr>
<tr><td>PirCon004_Smokestack(explode)01</td><td>level-instance</td></tr>
<tr><td>PirCon004_Smokestack(explode)02</td><td>level-instance</td></tr>
<tr><td>PirCon004_Tanker(explode)</td><td>level-instance</td></tr>
<tr><td>PirCon004_TruckGoal</td><td>level-instance</td></tr>
<tr><td>PirCon004_TruckSpawn</td><td>level-instance</td></tr>
<tr><td>Pistol (silver)</td><td>0x8000508E</td></tr>
<tr><td>PLZ45 (DLC) (LongHib) (Prototype)</td><td>level-instance</td></tr>
<tr><td>PMC</td><td>level-instance</td></tr>
<tr><td>Pmc001_Door_Front</td><td>level-instance</td></tr>
<tr><td>PMC001_Door_Front</td><td>level-instance</td></tr>
<tr><td>PMC001_EntourageScorpion</td><td>level-instance</td></tr>
<tr><td>PMC001_FrontDoor_InvisiblePhysics</td><td>level-instance</td></tr>
<tr><td>PMC001_GarageEntrance</td><td>level-instance</td></tr>
<tr><td>PMC001_HVT_01</td><td>level-instance</td></tr>
<tr><td>PMC001_HVT_02</td><td>level-instance</td></tr>
<tr><td>PMC001_HVT_03</td><td>level-instance</td></tr>
<tr><td>PMC001_HVT_04</td><td>level-instance</td></tr>
<tr><td>PMC001_HVT_05</td><td>level-instance</td></tr>
<tr><td>PMC002 Oilrig</td><td>level-instance</td></tr>
<tr><td>PMC002_Office</td><td>level-instance</td></tr>
<tr><td>PMC003_AMX_01</td><td>level-instance</td></tr>
<tr><td>PMC003_AMX_02</td><td>level-instance</td></tr>
<tr><td>PMC003_AMX_03</td><td>level-instance</td></tr>
<tr><td>PMC003_AMX_04</td><td>level-instance</td></tr>
<tr><td>PMC003_EwanTaxi</td><td>level-instance</td></tr>
<tr><td>PMC_CentralBuilding</td><td>level-instance</td></tr>
<tr><td>pmc_middle_gate</td><td>level-instance</td></tr>
<tr><td>PmcCon002 Blanco</td><td>level-instance</td></tr>
<tr><td>PmcCon002 Exit</td><td>level-instance</td></tr>
<tr><td>PmcCon002 Explosion</td><td>level-instance</td></tr>
<tr><td>PmcCon002_OilrigA</td><td>level-instance</td></tr>
<tr><td>PmcCon002_OilrigB</td><td>level-instance</td></tr>
<tr><td>PmcCon002_OilrigC</td><td>level-instance</td></tr>
<tr><td>PmcCon002_OilrigD</td><td>level-instance</td></tr>
<tr><td>PmcCon003_Heli_BridgeAmbush</td><td>level-instance</td></tr>
<tr><td>PmcCon013_Loc</td><td>level-instance</td></tr>
<tr><td>PmcCon013_Target</td><td>level-instance</td></tr>
<tr><td>PmcCon015_RaceCar</td><td>level-instance</td></tr>
<tr><td>PMCCon018OutOfBounds</td><td>level-instance</td></tr>
<tr><td>PMCCon032_Easy_LR1</td><td>level-instance</td></tr>
<tr><td>PMCCon032_Easy_LR2</td><td>level-instance</td></tr>
<tr><td>PMCCon032_Easy_LR3</td><td>level-instance</td></tr>
<tr><td>PMCCon032_Easy_LR4</td><td>level-instance</td></tr>
<tr><td>PMCCon032_Easy_LR5</td><td>level-instance</td></tr>
<tr><td>PMCCon033_LR1</td><td>level-instance</td></tr>
<tr><td>PMCCon033_LR2</td><td>level-instance</td></tr>
<tr><td>PMCCon033_LR3</td><td>level-instance</td></tr>
<tr><td>PMCCon033_LR4</td><td>level-instance</td></tr>
<tr><td>PMCCon033_LR5</td><td>level-instance</td></tr>
<tr><td>PMCCon034OutOfBounds</td><td>level-instance</td></tr>
<tr><td>pmcoutpost_bld_hqgarage</td><td>level-instance</td></tr>
<tr><td>ProjectsBuildingGurcon002</td><td>level-instance</td></tr>
<tr><td>psych</td><td>level-instance</td></tr>
<tr><td>pth_explodingmans</td><td>level-instance</td></tr>
<tr><td>refinery_doc_warehouse01</td><td>level-instance</td></tr>
<tr><td>refinery_office02</td><td>level-instance</td></tr>
<tr><td>refinery_office03</td><td>level-instance</td></tr>
<tr><td>Reg_AllCon002_Strikes</td><td>level-instance</td></tr>
<tr><td>reg_MargaritaChinaFactionZone</td><td>level-instance</td></tr>
<tr><td>Reg_Oil020_EndPursuit</td><td>level-instance</td></tr>
<tr><td>Region_AllJob002_04_TriggerJeep</td><td>level-instance</td></tr>
<tr><td>region_brokenbridge</td><td>level-instance</td></tr>
<tr><td>Region_JetCon001_BBWarning</td><td>level-instance</td></tr>
<tr><td>Region_JetCon001_BunkerIslandArrive</td><td>level-instance</td></tr>
<tr><td>Region_JetCon001_Checkpoint</td><td>level-instance</td></tr>
<tr><td>Region_JetCon001_CopterAttack</td><td>level-instance</td></tr>
<tr><td>Region_JetCon001_NearBunker</td><td>level-instance</td></tr>
<tr><td>Region_JetCon001_Supply_AASite01</td><td>level-instance</td></tr>
<tr><td>Region_JetCon001_SupplyBeachAssault</td><td>level-instance</td></tr>
<tr><td>Region_JetCon001_TravelMusic</td><td>level-instance</td></tr>
<tr><td>region_killvzaheli</td><td>level-instance</td></tr>
<tr><td>Region_PMC001_Banter01</td><td>level-instance</td></tr>
<tr><td>Region_PMC001_EndPursuit</td><td>level-instance</td></tr>
<tr><td>Region_PMC001_VZCheckpointRegion</td><td>level-instance</td></tr>
<tr><td>Region_Pmc003_Bunker_TankAmbush01</td><td>level-instance</td></tr>
<tr><td>Region_PMC_FrontGate</td><td>level-instance</td></tr>
<tr><td>Region_PmcCon001_VillaWideRegion</td><td>level-instance</td></tr>
<tr><td>Region_PmcCon003_AngelFallsBridge</td><td>level-instance</td></tr>
<tr><td>region_pmccon003_angelfallsbridge</td><td>level-instance</td></tr>
<tr><td>Region_PmcCon003_Bunker_ApproachEnc01</td><td>level-instance</td></tr>
<tr><td>region_vza_handbrake</td><td>level-instance</td></tr>
<tr><td>region_vza_tankswitch</td><td>level-instance</td></tr>
<tr><td>region_vza_usegrenade</td><td>level-instance</td></tr>
<tr><td>ResidentialBuildingGurcon002</td><td>level-instance</td></tr>
<tr><td>rgn_atmo_Angelfalls</td><td>level-instance</td></tr>
<tr><td>rgn_atmo_caracas</td><td>level-instance</td></tr>
<tr><td>rgn_atmo_carmonaislandrain</td><td>level-instance</td></tr>
<tr><td>rgn_atmo_interior</td><td>level-instance</td></tr>
<tr><td>rgn_atmo_Maracaibo</td><td>level-instance</td></tr>
<tr><td>rgn_atmo_PMCinterior</td><td>level-instance</td></tr>
<tr><td>rgn_checkspawn_a</td><td>level-instance</td></tr>
<tr><td>rgn_checkspawn_b</td><td>level-instance</td></tr>
<tr><td>rgn_checkspawn_c</td><td>level-instance</td></tr>
<tr><td>rgn_checkspawn_d</td><td>level-instance</td></tr>
<tr><td>rgn_checkspawn_e</td><td>level-instance</td></tr>
<tr><td>rgn_checkspawn_f</td><td>level-instance</td></tr>
<tr><td>rgn_checkspawn_g</td><td>level-instance</td></tr>
<tr><td>rgn_checkspawn_h</td><td>level-instance</td></tr>
<tr><td>rgn_checkspawn_i</td><td>level-instance</td></tr>
<tr><td>rgn_sfx_GurCon002</td><td>level-instance</td></tr>
<tr><td>RiverBoat_</td><td>level-instance</td></tr>
<tr><td>Road</td><td>0x80004514</td></tr>
<tr><td>Scorpion_TankAmbush01</td><td>level-instance</td></tr>
<tr><td>Smart Bomb Projectile</td><td>0x80008E45</td></tr>
<tr><td>Solano_Bunker</td><td>level-instance</td></tr>
<tr><td>Solano_Bunker_PMC004</td><td>level-instance</td></tr>
<tr><td>SolanoBunkerDoors</td><td>level-instance</td></tr>
<tr><td>SpeedAtmo2</td><td>level-instance</td></tr>
<tr><td>Squad_PatrolOne</td><td>level-instance</td></tr>
<tr><td>stager</td><td>level-instance</td></tr>
<tr><td>Starter</td><td>level-instance</td></tr>
<tr><td>Starter_Oil0_Start1</td><td>level-instance</td></tr>
<tr><td>Starter_Pmc_Start1</td><td>level-instance</td></tr>
<tr><td>StatueMoveLoc</td><td>level-instance</td></tr>
<tr><td>Support Vehicle (Cruise Missile)</td><td>0x80008E48</td></tr>
<tr><td>Support Vehicle (Mig27)</td><td>0x80009AD2</td></tr>
<tr><td>Target1</td><td>level-instance</td></tr>
<tr><td>Target4</td><td>level-instance</td></tr>
<tr><td>timerLineRegion</td><td>level-instance</td></tr>
<tr><td>top02</td><td>level-instance</td></tr>
<tr><td>top03</td><td>level-instance</td></tr>
<tr><td>top04</td><td>level-instance</td></tr>
<tr><td>TransitHeli_Landing</td><td>level-instance</td></tr>
<tr><td>TransitHeli_Landing02</td><td>level-instance</td></tr>
<tr><td>TransitHeli_Spawn</td><td>level-instance</td></tr>
<tr><td>TruckMoveLoc</td><td>level-instance</td></tr>
<tr><td>Turncoat</td><td>level-instance</td></tr>
<tr><td>UH1 Transport (PMC)</td><td>0x80008206</td></tr>
<tr><td>UPseat</td><td>level-instance</td></tr>
<tr><td>Van (Racing)</td><td>0x800074A6</td></tr>
<tr><td>VZ</td><td>0x80004382</td></tr>
<tr><td>VZ Soldier</td><td>0x80004385</td></tr>
<tr><td>vz_mine_gate</td><td>level-instance</td></tr>
<tr><td>vza001_gate</td><td>level-instance</td></tr>
<tr><td>vza001_gate2</td><td>level-instance</td></tr>
<tr><td>vza_beachguard_1</td><td>level-instance</td></tr>
<tr><td>vza_beachguard_2</td><td>level-instance</td></tr>
<tr><td>vza_beachguard_3</td><td>level-instance</td></tr>
<tr><td>vza_beachguard_4</td><td>level-instance</td></tr>
<tr><td>vza_treeattack_1</td><td>level-instance</td></tr>
<tr><td>vza_treehillpath_2</td><td>level-instance</td></tr>
<tr><td>vza_villageguard_1</td><td>level-instance</td></tr>
<tr><td>vza_villageguard_2</td><td>level-instance</td></tr>
<tr><td>vza_villageguard_3</td><td>level-instance</td></tr>
<tr><td>VzaCon001_StartingBoat</td><td>level-instance</td></tr>
<tr><td>VZBlock_1</td><td>level-instance</td></tr>
<tr><td>w2_bottom01</td><td>level-instance</td></tr>
<tr><td>w2_bottom02</td><td>level-instance</td></tr>
<tr><td>w2_bottom03</td><td>level-instance</td></tr>
<tr><td>w2_bottom04</td><td>level-instance</td></tr>
<tr><td>w2_top01</td><td>level-instance</td></tr>
<tr><td>w2_top02</td><td>level-instance</td></tr>
<tr><td>w2_top03</td><td>level-instance</td></tr>
<tr><td>w2_top04</td><td>level-instance</td></tr>
<tr><td>Wager Exit</td><td>level-instance</td></tr>
<tr><td>ZTZ63a (DLC) (LongHib) (Prototype)</td><td>level-instance</td></tr>
<tr><td>ZTZ98 (DLC) (LongHib) (Prototype)</td><td>level-instance</td></tr>
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
