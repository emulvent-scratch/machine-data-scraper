# Vow.id – kritische Einschätzung (für Oli)

> Stand: 24.11.2026. Grundlage sind die anonymisierte Auswertung unserer Gruppenfragen (`../Onboarding/gruppenfragen-auswertung.md`) sowie die Wiki-Seiten [Vow.id](./vow-id.md), [Plaid-Bankverknüpfung](./vow-id-plaid-bankverknuepfung.md) und [Wirtschaft und Einwände](./vow-id-wirtschaft-und-einwaende.md). Quellen dort: AGB, Datenschutzerklärung und Dokumentation von vow.id (20.11.2026), Premium-Aufklärung (22.11.2026), Registerdaten, BaFin-Meldung, Berichte zum Hack von 2024 und Beobachtungen aus unserer Gruppe. Das ist eine eigene Einschätzung und keine Anlage- oder Rechtsberatung.
>
> Vorweg: Fast alle Produktangaben stammen vom Betreiber selbst. Ein unabhängiges Audit, geprüfte Zahlen oder eine Behördenentscheidung liegen nicht vor.

## Das Ergebnis in fünf Sätzen

1. Vow.id ist kein Cashback. Für Einkäufe gibt es MR, also Rechte. Wer sie in v$ umwandelt, muss VOW einzahlen und erhält neu erzeugte Rabattgutscheine.
2. Was sich davon heute in echtes Geld umrechnen lässt, ist klein: bei Energie rund 11 % des Rechnungsbetrags, bei Shops rund 4 %, im kostenlosen Konto rund 1 %. Jeweils vor Gebühren und nur, wenn alles funktioniert.
3. Der entscheidende Schritt läuft noch gar nicht. Die Prüfung durch die Verifizierer ist nicht aktiv, und niemand aus der Community hat MR bisher real in v$ umgewandelt.
4. Hinter dem Produkt steht eine im September 2026 gegründete Ein-Personen-Firma mit Briefkastenadresse. Das Ökosystem hat eine belastete Vorgeschichte: BaFin-Ermittlung 2024 und ein Hack mit rund 80 % Kurseinbruch.
5. Meine Empfehlung: kostenlos testen, kein Geld einsetzen und niemanden aktiv werben, bis der ganze Weg einmal nachweislich funktioniert hat.

## 1. Die Wirtschaftlichkeit, nüchtern gerechnet

Mit den Kursen vom 22.11.2026 (v$ ≈ 0,21 $, VOW ≈ 0,031 $):

Pro MR zahlt man VOW im Wert von 50 % des v$-Kurses ein und bekommt 1 v$. Der realisierbare Gewinn liegt damit immer bei **MR × 0,5 × v$-Kurs**, vor Netzwerkgebühren, Tauschkosten und Kursverlust zwischen Einzahlen und Verkaufen.

| Fall | MR je 100 $ Umsatz | Gewinn beim Tausch | Premium (49 $) hereingeholt ab |
|---|---|---|---|
| Kostenloses Konto, Beleg an @vow.id | bis 10 | ≈ 1 $ | – (keine Gebühr) |
| Premium, Shops (Featured) | bis 40 | ≈ 4 $ | ≈ 1.200 $ Umsatz bei gelisteten Shops |
| Premium, Energie | bis 100 | ≈ 10,5 $ | ≈ 470 $ Energiekosten, **wenn die Lastschrift überhaupt erkannt wird** |

Ab dem zweiten Jahr kostet Premium 99 $, die Schwellen verdoppeln sich also.

Was dazu kommt:
- **Alle Sätze sind Höchstwerte.** Vow.id darf sie für künftige Käufe ohne Ankündigung ändern.
- **Ob Energie zählt, ist offen.** In unserer Gruppe hat die Abbuchung eines gelisteten Stadtwerks keine MR ergeben. Strom wird meist per Lastschrift bezahlt, die Einwilligung spricht aber von Kartenzahlungen. Damit ist die stärkste Werbeaussage („bis 100 % auf Energie“) derzeit nicht belegt.
- **Den v$-Wert gibt der Markt vor.** Jedes Ausüben erzeugt neue v$. Verkaufen viele, fällt der Kurs. Der Markt ist dünn: Am 22.11.2026 lagen im v$-Pool auf der BNB Smart Chain rund 1,1 Mio. $ Liquidität bei nur etwa 52.000 $ Tagesumsatz (VOW: 2,3 Mio. $ Liquidität, 219.000 $ Umsatz; v£: 674 $ Umsatz). Schon ein paar Hundert Mitglieder, die ihre v$ gleichzeitig verkaufen, würden den Kurs spürbar drücken.
- **Der „volle“ Wert von 1 $ je v$** gilt nur als Rabatt bei Händlern, die v$ annehmen. Das ist vor allem Vow.Market, und das gehört derselben Firma wie vow.id. Im Code von Vow.Market gibt es eine Stelle, die Preise bestimmter Lieferantenprodukte verdoppelt. Ohne Preisvergleich ist der Rabatt nichts wert.
- **Vow.id nimmt seine eigene Währung nicht an.** Premium ist seit dem 22.11.2026 nur noch per Karte, USDC oder USDT zu bezahlen, nicht mit v$ oder VOW. Interessenten lesen das als Misstrauen des Systems gegenüber dem eigenen Token. Der Einwand ist berechtigt.
- **60 Tage Frist.** Genehmigte MR verfallen, wenn sie nicht rechtzeitig ausgeübt werden.

## 2. Was noch nicht funktioniert

| Baustein | Stand |
|---|---|
| Registrierung, Belegadresse, Bankverknüpfung, Wallet-Scan | läuft, Bank je nach Institut wackelig |
| Einkäufe als „ausstehende MR“ erfassen | läuft |
| Prüfung durch Verifizierer | **nicht aktiv**, Contract „in Kürze“ (Screenshot ohne Datum) |
| MR in v$ umwandeln | **noch nie real gesehen** |
| Verifier-Rollen (VV/QVV) und damit Referral-Erträge | „Coming soon“ |
| v$ bei vowhotels und vowchers | „in Kürze“ |

Wir sehen heute also nur Zahlen in einer App. Ausstehende MR sind laut Vow.id ausdrücklich „nur Vorschläge“ und werden möglicherweise nie genehmigt. Auch unsere eigenen Werber sagen in der Gruppe, die erste echte Umwandlung wäre das „Sahnehäubchen“.

## 3. Wer dahinter steht

- **Betreiber:** N888 LIMITED, London. Gegründet am 2.9.2026, ein Direktor und Alleineigentümer (Pál Teleky). Adresse 20 Wenlock Road, unter der rund 29.000 Firmen gemeldet sind. Keine Abschlüsse, keine Umsätze, keine Mitarbeiterzahl.
- **Haftung:** Bei einer so jungen Limited ohne Geschäftshistorie ist im Streitfall wenig zu holen.
- **Aufsicht:** Keine FCA-Zulassung. Dass MR nicht unter Finanzaufsicht fallen, ist die eigene Einschätzung von Vow.id und keine Behördenentscheidung.
- **Technik:** Gehostet auf Lovable Cloud, einer Plattform, mit der man Apps per KI-Baukasten erstellt. Das ist für eine Beta legitim. Für eine Anwendung, die Bankdaten, Reisepassnummern und Wallets verwaltet, ist es aber ein Punkt, nach dem man fragen sollte (Sicherheitsprüfung, Penetrationstest).

## 4. Die Vorgeschichte des VOW-Ökosystems

- **BaFin, 7.3.2024:** Ermittlungen gegen Vow Limited und die „Vow App“ wegen des Verdachts unerlaubter Bank- oder Finanzgeschäfte. Ein Abschluss ist nicht bekannt. Formal betrifft das nicht N888. vow.id baut aber auf VOW und v$ auf, also auf genau diesem Ökosystem.
- **Hack, 13.8.2024:** Beim Testen auf der Live-Chain wurde der Umrechnungskurs falsch gesetzt. Ein Angreifer erzeugte massenhaft v$, Schaden rund 1,2 Mio. $, Kurs zeitweise etwa −80 %. Vow.id sagt, die neuen Verträge seien unveränderlich und ohne Admin-Schlüssel. Ein Audit dazu liegt uns nicht vor.
- **Ältere Engagements hängen.** In unserer Gruppe fragt eine Langzeit-Halterin, die vor rund drei Jahren Geld in den „VOW Tresor“ gegeben hat, warum dort „gar nichts mehr läuft“. Ein Mitglied berichtet (Hörensagen), eine 82.000-$-Position im VOW/v$-Pool sei seit 1.9. auf rund 30.000 $ gefallen. Wer schon in VOW steckt, wird Olis Frage „warum diesmal?“ selbst stellen.
- **v$ steht bei 0,21 $ statt 1 $.** Der ursprüngliche Anspruch eines Gutscheins im Wert von einem Dollar hat sich am Markt nicht gehalten.
- **Die Aussage „Vow Limited ist eine australische Firma ohne Bezug zum Token“** ist nicht belegt. Whitepaper und Kanzleibericht nennen Vow Limited als Herausgeber des VOW-Tokens. Wir sollten das Argument nicht verwenden.

## 5. Der Interessenkonflikt, offen gesagt

Wer VOW hält oder im TLN-Pool steckt, profitiert, wenn andere über vow.id VOW kaufen müssen. 20 % jedes Beitrags werden vernichtet, 80 % gehen in eine Contract-Kasse, deren Verwendung nicht beschrieben ist.

Das gilt auch für mich: Meine Anleitungen enthalten meinen eigenen Einladungslink. Wer über mich einsteigt, steht dauerhaft in meinem Empfehlungsbaum. Das soll Oli wissen, bevor er meine Einschätzung liest.

Das heißt nicht, dass vow.id nur dafür gebaut ist. Es heißt aber: Wer aus dem TLN-Umfeld vow.id empfiehlt, sollte damit rechnen, dass ein kritisches Gegenüber genau das unterstellt. Und an bestehenden Positionen im Minus ändert vow.id nichts. Zum Ausüben braucht man zusätzliches VOW.

## 6. Daten und Sicherheit

- **Der Vault ist nicht zero-knowledge.** Die Verschlüsselung läuft serverseitig, Personal und Serverfunktionen können entschlüsseln. Das sagt Vow.id selbst.
- **Belegtexte gehen an OpenAI in den USA.** Laut Vow.id keine Anhänge und keine Bankdaten.
- **Bank:** Die Verbindung ist nur lesend und lässt sich trennen. Bei Volks- und Raiffeisenbanken gibt man VR-NetKey und PIN im Plaid-Fenster ein, die Zugangsdaten gehen also an Plaid. Ob in der EU ein lizenzierter Kontoinformationsdienst dazwischen sitzt, ist nicht dokumentiert. In der Gruppe tauchten fremde Transaktionen in einem Konto auf. Mehrere Mitglieder haben Premium doppelt bezahlt.
- **Die Erfassung ist unzuverlässig.** Bei Amazon wurde von zwei Bestellungen nur eine erkannt. Temu-Bestätigungen kamen nicht an. Erste Bank (Österreich), Salzburg AG und Schweizer Banken funktionieren laut Gruppe noch nicht.
- **Festlegungen sind endgültig.** Wallet, Empfehler und Handle lassen sich nach der Registrierung nicht mehr ändern. Geht die Wallet verloren, ist die Vow.id samt MR weg. Die Wiederherstellung über eine Backup-Wallet ist nur angekündigt.
- **On-chain-Spuren sind dauerhaft.** Wallet, MR-Zuteilungen und Abstimmungen lassen sich nicht löschen. Sie sind pseudonym, nicht anonym.

## 7. Empfehlungen und Strukturvertrieb

- Zehn Ebenen, ein Pool von 0,5 % des Umsatzes. Das sind 0,05 % je Ebene. Bei zehn Geworbenen mit zusammen 5.000 $ Monatsumsatz kommen etwa 2,5 MR im Monat zusammen, umgerechnet rund 0,25 $. Als Einkommen ist das bedeutungslos, und die nötigen Verifier-Rollen sind noch nicht freigeschaltet.
- Das eigentliche Risiko trägt der Werber selbst: Wer „Cashback“, „100 %“ oder „Einkommen“ sagt und Freunde zu Premium und VOW-Käufen bringt, haftet mit seinem Ruf. Unter Umständen auch rechtlich, etwa bei irreführender Werbung.

## 8. Was ehrlich für Vow.id spricht

- Das kostenlose Konto kostet nichts außer Daten und Zeit.
- Die AGB sind ungewöhnlich offen. Kein Geld, kein Cashback, keine Garantie, ausführliche Risikohinweise. Versprochen wird nichts.
- Die Bankverbindung ist nur lesend und freiwillig.
- Die Erfassung funktioniert grundsätzlich. Belegte Beispiele aus der Gruppe: Spotify 12,99 € ergab 5,82 MR (40 %, über die Bank), Booking.com 640 C$ ergab 185,95 MR in Kanada. Alles davon ist noch „ausstehend“.
- Die Belegadresse und der Wallet-Scanner sind für sich genommen nützliche Funktionen.
- Der Ansatz, Händler-Rabatte statt ausgedachter Renditen zu verteilen, ist als Idee nachvollziehbar und kein klassisches Schneeballsystem. Ob er trägt, hängt aber allein davon ab, ob Händler v$ annehmen und Käufer v$ wollen.

## 9. Drei Szenarien

| Szenario | Was passiert | Folge für uns |
|---|---|---|
| **Schlecht** | Verifizierung kommt spät oder gar nicht. Oder v$ fällt durch viele Verkäufe weiter. | Free-Nutzer verlieren nur Zeit. Premium-Käufer verlieren die Gebühr. Werber verlieren Glaubwürdigkeit. |
| **Mittel (wahrscheinlich)** | Ausüben funktioniert, aber holprig. Energie per Lastschrift wird nur teilweise erkannt. v$ bleibt zwischen 0,10 und 0,25 $. | Ein paar Prozent Rabatt auf Einkäufe, viel Handarbeit. Premium lohnt sich nur für Vielkäufer. |
| **Gut** | Alles läuft, weitere Händler nehmen v$ an, die Nachfrage hält den Kurs. | Spürbarer Rabatt, vor allem bei Energie. Erst dann wäre es seriös, aktiv zu empfehlen. |

## 10. Mein Vorschlag, wie wir vorgehen

1. **Kostenlos registrieren** und die @vow.id-Adresse bei zwei, drei Shops hinterlegen. Kein Geld einsetzen.
2. **Premium nur, wenn** feststeht, dass die eigene Bank verbindet und der eigene Energieversorger per Lastschrift erkannt wird. Am besten wartet man auf Berichte anderer.
3. **Kein VOW kaufen,** bevor nicht mindestens ein Mitglied die ganze Kette nachweislich durchlaufen hat: genehmigte MR → v$ → verkauft oder bei Vow.Market eingelöst, mit Transaktions-Hash.
4. **Nicht aktiv werben,** solange Punkt 3 offen ist. Danach nur mit ehrlicher Sprache: MR, Rabattgutscheine, Experiment. Nie Cashback oder Einkommen.
5. **Ausstiegskriterien festlegen:** Ist die Verifizierung bis zu einem festen Datum (zum Beispiel 31.1.2027) nicht aktiv, nehmen wir es als Warnsignal und empfehlen nichts weiter.

## Fragen, die Vow vorher beantworten sollte

- Wann genau startet die Verifizierung, und wo ist der Contract (Adresse, Audit)?
- Werden Lastschriften für Energie erkannt, ja oder nein?
- Wofür wird die Contract-Kasse verwendet (80 % der VOW-Beiträge)?
- Wie hängen N888 LIMITED und Vow Limited zusammen, und wie ist der Stand des BaFin-Verfahrens?
- Gibt es einen Sicherheitstest der App, die Bankdaten verarbeitet?
- Welcher lizenzierte Kontoinformationsdienst sitzt in der EU zwischen Plaid und der Bank?
- Wie viele v$ sind im Umlauf, und wie viel Nachfrage steht dem gegenüber?
