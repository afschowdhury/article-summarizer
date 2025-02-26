# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 13:01:01 2025
@author: anthony
"""
import os
from typing import Dict, List

from serpapi.google_scholar_search import GoogleScholarSearch


def get_article(keywords: str) -> List[Dict]:
    # Retrieves academic article information based on user-provided keywords using SerpApi.
    api_key = os.getenv("SERPAPI_KEY")  # You should use environment variables properly

    if not api_key:
        # Fallback to your hardcoded key if needed, though not recommended for security
        api_key = "b8a646e2d1f0bc3a3acd57029db888cd038496af265027a60f8577766298c839"

    if not api_key:
        raise ValueError("SerpApi API key is not set.")

    search = GoogleScholarSearch(
        {"q": keywords, "api_key": api_key, "num": 25}
    )  # Simplified parameters
    results = search.get_dict().get("organic_results", [])  # Use get_dict() method

    articles = []
    for result in results:
        article = {
            "title": result.get("title"),
            "author": result.get("publication_info", {}).get("authors"),
            "pdf_link": (
                result.get("resources", [{}])[0].get("link")
                if result.get("resources")
                else None
            ),
            "link": result.get("link"),
            "snippet": result.get("snippet"),
        }
        articles.append(article)

    return articles
