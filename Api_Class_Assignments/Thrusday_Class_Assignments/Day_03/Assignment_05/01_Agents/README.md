# 01_Agents - Basic Agent Handoffs 🤝

## Overview

This sub-project demonstrates agent-to-agent handoffs, where one agent can pass control to specialized agents based on the type of request. It showcases how agents can delegate tasks to more specialized agents for better performance and accuracy.

## Features Implemented

### 1. Agent Handoffs

- **Location:** `main.py`
- **Feature:** `handoffs=[math_agent, time_agent, calendar_agent]`
- **Purpose:** Allows main agent to delegate to specialized agents

### 2. Specialized Agents

- **Math Agent:** Handles mathematical operations
- **Time Agent:** Provides time-related information
- **Calendar Agent:** Manages calendar events with structured output

### 3. Agent Hooks

- **Location:** `main.py`
- **Feature:** `CustomAgentHooks` class
- **Purpose:** Lifecycle event handling and logging

### 4. Context Management

- **Location:** `main.py`
- **Feature:** `UserContext` dataclass
- **Purpose:** User-specific context and preferences

## Technical Implementation

### Main Agent with Handoffs

```python
main_agent = Agent[UserContext](
    name="Assistant Agent",
    instructions=dynamic_instructions,
    model=gemini_model,
    tools=[get_weather, get_time, add],
    handoffs=[math_agent, time_agent, calendar_agent],  # Handoff configuration
    hooks=CustomAgentHooks(),
    model_settings=main_model_settings,
)
```

### Specialized Agents

#### Math Agent

```python
math_agent = Agent[UserContext](
    name="Math Agent",
    instructions="Handle mathematical queries, such as addition.",
    model=gemini_model,
    tools=[add],
    model_settings=math_model_settings,
)
```

#### Time Agent

```python
time_agent = Agent[UserContext](
    name="Time Agent",
    instructions="Provide time-related information using the get_time tool.",
    model=gemini_model,
    tools=[get_time],
    model_settings=time_model_settings,
)
```

#### Calendar Agent

```python
calendar_agent = Agent[UserContext](
    name="Calendar Agent",
    instructions="Extract calendar events from text and return structured output.",
    model=gemini_model,
    output_type=CalendarEvent,  # Structured output
)
```

### Agent Hooks

```python
class CustomAgentHooks(AgentHooks):
    async def on_agent_start(self, agent, input_data):
        print(f"Agent {agent.name} started with input: {input_data}")

    async def on_agent_complete(self, agent, output):
        print(f"Agent {agent.name} completed with output: {output}")
```

### Context Management

```python
@dataclass
class UserContext:
    uid: str
    is_pro_user: bool
    name: Optional[str] = None

    async def fetch_preferences(self) -> dict:
        return {"preferred_timezone": "UTC", "language": "English"}
```

## How to Run

### Prerequisites

- Python 3.8+
- Required packages: `agents`, `chainlit`, `python-dotenv`, `decouple`, `requests`, `pytz`, `pydantic`

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

1. ✅ Math queries → Handoff to Math Agent
2. ✅ Time queries → Handoff to Time Agent
3. ✅ Calendar events → Handoff to Calendar Agent
4. ✅ Weather queries → Main agent handles directly
5. ✅ Complex queries → Appropriate agent delegation
6. ✅ Fun queries → Special fun agent handling

## Learning Objectives

- Agent handoff implementation
- Specialized agent creation
- Agent lifecycle hooks
- Context management
- Structured output handling

## Key Concepts Demonstrated

### Handoff Mechanism

- **Purpose:** Delegate tasks to specialized agents
- **Implementation:** `handoffs` parameter in agent configuration
- **Benefits:** Better performance and accuracy for specific tasks

### Agent Specialization

- **Math Agent:** Focused on mathematical operations
- **Time Agent:** Specialized in time-related queries
- **Calendar Agent:** Structured calendar event handling

### Lifecycle Management

- **Hooks:** Track agent start and completion events
- **Logging:** Monitor agent behavior and performance
- **Debugging:** Understand agent decision-making process

## File Structure

```
01_Agents/
├── main.py          # Main application with handoff agents
├── tools/
│   ├── addition_tool.py      # Math operations
│   ├── weather_api_tool.py   # Weather API integration
│   └── datetime_tool.py      # Time zone handling
├── pyproject.toml   # Project dependencies
├── README.md        # This documentation
└── chainlit.md      # Chainlit welcome screen
```

## Next Steps

This handoff system demonstrates how to build scalable agent architectures. The next sub-projects will explore advanced tool configurations, modular architectures, and model optimization techniques.
