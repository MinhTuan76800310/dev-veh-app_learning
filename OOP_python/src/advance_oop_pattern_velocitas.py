import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from vehicle import Vehicle, vehicle
from velocitas_sdk.vehicle_app import VehicleApp, subscribe_topic

# Abstract base class for vehicle features
class VehicleFeature(ABC):
    """Abstract base class for vehicle features."""
    
    def __init__(self, vehicle_client: Vehicle):
        self.vehicle = vehicle_client
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the feature."""
        pass
    
    @abstractmethod
    async def update(self, data: Dict[str, Any]) -> bool:
        """Update the feature with new data."""
        pass

# Concrete implementation of a vehicle feature
class ClimateControlFeature(VehicleFeature):
    """Feature for controlling vehicle climate."""
    
    def __init__(self, vehicle_client: Vehicle):
        super().__init__(vehicle_client)
        self._target_temperature = 22.0  # Default temperature in Celsius
        self._is_ac_on = False
        self._fan_speed = 0
    
    async def initialize(self) -> bool:
        """Initialize climate control settings."""
        try:
            # Set initial values
            await self.vehicle.Cabin.HVAC.Temperature.set(self._target_temperature)
            await self.vehicle.Cabin.HVAC.AirConditioning.IsActive.set(self._is_ac_on)
            await self.vehicle.Cabin.HVAC.FanSpeed.set(self._fan_speed)
            return True
        except Exception as e:
            logging.error(f"Error initializing climate control: {e}")
            return False
    
    async def update(self, data: Dict[str, Any]) -> bool:
        """Update climate control settings."""
        try:
            tasks = []
            
            if "temperature" in data:
                self._target_temperature = data["temperature"]
                tasks.append(
                    asyncio.create_task(
                        self.vehicle.Cabin.HVAC.Temperature.set(self._target_temperature)
                    )
                )
            
            if "ac" in data:
                self._is_ac_on = bool(data["ac"])
                tasks.append(
                    asyncio.create_task(
                        self.vehicle.Cabin.HVAC.AirConditioning.IsActive.set(self._is_ac_on)
                    )
                )
            
            if "fanSpeed" in data:
                self._fan_speed = int(data["fanSpeed"])
                tasks.append(
                    asyncio.create_task(
                        self.vehicle.Cabin.HVAC.FanSpeed.set(self._fan_speed)
                    )
                )
            
            if tasks:
                await asyncio.gather(*tasks)
            
            return True
        except Exception as e:
            logging.error(f"Error updating climate control: {e}")
            return False
    
    @property
    def current_settings(self) -> Dict[str, Any]:
        """Get current climate control settings."""
        return {
            "temperature": self._target_temperature,
            "ac": self._is_ac_on,
            "fanSpeed": self._fan_speed
        }

# Factory for creating vehicle features
class VehicleFeatureFactory:
    """Factory for creating vehicle features."""
    
    @staticmethod
    def create_feature(feature_type: str, vehicle_client: Vehicle) -> Optional[VehicleFeature]:
        """Create a vehicle feature of the specified type."""
        if feature_type.lower() == "climate":
            return ClimateControlFeature(vehicle_client)
        # Add more feature types as needed
        return None

# Observer pattern for feature updates
class FeatureUpdateObserver(ABC):
    """Observer interface for feature updates."""
    
    @abstractmethod
    async def on_feature_update(self, feature_type: str, data: Dict[str, Any]) -> None:
        """Called when a feature is updated."""
        pass

# Concrete observer implementation
class FeatureUpdateLogger(FeatureUpdateObserver):
    """Observer that logs feature updates."""
    
    async def on_feature_update(self, feature_type: str, data: Dict[str, Any]) -> None:
        """Log feature updates."""
        logging.info(f"Feature update: {feature_type} - {json.dumps(data)}")

# Subject in the observer pattern
class FeatureManager:
    """Manager for vehicle features that supports the observer pattern."""
    
    def __init__(self, vehicle_client: Vehicle):
        self.vehicle = vehicle_client
        self.features: Dict[str, VehicleFeature] = {}
        self.observers: List[FeatureUpdateObserver] = []
        self.factory = VehicleFeatureFactory()
    
    def register_observer(self, observer: FeatureUpdateObserver) -> None:
        """Register an observer for feature updates."""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def unregister_observer(self, observer: FeatureUpdateObserver) -> None:
        """Unregister an observer."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    async def notify_observers(self, feature_type: str, data: Dict[str, Any]) -> None:
        """Notify all observers of a feature update."""
        for observer in self.observers:
            await observer.on_feature_update(feature_type, data)
    
    async def initialize_feature(self, feature_type: str) -> bool:
        """Initialize a feature of the specified type."""
        if feature_type in self.features:
            return True
        
        feature = self.factory.create_feature(feature_type, self.vehicle)
        if feature:
            success = await feature.initialize()
            if success:
                self.features[feature_type] = feature
            return success
        
        return False
    
    async def update_feature(self, feature_type: str, data: Dict[str, Any]) -> bool:
        """Update a feature with new data."""
        if feature_type not in self.features:
            success = await self.initialize_feature(feature_type)
            if not success:
                return False
        
        feature = self.features[feature_type]
        success = await feature.update(data)
        
        if success:
            await self.notify_observers(feature_type, data)
        
        return success
    
    def get_feature(self, feature_type: str) -> Optional[VehicleFeature]:
        """Get a feature by type."""
        return self.features.get(feature_type)

class AdvancedVehicleApp(VehicleApp):
    """Advanced vehicle app using various OOP patterns."""
    
    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.Vehicle = vehicle_client
        self.feature_manager = FeatureManager(vehicle_client)
        
        # Register observers
        self.feature_manager.register_observer(FeatureUpdateLogger())
    
    async def on_start(self):
        """Initialize the app when it starts."""
        logging.info("Starting AdvancedVehicleApp...")
        
        # Initialize features
        await self.feature_manager.initialize_feature("climate")
    
    @subscribe_topic("vehicle/feature/update")
    async def on_feature_update_request(self, data: str):
        """Handle requests to update vehicle features."""
        try:
            payload = json.loads(data)
            feature_type = payload.get("type")
            feature_data = payload.get("data", {})
            
            if not feature_type:
                raise ValueError("Feature type is required")
            
            success = await self.feature_manager.update_feature(feature_type, feature_data)
            
            if success:
                # Get updated feature settings
                feature = self.feature_manager.get_feature(feature_type)
                if feature and hasattr(feature, "current_settings"):
                    current_settings = feature.current_settings
                else:
                    current_settings = {}
                
                await self.publish_event(
                    "vehicle/feature/update/response",
                    json.dumps({
                        "result": {
                            "status": 0,
                            "message": f"Feature {feature_type} updated successfully",
                            "settings": current_settings
                        }
                    })
                )
            else:
                raise ValueError(f"Failed to update feature: {feature_type}")
                
        except Exception as e:
            logging.error(f"Error updating feature: {e}")
            await self.publish_event(
                "vehicle/feature/update/response",
                json.dumps({
                    "result": {
                        "status": 1,
                        "message": f"Error: {str(e)}"
                    }
                })
            )

async def main():
    """Main function to start the app."""
    logging.info("Initializing AdvancedVehicleApp...")
    app = AdvancedVehicleApp(vehicle)
    await app.run()

# Run the app
asyncio.run(main())
