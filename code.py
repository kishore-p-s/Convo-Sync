import speech_recognition as sr
import pyttsx3
import time
import pytz
import datetime
import openai  # Make sure to install the 'openai' library using pip
import random

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai.api_key = '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'

RESPONSE_TIMEOUT = 300

class WeatherAPI:
    def get_weather(self, city):
        # Implement actual logic to fetch weather information from a weather API
        return {'description': 'Clear sky', 'temperature': 25}

class EmailReader:
    def login(self, user, password):
        # Implement actual logic to log in to the email account
        pass

    def get_latest_email(self):
        # Implement actual logic to retrieve the latest email
        return {'sender': 'example@example.com', 'subject': 'Test Email', 'content': 'This is a test email.'}

class MusicAPI:
    def get_recommendation(self, genre):
        # Implement actual logic to fetch music recommendations from a music API
        return 'Song Name'

class NLPAPI:
    def analyze_text(self, text):
        # Implement actual logic to analyze text using an NLP API
        return {'intent': 'greeting', 'entities': {'subject': 'Jarvis'}}

weather_api = WeatherAPI()
email_reader = EmailReader()
music_api = MusicAPI()
nlp_api = NLPAPI()

listener = sr.Recognizer()
engine = pyttsx3.init()

# Set voice to a female voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Jarvis is listening...')
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            print('Listening complete...')
            command = listener.recognize_google(voice).lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                print('Command:', command)

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you please repeat?")
        command = take_command()
    except sr.RequestError:
        print("There was an error with the speech recognition service. Please try again later.")
        command = ""

    return command

def location_based_services():
    talk("Sure, I can provide weather updates. Could you please provide your city?")
    city = take_command()
    try:
        weather_info = weather_api.get_weather(city)
        talk(f"The current weather in {city} is {weather_info['description']} with a temperature of {weather_info['temperature']} degrees Celsius.")
        print(f"City: {city}, Weather: {weather_info['description']}, Temperature: {weather_info['temperature']}°C")
    except Exception as e:
        talk(f"I'm sorry, I couldn't retrieve weather information for {city}. Please try again later.")

def email_integration():
    talk("Sure, I can read your latest email. Please provide your email credentials.")
    try:
        email_reader.login(user='your_email@example.com', password='your_password')
        latest_email = email_reader.get_latest_email()
        talk(f"Your latest email is from {latest_email['sender']} with the subject: {latest_email['subject']}.")
        talk("Would you like me to read the content of the email?")
        response = take_command()
        if 'yes' in response:
            talk(f"Here is the content: {latest_email['content']}")
        else:
            talk("Alright, let me know if you need anything else.")
    except Exception as e:
        talk("I'm sorry, I couldn't retrieve your email. Please check your credentials and try again.")

def music_recommendations():
    talk("Sure, I can recommend a song. What's your favorite genre?")
    genre = take_command()
    try:
        recommended_song = music_api.get_recommendation(genre)
        talk(f"I recommend listening to {recommended_song} in the {genre} genre.")
    except Exception as e:
        talk(f"I'm sorry, I couldn't fetch music recommendations at the moment. Please try again later.")

def natural_language_understanding():
    talk("I'm currently analyzing your input. Please speak a sentence.")
    user_input = take_command()
    try:
        analysis_result = nlp_api.analyze_text(user_input)
        talk(f"Here's what I found: Intent - {analysis_result['intent']}, Entities - {analysis_result['entities']}")
    except Exception as e:
        talk("I'm sorry, I couldn't analyze your input at the moment. Please try again later.")

def interactive_games():
    talk("Great! Let's play a guessing game. I'm thinking of a number between 1 and 10.")
    correct_number = random.randint(1, 10)
    
    for _ in range(3):  # Give the user 3 chances
        talk("Take a guess.")
        user_guess = int(take_command())
        if user_guess == correct_number:
            talk("Congratulations! You guessed the correct number.")
            break
        else:
            talk("Sorry, that's not the correct number. Try again!")

    talk(f"The correct number was {correct_number}. Thanks for playing!")

def run_Jarvis():
    start_time = time.time()  # Start time for the conversation

    # Get the current date and time in the local timezone
    local_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(local_timezone).strftime("%Y-%m-%d %H:%M:%S")

    talk(f"Good {current_time}! How can I assist you today?")

    while True:
        command = take_command()

        if 'exit' in command or check_response_timeout(start_time):
            talk("It was great talking to you! See you next time.")
            return

        if not command:
            talk("I'm sorry, but I couldn't understand your command.")
            continue

        prompt = f"Jarvis, {command}"

        response = generate_response(prompt)

        print(response)
        talk(response)

        # Call additional functions based on specific commands
        if 'translate' in command:
            language_translation()
        elif 'location' in command:
            location_based_services()
        elif 'email' in command:
            email_integration()
        elif 'custom' in command:
            custom_commands()
        elif 'recommend' in command:
            music_recommendations()
        elif 'understand' in command:
            natural_language_understanding()
        elif 'game' in command:
            interactive_games()


while True:
    run_Jarvis()
