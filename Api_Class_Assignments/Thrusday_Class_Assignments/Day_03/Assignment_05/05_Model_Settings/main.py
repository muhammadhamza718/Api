# agent_using_gemini.py
import asyncio
from dataclasses import dataclass
import uuid
from dotenv import load_dotenv
from decouple import config

# Agents SDK imports
from agents import (
    Agent,
    Runner,
    ModelSettings,
    OpenAIChatCompletionsModel,  # model adapter used by the SDK
    AsyncOpenAI,  # async client wrapper (uses api_key + base_url)
    set_tracing_disabled,
)

import chainlit as cl

# Your tool functions (example modules)
from tools.weather_api_tool import get_weather
from tools.datetime_tool import get_time
from tools.addition_tool import add_numbers

# Load .env
load_dotenv()

# disabling tool tracing
set_tracing_disabled("true")

# Read Gemini credentials from environment
GEMINI_API_KEY = config("GEMINI_API_KEY")
GEMINI_BASE_URL = config("GEMINI_BASE_URL")  # e.g., "https://api.gemini.example" or appropriate endpoint

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")

# Create the async Gemini client the SDK expects
gemini_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_BASE_URL)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=gemini_client,
)

# Configure ModelSettings for Gemini (using only supported parameters)
model_settings = ModelSettings(
    temperature=0.7,        # Controls randomness (0.0-2.0)
    top_p=0.9,             # Nucleus sampling (0.0-1.0)
    max_tokens=1000,       # Maximum tokens to generate
    tool_choice="auto",    # Let model decide when to use tools
    # Note: frequency_penalty and presence_penalty are NOT supported by Gemini
)

# Example: Minimal context object passed to Runner.run
@dataclass
class UserContext:
    user_id: str
    locale: str

# Build the agent
agent = Agent[UserContext](
    name="GeminiToolAgent",
    instructions="You are a helpful agent. When appropriate use the tools provided to answer user queries.",
    model=gemini_model,
    tools=[get_weather, get_time, add_numbers],
    model_settings=model_settings,
)

# Terminal-based Testing of the Agent
# if __name__ == "__main__":
#     async def main():
#         runner = Runner()
#         context = UserContext(user_id="u123", locale="en-US")
#         try:
#             result = await runner.run(agent, "What's the weather in Lahore and whats the time in the America/new_york timezone?", context=context)
#             print("Agent result:", result.final_output or "No response from the agent")
#         except Exception as e:
#             # Basic error handling; log and re-raise or adapt for production usage
#             print("Error running agent:", e)

#     asyncio.run(main())


# Create a global runner instance
runner = Runner()

@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    
    await cl.Message(
        content="Hello! I'm your Gemini-powered assistant. I can help you with:\n"
                "🌤️ Weather information for any city\n"
                "🕐 Current time in any timezone\n"
                "➕ Mathematical calculations\n"
                "Ask me anything!"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    try:
        # Get session ID from user session or generate a new one
        session_id = cl.user_session.get("session_id") or str(uuid.uuid4())
        
        # Create user context
        context = UserContext(user_id=session_id, locale="en-US")
        
        # Show typing indicator
        await cl.Message(content="Thinking...").send()
        
        # Run the agent using the global runner instance
        result = await runner.run(agent, message.content, context=context)
        
        # Send the response
        response_content = result.final_output or "I couldn't generate a response. Please try again."
        await cl.Message(content=response_content).send()
        
    except Exception as e:
        # Handle errors gracefully
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()
        print(f"Error in main: {e}")