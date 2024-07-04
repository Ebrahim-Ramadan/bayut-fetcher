import requests
import json

url = "https://bayut.p.rapidapi.com/properties/list"

querystring = {
    "locationExternalIDs": "5002,6020",
    "purpose": "for-rent",
    "hitsPerPage": "25",
    "page": "0",
    "lang": "en",
    "sort": "city-level-score",
    "rentFrequency": "monthly",
    "categoryExternalID": "4"
}

headers = {
    "x-rapidapi-key": "4e8f2d74b0mshaa3d0089a1e11d9p1d2340jsn48f891afc053",
    "x-rapidapi-host": "bayut.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

json_response = response.json()

# Save the JSON response to a file
with open("ass.json", "w") as file:
    json.dump(json_response, file, indent=4)

print("JSON response saved to ass.json")
