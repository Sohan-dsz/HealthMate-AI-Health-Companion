import gradio as gr
import os
import ast
import json
import tempfile
import requests
import csv
from dotenv import load_dotenv
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs
from doctor_recommendation_model import recommend_doctors_by_location
from location_service import location_service

load_dotenv()
API_URL = "http://localhost:8000"
access_token = None
current_username = None  # Track logged-in username

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

SYSTEM_PROMPT = (
    "As a professional doctor, I am unable to provide a diagnosis or specific medical advice based on an image. "
    "My role is to offer general health information, and I am not equipped to provide the kind of personalized medical guidance that you would receive from a qualified healthcare professional "
    "who can perform a physical examination and take a complete medical history. For any health concerns, it is crucial to consult with a doctor or a specialist in person to receive an accurate diagnosis and appropriate treatment. "
    "They can provide the necessary medical care and prescribe specific medications or treatments tailored to your individual needs."
)

OUTPUT_DIR = tempfile.gettempdir()
CSV_FILEPATH = os.path.join(OUTPUT_DIR, "prescription.csv")
VOICE_PATH = os.path.join(OUTPUT_DIR, "doctor_response.wav")

HISTORY_FILE = os.path.join(OUTPUT_DIR, "user_history.json")

def load_user_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_user_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def add_history(username, user_prompt, doctor_response):
    history = load_user_history()
    user_hist = history.get(username, [])
    user_hist.append({"prompt": user_prompt, "response": doctor_response})
    history[username] = user_hist
    save_user_history(history)

def get_user_history(username):
    history = load_user_history()
    return history.get(username, [])

def register_user(username, password):
    try:
        r = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
        if r.ok:
            return r.json().get("message", "Registration successful!")
        else:
            return f"Registration failed: {r.text}"
    except Exception as e:
        return f"Request error: {e}"

def login_user(username, password):
    global access_token, current_username
    try:
        r = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if r.ok:
            data = r.json()
            access_token = data.get("access_token", None)
            if access_token:
                current_username = username
                return "Login successful!"
            else:
                return "Login failed!"
        else:
            return f"Login failed: {r.text}"
    except Exception as e:
        return f"Request error: {e}"

def get_prescription_llm(symptom_text, image_context=""):
    prompt = f"""
For the following health complaint, recommend disease-related ointments, tablets, creams etc. in this format (number and newline for each):
1) Drug Name
Timings/Instructions:
2) Drug Name
Timings/Instructions:
...
Be medically specific and concise.
Complaint: {symptom_text}
Image findings/context: {image_context}
"""
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",  # Use working model from provided code
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,  # Reduce max tokens
        "temperature": 0.4
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=60
    )
    msg = response.json()
    if "choices" in msg and len(msg["choices"]) > 0:
        return msg["choices"][0]["message"]["content"].strip()
    else:
        return f"Error from LLM: {msg.get('error', {}).get('message', 'Unknown error')}"

def parse_and_save_prescription(prescription_str, csv_path):
    import re
    meds = []
    for match in re.finditer(r"\d+\)\s*([^\n]+)\nTimings/Instructions:\s*([^\n]+)", prescription_str):
        drug, timing = match.groups()
        meds.append([drug.strip(), timing.strip()])
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Drug Name", "Timings/Instructions"])
        for row in meds:
            writer.writerow(row)
    display_block = ""
    for idx, row in enumerate(meds, 1):
        display_block += f"{idx}) {row[0]}\nTimings: {row[1]}\n"
    if not meds:
        display_block = "No prescription medicines found."
    return display_block

def process_inputs(audio_filepath, image_filepath, max_distance_km=50, use_location=True):
    global current_username
    if not access_token or not current_username:
        return ("Please login to continue.", "", "", None, "", "You must login first", None)
    if not audio_filepath and not image_filepath:
        return ("Please provide audio or image input.", "", "", None, "", "", None)

    try:
        speech_text = transcribe_with_groq(
            stt_model="whisper-large-v3-turbo",
            audio_filepath=audio_filepath,
            GROQ_API_KEY=GROQ_API_KEY,
        )
    except Exception as e:
        return f"Speech-to-text error: {e}", "", "", None, "", "", None

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=SYSTEM_PROMPT + speech_text,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze"

    prescription_text = get_prescription_llm(speech_text, doctor_response)
    presc_display = parse_and_save_prescription(prescription_text, CSV_FILEPATH)

    doctor_response = prescription_text

    # Save user prompt and response history
    add_history(current_username, speech_text, doctor_response)

    voice_file = VOICE_PATH
    audio_status = ""
    try:
        text_to_speech_with_elevenlabs(doctor_response, output_filepath=voice_file)
        audio_status = "Audio Ready"
    except Exception as e:
        audio_status = f"TTS unavailable: {str(e)}"
        voice_file = None

    location_info = location_service.get_location_info()
    location_status = f"Location: {location_info['coordinates'] if location_info['coordinates'] else 'Default Bangalore'}"

    doc_recs_text = "Location-based recommendations disabled."
    if use_location:
        recs = recommend_doctors_by_location(
            disease_text=speech_text,
            max_distance_km=max_distance_km,
            top_n=3,
            user_location=location_info['coordinates'] or None,
        )
        doc_recs_text = (
            "\n".join(
                f"Dr. {d['name']} - {d['specialty']} - {d['city']} - {d.get('distance_km', '?')} km" for d in recs
            ) if recs else "No doctors found nearby for your condition."
        )
    return (
        speech_text,
        doctor_response + (f"\n\n{audio_status}" if audio_status else ""),
        doc_recs_text,
        voice_file,
        location_status,
        presc_display,
        CSV_FILEPATH,
    )

def show_user_history():
    global current_username
    if not current_username:
        return "Please log in to see your history."
    history = get_user_history(current_username)
    if not history:
        return "No history found."
    display_text = ""
    for idx, item in enumerate(history[-20:], 1):  # show last 20 entries
        display_text += f"{idx}) Query:\n{item['prompt']}\nResponse:\n{item['response']}\n---\n"
    return display_text

with gr.Blocks() as demo:
    with gr.Tab("Sign Up"):
        su_user = gr.Textbox(label="Username")
        su_pass = gr.Textbox(type="password", label="Password")
        su_btn = gr.Button("Register")
        su_msg = gr.Textbox()
        su_btn.click(register_user, inputs=[su_user, su_pass], outputs=[su_msg])
    with gr.Tab("Login"):
        li_user = gr.Textbox(label="Username")
        li_pass = gr.Textbox(type="password", label="Password")
        li_btn = gr.Button("Log In")
        li_msg = gr.Textbox()
        li_btn.click(login_user, inputs=[li_user, li_pass], outputs=[li_msg])
    with gr.Tab("HealthMate AI"):
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Speak your symptoms")
        image_input = gr.Image(type="filepath", label="Upload affected area image")
        max_dist = gr.Slider(minimum=5, maximum=100, step=1, value=50, label="Maximum Distance (km)")
        use_loc = gr.Checkbox(value=True, label="Use Location")
        submit_btn = gr.Button("Submit")
        speech_out = gr.Textbox(label="Speech to Text", interactive=False)
        doctor_resp_out = gr.Textbox(label="Doctor's Response", interactive=False)
        recs_out = gr.Textbox(label="Doctor Recommendations", interactive=False)
        audio_out = gr.Audio(label="Voice Response", type="filepath")
        loc_status_out = gr.Textbox(label="Location Status", interactive=False)
        presc_text_out = gr.Textbox(label="Prescription", lines=8, interactive=False)
        presc_csv_out = gr.File(label="Download Prescription CSV")
        submit_btn.click(
            process_inputs,
            inputs=[audio_input, image_input, max_dist, use_loc],
            outputs=[speech_out, doctor_resp_out, recs_out, audio_out, loc_status_out, presc_text_out, presc_csv_out],
        )
    with gr.Tab("History"):
        hist_out = gr.Textbox(label="Your Query History", lines=20, interactive=False)
        refresh_btn = gr.Button("Refresh History")
        refresh_btn.click(fn=show_user_history, inputs=None, outputs=hist_out)

demo.launch()
