# Visual system

## The grid

- One cell is `1ch` wide (one JetBrains Mono character) and `var(--line-height)` tall.
- `--line-height: 1.203125rem`. That's 1.2rem, nudged so browser layout units of 1/64px
  stay exact and lines never drift. Don't round it.
- Root font size is 16px, dropping to 14px at 480px wide or less. Everything scales from it.
- Widths:
  - Page column: `min(100ch, 100%)`
  - Prose: `min(80ch, 100%)`
  - Docs sidebar: 28ch
  - Card grid minimum: 32ch
  - Hero lede: 60ch
- Snap widths to whole characters: `calc(round(down, 100%, 1ch))`.
- Bordered box padding: `calc(var(--line-height) - var(--border-thickness)) calc(2ch - var(--border-thickness))`.
- Vertical rhythm: children of `.stack`, `.prose` and `.panel-body` get one line of top margin.
  Paragraphs have one line of bottom margin. Sections have two lines below and h2 has two lines above.

## Colour tokens (the only colours)

| Token | Light | Dark | Use |
|---|---|---|---|
| `--text-color` | `#000` | `#fff` | Text, borders, inverse-video fills |
| `--text-color-alt` | `#666` | `#aaa` | Secondary text, captions, `## ` prefixes, PREVIEW labels |
| `--background-color` | `#fff` | `#000` | Page |
| `--background-color-alt` | `#eee` | `#111` | Code blocks, hover |

Theme selection:
- The page follows `prefers-color-scheme`.
- `<html data-theme="light|dark">` overrides it.
- `site.js` sets `data-theme` from a System/Light/Dark `<select data-appearance>` and stores the choice
  in `localStorage['overalls:theme']`.
- The script loads in `<head>` without `defer`, so the theme is applied before first paint.
- With JS off, the page still follows the OS.

Emphasis, in increasing strength:
1. `--text-color-alt`
2. Weight 600
3. Weight 800
4. Inverse video (background is `--text-color`, text is `--background-color`)

Inverse video marks the current nav item, the primary button and EXPERIMENTAL labels.

## Type

- **Typeface:** JetBrains Mono only, self-hosted as woff2 in weights 500, 500 italic, 600 and 800.
  Preload the 500 weight.
- **Weights:** body 500; `th`, `summary`, `label`, `code` and buttons 600; headings and `strong` 800.
- **Numbers:** `font-variant-numeric: tabular-nums lining-nums`.
- **Type scale:** there are exactly two sizes.
  - `h1` is 2rem, two lines tall, UPPERCASE. On screens of 480px or less, the hero h1 drops to 1.5rem.
  - Everything else is 1rem.
- **Heading prefixes:** h2 is UPPERCASE with a muted `## ` added by CSS (`section > h2::before`).
  Category h3 inside "What you get" gets a muted `### `. Card titles are h4, in sentence case.
- **Wrapping:** use `text-wrap: balance` on headlines and taglines so no line ends with a lone word.
  Force a deliberate line break with `<span class="line">` (display: block) rather than `<br>`.
  For example, "An AI-first developer platform / that you own."
- **Links:** underlined with a 2px decoration and the same colour as text. External links end in ` ↗`.

## Borders and shapes

- Borders are always `2px solid var(--text-color)`. Focused form controls go to 3px.
- `border-radius: 0` everywhere. Radio buttons are the only round thing.
- Variants:
  - Dashed: empty or placeholder states.
  - Double 6px: danger panels and `hr` rules.
  - Double 6px top border: the site footer.
- No shadows, gradients or blur. The only motion is `button:active { transform: translate(2px, 2px) }`,
  and only when reduced motion isn't requested.

## Glyphs (the icon set)

Use only these glyphs, written as plain text:

```
↗  external link        ←  back / previous      →  next / go
▶ ▼  details markers      ▾  select arrow         ■  done / button (mark)
[ ] [■] [▸]  step ladder   ·  separator            ▲ ▼ ◀ ▶  diagram arrowheads
─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ║ ╨  box drawing (see diagrams.md)
```

Status words always appear in brackets: `[STABLE]`, `[running]`. The brackets come from CSS on
`.status-label`, so the DOM text stays clean.

## Layout patterns

- **Page:** `.public-page` centres a 100ch column with 2ch side padding and one line of top padding.
- **Header:** the Monospace Web `table.header`. See components.md.
- **Hero:** a two-column grid, with copy (h1, two lede paragraphs, button row) on the left and the
  ASCII mark in a `<figure>` with a muted caption on the right. Below 800px it becomes one column,
  with the mark first and centred.
- **Card grid:** `.cols`, an auto-fit grid with `minmax(32ch, 1fr)` columns and a 1-line × 2ch gap.
  That gives two columns at desktop width and one on phones.
- **Docs:** `.docs-shell`, a 28ch `.tree` sidebar next to `main.docs-content.prose`. Below 800px the
  nav stacks on top with a bottom rule.
- **Responsive breakpoints:** 800px (header stacks, grids collapse) and 480px (14px root, smaller hero h1).
- **Overflow:** the page never scrolls sideways. Only `pre` scrolls horizontally (`white-space: pre; overflow-x: auto`).

## Print

The `@media print` block forces light tokens (`--text-color-alt: #444`, `--background-color-alt: #fff`)
and hides the appearance row, copy buttons and skip link.
