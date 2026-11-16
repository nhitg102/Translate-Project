
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MICROSOFT_TRANSLATOR_KEY")
ENDPOINT = os.getenv(
    "MICROSOFT_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com"
)

url = f"{ENDPOINT}/translate"

params = {
    "api-version": "3.0",
    "from": "en",
    "to": "vi"
}

headers = {
    "Ocp-Apim-Subscription-Key": API_KEY.strip(),
    "Ocp-Apim-Subscription-Region": "eastasia",
    "Content-Type": "application/json"
}

body = [
    {"text": "Hello! Welcome to our translation application."}
]

try:
    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=body,
        timeout=30
    )

    response.raise_for_status()

    result = response.json()
    print("Original:", body[0]["text"])
    print("Translation:", result[0]["translations"][0]["text"])
    print("API connection successful!")

except requests.exceptions.RequestException as error:
    print("API connection failed:", error)
    if getattr(error, "response", None) is not None:
        print(error.response.text)


REGION = os.getenv("MICROSOFT_TRANSLATOR_REGION")

headers = {
    "Ocp-Apim-Subscription-Key": API_KEY.strip(),
    "Ocp-Apim-Subscription-Region": REGION,
    "Content-Type": "application/json"
}