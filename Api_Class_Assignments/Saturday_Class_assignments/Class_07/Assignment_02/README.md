# Hotel Assistant with Input Guardrails

## Overview

This project implements an intelligent hotel booking assistant with input guardrails using OpenAI's Agent SDK. The system provides hotel information for specific hotels while blocking off-topic queries through intelligent input validation.

## Features

### 🏨 Hotel Information System

- **Grand Palace Hotel**: Luxury accommodation in Karachi, Pakistan
- **Sea View Hotel**: Beachfront hotel in Karachi
- Detailed information including location, room types, pricing, and contact details

### ��️ Input Guardrails

- **Query Classification**: Automatically detects if user queries are related to the available hotels
- **Off-topic Filtering**: Blocks queries unrelated to hotel services (e.g., weather, politics, etc.)
- **Intelligent Response**: Provides appropriate responses for both valid and invalid queries

### 🤖 AI-Powered Assistant

- Built with Gemini 2.5 Pro model
- Dynamic instruction generation
- Structured output validation using Pydantic models

## Project Structure

```
Assignment_02/
├── main.py              # Main application with hotel assistant and guardrails
├── README.md            # This documentation file
├── chainlit.md          # Chainlit integration guide
├── .env                 # Environment variables (not tracked in git)
└── .gitignore           # Git ignore rules
```

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Class_Assignments/Saturday_Class_assignments/Class_07/Assignment_02
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file with:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
   ```

## Usage

### Running the Application

```bash
uv run main.py
```

### Available Hotels

| Hotel              | Location           | Room Types                    | Price            | Contact         |
| ------------------ | ------------------ | ----------------------------- | ---------------- | --------------- |
| **Grand Palace**   | Karachi, Pakistan  | Luxury suites, standard rooms | Rs. 15,000/night | +92-300-1234567 |
| **Sea View Hotel** | Karachi Beachfront | Sea view deluxe rooms         | Rs. 10,000/night | +92-300-7654321 |

### Example Queries

#### ✅ Valid Queries (Will be processed)

- "Grand Palace details?"
- "Tell me about Sea View Hotel"
- "What rooms are available at Grand Palace?"
- "How much does Sea View Hotel cost?"

#### ❌ Invalid Queries (Will be blocked)

- "What's the weather like?"
- "Tell me about politics"
- "How to cook pasta?"
- "What's the latest news?"

## Technical Implementation

### Core Components

1. **Hotel Assistant Agent**

   - Primary agent for handling hotel-related queries
   - Dynamic instructions based on available hotels
   - Provides detailed hotel information

2. **Guardrail Agent**

   - Classifies user queries as hotel-related or off-topic
   - Uses structured output with Pydantic validation
   - Triggers tripwire for non-hotel queries

3. **Input Guardrail Function**
   - Decorated with `@input_guardrail`
   - Processes queries through guardrail agent
   - Blocks execution for off-topic queries

### Data Models

```python
class MyDataType(BaseModel):
    is_query_about_Grand_Palace_Hotel_or_Sea_View_Hotel: bool
    reason: str
```

### Error Handling

The application uses `InputGuardrailTripwireTriggered` exception to handle blocked queries gracefully.

## Testing

### Test Cases

1. **Hotel-related queries** should return hotel information
2. **Off-topic queries** should trigger the guardrail and be blocked
3. **Edge cases** should be handled appropriately

### Running Tests

```bash
# Test with hotel query
uv run main.py
# Input: "Grand Palace details?"

# Test with off-topic query
uv run main.py
# Input: "What's the weather?"
```

## Dependencies

- `agents`: OpenAI Agent SDK for AI agent functionality
- `python-decouple`: Environment variable management
- `python-dotenv`: Environment file loading
- `pydantic`: Data validation and settings management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Agentic AI c
