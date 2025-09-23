import streamlit as st
import requests
import openai
import re

API_KEY = "b9d25f086ac546bb85080340252204"
BASE_URL = "http://api.weatherapi.com/v1/"
# Main function to run the Streamlit app
def get_weather(location, date=None):
    if date:
        endpoint = 'history.json'
        params = {'key': API_KEY, 'q': location, 'dt': date}
    else:
        endpoint = 'current.json'
        params = {'key': API_KEY, 'q': location}

    response = requests.get(BASE_URL + endpoint, params=params)
    data = response.json()

    if "error" in data:
        return f"❌ Error: {data['error']['message']}"

    if date:
        weather = data['forecast']['forecastday'][0]['day']
        return f"📅 Weather in {location} on {date}:\n☁ {weather['condition']['text']}, 🌡 Avg Temp: {weather['avgtemp_c']}°C"
    else:
        weather = data['current']
        return f"📍 Current weather in {location}:\n☁ {weather['condition']['text']}, 🌡 Temp: {weather['temp_c']}°C"
def main():
    # Sidebar configuration
    st.sidebar.title("⛅ Weather Forecast AI")
    user_query = st.sidebar.text_input("Ask me about the weather:")

    if user_query:
        # Simple parsing for date and location
        date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', user_query)
        today_keywords = ['today', 'now', 'current']
        # Button to fetch and display weather data
        if any(word in user_query.lower() for word in today_keywords):
            location = st.sidebar.text_input("Enter location:")
            if location and st.sidebar.button("Get Weather"):
                result = get_weather(location)
                st.write(result)
        elif date_match:
            location = st.sidebar.text_input("Enter location:")
            selected_date = date_match.group(1)
            if location and st.sidebar.button("Get Weather"):
                result = get_weather(location, selected_date)
                st.write(result)
        else:
            st.write("📩 Please mention if you want the weather for today or on a specific date (YYYY-MM-DD).")

    openai_api_key = "sk-proj-zI9Ena4htidPwWtD5zmw75MVIIZEd"

if __name__ == "__main__":
    main()