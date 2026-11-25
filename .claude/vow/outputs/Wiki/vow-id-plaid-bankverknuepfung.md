# Vow.id – Bankverknüpfung über Plaid

> Stand: 23.11.2026 (Erstfassung 22.11.2026). Der Abschnitt „Aus der Praxis" beruht auf Beobachtungen aus der Community und ist nicht offiziell belegt. Quellen: https://vow.id/terms (§ 8, § 9, § 13), https://vow.id/privacy (§ 4, § 7, § 9, § 12, § 15, § 16), https://vow.id/documentation (Abschnitt 11) sowie Texte und Code der Bank-Komponente im Frontend von vow.id. Übersicht zu Vow.id: [vow-id.md](./vow-id.md).

## Worum es geht

Mit der Bankverknüpfung weisen **Premium-Mitglieder** Käufe über ihre Kartentransaktionen nach statt über E-Mail-Belege. Sie müssen dafür keine E-Mail-Adressen bei Händlern ändern. Vow.id nutzt dafür **Plaid**. Der Dienst heißt in der App **„Bank Feed“** bzw. **„Bank MR matching“**. Laut AGB § 8: *„Plaid bank linking is live.“*

Hauptanwendungsfall laut Startseite: *„Connect your bank and collect up to 100% MR on energy purchases, proven by verified bank transactions.“*

## Voraussetzungen

- **Premium-Abo** (99 US$/Jahr; Launch-Angebot 49 US$ im ersten Jahr bei Beitritt bis 31.12.2026). Free-Nutzer sehen: *„Bank connections are a Premium feature — upgrade to link your account.“*
- Eine **unterstützte Bank**, die an Plaid teilnimmt. Dazu können Onboarding-Checks kommen.
- Ein **separates Opt-in** mit ausdrücklicher Einwilligung. Die Bankverknüpfung ist kein Cookie-Consent und für das Free-Konto nicht nötig.
- **Regionen:** In der Bankliste markiert die App jede Verbindung als **„UK & Europe“** oder **„USA“**. Es gibt also eine Plaid-Anbindung für UK/EU und eine für die USA. Welche Banken genau unterstützt werden, hängt von Plaid ab.

## Ablauf in der App

1. Unter Profil → Bank: **„Add a bank account“**.
2. Einwilligung per Checkbox („Bank data consent“):
   > *„I consent to Vow.id collecting, processing and storing my bank connection information and cleared card transactions (merchant, amount, currency and date) through Plaid to provide Bank Feed and match eligible purchases to MR.“*
3. **„Continue to bank“**: Vow.id schickt einen **6-stelligen Sicherheitscode** an die verifizierte E-Mail-Adresse (Betreff: „Your Vow.id bank link code“). Der Nutzer gibt ihn ein.
4. Der Server erzeugt einen **Plaid Link Token**. Dann öffnet sich das Plaid-Link-Fenster (`cdn.plaid.com/link/v2/stable/link-initialize.js`).
5. Der Login läuft **beim Bank- bzw. Plaid-Flow**. Banken mit OAuth leiten auf `https://vow.id/plaid/oauth` zurück („Connecting your bank — Vow.id“).
6. Nach erfolgreichem Login tauscht Vow.id serverseitig den Public Token gegen einen **Access Token**. Die App meldet z. B. „*[Bank] is connected — N transactions imported*“.
7. Die verknüpften Banken erscheinen mit Name und Region. Man kann sie manuell aktualisieren („Everything is up to date“) und **trennen** („Disconnect“).

## Welche Daten Vow.id bekommt

| Daten | Ja/Nein |
|---|---|
| Online-Banking-Zugangsdaten | **Nein.** Vow.id fragt sie weder ab noch speichert es sie. |
| Plaid Access Token | Ja, **verschlüsselt** gespeichert |
| Gebuchte Kartentransaktionen: Händler, Betrag, Währung, Datum | Ja |
| Historie bei Erstverknüpfung | bis zu **30 Tage** zurück |
| Laufende Aktualisierung | Ja, solange die Verknüpfung aktiv ist |
| Zahlungen auslösen oder Geld bewegen | **Nein.** Die Verbindung ist nur lesend. |

## Wofür die Daten genutzt werden

- Gebuchte Käufe bei **gelisteten, berechtigten Händlern und Diensten** werden erkannt. Daraus erstellt Vow.id Vorschläge für **Pending MR** zum jeweiligen Premium-Satz:
  - bis 40 % bei Featured Merchants
  - bis 100 % bei Energierechnungen
  - höchstens 500 US$ bzw. 500 MR pro Kauf
- **Deduplizierung:** Beleg und Banktransaktion zählen pro Kauf nur einmal. Abgeglichen werden Händler, Betrag und Datum innerhalb von ±5 Tagen; bei Fremdwährung ±5 % auf den USD-Wert. Passt ein Beleg zur Transaktion, können Prüfer ihn in verkürzter Form als Zusatznachweis sehen.
- Außerdem: Sicherheit, Betrugs- und Duplikatsprävention, Verwaltung.
- **Rechtsgrundlage:** gesonderte Einwilligung (Opt-in), bei Bedarf auch Vertragserfüllung für das Bank-Matching (Privacy § 4).
- Eine Transaktion qualifiziert sich nur, wenn sie **gebucht** ist (cleared) und die Angebotsregeln erfüllt. Rückbuchungen und Stornos können den Vorschlag ungültig machen.

## Wer die Bankdaten sieht

- **Normale Retail-Partner** im Ökosystem bekommen **keine** Banktransaktionen.
- **Unabhängige Vow Verifiers** sehen in einer eingeschränkten Prüfansicht einen pseudonymisierten Nachweis:
  - Claim-ID und Status
  - Tarif und Mitgliedsdauer
  - maskierte Wallet
  - Händler, Kaufdatum, Betrag und Währung, Netto-Umsatz
  - Refund-Status
  - Angebotsversion, Funding-Typ, Reward-Satz
  - Wechselkurs mit Quelle und Datum
  - vorgeschlagene Shopper- und Affiliate-MR
  - Claim-Fingerprint

  Sie sehen **keine** Bank-Zugangsdaten und keine anderen Transaktionen des Kontos.
- Wird ein Claim angefochten, sehen die **drei anderen Proposer** zusätzlich die relevanten Bank- und Beleg-Nachweise.
- **On-chain (BNB Smart Chain)** steht nur ein gesalzenes Keccak-256-Commitment, keine Bankdaten.
- **OpenAI** bekommt **keine** Banktransaktionen, nur Belegtexte. Meta- und Google-Pixel bekommen ebenfalls keine.

## Trennen und Löschen

- **Bank entfernen:** Die Synchronisierung stoppt. Token und gespeicherte Transaktionen werden aus den Live-Systemen gelöscht. Das gilt auch, wenn das Konto geschlossen wird.
- **Weiterhin gespeichert bleiben:** Was Plaid, die Bank oder ein Kontoinformationsdienst nach eigenen Bedingungen aufbewahrt. Dazu kommen Datenbank-Backups und Plattform-Logs nach den Fristen der jeweiligen Anbieter.
- Bereits eingereichte On-chain-Commitments und Entscheidungen bleiben dauerhaft bestehen.
- Läuft die Verbindung ab oder wird sie widerrufen, garantiert Vow.id kein weiteres Matching.
- Wer die Einwilligung widerruft, bekommt aus dieser Quelle keine neuen MR-Vorschläge mehr.

## Aus der Praxis (Beobachtungen, Stand 23.11.2026)

**Kontoauswahl.** Bei der Freigabe wählt man die Konten aus. Beispiel Sparkasse: Karte und Girokonto wurden freigegeben, Tagesgeld und Depot nicht. Mehrere Konten bei verschiedenen Banken lassen sich nacheinander verbinden; jedes erscheint einzeln und lässt sich einzeln entfernen.

**Anmeldung je nach Bank verschieden.** Manche Banken öffnen die eigene Banking-App zur Freigabe (zum Beispiel Revolut). Bei Volks- und Raiffeisenbanken erscheint im Plaid-Fenster ein Formular für VR-NetKey oder Alias und PIN. In diesem Fall gehen die Zugangsdaten an Plaid, nicht an Vow.id. Die Aussage „Anmeldung nur bei der eigenen Bank" stimmt also nicht für alle Institute.

**Gesehene Institute.** In Screenshots verbundener Konten tauchten auf: Sparkasse, Volksbanken Raiffeisenbanken, DKB, N26, Targobank, Revolut, Wise, PayPal. Das ist keine offizielle Liste. Aus Österreich (Erste Bank) und der Schweiz wurden Probleme gemeldet. American Express Deutschland und die Miles-&-More-Karte wurden als fehlend genannt.

**Bankabdeckung prüfen.** In der App gibt es für Premium Listen zur Abdeckung des Anbieters (USA und EU, als CSV). Laut Vow.id ist auch ein Eintrag dort keine Garantie, und Premium garantiert keine Verbindung.

**Kartenzahlung ja, Lastschrift fraglich.** Ein Kartenkauf im Supermarkt wurde sofort als MR-Vorschlag erkannt. Die Abbuchung eines gelisteten Energieversorgers (in der Liste „Stadtwerke Kassel", auf dem Konto „Städtische Werke Kassel") ergab keine MR. Mögliche Ursachen: Die Einwilligung spricht von Kartenzahlungen, Strom wird aber meist per Lastschrift bezahlt; oder der Name weicht ab. Ungeklärt. Das ist für das Versprechen „bis zu 100 % MR auf Energie" wesentlich.

**Erkennungsregel.** Laut „New User Overview" (Ausgabe 11) verlangt Bank-MR eine sichere Händlererkennung und eine Händler-Website, die zur registrierten Liste passt. Der Text auf dem Kontoauszug allein reicht nicht. Nicht jede importierte Zeile ergibt MR.

**Weitere Beobachtungen.**
- Die Verbindung scheiterte bei einem Mitglied tagelang und funktionierte nach dem Wechsel vom Samsung-Browser zu Chrome.
- Unter den Bank-Transaktionen erschienen bei einem Mitglied Einträge, die es nicht zuordnen konnte. Der Leitfaden rät: verbundenes Konto prüfen, bei der Bank nachfragen.
- Mehrere Mitglieder haben Premium doppelt bezahlt, weil der erste Versuch scheinbar hing.
- Gemeinschaftskonto mit zwei Vow.ids: nicht geregelt. Sicher ist nur, dass jeder Kauf einmal zählt und der erste gültige Anspruch gewinnt.
- Vorteile der Kreditkarte (Cashback, Meilen): in den Unterlagen nicht erwähnt. Die Verbindung ist nur lesend und ändert die Zahlung nicht.

## Offene Punkte (öffentlich nicht dokumentiert)

- Welche Plaid-Produkte genau genutzt werden. Der Code deutet auf Link plus Transactions hin; Auth, Identity oder Payment Initiation werden nicht genannt.
- Eine verbindliche Liste unterstützter Banken und Länder. Deutsche Institute sind nach den Beobachtungen oben angebunden; die Abdeckungslisten aus der App liegen diesem Wiki nicht vor.
- Ob Lastschriften (zum Beispiel für Energie) für MR erkannt werden oder nur Kartenzahlungen.
- Ob in der EU ein lizenzierter Kontoinformationsdienst (AISP) dazwischengeschaltet ist. Die AGB erwähnen nur allgemein „any account-information provider“.
- Welche Energieversorger bzw. „eligible listed services“ beim Bank-Matching als berechtigt gelten.

## Welche Karte wird erkannt (Stand 25.11.2026, aus der Community, nicht offiziell belegt)

Grundregel aus der Gruppe: Der Bank-Scanner muss in der Buchung erkennen können, wo eingekauft wurde.

- Girocard und Debitkarte der verbundenen Bank: Einzelbuchung mit Händlername auf dem Girokonto, wird grundsätzlich erkannt.
- Kreditkarte mit Sammelabrechnung: auf dem Girokonto nur die Gesamtsumme, wird nicht erkannt. Ausnahme: Das Kartenkonto lässt sich bei der Verknüpfung als eigenes Konto auswählen.
- Karten fremder Anbieter (zum Beispiel Vault27): laufen nicht über die verbundene Bank, werden nicht erkannt.
- Offen: ob Supermärkte überhaupt als Anbieter gelistet sind; ob Apple Pay/Google Pay den Händlernamen unverändert durchreichen.
