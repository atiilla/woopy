from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooGetCategoriesGui(MDApp):
    """
    WooGetCategoriesGui class aims to provide a GUI for getting all categories in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    get_categories_event: Get categories method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.get_categories = MDRaisedButton(text="Get Categories", on_release=self.get_categories_event)
        self.category_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.get_categories)
        app_layout.add_widget(self.category_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def get_categories_event(self, *args):
        """
        Get categories method
        """
        self.category_info.text = "Getting all categories"
        
        

def main():
    """
    Main function
    """
    WooGetCategoriesGui().run()
    
if __name__ == '__main__':
    main()


    

