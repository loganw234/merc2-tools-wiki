---
title: Tutorials
nav_order: 4
has_children: true
has_toc: false
---

# Tutorials

Ten small, guided lessons, meant to be done roughly in order. Where [Getting Started](../getting-started)
gets the tooling installed and [Your First Mod](../first-mod) gets one script running end to end, this
section slows down and gives each individual idea — a log line, a menu toggle, a timer, an event hook — its
own page, with room to explain the parts other pages take for granted or mention only in passing. Where
[Recipes](../recipes) is a grab-bag you dip into once you already know what you're looking for, this is the
ladder that gets you to "knowing what you're looking for" in the first place.

Every tutorial ends with a **Try it yourself** section — small, deliberate changes to make on your own
before moving to the next page. Making the change yourself and watching it work (or fail, and figuring out
why) is worth more than reading ten more paragraphs about it.

**No tutorial here uses the REPL/console.** Every example is a script you drop into `scripts/OnKey/` or
`scripts/OnLoad/` and trigger by pressing a key or loading a level, exactly as described in
[Getting Started](../getting-started#two-ways-to-run-code). That's deliberately the more visible way to do
it while you're still getting your bearings: save the file, press a key, watch something happen — no
separate tool to learn first. (The REPL is genuinely faster once you're comfortable — see
[Getting Started](../getting-started#1-the-repl-fastest-for-iterating) when you're ready for it.)

## The ladder

1. [Hello, Log](hello-log) — get one line of your own text into a log file you control.
2. [Hello, Screen](hello-screen) — get a message to show up *in the game*, not just in a log file.
3. [Reading Before Writing](reading-state) — ask the game a question and show yourself the answer.
4. [Two Clocks, Side by Side](two-clocks) — the same action, triggered automatically vs. on demand.
5. [Why `import()`?](why-import) — why some calls need a setup line first and others don't.
6. [Don't Let One Bad Line Kill Your Script](pcall-safety) — survive your own mistakes with `pcall`.
7. [Remembering Things: A Press Counter](press-counter) — make a script remember a number between presses.
8. [Making Time Pass on Its Own](timers) — schedule something to happen later, and keep happening.
9. [Reacting Instead of Waiting](reacting-to-events) — respond to something the game itself tells you,
   instead of checking for it yourself.
10. [Finding Something in the World by Name](finding-by-name) — look an object up by name and ask where
    it is.
11. [Editing an Existing Script](editing-existing-scripts) — everything above has you writing something
    from scratch; this one hands you a real, much bigger script and asks you to change one thing about it.

One prerequisite for all eleven: lua-bridge installed and working, confirmed by getting *something* to
happen from a script at least once. The [Getting Started](../getting-started) rapid overview is enough to
get there if you haven't yet.
