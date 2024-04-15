#!/bin/bash

# Read all the arguments passed to the script from .env file
while IFS= read -r line; do
    export $line
done < .env

# Check if all the required environment variables are set
if [[ -z "${project_name}" || -z "${app_name}" || -z "${bundle}" || -z "${version}" || -z "${url}" || -z "${license}" || -z "${author}" || -z "${author_email}" || -z "${formal_name}" || -z "${description}" || -z "${long_description}" ]]; then
    echo "One or more required environment variables are not set. Aborting."
    exit 1
fi

echo "Creating project..."

if [[ -d "${project_name}" ]]; then
    echo "Directory already exists. Aborting. Please remove the directory and try again."
    exit 1
fi

briefcase new -Q "project_name=${project_name}" \
    -Q "app_name=${app_name}" \
    -Q "bundle=${bundle}" \
    -Q "version=${version}" \
    -Q "url=${url}" \
    -Q "license=${license}" \
    -Q "author=${author}" \
    -Q "author_email=${author_email}" \
    -Q "formal_name=${formal_name}" \
    -Q "description=${description}" \
    -Q "long_description=${long_description}" \
    --no-input


echo "Project created successfully."

pushd "${project_name}" || exit

echo "Updating app.py code to include webview..."

app_py_path="src/${app_name}/app.py"

app_code=$(cat <<EOF
"""
Webshop Native Application
"""
import toga
from toga.style import Pack


class {{app_name}}(toga.App):
    """The main application class for {{app_name}}.

    This class represents the Toga application for {{app_name}}. It inherits from
    the toga.App class and provides the necessary methods for starting up and running the application.

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
        load_webview(self.main_window, "{{app_url}}")
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
    return {{app_name}}()

EOF
)

# Replace {{app_name}} with the actual app name using awk
app_code=$(echo "${app_code}" | awk -v app_name="${app_name}" '{gsub("{{app_name}}", app_name); print}')
# Replace {{app_url}} with the actual app URL using awk
app_code=$(echo "${app_code}" | awk -v app_url="${url}" '{gsub("{{app_url}}", app_url); print}')

echo "${app_code}" > "${app_py_path}"

popd || exit

echo "app.py updated successfully."
