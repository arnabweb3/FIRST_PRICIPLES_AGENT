from tools import calculator,calculate_revenue,write_file,read_file,revenue_by_product,get_highest_revenue_product, database_query, search_web, is_retryable_error

TOOL_REGISTRY = {
    "calculator" : {
        "function" : calculator,
        "arguments" : ["a" , "b" , "operation"],
        "description" : "Perform arithmatic operations"
    },
    "calculate_revenue" : {
        "function" : calculate_revenue,
        "arguments" : ["filepath"],
        "description" : "Calculate total revenue from a sales csv file"
    },
    "write_file" : {
        "function" : write_file,
        "arguments" : ["filepath","content"],
        "description" : "Write the provided content in a specific file",
        "retry_safe" : True
    },
    "read_file" : {
        "function" : read_file,
        "arguments" : ["filepath"],
        "description" : "Read the contents from a specific file"
    },
    "revenue_by_product" : {
        "function" : revenue_by_product,
        "arguments" : ['filepath'],
        "description" : "Calculate revenue of specific products"
    },
    "get_highest_revenue_product" : {
        "function" : get_highest_revenue_product,
        "arguments" : ['product_revenue'],
        "description" : "Identify the product category with highest revenue"
    },
    "database_query" : {
        "function" :  database_query,
        "arguments" : ['query'],
        "description" : "Fetch records from the sales SQLite database",
        "retry_safe" : True
    },
    "search_web" : {
        "function" :  search_web,
        "arguments" : ['query'],
        "description" : "Retrieve relevant data from the internet",
        "retry_safe" : True
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



def execute_tool(tool_name,arguments):
    try:
        validate_tool_call(tool_name,arguments)

        tool_function = TOOL_REGISTRY[tool_name]['function']

        result = tool_function(**arguments)

        return {
            "success" : True,
            "tool" : tool_name,
            "result" : result,
            "error" : None
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