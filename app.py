import pandas as pd
import streamlit as st

from data_extractor import get_scrapped_content
from scraping import get_article
from summarizer import get_summary

# Set page configuration
st.set_page_config(
    page_title="Research Article Summarizer", page_icon="📚", layout="wide"
)

# App title and description
st.title("📚 Research Article Summarizer")
st.markdown(
    """
    This application helps you quickly generate summaries for research articles 
    based on your keywords of interest. Simply enter your research keywords,
    select the number of articles to summarize, and click the button.
"""
)

# Sidebar for inputs
with st.sidebar:
    st.header("Search Parameters")

    # Input for research keywords
    keywords = st.text_input(
        "Research Keywords", placeholder="e.g., artificial intelligence ethics"
    )

    # Slider for number of articles
    num_articles = st.slider(
        "Number of Articles to Summarize", min_value=1, max_value=7, value=5, step=1
    )

    # Generate button
    generate_button = st.button(
        "Generate Summaries", type="primary", use_container_width=True
    )

    # Information about the app
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown(
        """
        1. Enter your research keywords
        2. Select the number of articles
        3. Click the generate button
        4. Wait for the summaries to be generated
    """
    )

# Main content area
if generate_button and keywords:
    # Create a progress indicator
    with st.status("Generating research summaries...", expanded=True) as status:
        st.write("Searching for articles...")
        articles = get_article(keywords=keywords)

        st.write(f"Found {num_articles} articles.")
        st.write("Screapping articles...")
        processed_articles = get_scrapped_content(articles, num_articles)
        st.write("Scrapping complete!")
        st.write("Generating summaries...")
        summaries = get_summary(keywords, processed_articles)

        status.update(
            label="Summary generation complete!", state="complete", expanded=False
        )

    # Display the summaries in a tabular format
    st.header("Research Summaries")

    # Convert to DataFrame for easy display
    summary_df = pd.DataFrame(summaries)

    # Create expandable sections for each summary
    for i, summary in enumerate(summaries):
        with st.expander(f"{i+1}. {summary['title']}", expanded=i == 0):
            cols = st.columns([3, 1])
            with cols[0]:
                # st.markdown(f"**Date:** {summary['date']}")
                st.markdown(f"**Author:** {summary['author']}")
                st.markdown("### Summary")
                st.write(summary["summary"])
            with cols[1]:
                st.markdown("### Source")
                st.markdown(f"[Read Original Article]({summary['url']})")

    # Also provide a downloadable CSV
    csv = summary_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Summaries as CSV",
        data=csv,
        file_name=f"research_summaries_{keywords.replace(' ', '_')}.csv",
        mime="text/csv",
    )

elif generate_button and not keywords:
    st.warning("Please enter research keywords before generating summaries.")
else:
    # Display placeholder when no search has been performed
    st.info(
        "Enter your research keywords and click 'Generate Summaries' to get started."
    )
