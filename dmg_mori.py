from base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import re
import os


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

            # Versuche, Maschinenmodelle zu finden (CSS-Selector anpassen bei Bedarf)
            # Standard-Selectors:
            machine_links = soup.select('.machine-model a, .product-card a, [data-product-id] a')

            if not machine_links:
                # Fallback: alle Links mit "modell" oder "maschine" im Text
                all_links = soup.find_all('a')
                machine_links = [l for l in all_links if l.text and any(
                    keyword in l.text.lower() for keyword in ['modell', 'maschine', 'fraes', 'dreh']
                )]

            if not machine_links:
                self.add_error("No machine links found. Website structure may have changed.")
                self.success = False
                return False

            self.log(f"Found {len(machine_links)} potential machine links")

            # Begrenzen auf erste 20 Modelle für schnelleres Testing
            for link in machine_links[:20]:
                try:
                    machine_url = link.get('href')
                    if not machine_url:
                        continue
                    if not machine_url.startswith('http'):
                        machine_url = self.base_url + machine_url

                    self._scrape_machine_detail(machine_url)
                except Exception as e:
                    self.add_error(f"Error scraping {machine_url}: {str(e)}")

            # Zu WordPress hochladen
            success = self.upload_to_wordpress()
            self.log(f"Scrape {'succeeded' if success else 'failed'}. {len(self.models)} models, {len(self.errors)} errors")
            os.environ['SCRAPER_DMG_SUCCESS'] = str(success).lower()
            return success

        except Exception as e:
            self.add_error(f"Scrape failed: {str(e)}")
            self.success = False
            return False

    def _scrape_machine_detail(self, url: str):
        """Detail-Seite einer Maschine scrapen"""
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Title
        title_elem = soup.select_one('.machine-title, .product-title, h1')
        if not title_elem:
            return
        title = title_elem.text.strip()

        if not title or len(title) < 3:
            return

        # Spezifikationen extrahieren
        specs = {
            'volume': self._extract_spec(soup, 'Behälter|Tank|Volume', r'(\d+)\s*(?:l|L|liter)'),
            'height': self._extract_spec(soup, 'Höhe|Height|Bauhöhe', r'(\d+)\s*(?:mm|MM)'),
            'depth': self._extract_spec(soup, 'Tiefe|Depth|Bautiefe', r'(\d+)\s*(?:mm|MM)'),
            'width': self._extract_spec(soup, 'Breite|Width|Baubreite', r'(\d+)\s*(?:mm|MM)'),
            'separators': self._extract_spec(soup, 'Trennwand|Partition|Behälter-Abteilung', r'(\d+)') or 0,
            'water_mixed': 'wassermischbar' in soup.get_text().lower() or 'wasserlöslich' in soup.get_text().lower(),
            'url': url,
        }

        self.add_model(title, specs)

    def _extract_spec(self, soup, label_pattern: str, regex_pattern: str) -> int:
        """Spezifikation aus HTML extrahieren"""
        text = soup.get_text()

        # Label-Pattern suchen
        if not re.search(label_pattern, text, re.IGNORECASE):
            return None

        # Wert extrahieren
        match = re.search(regex_pattern, text)
        if match:
            return int(match.group(1))

        return None


if __name__ == '__main__':
    scraper = DMGMoriScraper()
    scraper.run()
