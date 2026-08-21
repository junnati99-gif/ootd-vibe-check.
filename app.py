import os
import streamlit as st
from PIL import Image
from google import genai

st.set_page_config(page_title="OOTD Vibe Check", page_icon="✨")
st.title("✨ OOTD Vibe Check & Fit Rater")

# Retrieve API key securely
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ API Key missing! Add GEMINI_API_KEY in Streamlit Settings -> Secrets.")

uploaded_file = st.file_uploader("Upload your outfit pic...", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="Submitted Fit", use_container_width=True)
    
    if st.button("Rate My Drip 🔥"):
        with st.spinner("Analyzing the fit..."):
            client = genai.Client(api_key=api_key)
            prompt = """
            Analyze this outfit photo for a Gen Z / Gen Alpha audience.
            Respond using this layout:
            - **Core Aesthetic**: (e.g., Y2K, Streetwear, Gorpcore, Coquette, Quiet Luxury)
            - **Drip Score**: X/10
            - **The Vibe Roast**: (Write 2 witty, trend-aware sentences analyzing the outfit)
            - **Level Up Tip**: (Suggest 1 item or accessory to complete the fit)
            """
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[image, prompt]
            )
            st.markdown(response.text)
