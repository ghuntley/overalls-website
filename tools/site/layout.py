"""Shared page chrome for the Overalls static site. Output is plain HTML."""

SOURCE = "https://github.com/ghuntley/overalls"
DOCS = SOURCE + "/blob/main/docs/"
ADR = DOCS + "architecture/decisions/"

MARK = """\
    ╱╲         ╱╲
   ╱  ╲───────╱  ╲
  │    ●     ●    │
  │  ═    ▾    ═  │
  │  ═   ╰┴╯   ═  │
   ╲─┬─────────┬─╱
  ┌──■─────────■──┐
 ╭┤   ┌───────┐   ├╮
 ││   ├───────┤   ││
 ●│   └───────┘   │●
┌─┴───────────────┴─┐
│■                 ■│
│       ┌───┐       │   ╭─╮
│       │   │       │   │ │
│       │   │       ├───╯ │
└───────┘   └───────┘─────╯
 ╰─●─●─╯     ╰─●─●─╯"""

# Simple Analytics, on every page. The only third-party resource the site loads.
ANALYTICS = """<script data-collect-dnt="true" async src="https://scripts.simpleanalyticscdn.com/latest.js"></script>
<noscript><img src="https://queue.simpleanalyticscdn.com/noscript.gif?collect-dnt=true" alt="" referrerpolicy="no-referrer-when-downgrade"/></noscript>
"""

GUIDE = [
    ("index.html", "Overview"),
    ("provision.html", "Provision a host"),
    ("deploy.html", "Deploy the control plane"),
    ("enroll.html", "Enroll hosts and images"),
    ("first-machine.html", "Your first machine"),
    ("operations.html", "Day-two operations"),
]


def head(title, description, r):
    full = f"{title} · Overalls" if title != "Overalls" else "Overalls: an AI-first developer platform that you own"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{description}">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<link rel="icon" type="image/svg+xml" href="{r}favicon.svg">
<link rel="preload" as="font" type="font/woff2" crossorigin href="{r}assets/fonts/jetbrains-mono-500.woff2">
<link rel="stylesheet" href="{r}assets/css/site.css">
<script src="{r}assets/js/site.js"></script>
</head>
"""


def header(r, current):
    def link(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{r}{href}"{cur}>{label}</a>'

    return f"""<a href="#main-content" class="skip-link">Skip to content</a>
<header class="public-header">
<table class="header">
<tr>
<td colspan="2" rowspan="2" class="width-auto">
<p class="title"><a href="{r}index.html" class="console-brand">Overalls<span class="brand-dot">.</span></a></p>
<p class="tagline">An AI-first developer platform that you own.</p>
</td>
<th class="width-min">Guide</th>
<td class="width-min">{link("self-host/index.html", "Self-host", "guide")}</td>
</tr>
<tr>
<th class="width-min">Design</th>
<td class="width-min">{link("architecture.html", "Architecture", "architecture")}</td>
</tr>
<tr class="appearance-row">
<th class="width-min">Source</th>
<td class="width-auto"><a href="{SOURCE}">GitHub <span aria-hidden="true">↗</span></a> · MIT</td>
<th class="width-min">Appearance</th>
<td class="width-min"><label class="appearance-control select"><span class="sr-only">Appearance</span><select data-appearance aria-label="Appearance">
<option value="system">System</option>
<option value="light">Light</option>
<option value="dark">Dark</option>
</select></label></td>
</tr>
</table>
</header>
"""


def footer(r):
    return f"""<footer class="site-footer">
<p><a href="{r}index.html">Overalls</a> is open source under the <a href="{SOURCE}/blob/main/LICENSE">MIT licence <span aria-hidden="true">↗</span></a>. There is no hosted service: you run it.</p>
<p>Set in <a href="https://www.jetbrains.com/lp/mono/">JetBrains Mono <span aria-hidden="true">↗</span></a> (<a href="{r}assets/fonts/jetbrainsmono-OFL.txt">OFL</a>). Styled after <a href="https://owickstrom.github.io/the-monospace-web/">The Monospace Web <span aria-hidden="true">↗</span></a> by Oskar Wickström (<a href="{r}assets/monospace-web-LICENSE.md">MIT</a>). <a href="{r}security/">Security</a> · <a href="{r}llms.txt">llms.txt</a></p>
</footer>
"""


def page(title, description, body, r="", current=None):
    return (
        head(title, description, r)
        + '<body>\n<div class="public-page">\n'
        + header(r, current)
        + body
        + footer(r)
        + "</div>\n"
        + ANALYTICS
        + "</body>\n</html>\n"
    )


def guide_page(slug, title, description, body):
    r = "../"
    items = []
    for href, label in GUIDE:
        cur = ' aria-current="page"' if href == slug else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    idx = [h for h, _ in GUIDE].index(slug)
    prev_link = (
        f'<a href="{GUIDE[idx - 1][0]}">← {GUIDE[idx - 1][1]}</a>' if idx > 0 else "<span></span>"
    )
    next_link = (
        f'<a href="{GUIDE[idx + 1][0]}">{GUIDE[idx + 1][1]} →</a>'
        if idx + 1 < len(GUIDE)
        else f'<a href="../architecture.html">Architecture →</a>'
    )
    nav = (
        '<div class="docs-shell">\n<aside class="docs-nav">\n<nav aria-label="Self-hosting guide">\n<ul class="tree">\n'
        '<li><strong>Self-host</strong>\n<ul>\n'
        + "\n".join(items)
        + "\n</ul>\n</li>\n"
        '<li><strong>Reference</strong>\n<ul>\n'
        '<li><a href="../architecture.html">Architecture</a></li>\n'
        f'<li><a href="{SOURCE}/tree/main/docs">Repository docs ↗</a></li>\n'
        f'<li><a href="{SOURCE}/tree/main/docs/architecture/decisions">Decision records ↗</a></li>\n'
        "</ul>\n</li>\n</ul>\n</nav>\n</aside>\n"
    )
    main = (
        '<main id="main-content" class="docs-content prose">\n'
        + body
        + f'<nav class="pager" aria-label="Guide pages">{prev_link}{next_link}</nav>\n'
        + "</main>\n</div>\n"
    )
    return page(title, description, nav + main, r=r, current="guide")
