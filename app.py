from datetime import datetime
import streamlit as st
import requests
from transformers import pipeline

def get_weather_data(city, weather_api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get(complete_url)
    return response.json()

generator = pipeline("text2text-generation", model="google/flan-t5-small", device=-1)
def generate_weather_description(data):
    try:
        temperature = data['main']['temp'] - 273.15
        description = data['weather'][0]['description']
        prompt = f"The current weather in your city is {description} with a temperature of {temperature:.1f}°C."

        result = generator(prompt, max_length=60)[0]['generated_text']
        return result
    except Exception as e:
        return str(e)

def get_weekly_forecast(weather_api_key, lat, lon):
    complete_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={weather_api_key}"
    response = requests.get(complete_url)
    return response.json()

def display_weekly_forecast(data):
    try:
        st.write("===================================================================================")
        st.write("### Weekly Weather Forecast")
        displayed_dates = set()

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("", "Day")
        
        with c2:
            st.metric("", "Desc")
        
        with c3:
            st.metric("", "Min_temp")

        with c4:
            st.metric("", "Max_temp")

        for day in data['list']:
            
            date = datetime.fromtimestamp(day['dt']).strftime('%A, %B %d')

            if date not in displayed_dates:
                displayed_dates.add(date)

                min_temp = day['main']['temp_min'] - 273.15
                max_temp = day['main']['temp_max'] - 273.15
                description = day['weather'][0]['description']

                with c1:
                    st.write(f"{date}")

                with c2:
                    st.write(f"{description.capitalize()}")
                
                with c3:
                    st.write(f"{min_temp:.1f}°C")
                
                with c4:
                    st.write(f"{max_temp:.1f}°C")
    except Exception as e:
        st.error("Error in displaying weekly forecast: " + str(e))


#MAIN FUNCTION TO RUN THE STREAMLIT APP
def main():

    st.sidebar.title("⛅ Weather Forecast AI")
    city = st.sidebar.text_input("Enter City Name:")

    #API KEYS
    weather_api_key = "2bf4686b58e818560cb0aa13c5fd0722"

    #BUTTON TO FETCH AND DISPLAY WEATHER DATA
    submit = st.sidebar.button("Get Weather")

    if submit:
        st.title("Weather Updates for " + city + " is:")
        with st.spinner('Fetching weather data.....'):
            weather_data = get_weather_data(city, weather_api_key)
            print(weather_data)

            if weather_data.get("cod") != 404:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature 🌡", f"{weather_data['main']['temp'] - 273.15:.2f} °C")
                    st.metric("Humidity 💧", f"{weather_data['main']['humidity']}%")
                with col2:
                    st.metric("Pressure 🌌", f"{weather_data['main']['pressure']} hPa")
                    st.metric("Wind Speed 🌫", f"{weather_data['wind']['speed']} m/s")

                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']
            
                weather_description = generate_weather_description(weather_data)
                st.subheader("AI Weather Summary")
                st.write(weather_description)

                #FUNCTION TO GET WEEKLY FORECAST
                forecast_data = get_weekly_forecast(weather_api_key, lat, lon)

                print(forecast_data)
                if forecast_data.get("cod") != "404":
                    display_weekly_forecast(forecast_data)
                else:
                    st.error("Error fetching!")

            else:
                st.error("‼Error‼")




if __name__ == "__main__":
    main()
    


    