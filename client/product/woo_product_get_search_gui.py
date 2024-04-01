from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooSearchProductGui(MDApp):
    """
    WooSearchProductGui class aims to provide a GUI for searching a product in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    search_product_event: Search product method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.product_name = MDTextField(hint_text="Product Name")
        
        self.search_product = MDRaisedButton(text="Search Product", on_release=self.search_product_event)
        self.product_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        app_layout.add_widget(self.product_name)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.search_product)
        app_layout.add_widget(self.product_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def search_product_event(self, *args):
        """
        Search product method
        """
        product_name = self.product_name.text
        self.product_info.text = f"Product Name: {product_name}"
        
        
