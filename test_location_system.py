#!/usr/bin/env python3
"""
Test script for the location-based doctor recommendation system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from doctor_recommendation_model import recommend_doctors_by_location, get_nearby_doctors
from location_service import location_service

def test_recommendation_system():
    """Test the complete location-based recommendation system."""
    
    print("🩺 Testing Location-Based Doctor Recommendation System")
    print("=" * 60)
    
    # Test 1: Basic recommendation with manual location
    print("\n1. Testing with manual location (Bangalore):")
    bangalore_location = (12.9716, 77.5946)
    
    recommendations = recommend_doctors_by_location(
        disease_text="chest pain",
        user_location=bangalore_location,
        max_distance_km=50,
        top_n=3
    )
    
    print(f"Found {len(recommendations)} doctors for chest pain near Bangalore:")
    for i, doctor in enumerate(recommendations, 1):
        print(f"  {i}. {doctor['name']} - {doctor['specialty']} ({doctor['distance_km']} km)")
    
    # Test 2: Get all nearby doctors
    print("\n2. Testing nearby doctors without specialty filter:")
    nearby = get_nearby_doctors(
        user_location=bangalore_location,
        max_distance_km=25
    )
    
    print(f"Found {len(nearby)} doctors within 25km:")
    for doctor in nearby:
        print(f"  - {doctor['name']} ({doctor['specialty']}) - {doctor['distance_km']} km")
    
    # Test 3: Test location service
    print("\n3. Testing location service:")
    location_info = location_service.get_location_info()
    print(f"Current location info: {location_info}")
    
    # Test 4: Test with different specialties
    print("\n4. Testing different specialties:")
    specialties_to_test = ["skin", "child", "bone"]
    
    for specialty in specialties_to_test:
        recs = recommend_doctors_by_location(
            disease_text=f"problems with {specialty}",
            user_location=bangalore_location,
            max_distance_km=30,
            top_n=2
        )
        print(f"\n{specialty.capitalize()} specialists:")
        for doc in recs:
            print(f"  - {doc['name']} ({doc['specialty']}) - {doc['distance_km']} km")
    
    print("\n✅ All tests completed successfully!")
    print("The location-based doctor recommendation system is ready to use!")

if __name__ == "__main__":
    test_recommendation_system()
