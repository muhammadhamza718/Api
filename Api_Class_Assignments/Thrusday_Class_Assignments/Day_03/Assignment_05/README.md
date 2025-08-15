# Day 03 Assignment 05 - Advanced Agent Features 🚀

## Overview

This assignment demonstrates advanced agent features including handoffs, guardrails, model settings, agent hooks, and specialized agent configurations. The assignment is divided into five sub-projects, each focusing on different advanced concepts.

## Sub-Projects Overview

### 1. 01_Agents - Basic Agent Handoffs

- **Focus:** Agent-to-agent handoffs and specialized agents
- **Features:** Math agent, time agent, calendar agent with handoff capabilities
- **Learning:** How agents can pass control to specialized agents

### 2. 02_Tools - Advanced Tool Configuration

- **Focus:** Tool organization and advanced tool features
- **Features:** Modular tool structure with enhanced capabilities
- **Learning:** Tool management and advanced tool configurations

### 3. 03_Agents_Module - Agent Modularity

- **Focus:** Modular agent architecture and organization
- **Features:** Agent modules and component-based design
- **Learning:** Scalable agent architecture patterns

### 4. 04_Agents_Reference - Agent References and Context

- **Focus:** Agent context management and reference handling
- **Features:** Context-aware agents with reference capabilities
- **Learning:** Context management and agent state handling

### 5. 05_Model_Settings - Advanced Model Configuration

- **Focus:** Model settings and configuration optimization
- **Features:** Temperature, top_p, max_tokens, and other model parameters
- **Learning:** Model parameter tuning and optimization

## Common Features Across All Sub-Projects

### Advanced Agent Concepts

- **Handoffs:** Agent-to-agent control transfer
- **Guardrails:** Input validation and safety measures
- **Hooks:** Lifecycle event handling
- **Context Management:** User context and state handling
- **Model Settings:** Advanced model configuration

### Technical Implementation

- **Type Safety:** Proper type annotations throughout
- **Error Handling:** Comprehensive error management
- **Modular Design:** Clean separation of concerns
- **Documentation:** Detailed code documentation
- **Testing:** Comprehensive test scenarios

## How to Navigate

Each sub-project is self-contained and can be run independently:

```bash
# Navigate to specific sub-project
cd 01_Agents/
cd 02_Tools/
cd 03_Agents_Module/
cd 04_Agents_Reference/
cd 05_Model_Settings/

# Run any sub-project
chainlit run main.py
```

## Prerequisites

### Environment Variables

Create a `.env` file in each sub-project:

```
GEMINI_API_KEY=your_gemini_api_key
GEMINI_BASE_URL=your_gemini_base_url
WEATHER_API_KEY=your_openweathermap_api_key
```

### Dependencies

Each sub-project includes its own `pyproject.toml` with specific dependencies.

## Learning Objectives

### Advanced Agent Features

- **Handoffs:** Understanding agent delegation patterns
- **Guardrails:** Implementing safety and validation measures
- **Hooks:** Managing agent lifecycle events
- **Context:** Handling user context and state
- **Model Settings:** Optimizing model performance

### Architecture Patterns

- **Modularity:** Building scalable agent systems
- **Separation of Concerns:** Clean code organization
- **Reusability:** Creating reusable agent components
- **Maintainability:** Long-term code maintenance

### Best Practices

- **Type Safety:** Proper type annotations
- **Error Handling:** Graceful error management
- **Documentation:** Clear code documentation
- **Testing:** Comprehensive testing strategies

## File Structure

```
Assignment_05/
├── README.md                    # This documentation
├── 01_Agents/                   # Agent handoffs
│   ├── main.py
│   ├── tools/
│   ├── README.md
│   └── chainlit.md
├── 02_Tools/                    # Advanced tools
│   ├── main.py
│   ├── tools/
│   ├── README.md
│   └── chainlit.md
├── 03_Agents_Module/            # Modular agents
│   ├── main.py
│   ├── tools/
│   ├── README.md
│   └── chainlit.md
├── 04_Agents_Reference/         # Agent references
│   ├── main.py
│   ├── tools/
│   ├── README.md
│   └── chainlit.md
└── 05_Model_Settings/           # Model configuration
    ├── main.py
    ├── tools/
    ├── README.md
    └── chainlit.md
```

## Getting Started

1. **Choose a sub-project** based on your learning goals
2. **Set up environment variables** in the sub-project directory
3. **Install dependencies** using the project's package manager
4. **Run the application** and explore the features
5. **Review the code** to understand the implementation
6. **Experiment** with modifications and customizations

## Next Steps

After completing all sub-projects, you'll have a comprehensive understanding of:

- Advanced agent architectures
- Tool management and organization
- Agent lifecycle management
- Model optimization techniques
- Scalable agent system design

This foundation prepares you for building production-ready agent systems with advanced features and robust architecture.

