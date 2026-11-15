from tool_registry import TOOL_REGISTRY



def validate_plan(plan):
    errors = []


    if not isinstance(plan, dict):
        return ['Plan must be a dictionary']

    if plan.get('status') != 'ready':
        return ["Plan is not ready for execution"]


    tasks = plan.get('tasks')

    if not isinstance(tasks,list) or not tasks:
        return ['Plan must contain a non-empty task list']


    task_ids = [task.get('task_id') for task in tasks]

    print(task_ids)
    print(set(task_ids))

    if len(task_ids) != len(set(task_ids)):
        errors.append('Duplicate task IDs found')

    if any(
        not isinstance(task_id, int) or isinstance(task_id, bool)
        for task_id in task_ids
    ):
        errors.append("Task IDs must be integers")

    if errors:
        return errors


    known_ids = set(task_ids)
    seen_ids = set()


    for task in tasks:

        task_id = task["task_id"]
        tool_name = task.get("tool")
        arguments = task.get("arguments")
        dependencies = task.get("depends_on", [])

        if tool_name not in TOOL_REGISTRY:
            errors.append(
                f"Task {task_id}: Unknown tool {tool_name}"
            )
            continue

        if not isinstance(arguments, dict):
            errors.append(
                f"Task {task_id}: Arguments must be a dictionary"
            )
            continue

        required = set(
            TOOL_REGISTRY[tool_name]["arguments"]
        )

        supplied = set(arguments.keys())

        if required != supplied:
            errors.append(
                f"Task {task_id}: Expected arguments {required}, "
                f"received {supplied}"
            )

        if not isinstance(dependencies, list):
            errors.append(
                f"Task {task_id}: Dependencies must be a list"
            )
            continue

        if len(dependencies) != len(set(dependencies)):
            errors.append(
                f"Task {task_id}: Duplicate dependencies"
            )

        for dependency in dependencies:

            if dependency not in known_ids:
                errors.append(
                    f"Task {task_id}: Unknown dependency {dependency}"
                )

            elif dependency not in seen_ids:
                errors.append(
                    f"Task {task_id}: Dependency must appear earlier "
                    "in the plan"
                )

            if dependency == task_id:
                errors.append(
                    f"Task {task_id}: Cannot depend on itself"
                )

        seen_ids.add(task_id)

    return errors