FROM python:3.7-alpine

# Copy the dependencies file to the working directory
COPY requirements.txt /app

# Copy .env file to the working directory
COPY test/.env /app

# Copy shared, native, cli, and web files to the container
COPY bridge /app/bridge
COPY cli /app/cli
COPY client /app/client
COPY native /app/native
COPY shared /app/shared
COPY web /app/web


# Install the required dependencies
RUN pip3 install -r /app/requirements.txt

ENV FLASK_HOST=https://localhost:5000

# Set the working directory
WORKDIR /app

# Set the command to run the CLI with --help
CMD [ "python3", "-m", "cli", "--help" ]



