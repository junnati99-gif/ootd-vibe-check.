# OOTD Vibe Check 💀🔥

A fun, Gen Z/Alpha–coded "outfit rating" web app. Upload a photo of your fit, pick a mode (hype, roast, or surprise), and get a randomized brainrot verdict — plus a downloadable shareable result card for your story.

**Live app:** [https://ootd-vibe-check-btgigvacujkwjcsybrztte.streamlit.app/]

(add-a-screenshot-or-gif-here.png)

## What it does

- Upload a photo (or paste an image URL)
- Choose a mode: **Hype me up**, **Roast me**, or **Surprise me**
- The app scores the image based on color saturation and brightness, then pairs that score with a random line from a bank of Gen Z/Alpha slang (rizz, gyatt, skibidi, fanum tax, sigma, etc.)
- Generates a polished, shareable PNG "vibe card" (photo + verdict + score) you can download and post

## How it works

Built entirely in Python with [Streamlit](https://streamlit.io) for the UI. There's no external AI API involved — the "vibe score" is calculated locally using `Pillow` and `colorsys` by converting the image to HSV and averaging saturation/brightness across pixels, with a small randomized offset so results feel fresh on repeat uploads. This keeps the app 100% free to run with no API keys or subscriptions.

The shareable result card is also generated locally with `Pillow`'s `ImageDraw`, drawing an original gradient background, the user's photo, and text — no third-party meme templates or copyrighted assets involved.

## Tech stack

- **Streamlit** — UI framework and hosting
- **Pillow (PIL)** — image processing, color analysis, and card generation
- **Python** `colorsys`, `random`, `io`

## Run it locally

```bash
git clone https://github.com/<your-username>/ootd-vibe-check.git
cd ootd-vibe-check
pip install -r requirements.txt
streamlit run app.py
```

## Notes

This is a personal project built for fun and to practice shipping a full app end-to-end — including debugging real deployment issues (dependency conflicts, image-handling edge cases) along the way. Not a production tool, no data is stored or sent anywhere.ootd-vibe-check.