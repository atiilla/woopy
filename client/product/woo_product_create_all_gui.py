import inquirer
from inquirer import Checkbox
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


class WooCreateProductAllGui(MDApp):
    """
    WooCreateProductAllGui class aims to provide a GUI for creating a product in WooCommerce
    
    Args:
    MDApp: The MDApp class is the base
    
    Methods:
    build: Build method
    create_product_event: Create product method
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.import_file = MDRaisedButton(text="Import File", on_release=self.import_file_event)
        self.import_products = MDRaisedButton(text="Import Products", on_release=self.import_products_event)
        self.product_info = MDLabel()
    
    
    def build(self):
        """"
        Build method
        """
        main_screen = MDScreen()
        
        # Create app layout with GridLayout
        app_layout = MDGridLayout(cols=1, padding=10)
        app_layout.add_widget(self.import_file)
        app_layout.add_widget(self.import_products)
        app_layout.add_widget(self.product_info)
        main_screen.add_widget(app_layout)
        
        return main_screen

    def import_file_event(self, *args):
        questions = [
            Checkbox('import_file', message="Select the file to import", choices=['products.csv', 'products.json'])
        ]
        answers = inquirer.prompt(questions)
        self.product_info.text = f"File {answers['import_file']} selected"
        
    def import_products_event(self, *args):
        self.product_info.text = "Products imported successfully"
        
        

def main():
    """
    Main function
    """
    # Create the WooCreateProductAllGui object
    WooCreateProductAllGui().run()
    
    
if __name__ == '__main__':
    main()
