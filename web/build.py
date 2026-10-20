#!/usr/bin/env python3
"""Build the CS102 enrolment site into ../_site.

Plain Python, no third-party packages. Content lives in web/content/*.py,
Java listings in web/java/, static assets in web/static/.

    python3 web/build.py          # build
    python3 web/build.py --serve  # build, then serve on http://localhost:8000
"""

import html
import json
import re
import shutil
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parent
sys.path.insert(0, str(WEB))

from content.classes import CLASSES  # noqa: E402
from content.data import (  # noqa: E402
    DEFAULT_ADMIN, EXAM_TYPES, EXCEPTIONS, FILES, GUARDS, PERSISTENCE, SAMPLE, VALIDATORS, lines_for,
)
from content.pages import (  # noqa: E402
    DESIGN, IMPROVEMENTS, ISSUES, POLICIES, REPORT_SECTIONS, SITE, STARTUP,
)
from content.workflows import WORKFLOWS  # noqa: E402

OUT = WEB.parent / "_site"
ASSET_VERSION = "4"
PAGES = []          # (path, title) for the sitemap
SEARCH = []         # search index entries

esc = html.escape


def url(path=""):
    """Root-relative URL for a page path like 'student/' or ''."""
    return "/" + path


# ---------------------------------------------------------------------------
# Java: highlighting and member parsing
# ---------------------------------------------------------------------------

KEYWORDS = set("""abstract assert boolean break byte case catch char class const continue default do double
else enum extends final finally float for goto if implements import instanceof int interface long native new
package private protected public return short static strictfp super switch synchronized this throw throws
transient try void volatile while var true false null""".split())

TOKEN = re.compile(r"""
    (?P<com>//.*)
  | (?P<bcs>/\*)
  | (?P<str>"(?:\\.|[^"\\])*"?)
  | (?P<chr>'(?:\\.|[^'\\])'?)
  | (?P<ann>@\w+)
  | (?P<num>\b\d+(?:\.\d+)?[dDfFlL]?\b)
  | (?P<id>[A-Za-z_$][\w$]*)
  | (?P<ws>\s+)
  | (?P<op>.)
""", re.X)


def highlight_java(code):
    """Return a list of highlighted HTML strings, one per source line."""
    out, in_block = [], False
    for line in code.split("\n"):
        parts, i = [], 0
        while i < len(line):
            if in_block:
                end = line.find("*/", i)
                stop = len(line) if end < 0 else end + 2
                parts.append(f'<span class="t-com">{esc(line[i:stop])}</span>')
                in_block = end < 0
                i = stop
                continue
            m = TOKEN.match(line, i)
            kind, text = m.lastgroup, m.group()
            if kind == "bcs":
                in_block = True
                continue
            if kind == "id":
                rest = line[m.end():].lstrip()
                if text in KEYWORDS:
                    cls = "t-kw"
                elif rest.startswith("("):
                    cls = "t-fn"
                elif text[0].isupper():
                    cls = "t-ty"
                else:
                    cls = None
            else:
                cls = {"com": "t-com", "str": "t-str", "chr": "t-str", "ann": "t-ann", "num": "t-num"}.get(kind)
            parts.append(f'<span class="{cls}">{esc(text)}</span>' if cls else esc(text))
            i = m.end()
        out.append("".join(parts))
    return out


def highlight_inline(sig):
    return highlight_java(sig)[0]


MODS = {"public", "private", "protected", "static", "final", "abstract", "synchronized"}


def parse_java(code, class_name):
    """Find class-level declarations (4-space indent) with line numbers."""
    lines = code.split("\n")
    members, header = [], None
    i = 0
    while i < len(lines):
        raw = lines[i]
        if header is None and re.match(r"^public\s.*\b(class|interface)\b", raw):
            header = re.sub(r"\s*\{\s*$", "", raw).strip()
        if not raw.startswith("    ") or raw.startswith("     "):
            i += 1
            continue
        s = raw.strip()
        if not s or s.startswith(("//", "/*", "*", "@", "}")):
            i += 1
            continue
        start = i
        sig = re.sub(r"//.*$", "", s)
        while not re.search(r"[{;]\s*(\}\s*)?$", sig) and i + 1 < len(lines):
            i += 1
            sig += " " + re.sub(r"//.*$", "", lines[i].strip())
        sig = re.sub(r"\s+", " ", sig).strip()
        i += 1
        enum = re.match(r"^((?:\w+\s+)*)enum\s+(\w+)", sig)
        if enum:
            body = []
            j = start + 1
            while j < len(lines) and "}" not in lines[j]:
                body.append(lines[j])
                j += 1
            values = [v.strip() for v in re.sub(r"[;\s]+", " ", " ".join(body)).replace(" ", "").split(",") if v.strip()]
            if not values:
                values = [v.strip() for v in re.findall(r"\{(.*)\}", sig)[0].split(",")] if "{" in sig else []
            members.append({"kind": "enum", "name": enum.group(2), "line": start + 1, "values": values,
                            "sig": f"enum {enum.group(2)}", "mods": enum.group(1).split()})
            i = j + 1
            continue
        paren = sig.find("(")
        eq = sig.find("=")
        if paren >= 0 and (eq < 0 or paren < eq):
            head = sig[:paren].strip()
            params = sig[paren + 1:sig.rfind(")")].strip()
            words = head.split()
            mods = []
            while words and words[0] in MODS:
                mods.append(words.pop(0))
            tparams = ""
            if words and words[0].startswith("<"):
                depth, k = 0, 0
                joined = " ".join(words)
                for k, ch in enumerate(joined):
                    depth += ch == "<"
                    depth -= ch == ">"
                    if depth == 0:
                        break
                tparams = joined[:k + 1]
                words = joined[k + 1:].split()
            if not words:
                continue
            name = words[-1]
            ret = " ".join(words[:-1])
            if not re.match(r"^\w+$", name) or name in KEYWORDS:
                continue
            kind = "ctor" if name == class_name and not ret else "method"
            clean = re.sub(r"\s*\{.*$", "", sig).rstrip(";").strip()
            members.append({"kind": kind, "name": name, "line": start + 1, "mods": mods, "ret": ret,
                            "tparams": tparams, "params": params, "sig": clean,
                            "abstract": "abstract" in mods})
        else:
            decl = re.sub(r"\s*=.*$", "", sig.rstrip(";")).strip()
            words = decl.split()
            mods = []
            while words and words[0] in MODS:
                mods.append(words.pop(0))
            rest = " ".join(words)
            mt = re.match(r"^([\w.$]+(?:<.*>)?(?:\[\])?)\s+(.+)$", rest)
            if not mt:
                continue
            ftype, names = mt.group(1), [n.strip() for n in mt.group(2).split(",")]
            const = "static" in mods and "final" in mods
            for n in names:
                members.append({"kind": "const" if const else "field", "name": n, "line": start + 1,
                                "mods": mods, "type": ftype, "sig": sig.rstrip(";")})
    return header, members


def vis(m):
    for v in ("public", "private", "protected"):
        if v in m.get("mods", []):
            return v
    return "package"


def accessor(name):
    return re.match(r"^(get|set)[A-Z]", name) is not None


# ---------------------------------------------------------------------------
# Small HTML helpers
# ---------------------------------------------------------------------------

ICON_TITLES = {"C": "Class", "A": "Abstract class", "S": "Static/singleton class", "M": "Main class",
               "I": "Instructor session", "R": "Run configuration"}


def file_icon(kind, letter=""):
    return f'<span class="fi fi-{kind}" aria-hidden="true">{esc(letter)}</span>'


def badge(text, tone=""):
    return f'<span class="badge {tone}">{esc(text)}</span>'


def code(text):
    return f"<code>{esc(text)}</code>"


def term_block(text, label=None):
    lines = "\n".join(esc(t) for t in text.split("\n"))
    head = f'<span class="term-label">{esc(label)}</span>' if label else ""
    return f'<pre class="term">{head}{lines}</pre>'


def section(id_, title, body, kicker=None, cls=""):
    k = f'<p class="kicker">{esc(kicker)}</p>' if kicker else ""
    return f'<section class="sec {cls}" id="{id_}">{k}<h2>{esc(title)}<a class="anchor" href="#{id_}" aria-label="Link to this section">#</a></h2>{body}</section>'


def by_slug(slug):
    return next(c for c in CLASSES if c["slug"] == slug)


def member_link(slug, method):
    if method is None:
        return url(slug + "/")
    return url(f"{slug}/#m-{method}")


# ---------------------------------------------------------------------------
# Project tree (left tool window)
# ---------------------------------------------------------------------------

def tree_items():
    src = [(c["slug"] + "/", c["file"], ("cls", c["icon"])) for c in CLASSES]
    runs = [("run/", "Main.run", ("run", "▶"))] + [
        (w["slug"] + "/", w["title"], ("run", "▶")) for w in WORKFLOWS]
    data = [(f"data-files/#{f['key']}", f["name"], ("txt", "")) for f in FILES]
    docs = [
        ("architecture/", "ARCHITECTURE.md", ("md", "")),
        ("validation/", "VALIDATION.md", ("md", "")),
        ("reports-and-statistics/", "REPORTS.md", ("md", "")),
        ("notes/", "KNOWN_ISSUES.md", ("md", "")),
        ("project-report/", "report.pdf", ("pdf", "")),
    ]
    return [
        ("folder", "src/schoolcourseenrolmentsystem", src, True),
        ("folder", "run configurations", runs, True),
        ("folder", "data", [("data-files/", "data/ (overview)", ("dir", ""))] + data, True),
        ("folder", "docs", docs, True),
        ("folder", "policies", [(p["slug"] + "/", p["title"], ("md", "")) for p in POLICIES], False),
    ]


def render_tree(active):
    out = ['<nav class="tree" aria-label="Project files">',
           f'<a class="tree-root{" is-active" if active == "" else ""}" href="{url()}">'
           f'{file_icon("proj")}<span>enrolment</span><span class="tree-dim">README.md</span></a>']
    for _, label, items, open_ in tree_items():
        has_active = any(p.split("#")[0] == active for p, _, _ in items)
        out.append(f'<details class="tree-folder"{" open" if open_ or has_active else ""}>'
                   f'<summary>{file_icon("dir")}<span>{esc(label)}</span></summary><ul>')
        for path, name, (kind, letter) in items:
            current = path == active
            out.append(f'<li><a href="{url(path)}"{" aria-current=page" if current else ""}>'
                       f'{file_icon(kind, letter)}<span>{esc(name)}</span></a></li>')
        out.append("</ul></details>")
    out.append("</nav>")
    return "".join(out)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def layout(path, title, body, *, description=None, tab=None, tab_icon=("md", ""), crumbs=(), structure=(),
           tree_active=None, head_title=None, wide=False, kind="page"):
    description = description or SITE["description"]
    full_title = head_title or (f"{title} · CS102 Enrolment System" if path else f"{SITE['title']} · CS102")
    canonical = SITE["url"] + path
    tab = tab or title
    crumb_html = "".join(f'<span class="crumb-sep">›</span><span>{esc(c)}</span>' for c in crumbs)
    if structure:
        items = []
        for sid, label, skind, level in structure:
            ic = {"f": "fi-f", "m": "fi-m", "c": "fi-c", "e": "fi-e", "h": "fi-h", "s": "fi-s"}.get(skind, "fi-h")
            letter = {"f": "f", "m": "m", "c": "c", "e": "e", "s": "▸"}.get(skind, "#")
            items.append(f'<li class="lv{level}"><a href="#{sid}"><span class="fi {ic}" aria-hidden="true">{letter}</span>'
                         f'<span>{esc(label)}</span></a></li>')
        structure_html = ('<aside class="pane pane-structure" aria-label="On this page">'
                          '<div class="pane-head"><span>Structure</span></div>'
                          f'<ul class="structure">{"".join(items)}</ul></aside>')
    else:
        structure_html = ""
    tree = render_tree(path if tree_active is None else tree_active)
    PAGES.append((path, title))
    tab_ic = file_icon(*tab_icon) if tab_icon else ""
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#1e1f22">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE['title'])}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['url']}img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<script>try{{var t=localStorage.getItem("ce-theme");document.documentElement.dataset.theme=t||(matchMedia("(prefers-color-scheme: light)").matches?"light":"dark")}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap">
<link rel="stylesheet" href="/css/site.css?v={ASSET_VERSION}">
</head>
<body class="kind-{kind}{' is-wide' if wide else ''}">
<a class="skip" href="#main">Skip to content</a>
<header class="titlebar">
  <button class="tb-btn tb-menu" type="button" data-toggle-tree aria-label="Show project files" aria-expanded="false">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
  </button>
  <a class="brand" href="{url()}" aria-label="CS102 enrolment: home">
    <span class="brand-mark"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 16h9a3 3 0 0 0 3-3v-1h.5a2 2 0 0 0 0-4H18V7H5v6a3 3 0 0 0 1 3Zm12-6h.5a.4.4 0 0 1 0 .8H18Z"/><path d="M5 19h13" class="stroke"/></svg></span>
    <span class="brand-text"><b>CS102</b><span class="brand-sep">/</span>enrolment</span>
  </a>
  <nav class="crumbs" aria-label="Location"><span class="crumb-sep">›</span><span>{esc(tab)}</span></nav>
  <div class="tb-spacer"></div>
  <button class="tb-search" type="button" data-open-search aria-label="Search everywhere">
    <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6"/><path d="m20 20-4.2-4.2"/></svg>
    <span>Search</span><kbd>/</kbd>
  </button>
  <button class="tb-run" type="button" data-run aria-label="Run the program in the console">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg><span>Run</span>
  </button>
  <button class="tb-btn" type="button" data-theme-toggle aria-label="Toggle light and dark theme">
    <svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    <svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/></svg>
  </button>
  <a class="tb-btn" href="{SITE['repo']}" target="_blank" rel="noopener" aria-label="Source on GitHub">
    <svg viewBox="0 0 24 24" aria-hidden="true" class="fill"><path d="M12 2a10 10 0 0 0-3.2 19.5c.5.1.7-.2.7-.5v-1.7c-2.8.6-3.4-1.3-3.4-1.3-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.6 2.4 1.1 3 .8.1-.7.4-1.1.6-1.4-2.2-.3-4.6-1.1-4.6-5a3.9 3.9 0 0 1 1-2.7 3.6 3.6 0 0 1 .1-2.7s.8-.3 2.8 1a9.6 9.6 0 0 1 5 0c1.9-1.3 2.8-1 2.8-1 .5 1.4.2 2.4.1 2.7a3.9 3.9 0 0 1 1 2.7c0 3.9-2.4 4.7-4.6 5 .4.3.7.9.7 1.9V21c0 .3.2.6.7.5A10 10 0 0 0 12 2Z"/></svg>
  </a>
  <a class="tb-report" href="{url('project-report/')}">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></svg><span>Report</span>
  </a>
</header>
<div class="workspace">
  <aside class="pane pane-project" id="project" aria-label="Project">
    <div class="pane-head"><span>Project</span><button class="pane-x" type="button" data-toggle-tree aria-label="Close project files">×</button></div>
    {tree}
  </aside>
  <div class="editor">
    <div class="tabs" role="list" data-tabs data-current="{esc(path)}" data-label="{esc(tab)}" data-icon="{esc(tab_icon[0] if tab_icon else 'md')}" data-letter="{esc(tab_icon[1] if tab_icon else '')}">
      <a class="tab is-active" role="listitem" href="{url(path)}" aria-current="page">{tab_ic}<span>{esc(tab)}</span></a>
    </div>
    <div class="pathbar"><span>enrolment</span>{crumb_html}</div>
    <main id="main" class="doc">
{body}
    </main>
    {footer()}
  </div>
  {structure_html}
</div>
<footer class="statusbar" aria-label="Status bar">
  <span class="sb-item sb-branch"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="6" cy="6" r="2"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="8" r="2"/><path d="M6 8v8M18 10c0 4-6 3-10 6"/></svg>main</span>
  <span class="sb-item">schoolcourseenrolmentsystem</span>
  <span class="sb-grow"></span>
  <span class="sb-item sb-hide">{esc(SITE['course'])} · {esc(SITE['course_name'])}</span>
  <span class="sb-item sb-hide">Java 8</span>
  <span class="sb-item sb-hide">UTF-8</span>
  <span class="sb-item">LF</span>
</footer>
<div class="dock" id="dock" hidden></div>
<div class="palette" id="palette" hidden></div>
<script src="/js/sample-data.js?v={ASSET_VERSION}"></script>
<script src="/js/site.js?v={ASSET_VERSION}" defer></script>
<script src="/js/console.js?v={ASSET_VERSION}" defer></script>
</body>
</html>
"""


def footer():
    return f"""<footer class="site-foot">
  <div class="foot-grid">
    <div class="foot-brand">
      <p class="kicker">// {esc(SITE['course'])} · {esc(SITE['course_name'])}</p>
      <p class="foot-title">{esc(SITE['title'])}</p>
      <p class="foot-text">A Java console application for students, instructors and administrators, documented class by class.</p>
      <p class="foot-text dim">{esc(SITE['author'])} · {esc(SITE['institution'])}</p>
    </div>
    <div><p class="foot-head">Explore</p>
      <a href="{url('architecture/')}">Architecture</a><a href="{url('run/')}">Run the program</a>
      <a href="{url('student-workflow/')}">Role sessions</a><a href="{url('data-files/')}">Data files</a>
      <a href="{url('notes/')}">Known issues</a></div>
    <div><p class="foot-head">Policies</p>
      {''.join(f'<a href="{url(p["slug"] + "/")}">{esc(p["title"].split(" &")[0])}</a>' for p in POLICIES)}</div>
    <div><p class="foot-head">Links</p>
      <a href="{SITE['main_site']}" target="_blank" rel="noopener">Main website</a>
      <a href="{SITE['repo']}" target="_blank" rel="noopener">GitHub repository</a>
      <a href="mailto:{SITE['email']}">{SITE['email']}</a>
      <a href="{url('project-report/')}">Project report (PDF)</a>
      <a href="{SITE['blueprint']}" target="_blank" rel="noopener">Made by Blueprint</a></div>
  </div>
  <div class="foot-bar"><span>© 2026 {esc(SITE['author_full'])} · All rights reserved</span><span><code>System.exit(0);</code> // thanks for reading</span></div>
</footer>"""


def write(path, content):
    target = OUT / path / "index.html" if not path.endswith(".html") else OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def add_search(title, path, kind, text="", parent=None):
    SEARCH.append({"t": title, "u": url(path), "k": kind, "x": re.sub(r"\s+", " ", text)[:180], "p": parent or ""})


# ---------------------------------------------------------------------------
# Diagrams
# ---------------------------------------------------------------------------

def class_diagram(compact=False):
    """UML-style class diagram as inline SVG; boxes link to class pages."""
    W, H = 960, 520
    boxes = {
        "user": (370, 20, 220, ["«abstract»", "User<T>"], ["name, ID, password", "email, phoneNumber, address", "login() · logout()"]),
        "student": (80, 200, 220, ["Student"], ["creditLimit", "enrolledCourses", "enroll_In_Course()"]),
        "instructor": (370, 200, 220, ["Instructor"], ["viewEnrolledStudents()", "gradeStudent()", "updateCourseInfo()"]),
        "administrator": (660, 200, 220, ["Administrator"], ["addStudent() · addCourse()", "assignInstructor()", "closeCourse()"]),
        "course": (80, 380, 220, ["Course"], ["instructor : Instructor", "capacity · enrollmentStatus", "isFull()"]),
        "assessment": (370, 380, 220, ["Assessment"], ["studentId · courseCode", "examType · score", "assignGrade()"]),
        "data-manager": (660, 380, 220, ["«singleton»", "dataManager"], ["5 lists · 5 files", "load* / save*", "getInstance()"]),
    }
    hdr = lambda t: 22 + 16 * (len(t) - 1)  # noqa: E731
    box_h = lambda b: hdr(b[3]) + 14 + 16 * len(b[4])  # noqa: E731
    parts = [f'<svg class="uml" viewBox="0 0 {W} {H}" role="img" aria-labelledby="uml-t uml-d">'
             '<title id="uml-t">Class diagram</title>'
             '<desc id="uml-d">Student, Instructor and Administrator extend the abstract User class. Courses reference an instructor and a list of students; '
             'students reference their courses; assessments link a student ID and a course code. dataManager holds every list.</desc>'
             '<defs><marker id="tri" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" orient="auto">'
             '<path d="M1 1 11 6 1 11Z" class="uml-tri"/></marker>'
             '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
             '<path d="M1 1 9 5 1 9" class="uml-arr"/></marker></defs>']

    def anchor(key, side):
        x, y, w, t, m = boxes[key]
        h = box_h(boxes[key])
        return {"top": (x + w / 2, y), "bottom": (x + w / 2, y + h), "left": (x, y + h / 2), "right": (x + w, y + h / 2)}[side]

    ux, uy = anchor("user", "bottom")
    for k in ("student", "instructor", "administrator"):
        sx, sy = anchor(k, "top")
        mid = uy + 34
        parts.append(f'<path class="uml-inh" d="M{sx} {sy} V{mid} H{ux} V{uy + 1}" marker-end="url(#tri)"/>')
    assoc = [
        ("course", "top", "student", "bottom", "enrolledStudents *", -1),
        ("student", "bottom", "course", "top", "enrolledCourses *", 1),
        ("course", "right", "assessment", "left", "grades *", 0),
    ]
    for a, sa, b, sb, label, off in assoc:
        x1, y1 = anchor(a, sa)
        x2, y2 = anchor(b, sb)
        if a == "course" and b == "instructor":
            y1 += 18
            parts.append(f'<path class="uml-assoc" d="M{x1} {y1} H330 V{y2 + 52} H{x2} V{y2 + 2}" marker-end="url(#arr)"/>'
                         f'<text class="uml-lbl" x="{x2 + 8}" y="{y2 + 22}">instructor</text>')
            continue
        if off:
            x1 += off * 44
            x2 += off * 44
        if a == "course" and b == "assessment":
            y1 -= 18
            y2 -= 18
        parts.append(f'<path class="uml-assoc" d="M{x1} {y1} L{x2} {y2}" marker-end="url(#arr)"/>')
        lx = (x1 + x2) / 2 + (8 if off >= 0 else -8)
        ly = (y1 + y2) / 2 + (-6 if a == "course" and b == "assessment" else 4)
        anchor_txt = "start" if off >= 0 else "end"
        parts.append(f'<text class="uml-lbl" x="{lx}" y="{ly}" text-anchor="{anchor_txt if off else "middle"}">{esc(label)}</text>')
    for key, (x, y, w, title, mems) in boxes.items():
        h = box_h(boxes[key])
        th = hdr(title)
        abstract = "abstract" in title[0]
        parts.append(f'<a href="{url(key + "/")}" class="uml-box{" is-abstract" if abstract else ""}" data-cls="{key}">'
                     f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
                     f'<rect class="uml-head" x="{x}" y="{y}" width="{w}" height="{th}" rx="8"/>'
                     f'<rect class="uml-head" x="{x}" y="{y + th - 8}" width="{w}" height="8"/>'
                     f'<line x1="{x}" x2="{x + w}" y1="{y + th}" y2="{y + th}"/>')
        for i, t in enumerate(title):
            stereo = t.startswith("«")
            parts.append(f'<text class="{"uml-stereo" if stereo else "uml-name"}" x="{x + w / 2}" y="{y + 16 + 16 * i}" text-anchor="middle">{esc(t)}</text>')
        for i, t in enumerate(mems):
            parts.append(f'<text class="uml-mem" x="{x + 12}" y="{y + th + 18 + 16 * i}">{esc(t)}</text>')
        parts.append("</a>")
    parts.append("</svg>")
    return "".join(parts)


def files_diagram():
    W, H = 1030, 330
    pos = {"students": (30, 40), "courses": (430, 40), "instructors": (790, 40),
           "assessments": (240, 236), "administrators": (790, 236)}
    w, h = 210, 70
    out = [f'<svg class="erd" viewBox="0 0 {W} {H}" role="img" aria-labelledby="erd-t erd-d">'
           '<title id="erd-t">How the data files reference each other</title>'
           '<desc id="erd-d">students.txt lists course codes from courses.txt. courses.txt stores an instructor ID from instructors.txt and student IDs from students.txt. '
           'assessments.txt stores a student ID and a course code. administrators.txt stands alone.</desc>'
           '<defs><marker id="erd-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
           '<path d="M1 1 9 5 1 9" class="uml-arr"/></marker></defs>']
    # (label, start, end, label position, anchor)
    edges = [
        ("enrolledCourses \u2192 code", (240, 62), (430, 62), (335, 52), "middle"),
        ("enrolledStudents \u2192 id", (430, 90), (240, 90), (335, 108), "middle"),
        ("instructor \u2192 id", (640, 75), (790, 75), (715, 65), "middle"),
        ("studentId \u2192 id", (290, 236), (150, 110), (212, 168), "end"),
        ("courseCode \u2192 code", (400, 236), (520, 110), (472, 168), "start"),
    ]
    for label, (x1, y1), (x2, y2), (lx, ly), anc in edges:
        out.append(f'<path class="uml-assoc" d="M{x1} {y1} L{x2} {y2}" marker-end="url(#erd-a)"/>')
        out.append(f'<text class="uml-lbl" x="{lx}" y="{ly}" text-anchor="{anc}">{esc(label)}</text>')
    for key, (x, y) in pos.items():
        f = next(f for f in FILES if f["key"] == key)
        out.append(f'<a href="#{key}" class="uml-box"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
                   f'<text class="uml-name" x="{x + 14}" y="{y + 28}">{esc(f["name"])}</text>'
                   f'<text class="uml-mem" x="{x + 14}" y="{y + 50}">{len(f["columns"])} columns · {esc(f["entity"])}</text></a>')
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

PARSED = {}


def load_java():
    for c in CLASSES:
        # Stored as .java.txt so Java tooling doesn't try to compile the listings.
        src = (WEB / "java" / (c["file"] + ".txt")).read_text(encoding="utf-8").rstrip("\n")
        header, members = parse_java(src, c["name"])
        PARSED[c["slug"]] = {"src": src, "header": header, "members": members, "lines": src.count("\n") + 1}


def signature_html(m, cls_name):
    if m["kind"] in ("field", "const"):
        return highlight_inline(f'{m["type"]} {m["name"]}')
    params = re.sub(r"\s+", " ", m["params"])
    ret = (m["tparams"] + " " if m["tparams"] else "") + (m["ret"] + " " if m["ret"] else "")
    return highlight_inline(f"{ret}{m['name']}({params})")


def member_row(slug, m, doc, cls_name):
    desc, details = doc if doc else ("", [])
    v = vis(m)
    static = "static" in m["mods"]
    flags = []
    if m.get("abstract"):
        flags.append(badge("abstract", "violet"))
    if static:
        flags.append(badge("static"))
    if v != "public":
        flags.append(badge(v, "dim"))
    det = "".join(f"<li>{esc(d)}</li>" for d in details)
    return (f'<li class="mem" id="m-{m["name"]}">'
            f'<div class="mem-sig"><span class="fi fi-m v-{v}" aria-hidden="true">m</span>'
            f'<code class="sig">{signature_html(m, cls_name)}</code>{"".join(flags)}'
            f'<a class="ln-link" href="#L{m["line"]}" data-goto-line="{m["line"]}" title="Show in source">L{m["line"]}</a></div>'
            + (f'<p class="mem-desc">{esc(desc)}</p>' if desc else "")
            + (f'<ul class="mem-det">{det}</ul>' if det else "")
            + "</li>")


def build_class(c, idx):
    slug = c["slug"]
    p = PARSED[slug]
    members = p["members"]
    methods = [m for m in members if m["kind"] == "method"]
    by_name = {}
    for m in methods:
        by_name.setdefault(m["name"], m)
    fields = [m for m in members if m["kind"] == "field"]
    consts = [m for m in members if m["kind"] == "const"]
    enums = [m for m in members if m["kind"] == "enum"]
    ctors = [m for m in members if m["kind"] == "ctor"]
    structure = []
    body = []

    # Header
    extends = ""
    if c.get("extends"):
        parent = by_slug(c["extends"])
        extends = f'<a class="chip" href="{url(parent["slug"] + "/")}">{file_icon("cls", parent["icon"])}extends {esc(parent["name"])}</a>'
    used_by = [w for w in WORKFLOWS if any(o["target"][0] == slug for o in w["options"])]
    used = "".join(f'<a class="chip" href="{url(w["slug"] + "/")}">{file_icon("run", "▶")}{esc(w["title"])}</a>' for w in used_by)
    facts = "".join(f'<div class="fact"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in c["facts"])
    body.append(f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("cls", c["icon"])}<span>{esc(c["kind"])}</span><span class="dim">· schoolcourseenrolmentsystem</span></p>
  <h1 class="mono-title">{esc(c["name"])}<span class="dim">.java</span></h1>
  <p class="lede">{esc(c["lede"])}</p>
  <pre class="decl"><code>{highlight_inline(p["header"] or "")}</code></pre>
  <div class="chips">{extends}{used}</div>
  <dl class="facts">{facts}</dl>
  <div class="view-switch" role="tablist" aria-label="View">
    <button type="button" role="tab" aria-selected="true" data-view="overview">Overview</button>
    <button type="button" role="tab" aria-selected="false" data-view="source">Source <span class="dim">{p["lines"]} lines</span></button>
  </div>
</header>""")

    ov = []
    # Responsibilities
    ov.append(section("responsibilities", "Responsibilities",
                      '<ul class="checks">' + "".join(f"<li>{esc(r)}</li>" for r in c["responsibilities"]) + "</ul>"))
    structure.append(("responsibilities", "Responsibilities", "h", 0))
    for tone, title, text in c.get("callouts", []):
        ov.append(f'<aside class="callout {tone}"><p class="callout-t">{esc(title)}</p><p>{esc(text)}</p></aside>')

    # Fields & enums
    if fields or enums or consts:
        rows = []
        for m in fields + consts:
            v = vis(m)
            rows.append(f'<tr id="m-{m["name"]}"><td><span class="fi fi-f v-{v}" aria-hidden="true">f</span></td>'
                        f'<td><code class="sig">{highlight_inline(m["type"])}</code></td><td><code>{esc(m["name"])}</code></td>'
                        f'<td>{" ".join(badge(x, "dim") for x in m["mods"])}</td>'
                        f'<td class="num"><a class="ln-link" href="#L{m["line"]}" data-goto-line="{m["line"]}">L{m["line"]}</a></td></tr>')
        table = ""
        if rows:
            table = ('<div class="table-wrap"><table class="grid fields"><thead><tr><th></th><th>Type</th><th>Name</th><th>Modifiers</th><th class="num">Line</th></tr></thead>'
                     f'<tbody>{"".join(rows)}</tbody></table></div>')
        enum_html = ""
        for e in enums:
            enum_html += (f'<div class="enum" id="m-{e["name"]}"><p class="enum-name"><span class="fi fi-e" aria-hidden="true">e</span>'
                          f'<code>enum {esc(e["name"])}</code><a class="ln-link" href="#L{e["line"]}" data-goto-line="{e["line"]}">L{e["line"]}</a></p>'
                          f'<div class="enum-vals">{"".join(f"<code>{esc(v)}</code>" for v in e["values"])}</div></div>')
        ov.append(section("fields", "Fields & enums", enum_html + table))
        structure.append(("fields", "Fields & enums", "h", 0))
        for m in (fields + consts)[:12]:
            structure.append((f"m-{m['name']}", m["name"], "f", 1))
        for e in enums:
            structure.append((f"m-{e['name']}", e["name"], "e", 1))

    # Constructors
    if ctors:
        items = []
        for i, m in enumerate(ctors):
            note = c["ctor_notes"][i] if i < len(c["ctor_notes"]) else ""
            label = "Default" if not m["params"].strip() else "Parameterised"
            items.append(f'<li class="mem"><div class="mem-sig"><span class="fi fi-c" aria-hidden="true">c</span>'
                         f'<code class="sig">{highlight_inline(c["name"] + "(" + re.sub(chr(10), " ", m["params"]) + ")")}</code>{badge(label, "dim")}'
                         f'<a class="ln-link" href="#L{m["line"]}" data-goto-line="{m["line"]}">L{m["line"]}</a></div>'
                         + (f'<p class="mem-desc">{esc(note)}</p>' if note else "") + "</li>")
        ov.append(section("constructors", "Constructors", f'<ul class="members">{"".join(items)}</ul>'))
        structure.append(("constructors", "Constructors", "h", 0))

    # Method groups
    shown = set()
    for gi, (gtitle, names, blurb) in enumerate(c["groups"]):
        gid = "g-" + re.sub(r"[^a-z0-9]+", "-", gtitle.lower()).strip("-")
        rows = []
        for n in names:
            m = by_name.get(n)
            if not m:
                continue
            shown.add(n)
            rows.append(member_row(slug, m, c["members"].get(n), c["name"]))
        if not rows:
            continue
        b = f'<p class="sec-blurb">{esc(blurb)}</p>' if blurb else ""
        ov.append(section(gid, gtitle, b + f'<ul class="members">{"".join(rows)}</ul>', kicker=f"{len(rows)} method{'s' if len(rows) != 1 else ''}"))
        structure.append((gid, gtitle, "h", 0))
        for n in names:
            if n in by_name:
                structure.append((f"m-{n}", n, "m", 1))
    rest = [m for m in methods if m["name"] not in shown and not accessor(m["name"])]
    if rest:
        ov.append(section("other", "Other methods", f'<ul class="members">{"".join(member_row(slug, m, c["members"].get(m["name"]), c["name"]) for m in rest)}</ul>'))
        structure.append(("other", "Other methods", "h", 0))
    acc = [m for m in methods if m["name"] not in shown and accessor(m["name"])]
    if acc:
        note = f'<p class="sec-blurb">{esc(c["accessors_note"])}</p>' if c.get("accessors_note") else ""
        listing = "".join(
            f'<li><code class="sig">{signature_html(m, c["name"])}</code><a class="ln-link" href="#L{m["line"]}" data-goto-line="{m["line"]}">L{m["line"]}</a></li>'
            for m in acc)
        ov.append(section("accessors", "Getters & setters",
                          note + f'<details class="fold"><summary>{len(acc)} accessors</summary><ul class="acc">{listing}</ul></details>'))
        structure.append(("accessors", "Getters & setters", "h", 0))

    # Issues
    related = [i for i in ISSUES if i["where"][0] == slug]
    if related:
        items = "".join(
            f'<li class="issue-mini {i["kind"]}"><a href="{url("notes/")}#{i["id"]}"><span class="badge {i["kind"]}">{i["kind"]}</span>{esc(i["title"])}</a></li>'
            for i in related)
        ov.append(section("issues", "Known issues", f'<ul class="issue-list">{items}</ul>'))
        structure.append(("issues", "Known issues", "h", 0))

    # Source view
    hl = highlight_java(p["src"])
    decl_lines = {m["line"]: m["name"] for m in members}
    rows = "".join(
        f'<div class="l{" is-decl" if n in decl_lines else ""}" id="L{n}"><a class="n" href="#L{n}">{n}</a><span class="c">{line or " "}</span></div>'
        for n, line in enumerate(hl, 1))
    source = (f'<div class="code-view"><div class="code-head">{file_icon("cls", c["icon"])}<span>{esc(c["file"])}</span>'
              f'<span class="dim">{p["lines"]} lines · from the project report</span><span class="grow"></span>'
              f'<button type="button" class="mini-btn" data-copy-source>Copy</button></div>'
              f'<div class="code-body" data-source>{rows}</div></div>')

    prev_c = CLASSES[idx - 1] if idx > 0 else None
    next_c = CLASSES[idx + 1] if idx + 1 < len(CLASSES) else None
    body.append(f'<div class="view" data-view-panel="overview">{"".join(ov)}</div>')
    body.append(f'<div class="view" data-view-panel="source" id="source"><h2 class="sr-only">Source</h2>{source}</div>')
    body.append(pager(prev_c and (prev_c["slug"] + "/", prev_c["file"]), next_c and (next_c["slug"] + "/", next_c["file"])))
    structure.append(("source", "Source", "s", 0))

    add_search(c["file"], slug + "/", "class", c["lede"])
    for m in members:
        if m["kind"] in ("method", "field", "enum", "const"):
            doc = c["members"].get(m["name"])
            add_search(f'{c["name"]}.{m["name"]}' + ("()" if m["kind"] == "method" else ""), f"{slug}/#m-{m['name']}",
                       m["kind"], doc[0] if doc else "", c["file"])
    return layout(slug + "/", c["name"], "".join(body), description=f'{c["name"]} ({c["kind"]}): {c["tagline"]} Fields, methods and full Java source.',
                  tab=c["file"], tab_icon=("cls", c["icon"]), crumbs=("src", "schoolcourseenrolmentsystem", c["file"]),
                  structure=structure, kind="class")


def pager(prev, nxt):
    def link(item, label, cls):
        if not item:
            return "<span></span>"
        return f'<a class="pager-link {cls}" href="{url(item[0])}"><span>{label}</span><strong>{esc(item[1])}</strong></a>'
    return f'<nav class="pager" aria-label="Previous and next">{link(prev, "← Previous", "prev")}{link(nxt, "Next →", "next")}</nav>'


STEP_LABEL = {"in": "input", "do": "process", "check": "check", "out": "output", "save": "save"}


def build_workflow(w, idx):
    structure = []
    cls = by_slug(w["cls"])
    menu_lines = [w["menu_header"]] + [f'{o["n"]}. {o["label"]}' for o in w["options"]]
    saves_now = [o for o in w["options"] if o["save"]]
    tabs = "".join(
        f'<a class="seg{" is-on" if x is w else ""}" href="{url(x["slug"] + "/")}"{" aria-current=page" if x is w else ""}>{file_icon("run", "▶")}{esc(x["name"])}</a>'
        for x in WORKFLOWS)
    body = [f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("run", "▶")}<span>run configuration</span><span class="dim">· {esc(w["role"])} session</span></p>
  <h1>{esc(w["title"])}</h1>
  <p class="lede">{esc(w["lede"])}</p>
  <nav class="segs" aria-label="Role sessions">{tabs}</nav>
  <div class="run-strip">
    <button type="button" class="btn btn-run" data-run="{w["role"]}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>Run as {esc(w["name"])}</button>
    <span class="dim">Demo login <code>{esc(w["sample"])}</code></span>
  </div>
</header>"""]

    # Session at a glance
    flow = f"""<ol class="session">
  <li><span class="node in">role</span><code>{esc(w["role"])}</code></li>
  <li><span class="node do">login</span><code>Helpers.login&lt;{esc(cls["name"])}&gt;</code></li>
  <li><span class="node out">menu</span><code>Helpers.{esc(w["menu_method"])}()</code></li>
  <li><span class="node in">option</span><code>getSafeIntInput("Option: ")</code></li>
  <li><span class="node do">handle</span><code>switch (choice)</code></li>
  <li class="loop"><span class="node check">loop</span><span>until Logout</span></li>
</ol>"""
    menu = term_block("\n".join(menu_lines), f"Helpers.{w['menu_method']}()")
    matrix_rows = "".join(
        f'<tr><td class="num"><a href="#opt-{o["n"]}">{o["n"]}</a></td><td>{esc(o["label"])}</td>'
        f'<td><code class="sig">{highlight_inline(o["call"])}</code></td>'
        f'<td>{badge("saves " + o["save"], "ok") if o["save"] else badge("on exit", "dim")}</td></tr>'
        for o in w["options"])
    body.append(section("overview", "At a glance",
                        f'<div class="split"><div>{menu}</div><div>{flow}'
                        f'<p class="note">{len(saves_now)} of {len(w["options"])} options write to disk straight away. '
                        f'The rest change the in-memory lists, which are saved when someone types <code>exit</code>.</p></div></div>'
                        f'<div class="table-wrap"><table class="grid matrix"><thead><tr><th class="num">#</th><th>Menu text</th><th>main() calls</th><th>Persistence</th></tr></thead>'
                        f'<tbody>{matrix_rows}</tbody></table></div>', kicker=f"{len(w['options'])} options"))
    structure.append(("overview", "At a glance", "h", 0))

    cards = []
    for o in w["options"]:
        steps = "".join(f'<li class="step {k}"><span class="node {k}">{STEP_LABEL[k]}</span><span>{esc(t)}</span></li>' for k, t in o["steps"])
        outs = "".join(f'<div class="outcome"><dt>{esc(k)}</dt><dd>{term_block(v)}</dd></div>' for k, v in o["outcomes"])
        tslug, tmeth = o["target"]
        tcls = by_slug(tslug)
        cards.append(f"""<article class="opt" id="opt-{o['n']}">
  <header class="opt-head"><span class="opt-n">{o['n']}</span><div><h3>{esc(o['label'])}</h3><p>{esc(o['summary'])}</p></div>
    <div class="opt-meta">{badge("saves " + o["save"], "ok") if o["save"] else ""}<a class="chip" href="{member_link(tslug, tmeth)}">{file_icon("cls", tcls["icon"])}{esc(tcls["name"])}.{esc(tmeth or "")}()</a></div></header>
  <div class="opt-body"><ol class="flow">{steps}</ol><dl class="outcomes">{outs}</dl></div>
</article>""")
        structure.append((f"opt-{o['n']}", f"{o['n']}. {o['label'].rstrip('.')}", "m", 1))
        add_search(f"{w['name']} menu {o['n']}: {o['label']}", f"{w['slug']}/#opt-{o['n']}", "option", o["summary"], w["title"])
    body.append(section("options", "Every option", "".join(cards), kicker="flow + example output"))
    structure.insert(1, ("options", "Every option", "h", 0))
    prev_w = WORKFLOWS[idx - 1] if idx > 0 else None
    next_w = WORKFLOWS[idx + 1] if idx + 1 < len(WORKFLOWS) else None
    body.append(pager((prev_w["slug"] + "/", prev_w["title"]) if prev_w else ("run/", "Main.run"),
                      (next_w["slug"] + "/", next_w["title"]) if next_w else ("data-files/", "Data files")))
    add_search(w["title"], w["slug"] + "/", "page", w["lede"])
    return layout(w["slug"] + "/", w["title"], "".join(body),
                  description=f"{w['title']} in the CS102 enrolment system: every menu option, what it calls, what it prints and when it saves.",
                  tab=w["title"], tab_icon=("run", "▶"), crumbs=("run configurations", w["title"]), structure=structure, kind="workflow")


def build_run():
    structure = [("startup", "Start-up to exit", "h", 0), ("console", "Interactive console", "h", 0),
                 ("roles", "Role prompt", "h", 0), ("exit", "Exit & errors", "h", 0)]
    steps = "".join(
        f'<li><div class="tl-dot"></div><div class="tl-body"><code class="sig">{highlight_inline(a)}</code><p>{esc(b)}</p>{term_block(c)}</div></li>'
        for a, b, c in STARTUP)
    roles = "".join(
        f'<a class="role-card" href="{url(w["slug"] + "/")}"><span class="fi fi-run" aria-hidden="true">▶</span><strong>{esc(w["role"])}</strong>'
        f'<span>{len(w["options"])} options · {esc(w["name"])}</span><code>{esc(w["sample"])}</code></a>'
        for w in WORKFLOWS)
    body = f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("run", "▶")}<span>run configuration</span><span class="dim">· SchoolCourseEnrolmentSystem.main()</span></p>
  <h1>Run the program</h1>
  <p class="lede">The whole application is one loop in <a href="{url('main/')}"><code>main()</code></a>. Follow it from start-up to exit, or run it right here: the console below replays the report's code against sample data, quirks included.</p>
</header>
{section("startup", "Start-up to exit", f'<ol class="timeline">{steps}</ol>', kicker="what main() does, in order")}
{section("console", "Interactive console", '<div class="inline-console" data-inline-console></div><p class="note">Commands are typed exactly as in the Java program. Try <code>student</code>, then <code>2200000001</code> and <code>Student1234</code>. Use the <strong>Files</strong> tab to compare what is on disk with what is still only in memory.</p>', kicker="sample data, runs in your browser")}
{section("roles", "Role prompt", f'<p>Typing anything other than these four words prints <code>Invalid role. Try again.</code> The match ignores case and only reads the first word.</p><div class="role-grid">{roles}<div class="role-card is-exit"><span class="fi fi-x" aria-hidden="true">⏻</span><strong>exit</strong><span>saveAllData(), then “Goodbye.”</span></div></div>')}
{section("exit", "Exit & errors", f'''<div class="cards two">
<div class="card"><h3>Clean exit</h3><p>Typing <code>exit</code> sets the loop flag, calls <code>saveAllData()</code> to write all five files, prints <code>Goodbye.</code> and lets <code>main()</code> return.</p></div>
<div class="card warn"><h3>Unexpected error</h3><p>One <code>try/catch (Exception e)</code> wraps the whole loop. If anything escapes the inner handlers it prints <code>Error: &lt;message&gt;</code> and the program ends <em>without</em> saving.</p></div>
</div><p>Every guard and handler is listed on <a href="{url('validation/')}">Validation &amp; errors</a>.</p>''')}
{pager(("admin-workflow/", "Admin session"), ("student-workflow/", "Student session"))}"""
    add_search("Run the program", "run/", "page", "main loop, start-up, exit, interactive console")
    return layout("run/", "Run the program", body, tab="Main.run", tab_icon=("run", "▶"),
                  description="Run the CS102 School Course Enrolment System in your browser and follow main() from start-up to exit.",
                  crumbs=("run configurations", "Main.run"), structure=structure, kind="run")


def loc_chart():
    rows = sorted(((c, PARSED[c["slug"]]["lines"], len([m for m in PARSED[c["slug"]]["members"] if m["kind"] == "method"]))
                   for c in CLASSES), key=lambda r: -r[1])
    top = rows[0][1]
    bars = "".join(
        f'<li><a href="{url(c["slug"] + "/")}"><span class="bar-label">{file_icon("cls", c["icon"])}{esc(c["name"])}</span>'
        f'<span class="bar-track"><span class="bar layer-{c["layer"]}" style="--w:{n / top * 100:.1f}%"></span></span>'
        f'<span class="bar-val">{n}<span class="dim"> lines · {mcount} methods</span></span></a></li>'
        for c, n, mcount in rows)
    total = sum(r[1] for r in rows)
    return total, f'<ul class="bars" aria-label="Lines of code per class">{bars}</ul>'


def build_home():
    total_loc, chart = loc_chart()
    n_methods = sum(len([m for m in PARSED[c["slug"]]["members"] if m["kind"] == "method"]) for c in CLASSES)
    n_options = sum(len(w["options"]) for w in WORKFLOWS)
    roles = "".join(f"""<a class="role-tile" href="{url(w['slug'] + '/')}">
  <span class="role-ic">{esc(w['icon'])}</span>
  <span class="role-name">{esc(w['name'])}</span>
  <span class="role-meta">{len(w['options'])} options</span>
  <ol>{''.join(f'<li>{esc(o["label"])}</li>' for o in w['options'][:5])}{'<li class="more">…</li>' if len(w['options']) > 5 else ''}</ol>
</a>""" for w in WORKFLOWS)
    docs = [
        ("architecture/", "ARCHITECTURE.md", "Layers, class map, design decisions and the full class index."),
        ("data-files/", "data/", "Five pipe-delimited files, column by column, with sample records."),
        ("validation/", "VALIDATION.md", "Every validator, guard and exception handler and what it prints."),
        ("reports-and-statistics/", "REPORTS.md", "The two admin reports, computed from the sample data."),
        ("notes/", "KNOWN_ISSUES.md", f"{len(ISSUES)} behaviours worth knowing, each linked to its line of code."),
        ("project-report/", "report.pdf", "The 102-page submitted report, readable in the browser."),
    ]
    doc_rows = "".join(f'<a class="doc-row" href="{url(p)}">{file_icon("md")}<code>{esc(n)}</code><span>{esc(d)}</span></a>' for p, n, d in docs)
    body = f"""
<section class="welcome">
  <div class="welcome-copy">
    <p class="eyebrow">{file_icon("proj")}<span>{esc(SITE['course'])} · {esc(SITE['course_name'])}</span><span class="dim">· {esc(SITE['institution'])}</span></p>
    <h1 class="hero-title">The registrar's office,<br><span>written in Java.</span></h1>
    <p class="lede">A console application where students enrol, instructors grade and administrators run the course catalogue, saved to plain text files between sessions. This site documents it class by class, and runs it in your browser.</p>
    <div class="actions">
      <button type="button" class="btn btn-run" data-run><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>Run the program</button>
      <a class="btn" href="{url('architecture/')}">Open the architecture</a>
      <a class="btn ghost" href="{url('student/')}">{file_icon("cls", "C")}Student.java</a>
    </div>
    <dl class="stats">
      <div><dt>classes</dt><dd>{len(CLASSES)}</dd></div>
      <div><dt>methods</dt><dd>{n_methods}</dd></div>
      <div><dt>menu options</dt><dd>{n_options}</dd></div>
      <div><dt>lines of Java</dt><dd>{total_loc:,}</dd></div>
    </dl>
  </div>
  <div class="welcome-console">
    <div class="inline-console" data-inline-console data-autoplay></div>
    <p class="console-hint">Live: type into it. Demo logins on the <a href="{url('run/')}">Run page</a>.</p>
  </div>
</section>
{section("roles", "Three roles, one menu loop each", f'<div class="role-tiles">{roles}</div>', kicker="run configurations")}
{section("map", "Class map", f'<div class="figure">{class_diagram()}</div><p class="note">Click a class to open it. Helpers and the main class sit around this core: Helpers collects input and calls these classes, and main() drives the loop.</p>', kicker="src/schoolcourseenrolmentsystem")}
{section("size", "Where the code lives", chart + '<p class="note">Helpers and dataManager hold more than half of the code: the console flows and the file handling. The entity classes stay small.</p>', kicker="lines per class, from the report")}
{section("docs", "Documentation", f'<div class="doc-rows">{doc_rows}</div>', kicker="docs/")}
"""
    add_search("README", "", "page", SITE["description"])
    return layout("", "Home", body, tab="README.md", tab_icon=("md", ""), crumbs=("README.md",), kind="home", wide=True)


def build_architecture():
    structure = [("layers", "Layers", "h", 0), ("map", "Class map", "h", 0), ("classes", "Class index", "h", 0),
                 ("design", "Design decisions", "h", 0), ("persistence", "When data is saved", "h", 0), ("layout", "Project layout", "h", 0)]
    layer_names = {"entity": ("Entities", "Model the people, courses and grades."),
                   "support": ("Support", "Input, validation, menus and file storage."),
                   "app": ("Application", "The loop that ties it together.")}
    layers = ""
    for key, (title, blurb) in layer_names.items():
        items = "".join(f'<a href="{url(c["slug"] + "/")}">{file_icon("cls", c["icon"])}<span>{esc(c["name"])}</span></a>' for c in CLASSES if c["layer"] == key)
        layers += f'<div class="layer layer-{key}"><div class="layer-head"><strong>{title}</strong><span>{blurb}</span></div><div class="layer-items">{items}</div></div>'
    idx_rows = "".join(
        f'<tr><td>{file_icon("cls", c["icon"])}<a href="{url(c["slug"] + "/")}"><code>{esc(c["name"])}</code></a></td><td>{esc(c["kind"])}</td>'
        f'<td>{esc(c["tagline"])}</td><td class="num">{PARSED[c["slug"]]["lines"]}</td>'
        f'<td class="num"><a href="{url(c["slug"] + "/#source")}">source</a></td></tr>' for c in CLASSES)
    design = "".join(f'<a class="card link" href="{url(d["cls"] + "/")}"><h3>{esc(d["title"])}</h3><code class="sig">{highlight_inline(d["code"])}</code><p>{esc(d["body"])}</p></a>' for d in DESIGN)
    pers = "".join(
        f'<tr><td>{esc(who)}</td><td>{esc(what)}</td><td><code>{esc(f)}</code></td><td>{badge("immediately", "ok") if when == "now" else badge("on exit only", "warn")}</td></tr>'
        for who, what, f, when in PERSISTENCE)
    tree = """SchoolCourseEnrolmentSystem/
├─ src/schoolcourseenrolmentsystem/
│  ├─ User.java  Student.java  Instructor.java  Administrator.java
│  ├─ Course.java  Assessment.java
│  ├─ Helpers.java  dataManager.java
│  └─ SchoolCourseEnrolmentSystem.java   ← main()
├─ students.txt  instructors.txt  administrators.txt
├─ courses.txt  assessments.txt         ← written next to the program
└─ web/                                 ← this website"""
    body = f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("md")}<span>ARCHITECTURE.md</span></p>
  <h1>Architecture</h1>
  <p class="lede">Nine classes in one package, in three layers: entities that model the university, support classes for input and storage, and a main class that runs the loop.</p>
</header>
{section("layers", "Layers", f'<div class="layers">{layers}</div>')}
{section("map", "Class map", f'<div class="figure">{class_diagram()}</div>')}
{section("classes", "Class index", f'<div class="table-wrap"><table class="grid"><thead><tr><th>Class</th><th>Kind</th><th>Responsibility</th><th class="num">Lines</th><th class="num"></th></tr></thead><tbody>{idx_rows}</tbody></table></div><p class="note">Listings come from the project report and were re-indented when extracted from the PDF, so wrapping may differ slightly from the original files.</p>')}
{section("design", "Design decisions", f'<div class="cards three">{design}</div>')}
{section("persistence", "When data is saved", f'<p>Only a few actions write to disk immediately. Everything else waits for <code>saveAllData()</code> at exit, which is why closing the window loses work (see <a href="{url("notes/")}#save-on-exit">Known issues</a>).</p><div class="table-wrap"><table class="grid"><thead><tr><th>Who</th><th>Action</th><th>File</th><th>Written</th></tr></thead><tbody>{pers}</tbody></table></div>')}
{section("layout", "Project layout", term_block(tree, "tree"))}
{pager(("", "README.md"), ("run/", "Main.run"))}"""
    add_search("Architecture", "architecture/", "page", "layers, class diagram, design decisions, singleton, generics, persistence")
    return layout("architecture/", "Architecture", body, tab="ARCHITECTURE.md", crumbs=("docs", "ARCHITECTURE.md"), structure=structure)


def build_data():
    structure = [("relations", "How files connect", "h", 0)]
    blocks = []
    for f in FILES:
        lines = lines_for(f["key"])
        cols = f["columns"]
        rows = "".join(
            f'<tr><td class="num"><span class="col-i c{i % 9}">{i}</span></td><td><code>{esc(n)}</code></td><td><code class="sig">{highlight_inline(t)}</code></td><td>{esc(how)}</td></tr>'
            for i, (n, t, how) in enumerate(cols))
        sample_lines = []
        for ln in lines:
            parts = ln.split("|")
            segs = []
            for i, part in enumerate(parts):
                segs.append(f'<span class="seg c{i % 9}" title="{esc(cols[i][0]) if i < len(cols) else ""}">{esc(part) or "&#8203;"}</span>')
            sample_lines.append('<span class="pipe">|</span>'.join(segs))
        refs = "".join(f'<li><code>{esc(a)}</code> → <a href="#{b}"><code>{esc(b)}.txt</code></a> by {esc(k)}</li>' for a, b, k in f["refs"])
        blocks.append(f"""<section class="sec datafile" id="{f['key']}">
  <p class="kicker">{esc(f['entity'])} · {f['min']}+ fields per line</p>
  <h2>{file_icon("txt")}<code>{esc(f['name'])}</code><a class="anchor" href="#{f['key']}" aria-label="Link to this section">#</a></h2>
  <p>{esc(f['blurb'])} Read by <a href="{url('data-manager/#m-' + f['loader'])}"><code>{f['loader']}()</code></a>, written by <a href="{url('data-manager/#m-' + f['saver'])}"><code>{f['saver']}()</code></a>.</p>
  <div class="file-view"><div class="code-head">{file_icon("txt")}<span>{esc(f['name'])}</span><span class="dim">sample · {len(lines)} lines</span></div>
  <pre class="records">{chr(10).join(sample_lines)}</pre></div>
  <div class="table-wrap"><table class="grid schema"><thead><tr><th class="num">#</th><th>Field</th><th>Java type</th><th>How it loads</th></tr></thead><tbody>{rows}</tbody></table></div>
  {f'<ul class="refs">{refs}</ul>' if refs else ''}
</section>""")
        structure.append((f["key"], f["name"], "f", 0))
        add_search(f["name"], f"data-files/#{f['key']}", "file", f["blurb"] + " " + " ".join(c[0] for c in cols))
    body = f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("dir")}<span>data/</span><span class="dim">· managed by dataManager</span></p>
  <h1>Data files</h1>
  <p class="lede">Each entity type lives in its own text file, one record per line, fields separated by <code>|</code> and lists by commas. The columns below are taken from the load and save methods.</p>
  <div class="chips"><span class="chip">delimiter <code>|</code></span><span class="chip">list separator <code>,</code></span><span class="chip">missing file → empty list</span><span class="chip">plain-text passwords</span></div>
</header>
{section("relations", "How files connect", f'<div class="figure">{files_diagram()}</div><aside class="callout warn"><p class="callout-t">Load order matters</p><p>Students load before courses, so the course codes in <code>students.txt</code> cannot be resolved and every student starts with an empty timetable. Course rosters in <code>courses.txt</code> still list them. <a href="{url("notes/")}#load-order">More in Known issues.</a></p></aside>')}
{''.join(blocks)}
{pager(("admin-workflow/", "Admin session"), ("validation/", "VALIDATION.md"))}"""
    add_search("Data files", "data-files/", "page", "students.txt courses.txt instructors.txt administrators.txt assessments.txt delimiter")
    return layout("data-files/", "Data files", body, tab="data/", tab_icon=("dir", ""), crumbs=("data",), structure=structure,
                  description="The five pipe-delimited text files behind the CS102 enrolment system: every column, how it loads, and sample records.")


def build_validation():
    structure = [("validators", "Validators", "h", 0), ("guards", "Guards & messages", "h", 0), ("exceptions", "Exception handling", "h", 0)]
    vrows = "".join(
        f'<tr><td><a href="{url("helpers/#m-" + v["method"])}"><code>{v["method"]}</code></a></td><td><code class="sig">{highlight_inline(v["rule"])}</code></td>'
        f'<td><span class="pass">{esc(v["ok"])}</span></td><td><span class="fail">{esc(v["bad"])}</span></td><td>{esc(v["used"])}</td></tr>'
        for v in VALIDATORS)
    grows = "".join(f'<tr><td><code>{esc(a)}</code></td><td>{esc(b)}</td><td><code class="out">{esc(c)}</code></td></tr>' for a, b, c in GUARDS)
    erows = "".join(f'<tr><td><code>{esc(a)}</code></td><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for a, b, c in EXCEPTIONS)
    body = f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("md")}<span>VALIDATION.md</span></p>
  <h1>Validation &amp; errors</h1>
  <p class="lede">Input is checked in three places: the Helpers validators before any setter runs, guards inside a few setters and loops, and try/catch blocks that keep the program alive.</p>
</header>
{section("validators", "Validators", f'<p>Each returns <code>true</code> or <code>false</code>, so prompts loop until the input passes. They are passed around as <code>Predicate&lt;String&gt;</code> method references, e.g. <code>Helpers::ValidateEmail</code>.</p><div class="table-wrap"><table class="grid"><thead><tr><th>Method</th><th>Passes when</th><th>Passes</th><th>Fails</th><th>Used by</th></tr></thead><tbody>{vrows}</tbody></table></div><div class="validator-lab" data-validator-lab></div><p class="note">Phone numbers are checked for length only, so any ten characters pass. The report suggests a regular expression instead.</p>', kicker="Helpers.Validate*")}
{section("guards", "Guards & messages", f'<div class="table-wrap"><table class="grid"><thead><tr><th>Where</th><th>Rule</th><th>Prints</th></tr></thead><tbody>{grows}</tbody></table></div>')}
{section("exceptions", "Exception handling", f'<div class="table-wrap"><table class="grid"><thead><tr><th>Where</th><th>Catches</th><th>What happens</th></tr></thead><tbody>{erows}</tbody></table></div><aside class="callout note"><p class="callout-t">Design rule</p><p>Never let user input crash the program, show a readable message instead of a stack trace, and handle the problem where it happens.</p></aside>')}
{pager(("data-files/", "data/"), ("reports-and-statistics/", "REPORTS.md"))}"""
    add_search("Validation & errors", "validation/", "page", "ValidatePassword ValidateEmail ValidatePhoneNumber getSafeIntInput exceptions")
    return layout("validation/", "Validation & errors", body, tab="VALIDATION.md", crumbs=("docs", "VALIDATION.md"), structure=structure)


def sample_state():
    """Course rosters as loaded from the sample courses.txt."""
    return [(c, len(c["students"])) for c in SAMPLE["courses"]]


def build_reports():
    structure = [("statistics", "Enrollment statistics", "h", 0), ("popular", "Most popular course", "h", 0), ("limits", "Limitations", "h", 0)]
    state = sample_state()
    stat_lines = ["---------Enrollment Statistics---------"] + [
        f'Course: {c["name"]} ({c["code"]}) - Enrolled: {n}' for c, n in state]
    total = sum(n for _, n in state)
    any_open = any(c["status"] == "Open" for c, _ in state)
    stat_lines += [f"Total enrolled students across all courses: {total}", f"Open courses available: {'Yes' if any_open else 'No'}"]
    best, best_n = None, 0
    for c, n in state:
        if n > best_n:
            best, best_n = c, n
    pop = ["---------Enrollment Report---------",
           f'Most popular course: {best["name"]} ({best["code"]}) - Enrolled: {best_n}.' if best else "No enrollments found."]
    bars = "".join(
        f'<li><span class="bar-label"><code>{esc(c["code"])}</code> {esc(c["name"])}</span>'
        f'<span class="bar-track cap"><span class="bar{" is-full" if n >= c["capacity"] else ""}" style="--w:{min(n / c["capacity"], 1) * 100:.1f}%"></span></span>'
        f'<span class="bar-val">{n}/{c["capacity"]}<span class="dim"> · {esc(c["status"])}</span></span></li>'
        for c, n in state)
    body = f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("md")}<span>REPORTS.md</span><span class="dim">· admin options 12 and 13</span></p>
  <h1>Reports &amp; statistics</h1>
  <p class="lede">Two console reports for administrators, both computed from each course's <code>enrolledStudents</code> list. The output below is what they print for the sample data.</p>
</header>
{section("statistics", "Enrollment statistics", f'<p>Admin option 12 calls <a href="{url("data-manager/#m-viewEnrollmentStatistics")}"><code>dataManager.viewEnrollmentStatistics()</code></a>: one line per course, a running total, and whether any course is open.</p><div class="split"><div>{term_block(chr(10).join(stat_lines), "admin › 12")}</div><div><p class="mini-title">Seats taken / capacity</p><ul class="bars cap">{bars}</ul></div></div>', kicker="option 12")}
{section("popular", "Most popular course", f'<p>Admin option 13 calls <a href="{url("data-manager/#m-generateReports")}"><code>dataManager.generateReports()</code></a>. It keeps the first course with the highest count, so a tie goes to the course listed first.</p>{term_block(chr(10).join(pop), "admin › 13")}', kicker="option 13")}
{section("limits", "Limitations", '<ul class="checks muted"><li>Console text only: no charts and no file export</li><li>No history and no comparison across semesters</li><li>Dropped students are still counted, because dropping does not update the roster</li></ul>')}
{pager(("validation/", "VALIDATION.md"), ("notes/", "KNOWN_ISSUES.md"))}"""
    add_search("Reports & statistics", "reports-and-statistics/", "page", "viewEnrollmentStatistics generateReports most popular course")
    return layout("reports-and-statistics/", "Reports & statistics", body, tab="REPORTS.md", crumbs=("docs", "REPORTS.md"), structure=structure)


def build_notes():
    structure = []
    counts = {k: len([i for i in ISSUES if i["kind"] == k]) for k in ("bug", "quirk", "design")}
    cards = []
    for i in ISSUES:
        slug, meth = i["where"]
        cls = by_slug(slug)
        line = ""
        if meth:
            m = next((m for m in PARSED[slug]["members"] if m["name"] == meth), None)
            if m:
                line = f'<a class="ln-link" href="{url(slug + "/")}#L{m["line"]}">L{m["line"]}</a>'
        where = f'<a class="chip" href="{member_link(slug, meth)}">{file_icon("cls", cls["icon"])}{esc(cls["name"])}{"." + esc(meth) + "()" if meth else ""}</a>{line}'
        src = "from the report" if i["source"] == "report" else "seen in the listing"
        fix = f'<p class="fix"><span>Fix</span>{esc(i["fix"])}</p>' if i["fix"] else ""
        cards.append(f"""<article class="issue {i['kind']}" id="{i['id']}" data-kind="{i['kind']}">
  <header><span class="badge {i['kind']}">{i['kind']}</span><h3>{esc(i['title'])}</h3><span class="dim src">{src}</span></header>
  <p>{esc(i['body'])}</p>{fix}<div class="issue-where">{where}</div>
</article>""")
        structure.append((i["id"], i["title"], "m" if i["kind"] == "bug" else "f", 0))
        add_search(i["title"], f"notes/#{i['id']}", "issue", i["body"], "KNOWN_ISSUES.md")
    filt = "".join(f'<button type="button" class="seg" data-filter="{k}" aria-pressed="false">{k} <span class="dim">{n}</span></button>' for k, n in counts.items())
    imp = "".join(f"<li>{esc(t)}</li>" for t in IMPROVEMENTS)
    body = f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("md")}<span>KNOWN_ISSUES.md</span></p>
  <h1>Known issues</h1>
  <p class="lede">Behaviours worth knowing before you read or run the code. Some come from the report itself; the rest were found by reading the report's listings line by line. The console on this site reproduces them.</p>
  <div class="segs" role="group" aria-label="Filter by kind"><button type="button" class="seg is-on" data-filter="all" aria-pressed="true">all <span class="dim">{len(ISSUES)}</span></button>{filt}</div>
</header>
<div class="issues" data-issues>{''.join(cards)}</div>
{section("ideas", "Improvement ideas", f'<ul class="checks">{imp}</ul>', kicker="from the report")}
{pager(("reports-and-statistics/", "REPORTS.md"), ("project-report/", "report.pdf"))}"""
    structure.append(("ideas", "Improvement ideas", "h", 0))
    add_search("Known issues", "notes/", "page", "bugs quirks design notes")
    return layout("notes/", "Known issues", body, tab="KNOWN_ISSUES.md", crumbs=("docs", "KNOWN_ISSUES.md"), structure=structure,
                  description="Known issues in the CS102 School Course Enrolment System: bugs, quirks and design notes, each linked to its line of Java.")


def build_report():
    rows = "".join(f'<tr><td>{esc(a)}</td><td class="num">{esc(b)}</td><td><a href="{url(c)}">open</a></td></tr>' for a, b, c in REPORT_SECTIONS)
    pdf = url(SITE["pdf"])
    body = f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("pdf")}<span>report.pdf</span><span class="dim">· 102 pages</span></p>
  <h1>Project report</h1>
  <p class="lede">The full report for the School Course Enrolment System, submitted for {esc(SITE['course'])} ({esc(SITE['course_name'])}) at {esc(SITE['institution'])} by {esc(SITE['author'])}.</p>
  <div class="actions"><a class="btn btn-run" href="{pdf}" download>Download PDF</a><a class="btn" href="{pdf}" target="_blank" rel="noopener">Open in a new tab</a></div>
</header>
{section("map", "What it covers", f'<div class="table-wrap"><table class="grid"><thead><tr><th>Section</th><th class="num">Pages</th><th>On this site</th></tr></thead><tbody>{rows}</tbody></table></div>')}
{section("read", "Read online", f'<div class="pdf-frame"><object data="{pdf}" type="application/pdf"><p>Your browser cannot show the PDF here. <a href="{pdf}">Download the report</a> instead.</p></object></div>')}
{pager(("notes/", "KNOWN_ISSUES.md"), ("", "README.md"))}"""
    add_search("Project report (PDF)", "project-report/", "page", "102 pages PDF download")
    return layout("project-report/", "Project report", body, tab="report.pdf", tab_icon=("pdf", ""), crumbs=("docs", "report.pdf"),
                  structure=[("map", "What it covers", "h", 0), ("read", "Read online", "h", 0)])


def build_policy(p):
    structure = [(m.group(1), html.unescape(m.group(2)), "h", 0) for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', p["html"])]
    body = f"""
<header class="doc-head">
  <p class="eyebrow">{file_icon("md")}<span>policies</span></p>
  <h1>{esc(p['title'])}</h1>
  <p class="lede dim">{esc(p['updated'])}</p>
</header>
<div class="prose">{p['html']}</div>"""
    return layout(p["slug"] + "/", p["title"], body, tab=p["title"], crumbs=("policies", p["title"]), structure=structure)


def build_404():
    body = f"""
<section class="nf">
  {term_block("Exception in thread \"main\" java.io.FileNotFoundException: page not found" + chr(10) + "    at Router.open(Router.java:404)", "stderr")}
  <h1>This page isn't on the class path.</h1>
  <p class="lede">The site was rebuilt, and some old addresses moved. Try search, or start from the README.</p>
  <div class="actions"><a class="btn btn-run" href="{url()}">README.md</a><button type="button" class="btn" data-open-search>Search everywhere</button></div>
</section>"""
    return layout("404.html", "Not found", body, tab="404", crumbs=("404",))


REDIRECTS = {
    "structure": "architecture/", "file-structure": "architecture/#layout", "code-per-class": "architecture/#classes",
    "code-main": "main/", "code-helpers": "helpers/", "code-data-manager": "data-manager/",
    "menus": "run/", "exit-exception": "run/#exit", "exceptions-and-validation": "validation/",
}
for _s in ("main", "user", "student", "instructor", "administrator", "assessment", "course", "helpers", "data-manager"):
    REDIRECTS[f"source-code/{_s}"] = f"{_s}/#source"


def redirect_page(target):
    t = url(target)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title>'
            f'<link rel="canonical" href="{SITE["url"]}{target}"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={t}"></head>'
            f'<body><p>This page moved to <a href="{t}">{t}</a>.</p></body></html>')


def sample_js():
    disk = {f["key"]: lines_for(f["key"]) for f in FILES}
    payload = {"disk": disk, "defaultAdmin": DEFAULT_ADMIN, "examTypes": EXAM_TYPES,
               "validators": VALIDATORS}
    return "window.CE_SAMPLE=" + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n"


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(WEB / "static", OUT)
    load_java()
    write("", build_home())
    for i, c in enumerate(CLASSES):
        write(c["slug"] + "/", build_class(c, i))
    for i, w in enumerate(WORKFLOWS):
        write(w["slug"] + "/", build_workflow(w, i))
    write("run/", build_run())
    write("architecture/", build_architecture())
    write("data-files/", build_data())
    write("validation/", build_validation())
    write("reports-and-statistics/", build_reports())
    write("notes/", build_notes())
    write("project-report/", build_report())
    for p in POLICIES:
        write(p["slug"] + "/", build_policy(p))
        add_search(p["title"], p["slug"] + "/", "page", "")
    (OUT / "404.html").write_text(build_404(), encoding="utf-8")
    PAGES.pop()  # 404 is not part of the sitemap
    for old, new in REDIRECTS.items():
        write(old + "/", redirect_page(new))
    (OUT / "js" / "sample-data.js").write_text(sample_js(), encoding="utf-8")
    (OUT / "search.json").write_text(json.dumps(SEARCH, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    sitemap = "".join(f"<url><loc>{SITE['url']}{p}</loc></url>" for p, _ in PAGES)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>\n',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}sitemap.xml\n", encoding="utf-8")
    print(f"Built {len(PAGES)} pages, {len(REDIRECTS)} redirects, {len(SEARCH)} search entries → {OUT}")


if __name__ == "__main__":
    main()
    if "--serve" in sys.argv:
        import functools
        import http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("Serving on http://localhost:8000")
        http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()
