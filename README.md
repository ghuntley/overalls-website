# overalls.dev

The public website for [Overalls](https://github.com/ghuntley/overalls), the
self-hosted platform for persistent Firecracker development machines and the AI
agents that work on them. GitHub Pages serves the committed static HTML: there
is no build step at deployment. Fonts, CSS and JavaScript are self-hosted, apart
from Simple Analytics through the `api.ghuntley.com` proxy.

- `index.html`, `architecture.html`, `self-host/*.html`, `404.html`: pages
- `assets/css/site.css`: the Monospace Web theme (four colour tokens per theme)
- `assets/js/site.js`: optional appearance switch and copy buttons
- `assets/fonts/`: JetBrains Mono, self-hosted

- `tools/site/`: the Python generator that writes the HTML (see its README)
- `.claude/skills/overalls-design/`: the Overalls brand pack and style guide, as a Claude Code skill

Edit the generators in `tools/site/`, then rebuild and check the result:

```sh
python3 -I tools/site/build.py .
python3 -I tools/site/check.py .
```

Application references point at the `trunk` branch of
[`ghuntley/overalls`](https://github.com/ghuntley/overalls/tree/trunk).
This website publishes directly from `main`.

Preview locally with `python3 -m http.server 8080` and open http://localhost:8080.
See `NOTICE.md` for third-party licences.
