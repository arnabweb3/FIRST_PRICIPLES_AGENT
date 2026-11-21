from plan_executor import execute_with_retry


attempt_counter = {"count": 0}


def fake_execute_tool(tool_name, arguments):

    attempt_counter["count"] += 1

    if attempt_counter["count"] < 3:
        return {
            "success": False,
            "tool": tool_name,
            "error": "Connection timed out",
            "retryable": True
        }

    return {
        "success": True,
        "tool": tool_name,
        "result": "Operation successful"
    }


def test_retry():

    global_result = execute_with_retry(
        tool_name="search_web",
        arguments={"query": "AI agents"},
        max_attempts=3,
        base_delay=0,
        execute_fn=fake_execute_tool
    )

    print(global_result)
    print("Attempts:", attempt_counter["count"])


if __name__ == "__main__":
    test_retry()
