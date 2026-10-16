# Diagrams

Diagrams are box-drawing text in `<figure class="diagram"><pre role="img" aria-label="…">`.
They inherit the theme, copy as text, and stay sharp at every zoom level. Never use SVG or images
for architecture.

## How to draw

1. Use `../scripts/canvas.py` (or the site's `tools/site/diagram_*.py`). Place boxes by coordinates
   and compute connector positions from box midpoints (`mid = x + width // 2`). Never hand-align
   strings in an editor; a column off by one shows immediately.
2. Draw in this order: boxes, then bus lines, then junctions (`┬ ┴ ┼`), then arrowheads, then labels.
   Later writes win.
3. Keep labels out of borders when a connector has to land on that border. A title in a top border
   collides with a `┴` junction, so put the title on the first inside line in CAPS instead.
4. Arrowheads point the way the connection is *initiated*. Lilly hosts dial out to Marshall, so the
   arrow points up (`▲`) under Marshall, not down at the hosts. Use `◀─▶` for two-way links.
5. Width budget:
   - At most about 84 columns, so a diagram fits the 100ch page inside the figure's padding and border.
   - `canvas.render()` refuses anything over 88.
   - On phones, `pre` scrolls sideways, which is fine.
6. Paste the output into the generator as a triple-quoted string. The site's generator keeps it as
   `LANDING_DIAGRAM`, `REGIONS_DIAGRAM`, `ARCH_*` and so on in `tools/site/pages_main.py`.
7. Write an `aria-label` that tells the whole story in plain sentences, and a one-line `figcaption`
   that states the point ("Centralise the control plane; distribute the hosts.").

## Characters

```
corners   ┌ ┐ └ ┘        lines   ─ │        double   ║ ═ ╨
tees      ├ ┤ ┬ ┴ ┼      arrows  ▲ ▼ ◀ ▶ ─▶ ◀─▶
separator ·              ellipsis between boxes  ··  (inside the gap, never over a border)
```

## Canonical diagrams on the site

**Request path (landing page).** The browser goes through a proxy and SSH through Porsche to
Marshall, which uses PostgreSQL. Marshall fans out to three Lilly host boxes, each holding
`┌────┐│ vm │` guests, with "HTTPS, dialled out by every host" on the bus. Audi routes SSH and web
traffic to whichever host runs the guest.

**Regions.**

```
          ┌─ control plane · one region ───────────────────────────────┐
          │                                                            │
          │  HAProxy ─▶ Marshall · Marshall · Marshall ◀─▶ PostgreSQL  │
          │  several Marshall instances for high availability          │
          │                                                            │
          └──────────────────────────────┬─────────────────────────────┘
                                         ▲
                                         │  HTTPS, dialled out by every host
                                         │
            ┌────────────────────────────┼────────────────────────────┐
 ┌──────────┴──────────┐      ┌──────────┴──────────┐      ┌──────────┴──────────┐
 │ WASHINGTON DC       │      │ LONDON              │      │ SINGAPORE           │
 │ Lilly  Lilly  Lilly │      │ Lilly  Lilly        │      │ Lilly  Lilly        │
 │ guests on ZFS       │      │ guests on ZFS       │      │ guests on ZFS       │
 │ Audi: SSH, web apps │      │ Audi: SSH, web apps │      │ Audi: SSH, web apps │
 └─────────────────────┘      └─────────────────────┘      └─────────────────────┘
            ▲                            ▲                            ▲
      developers in                developers in                developers in
      the Americas                    Europe                    Asia-Pacific
```

**Two paths to a machine** (`tools/site/diagram_paths.py`). This is the locality story: SSH and
VS Code go direct to Audi in the same region, while the browser terminal and browser editor are relayed
through the central control plane. Keep the two paths visibly different (up-and-over versus straight across).

```
      ┌─ control plane · one region ─────────────────────────────────────────┐
      │  HAProxy ─▶ Marshall · Marshall · Marshall ◀─▶ PostgreSQL            │
      └───────▲──────────────────────────────────────────────────────▲───────┘
              │ web terminal and                  relay over HTTPS,  │
              │ browser editor                 dialled out by Lilly  │
              │                                                      │
 ┌────────────┴────────────┐                          ┌──────────────┴─────────────┐
 │ DEVELOPER IN SINGAPORE  │                          │ HOST IN SINGAPORE          │
 │ browser                 │   direct, same region    │                            │
 │ ssh, VS Code ───────────┼─────────────────────────▶│ Audi ─▶ Lilly ─▶ guest     │
 └─────────────────────────┘                          └────────────────────────────┘
```

**Lifecycle (architecture page).** States are bracketed words, `[pending] ─▶ [running]`, and side
effects branch off a `├─` rail: `├─ relocate ─▶ another host`.

**Guest edge.** A guest box on the left, with `──┼──▶` arrows out to Brady, Enrico, Ziggy and
Galileo, each followed by a short role.
