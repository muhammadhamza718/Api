# Agentic AI with Output Guardrails

## Overview
This project implements an AI agent that can solve math problems while avoiding political topics and references to political figures using output guardrails.

## Features
- Math problem solving
- Output guardrails to block political content

## How to Run
1. Ensure you have the required dependencies installed.
2. Run the application using:
   ```bash
   uv run main.py
   ```

## Usage
- Enter a math question to receive an answer.
- If a political question is asked, the agent will respond with a message indicating it cannot answer.

## Implementation Details
- The output guardrail checks for political keywords in the agent's responses and blocks them accordingly.