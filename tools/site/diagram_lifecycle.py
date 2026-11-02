"""Persistent machine identity across power and lifecycle operations."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / ".claude/skills/overalls-design/scripts"))
from canvas import Canvas

c = Canvas(84, 10)
flow = "new ─▶ [pending] ─▶ [running] ◀── start ─── [stopped]"
START = 2
c.put(0, START, flow)
running = START + flow.index("[running]") + len("[running]") // 2
stopped = START + flow.index("[stopped]") + len("[stopped]") // 2
c.put(1, running + 3, "│")
c.put(1, stopped, "▲")
c.hline(2, running + 3, stopped - running - 2, start="└", end="┤")
c.put(2, running + 10, " stop ")
c.vline(1, running, 3)
c.vline(3, stopped, 1)
c.hline(4, running, stopped - running + 1, start="└", end="┘")
operations = running + 8
c.put(4, operations, "┬")
for row, text in enumerate([
    "relocate ─▶ another host",
    "clone ────▶ new private identity and disk",
    "resize ───▶ CPU, memory and disk size",
    "rm ───────▶ disk deleted",
], 5):
    c.put(row, operations, ("└─ " if row == 8 else "├─ ") + text)
print(c.render())
