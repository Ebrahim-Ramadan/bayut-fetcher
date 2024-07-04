import requests
import json
import csv

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
    "x-rapidapi-key": "bayut-api-key",
    "x-rapidapi-host": "bayut.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
json_response = response.json()

# Function to extract location details
def get_location_details(location_array):
    city = next((loc['name'] for loc in location_array if loc['level'] == 1), None)
    location1 = next((loc['name'] for loc in location_array if loc['level'] == 2), None)
    location2 = next((loc['name'] for loc in location_array if loc['level'] == 3), None)
    return city, location1, location2

# Prepare data for CSV
csv_data = []
for hit in json_response['hits']:
    city, location1, location2 = get_location_details(hit.get('location', []))
    full_address = ', '.join(filter(None, [loc.get('name') for loc in reversed(hit.get('location', []))]))
    
    row = {
        'Link': f"https://www.bayut.com/property/{hit.get('externalID')}" if hit.get('externalID') else None,
        'Bedrooms': hit.get('rooms', None),
        'Bathrooms': hit.get('baths', None),
        'Area': round(hit.get('area', 0) * 0.092903, 2),  # Convert sq ft to sq meters
        'Price': hit.get('price', None),
        'Address': full_address,
        'City': city,
        'Location 1': location1,
        'Location 2': location2,
        'Unit': hit.get('category', [{}])[0].get('nameSingular', None),
        'Type': hit.get('purpose', '').split('-')[0] if hit.get('purpose') else None,
        'Rent_sale': 'Rent' if hit.get('purpose') == 'for-rent' else 'Sale'
    }
    csv_data.append(row)

# Save to CSV
csv_filename = "property_data.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_data[0].keys())
    writer.writeheader()
    writer.writerows(csv_data)

print(f"Data saved to {csv_filename}")