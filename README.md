# Local AI Agent with RAG and Streamlit Dashboard

A local AI agent that scrapes public data (SEC 10-K filings, Crunchbase, product docs, Trustpilot reviews) and generates three actionable insights using a RAG pipeline with Mistral 7B (Ollama). Insights are displayed via a Streamlit dashboard. The system is optimized for ~200-350 ms latency and deployed with Docker.

## Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Ollama (`mistral:7b-instruct-v0.3-q4_0`)
- Redis
- Hardware: 8GB RAM, 4-core CPU

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/local-ai-agent-rag-system.git
   cd local-ai-agent-rag-system