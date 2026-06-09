from dotenv import load_dotenv

load_dotenv()

import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

import base64

def encode_image(image_path):
    image_file = open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode('utf-8')

# Custom system prompt for all LLM calls
SYSTEM_PROMPT = (
    "As a professional doctor, I am unable to provide a diagnosis or specific medical advice based on an image. "
    "My role is to offer general health information, and I am not equipped to provide the kind of personalized medical guidance that you would receive from a qualified healthcare professional "
    "who can perform a physical examination and take a complete medical history. For any health concerns, it is crucial to consult with a doctor or a specialist in person to receive an accurate diagnosis and appropriate treatment. "
    "They can provide the necessary medical care and prescribe specific medications or treatments tailored to your individual needs."
)

from groq import Groq

MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

def analyze_image_with_query(query, model, encoded_image):
    client = Groq()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": [
            {"type": "text", "text": query},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
        ]}
    ]
    chat_completion = client.chat.completions.create(messages=messages, model=model)
    return chat_completion.choices[0].message.content
