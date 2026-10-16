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

## The mark: two kittens in one pair of overalls

Overalls grew out of Kittens, so the mark is two kittens squeezed side by side into one pair of
overalls:

```
   ╱╲     ╱╲   ╱╲     ╱╲
  ╱  ╲───╱  ╲ ╱  ╲───╱  ╲
  │  ●     ● │ │ ●     ●  │
  │ ═   ▾   ═│ │═   ▾   ═ │
  │    ╰┴╯   │ │   ╰┴╯    │
   ╲─┬─────┬╱   ╲┬─────┬─╱
  ┌──■─────■─────■─────■──┐
 ╭┤      ┌─────────┐      ├╮
 ││      ├─────────┤      ││
 ●│      └─────────┘      │●
┌─┴───────────────────────┴─┐
│■                         ■│
│           ┌───┐           │   ╭─╮
│           │   │           │   │ │
│           │   │           ├───╯ │
└───────────┘   └───────────┘─────╯
 ╰──●─●──╯         ╰──●─●──╯
```

- **Parts:**
  - Two box-drawn heads, leaning in towards each other, each with pointed `╱╲` ears, `●` eyes, a
    `▾` nose, an `ω`-shaped mouth (`╰┴╯`) and `═` whiskers.
  - Each kitten's straps (`┬`) run from its chin to its own pair of button rivets (`■`), so the bib
    has four.
  - One bib pocket with a flap (`├─────────┤`), centred.
  - Arms with round `●` paws at the outer sides.
  - Waistband side buttons and two legs.
  - A tail curling up behind the right leg.
  - Toe-bean feet: `╰──●─●──╯`.
- **Rendering:** a `<pre class="mark" aria-hidden="true">` inside a `<figure>`, weight 800.
  - It's 35 columns wide.
  - In `.mark` it's drawn at `font-size: .875rem` with `line-height: 1.2` (em-relative, so the box
    drawing joins up). That keeps the hero headline on two lines at desktop width next to it.
  - On phones it sits centred above the h1.
- **Caption:** `made to get dirty`, in muted text, centred under the mark.
- **Where it goes:** the landing hero and the 404 page. Nowhere else, to keep it special.
- **Source:** `MARK` in `tools/site/layout.py`. Change it there and rebuild; never edit the HTML copies.
- **History:**
  1. A pair of overalls with no wearer. An earlier version with two `■` dots inside the bib read as a
     robot face, so avoid that.
  2. One kitten in overalls (27 columns).
  3. Two kittens, the current mark.

  Another option considered was a tiny kitten peeking out of the bib pocket. Compare drafts by
  rendering them side by side in JetBrains Mono at 2x, never by eye in a terminal.

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
