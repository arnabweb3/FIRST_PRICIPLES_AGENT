from tool_registry import execute_tool



print(
    execute_tool(
        "calculator",
        {
            "a" : 10,
            "b" : 20,
            "operation" : "add"
        }
    )
)

print(
    execute_tool(
        "calculate_revenue",
        {
            "filepath" : "data/sales.csv",
            
        }
    )
)


print(
    execute_tool(
        "read_file",
        {
            "filepath" : "data/sales.csv"
        }
    )
)

print(
    execute_tool(
        "write_file",
        {
            "filepath" : "text.txt",
            "content" : "This is tool registry testing"
        }
    )
)