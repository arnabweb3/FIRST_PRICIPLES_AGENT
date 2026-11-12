import json
from state import initialize_state, record_action, record_observation, update_status, build_context
from tool_registry import execute_tool
from decision_engine import get_decision

def run_agent(goal):

    state = initialize_state(goal=goal)

    max_iteration = 5

    for iteration in range(max_iteration):

        print(f"\n ---- Iteration {iteration + 1} ----\n")

        observations = state['observations']
        
        decision = get_decision(
            user_goal=goal,
            observations=observations
        ) # type: ignore

        print(f"Decision : {decision}")

        if not isinstance(decision, dict):
            update_status(state=state,status="failed")
            break

        action = decision.get("action")
        arguments = decision.get("arguments", {})



        if action == 'finish':

            final_answer = arguments.get("final_answer")

            update_status(
                state=state,
                status="completed",
                final_answer=final_answer
            )

            break

          


        if action == "ask_user":
            question = arguments.get("question")
            update_status(state=state, status="waiting for user")
            print(f"Clarification required : {question}")
            break

         
        record_action(
            state=state,
            tool_name=action,
            arguments=arguments,
        )
    
        result = execute_tool(tool_name=action , arguments=arguments)

         
        record_observation(
            state=state,
            tool_name=action,
            result=result,
            success=result['success']
        )

        print(f"Tool result : {result}")

        # return {
        #     "success" : True,
        #     "type" : "tool_execution",
        #     "result" : result['result'],
        #     "error" :  result['error']
        # }

    else:
        update_status(state=state, status="Max iteration reached")


    return state
 
    # update_status(
    #     state=state,
    #     status="completed",
    #     final_answer=str(result)
    # )


    # print(f"Final State : {state} \n")

    # return result



    # if decision["action"] == "calculator":
    #     args = decision["arguments"]

    #     record_action(
    #         state=state,
    #         tool_name= "calculator",
    #         arguments = args,
    #     )
    
    #     result = calculator(**args)


    #     record_observation(
    #         state=state,
    #         tool_name="calculator",
    #         result = result
    #     )

    #     update_status(
    #         state=state,
    #         status="completed",
    #         final_answer=str(result)
    #     )

    #     print(f"State : {state} \n")


    #     record_action(
    #         state=state,
    #         tool_name="write_file",
    #         arguments={"path" : "result.txt", "content" : str(state)}
    #     )


    #     write_file("result.txt" , str(result))

    #     record_observation(
    #         state=state,
    #         tool_name="write_file",
    #         result="File saved successfully"
    #     )

    #     update_status(
    #         state=state,
    #         status="completed",
    #         final_answer=f"Result : {result}. Saved in result.txt"
    #     )

    #     print(f"State : {state} \n")

    #     return f"Result : {result}"

        
    # elif decision['action'] == "read_file":

    #     record_action(
    #         state=state,
    #         tool_name = "read_file",
    #         arguments = {"content"  : prompt}
    #     )



    #     content = read_file(filepath="data/sales.csv")

    #     record_observation(
    #         state=state,
    #         tool_name="read_file",
    #         result=content
    #     )

    #     update_status(
    #         state=state,
    #         status="completed",
    #         final_answer=f"Extacted content from file \n {content}"
    #     )

    #     print(f"Final state : {state}")

    #     return f"Extacted content from file \n {content}"

    
 
    # elif decision['action'] == "calculate_revenue":
    #     args = decision['arguments']

    #     print(f"args : {args}")
    #     record_action(
    #         state=state,
    #         tool_name="calculate_revenue",
    #         arguments=args
    #     )

    #     result = calculate_revenue(**args)

    #     record_observation(
    #         state= state,
    #         tool_name="calculate_revenue",
    #         result=result
    #     )

    #     update_status(
    #         state=state,
    #         status="completed",
    #         final_answer=f"Total calculated revenue : {result}"
    #     )

    #     print(f"Final state : {state}")


    #     return result
    

    # elif decision['action'] == "write_file":
    #     args = decision['arguments']

    #     print(f"args : {args}")

    #     record_action(
    #         state=state,
    #         tool_name = "write_file",
    #         arguments=args
    #     )    

    #     result = write_file(**args)

    #     record_observation(
    #         state=state,
    #         tool_name="write_file",
    #         result="File write successful",      
    #     )

    #     update_status(
    #         state=state,
    #         status="completed",
    #         final_answer="Content saved in file successfully"
    #     )

    #     return "Content written in file"

    # elif decision['action'] == "respond":
    #     record_action(
    #         state= state,
    #         tool_name = "respond",
    #         arguments = {"content" : prompt}            
    #     )

    #     record_observation(
    #         state= state,
    #         tool_name="respond",
    #         result = decision['response'],
    #     )

    #     update_status(
    #         state=state,
    #         status="completed",
    #         final_answer=decision['response']
    #     )

    #     print(f"Final State : {state}")
        
    #     return decision["response"]

    # else:
    #     raise ValueError("Unknown action")


