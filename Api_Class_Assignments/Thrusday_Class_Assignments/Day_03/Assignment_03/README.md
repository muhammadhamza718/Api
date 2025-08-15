# Day 03 Assignment 03 - Weather Agent with External API 🌤️

## Overview

This assignment demonstrates the creation of a weather assistant agent that integrates with external APIs (OpenWeatherMap) to provide real-time weather information. The agent uses function tools to fetch weather data for any city worldwide.

## Features Implemented

### 1. External API Integration

- **Location:** `weather_api.py`
- **Feature:** OpenWeatherMap API integration for weather data
- **Purpose:** Fetches real-time temperature data for any city

### 2. Weather Function Tool

- **Location:** `main.py`
- **Feature:** `function_tool(get_weather)` registration
- **Purpose:** Converts external API function into an AI tool

### 3. Weather Agent

- **Location:** `main.py`
- **Feature:** Specialized weather assistant with API tools
- **Purpose:** Provides accurate weather information using external data

## Technical Implementation

### Weather API Function

```python
# In weather_api.py
def get_weather(city: str) -> str:
    """Fetches the current temperature for a given city using the OpenWeatherMap API."""
    # API calls to OpenWeatherMap for geocoding and weather data
    return f"The current temperature in {city} is {temp}°C."
```

### Agent Configuration with External Tool

```python
weather_agent = Agent(
    name="WeatherBot",
    instructions="You are a weather assistant. Use the `get_weather` tool to answer weather queries.",
    model=gemini_model,
    tools=[function_tool(get_weather)]  # Register external API function
)
```

### API Integration Features

- **Geocoding:** Converts city names to coordinates
- **Weather Data:** Fetches current temperature in Celsius
- **Error Handling:** Graceful handling of invalid cities or API errors
- **Type Safety:** Proper type annotations for function parameters

## How to Run

### Prerequisites

- Python 3.8+
- Required packages: `agents`, `chainlit`, `python-dotenv`, `decouple`, `requests`

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

1. ✅ Ask "What is the weather in Karachi?" → Agent fetches real weather data
2. ✅ Ask "What's the temperature in London?" → Agent provides current temperature
3. ✅ Ask "Weather in New York?" → Agent uses API to get accurate data
4. ✅ Ask "Temperature in Tokyo?" → Agent handles international cities
5. ✅ Ask invalid city → Agent provides error message
6. ✅ Ask non-weather questions → Agent responds appropriately

## Learning Objectives

- External API integration with agents
- Function tool registration for external services
- Error handling in API calls
- Real-time data fetching
- Type annotations for external functions

## File Structure

```
Assignment_03/
├── main.py          # Main application with weather agent
├── weather_api.py   # External API integration
├── pyproject.toml   # Project dependencies
├── README.md        # This documentation
└── chainlit.md      # Chainlit welcome screen
```

## Key Concepts Demonstrated

### External API Integration

- **Purpose:** Extend agent capabilities with real-world data
- **Implementation:** HTTP requests to external services
- **Benefits:** Real-time, accurate information

### Function Tool Registration

- **Import:** External functions can be imported and registered
- **Decoration:** Use `function_tool()` wrapper for external functions
- **Integration:** Seamless integration with agent workflow

### Error Handling

- **API Errors:** Graceful handling of network issues
- **Invalid Input:** User-friendly error messages
- **Fallback:** Appropriate responses when data unavailable

## API Details

### OpenWeatherMap Integration

- **Geocoding API:** Converts city names to coordinates
- **Weather API:** Fetches current weather data
- **Units:** Temperature in Celsius (metric)
- **Rate Limits:** Respects API usage limits

## Next Steps

This weather agent demonstrates external API integration. The next assignments will build on this by adding multiple tools, more complex integrations, and advanced agent features.
