"""
Debug script to check database schema and data types
"""
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

# Get connection string from .env
db_url = os.getenv("DATABASE_URL")

# Parse the connection string
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

print("=" * 80)
print("1. TASKS TABLE SCHEMA")
print("=" * 80)

# Get table schema
cursor.execute("""
    SELECT
        column_name,
        data_type,
        character_maximum_length,
        is_nullable,
        column_default
    FROM information_schema.columns
    WHERE table_name = 'tasks'
    ORDER BY ordinal_position;
""")

schema = cursor.fetchall()
for col in schema:
    print(f"Column: {col[0]:<20} Type: {col[1]:<20} Nullable: {col[3]:<5} Default: {col[4]}")

print("\n" + "=" * 80)
print("2. USERS TABLE SCHEMA")
print("=" * 80)

# Get users table schema
cursor.execute("""
    SELECT
        column_name,
        data_type,
        character_maximum_length,
        is_nullable,
        column_default
    FROM information_schema.columns
    WHERE table_name = 'user'
    ORDER BY ordinal_position;
""")

user_schema = cursor.fetchall()
for col in user_schema:
    print(f"Column: {col[0]:<20} Type: {col[1]:<20} Nullable: {col[3]:<5} Default: {col[4]}")

print("\n" + "=" * 80)
print("3. CHECK IF TASKS EXIST")
print("=" * 80)

# Count tasks
cursor.execute("SELECT COUNT(*) FROM tasks;")
count = cursor.fetchone()[0]
print(f"Total tasks in database: {count}")

if count > 0:
    print("\n" + "=" * 80)
    print("4. SAMPLE TASK DATA (First 3 tasks)")
    print("=" * 80)

    # Get sample tasks with their data types
    cursor.execute("""
        SELECT
            id,
            user_id,
            title,
            status,
            pg_typeof(id) as id_type,
            pg_typeof(user_id) as user_id_type
        FROM tasks
        LIMIT 3;
    """)

    tasks = cursor.fetchall()
    for task in tasks:
        print(f"\nTask ID: {task[0]} (Type: {task[4]})")
        print(f"  User ID: {task[1]} (Type: {task[5]})")
        print(f"  Title: {task[2]}")
        print(f"  Status: {task[3]}")

    print("\n" + "=" * 80)
    print("5. CHECK FOR TYPE INCONSISTENCIES")
    print("=" * 80)

    # Check if user_id has consistent type
    cursor.execute("""
        SELECT DISTINCT pg_typeof(user_id) as user_id_type
        FROM tasks;
    """)

    types = cursor.fetchall()
    print(f"User ID types found in tasks table: {[t[0] for t in types]}")

print("\n" + "=" * 80)
print("6. CHECK USERS TABLE")
print("=" * 80)

cursor.execute("SELECT COUNT(*) FROM \"user\";")
user_count = cursor.fetchone()[0]
print(f"Total users in database: {user_count}")

if user_count > 0:
    cursor.execute("""
        SELECT
            id,
            email,
            pg_typeof(id) as id_type
        FROM "user"
        LIMIT 3;
    """)

    users = cursor.fetchall()
    for user in users:
        print(f"\nUser ID: {user[0]} (Type: {user[2]})")
        print(f"  Email: {user[1]}")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
