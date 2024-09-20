import streamlit as st
from scrape import (
    scrape_website,
    read_scraped_data,
    split_dom_content,
)
from parse import parse_with_ollama

# Streamlit UI
st.title("IHRD Infobot")
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")

        # Scrape the website
        # dom_content = scrape_website(url)
        # print(dom_content)
        
        file_path = "cec.txt"
        dom_content = read_scraped_data(file_path)

        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = dom_content

        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", dom_content, height=300)


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)