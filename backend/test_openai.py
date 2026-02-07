"""
Test OpenAI integration to debug chatbot issues.
"""

import sys
from openai import OpenAI
from core.config import settings
from tools.task_tools import TASK_TOOLS

print("=" * 60)
print("OpenAI Integration Test")
print("=" * 60)

# Test 1: Check API key
print("\n1. Checking API key...")
if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith('sk-'):
    print(f"✓ API key configured: {settings.OPENAI_API_KEY[:15]}...")
else:
    print("✗ API key not configured properly")
    sys.exit(1)

# Test 2: Initialize client
print("\n2. Initializing OpenAI client...")
try:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
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
