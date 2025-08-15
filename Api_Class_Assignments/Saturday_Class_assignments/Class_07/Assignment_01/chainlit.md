# Chainlit Integration for Agentic AI

## Overview
This document outlines the integration of Chainlit with the Agentic AI project to provide a user-friendly interface for interacting with the AI agent.

## Features
- User session management
- Message history tracking
- Real-time interaction with the AI agent

## How to Use
1. Start the Chainlit server:
   ```bash
   chainlit run main.py
   ```
2. Open your browser and navigate to the Chainlit interface.
3. Interact with the AI agent by sending messages.

## Implementation Details
- The agent is configured to handle user messages and respond accordingly.
- The output guardrails are applied to ensure that the agent does not respond to political queries.