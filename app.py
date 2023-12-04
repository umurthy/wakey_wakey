import os
os.system("pip install git+https://github.com/openai/whisper.git")
import gradio as gr
import whisper

from share_btn import community_icon_html, loading_icon_html, share_js

model = whisper.load_model("small")


        
def inference(audio):
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)
    
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    
    _, probs = model.detect_language(mel)
    
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)
    
    print(result.text)
    return result.text  # Return only the text to be displayed


css = """
        .gradio-container {
            font-family: 'IBM Plex Sans', sans-serif;
        }
        .title-text {
            font-weight: bold;
            color: #30AADD; /* Example fun color */
            margin-bottom: 1rem; /* Add space between the heading */
        }
        .sub-text {
            font-family: 'Comic Sans MS', cursive; /* Comic font */
            font-size: 1.2rem;
            font-weight: bold;
            background: linear-gradient(90deg, #ff0000, #ffa500, #ffff00, #008000, #0000ff, #4b0082, #ee82ee);
            -webkit-background-clip: text;
            color: transparent; /* Make the text color transparent to show the gradient */
            margin-bottom: 10px;
        }
        .logo {
            width: 100px; /* Adjust as needed */
            height: auto;
            display: block; /* Center the logo */
            margin: 20px auto 20px auto; /* Add space and center horizontally */
        }
        /* Other styles */
        ...
    """

block = gr.Blocks(css=css)

with block:
    gr.HTML(
        """
        <div style="text-align: center; max-width: 650px; margin: auto;">
            <img src='logo.png' alt='logo' class='logo'/> <!-- Ensure the 'logo.png' file is in the correct directory -->
            <div class="title-text">
                Speak with Your Wakey Wakey 🌞 and Get in Touch with the World 🌍
            </div>
            <p class="sub-text">
                Wake up to ask about your calendar, check the weather, and command the app to play your favorite songs based on your mood. A fun and interactive way to start your day!
            </p>
            <!-- The link button -->
            <a href="https://replit.com/@QQZ/testpromptpy#main.py" target="_blank" class="gr-button">Click to see how our clock internal works</a>
        </div>
        """
    )
    with gr.Group():
        with gr.Box():
            with gr.Row().style(mobile_collapse=False, equal_height=True):
                audio = gr.Audio(
                    label="Input Audio",
                    show_label=False,
                    source="microphone",
                    type="filepath"
                )
                btn = gr.Button("Transcribe")
        text = gr.Textbox(show_label=False, elem_id="result-textarea")

    btn.click(inference, inputs=[audio], outputs=[text])

block.launch()