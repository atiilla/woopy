"""
My first application
"""
import toga
from toga.style import Pack


class woostore(toga.App):
    """The main application class for Woostore.

    This class represents the Toga application for Woostore. It inherits from
    the `toga.App` class and provides the necessary methods for starting up
    and running the application.

    Attributes:
        main_window (toga.MainWindow): The main window of the application.

    """

    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_window = toga.MainWindow()
        load_webview(self.main_window, "https://www.eticaret.com/")
        self.main_window.show()


def load_webview(widget, url):
    """
    Load a webview into the given widget with the specified URL.

    Args:
        widget (toga.Widget): The widget to load the webview into.
        url (str): The URL to load in the webview.
    """
    webview = toga.WebView(style=Pack(flex=1))
    webview.url = url
    widget.content = webview

def main():
    """
    This is the main function of the woostore application.
    It returns the result of the woostore function.
    """
    return woostore()