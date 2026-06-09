import json
import math
from typing import List, Dict, Any, Optional, Tuple

# Import the new location service
from location_service import location_service

# Load doctors dataset
with open("karnataka_doctors.json", "r") as f:
    doctors = json.load(f)

# Enhanced disease to specialty mapping
disease_specialty_map = {
    "cardiac": "Cardiology",
    "heart": "Cardiology",
    "chest pain": "Cardiology",
    "skin": "Dermatology",
    "rash": "Dermatology",
    "acne": "Dermatology",
    "bone": "Orthopedics",
    "fracture": "Orthopedics",
    "joint": "Orthopedics",
    "child": "Pediatrics",
    "baby": "Pediatrics",
    "fever": "General Medicine",
    "infection": "General Medicine",
    "cold": "General Medicine",
    "flu": "General Medicine",
    "headache": "General Medicine",
    "stomach": "Gastroenterology",
    "digestion": "Gastroenterology",
    "anxiety": "Psychiatry",
    "depression": "Psychiatry",
    "stress": "Psychiatry",
    "diabetes": "Endocrinology",
    "thyroid": "Endocrinology",
    "cancer": "Oncology",
    "tumor": "Oncology",
    "kidney": "Nephrology",
    "urine": "Nephrology",
    "lung": "Pulmonology",
    "breathing": "Pulmonology",
    "asthma": "Pulmonology",
    "eye": "Ophthalmology",
    "vision": "Ophthalmology",
    "ear": "ENT",
    "nose": "ENT",
    "throat": "ENT",
    "women": "Gynecology",
    "pregnancy": "Obstetrics",
    "bone marrow": "Hematology",
    "blood": "Hematology"
}

def get_specialty_from_disease(disease_text: str) -> str:
    """Determine specialty from disease description."""
    disease_text = disease_text.lower()
    
    # Check for exact matches first
    for keyword, specialty in disease_specialty_map.items():
        if keyword in disease_text:
            return specialty
    
    # Check for multi-word matches
    words = disease_text.split()
    for word in words:
        for keyword, specialty in disease_specialty_map.items():
            if word in keyword:
                return specialty
    
    return "General Medicine"

def recommend_doctors_by_location(
    disease_text: str, 
    max_distance_km: float = 50, 
    top_n: int = 3,
    user_location: Optional[Tuple[float, float]] = None
) -> List[Dict[str, Any]]:
    """
    Recommend doctors based on disease and user location.
    
    Args:
        disease_text: Description of the health issue
        max_distance_km: Maximum distance to search for doctors
        top_n: Number of recommendations to return
        user_location: Optional manual location override
        
    Returns:
        List of recommended doctors with distance information
    """
    # Get user location if not provided
    if user_location is None:
        user_location = location_service.get_user_location()
    
    if not user_location:
        # Fallback to a default location (Bangalore)
        user_location = (12.9716, 77.5946)
    
    specialty = get_specialty_from_disease(disease_text)
    
    # Filter doctors by specialty
    filtered_doctors = [doc for doc in doctors if doc["specialty"] == specialty]
    
    if not filtered_doctors:
        # If no doctors for specialty, return general medicine
        filtered_doctors = [doc for doc in doctors if doc["specialty"] == "General Medicine"]
    
    # Calculate distance and add to each doctor
    for doc in filtered_doctors:
        distance = location_service.calculate_distance(user_location, doc["coordinates"])
        doc["distance_km"] = round(distance, 2)
    
    # Sort by distance and filter by max distance
    filtered_doctors = [
        doc for doc in filtered_doctors 
        if doc["distance_km"] <= max_distance_km
    ]
    
    filtered_doctors.sort(key=lambda x: x["distance_km"])
    
    # Return top N doctors
    return filtered_doctors[:top_n]

def get_nearby_doctors(
    user_location: Optional[Tuple[float, float]] = None,
    max_distance_km: float = 25,
    specialty: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get all nearby doctors regardless of specialty.
    
    Args:
        user_location: Optional manual location override
        max_distance_km: Maximum distance to search
        specialty: Optional specialty filter
        
    Returns:
        List of nearby doctors
    """
    if user_location is None:
        user_location = location_service.get_user_location()
    
    if not user_location:
        user_location = (12.9716, 77.5946)  # Default to Bangalore
    
    # Filter by specialty if provided
    if specialty:
        filtered_doctors = [doc for doc in doctors if doc["specialty"] == specialty]
    else:
        filtered_doctors = doctors
    
    # Calculate distances
    for doc in filtered_doctors:
        distance = location_service.calculate_distance(user_location, doc["coordinates"])
        doc["distance_km"] = round(distance, 2)
    
    # Filter by distance and sort
    nearby_doctors = [
        doc for doc in filtered_doctors 
        if doc["distance_km"] <= max_distance_km
    ]
    
    nearby_doctors.sort(key=lambda x: x["distance_km"])
    
    return nearby_doctors

# Backward compatibility function
def recommend_doctors(disease_text, user_location=None, top_n=3):
    """Legacy function for backward compatibility."""
    if user_location is None:
        user_location = location_service.get_user_location()
    
    return recommend_doctors_by_location(
        disease_text=disease_text,
        max_distance_km=50,
        top_n=top_n,
        user_location=user_location
    )
