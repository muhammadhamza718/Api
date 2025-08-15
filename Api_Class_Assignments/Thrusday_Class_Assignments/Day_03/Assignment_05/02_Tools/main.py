import chainlit as cl
from dotenv import load_dotenv
from decouple import config
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from tools.weather_api_tool import get_weather
from tools.datetime_tool import get_time
from tools.addition_tool import add

# Load environment variables
load_dotenv()
set_tracing_disabled(True)

# Get Gemini API key and base URL
key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")

# Create asynchronous Gemini client
gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

# Define Gemini model
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",
    openai_client=gemini_client,
)

# Main agent configuration
main_agent = Agent(
    name="Assistant Agent",
    instructions="You are a helpful assistant. Use the provided tools to answer user queries.",
    model=gemini_model,
    tools=[get_weather, get_time, add],
)

# Terminal-based testing for the main agent
if __name__ == "__main__":
    runner = Runner()
    result = runner.run_sync(main_agent, "what the time in the Asia/karachi rn?")
    print(result.final_output)

# Chainlit interface
@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome! Ask about weather, time, or math calculations.").send()

@cl.on_message
async def main(message: cl.Message):
    try:
        # Initialize runner
        runner = Runner()
        
        # Run the agent
        result = await runner.run(
            starting_agent=main_agent,
            input=message.content,
        )
        
        # Send the response
        await cl.Message(content=result.final_output).send()
        
    except Exception as e:
        await cl.Message(content=f"Error: {str(e)}").send()