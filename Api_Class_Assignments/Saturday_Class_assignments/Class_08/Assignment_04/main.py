import asyncio
from typing import Dict, Any
from dataclasses import dataclass # Keep using dataclass as you said

from decouple import config
from dotenv import load_dotenv

# Import the specific utilities we now know are required
from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    set_tracing_disabled,
    Tool,
    RunContextWrapper,
)

# --- 1. SETUP ---
load_dotenv()
set_tracing_disabled(True)

try:
    key = config("GEMINI_API_KEY")
    base_url = config("GEMINI_BASE_URL")
    gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)
    gemini_model = OpenAIChatCompletionsModel(
        model="gemini-1.5-flash",
        openai_client=gemini_client,
    )
except Exception as e:
    print(f"Could not set up the model. Please check your .env file. Error: {e}")
    exit()

# --- 2. DATA ---
SIMULATED_ORDERS_DB = {
    "12345": {"status": "Shipped"},
    "67890": {"status": "Processing"},
}

# --- 3. FUNCTION TOOLS ---

# Tool #1: Get Order Status
@function_tool
def get_order_status(order_id: str) -> str:
    """Fetches the status of an order by its ID."""
    print(f"🔧 Tool called: get_order_status with ID: {order_id}")
    if order_id in SIMULATED_ORDERS_DB:
        status = SIMULATED_ORDERS_DB[order_id]['status']
        return f"The status for order {order_id} is: {status}."
    else:
        return f"I could not find an order with the ID {order_id}."

# --- 4. AGENT DEFINITIONS ---

# Agent #1: The Human Escalation Point
human_agent = Agent(
    name="HumanSupportAgent",
    instructions="You are a human support agent. A customer has been escalated to you. Greet them and ask how you can help.",
    model=gemini_model,
)

# Tool #2: The Handoff Tool
# Keep HandoffInput as a dataclass, as you correctly identified.
@dataclass
class HandoffInput:
    message: str
    
async def invoke_handoff(context: RunContextWrapper, kwargs: Dict[str, Any]) -> str:
    print("🤝 Handoff invoked. Running the human agent...")
    result = await Runner.run(
        starting_agent=human_agent,
        input=kwargs.get("message", "The user was transferred."),
        max_turns=2,
    )
    return result.final_output

# Agent #2: The Main Customer Support Bot
bot_agent = Agent(
    name="SupportBot",
    instructions=(
        "You are a customer support bot.\n"
        "1. Answer FAQs (Return policy is 30 days).\n"
        "2. Use `get_order_status` to check order status.\n"
        "3. If the user wants a 'refund' or 'complaint', you MUST handoff to a human support agent.\n"
    ),
    model=gemini_model,
    tools=[get_order_status],
    handoffs=[human_agent],
)

# --- 5. MAIN EXECUTION LOGIC ---
async def main():
    print("🤖 Simple Customer Support Bot is ready!")
    print("Type 'exit' to end.")

    while True:
        query = input("\n👤 You: ")
        if query.lower() in ["exit", "quit"]:
            print("🤖 Bot: Goodbye!")
            break

        # Simple guardrail check
        offensive_words = ["stupid", "useless", "terrible"]
        if any(word in query.lower() for word in offensive_words):
            print("🛡️ Guardrail triggered.")
            print("🤖 Assistant: Please be respectful. How can I help you?")
            continue

        try:
            result = await Runner.run(
                starting_agent=bot_agent,
                input=query,
                max_turns=5,
            )
            print(f"🤖 Assistant: {result.final_output}")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
