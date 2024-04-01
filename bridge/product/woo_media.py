import csv
import json
import os
import sys
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


def main():
    """
    Main function to read products from a CSV file and post them to the WooCommerce store.
    """
    # Download all media items from the store with 175 pages
    start_page = sys.argv[1]
    end_page = sys.argv[2]
    
    if not start_page or not end_page:
        print("Please provide the start and end page numbers.")
        return
    
    download_media_and_ids_as_csv(os.getenv("WOOCOMMERCE_STORE_URL"), int(start_page), int(end_page))
    
    # Read id,url from the MEDIA.csv file and assign it to a dictionary
    media_csv_base = os.path.join(os.getcwd(), "csv_data")
    media_dict = {}
    with open(os.path.join(media_csv_base, "MEDIA.csv"), "r", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        # Loop through each row in the CSV file
        for row in csv_reader:
            media_dict[row['url']] = row['id']
            
            
if __name__ == "__main__":
    main()
            
    