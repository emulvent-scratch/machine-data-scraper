# Ideen-Backlog emulvent® App

Ideen für die Weiterentwicklung der App, die emulvents Sensorik mit der Dokumentation verbindet.
Jede Idee hat einen Status und eine kurze Einordnung. Details stehen im jeweiligen Abschnitt.

| ID | Idee | Status | Priorität |
|----|------|--------|-----------|
| I-001 | KI-Bewertung der Fehlerwertigkeit gelber Servicesituationen mit Maßnahmenvorschlag | Idee | Hoch |

Status-Werte: `Idee` → `Geprüft` → `In Planung` → `In Umsetzung` → `Umgesetzt` / `Verworfen`

---

## I-001: KI-Bewertung der Fehlerwertigkeit von Servicesituationen

**Status:** Idee
**Erfasst:** 2026-10-13
**Bereich:** Servicesituationen (gelb), Schichtleiter-Workflow, Sensorik-Anbindung

### Kurzbeschreibung

Ein Mitarbeiter erfasst eine Servicesituation (Kennzeichnung gelb) in der App in seiner Muttersprache.
Eine KI prüft die Beschreibung, ordnet die Fehlerwertigkeit ein und schlägt dem Schichtleiter
passende Maßnahmen vor. Der Schichtleiter prüft den Vorschlag und entscheidet. Ziel ist, dem
Schichtleiter die Beurteilung zu erleichtern und Zeit zu sparen.

### Nutzen

- **Zeitersparnis** bei der Beurteilung und beim Finden geeigneter Maßnahmen
- **Einheitlichere Bewertung** über Schichten und Schichtleiter hinweg
- **Sprachbarrieren abbauen**: Mitarbeiter müssen nicht in der Betriebssprache schreiben
- **Bessere Datenbasis** für Auswertungen (Pareto, Wiederholungsfehler, Trends)

### Wichtige Leitplanken

Die Fehlerwertigkeit hat Auswirkungen auf Sicherheit, Qualität und Eskalation. Daraus folgen Regeln für das Design:

1. **KI schlägt vor, der Mensch entscheidet.** Der Schichtleiter bestätigt oder korrigiert die Bewertung. Die KI entscheidet nie allein über Eskalation oder Stillstand.
2. **Sicherheitsrelevante Fälle werden nie heruntergestuft.** Vor der KI läuft eine deterministische Regelprüfung (Schlüsselwörter, Sensorwerte, Alarmcodes). Trifft eine Regel zu, ist die Mindestwertigkeit fest gesetzt. Die KI darf nur nach oben korrigieren.
3. **Unsichere Fälle werden sichtbar.** Bei niedriger Konfidenz oder fehlenden Angaben kennzeichnet die App den Fall als „manuell prüfen“ statt eine Wertigkeit zu raten.
4. **Jede Bewertung ist nachvollziehbar.** Gespeichert werden Eingabe, Übersetzung, Vorschlag, Begründung, Modellversion und die Entscheidung des Schichtleiters.
5. **Datenschutz von Anfang an.** Erfassungen enthalten personenbezogene Daten (Mitarbeiter, Schicht). Klärung mit Datenschutzbeauftragtem und ggf. Betriebsrat vor dem Pilot.

### Vorgeschlagener Ablauf

```
Mitarbeiter (Muttersprache)
   │  Text oder Sprache, Maschine, Kennzeichnung gelb
   ▼
[1] Normalisierung   → Übersetzung nach Deutsch, Fachbegriffe erhalten,
                       Originaltext bleibt gespeichert
   ▼
[2] Regelprüfung     → Schlüsselwörter, Alarmcodes, Sensorgrenzwerte
                       setzen eine Mindestwertigkeit
   ▼
[3] KI-Klassifikation → strukturierte Ausgabe:
                       wertigkeit, begründung, konfidenz,
                       massnahmen[], fehlende_angaben[]
   ▼
[4] Schichtleiter-Review → Vorschlag annehmen / ändern / ablehnen,
                           Maßnahme zuweisen
   ▼
[5] Speicherung + Audit  → Entscheidung, Zeitstempel, Versionen
```

Die Ausgabe der KI hat ein festes Schema (JSON) und wird vor der Anzeige validiert.
Ungültige oder unvollständige Antworten landen im Status „manuell prüfen“.

### Eingabe für die Klassifikation

Der Prompt bekommt:

- die **Wertigkeitsskala** mit klaren Kriterien je Stufe (Beispiele je Stufe, nicht nur Definitionen)
- den **Maßnahmenkatalog** (feste IDs, damit Vorschläge zuordenbar sind)
- den **Kontext**: Maschine, Baugruppe, letzte Alarme und Sensorwerte, ähnliche frühere Fälle
- die **Erfassung** im Original und in der Übersetzung

### Ausbau in Stufen

#### Stufe 0: Klärung und Datenbasis (Voraussetzung, keine Software)

- **Wertigkeitsskala festlegen**: Anzahl der Stufen, Kriterien je Stufe, Eskalationsregeln. Fachverantwortliche aus Service und Qualität entscheiden.
- **Maßnahmenkatalog** erfassen, mit Ids, Verantwortlichen und typischer Dauer.
- **Historie sichten**: vorhandene gelbe Servicesituationen mit der tatsächlich vergebenen Wertigkeit und Maßnahme. Ergibt ein erstes Testset (Ziel: 100 bis 200 Fälle, quer über Maschinen und Schichten).
- **Sprachen festlegen**: welche Muttersprachen im Betrieb vorkommen. Testsätze in jeder Sprache mit Fachleuten prüfen.
- **Datenschutz und Mitbestimmung** klären.
- **Erfolgsmessung definieren** (siehe unten), bevor gebaut wird.

#### Stufe 1: MVP – Vorschlag mit Schichtleiter-Review (Pilot, eine Schicht/Linie)

- Erfassung in der App mit Auswahl der Sprache, Übersetzung nach Deutsch
- Regelprüfung für Mindestwertigkeit
- KI-Klassifikation mit Wertigkeit, Begründung, Konfidenz und 2 bis 3 Maßnahmenvorschlägen
- Schichtleiter-Ansicht: Vorschlag annehmen, ändern, ablehnen; Erfassung in Originalsprache sichtbar
- Protokollierung jeder Entscheidung (Basis für alle späteren Verbesserungen)
- **Bewusst nicht enthalten:** automatische Eskalation, Sensordaten, Auswertungen

Ergebnis: Der Pilot liefert echte Korrekturdaten. Das ist der wichtigste Output der Stufe.

#### Stufe 2: Sensorik-Kontext (Verknüpfung mit Maschinendaten)

- Alarme, Betriebszustände und Sensorwerte zum Zeitpunkt der Erfassung automatisch an die Situation hängen
- Kontext in den Prompt und in die Regelprüfung einbeziehen (z. B. Temperaturgrenze überschritten → Mindestwertigkeit)
- Sensorwerte im Review anzeigen, damit der Schichtleiter den Zusammenhang sieht
- Anbindung über die bestehende Datenbasis (WordPress/REST-Plugin, siehe `emulvent-machine-data.php`) oder eine eigene Schnittstelle zur Maschinensteuerung

Dieser Schritt ist der eigentliche Mehrwert von emulvent gegenüber einer reinen Textklassifikation.

#### Stufe 3: Ähnliche Fälle und Wissen (Retrieval)

- Bei jeder neuen Situation die ähnlichsten früheren Fälle suchen (Embeddings über Beschreibungen und Maßnahmen) und dem Schichtleiter zeigen
- Vorschläge stützen sich auf Erfahrung: „Vergleichbarer Fall am 12.03., Maßnahme X, Wirksamkeit gut/schlecht“
- Wiederholungsfehler erkennen (gleiche Maschine, gleiches Muster, Zeitfenster)

#### Stufe 4: Lernschleife und Qualitätssicherung

- Korrekturen des Schichtleiters werden zu Evaluationsdaten
- Feste Evaluationsläufe: Jede Änderung an Prompt, Skala oder Modell wird gegen das Testset gemessen, bevor sie live geht
- Modellversion und Prompt-Version pro Bewertung speichern
- Monitoring: Fehlerquote, Korrekturquote, Anteil „manuell prüfen“

#### Stufe 5: Maßnahmen-Steuerung und Nachverfolgung

- Maßnahmen werden Aufgaben mit Verantwortlichem, Frist und Status
- Eskalation nach Regel (z. B. ab Stufe X sofort Push an Schichtleiter und Instandhaltung)
- Wirksamkeitsprüfung: Kehrt der Fehler zurück, wird die Maßnahme als unwirksam markiert
- Dashboard mit Pareto nach Maschine, Fehlerart, Zeit, Schicht

#### Stufe 6: Skalierung und Anbindung

- Mehrere Standorte und Maschinenparks
- Schnittstelle zum QM-System (z. B. Korrektur- und Vorbeugemaßnahmen)
- Berichte für Kundenaudits

### Erfolgsmessung

| Kennzahl | Ziel (Vorschlag) | Bemerkung |
|----------|------------------|-----------|
| Zeit bis zur festgelegten Maßnahme | deutlich unter Ausgangswert | Vorher/Nachher im Pilot messen |
| Übereinstimmung KI vs. Schichtleiter | steigend, Zielwert mit Fachbereich festlegen | Basis: Korrekturquote |
| **Unterbewertungsrate** (KI niedriger als Schichtleiter bei kritischen Fällen) | **nahe null** | wichtigste Sicherheitskennzahl |
| Anteil „manuell prüfen“ | stabil, nicht zu hoch | zu hoch = Nutzen sinkt |
| Nutzungsquote | > 80 % der gelben Fälle | zeigt Akzeptanz |

### Risiken und Gegenmaßnahmen

| Risiko | Gegenmaßnahme |
|--------|---------------|
| Fehlklassifikation, zu niedrige Wertigkeit | Regelprüfung als Untergrenze, Unterbewertungsrate als Pflichtkennzahl, Schichtleiter bleibt Entscheider |
| Falsche Übersetzung von Fachbegriffen | Glossar je Standort, Anzeige des Originaltexts, Testsätze je Sprache |
| Mitarbeiter nutzen die App nicht | Kurzer Aufwand bei der Erfassung, Feedback an den Mitarbeiter („Ihre Meldung wurde als X eingeordnet“) |
| Datenschutz und Mitbestimmung | Zweckbindung, Löschfristen, keine Leistungsbewertung von Personen aus den Daten |
| KI-Ausfall oder hohe Kosten | Fallback auf manuelle Erfassung, Kosten pro Fall im Monitoring |
| Haftungsfrage bei Fehlentscheidungen | Dokumentierte Entscheidung des Schichtleiters, Audit-Log |
| Modelländerung verändert Ergebnisse | Versionierung, Regressionstests gegen das Testset vor jedem Wechsel |

### Offene Fragen

1. Wer legt die Wertigkeitsskala fest, und gibt es sie bereits schriftlich?
2. Gibt es eine Historie gelber Servicesituationen mit Bewertung und Maßnahme für ein Testset?
3. Welche Sprachen werden im Betrieb genutzt?
4. Gibt es Sensorwerte und Alarme bereits zentral abrufbar, und in welchem System liegen sie?
5. Wer ist Entscheider für Eskalation und Stillstand, und gilt die KI-Bewertung nur als Empfehlung?
6. Ist eine Cloud-Verarbeitung der Texte mit dem Datenschutz vereinbar, oder ist eine lokale Lösung nötig?
7. Welche Akzeptanzkriterien gelten für den Pilot?

### Nächster Schritt

**Stufe 0 starten:** Wertigkeitsskala, Maßnahmenkatalog und Testset zusammenstellen. Ohne diese Grundlagen lässt sich weder die KI-Qualität messen noch der Pilot sinnvoll auswerten.

### Änderungshistorie

| Datum | Änderung |
|-------|----------|
| 2026-10-13 | Idee erfasst, Ausbaustufen 0 bis 6 ausgearbeitet |
