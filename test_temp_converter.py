#!/usr/bin/env python3
"""
Simple tests for the Temperature Converter POC
"""

import unittest
from temp_converter import TempConverter


class TestTempConverter(unittest.TestCase):
    """Test cases for TempConverter class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.converter = TempConverter()
    
    def test_celsius_to_fahrenheit(self):
        """Test Celsius to Fahrenheit conversion"""
        # Freezing point of water
        self.assertAlmostEqual(TempConverter.celsius_to_fahrenheit(0), 32.0, places=2)
        # Boiling point of water
        self.assertAlmostEqual(TempConverter.celsius_to_fahrenheit(100), 212.0, places=2)
        # Room temperature
        self.assertAlmostEqual(TempConverter.celsius_to_fahrenheit(25), 77.0, places=2)
    
    def test_fahrenheit_to_celsius(self):
        """Test Fahrenheit to Celsius conversion"""
        # Freezing point of water
        self.assertAlmostEqual(TempConverter.fahrenheit_to_celsius(32), 0.0, places=2)
        # Boiling point of water
        self.assertAlmostEqual(TempConverter.fahrenheit_to_celsius(212), 100.0, places=2)
        # Room temperature
        self.assertAlmostEqual(TempConverter.fahrenheit_to_celsius(77), 25.0, places=2)
    
    def test_celsius_to_kelvin(self):
        """Test Celsius to Kelvin conversion"""
        # Absolute zero
        self.assertAlmostEqual(TempConverter.celsius_to_kelvin(-273.15), 0.0, places=2)
        # Freezing point of water
        self.assertAlmostEqual(TempConverter.celsius_to_kelvin(0), 273.15, places=2)
        # Room temperature
        self.assertAlmostEqual(TempConverter.celsius_to_kelvin(25), 298.15, places=2)
    
    def test_kelvin_to_celsius(self):
        """Test Kelvin to Celsius conversion"""
        # Absolute zero
        self.assertAlmostEqual(TempConverter.kelvin_to_celsius(0), -273.15, places=2)
        # Freezing point of water
        self.assertAlmostEqual(TempConverter.kelvin_to_celsius(273.15), 0.0, places=2)
        # Room temperature
        self.assertAlmostEqual(TempConverter.kelvin_to_celsius(298.15), 25.0, places=2)
    
    def test_convert_method(self):
        """Test the general convert method"""
        # Same unit conversion
        self.assertEqual(self.converter.convert(25, 'C', 'C'), 25)
        
        # Cross conversions
        self.assertAlmostEqual(self.converter.convert(0, 'C', 'F'), 32.0, places=2)
        self.assertAlmostEqual(self.converter.convert(32, 'F', 'C'), 0.0, places=2)
        self.assertAlmostEqual(self.converter.convert(0, 'C', 'K'), 273.15, places=2)
        self.assertAlmostEqual(self.converter.convert(273.15, 'K', 'C'), 0.0, places=2)
    
    def test_case_insensitive_units(self):
        """Test that unit input is case insensitive"""
        result1 = self.converter.convert(25, 'c', 'f')
        result2 = self.converter.convert(25, 'C', 'F')
        self.assertEqual(result1, result2)
    
    def test_invalid_units(self):
        """Test error handling for invalid units"""
        with self.assertRaises(ValueError):
            self.converter.convert(25, 'X', 'C')
        
        with self.assertRaises(ValueError):
            self.converter.convert(25, 'C', 'Y')
    
    def test_absolute_zero_validation(self):
        """Test validation for temperatures below absolute zero"""
        # Negative Kelvin should raise error
        with self.assertRaises(ValueError):
            self.converter.convert(-10, 'K', 'C')
        
        # Temperature below absolute zero in Celsius should raise error
        with self.assertRaises(ValueError):
            self.converter.convert(-300, 'C', 'F')
        
        # Temperature below absolute zero in Fahrenheit should raise error
        with self.assertRaises(ValueError):
            self.converter.convert(-500, 'F', 'C')
    
    def test_round_trip_conversions(self):
        """Test that converting back and forth gives original value"""
        original_temp = 25.0
        
        # C -> F -> C
        fahrenheit = self.converter.convert(original_temp, 'C', 'F')
        back_to_celsius = self.converter.convert(fahrenheit, 'F', 'C')
        self.assertAlmostEqual(original_temp, back_to_celsius, places=10)
        
        # C -> K -> C
        kelvin = self.converter.convert(original_temp, 'C', 'K')
        back_to_celsius = self.converter.convert(kelvin, 'K', 'C')
        self.assertAlmostEqual(original_temp, back_to_celsius, places=10)


if __name__ == '__main__':
    print("Running Temperature Converter Tests...")
    unittest.main(verbosity=2) 