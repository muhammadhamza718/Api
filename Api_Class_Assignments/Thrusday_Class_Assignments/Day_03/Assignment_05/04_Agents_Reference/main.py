import chainlit as cl
from dotenv import load_dotenv
from decouple import config
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, AgentHooks, RunContextWrapper
from tools.weather_api_tool import get_weather
from tools.datetime_tool import get_time
from tools.addition_tool import add
import asyncio
from typing import Any

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

class MyAgentHooks(AgentHooks):
    def __init__(self):
        self.count = 0

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        """Called before the agent is invoked. Called each time the running agent is changed to this
        agent."""
        self.count = 10
        print(f"\n\n agent start : {agent.name}")

    async def on_end(
        self,
        context: RunContextWrapper,
        agent: Agent,
        output: Any,
    ) -> None:
        """Called when the agent produces a final output."""
        print(f"\n\n count : {self.count}")
        print(f"\n\n agent end : {agent.name}")
        print(f"\n\n agent output : {output}")

# 6. Sub-agent for weather
weather_agent = Agent(
    name="WeatherSpecialist",
    instructions="You are specialized in answering only weather questions.",
    model=gemini_model,
    hooks=MyAgentHooks(),
    tools=[get_weather],
)

# 5. Main agent
main_agent = Agent(
    name="UtilityAgent",
    instructions="You are a helpful assistant that can provide weather, time, and math results.",
    model=gemini_model,
    tools=[get_time, add],
    handoffs=[weather_agent],  # Will add later
    hooks=MyAgentHooks(),
)

# 7. Demonstrate clone()
agent_clone = main_agent.clone(name="UtilityAgentClone")

# Terminal-based testing for the main agent
if __name__ == "__main__":
    async def test_agent():
        runner = Runner()
        result = await runner.run(
            starting_agent=main_agent,
            input="what the weather in the Asia/karachi rn?"
        )
        print(result.final_output)
    
    asyncio.run(test_agent())

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