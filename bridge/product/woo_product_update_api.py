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


class WooProductUpdateApi(Flask):
    """
    WooProductUpdateApi class aims to provide an API for updating a product in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    update_product: Update product method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/product/update", methods=["POST"])(self.update_product_event)
        self.route("/", methods=["GET"])(self.api_info_event)
        
        
    def api_info_event(self):
        """
        API info method
        """
        
        api_usage = {
            "API": "WooCommerce Product Update API",
            "Description": "This API allows you to update a product in WooCommerce.",
            "Endpoints": {
                "/product/update": {
                    "Description": "Update a product in WooCommerce.",
                    "Method": "POST",
                    "Request Body": {
                        "product_id": "int",
                        "name": "string",
                        "sku": "string",
                        "regular_price": "string",
                        "description": "string",
                        "short_description": "string",
                        "image_id": "int",
                        "main_category": "string"
                    },
                    "Response": {
                        "success": "Product updated successfully."
                    }
                }
            }
        }
        
        return jsonify(api_usage)
    
    def update_product_event(self):
        """
        Update product event method
        """
        product_id = request.form.get("product_id")
        if not product_id:
            return jsonify({"error": "Please provide the product ID."}), 400
        
        data = {
            "name": request.form.get("name"),
            "sku": request.form.get("sku"),
            "regular_price": request.form.get("regular_price"),
            "description": request.form.get("description"),
            "short_description": request.form.get("short_description"),
            "categories": [
                {
                    "id": request.form.get("main_category")
                }
            ],
            "images": [
                {
                    "id": request.form.get("image_id")
                }
            ]
        }
        
        response = wcapi.put(f"products/{product_id}", data).json()
        
        return jsonify(response)

