#!/usr/bin/env python3
"""
Example usage of the Temperature Converter POC
"""

from temp_converter import TempConverter


def main():
    """Demonstrate temperature converter usage"""
    print("🌡️  Temperature Converter Examples")
    print("=" * 50)
    
    converter = TempConverter()
    
    # Example conversions
    examples = [
        (0, 'C', 'F', "Water freezing point"),
        (100, 'C', 'F', "Water boiling point"),
        (32, 'F', 'C', "Water freezing point"),
        (212, 'F', 'C', "Water boiling point"),
        (25, 'C', 'K', "Room temperature"),
        (298.15, 'K', 'C', "Room temperature"),
        (98.6, 'F', 'C', "Human body temperature"),
        (-40, 'C', 'F', "Special point where C and F are equal"),
    ]
    
    for temp, from_unit, to_unit, description in examples:
        try:
            result = converter.convert(temp, from_unit, to_unit)
            print(f"{description}:")
            print(f"  {temp}° {from_unit} = {result:.2f}° {to_unit}")
            print()
        except ValueError as e:
            print(f"Error converting {temp}° {from_unit} to {to_unit}: {e}")
            print()
    
    # Demonstrate error handling
    print("Error Handling Examples:")
    print("-" * 30)
    
    error_examples = [
        (-300, 'C', 'F', "Temperature below absolute zero"),
        (25, 'X', 'C', "Invalid source unit"),
        (25, 'C', 'Y', "Invalid target unit"),
    ]
    
    for temp, from_unit, to_unit, description in error_examples:
        try:
            result = converter.convert(temp, from_unit, to_unit)
            print(f"{description}: {temp}° {from_unit} = {result:.2f}° {to_unit}")
        except ValueError as e:
            print(f"{description}: ❌ {e}")
        print()


if __name__ == "__main__":
    main() 