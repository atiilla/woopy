#!/bin/bash

# The script is a simple curl command that sends a POST request to the server with the site title and URL as the request body. 
# The server responds with a zip file containing the generated site files. The script then unzips the file and checks if the operation was successful.

curl -X 'POST' \
  'http://localhost:5000/' \
  -H 'accept: application/zip' \
  -H 'Content-Type: text/plain' \
  -d 'SITE_TITLE=example
SITE_URL=example.com' \
  -o ~/Downloads/automated-test.zip

unzip -l ~/Downloads/automated-test.zip

# Verify the output
if [ $? -eq 0 ]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed"
  exit 1
fi



