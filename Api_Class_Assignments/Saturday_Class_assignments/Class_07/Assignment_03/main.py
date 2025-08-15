import os
from agents import Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from Agents.agents import bot_agent, human_agent
import chainlit as cl
from agents import set_tracing_disabled

# Disable LiteralAI/OpenAI instrumentation to avoid NotGiven/tool serialization issues
os.environ["LITERALAI_DISABLED"] = "1"
# cl.instrument_openai()  # disable for non-OpenAI base_url to avoid serialization conflicts
set_tracing_disabled(True)  # disable internal tracing

# # Optional terminal testing (uncomment to run outside Chainlit)
# if __name__ == "__main__":
#     test_inputs = [
#         "What is the status of my order 123?",
#         "You guys are stupid",
#         "I want a refund!",
#         "What colors does the widget come in?"
#     ]
#     for text in test_inputs:
#         try:
#             res = Runner.run_sync(bot_agent, text, context={"user_input": text})
#             print("Bot:", res.final_output)
#         except InputGuardrailTripwireTriggered:
#             res = Runner.run_sync(human_agent, text, context={"user_input": text})
#             print("Human:", res.final_output)

# Chainlit event handler for chat start
@cl.on_chat_start
async def start_chat():
    await cl.Message(
        content="🤖 Welcome! I'm your customer service assistant. I can help with order status, product info, and more. If I can't help, I'll transfer you to a human agent."
    ).send()

# Chainlit event handler for incoming messages
@cl.on_message
async def main(message: cl.Message):
    try:
        # Try bot agent first
        result = await Runner.run(
            starting_agent=bot_agent,
            input=message.content,
            context={"user_input": message.content}
        )
        await cl.Message(content=f"🤖 Bot: {result.final_output}").send()
    except InputGuardrailTripwireTriggered:
        # If guardrail triggered, use human agent
        result = await Runner.run(
            starting_agent=human_agent,
            input=message.content,
            context={"user_input": message.content}
        )
        await cl.Message(content=f"👤 Human Agent: {result.final_output}").send()

