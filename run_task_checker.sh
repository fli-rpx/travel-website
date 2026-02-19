#!/bin/bash

# Navigate to the project directory
cd /Users/fudongli/travel-website

# Activate the virtual environment
source .venv/bin/activate

# Run the Python script
python3 check_tasks.py

# Deactivate the virtual environment (optional, as the script will exit anyway)
deactivate