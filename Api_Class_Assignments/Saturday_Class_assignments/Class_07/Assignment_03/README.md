# Day 07 Assignment 01 - Agentic AI with Tools, Handoffs, and Guardrails

## Features Implemented:

### 1. Tool Call
- **Location:** `Tools/tools.py`
- **Feature:** `@function_tool` decorator for `get_order_status()`
- **Purpose:** Fetches order status from simulated database

### 2. Handoff
- **Location:** `Agents/agents.py`
- **Feature:** Two agents (bot_agent, human_agent) with automatic handoff
- **Purpose:** Escalates complex/rude queries to human agent

### 3. Guardrail
- **Location:** `Guardrails/Guardrail.py`
- **Feature:** `@input_guardrail` decorator for `check_input()`
- **Purpose:** Detects negative terms and triggers handoff

### 4. ModelSettings
- **Location:** `Agents/agents.py`
- **Feature:** `tool_choice="required"` in ModelSettings
- **Purpose:** Forces tool usage when appropriate

### 5. Function Tool Decorators
- **Location:** `Tools/tools.py`
- **Feature:** `@function_tool` decorator
- **Purpose:** Converts Python function to AI tool

## Test Scenarios:
1. ✅ Normal order status query → Bot agent responds
2. ✅ Rude language → Guardrail triggers → Human agent takes over
3. ✅ Refund requests → Guardrail triggers → Human agent handles
4. ✅ Unknown queries → Bot agent responds appropriately

## How to Run:
```bash
uv run main.py
```
```

## 🎯 **Conclusion:**

**You have completed 95% of the assignment!** All the required features are implemented and working. You just need to:

1. Add the documentation above to your README.md
2. Add inline comments to your code explaining where each feature is used
3. Save the terminal output as proof of functionality

Your implementation is solid and demonstrates all the required concepts! 🚀