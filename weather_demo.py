#!/usr/bin/env python3
"""
Weather Fetcher Demo Script
Shows how to use the weather fetcher programmatically
"""

from weather_fetcher import WeatherFetcher


def main():
    """Demonstrate weather fetcher for different locations"""
    fetcher = WeatherFetcher()
    
    print("🌤️  Weather Fetcher Demo")
    print("=" * 60)
    print()
    
    # Demo 1: Auto-detect location
    print("1️⃣  Auto-detecting your location...")
    fetcher.display_weather_report()
    print()
    
    # Demo 2: Specific cities
    cities = ["London", "Tokyo", "New York", "Sydney", "Cairo"]
    
    for i, city in enumerate(cities, 2):
        print(f"{i}️⃣  Getting weather for {city}...")
        try:
            fetcher.display_weather_report(city)
        except Exception as e:
            print(f"❌ Could not get weather for {city}: {e}")
        print()
    
    # Demo 3: Programmatic usage example
    print("🔧 Programmatic Usage Example:")
    print("-" * 40)
    try:
        data = fetcher.get_temperature_in_all_formats("Paris")
        temps = data["temperatures"]
        location = data["location"]
        
        print(f"Location: {location['name']}, {location.get('country', '')}")
        print(f"Temperature: {temps['celsius']:.1f}°C / {temps['fahrenheit']:.1f}°F / {temps['kelvin']:.1f}K")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("Demo complete! Use 'python3 weather_fetcher.py' for interactive mode.")


if __name__ == "__main__":
    main() 