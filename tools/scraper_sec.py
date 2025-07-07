import requests
from bs4 import BeautifulSoup

def scrape_sec(company_name):
    query = company_name.replace(" ", "+")
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?company={query}&type=10-K&count=10"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    links = soup.find_all("a", string="Documents")

    results = []
    for link in links[:1]:  # limit for demo
        href = "https://www.sec.gov" + link['href']
        filing_page = requests.get(href, headers=headers)
        filing_soup = BeautifulSoup(filing_page.content, "html.parser")
        txt_link = filing_soup.find("a", string=lambda t: t and "htm" in t)
        if txt_link:
            full_link = "https://www.sec.gov" + txt_link['href']
            raw_txt = requests.get(full_link, headers=headers).text
            results.append({"source": full_link, "text": raw_txt[:3000]})  # Limit size

    return results
