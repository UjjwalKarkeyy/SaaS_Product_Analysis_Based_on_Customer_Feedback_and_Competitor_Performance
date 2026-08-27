import os
import requests
import json
from dotenv import load_dotenv

def fetch_play_store_reviews(app_id, api_key, startPage=1, pages=10, maxReviews=2000):
    """
        Extract Google Play reviews using the FetchLayer API 
    """

    # fetchlayer endpoint for Google Play Reviews
    url = "https://api.fetchlayer.dev/playstore/reviews"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-type": "application/json"
    }

    body = {
        "appIdOrUrl": app_id,
        "sortBy": "newest",
        "startPage": startPage,
        "reviewsPerPage": 200,
        "pages": pages,
        "maxReviews": maxReviews,
        "language": ["en"],
        "uniqueOnly": True
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=120)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    except requests.exceptions.Timeout:
        print("The request timed out. Try reducing the limit or increasing the timeout threshold.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("PLAY_STORE_API")
    APP_ID = os.getenv("APP_ID")
    print(f"Fetching reviews for {APP_ID} . . .")
    for i in range(0, 4):
        startPage = [1, 11, 21, 31]

        if i in (2, 3):
            data = fetch_play_store_reviews(APP_ID, API_KEY, startPage[i], pages=5, maxReviews=1000)
        else: data = fetch_play_store_reviews(APP_ID, API_KEY, startPage[i])

        if data:
            try:
                ROOT_DIR = os.getenv("ROOT_DIR")
                chunk = f"chunk-{i+1}-startPage-{startPage[i]}"
                with open(f"{ROOT_DIR}\\data\\cisco_webex\\{chunk}\\webex_raw_reviews.json", "w", encoding="utf-8") as file:
                    '''
                        ensure_ascii=False, is so non-ASCII chars aren't saved in escaped Unicode sequence 
                        like instead of '\u00e9', it stores 'é'
                    '''
                    json.dump(data, file, indent=4, ensure_ascii=False) 
                    print(f"Fetched StartPage-{startPage[i]} and dumped json data on {chunk}!")
            except Exception as e:
                print(f"Error occurred: {e}")

