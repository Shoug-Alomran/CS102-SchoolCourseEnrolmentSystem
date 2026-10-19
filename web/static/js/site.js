/* CS102 enrolment site: workspace behaviour. No dependencies. */
(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.add("js");

  function store(key, value) {
    try {
      if (value === undefined) return JSON.parse(localStorage.getItem(key));
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      return null;
    }
  }

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- Theme ---------- */
  $$("[data-theme-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var next = doc.dataset.theme === "light" ? "dark" : "light";
      doc.dataset.theme = next;
      try { localStorage.setItem("ce-theme", next); } catch (e) { /* private mode */ }
    });
  });

  /* ---------- Project drawer (narrow screens) ---------- */
  function setTree(open) {
    document.body.classList.toggle("tree-open", open);
    $$("[data-toggle-tree]").forEach(function (b) { b.setAttribute("aria-expanded", String(open)); });
  }
  $$("[data-toggle-tree]").forEach(function (b) {
    b.addEventListener("click", function () { setTree(!document.body.classList.contains("tree-open")); });
  });
  $$(".tree a").forEach(function (a) { a.addEventListener("click", function () { setTree(false); }); });

  /* ---------- Editor tabs: recently opened pages ---------- */
  var tabs = $("[data-tabs]");
  if (tabs) {
    var current = {
      path: tabs.dataset.current,
      label: tabs.dataset.label,
      icon: tabs.dataset.icon,
      letter: tabs.dataset.letter
    };
    var list = store("ce-tabs") || [];
    if (!Array.isArray(list)) list = [];
    list = list.filter(function (t) { return t && t.path !== current.path && t.path !== "404.html"; });
    if (current.path !== "404.html") list.unshift(current);
    list = list.slice(0, 7);
    store("ce-tabs", list);
    var order = (store("ce-tab-order") || []).filter(function (p) { return list.some(function (t) { return t.path === p; }); });
    list.forEach(function (t) { if (order.indexOf(t.path) < 0) order.push(t.path); });
    store("ce-tab-order", order);
    var ordered = order.map(function (p) { return list.filter(function (t) { return t.path === p; })[0]; });

    tabs.innerHTML = ordered.map(function (t) {
      var active = t.path === current.path;
      return '<a class="tab' + (active ? " is-active" : "") + '" role="listitem" href="/' + escapeHtml(t.path) + '"' +
        (active ? ' aria-current="page"' : "") + ">" +
        '<span class="fi fi-' + escapeHtml(t.icon) + '" aria-hidden="true">' + escapeHtml(t.letter || "") + "</span>" +
        "<span>" + escapeHtml(t.label) + "</span>" +
        '<button class="tab-x" type="button" data-close="' + escapeHtml(t.path) + '" aria-label="Close ' + escapeHtml(t.label) + '">×</button></a>';
    }).join("");

    tabs.addEventListener("click", function (e) {
      var x = e.target.closest("[data-close]");
      if (!x) return;
      e.preventDefault();
      var path = x.dataset.close;
      var remaining = (store("ce-tabs") || []).filter(function (t) { return t.path !== path; });
      store("ce-tabs", remaining);
      store("ce-tab-order", (store("ce-tab-order") || []).filter(function (p) { return p !== path; }));
      if (path === current.path) {
        location.href = "/" + (remaining[0] ? remaining[0].path : "");
      } else {
        x.closest(".tab").remove();
      }
    });
    var active = $(".tab.is-active", tabs);
    if (active) active.scrollIntoView({ block: "nearest", inline: "nearest" });
  }

  /* ---------- Class pages: Overview / Source ---------- */
  var panels = $$("[data-view-panel]");
  var switches = $$("[data-view]");
  function showView(name) {
    panels.forEach(function (p) { p.hidden = p.dataset.viewPanel !== name; });
    switches.forEach(function (b) { b.setAttribute("aria-selected", String(b.dataset.view === name)); });
  }
  function flashLine(n) {
    var row = document.getElementById("L" + n);
    if (!row) return;
    $$(".l.is-hit").forEach(function (r) { r.classList.remove("is-hit"); });
    row.classList.add("is-hit");
    row.scrollIntoView({ block: "center" });
  }
  function fromHash() {
    var h = location.hash;
    if (!panels.length) return;
    if (/^#L\d+$/.test(h)) {
      showView("source");
      flashLine(h.slice(2));
    } else if (h === "#source") {
      showView("source");
      window.scrollTo(0, 0);
    } else {
      showView("overview");
    }
  }
  if (panels.length) {
    switches.forEach(function (b) {
      b.addEventListener("click", function () {
        var name = b.dataset.view;
        history.replaceState(null, "", name === "source" ? "#source" : location.pathname);
        showView(name);
      });
    });
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-goto-line]");
      if (!a) return;
      e.preventDefault();
      history.pushState(null, "", "#L" + a.dataset.gotoLine);
      showView("source");
      flashLine(a.dataset.gotoLine);
    });
    window.addEventListener("hashchange", fromHash);
    fromHash();
  }

  $$("[data-copy-source]").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = $$("[data-source] .c").map(function (c) { return c.textContent; }).join("\n");
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(function () {
        b.textContent = "Copied";
        setTimeout(function () { b.textContent = "Copy"; }, 1600);
      }, function () { b.textContent = "Select and copy"; });
    });
  });

  /* ---------- Structure scrollspy ---------- */
  var sLinks = $$(".structure a");
  if (sLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    sLinks.forEach(function (a) { byId[decodeURIComponent(a.hash.slice(1))] = a; });
    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
      var first = sLinks.filter(function (a) { return visible[decodeURIComponent(a.hash.slice(1))]; })[0];
      if (!first) return;
      sLinks.forEach(function (a) { a.classList.toggle("is-current", a === first); });
      var box = first.closest(".pane");
      if (box) {
        var r = first.getBoundingClientRect(), b = box.getBoundingClientRect();
        if (r.top < b.top + 40 || r.bottom > b.bottom - 10) box.scrollTop += r.top - b.top - b.height / 3;
      }
    }, { rootMargin: "-90px 0px -55% 0px" });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
    sLinks.forEach(function (a) {
      a.addEventListener("click", function () {
        if (a.hash === "#source") return;
        if (panels.length && !/^#L/.test(a.hash)) showView("overview");
      });
    });
  }

  /* ---------- Known issues filter ---------- */
  var issueBox = $("[data-issues]");
  if (issueBox) {
    $$("[data-filter]").forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.dataset.filter;
        $$("[data-filter]").forEach(function (o) {
          o.classList.toggle("is-on", o === b);
          o.setAttribute("aria-pressed", String(o === b));
        });
        $$(".issue", issueBox).forEach(function (i) { i.hidden = k !== "all" && i.dataset.kind !== k; });
      });
    });
  }

  /* ---------- Validator lab ---------- */
  var lab = $("[data-validator-lab]");
  var sample = window.CE_SAMPLE;
  if (lab && sample) {
    var rules = {
      ValidateName: function (v) { return v.length > 3; },
      ValidatePassword: function (v) { return v.length > 8; },
      ValidateEmail: function (v) { return v.indexOf("@") >= 0 && v.indexOf(".") >= 0; },
      ValidatePhoneNumber: function (v) { return v.length === 10; },
      ValidateAddress: function (v) { return v.length > 3; }
    };
    lab.innerHTML = '<div class="lab"><label for="lab-in">Try a validator</label><div class="lab-row">' +
      '<select id="lab-m" aria-label="Validator">' + sample.validators.map(function (v) {
        return "<option>" + escapeHtml(v.method) + "</option>";
      }).join("") + "</select>" +
      '<input id="lab-in" autocomplete="off" spellcheck="false" placeholder="Type a value">' +
      '<span class="lab-out badge" aria-live="polite"></span></div></div>';
    var sel = $("#lab-m", lab), inp = $("#lab-in", lab), out = $(".lab-out", lab);
    function run() {
      var v = inp.value;
      if (!v) { out.className = "lab-out badge"; out.textContent = "waiting"; return; }
      var ok = rules[sel.value](v);
      out.className = "lab-out badge " + (ok ? "ok" : "bug");
      out.textContent = ok ? "true" : "false";
    }
    sel.addEventListener("change", function () {
      var v = sample.validators.filter(function (x) { return x.method === sel.value; })[0];
      inp.placeholder = "e.g. " + v.ok;
      run();
    });
    inp.addEventListener("input", run);
    sel.dispatchEvent(new Event("change"));
  }

  /* ---------- Search everywhere ---------- */
  var palette = $("#palette");
  var index = null;
  var selected = 0;
  var results = [];
  var KIND = { "class": "class", method: "method", field: "field", "const": "const", "enum": "enum", page: "page",
    option: "menu", file: "file", issue: "issue" };
  var ICON = { "class": ["cls", "C"], method: ["m", "m"], field: ["f", "f"], "const": ["f", "f"], "enum": ["e", "e"],
    page: ["md", ""], option: ["run", "▶"], file: ["txt", ""], issue: ["x", "!"] };

  function score(entry, q) {
    var t = entry.t.toLowerCase();
    var x = (entry.x + " " + entry.p).toLowerCase();
    if (t === q) return 100;
    if (t.indexOf(q) === 0) return 80;
    var tail = t.split(".").pop();
    if (tail.indexOf(q) === 0) return 70;
    if (t.indexOf(q) >= 0) return 55;
    var words = q.split(/\s+/).filter(Boolean);
    if (words.length > 1 && words.every(function (w) { return t.indexOf(w) >= 0 || x.indexOf(w) >= 0; })) return 35;
    if (x.indexOf(q) >= 0) return 20;
    var i = 0;
    for (var k = 0; k < t.length && i < q.length; k++) if (t[k] === q[i]) i++;
    return i === q.length ? 10 : 0;
  }

  function mark(text, q) {
    var i = text.toLowerCase().indexOf(q);
    if (!q || i < 0) return escapeHtml(text);
    return escapeHtml(text.slice(0, i)) + "<mark>" + escapeHtml(text.slice(i, i + q.length)) + "</mark>" + escapeHtml(text.slice(i + q.length));
  }

  function render(q) {
    var list = $(".pal-list", palette);
    q = q.trim().toLowerCase();
    if (!index) { list.innerHTML = '<li class="pal-empty">Loading…</li>'; return; }
    if (!q) {
      results = index.filter(function (e) { return e.k === "class" || e.k === "page"; }).slice(0, 14);
    } else {
      results = index.map(function (e) { return { e: e, s: score(e, q) }; })
        .filter(function (r) { return r.s > 0; })
        .sort(function (a, b) { return b.s - a.s || a.e.t.length - b.e.t.length; })
        .slice(0, 40).map(function (r) { return r.e; });
    }
    selected = 0;
    if (!results.length) { list.innerHTML = '<li class="pal-empty">Nothing matches “' + escapeHtml(q) + "”</li>"; return; }
    list.innerHTML = results.map(function (e, i) {
      var ic = ICON[e.k] || ["md", ""];
      return '<li><a href="' + escapeHtml(e.u) + '" data-i="' + i + '"' + (i === 0 ? ' aria-selected="true"' : "") + ">" +
        '<span class="fi fi-' + ic[0] + '" aria-hidden="true">' + ic[1] + "</span>" +
        "<span><span>" + mark(e.t, q) + "</span>" + (e.x || e.p ? '<span class="pal-x">' + escapeHtml(e.p ? e.p + " · " + e.x : e.x) + "</span>" : "") + "</span>" +
        '<span class="pal-k">' + (KIND[e.k] || e.k) + "</span></a></li>";
    }).join("");
  }

  function move(d) {
    var links = $$(".pal-list a", palette);
    if (!links.length) return;
    selected = (selected + d + links.length) % links.length;
    links.forEach(function (a, i) { a.setAttribute("aria-selected", String(i === selected)); });
    links[selected].scrollIntoView({ block: "nearest" });
  }

  var lastFocus = null;
  function openPalette() {
    if (!palette) return;
    lastFocus = document.activeElement;
    palette.innerHTML = '<div class="pal" role="dialog" aria-modal="true" aria-label="Search everywhere">' +
      '<div class="pal-head"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6"/><path d="m20 20-4.2-4.2"/></svg>' +
      '<input type="search" placeholder="Search classes, methods, menu options, files…" aria-label="Search" autocomplete="off" spellcheck="false">' +
      '<span class="pal-scope">everywhere</span></div><ul class="pal-list" role="listbox"></ul>' +
      '<div class="pal-foot"><span>↑↓ move</span><span>↵ open</span><span>esc close</span></div></div>';
    palette.hidden = false;
    var input = $("input", palette);
    input.focus();
    input.addEventListener("input", function () { render(input.value); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      if (e.key === "Enter") {
        var a = $$(".pal-list a", palette)[selected];
        if (a) { e.preventDefault(); closePalette(); location.href = a.href; }
      }
    });
    if (!index) {
      fetch("/search.json").then(function (r) { return r.json(); }).then(function (data) {
        index = data;
        render(input.value);
      }, function () { $(".pal-list", palette).innerHTML = '<li class="pal-empty">Search is unavailable offline.</li>'; });
    }
    render("");
  }
  function closePalette() {
    if (!palette || palette.hidden) return;
    palette.hidden = true;
    palette.innerHTML = "";
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  if (palette) {
    palette.addEventListener("click", function (e) {
      if (e.target === palette) closePalette();
      if (e.target.closest(".pal-list a")) closePalette();
    });
  }
  $$("[data-open-search]").forEach(function (b) { b.addEventListener("click", openPalette); });
  document.addEventListener("keydown", function (e) {
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName) || document.activeElement.isContentEditable;
    if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !typing)) {
      e.preventDefault();
      if (palette && palette.hidden) openPalette(); else closePalette();
    }
    if (e.key === "Escape") { closePalette(); setTree(false); }
  });

  window.CE = { escapeHtml: escapeHtml, $: $, $$: $$ };
})();
