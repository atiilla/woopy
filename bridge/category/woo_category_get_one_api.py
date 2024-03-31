import os

import woocommerce
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

wcapi = woocommerce.API(
    url=os.getenv("WOOCOMMERCE_STORE_URL"),
    consumer_key=os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
    consumer_secret=os.getenv("WOOCOMMERCE_CONSUMER_SECRET"),
)


class WooCategoryGetOneApi(Flask):
    """
    WooCategoryCreateApi class aims to provide an API for getting a category by ID or slug in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    get_category: Get category method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/category/get", methods=["POST"])(self.get_category)
        self.route("/", methods=["GET"])(self.api_info)
        
    def get_category(self):
        """
        Get category method
        """
        category_id = request.json.get("category_id")
        category_slug = request.json.get("category_slug")
        
        if not category_id and not category_slug:
            return jsonify({"error": "Please provide a category ID or slug."}), 400
        
        if category_id:
            response = wcapi.get(f"products/categories/{category_id}").json()
        else:
            response = wcapi.get("products/categories", params={"slug": category_slug}).json()
        
        return jsonify(response)
    
    
    def api_info(self):
        
        api_usage = {
            "API": "WooCommerce Category Get One API",
            "Description": "This API allows you to get a category by ID or slug in WooCommerce.",
            "Endpoints": {
                "/category/get": {
                    "Description": "Get a category by ID or slug.",
                    "Methods": ["POST"],
                    "Body": {
                        "category_id": "The ID of the category to get.",
                        "category_slug": "The slug of the category to get."
                    }
                }
            }
        }
        
        return jsonify(api_usage)
    
    

    
