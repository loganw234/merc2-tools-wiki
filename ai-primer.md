---
title: AI Primer
nav_order: 12
---

# AI Primer

A single, dense block meant to be pasted into another LLM's context (a chat, a system prompt, a project
memory) to quickly ground it in this game's modding surface — what exists, how the pieces fit, concrete
code shapes to reuse, and where to send you back to this wiki for anything more specific than "surface
level." It is deliberately compressed; it is not a replacement for the rest of this site.

```text
MERCENARIES 2 MODDING PRIMER — for AI assistants. Full wiki: https://wiki.mercs2.tools (this is a
compressed map of it, not a replacement — when a task needs more than this covers, ask the user to paste
the specific page named below rather than guessing).

RULES — READ FIRST
- ALWAYS use Loader.Printf(sMsg) for your own debug output. NEVER Debug.Printf for this purpose — that's
  the engine's own internal log, called thousands of times a second by stock game scripts; anything you
  print through it is buried in unreadable noise. Loader.Printf writes only to lua_loader_printf.log,
  next to the game exe — nothing else lands there, so it's actually readable.
- Wrap any engine call that could plausibly fail (stale uGuid, despawned object) in pcall — see below.
- import("ModuleName") is FILE-SCOPED. It does not leak to other files, other scripts, or console chunks
  — every file that calls into a resident module needs its own import() line, or you get
  `attempt to index global 'X' (a nil value)`.
- Engine namespaces (Object, Event, Player, Vehicle, ...) are always global — never import() these.
- Match the casing already used throughout this primer for engine/module calls: PascalCase.PascalCase
  (Object.GetPosition, MrxPmc.AddCashQty) — never lowercase these (object.getPosition is wrong and will
  fail). Locals use Hungarian-ish prefixes: bOn, nCount, sName, tArgs, uGuid.

WHAT THIS IS
Mercenaries 2: World in Flames (PC). A statically-linked Lua 5.1 VM drives world objects, missions, GUI,
AI — no official modding API ever existed. lua-bridge (an ASI plugin loaded via the pmc_bb.dll Fan Build
loader) injects a live console + script loader into that VM. Everything below is reverse-engineered from
decompiled source + live testing, not official documentation — treat "confirmed"/"verified" language as
meaningful (someone actually checked), its absence as "probably right, not yet double-checked."

RUNNING CODE — Console (interactive) plus 3 script-file hooks. Full detail: /getting-started, /first-mod,
/first-menu
- RECOMMENDED for rapid testing: scripts/OnKey/*.lua — runs once per keypress, edge-triggered, and is
  RE-READ FROM DISK ON EVERY PRESS: edit the file, save, press the key again in-game, see the result
  immediately — no restart, no separate reload step, nothing to run except a text editor and the game
  itself. This is the most beginner-friendly loop on offer, especially for anyone still getting
  comfortable with the tooling. Bind via `local KEYVAL = "keyname"` in the first 10 lines, or
  lua_loader.ini's [OnKey] section. A per-script reentrancy cooldown (~250ms) throttles rapid
  double-presses of the same key so a stuck/bouncing key can't queue up two overlapping runs.
- Console: tools/lua_console.py, TCP 127.0.0.1:27050, send a chunk then `<<<RUN>>>` — good for quick
  one-off queries/inspection (read a value, test a single call), but it's a separate tool with its own
  wire protocol to learn, a bigger step for a newcomer than just editing a file and pressing a key.
- scripts/OnBoot/*.lua — runs once, earliest possible (bridge captures Lua state).
- scripts/OnLoad/*.lua — runs once per level load (GlobalExit-Complete milestone).

Minimal OnKey skeleton:
    local KEYVAL = "insert"  -- must be in the first 10 lines
    Loader.Printf("hello from OnKey")

MODULE SYSTEM — no `require`. Full detail: /resident/, /namespaces/, /glossary
- Every src/resident/*.lua file is one global module table, named after its filename (crate.lua -> Crate).
- `inherit("Name")` = prototype-inherit via setmetatable __index chain (self falls back to parent table).
- `import("Name")` = pull a resident module in as a callable namespace (file-scoped — see RULES above).
- Engine namespaces (Object, Event, Player, Vehicle, Ai, Marker, Sound, Human, Camera, Airstrike, Weapon,
  Sys, Net, Gui, Hud, Controller, Junk, Pg, Graphics) are ALWAYS global, need no import, have no `.lua`
  file behind them (can't read their source, only observed behavior).
- Per-instance pattern: `Inheritable.Create(oPrototype, uGuid, ...)` -> setmetatable + a tInstance[uGuid]
  registry. NOT universal — many resident modules are stateless singletons using bare module-level
  globals instead. Check for OnActivate/Awake/Create/tInstance/setmetatable before assuming either way.
- `uGuid` = opaque runtime object handle (a spawned vehicle, a character, ...), not stable across game
  sessions, the first argument to most Object.*/Vehicle.* calls.
- 228 resident-module reference pages, categorized: Vehicles, Support & Airstrikes, Missions & Tasks,
  GUI & HUD, World Objects & Props, Audio & Music, Core Engine & Utilities, Cheats & Dev Tools.
- 19 engine namespace pages: Ai, Airstrike, Camera, Controller, Event, Graphics, Gui, Hud, Human, Junk,
  Marker, Net, Object, Pg, Player, Sound, Sys, Vehicle, Weapon.

QUICK FUNCTION REFERENCE — the ones nearly every script touches; full signatures/confirmation status on
each namespace's own page under /namespaces/<name> or /resident/<module>
    Object.GetPosition(uGuid) -> x, y, z
    Object.SetPosition(uGuid, x, y, z)
    Object.GetYaw(uGuid) -> n            Object.SetYaw(uGuid, n)
        (unit/axis convention unconfirmed — some scripts assume degrees, not verified against source)
    Object.IsAlive(uGuid) -> bool
    Object.HasLabel(uGuid, sLabel) -> bool
    Object.SetInvincible(uGuid, bOn, sReasonTag)
    Object.SetInfiniteAmmo(uGuid, bOn)
    Object.GetMass(uGuid) -> n            Object.ApplyImpulse(uGuid, x, y, z, bLocalSpace)
    Object.Remove(uGuid)
    Player.GetLocalCharacter() -> uGuid                      (your own character, single-player-safe)
    Player.GetPrimaryCharacter() / GetSecondaryCharacter() -> uGuid   (co-op player 1 / player 2)
    Player.GetLocalPlayer() -> uPlayerGuid                    (player-SLOT guid, distinct from character)
    Pg.Spawn(sTemplateName, x, y, z, ...) -> uGuid   e.g. Pg.Spawn("Veyron", x, y, z) — confirmed working;
        see /hash-lookup for the full real-template-name list
    Pg.GetGuidByName(sObjectName) -> uGuid                    (look up a placed/named object)
    Vehicle.GetFromRider(uCharGuid) -> uVehicleGuid           Vehicle.GetDriver(uVehicleGuid) -> uGuid
    Event.Create(EventType, tArgs, fCallback, tCallbackArgs) -> handle    Event.Delete(handle)
    import("MrxPmc"); MrxPmc.AddCashQty(n) / AddFuelQty(n)    (HUD-updating economy calls — plain
        Player.SetCash/AddCash change the value but skip the HUD refresh)
    Loader.Printf(sMsg)                                       Loader.IsKeyDown(vk) -> bool
    Loader.SaveVar(sKey, xValue)                              Loader.LoadVar(sKey) -> x | nil

LUA-BRIDGE ADDITIONS (not part of the game itself). Full detail: /lua-bridge-api/loader,
/lua-bridge-api/stdlib
- Loader.Printf(msg) — see RULES above.
- Loader.IsKeyDown(vk) / GetKeyboardState() / PopKeyEvents() / ClearKeyEvents() / IsGameFocused() — the
  only general-purpose keyboard input (the game's own Lua surface has none). IsKeyDown/GetKeyboardState
  for continuous/movement input; PopKeyEvents (edge-triggered ring buffer, focus-gated) for typed text —
  NOT interchangeable, PopKeyEvents has no "still held" signal. All three take a numeric Windows VK code
  — a DIFFERENT scheme from OnKey's `KEYVAL = "keyname"` string binding above; a keyname and a VK code are
  not interchangeable with each other either. Measured sub-microsecond per call — safe to call thousands
  of times in a single frame, no need to hand-roll throttling for these specifically.
- Loader.SaveVar(sKey, xValue) / Loader.LoadVar(sKey) — key-value persistence across game restarts
  (numbers/strings/booleans, type preserved on read-back). Stored in lua_loader_data.ini next to the
  .asi, human-readable/hand-editable. LoadVar returns nil for a key never saved — standard idiom:
  `local n = Loader.LoadVar("MyMod_progress") or 0`. Flat namespace shared by every script — prefix keys
  with your own script's name (MyMod_progress, not progress) to avoid colliding with another mod's data.
- Tcp.Send(host, port, msg) — fire-and-forget, localhost-only by design.
- Full math.* stdlib (sin, cos, tan, asin/acos/atan/atan2, sinh/cosh/tanh, sqrt, log, log10, fmod, ldexp,
  modf, frexp, random, randomseed, pi, huge) plus assert(v, msg) — polyfills, additive on top of the
  engine's own math.floor/abs/max/min/etc. assert's error correctly points at whatever called it, not at
  internal polyfill code. Same sub-microsecond hot-loop-safe cost as the input functions above. Older
  scripts on this wiki hand-roll a Taylor-series sin/cos fallback from before these existed — no longer
  necessary, harmless if left as-is.
- lua_Number is float, not double — precision-sensitive math can surprise you.
- Only math/assert were probed for completeness — os/io/coroutine/debug tables' presence isn't
  individually confirmed either way on this wiki. Check `type(os) == "table"` (etc.) before relying on
  something that "should" be there; don't assume stock-Lua-5.1 completeness beyond what's listed here.

CODE SAMPLES — reusable shapes, copy the pattern not necessarily the exact values

State that survives OnKey/OnLoad re-execution (_G is the only thing that persists between separate runs
of the same script within a session — plain `local`s don't):
    _G.MyState = _G.MyState or {bOn = false}
    local State = _G.MyState
    State.bOn = not State.bOn

Safe engine call (never lets one bad uGuid kill the rest of the script):
    local bOk, result = pcall(Object.SetInvincible, Player.GetLocalCharacter(), true, "mymod")
    if not bOk then
      Loader.Printf("SetInvincible failed: " .. tostring(result))
    end

A menu (auto-paginates past ~8 options):
    import("MrxMultiPageMenu")
    MrxMultiPageMenu.Reset()
    MrxMultiPageMenu.AddOption("Say hello", function() Loader.Printf("hi!") end)
    MrxMultiPageMenu.AddOption("Close this menu", nil, nil, true, true)  -- nil callback ONLY safe here,
                                                                          -- bound to the cancel button
    MrxMultiPageMenu.Display("Test Menu:")

Overriding existing game logic (resolves at CALL time, not definition time — this changes behavior for
every future call from anywhere, including from inside the original module's own other functions):
    import("SomeModule")
    SomeModule.SomeFunction = function(...)
      -- your replacement body
    end

COMMON GOTCHAS
- `X and A or B` is Lua's ternary-operator substitute — short-circuits to B if A itself is falsy, which
  is the one real gotcha (only safe when A can never be false/nil). Same underlying "or returns the first
  truthy value" behavior is what makes `_G.MyState = _G.MyState or {defaults}` work in CODE SAMPLES below.
- `pairs(t)` visits every key, any order; `ipairs(t)` only a plain 1..n array, in order, stopping at the
  first gap — mixing them up silently drops data instead of erroring.
- Functions can return multiple values at once: `local a, b, c = f()`.
- No native free-text input widget exists — hand-roll it via Loader.PopKeyEvents() + a VK-code-to-
  character table (see /snippets, /sample-scripts-onkey's CommonSpawnMenu.lua).
- This is Lua 5.1 specifically — no `+=`/`-=` compound assignment (no Lua version has ever had these), no
  `//` floor division or bitwise operators (`&`, `|`, `<<`, ...) — both added in Lua 5.3, well after this
  engine's runtime. Use `x = x + 1`, `math.floor(a / b)`, and don't reach for bit ops at all.
- An uncaught error in an OnKey/OnLoad/OnBoot script silently ends that run early — nothing gets printed
  anywhere, unlike Console's automatic `[runtime]` report. Wrapping risky calls in `pcall` and
  `Loader.Printf`-ing the error yourself (see CODE SAMPLES) is currently the only way to see what failed.

KNOWN HARD LIMITS — flag uncertainty rather than proposing confident workarounds for these
- No confirmed Lua touchpoint for firing a turret, or for a vehicle's camera while driving/gunning —
  extensively tested (multiple recipe matrices, hardpoint probing, camera-lock recipes), all native-only.
  See /namespaces/vehicle, /deep-dives/destroyer-vehicle.
- Object.ApplyImpulse/ApplyPointImpulse confirmed to affect vehicles/physics props; confirmed to NOT
  affect a standing player character (tested live, no effect).
- Multi-player teleport helpers can crash the game if used while inside an interior cell — outdoor-only.
- Physics on some set-dressing "vehicle" templates can't be fixed from Lua alone — needs external
  WAD-level editing tools that don't exist yet for this game.

IF YOU NEED MORE THAN THIS
This primer is intentionally shallow. For a specific module's full function list, exact call signatures,
event names, or a deep dive's full investigation, ask the user to paste the relevant page rather than
guessing — do NOT invent a URL path yourself; name the module/namespace/topic and let them find the page.
Good default ask: "what does wiki.mercs2.tools say about <ModuleName/Namespace>?"
```

## Testing notes

Cold-tested against 10 different LLMs (this primer pasted in fresh, no other context, then given the same
battery of questions/code requests). The restraint and escalation instructions — KNOWN HARD LIMITS, and
"ask rather than guess" for anything not covered — held up broadly, including on smaller local models, so
that part of the design seems to be working as intended. The one recurring weak spot: a bare
namespace/module name listed with no function detail next to it (e.g. the 19-namespace list under MODULE
SYSTEM) is an inviting surface for a model to confidently invent a plausible-sounding function that was
never actually stated anywhere in this primer. Treat any function name a pasted-in LLM produces that
*isn't* in this primer's own QUICK FUNCTION REFERENCE as unconfirmed until checked against the real wiki
page.

Of the local/self-hosted options tested, **Qwen2.5-coder-14b-instruct** performed capably enough to be a
viable choice if you want this running locally rather than against a cloud model.
