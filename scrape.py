import requests

# GoogleSearch.SERP_API_KEY = "59263e9285646cb5082978e5ec0c18518125436cb81f8e2e37a2855a1ef067f5"
DESIRED_RESULTS = ["shopping_results", "recipes_results","related_search_boxes", "organic_results"]
SHOPPING_RESULTS_KEY = ["title", "link", "thumbnail"]

def search_direct_request(params):
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
    # print(results)
    # results = search.get_dict()           # JSON -> Python dict
    ads = []
    if results:
        for kind in DESIRED_RESULTS: 
            if kind in results and len(ads) < 3:
                for element in results[kind]:
                    if isinstance(element, dict) and 'thumbnail' in element and len(ads) < 3:
                        ad = {key: element[key] for key in SHOPPING_RESULTS_KEY}
                        if 'price' in element:
                            ad['price'] = element['price']
                        ad["rating"] = 5 - len(ads) + .1 * len(ads)
                        print("scrape_topic got ad")
                        assert(isinstance(ad, dict))
                        ads.append(ad)
    else:
        return None

    return ads


def get_ads(topic_list):
    '''
    input: list of topics, []
    output: json ads {}
    '''
    ads = []
    for topic in topic_list:
        new_ads = scrape_topic(topic)
        if new_ads:
            ads = ads + new_ads
    return ads


# for x in scrape_topic():
#     print(x)
# for x in scrape_topic("coffee"):
#     print(x)


