import json
import re
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


def load_image(src):
    """Open an uploaded/captured image, bounding its size to avoid memory blowups."""
    img = Image.open(src)
    img.thumbnail((4000, 4000))  # downscale oversized uploads in place
    return img.convert("RGB")


def _safe(text):
    """Escape markdown so untrusted API/barcode text can't inject formatting or links."""
    return re.sub(r"([\\`*_{}\[\]()#+\-.!|<>~])", r"\\\1", str(text))


def read_barcode(image):
    """Read a UPC/EAN barcode from the image. Returns code string or None.

    Camera photos are often small/blurry, so we try several preprocessed
    variants (grayscale, 2x upscale, autocontrast) to boost decode success.
    Safely wrapped: if pyzbar / the native zbar lib isn't available, or no
    barcode is found, returns None.
    """
    try:
        from pyzbar.pyzbar import decode
        from PIL import ImageOps
    except Exception:
        return None

    variants = [image]
    try:
        gray = ImageOps.grayscale(image)
        w, h = gray.size
        variants += [gray, ImageOps.autocontrast(gray)]
        if w * h <= 2_000_000:  # only upscale small images (avoids memory blowups)
            variants.append(gray.resize((w * 2, h * 2)))
    except Exception:
        pass

    for v in variants:
        try:
            found = decode(v)
        except Exception:
            continue
        if found:
            for b in found:
                if b.type in ("EAN13", "EAN8", "UPCA", "UPCE"):
                    return b.data.decode("utf-8")
            return found[0].data.decode("utf-8")
    return None


def lookup_product(barcode):
    """Look up a barcode on Open Food Facts (free, no key).

    Returns (product_name, waste_type) or None. Never raises.
    """
    if not barcode or not barcode.isdigit():
        return None
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


def recycling_lookup(key):
    """Shared zip-code → Google Maps recycling-center lookup."""
    st.markdown("### 🗺️ Nearby Recycling Centers")
    zip_code = st.text_input("Enter your zip code to find drop-off locations:",
                             placeholder="07030", key=key)
    if zip_code.strip():
        query = f"recycling+centers+near+{zip_code.strip()}"
        st.link_button("🔎 Find recycling centers on Google Maps",
                       f"https://www.google.com/maps/search/{query}")
        st.caption("Opens Google Maps with drop-off locations near your zip code.")


tab_ai, tab_barcode = st.tabs(["📷 Identify item", "🔖 Scan barcode"])

# --- Tab 1: AI photo classification ---
with tab_ai:
    st.info(
        "📷 **For best results:** photograph the item against a plain, single-color "
        "background (table, wall, or floor) with nothing else in frame. Fill the frame "
        "with the item. Clutter or busy backgrounds can confuse the AI. "
        "**For packaged items (cans, bottles), use the 🔖 Scan barcode tab instead** — "
        "it's more accurate."
    )
    cam = st.camera_input("📸 Take a photo of a waste item", key="ai_cam")
    if cam:
        image = load_image(cam)
        with st.spinner("🔍 Analyzing with AI..."):
            try:
                predicted_type, confidence, top3 = classify(image)
            except FileNotFoundError:
                st.error("Model not loaded. See `train/README.md` to add `models/ecosort.pt`.")
                st.stop()
            except Exception as e:
                st.error(f"Classification failed: {e}")
                st.stop()
        info = WASTE_TYPES.get(predicted_type, {"instruction": "No disposal guidance available."})
        st.success(f"✅ Detected: **{predicted_type.upper()}** ({confidence:.1%} confidence)")
        st.info(f"📍 {info['instruction']}")
        others = ", ".join(f"{name} {c:.0%}" for name, c in top3[1:])
        if others:
            st.caption(f"Other possibilities: {others}")
        if confidence < 0.70:
            st.warning(
                "⚠️ Low confidence — try another angle or a plainer background. Shiny or "
                "partly-visible items (like cans) can read as paper or plastic. If it has a "
                "barcode, use the 🔖 Scan barcode tab."
            )
        recycling_lookup("zip_ai")

# --- Tab 2: Barcode scan ---
with tab_barcode:
    st.info(
        "🔖 **Scan a barcode** for packaged products (cans, bottles, snacks). Hold the "
        "**barcode flat and close**, fill the frame, keep it steady with good light. "
        "You can also upload a barcode photo."
    )
    bc_cam = st.camera_input("📸 Point the barcode at the camera", key="bc_cam")
    bc_file = st.file_uploader("…or upload a barcode image", type=["png", "jpg", "jpeg"],
                               key="bc_file")
    source = bc_cam or bc_file
    if source:
        image = load_image(source)
        with st.spinner("🔍 Reading barcode..."):
            barcode = read_barcode(image)
            product = lookup_product(barcode) if barcode else None
        if not barcode:
            st.error(
                "❌ Couldn't read a barcode. Get closer so the barcode fills the frame, "
                "hold steady, and avoid glare — then try again. Or use the 📷 Identify tab."
            )
        elif product and product[1]:
            name, predicted_type = product
            info = WASTE_TYPES[predicted_type]
            st.success(f"✅ Scanned: **{_safe(name)}** → **{predicted_type.upper()}**")
            st.info(f"📍 {info['instruction']}")
            st.caption(f"Barcode {_safe(barcode)} · identified via Open Food Facts.")
            recycling_lookup("zip_bc")
        elif product:
            st.warning(
                f"📦 Read barcode **{_safe(barcode)}** (**{_safe(product[0])}**), but no "
                "packaging info is on file. Use the 📷 Identify tab to classify it visually."
            )
        else:
            st.warning(
                f"📦 Read barcode **{_safe(barcode)}**, but it isn't in the Open Food Facts "
                "database. Use the 📷 Identify tab to classify it visually."
            )

# Footer
st.markdown("---")
st.caption("Built by Sam Mathew")
st.caption("[GitHub Repo](https://github.com/samsmathew939/ecosort-ai)")
