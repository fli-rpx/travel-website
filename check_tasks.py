
import psycopg2
import schedule
import time
from datetime import datetime

def check_for_tasks():
    """
    Connects to the travel_website database and checks for tasks
    in the travel.travel_development_ideas table where is_fixed is false.
    """
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            dbname="travel_website",
            user="fudongli",
            host="localhost"
        )
        cur = conn.cursor()

        # Execute the query to find tasks that are not fixed
        cur.execute("SELECT id, idea, created_at FROM travel.travel_development_ideas WHERE is_fixed = false ORDER BY id;")
        
        # Fetch all the results
        tasks = cur.fetchall()

        # Get the current time for logging
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if there are any tasks
        if tasks:
            print(f"[{current_time}] Found {len(tasks)} pending tasks:")
            for task in tasks:
                print(f"  - Task ID: {task[0]}, Idea: {task[1]}, Created At: {task[2]}")
        else:
            print(f"[{current_time}] No pending tasks found.")

    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()

def job():
    """
    This function is the job that will be scheduled to run every hour.
    """
    print("--- Running hourly task check ---")
    check_for_tasks()

# Schedule the job to run every hour
schedule.every().hour.do(job)

if __name__ == "__main__":
    print("Starting the task scheduler...")
    # Run the job once immediately
    job()
    
    # Keep the script running to execute the scheduled job
    while True:
        schedule.run_pending()
        time.sleep(1)
