---
title: Hud
parent: Engine Namespaces
nav_order: 12
---

# Hud

## Overview

`Hud` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it,
no `import()` call needed, and it's always globally available to every script. Unlike most other engine
namespaces documented in this section, `Hud` is not a flat list of functions: it's a table of roughly
23 **sub-namespace objects** (`Hud.Tutorial`, `Hud.Radar`, `Hud.MessageBox`, `Hud.Fanfare`, and so on),
each of which holds its own small set of methods. Most of those methods are called with **colon syntax**
(`Hud.Tutorial:SetText(...)`), passing a single table argument, though a handful of call sites use dot
syntax with a plain table instead. Together these sub-namespaces cover on-screen popups and "fanfare"
sequences (support drops, contact intros, job completion, unlocks), the objective radar (blips, line
regions, animated markers), the objective tray (the small numbered text/image slots under the radar),
resource counters (cash and fuel readouts), tutorial messages, message boxes (mission objective text),
and the in-game shop UI.

## Provenance

This page's list of sub-namespaces and their methods comes from a live `pairs(Hud)` enumeration in-game,
followed by a `pairs()` enumeration of each returned sub-table — not from reading engine source, since
the engine implementation isn't available to us. That two-level dump is complete and authoritative for
*names*: all 23 sub-namespaces and every method listed under them really exist. It says nothing about
parameters or behavior. Where a method is actually called somewhere in the ~230 decompiled `.lua`
scripts, this page shows a real argument pattern (almost always a single table with named fields, per
the `MrxGuiHudMessage`/`HudInterface` style used throughout `resident/mrxguiinterface.lua`, which is the
Lua-side layer that wires these calls through to the native HUD). Given the size of this namespace
(23 sub-tables, ~70 methods total), not every sub-namespace received individual grep verification in this
pass — `Tutorial`, `MessageBox`, the `Fanfare` family, `Radar`, `ObjectiveTray`, and `ResourceCounter` are
backed by real call sites; the rest (`Announcement`, `Cinematic`, `CinematicPlaceholder`, `ClassyText`,
`FactionDisplay`, `FanfareQueue`, `MapLabel`, `Satellite`, `Shop`, `SubtitleBuffer`, `SupportMenu`) are
listed with names only, on the presumption that they follow the same colon-call, single-table-argument
shape as their confirmed siblings — that presumption is not verified and should not be relied on.

## Functions

### Tutorial

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetText` | `Hud.Tutorial:SetText({vPlayer=uGuid, sText=sMessage})` | **Confirmed** in `resident/mrxtutorialmanager.lua`'s `ShowMessage`/`HideMessage` functions: `Hud.Tutorial:SetText({vPlayer = Player.GetLocalPlayer(), sText = sMessage})` shows a message, and calling it again with `sText = nil` clears it. This is the function underneath the already-documented, live-tested `MrxTutorialManager.ShowMessage` — see [Snippets: Show a custom HUD message](../snippets#show-a-custom-hud-message) for the recommended, higher-level way to trigger it rather than calling `Hud.Tutorial` directly. |
| `ShowTutorialForObject` | `Hud.Tutorial:ShowTutorialForObject({...})` | No call site checked in this pass — presumed similar table-argument shape to the confirmed `SetText` above. |
| `ShowTutorialOnscreen` | `Hud.Tutorial:ShowTutorialOnscreen({...})` | No call site checked in this pass — presumed similar table-argument shape to the confirmed `SetText` above. |

### MessageBox

| Function | Signature (best-known) | Notes |
|---|---|---|
| `AddMessage` | `tMsgIds = Hud.MessageBox:AddMessage({sMessage=s, nPriority=n, nDuration=n, bClearBuffer=b, bAllowsAppends=b, fCallback=fn})` | Confirmed in real scripts, e.g. `resident/mrxguiinterface.lua`'s `DisplayObjectiveMessage`: `Hud.MessageBox:AddMessage({sMessage = sMsg, nPriority = nPriority, nDuration = 5, bClearBuffer = true, bAllowsAppends = false, fCallback = _MsgDisplayed})`. Returns a value (message-id table) that call sites capture and later pass to `ModifyPendingMessage`. Also used with a minimal single-field table, e.g. `Hud.MessageBox:AddMessage({sMessage = "[Generic.CheckpointReached]"})`. Widely called across `resident/mrxsupport.lua`, `resident/mrxtaskcontract.lua`, `vz/wifpmcgarage.lua`, `vz/wifvzboundary.lua`. |
| `ModifyPendingMessage` | `bSuccess = Hud.MessageBox:ModifyPendingMessage({tMessageIds=t, sMessage=s})` | Confirmed in `resident/mrxguiinterface.lua`: `Hud.MessageBox:ModifyPendingMessage({tMessageIds = tMsgIds, sMessage = sMsg})`, called with the id table previously returned by `AddMessage`; returns a success boolean. |
| `RemovePendingMessage` | `Hud.MessageBox:RemovePendingMessage({...})` | No call site checked in this pass — presumed to take the same message-id table returned by `AddMessage`, by analogy with `ModifyPendingMessage`. |
| `Clear` | `Hud.MessageBox:Clear({})` | Confirmed in `resident/mrxtaskcontract.lua`: `Hud.MessageBox:Clear({})`, called with an empty table. |

### Fanfare family (Fanfare, SupportFanfare, ContactFanfare, EventFanfare, TextFanfare, CardFanfare, JobFanfare)

All seven "fanfare" sub-namespaces share the same overall pattern, confirmed by both real call sites and
by their shared implementation in `resident/mrxguiinterface.lua` (which defines `function Hud.Fanfare:Commence(tArgs)`,
`function Hud.SupportFanfare:Create(tArgs)`, etc., all funneling into an internal `MrxGuiHudMessage`/`_tFanfareQueue`
system): each variant is driven by `:Commence(tArgs)` to trigger the popup, with most variants also exposing
a `:Create(tArgs)` and/or `:AddItem(tArgs)` step to build up content before commencing, and `tArgs` always a
single table of named fields (title/name/text lines/faction/callback, depending on the variant). `JobFanfare`
differs slightly, exposing `Complete`/`Failed` instead of `Commence`.

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Fanfare.Create` | `Hud.Fanfare:Create({...})` | Confirmed call sites in `vz/mecjob.lua` and `resident/mrxtaskcontract.lua`, e.g. `Hud.Fanfare:Create({...})` followed later by `Hud.Fanfare:AddItem(tLedgerItem)` and `Hud.Fanfare:Commence({})`. |
| `Fanfare.AddItem` | `Hud.Fanfare:AddItem(tLedgerItem)` | Confirmed in `resident/mrxtaskcontract.lua`, called multiple times with a "ledger item" table before `Commence`. |
| `Fanfare.Commence` | `Hud.Fanfare:Commence(tArgs)` | Confirmed in `vz/mecjob.lua` (`Hud.Fanfare:Commence({})`) and implemented in `resident/mrxguiinterface.lua` as `function Hud.Fanfare:Commence(tArgs)`, which reads `tArgs.nSlowdownDuration`. |
| `SupportFanfare.Create` | `Hud.SupportFanfare:Create(tArgs)` | Implemented in `resident/mrxguiinterface.lua`; reads `tArgs.fCallback`, `tArgs.tCallbackData`. |
| `SupportFanfare.AddItem` | `Hud.SupportFanfare:AddItem(tArgs)` | Implemented in `resident/mrxguiinterface.lua`; reads `tArgs.sTexture`, `tArgs.sItemName`, `tArgs.sFaction`, `tArgs.sContactName`, `tArgs.sBlipName`. |
| `SupportFanfare.Commence` | `Hud.SupportFanfare:Commence(tArgs)` | Implemented in `resident/mrxguiinterface.lua`. |
| `ContactFanfare.Commence` | `Hud.ContactFanfare:Commence(tArgs)` | Confirmed in `vz/meccon001.lua`; implemented in `resident/mrxguiinterface.lua`, which reads `tArgs.fCallback`, `tArgs.tCallbackData`. |
| `EventFanfare.Commence` | `Hud.EventFanfare:Commence({sType=s, vText=s_or_t})` | Confirmed across many real call sites, e.g. `resident/mrxpmc.lua`, `resident/mrxunlockfanfare.lua`, `resident/mrxtaskjobverifyset.lua`: `Hud.EventFanfare:Commence({sType = sFanfareType, vText = sFanfareText})`. Implementation in `resident/mrxguiinterface.lua` normalizes a legacy `tArgs.sText` field into `tArgs.vText` if the latter is absent. **Confirmed working by live testing** — see the `sType` catalog and the "custom toast" trick just below the table. |
| `CardFanfare.Commence` | `Hud.CardFanfare:Commence({sFaction=s, sTitle=s, sName=s, sJobTitle=s, sPhone1=s, sPhone2=s, sEmail=s, nDisplayTime=n, fCallback=fn, tCallbackData=t})` | Confirmed in `resident/mrxbriefing.lua`; full field list read directly from the `resident/mrxguiinterface.lua` implementation, which forwards those fields to `MrxGuiHudMessage.CardFanfareSetParameters`. |
| `TextFanfare.Commence` | `Hud.TextFanfare:Commence({sLine1=s, sLine2=s, nEntranceTime=n, nDisplayTime=n, nFadeTime=n, fCallback=fn, tCallbackData=t})` | No direct top-level call site found in this pass, but field list confirmed from the `resident/mrxguiinterface.lua` implementation. |
| `JobFanfare.Complete` | `Hud.JobFanfare:Complete({...})` | No call site checked in this pass — presumed similar table-argument shape to confirmed siblings. |
| `JobFanfare.Failed` | `Hud.JobFanfare:Failed({...})` | No call site checked in this pass — presumed similar table-argument shape to confirmed siblings. |

#### EventFanfare sType catalog and the custom toast trick

`EventFanfare.Commence`'s implementation, confirmed directly in `resident/mrxguihudmessage.lua`, gates on
a lookup table before showing anything at all:

```lua
function ShowEventFanfare(sType, vText, fCallback, tCallbackData)
  if not sType or not _tEventTextures[sType] then
    return
  end
  ...
```

`sType` must be a key present in `_tEventTextures` or the call **silently does nothing** — no error, no
fallback icon, just a no-op. There are exactly 9 real values shipped in the game, each pairing a
localization-key title, an icon texture, and a sound cue (all confirmed directly from
`resident/mrxguihudmessage.lua`'s `_tEventTitles`/`_tEventTextures`/`_tEventSounds` tables):

| `sType` | Title key | Texture | Sound |
|---|---|---|---|
| `contact` | `[Fanfare.Common.NewContact]` | `unlockables_newcontact` | `ui_signal_ding` |
| `support` | `[Fanfare.Common.NewShopItem]` | `unlockables_newshopitem` | `ui_signal_ding` |
| `stockpile` | `[Fanfare.Common.NewStockpileItem]` | `unlockables_newstockpileitem` | `ui_signal_ding` |
| `landingzone` | `[Fanfare.Common.NewLandingZone]` | `unlockables_landingzone` | `ui_signal_ding` |
| `hvtcapture` | `[Fanfare.Common.HvtCaptured]` | `unlockables_hvtcaptured` | `ui_signal_generic` |
| `hvtkill` | `[Fanfare.Common.HvtKilled]` | `unlockables_hvtkilled` | `ui_signal_generic` |
| `bounty` | `[Fanfare.Common.NewBounties]` | `unlockables_newbounties` | `ui_signal_ding` |
| `outfit` | `[Fanfare.Common.NewOutfit]` | `unlockables_newoutfit` | `ui_signal_ding` |
| `highscore` | `[Fanfare.Common.NewHighScore]` | `unlockables_leaderboardupdated` | `ui_signal_ding` |

**Confirmed working by live testing** — cycling all 9 in a loop plays them out one after another
automatically, since they funnel through the same `_tFanfareQueue` every fanfare variant shares.

**Also confirmed by live testing**: since `_tEventTextures`/`_tEventTitles`/`_tEventSounds` are all
declared without `local` in source, they're reachable and writable via `import("MrxGuiHudMessage")`,
which means the no-op gate above can be sidestepped by adding your own key rather than patching
`ShowEventFanfare` itself:

```lua
import("MrxGuiHudMessage")

MrxGuiHudMessage._tEventTextures.custom = "this_texture_does_not_exist"
Hud.EventFanfare:Commence({sType = "custom", vText = "Whatever message I want!"})
```

Two real, confirmed behaviors from testing this, one of them a genuine surprise:

- **Reusing a real, existing texture name** (e.g. `unlockables_newstockpileitem`) makes the icon *and*
  the header text both display — but the header shown is that texture's own real title
  (`"NEW STOCKPILE ITEM"`), **not** whatever was set in `_tEventTitles.custom`. This means the visible
  on-screen header isn't actually driven by `_tEventTitles[sType]` on this code path at all — that table
  (and the separate `GetEventFanfareTitle` function) appears to only feed the co-op text-summary event
  (`Net.SendEvent_Fanfare`'s composed message), a different display surface entirely. Not fully
  understood, flagged honestly rather than guessed at further.
- **Using a texture name that doesn't correspond to a real loaded asset** produces a clean result: no
  icon, no gold header text, just the plain `vText` message centered on screen — confirmed by live
  testing. This is the simplest, lowest-effort way to print an arbitrary message dead-center on the HUD
  without building any custom widget at all.

### Radar

| Function | Signature (best-known) | Notes |
|---|---|---|
| `AddObjective` | `Hud.Radar:AddObjective({sName=s, nR=n, nG=n, nB=n, nWidth=n, nHeight=n, sTexture=s, uGuid=u, bSticky=b, bRotate=b, bOriented=b, nSortOrder=n, bDontNetSync=b})` | Confirmed extensively, e.g. `resident/blippable.lua`'s objective-marker class, `resident/mrxfactionmanager.lua`, `resident/mrxhq.lua`, `resident/mrxsupport.lua`, `resident/outpost.lua`, `resident/mrxtaskobjective.lua`, `resident/mrxtaskrace.lua`, `resident/mrxparkinglotmanager.lua`, `vz/wifpmcinterior.lua`. Adds a radar blip for an objective. |
| `RemoveObjective` | `Hud.Radar:RemoveObjective({sName=s [, bDontNetSync=b]})` | Confirmed widely alongside `AddObjective` in the same files; also seen called with a positional-array shape in one site: `Hud.Radar:RemoveObjective({uDoor})` (`vz/pmccon001.lua`), meaning the accepted shapes aren't fully uniform. |
| `UpdateObjective` | `Hud.Radar:UpdateObjective(tBlipConfig)` | Confirmed in `resident/mrxtaskobjective.lua`, passed a pre-built config table (`tBlipConfig`) matching the shape used by `AddObjective`. |
| `AnimateObjectiveSize` | `Hud.Radar:AnimateObjectiveSize({sName=s, ...})` | Confirmed in `resident/dangerousbuilding.lua`, `resident/mrxparkinglotmanager.lua`, `resident/mrxtaskobjective.lua`, `vz/oilcon002.lua`, `vz/wifpmcinterior.lua` (e.g. `Hud.Radar:AnimateObjectiveSize({sName = sBlipName})`). |
| `AnimateObjectiveAlpha` | `Hud.Radar:AnimateObjectiveAlpha({...})` | Confirmed in `resident/dangerousbuilding.lua` and `vz/oilcon002.lua`, called with a table argument; exact field list beyond a presumed `sName`/target key not fully pinned down in this pass. |
| `AnimateObjectiveSonar` | `Hud.Radar:AnimateObjectiveSonar({...})` | Confirmed in `resident/mrxfactionmanager.lua`, called with a table argument. |
| `UnanimateObjective` | `Hud.Radar:UnanimateObjective({...})` | No call site checked in this pass — presumed counterpart to the `Animate*` family above. |
| `AddLineRegion` | `Hud.Radar:AddLineRegion(tRegionParam)` | Confirmed in `resident/factionzone.lua`, `resident/mrxguiinterface.lua`, `vz/wifvzboundary.lua`, passed a pre-built region-parameter table. |
| `RemoveLineRegion` | `Hud.Radar:RemoveLineRegion({uGuid=u})` or `Hud.Radar:RemoveLineRegion(tRegionParam)` | Confirmed in the same three files as `AddLineRegion`; the removal form seen most often is `Hud.Radar:RemoveLineRegion({uGuid = uBoundary})`. |

### ObjectiveTray

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetSlotToText` | `Hud.ObjectiveTray:SetSlotToText({vPlayer=uGuid_or_nil, nSlot=n, sText=s})` | Extremely common across mission (`vz/`) scripts — dozens of confirmed call sites, e.g. `Hud.ObjectiveTray:SetSlotToText({nSlot = 1, sText = " "})` (`vz/chicon001.lua`) and the fuller form with `vPlayer = nil` (`vz/pircon004.lua`, `vz/allcon002.lua`). Sets the text shown in one of the small numbered objective-tray slots. |
| `ClearSlot` | `Hud.ObjectiveTray:ClearSlot({vPlayer=uGuid_or_nil, nSlot=n})` | Extremely common alongside `SetSlotToText`, e.g. `Hud.ObjectiveTray:ClearSlot({vPlayer = nil, nSlot = 1})` (`vz/allcon002.lua`, `vz/oilcon020.lua`, `vz/pircon002.lua`) and the shorter `Hud.ObjectiveTray:ClearSlot({nSlot = 1})` (`vz/pmccon013.lua`, `vz/pmccon032.lua`) — the `vPlayer` field appears to be optional. |
| `SetSlotToImage` | `Hud.ObjectiveTray:SetSlotToImage({...})` | Confirmed in `resident/mrxguiinterface.lua`, called with a table argument alongside `SetSlotToText` in the same dispatch function; exact field list not fully confirmed in this pass. |
| `SetSlotToWidget` | `Hud.ObjectiveTray:SetSlotToWidget({...})` | No call site checked in this pass — presumed similar shape to `SetSlotToText`/`SetSlotToImage`. |

### ResourceCounter

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetCash` | `Hud.ResourceCounter:SetCash({nValue=n, sReason=s_or_nil, nIncrement=n_or_nil})` | Confirmed in `resident/mrxpmc.lua`'s `DisplayCash`/`DisplayResources` functions: `Hud.ResourceCounter:SetCash({nValue = nCash or 0, sReason = sMappedReason, nIncrement = nChange})`. Drives the cash readout in the HUD's resource counter. |
| `SetFuel` | `Hud.ResourceCounter:SetFuel({nValue=n, nMax=n, nIncrement=n_or_nil})` | Confirmed in `resident/mrxpmc.lua`'s `DisplayResources`: `Hud.ResourceCounter:SetFuel({nValue = Player.GetFuel() or 0, nMax = GetFuelCapacity(), nIncrement = nFuelChange})`. |
| `SetSuppressed` | `Hud.ResourceCounter:SetSuppressed({bSuppressCash=b, bSuppressFuel=b})` | Confirmed in `resident/mrxstate.lua`: `Hud.ResourceCounter:SetSuppressed({bSuppressCash = true, bSuppressFuel = true})` and the inverse to re-enable; also called in `resident/mrxmissionflow.lua` with a table argument. Hides/shows the cash and fuel readouts independently. |
| `Show` | `Hud.ResourceCounter:Show({nDuration=n})` | Confirmed in `resident/mrxbriefing.lua`: `Hud.ResourceCounter:Show({nDuration = -1})`. |
| `Hide` | `Hud.ResourceCounter:Hide({})` | Confirmed in `resident/mrxbriefing.lua`: `Hud.ResourceCounter:Hide({})`, called with an empty table. |

### Everything else (no call sites checked in this pass)

The following sub-namespaces exist (confirmed via the live `pairs(Hud)` enumeration and per-sub-table
`pairs()` dumps) but were not individually grepped in this pass, given the size of this namespace.
Presume they follow the same colon-call, single-table-argument convention as the confirmed sub-namespaces
above — that presumption is unverified.

| Sub-namespace | Methods |
|---|---|
| `Announcement` | `Show` |
| `Cinematic` | `Hide`, `Play`, `Pause`, `Show` |
| `CinematicPlaceholder` | `Hide`, `Show` |
| `ClassyText` | `ShowText` |
| `FactionDisplay` | `SetValue`, `RemoveMeter`, `HideMeter`, `AddMeter`, `ConfigureThresholds`, `RemoveAllMeters`, `Show`, `StartPursuit`, `StartTimer`, `SetInsideFactionZone` |
| `FanfareQueue` | `ClientPause`, `Pause`, `ClientSetPending`, `Append` |
| `MapLabel` | `Show` |
| `Satellite` | `SetTutorialText` |
| `Shop` | `SetCallback`, `Create`, `Commence`, `AddItemFull`, `SetCloseCallback`, `Close`, `AddItem` |
| `SubtitleBuffer` | `ModifyPendingMessage`, `AddMessage`, `RemovePendingMessage`, `Clear` |
| `SupportMenu` | `SetShootingGalleryMode`, `RemoveItem`, `AddItem` |

## Notes for modders

- **Almost everything on this namespace is called with colon syntax and a single table argument**:
  `Hud.SubNamespace:Method({field = value, ...})`. This differs from most other engine namespaces
  documented in this section (e.g. `Object`, `Human`), which are called with dot syntax and positional
  `uGuid`-first arguments. Don't assume the positional convention carries over to `Hud`.
- `Hud.Tutorial:SetText` is the lowest-level, directly-confirmed entry point for showing a custom tutorial
  message, but you should not call it directly in a mod. Use `MrxTutorialManager.ShowMessage`/`HideMessage`
  instead — see [Snippets: Show a custom HUD message](../snippets#show-a-custom-hud-message-with-icon-and-sound) for the
  tested, higher-level wrapper, which additionally handles net-sync, duplicate-message suppression, and
  identifier-based message ownership that calling `Hud.Tutorial:SetText` directly would bypass.
- `SubtitleBuffer` exposes the exact same method names as `MessageBox` (`AddMessage`, `ModifyPendingMessage`,
  `RemovePendingMessage`, `Clear`) — very likely a parallel message queue for subtitles rather than
  objective-style HUD messages, but that relationship is inferred from naming only and was not confirmed
  against a call site in this pass.
- The seven fanfare sub-namespaces (`Fanfare`, `SupportFanfare`, `ContactFanfare`, `EventFanfare`,
  `TextFanfare`, `CardFanfare`, `JobFanfare`) all funnel through the same internal fanfare queue
  (`_tFanfareQueue`/`MrxGuiHudMessage`) as seen in `resident/mrxguiinterface.lua` — they're variations on
  one underlying popup system, not independent implementations, which is why their argument shapes rhyme
  so closely.
- Sub-namespaces listed with "no call sites checked in this pass" are real (confirmed via the live
  `pairs(Hud)` dump and per-sub-table enumeration) but their method signatures are unconfirmed beyond the
  presumed table-argument, colon-call convention — don't build mods around them without testing in-game
  first.
