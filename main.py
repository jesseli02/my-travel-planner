from together import Together

# Initialize Together AI client
client = Together(api_key="cbea512d1bf322aee99d7ce57605f76213a88036512f376396654844eba7efe8")

# Key user inputs
start_date = "2024-03-19"
end_date = "2024-03-23"
start_time = "noon"
end_time = "noon"
start_location = "Tulum, Mexico"
end_location = "Tulum, Mexico"
daily_budget = "200 CAD per person per day"
vibe = "relaxing, eat, and enjoy some food"
travelers = "7"
travel_speed = "slow to average"
additional_info = "We're going to be 3 couples and 1 single person"

# Crafting prompt for AI
prompt = (
    f"Hi, I would like to some help planning a travel itinerary - could you help plan a daily itinerary for me. "
    f"Here are some details about my travel plan: We will be arriving at {start_location} and departing at {end_location} on {start_date} and {end_date}. "
    f"We're going to be in total {travelers} people and {travel_speed} travelers. "
    f"We will be traveling with the intention of {vibe}. We will be budgeting for {daily_budget}. "
    f"In addition, {additional_info}."
)

stream = client.chat.completions.create(
  model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
  messages = [{"role": "user", "content": prompt}],
  max_tokens = 1000,
  stream = True
)

for chunk in stream:
  print(chunk.choices[0].delta.content or "", end="", flush=True)