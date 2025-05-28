# Temperature Converter POC

A simple proof-of-concept temperature converter in Python that converts between Celsius, Fahrenheit, and Kelvin. **Now with live weather data integration!**

## Features

- Convert between Celsius (°C), Fahrenheit (°F), and Kelvin (K)
- Interactive command-line interface
- **🆕 Fetch real-time local temperature from weather services**
- **🆕 Auto-detect your location or specify any city worldwide**
- **🆕 Display current temperature in all three formats simultaneously**
- Input validation (prevents temperatures below absolute zero)
- Case-insensitive unit input
- Comprehensive error handling
- Unit tests included

## Files

- `temp_converter.py` - Main temperature converter module
- `test_temp_converter.py` - Unit tests
- `example_usage.py` - Usage examples
- **🆕 `weather_fetcher.py` - Live weather data integration**
- **🆕 `weather_demo.py` - Weather fetcher demonstration**
- **🆕 `test_weather_fetcher.py` - Weather fetcher tests (unit + integration)**
- `README.md` - This documentation

## Usage

### 🌤️ Weather Mode (NEW!)

Get real-time temperature in all three formats:

```bash
python3 weather_fetcher.py
```

Example output:
```
🌡️  Current Weather Report
==================================================
📍 Location: Gilbert, Arizona, United States
🕐 Time: 2025-05-28T12:00

🌡️  Temperature:
   • 36.0°C (Celsius)
   • 96.8°F (Fahrenheit)
   • 309.1K (Kelvin)

💧 Humidity: 7%
💨 Wind Speed: 2.9 km/h
==================================================
```

### Weather Demo

See weather for multiple cities:

```bash
python3 weather_demo.py
```

### Programmatic Weather Usage

```python
from weather_fetcher import WeatherFetcher

fetcher = WeatherFetcher()

# Auto-detect your location
data = fetcher.get_temperature_in_all_formats()
temps = data["temperatures"]
print(f"Current temp: {temps['celsius']:.1f}°C / {temps['fahrenheit']:.1f}°F / {temps['kelvin']:.1f}K")

# Specific location
data = fetcher.get_temperature_in_all_formats("London")
```

### Interactive Mode

Run the main script for an interactive temperature conversion session:

```bash
python3 temp_converter.py
```

Example session:
```
🌡️  Temperature Converter POC
========================================
Supported units: C (Celsius), F (Fahrenheit), K (Kelvin)
Type 'quit' to exit

Enter temperature (e.g., '25' or 'quit'): 25
From unit (C/F/K): C
To unit (C/F/K): F
Result: 25.0° C = 77.00° F
----------------------------------------
```

### Programmatic Usage

```python
from temp_converter import TempConverter

converter = TempConverter()

# Convert 25°C to Fahrenheit
fahrenheit = converter.convert(25, 'C', 'F')
print(f"25°C = {fahrenheit}°F")  # Output: 25°C = 77.0°F

# Convert 32°F to Celsius
celsius = converter.convert(32, 'F', 'C')
print(f"32°F = {celsius}°C")  # Output: 32°F = 0.0°C
```

### Run Examples

See various conversion examples:

```bash
python3 example_usage.py
```

### Run Tests

Execute the test suite:

```bash
# Test core temperature converter
python3 test_temp_converter.py

# Test weather functionality (includes real API integration)
python3 test_weather_fetcher.py

# Run all tests
python3 test_temp_converter.py && python3 test_weather_fetcher.py
```

## Weather Data Integration

The weather fetcher uses:
- **Open-Meteo API** - Free, no API key required
- **Automatic location detection** via IP geolocation
- **Global city search** - Works with any city name
- **Real-time data** - Updated hourly
- **Additional info** - Humidity, wind speed, timestamps

### Supported Weather Features

- ✅ Current temperature in all three formats
- ✅ Automatic location detection
- ✅ Manual location search (any city worldwide)
- ✅ Additional weather metrics (humidity, wind)
- ✅ Timezone-aware timestamps
- ✅ Robust error handling with fallbacks

## Supported Conversions

The converter supports all combinations between:
- **Celsius (C)** - Standard metric temperature scale
- **Fahrenheit (F)** - Imperial temperature scale
- **Kelvin (K)** - Absolute temperature scale

## Conversion Formulas

- **Celsius to Fahrenheit**: `F = (C × 9/5) + 32`
- **Fahrenheit to Celsius**: `C = (F - 32) × 5/9`
- **Celsius to Kelvin**: `K = C + 273.15`
- **Kelvin to Celsius**: `C = K - 273.15`

## Error Handling

The converter validates input and prevents:
- Invalid temperature units
- Temperatures below absolute zero:
  - Kelvin: < 0 K
  - Celsius: < -273.15°C
  - Fahrenheit: < -459.67°F

## Requirements

- Python 3.6 or higher
- Internet connection (for weather features)
- No external dependencies required

## Design Principles

This POC follows KISS (Keep It Simple, Stupid) principles:
- Simple, straightforward implementation
- Clear error messages
- Comprehensive but not overly complex testing
- Easy to understand and maintain code
- Pragmatic approach focused on core functionality

## Quick Start Examples

### Just Temperature Conversion
```bash
python3 temp_converter.py
```

### Live Weather + Conversion
```bash
python3 weather_fetcher.py
```

### See Multiple Cities
```bash
python3 weather_demo.py
```

### Run Tests
```bash
python3 test_temp_converter.py
```

## Future Enhancements

Potential improvements for a production version:
- Web interface with weather maps
- Batch conversion from file
- Weather forecasts (not just current)
- Additional temperature scales (Rankine, Réaumur)
- Configuration file support
- Logging capabilities
- Weather alerts and notifications

## Testing

The POC includes comprehensive testing:

### Temperature Converter Tests (`test_temp_converter.py`)
- ✅ All conversion formulas (C↔F, C↔K, F↔K)
- ✅ Input validation and error handling
- ✅ Edge cases (absolute zero, round-trip accuracy)
- ✅ Case-insensitive unit handling

### Weather Fetcher Tests (`test_weather_fetcher.py`)
- ✅ **Unit Tests** - Mocked API calls for consistent testing
- ✅ **Integration Tests** - Real API calls (when internet available)
- ✅ Location detection (auto-detect and manual search)
- ✅ Temperature conversion integration
- ✅ Error handling (network issues, invalid locations, missing data)
- ✅ Fallback mechanisms for robust operation
- ✅ Output formatting verification

### Test Results Summary
- **18 total tests** (9 temperature converter + 9 weather fetcher + 1 integration)
- **100% pass rate** ✅
- **Mocked external dependencies** for reliable unit testing
- **Real-world integration testing** when network is available 