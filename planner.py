
import json

from decision_engine import client, get_tool_descriptions
from logger_config import logger

MODEL = "gemini-3.5-flash-lite"


def create_plan(user_goal):

    available_tools = get_tool_descriptions()

    prompt = f"""
You are an expert planning engine for a Python AI Agent.

YOUR RESPONSIBILITY:
Convert the user's goal into a structured, executable task plan.

USER GOAL:
{user_goal}

AVAILABLE TOOLS:
{json.dumps(available_tools, indent=2)}

PLANNING RULES:

1. Break the user goal into small, executable tasks.

2. Create a logical execution sequence.

3. Assign every task a unique integer task_id.

4. Use ONLY tools listed in AVAILABLE TOOLS.

5. Use the exact argument names specified in each
   tool's required_args.

6. Never invent tools, arguments, file paths,
   calculated values, or execution results.

7. Identify task dependencies accurately.

8. Tasks without dependencies should have:
   "depends_on": []

9. A task must depend on every earlier task whose
   output it uses.

10. Do not execute tools. Only create the plan.

11. If essential information is missing, return
    status as "needs_clarification".

DATA PASSING BETWEEN TASKS:

When a task requires the output of a previous task,
use exactly this placeholder format:

{{{{task_1.output}}}}

Replace 1 with the actual task ID.

Examples:

A. Direct output reference:

"content": "{{{{task_1.output}}}}"

B. Multiple references in one string:

"content": "Total Revenue: {{{{task_1.output}}}}\\nProduct Revenue: {{{{task_2.output}}}}"

C. Passing a dictionary output to another tool:

"product_revenue": "{{{{task_2.output}}}}"

IMPORTANT DATA PASSING RULES:

- Always use {{{{task_ID.output}}}}.
- Never use $task_ID.output.
- Never use task_ID.result.
- Never invent calculated values.
- References may appear inside larger strings.
- A reference must point to an existing earlier task.
- Use references only when actual previous task output is required.

DERIVED CALCULATIONS:

If a goal requires calculating something from
previous task output, use an appropriate registered tool.

Example:

To identify the highest-revenue product:

1. Execute revenue_by_product.
2. Pass its output to get_highest_revenue_product.
3. Use the result in the report.

Do not assume that write_file can perform calculations.

REPORT GENERATION:

When generating a report:

1. Identify all calculations required.
2. Execute those calculations first.
3. Create the report only after the required
   outputs are available.
4. Include references to actual task outputs.
5. Set depends_on to include every task whose
   output is used in the report.

DATABASE QUERY RULES:
- Use only columns defined in the database schema.
- The sales table has:
  order_id, customer, product, quantity, unit_price, region.
- There is no revenue column.
- Calculate revenue using quantity * unit_price.
- To calculate total revenue by product, use:
  SELECT product,
         SUM(quantity * unit_price) AS total_revenue
  FROM sales
  GROUP BY product;

TASK DEPENDENCY RULES:

- A task can execute only after all its dependencies
  have completed.
- Tasks without dependencies can execute independently.
- Use integer task IDs in depends_on.
- Do not create circular dependencies.

OUTPUT FORMAT:

Return ONLY valid JSON.
Do not include Markdown code fences or explanations.

For a valid plan, use:

{{
    "status": "ready",
    "goal": "Original user goal",
    "tasks": [
        {{
            "task_id": 1,
            "description": "Calculate total revenue",
            "tool": "calculate_revenue",
            "arguments": {{
                "path": "data/sales.csv"
            }},
            "depends_on": []
        }},
        {{
            "task_id": 2,
            "description": "Save calculated revenue",
            "tool": "write_file",
            "arguments": {{
                "path": "result.txt",
                "content": "Total Revenue: {{{{task_1.output}}}}"
            }},
            "depends_on": [1]
        }}
    ]
}}

For missing information, use:

{{
    "status": "needs_clarification",
    "goal": "Original user goal",
    "question": "Clarification required",
    "tasks": []
}}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    plan = json.loads(response.text)

    logger.info(
        f"Plan generated with {len(plan['tasks'])} tasks"
    )


    return plan
