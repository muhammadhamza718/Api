import chainlit as cl
from dotenv import load_dotenv
from decouple import config
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, AgentHooks, set_tracing_disabled, ModelSettings
from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Optional
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

# Custom context for dependency injection
@dataclass
class UserContext:
    uid: str
    is_pro_user: bool
    name: Optional[str] = None

    async def fetch_preferences(self) -> dict:
        return {"preferred_timezone": "UTC", "language": "English"}

# Structured output type using Pydantic
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: List[str]

# Lifecycle hooks for logging
class CustomAgentHooks(AgentHooks):
    async def on_agent_start(self, agent, input_data):
        print(f"Agent {agent.name} started with input: {input_data}")

    async def on_agent_complete(self, agent, output):
        print(f"Agent {agent.name} completed with output: {output}")

# Guardrail for input validation
async def input_guardrail(context, input_data: str) -> Optional[str]:
    if len(input_data.strip()) < 3:
        return "Input is too short. Please provide a more detailed query."
    if "inappropriate" in input_data.lower():
        return "Inappropriate content detected. Please rephrase your query."
    return None

# Dynamic instructions function
def dynamic_instructions(context, agent: Agent[UserContext]) -> str:
    user_name = context.context.name if context.context and context.context.name else "User"
    return (
        f"Hello, {user_name}! I am {agent.name}, here to assist you. "
        "Ask about weather, time, math, or calendar events, and I'll help or delegate to a specialist."
    )

# Define sub-agents for handoffs
math_model_settings = ModelSettings(tool_choice="required")
math_agent = Agent[UserContext](
    name="Math Agent",
    instructions="Handle mathematical queries, such as addition.",
    model=gemini_model,
    tools=[add],
    model_settings=math_model_settings,
)

time_model_settings = ModelSettings(tool_choice="required")
time_agent = Agent[UserContext](
    name="Time Agent",
    instructions="Provide time-related information using the get_time tool.",
    model=gemini_model,
    tools=[get_time],
    model_settings=time_model_settings,
)

calendar_agent = Agent[UserContext](
    name="Calendar Agent",
    instructions="Extract calendar events from text and return structured output.",
    model=gemini_model,
    output_type=CalendarEvent,
)

# Main agent configuration
main_model_settings = ModelSettings(tool_choice="auto", temperature=0.7)
main_agent = Agent[UserContext](
    name="Assistant Agent",
    instructions=dynamic_instructions,
    model=gemini_model,
    tools=[get_weather, get_time, add],
    handoffs=[math_agent, time_agent, calendar_agent],
    hooks=CustomAgentHooks(),
    model_settings=main_model_settings,
)

# Clone the main agent with modified behavior
fun_agent = main_agent.clone(
    name="Fun Agent",
    instructions="Respond in a playful, rhyming style.",
)

# Terminal-based testing for the main agent
if __name__ == "__main__":
    user_context = UserContext(uid="user123", is_pro_user=True, name="Alice")
    runner = Runner()
    result = runner.run_sync(main_agent, "tell me the weather of the karachi?", context=user_context)
    print(result.final_output)

# Chainlit interface (replace the existing Chainlit section in main.py)
@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome! Ask about weather, time, math, or calendar events. Include 'fun' for a rhyming fun fact!").send()

@cl.on_message
async def main(message: cl.Message):
    # Create user context
    user_context = UserContext(uid="user123", is_pro_user=True, name="Alice")

    # Apply guardrail
    guardrail_result = await input_guardrail(user_context, message.content)
    if guardrail_result:
        await cl.Message(content=guardrail_result).send()
        return

    # Initialize runner
    runner = Runner()

    # Check if input contains "fun" to decide which agent to run
    if "fun" in message.content.lower():
        try:
            fun_result = await runner.run(
                starting_agent=fun_agent,  # Run fun_agent for "fun" queries
                input=message.content,
                context=user_context,
            )
            await cl.Message(content=f"Fun Agent: {fun_result.final_output}").send()
        except Exception as e:
            await cl.Message(content=f"Error from Fun Agent: {str(e)}").send()
    else:
        try:
            result = await runner.run(
                starting_agent=main_agent,  # Run main_agent for other queries
                input=message.content,
                context=user_context,
            )
            await cl.Message(content=f"Main Agent: {result.final_output}").send()
        except Exception as e:
            await cl.Message(content=f"Error from Main Agent: {str(e)}").send()