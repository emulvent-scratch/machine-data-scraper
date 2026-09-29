import requests
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class BaseScraper:
    """Basis-Klasse für alle Scraper"""

    def __init__(self, manufacturer: str):
        self.manufacturer = manufacturer
        self.wp_rest_url = os.getenv('WP_REST_URL', '').rstrip('/')
        self.wp_webhook_token = os.getenv('WP_WEBHOOK_TOKEN', '')
        self.models = []
        self.errors = []
        self.success = False

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
            self.success = False
            return False

        try:
            headers = {
                'Authorization': f'Bearer {self.wp_webhook_token}',
                'Content-Type': 'application/json',
            }

            for model in self.models:
                post_data = {
                    'title': model['title'],
                    'content': json.dumps(model['specs'], indent=2, ensure_ascii=False),
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
                    'verification_count': 1,
                }
                post_data.update(meta_fields)

                # Erst prüfen, ob Modell schon existiert
                search_url = f"{self.wp_rest_url}/wp/v2/machine-models?search={model['title']}&per_page=1"
                resp_search = requests.get(search_url, headers=headers, timeout=10)

                if resp_search.status_code == 200 and resp_search.json():
                    # Update
                    post_id = resp_search.json()[0]['id']
                    put_url = f"{self.wp_rest_url}/wp/v2/machine-models/{post_id}"
                    resp = requests.put(put_url, json=post_data, headers=headers, timeout=10)
                    self.log(f"Updated model {post_id}: {model['title']}")
                else:
                    # Create
                    post_url = f"{self.wp_rest_url}/wp/v2/machine-models"
                    resp = requests.post(post_url, json=post_data, headers=headers, timeout=10)
                    self.log(f"Created new model: {model['title']}")

                if resp.status_code not in [200, 201]:
                    self.add_error(f"WordPress upload failed for {model['title']}: {resp.status_code} - {resp.text[:200]}")
                    return False

            self.log(f"✓ Uploaded {len(self.models)} models to WordPress")
            self.success = True
            return True

        except Exception as e:
            self.add_error(f"Upload exception: {str(e)}")
            self.success = False
            return False

    def run(self):
        """Überschreiben in Subklassen"""
        raise NotImplementedError("Subclasses must implement run()")


def upload_scraper_status():
    """Status aller Scraper zu WordPress hochladen"""
    from dmg_mori import DMGMoriScraper
    from haas import HAASScraper
    from grob import GROBScraper

    # Statuse sammeln (aus Umgebungsvariablen oder Dateien)
    status = {
        'dmg_mori': {'success': os.getenv('SCRAPER_DMG_SUCCESS', 'false').lower() == 'true', 'last_run_at': datetime.utcnow().isoformat()},
        'haas': {'success': os.getenv('SCRAPER_HAAS_SUCCESS', 'false').lower() == 'true', 'last_run_at': datetime.utcnow().isoformat()},
        'grob': {'success': os.getenv('SCRAPER_GROB_SUCCESS', 'false').lower() == 'true', 'last_run_at': datetime.utcnow().isoformat()},
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
        print(f"[{datetime.utcnow().isoformat()}] [INFO] Scraper status updated to WordPress")
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] [ERROR] Failed to update status: {e}")
