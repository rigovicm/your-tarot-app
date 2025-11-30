import streamlit as st
import pandas as pd
import random
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="AI-Free Tarot Reader", page_icon="🔮", layout="wide")

st.title("🔮 Tarot Card Reading")
st.write("Draw a tarot card and receive an interpretation — no API required!")

df = pd.read_csv("tarot_cards.csv")

# -------------------------------------------
# 🔥 GitHub 이미지 URL
# -------------------------------------------

GITHUB_IMAGE_BASE_URL = "https://github.com/rigovicm/your-tarot-app/tree/main/tarot_images"

def load_github_image(card_name):
    safe_name = card_name.replace(" ", "%20")
    image_url = f"{GITHUB_IMAGE_BASE_URL}/{safe_name}.png"

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            return None
    except:
        return None


def simple_reading(card_name, orientation, meaning):
    templates = [
        f"The energy of **{card_name} ({orientation})** is influencing you today.",
        f"The appearance of **{card_name}** suggests an important message.",
        f"This card reflects what your spirit needs to hear right now.",
        f"Your current path is being guided by the energy of **{card_name}**.",
    ]

    ending = [
        "Trust the process and stay open to change.",
        "Let intuition guide your next steps.",
        "Focus on what truly matters to you.",
        "A new opportunity may soon reveal itself.",
        "Stay grounded and listen to your inner voice.",
    ]

    return (
        random.choice(templates)
        + "\n\n"
        + f"**Meaning:** {meaning}\n\n"
        + random.choice(ending)
    )


# -------------------------------------------
# 🔮 Tarot Draw Logic
# -------------------------------------------

if st.button("Draw a Tarot Card"):
    card = df.sample(1).iloc[0]
    card_name = card["Card"]

    orientation = random.choice(["Upright", "Reversed"])
    meaning = card["Upright Meaning"] if orientation == "Upright" else card["Reversed Meaning"]

    st.subheader(f"✨ Card Drawn: {card_name} ({orientation})")

    # Load image from GitHub
    image = load_github_image(card_name)

    if image:
        st.image(image, width=350)
    else:
        st.warning("Image not found in GitHub repository.")

    # Show reading without OpenAI
    st.markdown("### 🔮 Your Reading")
    st.write(simple_reading(card_name, orientation, meaning))

else:
    st.info("Click the button above to draw a tarot card.")
