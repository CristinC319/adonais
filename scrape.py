import requests
import random
import os
from read_creds import read_creds

DESIRED_RESULTS = ["shopping_results", "recipes_results","related_search_boxes", "organic_results"]
SHOPPING_RESULTS_KEY = ["title", "link", "thumbnail"]
SERP_API_KEY = os.environ.get('SERP_API_KEY')
print(SERP_API_KEY)

def search_direct_request(params):
    read_creds()
    base_url = 'https://serpapi.com/search.json'
    resp = requests.get(base_url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        assert(isinstance(data, dict))
        return data
    else:
        print("serp direct request failed with", resp.status_code)
        return None

def scrape_topic(topic="Things to do in San Francisco", location="San Francisco"):
    '''
    input: topic (one word typically, but could be any search query)
    optional: location (natural language string)
    output: One Ad as a list {title:'', link:'', thumbnail:''}
    OR None --- HANDLE THIS CASE
    uses SERP API: https://serpapi.com/search-api
    '''
    params = {
            "api_key": SERP_API_KEY, # https://serpapi.com/manage-api-key
            "engine": "google",
            "gl": "us",
            "hl": "en",
            "location": location,
            "safe": "active",
            "num": 5
        }

    params["q"] = topic
    results = search_direct_request(params)
    if results:
        for kind in DESIRED_RESULTS: 
            if kind in results: # and len(ads) < 2:
                for element in results[kind]:
                    if isinstance(element, dict) and 'thumbnail' in element: # and len(ads) < 2:
                        ad = {key: element[key] for key in SHOPPING_RESULTS_KEY}
                        if 'price' in element:
                            ad['price'] = element['price']
                        ad["rating"] = 5 - random.random() #- len(ads) + .1 * len(ads)
                        print("scrape_topic got ad")
                        assert(isinstance(ad, dict))
                        return ad
    else:
        return None

def get_ads(topic_list):
    '''
    input: list of topics, []
    output: json ads {}
    '''
    ads = []
    for topic in topic_list:
        ad = scrape_topic(topic)
        if ad:
            ads.append(ad)
    return ads[:2]
