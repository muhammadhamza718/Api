# 02_Tools - Advanced Tool Configuration 🛠️

## Overview

This sub-project demonstrates advanced tool configuration and organization. It showcases how to build sophisticated tools with enhanced features, error handling, and modular design patterns.

## Features Implemented

### 1. Advanced Tool Organization

- **Location:** `tools/` directory
- **Feature:** Modular tool structure with enhanced capabilities
- **Purpose:** Clean separation of concerns and maintainable tool architecture

### 2. Enhanced Tool Features

- **Error Handling:** Comprehensive error management in tools
- **Type Safety:** Advanced type annotations and validation
- **Documentation:** Detailed tool documentation and examples
- **Modularity:** Reusable tool components

### 3. Tool Configuration

- **Location:** `main.py`
- **Feature:** Advanced tool registration and configuration
- **Purpose:** Demonstrates sophisticated tool management

## Technical Implementation

### Tool Structure

```
tools/
├── addition_tool.py      # Enhanced math operations
├── weather_api_tool.py   # Advanced weather API integration
└── datetime_tool.py      # Sophisticated time handling
```

### Enhanced Tool Examples

#### Advanced Addition Tool

```python
@function_tool
def add_numbers(a: float, b: float) -> float:
    """
    Adds two numbers and returns the result.

    Args:
        a: First number to add
        b: Second number to add

    Returns:
        Sum of the two numbers

    Raises:
        ValueError: If inputs are not valid numbers
    """
    try:
        return float(a) + float(b)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid input: {e}")
```

#### Advanced Weather Tool

```python
@function_tool
def get_weather_advanced(city: str, units: str = "metric") -> str:
    """
    Fetches comprehensive weather data for a given city.

    Args:
        city: Name of the city
        units: Temperature units (metric/imperial)

    Returns:
        Detailed weather information
    """
    # Enhanced API integration with error handling
```

#### Advanced Time Tool

```python
@function_tool
def get_time_advanced(timezone: str, format: str = "12h") -> str:
    """
    Returns the current time in the specified timezone with formatting options.

    Args:
        timezone: Timezone identifier
        format: Time format (12h/24h)

    Returns:
        Formatted current time
    """
    # Advanced timezone handling with formatting
```

## How to Run

### Prerequisites

- Python 3.8+
- Required packages: `agents`, `chainlit`, `python-dotenv`, `decouple`, `requests`, `pytz`

### Environment Variables

Create a `.env` file:

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

# Or run terminal version
python main.py
```

## Test Scenarios

1. ✅ Advanced math operations with error handling
2. ✅ Enhanced weather queries with multiple parameters
3. ✅ Sophisticated time handling with formatting options
4. ✅ Tool error recovery and graceful degradation
5. ✅ Complex tool interactions and combinations
6. ✅ Tool performance monitoring and optimization

## Learning Objectives

- Advanced tool design patterns
- Error handling in tools
- Tool modularity and reusability
- Type safety and validation
- Tool documentation and testing

## Key Concepts Demonstrated

### Advanced Tool Design

- **Modularity:** Tools organized in separate modules
- **Reusability:** Tools can be used across different agents
- **Maintainability:** Easy to update and extend tools
- **Documentation:** Comprehensive tool documentation

### Error Handling

- **Input Validation:** Robust input checking
- **Exception Handling:** Graceful error recovery
- **User Feedback:** Clear error messages
- **Fallback Mechanisms:** Alternative approaches when tools fail

### Type Safety

- **Type Annotations:** Proper type hints throughout
- **Validation:** Runtime type checking
- **Documentation:** Clear parameter and return type documentation

## File Structure

```
02_Tools/
├── main.py              # Main application with advanced tools
├── tools/
│   ├── addition_tool.py      # Enhanced math operations
│   ├── weather_api_tool.py   # Advanced weather API integration
│   └── datetime_tool.py      # Sophisticated time handling
├── pyproject.toml       # Project dependencies
├── README.md            # This documentation
└── chainlit.md          # Chainlit welcome screen
```

## Advanced Features

### Tool Configuration

- **Parameter Validation:** Advanced input validation
- **Default Values:** Sensible defaults for optional parameters
- **Documentation:** Comprehensive docstrings and examples
- **Testing:** Unit tests for tool functionality

### Performance Optimization

- **Caching:** Tool result caching for repeated queries
- **Async Support:** Asynchronous tool execution
- **Resource Management:** Efficient resource usage
- **Monitoring:** Tool performance tracking

## Next Steps

This advanced tool configuration demonstrates sophisticated tool design patterns. The next sub-projects will explore modular agent architectures, context management, and model optimization techniques.
