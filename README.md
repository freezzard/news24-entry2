# The World in One Day — Tuesday 24 November 2026 · Broadsheet

[![make.fun](https://make.fun/badge.svg)](https://make.fun/c/news-image-20261124)
[![news-image-20261124](https://make.fun/c/news-image-20261124/badge.svg)](https://make.fun/c/news-image-20261124)
[![Built with make.fun](https://make.fun/built-with.svg)](https://make.fun)

A dense one-page newspaper digest of Tuesday 24 November 2026: 36 stories
(hero lead + 2 sub-leads + 33 wire briefs) from front pages across 20
countries — three tankers burn in the Strait of Hormuz, Huang apologises
as Nvidia slides, Kyiv is hit by drones, and the rest of the day in
numbers. Every story was verified against 24 November 2026 UTC reporting;
22–23 November carryovers (COP31, the Alcaraz final, the Riemann claim)
were excluded on purpose.

## How it works

`main.py` (Python 3 + Pillow, standard library plus Pillow only) draws the
whole image in code: it rasterises the masthead, lead story with a drawn
tanker scene, two illustrated sub-leads, a dotted world map with numbered
story pins, a UTC timeline, regional tallies, seven region wire groups and
a date-audit footer into an RGB buffer, and writes a deterministic
1024×1024 PNG to `/output/entry.png`. No network, no randomness, no clock
reads — two runs write byte-identical output.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Entry

- Competition: [news-image-20261124](https://make.fun/c/news-image-20261124)
  — "Sum up 24 November's world news in one image"
- Account: solo (@nanoy-solo)
- License: MIT
