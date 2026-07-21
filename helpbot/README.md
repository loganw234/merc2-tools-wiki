# Wiki assistant (helpbot)

The chat assistant on [/assistant](https://wiki.mercs2.tools/assistant). Not part of the
published site — Jekyll is told to skip this directory in `_config.yml`.

## How it works

```
Browser (GitHub Pages)        Cloudflare Worker              DeepSeek
  assistant.md          POST   verify Turnstile        HTTPS
  chat UI, no key  ───────────▶ rate-limit by IP  ───────────▶ V4 Pro
  no pack          ◀─────────── prepend context pack ◀─────────
                        SSE     key from secret        stream
```

The Worker holds two things the browser must never see: the provider API key, and the
**context pack** — ~105k tokens of this wiki, compressed, sent as the system message on
every request. That pack is what makes a general-purpose model answer like it knows this
game.

### The cache invariant

DeepSeek bills a cached prefix at roughly 1% of the uncached rate. The pack is ~105k of the
~110k tokens in a typical request, so essentially the entire cost of the service depends on
that prefix hitting cache. The cache only matches on **exact bytes**, which is why:

- `build_pack.py` writes no timestamps, sorts every directory walk, and forces `\n` newlines
  so a Windows build and a Linux CI build produce identical files.
- The Worker builds the system message once at module scope and never interpolates anything
  into it.

If you add per-request context later, append it as a **later message**. Putting it in the
system message breaks the prefix and multiplies the bill by roughly 120x.

## Building the pack

```bash
python helpbot/build_pack.py --verbose   # build + per-section token report
python helpbot/build_pack.py --check     # CI gate: fails if the committed pack is stale
python helpbot/build_pack.py --coverage  # CI gate: fails on silent extraction holes
```

### Why `--coverage` exists

A user asked how to command NPCs and the assistant invented `Pg.Spawn("PMC Soldier", ...)`.
Nothing was broken in the usual sense — the pack simply had **no character templates in
it at all**, so the model filled the hole. Two causes:

- `hash-lookup.md` (6,101 names, the wiki's own "full real-template-name list") is a
  **top-level page**, and the builder only walked subfolders. Every top-level page was
  missing.
- `namespaces/controller.md` is a constants table, not a function table, so the signature
  extractor produced **zero lines** for it and no one noticed.

The lesson is that a missing section fails *silently* and looks exactly like a model
problem. `--coverage` asserts every namespace/ess page contributes entries, that
known-real symbols appear in the section they belong to, and that known-fake names
(`PMC Soldier`, `Ai.SetFactionGuid`) never appear in generated content. When adding an
extractor, add a canary for it.

Note it deliberately globs the filesystem rather than calling `md_pages()`. An earlier
version used `md_pages()` and, when that function was sabotaged in a negative test,
passed happily — it was asking the broken code what it should have found.

Output goes to `helpbot/pack/pack.txt` (bundled into the Worker) and `pack.meta.json`
(hash + per-section sizes). **Commit both.**

Current allocation, ~197k tokens against a 250k ceiling:

| section | ~tokens | source |
|---|---|---|
| system | 1.5k | `pack_src/00_system.md` (hand-written) |
| gotchas | 1.5k | `pack_src/10_gotchas.md` (hand-written) |
| namespaces | 32k | `namespaces/*.md` signature + constants tables |
| ess | 20k | `ess/*.md` overviews + signature tables |
| resident | 28k | `resident/*.md` — signatures only, 228 modules |
| lua-bridge | 6.8k | `lua-bridge-api/*.md` near-verbatim |
| spawn | 16k | `spawn-reference/*.md` curated lists |
| templates | 41k | `hash-lookup.md` — all 6,101 authoritative names |
| tutorials | 7.3k | `tutorials/*.md` truncated |
| toplevel | 41k | snippets, glossary, getting-started, first-mod/menu, sample scripts, cheat menu, sound |
| idioms | 0.9k | `pack_src/90_idioms.md` (hand-written) |

The budget was raised from ~100k to 250k after the hallucination described under
`--coverage` below. V4 Pro has a 1M context window and cached prefix tokens cost
~$0.0036/M, so breadth is close to free — **completeness beats compactness here**, because
a gap in the pack does not degrade gracefully, it gets confabulated over.

Tuning knobs, all in `build_pack.py`: per-section budgets in `SECTIONS`, and the
`note_limit`/`char_cap` arguments on each builder.

**Namespace signatures are auto-qualified.** The wiki is inconsistent — `object.md`
writes `Object.GetPosition(uGuid)` while `vehicle.md` writes a bare
`GetFromRider(uCharacter)`. `qualify()` rewrites the bare form so every line in the pack
is copy-pasteable as written, rather than leaving the model to infer a namespace.

**Editing the pack's judgment** — the system prompt, the gotchas list, the code idioms — means
editing `pack_src/*.md`, not the generated output. Those three files are where the assistant's
behaviour actually lives; everything else is mechanical extraction.

### Notes on what the extractors do

- **Resident pages are signatures only.** The job is "does this function exist and what are
  its arguments", not explaining it. For anything deeper the assistant is told to name the
  page and send the user there.
- **Unverified pages get an `[UNVERIFIED]` tag** and the system prompt tells the assistant to
  say so when answering from one. As of writing this tags nothing: all 228 resident pages
  with a `## Functions` section carry `verified: true`. The eight that don't are `cat-*.md`
  category indexes with no functions, which are skipped anyway. The mechanism is live and
  will tag correctly the moment an unverified module page lands.
- **The All Vehicles list is truncated** (700 of 2120 names) and *says so in the pack*, with a
  pointer to the full page. This matters: without the notice the assistant would treat a
  missing name as proof it doesn't exist, which is the wrong answer.

## Deploying the Worker

One-time setup:

```bash
cd helpbot/worker
npm install

# KV namespace for rate-limit counters -> paste the id into wrangler.toml
npx wrangler kv namespace create RATE_LIMIT

# Secrets (never committed)
npx wrangler secret put DEEPSEEK_API_KEY
npx wrangler secret put TURNSTILE_SECRET
npx wrangler secret put SESSION_SECRET     # any long random string
```

Then, for every deploy:

```bash
npm run deploy      # rebuilds the pack, then wrangler deploy
npm run tail        # live logs, including the usage frames
```

Finally, edit the two placeholders at the top of the `<script>` in `../assistant.md`:
`WORKER_URL` (the deployed Worker URL) and `TURNSTILE_SITEKEY` (from the Turnstile dashboard;
the site key is public, the secret is not).

### Before the first deploy — verify these

1. **`DEEPSEEK_MODEL` in `wrangler.toml`.** Defaults to `deepseek-v4-pro`. Check the current
   id against <https://api-docs.deepseek.com>; a wrong id is a 404 from their API, which
   surfaces as a generic 502 from the Worker.
2. **Context window.** The pack is ~105k tokens before the conversation. Confirm the model's
   window comfortably exceeds that; if not, drop a section budget in `build_pack.py`.
3. **A spend cap on the DeepSeek account.** This is the real backstop, not the rate limiter.
   DeepSeek is prepaid, so keeping a small balance *is* a hard cap — use that deliberately
   rather than topping it up to a large number.

## The chat page: assistant.md + assets/assistant.{js,css}

`assistant.md` is only the HTML skeleton. The app lives in `assets/assistant.js`
and `assets/assistant.css`, which Jekyll copies verbatim.

**Never put an inline `<script>` back into assistant.md** (or any wiki page).
The remote just-the-docs layout collapses served HTML onto a single line — the
live page is ~90 KB across 2 lines — and once newlines are gone, the first `//`
comment comments out the entire rest of an inline script. The page renders
perfectly and silently does nothing: no console error, no visual clue. This
happened; it cost a debugging session. External `src=` tags are safe (static
assets aren't minified), which is the whole reason for the current layout.

CI enforces both halves: `node --check assets/assistant.js` must pass, and any
inline `<script>` block in assistant.md fails the build.

**Cache-busting:** the asset tags in assistant.md carry `?v=N`. Bump it whenever
you change the js/css, or browsers hold the old version for up to 10 minutes
(GitHub Pages serves `max-age=600`) — long enough to "verify" a fix that isn't
actually loaded.

### Chat UI features and their moving parts

| Feature | How it works |
|---|---|
| File attachments | Client-side only. Files are read in the browser and appended to the message text between `--- attached file: NAME ---` markers (the system prompt documents the format for the model). Nothing is uploaded anywhere except as part of the normal chat request. Caps: 4 files, 90k chars each, text types only. |
| Thinking display | The Worker passes the provider stream through untouched. If DeepSeek emits `delta.reasoning_content` (or inline `<think>` tags), the UI streams it into a collapsible "Thought process" pane that auto-collapses when the answer starts. If the model emits neither, the pane never appears. **To turn reasoning on**, set the `EXTRA_BODY_JSON` env var in wrangler.toml with the thinking parameter from DeepSeek's docs and redeploy — the shape is deliberately not hardcoded because it should come from their docs, not from a guess. |
| Stop / regenerate | Stop aborts the fetch (Esc works too) and keeps the partial answer. Regenerate pops the last assistant turn and re-runs the completion — only offered on the newest answer. |
| Persistence | Conversation is kept in `sessionStorage` (per-tab, cleared when the tab closes). "New chat" wipes it. |
| Payload caps | Mirrored client-side from wrangler.toml (100k/message, 240k/conversation, 16 turns) so users get a friendly counter instead of a 400. Change them in both places. |

## Abuse controls

| Control | Where | Notes |
|---|---|---|
| Provider spend cap | DeepSeek account | The only true backstop. Everything else is optimisation. |
| Turnstile | `/session` | Traded once for a 2h HMAC-signed session bound to the client IP. Chat requests don't re-solve it. |
| Per-IP rate limit | `/chat`, KV | 25/hour, 80/day by default. KV is eventually consistent and caps at ~1 write/sec/key, so a race can leak a few extra requests — acceptable at this scale, and the spend cap covers it. |
| Payload caps | `/chat` | 16 turns, 100k chars/message (~2900 lines of Lua), 240k total. Sized so someone can paste a whole mod file; V4 Pro's 1M context means pack + conversation still peaks near 165k. |
| Output cap | `/chat` | `MAX_OUTPUT_TOKENS`, default 8000 (~600 lines of returned Lua plus explanation). |
| CORS lock | all | Stops other sites embedding the endpoint. Not a security boundary — curl sends any Origin it likes. |
| Prompt-injection note | `pack_src/00_system.md` | Pasted scripts and logs are treated as data, not instructions. |

## Verifying the cache actually hits

This is the one post-deploy check worth doing carefully, because everything about the cost
model depends on it and nothing visibly breaks when it's wrong.

```bash
npm run tail
```

Ask two questions in a row and watch for the `usage` log lines. The second should show
`cache_hit_tokens` at roughly the pack size (~105k) and `cache_miss_tokens` near zero. If
`cache_hit_tokens` stays at zero across requests, the prefix is unstable — something is
varying inside the system message, and every request is being billed at the full input rate.

Rough cost per 5-turn conversation with the cache working: **about two cents**. Without it,
closer to thirty.

## Keeping the pack current

`.github/workflows/helpbot-pack.yml` runs `build_pack.py --check` on any PR or push that
touches wiki content the pack draws from, and fails if `pack/pack.txt` wasn't regenerated.
So the workflow after editing a namespace or resident page is:

```bash
python helpbot/build_pack.py      # regenerate
git add helpbot/pack/             # commit alongside the wiki edit
cd helpbot/worker && npm run deploy
```

The Action gates staleness; it does **not** deploy. Deploys stay manual and deliberate, since
each one costs one cold cache write (~$0.05) and changes what every user sees.
