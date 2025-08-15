# Day 03 Assignment 04 - Multi-Tool Agent 🛠️

## Overview

This assignment demonstrates the creation of a versatile assistant agent that can handle multiple types of tasks using various tools. The agent integrates math, weather, and time tools to provide comprehensive assistance.

## Features Implemented

### 1. Multiple Function Tools

- **Location:** `tools/` directory
- **Feature:** Three specialized tools for different tasks
- **Purpose:** Demonstrates agent capability to handle diverse requests

### 2. Multi-Tool Agent

- **Location:** `main.py`
- **Feature:** Agent configured with multiple tools
- **Purpose:** Single agent that can handle math, weather, and time queries

### 3. Tool Organization

- **Location:** `tools/` directory structure
- **Feature:** Modular tool organization
- **Purpose:** Clean separation of concerns and maintainable code

## Technical Implementation

### Tool Structure

```
tools/
├── addition_tool.py      # Mathematical operations
├── weather_api_tool.py   # Weather data fetching
└── datetime_tool.py      # Time zone information
```

### Multi-Tool Agent Configuration

```python
multi_tool_agent = Agent(
    name="MultiToolBot",
    instructions="""
    You are a versatile assistant that can handle multiple tasks:
    - For math questions like 'What is X + Y?', use the `add` tool
    - For weather queries like 'What's the weather in [city]?', use the `get_weather` tool
    - For time queries like 'What time is it in [timezone]?', use the `get_time` tool
    """,
    model=gemini_model,
    tools=[add, get_weather, get_time]  # Multiple tools registered
)
```

### Individual Tools

#### Addition Tool

```python
@function_tool
def add(a: float, b: float) -> float:
    """Adds two numbers and returns the result."""
    return a + b
```

#### Weather Tool

```python
@function_tool
def get_weather(city: str) -> str:
    """Fetches the current temperature for a given city."""
    # OpenWeatherMap API integration
```

#### Time Tool

```python
@function_tool
def get_time(timezone: str) -> str:
    """Returns the current time in the specified timezone."""
    # pytz timezone handling
```

## How to Run

### Prerequisites

- Python 3.8+
- Required packages: `agents`, `chainlit`, `python-dotenv`, `decouple`, `requests`, `pytz`

### Environment Variables

Create a `.env` file with:

```
GEMINI_API_KEY=your_gemini_api_key
GEMINI_BASE_URL=your_gemini_base_url
WEATHER_API_KEY=your_openweathermap_api_key
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

1. ✅ Math: "What is 2 + 2?" → Agent uses add tool
2. ✅ Weather: "What's the weather in New York?" → Agent uses weather tool
3. ✅ Time: "What time is it in Tokyo?" → Agent uses time tool
4. ✅ Combined: "What's 5+3 and the weather in London?" → Agent uses multiple tools
5. ✅ Invalid queries → Agent responds appropriately
6. ✅ Mixed requests → Agent handles multiple tool types

## Learning Objectives

- Multi-tool agent configuration
- Tool organization and modularity
- Agent decision-making with multiple tools
- Tool selection based on user intent
- Complex query handling

## File Structure

```
Assignment_04/
├── main.py              # Main application with multi-tool agent
├── tools/
│   ├── addition_tool.py      # Math operations
│   ├── weather_api_tool.py   # Weather API integration
│   └── datetime_tool.py      # Time zone handling
├── pyproject.toml       # Project dependencies
├── README.md            # This documentation
└── chainlit.md          # Chainlit welcome screen
```

## Key Concepts Demonstrated

### Multi-Tool Integration

- **Purpose:** Single agent handling diverse tasks
- **Implementation:** Multiple tools registered with one agent
- **Benefits:** Versatile assistance, reduced complexity

### Tool Organization

- **Modular Structure:** Tools organized in separate files
- **Clean Imports:** Clear separation of concerns
- **Maintainability:** Easy to add/remove/modify tools

### Agent Decision Making

- **Tool Selection:** Agent chooses appropriate tool based on query
- **Context Understanding:** Natural language processing for intent
- **Response Generation:** Contextual responses with tool results

## Tool Capabilities

### Math Operations

- Addition of any two numbers
- Decimal and integer support
- Clear result presentation

### Weather Information

- Real-time temperature data
- Worldwide city coverage
- Error handling for invalid cities

### Time Zone Support

- Current time in any timezone
- Standard timezone format support
- Error handling for invalid timezones

## Next Steps

This multi-tool agent demonstrates the power of combining multiple capabilities. The next assignment will build on this by adding advanced features like handoffs, guardrails, and agent specialization.
