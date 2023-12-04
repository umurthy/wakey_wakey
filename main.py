import os
import tkinter as tk
from tkinter import ttk

import requests
from openai import OpenAI
from replit import audio
root = tk.Tk()
root.title("Wakie Wakie Landing Page")

root.attributes('-fullscreen', True)

# Configure the root window background
root.configure(bg="white")

# Style configuration
style = ttk.Style()
style.configure("TLabel", background="white", font=("Arial", 24))

# Title Label
title_label = ttk.Label(root, text="Wakie Wakie", style="TLabel")
title_label.pack(pady=50)  # Add some vertical padding

# Description or additional content
description_label = ttk.Label(root, text="Welcome to the Wakie Wakie App!",
                              font=("Arial", 14), background="white")
description_label.pack(pady=10)


weather = {"time":["2023-12-10"],"temperature_2m_max":[6.4],"temperature_2m_min":[3.1],"precipitation_sum":[10.20],"rain_sum":[10.05],"showers_sum":[0.10],"snowfall_sum":[0.03],"precipitation_hours":[7.0]}


context = {
    "name":
    "Shruthi",
    "schedule": [
        "8:00 AM - Morning Yoga", 
        "8:30 AM - 9:00 AM Kids dropoff", 
        "10:00 AM - 10:30 AM - 1:1 with Mike",
        "10:30 AM - 11:00 AM - 1:1 with Amy",
        "11:00 AM - 12:00 PM - Team Sprint Planning Meeting",
        "1:00 PM - 3:30 PM - Focus work",
        "3:30 PM - 4:30 PM - Doctor's Appointment",
        "4:30 PM - 5:30 PM - Kids pickup",
        "6:00 PM - 7:30 PM - Family Dinner", 
        "8:00 PM - 10:00 PM - Relaxation Time"
    ],
    "tasks": [],
    "weather": weather,
    "location":
    "New York, NY",
}


def generate_alarm_text(persona, context):

  personas = {
      "sassy": {
          "speaker":
          "patrick",
          "prompt":
          "Use wry humor a witty attitude to  prod the person awake. Incorporate sassy remarks and a bold tone."
      },
      "mom": {
          "speaker":
          "mom",
          "prompt":
          "Gently encourage and motivate with a warm and loving approach, like a nurturing mother. Use the context to create sweet affirmations to motivate me to start my day."
      },
      "siri": {
          "speaker":
          "siri",
          "prompt":
          "dopt a straightforward, factual style, resembling a personal assistant or AI, focusing on efficiency and the day's schedule."
      },
      "aggressive": {
          "speaker":
          "aggressive",
          "prompt":
          "Use a super aggressive approach like a sports coach, with a tone of urgency to emphasize the importance of starting the day without delay."
      },
  }

  if persona not in personas.keys():
    raise ValueError(
        f"{persona} is not a valid persona."
        "Please choose from the following personas: sassy, mom, siri, aggressive"
    )

  client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

  response = client.completions.create(model="gpt-3.5-turbo-instruct",
                                       prompt="Say this is a test",
                                       max_tokens=7,
                                       temperature=0)
  prompt = f"Write a 2 paragraph text to speech message towake me up. Here is context about me and my day. Be concise. {context}. {personas[persona]['prompt']}:"

  #openai
  response = client.completions.create(model="gpt-3.5-turbo-instruct",
                                       prompt=prompt,
                                       max_tokens=300,
                                       temperature=0)
  return (response.choices[0].text.strip())



def text_to_speech_openai(text):

  openai_api_key=os.environ['OPENAI_API_KEY']

  headers = {
      'Authorization': f'Bearer {openai_api_key}',
      'Content-Type': 'application/json',
  }

  data = {
      'model': 'tts-1',
      'input': text,
      'voice': 'alloy',
  }

  response = requests.post('https://api.openai.com/v1/audio/speech', headers=headers, json=data)

  # Write the response content to a file
  with open('speech.mp3', 'wb') as file:
      file.write(response.content)
  print("finished writing mp3")

  source = audio.play_file('speech.mp3')
  while True:
    pass


gen_text = generate_alarm_text("aggressive", context)
print(gen_text)
text_to_speech_openai(gen_text)
response_label = ttk.Label(root, text=gen_text, font=("Arial", 12))
response_label.pack(pady=20)
root.mainloop()
