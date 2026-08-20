"""Measured-drawing primitives: a block grid, a scale bar, and a human body.

Everything here is drawn in BLOCKS and converted once, so no figure on any
sheet can be drawn at a scale other than the one its sheet declares.
"""

# One ink set for every sheet, so a colour means the same thing throughout.
PAPER = '#fbfaf7'
INK = '#23201c'
GREY = '#6b655c'
FAINT = '#9a938a'
GRID = '#e7e3d9'
GRID_MAJOR = '#cec7b6'
ALLOC = '#2f6f8f'          # a box the site plan hands out
ALLOC_FILL = '#eaf2f6'
PART = '#8a7a63'           # geometry the zone program actually builds
PART_FILL = '#d8cdb9'
OVER = '#b1372f'           # anything past the box it was given
SEA = '#bcd7e5'
BODY = '#17604a'           # a player
GOLD = '#a5762a'


class Sheet:
    """An SVG page whose only unit is the block."""

    def __init__(self, scale, width_px, height_px, title):
        self.s = scale
        self.w = width_px
        self.h = height_px
        self.title = title
        self.out = []

    # --- raw ---------------------------------------------------------------
    def raw(self, s):
        self.out.append(s)

    def rect(self, x, y, w, h, fill='none', stroke='none', sw=1, op=1,
             dash=None, rx=0):
        d = ' stroke-dasharray="%s"' % dash if dash else ''
        self.raw('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" '
                 'stroke="%s" stroke-width="%.2f" opacity="%.3f" rx="%.1f"%s/>'
                 % (x, y, w, h, fill, stroke, sw, op, rx, d))

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1, dash=None, op=1):
        d = ' stroke-dasharray="%s"' % dash if dash else ''
        self.raw('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" '
                 'stroke-width="%.2f" opacity="%.3f"%s/>'
                 % (x1, y1, x2, y2, stroke, sw, op, d))

    def text(self, x, y, s, size=11, fill=INK, anchor='start', weight='normal',
             style='normal', op=1):
        self.raw('<text x="%.2f" y="%.2f" font-family="Helvetica Neue,Helvetica,'
                 'Arial,sans-serif" font-size="%.1f" fill="%s" text-anchor="%s" '
                 'font-weight="%s" font-style="%s" opacity="%.3f">%s</text>'
                 % (x, y, size, fill, anchor, weight, style, op, esc(s)))

    def poly(self, pts, fill='none', stroke=INK, sw=1, dash=None, op=1):
        d = ' stroke-dasharray="%s"' % dash if dash else ''
        p = ' '.join('%.2f,%.2f' % q for q in pts)
        self.raw('<polyline points="%s" fill="%s" stroke="%s" stroke-width="%.2f"'
                 ' opacity="%.3f"%s/>' % (p, fill, stroke, sw, op, d))

    # --- furniture ---------------------------------------------------------
    def grid(self, ox, oy, w_blocks, h_blocks, step=10, major=50, flip_y=False):
        """A block grid over a box whose top-left pixel is (ox, oy)."""
        s = self.s
        for i in range(0, w_blocks + 1, step):
            c = GRID_MAJOR if i % major == 0 else GRID
            self.line(ox + i * s, oy, ox + i * s, oy + h_blocks * s, c, 1)
        for j in range(0, h_blocks + 1, step):
            c = GRID_MAJOR if j % major == 0 else GRID
            self.line(ox, oy + j * s, ox + w_blocks * s, oy + j * s, c, 1)

    def scalebar(self, x, y, blocks=50, label=None):
        """The ruler. Every sheet carries one; without it nothing here is a
        measurement."""
        s = self.s
        self.line(x, y, x + blocks * s, y, INK, 1.6)
        for i in range(0, blocks + 1, 10):
            self.line(x + i * s, y - 4, x + i * s, y + 4, INK, 1.2)
        for i in range(0, blocks, 20):
            self.rect(x + i * s, y - 3, 10 * s, 3, INK, 'none')
        self.text(x, y + 15, '0', 9, GREY, 'middle')
        self.text(x + blocks * s, y + 15, str(blocks), 9, GREY, 'middle')
        self.text(x + blocks * s / 2, y - 9,
                  label or '%d blocks  ·  1 block = 1 m' % blocks,
                  9, GREY, 'middle')

    def north(self, x, y, r=13):
        self.line(x, y + r, x, y - r, INK, 1.4)
        self.poly([(x - 4, y - r + 6), (x, y - r), (x + 4, y - r + 6)],
                  fill=INK, stroke=INK, sw=1)
        self.text(x, y - r - 5, 'N', 10, INK, 'middle', 'bold')

    # --- a person ----------------------------------------------------------
    def body_elev(self, x_px, ground_px, colour=BODY, op=1.0):
        """A standing player in elevation or section: 1 block wide, 2 tall."""
        s = self.s
        h = 2 * s
        cx = x_px + s / 2
        self.raw('<g opacity="%.3f">' % op)
        self.raw('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>'
                 % (cx, ground_px - h + s * 0.30, s * 0.30, colour))
        self.rect(x_px + s * 0.18, ground_px - h + s * 0.62, s * 0.64,
                  h - s * 0.62, colour, 'none', 0, 1, rx=s * 0.14)
        self.raw('</g>')

    def body_plan(self, x_px, y_px, colour=BODY, op=1.0):
        """A player seen from above: the 1x1 cell a body stands in."""
        s = self.s
        self.raw('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" '
                 'opacity="%.3f"/>' % (x_px + s / 2, y_px + s / 2,
                                       s * 0.34, colour, op))

    def party_plan(self, x_px, y_px, colour=BODY):
        """The four players a delve is built for, shoulder to shoulder."""
        for i in range(4):
            self.body_plan(x_px + i * self.s, y_px, colour)

    def party_elev(self, x_px, ground_px, colour=BODY):
        for i in range(4):
            self.body_elev(x_px + i * self.s, ground_px, colour)

    # --- output ------------------------------------------------------------
    def render(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
                'viewBox="0 0 %d %d">\n<title>%s</title>\n'
                '<rect width="%d" height="%d" fill="%s"/>\n%s\n</svg>\n'
                % (self.w, self.h, self.w, self.h, esc(self.title),
                   self.w, self.h, PAPER, '\n'.join(self.out)))

    def write(self, path):
        with open(path, 'w') as f:
            f.write(self.render())


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;'))


def runs(row):
    """Horizontal runs of set cells in a mask row: '..##.#' -> [(2,2),(5,1)]."""
    out, i, n = [], 0, len(row)
    while i < n:
        if row[i] == '#':
            j = i
            while j < n and row[j] == '#':
                j += 1
            out.append((i, j - i))
            i = j
        else:
            i += 1
    return out
