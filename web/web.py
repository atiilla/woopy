import logging
import os
import tempfile
from datetime import datetime

from flask import Flask, jsonify, request, send_file
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint

from shared.models import (Database, Admin, Website, Cache, Proxy, Vault,
                           Monitoring, Management, Code, Project, Mail, Networks, Volumes)

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app)


class Health(Resource):
    def get(self):
        return jsonify({
            'status': 'ok',
            'message': 'server is running',
            'version': '1.0.0'
        })


api.add_resource(Health, '/health')


class DockerCompose(Resource):
    def post(self):
        """
        Get the docker-compose.yml file
        ---
        tags:
          - Docker Compose
        responses:
            200:
                description: docker-compose.yml file
                content:
                application/json:
                    schema:
                    type: object
                    properties:
                        status:
                        type: string
                        example: ok
                        message:
                        type: string
                        example: docker-compose.yml file created
                        version:
                        type: string
                        example: 1.0.0
                        file:
                        type: string
                        example: docker-compose.yml file
        """
        # create a dictionary from the .env file
        env = {}
        env_data = request.data.decode().split('\n')
        for line in env_data:
            if line:
                key, value = line.split('=')
                env[key] = value

        database = Database(database_name=env['DATABASE_NAME'], database_user=env['DATABASE_USER'],
                            database_host=env['DATABASE_HOST'])
        email = Mail(env['MAIL_SMTP_HOST'], env['MAIL_SMTP_USER'])
        cache = Cache(env['CACHE_HOST'], env['CACHE_PORT'])
        website = Website(title=env['WEBSITE_TITLE'], host=env['WEBSITE_HOSTNAME'], user=env['WEBSITE_ADMIN_USERNAME'],
                          email=env['WEBSITE_ADMIN_EMAIL'], database=database, mail=email, cache=cache)
        admin = Admin(database, website)
        proxy = Proxy(env['PROXY_TITLE'], env['PROXY_HOSTNAME'], website)
        monitoring = Monitoring(env['HOST_HOSTNAME'], env['HOST_IP'], env['HOST_MAC'], env['HOST_CPU'], env['HOST_RAM'],
                                env['HOST_OS'], env['HOST_KERNEL'], env['HOST_DOCKER'])
        management = Management(website)
        vault = Vault(website)
        code = Code(website)

        networks = Networks()
        volumes = Volumes()

        project = Project(
            project_base_dir=os.path.join(os.getcwd(), website.website_title),
            project_name=website.website_title,
            project_email=website.website_admin_email,
            project_author=website.website_admin_username,
            project_description=f"WooCommerce project for {website.website_title}",
            website=website,
            database=database,
            admin=admin,
            cache=cache,
            proxy=proxy,
            monitoring=monitoring,
            management=management,
            vault=vault,
            code=code,
            networks=networks,
            volumes=volumes
        )

        # Create docker-compose.yaml file in current working directory / website_title / docker-compose.yml
        project_docker_compose_file = os.path.join(project.project_base_dir, 'docker-compose.yml')
        if not os.path.exists(project.project_base_dir):
            os.makedirs(project.project_base_dir)
        with open(project_docker_compose_file, 'w', encoding='utf-8') as f:
            docker_compose_data = project.get_docker_compose_data()
            f.write(docker_compose_data)
            logging.info(
                '################################################################################################')
            logging.info(
                f'Generated docker-compose.yml file for {website.website_title} in {project_docker_compose_file}')
            logging.info(
                '################################################################################################')

            # generate project-report.txt file
            project_report_file = os.path.join(project.project_base_dir, 'project-report.txt')
            with open(project_report_file, 'w', encoding='utf-8') as f:
                project_report_data = project.get_project_report()
                f.write(project_report_data)
                logging.info(
                    '################################################################################################')
                logging.info(
                    f'Generated project-report.txt file for {website.website_title} in {project_report_file}')
                logging.info(
                    '################################################################################################')

        try:
            return send_file(project_docker_compose_file, mimetype='text/yaml', as_attachment=True)
        except Exception as e:
            return str(e)


api.add_resource(DockerCompose, '/docker-compose')


# Create a class that has an endpoint to get the project report.
# website_title is a parameter in the endpoint
# The project report is a text file that contains the following information:

class ProjectReport(Resource):
    # require website_title as a parameter
    @app.route('/project-report/<website_title>')
    def get(self, website_title):
        """
        Get the project report
        ---
        tags:
          - Project Report
        parameters:
            - name: website_title
                in: path
                description: Website title
                required: true
                schema:
                type: string
        responses:
            200:
                description: project report
                content:
                application/json:
                    schema:
                    type: object
                    properties:
                        status:
                        type: string
                        example: ok
                        message:
                        type: string
                        example: project report created
                        version:
                        type: string
                        example: 1.0.0
                        file:
                        type: string
                        example: project report
        """
        # Create project report file in current working directory / website_title / project-report.txt
        # Get project report file from request as website_title / project-report.txt

        project_base_dir = os.path.join(os.getcwd(), website_title)
        project_report_file = os.path.join(project_base_dir, 'project-report.txt')
        with open(project_report_file, 'r', encoding='utf-8') as f:
            project_report_data = f.read()
            logging.info(
                '################################################################################################')
            logging.info(f'Getting project report for {website_title} from {project_report_file}')
            logging.info(
                '################################################################################################')

        try:
            return jsonify(
                status='ok',
                message='project report generated',
                version='1.0.0',
                file=project_report_data
            )
        except Exception as e:
            return str(e)


# Configure Swagger UI
SWAGGER_URL = '/api'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Docker Compose Generator"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.json')
def swagger():
    return f"""
{{
    "openapi": "3.0.0",
    "info": {{
        "title": "Docker Compose Generator",
        "description": "Generate a docker-compose.yml file",
        "version": "1.0.0"
    }},
    "servers": [
        {{
            "url": "http://localhost:5000",
            "description": "Local server"
        }}
    ],
    "tags": [
        {{
            "name": "Docker Compose",
            "description": "Generate a docker-compose.yml file"
        }}
    ],
    "paths": {{
        "/health": {{
            "get": {{
                "tags": [
                    "Health"
                ],
                "summary": "Get the server health",
                "description": "Get the server health",
                "operationId": "getHealth",
                "responses": {{
                    "200": {{
                        "description": "server is running",
                        "content": {{
                            "application/json": {{
                                "schema": {{
                                    "type": "object",
                                    "properties": {{
                                        "status": {{
                                            "type": "string",
                                            "example": "ok"
                                        }},
                                        "message": {{
                                            "type": "string",
                                            "example": "server is running"
                                        }},
                                        "version": {{
                                            "type": "string",
                                            "example": "1.0.0"
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }},
        "/docker-compose": {{
            "post": {{
                "tags": [
                    "Docker Compose"
                ],
                "summary": "Get the docker-compose.yml file",
                "description": "Get the docker-compose.yml file",
                "operationId": "postDockerCompose",
                "requestBody": {{
                    "description": "Environment variables",
                    "content": {{
                        "text/plain": {{
                            "schema": {{
                                "type": "string"
                            }}
                        }}
                    }}
                }},
                "responses": {{
                    "200": {{
                        "description": "docker-compose.yml file",
                        "content": {{
                            "application/json": {{
                                "schema": {{
                                    "type": "object",
                                    "properties": {{
                                        "status": {{
                                            "type": "string",
                                            "example": "ok"
                                        }},
                                        "message": {{
                                            "type": "string",
                                            "example": "docker-compose.yml file created"
                                        }},
                                        "version": {{
                                            "type": "string",
                                            "example": "1.0.0"
                                        }},
                                        "file": {{
                                            "type": "string",
                                            "example": "docker-compose.yml file"
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }},
        "/project-report": {{
            "get": {{
                "tags": [
                    "Project Report"
                ],
                "summary": "Get the project report",
                "description": "Get the project report",
                "operationId": "getProjectReport",
                "parameters": [
                    {{
                        "name": "website_title",
                        "in": "path",
                        "description": "Website title",
                        "required": true,
                        "schema": {{
                            "type": "string"
                        }}
                    }}
                ],
                "responses": {{
                    "200": {{
                        "description": "project report",
                        "content": {{
                            "application/json": {{
                                "schema": {{
                                    "type": "object",
                                    "properties": {{
                                        "status": {{
                                            "type": "string",
                                            "example": "ok"
                                        }},
                                        "message": {{
                                            "type": "string",
                                            "example": "project report created"
                                        }},
                                        "version": {{
                                            "type": "string",
                                            "example": "1.0.0"
                                        }},
                                        "file": {{
                                            "type": "string",
                                            "example": "project report"
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}

"""
