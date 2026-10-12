"""Build every place's program (or the ones named): python3 generators/build.py [node ...]."""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import places_town  # noqa: E402
import places_flat  # noqa: E402
import places_body  # noqa: E402

BUILDERS = {}
for mod in (places_town, places_flat, places_body):
    BUILDERS.update(mod.BUILDERS)


def main(argv):
    # node/sea-skiff is reached only by a carry and cannot be detailed (see
    # GENERATION.md); its builder is kept, its program is not written by default
    names = argv or sorted(n for n in BUILDERS if n != "node/sea-skiff")
    for n in names:
        if not n.startswith("node/"):
            n = "node/" + n
        path = BUILDERS[n](n)
        print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1:])
