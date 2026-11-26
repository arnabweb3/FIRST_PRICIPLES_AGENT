from logger_config import logger
from plan_executor import execute_plan
from state import initialize_state, update_status
from planner import create_plan
from plan_validator import validate_plan
import time

def run_integrated_assistant(goal):
    start_time = time.time()

    state = initialize_state(goal=goal)

    logger.info("Integrated assistant started")

    logger.info(f"User goal: {goal}")

    try:
        plan = create_plan(user_goal=goal)

        logger.info(
            f"Plan generated : {len(plan['tasks'])} tasks"
        )

        validate_plan(plan=plan)

        logger.info("Plan validation successful")

        execution_result = execute_plan(goal)

        final_status = execution_result['status']

        update_status(state=state, status=final_status)

        duration = time.time() - start_time

        logger.info(
            f"Duration : {duration:.2f} seconds"
        )

        return {
            "status" : final_status,
            "goal" : goal,
            "execution_result" :  execution_result,
            "duration_seconds" : round(duration, 2)
        }

    except Exception as error:
        update_status(state=state, status="failed")

        logger.exception("Integrated assistent failed")

        return {
            "status" : "failed",
            "goal" : goal,
            "error" : str(error),
            "duration_seconds" : round(
                time.time() - start_time, 2
            )
        }

