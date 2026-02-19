
import os
import json
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta

def get_db_connection():
    return psycopg2.connect(
        dbname="travel_website",
        user="fudongli",
        password="",
        host="localhost",
        port="5432",
        options="-c search_path=travel"
    )

def verify_completed_tasks():
    conn = get_db_connection()
    cur = conn.cursor()

    # Get tasks that were marked as fixed in the last 30 minutes
    thirty_minutes_ago = datetime.now() - timedelta(minutes=30)
    cur.execute(
        sql.SQL("SELECT id, idea, fixed_at FROM travel_development_ideas WHERE is_fixed = true AND fixed_at >= %s"),
        (thirty_minutes_ago,)
    )
    completed_tasks = cur.fetchall()

    for task_id, idea, fixed_at in completed_tasks:
        # Check if the task is related to image optimization
        if "Optimize image" in idea:
            # Extract image path from the idea
            parts = idea.split(" for city ")
            if len(parts) == 2:
                image_path = parts[0].replace("Optimize image ", "").strip()
                city_name = parts[1].strip()
                
                # Check if the optimized image exists
                if not os.path.exists(image_path):
                    # If the optimized image doesn't exist, create a new task
                    new_task_description = f"Image optimization failed for {image_path} in {city_name}"
                    cur.execute(
                        sql.SQL("INSERT INTO travel_development_ideas (idea, is_fixed) VALUES (%s, %s)"),
                        (new_task_description, False)
                    )
                    conn.commit()
                    print(f"Created new task for failed optimization: {new_task_description}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    verify_completed_tasks()
