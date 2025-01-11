-- Create the database (optional step if your system requires it)
CREATE DATABASE WeatherForecastDB;

-- Switch to the database
USE WeatherForecastDB;

-- Create a table to store city information
CREATE TABLE Cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL
);

-- Create a table to store weather forecasts
CREATE TABLE Forecasts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    forecast_date DATE NOT NULL,
    temperature DECIMAL(5, 2) NOT NULL,
    weather_description VARCHAR(255) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES Cities(id) ON DELETE CASCADE
);

-- Insert sample city data
INSERT INTO Cities (name, country, latitude, longitude)
VALUES
    ('New York', 'USA', 40.7128, -74.0060),
    ('Mumbai', 'India', 19.0760, 72.8777),
    ('Tokyo', 'Japan', 35.6895, 139.6917);

-- Insert sample forecast data
INSERT INTO Forecasts (city_id, forecast_date, temperature, weather_description)
VALUES
    (1, '2025-01-12', 5.3, 'Clear sky'),
    (2, '2025-01-12', 25.4, 'Scattered clouds'),
    (3, '2025-01-12', 10.8, 'Rain');
