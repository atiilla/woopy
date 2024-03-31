from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooDeleteProductGui(MDApp):
    """
    WooDeleteProductGui class aims to provide a GUI for deleting a product in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    delete_product_event: Delete product method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.product_id = MDTextField(hint_text="Product ID")
        
        self.delete_product = MDRaisedButton(text="Delete Product", on_release=self.delete_product_event)
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
        app_layout.add_widget(self.delete_product)
        app_layout.add_widget(self.product_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def delete_product_event(self, *args):
        """
        Delete product method
        """
        product_id = self.product_id.text
        self.product_info.text = f"Product ID: {product_id}"
        
        


