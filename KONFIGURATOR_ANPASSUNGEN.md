# emulvent Konfigurator – Anpassungsliste mit Priorität und Aufwand

Stand: 24.10.2026
Grundlage: Repo machine-data-scraper (Plugin, Scraper, Architektur-Doku), Notion-Konzepte ROI-Rechner und Angebot.
Der Konfigurator-Quellcode selbst war in dieser Prüfung nicht zugänglich. Aufwände sind Schätzungen in Entwicklerstunden.

Prioritäten:
- P1 = vor dem nächsten Kundenkontakt, blockiert sonst den Nutzen
- P2 = nächste Iteration, verbessert Abschluss und Vertrauen
- P3 = später, Skalierung und Komfort

## P1 – sofort (Summe ca. 14–20 h)

| Nr | Anpassung | Warum | Aufwand |
|----|-----------|-------|---------|
| 1 | Fallback „Meine Maschine ist nicht dabei" mit manueller Eingabe (Tankvolumen, Maße, Trennwände, wassermischbar) | Nur drei Hersteller in der Liste. Jeder Hermle-, Mazak- oder Chiron-Kunde kommt sonst nicht weiter. Das ist der häufigere Fall, nicht die Ausnahme. | 4–6 h |
| 2 | Auswahl zweistufig: erst Hersteller, dann Modell mit Suchfeld (Tippen filtert) | Ein Dropdown mit 100+ Einträgen ist am Handy in der Halle unbenutzbar. | 4–6 h |
| 3 | Fehlerzustand entschärfen: statt „Fehler: HTTP 500" ein ruhiger Satz und automatischer Wechsel in die manuelle Eingabe | Technische Fehlermeldungen beim Kunden kosten Vertrauen und beenden den Durchlauf. | 1–2 h |
| 4 | Leere Werte ausblenden statt „(0L)" | Ein Modell mit „0 L" wirkt fehlerhaft, obwohl nur der Scraper nichts gefunden hat. | 1 h |
| 5 | Anrede einheitlich „Sie" | Entwurf sagt „Wähle deine Maschine", Pitch, Angebot und Website sagen „Sie". | 1–2 h |
| 6 | Produktname vereinheitlichen: überall „emulvent Konfigurator" (README nennt „Produktkonfigurator-App") | Ein Name, auf Englisch direkt „emulvent Configurator". | 1 h |
| 7 | API-Caching im Plugin: Transient 12 h plus Cache-Control-Header auf /models | Jeder Aufruf liest alle Modelle ungecacht aus der Datenbank. Auf Strato-Shared-Hosting spürbar langsam. | 1–2 h |

## P2 – nächste Iteration (Summe ca. 22–35 h)

| Nr | Anpassung | Warum | Aufwand |
|----|-----------|-------|---------|
| 8 | UI-Texte in Sprachdateien auslagern (de.json, en.json), Sprache aus dem lang-Attribut der Seite | Voraussetzung für jede Übersetzung. Aktuell steht alles fest im Code. | 4–8 h |
| 9 | Englische Fassung aller Konfigurator-Texte | Europa ist im Pitch der Markt (über 1 Mio. Kreisläufe), englischer Pitch existiert schon. | 2–3 h |
| 10 | Zahlen, Einheiten und Datum per Intl formatieren („1.000 l" vs. „1,000 l") | Sonst wirkt die englische Version unsauber. | 1–2 h |
| 11 | Ergebnis als Empfehlung formulieren und zum ROI-Rechner verlinken („Für Ihre DMU 50 empfehlen wir …, bezahlt nach X Monaten") | Konfigurator und ROI-Rechner sind heute getrennt. Zusammen ergeben sie den Kaufgrund in einem Satz. | 4–8 h |
| 12 | Datenstand anzeigen und Korrektur erlauben („Herstellerangabe, Stand 09/2026 – Werte stimmen nicht?") | Gescrapte Daten können falsch sein. Das Feld verification_count existiert schon, wird aber nicht genutzt. | 4–6 h |
| 13 | Scraper: Duplikatabgleich exakt auf Titel statt Suchtreffer | „DMU 50" trifft auch „DMU 50 eVo" und überschreibt das falsche Modell. Falsche Daten landen direkt im Konfigurator. | 1–2 h |
| 14 | Mobile-Ansicht prüfen und anpassen | Der Betriebsleiter steht an der Maschine, nicht am Schreibtisch. | 2–4 h (Prüfung) |
| 15 | Mietmodell im Konfigurator klar benennen und mit Kaufpreis vergleichbar machen | Laut Notion existiert es, im Pitch darf es erst genannt werden, wenn es sauber angeboten wird. | 2 h |

## P3 – später (Summe ca. 20–40 h)

| Nr | Anpassung | Warum | Aufwand |
|----|-----------|-------|---------|
| 16 | Plugin i18n-fähig machen (Text-Domain, __(), .pot) | Admin-Oberfläche ist nur für Björn und dich, daher nachrangig. | 3–4 h |
| 17 | Hersteller aus der Taxonomie ableiten statt hart codiert (Dashboard, Scraper-Status) | Ein vierter Hersteller erfordert heute Änderungen an drei Stellen. | 2–3 h |
| 18 | Weitere Hersteller-Scraper (Hermle, Mazak, Chiron …) | Mehr Treffer in der Liste, weniger manuelle Eingaben. | 4–8 h je Hersteller |
| 19 | Lead-Erfassung am Ende (Firma, E-Mail gegen personalisiertes Ergebnis-PDF), nach Stufe 3 des Notion-Konzepts | Sauberster Weg zur Wiedererkennung und zum Vertriebssignal. Datenschutztext nötig. | 6–10 h |
| 20 | Sprachabhängige Routen und Anbindung an Polylang/WPML | Erst sinnvoll, wenn die Website selbst zweisprachig ist. | 4–8 h |
| 21 | Admin-Dashboard: „Fehler" statt „Pending" bei Fehlern, Deutsch/Englisch vereinheitlichen | Nur intern sichtbar. | 1 h |

## Nicht enthalten

- Die Lovable-App (kss-check-buddy) ist ein eigenes Thema und hier nicht bewertet.
- Preise in Euro hängen vom Stundensatz ab. Bei 80–120 €/h liegt P1 bei etwa 1.100–2.400 €.
