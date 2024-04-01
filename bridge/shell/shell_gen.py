import csv
import os

from PIL import Image


def generate_wp_import_script(media_folder):
    """
    Generate a shell script for importing images into WordPress.
    """
    # Check if the directory exists
    if not os.path.isdir(media_folder):
        print(f"The directory {media_folder} does not exist.")
        return

    # Get a list of all .jpg files in the directory
    files = [f for f in os.listdir(media_folder) if f.endswith('.jpg')]

    # Check if there are any .jpg files in the directory
    if not files:
        print(f"There are no .jpg files in the directory {media_folder}.")
        return

    # Check if the files are valid images
    for file in files:
        try:
            with Image.open(os.path.join(media_folder, file)) as img:
                img.verify()
        except (IOError, SyntaxError):
            print(f"The file {file} is not a valid image.")
            return

    # Generate the script
    script = f"#!/bin/bash\ncd {media_folder}\nwp media import *.jpg"

    # Write the script to a file
    with open("wp_import_script.sh", "w", newline='', encoding='utf-8') as f:
        f.write(script)

    print("The script has been generated successfully.")


def generate_wc_import_script(csv_file, cli_user):
    """
    Generate a shell script for importing products into WooCommerce.
    """
    # Check if the CSV file exists
    if not os.path.isfile(csv_file):
        print(f"The file {csv_file} does not exist.")
        return
    
    if not cli_user:
        print("WP-CLI user is required to generate the shell script.")
        return

    # Check the CSV headers
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)

    required_headers = ['type', 'sku', 'name', 'status', 'featured', 'catalog_visibility', 'short_description', 
                        'description', 'date_on_sale_from', 'date_on_sale_to', 'tax_status', 'tax_class', 
                        'stock_status', 'backorders', 'sold_individually', 'weight', 'length', 'width', 'height', 
                        'reviews_allowed', 'purchase_note', 'sale_price', 'regular_price', 'categories', 
                        'tags', 'shipping_class', 'images', 'download_limit', 'download_expiry', 'parent', 
                        'grouped_products', 'upsell_ids', 'cross_sell_ids', 'user', 'position', 'stock', 
                        'category_ids', 'tag_ids', 'shipping_class_id', 'downloads', 'image_id', 
                        'gallery_image_ids', 'download_limit', 'download_expiry', 'rating_counts', 'average_rating', 
                        'review_count']

    for header in required_headers:
        if header not in headers:
            print(f"The CSV file is missing the required header: {header}")
            return

    # Generate the script
    script = f"#!/bin/bash\nwp wc product csv import {csv_file} --user={cli_user}"

    # Write the script to a file
    with open("wc_import_script.sh", "w", newline='', encoding='utf-8') as f:
        f.write(script)

    print("The script has been generated successfully.")


