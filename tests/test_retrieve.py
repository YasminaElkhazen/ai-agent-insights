import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.rag import retrieve_relevant_docs

def test_retrieve():
    query = "Key insights about NVIDIA's product strengths"
    collection = "nvidia_docs"  # Same name returned in indexing
    docs, metadata = retrieve_relevant_docs(query, collection)

    for i, doc in enumerate(docs):
        print(f"[{metadata[i]['source']}]: {doc[:200]}...")  # Preview

if __name__ == "__main__":
    test_retrieve()
