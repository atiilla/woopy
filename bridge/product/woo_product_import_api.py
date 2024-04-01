import csv
import os
import time

import woocommerce
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

wcapi = woocommerce.API(
    url=os.getenv("WOOCOMMERCE_STORE_URL"),
    consumer_key=os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
    consumer_secret=os.getenv("WOOCOMMERCE_CONSUMER_SECRET"),
)


class WooProductImportApi(Flask):
    """
    WooProductImportApi class aims to provide an API for importing products in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    import_product_event: Import product event method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/product/import", methods=["POST"])(self.import_product_event)
        self.route("/", methods=["GET"])(self.api_info_event)
    
    def import_product_event(self):
        """
        Import product event method
        """
        # Read id,url from the MEDIA.csv file and assign it to a dictionary
        media_csv_base = os.path.join(os.getcwd(), request.form.get("base_path"))
        media_dict = {}
        with open(os.path.join(media_csv_base, "MEDIA.csv"), "r", encoding="utf-8") as f:
            csv_reader = csv.DictReader(f)
            # Loop through each row in the CSV file
            for row in csv_reader:
                media_dict[row['url']] = row['id']

        # Read the products from the CSV file
        product_csv_path = request.form.get("csv_path")
        if not product_csv_path:
            return jsonify({"error": "Please provide the path to the products CSV file."}), 400

        
        products = self.get_all_products_event(os.path.join(media_csv_base, product_csv_path))
        responses = []
        errors = []
        # Create products from the list
        for product in products:
            
            # Create the product
            response = wcapi.post("products", product)
            time.sleep(0.5)
            
            if response.status_code != 201:
                errors.append(response.json())
            else:
                responses.append(response.json())
            
        if errors:
            return jsonify({"errors": errors}), 400
        
        return jsonify({"responses": responses})
    
    
    def get_all_products_event(self, product_csv_path):
        """
        Get all products method
        """
        products = []
        with open(product_csv_path, "r", encoding="utf-8") as f:
            csv_reader = csv.DictReader(f)
            # Loop through each row in the CSV file
            for row in csv_reader:
                products.append(row)
        
        return products
    
    
    def api_info_event(self):
        """
        API info method
        """
        
        api_usage = {
            "API": "WooCommerce Product Import API",
            "Description": "This API allows you to import products in WooCommerce.",
            "Endpoints": {
                "/product/import": {
                    "Description": "Import products in WooCommerce",
                    "Method": "POST",
                    "Data": {
                        "product_csv_path": "Path to the products CSV file",
                    },
                },
            },
        }
        
        return jsonify({"message": api_usage})
    
    
