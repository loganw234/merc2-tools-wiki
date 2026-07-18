---
title: Sound & HUD
parent: Essentials (Ess)
nav_order: 8
---

# Sound & HUD

## Overview

`Ess.Sound` and `Ess.Hud` cover getting the player's attention: a direct one-shot sound/ambience cueing
layer, and native HUD popups (hint, banner, objective tray, radio subtitle) built on confirmed-working
resident-module patterns instead of a hand-rolled custom widget. Part of [Essentials (Ess)](index).

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

## Ess.Hud

Native HUD popups, using confirmed-working resident-module patterns instead of a hand-rolled custom
widget — distinct from `Ess.UI.Toast` (a custom `.gfx` movie widget); these drive the game's own built-in
popup chrome. See [Hud](../namespaces/hud) for the raw sub-namespaces underneath (`Hud.Tutorial`,
`Hud.EventFanfare`, `Hud.ObjectiveTray`).

| Function | Signature | What it does |
|---|---|---|
| `hint` | `Ess.Hud.hint(sMsg, sId, bBroadcast)` | The native tutorial-style hint popup (icon + sound); stays up until hidden. |
| `hideHint` | `Ess.Hud.hideHint(sId, bBroadcast)` | Clears a hint shown with a matching `sId`. |
| `banner` | `Ess.Hud.banner(sMsg)` | A clean, icon-free, centered text banner. |
| `objective` | `Ess.Hud.objective(sText, nSlot=1)` | Sets the objective-tray line at `nSlot`; `nil` `sText` clears that slot. |
| `radio` | `Ess.Hud.radio(sText, nHold)` | A transient radio-chatter subtitle, self-clearing after `nHold` s (default 5). |

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

**`objective(sText, nSlot=1)`** drives `Hud.ObjectiveTray` (`SetSlotToText`/`ClearSlot`) — exactly what
`Ess.Contract` drives its own objective line with, promoted here so any mission/mod can set the HUD
objective without reaching into Contract or re-deriving the shape. `nSlot` defaults to 1 (the "current
objective" line, unchanged from before); it's a new, backward-compatible parameter that exists so a
goal-tracking system built on a different tray slot can show its own line without fighting a running
Contract for slot 1. `nil` `sText` clears that slot. Written and internally consistent, not yet confirmed
via live testing.

**`radio(sText, nHold)`** uses `Hud.ObjectiveTray` slot 3 as a transient "radio chatter" subtitle — the
game's own one-off mission-chatter line, and the natural fit for cutscene dialogue/subtitles. It
self-clears after `nHold` seconds via a generation counter: a newer `radio()` call bumps the generation, so
an older line's pending clear-timer won't wipe out a message that superseded it — an improvement over
`Ess.Contract`'s own `hudSay`, which can suffer exactly that race.

A real usage from the sample catalog — the four notification styles and when to reach for each:

```lua
Ess.Easy.Toast("Pickup collected")            -- a small custom-UI toast, auto-dismisses (a pickup, a small event)
Ess.Hud.banner("Area Cleared")                -- a big centered fanfare-style banner (a milestone)
Ess.Hud.objective("Objective: reach the LZ")  -- the persistent objective-tray line (the current task)
Ess.Hud.radio("\"On my way, over.\"", 4)      -- a self-clearing lower-third subtitle (radio chatter / dialogue)

Ess.Easy.Triggers.after(5, function() Ess.Hud.objective(nil) end)   -- clear the objective line again
```

## See also

- [Essentials (Ess)](index) — the framework index.
- [Ess.Easy](easy) — `Ess.Easy.Sound.play`, `Ess.Easy.Toast`, and every other namespace's one-liner tier.
- [Sound](../namespaces/sound), [Hud](../namespaces/hud) — the raw engine namespaces underneath.
- [Snippets](../snippets) — the live-tested screenshot confirmation for the tutorial-hint trick.
