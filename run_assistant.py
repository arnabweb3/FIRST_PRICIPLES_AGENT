from integrated_assistent import run_integrated_assistant


def run_assistant():
    goal = input("User : ")

    result = run_integrated_assistant(goal=goal)


    print("\n--FINAL RESULT--\n")

    print(f"Status : ", result['status'])

    if result['status'] == 'completed':
        print("All tasks completed successfully")

    else:
        print("Execution did not complete successfully")


    print("\nFull execution details:")

    print(result)