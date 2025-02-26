# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 17:28:58 2025

@author: LRangel , Menna
"""

import logging
import os
import re
from typing import Dict, List

import requests
from pdfminer.high_level import extract_text

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def download_pdf(pdf_url: str, output_path: str) -> bool:
    """Downloads a PDF from a URL to a local path."""

    # Create directory for the output file if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logging.info(f"Created directory: {output_dir}")
        except Exception as e:
            logging.error(f"Error creating directory {output_dir}: {e}")
            return False

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        logging.info(f"Downloading PDF from: {pdf_url}")
        response = requests.get(pdf_url, headers=headers, timeout=30)  # Added timeout
        response.raise_for_status()

        with open(output_path, "wb") as file:
            file.write(response.content)

        logging.info(f"Successfully downloaded PDF to: {output_path}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error downloading PDF: {e}")
        return False
    except IOError as e:
        logging.error(f"IO error saving PDF: {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error downloading PDF: {e}")
        return False


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    try:
        if not os.path.exists(pdf_path):
            logging.error(f"File not found: {pdf_path}")
            return ""

        logging.info(f"Extracting text from: {pdf_path}")
        text = extract_text(pdf_path)
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text from {pdf_path}: {e}")
        return ""


def clean_extracted_text(text: str) -> str:
    """Cleans the extracted text by removing page numbers, images, references, headers, and footers."""
    logging.info("Cleaning extracted text")

    # Remove page numbers (assuming they are standalone numbers)
    text = re.sub(r"\b\d+\b", "", text)

    # Remove common header/footer patterns (e.g., "Page 1 of 10", "Header text", "Footer text")
    text = re.sub(r"Page \d+ of \d+", "", text)
    text = re.sub(r"Header text", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Footer text", "", text, flags=re.IGNORECASE)

    # Remove references section (assuming it starts with "References" or "Bibliography")
    text = re.split(r"References|Bibliography", text, flags=re.IGNORECASE)[0]

    # Remove image captions (assuming they are labeled as "Figure" or "Image")
    text = re.sub(r"Figure \d+.*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Image \d+.*", "", text, flags=re.IGNORECASE)

    return text.strip()


def get_scrapped_content(
    data_dict: List[Dict], num_articles: int, temp_dir: str = "temp"
) -> List[Dict]:
    """Extracts and processes content from PDF papers."""

    # Make sure the temp directory exists
    if not os.path.exists(temp_dir):
        try:
            os.makedirs(temp_dir)
            logging.info(f"Created temporary directory: {temp_dir}")
        except Exception as e:
            logging.error(f"Error creating temporary directory: {e}")
            return []

    processed_articles = []
    for i, article in enumerate(data_dict):
        if len(processed_articles) >= num_articles:
            break

        logging.info(
            f"Processing article {i+1}/{min(len(data_dict), num_articles)}: {article.get('title', 'Unknown title')}"
        )

        pdf_url = article.get("pdf_link")
        if not pdf_url:
            logging.warning("No PDF link found for article.")
            continue

        pdf_filename = os.path.basename(pdf_url)
        # Sanitize filename if needed
        pdf_filename = re.sub(
            r'[\\/*?:"<>|]', "_", pdf_filename
        )  # Replace invalid chars
        pdf_path = os.path.join(temp_dir, pdf_filename)

        if not download_pdf(pdf_url, pdf_path):
            continue

        text = extract_text_from_pdf(pdf_path)
        if not text:
            logging.warning(f"No text extracted from PDF: {pdf_path}")
            continue

        cleaned_text = clean_extracted_text(text)
        content_length = len(cleaned_text.split())
        logging.info(f"Extracted {content_length} words from the PDF")

        if content_length > 10000:
            # Extract Abstract, Results, and Discussion sections
            abstract = ""
            results = ""
            discussion = ""

            # Safely extract sections
            if "Abstract:" in cleaned_text:
                parts = cleaned_text.split("Abstract:", 1)
                abstract_text = parts[1]
                if "Results:" in abstract_text:
                    abstract = abstract_text.split("Results:", 1)[0].strip()
                elif "Introduction:" in abstract_text:
                    abstract = abstract_text.split("Introduction:", 1)[0].strip()
                else:
                    abstract = abstract_text[
                        :1000
                    ].strip()  # Take first 1000 chars as fallback

            if "Results:" in cleaned_text:
                parts = cleaned_text.split("Results:", 1)
                results_text = parts[1]
                if "Discussion:" in results_text:
                    results = results_text.split("Discussion:", 1)[0].strip()
                else:
                    results = results_text[
                        :2000
                    ].strip()  # Take first 2000 chars as fallback

            if "Discussion:" in cleaned_text:
                discussion = cleaned_text.split("Discussion:", 1)[1].strip()
                if "Conclusion:" in discussion:
                    discussion = discussion.split("Conclusion:", 1)[0].strip()

            content = f"Abstract: {abstract}\n\nResults: {results}\n\nDiscussion: {discussion}"
            is_full = False
            logging.info("Document was large, extracted key sections only")
        else:
            content = cleaned_text
            is_full = True
            logging.info("Document was under the size threshold, keeping full content")

        processed_article = article.copy()
        processed_article["content"] = content
        processed_article["is_full"] = is_full
        processed_articles.append(processed_article)
        logging.info(
            f"Successfully processed article: {article.get('title', 'Unknown title')}"
        )

    return processed_articles
