"""
WooCommerce Custom Website Website Full-screen Webview Cross Platform App
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class WooPyGui(toga.App):
    """A Toga application for displaying a full screen webview.

    This application creates a main window with a full screen webview
    that displays a given website URL. The webview is styled to remove
    all margins and paddings, and the title bar is also removed.

    Attributes:
        main_window (toga.MainWindow): The main window of the application.
    """

    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()
        
        # Create a full screen webview to display given website URL
        webview = toga.WebView(style=Pack(flex=1))
        # Remove title bar from the webview, make it look like a native app
        webview.window.user_insets = (0, 0, 0, 0)
        # Remove all margins and paddings, and set the webview to full screen
        webview.style.update({
            'margin': 0,
            'padding': 0,
            'flex': 1
        })
        # Read website URL from .env file
        webview.url = "https://h2oheating.xyz"
        # Remove title bar from the webview
        webview.window.user_insets = (0, 0, 0, 0)
        # Add the webview to the main box
        main_box.add(webview)
        # Set main box as the content of the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        # Set the main window to full screen and remove the title bar
        self.main_window.app.window.user_insets = (0, 0, 0, 0)
        self.main_window.app.window.full_screen = True
        self.main_window.app.window.show_toolbar = False
        self.main_window.app.window.show_status = False
        self.main_window.app.window.show_scrollbars = False
        self.main_window.app.window.show_resize_corner = False
        self.main_window.app.window.show_full_screen_button = False
        # Show the main window
        self.main_window.show()
        

def main():
    return WooPyGui()

