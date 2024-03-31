from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooGetProductsGui(MDApp):
    """
    WooGetProductsGui class aims to provide a GUI for getting all products in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    get_products_event: Get products method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.get_products = MDRaisedButton(text="Get Products", on_release=self.get_products_event)
        self.product_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.get_products)
        app_layout.add_widget(self.product_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def get_products_event(self, *args):
        """
        Get products method
        """
        self.product_info.text = "Getting all products"
        
        



