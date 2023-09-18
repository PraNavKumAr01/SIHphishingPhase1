from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import quote
import requests
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ADD THE ACCESS ORIGINS
origins = ["*"]

# CONFIGURING THE ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLInput(BaseModel):
    url: str

@app.get("/check-url/")
async def check_url(url_input: URLInput):
    url = url_input.url
    
    # URL-encode the input URL
    encoded_url = quote(url, safe="")

    # API endpoint URL
    api_url = f"https://www.ipqualityscore.com/api/json/url/U65ppQwOgV9QLpFJNwGfs8jgXg9pLwBH/{encoded_url}"

    # Send a GET request to the API
    response = requests.get(api_url)

    if response.status_code == 200:
        # API call was successful
        data = response.json()
        # List of keys to exclude
        exclude_keys = ['message', 'success', 'status_code', 'language_code', 'request_id']

        output_data = {key: data[key] for key in data if key not in exclude_keys}
        
        output_json = json.dumps(output_data, indent=4)

        return output_json

    else:
        # API call failed
        return {"error": f"API call failed with status code: {response.status_code}"}
