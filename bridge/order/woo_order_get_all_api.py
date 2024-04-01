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


class WooOrderGetAllApi(Flask):
    """
    WooOrderGetAllApi class aims to provide an API for getting all orders in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    get_all_orders: Get all orders method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/order/get_all", methods=["GET"])(self.get_all_orders_event)
        self.route("/", methods=["GET"])(self.api_info_event)
    
    def get_all_orders_event(self):
        """
        Get all orders method
        """
        orders = wcapi.get("orders").json()
        return jsonify(orders)
    
    def api_info_event(self):
        """
        API info method
        """
        return jsonify({"message": "WooCommerce Order Get All API"})
    
