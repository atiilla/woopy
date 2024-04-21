import os
import logging
import requests
import typer
from typing_extensions import Annotated
from io import BytesIO


logging.basicConfig(level=logging.INFO)
app = typer.Typer()

# Load .env into a string stream
def load_env(env_path: str = os.path.join(os.getcwd(), '.env')) -> BytesIO:
    stream = BytesIO()
    with open(env_path, 'r', encoding='utf-8') as file:
        stream.write(file.read().encode('utf-8'))
    stream.seek(0)
    return stream


# Function to generate a docker-compose.yml file
@app.command(add_help_option=True, help="Generate a docker-compose.yml file")
def gen_dc(company: Annotated[str, "The name of the company"],
           api_url: Annotated[str, "The URL of the WooPyAPI server"],
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
        f"http://{api_url}:5000/api/docker-compose",
        headers={'Content-Type': 'text/plain',
                 'Accept': 'text/plain',
                 'User-Agent': 'WooPyAPI',
                 'Connection': 'keep-alive'},
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
