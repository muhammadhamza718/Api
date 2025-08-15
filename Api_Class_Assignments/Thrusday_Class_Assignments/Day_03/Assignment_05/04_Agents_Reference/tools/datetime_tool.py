import pytz
from datetime import datetime
from agents import function_tool

@function_tool
def get_time(timezone: str) -> str:
    """Returns the current time in the specified timezone (e.g., 'America/New_York')."""
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime("%I:%M %p %Z")
        return f"The current time in {timezone} is {current_time}."
    except pytz.exceptions.UnknownTimeZoneError:
        return "Invalid timezone. Please provide a valid timezone (e.g., 'America/New_York')."