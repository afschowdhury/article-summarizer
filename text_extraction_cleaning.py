# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 17:28:58 2025

@author: LRangel
"""

import os
from typing import Dict, List
import logging
from pdfminer.high_level import extract_text
import requests
import re


def download_pdf(pdf_url: str, output_path: str) -> bool:
    """Downloads a PDF from a URL to a local path."""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    try:
        response = requests.get(pdf_url, headers=headers)
        response.raise_for_status()
        with open(output_path, 'wb') as file:
            file.write(response.content)
        return True
    except Exception as e:
        logging.error(f"Error downloading PDF: {e}")
        return False

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    try:
        if not os.path.exists(pdf_path):
            logging.error("File not found.")
            return ""
        
        text = extract_text(pdf_path)
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text: {e}")
        return ""

def clean_extracted_text(text: str) -> str:
    """Cleans the extracted text by removing page numbers, images, references, headers, and footers."""
    # Remove page numbers (assuming they are standalone numbers)
    text = re.sub(r'\b\d+\b', '', text)
    
    # Remove common header/footer patterns (e.g., "Page 1 of 10", "Header text", "Footer text")
    text = re.sub(r'Page \d+ of \d+', '', text)
    text = re.sub(r'Header text', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Footer text', '', text, flags=re.IGNORECASE)
    
    # Remove references section (assuming it starts with "References" or "Bibliography")
    text = re.split(r'References|Bibliography', text, flags=re.IGNORECASE)[0]
    
    # Remove image captions (assuming they are labeled as "Figure" or "Image")
    text = re.sub(r'Figure \d+.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Image \d+.*', '', text, flags=re.IGNORECASE)
    
    return text.strip()

def get_scrapped_content(data_dict: List[Dict], num_articles: int) -> List[Dict]:
    """Extracts and processes content from PDF papers u."""
    processed_articles = []
    for article in data_dict:
        if len(processed_articles) >= num_articles:
            break
        
        pdf_url = article.get("pdf_link")
        if not pdf_url:
            logging.warning("No PDF link found for article.")
            continue
        
        pdf_path = os.path.join("temp", os.path.basename(pdf_url))
        if not download_pdf(pdf_url, pdf_path):
            continue
        
        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue
        
        cleaned_text = clean_extracted_text(text)
        content_length = len(cleaned_text.split())
        if content_length > 10000:
            # Extract Abstract, Results, and Discussion sections
            abstract = cleaned_text.split("Abstract:")[1].split("Results:")[0].strip() if "Abstract:" in cleaned_text else ""
            results = cleaned_text.split("Results:")[1].split("Discussion:")[0].strip() if "Results:" in cleaned_text else ""
            discussion = cleaned_text.split("Discussion:")[1].strip() if "Discussion:" in cleaned_text else ""
            content = f"Abstract: {abstract}\nResults: {results}\nDiscussion: {discussion}"
            is_full = False
        else:
            content = cleaned_text
            is_full = True
        
        processed_article = article.copy()
        processed_article["content"] = content
        processed_article["is_full"] = is_full
        processed_articles.append(processed_article)
    
    return processed_articles

# Example usage
data_dict = [
    {
        "title": "Food Insecurity: A Public Health Issue",
        "author": "Murthy, Vivek, H.",
        "pdf_link": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5230819/pdf/10.1177_0033354916664154.pdf",
        "publication_year": "2016",
        "journal": "SAGE Publications"
    }
]

num_articles = 1
processed_content = get_scrapped_content(data_dict, num_articles)
for article in processed_content:
    print(article)

