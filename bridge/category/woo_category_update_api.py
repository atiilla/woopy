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


class WooCategoryUpdateApi(Flask):
    """
    WooCategoryCreateApi class aims to provide an API for updating category name by given ID in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    update_category: Update category method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/category/update", methods=["POST"])(self.update_category)
        self.route("/", methods=["GET"])(self.api_info)
        
    def update_category(self):
        """
        Update category method
        """
        category_id = request.json.get("category_id")
        category_name = request.json.get("category_name")
        
        if not category_id:
            return jsonify({"error": "Please provide a category ID."}), 400
        
        if not category_name:
            return jsonify({"error": "Please provide a category name."}), 400
        
        data = {
            "name": category_name,
        }
        
        response = wcapi.put(f"products/categories/{category_id}", data).json()
        
        return jsonify(response)
    
    
    def api_info(self):
        """
        API info method
        """
        
        api_usage = {
            "API": "WooCommerce Category Update API",
            "Description": "This API allows you to update a category name by given ID in WooCommerce.",
            "Endpoints": {
                "/category/update": {
                    "Description": "Update a category name by given ID.",
                    "Methods": ["POST"],
                    "Body": {
                        "category_id": "The ID of the category to update.",
                        "category_name": "The new name of the category."
                    },
                    "Returns": {
                        "id": "The ID of the category.",
                        "name": "The name of the category.",
                    }
                }
            }
        }
        
        return jsonify(api_usage)
    
    
