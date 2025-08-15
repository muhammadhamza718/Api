# 04_Agents_Reference - Agent References and Context 🔗

## Overview

This sub-project demonstrates agent context management and reference handling. It showcases how agents can maintain context, handle references, and manage state across interactions.

## Features Implemented

### 1. Context Management

- **Location:** `main.py`
- **Feature:** Advanced context handling and state management
- **Purpose:** Maintaining conversation context and user state

### 2. Agent References

- **Location:** `main.py`
- **Feature:** Reference handling and context awareness
- **Purpose:** Agents that can reference and maintain context

### 3. State Persistence

- **Location:** Context management system
- **Feature:** Persistent state across interactions
- **Purpose:** Maintaining conversation history and user preferences

## Technical Implementation

### Context Management System

```python
@dataclass
class UserContext:
    user_id: str
    session_id: str
    conversation_history: List[Dict[str, str]]
    user_preferences: Dict[str, Any]
    current_topic: Optional[str] = None

    def add_message(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_context_summary(self) -> str:
        """Get summary of conversation context."""
        return f"User {self.user_id} has {len(self.conversation_history)} messages in history"
```

### Reference-Aware Agent

```python
class ContextAwareAgent(Agent):
    def __init__(self, name: str, model: Any, context_manager: ContextManager):
        super().__init__(name=name, model=model)
        self.context_manager = context_manager

    async def process_with_context(self, message: str, user_context: UserContext) -> str:
        """Process message with full context awareness."""
        # Add message to context
        user_context.add_message("user", message)

        # Get relevant context
        context_summary = self.context_manager.get_relevant_context(user_context, message)

        # Process with context
        response = await self.generate_response(message, context_summary)

        # Update context with response
        user_context.add_message("assistant", response)

        return response
```

### Context Manager

```python
class ContextManager:
    def __init__(self):
        self.contexts: Dict[str, UserContext] = {}

    def get_or_create_context(self, user_id: str, session_id: str) -> UserContext:
        """Get existing context or create new one."""
        key = f"{user_id}_{session_id}"
        if key not in self.contexts:
            self.contexts[key] = UserContext(
                user_id=user_id,
                session_id=session_id,
                conversation_history=[],
                user_preferences={}
            )
        return self.contexts[key]

    def get_relevant_context(self, context: UserContext, message: str) -> str:
        """Extract relevant context for current message."""
        # Analyze message and extract relevant history
        relevant_messages = self.analyze_relevance(context.conversation_history, message)
        return self.format_context(relevant_messages)
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

1. ✅ Context persistence across interactions
2. ✅ Reference handling in conversations
3. ✅ State management and updates
4. ✅ Context-aware responses
5. ✅ Conversation history tracking
6. ✅ User preference management

## Learning Objectives

- Context management in agents
- Reference handling and state persistence
- Conversation history tracking
- User preference management
- Context-aware response generation

## Key Concepts Demonstrated

### Context Management

- **State Persistence:** Maintaining context across interactions
- **History Tracking:** Recording conversation history
- **Context Analysis:** Extracting relevant context for responses
- **State Updates:** Updating context based on interactions

### Reference Handling

- **Context References:** Agents referencing previous interactions
- **State Awareness:** Agents aware of current conversation state
- **Memory Management:** Efficient context storage and retrieval
- **Context Relevance:** Determining relevant context for responses

### Advanced Context Features

- **Context Summarization:** Summarizing long conversation histories
- **Context Filtering:** Filtering relevant context for specific queries
- **Context Compression:** Efficient context storage
- **Context Expiration:** Managing context lifecycle

## File Structure

```
04_Agents_Reference/
├── main.py              # Main application with context-aware agents
├── tools/
│   ├── addition_tool.py      # Math operations
│   ├── weather_api_tool.py   # Weather API integration
│   └── datetime_tool.py      # Time zone handling
├── pyproject.toml       # Project dependencies
├── README.md            # This documentation
└── chainlit.md          # Chainlit welcome screen
```

## Advanced Features

### Context Intelligence

- **Semantic Analysis:** Understanding context relevance
- **Context Clustering:** Grouping related context elements
- **Context Prediction:** Predicting future context needs
- **Context Optimization:** Optimizing context for performance

### Reference Resolution

- **Entity Resolution:** Resolving references to entities
- **Pronoun Resolution:** Understanding pronoun references
- **Context Linking:** Linking related context elements
- **Reference Tracking:** Tracking reference chains

## Next Steps

This context management system demonstrates sophisticated state handling. The final sub-project will explore model optimization and configuration techniques.

