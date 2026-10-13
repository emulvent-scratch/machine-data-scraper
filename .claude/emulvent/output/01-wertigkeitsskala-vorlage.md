# Vorlage: Fehlerwertigkeit gelber Servicesituationen

**Zweck:** Gemeinsame Skala für Service, Qualität und Schichtleitung. Diese Skala ist die Grundlage für die KI-Klassifikation (I-001, Stufe 0).
**Status:** Entwurf, noch nicht freigegeben
**Verantwortlich für Freigabe:** _[Name, Funktion]_
**Gültig ab:** _[Datum]_
**Version:** 0.1

---

## 1. Stufen

Bitte je Stufe ausfüllen. Die Stufenanzahl ist ein Vorschlag (4 Stufen), kann angepasst werden.

| Stufe | Bezeichnung | Kurzdefinition | Eskalation | Reaktionszeit |
|-------|-------------|----------------|------------|---------------|
| 1 | Gering | _Keine Auswirkung auf Qualität, Sicherheit oder Verfügbarkeit_ | Keine, Erfassung im Schichtbuch | _z. B. nächste Schichtübergabe_ |
| 2 | Mittel | _Geringe Auswirkung, Maschine läuft mit Einschränkung_ | Schichtleiter | _z. B. innerhalb der Schicht_ |
| 3 | Hoch | _Auswirkung auf Qualität oder Verfügbarkeit, Ausschuss möglich_ | Schichtleiter + Instandhaltung/Qualität | _z. B. sofort_ |
| 4 | Kritisch | _Sicherheitsrelevant oder Stillstand der Linie_ | Sofort-Eskalation, Stillstandsregel greift | _sofort_ |

---

## 2. Kriterien je Stufe

Für jede Stufe mindestens drei Kriterien, die im Alltag prüfbar sind.

### Stufe 1: Gering
- _Kriterium 1_
- _Kriterium 2_
- _Kriterium 3_

### Stufe 2: Mittel
- _Kriterium 1_
- _Kriterium 2_
- _Kriterium 3_

### Stufe 3: Hoch
- _Kriterium 1_
- _Kriterium 2_
- _Kriterium 3_

### Stufe 4: Kritisch
- _Kriterium 1_
- _Kriterium 2_
- _Kriterium 3_

---

## 3. Beispiele je Stufe

Beispiele sind wichtiger als Definitionen. Sie sollten echte Fälle aus der Historie abdecken.

| Stufe | Beispielbeschreibung (Originalwortlaut) | Maschine | Zugeordnete Maßnahme |
|-------|------------------------------------------|----------|----------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

---

## 4. Harte Regeln (Mindestwertigkeit)

Diese Regeln gelten vor der KI-Bewertung. Trifft eine Regel zu, ist die Mindeststufe fest gesetzt. Die KI darf nur höher einstufen.

| Regel-ID | Bedingung | Mindeststufe | Begründung |
|----------|-----------|--------------|------------|
| R-01 | Schlüsselwort: _z. B. „Rauch“, „Funken“, „Leck“_ | 4 | _Sicherheit_ |
| R-02 | Alarmcode: _Liste ergänzen_ | _ _ | |
| R-03 | Sensorwert außerhalb Grenzwert: _Grenzwerte ergänzen_ | _ _ | |

Die Schlüsselwörter müssen je Sprache gepflegt werden (siehe Abschnitt 6).

---

## 5. Maßnahmenkatalog (Verweis)

Jede Stufe braucht eine Maßnahmen-Zuordnung. Die Maßnahmen bekommen feste IDs, damit Vorschläge der KI eindeutig sind.

| Maßnahmen-ID | Maßnahme | Typische Stufe | Verantwortlich | Typische Dauer |
|--------------|----------|----------------|----------------|----------------|
| M-001 | _z. B. Maschine kurz prüfen, Protokoll_ | 1–2 | | |
| M-002 | _z. B. Instandhaltung informieren_ | 2–3 | | |
| M-003 | _z. B. Linie anhalten, Freigabe Qualität_ | 4 | | |

---

## 6. Sprache und Begriffe

- Sprachen im Betrieb: _Liste_
- Fachbegriffe mit Übersetzung (Glossar): _Verweis auf Datei_
- Testsätze je Sprache geprüft von: _Name_

---

## 7. Änderungshistorie

| Version | Datum | Änderung | Von |
|---------|-------|----------|-----|
| 0.1 | 2026-10-13 | Erstentwurf | |
