# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 13:01:01 2025

@author: antho
"""

import os
from typing import List, Dict
from serpapi import GoogleSearch # import needed packages


def get_article(keywords: str = "machine learning") -> List[Dict]: # Retrieves academic article information based on user-provided keywords using SerpApi.
    api_key = "e635b72cd34e5b9ffa4e2dbab293fd432c7fe2d89b231c73db0045207b551274"
    
    if not api_key:
        raise ValueError("SerpApi API key is not set.")
        
    # Define search query
    search = GoogleSearch({
            "q": keywords,
            "engine": "google_scholar",
            "api_key":api_key
    })
    
    results = search.get_dict().get("organic_results", [])
    
    articles = []
    
    for result in results:
        article ={}
        pdf_link = result.get("resources", [{}])[0].get("link") if result.get("resources") else None
        if pdf_link and pdf_link.endswith(".pdf"):
            article = {
                "title": result.get("title"),
                "author": result.get("publication_info", {}).get("authors"),
                "pdf_link": pdf_link,
                "link": result.get("link"),
                "snippet": result.get("snippet")
        }
        articles.append(article)
        
        if len(articles) >= 7:
            break
        
    return articles 
    
articles = get_article()
if articles:
    for article in articles:
        title = article.get('title', 'No title available')
        author = article.get('author', 'No author information available')
        pdf_link = article.get('pdf_link', 'No PDF link available')
        link = article.get('link', 'No link available')
        snippet = article.get('snippet', 'No snippet available')
        
        print(f"Title: {title}")
        print(f"Authors: {author}")
        print(f"PDF Link: {pdf_link}")
        print(f"Link: {link}")
        print(f"Snippet: {snippet}")
        print("\n---\n")
    else:
        print("No articles found.")

