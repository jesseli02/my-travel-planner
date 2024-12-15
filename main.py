from together import Together

client = Together(api_key="cbea512d1bf322aee99d7ce57605f76213a88036512f376396654844eba7efe8")

stream = client.chat.completions.create(
  model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
  messages=[{"role": "user", "content": "What are the top 3 things to do in New York?"}],
  stream=True,
)

for chunk in stream:
  print(chunk.choices[0].delta.content or "", end="", flush=True)