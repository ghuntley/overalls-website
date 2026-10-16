"""Check an Overalls-style static site: local links and anchors resolve, nothing loads
from another origin, and site.css has no colour literals outside the tokens and print
blocks. Usage: python3 -I check.py SITE_ROOT
"""
import re, sys, pathlib, html.parser, urllib.parse
root = pathlib.Path(sys.argv[1]); bad = []; ext = set()
class P(html.parser.HTMLParser):
    def __init__(s): super().__init__(); s.refs=[]; s.ids=set()
    def handle_starttag(s, tag, a):
        a = dict(a)
        if 'id' in a: s.ids.add(a['id'])
        for k in ('href','src'):
            if k in a: s.refs.append((tag, k, a[k]))
pages = {}
def visible(path): return not any(part.startswith('.') for part in path.relative_to(root).parts)
for f in filter(visible, root.rglob('*.html')):
    p = P(); p.feed(f.read_text()); pages[f] = p
for f, p in pages.items():
    for tag, k, v in p.refs:
        if v.startswith(('http://','https://')):
            if tag in ('link','script','img'): bad.append(f'{f}: external resource {v}')
            ext.add(v); continue
        u = urllib.parse.urlparse(v)
        if f.name == '404.html' and v.startswith('/'): target = root / u.path.lstrip('/')
        elif not u.path: target = f
        else: target = (f.parent / u.path).resolve()
        if not target.exists(): bad.append(f'{f.relative_to(root)}: missing {v}')
        if u.fragment and target in pages and u.fragment not in pages[target].ids: bad.append(f'{f}: bad anchor {v}')
css_files = sorted(filter(visible, root.rglob('site.css')))
if not css_files: sys.exit('no site.css found under ' + str(root))
css = css_files[0].read_text()
body = css.split('/* ---- fonts')[1] if '/* ---- fonts' in css else css
for m in re.finditer(r'#[0-9a-fA-F]{3,6}\b|rgba?\(|hsl|color-mix', body):
    ctx = body[max(0,m.start()-200):m.start()]
    if '@media print' not in ctx: bad.append(f'colour literal: {m.group()}')
if re.search(r'url\(https?:|@import', css): bad.append('external css')
print('\n'.join(bad) or 'OK: no problems')
print(len(ext), 'external links:'); print('\n'.join(sorted(ext)))
