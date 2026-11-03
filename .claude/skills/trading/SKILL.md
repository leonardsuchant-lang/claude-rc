---
name: trading
description: >-
  Trading-Komplettpaket in einem Skill: elf Module unter einem Befehl.
  copycat (13F eines Investors nachbauen, z. B. Buffett/Berkshire kopieren),
  news (Schlagzeilen und 8-K-Meldungen zu deinen Aktien), budget (Positionen
  auf dein Budget zuschneiden, Cash-Puffer, Obergrenze je Aktie), pelosi
  (Aktiengeschaefte von US-Kongressmitgliedern, House PTRs), analyst
  (Quartalszahlen aus SEC XBRL), screener (Aktien nach eigenen Regeln filtern),
  risk (jede Order gegen deine Limits pruefen), broker (genehmigte Order als
  Ticket fuer den Broker-Connector, nur nach deinem Ja), tax (Steuer-Lots,
  Tax-Loss-Harvesting, Wash Sales), alerts (Kursalarme, NYSE-Handelszeiten,
  Kurse holen) und rebalance (Portfolio zurueck auf Zielgewichte). Verwenden,
  wenn der Nutzer "/trading" schreibt oder etwas zu Aktien, Depot, Portfolio,
  13F, Buffett kopieren, Pelosi, Kongress-Trades, Nachrichten zu Aktien,
  Earnings, Screening, Order, Broker, Alpaca, Risiko, Steuer, Kursalarm,
  Marktoeffnung oder Rebalancing sagt.
argument-hint: "[modul] [argumente]  z. B. copycat berkshire --top 5"
---

# trading

Ein Skill, elf Module. Jedes Modul hat einen eigenen Leitfaden (`GUIDE.md`)
und ein Python-Werkzeug (nur Standardbibliothek, Python 3.8+) in seinem
Unterordner. `${CLAUDE_SKILL_DIR}` ist dieser Ordner (wo diese SKILL.md liegt).
Ist die Variable nicht gesetzt (z. B. in der Claude-App), setze sie selbst auf
diesen Ordner, etwa `export CLAUDE_SKILL_DIR=/mnt/skills/user/trading`, und
pruefe den Pfad vorher mit `ls`.

Antworte in der Sprache des Nutzers.

## So gehst du vor

1. **Modul bestimmen.** Ist das erste Argument ein Modulname (`copycat`,
   `news`, ...), nimm dieses Modul und reiche den Rest als Argumente weiter.
   Sonst waehle das Modul anhand der Anfrage aus der Tabelle unten. Ohne
   Argument und ohne erkennbare Absicht: zeige die Tabelle und frage, was der
   Nutzer tun moechte.
2. **Leitfaden lesen.** Lies `${CLAUDE_SKILL_DIR}/<modul>/GUIDE.md` vollstaendig,
   bevor du etwas ausfuehrst, und folge ihm. Lies nur die Leitfaeden, die du
   gerade brauchst.
3. **Weiterreichen.** Wo ein Leitfaden auf `/trading <modul>` verweist, ist
   damit das jeweilige Modul gemeint: lies dessen `GUIDE.md` und mach dort
   weiter, wenn der Nutzer das will.

| Modul | Aufgabe | Werkzeug |
| --- | --- | --- |
| `copycat` | Liest das 13F-HR eines Investors bei SEC EDGAR, baut das Portfolio als Gewichte nach, zeigt Kaeufe/Verkaeufe seit dem Vorquartal, schreibt `trader/targets.json` | `copycat/edgar13f.py` |
| `news` | Schlagzeilen und 8-K-Meldungen zu allen gehaltenen Aktien, nur Neues | `news/news.py` |
| `budget` | Teilt das Budget auf, Cash-Puffer, Obergrenze je Aktie, schreibt `trader/orders.json` als Vorschlaege | `budget/size.py` |
| `pelosi` | Liest die Aktiengeschaefte von Kongressmitgliedern (House PTRs), meldet jede neue Meldung einmal | `pelosi/ptr.py` |
| `analyst` | Umsatz, Gewinn, EPS, Margen und Wachstum aus den SEC-XBRL-Daten | `analyst/facts.py` |
| `screener` | Filtert Unternehmen nach eigenen Regeln und rankt die Treffer | `screener/screen.py` |
| `risk` | Prueft jede vorgeschlagene Order gegen die Limits: PASS oder BLOCK | `risk/check.py` |
| `broker` | Macht aus einer gepruefen Order das Ticket fuer den Broker-Connector und protokolliert das Ja | `broker/ticket.py` |
| `tax` | Steuer-Lots, Gewinne/Verluste, Tax-Loss-Harvesting, Wash Sales | `tax/lots.py` |
| `alerts` | Kursziele, Stops, Eroeffnungsglocke, NYSE-Kalender, schreibt `trader/prices.json` | `alerts/alerts.py` |
| `rebalance` | Bringt das Portfolio zurueck auf die Zielgewichte, wenn es aus dem Band laeuft | `rebalance/rebalance.py` |

## Ablaeufe

Alle Daten landen im Ordner `trader/` des Projekts, jedes Modul liest, was das
vorige geschrieben hat:

```
copycat -> budget -> risk -> broker            (Investor kopieren)
news / pelosi / alerts                          (beobachten, auch per Zeitplan)
analyst -> screener -> budget -> risk -> broker (selbst auswaehlen)
rebalance / tax -> risk -> broker               (pflegen)
```

Einstellungen: `trader/config.json` (Vorlage: `budget/config.example.json`).
SEC verlangt eine Absenderkennung: `"sec_user_agent": "Name email@example.com"`
in `trader/config.json` oder die Umgebungsvariable `SEC_USER_AGENT`.

## Regeln, die immer gelten

- **Keine Anlageberatung (not financial advice).** Das ist Software, die
  oeffentliche Daten liest und rechnet. Sag das einmal, bevor es um konkrete
  Kaeufe oder Verkaeufe geht.
- **Keine Order ohne ausdrueckliches Ja.** Nur das Modul `broker` kann zu einer
  Order fuehren, und nur wenn `risk` genau diese Order heute mit PASS geprueft
  hat UND der Nutzer im Chat fuer genau diese Order "yes"/"ja" schreibt.
  Ein BLOCK ist endgueltig. Alle anderen Module schreiben nur Vorschlaege.
- **Papierhandel ist Standard** (`"paper": true`). Keine Optionen, kein
  Margin, keine Leerverkaeufe, kein Hebel, solange der Nutzer das nicht selbst
  einschaltet.
- **API-Schluessel nie im Chat.** Sie gehoeren in Umgebungsvariablen.
- **Daten sind verzoegert und unvollstaendig.** 13F-Daten sind bis zu 45 Tage
  alt, Kongressmeldungen bis zu 45 Tage nach dem Trade, Kurse sind verzoegert.
  Vor einer Entscheidung beim Broker gegenpruefen.
- **Steuern:** `tax` rechnet nur. Keine Steuerberatung.

Herkunft: zusammengefuehrt aus dem MIT-lizenzierten Paket "trader-skill" von
Jake Schincariol (siehe `LICENSE`).
