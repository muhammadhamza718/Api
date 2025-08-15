from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import chainlit as cl
from dotenv import load_dotenv
from decouple import config
# Load environment variables (OPENAI_API_KEY)
load_dotenv()
set_tracing_disabled(True)

key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")

gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",
    openai_client=gemini_client,
)

# Define the math function as a tool
@function_tool
def add(a: float, b: float) -> float:
    """Adds two numbers and returns the result."""
    return a + b

# Define the Math Agent with the tool
math_agent = Agent(
    name="MathBot",
    instructions="You are a helpful math assistant. Use the provided tools to perform calculations when needed.",
    model=gemini_model,
    tools=[add]
)

# Terminal-based testing for the FAQ agent
# Result = Runner.run_sync(math_agent, "What is 2 + 2?")
# print(Result.final_output)

@cl.on_chat_start
async def start_chat():
    # Initialize user session with system message
    cl.user_session.set("message_history", [{"role": "system", "content": math_agent.instructions}])

# Chainlit event handler for incoming messages
@cl.on_message
async def main(message: cl.Message):
    # Get user input
    user_input = message.content

    # Add user input to message history
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": user_input})

    # Run the agent with the user input
    result = Runner.run_sync(math_agent, user_input)

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