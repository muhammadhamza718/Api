from agents import (
	Agent, 
	Runner, 
	AsyncOpenAI, 
	OpenAIChatCompletionsModel, 
	set_tracing_disabled,  
	RunContextWrapper, 
	output_guardrail,
	GuardrailFunctionOutput,
	InputGuardrailTripwireTriggered,
	TResponseInputItem,
	ModelSettings,
)

import chainlit as cl
from dotenv import load_dotenv
from decouple import config
from pydantic import BaseModel
from typing import Any
import asyncio
import json

load_dotenv()
set_tracing_disabled(True)

key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")

gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",
    openai_client=gemini_client,
)

# --- Output model ---
class PoliticalCheckOutput(BaseModel):
    is_political: bool
    reason: str

@output_guardrail
async def check_output(
	ctx: RunContextWrapper[Any],
	agent: Agent[Any],
	input_data: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
	"""
	Blocks political content in agent responses.
	"""
	checker_agent = Agent(
		"OutputGuardrailAgent",
		instructions=(
			"You are a strict classifier. Read the given text and determine if it contains political topics "
			"or references to political figures. "
			"Respond ONLY with a single JSON object matching this schema: "
			'{"is_political": boolean, "reason": string}. '
			"No extra words, no code fences, no prefixes or suffixes."
		),
		model=gemini_model,
	)

	result = await Runner.run(checker_agent, input_data, context=ctx.context)
	raw = result.final_output if isinstance(result.final_output, str) else str(result.final_output)

	# Try to extract and parse JSON
	start = raw.find("{")
	end = raw.rfind("}")
	parsed = None
	if start != -1 and end != -1 and end > start:
		try:
			obj = json.loads(raw[start : end + 1])
			parsed = PoliticalCheckOutput(**obj)
		except Exception:
			parsed = None

	if parsed is None:
		parsed = PoliticalCheckOutput(is_political=False, reason="Non-JSON output from checker")

	return GuardrailFunctionOutput(
		output_info=parsed,
		tripwire_triggered=parsed.is_political
	)

# Define the math Agent
math_agent = Agent(
	name="MathBot",
	instructions=(
		"You are a math tutor. Only answer math problems. "
		"If the user asks anything that is not strictly a math question, "
		"respond exactly: 'I can only answer math questions.' "
		"Do not add any other words."
	),
	model=gemini_model,
	model_settings=ModelSettings(temperature=0.2),
	output_guardrails=[check_output]
)

# Terminal-based testing for the FAQ agent
# async def main():
#     try:
#         # a = 10/0
#         msg = input("Enter you question : ")
#         result = await Runner.run(math_agent, msg)
#         print(f"\n\n final output : {result.final_output}")
#     except InputGuardrailTripwireTriggered as ex:
#         print("Error : invalid prompt")

# asyncio.run(main())


# Chainlit event handler for chat start
@cl.on_chat_start
async def start_chat():
    # Initialize user session
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

