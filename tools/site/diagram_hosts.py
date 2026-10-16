W, H = 82, 19
g = [[" "] * W for _ in range(H)]
def put(r, c, s):
    for i, ch in enumerate(s): g[r][c + i] = ch
def box(r, c, w, h):
    put(r, c, "┌" + "─" * (w - 2) + "┐")
    for k in range(1, h - 1): put(r + k, c, "│"); put(r + k, c + w - 1, "│")
    put(r + h - 1, c, "└" + "─" * (w - 2) + "┘")
BW, GAP, X0 = 22, 6, 1
hosts = [X0 + i * (BW + GAP) for i in range(3)]
mid = [x + BW // 2 for x in hosts]
# Marshall, centred over the middle host
MW = 17; mx = mid[1] - MW // 2
box(0, mx, MW, 4); put(1, mx + 5, "Marshall"); put(2, mx + 2, "control plane")
put(0, mx + MW + 1, "◀──▶ PostgreSQL")
left = "browser ─HTTPS─▶ proxy ─"; put(1, mx - len(left) - 2, left + "▶")
left = "ssh ──manage──▶ Porsche ─"; put(2, mx - len(left) - 2, left + "▶")
put(3, mid[1], "▲")
put(4, mid[1] - 15, "HTTPS, dialled out by every host")
# fan-out bar to hosts
put(5, mid[0], "┌" + "─" * (mid[2] - mid[0] - 1) + "┐"); put(5, mid[1], "┼")
for i, x in enumerate(hosts):
    box(6, x, BW, 7)
    put(6, mid[i], "┴")
    put(7, x + 2, ["Lilly · host 1", "Lilly · host 2", "Lilly · host N"][i])
    n = [3, 2, 3][i]
    for j in range(n):
        vx = x + 2 + j * 6
        put(8, vx, "┌────┐"[:6]); put(9, vx, "│ vm │"); put(10, vx, "└────┘")
    put(11, x + 2, "Firecracker · ZFS")
    put(12, mid[i], "▲")
put(9, hosts[1] + BW + 1, " ·· ")
# Audi routing bar under hosts
put(13, mid[0], "└" + "─" * (mid[2] - mid[0] - 1) + "┘"); put(13, mid[1], "┬")
put(14, mid[1], "│")
tail = "▶ Audi ───┘"; start = mid[1] - len(tail) + 1
put(15, 0, "ssh · web " + "─" * (start - 10)); put(15, start, tail)
put(15, mid[1] + 3, "routes each request to the")
put(16, mid[1] + 3, "host running that guest")
rows = ["".join(r).rstrip() for r in g]
while rows and not rows[-1]: rows.pop()
print("\n".join(rows))
