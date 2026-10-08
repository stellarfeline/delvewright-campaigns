# The Touched Clerk

The demo level for **a span of text that carries a style** (spec-0096): a
`[[<styles>|<text>]]` span inside a player-facing line, lowered to a vanilla
text component, and kept through the Chinese transcreation.

The level is a campaign, so it lives where every campaign lives:

    campaigns/the-touched-clerk/

Its one piece, `prefab/counting-room`, is in the prefab library
(`prefabs/counting-room.{nbt,json}`) and is expanded from the grammar program
`campaigns/the-touched-clerk/design/programs/counting-room.json` (13 × 6 × 11,
seed 1, named in `zones.json` beside it).

## What it is

The counting-room of a wool merchant's house: stone-brick walls, a spruce
floor, a dark-oak ceiling on two beams with four lanterns hanging from them.
Shelves of ledgers stand either side of a window. The clerk's long desk crosses
the room, with a lantern at each end. Barrels of stock are stacked against one
wall, a second window lights the other, and the iron door is shut. You arrive
just inside the door, facing the desk.

The clerk, Tobin Hale, stands behind the desk. Every morning there is a new line
at the foot of his ledger, in his handwriting, and he did not write it. He has
put the ledger in the chest under the window. He gives you the key and asks you
to lock it in, and to keep the key overnight.

## The three spans

| Where | The English | The zh-cn row |
| --- | --- | --- |
| His second bark, after he hands over the key | `The ledger is kept by [[obfuscated\|someone else]] at night.` | `账本到了夜里，就换[[obfuscated\|别的什么人]]来记。` |
| His dialogue, *What does it say?* | `"This morning it says [[color=dark_red\|Paid in full. Nothing more is owed.]] I keep only black ink in this room, and nobody has paid us anything."` | `"今天早上写的是[[color=dark_red\|已结清，再无欠款。]]我这屋里只备黑墨水。再说，根本没人付过我们一分钱。"` |
| The second objective's title | `Lock the [[bold\|ledger]] in the chest` | `把[[bold\|账本]]锁进箱子` |

Each span is its own translated component under the line's key plus
`.span.<i>`. The style rides on the component, never in the language file:

```
en_us  cast.lock-it-away.clerk.0.bark.1        = The ledger is kept by %1$s at night.
en_us  cast.lock-it-away.clerk.0.bark.1.span.0 = someone else
zh_cn  cast.lock-it-away.clerk.0.bark.1        = 账本到了夜里，就换%1$s来记。
zh_cn  cast.lock-it-away.clerk.0.bark.1.span.0 = 别的什么人
```

`bark_clerk_2` (the bark function of the second quest) holds three rungs, and
the styled line is the second. Its `tellraw` carries
`"with":[{"obfuscated":true,…"translate":"….bark.1.span.0"}]` under the italic
bark.

The zh-cn sidecar was transcreated by the engine's translation tool, then seven
rows were rewritten by hand. The obfuscated bark had used 保管 (to hold in
custody), which is the wrong sense of "kept". 账房 had named both the room and
the clerk, so the clerk is now 账房先生. The title's 被触碰 was a word-for-word
calque of "touched" and is now 撞了邪.

## What to look for

Walk it twice: once with the client in English, once in 简体中文.

1. At the spawn, look round the room. Does it read as a counting-room, a place
   where a clerk keeps a merchant's books?
2. Right-click Tobin and ask *What does it say?* Is the quoted line in dark
   red, and only that line? In Chinese, does the red start and stop where the
   sentence puts the quote?
3. Ask *What do you need?*, then *Give me the key.* You get a Chest Key. The
   new objective is announced as **Lock the ledger in the chest**. Does the bold
   *ledger* read as the name of a thing, or as the game raising its voice? The
   writing rule allows a style only for a fact about the text itself, and a
   bold word in an objective title has no reading under that rule. This one is
   here because the row asks for it, and it is the one to judge.
4. Before you lock the chest, right-click Tobin three times. The second line's
   *someone else* (Chinese: *别的什么人*) is drawn as shifting glyphs. Does it
   read as a mind something has been in, or as a rendering fault? In Chinese,
   does the blur sit on the phrase the sentence puts it on?
5. Right-click the chest under the window with the key in your hand. The delve
   completes.
6. Decline the resource-pack prompt once and walk it again in English. The
   English fallback should still show every span styled: the red quote, the
   bold word and the blur.

## The refusals

The same campaign with one edit each, run through `delvec validate`. The
transcripts are verbatim. Each exits 1.

**A span left open** (`a-span-left-open.txt`): the bark with its closing `]]`
removed. The refusal names the line by its key and the character the span
opens at:

```
DW0975 [error] l10n #/cast.lock-it-away.clerk.0.bark.1: player-visible string `cast.lock-it-away.clerk.0.bark.1` has malformed style markup at character 22: `[[` opens a span that is never closed with `]]` — …
```

`DW0187` follows it, because the zh-cn row was transcreated from the line
before the edit.

**A translation that loses its blur** (`a-translation-that-loses-its-blur.txt`):
the zh-cn row of that bark with its obfuscated span dropped. The refusal names
both lines' spans:

```
DW0976 [error] l10n l10n/zh-cn.json#/content/cast.lock-it-away.clerk.0.bark.1: `zh-cn` row `cast.lock-it-away.clerk.0.bark.1` does not carry the English's styled spans: the English carries span(s) [obfuscated] and the translation []. …
```

## The ladder

Built with an engine that carries spec-0096, which no released engine does yet:

- `delvec validate`, `delvec analyze`, `delvec build`: exit 0. The
  inline-style binding reports 3 of 25 player-facing lines carrying 3 spans,
  and 25 sidecar rows held to their English's spans. Two builds are identical
  (106 files).
- PackTest (`validation/packtest-run.sh`): all 22 required tests passed, 0 live
  bootstrap fetches.
- Bot critical path (`validation/bot-run.sh`): passed, 4 steps. die-retry and
  death-loop did not run, because the level has no combat and no death.
- Staging gate (`tools/creator/staging-gate.py`): **refused**, 2 of 122
  findings unbound, both for the same reason: the campaign has no design
  record (`drill3-01`, `drill3-03`). The other 120 are 24 bound, 25 declared
  uncoverable and 71 inapplicable. Clearing it needs an approved concept
  picture in `design.json` and a camera in `design/cameras.json` that answers
  it.

## What this level does not show

The room has no way in: the party arrives inside and the iron door stays shut.
So the piece declares no spatial contract, and the light probe has no grade
entrance to measure from. Its lighting profile is `unmeasured`. The light comes
from six lanterns and two windows.
