---
title: Marker
parent: Engine Namespaces
nav_order: 17
---

# Marker

## Overview

`Marker` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it, no
`import()` call needed, and it's always globally available to every script. It manages minimap/radar blips
and in-world markers (discs, tripwires, 3D icons) attached to object `uGuid`s or raw world coordinates. It is
very likely a thin public wrapper around a set of underscore-prefixed internal primitives on
[`Gui`](gui#internal-marker-primitives) (`Gui._MarkerAdd`, `Gui._MarkerRemove`, etc.) — see that page for the
detailed 1:1 naming-correspondence analysis; this page only cross-links it rather than repeating it.

## Provenance

This page's function list comes from a live `pairs(Marker)` enumeration in-game (via lua-bridge), not from
reading engine source — the engine implementation isn't available to us. That means the list of 13 function
names below is complete and authoritative: every one of them really exists on the namespace. It does **not**
mean every entry is documented with confirmed arguments. Where a function is actually called somewhere in
the ~230 decompiled `.lua` scripts, we can show a real argument pattern. Where it isn't called anywhere in
that corpus, we only know the name — arguments, return values, and behavior for those are unconfirmed.

`AddBlip` is the one function on this page backed by an actual **live in-game test**, not just source
call-site evidence — see [Snippets: put a marker/blip on an object](../snippets#put-a-marker-blip-on-an-object)
for the tested call, the caveat about the trailing numeric arguments not being individually confirmed, and a
note about blip visibility at ground level. It is cross-linked here rather than re-derived.

## Functions

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Add` | `uMarker = Marker.Add(nOffsetX, nOffsetY, nOffsetZ, uGuid, nR, nG, nB, nRadius)` | Confirmed in real scripts, e.g. `tTargetData.uMarker = Marker.Add(0, 2, 0, uGuid, r, g, b, 0.05)` (`mrxtaskobjectivedeliver.lua`) — an offset vector, then a target `uGuid`, then RGB color and a radius-looking final value. Returns a marker handle later passed to `Remove`. |
| `Add3D` | `uMarker = Marker.Add3D(uGuid, sIconName, nR, nG, nB [, nWidth])` | Confirmed in real scripts, e.g. `Marker.Add3D(uGuid, "global_tripwirefinish", r, g, b)` and `Marker.Add3D(uGuid, "global_airring", r, g, b, fWidth)` (`mrxtaskrace.lua`) — a `uGuid`, an icon/model name string, RGB color, and an optional trailing width value (only seen on the `"global_airring"` call). |
| `AddBlip` | `uMarker = Marker.AddBlip(uGuid, sTextureName, nSize, nR, nG, nB, nAlpha, ...)` | **Confirmed working by live testing** — see [Snippets](../snippets#put-a-marker-blip-on-an-object). Also used extensively in real scripts, e.g. `Marker.AddBlip(uGuid, tFactionData.sMarkerTexture, 32, 255, 255, 255, 255, 2, nil, nil, 32, nil, true)` (`mrxfactionmanager.lua`) — a longer argument list than the snippet's tested call, with `nil` gaps, meaning the full parameter set (beyond texture/size/RGBA) is still not individually confirmed. |
| `AddDisc` | `uMarker = Marker.AddDisc(uGuidOrLocation, nRadius, nR, nG, nB, nThickness)` | Confirmed in real scripts, e.g. `Marker.AddDisc(Pg.GetGuidByName("PmcCon013_Loc"), nRadius, 255, 200, 0, 0.25)` (`pmccon013.lua`) and `Marker.AddDisc(uGuid, 0.5, disc_r, disc_g, disc_b, 0.1)` (`wifpmcinterior.lua`, `mrxhq.lua`). One call site passes a location vector directly instead of a `uGuid`: `Marker.AddDisc(tConfig.vDestLoc, tConfig.fDist, r, g, b, 0.02)` (`mrxtaskobjectivedeliver.lua`), so the first argument accepts either form. Draws a flat colored ring/disc on the ground. |
| `AddTripwire` | `uMarker = Marker.AddTripwire(nX, nY, nZ, nWidth, nYaw, nR, nG, nB)` | Confirmed in real scripts, e.g. `Marker.AddTripwire(x0, y0, z0, fWidth, yaw0, r, g, b)` (`mrxtaskrace.lua`) — raw world coordinates plus width, yaw, and RGB color, used for race-gate finish lines (paired with `Add3D` for the visual finish-line icon at the same location). |
| `HaltPulse` | `Marker.HaltPulse(uGuid)` | Confirmed in real scripts, e.g. `Marker.HaltPulse(uGuid)` (`mrxfactionmanager.lua`), called when tearing down a reporting-display marker to stop a previously-started `Pulse`. |
| `Pulse` | `Marker.Pulse(uGuid, nR, nG, nB)` | Confirmed in real scripts, e.g. `Marker.Pulse(uGuid, nPulseR, nPulseG, nPulseB)` (`mrxfactionmanager.lua`) and `Marker.Pulse(uGuid, 0, 255, 0)` (`munitions.lua`) — a `uGuid` and an RGB color, presumably flashes/pulses the object's existing marker in that color. Paired with `HaltPulse` to stop it. |
| `Remove` | `Marker.Remove(uMarker)` | Extremely common in real scripts, always called with a marker handle previously returned by `Add`, `Add3D`, `AddBlip`, `AddDisc`, or `AddTripwire` (e.g. `Marker.Remove(self.uMarkerGuid)`, `Marker.Remove(uMarker)`, `Marker.Remove(self.uRing)`) — not a raw object `uGuid`. |
| `SetColor` | `Marker.SetColor(uMarker, nR, nG, nB)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the RGB triples used throughout the confirmed `Add*`/`Pulse` functions above. |
| `SetFollowGuid` | `Marker.SetFollowGuid(uMarker, uGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Name suggests re-attaching an existing marker to follow a different object. |
| `SetGroupedBlipLimit` | `Marker.SetGroupedBlipLimit(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Corresponds by function (not exact name) to `Gui._MarkerSetBlipLimit` — see [Gui](gui#internal-marker-primitives). Presumably caps how many blips of a group/type collapse into a single minimap icon. |
| `SetLocation` | `Marker.SetLocation(uMarker, nX, nY, nZ)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Name suggests moving an existing marker to new world coordinates. |
| `SetScale` | `Marker.SetScale(uMarker, nScale)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

## Notes for modders

- Start with [Snippets: put a marker/blip on an object](../snippets#put-a-marker-blip-on-an-object) — it's the
  one call on this page confirmed by live in-game testing, and the recommended template for adding your own
  minimap blip to an object.
- Every `Add*` function returns a marker handle (not a `uGuid`) that must be kept and later passed to
  `Remove` to clean the marker up — see the many real call sites doing exactly that (`crate.lua`,
  `blippable.lua`, `mrxtaskrace.lua`, etc.). There is no visible "clear all markers" function on this
  namespace.
- `Pulse` / `HaltPulse` are a confirmed start/stop pair (`mrxfactionmanager.lua`), both taking a `uGuid`, not
  a marker handle.
- For the likely internal implementation behind these public functions, and a discussion of where the naming
  correspondence is and isn't exact, see [Gui: Internal Marker Primitives](gui#internal-marker-primitives).
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Marker)` dump) but their
  argument shape is a guess based on naming convention and analogy to confirmed sibling functions only —
  don't build mods around them without testing in-game first.
