import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from agent.run import run_pipeline
import redis
import json

st.title("Company Insights Dashboard")

# Input form
with st.form("company_form"):
    ticker = st.text_input("Stock Ticker (e.g., NVDA)")
    company_name = st.text_input("Company Name (e.g., NVIDIA)")
    doc_url = st.text_input("Product Documentation URL (e.g., https://docs.nvidia.com)")
    submitted = st.form_submit_button("Generate Insights")

# Check Redis cache
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
insights = []
if submitted and ticker and company_name and doc_url:
    with st.spinner("Generating insights..."):
        insights = run_pipeline(ticker, company_name, doc_url)
else:
    # Check cache for previous insights
    cache_key = f"insights_{company_name}" if company_name else None
    if cache_key and r.get(cache_key):
        insights = json.loads(r.get(cache_key))
        st.write("Loaded cached insights.")

# Display insights
if insights:
    st.header("Insights")
    for i, insight in enumerate(insights, 1):
        st.markdown(f"**{i}.** {insight}")
else:
    st.write("Enter company details to generate insights.")