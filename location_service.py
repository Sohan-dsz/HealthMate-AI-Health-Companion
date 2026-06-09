import json
import requests
import math
from typing import Tuple, Optional, Dict, Any

class LocationService:
    """Service for detecting user location and calculating distances."""
    
    def __init__(self):
        self.user_location = None
        self.location_accuracy = None
        
    def get_location_from_browser(self) -> Optional[Tuple[float, float]]:
        """
        Get location using browser geolocation API.
        This would typically be called from JavaScript in the browser.
        Returns tuple of (latitude, longitude) or None if not available.
        """
        # This is a placeholder for browser-based location detection
        # In practice, this would be handled via JavaScript in the web interface
        return None
    
    def get_location_from_ip(self) -> Optional[Tuple[float, float]]:
        """
        Get approximate location based on IP address.
        Returns tuple of (latitude, longitude) or None if not available.
        """
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return (float(data.get('latitude', 0)), float(data.get('longitude', 0)))
        except Exception as e:
            print(f"Error getting location from IP: {e}")
        return None
    
    def get_user_location(self, use_browser: bool = True) -> Optional[Tuple[float, float]]:
        """
        Get user location with fallback options.
        
        Args:
            use_browser: Try browser geolocation first if True
            
        Returns:
            Tuple of (latitude, longitude) or None if location unavailable
        """
        if use_browser:
            # Try browser location first
            location = self.get_location_from_browser()
            if location:
                self.user_location = location
                self.location_accuracy = "high"
                return location
        
        # Fallback to IP-based location
        location = self.get_location_from_ip()
        if location:
            self.user_location = location
            self.location_accuracy = "medium"
            return location
        
        return None
    
    def calculate_distance(self, coord1: Tuple[float, float], 
                          coord2: Tuple[float, float]) -> float:
        """
        Calculate distance between two coordinates using haversine formula.
        
        Args:
            coord1: (latitude, longitude) of first point
            coord2: (latitude, longitude) of second point
            
        Returns:
            Distance in kilometers
        """
        return self.haversine_distance(coord1, coord2)
    
    @staticmethod
    def haversine_distance(coord1: Tuple[float, float], 
                          coord2: Tuple[float, float]) -> float:
        """
        Calculate distance between two coordinates using haversine formula.
        
        Args:
            coord1: (latitude, longitude) of first point
            coord2: (latitude, longitude) of second point
            
        Returns:
            Distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def filter_by_distance(self, locations: list, max_distance_km: float = 50) -> list:
        """
        Filter locations by maximum distance from user.
        
        Args:
            locations: List of dicts with 'coordinates' key
            max_distance_km: Maximum distance in kilometers
            
        Returns:
            Filtered list of locations within specified distance
        """
        if not self.user_location:
            return locations
        
        filtered = []
        for location in locations:
            if 'coordinates' in location:
                distance = self.calculate_distance(
                    self.user_location, 
                    tuple(location['coordinates'])
                )
                if distance <= max_distance_km:
                    location['distance_km'] = round(distance, 2)
                    filtered.append(location)
        
        return sorted(filtered, key=lambda x: x['distance_km'])
    
    def get_location_info(self) -> Dict[str, Any]:
        """Get current location information."""
        return {
            'coordinates': self.user_location,
            'accuracy': self.location_accuracy,
            'is_available': self.user_location is not None
        }

# Global instance
location_service = LocationService()

# JavaScript code for browser geolocation (to be used in web interface)
BROWSER_LOCATION_JS = """
function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error("Geolocation is not supported by this browser."));
            return;
        }
        
        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy
                });
            },
            (error) => {
                reject(error);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000
            }
        );
    });
}

// Usage example:
// getUserLocation()
//     .then(location => console.log(location))
//     .catch(error => console.error(error));
"""
