from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooCreateCategoryGui(MDApp):
    """
    WooCreateCategoryGui class aims to provide a GUI for creating a category in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    create_category_event: Create category method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.category_name = MDTextField(hint_text="Category Name")
        self.category_description = MDTextField(hint_text="Category Description")
        self.category_image = MDTextField(hint_text="Category Image URL")
        
        self.add_category = MDRaisedButton(text="Add Category", on_release=self.add_category_event)
        self.category_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        app_layout.add_widget(self.category_name)
        app_layout.add_widget(self.category_description)
        app_layout.add_widget(self.category_image)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.add_category)
        app_layout.add_widget(self.category_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def add_category_event(self, *args):
        """
        Add category method
        """
        category_name = self.category_name.text
        category_description = self.category_description.text
        category_image = self.category_image.text
        self.category_info.text = f"Category Name: {category_name}\nCategory Description: {category_description}\nCategory Image: {category_image}"
        

def main():
    """
    Main function
    """
    app = WooCreateCategoryGui()
    app.run()
    
if __name__ == '__main__':
    main()


    

