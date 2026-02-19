
#!/bin/bash

# Navigate to the project directory
cd /Users/fudongli/travel-website

while true; do
    echo "$(date): Starting automated workflow..."
    
    # Git pull to overwrite existing files if needed
    echo "$(date): Pulling latest changes from git..."
    git fetch origin main
    git reset --hard origin/main
    
    # Activate the virtual environment and run the Python scripts
    source .venv/bin/activate
    
    echo "$(date): Running task check..."
    python3 check_tasks.py
    
    echo "$(date): Checking for optimization needs..."
    python3 check_optimizations.py
    
    echo "$(date): Verifying completed tasks from last 30 minutes..."
    python3 verify_completed_tasks.py
    
    deactivate
    
    # Wait for 30 minutes (1800 seconds) before running again
    echo "$(date): Sleeping for 30 minutes..."
    sleep 1800
done
