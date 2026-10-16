# Brand

## Name and wordmark

- **Overalls**: workwear, the thing you put on before getting your hands dirty. The first production
  host was called `overalls`, and its sibling is `dungarees`.
- **Wordmark:** `OVERALLS.`, set in JetBrains Mono 800, uppercase, with the full stop in
  `--text-color-alt`:

  ```html
  <a class="console-brand">Overalls<span class="brand-dot">.</span></a>
  ```

  It's 2rem in the header and 1rem inline. The word is the logo; there is no logotype image.
- **Tagline:** "An AI-first developer platform that you own." It goes under the wordmark (muted,
  balanced wrap) and in the hero h1, which breaks before "that you own." on desktop.

## The mark: a pair of overalls

```
    ║        ║
    ║        ║
  ┌─■────────■─┐
  │  ┌──────┐  │
  │  ├──────┤  │
  │  └──────┘  │
┌─┴────────────┴─┐
│■              ■│
│      ┌──┐      │
│      │  │      │
│      │  │      │
└──────┘  └──────┘
```

- **Parts:**
  - Double-line straps (`║`) attach at button rivets (`■`) on the bib.
  - A bib pocket with a flap (`├──────┤`).
  - Waistband side buttons.
  - Two legs.
- **Rendering:** a `<pre class="mark" aria-hidden="true">` inside a `<figure>`, weight 800,
  `line-height: var(--line-height)` so box characters join up.
- **Caption:** `made to get dirty`, in muted text, centred under the mark.
- **Where it goes:** the landing hero (right column; first and centred on mobile) and the 404 page.
  Nowhere else, to keep it special.
- **Don't** put `■` dots inside the bib without the pocket. An earlier version did, and it read as
  a robot face.

## Favicon

`assets/favicon.svg` is a 32×32 monochrome overalls silhouette: straps, bib with pocket, legs. It's
drawn as a 2.4px mitred stroke on a square. An internal `prefers-color-scheme` style flips it to
white on black. No colour.

## Colour

There is no brand colour. The brand is black on white and white on black, plus two greys (see the
token table in visual-system.md). Inverse video is the accent.

## Credits (always include)

- The Monospace Web © Oskar Wickström, MIT: `assets/monospace-web-LICENSE.md`
- JetBrains Mono © JetBrains, SIL OFL 1.1: `assets/fonts/jetbrainsmono-OFL.txt`
