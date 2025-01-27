import math


def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Parameters:
        a (float): First number to multiply
        b (float): Second number to multiply

    Returns:
        float: The product of the two numbers
    """
    return a * b


def add(a: float, b: float) -> float:
    """Add two numbers.

    Parameters:
        a (float): First number to add
        b (float): Second number to add

    Returns:
        float: The sum of the two numbers
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract two numbers.

    Parameters:
        a (float): First number to subtract
        b (float): Second number to subtract

    Returns:
        float: The difference of the two numbers
    """
    return a - b


def divide(a: float, b: float) -> float:
    """Divide two numbers.

    Parameters:
        a (float): First number to divide
        b (float): Second number to divide

    Returns:
        float: The quotient of the two numbers
    """
    return a / b


def power(base: float, exponent: float) -> float:
    """Calculate base raised to exponent.

    Parameters:
        base (float): The base number
        exponent (float): The exponent to raise the base to

    Returns:
        float: The result of base raised to the power of exponent
    """
    return base**exponent


def sqrt(value: float) -> float:
    """Calculate the square root of a number.

    Parameters:
        value (float): The number to calculate the square root of

    Returns:
        float: The square root of the number
    """
    return math.sqrt(value)


def factorial(n: int) -> int | None:
    """Calculate the factorial of a number.

    Parameters:
        n (int): The number to calculate the factorial of

    Returns:
        int: The factorial of the number
    """
    return math.factorial(n) if n >= 0 else None
