# 05_Model_Settings - Advanced Model Configuration ⚙️

## Overview

This sub-project demonstrates advanced model configuration and optimization techniques. It showcases how to fine-tune model parameters for optimal performance in different scenarios.

## Features Implemented

### 1. Model Settings Configuration

- **Location:** `main.py`
- **Feature:** Advanced ModelSettings configuration
- **Purpose:** Optimizing model performance through parameter tuning

### 2. Parameter Optimization

- **Location:** Model configuration
- **Feature:** Temperature, top_p, max_tokens, and other parameters
- **Purpose:** Fine-tuning model behavior for specific use cases

### 3. Performance Tuning

- **Location:** Model optimization
- **Feature:** Performance monitoring and optimization
- **Purpose:** Achieving optimal model performance

## Technical Implementation

### Advanced Model Settings

```python
# Comprehensive model settings configuration
model_settings = ModelSettings(
    temperature=0.7,        # Controls randomness (0.0-2.0)
    top_p=0.9,             # Nucleus sampling (0.0-1.0)
    max_tokens=1000,       # Maximum tokens to generate
    tool_choice="auto",    # Let model decide when to use tools
    # Note: frequency_penalty and presence_penalty are NOT supported by Gemini
)
```

### Specialized Model Configurations

```python
# Creative/Exploratory settings
creative_settings = ModelSettings(
    temperature=0.9,        # Higher creativity
    top_p=0.95,            # More diverse sampling
    max_tokens=1500,       # Longer responses
    tool_choice="auto"
)

# Precise/Factual settings
precise_settings = ModelSettings(
    temperature=0.1,        # Lower creativity, more focused
    top_p=0.8,             # More conservative sampling
    max_tokens=500,        # Shorter, more concise responses
    tool_choice="required"  # Force tool usage
)

# Balanced settings
balanced_settings = ModelSettings(
    temperature=0.5,        # Balanced creativity
    top_p=0.9,             # Balanced sampling
    max_tokens=1000,       # Moderate response length
    tool_choice="auto"
)
```

### Model Configuration Manager

```python
class ModelConfigManager:
    def __init__(self):
        self.configurations = {
            "creative": creative_settings,
            "precise": precise_settings,
            "balanced": balanced_settings
        }

    def get_config(self, config_type: str) -> ModelSettings:
        """Get model configuration by type."""
        return self.configurations.get(config_type, balanced_settings)

    def create_custom_config(self, **kwargs) -> ModelSettings:
        """Create custom model configuration."""
        return ModelSettings(**kwargs)
```

## How to Run

### Prerequisites

- Python 3.8+
- Required packages: `agents`, `chainlit`, `python-dotenv`, `decouple`, `requests`, `pytz`

### Environment Variables

Create a `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key
GEMINI_BASE_URL=your_gemini_base_url
WEATHER_API_KEY=your_openweathermap_api_key
```

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Chainlit
chainlit run main.py

# Or run terminal version
python main.py
```

## Test Scenarios

1. ✅ Different temperature settings and their effects
2. ✅ Top_p parameter optimization
3. ✅ Max_tokens configuration
4. ✅ Tool_choice parameter testing
5. ✅ Performance comparison between configurations
6. ✅ Custom configuration creation

## Learning Objectives

- Model parameter optimization
- Performance tuning techniques
- Configuration management
- Parameter effects on model behavior
- Custom configuration creation

## Key Concepts Demonstrated

### Model Parameters

#### Temperature (0.0-2.0)

- **Low (0.0-0.3):** More deterministic, focused responses
- **Medium (0.4-0.7):** Balanced creativity and consistency
- **High (0.8-2.0):** More creative, diverse responses

#### Top_p (0.0-1.0)

- **Low (0.0-0.5):** More conservative word selection
- **Medium (0.6-0.9):** Balanced diversity
- **High (0.9-1.0):** More diverse word selection

#### Max_tokens

- **Short (100-500):** Concise responses
- **Medium (500-1000):** Standard responses
- **Long (1000+):** Detailed, comprehensive responses

#### Tool_choice

- **"auto":** Model decides when to use tools
- **"required":** Force tool usage when available
- **"none":** Disable tool usage

### Performance Optimization

- **Response Quality:** Optimizing for better responses
- **Response Speed:** Balancing quality and speed
- **Tool Usage:** Optimizing tool selection
- **Cost Efficiency:** Balancing performance and cost

## File Structure

```
05_Model_Settings/
├── main.py              # Main application with advanced model settings
├── tools/
│   ├── addition_tool.py      # Math operations
│   ├── weather_api_tool.py   # Weather API integration
│   └── datetime_tool.py      # Time zone handling
├── pyproject.toml       # Project dependencies
├── README.md            # This documentation
└── chainlit.md          # Chainlit welcome screen
```

## Advanced Features

### Configuration Profiles

- **Creative Profile:** High temperature, high top_p for creative tasks
- **Precise Profile:** Low temperature, low top_p for factual tasks
- **Balanced Profile:** Medium settings for general use
- **Custom Profiles:** User-defined configurations

### Performance Monitoring

- **Response Time:** Monitoring generation speed
- **Quality Metrics:** Assessing response quality
- **Tool Usage:** Tracking tool utilization
- **Cost Analysis:** Monitoring API usage costs

### Dynamic Configuration

- **Context-Aware:** Adjusting settings based on context
- **User Preferences:** Personalizing settings per user
- **Task-Specific:** Optimizing for specific task types
- **Real-Time Adjustment:** Dynamic parameter tuning

## Best Practices

### Parameter Selection

- **Start with Balanced:** Begin with medium settings
- **Test Incrementally:** Make small adjustments
- **Monitor Performance:** Track the effects of changes
- **Document Changes:** Keep records of configuration changes

### Optimization Strategy

- **Define Objectives:** Clear performance goals
- **Measure Baseline:** Establish performance baseline
- **Iterate Gradually:** Make incremental improvements
- **Validate Results:** Test changes thoroughly

## Next Steps

This model configuration system demonstrates advanced optimization techniques. Combined with the other sub-projects, you now have a comprehensive understanding of building production-ready agent systems.

