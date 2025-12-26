from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import google.genai as genai
from dotenv import load_dotenv
import os


# Load API key
load_dotenv()
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise RuntimeError("GENAI_API_KEY missing in .env")


client = genai.Client(api_key=api_key)

app = FastAPI()

# serve UI
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def ui():
    return open("static/chat.html").read()


@app.post("/chat")
def chat(message: str = Form(...)):
    response = client.models.generate_content(
        model="models/gemma-3-4b-it",
        contents=message
    )
    return {"reply": response.text.strip()}