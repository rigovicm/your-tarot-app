import streamlit as st
import pandas as pd
import random
import os
import requests
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Tarot Reader", page_icon="🔮", layout="wide")

st.title("🔮 AI Tarot Card Reading")
st.write("Draw a tarot card and receive an AI-powered reading!")

df = pd.read_csv("tarot_cards.csv")

# -------------------------------------------
# 🔥 GitHub에 있는 이미지 URL 불러오기 함수
# -------------------------------------------

# 예: https://raw.githubusercontent.com/USERNAME/REPO/main/tarot_images/The Fool.png
GITHUB_IMAGE_BASE_URL = "https://github.com/rigovicm/your-tarot-app/tree/main/tarot_images"

def load_github_image(card_name):
    """
    Load tarot card image from GitHub repository.
    """
    image_url = f"{GITHUB_IMAGE_BASE_URL}/{card_name}.png"

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            return None
    except:
        return None


# -------------------------------------------
# 🔮 AI Tarot Reading Generator
# -------------------------------------------

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


# -------------------------------------------
# 🔮 Tarot Draw Logic
# -------------------------------------------

if st.button("Draw a Tarot Card"):
    # 1. Pick a card
    card = df.sample(1).iloc[0]
    card_name = card["Card"]

    # 2. Orientation
    orientation = random.choice(["Upright", "Reversed"])
    meaning = card["Upright Meaning"] if orientation == "Upright" else card["Reversed Meaning"]

    st.subheader(f"✨ Card Drawn: {card_name} ({orientation})")

    # 3. Load image from GitHub
    from PIL import Image
    image = load_github_image(card_name)

    if image:
        st.image(image, width=350)
    else:
        st.warning("Image not found in GitHub repository.")

    # 4. AI Reading
    reading = generate_reading(card_name, orientation, meaning)
    st.markdown("### 🔮 Your Reading")
    st.write(reading)

else:
    st.info("Click the button above to draw a tarot card.")
