import streamlit as st
from agent.run import run_agent

st.title("📊 AI Business Insight Agent")

company = st.text_input("Company Name", "Tesla")
location = st.selectbox("Location", ["USA", "UK", "Nigeria", "Multinational"])
sector = st.selectbox("Sector", ["Finance", "Tech", "Retail", "Other"])

if st.button("Run Agent"):
    with st.spinner("Scraping + thinking..."):
        result = run_agent(company, location, sector)
        st.success("Done!")
        st.markdown(result)
