# Strike Cup 🏆

**Fantasy trading on Strike.** Draft five real traders from Strike's copy-trading universe, and their actual 7-day returns become your score. Climb the leaderboard against other teams, golf-tournament style.

**Live demo:** https://strike-cup.onrender.com

Built for the first Strike Hackathon.

---

## Why

Copy trading asks people to risk money on traders they barely know. Strike Cup turns trader discovery into a game: you study traders, build a roster, and follow how they perform, with no money at risk. It gives anyone, including people who don't trade yet, a reason to browse Strike's traders every week, and gives good traders a new kind of visibility.

## How it works

1. **Draft.** Search Strike traders (and the Hyperliquid wallets Strike mirrors) with the same filters as Strike's Explore Traders page: platform, trading style, long/short bias, markets traded, profit, account size, volume, rank, copy score, max drawdown, and share of trading in Strike markets.
2. **Salary cap.** Every trader has a salary based on Strike's copy score ($4k–$15k). You get $50k for five picks, so you can't just take the top five.
3. **Score.** Each trader earns 10 points per 1% of 7-day return. Points are capped at ±500 per trader per week, and only accounts with $1k+ are draftable, so tiny accounts with meaningless percentages can't swing the league.
4. **Compete.** Name your team and see where you rank, with gold, silver, and bronze for the top three.

Drafted traders refresh from Strike every minute.

## Season format (launching soon)

The full Strike Cup format, shown in the promo video, is next on the build list:

- **Re-draft every week.** Pick five fresh traders each week. Rosters lock when the week starts, and each trader's return is measured from that moment, so everyone is scored over the same window.
- **Weekly Winners.** The top score each week takes the week.
- **4-week seasons.** Your four weekly scores add up, and the best total is crowned Season-Long Champion and lifts the Strike Cup.

Today's version is a live single-week game: the draft, filters, salary cap, scoring, and leaderboard all work with real Strike data, and the rival teams on the leaderboard are demo teams until shared leagues launch.

## Strike integration

Strike Cup uses Strike's public, read-only copy-trading API (no API key needed):

| Endpoint | Used for |
| --- | --- |
| `GET /v2/copy/discover` | Searching and filtering traders, with all filters passed through to Strike |
| `GET /v2/copy/discover/filters` | Checking the live connection |
| `GET /v2/copy/discover/{address}` | Refreshing drafted traders' returns |

Fields used include `roi` and `pnl` (1d/7d/30d/all), `account_value`, `volume`, `copy_score`, `style`, `bias`, `top_assets`, `pnl_curve_30d` (sparklines), and the drawdown from `copy_score_breakdown`.

## Run it yourself

Requires Python 3.8+ and nothing else (standard library only).

```
python strike_cup_server.py
```

Then open http://localhost:8000. The server serves the page and forwards requests to `https://api.strikefinance.org`. Set `STRIKE_API` to point at Strike's testnet, or `PORT` to change the port.

If the page is opened without the server, it falls back to sample traders in the same data format as Strike's API.

## Files

- `strike-cup.html`: the whole app (draft, team, leaderboard, scoring) in one page
- `strike_cup_server.py`: tiny server that serves the page and proxies Strike's public API

## Roadmap

- **Shared leagues:** save rosters in a database so real players compete on the same leaderboard
- **Season format:** weekly roster locks and re-drafts, Weekly Winners, and 4-week seasons with a Season-Long Champion
- **Wallet sign-in:** sign in with a Cardano wallet and show your Strike handle on the leaderboard
- **"Copy my roster":** one tap to follow your drafted traders on Strike
- **Prizes:** STRIKE token rewards for weekly winners
- **Live draft night:** captains draft in real time, snake-draft style

## Disclaimer

Strike Cup is a game for fun and is not financial advice. Past returns don't predict future results, and copy trading can lose money.
