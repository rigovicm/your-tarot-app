import streamlit as st
import pandas as pd
import random
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Tarot Reader", page_icon="🔮", layout="wide")

st.title("🔮 AI Tarot Card Reading")
st.write("Draw a tarot card and receive an AI-powered reading!")

df = pd.read_csv("tarot_cards.csv")


def generate_reading(card_name, orientation, meaning):
    prompt = f"""
You are a mystical tarot fortune teller.

Card: {card_name}
Orientation: {orientation}
Meaning: {meaning}

Give an insightful, friendly, magical tarot reading.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


if st.button("Draw a Tarot Card"):
    # 1. Pick a card from CSV
    card = df.sample(1).iloc[0]
    card_name = card["Card"]

    # 2. Decide orientation
    orientation = random.choice(["Upright", "Reversed"])
    meaning = (
        card["Upright Meaning"]
        if orientation == "Upright"
        else card["Reversed Meaning"]
    )

    st.subheader(f"✨ Card Drawn: {card_name} ({orientation})")

    # 3. Show image
    image_path = f"images/{card_name}.png"
    if os.path.exists(image_path):
        st.image(image_path, width=350)
    else:
        st.warning("Image not found. Run generate_images.py first.")

    # 4. Generate AI reading
    reading = generate_reading(card_name, orientation, meaning)
    st.markdown("### 🔮 Your Reading")
    st.write(reading)

else:
    st.info("Click the button above to draw a tarot card.")
