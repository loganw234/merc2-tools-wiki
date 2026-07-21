/* Mercenaries 2 wiki assistant — chat client.
 *
 * Lives here as a STATIC ASSET, not inline in assistant.md, on purpose: the
 * theme's layout minifies HTML pages onto a single line, which turns any //
 * comment in an inline script into "comment out the rest of the file". Static
 * .js files are copied verbatim by Jekyll, so normal code is safe here.
 * CI runs `node --check` on this file and fails the build if assistant.md ever
 * grows an inline <script> again.
 *
 * Talks to the Cloudflare Worker (see helpbot/worker/):
 *   POST /session  { turnstileToken }      -> { session, expiresAt }
 *   POST /chat     { session, messages[] } -> SSE passthrough from DeepSeek
 *
 * Thinking display: DeepSeek streams reasoning as `delta.reasoning_content`
 * (and some builds emit inline <think>...</think> in the content instead).
 * Both are routed into a collapsible "Thought process" pane. If the model
 * emits neither, the pane simply never appears.
 */
(function () {
  "use strict";

  /* ---- configuration ------------------------------------------------- */
  /* Public by design: the site key is meant to be readable, and the Worker
     URL is the endpoint this page calls. Secrets live in Worker secrets. */
  var WORKER_URL = "https://mercs2-wiki-assistant.loganw423.workers.dev";
  var TURNSTILE_SITEKEY = "0x4AAAAAAD6JJPjdx7gnHwnf";

  /* Mirror of the Worker's payload caps (wrangler.toml). Checked client-side
     so the user gets a friendly message instead of a 400. */
  var LIMIT_PER_MESSAGE = 100000;
  var LIMIT_TOTAL = 240000;
  var LIMIT_TURNS = 16;

  var MAX_FILES = 4;
  var MAX_FILE_CHARS = 90000;
  var STORE_KEY = "m2assist.v1";

  var SUGGESTIONS = [
    "Why does my OnKey script stop halfway through with no error?",
    "How do I spawn a vehicle in front of the player?",
    "Show me a minimal Ess menu bound to F8",
    "How do I make a repeating timer?"
  ];

  var FILE_ACCEPT = ".lua,.txt,.log,.ini,.md,.json";
  var LANG_BY_EXT = { lua: "lua", json: "json", md: "markdown", ini: "text", log: "text", txt: "text" };

  /* ---- svg icons (inline so the page stays dependency-free) ----------- */
  var ICONS = {
    send: '<svg viewBox="0 0 16 16" width="15" height="15" fill="currentColor"><path d="M8 1.5l5.5 5.5-1.06 1.06L8.75 4.37V14.5h-1.5V4.37L3.56 8.06 2.5 7z"/></svg>',
    stop: '<svg viewBox="0 0 16 16" width="13" height="13" fill="currentColor"><rect x="3" y="3" width="10" height="10" rx="1.5"/></svg>',
    clip: '<svg viewBox="0 0 16 16" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M13.2 7.3l-5.1 5.1a3.1 3.1 0 01-4.4-4.4l5.8-5.8a2.1 2.1 0 013 3l-5.5 5.5a1.05 1.05 0 01-1.5-1.5l4.8-4.8"/></svg>',
    copy: '<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/><path d="M10.5 5.5v-2a1.5 1.5 0 00-1.5-1.5H4A1.5 1.5 0 002.5 3.5v5A1.5 1.5 0 004 10h1.5"/></svg>',
    redo: '<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M2.5 8a5.5 5.5 0 019.3-4L13.5 5.7M13.5 2v4h-4"/><path d="M13.5 8a5.5 5.5 0 01-9.3 4L2.5 10.3M2.5 14v-4h4"/></svg>'
  };

  /* ---- element handles ------------------------------------------------ */
  function $(id) { return document.getElementById(id); }
  var logEl, inputEl, sendBtn, attachBtn, fileInput, chipsEl, statusEl,
      hintEl, counterEl, composerEl, formEl;

  /* ---- state ---------------------------------------------------------- */
  /* history entries: { role, content, display?, files?, think?, ms? }
     Only { role, content } is ever sent to the Worker. */
  var history = [];
  var attachments = [];    /* { name, lang, text, size } */
  var session = null;      /* { token, expiresAt } */
  var busy = false;
  var abortCtl = null;
  var seq = 0;

  /* ================= rendering ================= */

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function inline(md) {
    /* input is already HTML-escaped */
    return md
      .replace(/`([^`\n]+)`/g, function (_, c) { return "<code>" + c + "</code>"; })
      .replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>")
      .replace(/\[([^\]\n]+)\]\((https?:[^)\s]+)\)/g,
        '<a href="$2" target="_blank" rel="noopener noreferrer nofollow">$1</a>')
      .replace(/(^|[\s(])((?:https?:\/\/)[^\s<)]+[^\s<).,])/g,
        '$1<a href="$2" target="_blank" rel="noopener noreferrer nofollow">$2</a>');
  }

  function renderTable(lines) {
    var rows = lines.map(function (l) {
      return l.replace(/^\||\|$/g, "").split("|").map(function (c) { return c.trim(); });
    });
    var html = '<div class="md-tablewrap"><table>';
    rows.forEach(function (cells, i) {
      if (i === 1 && cells.every(function (c) { return /^:?-{2,}:?$/.test(c); })) return;
      var tag = i === 0 ? "th" : "td";
      html += "<tr>" + cells.map(function (c) {
        return "<" + tag + ">" + inline(c) + "</" + tag + ">";
      }).join("") + "</tr>";
    });
    return html + "</table></div>";
  }

  /* A | row only starts a table when its |---| separator has ALSO arrived.
     During streaming the first row lands a chunk before the separator; without
     this look-ahead, that line was claimed by no branch and the paragraph loop
     spun forever appending empty <p></p> until "Invalid string length". */
  function isTableStart(lines, i) {
    return /^\s*\|.*\|\s*$/.test(lines[i]) && i + 1 < lines.length &&
      /^\s*\|[\s:|-]+\|\s*$/.test(lines[i + 1]);
  }

  function renderProse(text) {
    var lines = escapeHtml(text).split("\n");
    var html = "", i = 0;
    while (i < lines.length) {
      var line = lines[i];

      if (!line.trim()) { i++; continue; }

      if (isTableStart(lines, i)) {
        var tbl = [];
        while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) tbl.push(lines[i++]);
        html += renderTable(tbl);
        continue;
      }

      /* headers */
      var h = line.match(/^(#{1,6})\s+(.*)$/);
      if (h) { html += '<div class="md-h">' + inline(h[2]) + "</div>"; i++; continue; }

      /* lists */
      if (/^\s*([-*]|\d+\.)\s+/.test(line)) {
        var ordered = /^\s*\d+\./.test(line);
        var items = [];
        while (i < lines.length && /^\s*([-*]|\d+\.)\s+/.test(lines[i])) {
          items.push(lines[i].replace(/^\s*([-*]|\d+\.)\s+/, ""));
          i++;
        }
        var tag2 = ordered ? "ol" : "ul";
        html += "<" + tag2 + ">" + items.map(function (it) {
          return "<li>" + inline(it) + "</li>";
        }).join("") + "</" + tag2 + ">";
        continue;
      }

      /* paragraph: consume until blank line or a line another branch owns */
      var para = [];
      while (i < lines.length && lines[i].trim() &&
             !/^(#{1,6})\s|^\s*([-*]|\d+\.)\s/.test(lines[i]) &&
             !isTableStart(lines, i)) {
        para.push(lines[i]); i++;
      }
      /* guaranteed progress: whatever happens above, never loop in place */
      if (!para.length) { para.push(lines[i]); i++; }
      html += "<p>" + inline(para.join("<br>")) + "</p>";
    }
    return html;
  }

  function renderMarkdown(text) {
    var out = "";
    var parts = text.split("```");
    for (var i = 0; i < parts.length; i++) {
      if (i % 2 === 1) {
        var m = parts[i].match(/^([a-zA-Z0-9_-]*)\n([\s\S]*)$/);
        var lang = m ? (m[1] || "code") : "code";
        var code = m ? m[2] : parts[i];
        out += '<div class="codeblock"><div class="codehead"><span>' +
          escapeHtml(lang) + '</span><button type="button" class="ghost-btn copy-code">' +
          ICONS.copy + " Copy</button></div><pre><code>" +
          escapeHtml(code.replace(/\n$/, "")) + "</code></pre></div>";
      } else {
        out += renderProse(parts[i]);
      }
    }
    return out;
  }

  /* Split inline <think>...</think> out of raw streamed content. */
  function splitThink(raw) {
    if (raw.lastIndexOf("<think>", 0) !== 0) return { think: "", rest: raw };
    var end = raw.indexOf("</think>");
    if (end === -1) return { think: raw.slice(7), rest: "" };
    return { think: raw.slice(7, end), rest: raw.slice(end + 8) };
  }

  function humanSize(n) {
    return n < 1024 ? n + " B" : (n / 1024).toFixed(1) + " KB";
  }

  function pinned() {
    return logEl.scrollHeight - logEl.scrollTop - logEl.clientHeight < 90;
  }
  function scrollDown(force) {
    if (force || pinned()) logEl.scrollTop = logEl.scrollHeight;
  }

  /* ---- message rows ---- */

  function emptyState() {
    var d = document.createElement("div");
    d.id = "chat-empty";
    d.innerHTML =
      '<div class="empty-title">Mercs2 modding assistant</div>' +
      '<div class="empty-sub">Answers come from this wiki’s own pages. ' +
      "Paste a script, attach a .lua file, or start with one of these:</div>" +
      '<div class="sugg-row">' + SUGGESTIONS.map(function (s) {
        return '<button type="button" class="sugg">' + escapeHtml(s) + "</button>";
      }).join("") + "</div>";
    return d;
  }

  function clearEmptyState() {
    var e = $("chat-empty");
    if (e) e.remove();
  }

  function addUserRow(displayText, files) {
    clearEmptyState();
    var row = document.createElement("div");
    row.className = "row user";
    var chips = (files && files.length)
      ? '<div class="msg-files">' + files.map(function (f) {
          return '<span class="chip static">' + ICONS.clip + " " +
            escapeHtml(f.name) + " <small>" + humanSize(f.size) + "</small></span>";
        }).join("") + "</div>"
      : "";
    row.innerHTML =
      '<div class="avatar av-user">You</div>' +
      '<div class="content"><div class="who">You</div>' + chips +
      '<div class="body"></div></div>';
    row.querySelector(".body").innerHTML =
      "<p>" + escapeHtml(displayText || "(attached files)").replace(/\n/g, "<br>") + "</p>";
    logEl.appendChild(row);
    scrollDown(true);
    return row;
  }

  function addAssistantRow() {
    clearEmptyState();
    var row = document.createElement("div");
    row.className = "row assistant";
    row.id = "arow-" + (++seq);
    row.innerHTML =
      '<div class="avatar av-bot">M2</div>' +
      '<div class="content"><div class="who">Assistant</div>' +
      '<details class="think" hidden><summary><span class="think-label">Thinking…</span></summary>' +
      '<div class="think-body"></div></details>' +
      '<div class="body"><span class="typing">▋</span></div>' +
      '<div class="meta" hidden></div></div>';
    logEl.appendChild(row);
    scrollDown(true);
    return row;
  }

  function finishAssistantRow(row, entry, opts) {
    var meta = row.querySelector(".meta");
    var bits = [];
    if (entry.ms) bits.push((entry.ms / 1000).toFixed(1) + "s");
    if (opts && opts.stopped) bits.push("stopped");
    meta.innerHTML =
      '<span class="meta-time">' + bits.join(" · ") + "</span>" +
      '<span class="meta-actions">' +
      '<button type="button" class="ghost-btn copy-msg">' + ICONS.copy + " Copy</button>" +
      '<button type="button" class="ghost-btn regen-btn">' + ICONS.redo + " Regenerate</button>" +
      "</span>";
    meta.hidden = false;
    row.__raw = entry.content || "";
    /* only the LAST assistant row offers regenerate */
    var regs = logEl.querySelectorAll(".regen-btn");
    for (var i = 0; i < regs.length - 1; i++) regs[i].remove();
  }

  function addErrorRow(message) {
    var row = document.createElement("div");
    row.className = "row error-row";
    row.innerHTML =
      '<div class="avatar av-err">!</div>' +
      '<div class="content"><div class="who">Error</div><div class="body"><p>' +
      escapeHtml(message) + '</p><button type="button" class="btn retry-btn">Try again</button></div></div>';
    logEl.appendChild(row);
    scrollDown(true);
  }

  /* ================= persistence ================= */

  function persist() {
    try {
      sessionStorage.setItem(STORE_KEY, JSON.stringify({ history: history }));
    } catch (e) { /* storage full or blocked — chat still works */ }
  }

  function restore() {
    var raw;
    try { raw = sessionStorage.getItem(STORE_KEY); } catch (e) { return; }
    if (!raw) return;
    var data;
    try { data = JSON.parse(raw); } catch (e) { return; }
    if (!data || !Array.isArray(data.history) || !data.history.length) return;
    history = data.history;
    history.forEach(function (m) {
      if (m.role === "user") {
        addUserRow(m.display !== undefined ? m.display : m.content, m.files || []);
      } else {
        var row = addAssistantRow();
        row.querySelector(".body").innerHTML = renderMarkdown(m.content || "");
        if (m.think) {
          var d = row.querySelector(".think");
          d.hidden = false;
          d.querySelector(".think-label").textContent = "Thought process";
          d.querySelector(".think-body").textContent = m.think;
        }
        finishAssistantRow(row, m);
      }
    });
    scrollDown(true);
  }

  /* ================= turnstile / session ================= */

  var widgetId = null;

  function waitForTurnstile(ms) {
    return new Promise(function (resolve, reject) {
      var t0 = Date.now();
      (function poll() {
        if (typeof turnstile !== "undefined") return resolve();
        if (Date.now() - t0 > ms) {
          return reject(new Error("Verification widget failed to load. An ad blocker may be blocking challenges.cloudflare.com."));
        }
        setTimeout(poll, 120);
      })();
    });
  }

  function getTurnstileToken() {
    return waitForTurnstile(6000).then(function () {
      return new Promise(function (resolve, reject) {
        var holder = $("turnstile-holder");
        holder.hidden = false;
        if (widgetId !== null) turnstile.reset(widgetId);
        widgetId = turnstile.render("#turnstile-holder", {
          sitekey: TURNSTILE_SITEKEY,
          size: "flexible",
          callback: function (tok) { holder.hidden = true; resolve(tok); },
          "error-callback": function () { reject(new Error("Verification failed. Reload and try again.")); }
        });
      });
    });
  }

  function ensureSession() {
    if (session && session.expiresAt > Date.now() / 1000 + 30) {
      return Promise.resolve(session.token);
    }
    setStatus("Verifying you’re human…");
    return getTurnstileToken().then(function (tok) {
      return fetch(WORKER_URL + "/session", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ turnstileToken: tok })
      });
    }).then(function (res) {
      return res.json().then(function (data) {
        if (!res.ok) throw new Error(data.message || "Could not start a session.");
        session = { token: data.session, expiresAt: data.expiresAt };
        setStatus("");
        return session.token;
      });
    });
  }

  /* ================= sending ================= */

  function setStatus(text, isError) {
    statusEl.textContent = text || "";
    statusEl.className = isError ? "error" : "";
  }

  function setBusy(b) {
    busy = b;
    sendBtn.innerHTML = b ? ICONS.stop : ICONS.send;
    sendBtn.title = b ? "Stop (Esc)" : "Send (Enter)";
    sendBtn.classList.toggle("stop", b);
    attachBtn.disabled = b;
  }

  function payloadChars() {
    var n = inputEl.value.length;
    attachments.forEach(function (f) { n += f.text.length + f.name.length + 80; });
    return n;
  }

  function updateCounter() {
    var n = payloadChars();
    if (n > 50000) {
      counterEl.hidden = false;
      counterEl.textContent = n.toLocaleString() + " / " + LIMIT_PER_MESSAGE.toLocaleString() + " characters";
      counterEl.classList.toggle("over", n > LIMIT_PER_MESSAGE);
    } else {
      counterEl.hidden = true;
    }
  }

  function attachmentBlock(f) {
    return "\n\n--- attached file: " + f.name + " (" + humanSize(f.size) + ") ---\n" +
      "```" + f.lang + "\n" + f.text + "\n```\n--- end of attached file ---";
  }

  function stripForApi(list) {
    return list.map(function (m) { return { role: m.role, content: m.content }; });
  }

  function submit() {
    if (busy) return;
    var q = inputEl.value.trim();
    if (!q && !attachments.length) return;

    if (history.length >= LIMIT_TURNS) {
      setStatus("This conversation is at its length limit — start a new one.", true);
      return;
    }
    var content = q + attachments.map(attachmentBlock).join("");
    if (content.length > LIMIT_PER_MESSAGE) {
      setStatus("Message too large (" + content.length.toLocaleString() +
        " chars, limit " + LIMIT_PER_MESSAGE.toLocaleString() + "). Trim the attachments.", true);
      return;
    }
    var total = content.length;
    history.forEach(function (m) { total += m.content.length; });
    if (total > LIMIT_TOTAL) {
      setStatus("Conversation too long for one thread — start a new one.", true);
      return;
    }

    var files = attachments.map(function (f) { return { name: f.name, size: f.size }; });
    history.push({ role: "user", content: content, display: q, files: files });
    addUserRow(q, files);
    inputEl.value = "";
    attachments = [];
    renderChips();
    autoGrow();
    updateCounter();
    setStatus("");
    persist();
    runCompletion();
  }

  function runCompletion() {
    setBusy(true);
    var row = addAssistantRow();
    var body = row.querySelector(".body");
    var think = row.querySelector(".think");
    var thinkBody = row.querySelector(".think-body");
    var thinkLabel = row.querySelector(".think-label");

    var reasoning = "";
    var answerRaw = "";
    var t0 = Date.now();
    var tContent = 0;
    abortCtl = new AbortController();

    function paint() {
      var st = splitThink(answerRaw);
      var allThink = (reasoning + st.think).trim();
      if (allThink) {
        think.hidden = false;
        if (!st.rest && !think.__closed) think.open = true;
        thinkBody.textContent = allThink;
      }
      if (st.rest) {
        if (!tContent) {
          tContent = Date.now();
          if (allThink) {
            thinkLabel.textContent = "Thought for " + ((tContent - t0) / 1000).toFixed(1) + "s";
            think.open = false;
            think.__closed = true;
          }
        }
        body.innerHTML = renderMarkdown(st.rest) + '<span class="typing">▋</span>';
      }
      scrollDown(false);
      return st;
    }

    function finalize(stopped) {
      var st = splitThink(answerRaw);
      var allThink = (reasoning + st.think).trim();
      var entry = null;
      if (st.rest || allThink) {
        entry = {
          role: "assistant",
          content: st.rest || "(no answer text)",
          think: allThink || undefined,
          ms: (tContent || Date.now()) - t0
        };
        history.push(entry);
        body.innerHTML = renderMarkdown(entry.content);
        if (allThink && !think.__closed) {
          thinkLabel.textContent = "Thought process";
          think.open = false;
        }
        finishAssistantRow(row, entry, { stopped: stopped });
        persist();
      } else {
        row.remove();
        if (!stopped) addErrorRow("No answer came back. Try again.");
      }
      setBusy(false);
      abortCtl = null;
      scrollDown(false);
    }

    ensureSession().then(function (token) {
      return fetch(WORKER_URL + "/chat", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ session: token, messages: stripForApi(history) }),
        signal: abortCtl.signal
      });
    }).then(function (res) {
      if (!res.ok) {
        return res.json().catch(function () { return {}; }).then(function (err) {
          if (res.status === 401) session = null;
          throw new Error(err.message || "Request failed (" + res.status + ").");
        });
      }
      var reader = res.body.getReader();
      var decoder = new TextDecoder();
      var buffer = "";
      function pump() {
        return reader.read().then(function (chunk) {
          if (chunk.done) return;
          buffer += decoder.decode(chunk.value, { stream: true });
          var frames = buffer.split("\n\n");
          buffer = frames.pop();
          frames.forEach(function (frame) {
            var line = frame.trim();
            if (line.lastIndexOf("data:", 0) !== 0) return;
            var payload = line.slice(5).trim();
            if (payload === "[DONE]") return;
            var obj;
            try { obj = JSON.parse(payload); } catch (e) { return; }
            var delta = obj.choices && obj.choices[0] && obj.choices[0].delta;
            if (!delta) return;
            if (delta.reasoning_content) reasoning += delta.reasoning_content;
            if (delta.content) answerRaw += delta.content;
            paint();
          });
          return pump();
        });
      }
      return pump();
    }).then(function () {
      finalize(false);
    }).catch(function (e) {
      if (e && e.name === "AbortError") { finalize(true); return; }
      row.remove();
      setBusy(false);
      abortCtl = null;
      addErrorRow(e && e.message ? e.message : String(e));
    });
  }

  function regenerate() {
    if (busy || !history.length) return;
    if (history[history.length - 1].role !== "assistant") return;
    history.pop();
    var rows = logEl.querySelectorAll(".row.assistant");
    if (rows.length) rows[rows.length - 1].remove();
    persist();
    runCompletion();
  }

  /* ================= attachments ================= */

  function renderChips() {
    chipsEl.innerHTML = attachments.map(function (f, i) {
      return '<span class="chip">' + ICONS.clip + " " + escapeHtml(f.name) +
        " <small>" + humanSize(f.size) + "</small>" +
        '<button type="button" class="chip-x" data-i="' + i + '" title="Remove">×</button></span>';
    }).join("");
    chipsEl.hidden = attachments.length === 0;
    updateCounter();
  }

  function addFiles(fileList) {
    var files = Array.prototype.slice.call(fileList);
    files.forEach(function (file) {
      if (attachments.length >= MAX_FILES) {
        setStatus("At most " + MAX_FILES + " files per message.", true);
        return;
      }
      var ext = (file.name.split(".").pop() || "").toLowerCase();
      if (!(ext in LANG_BY_EXT)) {
        setStatus("Only text files are supported (" + FILE_ACCEPT + ").", true);
        return;
      }
      var reader = new FileReader();
      reader.onload = function () {
        var text = String(reader.result || "");
        if (text.length > MAX_FILE_CHARS) {
          setStatus(file.name + " is too large (" + text.length.toLocaleString() +
            " chars, limit " + MAX_FILE_CHARS.toLocaleString() + "). Paste the relevant part instead.", true);
          return;
        }
        attachments.push({ name: file.name, lang: LANG_BY_EXT[ext], text: text, size: file.size });
        setStatus("");
        renderChips();
      };
      reader.readAsText(file);
    });
  }

  /* ================= composer ================= */

  function autoGrow() {
    inputEl.style.height = "auto";
    inputEl.style.height = Math.min(inputEl.scrollHeight, 220) + "px";
  }

  function newConversation() {
    if (busy && abortCtl) abortCtl.abort();
    history = [];
    attachments = [];
    renderChips();
    logEl.innerHTML = "";
    logEl.appendChild(emptyState());
    setStatus("");
    try { sessionStorage.removeItem(STORE_KEY); } catch (e) { /* fine */ }
    inputEl.focus();
  }

  function copyText(text, btn) {
    var done = function () {
      if (!btn) return;
      var old = btn.innerHTML;
      btn.innerHTML = "Copied";
      setTimeout(function () { btn.innerHTML = old; }, 1200);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, done);
    } else {
      var ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta);
      ta.select(); document.execCommand("copy"); ta.remove(); done();
    }
  }

  /* ================= wiring ================= */

  function init() {
    logEl = $("chat-log"); inputEl = $("chat-input"); sendBtn = $("chat-send");
    attachBtn = $("attach-btn"); fileInput = $("file-input"); chipsEl = $("attach-chips");
    statusEl = $("chat-status"); hintEl = $("chat-hint"); counterEl = $("chat-counter");
    /* the composer <form> is both the submit target and the drop zone */
    composerEl = $("composer"); formEl = composerEl;
    if (!logEl || !formEl) return;

    sendBtn.innerHTML = ICONS.send;
    attachBtn.innerHTML = ICONS.clip;
    fileInput.accept = FILE_ACCEPT;
    logEl.appendChild(emptyState());
    restore();

    formEl.addEventListener("submit", function (e) {
      e.preventDefault();
      if (busy) { if (abortCtl) abortCtl.abort(); return; }
      submit();
    });

    inputEl.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        formEl.dispatchEvent(new Event("submit", { cancelable: true }));
      }
    });
    inputEl.addEventListener("input", function () { autoGrow(); updateCounter(); });

    window.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && busy && abortCtl) abortCtl.abort();
    });

    attachBtn.addEventListener("click", function () { fileInput.click(); });
    fileInput.addEventListener("change", function () {
      addFiles(fileInput.files);
      fileInput.value = "";
    });

    ["dragover", "dragenter"].forEach(function (ev) {
      composerEl.addEventListener(ev, function (e) {
        e.preventDefault();
        composerEl.classList.add("dragging");
      });
    });
    ["dragleave", "drop"].forEach(function (ev) {
      composerEl.addEventListener(ev, function (e) {
        e.preventDefault();
        composerEl.classList.remove("dragging");
      });
    });
    composerEl.addEventListener("drop", function (e) {
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length) {
        addFiles(e.dataTransfer.files);
      }
    });

    $("chat-reset").addEventListener("click", newConversation);

    /* one delegated handler for everything inside the log + chips */
    document.addEventListener("click", function (e) {
      var t = e.target.closest ? e.target : null;
      if (!t) return;
      var el;
      if ((el = e.target.closest(".sugg"))) {
        inputEl.value = el.textContent;
        autoGrow();
        formEl.dispatchEvent(new Event("submit", { cancelable: true }));
      } else if ((el = e.target.closest(".copy-code"))) {
        var pre = el.closest(".codeblock").querySelector("code");
        copyText(pre.textContent, el);
      } else if ((el = e.target.closest(".copy-msg"))) {
        var r = el.closest(".row");
        copyText(r.__raw || "", el);
      } else if ((el = e.target.closest(".regen-btn"))) {
        regenerate();
      } else if ((el = e.target.closest(".retry-btn"))) {
        el.closest(".row").remove();
        if (history.length && history[history.length - 1].role === "user") runCompletion();
      } else if ((el = e.target.closest(".chip-x"))) {
        attachments.splice(parseInt(el.getAttribute("data-i"), 10), 1);
        renderChips();
      }
    });

    autoGrow();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
