# Temperature Converter POC

A simple proof-of-concept temperature converter in Python that converts between Celsius, Fahrenheit, and Kelvin.

## Features

- Convert between Celsius (°C), Fahrenheit (°F), and Kelvin (K)
- Interactive command-line interface
- Input validation (prevents temperatures below absolute zero)
- Case-insensitive unit input
- Comprehensive error handling
- Unit tests included

## Files

- `temp_converter.py` - Main temperature converter module
- `test_temp_converter.py` - Unit tests
- `example_usage.py` - Usage examples
- `README.md` - This documentation

## Usage

### Interactive Mode

Run the main script for an interactive temperature conversion session:

```bash
python temp_converter.py
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
python example_usage.py
```

### Run Tests

Execute the test suite:

```bash
python test_temp_converter.py
```

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
- No external dependencies required

## Design Principles

This POC follows KISS (Keep It Simple, Stupid) principles:
- Simple, straightforward implementation
- Clear error messages
- Comprehensive but not overly complex testing
- Easy to understand and maintain code
- Pragmatic approach focused on core functionality

## Future Enhancements

Potential improvements for a production version:
- Web interface
- Batch conversion from file
- Additional temperature scales (Rankine, Réaumur)
- Configuration file support
- Logging capabilities 