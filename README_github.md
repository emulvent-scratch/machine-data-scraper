# emulvent® Machine Data Scraper

Automatischer Web-Scraper für Maschinenmodelle von DMG MORI, HAAS und GROB. Läuft wöchentlich via GitHub Actions und lädt Daten direkt zu WordPress.

---

## 🎯 Ziel

Maschinenmodelle automatisch von Hersteller-Websites scrapen und in WordPress speichern. Die Daten sind dann über REST-API für die emulvent® Produktkonfigurator-App verfügbar.

---

## 📋 Voraussetzungen

- GitHub-Account
- WordPress-Installation mit **emulvent Machine Data Plugin**
- Webhook-Token vom Plugin

---

## 🚀 Setup

### 1. Repository klonen

```bash
git clone https://github.com/emulvent/machine-data-scraper.git
cd machine-data-scraper
```

### 2. Secrets in GitHub konfigurieren

**Settings → Secrets and variables → Actions → New repository secret**

| Name | Wert |
|------|------|
| `WP_REST_URL` | `https://emulvent.de/wp-json` |
| `WP_WEBHOOK_TOKEN` | (vom WordPress Plugin kopieren) |

### 3. Workflow aktivieren

- Repo → Actions → "Scrape Machine Data" sollte sichtbar sein
- Automatisch lädt jeden Sonntag um 02:00 UTC

### 4. Manueller Test

- Actions → "Scrape Machine Data" → "Run workflow" → "Run"
- Logs beobachten

---

## 📁 Struktur

```
machine-data-scraper/
├── .github/workflows/
│   └── scrape-machines.yml          # GitHub Actions Workflow
├── scrapers/
│   ├── base_scraper.py              # Basis-Klasse
│   ├── dmg_mori.py                  # DMG MORI Scraper
│   ├── haas.py                      # HAAS Scraper
│   └── grob.py                      # GROB Scraper
├── requirements.txt                  # Python Dependencies
├── .gitignore                        # Git-Ignore
└── README.md                         # Diese Datei
```

---

## 🔧 Verwendung

### Lokal testen

```bash
# Dependencies installieren
pip install -r requirements.txt

# Token setzen
export WP_REST_URL="https://emulvent.de/wp-json"
export WP_WEBHOOK_TOKEN="dein-token-hier"

# Einzelnen Scraper ausführen
python scrapers/dmg_mori.py
```

### GitHub Actions anpassen

Datei `.github/workflows/scrape-machines.yml` bearbeiten:

```yaml
on:
  schedule:
    - cron: '0 2 * * 0'  # Sonntag 02:00 UTC
```

[Cron-Syntax Referenz](https://crontab.guru/)

---

## 📊 API-Endpunkte

Nach erfolgreichem Scraping sind Daten über REST-API verfügbar:

```bash
# Alle Modelle abrufen
curl https://emulvent.de/wp-json/machine-data/v1/models

# Scraper-Status abrufen
curl -H "Authorization: Bearer $TOKEN" https://emulvent.de/wp-json/machine-data/v1/scraper-status
```

---

## ⚠️ Fehlerbehandlung

| Problem | Lösung |
|---------|--------|
| **401 Unauthorized** | Token-Mismatch → Im WordPress Plugin überprüfen |
| **Keine Modelle gefunden** | CSS-Selectors in `scrapers/*.py` anpassen (Website-Struktur ändert sich) |
| **Workflow schlägt fehl** | Actions → Failed run → Logs ansehen |
| **Alte Modelle verschwinden** | Sie sind noch in WordPress, nur nicht im aktuellen Scraper → Manuell überprüfen |

---

## 🛠️ Scraper anpassen

Wenn eine Website-Struktur sich ändert:

1. Browser öffnen → DevTools (F12)
2. Inspect Element → CSS-Klassen/IDs notieren
3. In `scrapers/xyz.py` anpassen:
   ```python
   machine_links = soup.select('.neue-klasse, .machine-link')
   ```
4. Commit & Push
5. Nächster automatischer Run (oder manuell triggern)

---

## 📅 Schedule

- **Automatisch:** Jeden Sonntag um 02:00 UTC (03:00 CET)
- **Manuell:** GitHub UI → Actions → "Scrape Machine Data" → "Run workflow"

---

## 📞 Support

- Fehler-Logs: GitHub Actions
- Status-Check: WordPress Admin → Maschinenmodelle → Scraper-Setup
- API-Test: `curl https://emulvent.de/wp-json/machine-data/v1/models`

---

**emulvent® GbR**  
Haiger, Hessen  
info@emulvent.de
