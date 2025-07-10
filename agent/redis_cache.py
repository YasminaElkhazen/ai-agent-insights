import redis
import json

def cache_insights(company_name, insights):
    #r = redis.Redis(host='redis', port=6379, decode_responses=True)
    r = redis.Redis(host="localhost", port=6379)
    cache_key = f"insights_{company_name}"
    r.setex(cache_key, 3600, json.dumps(insights))
    print("Insights cached successfully")