import csv
import os
import sys

from client.api.media.woo_media_download_api import \
    download_media_and_ids_as_csv


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
            
