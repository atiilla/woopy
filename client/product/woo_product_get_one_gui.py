from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooGetOneProductGui(MDApp):
    """
    WooGetProductGui class aims to provide a GUI for getting a product in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    get_product_event: Get product method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.product_id = MDTextField(hint_text="Product ID")
        
        self.get_product = MDRaisedButton(text="Get Product", on_release=self.get_product_event)
        self.product_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        app_layout.add_widget(self.product_id)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.get_product)
        app_layout.add_widget(self.product_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def get_product_event(self, *args):
        """
        Get product method
        """
        product_id = self.product_id.text
        self.product_info.text = f"Product ID: {product_id}"
        
        
