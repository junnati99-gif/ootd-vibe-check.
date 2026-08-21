import io
from PIL import Image
import requests
import google.generativeai as genai
import streamlit as st

# Page setup
st.set_page_config(page_title="Brainrot Fit Check", page_icon="🗿")
st.title("Brainrot Fit Check 🗿🔥")

# 1. Secure API Configuration
# Add GEMINI_API_KEY = "your_api_key_here" to .streamlit/secrets.toml
if "GEMINI_API_KEY" in st.secrets:
  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
  st.error("Missing GEMINI_API_KEY in Streamlit secrets.")
  st.stop()

# 2. Up-to-date Model Target
MODEL_NAME = "gemini-3.6-flash"


def calculate_fit_score(image: Image.Image) -> str:
  """Sends image to Gemini with error handling to avoid app crashes."""
  prompt = (
      "Analyze this outfit. Rate its Rizz and Aura on a scale of 1-100 using"
      " brainrot slang (skibidi, sigmas, W/L fit, unspoken rizz). Keep it funny"
      " and snappy."
  )

  try:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content([prompt, image])
    return response.text
  except Exception as e:
    return f"⚠️ Could not process image: {str(e)}"


# 3. Image Input UI
st.write("Submit a fit to calculate your Rizz & Aura.")

image_input = None
input_type = st.radio("Image Source:", ["Upload File", "Image URL"])

if input_type == "Upload File":
  uploaded_file = st.file_uploader(
      "Choose a photo", type=["jpg", "jpeg", "png", "webp"]
  )
  if uploaded_file:
    image_input = Image.open(uploaded_file)
    st.image(image_input, caption="Submitted Fit", use_column_width=True)

else:
  image_url = st.text_input("Paste Image URL:")
  if image_url:
    try:
      res = requests.get(image_url, timeout=5)
      res.raise_for_status()
      image_input = Image.open(io.BytesIO(res.content))
      st.image(image_input, caption="Submitted Fit", use_column_width=True)
    except Exception as e:
      st.error(f"Failed to fetch image from URL: {e}")

# 4. Processing Trigger
if st.button("CALCULATE RIZZ & AURA 🗿🔥"):
  if image_input is not None:
    with st.spinner("Calculating aura levels..."):
      result = calculate_fit_score(image_input)
      st.success("Fit Analyzed!")
      st.write(result)
  else:
    st.warning("Please upload an image or provide a valid URL first!")
