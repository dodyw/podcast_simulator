import gradio as gr
from podcast_simulator import create_podcast

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
