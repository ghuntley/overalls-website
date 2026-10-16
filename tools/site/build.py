import datetime, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pages_main as m, pages_guide as g, pages_security as sec

BASE = "https://overalls.dev/"

out = pathlib.Path(sys.argv[1])
files = {
    "index.html": m.landing(), "architecture.html": m.architecture(), "404.html": m.not_found(),
    "self-host/index.html": g.overview(), "self-host/provision.html": g.provision(),
    "self-host/deploy.html": g.deploy(), "self-host/enroll.html": g.enroll(),
    "self-host/first-machine.html": g.first_machine(), "self-host/operations.html": g.operations(),
    "security/index.html": sec.policy(), "security/hall-of-fame/index.html": sec.hall_of_fame(),
}


def url_for(name):
    # Directory indexes are published at their folder URL.
    return BASE + (name[: -len("index.html")] if name.endswith("index.html") else name)


# A page keeps its previous <lastmod> unless its HTML actually changed.
sitemap = out / "sitemap.xml"
previous = dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sitemap.read_text())) if sitemap.exists() else {}
today = datetime.date.today().isoformat()

entries = []
for name, html in files.items():
    path = out / name
    changed = not path.exists() or path.read_text() != html
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html)
    print(name, len(html))
    if name == "404.html":
        continue
    loc = url_for(name)
    lastmod = today if changed or loc not in previous else previous[loc]
    priority = "1.0" if name == "index.html" else "0.8" if name in ("architecture.html", "self-host/index.html") else "0.4" if name.startswith("security/") else "0.6"
    entries.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <priority>{priority}</priority>\n  </url>")

sitemap.write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(entries)
    + "\n</urlset>\n"
)
# security.txt (RFC 9116) at the well-known path, plus the legacy root copy.
(out / ".well-known").mkdir(exist_ok=True)
(out / ".well-known" / "security.txt").write_text(sec.security_txt())
(out / "security.txt").write_text(sec.security_txt())
(out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
print("sitemap.xml", len(entries), "urls")
