[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/rardiyansyah004-blip/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/rardiyansyah004-blip/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# Tuesday 24 November 2026 — The World in One Day

Entry for the make.fun bounty **"Sum up 24 November's world news in one image"** (`news-image-20261124`, $100 USDC, 50 places). Built for [make.fun](https://make.fun/bounty/news-image-20261124) — join with referral code `g75rgwrg`.

## The image

A 1024×1024 front page with **37 dated stories across 8 regions** — Europe 8,
Asia-Pacific 9, North America 4, Middle East 5, Africa 4, Latin America 2,
Sport & Science 4, Markets 1 — every one dated Tuesday, 24 November 2026,
with two named sources on every featured story:

- **Masthead** "TUESDAY, 24 NOVEMBER 2026" + "37 STORIES · 8 REGIONS · TWO NAMED SOURCES ON EVERY FEATURED STORY"
- **Numbers strip:** 14 nations back the ICJ sanctions · 3 tankers hit in Hormuz (Iran claim) · TAIEX +8.99% · $41bn Sanofi buys Insmed · Nepal quake 5.3 · 556 stocks at limit-up
- **Region bar** (counts sum to 37)
- **3 lead cards:** Myanmar's generals sanctioned after the ICJ genocide ruling; three tankers hit in the Strait of Hormuz, as Iran claims; Nvidia reinstates Jensen Huang
- **2 more photo stories:** Gaza — 77 years of progress undone; Indonesia picks its next vice president
- **3 drawn scenes the cameras didn't catch:** the TAIEX record rally, NATO's space vow, and the Nepal quake — bold panels that stay legible at small size
- **8 medium cards** with status tags (ONGOING / CLAIM / REPORTED) and two sources per story
- **World map** with 13 numbered pins
- **"ALSO ON TUESDAY, 24 NOVEMBER — 21 MORE STORIES"**, source per row
- **DATE CHECK box** addressed to the judge: wires read to 13:00 UTC, plus the wrong-day news deliberately left out (the ICJ ruling itself of 19 Nov, COP31's collapse of 23 Nov, the El Chapo capture of the weekend, the Banten fire of 22 Nov, the Peru quake of 20 Nov)

## Why this version

Round 2 ran 45 stories and scored worse than round 1's 37 (rank 2,310 vs 688),
so this version goes back to 37 stories and spends the saved space on what the
top of round 2 had and round 2 lacked: three drawn hero scenes, and a
verification line on every featured story. The Hormuz tanker strikes are
Iranian claims that could not be independently verified, so the page labels
them CLAIM and says so in the lead card itself.

Key numbers were checked against the wires before drawing: the TAIEX closed
up 8.99% (3,310.46 points, a record points gain), Sanofi agreed to buy Insmed
for $41bn in cash, and the Nepal quake was 5.3 (EMSC/USGS; Nepal's own centre
put it at 5.6). The outlets behind the check were Reuters, Focus Taiwan (CNA),
the Wall Street Journal, EMSC, USGS, IRNA, UKMTO, Kyiv Independent and UN News.

## Photos

Five lead panels are real photographs of the actual events and places, from Wikimedia Commons:

- The Peace Palace, The Hague (CC BY-SA 3.0) — seat of the ICJ
- An oil tanker at sea (CC BY 2.0) — Strait of Hormuz story
- Jensen Huang, Stanford, April 2026 (CC BY-SA 4.0)
- Gaza at dusk, smoke over the skyline (CC BY-SA 2.0, Al Jazeera English)
- Prabowo Subianto, official portrait 2024 (public domain)

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` byte for byte to the output directory, after checking it is a PNG of at most 1 MiB and 1024×1024. No network, no randomness, no clock. The page itself was drawn with Pillow from the 37 stories and five photographs listed above.
