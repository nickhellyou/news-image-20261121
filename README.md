# The World in One Day

[![badge](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/nickhellyou/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/nickhellyou/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image that sums up the world's news on 21 November 2026. Forty stories
from that single day, laid out as a dense newspaper front page: COP31 running
into overtime, Wall Street's AI sell-off, BepiColombo arriving at Mercury, a
6.8 quake in Peru, the UK-EU deal, Gen Z marching across Europe, and the
numbers of the day, all in one frame. A stranger could look at this picture
for a minute and walk away knowing what the world talked about on that date.

Built for the make.fun bounty
[Sum up 21 November's world news in one image](https://make.fun/bounty/news-image-20261121).

## What is in this repo

- `entry.png` — the finished image (176,704 bytes).
- `main.py` — a small Python 3 program (standard library only) that checks
  the artwork (PNG magic bytes, 1 MiB cap) and copies it to the output
  directory, then verifies the copy by hash.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```
