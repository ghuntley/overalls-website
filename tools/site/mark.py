"""The two-kittens-in-overalls mark, drawn on the character canvas so every
ear, strap and seam lines up. Run it and paste the output into MARK in layout.py."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / ".claude/skills/overalls-design/scripts"))
from canvas import Canvas

c = Canvas(40, 18)
HW = 13                       # head width, odd so the nose has a centre column
heads = [2, 16]               # left wall of each head
for L in heads:
    R = L + HW - 1
    c.put(0, L + 2, "╱╲"); c.put(0, R - 3, "╱╲")                  # ear tips
    c.put(1, L + 1, "╱"); c.put(1, L + 4, "╲")                    # ear bases
    c.put(1, L + 5, "─" * (R - L - 9)); c.put(1, R - 4, "╱"); c.put(1, R - 1, "╲")
    for row in (2, 3, 4):
        c.put(row, L, "│"); c.put(row, R, "│")
    c.put(2, L + 3, "●"); c.put(2, R - 3, "●")                    # eyes
    c.put(3, L + 2, "═"); c.put(3, R - 2, "═"); c.put(3, L + 6, "▾")
    c.put(4, L + 2, "═"); c.put(4, R - 2, "═"); c.put(4, L + 5, "╰┴╯")
    c.put(5, L + 1, "╲" + "─" * (HW - 4) + "╱")                   # chin
    c.put(5, L + 3, "┬"); c.put(5, R - 3, "┬")                    # straps under the eyes

BL, BR = heads[0], heads[1] + HW - 1                               # bib walls line up with the outer cheeks
mid = (BL + BR) // 2
c.put(6, BL, "┌" + "─" * (BR - BL - 1) + "┐")
for L in heads:
    c.put(6, L + 3, "■"); c.put(6, L + HW - 4, "■")              # button rivets under each strap
for row, pocket in ((7, "┌─────────┐"), (8, "├─────────┤"), (9, "└─────────┘")):
    c.put(row, BL, "│"); c.put(row, BR, "│"); c.centre(row, mid, pocket)
c.put(7, BL - 1, "╭┤"); c.put(7, BR, "├╮")                      # arms
c.put(8, BL - 1, "│"); c.put(8, BR + 1, "│")
c.put(9, BL - 1, "●"); c.put(9, BR + 1, "●")                    # paws

WL, WR = BL - 2, BR + 2                                            # waist is two columns wider each side
c.put(10, WL, "┌─" + "─" * (WR - WL - 3) + "─┐"); c.put(10, BL, "┴"); c.put(10, BR, "┴")
c.put(11, WL, "│■" + " " * (WR - WL - 3) + "■│")
for row in (12, 13, 14):
    c.put(row, WL, "│"); c.put(row, WR, "│")
c.put(12, mid - 2, "┌───┐")
for row in (13, 14):
    c.put(row, mid - 2, "│"); c.put(row, mid + 2, "│")
c.put(15, WL, "└" + "─" * (mid - 2 - WL - 1) + "┘   └" + "─" * (WR - mid - 3) + "┘")
c.put(12, WR + 4, "╭─╮"); c.put(13, WR + 4, "│ │")             # tail
c.put(14, WR, "├───╯ │"); c.put(15, WR, "┘─────╯")
c.centre(16, (WL + mid - 2) // 2, "╰──●─●──╯")                    # toe beans
c.centre(16, (mid + 2 + WR) // 2, "╰──●─●──╯")
print(c.render())
