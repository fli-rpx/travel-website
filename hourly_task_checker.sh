#!/bin/bash

# Navigate to the project directory
cd /Users/fudongli/travel-website

while true; do
    echo "$(date): Running task check..."
    
    # Activate the virtual environment and run the Python script
    source .venv/bin/activate
    python3 check_tasks.py
    deactivate
    
    # Wait for 1 hour (3600 seconds) before running again
    echo "$(date): Sleeping for 1 hour..."
    sleep 3600
done