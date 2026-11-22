from logger_config import logger
from execution_tracker import record_execution


def run_tests():

    logger.info("Agent started")

    logger.info("Planner generated a plan")

    logger.warning("Temporary network error")

    logger.error("Tool execution failed")

    record_execution(
        "test_execution",
        {
            "tool": "calculator",
            "success": True
        }
    )

    print("Logging tests completed.")


if __name__ == "__main__":
    run_tests()