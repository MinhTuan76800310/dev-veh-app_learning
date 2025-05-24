import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import json

# Assuming we're testing the ClimateControlFeature from earlier examples
class TestClimateControlFeature(unittest.TestCase):
    def setUp(self):
        # Create a mock Vehicle object
        self.mock_vehicle = MagicMock()
        
        # Set up the mock HVAC structure
        self.mock_vehicle.Cabin.HVAC.Temperature.set = AsyncMock()
        self.mock_vehicle.Cabin.HVAC.AirConditioning.IsActive.set = AsyncMock()
        self.mock_vehicle.Cabin.HVAC.FanSpeed.set = AsyncMock()
        
        # Create the feature with the mock vehicle
        self.climate_feature = ClimateControlFeature(self.mock_vehicle)
    
    async def test_initialize(self):
        # Test that initialize sets the correct initial values
        result = await self.climate_feature.initialize()
        
        self.assertTrue(result)
        self.mock_vehicle.Cabin.HVAC.Temperature.set.assert_called_once_with(22.0)
        self.mock_vehicle.Cabin.HVAC.AirConditioning.IsActive.set.assert_called_once_with(False)
        self.mock_vehicle.Cabin.HVAC.FanSpeed.set.assert_called_once_with(0)
    
    async def test_update(self):
        # Test updating climate settings
        update_data = {
            "temperature": 24.5,
            "ac": True,
            "fanSpeed": 3
        }
        
        result = await self.climate_feature.update(update_data)
        
        self.assertTrue(result)
        self.mock_vehicle.Cabin.HVAC.Temperature.set.assert_called_once_with(24.5)
        self.mock_vehicle.Cabin.HVAC.AirConditioning.IsActive.set.assert_called_once_with(True)
        self.mock_vehicle.Cabin.HVAC.FanSpeed.set.assert_called_once_with(3)
        
        # Check that the internal state was updated
        self.assertEqual(self.climate_feature._target_temperature, 24.5)
        self.assertEqual(self.climate_feature._is_ac_on, True)
        self.assertEqual(self.climate_feature._fan_speed, 3)
    
    def test_current_settings(self):
        # Test the current_settings property
        self.climate_feature._target_temperature = 25.0
        self.climate_feature._is_ac_on = True
        self.climate_feature._fan_speed = 4
        
        settings = self.climate_feature.current_settings
        
        expected_settings = {
            "temperature": 25.0,
            "ac": True,
            "fanSpeed": 4
        }
        
        self.assertEqual(settings, expected_settings)

# Testing the VehicleApp class
class TestAdvancedVehicleApp(unittest.TestCase):
    def setUp(self):
        # Create mock objects
        self.mock_vehicle = MagicMock()
        
        # Patch the FeatureManager
        self.mock_feature_manager = MagicMock()
        self.mock_feature_manager.initialize_feature = AsyncMock(return_value=True)
        self.mock_feature_manager.update_feature = AsyncMock(return_value=True)
        
        # Create a mock feature with current_settings
        self.mock_feature = MagicMock()
        self.mock_feature.current_settings = {
            "temperature": 22.0,
            "ac": False,
            "fanSpeed": 2
        }
        
        self.mock_feature_manager.get_feature.return_value = self.mock_feature
        
        # Create the app with patches
        with patch('__main__.FeatureManager', return_value=self.mock_feature_manager):
            self.app = AdvancedVehicleApp(self.mock_vehicle)
        
        # Mock the publish_event method
        self.app.publish_event = AsyncMock()
    
    async def test_on_start(self):
        # Test that on_start initializes the climate feature
        await self.app.on_start()
        
        self.mock_feature_manager.initialize_feature.assert_called_once_with("climate")
    
    async def test_on_feature_update_request_success(self):
        # Test successful feature update
        request_data = json.dumps({
            "type": "climate",
            "data": {
                "temperature": 23.0,
                "ac": True
            }
        })
        
        await self.app.on_feature_update_request(request_data)
        
        # Check that the feature manager was called correctly
        self.mock_feature_manager.update_feature.assert_called_once_with(
            "climate",
            {"temperature": 23.0, "ac": True}
        )
        
        # Check that the response was published
        self.app.publish_event.assert_called_once()
        call_args = self.app.publish_event.call_args[0]
        
        self.assertEqual(call_args[0], "vehicle/feature/update/response")
        
        response_data = json.loads(call_args[1])
        self.assertEqual(response_data["result"]["status"], 0)
        self.assertEqual(response_data["result"]["settings"], self.mock_feature.current_settings)
    
    async def test_on_feature_update_request_failure(self):
        # Test feature update failure
        self.mock_feature_manager.update_feature.reset_mock(return_value=True)
        self.mock_feature_manager.update_feature.return_value = False
        
        request_data = json.dumps({
            "type": "unknown_feature",
            "data": {}
        })
        
        await self.app.on_feature_update_request(request_data)
        
        # Check that the error response was published
        self.app.publish_event.assert_called_once()
        call_args = self.app.publish_event.call_args[0]
        
        self.assertEqual(call_args[0], "vehicle/feature/update/response")
        
        response_data = json.loads(call_args[1])
        self.assertEqual(response_data["result"]["status"], 1)
        self.assertIn("Error", response_data["result"]["message"])

if __name__ == '__main__':
    unittest.main()
        