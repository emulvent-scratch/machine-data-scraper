# Vow.id

> Stand: 22.11.2026. Quellen: Website https://vow.id (Startseite, `/documentation`, `/terms`, `/privacy`; AGB und Datenschutzerklärung jeweils „Last updated · 20 November 2026“). Die Seite ist eine Single-Page-App; die Texte stammen aus den ausgelieferten JS-Bundles der Seite. Die Website führt Vow.id als **Beta**.
>
> Details zur Bankanbindung: siehe [Plaid-Bankverknüpfung](./vow-id-plaid-bankverknuepfung.md).

## Kurzüberblick

Vow.id ist eine an eine Krypto-Wallet gebundene Identitäts- und Reward-Plattform aus dem **VOW-Ökosystem**. Slogan: *„Your identity. Your wallet. Your rewards.“* Laut Startseite bietet sie „eine private Identität, um deine Daten zu verwalten, deine Wallet zu schützen und Rewards zu sammeln“.

| | |
|---|---|
| Betreiber / Verantwortlicher | **N888 LIMITED**, Company No. 17434249, 20 Wenlock Road, London, England, N1 7GU (Vow.id wird von N888 „inkubiert“) |
| Datenschutzkontakt | Paul Teleky, Director. ICO-Registrierung ZC277515 |
| Kontakt | privacy@vow.id, security@vow.id |
| Blockchains (Login/Vault) | BNB Smart Chain, Ethereum |
| Reward-Protokoll | Smart Contracts auf **BNB Smart Chain** (nicht von Vow.id/N888 entwickelt oder deployed; laut Vow.id unveränderlich und ohne Admin- oder Upgrade-Keys) |
| Hosting / Tech | Lovable Cloud; Wallet-Verbindung über Reown/WalletConnect (laut Startseite „+300“ Wallets) |
| Aufsichtsrecht | Britisches Unternehmen, Beschwerden an das UK ICO. Es gibt **keine FCA-Zulassung**; das wird ausdrücklich so gesagt. |

## Funktionen

### 1. Wallet-basierte Identität
- Login per **signierter Wallet-Challenge**. Die Signatur „kann keine Gelder bewegen“.
- Jeder Nutzer bekommt eine ID im Format `VOW-XXXX-XXXX` und einen Handle `yourname@vow.id`. Optional kann eine Vow-Domain wie `yourname.vow` registriert werden (über Freename).
- Optional: 2FA per Authenticator-App mit Recovery-Codes.

### 2. Privater Daten-Vault
- Speichert Kontaktdaten, verifizierte Weiterleitungsadressen, Lieferadressen, Präferenzen und optional Reisedokumente (Pass- oder Führerscheinnummer).
- Verschlüsselung: **AES-256-GCM mit serverseitig verwalteten Schlüsseln**. Vow.id sagt selbst: *„not end-to-end or zero-knowledge encryption“*. Autorisierte Serverfunktionen und berechtigtes Personal können die Daten entschlüsseln.
- Partner (Ökosystem-Sites) bekommen nur Identifier, Präferenzen und „Readiness“-Indikatoren. Den Vault selbst sehen sie nicht. Ausnahmen:
  - Hotel- oder Flugbuchungen: Vor- und Nachname
  - Lieferungen: Name und Adresse für den Lieferanten
- Kommunikation läuft über Vow.id („The site asks. We handle it.“). Partner bekommen weder E-Mail noch Telefonnummer.

### 3. `@vow.id`-Belegadresse
- Die Adresse `yourname@vow.id` ist **kein normales Postfach**. Sie nimmt nur Belege von freigegebenen, authentifizierten Shop-Absendern an. Alles andere wird abgewiesen.
- Typischer Einsatz laut Startseite: die Adresse als **Amazon-E-Mail** hinterlegen.
- Angenommene Belege werden verschlüsselt gespeichert, klassifiziert und bereinigt (Links und unsicheres HTML entfernt) an die private E-Mail weitergeleitet.
- **KI-Extraktion:** Absender, Betreff und Text gehen an OpenAI (USA). Das läuft direkt über N888s OpenAI-Projekt oder über das Lovable AI Gateway. Anhänge, Bankdaten, Vault-Felder und Wallet-Keys werden laut Vow.id **nicht** übertragen.
- Manuelle Beleg-Uploads sind nicht möglich.

### 4. Wallet Security (Permission-Scanner)
- Scannt **Ethereum, BNB Smart Chain, Polygon, Arbitrum, Base und Optimism**. Standardmäßig laufen ETH und BSC, die vier anderen Netze sind „einen Tap entfernt“.
- Zeigt Token-Approvals, unbegrenzte Allowances, NFT-Operator-Rechte und Delegation-Contracts, sortiert nach Risiko (Critical/High/Low).
- Der Scan ist nur lesend, wird nicht gespeichert und dauert bis zu 3 Minuten. Approvals widerruft der Nutzer selbst über seine Wallet.
- Datenquellen: Moralis, QuickNode und Blockchain-Nodes.
- Free-Konto: **1 Scan**. Premium: **unbegrenzt**.

### 5. Shopping-Rewards: Member Rewards (MR)
Es gibt drei Wege, einen Kauf nachzuweisen:

| Weg | Plan | Status | Max. MR |
|---|---|---|---|
| **By Vow.id**: Beleg an `@vow.id` | Free | live | bis **10 %** |
| **By bank**: Plaid-Bankverknüpfung | Premium | live | bis **40 %** bei Featured Merchants, bis **100 %** bei Energierechnungen |
| **By link**: Shopping- und Referral-Links | – | „Coming soon“ | – |

Alle Prozentsätze sind Höchstwerte und keine Garantie. Pro Kauf gilt ein Cap von **500 MR** (Shopper-MR, nach Umrechnung in USD).

**Was MR sind:**
- MR sind kostenlose, **nicht übertragbare, an die Wallet gebundene** Smart-Contract-Einträge.
- Sie sind kein Geld, kein Token und kein Cashback.
- „Pending MR“ sind nur Vorschläge.

**Ablauf vom Kauf bis zum v$:**
1. **Vorschlag:** Vow.id reicht einen Vorschlag über eine von **4 autorisierten Proposer-Wallets** ein. Jeder Proposer hinterlegt VOW im Wert von 500 US$ als Sicherheit.
2. **Prüfung:** Unabhängige **Vow Verifiers** prüfen den Vorschlag. Die Regel ist „first-to-three“:
   - 3 gültige Approvals: Die MR werden genehmigt, und zwar atomar in der dritten Vote-Transaktion.
   - 3 Challenges: Der Vorschlag ist abgelehnt.
   - Begünstigter, dessen Referrer und der Proposer dürfen nicht mitstimmen.
3. **Verifier-Belohnung:** Bei Genehmigung bekommen drei Verifier aus der Warteschlange je 0,33 MR.
4. **Challenges:** Wer challengt, hinterlegt VOW im Wert von 10 US$. Nach 3 Challenges prüfen die drei anderen Proposer den Fall. Mindestens 2 von 3 müssen die Challenge bestätigen. Das Ergebnis regelt nur die Einsätze; die ursprüngliche Abstimmung wird dadurch nicht umgekehrt.
5. **Einlösung („Exercise“):** Genehmigte MR können **innerhalb von 60 Tagen** eingelöst werden. Danach verfallen sie.
   - 1 MR plus ein VOW-Beitrag im Wert von 50 % des Marktwerts von v$1 ergibt 1 **v$** (Voucher Dollar).
   - Der Marktwert kommt aus dem Chainlink-Preisfeed.
   - Vom eingezahlten VOW werden 20 % verbrannt, 80 % gehen an die Contract-Treasury.
   - Der Beitrag ist endgültig und wird nicht zurückgezahlt.
6. **v$:** v$ ist ein übertragbares digitales Recht, einen **Rabatt von 1 $** anzubieten oder anzunehmen.
   - Es ist nicht durch Vermögenswerte gedeckt und nicht in Geld einlösbar.
   - Niemand ist verpflichtet, v$ anzunehmen.

**Datenschutz und Nachweis:** Die Kaufnachweise bleiben off-chain. On-chain steht nur ein **gesalzenes Keccak-256-Commitment**. Verifier gleichen es im Browser mit den Nachweisen ab. On-chain liegen außerdem Wallet-Adressen, MR-Zuteilungen, Verifier-Entscheidungen und Zeitstempel. Diese Daten sind pseudonym, nicht anonym, und lassen sich nicht löschen.

**Deduplizierung:**
- Der erste gültige Claim für eine Kombination aus Händler und Referenz gewinnt, auch über verschiedene Nutzer hinweg.
- Beleg und Banktransaktion zählen pro Kauf nur einmal. Abgeglichen werden Händler, Betrag und Datum innerhalb von ±5 Tagen; bei Fremdwährung ±5 % auf den USD-Wert.

### 6. Verifier-Rollen und Staking
- **VV (Vow Verifier):** VOW-Lock im Wert von 500 bis unter 10.000 US$.
- **QVV:** VOW-Lock von genau 10.000 US$ (Obergrenze pro Wallet).
- Lock-Dauer: **1.000 Tage**. Jeder Top-up setzt die Frist für die ganze Position neu. Weitere Top-ups mindestens 100 US$.
- Vorzeitiger Ausstieg ist nicht möglich. Bei Fälligkeit kommt dieselbe Token-Menge zurück, nicht der ursprüngliche USD-Wert.
- Für Downline-Berechtigung muss man in einem rollierenden 30-Tage-Fenster an Verifikationen teilnehmen.

### 7. Decentralised Affiliate Tree (Referral)
- Der Referral-Pool beträgt als Richtwert **0,5 % des qualifizierenden Umsatzes**, aufgeteilt auf 10 Ebenen:
  - VV-Wallets qualifizieren für Ebene 1–3.
  - QVV-Wallets qualifizieren für Ebene 4–10.
- Der Beitritt ist kostenlos (nur Netzwerkgebühr). Der Referrer wird beim Beitritt festgelegt und ändert sich nicht mehr.
- Qualifizierung:
  - Free: ein gültiger Beleg.
  - Premium: eine verifizierte Premium-Zahlung plus Beleg oder positiver Bankkauf.

## Preise

| Plan | Preis | Inhalt |
|---|---|---|
| **Free** | 0 € | Identität, Vault, `@vow.id`-Belege (bis 10 % MR), 1 Wallet-Scan |
| **Premium** | **99 US$/Jahr**; Launch-Angebot: **49 US$ im ersten Jahr** bei Beitritt bis 31.12.2026 | Bankverknüpfung via Plaid, bis 40 %/100 % MR, unbegrenzte Wallet-Scans |

- Kartenzahlung über **Stripe** mit automatischer jährlicher Verlängerung. Kündigung über das Billing-Portal.
- Alternativ **USDC**: 12 Monate ohne automatische Verlängerung.
- v$, v€, v£ und VOW werden als Zahlungsmittel **nicht** akzeptiert.
- Laut Vow.id ist die Premium-Gebühr „kein Preis für MR“.

## VOW-Ökosystem

| Dienst | Zweck |
|---|---|
| **Vow.id** | Identität, Vault, Rewards (dieser Artikel) |
| **Vow.Market** (vow.market) | E-Commerce und Marktplatz mit Krypto-Checkout |
| **Vow.Community** (vow.community) | P2P-Marktplatz zum Tausch von Skills und Services gegen Vow-Währungen |
| **Vowhotels** (vowhotels.com) | Hotelbuchung mit vCurrency direkt aus der Wallet |
| **Vowchers** (vowchers.com) | Rabattkapazität monetarisieren, digitale Rabatt-Voucher on-chain |
| **VOW Ecosystem** (vowecosystem.com) | Dachseite; eine Vow-ID für alle VOW-Sites |

Für Ökosystem-Betreiber gibt es eine Partner-API:
- Wallet-Sign-in der Kunden, Präferenzen, private Nachrichten und Mailingliste, ohne dass der Partner Kunden-E-Mails sammelt.
- Authentifizierung über `x-vow-api-key` (nur serverseitig), z. B. `POST https://vow.id/api/public/preferences`.
- Doku unter `/documentation`, Bewerbung über `/partners`.

## Dienstleister (laut Datenschutzerklärung)

Lovable Cloud (Hosting), Resend (E-Mail), Reown/WalletConnect, OpenAI und Lovable AI Gateway (Belegextraktion), **Plaid** (Bank), Stripe (Zahlung), Freename (Domains), CJ, Printful und Paketdienste (Fulfillment), Moralis und QuickNode (Blockchain-Daten), Meta- und Google-Pixel (nur nach Consent), Google Fonts.

## Aufbewahrung (Auszug)

| Daten | Frist |
|---|---|
| Konto, Vault, Belege | Solange das Konto besteht; Löschung innerhalb von 30 Tagen nach bestätigter Schließung |
| Plaid-Token und Banktransaktionen | Solange die Bank verknüpft ist; Entfernung beim Trennen oder bei Kontoschließung |
| App-Logs | 90 Tage |
| E-Mails an privacy@ und security@ | 2 Jahre |
| Geschlossenes Konto (HMAC-SHA-256-Fingerprint der Wallet), Premium-Zahlungsbuchhaltung | 6 Jahre |
| On-chain-Daten | dauerhaft, nicht löschbar |

## Risiken und Einordnung (eigene Zusammenfassung)

- **Vow.id verspricht keine Gegenleistung:** Nichts ist garantiert, weder MR-Genehmigung, Rabatt-Akzeptanz noch v$-Wert oder Liquidität. MR haben ohne VOW-Beitrag keinen Nutzen.
- **Krypto-Einsatz nötig:** Um MR einzulösen, muss man VOW kaufen und dauerhaft abgeben. Die AGB warnen ausführlich vor Markt-, Liquiditäts- und Smart-Contract-Risiken.
- **Regulierung:** Vow.id stuft MR als außerhalb von UK-Finanzwerbung, MiCA und US-Wertpapierrecht ein. Das ist Vow.ids eigene Einschätzung und **keine** Entscheidung einer Behörde. VOW und v$ müssen nach eigener Aussage gesondert bewertet werden.
- **Datenschutz:** Die Verschlüsselung ist serverseitig und nicht zero-knowledge. Belegtexte gehen an OpenAI in den USA. On-chain-Spuren sind pseudonym und dauerhaft.
- Das Produkt ist als **Beta** gekennzeichnet.
