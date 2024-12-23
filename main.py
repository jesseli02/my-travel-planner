from together import Together as tg
import json
import streamlit as st
import pandas as pd

# Initialize Together AI client
client = tg(api_key="cbea512d1bf322aee99d7ce57605f76213a88036512f376396654844eba7efe8")

# Key user inputs
user_input = {
    "arrival_date": "2025-03-19",
    "departure_date": "2025-03-23",
    "arrival_time": "noon",
    'departure_time': 'noon',
    'start_location': 'Tulum, Mexico',
    'end_location': 'Tulum, Mexico',
    'daily_budget': '200 CAD per person per day',
    'vibe': 'relaxing, eat, and enjoy some food',
    'number_of_travelers': '7',
    'travel_speed': 'average speed',
    'must-visit places' : 'cenotes',
    'interests' : 'eating authentic mexican food, exploring culture, enjoying the nice weather and beaches',
    'additional_info' : "2 of our friends will be only joining us on the Friday at noon. We plan on working remotely from 9am to 6pm during the weekday so can't really commit to anything big during those days."
}

# Crafting request message for AI
prompt = "Could you help me plan a daily itinerary for my upcoming trip? Here are the details below: "
trip_info = json.dumps(user_input)

print(prompt)
print(trip_info)
print("\n")

# Calling Together AI model
stream = client.chat.completions.create(
  model = "meta-llama/Llama-3.3-70B-Instruct-Turbo",
  messages = [{"role": "user", "content": (prompt + trip_info)}],
  max_tokens = 1000,
  stream = True
)

for chunk in stream:
  print(chunk.choices[0].delta.content or "", end="", flush=True)