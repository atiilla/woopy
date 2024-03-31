from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooGetCategoryGui(MDApp):
    """
    WooGetCategoryGui class aims to provide a GUI for getting a category in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    get_category_event: Get category method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.category_id = MDTextField(hint_text="Category ID")
        
        self.get_category = MDRaisedButton(text="Get Category", on_release=self.get_category_event)
        self.category_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        app_layout.add_widget(self.category_id)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.get_category)
        app_layout.add_widget(self.category_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def get_category_event(self, *args):
        """
        Get category method
        """
        category_id = self.category_id.text
        self.category_info.text = f"Category ID: {category_id}"


def main():
    """
    Main function
    """
    WooGetCategoryGui().run()
    
if __name__ == '__main__':
    main()


    

