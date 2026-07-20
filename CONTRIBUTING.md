# Contributing

Thanks for helping. Corrections are the most valuable thing you can send — a lot of this wiki was written
by reading the game's decompiled scripts, so anything confirmed against a *running game* beats anything
inferred from source.

See the [README](README.md) for the full conventions. The short version:

## Sending a change

- **Typo, wrong argument, broken link** — click **Edit this page on GitHub** at the bottom of any page on
  [wiki.mercs2.tools](https://wiki.mercs2.tools) and submit a PR from the browser. No clone needed.
- **Anything larger** — fork, branch, PR. If you're unsure it belongs, open an issue first; that's cheaper
  than writing a page that gets turned down.
- **Previewing locally** is optional: `bundle install && bundle exec jekyll serve`.

## In your PR, please say how you know

This is the one thing worth being strict about. State the evidence:

- **"Confirmed in-game"** — what you ran, and what actually happened. This is the gold standard.
- **"From the decompiled source"** — cite the file, e.g. `resident/mrxsomething.lua:120`.
- **"Untested / inferred"** — say so plainly. This is a perfectly good contribution; it just gets written
  as uncertain rather than as fact.

Please don't fill a gap with a plausible guess presented as fact. An honest blank is more useful, because
the next reader will trust whatever is written.

Corrections to existing pages are welcome even where they're stated confidently — several have been wrong.
Being wrong in public and fixed later is the intended lifecycle here, not a failure.

## Verifying a page

Pages under `resident/` carry a **"not yet verified in-game"** banner until someone confirms them against a
real game. If you check one, flip it in that page's front matter:

```yaml
verified: true
verified_note: "Confirmed in-game 2026-01-01 - behaves as described."
```

Quote the whole `verified_note` value — an unquoted string containing `: ` breaks the YAML and silently
drops the page from the navigation.

**228 of 237** resident pages are verified. Confirming one of the rest, or catching one that's marked
verified but wrong, is a great first contribution.

## Two things that break the build

1. A Lua table literal's `{{` is read as a Liquid tag. Wrap those snippets in `{% raw %}` / `{% endraw %}`.
   A single `{}` is fine.
2. Unquoted front-matter containing `: ` breaks YAML *silently* — the page builds but vanishes from the nav.

## Scope

This wiki documents *Mercenaries 2* modding: the engine's Lua API, the game's own script modules, the
community frameworks, and the tooling around them. It doesn't host game assets, and it isn't a general
piracy or DRM resource.
