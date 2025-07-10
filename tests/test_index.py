import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.rag import index_data

def test_index():
    ticker = "NVDA"
    company_name = "NVIDIA"
    doc_url = "https://docs.nvidia.com"  # or your scraped content path

    collection_name = index_data(ticker, company_name, doc_url)
    print(f"Indexed collection: {collection_name}")

if __name__ == "__main__":
    test_index()
