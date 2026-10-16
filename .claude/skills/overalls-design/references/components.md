# Components (copy-paste HTML)

Every class below is defined in `assets/css/site.css`. Prefer plain elements, and add a class only
when the recipe uses one.

## Page skeleton

See `../assets/page-template.html`. In order:

1. `<head>`: charset, viewport, title, description, `color-scheme`, OG tags, favicon,
   font preloads (500, 600 and 800 weights), `site.css`, and `site.js` in head without `defer`.
2. `<div class="public-page">`, then the skip link, header, `<main id="main-content">` and footer.

Titles use the form `Page · Overalls`. The home page title is `Overalls: an AI-first developer platform that you own`.

## Announcement banner (every page, above the header)

```html
<aside class="announcement" aria-label="Announcement">
<span class="status-label" data-tone="experimental">RESEARCH PREVIEW</span>
<p>Overalls launches on <time datetime="2026-11-03">3 November 2026</time>. <a href="index.html#newsletter">Get notified →</a></p>
</aside>
```

- It's a dashed 2px box, half a line of padding top and bottom, with an inverse-video label and a
  bold `<time>`.
- Keep it to one sentence plus one link, so it fits on one line at desktop width.
- `announcement()` in `tools/site/layout.py` renders it. Change or remove it there after launch.

## Header (every page)

```html
<header class="public-header">
<table class="header">
<tr>
<td colspan="2" rowspan="2" class="width-auto">
<p class="title"><a href="index.html" class="console-brand">Overalls<span class="brand-dot">.</span></a></p>
<p class="tagline">An AI-first developer platform that you own.</p>
</td>
<th class="width-min">Guide</th>
<td class="width-min"><a href="self-host/index.html">Self-host</a></td>
</tr>
<tr>
<th class="width-min">Design</th>
<td class="width-min"><a href="architecture.html">Architecture</a></td>
</tr>
<tr class="appearance-row">
<th class="width-min">Source</th>
<td class="width-auto"><a href="https://github.com/ghuntley/overalls">GitHub <span aria-hidden="true">↗</span></a> · MIT</td>
<th class="width-min">Appearance</th>
<td class="width-min"><label class="appearance-control select"><span class="sr-only">Appearance</span><select data-appearance aria-label="Appearance">
<option value="system">System</option><option value="light">Light</option><option value="dark">Dark</option>
</select></label></td>
</tr>
</table>
</header>
```

- Mark the current section with `aria-current="page"` on its link, which renders it in inverse video.
- Below 800px the table becomes labelled lines: a 14ch label column, then the value.

## Buttons

```html
<div class="row actions">
<a class="console-button primary" href="self-host/index.html">Self-host it →</a>
<a class="console-button" href="https://github.com/…">Source on GitHub <span aria-hidden="true">↗</span></a>
</div>
```

- Buttons are uppercase, weight 600 and two lines tall.
- `primary` is inverse video. Use one per view at most.
- `ghost` has no border until hover. `compact` is one line tall and underlined.

## Status labels

```html
<span class="status-label" data-tone="stable">STABLE</span>
<span class="status-label" data-tone="preview">PREVIEW</span>
<span class="status-label" data-tone="experimental">EXPERIMENTAL</span>
```

| Tone | Rendering |
|---|---|
| stable | bold |
| preview | muted |
| experimental | inverse video, bold |

Always show the legend near a group of labels:

```html
<p class="legend"><span class="status-label" data-tone="stable">STABLE</span> built and covered by acceptance tests · <span class="status-label" data-tone="preview">PREVIEW</span> works, with rough edges · <span class="status-label" data-tone="experimental">EXPERIMENTAL</span> still being built</p>
```

## Feature cards, grouped by category

```html
<div class="feature-group">
<h3>Machines</h3>
<div class="cols feature-grid">
<article class="panel">
<header><h4>Persistent microVMs</h4><span class="status-label" data-tone="stable">STABLE</span></header>
<p>One to three sentences. What it does, then why you'd care.</p>
</article>
</div>
</div>
```

- Within each category, order cards stable, then preview, then experimental.
- The categories on the site: Machines, Operating systems, Working on a machine, Collaboration,
  Starting from a repository, AI, Running the platform.
- In the generator, `FEATURES` and `CATEGORIES` live in `tools/site/pages_main.py`. An assert fails
  the build if a card isn't in exactly one category.

## Sections

```html
<section aria-labelledby="how">
<h2 id="how">How it fits together</h2>
<p>…</p>
</section>
```

h2 gets a muted `## ` prefix automatically. Write headings in sentence case; CSS uppercases them.

## Key/value facts

```html
<dl class="kv">
<div><dt>Hardware</dt><dd>x86_64 bare metal with a working <code>/dev/kvm</code></dd></div>
</dl>
```

Muted 12ch+ keys sit beside values. Use this at the top of each guide page (audience, time, status)
and for requirements.

## Step ladder

```html
<ol class="steps">
<li data-state="done"><span class="step-marker" aria-hidden="true"></span>Done step</li>
<li data-state="current"><span class="step-marker" aria-hidden="true"></span>Current step</li>
<li><span class="step-marker" aria-hidden="true"></span><a href="…">Pending step</a></li>
</ol>
```

The markers render as `[■]` (done), `[▸]` (current) and `[ ]` (pending). Pending steps are muted.

## Command blocks

```html
<pre class="term" data-copy><span class="prompt">$ </span>ssh &lt;gateway&gt; new --name scratch</pre>
```

- `data-copy` adds a `COPY` button when JS runs.
- Spans with class `prompt` or `out` are left out of the copied text.
- In guide pages, `pre` inside `.docs-content` gets the alt background automatically.
- Escape `<` and `>` in placeholders: `&lt;your-domain&gt;`. The generator's `sh()` and `code()`
  helpers do this for you.

## Diagram figure

```html
<figure class="diagram">
<pre role="img" aria-label="Plain-English description of the whole picture.">…box drawing…</pre>
<figcaption>One short line, then a link if needed. <a href="architecture.html">Full architecture →</a></figcaption>
</figure>
```

## Tables

- Use semantic `<table>` with `thead`, and `.width-min` / `.width-auto` on columns.
- Add `class="table-stack"` and `data-label="Name:"` on cells so the table becomes one block per
  row below 800px.

## FAQ

```html
<section aria-labelledby="faq" class="faq">
<h2 id="faq">Questions</h2>
<details><summary>Is there a hosted Overalls I can sign up for?</summary><p>No. …</p></details>
</section>
```

## Guide page layout

Use a `.docs-shell` grid:
- `aside.docs-nav`: a `ul.tree` with "Self-host" and "Reference" groups, the current page marked
  with `aria-current="page"`.
- `main.docs-content.prose`, which contains in order:
  - an h1
  - a lead paragraph
  - a `dl.kv` of facts
  - numbered h2 steps (`1. Discover`)
  - `Full reference: … ↗` lines linking to the repo docs
  - `nav.pager` with `← Previous` and `Next →`

`guide_page()` in `tools/site/layout.py` builds all of this.

## Newsletter signup (Ghost)

```html
<form class="newsletter-form" action="https://ghuntley.com/newsletter/" method="get" data-ghost-site="https://ghuntley.com">
<label for="newsletter-email" class="sr-only">Email address</label>
<input id="newsletter-email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required>
<button type="submit" class="console-button primary">Subscribe</button>
</form>
<p class="newsletter-status muted" role="status" aria-live="polite">Unsubscribe any time. Sent from <a href="https://ghuntley.com/newsletter/">ghuntley.com ↗</a>.</p>
```

- `site.js` makes the same two calls as Ghost's own embeddable signup form, without its iframe or
  third-party script:
  1. `GET /members/api/integrity-token/`
  2. `POST /members/api/send-magic-link/` with `{email, emailType: "signup", integrityToken}`
- Ghost answers every origin with `access-control-allow-origin: *`, on its 4xx errors too, so a
  refusal from Ghost itself (`Email is not valid`, Ghost's own 429s) is shown verbatim.
- ghuntley.com is on Ghost(Pro). Fastly's WAF sits in front of `/members/api/` and refuses some
  networks (VPNs, shared and datacenter addresses, addresses that signed up repeatedly) with a
  `429 Too many sign-up attempts` that has no CORS headers and also covers preflights. The browser
  reports that only as `Failed to fetch`. The status line then explains the likely cause and links
  to `ghuntley.com/#/portal/signup`, where Portal runs on Ghost's own origin and can show the real
  reason. Nothing on this site can get past that block.
- Status text is always set with `textContent`, never `innerHTML`.
- Without JS, the form opens ghuntley.com/newsletter/.
- Testing: a blocked network cannot test this at all, and a browser gives no detail, so test with
  curl from a network you haven't signed up from (a GitHub Actions runner works):

  ```sh
  O="Origin: https://overalls.dev"
  curl -sS -D - -o tok.txt -H "$O" https://ghuntley.com/members/api/integrity-token/
  curl -sS -D - -H "$O" -H "Content-Type: application/json" \
    -d "{\"email\":\"a@b\",\"emailType\":\"signup\",\"integrityToken\":\"$(cat tok.txt)\"}" \
    https://ghuntley.com/members/api/send-magic-link/
  ```

  Healthy: `200` with the token, then `400 {"errors":[{"message":"Email is not valid"}]}`, both
  with `access-control-allow-origin: *`. A real address returns `201` and sends the magic link, so
  use one only when you mean to sign it up. Blocked: `429` from `server: Varnish` with no CORS
  header on every request, including the token and `OPTIONS`.

## Footer

```html
<footer class="site-footer">
<p><a href="index.html">Overalls</a> is open source under the <a href="…/LICENSE">MIT licence ↗</a>. There is no hosted service: you run it.</p>
<p>Set in JetBrains Mono (OFL). Styled after The Monospace Web by Oskar Wickström (MIT). <a href="llms.txt">llms.txt</a></p>
</footer>
```

The footer has a double rule on top and muted text and links.
