
'''
Web scraper
'''
from serpapi import GoogleSearch 
import requests

GoogleSearch.SERP_API_KEY = "59263e9285646cb5082978e5ec0c18518125436cb81f8e2e37a2855a1ef067f5"
DESIRED_RESULT = "shopping_results"
SHOPPING_RESULTS_KEY = ["title", "link", "thumbnail"]

def search_direct_request(params):
    base_url = 'https://serpapi.com/search.json'

    return requests.get(base_url, params=params)



def scrape_topic(topic="Things to do in San Francisco", location="San Francisco"):
    '''
    input: topic (one word typically, but could be any search query)
    optional: location (natural language string)
    output: One Ad as a list {title:'', link:'', thumbnail:''}
    OR None --- HANDLE THIS CASE
    uses SERP API: https://serpapi.com/search-api
    '''
    params = {
            "api_key": "59263e9285646cb5082978e5ec0c18518125436cb81f8e2e37a2855a1ef067f5",                 # https://serpapi.com/manage-api-key
            "engine": "google",               # search engine
            # "q": "buy rtx 3080",              # search query 
            "gl": "us",                       # country to search from
            "hl": "en",                        # language
            "location": location,
            "safe": "active",
            "num": 5
        }

    params["q"] = topic

    # search = GoogleSearch(params)         # where data extraction happens
    results = search_direct_request(params)
    print(results)
    # results = search.get_dict()           # JSON -> Python dict
    if DESIRED_RESULT in results:
        for element in results[DESIRED_RESULT]:
            return {key: element[key] for key in SHOPPING_RESULTS_KEY}
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
    return ads


# for x in scrape_topic():
#     print(x)
# for x in scrape_topic("coffee"):
#     print(x)


