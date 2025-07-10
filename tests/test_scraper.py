import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.scraper import scrape_product_docs # Or whatever your function is called

def test_scraper():
    url = "https://docs.nvidia.com"
    data = scrape_product_docs(url)
    print("Scraped content:", data[:5000])  # Preview only part to avoid clutter

if __name__ == "__main__":
    test_scraper()
