
#!/bin/bash

# Navigate to the project directory
cd /Users/fudongli/travel-website

while true; do
    echo "$(date): Running checks..."
    
    # Activate the virtual environment and run the Python scripts
    source .venv/bin/activate
    python3 check_tasks.py
    python3 check_optimizations.py
    deactivate
    
    # Wait for 30 minutes (1800 seconds) before running again
    echo "$(date): Sleeping for 30 minutes..."
    sleep 1800
done
