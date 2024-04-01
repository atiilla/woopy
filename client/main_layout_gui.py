from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.screen import MDScreen

from client.product.woo_product_main_layout_gui import WooProductMainLayout

# Build a layout to open sub-screens such as product -> WooCreateProductGui, WooUpdateProductGui, WooGetCategoriesGui, etc.

DRAWER_WIDTH = 120

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
        
        # Set dark theme 
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
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
        
        
    def init_buttons_style(self):
        """
        Initializes the style of the buttons in the GUI.
        
        Sets the following style properties for each button:
        - No background color
        - Light gray text color
        - Bold text
        - Font size of 20
        - Padding of 10
        - Width of 200
        """
        self.navigate_to_product_button.theme_text_color = "Custom"
        self.navigate_to_product_button.text_color = 1, 1, 1, 1
        self.navigate_to_product_button.font_style = "H6"
        self.navigate_to_product_button.font_size = 20
        self.navigate_to_product_button.padding = 10
        self.navigate_to_product_button.width = DRAWER_WIDTH
        
        self.navigate_to_category_button.theme_text_color = "Custom"
        self.navigate_to_category_button.text_color = 1, 1, 1, 1
        self.navigate_to_category_button.font_style = "H6"
        self.navigate_to_category_button.font_size = 20
        self.navigate_to_category_button.padding = 10
        self.navigate_to_category_button.width = DRAWER_WIDTH
        
        self.navigate_to_order_button.theme_text_color = "Custom"
        self.navigate_to_order_button.text_color = 1, 1, 1, 1
        self.navigate_to_order_button.font_style = "H6"
        self.navigate_to_order_button.font_size = 20
        self.navigate_to_order_button.padding = 10
        self.navigate_to_order_button.width = DRAWER_WIDTH
        
        self.navigate_to_customer_button.theme_text_color = "Custom"
        self.navigate_to_customer_button.text_color = 1, 1, 1, 1
        self.navigate_to_customer_button.font_style = "H6"
        self.navigate_to_customer_button.font_size = 20
        self.navigate_to_customer_button.padding = 10
        self.navigate_to_customer_button.width = DRAWER_WIDTH
        
        self.close_button.theme_text_color = "Custom"
        self.close_button.text_color = 1, 1, 1, 1
        self.close_button.font_style = "H6"
        self.close_button.font_size = 20
        self.close_button.padding = 10
        self.close_button.width = DRAWER_WIDTH
        
    def build(self):
        """
        Builds the main layout of the application.
        
        Returns:
            MDScreen: The main screen of the application.
        """
        screen = MDScreen()
        screen.add_widget(self.drawer)
        
        self.init_buttons_style()
        
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
    