import streamlit as st
import pandas as pd
import json
from bs4 import BeautifulSoup
import re

def remove_footer(text):
    # Basic patterns for common footer starts
    footer_patterns = [
        r"(?i)(?:regards|sincerely|best|thanks|thank you|cheers|confidential|disclaimer|this email and any attachments|this message is intended|C2 General)[\s\S]*$",  # Common signatures or disclaimers
        r"(?i)^[-–—]*\s*(?:On|From|Sent|To|Subject):",  # Forwarded or replied email headers
    ]
    
    for pattern in footer_patterns:
        text = re.sub(pattern, "", text).strip()
    
    return text

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
                    # Remove email footers and disclaimers
                    cleaned_body_text = remove_footer(body_text)
                    body_content.append({"body": cleaned_body_text})

    # Convert to DataFrame
    if body_content:
        df = pd.DataFrame(body_content)

        # Display the DataFrame in a table
        st.write("Plain text body content from threads (excluding EventInfo, footers removed):")
        st.dataframe(df)
    else:
        st.write("No relevant 'body' content found in the threads.")
