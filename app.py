import streamlit as st
import pandas as pd
import random
import urllib.parse
import random

def generate_fortune_text(card_name, orientation, meaning):
    # Atmosphere / tone
    tones = [
        "A calm, spiritual energy surrounds you today.",
        "A new path is quietly opening before you.",
        "Your intuition feels sharper and clearer than usual.",
        "A subtle yet powerful shift is moving through your life.",
        "Something deep within you is beginning to awaken.",
    ]

    # Advice templates
    advice_templates = [
        "This card encourages you to take a closer look at your current situation.",
        "A choice you make now will influence the direction of your future.",
        "A hidden opportunity is getting ready to reveal itself.",
        "Pay attention to the emotions or signs you may have overlooked.",
        "If you take a small step forward, the energy around you will start to flow in your favor.",
    ]

    tone = random.choice(tones)
    advice = random.choice(advice_templates)

    fortune = f"""
### 🔮 Tarot Interpretation  
**Card:** {card_name} ({orientation})

**General Meaning:**  
{meaning}

---

### ✨ Overall Reading  
{tone}  
The appearance of **{card_name}** suggests that this card carries an important message for you today.  
{meaning}

---

### 📌 Advice for You  
{advice}
"""

    return fortune



df = pd.read_csv("tarot_cards.csv")

GITHUB_BASE = "https://raw.githubusercontent.com/rigovicm/your-tarot-app/main/tarot_images"


st.set_page_config(page_title="AI Tarot Reader", page_icon="🔮", layout="wide")
st.title("🔮 Tarot Reading App")
st.write("Choose your reading type!")


def load_github_image_url(card_name):
    safe_name = card_name.strip()
    safe_name = safe_name.replace("/", "_")
    safe_name = safe_name.replace(" ", "_")

    safe_name = urllib.parse.quote(safe_name)

    image_url = f"{GITHUB_BASE}/{safe_name}.png"
    return image_url

def pick_card():
    card = df.sample(1).iloc[0]
    orientation = random.choice(["Upright", "Reversed"])
    meaning = (
        card["Upright Meaning"]
        if orientation == "Upright"
        else card["Reversed Meaning"]
    )

    return {
        "name": card["Card"],
        "orientation": orientation,
        "meaning": meaning,
        "image": load_github_image_url(card["Card"])
    }


st.header("🌟 Today's Fortune")

if st.button("Draw Today's Fortune"):
    card = pick_card()

    st.subheader(f"✨ {card['name']} ({card['orientation']})")
    st.image(card["image"], width=300)
    st.markdown("#### 🔮 Interpretation")
    fortune_text = generate_fortune_text(card['name'], card['orientation'], card['meaning'])
    st.markdown(fortune_text)


st.markdown("---")


st.header("🔮 Past / Present / Future")

if st.button("Start to draw 3 cards"):
    past = pick_card()
    present = pick_card()
    future = pick_card()

    col1, col2, col3 = st.columns(3)

    # Past
    with col1:
        st.subheader("🕰️ Past")
        st.image(past["image"], width=250)
        st.write(f"**{past['name']} ({past['orientation']})**")
        st.markdown(generate_fortune_text(past['name'], past['orientation'], past['meaning']))


    # Present
    with col2:
        st.subheader("📌 Present")
        st.image(present["image"], width=250)
        st.write(f"**{present['name']} ({present['orientation']})**")
        st.markdown(generate_fortune_text(present['name'], present['orientation'], present['meaning']))


    # Future
    with col3:
        st.subheader("🔮 Future")
        st.image(future["image"], width=250)
        st.markdown(generate_fortune_text(future['name'], future['orientation'], future['meaning']))

