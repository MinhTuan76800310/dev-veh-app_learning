import asyncio
import json
import logging
from typing import List, Dict, Any
from vehicle import Vehicle, vehicle
from velocitas_sdk.vdb.reply import DataPointReply
from velocitas_sdk.vehicle_app import VehicleApp, subscribe_topic

class DrivingMode:
    """Class representing a driving mode configuration."""
    
    def __init__(self, name: str, settings: Dict[str, Any]):
        self.name = name
        self.settings = settings
    
    def apply_to_vehicle(self, vehicle_client: Vehicle) -> List[asyncio.Task]:
        """Apply this driving mode's settings to the vehicle."""
        tasks = []
        
        # Example: Set ADAS settings based on mode
        if "adas" in self.settings:
            adas_settings = self.settings["adas"]
            if "cruiseControl" in adas_settings:
                cc_settings = adas_settings["cruiseControl"]
                if "speedLimit" in cc_settings:
                    tasks.append(
                        asyncio.create_task(
                            vehicle_client.ADAS.CruiseControl.SpeedLimit.set(
                                cc_settings["speedLimit"]
                            )
                        )
                    )
        
        # Example: Set powertrain settings based on mode
        if "powertrain" in self.settings:
            pt_settings = self.settings["powertrain"]
            if "responseMode" in pt_settings:
                tasks.append(
                    asyncio.create_task(
                        vehicle_client.Powertrain.ResponseMode.set(
                            pt_settings["responseMode"]
                        )
                    )
                )
        
        return tasks

class DrivingModeManager:
    """Class to manage different driving modes."""
    
    def __init__(self, vehicle_client: Vehicle):
        self.vehicle = vehicle_client
        self.available_modes: Dict[str, DrivingMode] = {}
        self.current_mode: str = "NORMAL"
        
        # Initialize with default modes
        self._initialize_default_modes()
    
    def _initialize_default_modes(self):
        """Set up default driving modes."""
        self.available_modes["ECO"] = DrivingMode("ECO", {
            "powertrain": {
                "responseMode": "ECO",
                "regenerativeBraking": "HIGH"
            },
            "adas": {
                "cruiseControl": {
                    "speedLimit": 110
                }
            }
        })
        
        self.available_modes["SPORT"] = DrivingMode("SPORT", {
            "powertrain": {
                "responseMode": "SPORT",
                "regenerativeBraking": "LOW"
            },
            "adas": {
                "cruiseControl": {
                    "speedLimit": 150
                }
            }
        })
        
        self.available_modes["NORMAL"] = DrivingMode("NORMAL", {
            "powertrain": {
                "responseMode": "NORMAL",
                "regenerativeBraking": "MEDIUM"
            },
            "adas": {
                "cruiseControl": {
                    "speedLimit": 130
                }
            }
        })
    
    async def set_mode(self, mode_name: str) -> bool:
        """Set the current driving mode."""
        if mode_name not in self.available_modes:
            return False
        
        mode = self.available_modes[mode_name]
        tasks = mode.apply_to_vehicle(self.vehicle)
        
        if tasks:
            await asyncio.gather(*tasks)
        
        self.current_mode = mode_name
        return True
    
    def get_current_mode(self) -> str:
        """Get the name of the current driving mode."""
        return self.current_mode
    
    def get_available_modes(self) -> List[str]:
        """Get a list of available driving modes."""
        return list(self.available_modes.keys())

class DrivingModeApp(VehicleApp):
    """Vehicle app for managing driving modes."""
    
    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.Vehicle = vehicle_client
        self.mode_manager = DrivingModeManager(vehicle_client)
    
    async def on_start(self):
        """Initialize the app when it starts."""
        logging.info("Starting DrivingModeApp...")
        # Set initial driving mode
        await self.mode_manager.set_mode("NORMAL")
    
    @subscribe_topic("drivingmode/set")
    async def on_set_mode_request(self, data: str):
        """Handle requests to change the driving mode."""
        try:
            payload = json.loads(data)
            mode_name = payload.get("mode", "").upper()
            
            if not mode_name:
                raise ValueError("Mode name is required")
            
            success = await self.mode_manager.set_mode(mode_name)
            
            if success:
                await self.publish_event(
                    "drivingmode/set/response",
                    json.dumps({
                        "result": {
                            "status": 0,
                            "message": f"Mode set to {mode_name}"
                        }
                    })
                )
            else:
                raise ValueError(f"Invalid mode: {mode_name}")
                
        except Exception as e:
            logging.error(f"Error setting driving mode: {e}")
            await self.publish_event(
                "drivingmode/set/response",
                json.dumps({
                    "result": {
                        "status": 1,
                        "message": f"Error: {str(e)}"
                    }
                })
            )
    
    @subscribe_topic("drivingmode/get")
    async def on_get_mode_request(self, data: str):
        """Handle requests to get the current driving mode."""
        current_mode = self.mode_manager.get_current_mode()
        available_modes = self.mode_manager.get_available_modes()
        
        await self.publish_event(
            "drivingmode/get/response",
            json.dumps({
                "result": {
                    "status": 0,
                    "currentMode": current_mode,
                    "availableModes": available_modes
                }
            })
        )

async def main():
    """Main function to start the app."""
    logging.info("Initializing DrivingModeApp...")
    app = DrivingModeApp(vehicle)
    await app.run()

# Run the app
asyncio.run(main())
