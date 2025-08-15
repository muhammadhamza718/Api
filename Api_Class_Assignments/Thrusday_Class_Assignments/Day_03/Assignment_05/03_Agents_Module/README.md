# 03_Agents_Module - Agent Modularity 🧩

## Overview

This sub-project demonstrates modular agent architecture and organization. It showcases how to build scalable agent systems using component-based design patterns and modular structures.

## Features Implemented

### 1. Modular Agent Architecture

- **Location:** `main.py`
- **Feature:** Component-based agent design
- **Purpose:** Scalable and maintainable agent system architecture

### 2. Agent Modules

- **Location:** Modular agent components
- **Feature:** Reusable agent modules
- **Purpose:** Building complex agents from simple components

### 3. Component Organization

- **Location:** Organized agent structure
- **Feature:** Clean separation of agent components
- **Purpose:** Easy maintenance and extension of agent capabilities

## Technical Implementation

### Modular Agent Structure

```python
# Base agent module
class BaseAgentModule:
    def __init__(self, name: str, model: Any):
        self.name = name
        self.model = model
        self.tools = []
        self.hooks = []

# Specialized agent modules
class MathAgentModule(BaseAgentModule):
    def __init__(self, model: Any):
        super().__init__("Math Agent", model)
        self.tools = [add_numbers]
        self.instructions = "Handle mathematical operations"

class WeatherAgentModule(BaseAgentModule):
    def __init__(self, model: Any):
        super().__init__("Weather Agent", model)
        self.tools = [get_weather]
        self.instructions = "Provide weather information"
```

### Agent Composition

```python
# Compose agents from modules
def create_composite_agent(modules: List[BaseAgentModule]) -> Agent:
    """Create a composite agent from multiple modules."""
    all_tools = []
    all_instructions = []

    for module in modules:
        all_tools.extend(module.tools)
        all_instructions.append(module.instructions)

    return Agent(
        name="Composite Agent",
        instructions="\n".join(all_instructions),
        model=gemini_model,
        tools=all_tools
    )
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

1. ✅ Modular agent composition
2. ✅ Component-based agent building
3. ✅ Reusable agent modules
4. ✅ Scalable agent architecture
5. ✅ Module interaction and coordination
6. ✅ Dynamic agent composition

## Learning Objectives

- Modular agent architecture design
- Component-based agent building
- Scalable agent system patterns
- Reusable agent components
- Agent composition techniques

## Key Concepts Demonstrated

### Modular Architecture

- **Component Design:** Building agents from reusable components
- **Separation of Concerns:** Clear boundaries between agent modules
- **Reusability:** Modules can be used across different agents
- **Maintainability:** Easy to update and extend individual modules

### Agent Composition

- **Dynamic Composition:** Building agents at runtime
- **Module Integration:** Combining multiple modules into single agents
- **Tool Aggregation:** Collecting tools from multiple modules
- **Instruction Combination:** Merging instructions from different modules

### Scalability Patterns

- **Horizontal Scaling:** Adding new modules to existing agents
- **Vertical Scaling:** Enhancing individual modules
- **Modular Growth:** Expanding agent capabilities incrementally
- **Component Isolation:** Independent module development and testing

## File Structure

```
03_Agents_Module/
├── main.py              # Main application with modular agents
├── tools/
│   ├── addition_tool.py      # Math operations
│   ├── weather_api_tool.py   # Weather API integration
│   └── datetime_tool.py      # Time zone handling
├── pyproject.toml       # Project dependencies
├── README.md            # This documentation
└── chainlit.md          # Chainlit welcome screen
```

## Advanced Features

### Module Management

- **Module Registry:** Central registry for available modules
- **Dependency Management:** Handling module dependencies
- **Version Control:** Module versioning and compatibility
- **Configuration Management:** Module-specific configurations

### Dynamic Composition

- **Runtime Assembly:** Building agents dynamically
- **Configuration-Driven:** Agent composition from configuration
- **Plugin Architecture:** Extensible module system
- **Hot Swapping:** Replacing modules without restart

## Next Steps

This modular agent architecture demonstrates scalable design patterns. The next sub-projects will explore agent context management, reference handling, and model optimization techniques.

