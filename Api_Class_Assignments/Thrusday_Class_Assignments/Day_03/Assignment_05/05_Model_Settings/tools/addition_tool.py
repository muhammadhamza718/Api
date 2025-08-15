from agents import function_tool

@function_tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers and returns the result."""
    return a + b