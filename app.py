
from flask import Flask, request, jsonify
from flask_cors import CORS
from main import ChatBot

app = Flask(__name__)
CORS(app)

# Instantiate the chat bot
chat_bot = ChatBot()

def is_valid_text(text):
    return text and not text.isspace()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/predict", methods=["POST"])
def predict():
    # Get the text from the JSON payload
    text = request.get_json().get("message")

    # Validate the text
    if not is_valid_text(text):
        return jsonify({"error": "Invalid text input"}), 400

    # If the text is valid, proceed with getting the response
    response = chat_bot.get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
