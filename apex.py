from google import genai

client = genai.Client(api_key="AIzaSyDh0UKb87W5gYp8gZx2fJFDyEDRBCsd37c")

# Load memory
try:
    with open("memory.txt", "r") as f:
        memory = f.read()
except:
    memory = ""

# Get input from user
user_input = input("You: ")

prompt = f"""
Apex, you are my personal assistant.
Here is your memory of me so far:
{memory}

Respond to the user, and after responding,
append any new important information to memory.txt.
User says: {user_input}
"""

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=prompt
)

print("Apex:", response.text)

# Save updated memory
with open("memory.txt", "w") as f:
    f.write(memory + "\n" + response.text)