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


class WooCategoryDeleteApi(Flask):
    """
    WooCategoryCreateApi class aims to provide an API for deleting a category by given ID in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    delete_category: Delete category method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/category/delete", methods=["POST"])(self.delete_category)
        self.route("/", methods=["GET"])(self.api_info)
        
    def delete_category(self):
        """
        Update category method
        """
        category_id = request.json.get("category_id")
        
        if not category_id:
            return jsonify({"error": "Please provide a category ID."}), 400
        
        response = wcapi.delete(f"products/categories/{category_id}", params={"force": True}).json()
        
        return jsonify(response)
    
    
    def api_info(self):
        """
        API info method
        """
        
        api_usage = {
            "API": "WooCommerce Category Delete API",
            "Description": "This API allows you to delete a category in WooCommerce.",
            "Endpoints": {
                "/category/delete": {
                    "Description": "Delete a category by given ID.",
                    "Methods": ["POST"],
                    "Body": {
                        "category_id": "The ID of the category to delete."
                    },
                    "Returns": {
                        "id": "The ID of the category.",
                        "name": "The name of the category.",
                        "slug": "The slug of the category.",
                        "parent": "The parent category ID.",
                        "description": "The description of the category.",
                        "display": "The display type of the category.",
                        "image": "The image URL of the category.",
                        "menu_order": "The order of the category in the menu.",
                        "count": "The number of products in the category."
                    }
                }
            }
        }
        
        return jsonify(api_usage)

