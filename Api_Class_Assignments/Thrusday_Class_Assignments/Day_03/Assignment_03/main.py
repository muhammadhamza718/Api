from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
import chainlit as cl
from dotenv import load_dotenv
from decouple import config
from weather_api import get_weather

# Load environment variables (GEMINI_API_KEY, GEMINI_BASE_URL, WEATHER_API_KEY)
load_dotenv()
set_tracing_disabled(True)

# Get the GEMINI API key and base URL from environment variables
key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")

# Create an asynchronous OpenAI client for GEMINI
gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

# Define the GEMINI model
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",
    openai_client=gemini_client,
)

weather_agent = Agent(
    name="WeatherBot",
    instructions="You are a weather assistant. Use the `get_weather` tool to answer weather queries.",
    model=gemini_model,
    tools=[function_tool(get_weather)]  # Register the imported function as a tool
)

# Terminal-based testing for the FAQ agent
# Result = Runner.run_sync(weather_agent, "What is the weather of the karachi?")
# print(Result.final_output)

@cl.on_chat_start
async def start_chat():
    cl.user_session.set("message_history", [{"role": "system", "content": weather_agent.instructions}])

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": user_input})

    result = Runner.run_sync(weather_agent, user_input)
    response = result.final_output
    message_history.append({"role": "assistant", "content": response})

    msg = cl.Message(content=response)
    await msg.send()