import streamlit as st
from comments import fetch_comments
from utils import get_summary

st.title("YouTube Comments Summarizer")

st.write(
    "Use this tool to generate summaries from comments under any YouTube video. "
    "The tool uses Google Gemini paired with Lang Chain to generate the summaries."
)

left, right = st.columns(2)
form = left.form("template_form")

url_input = form.text_input(
    "Enter YouTube video URL",
    placeholder="",
    value="",
)

submit = form.form_submit_button("Get Summary")

gemini_api_key = st.secrets['GEMINI_API_KEY']

with st.container():
    if submit and url_input:
        with st.spinner("Fetching Summary..."):
            # Get Comments from YouTube API - INPUT
            text = fetch_comments(url_input)
            
            if text:  # Proceed only if comments are fetched
                # Tokenization and Summarization - MAIN CODE
                final_summary = get_summary(text)
                
                # Display the output on Streamlit - OUTPUT
                with right:
                    right.write(f"{final_summary}")
            else:
                st.error("Unable to fetch comments. Please check the video or try again.")
