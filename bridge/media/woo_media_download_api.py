import os
import time

import requests
import woocommerce
from dotenv import load_dotenv

load_dotenv()

wcapi = woocommerce.API(
    url=os.getenv("WOOCOMMERCE_STORE_URL"),
    consumer_key=os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
    consumer_secret=os.getenv("WOOCOMMERCE_CONSUMER_SECRET"),
)

def download_media_and_ids_as_csv(site_url: str, start_page, end_page: int):
    """
    Download media items from the WooCommerce store and save them to a CSV file.
    Args:
        site_url (str): The URL of the WooCommerce store.
        number_of_pages (int): The number of pages of media items to download.
    """
    # There are 17,452 media items in the store
    for i in range(start_page, end_page + 1):
        q = f"{site_url}/wp-json/wp/v2/media?page={i}&per_page=100"
        response = requests.get(q, headers={"Accept": "application/json"}, timeout=10)
        response_json = response.json()
        time.sleep(0.15)
        # Add the media items to the CSV file
        with open(os.path.join(os.getcwd(), "csv_data", "MEDIA.csv"), "a", encoding="utf-8") as f:
            # write header if it's the first page
            if i == 1:
                f.write("id,url\n")
            for media in response_json:
                try:
                    media_src = media['media_details']['sizes']['full']['source_url']
                    media_id = media['id']
                    if media_id and media_src:
                        f.write(f"{media_id},{media_src}\n")
                except KeyError:
                    print(f"Media item {media['id']} does not have a source URL.")
                    continue
