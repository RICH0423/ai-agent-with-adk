import datetime

from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_news(city: str) -> dict:
   """Retrieves the news of a particular city.
   Args:
       city (str): The name of the city for which to retrieve the news.

   Returns:
       dict: headline and content of the news, or error message.
   """
   if city.lower() == "taipei" or city.lower() == "台北":
       return {
           "headline": "北捷博愛座事件",
           "content": "一位白髮婦人在捷運上因讓座問題，不僅涉嫌竊盜遭通緝，還因用雨傘毆打博愛座女童而被檢方起訴。",
       }
   else:
       return {
           "error_message": f"News for '{city}' is not available.",
       }

root_agent = Agent(
   name="news_assistant_agent",
   model="gemini-2.5-flash",
   description=(
       "Agent to retrieve news for any particular city."
   ),

   instruction=(
       "You are a helpful agent who can answer user questions related to news of any city."
   ),
   tools=[get_news],
)
