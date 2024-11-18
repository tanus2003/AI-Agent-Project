import streamlit as st
import pandas as pd
from utils.google_sheets import connect_google_sheets
from utils.web_search import search_web
from utils.llm_processing import extract_data
from utils.helpers import download_csv

# App Title
st.title("AI Agent Dashboard")

# File Upload Section
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:", df.head())

    # Select column for query
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select the column to process:", columns)

    # Input prompt template
    prompt_template = st.text_input("Enter your prompt template (use {entity} for placeholders):", 
                                     "Get me the email address of {entity}.")

    if st.button("Process"):
        try:
            results = []
            for entity in df[selected_column]:
                # Generate query and fetch web results
                query = prompt_template.replace("{entity}", str(entity))
                search_results = search_web(query)

                # Pass to LLM for extraction
                extracted_info = extract_data(entity, search_results)
                results.append({"Entity": entity, "Result": extracted_info})

            # Display results
            result_df = pd.DataFrame(results)
            st.write("Results:", result_df)

            # Download results
            st.download_button("Download Results", download_csv(result_df), "results.csv")
        except Exception as e:
            st.error(f"An error occurred: {e}")
