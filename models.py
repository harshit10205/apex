from google import genai

client = genai.Client(api_key="AIzaSyDh0UKb87W5gYp8gZx2fJFDyEDRBCsd37c")

models = client.models.list()

for m in models:
    print(m.name)