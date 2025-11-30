import streamlit as st
import pandas as pd
import random
import requests
from io import BytesIO
from PIL import Image
import urllib.parse

st.set_page_config(page_title="Tarot Reader", page_icon="🔮", layout="wide")

st.title("🔮 Tarot Card Reading (No OpenAI)")
st.write("Draw a tarot card and receive an interpretation!")

# Load CSV
df = pd.read_csv("tarot_cards.csv")

# -------------------------------------------
# 🔥 YOUR GitHub raw base URL
# -------------------------------------------
GITHUB_IMAGE_BASE_URL = "https://raw.githubusercontent.com/rigovicm/your-tarot-app/main/tarot_images"


# -------------------------------------------
# 🔥 Load image from GitHub with safe encoding
# -------------------------------------------
def load_github_image(card_name):
    safe_name = card_name.strip() 
    safe_name = safe_name.replace("/", "_")  
    safe_name = safe_name.replace(" ", "_")  

   
    safe_name = urllib.parse.quote(safe_name)


    image_url = f"{GITHUB_IMAGE_BASE_URL}/{safe_name}.png"

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.warning(f"❌ Image not found: {image_url}")
            return None
    except:
        st.warning(f"⚠️ Failed to load image: {image_url}")
        return None


# -------------------------------------------
# 🔮 Simple Reading Generator (No OpenAI)
# -------------------------------------------
def generate_simple_reading(card_name, orientation, meaning):
    templates = [
        f"The energy of **{card_name} ({orientation})** surrounds you.",
        f"The presence of **{card_name}** signals an important message.",
        f"This card reflects a shift happening within you.",
    ]

    endings = [
        "Trust your instincts and stay open to change.",
        "Let intuition guide your next move.",
        "A new opportunity may be approaching.",
        "Stay grounded and listen to your inner voice.",
    ]

    return (
        random.choice(templates)
        + "\n\n"
        + f"**Meaning:** {meaning}\n\n"
        + random.choice(endings)
    )


# -------------------------------------------
# 🔮 Main Tarot Draw Logic
# -------------------------------------------
if st.button("Draw a Tarot Card"):
    card = df.sample(1).iloc[0]
    card_name = card["Card"]

    orientation = random.choice(["Upright", "Reversed"])
    meaning = (
        card["Upright Meaning"]
        if orientation == "Upright"
        else card["Reversed Meaning"]
    )

    st.subheader(f"✨ Card Drawn: {card_name} ({orientation})")

    # Load GitHub image
    image = load_github_image(card_name)

    if image:
        st.image(image, width=350)

    # Show reading
    st.markdown("### 🔮 Your Reading")
    st.write(generate_simple_reading(card_name, orientation, meaning))

else:
    st.info("Click the button above to draw a tarot card.")
