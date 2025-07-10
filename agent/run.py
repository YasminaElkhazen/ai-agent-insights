import redis
from agent.rag import index_data, retrieve_relevant_docs
from agent.llm_preprocessor import generate_insights
from agent.redis_cache import cache_insights
import json 
def run_pipeline(ticker, company_name, doc_url):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    cache_key = f"insights_{company_name}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)
    
    print(f"Indexing data for {company_name}...")
    collection_name = index_data(ticker, company_name, doc_url)
    
    print("Retrieving relevant context...")
    query = f"Key insights about {company_name}'s financial performance, product strengths, and customer sentiment"
    docs, metadata = retrieve_relevant_docs(query, collection_name)
    context = "\n".join([f"[{m['source']}]: {d}" for d, m in zip(docs, metadata)])
    
    print("Generating insights...")
    insights = generate_insights(context)
    
    cache_insights(company_name, insights)
    return insights