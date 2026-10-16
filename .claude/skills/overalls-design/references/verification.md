# Verification

Run these before calling any change done.

## 1. Rebuild and check

```sh
python3 -I tools/site/build.py .
python3 -I tools/site/check.py .
```

`check.py` (also in `../scripts/check.py`) checks three things:
- Every relative `href` and `src` resolves, including `#anchors`.
- Nothing in `link`, `script` or `img` loads from another origin.
- There are no colour literals in `site.css` outside the token and print blocks.

It also prints the list of external links. Check every GitHub link against the source repo:

```sh
git -C ~/src/kittens cat-file -e origin/main:docs/nixos.md && echo ok
```

## 2. HTML validity

```sh
for f in *.html self-host/*.html; do
  nix shell nixpkgs#html-tidy -c tidy -q -e "$f" 2>&1 \
    | grep -v "trimming empty\|proprietary attribute\|<dd>\|<dt>\|<dl>\|</dl>\|</div>\|<div>"
done
```

The filters drop tidy's false positives on `<div>` inside `<dl>`, which is valid HTML5. Anything
left is real, usually an unescaped `<placeholder>` in a `pre`.

## 3. Screenshots, then look at them

Port 8080 is taken on this machine, so use 8731:

```sh
python3 -m http.server 8731 --bind 127.0.0.1 & SERVER=$!
CH=$(nix shell nixpkgs#chromium -c sh -c 'command -v chromium')
shot() { $CH --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --virtual-time-budget=3000 $3 --window-size=$2 --screenshot=$SCRATCH/$1.png "$4"; }
shot light   1280,4000 ""                 http://127.0.0.1:8731/index.html
shot dark    1280,4000 --force-dark-mode  http://127.0.0.1:8731/index.html
shot mobile  390,3000  ""                 http://127.0.0.1:8731/index.html
shot hero2x  1280,600  --force-device-scale-factor=2 http://127.0.0.1:8731/index.html
kill $SERVER   # not pkill -f: it matches this shell's own command line and kills it
```

- `--virtual-time-budget` prevents blank captures.
- Save screenshots to the session scratchpad, never into the repo.

What to look for:
- Box drawing joins up, with no gaps between lines.
- Headings wrap without leaving one word alone on the last line.
- On mobile, the header stacks into labelled lines, the mark sits centred above the h1, and the page
  never scrolls sideways.
- Status labels read correctly in both themes.

## 4. Publish

```sh
git add -A && git commit -m "…" && git push
for i in $(seq 1 15); do sleep 10; curl -s https://ghuntley.dev/ | grep -q "NEW TEXT" && { echo live; break; }; done
```

GitHub Pages serves `main` at the repo root, with the custom domain in `CNAME` and HTTPS enforced.
