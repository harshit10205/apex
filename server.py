from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from google import genai
import re

client = genai.Client(api_key="AIzaSyDh0UKb87W5gYp8gZx2fJFDyEDRBCsd37c")
app = FastAPI()

# Load memory
def load_memory():
    try:
        with open("memory.txt", "r") as f:
            return f.read()
    except:
        return ""

# Save only long-term memory, not whole chat
def update_memory(text):
    with open("memory.txt", "a") as f:
        f.write(text + "\n")

# Load chat history
def load_chat():
    try:
        with open("chat.txt", "r") as f:
            return f.read().replace("\n", "<br>")
    except:
        return ""

# Save chat for UI only
def save_chat(role, text):
    with open("chat.txt", "a") as f:
        f.write(f"{role}: {text}\n")


@app.get("/", response_class=HTMLResponse)
def home():
    chat = load_chat()
    return f"""
    <html>
    <body style="font-family:sans-serif;max-width:600px;margin:auto;padding:20px;">
        <h2>Apex - Personal AI</h2>
        <div style="border:1px solid #ddd;padding:10px;height:400px;overflow-y:auto;background:#fafafa">
            {chat}
        </div>
        <form action="/chat" method="post" style="margin-top:15px;">
            <input type="text" name="msg" placeholder="Type message..." style="width:75%;padding:8px;">
            <button type="submit" style="padding:8px 12px;">Send</button>
        </form>
    </body>
    </html>
    """

@app.post("/chat", response_class=HTMLResponse)
def chat(msg: str = Form(...)):
    memory = load_memory()

    prompt = f"""
    You are Apex, my personal AI with memory.
    Here is what you know so far:
    {memory}

    Respond to the user.
    If message contains personal details (name, goal, preferences),
    store only essential info for future.
    
    User says: {msg}
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    reply = response.text.strip()

    # Basic rule to detect personal detail e.g. "my name is ___"
    name_match = re.search(r"my name is ([A-Za-z ]+)", msg, re.IGNORECASE)
    if name_match:
        update_memory(f"User's name: {name_match.group(1)}")

    save_chat("You", msg)
    save_chat("Apex", reply)

    return home()