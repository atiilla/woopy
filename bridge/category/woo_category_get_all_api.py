import os

import woocommerce
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

wcapi = woocommerce.API(
    url=os.getenv("WOOCOMMERCE_STORE_URL"),
    consumer_key=os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
    consumer_secret=os.getenv("WOOCOMMERCE_CONSUMER_SECRET"),
)


class WooCategoryGetAllApi(Flask):
    """
    WooCategoryCreateApi class aims to provide an API for getting all categories in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    get_all_categories: Get all categories method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/category/get_all", methods=["GET"])(self.get_all_categories)
        self.route("/", methods=["GET"])(self.api_info)
        
    def get_all_categories(self):
        """
        Get all categories method
        """
        response = wcapi.get("products/categories").json()
        
        return jsonify(response)
    

    def api_info(self):
        """
        API info method
        """
        
        api_usage = {
            "API": "WooCommerce Category Get All API",
            "Description": "This API allows you to get all categories in WooCommerce.",
            "Endpoints": {
                "/category/get_all": {
                    "Description": "Get all categories.",
                    "Methods": ["GET"],
                }
            }
        }
        
        return jsonify(api_usage)
    
    
