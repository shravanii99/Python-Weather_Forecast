import pymysql
import requests
import os

# Database connection details
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_NAME = 'WeatherForecastDB'

# OpenWeatherMap API details
API_KEY = os.environ.get('OPENWEATHER_API_KEY')  # Set your API key in environment variables
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Database connection function
def connect_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to fetch weather data from the API
def fetch_weather(city_name):
    params = {'q': city_name, 'units': 'metric', 'appid': API_KEY}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data for {city_name}. Status code: {response.status_code}")
        return None

# Function to insert weather data into the database
def save_weather_to_db(city_name, weather_data):
    try:
        connection = connect_db()
        with connection.cursor() as cursor:
            # Get city ID
            cursor.execute("SELECT id FROM Cities WHERE name = %s", (city_name,))
            city = cursor.fetchone()
            
            if not city:
                print(f"City {city_name} not found in database.")
                return
            
            city_id = city['id']
            forecast_date = weather_data['dt']  # Epoch timestamp
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            
            # Insert forecast data
            sql = """
            INSERT INTO Forecasts (city_id, forecast_date, temperature, weather_description)
            VALUES (%s, FROM_UNIXTIME(%s), %s, %s)
            """
            cursor.execute(sql, (city_id, forecast_date, temperature, description))
            connection.commit()
            print(f"Weather data for {city_name} saved successfully.")
    finally:
        connection.close()

# Main function to run the program
def main():
    city_name = input("Enter city name: ").strip()
    if not API_KEY:
        print("Error: OpenWeatherMap API key not found.")
        return
    
    weather_data = fetch_weather(city_name)
    if weather_data:
        save_weather_to_db(city_name, weather_data)

if __name__ == "__main__":
    main()
