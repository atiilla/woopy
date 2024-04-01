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


class WooProductGetOneApi(Flask):
    """
    WooProductGetOneApi class aims to provide an API for getting one product in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    get_one_product: Get one product method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/product/get_one", methods=["POST"])(self.get_one_product_event)
        self.route("/", methods=["GET"])(self.api_info_event)
    
    def get_one_product_event(self):
        """
        Get one product method
        """
        product_id = request.json.get("product_id")
        product = wcapi.get(f"products/{product_id}").json()
        return jsonify(product)
    
    def api_info_event(self):
        """
        API info method
        """
        return jsonify({"message": "WooCommerce Product Get One API"})