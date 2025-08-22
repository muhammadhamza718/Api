# app/agent_with_tavily.py
import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from tavily import TavilyClient
from agents import (
    Agent,
    Runner,
    RunContextWrapper,
    function_tool,
    set_tracing_disabled,
    AsyncOpenAI,
    output_guardrail,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
)

from gemini_helper.core import get_gemini_model
from decouple import config
from dataclasses import dataclass
from typing import Any

load_dotenv()
set_tracing_disabled(True)

key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL")

gemini_client = AsyncOpenAI(api_key=key, base_url=base_url)
gemini_model = get_gemini_model()

@dataclass
class AppContext:
    tavily: Any

class SearchArgs(BaseModel):
    query: str

# Alternative approach: Define the function tool manually
@function_tool
def tavily_search(ctx: RunContextWrapper[AppContext], args: SearchArgs) -> str:
    """Search the web via Tavily and return JSON with answer and top results.
    
    Args:
        query: The search query string
    """
    print(f"🔍 Searching for: {args.query}")
    try:
        resp = ctx.context.tavily.search(args.query, max_results=5)
        results = resp.get("results", [])[:5]
        out = {
            "query": resp.get("query", args.query),
            "answer": resp.get("answer"),
            "results": [
                {"title": r.get("title"), "url": r.get("url"), "snippet": r.get("content")}
                for r in results
            ],
        }
        return json.dumps(out, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Tavily search error: {e}")
        return json.dumps({"error": str(e), "query": args.query})

class AgentOutput(BaseModel):
    response: str

class PoliticalCheck(BaseModel):
    contains_political: bool
    reasoning: str

# Political content detection agent
political_guardrail_agent = Agent(
    name="Political Content Detector",
    instructions=(
        "Analyze the text for political content. Look for:\n"
        "- Political figures (presidents, ministers, senators, governors, etc.)\n"
        "- Political parties or movements\n"
        "- Elections, campaigns, or voting\n"
        "- Government policies or legislation\n"
        "- Political controversies or debates\n\n"
        "Return contains_political=true if ANY political content is found, false otherwise.\n"
        "Provide clear reasoning for your decision."
    ),
    model=gemini_model,
    output_type=PoliticalCheck,
)

@output_guardrail
async def political_output_guardrail(
    ctx: RunContextWrapper[AppContext],
    agent: Agent,
    output: AgentOutput,
) -> GuardrailFunctionOutput:
    """Check if the agent output contains political content."""
    text = output.response
    print(f"🛡️ Checking for political content...")
    
    try:
        guard_result = await Runner.run(
            political_guardrail_agent, 
            f"Analyze this text for political content:\n\n{text}", 
            context=ctx.context
        )
        final = guard_result.final_output
        
        print(f"🛡️ Political content detected: {final.contains_political}")
        print(f"🛡️ Reasoning: {final.reasoning}")
        
        return GuardrailFunctionOutput(
            output_info=final,
            tripwire_triggered=final.contains_political,
        )
    except Exception as e:
        print(f"❌ Political guardrail error: {e}")
        # Fail safe - let content through if guardrail fails
        return GuardrailFunctionOutput(
            output_info={"error": str(e)},
            tripwire_triggered=False,
        )

def build_agent() -> Agent[AppContext]:
    return Agent[AppContext](
        name="Web Researcher",
        instructions=(
            "You are a helpful research assistant. When users ask for current information, "
            "recent developments, or latest discoveries, ALWAYS use the tavily_search tool first. "
            "Then provide a comprehensive response based on the search results.\n\n"
            "IMPORTANT: Avoid political topics, political figures, elections, government policies, "
            "or partisan content. Focus on science, technology, education, and general knowledge."
        ),
        model=gemini_model,
        tools=[tavily_search],
        output_type=AgentOutput,
        output_guardrails=[political_output_guardrail],
    )

async def main():
    print("🚀 Starting Web Researcher with Political Content Guardrail...")
    
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY missing from environment variables")
    
    ctx = AppContext(tavily=TavilyClient(api_key=api_key))
    agent = build_agent()

    # Test queries
    test_queries = [
        "What are the latest discoveries about exoplanets?",  # Safe - science
        "Summarize recent advances in AI and machine learning.",  # Safe - technology
        "Tell me about the current President of the United States.",  # Political - should be blocked
        "What are the latest developments in renewable energy?",  # Safe - technology/environment
        "Who won the 2024 election?",  # Political - should be blocked
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"🔍 Test Query {i}: {query}")
        print('='*70)
        
        try:
            result = await Runner.run(agent, query, context=ctx)
            print("✅ SUCCESS - Agent Response:")
            print(result.final_output.response)
            
        except OutputGuardrailTripwireTriggered as e:
            guard_info = e.guardrail_result.output.output_info
            print("🚫 BLOCKED by Political Content Guardrail!")
            print(f"🚫 Reasoning: {guard_info.reasoning}")
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())