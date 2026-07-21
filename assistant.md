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
general knowledge about Lua.

{: .warning }
> It is still a language model and it *can* be wrong. Anything it tells you about an
> unverified page is doubly worth checking. When it names a wiki page, go read that page —
> that's the authoritative version.

<div id="assistant-app" markdown="0">
  <div id="chat-log" role="log" aria-live="polite"></div>
  <div id="chat-status"></div>
  <form id="chat-form" autocomplete="off">
    <textarea id="chat-input" rows="3"
      placeholder="e.g. Why does my OnKey script stop halfway through with no error?"
      aria-label="Ask a question"></textarea>
    <div class="chat-row">
      <button type="submit" id="chat-send">Ask</button>
      <button type="button" id="chat-reset">New conversation</button>
      <span id="chat-hint">Enter to send &middot; Shift+Enter for a newline</span>
    </div>
  </form>
  <div id="turnstile-holder"></div>
</div>

{% raw %}
<style>
#assistant-app { margin-top: 1.5rem; }
#chat-log {
  border: 1px solid var(--border-color, #e6e6e6);
  border-radius: 6px; padding: 0; min-height: 120px; max-height: 60vh;
  overflow-y: auto; margin-bottom: .75rem;
}
#chat-log:empty { display: none; }
.msg { padding: .85rem 1rem; border-bottom: 1px solid var(--border-color, #eee); }
.msg:last-child { border-bottom: 0; }
.msg .who { font-size: .72rem; text-transform: uppercase; letter-spacing: .06em;
  opacity: .6; margin-bottom: .3rem; }
.msg.user { background: var(--sidebar-color, #f5f6fa); }
.msg .body p { margin: 0 0 .6rem; }
.msg .body p:last-child { margin-bottom: 0; }
.msg .body pre { margin: .5rem 0; padding: .7rem .85rem; overflow-x: auto;
  background: var(--code-background-color, #f5f6fa); border-radius: 4px;
  border: 1px solid var(--border-color, #e6e6e6); }
.msg .body code { font-size: .85em; }
.msg .body pre code { background: none; padding: 0; }
#chat-form textarea { width: 100%; box-sizing: border-box; font-family: inherit;
  font-size: .95rem; padding: .6rem; border-radius: 6px;
  border: 1px solid var(--border-color, #ccc); resize: vertical; }
.chat-row { display: flex; align-items: center; gap: .6rem; margin-top: .5rem; flex-wrap: wrap; }
#chat-form button { padding: .45rem 1.1rem; border-radius: 6px; cursor: pointer;
  border: 1px solid var(--border-color, #ccc); background: var(--sidebar-color, #f5f6fa);
  font-size: .9rem; }
#chat-send { background: #2b6cb0; color: #fff; border-color: #2b6cb0; font-weight: 600; }
#chat-form button[disabled] { opacity: .5; cursor: not-allowed; }
#chat-hint { font-size: .78rem; opacity: .6; }
#chat-status { font-size: .85rem; min-height: 1.2em; margin-bottom: .5rem; opacity: .75; }
#chat-status.error { color: #c53030; opacity: 1; }
.cursor::after { content: "\258B"; opacity: .5; }
#turnstile-holder { margin-top: .75rem; }
</style>

<script>
(function () {
  // ---- configuration -------------------------------------------------
  // Both values are public by design: the site key is meant to be readable in
  // page source, and the Worker URL is the endpoint the page calls. The Turnstile
  // *secret* and the provider key live in Worker secrets, never here.
  var WORKER_URL       = "https://mercs2-wiki-assistant.loganw423.workers.dev";
  var TURNSTILE_SITEKEY = "0x4AAAAAAD6JJPjdx7gnHwnf";

  var log     = document.getElementById("chat-log");
  var form    = document.getElementById("chat-form");
  var input   = document.getElementById("chat-input");
  var sendBtn = document.getElementById("chat-send");
  var resetBtn= document.getElementById("chat-reset");
  var status  = document.getElementById("chat-status");

  var history = [];      // [{role, content}] -- sent to the Worker each turn
  var session = null;    // signed token from POST /session
  var busy = false;
  var widgetId = null;

  function setStatus(text, isError) {
    status.textContent = text || "";
    status.className = isError ? "error" : "";
  }

  function setBusy(b) {
    busy = b;
    sendBtn.disabled = b;
    sendBtn.textContent = b ? "Thinking…" : "Ask";
  }

  // ---- rendering -----------------------------------------------------
  // Model output is untrusted text. Everything is escaped before it ever
  // touches innerHTML; the only markup we then re-introduce is our own.
  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderMarkdown(text) {
    var out = "";
    var parts = text.split("```");
    for (var i = 0; i < parts.length; i++) {
      if (i % 2 === 1) {
        // fenced block: drop an optional language tag on the first line
        var block = parts[i].replace(/^[a-zA-Z0-9_-]*\n/, "");
        out += "<pre><code>" + escapeHtml(block) + "</code></pre>";
      } else {
        var prose = escapeHtml(parts[i])
          .replace(/`([^`\n]+)`/g, "<code>$1</code>")
          .replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>");
        var paras = prose.split(/\n{2,}/);
        for (var p = 0; p < paras.length; p++) {
          if (paras[p].trim()) out += "<p>" + paras[p].replace(/\n/g, "<br>") + "</p>";
        }
      }
    }
    return out;
  }

  function addMessage(who, label) {
    var el = document.createElement("div");
    el.className = "msg " + who;
    var head = document.createElement("div");
    head.className = "who";
    head.textContent = label;
    var body = document.createElement("div");
    body.className = "body";
    el.appendChild(head);
    el.appendChild(body);
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return body;
  }

  // ---- turnstile / session -------------------------------------------
  function getTurnstileToken() {
    return new Promise(function (resolve, reject) {
      if (typeof turnstile === "undefined") {
        reject(new Error("Verification widget failed to load. Check your ad blocker."));
        return;
      }
      if (widgetId !== null) turnstile.reset(widgetId);
      widgetId = turnstile.render("#turnstile-holder", {
        sitekey: TURNSTILE_SITEKEY,
        size: "flexible",
        callback: resolve,
        "error-callback": function () { reject(new Error("Verification failed.")); }
      });
    });
  }

  async function ensureSession() {
    if (session && session.expiresAt > Date.now() / 1000 + 30) return session.token;
    setStatus("Verifying you're human…");
    var token = await getTurnstileToken();
    var res = await fetch(WORKER_URL + "/session", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ turnstileToken: token })
    });
    var data = await res.json();
    if (!res.ok) throw new Error(data.message || "Could not start a session.");
    session = { token: data.session, expiresAt: data.expiresAt };
    setStatus("");
    return session.token;
  }

  // ---- send ----------------------------------------------------------
  async function send(question) {
    setBusy(true);
    addMessage("user", "You").textContent = question;
    history.push({ role: "user", content: question });

    var body = addMessage("assistant", "Assistant");
    body.classList.add("cursor");
    var answer = "";

    try {
      var token = await ensureSession();
      var res = await fetch(WORKER_URL + "/chat", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ session: token, messages: history })
      });

      if (!res.ok) {
        var err = await res.json().catch(function () { return {}; });
        if (res.status === 401) session = null;   // expired -> re-verify next time
        throw new Error(err.message || "Request failed (" + res.status + ").");
      }

      // Server-sent events: frames are "data: {json}\n\n", terminated by [DONE].
      var reader = res.body.getReader();
      var decoder = new TextDecoder();
      var buffer = "";
      for (;;) {
        var chunk = await reader.read();
        if (chunk.done) break;
        buffer += decoder.decode(chunk.value, { stream: true });
        var frames = buffer.split("\n\n");
        buffer = frames.pop();
        for (var i = 0; i < frames.length; i++) {
          var line = frames[i].trim();
          if (line.indexOf("data:") !== 0) continue;
          var payload = line.slice(5).trim();
          if (payload === "[DONE]") continue;
          try {
            var obj = JSON.parse(payload);
            var delta = obj.choices && obj.choices[0] && obj.choices[0].delta;
            if (delta && delta.content) {
              answer += delta.content;
              body.innerHTML = renderMarkdown(answer);
              log.scrollTop = log.scrollHeight;
            }
          } catch (e) { /* partial or keep-alive frame; ignore */ }
        }
      }

      if (answer) {
        history.push({ role: "assistant", content: answer });
      } else {
        body.textContent = "No answer came back. Try rephrasing, or ask again.";
      }
    } catch (e) {
      body.textContent = "";
      body.parentNode.remove();
      history.pop();                       // don't poison the next turn
      setStatus(e.message || String(e), true);
    } finally {
      body.classList.remove("cursor");
      setBusy(false);
    }
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var q = input.value.trim();
    if (!q || busy) return;
    input.value = "";
    setStatus("");
    send(q);
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.dispatchEvent(new Event("submit", { cancelable: true }));
    }
  });

  resetBtn.addEventListener("click", function () {
    history = [];
    log.innerHTML = "";
    setStatus("");
    input.focus();
  });
})();
</script>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>
{% endraw %}
