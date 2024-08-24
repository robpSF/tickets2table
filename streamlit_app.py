import streamlit as st
import pandas as pd
import json
from bs4 import BeautifulSoup

# Load JSON data from file (In Streamlit Cloud, you will need to upload the file)
uploaded_file = st.file_uploader("Choose a JSON file", type="json")

if uploaded_file is not None:
    # Read and parse the JSON data
    data = json.load(uploaded_file)

    # Extract the "body" content from the threads, excluding "EventInfo" types
    body_content = []
    for ticket in data:
        for thread in ticket.get("threads", []):
            if thread.get("threadType") != "EventInfo":
                body_html = thread.get("body", "")
                if body_html:  # Check if body is not empty
                    # Convert HTML to plain text
                    soup = BeautifulSoup(body_html, "html.parser")
                    body_text = soup.get_text()
                    body_content.append({"body": body_text})

    # Convert to DataFrame
    if body_content:
        df = pd.DataFrame(body_content)

        # Display the DataFrame in a table
        st.write("Plain text body content from threads (excluding EventInfo):")
        st.dataframe(df)
    else:
        st.write("No relevant 'body' content found in the threads.")
