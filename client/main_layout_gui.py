from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen

from client.product.woo_product_main_layout_gui import WooProductMainLayout

# Build a layout to open sub-screens such as product -> WooCreateProductGui, WooUpdateProductGui, WooGetCategoriesGui, etc.

DRAWER_WIDTH = 180

class MainLayoutGui(MDApp):
    """
    The main layout GUI class for the application.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.drawer = MDNavigationDrawer()
        # set drawer open state
        self.drawer.set_state("open")
        self.drawer.width = DRAWER_WIDTH
        self.drawer.anchor = "left"
        
        self.vertical_layout = MDGridLayout(cols=1, padding=10, spacing=10)
        
        self.navigate_to_product_button = MDRectangleFlatButton(text="Product")
        self.navigate_to_category_button = MDRectangleFlatButton(text="Category")
        self.navigate_to_order_button = MDRectangleFlatButton(text="Order")
        self.navigate_to_customer_button = MDRectangleFlatButton(text="Customer")

        self.close_button = MDRectangleFlatButton(text="Close")
        
        self.vertical_layout.add_widget(self.navigate_to_product_button)
        self.vertical_layout.add_widget(self.navigate_to_category_button)
        self.vertical_layout.add_widget(self.navigate_to_order_button)
        self.vertical_layout.add_widget(self.navigate_to_customer_button)
        
        self.vertical_layout.add_widget(self.close_button)
        
        self.drawer.add_widget(self.vertical_layout)
        
        
    def build(self):
        """
        Builds the main layout of the application.
        
        Returns:
            MDScreen: The main screen of the application.
        """
        screen = MDScreen()
        screen.add_widget(self.drawer)
        
        # Bind the buttons to their respective functions
        self.navigate_to_product_button.bind(on_release=self.navigate_to_product)
        self.navigate_to_category_button.bind(on_release=self.navigate_to_category)
        self.navigate_to_order_button.bind(on_release=self.navigate_to_order)
        self.navigate_to_customer_button.bind(on_release=self.navigate_to_customer)
        
        self.close_button.bind(on_release=self.stop_app)
        
        return screen
    
    def stop_app(self, instance):
        """
        Stops the application.
        
        Args:
            instance: The instance that triggered the event.
        """
        print(f"Stopping the app from {instance}")
        self.stop()
    
    def navigate_to_product(self, instance):
        """
        Navigates to the product screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
        WooProductMainLayout().run()
        
    def navigate_to_category(self, instance):
        """
        Navigates to the category screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
        
        
    def navigate_to_order(self, instance):
        """
        Navigates to the order screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
        
    
    def navigate_to_customer(self, instance):
        """
        Navigates to the customer screen.
        
        Args:
            instance: The instance that triggered the event.
        """
        self.stop_app(instance)
    