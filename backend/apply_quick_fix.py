#!/usr/bin/env python3
"""
Apply quick fix to normalize enum data and remove unused ENUM types.
This will fix the immediate 500 error.
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    db_url = os.getenv("DATABASE_URL")

    print("=" * 80)
    print("APPLYING QUICK FIX FOR ENUM DATA")
    print("=" * 80)

    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    try:
        # Check current state
        print("\n1. Current state:")
        cursor.execute("SELECT DISTINCT status FROM tasks ORDER BY status;")
        statuses = [row[0] for row in cursor.fetchall()]
        print(f"   Status values: {statuses}")

        cursor.execute("SELECT DISTINCT priority FROM tasks ORDER BY priority;")
        priorities = [row[0] for row in cursor.fetchall()]
        print(f"   Priority values: {priorities}")

        # Normalize status values
        print("\n2. Normalizing status values to lowercase...")
        cursor.execute("""
            UPDATE tasks
            SET status = LOWER(status)
            WHERE status != LOWER(status);
        """)
        print(f"   Updated {cursor.rowcount} rows")

        # Fix 'in_progress' format
        print("\n3. Fixing 'in_progress' format...")
        cursor.execute("""
            UPDATE tasks
            SET status = 'in_progress'
            WHERE status IN ('IN_PROGRESS', 'In_Progress', 'in-progress');
        """)
        print(f"   Updated {cursor.rowcount} rows")

        # Normalize priority values
        print("\n4. Normalizing priority values to lowercase...")
        cursor.execute("""
            UPDATE tasks
            SET priority = LOWER(priority)
            WHERE priority != LOWER(priority);
        """)
        print(f"   Updated {cursor.rowcount} rows")

        # Drop unused ENUM types
        print("\n5. Dropping unused ENUM types...")
        try:
            cursor.execute("DROP TYPE IF EXISTS taskstatus CASCADE;")
            print("   Dropped taskstatus ENUM")
        except Exception as e:
            print(f"   Could not drop taskstatus: {e}")

        try:
            cursor.execute("DROP TYPE IF EXISTS taskpriority CASCADE;")
            print("   Dropped taskpriority ENUM")
        except Exception as e:
            print(f"   Could not drop taskpriority: {e}")

        # Commit changes
        conn.commit()
        print("\n6. Changes committed successfully!")

        # Verify final state
        print("\n7. Final state:")
        cursor.execute("""
            SELECT
                'status' as column_name,
                status as value,
                COUNT(*) as count
            FROM tasks
            GROUP BY status
            UNION ALL
            SELECT
                'priority' as column_name,
                priority as value,
                COUNT(*) as count
            FROM tasks
            GROUP BY priority
            ORDER BY column_name, value;
        """)

        print("\n   Value distribution:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]} ({row[2]} tasks)")

        print("\n" + "=" * 80)
        print("QUICK FIX COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nYou can now test GET /api/tasks endpoint.")
        print("The 500 error should be resolved.")

    except Exception as e:
        conn.rollback()
        print(f"\nERROR: {e}")
        print("Changes have been rolled back.")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
