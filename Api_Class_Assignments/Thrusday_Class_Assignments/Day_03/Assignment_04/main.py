from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
import chainlit as cl
from dotenv import load_dotenv
from decouple import config
from tools.weather_api_tool import get_weather
from tools.datetime_tool import get_time
from tools.addition_tool import add

# Load environment variables
load_dotenv()
set_tracing_disabled(True)

# Get the GEMINI API key, base URL, and OpenWeatherMap API key
key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")

# Create an asynchronous OpenAI client for GEMINI
gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

# Define the GEMINI model
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",
    openai_client=gemini_client,
)

multi_tool_agent = Agent(
    name="MultiToolBot",
    instructions="""
You are a versatile assistant that can handle multiple tasks:
- For math questions like 'What is X + Y?', use the `add` tool to calculate the sum.
- For weather queries like 'What's the weather in [city]?', use the `get_weather` tool to fetch the current temperature.
- For time queries like 'What time is it in [timezone]?', use the `get_time` tool to provide the current time.
If the user's request doesn't match these tasks, respond politely that you can only handle math, weather, or time queries.
""",
    model=gemini_model,
    tools=[add, get_weather, get_time]
)

# Terminal-based testing for the multi-tool agent
# Result = Runner.run_sync(multi_tool_agent, "What is 2 + 2?, What's the weather in New York?, What time is it in New York?")
# print(Result.final_output)

# Chainlit event handler for chat start
@cl.on_chat_start
async def start_chat():
    # Initialize user session with system message
    cl.user_session.set("message_history", [{"role": "system", "content": multi_tool_agent.instructions}])

# Chainlit event handler for incoming messages
@cl.on_message
async def main(message: cl.Message):
    # Get user input
    user_input = message.content

    # Add user input to message history
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": user_input})

    # Run the agent with the user input
    result = Runner.run_sync(multi_tool_agent, user_input)

    # Get the agent's response
    response = result.final_output

    # Update message history with the agent's response
    message_history.append({"role": "assistant", "content": response})

    # Stream the response to the Chainlit UI
    msg = cl.Message(content=response)
    await msg.send()

if __name__ == "__main__":
    # Chainlit will run the application
    pass

