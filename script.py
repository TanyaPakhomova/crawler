import requests
import json
import sys

url = "https://goldapple.ru/front/api/catalog/plp"
payload = {
    "categoryId": 1000000006,
    "cityId": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
    "cityDistrict": None,
    "filters": [],
    "pageNumber": 1
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

# Check the status code of the response
if response.status_code == 200:
    # Pretty print the JSON response
    formatted_response = json.dumps(response.json(), indent=2)
    print(formatted_response)
else:
    sys.exit(1)

