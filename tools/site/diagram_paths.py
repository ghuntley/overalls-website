"""Two paths to a machine: the web interface via the control plane, SSH direct."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / ".claude/skills/overalls-design/scripts"))
from canvas import Canvas

c = Canvas(84, 13)
DX, DW = 1, 27          # developer box
HX, HW = 54, 30         # host box
dmid, hmid = DX + DW // 2, HX + HW // 2
c.box(0, 6, 72, 3, title="control plane · one region")
c.put(1, 9, "HAProxy ─▶ Marshall · Marshall · Marshall ◀─▶ PostgreSQL")
c.put(2, dmid, "▲")
c.put(2, hmid, "▲")
for r in (3, 4, 5):
    c.put(r, dmid, "│")
    c.put(r, hmid, "│")
c.put(3, dmid + 2, "web terminal and")
c.put(4, dmid + 2, "browser editor")
c.put(3, hmid - 2 - len("relay over HTTPS,"), "relay over HTTPS,")
c.put(4, hmid - 2 - len("dialled out by Lilly"), "dialled out by Lilly")
c.box(6, DX, DW, 6)
c.put(6, dmid, "┴")
c.box(6, HX, HW, 6)
c.put(6, hmid, "┴")
c.put(7, DX + 2, "DEVELOPER IN SINGAPORE")
c.put(8, DX + 2, "browser")
c.put(9, DX + 2, "ssh, VS Code,")
c.put(10, DX + 2, "shared web apps")
c.put(7, HX + 2, "HOST IN SINGAPORE")
c.put(10, HX + 2, "Audi ─▶ Lilly ─▶ guest")
c.put(9, DX + DW + 3, "direct, same region")
c.put(10, DX + 18, "─" * (DW - 19))
c.put(10, DX + DW - 1, "┼" + "─" * (HX - DX - DW))
c.put(10, HX - 1, "▶")
c.put(10, HX, "│")
print(c.render())
