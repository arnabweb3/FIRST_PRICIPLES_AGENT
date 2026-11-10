from tool_registry import TOOL_REGISTRY
import json
from google import genai
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv


load_dotenv()

client = genai.Client()


def get_tool_descriptions():
    descriptions = {}

    for tool_name,details in TOOL_REGISTRY.items():
        descriptions[tool_name] = {
            "description" : details['description'],
            "required_args" : details['arguments']
        }


    return descriptions


def get_decision(user_goal):

    available_tools = get_tool_descriptions()


    prompt = f"""
    You are the decision engine of a Python AI agent.

    USER GOAL:
    {user_goal}

    AVAILABLE TOOLS:
    {json.dumps(available_tools, indent=2)}

    Your task:
    1. Decide whether a tool is required.
    2. If a tool is required, select exactly one tool.
    3. Provide all required arguments.
    4. If no tool is required, respond directly.

    Return ONLY valid JSON.

    For tool execution, use:
    {{
        "action": "tool_name",
        "arguments": {{}},
        "reason": "short explanation"
    }}

    For a direct response, use:
    {{
        "action": "respond",
        "arguments": {{
            "response": "Your answer"
        }},
        "reason": "short explanation"
    }}

    Never invent file paths.
    Never select tools that are not available.
    Do not return Markdown or code fences.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=GenerateContentConfig(
            temperature=0
        )
    )

    print(f"LLM response : {response.text}")

    return json.loads(response.text)

