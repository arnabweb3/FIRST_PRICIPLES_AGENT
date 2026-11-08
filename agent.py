import json
from tools import calculator
from google import genai
from google.genai.types import GenerateContentConfig
from state import initialize_state, record_action, record_observation, update_status, build_context
from tools import write_file,read_file,calculate_revenue

def agent(goal):

    state = initialize_state(goal=goal)

    prompt = f"""
        You are an AI Agent

        Goal : {goal}

        Available actions:
        1. calculator
        2. calculate_revenue
        3. read_file
        4. write_file
        5. respond

        Decide what action is needed

        If calculation is required then use calculator
        If a revenue specific calculation is required then use calculate_revenue
        If reading content from a file is required then use read_file
        If writing content to a file is required then use write_file
        Otherwise use respond

        Return ONLY valid json

        Format : {{
            "action" : "calculator or respond",
            "arguments" : {{
                "a" : 0,
                "b" : 0,
                "operation" :  "multiply"
            
            }},
            "response" : null
        }}

        OR

        Format : {{
            "action" : "calculate_revenue or respond",
            "arguments" : {{
                "filepath" : "data/sales.csv"
            
            }},
            "response" : null
        }}

        OR

        Format : {{
            "action" : "read_file or respond",
            "arguments" : {{
                "filepath" : "data/result.txt"
            
            }},
            "response" : null
        }}

        OR

        Format : {{
            "action" : "write_file or respond",
            "arguments" : {{
                "filepath" : "data/result.txt",
                "content" : "provided by user prompt"
            
            }},
            "response" : null
        }}
        

    
    """
    llm = genai.Client()

    decision_response = llm.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=GenerateContentConfig(
            temperature=0
        )
    )



    decision = json.loads(decision_response.text)



    if decision["action"] == "calculator":
        args = decision["arguments"]

        record_action(
            state=state,
            tool_name= "calculator",
            arguments = args,
        )
    
        result = calculator(**args)


        record_observation(
            state=state,
            tool_name="calculator",
            result = result
        )

        update_status(
            state=state,
            status="completed",
            final_answer=str(result)
        )

        print(f"State : {state} \n")


        record_action(
            state=state,
            tool_name="write_file",
            arguments={"path" : "result.txt", "content" : str(state)}
        )


        write_file("result.txt" , str(result))

        record_observation(
            state=state,
            tool_name="write_file",
            result="File saved successfully"
        )

        update_status(
            state=state,
            status="completed",
            final_answer=f"Result : {result}. Saved in result.txt"
        )

        print(f"State : {state} \n")

        return f"Result : {result}"

        
    elif decision['action'] == "read_file":

        record_action(
            state=state,
            tool_name = "read_file",
            arguments = {"content"  : prompt}
        )



        content = read_file(filepath="data/sales.csv")

        record_observation(
            state=state,
            tool_name="read_file",
            result=content
        )

        update_status(
            state=state,
            status="completed",
            final_answer=f"Extacted content from file \n {content}"
        )

        print(f"Final state : {state}")

        return f"Extacted content from file \n {content}"

    
 
    elif decision['action'] == "calculate_revenue":
        args = decision['arguments']

        print(f"args : {args}")
        record_action(
            state=state,
            tool_name="calculate_revenue",
            arguments=args
        )

        result = calculate_revenue(**args)

        record_observation(
            state= state,
            tool_name="calculate_revenue",
            result=result
        )

        update_status(
            state=state,
            status="completed",
            final_answer=f"Total calculated revenue : {result}"
        )

        print(f"Final state : {state}")


        return result
    

    elif decision['action'] == "write_file":
        args = decision['arguments']

        print(f"args : {args}")

        record_action(
            state=state,
            tool_name = "write_file",
            arguments=args
        )    

        result = write_file(**args)

        record_observation(
            state=state,
            tool_name="write_file",
            result="File write successful",      
        )

        update_status(
            state=state,
            status="completed",
            final_answer="Content saved in file successfully"
        )

        return "Content written in file"

    elif decision['action'] == "respond":
        record_action(
            state= state,
            tool_name = "respond",
            arguments = {"content" : prompt}            
        )

        record_observation(
            state= state,
            tool_name="respond",
            result = decision['response'],
        )

        update_status(
            state=state,
            status="completed",
            final_answer=decision['response']
        )

        print(f"Final State : {state}")
        
        return decision["response"]

    else:
        raise ValueError("Unknown action")


