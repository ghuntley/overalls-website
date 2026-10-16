W, H = 84, 22
g = [[" "] * W for _ in range(H)]
def put(r, c, s):
    for i, ch in enumerate(s): g[r][c + i] = ch
def box(r, c, w, h, title=None):
    top = "┌" + "─" * (w - 2) + "┐"
    if title: top = "┌─ " + title + " " + "─" * (w - 5 - len(title)) + "┐"
    put(r, c, top)
    for k in range(1, h - 1): put(r + k, c, "│"); put(r + k, c + w - 1, "│")
    put(r + h - 1, c, "└" + "─" * (w - 2) + "┘")
BW, GAP, X0 = 23, 6, 1
xs = [X0 + i * (BW + GAP) for i in range(3)]
mid = [x + BW // 2 for x in xs]
# control plane region box centred over the middle column
CW = 62; cx = mid[1] - CW // 2
box(0, cx, CW, 6, "control plane · one region")
put(2, cx + 3, "HAProxy ─▶ Marshall · Marshall · Marshall ◀─▶ PostgreSQL")
put(3, cx + 3, "several Marshall instances for high availability")
put(5, mid[1], "┬")
put(6, mid[1], "▲")
put(7, mid[1], "│  HTTPS, dialled out by every host")
put(8, mid[1], "│")
put(9, mid[0], "┌" + "─" * (mid[2] - mid[0] - 1) + "┐"); put(9, mid[1], "┼")
regions = [("Washington DC", "Lilly  Lilly  Lilly"), ("London", "Lilly  Lilly"), ("Singapore", "Lilly  Lilly")]
people = [("developers in", "the Americas"), ("developers in", "Europe"), ("developers in", "Asia-Pacific")]
for i, x in enumerate(xs):
    box(10, x, BW, 6)
    put(10, mid[i], "┴")
    put(11, x + 2, regions[i][0].upper())
    put(12, x + 2, regions[i][1])
    put(13, x + 2, "guests on ZFS")
    put(14, x + 2, "Audi: SSH, web apps")
    put(16, mid[i], "▲")
    put(17, mid[i] - len(people[i][0]) // 2, people[i][0])
    put(18, mid[i] - len(people[i][1]) // 2, people[i][1])
rows = ["".join(r).rstrip() for r in g]
while rows and not rows[-1]: rows.pop()
print("\n".join(rows))
