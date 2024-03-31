from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooUpdateCategoryGui(MDApp):
    """
    WooUpdateCategoryGui class aims to provide a GUI for updating a category in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    update_category_event: Update category method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.category_id = MDTextField(hint_text="Category ID")
        self.category_name = MDTextField(hint_text="Category Name")
        self.category_description = MDTextField(hint_text="Category Description")
        self.category_image = MDTextField(hint_text="Category Image URL")
        
        self.update_category = MDRaisedButton(text="Update Category", on_release=self.update_category_event)
        self.category_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        app_layout.add_widget(self.category_id)
        app_layout.add_widget(self.category_name)
        app_layout.add_widget(self.category_description)
        app_layout.add_widget(self.category_image)
        
        # Set actions_layout to be at the bottom of the page by setting the height_hint to None
        app_layout.add_widget(self.update_category)
        app_layout.add_widget(self.category_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def update_category_event(self, *args):
        """
        Update category method
        """
        category_id = self.category_id.text
        category_name = self.category_name.text
        category_description = self.category_description.text
        category_image = self.category_image.text
        self.category_info.text = f"Category ID: {category_id}\nCategory Name: {category_name}\nCategory Description: {category_description}\nCategory Image: {category_image}"
        
        
def main():
    """
    Main function
    """
    WooUpdateCategoryGui().run()
    
if __name__ == '__main__':
    main()


    

