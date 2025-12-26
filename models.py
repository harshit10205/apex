from google import genai

client = genai.Client(api_key="AIzaSyA0KV0Q96_YVkDoVv5t1C71-aFzYmzkWHc")

models = client.models.list()

for m in models:
    print(m.name)