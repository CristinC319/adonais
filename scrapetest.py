from serpapi import GoogleSearch
import json 

def search(query):

    params = {
        "api_key": "d793723b97d9613681887babb61cd3b199882d669ef7d72dd3b1db64fc36f2af", # https://serpapi.com/manage-api-key
        "engine": "google", 
        "q": query, 
        "gl": "us", 
        "hl": "en" }

    params["q"] = query

    s = GoogleSearch(params) # data extraction 
    results = s.get_dict() # JSON -> Python dict
    
    if results.get("ads", []):
        for ad in results["ads"]:
            print(json.dumps(ad, indent=2))

    if results.get("shopping_results", []):
        for shopping_ad in results["shopping_results"]:
            print(json.dumps(shopping_ad, indent=2))
    else:
        print("no shopping ads found.")

search("Clothing purple jeans") 