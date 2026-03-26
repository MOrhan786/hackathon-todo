"""
Test OpenAI integration to debug chatbot issues.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if API key is set before importing OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("=" * 60)
    print("ERROR: OPENAI_API_KEY environment variable is not set!")
    print("=" * 60)
    print("\nPlease follow these steps:")
    print("1. Copy backend/.env.example to backend/.env")
    print("2. Get your API key from: https://platform.openai.com/api-keys")
    print("3. Add it to backend/.env:")
    print("   OPENAI_API_KEY=sk-your-actual-api-key-here")
    print("=" * 60)
    sys.exit(1)

from openai import OpenAI
from core.config import settings
from tools.task_tools import TASK_TOOLS

print("=" * 60)
print("OpenAI Integration Test")
print("=" * 60)

# Test 1: Check API key
print("\n1. Checking API key...")
if api_key and api_key.startswith('sk-'):
    print(f"✓ API key configured: {api_key[:15]}...")
else:
    print("✗ API key not configured properly")
    print(f"  Current value starts with: {api_key[:10] if api_key else 'EMPTY'}...")
    sys.exit(1)

# Test 2: Initialize client
print("\n2. Initializing OpenAI client...")
try:
    client = OpenAI(api_key=api_key)
    print("✓ Client initialized")
except Exception as e:
    print(f"✗ Failed to initialize client: {e}")
    sys.exit(1)

# Test 3: Check tools
print("\n3. Checking task tools...")
print(f"✓ Found {len(TASK_TOOLS)} tools:")
for tool in TASK_TOOLS:
    print(f"  - {tool['function']['name']}")

# Test 4: Simple API call (no tools)
print("\n4. Testing simple API call...")
try:
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word."}
        ],
        max_tokens=10
    )
    print(f"✓ API call successful")
    print(f"  Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"✗ API call failed: {e}")
    print(f"  Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: API call with tools
print("\n5. Testing API call with tools...")
try:
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a task management assistant."},
            {"role": "user", "content": "Create a task to test the integration"}
        ],
        tools=TASK_TOOLS,
        tool_choice="auto"
    )
    print(f"✓ API call with tools successful")

    if response.choices[0].message.tool_calls:
        print(f"  Tool calls requested: {len(response.choices[0].message.tool_calls)}")
        for tc in response.choices[0].message.tool_calls:
            print(f"    - {tc.function.name}")
    else:
        print(f"  No tool calls, response: {response.choices[0].message.content}")

except Exception as e:
    print(f"✗ API call with tools failed: {e}")
    print(f"  Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All tests passed! OpenAI integration working.")
print("=" * 60)
