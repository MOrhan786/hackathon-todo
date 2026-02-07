"""
Check enum values in database vs model definition
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

print("=" * 80)
print("CHECKING ENUM VALUES")
print("=" * 80)

# Check if there's an enum type in the database
cursor.execute("""
    SELECT n.nspname as schema, t.typname as typename, e.enumlabel as enumvalue
    FROM pg_type t
    JOIN pg_enum e ON t.oid = e.enumtypid
    JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
    WHERE t.typname = 'taskstatus'
    ORDER BY e.enumsortorder;
""")

enum_values = cursor.fetchall()
if enum_values:
    print("\nDatabase ENUM type 'taskstatus' values:")
    for val in enum_values:
        print(f"  - {val[2]}")
else:
    print("\nNo ENUM type 'taskstatus' found in database")

# Check actual status values in tasks table
cursor.execute("""
    SELECT DISTINCT status, pg_typeof(status) as type
    FROM tasks;
""")

status_values = cursor.fetchall()
print("\nActual status values in tasks table:")
for val in status_values:
    print(f"  - {val[0]!r} (type: {val[1]})")

# Check the column type
cursor.execute("""
    SELECT column_name, data_type, udt_name
    FROM information_schema.columns
    WHERE table_name = 'tasks' AND column_name = 'status';
""")

col_info = cursor.fetchone()
print(f"\nStatus column info:")
print(f"  Data type: {col_info[1]}")
print(f"  UDT name: {col_info[2]}")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print("Model definition expects:")
print("  TaskStatus.PENDING = 'pending'")
print("  TaskStatus.IN_PROGRESS = 'in_progress'")
print("  TaskStatus.COMPLETED = 'completed'")
print("=" * 80)
