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


class WooProductGetAllApi(Flask):
    """
    WooProductGetAllApi class aims to provide an API for getting all products in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    get_all_products: Get all products method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/product/get_all", methods=["GET"])(self.get_all_products_event)
        self.route("/", methods=["GET"])(self.api_info_event)
    
    def get_all_products_event(self):
        """
        Get all products method
        """
        products = wcapi.get("products").json()
        return jsonify(products)
    
    def api_info_event(self):
        """
        API info method
        """
        return jsonify({"message": "WooCommerce Product Get All API"})
    
