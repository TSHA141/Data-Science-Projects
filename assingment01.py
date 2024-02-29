#All the necessary module imports,the necessary pip files have been downloaded
import requests
from datetime import datetime, timedelta
import statistics
import json

# This function is meant to fetch data for the last 7 days
def get_historical_weather_data(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/history/city"
    params = {
        'q': city,
        'appid': api_key,
        'cnt': 7  
    }

    #Here we are raising any error that might come from the code
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        historical_data = response.json()
        return historical_data['hourly']
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
    return None

#Defining the function get_weather_data for the city info and api key
def get_weather_data(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key
        }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
    return None



def calculate_statistics(temperature_data):
    if not temperature_data:
        return None

    temperatures = [entry['temp'] for entry in temperature_data]
    avg_temp = statistics.mean(temperatures)
    median_temp = statistics.median(temperatures)
    mode_temp = statistics.mode(temperatures)

    return {
        'average_temperature': avg_temp,
        'median_temperature': median_temp,
        'mode_temperature': mode_temp
    }

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

#We create and thereafter call the main function to consolidate everything
def main():
    #This is the API key I created with openweather
    api_key = '3a597ca2e5e5404be6380a184d0bfb3e' 
    #We now ask the user to input a valid city the .strip is used to remove any accidental white spaces
    city = input("Enter the name of the city: ").strip()

    #This is in case the City name is incorrect, perhaps misspelled
    if not city:
        print("This city name is not valid. Exiting.")
        return

    #We are calling the weather_data function into action, withe city and api_key parameters
    current_weather_data = get_weather_data(city, api_key)

    #Now we are calling the historical_wether_data for the requested 7 day period
    historical_weather_data = get_historical_weather_data(city, api_key)

    #This if statement will print temp,humidity and description(e.g.cloudy)
    if current_weather_data:
        print("\nCurrent Weather Data:")
        print(f"Temperature: {current_weather_data['main']['temp']} °C")
        print(f"Humidity: {current_weather_data['main']['humidity']}%")
        print(f"Description: {current_weather_data['weather'][0]['description']}\n")

    #This is meant to display the stats for 7 days
    if historical_weather_data:
        print("\nHistorical Weather Data for the Last 7 Days:")
        for entry in historical_weather_data:
            timestamp = datetime.utcfromtimestamp(entry['dt'])
            print(f"{timestamp}: {entry['temp']} °C")

        stats = calculate_statistics(historical_weather_data)
        if stats:
            print("\nStatistical Analysis:")
            print(f"Average Temperature: {stats['average_temperature']} °C")
            print(f"Median Temperature: {stats['median_temperature']} °C")
            print(f"Mode Temperature: {stats['mode_temperature']} °C")

            save_to_file({
                'city': city,
                'historical_data': historical_weather_data,
                'statistics': stats
            }, 'weather_data.json')
            print("Data saved to 'weather_data.json'.")
        else:
            print("Unable to calculate statistics.")

if __name__ == "__main__": #This statement checks if the script is being run as the main program
    main() #calling the main function and running everything
