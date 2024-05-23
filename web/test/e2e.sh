#!/bin/bash

# The script is a simple curl command that sends a POST request to the server with the site title and URL as the request body. 
# The server responds with a zip file containing the generated site files. The script then unzips the file and checks if the operation was successful.

if [ ! -d ~/Downloads ]; then
    mkdir ~/Downloads
fi

if [ -f ~/Downloads/automated-test.zip ]; then
    rm ~/Downloads/automated-test.zip
fi

if [ -d ~/Downloads/automated-test ]; then
    rm -rf ~/Downloads/automated-test
fi

curl -X 'POST' \
  'http://localhost:5000/' \
  -H 'accept: application/zip' \
  -H 'Content-Type: text/plain' \
  -d 'SITE_TITLE=example
SITE_URL=example.com' \
  -o ~/Downloads/automated-test.zip

if [ $? -ne 0 ]; then
    echo "Failed to download zip file"
    exit 1
fi

if [ ! -f ~/Downloads/automated-test.zip ]; then
    echo "Zip file not found"
    exit 1
fi

unzip -o ~/Downloads/automated-test.zip -d ~/Downloads/automated-test

# Verify that the following files are present in the unzipped directory:
    # 10131  05-20-2024 23:40   docker-compose.yml
    #  3574  05-20-2024 23:40   README.md
    #  4344  05-20-2024 23:40   prerequisites.sh
    # 11449  05-20-2024 23:40   LICENSE
    #   222  05-20-2024 23:40   CONTRIBUTING.md
    #   159  05-20-2024 23:40   CODE_OF_CONDUCT.md
    #   192  05-20-2024 23:40   SECURITY.md
    #   369  05-20-2024 23:40   ROADMAP.md
    #   608  05-20-2024 23:40   .gitignore
    #   165  05-20-2024 23:40   .dockerignore
    #  1710  05-20-2024 23:40   woosh.sh
    #  1342  05-20-2024 23:40   cert.sh
    #   445  05-20-2024 23:40   CHANGELOG.md


downloads_path=~/Downloads/automated-test
files_to_verify=(
    "docker-compose.yml"
    "README.md"
    "prerequisites.sh"
    "LICENSE"
    "CONTRIBUTING.md"
    "CODE_OF_CONDUCT.md"
    "SECURITY.md"
    "ROADMAP.md"
    ".gitignore"
    ".dockerignore"
    "woosh.sh"
    "cert.sh"
    "CHANGELOG.md"
)

counter=0
for file in "${files_to_verify[@]}"; do
    if [ ! -f "$downloads_path/$file" ]; then
        echo "File $file not found in unzipped directory"
    else
        echo "File $file found"
    fi
    counter=$((counter+1))
done

if [ $counter -ne ${#files_to_verify[@]} ]; then
    echo "Some files are missing in the unzipped directory"
    echo "test failed"
    exit 1
else
    echo "All files are present in the unzipped directory"
    echo "test passed"
    rm -rf ~/Downloads/automated-test
    rm ~/Downloads/automated-test.zip
    exit 0
fi

