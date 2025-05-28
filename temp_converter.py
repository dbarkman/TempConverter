#!/usr/bin/env python3
"""
Temperature Converter POC
A simple utility to convert temperatures between Celsius, Fahrenheit, and Kelvin.
"""

class TempConverter:
    """Simple temperature converter class"""
    
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        """Convert Fahrenheit to Celsius"""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def celsius_to_kelvin(celsius):
        """Convert Celsius to Kelvin"""
        return celsius + 273.15
    
    @staticmethod
    def kelvin_to_celsius(kelvin):
        """Convert Kelvin to Celsius"""
        return kelvin - 273.15
    
    @staticmethod
    def fahrenheit_to_kelvin(fahrenheit):
        """Convert Fahrenheit to Kelvin"""
        celsius = TempConverter.fahrenheit_to_celsius(fahrenheit)
        return TempConverter.celsius_to_kelvin(celsius)
    
    @staticmethod
    def kelvin_to_fahrenheit(kelvin):
        """Convert Kelvin to Fahrenheit"""
        celsius = TempConverter.kelvin_to_celsius(kelvin)
        return TempConverter.celsius_to_fahrenheit(celsius)
    
    @classmethod
    def convert(cls, temperature, from_unit, to_unit):
        """
        Convert temperature from one unit to another
        
        Args:
            temperature (float): Temperature value to convert
            from_unit (str): Source unit ('C', 'F', 'K')
            to_unit (str): Target unit ('C', 'F', 'K')
            
        Returns:
            float: Converted temperature
            
        Raises:
            ValueError: If units are invalid or temperature is below absolute zero
        """
        from_unit = from_unit.upper()
        to_unit = to_unit.upper()
        
        # Validate units
        valid_units = ['C', 'F', 'K']
        if from_unit not in valid_units or to_unit not in valid_units:
            raise ValueError(f"Units must be one of: {valid_units}")
        
        # Validate temperature (basic absolute zero checks)
        if from_unit == 'K' and temperature < 0:
            raise ValueError("Temperature in Kelvin cannot be negative")
        if from_unit == 'C' and temperature < -273.15:
            raise ValueError("Temperature in Celsius cannot be below -273.15°C")
        if from_unit == 'F' and temperature < -459.67:
            raise ValueError("Temperature in Fahrenheit cannot be below -459.67°F")
        
        # If same unit, return as is
        if from_unit == to_unit:
            return temperature
        
        # Define conversion mapping
        conversions = {
            ('C', 'F'): cls.celsius_to_fahrenheit,
            ('F', 'C'): cls.fahrenheit_to_celsius,
            ('C', 'K'): cls.celsius_to_kelvin,
            ('K', 'C'): cls.kelvin_to_celsius,
            ('F', 'K'): cls.fahrenheit_to_kelvin,
            ('K', 'F'): cls.kelvin_to_fahrenheit,
        }
        
        conversion_func = conversions.get((from_unit, to_unit))
        if conversion_func:
            return conversion_func(temperature)
        else:
            raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported")


def main():
    """Interactive command-line interface for temperature conversion"""
    print("🌡️  Temperature Converter POC")
    print("=" * 40)
    print("Supported units: C (Celsius), F (Fahrenheit), K (Kelvin)")
    print("Type 'quit' to exit")
    print()
    
    converter = TempConverter()
    
    while True:
        try:
            # Get temperature input
            temp_input = input("Enter temperature (e.g., '25' or 'quit'): ").strip()
            if temp_input.lower() == 'quit':
                print("Goodbye! 👋")
                break
            
            temperature = float(temp_input)
            
            # Get source unit
            from_unit = input("From unit (C/F/K): ").strip()
            
            # Get target unit
            to_unit = input("To unit (C/F/K): ").strip()
            
            # Convert
            result = converter.convert(temperature, from_unit, to_unit)
            
            # Display result
            print(f"Result: {temperature}° {from_unit.upper()} = {result:.2f}° {to_unit.upper()}")
            print("-" * 40)
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            print("-" * 40)
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("-" * 40)


if __name__ == "__main__":
    main() 