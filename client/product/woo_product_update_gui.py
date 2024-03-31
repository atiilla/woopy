from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooUpdateProductGui(MDApp):
    """
    WooUpdateProductGui class aims to provide a GUI for updating a product in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    update_product_event: Update product method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.product_id = MDTextField(hint_text="Product ID")
        self.product_name = MDTextField(hint_text="Product Name")
        self.product_price = MDTextField(hint_text="Product Price")
        self.product_quantity = MDTextField(hint_text="Product Quantity")
        self.product_description = MDTextField(hint_text="Product Description")
        self.product_image = MDTextField(hint_text="Product Image URL")
        self.product_category = MDTextField(hint_text="Product Category")
        self.product_tags = MDTextField(hint_text="Product Tags")
        
        self.update_product = MDRaisedButton(text="Update Product", on_release=self.update_product_event)
        self.product_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        app_layout.add_widget(self.product_id)
        app_layout.add_widget(self.product_name)
        app_layout.add_widget(self.product_price)
        app_layout.add_widget(self.product_quantity)
        app_layout.add_widget(self.product_description)
        app_layout.add_widget(self.product_image)
        app_layout.add_widget(self.product_category)
        app_layout.add_widget(self.product_tags)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.update_product)
        app_layout.add_widget(self.product_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def update_product_event(self, *args):
        """
        Update product method
        """
        product_id = self.product_id.text
        product_name = self.product_name.text
        product_price = self.product_price.text
        product_quantity = self.product_quantity.text
        product_description = self.product_description.text
        product_image = self.product_image.text
        product_category = self.product_category.text
        product_tags = self.product_tags.text
        self.product_info.text = f"Product ID: {product_id}\nProduct Name: {product_name}\nProduct Price: {product_price}\nProduct Quantity: {product_quantity}\nProduct Description: {product_description}\nProduct Image: {product_image}\nProduct Category: {product_category}\nProduct Tags: {product_tags}"
                

