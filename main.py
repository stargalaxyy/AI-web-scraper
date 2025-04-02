import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama

st.title("AI Web Scraper")
url = st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the website")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    clean_content = clean_body_content(body_content)
    
    # Save cleaned content to the streamlit session to access later
    st.session_state.dom_content = clean_content
    
    # An expander is like a button that will toggle the display of content
    with st.expander("View DOM Content"):
        st.text_area("DOM Content", clean_content, height=500)
        
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")
        
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)
                











