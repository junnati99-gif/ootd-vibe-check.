import os
import random
import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="Brainrot Fit Check 🗿", page_icon="🚽", layout="centered")

# UI Header
st.title("🗿 MAX BRAINROT FIT CHECK 🚽")
st.caption("Upload your fit pic to calculate your Sigma Rizz, Fanum Tax risk, and Aura Points!")

# Retrieve API key
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ L Key missing! Add GEMINI_API_KEY in Streamlit Settings -> Secrets.")

uploaded_file = st.file_uploader("Drop the fit pic (PNG/JPG)...", type=["jpg", "jpeg", "png"])

# Meme Gif Pools
SIGMA_MEMES = [
    "https://media.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif", # Gigachad
    "https://media.giphy.com/media/X3Gb6WWzovT8iNJr7y/giphy.gif", # Mewing
]
OHIO_MEMES = [
    "https://media.giphy.com/media/H5C8CevNMbpBqMvzk9/giphy.gif", # Side eye
    "https://media.giphy.com/media/AAsj7jAReUKM8/giphy.gif", # Confused
]
COOKED_MEMES = [
    "https://media.giphy.com/media/ro08W31M2DEsw/giphy.gif", # Emotional damage
    "https://media.giphy.com/media/d22UJ4j3NDRAzURi/giphy.gif", # Crying cat
]

if uploaded_file and api_key:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Submitted Fit", use_container_width=True)
    
    if st.button("CALCULATE RIZZ & AURA 🗿🔥", use_container_width=True):
        with st.spinner("Mewing while checking your Ohio status... 🗿🧏"):
            try:
                client = genai.Client(api_key=api_key)
                prompt = """
                Analyze this outfit photo using 100% MAXIMUM Gen Alpha / Brainrot slang.
                Use vocabulary like: skibidi, rizz, sigma, mewing, looksmaxxing, ohio, fanum tax, cooked, chat is this real, W fit, L fit, aura points, baby gronk, livvy dunne.

                Formatting Layout Required:
                - **Aura Points**: (+/- Number, e.g., +1,000,000 Aura or -500,000 Aura)
                - **Rizz Level**: X/10 (Number must be explicit, e.g., 9/10 or 2/10)
                - **The Brainrot Verdict**: (3 sentences of peak unhinged brainrot commentary)
                - **Looksmaxxing Tip**: (1 funny fashion advice tip to gain maximum aura)
                """
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, prompt]
                )
                
                result_text = response.text
                st.markdown("---")
                st.markdown(result_text)
                
                # Check Rizz Level for animations
                if "/10" in result_text:
                    try:
                        score_str = result_text.split("/10")[0].split()[-1]
                        score = int(''.join(filter(str.isdigit, score_str)))
                        
                        st.subheader("Meme Reaction:")
                        if score >= 8:
                            st.balloons()
                            st.image(random.choice(SIGMA_MEMES), caption="W RIZZ SIGMA 🗿🔥")
                        elif score >= 5:
                            st.image(random.choice(OHIO_MEMES), caption="NPC FIT FROM OHIO 😐")
                        else:
                            st.image(random.choice(COOKED_MEMES), caption="BRO IS COOKED 💀")
                    except Exception:
                        st.image(random.choice(OHIO_MEMES))
                        
            except Exception as e:
                st.error(f"Chat is this real? Error: {e}")
