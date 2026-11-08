import json
import urllib.request
import streamlit as st
from PIL import Image
from pathlib import Path

st.set_page_config(page_title="EcoSort AI", page_icon="♻️", layout="centered")

st.title("♻️ EcoSort AI")
st.write("Point your camera at waste. I'll tell you how to dispose of it.")

# TrashNet classes (what the model was trained on) → disposal guidance
WASTE_TYPES = {
    "cardboard": {"instruction": "Flatten and place in recycling bin"},
    "glass": {"instruction": "Rinse and place in glass recycling"},
    "metal": {"instruction": "Rinse cans and place in recycling bin"},
    "paper": {"instruction": "Place in recycling bin (keep it dry)"},
    "plastic": {"instruction": "Rinse and check the resin code before recycling"},
    "trash": {"instruction": "Not recyclable — place in landfill/trash bin"},
}

MODEL_PATH = Path(__file__).parent / "models" / "ecosort.pt"


@st.cache_resource
def load_model():
    """Load the trained YOLOv8 classifier. Returns None if unavailable."""
    if not MODEL_PATH.exists():
        return None
    from ultralytics import YOLO
    return YOLO(str(MODEL_PATH))


# Barcode → disposal. Maps Open Food Facts packaging terms to our waste classes.
PACKAGING_MAP = {
    "metal": "metal", "aluminium": "metal", "aluminum": "metal", "can": "metal",
    "steel": "metal", "tin": "metal",
    "glass": "glass",
    "plastic": "plastic", "pet": "plastic", "hdpe": "plastic", "bottle": "plastic",
    "cardboard": "cardboard", "carton": "cardboard", "box": "cardboard",
    "paper": "paper",
}


def read_barcode(image):
    """Read a UPC/EAN barcode from the image. Returns code string or None.

    Safely wrapped: if pyzbar / the native zbar lib isn't available, or no
    barcode is found, returns None so the app falls back to the AI classifier.
    """
    try:
        from pyzbar.pyzbar import decode
        found = decode(image)
        for b in found:
            if b.type in ("EAN13", "EAN8", "UPCA", "UPCE"):
                return b.data.decode("utf-8")
        return found[0].data.decode("utf-8") if found else None
    except Exception:
        return None


def lookup_product(barcode):
    """Look up a barcode on Open Food Facts (free, no key).

    Returns (product_name, waste_type) or None. Never raises.
    """
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        req = urllib.request.Request(url, headers={"User-Agent": "EcoSort/1.0"})
        with urllib.request.urlopen(req, timeout=6) as r:
            data = json.load(r)
        if data.get("status") != 1:
            return None
        product = data["product"]
        name = product.get("product_name") or "Unknown product"
        terms = " ".join(str(product.get(k, "")) for k in
                         ("packaging", "packaging_tags", "packaging_materials")).lower()
        for keyword, waste in PACKAGING_MAP.items():
            if keyword in terms:
                return name, waste
        return name, None
    except Exception:
        return None


def classify(image):
    """Run real inference. Returns (label, confidence, top3) or raises."""
    model = load_model()
    if model is None:
        raise FileNotFoundError("model-missing")
    result = model(image, verbose=False)[0]
    label = result.names[result.probs.top1]
    confidence = float(result.probs.top1conf)
    top5 = result.probs.top5
    top5conf = result.probs.top5conf.tolist()
    top3 = [(result.names[i], c) for i, c in zip(top5, top5conf)][:3]
    return label, confidence, top3


st.info(
    "📷 **For best results:** photograph the item against a plain, single-color "
    "background (a table, wall, or floor) with nothing else in frame. Fill the "
    "frame with the item. Clutter or busy backgrounds can confuse the AI. "
    "**If the item has a barcode, point it at the camera** — EcoSort reads it for a "
    "more accurate result."
)

camera_input = st.camera_input("📸 Take a photo of a waste item")

if camera_input:
    image = Image.open(camera_input).convert("RGB")
    st.image(image, caption="Captured image", use_container_width=True)

    # 1. Try the barcode first — most reliable for packaged items (cans, bottles).
    with st.spinner("🔍 Checking for a barcode..."):
        barcode = read_barcode(image)
        product = lookup_product(barcode) if barcode else None

    handled = False
    if product and product[1]:
        name, predicted_type = product
        info = WASTE_TYPES[predicted_type]
        st.success(f"✅ Scanned: **{name}** → **{predicted_type.upper()}**")
        st.info(f"📍 {info['instruction']}")
        st.caption(f"Identified from barcode {barcode} via Open Food Facts.")
        handled = True
    elif product:
        st.caption(f"📦 Found barcode for **{product[0]}**, but no packaging info — using AI instead.")

    # 2. Fall back to the AI vision classifier.
    if not handled:
        with st.spinner("🔍 Analyzing waste type with AI..."):
            try:
                predicted_type, confidence, top3 = classify(image)
            except FileNotFoundError:
                st.error(
                    "Model not loaded. Train it with the notebook in `train/` and "
                    "place the weights at `models/ecosort.pt`. See `train/README.md`."
                )
                st.stop()
            except Exception as e:
                st.error(f"Classification failed: {e}")
                st.stop()

        info = WASTE_TYPES.get(predicted_type, {"instruction": "No disposal guidance available."})
        st.success(f"✅ Detected: **{predicted_type.upper()}** ({confidence:.1%} confidence)")
        st.info(f"📍 {info['instruction']}")

        # Show alternatives — a single photo can misread (e.g. a can seen edge-on).
        others = ", ".join(f"{name} {c:.0%}" for name, c in top3[1:])
        if others:
            st.caption(f"Other possibilities: {others}")
        if confidence < 0.70:
            st.warning(
                "⚠️ Low confidence — try another angle or a plainer background. "
                "Shiny or partly-visible items (like cans) can read as paper or plastic. "
                "Tip: if it has a barcode, make sure the barcode is clearly visible."
            )

    st.markdown("### 🗺️ Nearby Recycling Centers")
    zip_code = st.text_input("Enter your zip code to find drop-off locations:", placeholder="07030")
    if zip_code.strip():
        query = f"recycling+centers+near+{zip_code.strip()}"
        st.link_button(
            "🔎 Find recycling centers on Google Maps",
            f"https://www.google.com/maps/search/{query}",
        )
        st.caption("Opens Google Maps with drop-off locations near your zip code.")

# Footer
st.markdown("---")
st.caption("Built by Sam Mathew")
st.caption("[GitHub Repo](https://github.com/samsmathew939/ecosort-ai)")
