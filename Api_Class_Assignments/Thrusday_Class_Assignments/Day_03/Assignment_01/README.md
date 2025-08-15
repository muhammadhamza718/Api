# Day 03 Assignment 01 - Basic FAQ Agent 🤖

## Overview

This assignment demonstrates the creation of a basic FAQ chatbot using the OpenAI Agents SDK and Chainlit. The agent is designed to answer predefined questions about itself and provide helpful information.

## Features Implemented

### 1. Basic Agent Creation

- **Location:** `main.py`
- **Feature:** Simple FAQ agent with predefined responses
- **Purpose:** Demonstrates basic agent setup and configuration

### 2. Chainlit Integration

- **Location:** `main.py`
- **Feature:** Web-based chat interface using Chainlit
- **Purpose:** Provides user-friendly interface for interacting with the agent

### 3. Message History Management

- **Location:** `main.py`
- **Feature:** Session-based message history tracking
- **Purpose:** Maintains conversation context across interactions

## Predefined FAQ Questions

The agent can answer these specific questions:

1. **What is your name?** - Introduces the agent as FAQBot
2. **What can you do?** - Explains the agent's capabilities
3. **Who created you?** - Mentions the student developer
4. **Where are you from?** - Explains the digital nature
5. **How can I contact support?** - Provides support information

## Technical Implementation

### Agent Configuration

```python
faq_agent = Agent(
    name="FAQBot",
    instructions="...",  # Predefined FAQ responses
    model=gemini_model,
)
```

### Chainlit Event Handlers

- `@cl.on_chat_start`: Initializes chat session
- `@cl.on_message`: Handles incoming messages and agent responses

### Message History

- Stores conversation history in user session
- Maintains context for better user experience

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

1. ✅ Ask "What is your name?" → Agent responds with FAQBot introduction
2. ✅ Ask "What can you do?" → Agent explains capabilities
3. ✅ Ask "Who created you?" → Agent mentions student developer
4. ✅ Ask "Where are you from?" → Agent explains digital nature
5. ✅ Ask "How can I contact support?" → Agent provides support info
6. ✅ Ask unrelated questions → Agent politely redirects to FAQs

## Learning Objectives

- Basic agent creation and configuration
- Chainlit integration for web interface
- Session management and message history
- Predefined response handling
- Error handling and graceful responses

## File Structure

```
Assignment_01/
├── main.py          # Main application with FAQ agent
├── pyproject.toml   # Project dependencies
├── README.md        # This documentation
└── chainlit.md      # Chainlit welcome screen
```

## Next Steps

This basic FAQ agent serves as a foundation for more complex agents with tools, handoffs, and advanced features demonstrated in subsequent assignments.
