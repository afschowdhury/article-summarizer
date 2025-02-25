# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 13:01:01 2025

@author: antho
"""

import os
from typing import List, Dict
from serpapi import GoogleSearch # import needed packages

def get_article(keywords: str) -> List[Dict]: # Retrieves academic article information based on user-provided keywords using SerpApi.
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SerpApi API key is not set.")
       
        search = GoogleSearch({
            "q": keywords,
            "engine": "google_scholar",
            "api_key":api_key
            })
    results = search.get("organic_results")
    
    articles = []
    
    for result in results:
        article = {
            "title": result.get("title"),
            "author": result.get("publication_info", {}).get("authors"),
            "pdf_link": results.get("resources", [{}])[0].get("link") if result.get("resources") else None,
            "link": result.get("link"),
            "snippet": result.get("snippet")
            }
        articles.append(article)
        
        return articles 