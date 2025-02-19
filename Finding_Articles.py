# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 12:49:29 2025

@author: antho
"""

pip install scholarly google-search-results

from scholarly import scholarly
from serpapi import GoogleSearch

def search_google_scholar(query, api_key):
    """Search Google Scholar-SerpAPI."""
    question = {
        "engine": "google_scholar",
        "q": query,
        "api_key": api_key
        }
    
    search = GoogleSearch(question)
    results = search.get_dict()
    
    if "original_results" in results:
        return results["original_results"]
    else:
        return []
    
    def search_google_scholar(query):
        """ Search Google Scholar-Scholarly."""
        search_query = scholarly.search_pubs(query)
        return [next(search_query) for _ in range(10)]
    
    def main():
        query = input("Research Question: ")
        api_key = "SerpAPI_Key"
        
        print("\nGathering results from SerpAPI...\n")
        SerpAPI_results = search_scholar_serpapi(query, api_key)
        for i, result in enumerate(serpapi_results, 1):
            print(f"{i}. {result['title']}")
            print(f" Link: {result.get('link', 'No link')}")
            print(f" Description: {result.get('Description', 'No Description')}\n")
            
if __name__ == "__main__":
    main()