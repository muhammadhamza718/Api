from agents import (
    OpenAIChatCompletionsModel,
    set_tracing_export_api_key,
    RunConfig,
)
from openai import AsyncOpenAI
from decouple import config

# Required for Gemini via OpenAI-compatible endpoint
api_key = config("GEMINI_API_KEY")
base_url = config("GEMINI_BASE_URL", default="https://generativelanguage.googleapis.com/openai")
# Use a free-tier friendlier model to avoid 429s
model_name = config("GEMINI_MODEL_NAME", default="gemini-2.5-flash")

# Only set tracing if you have a dedicated tracing key; don't use your model API key
tracing_key = config("TRACING_API_KEY", default=None)
if tracing_key:
    set_tracing_export_api_key(tracing_key)

gemini_client = AsyncOpenAI(api_key=api_key, base_url=base_url)

gemini_model = OpenAIChatCompletionsModel(
    model=model_name,
    openai_client=gemini_client,
)
config = RunConfig(model=gemini_model, tracing_disabled=True)