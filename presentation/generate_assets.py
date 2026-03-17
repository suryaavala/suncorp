"""Generate presentation image assets using Google Gemini.

Generates branded images for the Streamlit presentation deck
and saves them to the assets/ directory.

Requires GEMINI_API_KEY environment variable to be set.
"""
import os
import sys
from pathlib import Path

from google import genai
from google.genai import types

ASSETS_DIR = Path(__file__).parent / "assets"

IMAGE_PROMPTS = {
    "title_bg.png": (
        "A professional, abstract, geometric background using dark green "
        "and gold colors, representing financial technology, data science, "
        "and artificial intelligence. Modern, clean, corporate aesthetic. "
        "No text. High resolution."
    ),
    "rag_architecture.png": (
        "A clean, minimalist enterprise architecture flowchart showing "
        "documents flowing into a vector database, being retrieved, and "
        "processed by an AI agent, using green and gold brand colors on "
        "a white background. Professional infographic style. No text labels."
    ),
}


def generate_images():
    """Generate all presentation assets using Gemini image generation."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please run: source .env")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, prompt in IMAGE_PROMPTS.items():
        output_path = ASSETS_DIR / filename

        if output_path.exists():
            print(f"  SKIP: {filename} already exists.")
            continue

        print(f"  Generating: {filename}...")
        try:
            response = client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                ),
            )

            if response.generated_images:
                image = response.generated_images[0]
                image.image.save(str(output_path))
                print(f"  SAVED: {output_path}")
            else:
                print(f"  WARNING: No image returned for {filename}.")
                print("  Creating placeholder...")
                _create_placeholder(output_path, filename)

        except Exception as e:
            print(f"  ERROR generating {filename}: {e}")
            print("  Creating placeholder...")
            _create_placeholder(output_path, filename)

    print("\nAsset generation complete.")


def _create_placeholder(path, filename):
    """Create a simple placeholder image when Gemini generation fails."""
    try:
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new("RGB", (1200, 675), color="#004647")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        except (OSError, IOError):
            font = ImageFont.load_default()

        text = f"[Placeholder: {filename}]"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (1200 - text_width) // 2
        y = (675 - text_height) // 2
        draw.text((x, y), text, fill="#FFCD05", font=font)
        img.save(str(path))
        print(f"  SAVED placeholder: {path}")

    except ImportError:
        print(f"  SKIP placeholder (Pillow not installed): {path}")


if __name__ == "__main__":
    print("Generating presentation assets...\n")
    generate_images()
