
from flask import Flask, request, jsonify
import openai
import requests
import os
from dotenv import load_dotenv


# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Helper function to fetch weather data
def get_weather(location):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(weather_url)
    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"The current temperature in {location} is {temp}°C with {description}."
    else:
        return "I couldn't fetch the weather data. Please check the location name."

# Chatbot logic
def generate_gardening_response(user_input):
    # Include gardening-specific context in prompts
    prompt = f"""
    You are a gardening assistant AI. Answer gardening-related questions, including plant care, watering schedules, soil, sunlight, and pest management. 
    User Input: {user_input}
    Response:
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Routes
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    location = data.get("location", None)

    if "weather" in user_input.lower() and location:
        weather_info = get_weather(location)
        response = f"{weather_info}\n\nDo you want advice based on this weather?"
    else:
        response = generate_gardening_response(user_input)
    
    return jsonify({"response": response})

# Run the Flask app
# if _name_ == "_main_":
#     app.run(debug=True)