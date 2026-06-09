from dotenv import load_dotenv
load_dotenv()

import os
import json
import requests
from typing import List, Dict, Any

class DoctorRecommender:
    def __init__(self):
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.mapmyindia_api_key = "e1b32f5449044ccb7d8d769324931a9f"
        
    def get_doctor_recommendations(self, diagnosis: str) -> List[Dict[str, Any]]:
        """Get doctor recommendations based on diagnosis using AI"""
        
        prompt = f"""
        Based on the medical diagnosis: "{diagnosis}"
        
        Provide specific doctor recommendations in JSON format:
        {{
            "recommendations": [
                {{
                    "specialty": "specific medical specialty",
                    "doctor_type": "type of doctor to consult",
                    "urgency": "urgent/soon/routine",
                    "reason": "why this specialist is needed"
                }}
            ]
        }}
        
        Focus on practical, actionable recommendations.
        """
        
        try:
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You are a medical referral assistant. Provide specific doctor recommendations based on diagnoses."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            recommendations = json.loads(content)
            return recommendations.get('recommendations', [])
            
        except Exception as e:
            # Fallback recommendations
            return self._get_fallback_recommendations(diagnosis)
    
    def _get_fallback_recommendations(self, diagnosis: str) -> List[Dict[str, Any]]:
        """Fallback recommendations when API fails"""
        diagnosis_lower = diagnosis.lower()
        
        if any(word in diagnosis_lower for word in ['skin', 'acne', 'rash', 'eczema']):
            return [
                {
                    "specialty": "Dermatology",
                    "doctor_type": "Dermatologist",
                    "urgency": "soon",
                    "reason": "Specialized in skin conditions and treatments"
                }
            ]
        elif any(word in diagnosis_lower for word in ['fever', 'cold', 'flu', 'infection']):
            return [
                {
                    "specialty": "Internal Medicine",
                    "doctor_type": "General Physician",
                    "urgency": "routine",
                    "reason": "Primary care for general infections and illnesses"
                }
            ]
        else:
            return [
                {
                    "specialty": "General Medicine",
                    "doctor_type": "General Physician",
                    "urgency": "routine",
                    "reason": "Initial consultation for proper diagnosis and referral"
                }
            ]
    
    def get_nearby_hospitals(self, location: str = "Chennai") -> List[Dict[str, Any]]:
        """Get nearby hospitals using MapMyIndia API"""
        
        try:
            # MapMyIndia API endpoint for nearby hospitals
            url = "https://atlas.mapmyindia.com/api/places/nearby/json"
            
            params = {
                "keywords": "hospital",
                "refLocation": "13.0827,80.2707",  # Chennai coordinates
                "radius": 5000,  # 5km radius
                "access_token": "e1b32f5449044ccb7d8d769324931a9f"
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            hospitals = []
            if 'suggestedLocations' in data:
                for place in data['suggestedLocations'][:5]:  # Top 5 hospitals
                    hospitals.append({
                        "name": place.get('placeName', 'Unknown Hospital'),
                        "address": place.get('placeAddress', 'Address not available'),
                        "phone": place.get('contactNo', 'Contact not available'),
                        "specialties": ["General Medicine", "Emergency", "Specialized Care"],
                        "rating": 4.0,
                        "distance": f"{place.get('distance', 0)/1000:.1f} km"
                    })
            
            return hospitals
            
        except Exception as e:
            # Fallback hospital data
            return self._get_fallback_hospitals()
    
    def _get_fallback_hospitals(self) -> List[Dict[str, Any]]:
        """Fallback hospital data when API fails"""
        return [
            {
                "name": "Apollo Hospital",
                "address": "21, Greams Lane, Off Greams Road, Chennai - 600006",
                "phone": "+91-44-2829 3333",
                "specialties": ["Cardiology", "Dermatology", "Orthopedics", "General Medicine"],
                "rating": 4.5,
                "distance": "2.3 km"
            },
            {
                "name": "Fortis Malar Hospital",
                "address": "52, 1st Main Road, Gandhi Nagar, Adyar, Chennai - 600020",
                "phone": "+91-44-4289 2222",
                "specialties": ["Emergency", "Dermatology", "Pediatrics", "General Medicine"],
                "rating": 4.3,
                "distance": "3.1 km"
            },
            {
                "name": "Sri Ramachandra Medical Centre",
                "address": "No.1, Ramachandra Nagar, Porur, Chennai - 600116",
                "phone": "+91-44-4592 8500",
                "specialties": ["All Specialties", "24/7 Emergency"],
                "rating": 4.4,
                "distance": "5.7 km"
            }
        ]
    
    def format_recommendations(self, recommendations: List[Dict], hospitals: List[Dict]) -> str:
        """Format recommendations and hospitals for display"""
        
        output = "🏥 **DOCTOR RECOMMENDATIONS & HOSPITALS**\n\n"
        
        # Doctor recommendations
        output += "**🩺 Recommended Specialists:**\n"
        for rec in recommendations:
            urgency_emoji = "🔴" if rec['urgency'] == 'urgent' else "🟡" if rec['urgency'] == 'soon' else "🟢"
            output += f"{urgency_emoji} **{rec['doctor_type']}** ({rec['specialty']})\n"
            output += f"   Reason: {rec['reason']}\n\n"
        
        # Nearby hospitals
        output += "**🏥 Nearby Hospitals:**\n"
        for hospital in hospitals[:3]:  # Show top 3
            output += f"📍 **{hospital['name']}**\n"
            output += f"   Address: {hospital['address']}\n"
            output += f"   Phone: {hospital['phone']}\n"
            output += f"   ⭐ Rating: {hospital['rating']}/5\n"
            output += f"   🏥 Specialties: {', '.join(hospital['specialties'])}\n"
            output += f"   📏 Distance: {hospital['distance']}\n\n"
        
        return output

# Global instance
recommender = DoctorRecommender()

def get_doctor_recommendations(diagnosis: str) -> str:
    """Main function to get doctor recommendations"""
    recommendations = recommender.get_doctor_recommendations(diagnosis)
    hospitals = recommender.get_nearby_hospitals()
    return recommender.format_recommendations(recommendations, hospitals)

def get_nearby_hospitals(diagnosis: str) -> str:
    """Main function to get nearby hospitals"""
    hospitals = recommender.get_nearby_hospitals()
    return json.dumps(hospitals, indent=2)
