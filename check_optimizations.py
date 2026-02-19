
import os
import json
import psycopg2
from psycopg2 import sql

def get_db_connection():
    return psycopg2.connect(
        dbname="travel_website",
        user="fudongli",
        password="",
        host="localhost",
        port="5432",
        options="-c search_path=travel"
    )

def check_and_insert_optimization_tasks():
    conn = get_db_connection()
    cur = conn.cursor()

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r') as f:
                try:
                    city_data = json.load(f)
                    if 'gallery' in city_data:
                        for image in city_data['gallery']:
                            if '_optimized.jpg' not in image:
                                task_description = f"Optimize image {image} for city {city_data.get('name', 'Unknown')}"
                                cur.execute(
                                    sql.SQL("INSERT INTO travel_development_ideas (idea, is_fixed) VALUES (%s, %s)"),
                                    (task_description, False)
                                )
                                conn.commit()
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from {filename}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    check_and_insert_optimization_tasks()
