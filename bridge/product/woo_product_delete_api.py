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


class WooProductDeleteApi(Flask):
    """
    WooProductDeleteApi class aims to provide an API for deleting a product in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    delete_product: Delete product method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/product/delete", methods=["POST"])(self.delete_product_event)
        self.route("/", methods=["GET"])(self.api_info_event)
        
        
    def api_info_event(self):
        """
        API info method
        """
        
        api_usage = {
            "API": "WooCommerce Product Delete API",
            "Description": "This API allows you to delete a product in WooCommerce.",
            "Endpoints": {
                "/product/delete": {
                    "Description": "Delete a product in WooCommerce.",
                    "Method": "POST",
                    "Request Body": {
                        "product_id": "int"
                    },
                    "Response": {
                        "success": "Product deleted successfully."
                    }
                }
            }
        }
        
        return jsonify(api_usage)
    
    
    def delete_product_event(self):
        """
        Delete product method
        """
        
        data = request.get_json()
        
        product_id = data.get("product_id")
        
        wcapi.delete(f"products/{product_id}")
        
        return jsonify({"success": "Product deleted successfully."})
    
