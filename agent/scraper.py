import requests
from bs4 import BeautifulSoup
import httpx
from parsel import Selector
import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def scrape_10k_filings(company_ticker):
    cache_key = f"10k_{company_ticker}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    url = f"https://www.sec.gov/edgar/search/#/q={company_ticker}&category=custom&forms=10-K"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/96.0.4664.110"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        filing_text = soup.get_text()[:5000]  # Increased for RAG
        r.setex(cache_key, 3600, json.dumps(filing_text))
        time.sleep(1)
        return filing_text
    except Exception as e:
        print(f"Error scraping 10-K: {e}")
        return ""

def scrape_crunchbase(company_name):
    cache_key = f"crunchbase_{company_name}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    url = f"https://www.crunchbase.com/organization/{company_name.lower().replace(' ', '-')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/96.0.4664.110"}
    try:
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            selector = Selector(response.text)
            data = {
                "name": selector.css("h1::text").get(),
                "funding": selector.css(".funding::text").get(),
                "description": selector.css(".description::text").get()
            }
            r.setex(cache_key, 3600, json.dumps(data))
            time.sleep(1)
            return data
    except Exception as e:
        print(f"Error scraping Crunchbase: {e}")
        return {}

def scrape_product_docs(url):
    cache_key = f"product_docs_{url}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/96.0.4664.110"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()[:5000]
        r.setex(cache_key, 3600, json.dumps(text))
        time.sleep(1)
        return text
    except Exception as e:
        print(f"Error scraping product docs: {e}")
        return ""

def scrape_customer_reviews(company_name):
    cache_key = f"reviews_{company_name}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    url = f"https://www.trustpilot.com/review/{company_name.lower().replace(' ', '')}.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/96.0.4664.110"}
    try:
        with httpx.Client() as client:
            response = client.get(url, headers=headers, timeout=10)
            selector = Selector(response.text)
            reviews = selector.css(".review-content__text::text").getall()
            reviews = [r.strip()[:500] for r in reviews][:5]
            r.setex(cache_key, 3600, json.dumps(reviews))
            time.sleep(1)
            return reviews
    except Exception as e:
        print(f"Error scraping reviews: {e}")
        return []