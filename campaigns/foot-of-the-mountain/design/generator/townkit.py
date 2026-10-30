"""The town kit is the skill's: every helper the lower street's generators
call is a general function of the starter's settlement module
(`$DELVEWRIGHT_SKILL/scripts/town.py`, re-exported by `starter.py`). This file
only names them for the generators that still `import townkit`; it holds no
implementation of its own.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import (AIR, HULL_ROLES, clip_beyond, clip_unwalled_edge, close_edge_gaps, hull,  # noqa: E402,F401
                     hull_on_stocks, loft, mast, pier, post_shed, slipway, street_front, street_seam,
                     water_step)
