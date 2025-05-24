import asyncio
from typing import List, Optional, Tuple
from vehicle import Vehicle, vehicle
from velocitas_sdk.vehicle_app import VehicleApp

class NavigationService:
    """A service for handling vehicle navigation."""
    
    def __init__(self, vehicle_client: Vehicle):
        self.vehicle = vehicle_client
        self._destinations: List[Tuple[float, float]] = []  # List of (latitude, longitude) tuples
        self._current_route: List[Tuple[float, float]] = []
        self._is_navigating: bool = False
    
    async def set_destination(self, latitude: float, longitude: float) -> bool:
        """Set a destination for navigation."""
        # In a real app, this would validate the coordinates and possibly
        # communicate with a navigation system
        self._destinations.append((latitude, longitude))
        
        # Update the vehicle's navigation system
        try:
            await self.vehicle.Cabin.Infotainment.Navigation.DestinationSet.set(True)
            return True
        except Exception as e:
            print(f"Error setting destination: {e}")
            return False
    
    async def start_navigation(self) -> bool:
        """Start navigating to the current destination."""
        if not self._destinations:
            return False
        
        self._is_navigating = True
        
        # In a real app, this would start turn-by-turn navigation
        try:
            await self.vehicle.Cabin.Infotainment.Navigation.IsActive.set(True)
            return True
        except Exception as e:
            print(f"Error starting navigation: {e}")
            self._is_navigating = False
            return False
    
    async def stop_navigation(self) -> bool:
        """Stop the current navigation."""
        self._is_navigating = False
        
        try:
            await self.vehicle.Cabin.Infotainment.Navigation.IsActive.set(False)
            return True
        except Exception as e:
            print(f"Error stopping navigation: {e}")
            return False
    
    def get_current_destination(self) -> Optional[Tuple[float, float]]:
        """Get the current destination coordinates."""
        if not self._destinations:
            return None
        return self._destinations[-1]
    
    @property
    def is_navigating(self) -> bool:
        """Check if navigation is currently active."""
        return self._is_navigating

class NavigationApp(VehicleApp):
    """Vehicle app that provides navigation services."""
    
    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.Vehicle = vehicle_client
        # Composition: NavigationApp has-a NavigationService
        self.nav_service = NavigationService(vehicle_client)
    
    async def on_start(self):
        """Initialize the app when it starts."""
        print("Starting NavigationApp...")
    
    async def set_destination_and_navigate(self, latitude: float, longitude: float) -> bool:
        """Set a destination and start navigation."""
        if await self.nav_service.set_destination(latitude, longitude):
            return await self.nav_service.start_navigation()
        return False

async def main():
    """Main function to start the app."""
    print("Initializing NavigationApp...")
    app = NavigationApp(vehicle)
    
    # Example usage
    success = await app.set_destination_and_navigate(37.7749, -122.4194)
    if success:
        print("Navigation started successfully")
        
        # Get current destination
        destination = app.nav_service.get_current_destination()
        if destination:
            lat, lon = destination
            print(f"Navigating to: {lat}, {lon}")
        
        # Stop navigation after 5 seconds
        await asyncio.sleep(5)
        await app.nav_service.stop_navigation()
        print("Navigation stopped")
    
    await app.run()

# Run the app
asyncio.run(main())
