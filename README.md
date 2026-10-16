# overalls.dev

The public website for [Overalls](https://github.com/ghuntley/overalls), the
self-hosted Firecracker dev-machine platform. It's flat static HTML served by GitHub
Pages: no build step and nothing loaded from other origins.

- `index.html`, `architecture.html`, `self-host/*.html`, `404.html`: pages
- `assets/css/site.css`: the Monospace Web theme (four colour tokens per theme)
- `assets/js/site.js`: optional appearance switch and copy buttons
- `assets/fonts/`: JetBrains Mono, self-hosted

- `tools/site/`: the Python generator that writes the HTML (see its README)
- `.claude/skills/overalls-design/`: the Overalls brand pack and style guide, as a Claude Code skill

Preview locally with `python3 -m http.server 8080` and open http://localhost:8080.
See `NOTICE.md` for third-party licences.
