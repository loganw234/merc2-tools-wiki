---
title: Home
nav_order: 1
---

# Mercenaries 2 Modding Wiki

A community reference for modding **Mercenaries 2: World in Flames (PC)** — how to get your own code
running in the live game, and what its Lua-scripted systems actually do.

This is a study/reference resource, not a redistribution of anything from the game — pages describe
observed engine behavior (module structure, functions, events, lifecycle) rather than reproducing game
files.

## Where to start

- **New here?** Read [Getting Started](getting-started) first — it covers `lua-bridge`, currently the
  only way to inject and run your own Lua against the live game.
- **Just want a working cheat menu?** Grab [All-In-One Cheat Menu](cheat-menu) — one script, one hotkey,
  no reading required.
- **Looking for a specific game object/system?** Browse [Resident Modules](resident/) — one reference
  page per engine module (`crate`, `airplane`, `mrxbriefing`, ...), covering what it does, what it
  inherits from, its functions, and the events it listens for.
- **Working with an AI assistant?** Paste it the [AI Primer](ai-primer) — a single compressed block that
  gets it oriented on this game's modding surface without reading the whole site.

## A note on accuracy

The per-module reference pages are drafted by a local LLM analyzing engine behavior, then spot-checked.
They're a strong starting point, not gospel — if something looks off in practice, that's worth flagging
so the page can be corrected.
