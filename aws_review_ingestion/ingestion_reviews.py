import os
import json
import requests
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError

FETCHLAYER_API_KEY = os.getenv("FETCHLAYER_API_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

APPS = {
    "zoom": "us.zoom.videomeetings",
    "google_meet": "com.google.android.apps.tachyon",
    "microsoft_teams": "com.microsoft.teams",
    "webex": "com.cisco.webex.meetings"
}

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)

def fetch_reviews(app_id):
    """
    Fetch the newest reviews from FetchLayer.
    """

    url = "https://api.fetchlayer.dev/playstore/reviews"

    headers = {
        "Authorization": f"Bearer {FETCHLAYER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "appIdOrUrl": app_id,
        "sortBy": "newest",
        "startPage": 1,
        "reviewsPerPage": 200,
        "pages": 2,
        "maxReviews": 400,
        "language": ["en"],
        "uniqueOnly": True
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"FetchLayer request failed for {app_id}: {e}")
        return None


def load_state(product):
    """
    Load previous watermark and known review IDs from S3.
    """

    key = f"state/{product}.json"

    try:
        response = s3.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=key
        )

        return json.loads(
            response["Body"].read().decode("utf-8")
        )

    except ClientError as e:

        error_code = e.response["Error"]["Code"]

        if error_code in ("NoSuchKey", "404"):
            print(f"No previous state found for {product}.")
            return {
                "latest_timestamp": None,
                "seen_review_ids": []
            }

        raise


def save_state(product, state):
    """
    Save updated watermark/state to S3.
    """

    key = f"state/{product}.json"

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=key,
        Body=json.dumps(
            state,
            ensure_ascii=False,
            indent=2
        ).encode("utf-8"),
        ContentType="application/json"
    )


def upload_new_reviews(product, app_id, reviews, old_watermark):
    """
    Upload only the newly discovered reviews.
    """

    if not reviews:
        print(f"{product}: No new reviews to upload.")
        return

    timestamps = [
        review.get("timestamp")
        for review in reviews
        if review.get("timestamp")
    ]

    newest_timestamp = max(timestamps) if timestamps else None

    ingestion_time = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%dT%H-%M-%SZ")

    key = (
        f"raw/{product}/"
        f"{ingestion_time}.json"
    )

    output = {
        "product": product,
        "app_id": app_id,
        "ingested_at": ingestion_time,
        "previous_watermark": old_watermark,
        "latest_timestamp": newest_timestamp,
        "new_review_count": len(reviews),
        "reviews": reviews
    }

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=key,
        Body=json.dumps(
            output,
            ensure_ascii=False,
            indent=2
        ).encode("utf-8"),
        ContentType="application/json"
    )

    print(
        f"{product}: uploaded {len(reviews)} new reviews "
        f"to s3://{S3_BUCKET_NAME}/{key}"
    )

def process_product(product, app_id):

    print("\n" + "=" * 50)
    print(f"Processing: {product}")
    print("=" * 50)

    # 1. Read previous state from S3
    state = load_state(product)

    seen_ids = set(
        state.get("seen_review_ids", [])
    )

    old_watermark = state.get(
        "latest_timestamp"
    )

    print(f"Previous watermark: {old_watermark}")
    print(f"Known review IDs: {len(seen_ids)}")

    # 2. Fetch newest reviews
    data = fetch_reviews(app_id)

    if not data:
        print(f"{product}: API returned no usable data.")
        return

    reviews = data.get("reviews", [])

    print(
        f"{product}: fetched {len(reviews)} reviews from API."
    )

    # 3. Identify unseen reviews
    new_reviews = []

    for review in reviews:

        review_id = review.get("reviewId")

        if review_id and review_id not in seen_ids:
            new_reviews.append(review)

    print(
        f"{product}: {len(new_reviews)} unseen reviews found."
    )

    # 4. Nothing new
    if not new_reviews:
        print(
            f"{product}: no new reviews. "
            f"Nothing uploaded."
        )
        return

    # 5. Upload new batch
    upload_new_reviews(
        product,
        app_id,
        new_reviews,
        old_watermark
    )

    # 6. Update known IDs
    for review in new_reviews:

        review_id = review.get("reviewId")

        if review_id:
            seen_ids.add(review_id)

    # 7. Update timestamp watermark
    timestamps = [
        review.get("timestamp")
        for review in reviews
        if review.get("timestamp")
    ]

    if timestamps:
        latest_timestamp = max(timestamps)
    else:
        latest_timestamp = old_watermark

    new_state = {
        "latest_timestamp": latest_timestamp,
        "seen_review_ids": list(seen_ids),
        "last_successful_run": datetime.now(
            timezone.utc
        ).isoformat()
    }

    # 8. Save updated state only after successful upload
    save_state(
        product,
        new_state
    )

    print(
        f"{product}: state updated successfully."
    )


def main():

    required_variables = {
        "FETCHLAYER_API_KEY": FETCHLAYER_API_KEY,
        "S3_BUCKET_NAME": S3_BUCKET_NAME,
        "AWS_REGION": AWS_REGION
    }

    missing = [
        name
        for name, value in required_variables.items()
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing environment variables: {missing}"
        )

    print("Starting incremental review ingestion...")

    for product, app_id in APPS.items():

        try:
            process_product(
                product,
                app_id
            )

        except Exception as e:
            print(
                f"{product}: ingestion failed: {e}"
            )

    print("\nIngestion completed.")


if __name__ == "__main__":
    main()