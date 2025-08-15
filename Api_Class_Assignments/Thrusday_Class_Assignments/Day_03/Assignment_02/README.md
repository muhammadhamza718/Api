# Day 03 Assignment 02 - Math Agent with Tools 🧮

## Overview

This assignment demonstrates the creation of a math assistant agent that uses function tools to perform calculations. The agent can handle mathematical operations and provide accurate results using the `@function_tool` decorator.

## Features Implemented

### 1. Function Tool Creation

- **Location:** `main.py`
- **Feature:** `@function_tool` decorator for `add()` function
- **Purpose:** Converts Python function into an AI tool that can be used by the agent

### 2. Math Agent with Tools

- **Location:** `main.py`
- **Feature:** Agent configured with mathematical tools
- **Purpose:** Demonstrates how agents can use tools to perform specific tasks

### 3. Chainlit Integration

- **Location:** `main.py`
- **Feature:** Web-based chat interface with tool-enabled agent
- **Purpose:** Provides interactive interface for mathematical calculations

## Technical Implementation

### Function Tool Definition

```python
@function_tool
def add(a: float, b: float) -> float:
    """Adds two numbers and returns the result."""
    return a + b
```

### Agent Configuration with Tools

```python
math_agent = Agent(
    name="MathBot",
    instructions="You are a helpful math assistant. Use the provided tools to perform calculations when needed.",
    model=gemini_model,
    tools=[add]  # Register the function tool
)
```

### Key Features

- **Type Annotations:** Function parameters and return types are properly typed
- **Docstring:** Clear description of what the function does
- **Tool Registration:** Function is registered with the agent via the `tools` parameter

## How to Run

### Prerequisites

- Python 3.8+
- Required packages: `agents`, `chainlit`, `python-dotenv`, `decouple`

### Environment Variables

Create a `.env` file with:

```
GEMINI_API_KEY=your_gemini_api_key
GEMINI_BASE_URL=your_gemini_base_url
```

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Chainlit
chainlit run main.py

# Or run terminal version (uncomment in main.py)
python main.py
```

## Test Scenarios

1. ✅ Ask "What is 2 + 2?" → Agent uses add tool and returns 4
2. ✅ Ask "Can you add 15.5 and 23.7?" → Agent calculates 39.2
3. ✅ Ask "What's 100 + 200?" → Agent provides accurate calculation
4. ✅ Ask non-math questions → Agent responds appropriately
5. ✅ Complex calculations → Agent handles multiple operations

## Learning Objectives

- Function tool creation and decoration
- Agent configuration with tools
- Type annotations for function tools
- Tool integration with Chainlit interface
- Mathematical operation handling

## File Structure

```
Assignment_02/
├── main.py          # Main application with math agent and tools
├── pyproject.toml   # Project dependencies
├── README.md        # This documentation
└── chainlit.md      # Chainlit welcome screen
```

## Key Concepts Demonstrated

### Function Tools

- **Purpose:** Extend agent capabilities with custom functions
- **Implementation:** Use `@function_tool` decorator
- **Benefits:** Type safety, clear documentation, automatic tool registration

### Agent-Tool Integration

- **Registration:** Tools are passed to agent via `tools` parameter
- **Usage:** Agent automatically decides when to use tools
- **Response:** Agent provides context and explanation with results

## Next Steps

This math agent demonstrates the foundation of tool usage. The next assignments will build on this by adding more complex tools, multiple tools, and advanced agent features.
