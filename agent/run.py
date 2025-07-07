from tools.scraper_sec import scrape_sec
from tools.summarizer import summarize_with_local_llm

def run_agent(company, location, sector):
    docs = scrape_sec(company)
    summary = summarize_with_local_llm(docs, company, sector)
    return summary
