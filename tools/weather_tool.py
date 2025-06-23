import requests
from gtts import gTTS
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather_and_speak(city, audio_output_path):
    if not OPENWEATHER_API_KEY:
        raise ValueError("OpenWeatherMap API key not set. Please set OPENWEATHER_API_KEY in your .env file.")

    url = f"{BASE_URL}appid={OPENWEATHER_API_KEY}&q={city}&units=metric"

    response = requests.get(url)
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

    data = response.json()

    if data.get("cod") != 200:
        raise ValueError(f"City not found or API error: {data.get('message', 'Unknown error')}")

    main_data = data['main']
    weather_data = data['weather'][0]

    temperature = main_data['temp']
    feels_like = main_data['feels_like']
    humidity = main_data['humidity']
    description = weather_data['description']
    city_name = data['name']

    weather_text = (
        f"The current weather in {city_name} is {description}. "
        f"The temperature is {temperature:.1f} degrees Celsius, "
        f"and it feels like {feels_like:.1f} degrees Celsius. "
        f"Humidity is {humidity} percent."
    )

    tts = gTTS(text=weather_text, lang='en')
    tts.save(audio_output_path)

    return weather_text