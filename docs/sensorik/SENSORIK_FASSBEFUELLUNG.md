# Sensorik: Faßbefüllung (Whiteboard-Konzept)

**Stand:** 08.11.2026 (Whiteboard-Session)
**Quelle:** Whiteboard-Fotos, siehe `docs/sensorik/whiteboard/`
**Status:** Konzept / Preisfindung, noch nicht final

Dieses Dokument hält den Wissensstand zum emulvent® Sensorik-Produkt
„Faßbefüllung" fest, so wie er am Whiteboard erarbeitet wurde. Es dient als
fachliche Grundlage für den Produktkonfigurator (Pakete, Zusatzmaschinen,
Optionen) und für die weitere Entwicklung der Sensorik-Boxen.

---

## 1. Worum geht es?

Die Faßbefüllung (Fassabfüllung von Getränken) soll mit Sensorik überwacht
werden. Pro Abfüllmaschine wird der **Füllstand** erfasst, zentral wird der
**Brix-Wert** (Zuckergehalt des Produkts in °Brix) gemessen. Die Sensoren
hängen an einer zentralen **Combox**, die Messwerte sammelt. Pro Maschine
sitzt eine **Box** (Split-Box analog oder Digital-Box), die Sensor,
Stromversorgung und Signalleuchte zusammenführt.

Begriffe vom Whiteboard:

| Begriff | Bedeutung |
|---------|-----------|
| **Brix** | Brix-Sensor (Refraktometer), misst den Zuckergehalt in °Brix. 1x pro Anlage, nicht pro Maschine. |
| **Combox** | Zentrale Kommunikations-/Sammelbox. Nimmt die Sensorsignale auf und stellt die Daten bereit. 1x pro Anlage. |
| **Füllstand** | Füllstandsensor am Fass bzw. an der Befüllung. 1x pro Maschine. |
| **Split / Box Split** | Analoge Verteilerbox pro Maschine. Anschlüsse: Leuchte, 230 V, Sensor. Im ersten Entwurf „Box Analog" genannt. |
| **Box Digital** | Digitale Variante der Maschinenbox. Anschlüsse: Leuchte, Sensor, RJ45 (LAN), WLAN. 230 V war im Entwurf eingezeichnet und wurde in der finalen Fassung wieder weggewischt. |
| **Halterung** | Mechanische Halterung für Sensor bzw. Box an der Maschine. |
| **230V** | Netzteil / Stromanschluss 230 V. |
| **Leuchte** | Signalleuchte (Statusanzeige an der Maschine), optional. |
| **Digi Modul** | Digitalmodul, macht aus der Split-Box eine Box Digital bzw. ergänzt digitale Signalverarbeitung, optional. |
| **WLAN Modul** | Funkanbindung der Box, optional. |
| **App automation** | Automatisierung über die App (z. B. Abschalten/Melden bei Füllstand erreicht), optional. |
| **Magnetventil** | Elektrisch schaltbares Ventil, um die Befüllung automatisch zu stoppen, optional. |

---

## 2. Pakete und Preise

### 2.1 Grundpaket: 1 Maschine

Preis am Whiteboard: **1.200 €**

| Menge | Position |
|------:|----------|
| 1x | Brix |
| 1x | Combox |
| 1x | Füllstand |
| 2x | Kabel |
| 2x | Halterung |
| 2x | 230 V |
| 1x | Split (Box Split) |

Lesart: Combox und Brix werden einmal pro Anlage benötigt und brauchen je ein
230-V-Netzteil, eine Halterung und ein Kabel. Die erste Maschine bekommt
Füllstandsensor und Split-Box.

### 2.2 Erweiterung: 2 bis 9 Maschinen

Preis am Whiteboard: **300 €** je zusätzlicher Maschine (Spalte „2–9 Masch.")

Je weiterer Maschine („+ jew."):

| Menge | Position |
|------:|----------|
| 1x | 230 V |
| 1x | Split (Box Split) |
| 1x | Halterung |
| 1x | Füllstand |

Brix und Combox werden nicht erneut benötigt. Der rote Pfeil am Whiteboard
verbindet „1x Split" mit der Zeichnung „Box Split": Split steht für die
analoge Maschinenbox.

Obergrenze 9 Maschinen: vermutlich die Anzahl Eingänge einer Combox. Ab
10 Maschinen wäre eine zweite Combox nötig. Das ist am Whiteboard nicht
ausformuliert und muss geklärt werden.

### 2.3 Optionen

Optionen für das Grundpaket (Spalte links unter „Optional"):

- Leuchte
- App automation
- Digi Modul
- WLAN Modul
- Magnetventil

Optionen je zusätzlicher Maschine (Spalte „2–9 Masch."):

- Leuchte
- Digi Modul
- WLAN Modul

App automation und Magnetventil tauchen nur beim Grundpaket auf. Ob sie pro
Anlage oder pro Maschine gelten, ist offen. Preise für Optionen sind am
Whiteboard nicht vermerkt.

### 2.4 Weitere Zahlen am Whiteboard (Interpretation offen)

Im letzten Foto stehen unten links zusätzlich:

| links | rechts |
|------:|-------:|
| 1450 | 1.080.000,- |
| 250 | 950.000,- |

Plausible Lesart: eine alternative Preisstaffel (1.450 € Grundpaket,
250 € je Zusatzmaschine) gegenüber 1.200 € / 300 €, und daneben zwei
Umsatz- bzw. Marktpotenzial-Szenarien. Die Zuordnung ist nicht belegt und
muss mit Björn/Thilo abgestimmt werden.

---

## 3. Box-Varianten (Hardware)

```
Box Split (analog)                  Box Digital
┌──────────┐── Leuchte              ┌──────────┐── Leuchte
│          │── 230 V                │          │── (230 V, weggewischt)
│          │── Sensor               │          │── RJ45
└──────────┘                        │          │── WLAN
                                    └──┬───────┘
                                       Sensor
```

- **Box Split** ist die Standardbox im Paket. Sie verteilt analog: Sensor
  rein, 230 V rein, Leuchte raus.
- **Box Digital** ist die Variante mit Netzwerkanbindung (RJ45 und/oder
  WLAN). Sie entsteht aus den Optionen „Digi Modul" und „WLAN Modul".
- Für den Konfigurator bedeutet das: Die Box-Variante ist kein eigener
  Artikel, sondern ergibt sich aus den gewählten Optionen.

---

## 4. Offene Punkte

1. Preise der Optionen (Leuchte, Digi Modul, WLAN Modul, App automation,
   Magnetventil).
2. Gilt „2–9 Maschinen" wegen der Combox-Eingänge? Was passiert ab 10?
3. Braucht die Box Digital 230 V oder läuft sie über PoE / Netzteil der
   Combox? Am Whiteboard wurde 230 V weggewischt.
4. Bedeutung der Zahlen 1450 / 250 und 1.080.000 / 950.000.
5. Sind App automation und Magnetventil pro Anlage oder pro Maschine?

---

## 5. Maschinenlesbare Form

Die Paketstruktur liegt zusätzlich in `docs/sensorik/sensorik_pakete.json`,
damit der Konfigurator sie später direkt laden kann. Preise dort sind der
Whiteboard-Stand, nicht freigegeben.
