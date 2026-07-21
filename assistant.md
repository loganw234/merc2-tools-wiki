---
title: Assistant
nav_order: 3
# Soft launch: reachable at /assistant but kept out of the sidebar nav while the
# provider path is being verified. Remove this line to list it.
nav_exclude: true
description: "Ask questions about modding Mercenaries 2. Answers come from this wiki's own content."
---

# Assistant
{: .no_toc }

Ask anything about modding Mercenaries 2 — engine namespaces, resident modules, Ess, spawn
template names, or why your script isn't running. The assistant is given a compressed copy of
this wiki as its reference, so it answers from what's actually documented here rather than from
general knowledge about Lua. You can attach `.lua` scripts and logs directly, or drag them onto
the message box.

{: .warning }
> It is still a language model and it *can* be wrong. Anything it tells you about an
> unverified page is doubly worth checking. When it names a wiki page, go read that page —
> that's the authoritative version.

<!-- The chat app is a static asset, NOT an inline script. The theme minifies
     HTML onto one line, which silently kills inline JS containing // comments
     (see helpbot/README.md). CI fails the build if an inline script block ever
     reappears on this page. Bump ?v= when the assets change. -->
<div id="assistant-app" markdown="0">
  <link rel="stylesheet" href="/assets/assistant.css?v=1">

  <div id="chat-shell">
    <div id="chat-topbar">
      <span class="title">Wiki Assistant</span>
      <span class="model-tag">answers from wiki.mercs2.tools</span>
      <span class="spacer"></span>
      <button type="button" id="chat-reset" class="btn">New chat</button>
    </div>

    <div id="chat-log" role="log" aria-live="polite"></div>

    <form id="composer" autocomplete="off">
      <div id="attach-chips" hidden></div>
      <div id="composer-row">
        <button type="button" id="attach-btn" class="icon-btn" title="Attach a script or log"></button>
        <textarea id="chat-input" rows="1"
          placeholder="Ask a question, or paste / attach a script…"
          aria-label="Ask a question"></textarea>
        <button type="submit" id="chat-send" class="icon-btn" title="Send (Enter)"></button>
      </div>
      <div id="composer-foot">
        <span id="chat-hint">Enter to send &middot; Shift+Enter for a newline &middot; drop files to attach</span>
        <span id="chat-counter" hidden></span>
      </div>
      <input type="file" id="file-input" multiple hidden>
    </form>

    <div id="chat-status"></div>
    <div id="turnstile-holder" hidden></div>
  </div>

  <script src="/assets/assistant.js?v=1" defer></script>
  <script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>
</div>

<!-- `composer` is the <form> element; assistant.js binds submit/drop/keys to it. -->
