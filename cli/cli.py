import os
import requests
import typer
from typing_extensions import Annotated

from shared.utils import load_env
from web.web import api as server

app = typer.Typer()


# Function to start the WooPyAPI server
@app.command(add_help_option=True, help="Start the WooPyAPI server")
def start_api():
    server.run(debug=True)


# Function to stop the WooPyAPI server
@app.command(add_help_option=True, help="Stop the WooPyAPI server")
def stop_api():
    # Implement the logic to stop the server
    server.stop()


# Function to restart the WooPyAPI server
@app.command(add_help_option=True, help="Restart the WooPyAPI server")
def restart_api():
    # Implement the logic to restart the server
    server.restart()


# Function to generate a docker-compose.yml file
@app.command(add_help_option=True, help="Generate a docker-compose.yml file")
def gen_dc(company: Annotated[str, "The name of the company"],
           force: Annotated[bool, "Overwrite the docker-compose.yml file if it already exists"] = False):

    company_path = os.path.join(os.getcwd(), company)
    env_path = os.path.join(company_path, '.env')
    compose_path = os.path.join(company_path, 'docker-compose.yml')

    print("################################################################################################")
    print(f"Generating docker-compose.yml file for {company} in {compose_path}")
    print("Company path: " + company_path)
    print("Env path: " + env_path)
    print("Compose path: " + compose_path)
    print("################################################################################################")

    if not os.path.exists(env_path):
        typer.echo(f"File {env_path} does not exist.")
        typer.echo("Please specify the path to the .env file using the --env-path option.")
        return

    if os.path.exists(compose_path) and not force:
        typer.echo(f"File {compose_path} already exists. Use --force to overwrite it.")
        return

    response = requests.post(
        'http://localhost:5000/docker-compose',
        headers={'Content-Type': 'text/plain',
                 'Accept': 'text/plain',
                 'User-Agent': 'WooPyAPI',
                 'Connection': 'keep-alive',
                 'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7;be=q=0.6,pt;q=0.5,de;q=0.4,ja;q=0.3,ru;q=0.2,ar;q=0.1'},
        data=load_env(env_path).read().decode('utf-8'))

    if response.status_code == 200 and response.text:
        if os.path.exists(compose_path) and force:
            os.remove(compose_path)

        with open(compose_path, 'wb') as output_file:
            output_file.write(response.content)
            typer.echo(f"docker-compose.yml file successfully created in {compose_path}")
    else:
        typer.echo(
            "Error while creating the docker-compose.yml file. Make sure the WooPyAPI server is running, and that the .env file is correctly configured.")
