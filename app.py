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


def classify(image):
    """Run real inference. Returns (label, confidence) or raises."""
    model = load_model()
    if model is None:
        raise FileNotFoundError("model-missing")
    result = model(image, verbose=False)[0]
    label = result.names[result.probs.top1]
    confidence = float(result.probs.top1conf)
    return label, confidence


camera_input = st.camera_input("📸 Take a photo of a waste item")

if camera_input:
    image = Image.open(camera_input).convert("RGB")
    st.image(image, caption="Captured image", use_container_width=True)

    with st.spinner("🔍 Analyzing waste type..."):
        try:
            predicted_type, confidence = classify(image)
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

    st.markdown("### 🗺️ Nearby Recycling Centers")
    st.write("Enter your zip code to find drop-off locations:")
    zip_code = st.text_input("Zip code", placeholder="07030")
    if zip_code:
        st.caption(
            "Live recycling-center lookup is on the roadmap. "
            "For now, search Earth911 or your town's public-works site."
        )

# Footer
st.markdown("---")
st.caption("Built by Sam Mathew")
st.caption("[GitHub Repo](https://github.com/samsmathew939/ecosort-ai)")
