import time

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooImportProductGui(MDApp):
    """
    WooImportProductGui class aims to provide a GUI for importing a product in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    import_product_event: Import product method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.product_csv_path = MDTextField(hint_text="Product CSV Path")
        self.import_product = MDRaisedButton(text="Import Product", on_release=self.import_product_event)
        self.product_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        app_layout.add_widget(self.product_csv_path)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.import_product)
        app_layout.add_widget(self.product_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def import_product_event(self, *args):
        """
        Import product method
        """
        csv_path = self.product_csv_path.text
        self.product_info.text = "Product import started: " + csv_path
        # Add a sleep to simulate the import process
        time.sleep(5)
        self.product_info.text = "Product import completed: " + csv_path
        
        
        
