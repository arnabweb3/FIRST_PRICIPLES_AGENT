from planner import create_plan
from tool_registry import execute_tool

import re

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
    plan = create_plan(user_goal=user_goal)


    if plan.get('status') != "ready":

        return {
            "status" : "needs_clarification",
            "plan" : plan
        }

    completed_tasks = []
    failed_tasks = []


    task_outputs = {}


    for task in plan['tasks']:
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





        result = execute_tool(
            tool_name=task['tool'],
            arguments=arguments
        )

        print(f"Result : {result}")


        if result['success']:

            completed_tasks.append(task['task_id'])

            task_outputs[task['task_id']] = result['result']

 
        else:

            failed_tasks.append( 
                {
                    'task_id' : task['task_id'],
                    'error' : result['error']
                }
            )

            break


    return {
        "status" : (
            "completed"
            if len(completed_tasks) == len(plan['tasks'])
            else "failed"
        ),
        "plan" : plan,
        "completed_tasks" : completed_tasks,
        "failed_tasks" : failed_tasks,
        "task_outputs" : task_outputs
    }

        

        

