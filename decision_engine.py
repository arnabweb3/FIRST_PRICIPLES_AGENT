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


def get_decision(user_goal,observations):

    available_tools = get_tool_descriptions()


    prompt = f"""
    You are the decision engine of a Python AI agent.

    USER GOAL:
    {user_goal}

    AVAILABLE TOOLS:
    {json.dumps(available_tools, indent=2)}


    PREVIOUS OBSERVATIONS:
    {json.dumps(observations, indent=2)}


    Decide the next action

    Rules:
    1. Select exactly one available tool if more work is required.
    2. Use previous observations when deciding the next action.
    3. Do not repeat successful actions unnecessarily.
    4. If the goal is fully completed, select finish.
    5. Never invent file paths or tool names.
    6. If required information is missing, select ask_user.
    
    Return ONLY valid JSON.

    For tool execution, use:
    {{
        "action": "tool_name",
        "arguments": {{}},
        "reason": "short explanation"
    }}

    For completion:
    {{
        "action": "finish",
        "arguments": {{
            "final_answer": "Task completion summary"
        }},
        "reason": "Goal achieved"
    }}

    For clarification:
    {{
        "action": "ask_user",
        "arguments": {{
            "question": "Clarification question"
        }},
        "reason": "Required information is missing"
    }}


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

