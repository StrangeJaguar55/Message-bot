from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")  # We'll set this on Render

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents":[{"parts":[{"text":prompt}]}]}
    response = requests.post(url, json=payload)
    data = response.json()
    return data['candidates'][0]['content']['parts'][0]['text']

@app.route("/sms", methods=['POST'])
def sms_reply():
    incoming_msg = request.form.get('Body')
    resp = MessagingResponse()
    try:
        reply = ask_gemini(incoming_msg)
    except:
        reply = "Sorry, I couldn't generate a response."
    resp.message(reply)
    return str(resp)

@app.route("/")
def home():
    return "Webhook is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
