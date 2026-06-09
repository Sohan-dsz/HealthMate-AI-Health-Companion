# 🩺 HealthMate: Your AI Health Companion

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Gradio](https://img.shields.io/badge/Gradio-Frontend-orange)
![AI](https://img.shields.io/badge/AI-Multimodal-red)
![Healthcare](https://img.shields.io/badge/Domain-Healthcare-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Overview

**HealthMate: Your AI Health Companion** is an AI-powered multimodal healthcare assistant designed to provide preliminary health guidance through text, voice, and image inputs.

The system leverages advanced AI models to analyze symptoms, generate contextual medical guidance, recommend nearby specialists, and provide voice-based responses to improve accessibility and user experience.

HealthMate aims to bridge the gap between healthcare accessibility and technology by enabling users to receive quick preliminary health insights before consulting healthcare professionals.

---

## 🎯 Problem Statement

Access to timely healthcare remains challenging due to:

* Limited healthcare professionals
* Long waiting times
* High consultation costs
* Geographical barriers
* Difficulty accessing reliable medical information

HealthMate addresses these challenges by providing:

* 24/7 AI-powered health assistance
* Preliminary symptom evaluation
* Doctor recommendations
* Voice-enabled interaction
* Multimodal healthcare analysis

---

## 🚀 Key Features

### 🗣️ Speech-Based Symptom Analysis

* Record symptoms using voice input
* Speech-to-text transcription using Whisper
* Real-time symptom extraction

### 🖼️ Image-Based Diagnosis Support

* Upload images of visible conditions
* Skin disease and visible symptom analysis
* AI-powered image understanding

### 🤖 AI Healthcare Assistant

* Context-aware healthcare conversations
* Preliminary health guidance
* Medical recommendations
* Personalized responses

### 🎙️ Voice Response Generation

* AI-generated voice responses
* Text-to-Speech support
* Accessibility-focused interaction

### 📍 Doctor Recommendation System

* Location-based specialist suggestions
* Distance-based doctor ranking
* Specialty matching

### 🔒 Secure User Authentication

* JWT Authentication
* User Registration & Login
* Protected user history

### 📜 Consultation History

* View previous consultations
* Persistent storage of interactions
* User-specific health records

---

## 🏗️ System Architecture

```text
User
 │
 ├── Voice Input
 ├── Text Input
 └── Image Input
        │
        ▼
 Data Preprocessing
        │
 ┌───────────────┐
 │ Whisper STT   │
 └───────────────┘
        │
        ▼
 ┌─────────────────────┐
 │ Llama 3 Vision AI   │
 └─────────────────────┘
        │
        ▼
 Diagnostic Engine
        │
 ├── Health Guidance
 ├── Doctor Recommendation
 ├── Audio Generation
 └── Consultation History
        │
        ▼
      User
```

---

## 🛠️ Tech Stack

### Frontend

* Gradio

### Backend

* FastAPI
* Python

### Database

* SQLite
* SQLAlchemy

### AI Models

* Llama 3 Vision
* Whisper Large v3

### APIs

* Groq API
* ElevenLabs API

### Authentication

* JWT Tokens
* OAuth2

### Location Services

* Haversine Distance Algorithm
* Geolocation APIs

---

## 📂 Project Structure

```bash
HealthMate/
│
├── frontend/
│
├── backend/
│   ├── auth/
│   ├── api/
│   ├── database/
│   ├── models/
│   └── services/
│
├── ai_modules/
│   ├── symptom_analysis/
│   ├── image_analysis/
│   ├── doctor_recommendation/
│   └── speech_processing/
│
├── data/
│   ├── doctors.json
│   └── user_history.db
│
├── static/
├── requirements.txt
├── app.py
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/HealthMate-AI-Health-Companion.git
cd HealthMate-AI-Health-Companion
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
SECRET_KEY=your_secret_key
```

⚠️ Never commit `.env` files to GitHub.

---

## ▶️ Run the Application

### Start Backend

```bash
uvicorn main:app --reload
```

### Launch Frontend

```bash
python app.py
```

---

## 📊 Workflow

1. User logs in
2. Records symptoms or uploads image
3. Whisper converts speech to text
4. Llama 3 Vision analyzes symptoms
5. AI generates diagnosis guidance
6. Doctor Recommendation Engine suggests specialists
7. ElevenLabs converts response to speech
8. Results are displayed on dashboard
9. Consultation is stored in history

---

## 📈 Future Enhancements

* Mobile Application (Android & iOS)
* Real-time Telemedicine Integration
* Appointment Booking System
* Electronic Health Records Integration
* Wearable Device Integration
* Explainable AI Diagnostics
* Personalized Health Monitoring
* Multi-language Support

---

## 👨‍💻 Team

* Sohan Dsouza
* Bhuvandeep D Achar
* Shubhra Rai D
* Sunag Aithal

Department of Intelligent Computing and Business Systems

St Joseph Engineering College, Mangaluru

---

## 📚 Academic Project

Developed as part of the Bachelor of Engineering (Computer Science & Business Systems) curriculum under Visvesvaraya Technological University (VTU), Belagavi.

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

## 🏷️ Topics

```text
healthcare-ai
medical-chatbot
multimodal-ai
llama3
whisper
groq
fastapi
gradio
python
computer-vision
speech-recognition
doctor-recommendation
health-tech
artificial-intelligence
machine-learning
healthcare
medical-diagnosis
```
