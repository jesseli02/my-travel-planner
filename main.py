from together import Together
import json

# Initialize Together AI client
client = Together(api_key="cbea512d1bf322aee99d7ce57605f76213a88036512f376396654844eba7efe8")

# Key user inputs
user_input = {
    "arrival_date": "2024-03-19",
    "departure_date": "2024-03-23",
    "arrival_time": "noon",
    'departure_time': 'noon',
    'start_location': 'Tulum, Mexico',
    'end_location': 'Tulum, Mexico',
    'daily_budget': '200 CAD per person per day',
    'vibe': 'relaxing, eat, and enjoy some food',
    'number_of_travelers': '7',
    'travel_speed': 'slow to average',
    'additional_info': "We're going to be 3 couples and 1 single person"
}

# Crafting request message for AI
prompt = "Could you help me plan a daily itinerary for my upcoming trip? Here are the details below: "
trip_info = json.dumps(user_input)

# Calling Together AI model
stream = client.chat.completions.create(
  model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
  messages = [{"role": "user", "content": (prompt + trip_info)}],
  max_tokens = 1000,
  stream = True
)

for chunk in stream:
  print(chunk.choices[0].delta.content or "", end="", flush=True)