import os
import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT").rstrip("/")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = "2023-05-15"

url = f"{endpoint}/openai/deployments?api-version={api_version}"
headers = {"api-key": api_key}

print(f"Requesting: {url}")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("Deployments found:")
    for item in data['data']:
        print(f"- ID: {item['id']}, Model: {item['model']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
