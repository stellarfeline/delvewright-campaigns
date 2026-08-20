"""Evaluate map.json's split tree to the box each zone is allocated.

An independent reading of the same program the engine expands: it walks the
`rules` the site plan actually declares, so a plan revision moves these boxes
without anything here being edited.
"""
import json

class Alloc:
    def __init__(self, prog, overrides=None):
        self.rules = prog['rules']
        self.params = dict(prog['params'])
        if overrides:
            self.params.update(overrides)
        self.boxes = {}      # symbol -> (origin, size) for every leaf that binds a zone
        self.nodes = []      # (symbol, origin, size)

    def ev(self, e, box):
        t = e['expr']
        if t == 'int':
            return e['value']
        if t == 'param':
            return self.params[e['name']]
        if t == 'dim':
            return box[1]['xyz'.index(e['dim'])]
        if t == 'arith':
            a, b = self.ev(e['lhs'], box), self.ev(e['rhs'], box)
            return {'add': a + b, 'sub': a - b,
                    'mul': a * b, 'div': a // b}[e['op']]
        raise ValueError(t)

    def cond(self, c, box):
        k = c['cond']
        if k == 'always':
            return True
        if k == 'all':
            return all(self.cond(x, box) for x in c['of'])
        if k == 'any':
            return any(self.cond(x, box) for x in c['of'])
        if k == 'cmp':
            a, b = self.ev(c['lhs'], box), self.ev(c['rhs'], box)
            return {'eq': a == b, 'ne': a != b, 'lt': a < b,
                    'le': a <= b, 'gt': a > b, 'ge': a >= b}[c['op']]
        raise ValueError(k)

    def call(self, sym, box):
        self.nodes.append((sym, box[0], box[1]))
        if sym not in self.rules:          # an included zone's own start symbol
            self.boxes[sym] = box
            return 'refused-or-zone'
        for prod in self.rules[sym]:
            if 'when' in prod and not self.cond(prod['when'], box):
                continue
            return self.op(prod['body'], box, sym)
        self.boxes[sym] = box              # no production applied: a refusal
        return 'refused'

    def op(self, b, box, sym):
        o = b['op']
        if o == 'call':
            return self.call(b['symbol'], box)
        if o == 'bind':
            return self.op(b['body'], box, sym)
        if o in ('fill', 'void'):
            return o
        if o == 'split':
            ax = 'xyz'.index(b['axis'])
            total = box[1][ax]
            sizes, rel = [], []
            for s in b['sizes']:
                if s['size'] == 'absolute':
                    sizes.append(self.ev(s['blocks'], box))
                else:
                    sizes.append(None)
                    rel.append(self.ev(s['weight'], box))
            fixed = sum(s for s in sizes if s is not None)
            left = total - fixed
            wsum = sum(rel) or 1
            it = iter(rel)
            for i, s in enumerate(sizes):
                if s is None:
                    sizes[i] = left * next(it) // wsum
            cur = box[0][ax]
            for s, ch in zip(sizes, b['children']):
                org = list(box[0]); org[ax] = cur
                siz = list(box[1]); siz[ax] = s
                self.op(ch, (tuple(org), tuple(siz)), sym)
                cur += s
            return 'split'
        raise ValueError(o)

def allocate(prog, region, overrides=None):
    a = Alloc(prog, overrides)
    a.call(prog['start'], ((0, 0, 0), tuple(region)))
    return a
