# claude-rc

## `/trading`: ein Skill für alles rund ums Trading

Die elf Skills aus dem Paket "trader-skill" (MIT, Jake Schincariol) sind hier
zu einem einzigen Projekt-Skill zusammengefasst: `.claude/skills/trading/`.

```
/trading                         Übersicht der Module
/trading copycat berkshire --top 5
/trading news AAPL KO
/trading budget 5000
/trading risk
/trading broker
```

Module: `copycat`, `news`, `budget`, `pelosi`, `analyst`, `screener`, `risk`,
`broker`, `tax`, `alerts`, `rebalance`. Jedes hat einen Leitfaden (`GUIDE.md`)
und ein Python-Werkzeug (nur Standardbibliothek, Python 3.8+). Man kann auch
einfach normal fragen ("Was hat Pelosi gekauft?"), der Skill wählt dann das
passende Modul.

Keine Anlageberatung. Keine Order ohne dein ausdrückliches Ja, Papierhandel ist
Standard. Daten landen im Ordner `trader/` (per `.gitignore` ausgeschlossen).

Global installieren statt nur für dieses Projekt:

```bash
cp -r .claude/skills/trading ~/.claude/skills/
```

Tests (offline):

```bash
python3 -m unittest discover -s tests
```
