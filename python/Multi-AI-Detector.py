import requests
import json
from urllib.parse import quote

# User-defined API keys and tokens
WINSTON_API_KEY = "Your API Key here"
WINSTON_BEARER_TOKEN = "Your Token here"
ORIGINALITY_API_KEY = "Your API Key here"
GPTZERO_API_KEY = "Your API Key here"

# This api may not be accessible
# def callAIContentDetector_v1(text):
#     endpoint_url = 'https://cdapi.goom.ai/api/v1/content/detect'
#     headers = {'Content-Type': 'application/json', 'referer': 'https://contentdetector.ai/'}
#     data = {"content": text}
#     response = requests.post(endpoint_url, headers=headers, json=data)
#     if response.status_code == 200:
#         return json.loads(response.text)['fake_probability']
#     else:
#         return "Error"

def zerogpt(text):
    base_url = 'https://zerogpt.cc/'
    # Encode the text to be URL-safe
    encoded_text = quote(text)
    full_url = f"{base_url}?Abstract={encoded_text}"

    response = requests.get(full_url)

    # Print the entire response body to debug
    # print(response.text)
    if response.status_code == 200:
        # Assuming the API returns JSON, parse it and extract the desired data
        return response.json().get('fake_probability', -1)  # Replace 'score' with the actual key you need
    else:
        return f"Error: {response.status_code}, {response.text}"

def contentdetectorai(text):
    endpoint_url = 'https://api.contentdetector.ai/api/v2/detect/ai_content'
    headers = {'Content-Type': 'application/json', 'referer': 'https://contentdetector.ai/'}
    data = {"content": text}
    response = requests.post(endpoint_url, headers=headers, json=data)
    if response.status_code == 200:
        return json.loads(response.text).get('ai_percentage', -1) / 100  # Normalize to [0, 1]
    else:
        return "Error"

def winstonai(text):
    API_URL = "https://api.gowinston.ai/functions/v1/predict"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkZ3NzdXRyaHpya2xsc3RnbGRiIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODY2ODc5MjMsImV4cCI6MjAwMjI2MzkyM30.bwSe1TrFMhcosgqFSlGIhMIv9fxohzLG0eyBEs7wUo8'
    }
    data = {
        "api_key": WINSTON_API_KEY,
        "text": text,
        "sentences": True,
        "language": "en"
    }
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        score = response.json().get('score', None)
        if score is not None:
            return 1 - (score / 100)  # Normalize to [0, 1] and invert
        else:
            return "Error: Score is None"
    else:
        return "Error: API Request Failed"

def originalityai(text):
    BASE_URL = "https://api.originality.ai/api/v1/scan/ai"
    headers = {
        "Accept": "application/json",
        "X-OAI-API-KEY": ORIGINALITY_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "content": text,
        "title": "optional title", 
        "aiModelVersion": "1",
        "storeScan": False  
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["score"]["ai"]
    else:
        return f"Error {response.status_code}: {response.text}"

def gptzero(text):
    API_URL = "https://api.gptzero.me/v2/predict/text"
    headers = {
        "x-api-key": GPTZERO_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"document": text, "version": "2023-09-14"}
    response = requests.post(API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['documents'][0]['completely_generated_prob']
    else:
        return "Error"

if __name__ == "__main__":
    user_input = input("Please enter the text you want to analyze: ")

    print("Sending the text to various APIs for analysis... Note that if the result is closer to 0 it means it is more likely to have been written by a human, and closer to 1 it means it is likely to have been generated by an AI.")
    zerogpt_result = zerogpt(user_input)
    contentdetectorai_result = contentdetectorai(user_input)
    winstonai_result = winstonai(user_input)
    originalityai_result = originalityai(user_input)
    gptzero_result = gptzero(user_input)
    
    print(f"ZeroGPT Result: {zerogpt_result}")
    print(f"ContentDetector.AI Result: {contentdetectorai_result}")
    print(f"Winston.AI Result: {winstonai_result}")
    print(f"Originality.AI Result: {originalityai_result}")
    print(f"GPTZero Result: {gptzero_result}")
