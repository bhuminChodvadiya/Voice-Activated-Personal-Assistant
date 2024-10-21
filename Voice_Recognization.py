import pyttsx3  # Text-to-speech conversion library
import speech_recognition as sr  # Library for performing speech recognition
import datetime  # For getting the current date and time
import wikipedia  # To fetch summaries from Wikipedia
import webbrowser  # To open web pages
import os  # For accessing operating system functionalities (like opening apps)
import requests  # To make HTTP requests (used for weather data)

# Initialize the speech engine (using the sapi5 voice engine)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')  # Get the available voices
engine.setProperty('voice', voices[0].id)  # Set the voice to the first one

# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to wish the user based on the current time
def wishme():
    hour = int(datetime.datetime.now().hour)  # Get the current hour
    if hour >= 0 and hour < 12:
        speak("Good Morning my dear friend")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon my dear friend")
    else:
        speak("Good Evening my dear friend")
    speak("Let me know how I can help you. What are you looking for?")

# Function to listen to user's voice command and recognize it
def takecommand():
    r = sr.Recognizer()  # Initialize the recognizer
    with sr.Microphone() as source:
        print("Listening to you...")
        r.pause_threshold = 1  # Wait for a second before considering as end of sentence
        audio = r.listen(source)  # Listen to the microphone input

    try:
        print("Recognizing your voice...")
        query = r.recognize_google(audio, language="en-in")  # Recognize the speech using Google API
        print(f"You said: {query}\n")
    except Exception as e:
        # Handle exceptions, such as when speech is not recognized
        print("Sorry, I didn't catch that. Please say it again.")
        return "None"  # Return 'None' if the speech isn't recognized

    return query.lower()  # Return the recognized query in lowercase for easier matching

# Function to get weather information from OpenWeatherMap
def get_weather(city):
    api_key = "Your_API-key"  # Replace with your correct OpenWeatherMap API key
    base_url = "http://api.openweathermap.org"
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"

    # Fetch weather data from the API
    response = requests.get(complete_url)
    data = response.json()

    # Debugging: Print the entire API response to check for issues
    print("API Response:", data)

    # Check if the response contains valid weather data (code != 404 means city is found)
    if data["cod"] != "404":
        main = data.get("main")
        if main:  # Ensure the 'main' section is present in the response
            weather_desc = data["weather"][0]["description"]  # Get the weather description
            temp = main.get("temp")  # Get the temperature
            speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}.")
        else:
            speak("Unable to retrieve weather information. Please try again later.")
    else:
        speak(f"City {city} not found. Please try again.")

# Main function to run the assistant
if __name__ == '__main__':
    wishme()  # Call the wishme function to greet the user

    while True:
        query = takecommand()  # Continuously listen for commands

        if 'exit' in query:  # Exit command to stop the assistant
            speak("Goodbye!")
            break  # Break the loop to exit

        if 'open wikipedia' in query:  # Wikipedia search command
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")  # Remove the word 'wikipedia' from the query
            result = wikipedia.summary(query, sentences=2)  # Fetch a summary of the search query
            speak("According to Wikipedia...")
            print(result)
            speak(result)

        elif 'open notepad' in query:  # Command to open Notepad
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)

        elif 'open paint' in query:  # Command to open Paint
            npath = "C:\\Windows\\system32\\mspaint.exe"
            os.startfile(npath)

        elif 'open youtube' in query:  # Command to open YouTube
            webbrowser.open('https://www.youtube.com')

        elif 'open google' in query:  # Command to open Google
            webbrowser.open('https://www.google.com')

        elif 'tell me the time' in query:  # Command to tell the current time
            strTime = datetime.datetime.now().strftime("%H:%M:%S")  # Get current time
            speak(f"My dear friend, the time is {strTime}")

        elif 'what is the weather in' in query:  # Command to get weather information
            city = query.replace("what is the weather in", "").strip()  # Extract city name
            get_weather(city)  # Fetch and announce weather for the city

        elif 'open linkedin' in query:  # Command to open LinkedIn
            webbrowser.open("https://www.linkedin.com/feed/")
