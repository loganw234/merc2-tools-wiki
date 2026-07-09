---
title: "2. Hello, Screen"
parent: Tutorials
nav_order: 2
---

# Tutorial 2: Hello, Screen

> Built on `MrxTutorialManager.ShowMessage`, already **confirmed working by live testing** elsewhere on
> this wiki (see [Snippets](../snippets#show-a-custom-hud-message-with-icon-and-sound)) — this page slows
> down to introduce it as a deliberate first step instead of a grab-bag entry.

[Tutorial 1](hello-log) got a line of text into a log file only you ever look at. This time, the message
shows up **in the game itself** — the same way the game's own "you're low on fuel" or "you're swimming"
hints do, because it's reusing that exact same system.

## The code

Create `scripts/OnKey/hello_screen.lua`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines

import("MrxTutorialManager")
MrxTutorialManager.ShowMessage("Hello from my mod!")
```

Load into a level and press **Insert**. Your text appears on-screen in the same popup widget the game's
built-in tutorial hints use, complete with its usual notification sound and a generic book icon:

> **[Image placeholder — `../img/helloscreenmessage.png`]** Screenshot of the in-game tutorial-hint popup
> showing the custom text "Hello from my mod!" with the default book icon, wherever the player character
> happens to be standing.

## Clearing it

Unlike the log file, this message doesn't disappear on its own — there's no auto-hide timer. Create a
second script, `scripts/OnKey/hello_screen_hide.lua`, bound to a different key:

```lua
local KEYVAL = "delete"  -- deliberately different from hello_screen.lua's "insert"

import("MrxTutorialManager")
MrxTutorialManager.HideMessage()
```

Press **Insert**, confirm the message appears, then press **Delete** and confirm it goes away.

## What's actually happening

`import("MrxTutorialManager")` pulls in a **resident module** — you'll see exactly why that line is
needed, and what breaks without it, in [Tutorial 5](why-import). `ShowMessage(sMessage)` and
`HideMessage()` are two of that module's functions: one displays a message in the standard tutorial-hint
widget, the other clears whatever's currently showing in it. Nothing about the widget is actually specific
to "tutorials" — it's a generic on-screen message box that the game's own tutorial system happens to be
the first thing to use.

## Try it yourself

- Show two different messages back to back (press Insert, edit the text in the file, save, press Insert
  again) — does the second message replace the first, or stack on top of it?
- Both functions take extra, optional arguments —
  `ShowMessage(sMessage, bDontNetSync, sIdentifierName)` and `HideMessage(bDontNetSync, sIdentifierName)`.
  Try giving your message an identifier tag (a third argument, a string like `"mytest"`), then call
  `HideMessage()` with **no** arguments at all — does it still clear? Compare your result against the
  confirmed answer in [Snippets](../snippets#show-a-custom-hud-message-with-icon-and-sound).
- Delete the `import("MrxTutorialManager")` line and press Insert again. Open your log file (you know how,
  from [Tutorial 1](hello-log)) and read the error. Keep that error in mind —
  [Tutorial 5](why-import) is entirely about it.

## Where this comes from

- [Snippets: Show a custom HUD message](../snippets#show-a-custom-hud-message-with-icon-and-sound) — the
  full confirmed writeup, including the identifier-tag behavior and a note on why you can't pick a
  different icon.
- [Glossary: `import("Name")`](../glossary#importname)

**Next:** [Tutorial 3: Reading Before Writing](reading-state) — every tutorial so far has told the game to
*do* something. Time to ask it a question instead.
