import base64
import os
# from google import genai
import google.generativeai as genai
# from google.genai import types

YOUR_API_KEY = "your gemini api"

genai.configure(api_key=YOUR_API_KEY)

def generate(input_text):
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = model.generate_content(
        input_text,
        generation_config=genai.types.GenerationConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=20
        )
    )

    return response.text 

