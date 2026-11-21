
import os


def check_tool_permission(
    tool_name,
    tool_registry,
    approved=False
):

    if tool_name not in tool_registry:
        return {
            "allowed": False,
            "reason": "Unknown tool."
        }

    permission = tool_registry[tool_name].get(
        "permission",
        "restricted"
    )

    if permission == "safe":
        return {
            "allowed": True,
            "reason": "Safe tool."
        }

    if permission == "restricted" and approved:
        return {
            "allowed": True,
            "reason": "User approval received."
        }

    return {
        "allowed": False,
        "reason": "Explicit user approval required."
    }


def validate_output_path(path):

    base_directory = os.path.abspath("output")

    target_path = os.path.abspath(
        os.path.join(base_directory, path)
        if not os.path.isabs(path)
        else path
    )

    try:
        common_path = os.path.commonpath([
            base_directory,
            target_path
        ])
    except ValueError:
        return False

    return common_path == base_directory
