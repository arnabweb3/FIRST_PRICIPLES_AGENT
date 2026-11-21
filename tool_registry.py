from tools import calculator,calculate_revenue,write_file,read_file,revenue_by_product,get_highest_revenue_product, database_query, search_web, is_retryable_error


from tool_safety import (
    check_tool_permission,
    validate_output_path
)

TOOL_REGISTRY = {
    "calculator" : {
        "function" : calculator,
        "arguments" : ["a" , "b" , "operation"],
        "description" : "Perform arithmatic operations",
        "permission" : "safe"
    },
    "calculate_revenue" : {
        "function" : calculate_revenue,
        "arguments" : ["filepath"],
        "description" : "Calculate total revenue from a sales csv file",
        "permission" : "safe"
    },
    "write_file" : {
        "function" : write_file,
        "arguments" : ["filepath","content"],
        "description" : "Write the provided content in a specific file",
        "retry_safe" : True,
        "permission" : "restricted"
    },
    "read_file" : {
        "function" : read_file,
        "arguments" : ["filepath"],
        "description" : "Read the contents from a specific file",
        "permission" : "safe"
    },
    "revenue_by_product" : {
        "function" : revenue_by_product,
        "arguments" : ['filepath'],
        "description" : "Calculate revenue of specific products",
        "permission" : "safe",
    },
    "get_highest_revenue_product" : {
        "function" : get_highest_revenue_product,
        "arguments" : ['product_revenue'],
        "description" : "Identify the product category with highest revenue",
        "permission" : "safe",

    },
    "database_query" : {
        "function" :  database_query,
        "arguments" : ['query'],
        "description" : "Fetch records from the sales SQLite database",
        "retry_safe" : True,
        "permission" : "safe",
        
    },
    "search_web" : {
        "function" :  search_web,
        "arguments" : ['query'],
        "description" : "Retrieve relevant data from the internet",
        "retry_safe" : True,
        "permission" : "safe",

    }
}




def validate_tool_call(tool_name,arguments):

    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool : {tool_name}")


    if not isinstance(arguments,dict):
        raise ValueError("Arguments must be a dictionary")


    required_args = TOOL_REGISTRY[tool_name]['arguments']


    missing_args = [
        arg for arg in required_args 
        if arg not in arguments
    ]

    if missing_args:
        raise ValueError(f"Missing required arguments : {missing_args}")


    unexpected_args = [
        arg for arg in arguments
        if arg not in required_args
    ]

    if unexpected_args:
        raise ValueError(f"Unexpected arguments provided : {unexpected_args}")


    return True






def execute_tool(tool_name, arguments, approved=False, tool_registry=None):

    try:
        # Step 1: Validate tool name and arguments
        validate_tool_call(tool_name, arguments)

        if tool_registry is None:
            raise ValueError("Tool registry must be provided.")

        # Step 2: Check tool permissions
        permission_result = check_tool_permission(
            tool_name,
            TOOL_REGISTRY,
            approved=approved
        )

        if not permission_result["allowed"]:
            return {
                "success": False,
                "tool": tool_name,
                "result": None,
                "error": permission_result["reason"],
                "error_type": "PermissionError",
                "retryable": False
            }

        # Step 3: Validate file output path
        if tool_name == "write_file":

            path = arguments.get("path")

            if not path or not validate_output_path(path):
                return {
                    "success": False,
                    "tool": tool_name,
                    "result": None,
                    "error": "Writing outside the output directory is prohibited.",
                    "error_type": "PathValidationError",
                    "retryable": False
                }

        # Step 4: Retrieve registered tool function
        tool_function = TOOL_REGISTRY[tool_name]["function"]

        # Step 5: Execute tool
        result = tool_function(**arguments)

        return {
            "success": True,
            "tool": tool_name,
            "result": result,
            "error": None,
            "retryable": False
        }

    except Exception as error:

        return {
            "success": False,
            "tool": tool_name,
            "result": None,
            "error": str(error),
            "error_type": type(error).__name__,
            "retryable": is_retryable_error(error)
        }

        # return {
        #     "success" : False,
        #     "tool" : tool_name,
        #     "result" : None,
        #     "error" : str(e)
        # }