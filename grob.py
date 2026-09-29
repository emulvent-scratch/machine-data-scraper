from base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import re
import os


class GROBScraper(BaseScraper):
    """Scraper für GROB Maschinenmodelle"""

    def __init__(self):
        super().__init__('GROB')
        self.base_url = 'https://www.grob.de/de/produkte/'

    def run(self):
        """Starte Scraping"""
        self.log(f"Starting scrape from {self.base_url}")

        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Maschinenlinks suchen
            machine_links = soup.select('a[href*="produkte"], .product-list a, [data-machine] a')

            if not machine_links:
                # Fallback: alle Links unter Produkten
                all_links = soup.find_all('a')
                machine_links = [l for l in all_links if l.get('href') and 'produkte' in l.get('href', '').lower()]

            if not machine_links:
                self.add_error("No machine links found on GROB website")
                self.success = False
                return False

            self.log(f"Found {len(machine_links)} machine links")

            # Begrenzen auf erste 15 Modelle
            for link in machine_links[:15]:
                try:
                    machine_url = link.get('href')
                    if not machine_url:
                        continue
                    if not machine_url.startswith('http'):
                        machine_url = 'https://www.grob.de' + machine_url

                    self._scrape_machine_detail(machine_url)
                except Exception as e:
                    self.add_error(f"Error scraping {machine_url}: {str(e)}")

            success = self.upload_to_wordpress()
            self.log(f"Scrape {'succeeded' if success else 'failed'}. {len(self.models)} models, {len(self.errors)} errors")
            os.environ['SCRAPER_GROB_SUCCESS'] = str(success).lower()
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
        title_elem = soup.select_one('h1, .machine-title, .product-title')
        if not title_elem:
            return

        title = title_elem.text.strip()

        if not title or len(title) < 3:
            return

        # Spezifikationen
        text = soup.get_text()

        specs = {
            'volume': self._extract_number(text, r'(?:Kühl|Kühlschmierstoff).*?(?:Behälter|Tank).*?(\d+)\s*(?:l|L|liter)', r'tank.*?(\d+)\s*(?:l|L|liter)'),
            'height': self._extract_number(text, r'höhe.*?(\d+)\s*(?:mm|MM)'),
            'depth': self._extract_number(text, r'tiefe.*?(\d+)\s*(?:mm|MM)'),
            'width': self._extract_number(text, r'breite.*?(\d+)\s*(?:mm|MM)'),
            'separators': 0,
            'water_mixed': 'wassermischbar' in text.lower() or 'wasserlöslich' in text.lower(),
            'url': url,
        }

        self.add_model(title, specs)

    def _extract_number(self, text: str, *patterns) -> int:
        """Zahlen aus Text extrahieren mit mehreren Patterns"""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None


if __name__ == '__main__':
    scraper = GROBScraper()
    scraper.run()
