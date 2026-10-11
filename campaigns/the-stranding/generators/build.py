"""Build every place's program (or the ones named): python3 generators/build.py [node ...]."""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import places_town  # noqa: E402

BUILDERS = {}
for mod in (places_town,):
    BUILDERS.update(mod.BUILDERS)


def main(argv):
    names = argv or sorted(BUILDERS)
    for n in names:
        if not n.startswith("node/"):
            n = "node/" + n
        path = BUILDERS[n](n)
        print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1:])
