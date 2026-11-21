from planner import create_plan
from tool_registry import execute_tool
from plan_validator import validate_plan
from state import initialize_state, record_action, record_observation, update_status, build_context
import re
import json
import time
import random
from tool_registry import TOOL_REGISTRY

def resolve_references(arguments, task_outputs):

    resolved_arguments = {}

    pattern = r"\{\{task_(\d+)\.output\}\}"

    for key, value in arguments.items():

        if isinstance(value, str):

            # Case 1: Entire argument is a placeholder
            match = re.fullmatch(pattern, value.strip())

            if match:

                task_id = int(match.group(1))

                if task_id not in task_outputs:
                    raise ValueError(
                        f"Task {task_id} output not found"
                    )

                # Preserve the original Python data type
                resolved_arguments[key] = task_outputs[task_id]

            else:

                # Case 2: Placeholder embedded in a string
                def replace_reference(match):

                    task_id = int(match.group(1))

                    if task_id not in task_outputs:
                        raise ValueError(
                            f"Task {task_id} output not found"
                        )

                    return str(task_outputs[task_id])

                resolved_arguments[key] = re.sub(
                    pattern,
                    replace_reference,
                    value
                )

        else:
            resolved_arguments[key] = value

    return resolved_arguments


def execute_plan(user_goal):
    MAX_ITERATIONS = 10

    state = initialize_state(goal=user_goal)

    plan = create_plan(user_goal=user_goal)

    errors = validate_plan(plan=plan)

    if errors:
        return {
            "status" : "invalid_plan",
            "errors" : errors,
            "plan" : plan
        }


    if plan.get('status') != "ready":

        return {
            "status" : "needs_clarification",
            "plan" : plan
        }

    completed_tasks = []
    failed_tasks = []


    task_outputs = {}


    iteration_count = 0
    executed_calls = set()


    

    for task in plan['tasks']:
        if iteration_count >= MAX_ITERATIONS:
            status = "max_iterations_reached"
            break

        iteration_count += 1

        print(
            f"\n Executing task : {task['description']} \n"
        )

        dependencies = task.get('depends_on', [])


        if not all(
            task_id in completed_tasks for task_id in dependencies
        ):

            failed_tasks.append(
                {
                    "task_id" : task['task_id'],
                    "error" : "Dependencies not completed"
                }
            )
            break


        arguments = resolve_references(
            task['arguments'],
            task_outputs
        )



        record_action(
            state=state,
            tool_name=task['tool'],
            arguments=arguments
        )


        call_signature = (
            task['tool'],
            json.dumps(arguments, sort_keys = True, default=str)
        )

        if call_signature in executed_calls:
            status = 'loop_detected'

            failed_tasks.append(
                {
                    "task_id" : task['task_id'],
                    "error" : "Repeated tool call detected"
                }
            )

            break

        executed_calls.add(call_signature)



        result = execute_tool(
            tool_name=task['tool'],
            arguments=arguments,
            tool_registry=TOOL_REGISTRY
        )

        if not result['success']:
            failed_tasks.append(
                { 
                    "task_id" : task['task_id'],
                    "error" : result['error']
                }
            )

            status = "failed"
            break

        
        
        print(f"Result : {result}")

        record_observation(
            state=state,
            tool_name=task['tool'],
            result=result,
            success=result['success']
        )


        if result['success']:

            completed_tasks.append(task['task_id'])

            task_outputs[task['task_id']] = result['result']


        else:

            update_status(
                state=state,
                status='failed',
                final_answer=result['error']
            )

            failed_tasks.append( 
                {
                    'task_id' : task['task_id'],
                    'error' : result['error']
                }
            )

            break

    update_status(
        state,
        "completed",
        "All planned tasks completed successfully."
    )


    if failed_tasks:
        status = "failed"
    elif len(completed_tasks) == len(plan['tasks']):
        status = "completed"

    elif status == "running":
        status = "blocked"



    return {
        "status" : status,
        "state" : state,
        "plan" : plan,
        "completed_tasks" : completed_tasks,
        "failed_tasks" : failed_tasks,
        "task_outputs" : task_outputs
    }

        
def execute_with_retry(
        tool_name,
        arguments,
        max_attempts = 3,
        base_delay = 1,
        execute_fn=None
):
    if execute_fn is None:
        execute_fn = execute_tool
    
    
    tool_config = TOOL_REGISTRY[tool_name]

    if not tool_config.get("retry_safe", False):
        return execute_tool(
            tool_name=tool_name,
            arguments=arguments,
            tool_registry=TOOL_REGISTRY
        )
        
    for attempt in range(1, max_attempts + 1):

        print(
            f"Attempt {attempt}/{max_attempts}: "
            f"{tool_name}"
        )

        # result = execute_tool(
        #     tool_name=tool_name,
        #     arguments=arguments
        # )

        result = execute_fn(
            tool_name=tool_name,
            arguments=arguments
        )

        # Stop immediately if successful
        if result["success"]:
            return result

        # Do not retry permanent errors
        if not result.get("retryable", False):
            return result

        # Stop if attempts are exhausted
        if attempt == max_attempts:
            return result

        # Exponential backoff with jitter
        delay = base_delay * (2 ** (attempt - 1))
        delay += random.uniform(0, 0.5)

        print(f"Temporary error. Retrying in {delay:.2f} seconds.")

        time.sleep(delay)

    return result
