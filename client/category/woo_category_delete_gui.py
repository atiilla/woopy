from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooDeleteCategoryGui(MDApp):
    """
    WooDeleteCategoryGui class aims to provide a GUI for deleting a category in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    delete_category_event: Delete category method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.category_id = MDTextField(hint_text="Category ID")
        
        self.delete_category = MDRaisedButton(text="Delete Category", on_release=self.delete_category_event)
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
        app_layout.add_widget(self.delete_category)
        app_layout.add_widget(self.category_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def delete_category_event(self, *args):
        """
        Delete category method
        """
        category_id = self.category_id.text
        self.category_info.text = f"Category ID: {category_id}"
        
        

def main():
    """
    Main function
    """
    WooDeleteCategoryGui().run()
    
if __name__ == '__main__':
    main()


    

