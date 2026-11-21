
from tool_safety import (
    check_tool_permission,
    validate_output_path
)

from tool_registry import TOOL_REGISTRY


def run_tests():

    # Test 1: Safe tool should be allowed
    result = check_tool_permission(
        "calculator",
        TOOL_REGISTRY
    )

    assert result["allowed"] is True
    print("Test 1 passed: Safe tool allowed.")

    # Test 2: Restricted tool without approval
    result = check_tool_permission(
        "write_file",
        TOOL_REGISTRY
    )

    assert result["allowed"] is False
    print("Test 2 passed: Restricted tool blocked.")

    # Test 3: Restricted tool with approval
    result = check_tool_permission(
        "write_file",
        TOOL_REGISTRY,
        approved=True
    )

    assert result["allowed"] is True
    print("Test 3 passed: Approved tool allowed.")

    # Test 4: Valid relative output path
    assert validate_output_path(
        "report.txt"
    ) is True

    print("Test 4 passed: Valid output path.")

    # Test 5: Path traversal blocked
    assert validate_output_path(
        "../secret.txt"
    ) is False

    print("Test 5 passed: Path traversal blocked.")

    # Test 6: Explicit output directory path
    assert validate_output_path(
        "output/report.txt"
    ) is True

    print("Test 6 passed: Output directory path.")

    # Test 7: Unknown tool blocked
    result = check_tool_permission(
        "unknown_tool",
        TOOL_REGISTRY
    )

    assert result["allowed"] is False
    print("Test 7 passed: Unknown tool blocked.")

    print("\nAll 7 safety tests passed!")


if __name__ == "__main__":
    run_tests()
