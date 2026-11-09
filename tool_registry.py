from tools import calculator,calculate_revenue,write_file,read_file



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
        "description" : "Write the provided content in a specific file"
    },
    "read_file" : {
        "function" : read_file,
        "arguments" : ["filepath"],
        "description" : "Read the contents from a specific file"
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
    except Exception as e:
        return {
            "success" : False,
            "tool" : tool_name,
            "result" : None,
            "error" : str(e)
        }