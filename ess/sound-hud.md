---
title: Sound & HUD
parent: Essentials (Ess)
nav_order: 8
---

# Sound & HUD

## Overview

`Ess.Sound` and `Ess.Hud` cover getting the player's attention. `Ess.Sound` is a direct one-shot
sound/ambience cueing layer, plus (new in 0.5.0) cue validation and the category mixer. `Ess.Hud` drives the
game's *own* native chrome — the tutorial-hint popup, the centered banner, the stylised animated title, the
region card, the message box, the objective tray, the resource readouts and the faction meters — built on
confirmed-working resident-module patterns instead of a hand-rolled custom widget. Part of
[Essentials (Ess)](index).

`Ess.Hud` is deliberately distinct from `Ess.UI.Toast` (a custom `.gfx` movie widget, see [Ess.UI](ui)):
everything here renders in the game's real HUD, with the game's real fonts, animation and sound.

**`Hud.*` is readable Lua, not a black box.** It was catalogued as an engine native for a long time and it
isn't one: `resident/mrxguiinterface.lua` opens with `_G.Hud = HudInterface` (and `_G.Pda = PdaInterface`),
and each of that one file's 106 published functions — 75 under `Hud`, 31 under `Pda` — is a thin wrapper
that resolves a Scaleform widget by name and forwards to it. The widget classes are script
too (`mrxguimanager.lua`, `mrxguitextbuffer.lua`, `mrxguihudmessage.lua`, `mrxguihudfactiongauge.lua`,
`mrxguihudfactionbuffer.lua`). So the whole `Ess.Hud` layer was written by *reading* those files rather than
probing blind, and then confirmed on screen — Ess records the 0.5.0 sweep as live-confirmed 2026-07-26. See
[Hud](../namespaces/hud) for the raw namespace underneath.

Two consequences that bite anyone calling `Hud.*` directly, and which every wrapper on this page already
handles: the functions are **method calls** (`Hud.MessageBox:AddMessage{...}` — colon, not dot; the wrapper
reads `self.sName` to pick its widget, and `Hud.SubtitleBuffer` is literally the same functions bound to a
table with a different `sName`), and **each takes one table** of named fields rather than positional
arguments.

Argument-guard failures on this page report through `Ess.Safe.reject`, which is silent unless `Ess.DEBUG` is
on — see [Core Primitives](core#essdebug--two-channels-of-silence).

## Ess.Sound

The raw one-shot sound-effect/ambience layer, wrapping the `Sound` engine namespace's confirmed
direct-cueing primitives (see [Sound](../namespaces/sound) for the full native namespace). Distinct from
music: `Ess.Contract`'s `music` support effect already wraps the higher-level dynamic-music state
machine — this is the "just play a sound effect" layer every mod eventually needs.

| Function | Signature | What it does |
|---|---|---|
| `cue` | `Ess.Sound.cue(uGuidOrNil, sCueName)` | `Sound.CueSound` — attach a sound to an object, or `nil`/0 for a UI/HUD one-shot. |
| `stop` | `Ess.Sound.stop(uGuidOrNil, sCueName)` | `Sound.StopSound` — must match the `(uGuid, sCueName)` pair a prior `cue` used. |
| `ambience` | `Ess.Sound.ambience(sStreamName)` | `Sound.CueAmbience`. |
| `stopAmbience` | `Ess.Sound.stopAmbience(sStreamName)` | `Sound.StopAmbience`. |
| `volume` | `Ess.Sound.volume(nLevel, nFadeTime)` | `Sound.SetMasterVolume`. |

**`cue(uGuidOrNil, sCueName)`** follows the confirmed pattern documented on the
[Sound namespace page](../namespaces/sound): a real object guid attaches the sound to that object (an
alarm on a building); `nil`/`0` is the convention used throughout the shipped UI code
(`mrxguidialogbox.lua` etc.) for a plain UI/HUD one-shot with no world position. It rejects a blank or
non-string cue name and logs through `Ess.Log` if the underlying `Sound.CueSound` call fails.

**`stop`** must be called with the same `(uGuid, sCueName)` pair a prior `cue` used, matching every
confirmed real call site on the Sound namespace page.

**`volume(nLevel, nFadeTime)`** — `nLevel` is observed as `0`/`1` at every confirmed real call site (not
necessarily a continuous 0..1 float range beyond that), `nFadeTime` in seconds, defaulting to 0.

`Ess.Easy.Sound.play(sCueName)` is the zero-config version — a plain UI one-shot, no guid/opts to think
about (it's just `Ess.Sound.cue(nil, sCueName)`). See [Ess.Easy](easy).

### Cue validation

**A mistyped cue name is completely silent.** `Sound.CueSound` raises nothing, returns nothing and logs
nothing for a name the engine can't resolve — the call simply produces no audio, and looks identical to a
call that worked on a machine with the speakers off. These three functions are the only way to catch that.

| Function | Signature | What it does |
|---|---|---|
| `duration` | `Ess.Sound.duration(sCue)` | `Sound.GetMaxDuration`, normalised. Returns seconds, `-1`, or `nil`. |
| `isCue` | `Ess.Sound.isCue(sCue)` | `duration(sCue) ~= nil` — can the engine resolve this name *right now*. |
| `isLooping` | `Ess.Sound.isLooping(sCue)` | `duration(sCue) == -1` — a cue with no fixed length. |

`duration` has three return cases, and the third is the one that matters:

| Return | Meaning |
|---|---|
| `> 0` | A real, currently-resolvable cue, and this is its length in seconds. |
| `-1` | A real cue with **no fixed length** — a loop. Measured on an alarm cue. |
| `nil` | Not resolvable: either the name is wrong, **or its bank is not loaded right now**. |

That last case is why this is **not quite an existence test**. The engine returns `0` for an unresolvable
cue, normalised to `nil` here because `0` would otherwise read as "a zero-length sound". A cue that is real
but whose bank has not streamed in is indistinguishable from a typo — confirmed during the 0.5.0 pass:
several cues the shipped scripts definitely use returned `0`, while others returned real durations. So a
`nil` means *"cannot answer"*, not *"does not exist"*, and a `false` from `isCue` is a reason to go and look
rather than proof of a typo.

**`isLooping`** is worth checking before cueing something you don't intend to stop: a loop runs until
`Ess.Sound.stop` is called with the same `(guid, cue)` pair.

```lua
local sCue = "amb_alarm_loop_" .. sVariant       -- a name built at runtime
if not Ess.Sound.isCue(sCue) then
    Ess.Log("no such cue (or its bank isn't loaded): " .. sCue)
elseif Ess.Sound.isLooping(sCue) then
    Ess.Sound.cue(uBuilding, sCue)               -- remember to stop it later
end
```

Everything in this subsection and the next was verified through **getters**, not by ear — the point of the
0.5.0 audio pass was that audio is the one area where the person (or agent) writing the wrapper can't check
their own work, and most of it turned out to be answerable from `Sound`'s real getters.

### The category mixer

| Function | Signature | What it does |
|---|---|---|
| `CATEGORIES` | `Ess.Sound.CATEGORIES` | The four real categories: `sfx`, `music`, `ambience`, `vo`. |
| `categoryVolume` | `Ess.Sound.categoryVolume(sCat)` | `Sound.GetCategoryVolume` — the **effective** volume (own level × parent), or `nil`. |
| `setCategoryVolume` | `Ess.Sound.setCategoryVolume(sCat, nLevel)` | `Sound.SetCategoryVolume` — sets the category's **own** level, 0..1. |
| `categoryPitch` | `Ess.Sound.categoryPitch(sCat)` | `Sound.GetCategoryPitch`. |
| `setCategoryPitch` | `Ess.Sound.setCategoryPitch(sCat, nPitch)` | `Sound.SetCategoryPitch`; `1` = normal. |
| `duck` | `Ess.Sound.duck(sCat, nLevel, nFade)` | `Sound.FadeCategoryDown`; `nLevel` defaults to 0.2, `nFade` to 0.5 s. |
| `unduck` | `Ess.Sound.unduck(sCat, nFade)` | `Sound.FadeCategoryUp`; `nFade` defaults to 0.5 s. |
| `clearDucking` | `Ess.Sound.clearDucking()` | `Sound.ClearFadeCategories` **and** `Sound.ClearPitchCategories`. |
| `info` | `Ess.Sound.info()` | A snapshot table: lib version, audio dir, music flags, and all four category volumes. |

**Get and set are not symmetric, and the categories nest.** This is the trap. `GetCategoryVolume` returns
the *effective* volume — the category's own level multiplied by its parent's — while `SetCategoryVolume`
sets the category's *own* level. Setting `ambience` to `0.42` and reading back `0.3148` is not a failed
write; it is 0.42 × its parent. The measured shape, from setting each category and watching what moved:

- `music` and `vo` are **top level**. Set `music` to 0.5 and it reads back exactly 0.5.
- `ambience` is a **child of `sfx`**. Its own level is 1.0 by default, which is why it normally reads the
  same as `sfx`; ducking `sfx` to 0.15 dragged `ambience` to 0.1499 with it, while `music` did not move.

**Never restore a category to a remembered *reading*.** Reading `ambience` as 0.7495 and writing 0.7495
back sets its own level to 0.7495 and leaves it audibly quieter than it started. Restoring own-level `1.0`
reproduced the original reading to the last digit. Remember what you **set**, or reset to 1.0.

**A setter's effect is not visible until the next frame.** Set-then-get in one chunk always returns the old
value. This cost a wrong conclusion during the 0.5.0 sweep — `SetCategoryVolume` and the whole fade path
were written off as inert on exactly that evidence, and both work fine when sampled a frame later. Never
verify an audio write in the chunk that made it.

**Fades are a stack, not a level.** Each `duck()` pushes one and each `unduck()` pops one, so three ducks
and one unduck leaves the category two levels down with no obvious way back. That is why `duck`/`unduck` are
named as a pair and why `clearDucking()` exists.

**`info()`** returns a table with `nLibVersion` (12 on this build; `mrxmusic` gates features on `>= 11`),
`sAudioDir` (`.\Data\Audios`), the three music-mode flags `bDynamicMusic` / `bFactionLocked` /
`bActionLocked`, and one key per category (`sfx`, `music`, `ambience`, `vo`) holding that category's
effective volume. Any field whose getter fails is simply absent rather than `nil`-filled.

The dynamic-music state machine is deliberately **not** wrapped here: it is the bulk of the `Sound`
namespace by call sites and is already wrapped at a higher level by the resident `MrxMusic` module, and by
`Ess.Contract`'s own `music` support effect.

## Ess.Hud

Seventeen verbs across five widgets: the tutorial-hint popup, the fanfare banner, the animated title and
region card, the message box, and the objective tray — plus the cash/fuel readouts. Grouped with prose in
the subsections below.

| Function | Signature | What it does |
|---|---|---|
| `hint` | `Ess.Hud.hint(sMsg, sId, bBroadcast)` | The native tutorial-style hint popup (icon + sound); stays up until hidden. |
| `hideHint` | `Ess.Hud.hideHint(sId, bBroadcast)` | Clears a hint shown with a matching `sId`. |
| `banner` | `Ess.Hud.banner(sMsg)` | A clean, icon-free, centered text banner. |
| `title` | `Ess.Hud.title(sText, nDur, tOpts)` | The stylised **animated** title overlay (`text_effect.swf`). `nDur` in s, default 3. |
| `location` | `Ess.Hud.location(sText, nDur)` | The region-name card ("Playa del Este"-style). `nDur` in s, default 10. |
| `message` | `Ess.Hud.message(sText, tOpts)` | Adds a line to the message box; returns a handle. **Negative duration = permanent.** |
| `updateMessage` | `Ess.Hud.updateMessage(handle, sText)` | Edits a message that is still **queued** — see the caveat below. |
| `removeMessage` | `Ess.Hud.removeMessage(handle)` | Removes a still-queued message. |
| `clearMessages` | `Ess.Hud.clearMessages()` | Wipes the message box, visible **and** queued. |
| `tutorial` | `Ess.Hud.tutorial(sText)` | The bare tutorial text strip. **Sticky** — pass `nil` to clear. |
| `objective` | `Ess.Hud.objective(sText, nSlot)` | Sets the objective-tray line at `nSlot` (default 1); `nil` `sText` clears that slot. |
| `radio` | `Ess.Hud.radio(sText, nHold)` | A transient radio-chatter subtitle in slot 3, self-clearing after `nHold` s (default 5). |
| `image` | `Ess.Hud.image(sTexture, nSlot, nW, nH)` | Puts an image in an objective-tray slot instead of text (`nSlot` default 1). |
| `cash` | `Ess.Hud.cash(nValue, tOpts)` | Moves the on-screen cash readout. **Display only.** |
| `fuel` | `Ess.Hud.fuel(nValue, nMax)` | Moves the on-screen fuel readout. **Display only.** |
| `resources` | `Ess.Hud.resources(bShow, nDur)` | Shows (for `nDur` s, default 3) or hides the cash+fuel readouts. |
| `suppressResources` | `Ess.Hud.suppressResources(bCash, bFuel)` | The game's own "hide these during a cutscene" switch, per counter. |

`Ess.Hud.RADAR_ICONS` is also exposed here: the minimap's 23-name icon vocabulary, read from `mrxutil.lua`'s
fixed `tObjRadarMaker` lookup table. It is a **closed set** — `MrxUtil.MarkerGetIndexByName_Radar` does a
linear search of that exact table and returns 0 for anything else. It is the radar counterpart to
`Ess.Pda.ICONS`, and it is what [Ess.Mark](mark)'s radar layer draws from.

### The hint popup and the banner

**`hint(sMsg, sId, bBroadcast)`** wraps `MrxTutorialManager.ShowMessage` — the same "you're swimming" /
"low on fuel" popup the game shows for its own tutorials turns out to be a completely generic, reusable
primitive underneath. **Confirmed by live testing with a screenshot**
(see [Snippets: Show a custom HUD message](../snippets#show-a-custom-hud-message-with-icon-and-sound)).
No auto-hide timer; it stays up until `hideHint` is called with a *matching* `sId` — a different or
missing id does not clear it, confirmed by live testing, which is useful when more than one script might
show a message at once. It's local-only by default (`bBroadcast` omitted/false); pass `bBroadcast=true` to
opt into the native's own co-op broadcast, whose actual network behavior is unconfirmed here (confirming
it needs a second player) — the safer local-only default was chosen deliberately, instead of matching the
native's own default-to-broadcast behavior.

**`banner(sMsg)`** is the confirmed live-tested trick documented in full on the
[Hud namespace page](../namespaces/hud#eventfanfare-stype-catalog-and-the-custom-toast-trick):
`Hud.EventFanfare:Commence` gates on `sType` being a key in `MrxGuiHudMessage._tEventTextures`, a table
declared without `local` and therefore writable via `import("MrxGuiHudMessage")`. `Ess.Hud.banner`
registers one extra key (`custom`, pointing at a texture name that doesn't correspond to any real loaded
asset) once, then commences a fanfare with `sType = "custom"`. A texture that doesn't resolve produces no
icon and no gold header — just `vText` centered on screen, confirmed by live testing. The 9 real `sType`
values (`contact`/`support`/`stockpile`/etc., already used by `Ess.Contract`'s own fanfare) are untouched
by this.

### Text overlays

**`title(sText, nDuration, tOpts)`** is the nicest-looking text primitive the game has: it loads
`text_effect.swf`, so it **animates** in and out rather than just appearing. Returns `true`, or `false` if
`sText` isn't a non-empty string.

Positioning works in a **640×480 virtual space** — not screen pixels, and not a 0..1 fraction. `nY = 240`
is the vertical middle, and the widget clamps the resolved value to `0..450`. Horizontal position is not
yours to set: `DisplayClassyText` overwrites whatever `nX` it is handed with a centred value
(`nX = (640 - 566.6667) * 0.5`) on its very first line, so the box is always centred and 566.67 wide;
`sJustification` only decides how the text sits *inside* that fixed box.

| `tOpts` field | Default | Meaning |
|---|---|---|
| `nY` | `240` (middle) | 0..450 in the 640×480 virtual space. Small numbers are near the top. |
| `sJustify` | `"center"` | `"center"` / `"left"` / `"right"`. The **engine's** own default is `"left"`; this wrapper overrides it, because centred is almost always what a title wants. |
| `sVertAnchor` | `"center"` | `"center"` / `"bottom"` / anything else = top. Decides what `nY` measures *to*. |
| `bExpand` | `false` | Passed straight through to the Flash movie. |

`nDuration` is in seconds (default 3) and is multiplied by 30 internally, so the movie is frame-timed.

**`location(sText, nDuration)`** is the region-name banner the game shows when you cross into a named area.
It is purely cosmetic and takes arbitrary text, so it doubles as a chapter/act card. `nDuration` is in
seconds and defaults to **10** in the wrapper — `Hud.MapLabel:Show` passes it straight to the widget
without a default of its own.

**`tutorial(sText)`** is the bare tutorial text strip. It is **sticky**: unlike every other text primitive
on this page there is no duration parameter, because the wrapper just calls `oWidget:SetText` and returns.
It stays until something clears it, *including* across whatever else you do — confirmed live. Pass `nil`
(or a blank string) to clear it, which is the game's own idiom.

`tutorial` is distinct from `hint`: `hint` goes through `MrxTutorialManager` and gets the popup chrome, the
icon and the notification sound; `tutorial` is the text strip with none of that. `Hud.Tutorial`'s other two
functions (`ShowTutorialOnscreen`, `ShowTutorialForObject`) are deliberately **not** wrapped — they are
broken in the shipped script for any explicit `vPlayer` (a userdata player builds an empty target list and
silently no-ops; a table player reads an undeclared global and errors inside `pairs(nil)`), only the
omitted-player path works, and nothing in the corpus ever called them.

### The message box

`Ess.Hud.message` adds a line to the notification stack the game itself uses for "Checkpoint reached",
support denials and so on. It returns the `tMessageIds` handle (a table keyed by widget owner), or `nil` if
the call was rejected.

| `tOpts` field | Default | Meaning |
|---|---|---|
| `nDuration` | `2` s | **A negative value means PERMANENT.** |
| `nPriority` | `5` | 0..5. Out-of-range values are silently clamped to 5; `0` takes a separate high-priority path in the widget that can cut short whatever is already on screen. |
| `nFade` | `0.25` s | Fade time. |
| `bClearBuffer` | off | Clear everything else when this one displays. |
| `bAppends` | `true` | Whether this message allows appends. |
| `fCallback` / `tCallbackData` | none | A real Lua callback, invoked by the widget. |

Only `nDuration` is defaulted by the Ess wrapper; the rest are passed through as `nil` and the widget's own
`ValidateParameter` defaults (listed above) apply.

**Negative duration means permanent.** `AddMessage` turns any `nDisplayDuration < 0` into a display
duration of 10000 *plus* a `bPersistent` flag, so the line stays until it is removed by hand. That is a
genuine engine behaviour, confirmed in `mrxguitextbuffer.lua`, not a convention Ess invented:

```lua
local h = Ess.Hud.message("HOLD POSITION", { nDuration = -1 })   -- stays until removed
-- ... later ...
Ess.Hud.clearMessages()
```

**`updateMessage(handle, sText)` only works while the message is still queued — read this before relying on
it.** The native is `ModifyPendingMessage` and it means "pending" literally: it searches the widget's
`PendingMessages` queue, so a message that has already reached the screen has moved to `CurrentMessages`
and cannot be found. You get a plain `false` with no other signal. Measured: adding one message to an empty
box displays it immediately, so the very next `updateMessage` call returns `false`. It is genuinely useful
for editing a line queued *behind* a busy stack — which is exactly what the game uses it for — and it is
not a general "change that text". To replace a visible line, remove it and add a new one.

`removeMessage(handle)` carries the same pending-only constraint. Note that it returns `true` once the
handle passes its type check; it does **not** report whether a message was actually found and removed.
`clearMessages()` has no pending caveat at all — it wipes visible and queued lines alike.

### The objective tray

**`objective(sText, nSlot)`** drives `Hud.ObjectiveTray` (`SetSlotToText`/`ClearSlot`) — exactly what
`Ess.Contract` drives its own objective line with, promoted here so any mission/mod can set the HUD
objective without reaching into Contract or re-deriving the shape. `nSlot` defaults to 1 (the "current
objective" line); it exists so a goal-tracking system built on a different tray slot can show its own line
without fighting a running Contract for slot 1 — see [Objectives & Quests](objectives), which uses exactly
that. `nil` `sText` clears the slot.

**`radio(sText, nHold)`** uses `Hud.ObjectiveTray` slot 3 as a transient "radio chatter" subtitle — the
game's own one-off mission-chatter line, and the natural fit for cutscene dialogue/subtitles. It
self-clears after `nHold` seconds via a generation counter: a newer `radio()` call bumps the generation, so
an older line's pending clear-timer won't wipe out a message that superseded it — an improvement over
`Ess.Contract`'s own `hudSay`, which can suffer exactly that race.

**`image(sTexture, nSlot, nW, nH)`** puts an image in a tray slot instead of text, using the same slot
numbering (1 = the current-objective line, 3 = the radio line). `nW`/`nH` are optional and passed straight
through to `SetSlotToImage`. Setting an image and setting text target the same slot, so they replace each
other.

### The resource readouts are display only

**`Ess.Hud.cash` and `Ess.Hud.fuel` do not change the player's money or fuel.** They write the widget, not
the save. The player's real cash and fuel are untouched, and the next genuine change overwrites whatever
you set. This is worth stating loudly because the function names read like setters and they are not: a
mission that "awards" $5,000 with `Ess.Hud.cash(nOld + 5000)` has awarded nothing.

That is the same asymmetry recorded for the economy setters, running the other way: `Ess.Player.giveCash`
routes through `MrxPmc` so the number and the HUD agree, while `Player.SetCash` moves the money without
telling the HUD. These move the HUD without touching the money. Use them for a *fake* readout — a heist
countdown, a fuel-siphon set piece, a mock economy for a custom mode — and use the economy layer for real
money.

| Call | Effect |
|---|---|
| `Ess.Hud.cash(nValue, tOpts)` | `tOpts.sReason` shows the game's own "+$500 (reason)" annotation; `tOpts.nIncrement` drives the roll-up animation. |
| `Ess.Hud.fuel(nValue, nMax)` | `nMax` is an undocumented extra the corpus never used: it appends `"/max"` to the readout. |
| `Ess.Hud.resources(bShow, nDur)` | Shows for `nDur` seconds (default 3), or hides indefinitely. |
| `Ess.Hud.suppressResources(bCash, bFuel)` | The cutscene-suppression switch, independently settable per counter and separate from show/hide. |

Two details from the source worth knowing, both read from `mrxguiinterface.lua` rather than tested live:

- **Only an explicit `false` hides.** `Ess.Hud.resources` tests `bShow == false`, so `resources()` or
  `resources(nil)` *shows* the readouts rather than hiding them.
- **Setting a value re-shows the readout.** `SetCash` and `SetFuel` both call `oWidget:Show()` after
  writing, so a `cash()` or `fuel()` call after `resources(false)` brings the counter back on screen.

`Ess.Hud.fuel` does not expose the native's `nIncrement` roll-up, which `SetFuel` accepts; `Ess.Hud.cash`
does, via `tOpts.nIncrement`.

### Choosing a notification style

A real usage from the sample catalog — the four notification styles and when to reach for each:

```lua
Ess.Easy.Toast("Pickup collected")            -- a small custom-UI toast, auto-dismisses (a pickup, a small event)
Ess.Hud.banner("Area Cleared")                -- a big centered fanfare-style banner (a milestone)
Ess.Hud.objective("Objective: reach the LZ")  -- the persistent objective-tray line (the current task)
Ess.Hud.radio("\"On my way, over.\"", 4)      -- a self-clearing lower-third subtitle (radio chatter / dialogue)

Ess.Easy.Triggers.after(5, function() Ess.Hud.objective(nil) end)   -- clear the objective line again
```

Add `Ess.Hud.title` for an animated act/chapter card, `Ess.Hud.location` for a region card, and
`Ess.Hud.message` for a stackable notification line that can be made permanent.

## Ess.Hud.Faction

A sub-table rather than eight more flat `Ess.Hud` verbs, because this is one coherent widget: a row of
labelled gauges, each belonging to a faction, that can show a value, flip into a red **pursuit** state, or
run a **timer**. The timer is the reason to care — it is the only on-screen countdown the game exposes, it
comes with real HUD chrome, and it fires a Lua callback when it expires.

| Function | Signature | What it does |
|---|---|---|
| `add` | `Ess.Hud.Faction.add(sFaction, sTexture)` | Puts a meter on screen for that faction. `sTexture` is the marker icon beside it. |
| `set` | `Ess.Hud.Faction.set(sFaction, nValue, bInit)` | Sets the meter, 0..100. `bInit` snaps instead of animating. |
| `timer` | `Ess.Hud.Faction.timer(sFaction, nSeconds, fn)` | The on-screen countdown. `fn()` fires once on expiry. |
| `pursuit` | `Ess.Hud.Faction.pursuit(sFaction, nSeconds, fn)` | The red "you are being hunted" gauge. `fn()` on completion. |
| `inZone` | `Ess.Hud.Faction.inZone(sFaction, bInside, bInit)` | Marks the player as inside that faction's territory (how the game highlights the relevant meter at a border). |
| `hide` | `Ess.Hud.Faction.hide(sFaction)` | Hides one meter. The real teardown, since `RemoveMeter` is a no-op. |
| `levels` | `Ess.Hud.Faction.levels(tThresholds, tNames, sPursuitName, bShow)` | Redefines the level bands. **Global and destructive** — see below. |
| `restoreLevels` | `Ess.Hud.Faction.restoreLevels()` | Puts the game's own level vocabulary back. |

Four constants come with it: `Ess.Hud.Faction.RANGE` (`nMin = 0`, `nMax = 100`),
`Ess.Hud.Faction.STOCK_THRESHOLDS` (`0, 25, 50, 75`), `Ess.Hud.Faction.STOCK_NAMES` and
`Ess.Hud.Faction.STOCK_PURSUIT` — the stock level vocabulary, copied verbatim from
`mrxguihudfactiongauge.lua` (the thresholds and names from its `Init()`, the pursuit label from its
module-level `_ksPursuit`).

**Values are 0..100.** `mrxguihudfactiongauge.lua` fixes `_knMin = 0` and `_knMax = 100`, and the bar maths
divides by the gap between thresholds, so feeding it a relation value straight from `Ess.Relations` will not
do — the game converts first, via `ConvertRelationToMeterValue`. `set` passes out-of-range values through
rather than clamping them, because the widget's own level maths treats the ends as open and clamping in the
wrapper would silently disagree with it.

**Setting a value above zero cancels an active pursuit** — `SetValue` calls `StopPursuit` when
`bPursuitActive` and `nValue > _knMin`. So don't drive a meter's value while its pursuit is running unless
ending it is what you meant.

`sFaction` is a faction code (`PMC`/`AN`/`CH`/`GR`/`OC`/`PR`/`VZ`). Note that the wrapper's guard only
checks for a non-empty string — it does not validate the code against that list, so a typo'd faction reaches
the widget.

**Three functions are deliberately not wrapped, because they are dead** — callable, returning `nil`, doing
nothing: `Hud.FactionDisplay.RemoveMeter` and `.RemoveAllMeters` (empty bodies in `mrxguiinterface.lua`;
use `hide()`, which is real), and `ShowAll` behind `Hud.FactionDisplay:Show` (the whole body in
`mrxguihudfactionbuffer.lua` is `function ShowAll(oWidget, nDuration) end`). An `Ess.Hud.Faction.show`
existed briefly and was withdrawn on measurement: it reported success and the meters still vanished,
because there was never any code behind it.

### The countdown timer

`Ess.Hud.Faction.timer(sFaction, nSeconds, fn)` is the only on-screen countdown the game exposes, and it
renders with real HUD chrome — a native-looking presentation for anything on a clock (defuse this, survive
this, reach it before the convoy) in about four lines. **Verified live:** the timer displayed, counted down,
fired, and its callback drove other Ess UI.

```lua
Ess.Hud.Faction.add("PMC")
Ess.Hud.Faction.timer("PMC", 30, function()
    Ess.Hud.banner("Out of time")
end)
```

Three constraints, all read from the widget source:

- **`nSeconds` must be positive.** Zero or negative is rejected with a reason.
- **The callback takes no arguments and fires once.** `_TimerCallback` unpacks only the callback data —
  which this passes none of, as everywhere else in Ess — and clears the stored callback before calling it.
- **The timer cannot be stopped through this namespace.** The widget *has* a `StopTimer`, but
  `Hud.FactionDisplay` never wraps it: ten functions, and that is not one of them. Starting a new timer on
  the same faction is the only way to displace a running one. (The widget's own `StopTimer` is mildly
  broken anyway — it calls `oTimer:Stop(nTime)` where `nTime` is an undeclared global.)

### The pursuit gauge

`Ess.Hud.Faction.pursuit(sFaction, nSeconds, fn)` is the red "you are being hunted" gauge. Pass
`nSeconds <= 0` (or omit it) for an indefinite pursuit with no callback, which is what the game does for a
pursuit that ends on an event rather than a clock.

**It fills, it does not drain** — confirmed on screen, and the source agrees: `StartPursuitGauge` first
snaps the bar to empty (`AnimateToPoint(nGaugeFrontEmptyPoint, 0, true)`) and then `_AnimateToEnd` animates
it out to the full gauge length over `nSeconds`. So it reads as a threat closing in rather than a timer
running out, which is the opposite of what "pursuit duration" suggests. This was documented backwards
initially and corrected from a screenshot.

This is a **display** widget. It visualises a pursuit; it does not create one. The actual wanted/heat
system — `Ess.Pursuit.start`, `state`, `level`, `clear`, the level ratchet and the restriction switches —
lives on [Pursuit & Wanted System](pursuit), and nothing on this page reads or writes it. Driving the gauge
from real pursuit state is your job:

```lua
Ess.Hud.Faction.add("AN")
Ess.Hud.Faction.pursuit("AN", 20, function()
    Ess.Hud.radio("\"They've got a fix on us.\"", 4)
end)
```

### Meters are transient by design

**A meter expires on its own about five seconds after its last update, and cannot be pinned open.**
`mrxguihudfactionbuffer.lua` gives each occupied slot a life that counts down every frame; a timer sets it
to `5 + the timer's duration` and a pursuit to `2 + its duration`. At zero the gauge slides out and frees
its slot, unless a pursuit is still running, which extends it.

This is a finding rather than an omission, and it was measured rather than assumed. The obvious workaround —
re-set the meter's value on a timer just under the ~5-second slot life, the way `Ess.Easy.World` holds an
atmosphere against the region system — was **built and then withdrawn**: a keeper refreshing every 3 seconds
against a ~5-second life, with both loops verified firing (4 refreshes in 12 seconds against a running tick
loop), still let the meter expire on schedule. So whatever actually renews a slot is not reachable through
`SetValue`, despite the buffer's `SetValue` path appearing to set `tSlotLife = math.max(5, remaining)`.

Combined with `Hud.FactionDisplay:Show` being an empty function, that makes the faction meters inherently
transient: they exist to flash up in response to something and then leave. Design around it. `timer` and
`pursuit` both hold the meter for their own duration, and that is the supported way to keep one up for a
known period.

### Rewriting the level vocabulary

**`Ess.Hud.Faction.levels` is global and destructive. Read this before calling it.**

It does not configure "your" meter. `SetLevels` writes the module-level `_tLevels` and `_tLevelNames` in
`mrxguihudfactiongauge.lua`, and **every** gauge reads those — including the game's own. A live test set
`ESS CALM` / `ESS EDGY` / `ESS ANGRY` / `ESS FURIOUS`, and Universal Petroleum's own faction meter
subsequently rendered "ESS FURIOUS" as its mood. The player's faction-standing display is simply wrong from
then on, for every faction, until the level reloads. This was caught from a screenshot, not from the code.

The stock names are localisation **tokens** (`[0x671b379b]` and friends) rather than English, which is
exactly why the real meters render proper faction moods from them and why substituting readable text breaks
them. There is no getter, so the previous vocabulary cannot be captured and restored generically — the only
recovery is knowing the stock values, which is why `STOCK_THRESHOLDS` / `STOCK_NAMES` / `STOCK_PURSUIT` are
recorded as constants and `Ess.Hud.Faction.restoreLevels()` exists. The thresholds are less dangerous than
the names (a value still lands in *some* band) but they are equally global, so a custom scale silently
rescales the real meters too.

So: do not call `levels()` to label a meter of your own. Use it only when you deliberately intend to
restyle the game's entire faction vocabulary, and restore it when you are done. A mod that just wants a
countdown or a gauge needs none of this — `timer`, `set` and `pursuit` don't touch it.

`restoreLevels()` is always available and always correct, because the stock values are constants rather than
something captured at runtime. Note that the meters do not repaint until something updates them, so a gauge
already showing a custom mood keeps that text until its next `set`/`timer`/`pursuit`; call `set()` on
anything visible to force it through.

`levels(tThresholds, tNames, sPursuitName, bShow)` takes ascending numbers **starting at 0** and a
same-length name list. The native validates hard and returns a bare `false` on a non-number threshold, a
non-string name, a first threshold that is not 0, or mismatched lengths; the wrapper checks those four
first so the failure arrives with a reason. It *looks* like the native validates ascending order too, and
it does not: that check compares every threshold against an `nPrevLevel` initialised to `-1` and never
updated inside the loop, so it can only ever fire for a value below `-1`. Descending or duplicate
thresholds sail through and produce a gauge whose level maths divides by a negative or zero range — so the
wrapper performs the ordering check the engine intended. `bShow` is forwarded as the native's
`bDisplayResult`; what it actually renders is undocumented even in the widget source, so treat it as an
experiment rather than a supported option.

## See also

- [Essentials (Ess)](index) — the framework index.
- [Ess.Easy](easy) — `Ess.Easy.Sound.play`, `Ess.Easy.Toast`, and every other namespace's one-liner tier.
- [Pursuit & Wanted System](pursuit) — the real wanted/heat system the pursuit gauge only *visualises*.
- [Objectives & Quests](objectives) — the stateful goal tracker built on `Ess.Hud.objective`.
- [Ess.UI](ui) — the custom `.gfx` widget kit, the other half of the on-screen story.
- [Sound](../namespaces/sound), [Hud](../namespaces/hud) — the raw engine namespaces underneath.
- [Snippets](../snippets) — the live-tested screenshot confirmation for the tutorial-hint trick.
