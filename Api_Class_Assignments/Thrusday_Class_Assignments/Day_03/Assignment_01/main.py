from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
import chainlit as cl
from dotenv import load_dotenv
from decouple import config

load_dotenv()
set_tracing_disabled(True)

key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")

gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)

gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",
    openai_client=gemini_client,
)

# Define the FAQ Agent
faq_agent = Agent(
    name="FAQBot",
    instructions="""
You are a helpful FAQ chatbot. Answer the following questions clearly and concisely:

1. **What is your name?**  
   My name is FAQBot, your friendly assistant!

2. **What can you do?**  
   I can answer common questions about myself and provide helpful information.

3. **Who created you?**  
   I was created by a student using the OpenAI Agents SDK and Chainlit.

4. **Where are you from?**  
   I'm a digital assistant, so I exist in the cloud, ready to help!

5. **How can I contact support?**  
   For support, please reach out to the developer who created me.

For any other questions, respond politely that you can only answer predefined FAQs.
""",
    model=gemini_model,  # Specify the model (adjust if using a different one)
)

# Terminal-based testing for the FAQ agent
# Result = Runner.run_sync(faq_agent, "What is your name?")
# print(Result.final_output)


# Chainlit event handler for chat start
@cl.on_chat_start
async def start_chat():
    # Initialize user session
    cl.user_session.set("message_history", [{"role": "system", "content": faq_agent.instructions}])

# Chainlit event handler for incoming messages
@cl.on_message
async def main(message: cl.Message):
    # Get user input
    user_input = message.content

    # Add user input to message history
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": user_input})

    # Run the agent with the user input
    result = Runner.run_sync(faq_agent, user_input)

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

