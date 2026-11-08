from tools import calculator


def workflow():
    result = calculator(
        a=10,
        b=20,
        operation="add"
    )

    return result


print(workflow())