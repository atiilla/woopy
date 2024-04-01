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


class WooProductCreateApi(Flask):
    """
    WooProductCreateApi class aims to provide an API for creating a product in WooCommerce
    
    Args:
    Flask: The Flask class is the base
    
    Methods:
    create_product: Create product method
    
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.route("/product/create", methods=["POST"])(self.create_product_event)
        self.route("/", methods=["GET"])(self.api_info_event)
        
        
    def api_info_event(self):
        """
        API info method
        """
        
        api_usage = {
            "API": "WooCommerce Product Create API",
            "Description": "This API allows you to create a product in WooCommerce.",
            "Endpoints": {
                "/product/create": {
                    "Description": "Create a product in WooCommerce.",
                    "Method": "POST",
                    "Request Body": {
                        "name": "string",
                        "sku": "string",
                        "regular_price": "string",
                        "description": "string",
                        "short_description": "string",
                        "image_id": "int",
                        "main_category": "string"
                    },
                    "Response": {
                        "success": "Product created successfully."
                    }
                }
            }
        }
        
        return jsonify(api_usage)

    
    
    def create_product_event(self):
        """
        Create product method
        """
        name = request.json.get("name")
        sku = request.json.get("sku")
        regular_price = request.json.get("regular_price")
        description = request.json.get("description")
        short_description = request.json.get("short_description")
        image_id = request.json.get("image_id")
        main_category = request.json.get("main_category")
        
        if not name or not sku or not regular_price or not description or not short_description or not main_category:
            return jsonify({"error": "Please provide all the required fields."}), 400
        
        # Construct product object
        create_product_request = {
            "name": name,
            "type": "simple",
            "sku": sku,
            "price": regular_price,
            "regular_price": regular_price,
            "on_sale": False,
            "description": description,
            "short_description": short_description,
            "categories": [
                {
                    "id": main_category
                }
            ],
            "manage_stock": True,
            "stock_quantity": 2000,
            "in_stock": True,
            "reviews_allowed": True,
            "tax_status": "taxable",
            "status": "publish",
            "catalog_visibility": "visible",
            "total_sales": 0,
            "virtual": False,
            "downloadable": False,
            "downloads": [],
            "download_limit": -1,
            "download_expiry": -1,
            "average_rating": "0.00",
            "rating_count": 0,
            "related_ids": [],
            "upsell_ids": [],
            "cross_sell_ids": [],
            "parent_id": 0,
            "purchase_note": "",
            "images": [
                {
                    "id": image_id,
                    "position": 0
                }
            ]
        }
        
        # Create the product
        response = wcapi.post("products", create_product_request)
        
        if response.status_code != 201:
            return jsonify({"error": "Failed to create product."}), 500
        
        return jsonify({"success": f"Product with ID {response.json()['id']} created successfully."})
        

