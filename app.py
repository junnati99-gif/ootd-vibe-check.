import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import colorsys
import io
from datetime import datetime

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="OOTD Vibe Check 💀",
    page_icon="🔥",
    layout="centered",
)

# ----------------------------------------------------------------------------
# BRAINROT CSS — loud, chaotic, gen z/alpha coded
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Bangers&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Fredoka', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }

    .brainrot-title {
        font-family: 'Bangers', cursive;
        font-size: 3.2rem;
        text-align: center;
        background: linear-gradient(90deg, #ff00cc, #333399, #00ffea, #ff9900);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s ease infinite;
        margin-bottom: 0;
    }

    @keyframes shimmer {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        opacity: 0.85;
        margin-bottom: 1.5rem;
    }

    .verdict-box {
        background: rgba(255,255,255,0.08);
        border: 2px solid rgba(255,255,255,0.25);
        border-radius: 20px;
        padding: 1.3rem;
        margin-top: 1rem;
        text-align: center;
        box-shadow: 0 0 25px rgba(255,0,204,0.25);
    }

    .score-text {
        font-family: 'Bangers', cursive;
        font-size: 2.4rem;
        letter-spacing: 2px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff00cc, #00ffea);
        color: black;
        font-weight: 700;
        border-radius: 12px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# BRAINROT VOCAB BANKS
# ----------------------------------------------------------------------------
HYPE_LINES = [
    "Certified DRIP. The rizz is unmatched. No cap. 🔥🔥",
    "This fit ate and left no crumbs 💅",
    "Skibidi swag detected. Gyatt-tier fashion. 🚿",
    "Fanum tax on everyone else's outfit, you're just built different.",
    "Sigma grindset fit fr fr, mother is mothering 💀",
    "This is giving main character energy, no notes.",
    "You just hit different. Certified W outfit.",
    "Ohio wouldn't even know what to do with this drip.",
    "That's a whole slay bestie, the ancestors are proud.",
    "10/10 rizzler behavior, chat is going feral rn 📈",
]

ROAST_LINES = [
    "Bro thought this was giving fire... it was giving Ohio. 💀",
    "This fit said 'skibidi' but meant 'oopsie'.",
    "Gyatt where. This is an L outfit, ratio.",
    "Mid. Just mid. Fanum taxed the drip from this one.",
    "This ain't it chief, the rizz has left the chat.",
    "Sigma? more like siggy-nah. Try again.",
    "NPC fit behavior detected, no bitches energy fr.",
    "This is negative aura points, get some grimace shake.",
    "The vibes are in the shadow realm rn 🪦",
    "Certified brain rot but the bad kind, not the fun kind.",
]

VERDICTS = ["MEGA RIZZ 🚀", "MID TIER 😐", "TOTAL FLOP 💀", "GOATED FIT 🐐", "CHAOS ENERGY 🌀"]

LOADING_MESSAGES = [
    "Consulting the skibidi council...",
    "Measuring rizz per square inch...",
    "Asking Ohio for a second opinion...",
    "Calculating gyatt coefficient...",
    "Running fit through the brainrot algorithm...",
]

# Original brainrot "stickers" — plain text/emoji, drawn by us, not real memes
# (no copyrighted meme templates or characters, so this stays 100% safe to ship)
STICKER_BANK = [
    "🔥 CERTIFIED DRIP 🔥",
    "GYATT 😳",
    "SKIBIDI RIZZ 🚿",
    "NO CAP 🧢❌",
    "MOTHER IS MOTHERING 💅",
    "OHIO ALERT 🚨",
    "MAIN CHARACTER 🎬",
    "FANUM TAXED 🍟",
    "SIGMA GRINDSET 📈",
    "AURA +9000 ✨",
    "RATIO'D 💀",
    "GOATED 🐐",
]

# ----------------------------------------------------------------------------
# FAKE "AI" VIBE ANALYSIS — deterministic-ish score from image color data
# (no external API needed = works 100% free, no keys, no subscriptions)
# ----------------------------------------------------------------------------
def analyze_vibe(image: Image.Image):
    img = image.convert("RGB").resize((60, 60))
    pixels = list(img.getdata())

    total_sat = 0
    total_bright = 0
    for r, g, b in pixels:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        total_sat += s
        total_bright += v

    avg_sat = total_sat / len(pixels)
    avg_bright = total_bright / len(pixels)

    # Mix in a little randomness so re-uploads still feel fun/varied
    chaos = random.uniform(-0.15, 0.15)
    raw_score = (avg_sat * 0.6 + avg_bright * 0.4) + chaos
    score = max(0, min(100, round(raw_score * 100)))
    return score


def get_verdict(score: int):
    if score >= 80:
        return "GOATED FIT 🐐", random.choice(HYPE_LINES)
    elif score >= 60:
        return "MEGA RIZZ 🚀", random.choice(HYPE_LINES)
    elif score >= 40:
        return "MID TIER 😐", random.choice(HYPE_LINES + ROAST_LINES)
    elif score >= 20:
        return "CHAOS ENERGY 🌀", random.choice(ROAST_LINES)
    else:
        return "TOTAL FLOP 💀", random.choice(ROAST_LINES)


def _strip_emoji(text: str) -> str:
    """Most standard fonts (DejaVu etc.) can't render color emoji glyphs and
    show blank boxes instead. Strip them out for text drawn onto the PNG
    share card — emoji still show fine everywhere else in the Streamlit UI."""
    import re
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001FAFF"
        "\U00002600-\U000027BF"
        "\U0001F1E6-\U0001F1FF"
        "\U00002190-\U000021FF"
        "\U00002B00-\U00002BFF"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text).strip()


def _load_font(size: int, bold: bool = True):
    """Try a real TTF font, fall back to PIL's built-in default if unavailable.
    This keeps the app from crashing on hosts that don't have DejaVu installed."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def generate_share_card(photo: Image.Image, verdict: str, score: int, line: str, sticker: str) -> Image.Image:
    """Builds a original, shareable 'brainrot' result card — square format,
    good for Snap/IG/TikTok story sharing. Everything drawn here is original
    (solid shapes + text), so there's no copyrighted meme artwork involved."""

    W, H = 1080, 1350
    card = Image.new("RGB", (W, H), (15, 12, 41))
    draw = ImageDraw.Draw(card)

    # Gradient-ish background using horizontal bands (simple, dependency-free)
    top_color = (255, 0, 204)
    bottom_color = (0, 255, 234)
    for y in range(H):
        t = y / H
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        draw.line([(0, y), (W, y)], fill=(r // 4, g // 4, b // 4))

    verdict = _strip_emoji(verdict)
    line = _strip_emoji(line)
    sticker = _strip_emoji(sticker)

    # Title
    title_font = _load_font(64)
    draw.text((W // 2, 70), "OOTD VIBE CHECK", font=title_font, fill="white", anchor="ma")

    # Photo, cropped to a square and centered with a white border
    photo_size = 760
    square_photo = ImageOps.fit(photo.convert("RGB"), (photo_size, photo_size))
    border = 12
    frame = Image.new("RGB", (photo_size + border * 2, photo_size + border * 2), "white")
    frame.paste(square_photo, (border, border))
    card.paste(frame, ((W - frame.width) // 2, 170))

    # Sticker badge over the photo (top-right corner)
    sticker_font = _load_font(34)
    badge_w, badge_h = 420, 70
    badge_x = W - badge_w - 60
    badge_y = 190
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=35, fill=(255, 255, 255)
    )
    draw.text(
        (badge_x + badge_w // 2, badge_y + badge_h // 2),
        sticker, font=sticker_font, fill=(20, 20, 20), anchor="mm"
    )

    # Verdict + score
    verdict_font = _load_font(70)
    line_font = _load_font(36)
    score_font = _load_font(44)

    y = 170 + frame.height + 40
    draw.text((W // 2, y), verdict, font=verdict_font, fill="white", anchor="ma")

    y += 100
    # Wrap the roast/hype line so it doesn't overflow the card width
    words = line.split()
    wrapped_lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip()
        if draw.textlength(test, font=line_font) > W - 140:
            wrapped_lines.append(current)
            current = w
        else:
            current = test
    if current:
        wrapped_lines.append(current)

    for wline in wrapped_lines:
        draw.text((W // 2, y), wline, font=line_font, fill=(230, 230, 230), anchor="ma")
        y += 46

    y += 20
    draw.text((W // 2, y), f"VIBE SCORE: {score}/100", font=score_font, fill=(255, 230, 0), anchor="ma")

    # Footer
    draw.text(
        (W // 2, H - 60),
        "made with OOTD Vibe Check - unserious results, no cap",
        font=_load_font(26, bold=False), fill=(255, 255, 255), anchor="ma"
    )

    return card


# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown('<p class="brainrot-title">OOTD VIBE CHECK 💀🔥</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">drop your fit. get rizzed or get ratio\'d. no cap.</p>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# MODE TOGGLE
# ----------------------------------------------------------------------------
mode = st.radio(
    "Pick your fate 🎯",
    ["Hype me up 🥰", "Roast me 💀", "Surprise me 🎲"],
    horizontal=True,
)

# ----------------------------------------------------------------------------
# IMAGE SOURCE
# ----------------------------------------------------------------------------
source = st.radio("Image Source:", ["Upload File", "Image URL"], horizontal=True)

image_input = None

if source == "Upload File":
    uploaded_file = st.file_uploader("Choose a photo of your fit", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file is not None:
        image_input = Image.open(uploaded_file)
else:
    url = st.text_input("Paste an image URL")
    if url:
        try:
            import requests
            from io import BytesIO

            resp = requests.get(url, timeout=8)
            image_input = Image.open(BytesIO(resp.content))
        except Exception:
            st.error("Couldn't load that URL bestie, try another one 😭")

# ----------------------------------------------------------------------------
# MAIN LOGIC — guard against None so the app never crashes on st.image()
# ----------------------------------------------------------------------------
if image_input is not None:
    st.image(image_input, caption="Submitted fit 📸", use_container_width=True)

    if st.button("RUN THE VIBE CHECK 🚨"):
        with st.spinner(random.choice(LOADING_MESSAGES)):
            score = analyze_vibe(image_input)

            if mode == "Hype me up 🥰":
                verdict, line = random.choice(VERDICTS[:2]), random.choice(HYPE_LINES)
            elif mode == "Roast me 💀":
                verdict, line = random.choice(VERDICTS[2:4]), random.choice(ROAST_LINES)
            else:
                verdict, line = get_verdict(score)

            sticker = random.choice(STICKER_BANK)

        st.markdown(
            f"""
            <div class="verdict-box">
                <div class="score-text">{verdict}</div>
                <p style="font-size:1.3rem; margin-top:0.5rem;">{line}</p>
                <p style="opacity:0.7; font-size:0.9rem;">Vibe Score: {score}/100 &nbsp;•&nbsp; {sticker}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(score / 100)

        if score >= 70:
            st.balloons()
        elif score < 30:
            st.snow()

        st.caption(f"Checked at {datetime.now().strftime('%I:%M %p')} — results are unserious, screenshot & share 📲")

        # ---------------- SHARE CARD ----------------
        with st.spinner("Cooking up your share card... 🎨"):
            card = generate_share_card(image_input, verdict, score, line, sticker)

        st.image(card, caption="Your shareable vibe card ✨", use_container_width=True)

        buf = io.BytesIO()
        card.save(buf, format="PNG")
        st.download_button(
            label="DOWNLOAD & SHARE 📲",
            data=buf.getvalue(),
            file_name="ootd_vibe_check.png",
            mime="image/png",
        )
else:
    st.info("Upload a fit pic (or drop a URL) to get your vibe checked 👆")

st.markdown("---")
st.caption("Made with 100% unpaid brainrot energy • no API keys, no subscriptions, no cap 🧢❌")