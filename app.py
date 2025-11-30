import streamlit as st
import pandas as pd
import random
import urllib.parse


df = pd.read_csv("tarot_cards.csv")


GITHUB_BASE = "https://raw.githubusercontent.com/rigovicm/your-tarot-app/main/tarot_images/"

# 기본 설정st.set_page_config(page_title="AI Tarot Reader", page_icon="🔮", layout="wide")
st.title("🔮 Tarot Reading App")
st.write("Choose your reading type!")



def load_github_image_url(card_name):
    safe_name = card_name.strip() 
    safe_name = safe_name.replace("/", "_")  
    safe_name = safe_name.replace(" ", "_")  

    safe_name = urllib.parse.quote(safe_name)

    image_url = f"{GITHUB_IMAGE_BASE_URL}/{safe_name}.png"



def pick_card():
    card = df.sample(1).iloc[0]
    orientation = random.choice(["Upright", "Reversed"])
    meaning = card["Upright Meaning"] if orientation == "Upright" else card["Reversed Meaning"]

    return {
        "name": card["Card"],
        "orientation": orientation,
        "meaning": meaning,
        "image": get_github_image_url(card["Card"])
    }



st.header("🌟 Today's Fortune")

if st.button("Draw Today's Fortune"):
    card = pick_card()

    st.subheader(f"✨ {card['name']} ({card['orientation']})")
    st.image(card["image"], width=300)
    st.markdown("#### 🔮 Interpretation")
    st.write(card["meaning"])

st.markdown("---")


st.header("🔮Past / Present / Future")

if st.button("Start to draw 3 cards"):
    past = pick_card()
    present = pick_card()
    future = pick_card()

    col1, col2, col3 = st.columns(3)

    # 과거
    with col1:
        st.subheader("🕰️ (Past)")
        st.image(past["image"], width=250)
        st.write(f"**{past['name']} ({past['orientation']})**")
        st.write(past["meaning"])

    # 현재
    with col2:
        st.subheader("📌 (Present)")
        st.image(present["image"], width=250)
        st.write(f"**{present['name']} ({present['orientation']})**")
        st.write(present["meaning"])

    # 미래
    with col3:
        st.subheader("🔮 (Future)")
        st.image(future["image"], width=250)
        st.write(f"**{future['name']} ({future['orientation']})**")
        st.write(future["meaning"])
