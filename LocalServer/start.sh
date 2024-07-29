#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Extract the parent directory (where the script is located)
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Target directory
TARGET_DIR="/home/ubuntu/"

# Name of the folder to be copied (same as the script directory name)
FOLDER_NAME="$(basename "$SCRIPT_DIR")"

# Perform the copy operation
cp -r "$PARENT_DIR/$FOLDER_NAME" "$TARGET_DIR"

# Check if the copy was successful
if [ $? -eq 0 ]; then
  echo "Successfully copied $FOLDER_NAME to $TARGET_DIR"
else
  echo "Failed to copy $FOLDER_NAME to $TARGET_DIR"
  exit 1
fi
