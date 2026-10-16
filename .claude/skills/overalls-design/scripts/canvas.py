"""Character canvas for Overalls box-drawing diagrams.

Draw by coordinates, never by hand-aligning strings. Usage:

    from canvas import Canvas
    c = Canvas(84, 20)
    c.box(0, 10, 30, 5, title="control plane")
    c.put(2, 13, "Marshall ◀─▶ PostgreSQL")
    c.hline(9, 12, 70)            # ─ run, use c.put to drop ┬ ┴ ┼ junctions on it
    c.vline(10, 40, 3, end="▲")   # │ run with an arrowhead at the bottom
    print(c.render())

Later writes overwrite earlier ones, so draw boxes first, then junctions,
arrowheads and labels. Run `python3 -I canvas.py` for a demo.
"""


class Canvas:
    def __init__(self, width, height):
        self.w, self.h = width, height
        self.g = [[" "] * width for _ in range(height)]

    def put(self, row, col, text):
        for i, ch in enumerate(text):
            if not (0 <= row < self.h and 0 <= col + i < self.w):
                raise ValueError(f"write outside canvas at row {row}, col {col + i}: {text!r}")
            self.g[row][col + i] = ch

    def box(self, row, col, width, height, title=None):
        top = "┌" + "─" * (width - 2) + "┐"
        if title:
            top = "┌─ " + title + " " + "─" * (width - 5 - len(title)) + "┐"
        self.put(row, col, top)
        for k in range(1, height - 1):
            self.put(row + k, col, "│")
            self.put(row + k, col + width - 1, "│")
        self.put(row + height - 1, col, "└" + "─" * (width - 2) + "┘")

    def hline(self, row, col, length, start="─", end="─"):
        self.put(row, col, start + "─" * (length - 2) + end)

    def vline(self, row, col, length, end="│"):
        for k in range(length - 1):
            self.put(row + k, col, "│")
        self.put(row + length - 1, col, end)

    def centre(self, row, mid, text):
        self.put(row, mid - len(text) // 2, text)

    def render(self):
        rows = ["".join(r).rstrip() for r in self.g]
        while rows and not rows[-1]:
            rows.pop()
        width = max(len(r) for r in rows)
        if width > 88:
            raise ValueError(f"diagram is {width} columns; keep it at 88 or less so it fits the 100ch page")
        return "\n".join(rows)


if __name__ == "__main__":
    # Derive every coordinate from box positions so connectors always line up.
    BW, GAP, X0 = 15, 3, 4
    xs = [X0 + i * (BW + GAP) for i in range(3)]
    mids = [x + BW // 2 for x in xs]
    c = Canvas(60, 12)
    c.box(0, mids[1] - 11, 23, 4)
    c.centre(1, mids[1], "Marshall")
    c.centre(2, mids[1], "control plane")
    c.put(3, mids[1], "┬")
    c.vline(4, mids[1], 2, end="│")
    c.put(4, mids[1], "▲")
    c.hline(6, mids[0], mids[2] - mids[0] + 1, start="┌", end="┐")
    c.put(6, mids[1], "┼")
    for x, m in zip(xs, mids):
        c.box(7, x, BW, 4)
        c.put(7, m, "┴")
        c.put(8, x + 2, "Lilly")
        c.put(9, x + 2, "vm  vm  vm")
    print(c.render())
