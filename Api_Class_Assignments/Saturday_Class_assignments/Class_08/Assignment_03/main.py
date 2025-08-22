import json
import asyncio
import time
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from agents import (
    Agent,
    Runner,
    RunContextWrapper,
    function_tool,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
)
from decouple import config
from dataclasses import dataclass, field
from typing import Any, Dict, List

# --- Setup (No changes here) ---
load_dotenv()
set_tracing_disabled(True)

key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")
gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",  # Switched to a faster, more common model to help with rate limits
    openai_client=gemini_client,
)

# --- Context (No changes here) ---
@dataclass
class AppContext:
    """Simple context to store hotel information"""
    hotels: Dict[str, dict] = field(default_factory=dict)

# --- Tools (No changes here) ---
@function_tool
def list_hotels(ctx: RunContextWrapper[AppContext]) -> str:
    """List all available hotels in the system."""
    print("🔧 list_hotels called")
    if not ctx.context.hotels:
        return "No hotels available in the system."
    result = "Available Hotels:\n"
    for hotel in ctx.context.hotels.values():
        result += f"- {hotel['name']} in {hotel['location']} (${hotel['price']}/night, {hotel['rooms']} rooms)\n"
    return result

@function_tool
def get_hotel_details(ctx: RunContextWrapper[AppContext], hotel_name: str) -> str:
    """Get detailed information about a specific hotel by name."""
    print(f"🔧 get_hotel_details called with: {hotel_name}")
    found_hotel = next((h for n, h in ctx.context.hotels.items() if n.lower() == hotel_name.lower()), None)
    if not found_hotel:
        available = list(ctx.context.hotels.keys())
        return f"Hotel '{hotel_name}' not found. Available hotels: {', '.join(available)}"
    return f"Hotel Details:\nName: {found_hotel['name']}\nLocation: {found_hotel['location']}\nPrice: ${found_hotel['price']}/night\nRooms: {found_hotel['rooms']}"

@function_tool
def add_hotel(ctx: RunContextWrapper[AppContext], name: str, location: str, price: float, rooms: int) -> str:
    """Add a new hotel to the system."""
    print(f"🔧 add_hotel called: {name}")
    ctx.context.hotels[name.lower()] = {"name": name, "location": location, "price": price, "rooms": rooms}
    return f"Successfully added {name} in {location} with {rooms} rooms at ${price}/night"

# --- ASSIGNMENT SOLUTION: DYNAMIC INSTRUCTIONS FUNCTION ---
def generate_dynamic_instructions(ctx: RunContextWrapper[AppContext], agent: Agent[AppContext]) -> str:
    """
    Generates instructions for the agent on-the-fly, including the current list of hotels.
    """
    print("🧠 Generating dynamic instructions...")
    
    hotel_names = list(ctx.context.hotels.keys())
    
    # Base instructions
    instructions = (
        "You are a helpful and efficient hotel assistant. You MUST use tools to answer questions.\n"
        "NEVER answer from memory; always use a tool to get the most up-to-date information.\n"
    )
    
    # Dynamically add the list of known hotels to the prompt
    if hotel_names:
        instructions += (
            "\nIMPORTANT: The user might ask about one of the following hotels. "
            "Use the `get_hotel_details` tool if they mention one of these names.\n"
            f"Known Hotels: {', '.join(hotel_names)}\n"
        )
    else:
        instructions += "\nThere are currently no hotels in the system. You can add one using the `add_hotel` tool.\n"
        
    instructions += "\nRULES:\n"
    instructions += "1. To see all hotels: Use `list_hotels()`.\n"
    instructions += "2. For a specific hotel's details: Use `get_hotel_details(hotel_name=...)`.\n"
    instructions += "3. To add a new hotel: Use `add_hotel(name=..., location=..., price=..., rooms=...)`."
    
    return instructions

# --- AGENT DEFINITION ---
def build_agent() -> Agent[AppContext]:
    """Builds the agent, now using the dynamic instructions function."""
    return Agent[AppContext](
        name="Hotel Assistant",
        # ASSIGNMENT SOLUTION: Pass the function itself, not the result of calling it.
        instructions=generate_dynamic_instructions,
        model=gemini_model,
        tools=[list_hotels, get_hotel_details, add_hotel],
    )

# --- MAIN EXECUTION LOGIC ---
async def main():
    """
    Runs the Hotel Assistant in an interactive loop.
    """
    print("🏨 Starting Hotel Assistant...")
    print("Type 'exit' or 'quit' to end the session.")
    
    ctx = AppContext()
    
    # Pre-populate with sample hotels
    ctx.hotels["grand hotel"] = {"name": "Grand Hotel", "location": "NYC", "price": 200.0, "rooms": 50}
    ctx.hotels["beach resort"] = {"name": "Beach Resort", "location": "Miami", "price": 150.0, "rooms": 30}
    
    agent = build_agent()
    
    # Interactive chat loop is better for testing and avoiding rate limits
    while True:
        try:
            query = input("\n👤 You: ")
            if query.lower() in ["exit", "quit"]:
                print("🤖 Assistant: Goodbye!")
                break

            print("\n" + "="*60)
            
            result = await Runner.run(agent, query, context=ctx, max_turns=10)
            
            if result.final_output:
                print(f"🤖 Assistant: {result.final_output}")
            else:
                # This can happen if the agent only uses tools but doesn't say anything after.
                print("🤖 Assistant: Action completed.")

            print("="*60)

        except Exception as e:
            print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
