#!/bin/bash

# remove all __pycache__ directories recursively from the current directory
find . -type d -name "__pycache__" -exec rm -rf {} \;

# remove all .pyc files recursively from the current directory
find . -type f -name "*.pyc" -exec rm -f {} \;

# remove all .pyo files recursively from the current directory
find . -type f -name "*.pyo" -exec rm -f {} \;

# remove all .pyd files recursively from the current directory
find . -type f -name "*.pyd" -exec rm -f {} \;

# remove all .pyo files recursively from the current directory
find . -type f -name "*.pyo" -exec rm -f {} \;

# remove all .pyc files recursively from the current directory
find . -type f -name "*.pyc" -exec rm -f {} \;

# For Windows
# Get-ChildItem -Path . -Include "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force
