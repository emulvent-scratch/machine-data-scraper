# Vow.id

> Stand: 23.11.2026 (Erstfassung 22.11.2026). Quellen: Website https://vow.id (Startseite, `/documentation`, `/terms`, `/privacy`; AGB und Datenschutzerklärung jeweils „Last updated · 20 November 2026“). Die Seite ist eine Single-Page-App; die Texte stammen aus den ausgelieferten JS-Bundles der Seite. Die Website führt Vow.id als **Beta**.
>
> Weitere Quellen seit der Erstfassung: „New User Overview" (Ausgabe 11 vom 21.11.2026), die Aufklärung für Premium-Mitglieder (Ausgabe 2026-11-22.2), die Seite vow.market und Beobachtungen aus der Community. Was nur auf Beobachtungen beruht, ist so gekennzeichnet.
>
> Weitere Seiten: [Plaid-Bankverknüpfung](./vow-id-plaid-bankverknuepfung.md) · [Wirtschaftliche Einordnung und häufige Einwände](./vow-id-wirtschaft-und-einwaende.md)

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
- Manuelle Beleg-Uploads sind laut AGB nicht möglich. Die „New User Overview" (Ausgabe 11) nennt dagegen eine private Foto-Einreichung für fehlende Belege, bei der man den Dienst auswählt; ein Foto wird geprüft und nicht automatisch gutgeschrieben. Die beiden Quellen widersprechen sich hier.
- Die Adresse ist laut Vow.id **keine verlässliche Adresse für Passwort-Rücksetzungen**. Erkannte Sicherheits-Mails anerkannter Shops werden weitergeleitet, andere Absender abgewiesen. Deshalb nie bei Google, Apple, Microsoft oder der Bank eintragen.

### 4. Wallet Security (Permission-Scanner)
- Scannt **Ethereum, BNB Smart Chain, Polygon, Arbitrum, Base und Optimism**. Standardmäßig laufen ETH und BSC, die vier anderen Netze sind „einen Tap entfernt“. Solana wird nur geprüft, wenn man eine Solana-Adresse angibt.
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
- Alternativ **USDC oder USDT**: 12 Monate ohne automatische Verlängerung. (USDT nennt die „New User Overview", Ausgabe 11.)
- Ein befristetes Angebot, Premium mit v$ zu bezahlen, endete am 22.11.2026 um 23:59 Uhr.
- Einen Monatsplan gibt es nicht. Laut Premium-Aufklärung „können" Beta-Einführungspreise für berechtigte Mitglieder verfügbar sein; maßgeblich ist der Preis im Checkout.
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

## Stand der Umsetzung (23.11.2026)

| Funktion | Stand |
|---|---|
| Registrierung, Vault, Handle, `@vow.id`-Belege | live |
| Bankverknüpfung für Premium | live, je nach Bank und Land unterschiedlich zuverlässig |
| Wallet-Scan | live |
| Erfassung von Einkäufen als „Ausstehende MR" (Pending) | live |
| **Prüfung durch Verifizierer („Verify"/„Challenge")** | **noch nicht aktiv.** Laut einer Mitteilung von Vow.id wartet sie auf den Verifizierungs-Contract, „Bereitstellung in Kürze". Die Mitteilung ist nur als Screenshot ohne Datum bekannt. |
| MR ausüben (in v$ umwandeln) | folgt erst nach der Prüfung; bisher hat das niemand in der Community real durchgeführt |
| Verifier-Rollen (VV/QVV) | „Coming soon" |
| On-Chain-Namen und Wiederherstellung über Backup-Wallet | angekündigt |
| v$ einsetzen bei Vow.Market | laut Seite möglich, kein Testkauf durchgeführt |
| v$ einsetzen bei vowhotels.com und vowchers.com | laut Community „in Kürze" |

Vow.id sichert unveröffentlichte Funktionen ausdrücklich nicht zu.

## Offizielle deutsche Begriffe

| App / englisch | Deutsch (Premium-Aufklärung) |
|---|---|
| Pending MR | Ausstehende MR |
| Active / Approved MR | Genehmigte MR |
| Claim MR / Exercise | MR beanspruchen / ausüben |
| Verifier | Verifizierer |

## Kurse und Rechenbeispiel (22.11.2026, BNB Smart Chain)

Kurse laut Screenshot einer Kurs-App: VOW 0,0309 $ · v$ 0,2065 $ · v£ 0,2196 $.

- Der VOW-Beitrag beim Ausüben beträgt **50 % des aktuellen Marktwerts des zu erhaltenden v$**, pro MR. Die Premium-Aufklärung bestätigt diese Lesart wörtlich. Es sind nicht 50 % von einem Dollar.
- Beispiel: 10 MR ausüben kostet VOW im Wert von etwa 1 $. Die 10 v$ sind an der Börse etwa 2 $ wert oder zählen bei Vow.Market als 10 $ Rabatt.
- Offen: ob der Chainlink-Kurs des Protokolls dem Börsenkurs entspricht.

## Vow.Market (eigene Prüfung der Seite, 22.11.2026)

- Betreiber laut Fußzeile: N888 LIMITED, wie bei Vow.id.
- „Use each v$ to enjoy a $1 discount", bei vielen Produkten „100% off with v$". Laut Bedingungen gilt die Rabattgrenze, die beim Produkt steht.
- Ohne v$: Zahlung mit USDT oder USDC, dafür 20 % zurück in v$.
- v$ sind dort kein gesetzliches Zahlungsmittel und nicht in Geld einlösbar. Bei Rückgabe werden sie dem Konto gutgeschrieben.
- Nach eigener Angabe über 75.000 Produkte, weltweiter Versand; Versandkosten werden getrennt berechnet.
- Im Code gibt es eine Stelle, die Preise bestimmter Lieferantenprodukte verdoppelt. Wofür genau, ist nicht geklärt. Preise vor einer Empfehlung mit anderen Shops vergleichen.

### Token-Adressen (aus dem Code von vow.market; deckt sich mit der Liste „Token hinzufügen" in Vow.id)

| Token | BNB Smart Chain | Ethereum |
|---|---|---|
| v$ (Vow Dollar) | `0x9C23942Ca2C35e06d1d20747F33705983A18d2AB` | `0xba7fe208e0167e4047a996e1efea830515f433f8` |
| v€ (Vow Euro) | `0x3745e245612f130B57589688060454A8ae43276C` | `0x448fa53be5b9f792d6f799428df8d4c89eb9f04a` |
| v£ (Vow Pound) | `0x6eA1734DF1627453DaA6834776CB0403ABC401b1` | `0x72bf018df20fbacf542f5ec159c6a7f0d7850967` |
| vkr (Vow Kroner, „vDK") | – | `0x40a07abd0da20d9ec859c564727c10ce5cb7600e` |
| v₹ (Vow Rupee) | – | `0x047128bf54f643403864cb37a5df134e3ecf1bf4` |
| v$ Australien | – | `0x547649976443cd3b6ad8c9781f17f8ad6f061f2f` |
| vR (Vow Rand) | – | `0xc669b1920bb901292c11020d27d1bf7168e49eac` |

Der VOW-Token selbst steht in keiner der beiden Listen. Seine Adresse auf der BNB Smart Chain ist laut Angabe des Nutzers (23.11.2026) `0xF585B5b4f22816BAf7629AEA55B701662630397b`. Sie ist nicht aus einer Betreiberquelle belegt und konnte nicht über BscScan geprüft werden (Bot-Sperre).

Weiterhin ohne Zuordnung: `0x6B27bB584F44f55E865432dCeb9eBBE9A17fd4A8`, `0x8B0B4C7878623DB8e5E6cB9bd0FA85C07C3B85f1`.

## Aufklärung für Premium-Mitglieder (Ausgabe 2026-11-22.2)

Premium-Mitglieder müssen in der App zehn Punkte einzeln bestätigen. Preis, Verlängerungsdatum und Vertrag ändern sich dadurch nicht. Die wichtigsten Aussagen:

- MR sind „kein Cashback, kein Bargeld, keine Token" und haben keinen Barwert. Ausstehende MR werden möglicherweise nie genehmigt.
- Premium garantiert nicht, dass die eigene Bank unterstützt wird oder sich verbinden lässt. In der App gibt es Listen zur Bankabdeckung des Anbieters (USA, EU) als CSV; auch ein Eintrag dort ist keine Garantie.
- Im Abo ist kein VOW enthalten. Das Ausüben ist freiwillig; niemand ist verpflichtet, VOW zu kaufen.
- Beworbene Sätze können sich für künftige Käufe ohne Ankündigung ändern. Bereits genehmigte MR werden nicht gekürzt.
- **Regeln fürs Weiterempfehlen:** keine Logos oder Markenbilder Dritter; Händler darf man beim Namen nennen und eigene Erfahrungen schildern, aber keine Partnerschaft oder Förderung andeuten.
- Herkunft der MR: vom Händler unterstützt, von der Community unterstützt oder beides. Vow.id schlägt vor und genehmigt nicht selbst.

## Abdeckung und Teilnahme

- Mindestalter 18 Jahre und Geschäftsfähigkeit. Ob sich Firmen registrieren dürfen, regeln die AGB nicht ausdrücklich.
- Kategorien in der Checkliste: Shops, Energie, Mobilfunk, Internet, Streaming, Lieferdienste, Reisen, KI-Dienste. Versicherungen und Tankstellen werden nicht genannt.
- Für Deutschland, Österreich und Spanien sind laut Ausgabe 11 weitere Energieversorger und deutsche Stadtwerke dazugekommen.
- Aus der Schweiz und aus Bulgarien berichten Mitglieder, dass Banken und Anbieter fehlen. Einen Zeitplan für weitere Länder (auch Süd- und Mittelamerika) gibt es nicht; der Ausbau richtet sich laut Vow.id nach Anfragen über „Contact".
- Beobachtung aus der Community: Vereinzelt werden nicht gelistete Händler erkannt, und manche gelisteten funktionieren noch nicht. Belege erscheinen teils erst am Folgetag, einzelne gar nicht.

## Referral in Zahlen

Der Richtwert von 0,5 % des qualifizierenden Umsatzes verteilt sich auf zehn Ebenen, also 0,05 % je Ebene. Zehn direkt Geworbene mit zusammen 5.000 $ Monatsumsatz bei gelisteten Anbietern ergeben auf der ersten Ebene rund 2,5 MR im Monat. Voraussetzung sind VV- oder QVV-Status und aktive Prüfer-Teilnahme; die Rollen sind noch nicht freigeschaltet. Der einmalige MR-Betrag je geworbener Person ist ein in der App eingestellter Wert und hier nicht bekannt.

## Onboarding-Material

Aus diesem Wiki abgeleitet, im Ordner `../Onboarding/`: Komplettanleitung, Starthilfe, Einsteiger-Seite, WhatsApp-Vorlagen und die anonymisierte Auswertung der Gruppenfragen.

## Risiken und Einordnung (eigene Zusammenfassung)

- **Vow.id verspricht keine Gegenleistung:** Nichts ist garantiert, weder MR-Genehmigung, Rabatt-Akzeptanz noch v$-Wert oder Liquidität. MR haben ohne VOW-Beitrag keinen Nutzen.
- **Krypto-Einsatz nötig:** Um MR einzulösen, muss man VOW kaufen und dauerhaft abgeben. Die AGB warnen ausführlich vor Markt-, Liquiditäts- und Smart-Contract-Risiken.
- **Regulierung:** Vow.id stuft MR als außerhalb von UK-Finanzwerbung, MiCA und US-Wertpapierrecht ein. Das ist Vow.ids eigene Einschätzung und **keine** Entscheidung einer Behörde. VOW und v$ müssen nach eigener Aussage gesondert bewertet werden.
- **Datenschutz:** Die Verschlüsselung ist serverseitig und nicht zero-knowledge. Belegtexte gehen an OpenAI in den USA. On-chain-Spuren sind pseudonym und dauerhaft.
- Das Produkt ist als **Beta** gekennzeichnet.
- Die ausführliche Einordnung mit Rechenbeispielen und den häufigsten Einwänden steht unter [Wirtschaftliche Einordnung und häufige Einwände](./vow-id-wirtschaft-und-einwaende.md).

## Best Practices für Belege (Text aus der App, übermittelt vom Nutzer am 25.11.2026, am Ende abgeschnitten)

1. Weiterleitungs-E-Mail verifiziert halten; normalen Posteingang und Spam auf zugestellte Kopien prüfen.
2. E-Mail-Adresse direkt beim Dienst ändern. Der Dienst muss Originalbelege an die @vow.id-Adresse senden; persönliche Weiterleitungen sind keine authentifizierten Händlerbelege.
3. Tatsächliche Von-Adresse prüfen. Anzeigename oder Belegfoto beweisen den Absender nicht.
4. Originalrechnung aufbewahren (Betrag, Währung, Kaufdatum, Bestellreferenz). Rechnungen von Apple und Google Play können den zugrunde liegenden Dienst identifizieren.
5. Nie Passwörter oder Anmeldecodes hochladen; vollständige Kartennummern und irrelevante Daten vor dem Einreichen eines Fotos abdecken.
6. Fehlenden Absender zur Überprüfung melden. Auch ein erkannter Absender braucht E-Mail-Authentifizierung; eine Genehmigung garantiert keine MR (Rest fehlt).

Folgerung: Es gibt eine Foto-Einreichung für Belege. Wie sie gewertet wird, ist offen.

## Anbieterliste Deutschland, Auswahl (aus der App, übermittelt vom Nutzer am 25.11.2026)

Alle mit dem Vermerk „Premium erfasst dies automatisch" und Status „Tracking". Die Liste wird nach Angabe des Nutzers wöchentlich länger.

| Kategorie | Premium-Satz | Anbieter |
|---|---|---|
| Marketplaces | 40 % | Shein, Temu, eBay, AliExpress, Vinted, Zalando, Wayfair, Wish |
| Dienstprogramme (Energie) | 100 % | E.ON, EnBW, Vattenfall, Stadtwerke Düsseldorf, enercity, N-ERGIE, enviaM, E WIE EINFACH, Yello, GASAG, Naturstrom, Grünwelt Energie, Pfalzwerke, Lechwerke, WEMAG |
| Mobilfunk | 40 % | Deutsche Telekom, O2 Deutschland, Vodafone Deutschland |
| Lieferung nach Hause | 22,5 % | Uber Eats, Just Eat |
| Streaming | 40 % | Netflix, Amazon Prime Video, Spotify, YouTube Premium |
| KI-Abonnements | 40 % | ChatGPT, Claude, Google Gemini, Microsoft Copilot, Perplexity, Adobe Firefly, Runway |
| Supermärkte | 20 % | Lidl, Aldi, Edeka, Rewe, Kaufland, Netto, Penny |
| Cafés | 22,5 % | Starbucks, Costa Coffee, Dunkin, Tchibo, Espresso House, Coffee Fellows, Balzac Coffee |

Offen: Sätze im kostenlosen Konto je Kategorie; ob Amazon (Shop) in einer anderen Kategorie steht.
