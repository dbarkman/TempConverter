#!/usr/bin/env python3
"""
Weather Fetcher for Temperature Converter POC
Fetches local temperature and converts to all three formats.
"""

import json
import urllib.request
import urllib.parse
from temp_converter import TempConverter


class WeatherFetcher:
    """Fetches weather data and converts temperatures"""
    
    def __init__(self):
        self.converter = TempConverter()
        self.base_url = "https://api.open-meteo.com/v1"
    
    def get_location_coordinates(self, location=None):
        """
        Get coordinates for a location using Open-Meteo's geocoding
        If no location provided, tries to detect automatically
        """
        if location:
            # Use geocoding API to get coordinates for specified location
            geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
            params = {"name": location, "count": 1, "language": "en", "format": "json"}
            url = f"{geocoding_url}?{urllib.parse.urlencode(params)}"
            
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = json.loads(response.read().decode())
                    if data.get("results"):
                        result = data["results"][0]
                        return {
                            "latitude": result["latitude"],
                            "longitude": result["longitude"],
                            "name": result["name"],
                            "country": result.get("country", ""),
                            "admin1": result.get("admin1", "")
                        }
            except Exception as e:
                print(f"Error getting coordinates for {location}: {e}")
                return None
        
        # If no location specified, try IP-based detection
        try:
            # Simple IP geolocation (basic, but works for demo)
            with urllib.request.urlopen("http://ip-api.com/json/?fields=lat,lon,city,regionName,country", timeout=10) as response:
                data = json.loads(response.read().decode())
                if data.get("lat") and data.get("lon"):
                    return {
                        "latitude": data["lat"],
                        "longitude": data["lon"],
                        "name": data.get("city", "Unknown"),
                        "country": data.get("country", ""),
                        "admin1": data.get("regionName", "")
                    }
        except Exception as e:
            print(f"Error detecting location: {e}")
            
        # Fallback to a default location (San Francisco)
        print("Using default location: San Francisco, CA")
        return {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "name": "San Francisco",
            "country": "United States",
            "admin1": "California"
        }
    
    def fetch_current_temperature(self, location=None):
        """
        Fetch current temperature for a location
        
        Args:
            location (str, optional): Location name (e.g., "New York", "London")
                                    If None, tries to detect automatically
        
        Returns:
            dict: Weather data with temperature and location info
        """
        # Get coordinates
        coords = self.get_location_coordinates(location)
        if not coords:
            raise ValueError(f"Could not find coordinates for location: {location}")
        
        # Fetch current weather
        params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "timezone": "auto"
        }
        
        url = f"{self.base_url}/forecast?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                
                current = data.get("current", {})
                temperature_c = current.get("temperature_2m")
                
                if temperature_c is None:
                    raise ValueError("Temperature data not available")
                
                return {
                    "location": coords,
                    "temperature_celsius": temperature_c,
                    "humidity": current.get("relative_humidity_2m"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "time": current.get("time"),
                    "timezone": data.get("timezone")
                }
                
        except Exception as e:
            raise ValueError(f"Error fetching weather data: {e}")
    
    def get_temperature_in_all_formats(self, location=None):
        """
        Get current temperature in Celsius, Fahrenheit, and Kelvin
        
        Args:
            location (str, optional): Location name
            
        Returns:
            dict: Temperature in all three formats with location info
        """
        weather_data = self.fetch_current_temperature(location)
        temp_c = weather_data["temperature_celsius"]
        
        # Convert to other formats
        temp_f = self.converter.convert(temp_c, 'C', 'F')
        temp_k = self.converter.convert(temp_c, 'C', 'K')
        
        return {
            "location": weather_data["location"],
            "temperatures": {
                "celsius": temp_c,
                "fahrenheit": temp_f,
                "kelvin": temp_k
            },
            "additional_info": {
                "humidity": weather_data.get("humidity"),
                "wind_speed": weather_data.get("wind_speed"),
                "time": weather_data.get("time")
            }
        }
    
    def display_weather_report(self, location=None):
        """
        Display a nicely formatted weather report with temperatures in all formats
        """
        try:
            data = self.get_temperature_in_all_formats(location)
            
            loc = data["location"]
            temps = data["temperatures"]
            info = data["additional_info"]
            
            print("🌡️  Current Weather Report")
            print("=" * 50)
            
            # Location info
            location_name = loc["name"]
            if loc.get("admin1"):
                location_name += f", {loc['admin1']}"
            if loc.get("country"):
                location_name += f", {loc['country']}"
            
            print(f"📍 Location: {location_name}")
            print(f"🕐 Time: {info.get('time', 'Unknown')}")
            print()
            
            # Temperature in all formats
            print("🌡️  Temperature:")
            print(f"   • {temps['celsius']:.1f}°C (Celsius)")
            print(f"   • {temps['fahrenheit']:.1f}°F (Fahrenheit)")
            print(f"   • {temps['kelvin']:.1f}K (Kelvin)")
            print()
            
            # Additional weather info
            if info.get("humidity"):
                print(f"💧 Humidity: {info['humidity']}%")
            if info.get("wind_speed"):
                print(f"💨 Wind Speed: {info['wind_speed']} km/h")
            
            print("=" * 50)
            print("Data provided by Open-Meteo.com")
            
        except Exception as e:
            print(f"❌ Error fetching weather: {e}")
            print("Please check your internet connection or try specifying a location.")


def main():
    """Interactive weather fetcher"""
    print("🌤️  Weather Temperature Fetcher")
    print("=" * 40)
    print("Get current temperature in all three formats!")
    print("Leave location blank to auto-detect your location.")
    print("Type 'quit' to exit")
    print()
    
    fetcher = WeatherFetcher()
    
    while True:
        try:
            location_input = input("Enter location (or press Enter for auto-detect): ").strip()
            
            if location_input.lower() == 'quit':
                print("Goodbye! 👋")
                break
            
            location = location_input if location_input else None
            
            print("\nFetching weather data...")
            fetcher.display_weather_report(location)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print()


if __name__ == "__main__":
    main() 