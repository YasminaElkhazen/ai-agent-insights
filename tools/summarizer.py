import subprocess

def summarize_with_local_llm(docs, company, sector):
    combined_text = "\n".join([doc["text"] for doc in docs])
    context = combined_text[:5000]  # Truncate

    prompt = f"""
You are an AI assistant. Based on the following documents, give 3 key business insights about {company}, a company in the {sector} sector.
Use only facts from the text.

Documents:
{context}
"""

    result = subprocess.run(["ollama", "run", "mistral"], input=prompt.encode(), stdout=subprocess.PIPE)
    return result.stdout.decode()
