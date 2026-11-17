from agent import run_agent
from dotenv import load_dotenv
from state import initialize_state, record_action, record_observation, update_status, build_context
from tools import calculator, write_file, calculate_revenue, database_query, search_web
from plan_executor import execute_plan



load_dotenv()






goal = input("User : ")


# goal = """
# Analyze data/sales.csv.

# 1. Calculate total revenue.
# 2. Calculate revenue by product.
# 3. Identify the highest-revenue product.
# 4. Save a complete report in output/sales_analysis.txt.
# """

# output = run_agent(goal)
output = execute_plan(goal)


print(f"Agent : {output}")


output_status = output['status']

final_answer = ""

if output_status == "completed":
    final_answer = "All planned tasks are completed"

elif output_status == "failed":
    final_answer = "Execution failed. Check the failed task details."

elif output_status == "loop_detected":
    final_answer = "Execution stopped because a repeated tool call was detected."

elif output_status == "max_iterations_reached":
    final_answer = "Execution stopped after reaching the iteration limit."

else:
    final_answer = "Execution could not complete all planned tasks."
    

# update_status(
#     output['state'],
#     output_status,
#     final_answer
# )


# state  = initialize_state(goal=goal)

# record_action(
#     state=state, 
#     tool_name="calculator", 
#     arguments={"a" : 100 , "b" : 200 , "operation" : "add"}
# )

# result = calculator(a=100, b=200, operation="add")

# record_observation(state=state, tool_name="calculator", result=result)


# print(state)


# record_action(
#     state=state,
#     tool_name="write_file",
#     arguments={"path" : "result.txt" , "content" : str(state)}
# )


# record_observation(
#     state=state,
#     tool_name="write_file",
#     result="File saved successfully",

# )


# update_status(
#     state=state,
#     status="completed",
#     final_answer="100 + 200 = 300 . Saved in result.txt"

# )

# print(state)

