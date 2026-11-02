"""Guest traffic reaches the reviewed egress, inference and integration services."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / ".claude/skills/overalls-design/scripts"))
from canvas import Canvas

c = Canvas(84, 7)
LEFT, WIDTH = 2, 39
RIGHT = LEFT + WIDTH - 1
c.box(0, LEFT, WIDTH, 5, title="guest")
routes = [
    ("apt · nix · pip · npm", "Brady · proxy and cache ─▶ internet"),
    ("https://llm.internal", "Ziggy ─▶ OpenAI, Anthropic"),
    ("https://x.integration.internal", "Galileo · adds credentials"),
]
for row, (source, destination) in enumerate(routes, 1):
    start = LEFT + 2
    c.put(row, start, source)
    c.hline(row, start + len(source) + 1, RIGHT - start - len(source))
    c.put(row, RIGHT, "┼──▶ " + destination)
c.put(6, LEFT, "platform credentials stay outside the guest; usage is recorded per account")
print(c.render())
