from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooCreateOrderGui(MDApp):
    """
    WooCreateOrderGui class aims to provide a GUI for creating a order in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    create_order_event: Create order method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.products_layout = MDGridLayout(cols=3, padding=10)
        self.products_items = []
        self.ordered_items = []
        
        # Create 10 demo products using a loop and add them to the products_layout
        for i in range(10):
            product = MDTextField(hint_text=f"Product {i}")
            self.products_items.append(product)
            self.products_layout.add_widget(product)
        
        self.add_order = MDRaisedButton(text="Add Order", on_release=self.add_order_event)
        self.order_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        app_layout.add_widget(self.products_layout)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.add_order)
        app_layout.add_widget(self.order_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def add_order_event(self, *args):
        """
        Add order method
        """
        self.order_info.text = "Adding order"
        self.ordered_items = []
        
        for product in self.products_items:
            if product.text:
                self.ordered_items.append(product.text)
                
        self.order_info.text = f"Ordered Items: {self.ordered_items}"
        

def main():
    """
    Main function
    """
    WooCreateOrderGui().run()
    
if __name__ == '__main__':
    main()



