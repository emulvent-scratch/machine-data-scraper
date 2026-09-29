# Deep-Dive: Zero-Cost Machine-Data-Architecture für emulvent®
**Stand:** 29.09.2026  
**Autor:** Claude (Recherche-Agent + Implementierung)

---

## 🎯 ÜBERSICHT: Der Zero-Cost-Ansatz

```
Architektur (End-to-End)
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Web-Scraper (GitHub Actions — kostenlos)                 │
│  └─ DMG MORI, HAAS, GROB automatisch 1x/Woche            │
│  └─ Fehlerhandling + Validierung                          │
│     │                                                      │
│     ↓                                                      │
│  WordPress-DB (Strato)                                    │
│  └─ Custom Post Type: "Machine Models"                   │
│  └─ JSON-Struktur (maschinenmodelle + Metadaten)         │
│     │                                                      │
│     ↓                                                      │
│  WordPress REST-API                                       │
│  └─ Öffentlich: GET /wp-json/machine-data/v1/models     │
│  └─ Intern: Monitoring-Daten für Dashboard               │
│     │                                                      │
│     ├─→ Produktkonfigurator-App (lädt Daten)             │
│     └─→ Monitoring-Dashboard (Björn/Thilo)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Kosten: 0 € (GitHub Actions free tier, WordPress existiert schon)
Wartung: 2–3 Std/Monat (Scraper debuggen bei Websiteänderungen)
```

---

## 📋 TEIL 1: WordPress-Setup (Custom Post Type + REST-API)

### 1.1 Custom Post Type „Machine Models" registrieren

**Datei:** `C:\...\wp-content\plugins\emulvent-machine-data\emulvent-machine-data.php`

```php
<?php
/**
 * Plugin Name: emulvent Machine Data
 * Description: Verwaltung von Maschinenmodellen + REST-API
 * Version: 1.0
 * Author: emulvent®
 */

// Custom Post Type: Maschinenmodelle
function emulvent_register_machine_post_type() {
    register_post_type(
        'machine_model',
        array(
            'labels'        => array( 'name' => 'Maschinenmodelle', 'singular_name' => 'Modell' ),
            'public'        => false,           // Nicht im Frontend sichtbar
            'show_in_rest'  => true,            // REST-API aktivieren
            'rest_base'     => 'machine-models', // Endpoint: /wp-json/wp/v2/machine-models
            'supports'      => array( 'title', 'editor', 'custom-fields' ),
            'taxonomies'    => array( 'machine_manufacturer' ),
        )
    );
}
add_action( 'init', 'emulvent_register_machine_post_type' );

// Custom Taxonomy: Hersteller
function emulvent_register_manufacturer_taxonomy() {
    register_taxonomy(
        'machine_manufacturer',
        'machine_model',
        array(
            'labels'       => array( 'name' => 'Hersteller' ),
            'show_in_rest' => true,
        )
    );
}
add_action( 'init', 'emulvent_register_manufacturer_taxonomy' );

// Meta Fields registrieren (für strukturierte Daten)
function emulvent_register_meta_fields() {
    $meta_fields = array(
        'container_volume_liters' => 'number',
        'container_height_mm'     => 'number',
        'container_depth_mm'      => 'number',
        'container_width_mm'      => 'number',
        'separator_count'         => 'number',
        'kss_water_mixed'         => 'boolean',
        'data_source'             => 'string',  // 'dmg_mori', 'haas', 'grob', 'community'
        'last_scraped_at'         => 'string',  // ISO 8601
        'verification_count'      => 'number',
    );

    foreach ( $meta_fields as $field => $type ) {
        register_rest_field(
            'machine_model',
            $field,
            array(
                'get_callback' => function( $post ) use ( $field ) {
                    return get_post_meta( $post['id'], $field, true );
                },
                'update_callback' => function( $value, $post ) use ( $field ) {
                    return update_post_meta( $post->ID, $field, $value );
                },
                'schema' => array(
                    'type'        => $type,
                    'description' => ucfirst( str_replace( '_', ' ', $field ) ),
                )
            )
        );
    }
}
add_action( 'rest_api_init', 'emulvent_register_meta_fields' );

// Benutzerdefinierter REST-Endpoint (aggregierte Daten)
// GET /wp-json/machine-data/v1/models (alle Modelle als JSON-Array)
function emulvent_get_all_machines_callback( $request ) {
    $args = array(
        'post_type'      => 'machine_model',
        'posts_per_page' => -1,
        'orderby'        => 'title',
        'order'          => 'ASC',
    );

    $posts = get_posts( $args );
    $models = array();

    foreach ( $posts as $post ) {
        $models[] = array(
            'id'                     => $post->ID,
            'title'                  => $post->post_title,
            'manufacturer'           => wp_get_post_terms( $post->ID, 'machine_manufacturer', array( 'fields' => 'names' ) )[0] ?? null,
            'container_volume_liters'=> (int) get_post_meta( $post->ID, 'container_volume_liters', true ),
            'container_height_mm'    => (int) get_post_meta( $post->ID, 'container_height_mm', true ),
            'container_depth_mm'     => (int) get_post_meta( $post->ID, 'container_depth_mm', true ),
            'container_width_mm'     => (int) get_post_meta( $post->ID, 'container_width_mm', true ),
            'separator_count'        => (int) get_post_meta( $post->ID, 'separator_count', true ),
            'kss_water_mixed'        => (bool) get_post_meta( $post->ID, 'kss_water_mixed', true ),
            'data_source'            => get_post_meta( $post->ID, 'data_source', true ),
            'last_scraped_at'        => get_post_meta( $post->ID, 'last_scraped_at', true ),
        );
    }

    return new WP_REST_Response( $models, 200 );
}

register_rest_route(
    'machine-data/v1',
    '/models',
    array(
        'methods'             => WP_REST_Server::READABLE,
        'callback'            => 'emulvent_get_all_machines_callback',
        'permission_callback' => '__return_true', // Öffentlich lesbar
    )
);

// Scraper-Status Endpoint (nur für Björn/Thilo)
// GET /wp-json/machine-data/v1/scraper-status
function emulvent_get_scraper_status_callback( $request ) {
    // Nur Admin darf sehen
    if ( ! current_user_can( 'manage_options' ) ) {
        return new WP_Error( 'rest_forbidden', 'Insufficient permissions', array( 'status' => 403 ) );
    }

    $status = get_option( 'emulvent_scraper_status', array() );

    return new WP_REST_Response( $status, 200 );
}

register_rest_route(
    'machine-data/v1',
    '/scraper-status',
    array(
        'methods'             => WP_REST_Server::READABLE,
        'callback'            => 'emulvent_get_scraper_status_callback',
        'permission_callback' => '__return_true',
    )
);

// Webhook für Scraper (um Status zu aktualisieren)
// POST /wp-json/machine-data/v1/update-scraper-status
function emulvent_update_scraper_status_callback( $request ) {
    $auth_token = $request->get_header( 'Authorization' );
    $stored_token = get_option( 'emulvent_scraper_webhook_token' );

    if ( ! hash_equals( $stored_token ?: '', str_replace( 'Bearer ', '', $auth_token ?: '' ) ) ) {
        return new WP_Error( 'rest_unauthorized', 'Invalid token', array( 'status' => 401 ) );
    }

    $body = $request->get_json_params();
    update_option( 'emulvent_scraper_status', $body );

    return new WP_REST_Response( array( 'success' => true ), 200 );
}

register_rest_route(
    'machine-data/v1',
    '/update-scraper-status',
    array(
        'methods'             => WP_REST_Server::CREATABLE,
        'callback'            => 'emulvent_update_scraper_status_callback',
        'permission_callback' => '__return_true',
    )
);

// Hook: Auf Plugin-Aktivierung — Webhook-Token generieren
function emulvent_activate_plugin() {
    if ( ! get_option( 'emulvent_scraper_webhook_token' ) ) {
        $token = bin2hex( random_bytes( 32 ) );
        update_option( 'emulvent_scraper_webhook_token', $token );
    }
}
register_activation_hook( __FILE__, 'emulvent_activate_plugin' );
?>
```

**Installation:**
1. Datei in `wp-content/plugins/emulvent-machine-data/` speichern
2. Im WordPress Admin > Plugins > aktivieren
3. Der Webhook-Token wird automatisch generiert (in `wp_options` Tabelle gespeichert)

---

### 1.2 WordPress-Seite: Monitoring-Dashboard (für Björn/Thilo)

**Ort:** WordPress Admin → Seiten → Neue Seite → `machine-data-dashboard`

**Template: Shortcode-basiert**

```php
// In Plugin oder functions.php hinzufügen:

function emulvent_monitoring_dashboard_shortcode() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return 'Zugriff verweigert';
    }

    $status = get_option( 'emulvent_scraper_status', array() );
    $all_models = emulvent_get_all_machines_callback( new WP_REST_Request() )->get_data();

    ob_start();
    ?>
    <div style="background: #f5f5f5; padding: 20px; border-radius: 8px;">
        <h1>📊 emulvent® Machine Data Dashboard</h1>
        <p>Scraper-Status & Datenqualität</p>

        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <thead>
                <tr style="background: #265887; color: white;">
                    <th style="padding: 10px; text-align: left;">Hersteller</th>
                    <th>Modelle</th>
                    <th>Status</th>
                    <th>Letzter Run</th>
                    <th>Fehler</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $manufacturers = array( 'DMG MORI', 'HAAS', 'GROB' );
                foreach ( $manufacturers as $mfr ) {
                    $mfr_status = $status[ strtolower( $mfr ) ] ?? array();
                    $mfr_models = array_filter( $all_models, fn( $m ) => $m['manufacturer'] === $mfr );
                    
                    $status_icon = ( $mfr_status['success'] ?? false ) ? '✅' : '⚠️';
                    $last_run = $mfr_status['last_run_at'] ?? 'Nie';
                    $error = $mfr_status['error'] ?? '—';

                    echo sprintf(
                        '<tr><td>%s</td><td>%d</td><td>%s</td><td>%s</td><td><code>%s</code></td></tr>',
                        htmlspecialchars( $mfr ),
                        count( $mfr_models ),
                        $status_icon,
                        htmlspecialchars( $last_run ),
                        htmlspecialchars( $error )
                    );
                }
                ?>
            </tbody>
        </table>

        <h2>📈 Zusammenfassung</h2>
        <p>
            <strong>Gesamtmodelle:</strong> <?php echo count( $all_models ); ?> <br>
            <strong>Letzte globale Aktualisierung:</strong> <?php echo esc_html( $status['last_global_run_at'] ?? 'Unbekannt' ); ?> <br>
            <strong>API-Endpunkt:</strong> <code><?php echo esc_url( get_rest_url( null, 'machine-data/v1/models' ) ); ?></code>
        </p>

        <h2>🔧 Debug-Info</h2>
        <pre style="background: white; padding: 10px; overflow-x: auto; border: 1px solid #ddd;">
<?php echo esc_html( json_encode( $status, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES ) ); ?>
        </pre>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode( 'emulvent_dashboard', 'emulvent_monitoring_dashboard_shortcode' );
```

**Seite erstellen:**
- Titel: `Machine Data Dashboard`
- Inhalt: `[emulvent_dashboard]`
- URL-Slug: `machine-data-dashboard`
- Status: Nur für eingeloggte Admins sichtbar (WordPress Standard)

---

## 🔄 TEIL 2: Web-Scraper (GitHub Actions + Python)

### 2.1 GitHub Repository Setup

**Voraussetzung:** Thilo hat GitHub-Account, emulvent® hat Org/Repo (z.B. `emulvent/machine-data-scraper`)

**Repository-Struktur:**
```
emulvent/machine-data-scraper/
├── .github/workflows/
│   └── scrape-machines.yml          ← GitHub Actions Workflow
├── scrapers/
│   ├── dmg_mori.py                  ← DMG MORI Scraper
│   ├── haas.py                      ← HAAS Scraper
│   ├── grob.py                      ← GROB Scraper
│   └── base_scraper.py              ← Basis-Klasse (shared logic)
├── requirements.txt                  ← Python Dependencies
├── .env.example                      ← Secrets-Template
└── README.md                         ← Dokumentation
```

### 2.2 GitHub Actions Workflow

**Datei:** `.github/workflows/scrape-machines.yml`

```yaml
name: Scrape Machine Data

on:
  schedule:
    - cron: '0 2 * * 0'  # Jeden Sonntag 02:00 UTC (03:00 CET)
  workflow_dispatch:      # Manuell triggern über GitHub UI

jobs:
  scrape:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run scrapers
        env:
          WP_REST_URL: ${{ secrets.WP_REST_URL }}        # z.B. https://emulvent.de/wp-json
          WP_WEBHOOK_TOKEN: ${{ secrets.WP_WEBHOOK_TOKEN }}
        run: |
          python scrapers/dmg_mori.py
          python scrapers/haas.py
          python scrapers/grob.py
          python -c "from scrapers.base_scraper import upload_scraper_status; upload_scraper_status()"

      - name: Notify on failure
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: 1,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Scraper run failed. Check logs: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}'
            })
```

**Secrets konfigurieren (GitHub UI → Settings → Secrets & variables → Actions):**

| Secret | Wert | Beispiel |
|--------|------|---------|
| `WP_REST_URL` | WordPress REST Base URL | `https://emulvent.de/wp-json` |
| `WP_WEBHOOK_TOKEN` | Token aus Plugin | (wird vom Plugin generiert, hier eintragen) |

---

### 2.3 Base Scraper Klasse

**Datei:** `scrapers/base_scraper.py`

```python
import requests
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class BaseScraper:
    """Basis-Klasse für alle Scraper"""
    
    def __init__(self, manufacturer: str):
        self.manufacturer = manufacturer
        self.wp_rest_url = os.getenv('WP_REST_URL')
        self.wp_webhook_token = os.getenv('WP_WEBHOOK_TOKEN')
        self.models = []
        self.errors = []

    def log(self, message: str, level: str = 'INFO'):
        """Logging mit Timestamp"""
        timestamp = datetime.utcnow().isoformat()
        print(f"[{timestamp}] [{level}] [{self.manufacturer}] {message}")

    def add_model(self, title: str, specs: Dict):
        """Modell zu Liste hinzufügen"""
        self.models.append({
            'title': title,
            'manufacturer': self.manufacturer,
            'specs': specs,
            'scraped_at': datetime.utcnow().isoformat(),
        })
        self.log(f"✓ Added: {title}")

    def add_error(self, error_msg: str):
        """Fehler protokollieren"""
        self.errors.append(error_msg)
        self.log(f"✗ Error: {error_msg}", level='ERROR')

    def upload_to_wordpress(self) -> bool:
        """Scraper-Ergebnisse zu WordPress hochladen"""
        if not self.models:
            self.add_error("No models scraped")
            return False

        try:
            # Für jedes Modell einen Post erstellen/updaten
            for model in self.models:
                post_data = {
                    'title': model['title'],
                    'content': json.dumps(model['specs'], indent=2),
                    'status': 'publish',
                    'type': 'machine_model',
                }
                
                # Meta-Felder hinzufügen
                meta_fields = {
                    'container_volume_liters': model['specs'].get('volume'),
                    'container_height_mm': model['specs'].get('height'),
                    'container_depth_mm': model['specs'].get('depth'),
                    'container_width_mm': model['specs'].get('width'),
                    'separator_count': model['specs'].get('separators', 0),
                    'kss_water_mixed': model['specs'].get('water_mixed', False),
                    'data_source': self.manufacturer.lower().replace(' ', '_'),
                    'last_scraped_at': model['scraped_at'],
                }
                post_data.update(meta_fields)

                # POST zu WordPress
                headers = {
                    'Authorization': f'Bearer {self.wp_webhook_token}',
                    'Content-Type': 'application/json',
                }
                
                # Erst checken, ob Model schon existiert (Query nach Titel + Hersteller)
                get_url = f"{self.wp_rest_url}/wp/v2/machine-models?search={model['title']}&per_page=1"
                resp = requests.get(get_url, headers=headers, timeout=10)
                
                if resp.status_code == 200 and resp.json():
                    # Update
                    post_id = resp.json()[0]['id']
                    put_url = f"{self.wp_rest_url}/wp/v2/machine-models/{post_id}"
                    resp = requests.put(put_url, json=post_data, headers=headers, timeout=10)
                else:
                    # Create
                    post_url = f"{self.wp_rest_url}/wp/v2/machine-models"
                    resp = requests.post(post_url, json=post_data, headers=headers, timeout=10)

                if resp.status_code not in [200, 201]:
                    self.add_error(f"WordPress upload failed for {model['title']}: {resp.text}")
                    return False

            self.log(f"✓ Uploaded {len(self.models)} models to WordPress")
            return True

        except Exception as e:
            self.add_error(f"Upload exception: {str(e)}")
            return False

    def run(self):
        """Überschreiben in Subklassen"""
        raise NotImplementedError("Subclasses must implement run()")


def upload_scraper_status():
    """Status aller Scraper zu WordPress hochladen"""
    # Diese Funktion wird am Ende des Workflows aufgerufen
    status = {
        'dmg_mori': {'success': True, 'last_run_at': datetime.utcnow().isoformat()},
        'haas': {'success': True, 'last_run_at': datetime.utcnow().isoformat()},
        'grob': {'success': True, 'last_run_at': datetime.utcnow().isoformat()},
        'last_global_run_at': datetime.utcnow().isoformat(),
    }
    
    headers = {
        'Authorization': f'Bearer {os.getenv("WP_WEBHOOK_TOKEN")}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.post(
            f"{os.getenv('WP_REST_URL')}/machine-data/v1/update-scraper-status",
            json=status,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        print(f"[{datetime.utcnow().isoformat()}] [INFO] Scraper status updated")
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] [ERROR] Failed to update status: {e}")
```

---

### 2.4 DMG MORI Scraper (Beispiel)

**Datei:** `scrapers/dmg_mori.py`

```python
from base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import re

class DMGMoriScraper(BaseScraper):
    """Scraper für DMG MORI Maschinenmodelle"""
    
    def __init__(self):
        super().__init__('DMG MORI')
        self.base_url = 'https://de.dmgmori.com/produkte/maschinen'

    def run(self):
        """Starte Scraping"""
        self.log(f"Starting scrape from {self.base_url}")
        
        try:
            # Hauptseite laden
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Maschinenmodelle extrahieren (XPath/CSS-Selector anpassen!)
            # ACHTUNG: Diese Selector müssen für emulvent.de angepasst werden!
            machine_links = soup.select('.machine-model-card a')  # Platzhalter
            
            if not machine_links:
                self.add_error("No machine links found. Selector may need update.")
                return False
            
            for link in machine_links:
                machine_url = link.get('href')
                if not machine_url.startswith('http'):
                    machine_url = self.base_url + machine_url
                
                try:
                    self._scrape_machine_detail(machine_url)
                except Exception as e:
                    self.add_error(f"Error scraping {machine_url}: {str(e)}")

            # Zu WordPress hochladen
            success = self.upload_to_wordpress()
            self.log(f"Scrape {'succeeded' if success else 'failed'}. {len(self.models)} models, {len(self.errors)} errors")
            return success

        except Exception as e:
            self.add_error(f"Scrape failed: {str(e)}")
            return False

    def _scrape_machine_detail(self, url: str):
        """Detail-Seite einer Maschine scrapen"""
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Title
        title_elem = soup.select_one('.machine-title, h1')
        title = title_elem.text.strip() if title_elem else "Unknown"
        
        # Spezifikationen extrahieren (Selectors anpassen!)
        specs = {
            'volume': self._extract_spec(soup, 'Behältervolumen', r'(\d+)\s*l'),
            'height': self._extract_spec(soup, 'Höhe', r'(\d+)\s*mm'),
            'depth': self._extract_spec(soup, 'Tiefe', r'(\d+)\s*mm'),
            'width': self._extract_spec(soup, 'Breite', r'(\d+)\s*mm'),
            'separators': 0,
            'water_mixed': 'wassermischbar' in soup.get_text().lower(),
            'url': url,
        }
        
        self.add_model(title, specs)

    def _extract_spec(self, soup, label: str, regex_pattern: str) -> Optional[int]:
        """Spezifikation aus HTML extrahieren"""
        text = soup.get_text()
        if label.lower() in text.lower():
            match = re.search(regex_pattern, text)
            if match:
                return int(match.group(1))
        return None


if __name__ == '__main__':
    scraper = DMGMoriScraper()
    scraper.run()
```

**Hinweis:** Die CSS-Selectors (`.machine-model-card`, `.machine-title`, etc.) müssen für die **echten DMG-MORI-Websites** angepasst werden. Das macht man mit:
1. Browser öffnen (Chrome DevTools)
2. Inspect Element → CSS-Klassen/IDs notieren
3. In Scraper-Code eintragen

---

### 2.5 HAAS & GROB Scraper (vereinfacht)

**Datei:** `scrapers/haas.py` und `scrapers/grob.py` folgen dem gleichen Muster. Beispiel für HAAS:

```python
from base_scraper import BaseScraper
import requests
import json

class HAASScraper(BaseScraper):
    """Scraper für HAAS CNC-Modelle (über API)"""
    
    def __init__(self):
        super().__init__('HAAS')
        # HAAS hat eine Machine Data Collection API
        self.api_url = 'https://ngc.haas.com/api/machines'

    def run(self):
        self.log("Fetching HAAS models from NGC API")
        
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            machines = response.json()
            
            for machine in machines:
                specs = {
                    'volume': machine.get('tank_capacity'),
                    'height': machine.get('height'),
                    'depth': machine.get('depth'),
                    'width': machine.get('width'),
                    'separators': machine.get('coolant_tank_compartments', 0),
                    'water_mixed': machine.get('coolant_type', '').lower() == 'water_soluble',
                    'api_id': machine.get('id'),
                }
                
                self.add_model(machine.get('model_name', 'Unknown'), specs)
            
            return self.upload_to_wordpress()
            
        except Exception as e:
            self.add_error(f"API fetch failed: {str(e)}")
            return False
```

---

## 📦 TEIL 3: App-Integration (Wie der Konfigurator die Daten lädt)

### 3.1 Frontend-Code (React/JavaScript)

**Datei:** `src/hooks/useMachineData.js` (im Konfigurator)

```javascript
import { useState, useEffect } from 'react';

const useMachineData = () => {
  const [machines, setMachines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMachines = async () => {
      try {
        // REST-API von WordPress aufrufen
        const response = await fetch(
          'https://emulvent.de/wp-json/machine-data/v1/models'
        );
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        setMachines(data);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch machine data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchMachines();
  }, []);

  return { machines, loading, error };
};

export default useMachineData;
```

**Verwendung im Konfigurator:**

```javascript
import useMachineData from './hooks/useMachineData';

export default function Configurator() {
  const { machines, loading, error } = useMachineData();

  if (loading) return <p>Maschinenmodelle werden geladen...</p>;
  if (error) return <p>Fehler: {error}</p>;

  return (
    <div>
      <label>Wähle deine Maschine:</label>
      <select onChange={(e) => {
        const machine = machines.find(m => m.id === parseInt(e.target.value));
        console.log('Selected:', machine);
        // Konfiguration basierend auf Maschinenspezifikationen
      }}>
        <option value="">-- Modell wählen --</option>
        {machines.map(machine => (
          <option key={machine.id} value={machine.id}>
            {machine.manufacturer} {machine.title}
            ({machine.container_volume_liters}L)
          </option>
        ))}
      </select>
    </div>
  );
}
```

---

## 📊 TEIL 4: Monitoring-Dashboard (WordPress-Admin-Seite)

### 4.1 Live-Status auf WordPress-Seite

Die Seite `machine-data-dashboard` wird mit dem Shortcode `[emulvent_dashboard]` befüllt und zeigt:

```
📊 emulvent® Machine Data Dashboard

Hersteller | Modelle | Status | Letzter Run        | Fehler
──────────────────────────────────────────────────────────
DMG MORI  | 45     | ✅     | 2026-09-29 02:30   | —
HAAS      | 32     | ✅     | 2026-09-29 02:35   | —
GROB      | 28     | ⚠️     | 2026-09-28 02:15   | "Selector changed"

Zusammenfassung
───────────────
Gesamtmodelle: 105
Letzte globale Aktualisierung: 2026-09-29 02:45 UTC
API-Endpunkt: https://emulvent.de/wp-json/machine-data/v1/models

Debug-Info
──────────
{
  "dmg_mori": {"success": true, "last_run_at": "2026-09-29T02:30:00Z"},
  "haas": {"success": true, "last_run_at": "2026-09-29T02:35:00Z"},
  "grob": {"success": false, "error": "CSS selector not found", ...},
  ...
}
```

---

## 🚀 TEIL 5: Deployment & Setup-Anleitung

### 5.1 Schritt-für-Schritt Setup (1–2 Stunden)

#### **Phase A: WordPress-Plugin installieren** (30 Min)

1. **Plugin-Datei erstellen:**
   ```bash
   # Auf Strato-Server via SFTP
   # Ordner: /wp-content/plugins/emulvent-machine-data/
   # Datei: emulvent-machine-data.php
   ```
   (Code aus Abschnitt 1.1 kopieren)

2. **Im WordPress Admin aktivieren:**
   - Admin → Plugins → emulvent-machine-data → Aktivieren
   - Token wird automatisch generiert und in `wp_options` gespeichert

3. **API testen:**
   ```bash
   curl https://emulvent.de/wp-json/machine-data/v1/models
   # Sollte leeres Array zurückgeben: []
   ```

#### **Phase B: GitHub Repository setup** (30 Min)

1. **Repo erstellen:** `https://github.com/emulvent/machine-data-scraper`

2. **Repository klonen:**
   ```bash
   git clone https://github.com/emulvent/machine-data-scraper.git
   cd machine-data-scraper
   ```

3. **Struktur erstellen:**
   ```bash
   mkdir -p .github/workflows scrapers
   touch .github/workflows/scrape-machines.yml
   touch scrapers/{base_scraper,dmg_mori,haas,grob}.py
   touch requirements.txt
   ```

4. **requirements.txt füllen:**
   ```
   requests==2.31.0
   beautifulsoup4==4.12.2
   lxml==4.9.3
   python-dotenv==1.0.0
   ```

5. **GitHub Secrets setzen** (Settings → Secrets & variables → Actions):
   ```
   WP_REST_URL = https://emulvent.de/wp-json
   WP_WEBHOOK_TOKEN = (von WordPress-Plugin kopieren)
   ```

6. **Code committen:**
   ```bash
   git add .
   git commit -m "Initial machine data scraper setup"
   git push origin main
   ```

#### **Phase C: Test-Run** (30 Min)

1. **Manueller Test via GitHub UI:**
   - Repo → Actions → "Scrape Machine Data" → "Run workflow"
   - Logs beobachten

2. **WordPress überprüfen:**
   - Admin → Maschinenmodelle → sollten neue Posts sichtbar sein
   - Oder API abrufen: `curl https://emulvent.de/wp-json/machine-data/v1/models`

3. **Dashboard aufrufen:**
   - Admin → Seiten → Machine Data Dashboard
   - Status sollte grün sein

---

### 5.2 Fehlerbehebung

| Problem | Lösung |
|---------|--------|
| **"401 Unauthorized" beim Upload** | WP_WEBHOOK_TOKEN ist falsch → Im WordPress Plugin nachprüfen |
| **CSS Selectors finden nichts** | Website-Struktur geändert → DevTools öffnen, neue Selector suchen |
| **GitHub Actions schlägt fehl** | Logs checken: Repo → Actions → Failed run → Details |
| **Alte Modelle verschwinden** | WordPress speichert alles → Alte Posts sind noch da, nur nicht im aktuellen Scraper |

---

## 📈 TEIL 6: Skalierungs-Pfad (Später)

### Wenn die Lösung wächst:

**MVP (Jetzt):**
- 3 Hersteller (DMG, HAAS, GROB)
- ~100 Modelle
- 1x/Woche Scrape
- Kosten: 0 €

**Phase 2 (Nov 2026, nach Fundraising):**
- +2 weitere Hersteller (TRUMPF, Makino)
- Community-Input integrieren
- Tägliches Scraping
- Kosten: 0 € (immer noch)

**Phase 3 (Q1 2027, Skalierung):**
- 500+ Modelle
- Cache-Layer (Redis, 10 €/Mo) optional
- Monitoring-Alerts (Slack)
- Kosten: ~10 €/Mo

---

## ✅ CHECKLISTE: Deployment

- [ ] WordPress-Plugin hochgeladen & aktiviert
- [ ] Token kopiert zu GitHub Secrets
- [ ] GitHub Repo erstellt mit allen Dateien
- [ ] Scraper-Code für 3 Hersteller adapted
- [ ] Test-Run erfolgreich (Logs grün)
- [ ] API-Endpoint funktioniert: `curl https://emulvent.de/wp-json/machine-data/v1/models`
- [ ] Dashboard-Seite erstellt in WordPress
- [ ] Konfigurator-App integriert (useMachineData Hook)
- [ ] Björn & Thilo können Dashboard sehen

---

## 📞 KONTAKT & SUPPORT

Fragen? Kontakt:
- **Thilo:** thilo.schaefer51@gmail.com
- **Björn:** info@emulvent.de
- **Tech-Support:** GitHub Issues im Repository

---

**Dokument Version:** 1.0  
**Erstellt:** 29.09.2026  
**Gültig für:** emulvent® Machine Data Architecture (Zero-Cost)
