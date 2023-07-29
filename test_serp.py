from serpapi import GoogleSearch

params = {
  "engine": "google",
  "q": "Food",
  "api_key": "59263e9285646cb5082978e5ec0c18518125436cb81f8e2e37a2855a1ef067f5"
}

search = GoogleSearch(params)
results = search.get_dict()
# organic_results = results["shopping_results"]

# print(organic_results)
print(results.keys())