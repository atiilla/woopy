import os

import kivy
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from shared.utils import load_env

kivy.require('2.0.0')


class GUI(App):
    def __init__(self, **kwargs):
        super().__init__()
        self.save_output_button = None
        self.company_name = None
        self.company_path = None
        self.env_path = None
        self.compose_path = None
        self.create_new_env_file_button = None
        self.checkbox_layout = None
        self.actions_layout = None
        self.data_layout = None
        self.create_buttons_layout = None
        self.create_new_project_button = None
        self.reset_button = None
        self.generate_docker_compose_button = None
        self.console_output = None
        self.env_file_chooser = None
        self.company_name_input = None
        self.company_path_label = None
        self.force_overwrite_checkbox = None
        self.force_overwrite_label = None

    def build(self):
        # Create layout
        layout = BoxLayout(orientation='horizontal')
        layout.padding = 10
        layout.spacing = 10
        layout.size_hint = (1, 1)

        # Create a split layout for the file chooser and the company name input
        self.data_layout = BoxLayout(orientation='vertical')
        self.data_layout.size_hint = (0.35, 1)
        layout.add_widget(self.data_layout)

        # Create FileChooser
        self.env_file_chooser = FileChooserListView(path='/', filters=['*.env'])
        self.env_file_chooser.size_hint = (1, 0.9)
        # add an event listener to the file chooser
        self.env_file_chooser.bind(selection=self.print_env_values_to_console_output)

        # Create a label for the company path
        self.company_path_label = Label()
        self.company_path_label.text = 'COMPANY NAME IS REQUIRED!'
        self.company_path_label.color = (1, 0, 0, 1)
        self.company_path_label.size_hint = (1, 0.02)
        self.company_path_label.padding = (0, 10)
        self.company_path_label.halign = 'center'
        self.company_path_label.valign = 'middle'
        self.company_path_label.font_size = 14
        self.company_path_label.color = (0.5, 0.5, 0.5, 1)

        # Create company name input
        self.company_name_input = TextInput(multiline=False)
        self.company_name_input.hint_text = 'Company name'
        self.company_name_input.size_hint = (1, 0.08)
        self.company_name_input.font_size = 14
        self.company_name_input.halign = 'left'
        self.company_name_input.valign = 'top'
        self.company_name_input.bind(text=self.on_company_name_change)

        # Create a split layout for button and console output
        self.actions_layout = BoxLayout(orientation='vertical')
        self.actions_layout.size_hint = (0.65, 1)
        layout.add_widget(self.actions_layout)

        # Create Submit button
        self.generate_docker_compose_button = Button(text='Generate')
        self.generate_docker_compose_button.bind(on_release=self.generate_docker_file)
        self.generate_docker_compose_button.background_color = (0.1, 0.5, 0.1, 1)
        self.generate_docker_compose_button.color = (1, 1, 1, 1)
        self.generate_docker_compose_button.size_hint = (1, 0.1)
        self.generate_docker_compose_button.disabled = True

        # Create Reset Button
        self.reset_button = Button(text='Reset')
        self.reset_button.bind(on_release=self.reset)
        self.reset_button.background_color = (0.5, 0.1, 0.9, 1)
        self.reset_button.color = (1, 1, 1, 1)
        self.reset_button.size_hint = (1, 0.05)

        # Create a layout for checkbox and label
        self.checkbox_layout = BoxLayout(orientation='horizontal')
        self.checkbox_layout.size_hint = (1, 0.05)

        # Create a label for the force overwrite checkbox
        self.force_overwrite_label = Label(text='Force overwrite')
        self.force_overwrite_label.size_hint = (0.5, 1)

        # Create a checkbox for force overwrite
        self.force_overwrite_checkbox = CheckBox()
        self.force_overwrite_checkbox.bind(active=self.on_force_overwrite_change)
        self.force_overwrite_checkbox.active = False
        self.force_overwrite_checkbox.size_hint = (0.5, 1)

        # Create console output
        self.console_output = TextInput(readonly=True)
        # Make the console output scrollable and dark mode (dark gray background, snow-white text)
        self.console_output.background_color = (0.1, 0.1, 0.1, 1)
        self.console_output.foreground_color = (1, 1, 1, 0.8)
        self.console_output.scroll_x = 0
        self.console_output.scroll_y = 0
        self.console_output.size_hint = (1, 0.75)
        self.console_output.font_size = 14
        self.console_output.halign = 'left'
        self.console_output.valign = 'top'
        self.console_output.multiline = True
        self.console_output.readonly = True

        # add save output button below console output
        self.save_output_button = Button(text='Save output')
        self.save_output_button.size_hint = (1, 0.05)
        self.save_output_button.bind(on_release=lambda x: open(os.path.join(os.getcwd(), 'woopy.log'), 'w+').write(self.console_output.text) if self.console_output.text else None)

        # Add create a horizontal layout for new buttons: create folder, create docker-compose.yml, create .env
        self.create_buttons_layout = BoxLayout(orientation='horizontal')
        self.create_buttons_layout.size_hint = (1, 0.05)

        self.create_new_project_button = Button(text='New folder')
        self.create_new_project_button.size_hint = (0.33, 1)
        folder_to_create = self.company_name_input.text if self.company_name_input.text else 'New folder'
        self.create_new_project_button.bind(on_release=lambda x: os.mkdir(os.path.join(os.getcwd(), folder_to_create)))
        self.create_new_env_file_button = Button(text='New file')
        self.create_new_env_file_button.size_hint = (0.33, 1)
        file_to_create = f"{self.company_name_input.text}.env" if self.company_name_input.text else '.env'
        self.create_new_env_file_button.bind(on_release=lambda x: open(os.path.join(os.getcwd(), file_to_create), 'w+'))
        self.create_buttons_layout.add_widget(self.create_new_project_button)
        self.create_buttons_layout.add_widget(self.create_new_env_file_button)

        self.data_layout.add_widget(self.create_buttons_layout)
        self.data_layout.add_widget(self.env_file_chooser)
        self.data_layout.add_widget(self.company_path_label)
        self.data_layout.add_widget(self.company_name_input)

        self.actions_layout.add_widget(self.generate_docker_compose_button)
        self.actions_layout.add_widget(self.reset_button)
        self.actions_layout.add_widget(self.checkbox_layout)
        self.checkbox_layout.add_widget(self.force_overwrite_label)
        self.checkbox_layout.add_widget(self.force_overwrite_checkbox)
        self.actions_layout.add_widget(self.console_output)
        self.actions_layout.add_widget(self.save_output_button)

        # Make sure that enter key press is not ignored by the text input
        self.company_name_input.bind(on_text_validate=self.generate_docker_file)

        # Add on start, stop and pause event listeners
        self.bind(on_start=self.on_start, on_stop=self.on_stop, on_pause=self.on_pause)

        return layout

    def on_company_name_change(self, instance, value):
        if value:
            self.company_name = value
            # Set red color border if company name is not empty
            self.company_path = os.path.join(os.getcwd(), self.company_name)
            self.compose_path = os.path.join(self.company_path, 'docker-compose.yml')
            self.company_path_label.text = self.company_path
            self.company_path_label.color = (0.5, 0.5, 0.5, 1)
            self.generate_docker_compose_button.disabled = False

        else:
            self.company_name = None
            self.compose_path = None
            self.company_path_label.text = 'COMPANY NAME IS REQUIRED!'
            self.company_path_label.color = (1, 0, 0, 1)
            self.generate_docker_compose_button.disabled = True

    def generate_docker_file(self, instance):
        # Get selected files
        selected_files = self.env_file_chooser.selection

        # Make sure that only one file is selected
        if len(selected_files) > 1:
            self.console_output.foreground_color = (1, 0, 0, 1)
            self.console_output.text += 'WARNING: Only one .env file can be selected!\n'
            self.print_split(instance)
            self.console_output.foreground_color = (1, 1, 1, 1)

        elif len(selected_files) == 0:
            self.console_output.foreground_color = (1, 0, 0, 1)
            self.console_output.text += 'ERROR: No .env file selected!\n'
            self.print_split(instance)
            self.console_output.foreground_color = (1, 1, 1, 1)

        else:
            self.env_path = self.env_file_chooser.selection[0]

            self.console_output.foreground_color = (1, 1, 1, 1)
            self.console_output.text += f"Generating docker-compose.yml file for {self.company_name_input.text} in {self.compose_path}\n"
            self.console_output.text += "Company path: " + self.company_path + "\n"
            self.console_output.text += "Env path: " + self.env_path + "\n"
            self.console_output.text += "Compose path: " + self.compose_path + "\n"

            if not os.path.exists(self.company_path):
                self.console_output.text += f"Directory {self.company_path} does not exist, will be created.\n"
                os.mkdir(self.company_path)

            response = requests.post(
                'http://localhost:5000/docker-compose',
                headers={'Content-Type': 'text/plain',
                         'Accept': 'text/plain',
                         'User-Agent': 'WooPyAPI',
                         'Connection': 'keep-alive',
                         'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7;be=q=0.6,pt;q=0.5,de;q=0.4,ja;q=0.3,ru;q=0.2,ar;q=0.1'},
                data=load_env(self.env_path).read().decode('utf-8'))

            if response.status_code == 200:
                if self.force_overwrite_checkbox.active:
                    os.remove(self.compose_path)

                with open(self.compose_path, 'wb') as output_file:
                    output_file.write(response.content)
                    self.console_output.text += f"docker-compose.yml file successfully created in {self.compose_path}"
                    self.open_directory_in_explorer(instance)
            else:
                self.console_output.text += f"Error while creating the docker-compose.yml file in {self.compose_path}. Error: {response.text}"

            self.print_split(instance)
            self.console_output.foreground_color = (1, 1, 1, 1)

    def reset(self, instance):
        self.console_output.text += 'Resetting GUI\n'
        self.company_name_input.text = ''
        self.force_overwrite_checkbox.active = False
        self.env_file_chooser.path = os.getcwd()
        self.company_path_label.text = "COMPANY NAME IS REQUIRED!"
        self.company_path_label.color = (1, 0, 0, 1)
        self.console_output.text += 'GUI reset is complete\n'
        self.print_split(instance)

    def restore(self, instance):
        self.console_output.text += 'Restoring .env file\n'
        if self.company_name:
            self.company_name_input.text = self.company_name
        if self.env_path:
            self.env_file_chooser.path = self.env_path
        if self.company_path:
            self.company_path_label.text = 'Project path: ' + self.company_path
        self.console_output.text += 'Restoring .env file is complete\n'
        self.print_split(instance)

    def open_directory_in_explorer(self, instance):
        self.console_output.text += f"Opening {os.path.join(os.getcwd(), self.company_path)} in explorer\n"
        if os.name == 'nt':
            os.system(f"explorer {os.path.join(os.getcwd(), self.company_path)}")
        elif os.name == 'posix':
            os.system(f"open {os.path.join(os.getcwd(), self.company_path)}")
        else:
            self.console_output.text += f"Cannot open {os.path.join(os.getcwd(), self.company_path)} in explorer. Unknown OS: {os.name}\n"
        self.print_split(instance)

    def print_env_values_to_console_output(self, instance, value):
        self.console_output.text += 'Selected .env file: ' + str(value) + '\n'
        env_content = load_env(value[0]).read().decode('utf-8')
        self.console_output.text += f"{env_content}\n"
        self.print_split(instance)

    def on_force_overwrite_change(self, instance, value):
        if value:
            self.console_output.text += 'Force overwrite is enabled\n'
        else:
            self.console_output.text += 'Force overwrite is disabled\n'
        self.print_split(instance)

    def print_split(self, instance):
        split_buffer = '--------------------------------------------------------------------------------------------------------------------------'
        self.console_output.text += split_buffer + '\n'

    def on_start(self, *args):
        self.console_output.text += 'GUI started\n'
        self.print_split(None)

    def on_stop(self, *args):
        self.console_output.text += 'GUI stopped\n'
        self.print_split(None)

    def on_pause(self, *args):
        self.console_output.text += 'GUI paused\n'
        self.print_split(None)

