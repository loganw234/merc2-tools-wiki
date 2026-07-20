# Mercenaries 2 Modding Wiki

The community reference for modding **Mercenaries 2: World in Flames** (PC) — engine namespaces, per-module
API documentation, deep dives on individual systems, and guides for the tooling built around the game.

**Live at [wiki.mercs2.tools](https://wiki.mercs2.tools).** This repository is the source.

Contributions are welcome — corrections especially. Most of this was written by reading the game's own
decompiled scripts, so the fastest way to improve it is to try something in-game and tell us what actually
happened.

---

## Contributing

**For a small fix** (a typo, a wrong argument, a broken link) you don't need to clone anything: open the page
on the live site, click **Edit this page on GitHub**, make the change, and submit a pull request from the
browser.

**For anything larger**, fork the repo and open a PR. If you're unsure whether something belongs, open an
issue first and ask — that's cheaper than writing a page that gets rejected.

### Running it locally (optional)

Only needed if you want to preview a larger change:

```bash
bundle install
bundle exec jekyll serve      # http://127.0.0.1:4000
```

The site is [Jekyll](https://jekyllrb.com/) with the
[just-the-docs](https://just-the-docs.com/) theme, built by GitHub Pages. There's no build step to commit —
push Markdown, Pages does the rest.

---

## What makes a good contribution

This wiki tries hard to distinguish **what is confirmed** from **what is assumed**. That distinction is the
most valuable thing here, and the easiest thing to accidentally erode.

- **Say how you know.** "Confirmed live — spawning X with argument Y produced Z" is worth far more than a
  plausible-sounding description. A real call site from the decompiled corpus (`resident/`, `vz/`, `shell/`)
  is also good evidence.
- **Don't fill gaps with guesses.** If a function's behaviour is unknown, saying so is a genuine
  contribution. An invented argument list is worse than an admitted blank, because the next person will
  trust it.
- **Corrections are welcome, including to things stated confidently.** Several pages have been wrong; being
  wrong in public and fixed later is the intended lifecycle.

### The `verified` flag

Pages under `resident/` were drafted from the decompiled source and carry a **"not yet verified in-game"**
banner by default. Once someone has actually confirmed a page's contents against a running game, that page
sets the flag in its own front matter:

```yaml
---
title: MrxSomeModule
parent: Resident Modules
verified: true
verified_note: "Confirmed in-game 2026-01-01 — spawn + teardown behave as described."
---
```

**228 of 237** resident pages are verified so far. Confirming one of the remainder — or catching a page that
is verified but wrong — is one of the most useful things you can do here.

---

## Page conventions

Every page starts with YAML front matter. `parent` places it under a section; `nav_order` sorts it within
that section:

```yaml
---
title: Event
parent: Engine Namespaces
nav_order: 3
---
```

### Two things that will silently break your page

1. **Lua table literals break the Liquid template engine.** A bare `{{` in a code block is read as a Liquid
   tag and the build fails. Wrap those snippets:

   ```liquid
   {% raw %}
   local t = {{1, 2}, {3, 4}}
   {% endraw %}
   ```

   A single `{}` (or `or {}`) is fine as-is — it's specifically the doubled brace.

2. **An unquoted front-matter value containing `: ` breaks the YAML** — and it fails *quietly*, dropping the
   page out of the navigation rather than erroring. Quote the whole value:

   ```yaml
   verified_note: "Confirmed: works as described."
   ```

---

## Repository layout

| Path | Contents |
|---|---|
| `namespaces/` | Engine namespace reference (`Object`, `Event`, `Ai`, …) |
| `resident/`, `vz/`, `shell/` | Per-module docs mirroring the game's own script modules |
| `deep-dives/` | Long-form explanations of individual systems |
| `tutorials/` | Task-oriented guides |
| `ess/`, `uilib/`, `contract-framework/` | Documentation for community frameworks |
| `lua-bridge-api/` | The lua-bridge injection tool and its wire protocols |
| `live-tools/` | The browser tools that connect to a running game |
| `spawn-reference/` | Confirmed spawnable template names |
| `_layouts/`, `_includes/` | Jekyll templates (including the verification banner) |

---

## Disclaimer

This is an unofficial, non-commercial community fan project. It is **not affiliated with, associated with,
authorized by, endorsed by, or in any way officially connected to Electronic Arts or Pandemic Studios**.
*Mercenaries 2: World in Flames* and all related marks are the property of their respective owners.

This repository contains original documentation only — no game assets are redistributed. See
[about](https://wiki.mercs2.tools/about) for more.
