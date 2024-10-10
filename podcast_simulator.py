import gradio as gr
import PyPDF2
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI client with OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_podcast_script(pdf_text, language, duration):
    language_prompt = {
        "English": "Write the script in English.",
        "Indonesian": "Write the script in Indonesian (Bahasa Indonesia).",
        "Arabic": "Write the script in Arabic.",
        "Japanese": "Write the script in Japanese."
    }

    duration_prompt = {
        "30 seconds": "The script should be very brief, suitable for a 30-second conversation.",
        "1 minute": "Keep the script concise, suitable for a 1-minute conversation.",
        "3 minutes": "The script should be moderately detailed, suitable for a 3-minute conversation.",
        "5 minutes": "Provide a more in-depth script, suitable for a 5-minute conversation."
    }

    prompt = f"""Based on the following text extracted from a PDF, create a podcast script for two hosts discussing the main points:

    {pdf_text[:2000]}  # Limiting to 2000 characters to avoid token limits

    Generate a conversation between Host A and Host B, discussing the key points from the text in a casual, engaging manner.
    
    {language_prompt[language]}
    {duration_prompt[duration]}"""

    try:
        response = client.chat.completions.create(
            model="nousresearch/hermes-3-llama-3.1-405b:free",
            messages=[
                {"role": "system", "content": "You are an AI assistant that creates podcast scripts based on PDF content."},
                {"role": "user", "content": prompt}
            ]
        )
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            return "Error: No response generated from the AI model."
    except Exception as e:
        return f"Error generating podcast script: {str(e)}"

def create_podcast(pdf_file, language, duration):
    try:
        if pdf_file is None:
            return "Error: No PDF file uploaded."
        
        pdf_text = extract_text_from_pdf(pdf_file.name)
        script = generate_podcast_script(pdf_text, language, duration)
        
        if script.startswith("Error"):
            return script
        
        return script
    except Exception as e:
        return f"Error creating podcast: {str(e)}"

# Gradio Interface
iface = gr.Interface(
    fn=create_podcast,
    inputs=[
        gr.File(label="Upload PDF"),
        gr.Dropdown(choices=["English", "Indonesian", "Arabic", "Japanese"], label="Select Output Language", value="English"),
        gr.Dropdown(choices=["30 seconds", "1 minute", "3 minutes", "5 minutes"], label="Select Dialog Length", value="1 minute")
    ],
    outputs=[
        gr.Textbox(label="Generated Script")
    ],
    title="PDF to Podcast Script Generator",
    description="Upload a PDF file to generate a podcast script based on its content, language, and desired length."
)

if __name__ == "__main__":
    iface.launch()