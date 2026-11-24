[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/rardiyansyah004-blip/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/rardiyansyah004-blip/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# Tuesday 24 November 2026 — The World in One Day

Entry for the make.fun bounty **"Sum up 24 November's world news in one image"** (`news-image-20261124`, $100 USDC, 50 places). Built for [make.fun](https://make.fun/bounty/news-image-20261124) — join with referral code `g75rgwrg`.

## The image

A 1024×1024 front page, drawn with Pillow, with **45
dated stories across 7 regions** — Europe 12, Asia-Pacific 9,
North America 6, Middle East 8, Africa 4, Latin America 3, Sport &
Science 3 — every one dated Tuesday, 24 November 2026 and carrying a source:

- **Masthead** "TUESDAY, 24 NOVEMBER 2026" + "45 STORIES · 7 REGIONS · EVERY ONE DATED TUESDAY, 24 NOVEMBER 2026"
- **Numbers strip:** 14 nations back the ICJ ruling · 3 tankers hit in Hormuz · Nasdaq +6.51% · 700,000 Russian dead (leak) · 5,303 migrants to return · $41bn Sanofi buys Insmed
- **Region bar** (counts sum to 45) and a **UTC timeline** (first-reported times, 00:30–05:54 UTC)
- **3 lead cards:** Myanmar's generals sanctioned after the ICJ genocide ruling; three tankers ablaze in the Strait of Hormuz; Nvidia reinstates Jensen Huang
- **2 more photo stories:** Gaza — 77 years of human development undone; Indonesia picks its next vice president
- **10 medium cards** with status tags (ONGOING / CLAIM / REPORTED) and a source per story
- **World map** with 13 numbered pins
- **"ALSO ON TUESDAY, 24 NOVEMBER — 30 MORE STORIES"**, source per row
- **DATE CHECK box** addressed to the judge: wires read to 13:00 UTC, plus the wrong-day news deliberately left out (the ICJ ruling itself of 19 Nov, COP31's collapse of 23 Nov, the Dymer rescue of 23 Nov, the El Chapo capture of the weekend, the Banten fire of 22 Nov, the Peru quake of 20 Nov, the Shenzhen summit of 19–20 Nov)

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

`main.ts` (Node 22, standard library only) copies `entry.png` byte for byte to the output directory and refuses anything that is not a PNG of at most 1 MiB and 1024×1024. No network, no randomness, no clock. The page itself was built with Pillow from the 45 stories and five photographs listed above.
