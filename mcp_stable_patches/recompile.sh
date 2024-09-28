#!/bin/bash

# URL to the JSON file containing libraries
JSON_URL="https://piston-meta.mojang.com/v1/packages/856d9bec08b0d567de39f46efaf4b76066b53059/1.8.9.json"

# Directory to store downloaded libraries
LIB_DIR="./lib"

# Create lib directory if it doesn't exist
mkdir -p "$LIB_DIR"

# Download the JSON file and extract the URLs of libraries using jq
echo "Downloading JSON metadata..."
curl -s "$JSON_URL" -o metadata.json

# Extract URLs of all libraries using jq (ensure jq is installed: apt install jq)
LIB_URLS=$(jq -r '.libraries[].downloads.artifact.url' metadata.json)

# Download each library
echo "Downloading libraries..."
for url in $LIB_URLS; do
    echo "Downloading $url..."
    curl -O --create-dirs -L "$url" -o "$LIB_DIR/$(basename $url)"
done

# Clean up the JSON metadata file
rm metadata.json

echo "Libraries downloaded to $LIB_DIR"
