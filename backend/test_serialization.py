"""
Test script to reproduce the serialization error
"""
from sqlmodel import Session, create_engine, select
from models.task import Task
from schemas.task import TaskResponse
import os
from dotenv import load_dotenv

load_dotenv()

# Get connection string from .env
db_url = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(db_url, echo=False)

print("=" * 80)
print("TESTING TASK SERIALIZATION")
print("=" * 80)

with Session(engine) as session:
    # Get first task
    statement = select(Task).limit(1)
    task = session.exec(statement).first()

    if task:
        print("\n1. Raw Task Object from Database:")
        print(f"   Type: {type(task)}")
        print(f"   ID: {task.id} (type: {type(task.id)})")
        print(f"   User ID: {task.user_id} (type: {type(task.user_id)})")
        print(f"   Title: {task.title}")

        print("\n2. Task.__dict__:")
        for key, value in task.__dict__.items():
            if not key.startswith('_'):
                print(f"   {key}: {value} (type: {type(value).__name__})")

        print("\n3. Attempting task.model_dump():")
        try:
            dumped = task.model_dump()
            print("   SUCCESS!")
            print("   Dumped data:")
            for key, value in dumped.items():
                print(f"   {key}: {value} (type: {type(value).__name__})")
        except Exception as e:
            print(f"   ERROR: {e}")
            print(f"   Error type: {type(e).__name__}")

        print("\n4. Attempting TaskResponse.model_validate(task.model_dump()):")
        try:
            dumped = task.model_dump()
            response = TaskResponse.model_validate(dumped)
            print("   SUCCESS!")
            print(f"   Response: {response}")
        except Exception as e:
            print(f"   ERROR: {e}")
            print(f"   Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()

        print("\n5. Attempting TaskResponse.model_validate(task):")
        try:
            response = TaskResponse.model_validate(task)
            print("   SUCCESS!")
            print(f"   Response ID: {response.id} (type: {type(response.id)})")
            print(f"   Response User ID: {response.user_id} (type: {type(response.user_id)})")
        except Exception as e:
            print(f"   ERROR: {e}")
            print(f"   Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()

        print("\n6. Check if user_id is a string or UUID object:")
        print(f"   task.user_id: {task.user_id!r}")
        print(f"   Type: {type(task.user_id)}")
        print(f"   Is string? {isinstance(task.user_id, str)}")

        # Try to access .id attribute
        print("\n7. Testing if user_id has .id attribute (the error suggests this):")
        try:
            print(f"   task.user_id.id: {task.user_id.id}")
        except AttributeError as e:
            print(f"   ERROR: {e}")
            print("   This confirms user_id is a string, not an object with .id")
    else:
        print("No tasks found in database!")

print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
