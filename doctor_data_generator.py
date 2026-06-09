import json
import random
import string
from datetime import datetime

class DoctorDataGenerator:
    def __init__(self):
        self.first_names = [
            "Dr. Rajesh", "Dr. Priya", "Dr. Sanjay", "Dr. Anjali", "Dr. Vikram", "Dr. Kavita",
            "Dr. Arjun", "Dr. Meera", "Dr. Ravi", "Dr. Sunita", "Dr. Manish", "Dr. Anita",
            "Dr. Deepak", "Dr. Neha", "Dr. Rohit", "Dr. Pooja", "Dr. Alok", "Dr. Sonia",
            "Dr. Nitin", "Dr. Rashmi", "Dr. Prakash", "Dr. Swati", "Dr. Mohit", "Dr. Divya",
            "Dr. Sunil", "Dr. Shweta", "Dr. Gaurav", "Dr. Nisha", "Dr. Sameer", "Dr. Tina"
        ]
        
        self.last_names = [
            "Sharma", "Verma", "Gupta", "Patel", "Joshi", "Mehta", "Singh", "Kumar", "Reddy",
            "Rao", "Chopra", "Malhotra", "Kapoor", "Bansal", "Agarwal", "Jain", "Shah",
            "Desai", "Pandey", "Mishra", "Nair", "Menon", "Iyer", "Chauhan", "Thakkar",
            "Saxena", "Bhatia", "Arora", "Khanna", "Dubey", "Tiwari", "Sinha", "Yadav"
        ]
        
        self.specialties = [
            "Cardiology", "Neurology", "Orthopedics", "Dermatology", "Pediatrics", "Gynecology",
            "General Medicine", "Oncology", "ENT", "Ophthalmology", "Psychiatry", "Endocrinology",
            "Gastroenterology", "Pulmonology", "Nephrology", "Urology", "Rheumatology", "Anesthesiology",
            "Radiology", "Pathology", "Emergency Medicine", "Family Medicine", "Internal Medicine",
            "Surgery", "Plastic Surgery", "Neurosurgery", "Cardiac Surgery", "Orthopedic Surgery"
        ]
        
        self.cities = [
            "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad",
            "Surat", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Visakhapatnam", "Indore", "Bhopal",
            "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut",
            "Rajkot", "Kalyan", "Vasai", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar",
            "Navi Mumbai", "Allahabad", "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior",
            "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota", "Guwahati", "Chandigarh", "Solapur"
        ]
        
        self.hospitals = [
            "Apollo Hospital", "Fortis Hospital", "Max Hospital", "Medanta Hospital", "AIIMS",
            "Sir Ganga Ram Hospital", "Lilavati Hospital", "Kokilaben Hospital", "Ruby Hall Clinic",
            "CARE Hospital", "Manipal Hospital", "Columbia Asia", "Wockhardt Hospital", "Global Hospital",
            "Narayana Health", "Breach Candy Hospital", "Hinduja Hospital", "Jaslok Hospital",
            "Saifee Hospital", "Bombay Hospital", "Tata Memorial Hospital", "Christian Medical College",
            "PGIMER", "SGPGI", "NIMHANS", "KEM Hospital", "Sion Hospital", "JJ Hospital"
        ]

    def generate_doctor(self, doctor_id):
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        full_name = f"{first_name} {last_name}"
        
        specialty = random.choice(self.specialties)
        city = random.choice(self.cities)
        
        # Generate coordinates based on city (approximate)
        base_coords = {
            "Mumbai": [19.0760, 72.8777],
            "Delhi": [28.7041, 77.1025],
            "Bangalore": [12.9716, 77.5946],
            "Chennai": [13.0827, 80.2707],
            "Kolkata": [22.5726, 88.3639],
            "Hyderabad": [17.3850, 78.4867]
        }
        
        if city in base_coords:
            lat, lng = base_coords[city]
            # Add small random offset
            lat += random.uniform(-0.1, 0.1)
            lng += random.uniform(-0.1, 0.1)
        else:
            lat = random.uniform(8, 37)  # India latitude range
            lng = random.uniform(68, 97)   # India longitude range
        
        # Generate phone number
        phone = f"+91-{random.randint(100, 999)}-{random.randint(10000000, 99999999)}"
        
        # Generate experience (1-30 years)
        experience = random.randint(1, 30)
        
        # Generate rating (3.0-5.0)
        rating = round(random.uniform(3.0, 5.0), 1)
        
        # Generate consultation fee (200-2000)
        consultation_fee = random.randint(200, 2000)
        
        # Generate availability
        availability = {
            "monday": random.choice([True, False]),
            "tuesday": random.choice([True, False]),
            "wednesday": random.choice([True, False]),
            "thursday": random.choice([True, False]),
            "friday": random.choice([True, False]),
            "saturday": random.choice([True, False]),
            "sunday": random.choice([True, False])
        }
        
        # Generate languages spoken
        languages = random.sample(["English", "Hindi", "Tamil", "Telugu", "Malayalam", "Kannada", "Marathi", "Gujarati", "Bengali"], random.randint(2, 4))
        
        return {
            "id": doctor_id,
            "name": full_name,
            "specialty": specialty,
            "city": city,
            "coordinates": [round(lat, 4), round(lng, 4)],
            "contact": phone,
            "email": f"{full_name.lower().replace(' ', '').replace('dr.', '')}@hospital.com",
            "experience": experience,
            "rating": rating,
            "consultation_fee": consultation_fee,
            "hospital": random.choice(self.hospitals),
            "availability": availability,
            "languages": languages,
            "education": f"MBBS, {random.choice(['MD', 'MS', 'DM', 'MCh'])}",
            "certifications": random.sample(["NMC", "MCI", "FRCS", "MRCP", "FACS"], random.randint(1, 3))
        }

    def generate_dataset(self, count=100000):
        """Generate a large dataset of doctors"""
        doctors = []
        for i in range(1, count + 1):
            doctor = self.generate_doctor(i)
            doctors.append(doctor)
            
            # Progress indicator for large datasets
            if i % 10000 == 0:
                print(f"Generated {i} doctors...")
        
        return doctors

    def save_to_json(self, doctors, filename="large_doctor_dataset.json"):
        """Save the generated dataset to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(doctors, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(doctors)} doctors to {filename}")

if __name__ == "__main__":
    generator = DoctorDataGenerator()
    
    print("Starting generation of 100,000 doctor records...")
    doctors = generator.generate_dataset(100000)
    
    generator.save_to_json(doctors, "large_doctor_dataset_100k.json")
    
    print("\nDataset generation complete!")
    print(f"Total doctors: {len(doctors)}")
    print(f"Specialties covered: {len(set(d['specialty'] for d in doctors))}")
    print(f"Cities covered: {len(set(d['city'] for d in doctors))}")
