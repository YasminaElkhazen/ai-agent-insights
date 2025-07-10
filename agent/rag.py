from sentence_transformers import SentenceTransformer
import chromadb
import redis
import json
from agent.scraper import scrape_10k_filings, scrape_crunchbase, scrape_product_docs, scrape_customer_reviews

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
embedder = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.HttpClient(host='localhost', port=8000)

def index_data(company_ticker, company_name, product_doc_url):
    collection_name = f"{company_name.lower().replace(' ', '_')}_docs"
    cache_key = f"collection_{collection_name}"
    
    # Check if collection is already indexed
    if r.get(cache_key):
        return collection_name
    
    try:
        # Create or get collection
        collection = client.get_or_create_collection(name=collection_name)
        
        # Scrape data
        filings = scrape_10k_filings(company_ticker)
        crunchbase = scrape_crunchbase(company_name)
        product_docs = scrape_product_docs(product_doc_url)
        reviews = scrape_customer_reviews(company_name)
        
        # Split into chunks (500 characters each for efficient retrieval)
        documents = []
        metadata = []
        ids = []
        for i, text in enumerate([filings, str(crunchbase), product_docs, " ".join(reviews)]):
            chunks = [text[j:j+500] for j in range(0, len(text), 500)]
            for j, chunk in enumerate(chunks):
                documents.append(chunk)
                metadata.append({"source": ["10-K", "Crunchbase", "Product Docs", "Reviews"][i]})
                ids.append(f"{i}_{j}")
        
        # Generate embeddings
        embeddings = embedder.encode(documents).tolist()
        
        # Store in Chroma
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadata,
            ids=ids
        )
        
        r.setex(cache_key, 3600, "indexed")
        return collection_name
    except Exception as e:
        print(f"Error indexing data: {e}")
        return collection_name

def retrieve_relevant_docs(query, collection_name, n_results=5):
    try:
        collection = client.get_collection(name=collection_name)
        query_embedding = embedder.encode(query).tolist()
        results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
        return results['documents'][0], results['metadatas'][0]
    except Exception as e:
        print(f"Error retrieving docs: {e}")
        return [], []