# hotel_assistant.py
from typing import Any
from agents import Agent, Runner, RunContextWrapper, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, input_guardrail,GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from decouple import config
from dotenv import load_dotenv
from pydantic import BaseModel
import chainlit as cl

load_dotenv()
set_tracing_disabled(True)

key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")

gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",
    openai_client=gemini_client,
)

# Example hotel data
hotels_data = {
    "Grand Palace": {
        "location": "Karachi, Pakistan",
        "rooms": "Luxury suites, standard rooms",
        "price": "Rs. 15,000 per night",
        "contact": "+92-300-1234567"
    },
    "Sea View Hotel": {
        "location": "Karachi Beachfront",
        "rooms": "Sea view deluxe rooms",
        "price": "Rs. 10,000 per night",
        "contact": "+92-300-7654321"
    }
}

dynamic_instructions = (
    "You are a helpful hotel booking assistant. "
    "Ask the user which hotel they want details for. "
    "If the user asks for details about a Grand Palace or Sea View they are asking about Grand Palace hotel or Sea View hotel, "
    "Available hotels: " + ", ".join(hotels_data.keys())
)

class MyDataType(BaseModel):
    is_query_about_Grand_Palace_Hotel_or_Sea_View_Hotel: bool
    reason: str

guardrial_agent = Agent(
    name="GuardrailAgent",
    instructions=(
        "You are a query classifier. Determine if the user's query is about Grand Palace Hotel or Sea View Hotel. "
        "Return is_query_about_Grand_Palace_Hotel_or_Sea_View_Hotel = true if the query mentions: "
        "- Grand Palace (hotel) "
        "- Sea View Hotel "
        "- Hotel booking, accommodation, rooms, pricing for these hotels "
        "Return is_query_about_Grand_Palace_Hotel_or_Sea_View_Hotel = false for any other topics like weather, politics, general questions, etc."
    ),
    model=gemini_model,
    output_type=MyDataType
)

@input_guardrail
async def guardrial_input_function(ctx:RunContextWrapper, agent, input):
    result = await Runner.run(guardrial_agent, input=input, context= ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_query_about_Grand_Palace_Hotel_or_Sea_View_Hotel
    )

agent = Agent(
    name="HotelAssistant",
    instructions=dynamic_instructions,
    model=gemini_model,
    input_guardrails=[guardrial_input_function]
)

# # Terminal-based testing for the hotel assistant
# async def main():
#     try:
#         msg = input("Enter your question: ")
#         res = await Runner.run(
#             starting_agent=agent, 
#             input=msg,
#         )
#         print(f"\nResponse: {res.final_output}")
#     except InputGuardrailTripwireTriggered as e:
#         print(f"Guardrail triggered: {e}")

# Chainlit event handler for chat start
@cl.on_chat_start
async def start_chat():
    await cl.Message(
        content="🏨 Welcome to Hotel Assistant! Ask me about Grand Palace or Sea View hotels."
    ).send()

# Chainlit event handler for incoming messages
@cl.on_message
async def main(message: cl.Message):
    try:
        result = await Runner.run(
            starting_agent=agent,
            input=message.content
        )
        await cl.Message(content=result.final_output).send()
    except InputGuardrailTripwireTriggered as e:
        await cl.Message(
            content="❌ I can only help with hotel-related queries! Ask me about Grand Palace or Sea View hotels."
        ).send()

# Run terminal version if not using Chainlit
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

