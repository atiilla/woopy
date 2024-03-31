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


class WooCategoryCreateApi(Flask):
    """
    WooCategoryCreateApi class aims to provide an API for creating a category in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    create_category: Create category method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/category/create", methods=["POST"])(self.create_category)
        self.route("/", methods=["GET"])(self.api_info)
    
    def create_category(self):
        """
        Create category method
        """
        category_name = request.json.get("category_name")
        
        if not category_name:
            return jsonify({"error": "Please provide a category name."}), 400
        
        data = {
            "name": category_name,
        }
        
        response = wcapi.post("products/categories", data).json()
        
        return jsonify(response)
    

    def api_info(self):
        """
        API info method
        """
        
        api_usage = {
            "API": "WooCommerce Category Create API",
            "Description": "This API allows you to create a category in WooCommerce.",
            "Endpoints": {
                "/category/create": {
                    "Description": "Create a category in WooCommerce",
                    "Method": "POST",
                    "Data": {
                        "category_name": "Category name",
                    },
                },
            },
        }
        
        return jsonify({"message": api_usage})
    

