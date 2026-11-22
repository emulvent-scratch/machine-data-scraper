# Vow.id – Bankverknüpfung über Plaid

> Stand: 22.11.2026. Quellen: https://vow.id/terms (§ 8, § 9, § 13), https://vow.id/privacy (§ 4, § 7, § 9, § 12, § 15, § 16), https://vow.id/documentation (Abschnitt 11) sowie Texte und Code der Bank-Komponente im Frontend von vow.id. Übersicht zu Vow.id: [vow-id.md](./vow-id.md).

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

## Offene Punkte (öffentlich nicht dokumentiert)

- Welche Plaid-Produkte genau genutzt werden. Der Code deutet auf Link plus Transactions hin; Auth, Identity oder Payment Initiation werden nicht genannt.
- Eine konkrete Liste unterstützter Banken und Länder, insbesondere ob deutsche Banken über Plaid EU angebunden sind.
- Ob in der EU ein lizenzierter Kontoinformationsdienst (AISP) dazwischengeschaltet ist. Die AGB erwähnen nur allgemein „any account-information provider“.
- Welche Energieversorger bzw. „eligible listed services“ beim Bank-Matching als berechtigt gelten.
