import streamlit as st
import pandas as pd
import json

# Load JSON data from file (In Streamlit Cloud, you will need to upload the file)
uploaded_file = st.file_uploader("Choose a JSON file", type="json")

if uploaded_file is not None:
    # Read and parse the JSON data
    data = json.load(uploaded_file)

    # Extract the "body" content from the threads
    body_content = []
    for ticket in data:
        for thread in ticket.get("threads", []):
            body = thread.get("body", "")
            if body:  # Check if body is not empty
                body_content.append({"body": body})

    # Convert to DataFrame
    if body_content:
        df = pd.DataFrame(body_content)

        # Display the DataFrame in a table
        st.write("Body content from threads:")
        st.dataframe(df)
    else:
        st.write("No 'body' content found in the threads.")
