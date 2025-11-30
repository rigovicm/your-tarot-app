import pandas as pd
from openai import OpenAI
import os
import base64
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_prompt(card_name, upright_meaning):
    """
    Create an image generation prompt based on card and upright meaning.
    """
    return f"""
Create a detailed, artistic tarot card illustration.

Card: {card_name}
Meaning: {upright_meaning}

Style:
- Mystical, elegant tarot card artwork
- Intricate symbolism
- Soft glowing colors
- High detail fantasy illustration
"""


def generate_tarot_image(prompt, card_name):
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="512x512"
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    os.makedirs("images", exist_ok=True)
    path = f"images/{card_name}.png"

    with open(path, "wb") as f:
        f.write(image_bytes)

    return path


def generate_all_images(csv_path="tarot_cards.csv"):
    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        card_name = row["Card"]
        upright = row["Upright Meaning"]

        prompt = build_prompt(card_name, upright)

        print(f"Generating image for {card_name}...")

        try:
            filepath = generate_tarot_image(prompt, card_name)
            print(f"✔ Saved → {filepath}")
        except Exception as e:
            print(f"❌ Error for {card_name}: {e}")


if __name__ == "__main__":
    generate_all_images()
