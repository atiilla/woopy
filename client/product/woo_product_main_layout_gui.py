from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen

from client.product.woo_product_create_gui import WooCreateProductGui
from client.product.woo_product_get_all_gui import WooGetAllProductsGui
from client.product.woo_product_get_one_gui import WooGetOneProductGui
from client.product.woo_product_get_search_gui import WooSearchProductGui
from client.product.woo_product_update_gui import WooUpdateProductGui

# Build a layout to open sub-screens such as product -> WooCreateProductGui, WooUpdateProductGui, WooGetCategoriesGui, etc.

class WooProductMainLayout(MDApp):
    """
    The main layout GUI class for the application.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.actions_layout = MDGridLayout(cols=3, padding=10, spacing=10)
        
        self.navigate_to_create_button = MDRectangleFlatButton(text="Create")
        self.navigate_to_update_button = MDRectangleFlatButton(text="Update")
        self.navigate_to_delete_button = MDRectangleFlatButton(text="Delete")
        self.navigate_to_get_one_button = MDRectangleFlatButton(text="Get One")
        self.navigate_to_search_button = MDRectangleFlatButton(text="Search")
        self.navigate_to_get_all_button = MDRectangleFlatButton(text="Get All")
        
        self.actions_layout.add_widget(self.navigate_to_create_button)
        self.actions_layout.add_widget(self.navigate_to_update_button)
        self.actions_layout.add_widget(self.navigate_to_delete_button)
        self.actions_layout.add_widget(self.navigate_to_get_one_button)
        self.actions_layout.add_widget(self.navigate_to_search_button)
        self.actions_layout.add_widget(self.navigate_to_get_all_button)
        
    def build(self):
        """
        Builds the main layout of the application.
        
        Returns:
            MDScreen: The main screen of the application.
        """
        screen = MDScreen()
        screen.add_widget(self.actions_layout)
        
        self.navigate_to_create_button.bind(on_release=self.navigate_to_create)
        self.navigate_to_update_button.bind(on_release=self.navigate_to_update)
        self.navigate_to_delete_button.bind(on_release=self.navigate_to_delete)
        self.navigate_to_get_one_button.bind(on_release=self.navigate_to_get_one)
        self.navigate_to_search_button.bind(on_release=self.navigate_to_search)
        self.navigate_to_get_all_button.bind(on_release=self.navigate_to_get_all)
        
        return screen
    
    def stop_app(self, instance):
        """
        Stops the application.
        
        Args:
            instance: The instance that triggered the event.
        """
        print(f"Stopping the app from {instance}")
        self.stop()
    
    def navigate_to_create(self, instance):
        """
        Navigates to the product screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
        WooCreateProductGui().run()
        
    def navigate_to_update(self, instance):
        """
        Navigates to the category screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
        WooUpdateProductGui().run()
        
    def navigate_to_delete(self, instance):
        """
        Navigates to the category screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
        WooDeleteProductGui().run()
        
    def navigate_to_get_one(self, instance):
        """
        Navigates to the category screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
        WooGetOneProductGui().run()
        
    def navigate_to_search(self, instance):
        """
        Navigates to the category screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
        WooSearchProductGui().run()
        
    def navigate_to_get_all(self, instance):
        """
        Navigates to the category screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
        WooGetAllProductsGui().run()

            
        