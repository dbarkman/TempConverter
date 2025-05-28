#!/usr/bin/env python3
"""
Tests for the Weather Fetcher POC
"""

import unittest
import json
from unittest.mock import patch, MagicMock
from weather_fetcher import WeatherFetcher


class TestWeatherFetcher(unittest.TestCase):
    """Test cases for WeatherFetcher class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.fetcher = WeatherFetcher()
        
        # Sample API responses for mocking
        self.sample_geocoding_response = {
            "results": [{
                "latitude": 40.7128,
                "longitude": -74.0060,
                "name": "New York",
                "country": "United States",
                "admin1": "New York"
            }]
        }
        
        self.sample_weather_response = {
            "current": {
                "time": "2025-05-28T12:00",
                "temperature_2m": 25.0,
                "relative_humidity_2m": 60,
                "wind_speed_10m": 10.5,
                "weather_code": 0
            },
            "timezone": "America/New_York"
        }
        
        self.sample_ip_location_response = {
            "lat": 37.7749,
            "lon": -122.4194,
            "city": "San Francisco",
            "regionName": "California",
            "country": "United States"
        }
    
    def test_temperature_converter_integration(self):
        """Test that weather fetcher correctly integrates with temperature converter"""
        # Test with known temperature value
        test_temp_c = 25.0
        
        # Mock the weather API response
        with patch.object(self.fetcher, 'fetch_current_temperature') as mock_fetch:
            mock_fetch.return_value = {
                "location": {"name": "Test City", "country": "Test Country"},
                "temperature_celsius": test_temp_c,
                "humidity": 60,
                "wind_speed": 10.5,
                "time": "2025-05-28T12:00"
            }
            
            result = self.fetcher.get_temperature_in_all_formats("Test City")
            
            # Verify the conversion is correct
            temps = result["temperatures"]
            self.assertAlmostEqual(temps["celsius"], 25.0, places=1)
            self.assertAlmostEqual(temps["fahrenheit"], 77.0, places=1)  # 25°C = 77°F
            self.assertAlmostEqual(temps["kelvin"], 298.15, places=1)    # 25°C = 298.15K
    
    @patch('urllib.request.urlopen')
    def test_get_location_coordinates_with_city(self, mock_urlopen):
        """Test getting coordinates for a specific city"""
        # Mock the geocoding API response
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = json.dumps(self.sample_geocoding_response)
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = self.fetcher.get_location_coordinates("New York")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "New York")
        self.assertEqual(result["latitude"], 40.7128)
        self.assertEqual(result["longitude"], -74.0060)
        self.assertEqual(result["country"], "United States")
    
    @patch('urllib.request.urlopen')
    def test_get_location_coordinates_auto_detect(self, mock_urlopen):
        """Test automatic location detection via IP"""
        # Mock the IP geolocation API response
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = json.dumps(self.sample_ip_location_response)
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = self.fetcher.get_location_coordinates()
        
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "San Francisco")
        self.assertEqual(result["latitude"], 37.7749)
        self.assertEqual(result["longitude"], -122.4194)
    
    @patch('urllib.request.urlopen')
    def test_fetch_current_temperature(self, mock_urlopen):
        """Test fetching current temperature"""
        # Mock both geocoding and weather API responses
        responses = [
            # First call: geocoding response
            MagicMock(),
            # Second call: weather response
            MagicMock()
        ]
        
        responses[0].read.return_value.decode.return_value = json.dumps(self.sample_geocoding_response)
        responses[1].read.return_value.decode.return_value = json.dumps(self.sample_weather_response)
        
        mock_urlopen.return_value.__enter__.side_effect = responses
        
        result = self.fetcher.fetch_current_temperature("New York")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["temperature_celsius"], 25.0)
        self.assertEqual(result["humidity"], 60)
        self.assertEqual(result["wind_speed"], 10.5)
        self.assertEqual(result["location"]["name"], "New York")
    
    def test_get_location_coordinates_fallback(self):
        """Test fallback to default location when APIs fail"""
        with patch('urllib.request.urlopen', side_effect=Exception("Network error")):
            result = self.fetcher.get_location_coordinates()
            
            # Should fallback to San Francisco
            self.assertIsNotNone(result)
            self.assertEqual(result["name"], "San Francisco")
            self.assertEqual(result["latitude"], 37.7749)
            self.assertEqual(result["longitude"], -122.4194)
    
    @patch('urllib.request.urlopen')
    def test_get_location_coordinates_no_results(self, mock_urlopen):
        """Test handling when geocoding returns no results"""
        # Mock empty geocoding response first call, then let it fallback to IP detection
        responses = [
            MagicMock(),  # Empty geocoding response
            MagicMock()   # Fallback IP detection would also fail
        ]
        
        responses[0].read.return_value.decode.return_value = json.dumps({"results": []})
        responses[1].side_effect = Exception("IP detection also fails")  # Force complete fallback
        
        mock_urlopen.return_value.__enter__.side_effect = responses
        
        result = self.fetcher.get_location_coordinates("NonexistentCity")
        
        # Should fallback to San Francisco (pragmatic approach)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "San Francisco")
        self.assertEqual(result["latitude"], 37.7749)
        self.assertEqual(result["longitude"], -122.4194)
    
    def test_error_handling_invalid_location(self):
        """Test error handling for invalid locations"""
        with patch.object(self.fetcher, 'get_location_coordinates', return_value=None):
            with self.assertRaises(ValueError) as context:
                self.fetcher.fetch_current_temperature("InvalidCity")
            
            self.assertIn("Could not find coordinates", str(context.exception))
    
    @patch('urllib.request.urlopen')
    def test_error_handling_missing_temperature_data(self, mock_urlopen):
        """Test error handling when temperature data is missing"""
        # Mock responses with missing temperature data
        responses = [
            MagicMock(),  # geocoding
            MagicMock()   # weather (missing temperature)
        ]
        
        responses[0].read.return_value.decode.return_value = json.dumps(self.sample_geocoding_response)
        
        # Weather response without temperature
        invalid_weather_response = {
            "current": {
                "time": "2025-05-28T12:00",
                "relative_humidity_2m": 60,
                "wind_speed_10m": 10.5
                # Missing temperature_2m
            }
        }
        responses[1].read.return_value.decode.return_value = json.dumps(invalid_weather_response)
        
        mock_urlopen.return_value.__enter__.side_effect = responses
        
        with self.assertRaises(ValueError) as context:
            self.fetcher.fetch_current_temperature("New York")
        
        self.assertIn("Temperature data not available", str(context.exception))
    
    def test_round_trip_temperature_accuracy(self):
        """Test that temperature conversions are accurate through the weather system"""
        test_temperatures = [0, 25, 100, -10, 37.5]  # Various test temperatures
        
        for temp_c in test_temperatures:
            with patch.object(self.fetcher, 'fetch_current_temperature') as mock_fetch:
                mock_fetch.return_value = {
                    "location": {"name": "Test", "country": "Test"},
                    "temperature_celsius": temp_c,
                    "humidity": 50,
                    "wind_speed": 5,
                    "time": "2025-05-28T12:00"
                }
                
                result = self.fetcher.get_temperature_in_all_formats()
                temps = result["temperatures"]
                
                # Verify conversions are accurate
                expected_f = (temp_c * 9/5) + 32
                expected_k = temp_c + 273.15
                
                self.assertAlmostEqual(temps["celsius"], temp_c, places=5)
                self.assertAlmostEqual(temps["fahrenheit"], expected_f, places=5)
                self.assertAlmostEqual(temps["kelvin"], expected_k, places=5)
    
    @patch('builtins.print')  # Mock print to test display output
    def test_display_weather_report_format(self, mock_print):
        """Test that display_weather_report formats output correctly"""
        with patch.object(self.fetcher, 'get_temperature_in_all_formats') as mock_get:
            mock_get.return_value = {
                "location": {
                    "name": "Test City",
                    "admin1": "Test State",
                    "country": "Test Country"
                },
                "temperatures": {
                    "celsius": 25.0,
                    "fahrenheit": 77.0,
                    "kelvin": 298.15
                },
                "additional_info": {
                    "humidity": 60,
                    "wind_speed": 10.5,
                    "time": "2025-05-28T12:00"
                }
            }
            
            self.fetcher.display_weather_report("Test City")
            
            # Verify print was called (output formatting)
            self.assertTrue(mock_print.called)
            
            # Check that temperature values appear in the output
            print_calls = [str(call) for call in mock_print.call_args_list]
            output_text = " ".join(print_calls)
            
            self.assertIn("25.0", output_text)  # Celsius
            self.assertIn("77.0", output_text)  # Fahrenheit
            self.assertIn("298.1", output_text)  # Kelvin
            self.assertIn("Test City", output_text)  # Location


class TestWeatherFetcherIntegration(unittest.TestCase):
    """Integration tests that test real API calls (when internet is available)"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        self.fetcher = WeatherFetcher()
    
    def test_real_api_integration(self):
        """Test with real API calls - only runs if internet is available"""
        try:
            # Try to get weather for a well-known city
            result = self.fetcher.get_temperature_in_all_formats("London")
            
            # Basic validation that we got reasonable data
            self.assertIsNotNone(result)
            self.assertIn("temperatures", result)
            self.assertIn("location", result)
            
            temps = result["temperatures"]
            
            # Sanity checks - temperatures should be reasonable for Earth
            self.assertGreater(temps["celsius"], -100)  # Above absolute zero practical limit
            self.assertLess(temps["celsius"], 100)      # Below extreme heat
            self.assertGreater(temps["kelvin"], 173)    # Above -100°C in Kelvin
            self.assertLess(temps["kelvin"], 373)       # Below 100°C in Kelvin
            
            # Temperature relationships should be correct
            self.assertAlmostEqual(temps["kelvin"], temps["celsius"] + 273.15, places=1)
            
            print(f"✅ Integration test passed: {result['location']['name']} = {temps['celsius']:.1f}°C")
            
        except Exception as e:
            # Skip if no internet connection
            self.skipTest(f"Skipping integration test due to network error: {e}")


if __name__ == '__main__':
    print("Running Weather Fetcher Tests...")
    print("=" * 50)
    
    # Run unit tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWeatherFetcher)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Run integration tests if unit tests pass
    if result.wasSuccessful():
        print("\n🌐 Running Integration Tests...")
        print("=" * 50)
        integration_suite = unittest.TestLoader().loadTestsFromTestCase(TestWeatherFetcherIntegration)
        runner.run(integration_suite)
    
    print("\n" + "=" * 50)
    print("Tests complete!") 