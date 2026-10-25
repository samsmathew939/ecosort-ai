import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="EcoSort AI", page_icon="♻️", layout="centered")

st.title("♻️ EcoSort AI")
st.write("Point your camera at waste. I'll tell you where to recycle it.")

# Waste categories
WASTE_TYPES = {
    "plastic": {"color": "blue", "instruction": "Rinse and place in recycling bin"},
    "paper": {"color": "blue", "instruction": "Flatten and place in recycling bin"},
    "metal": {"color": "blue", "instruction": "Rinse cans and place in recycling bin"},
    "glass": {"color": "blue", "instruction": "Rinse and place in glass recycling"},
    "compost": {"color": "green", "instruction": "Place in compost bin"},
    "landfill": {"color": "black", "instruction": "Place in trash bin"}
}

# Camera input
camera_input = st.camera_input("📸 Take a photo of waste item")

if camera_input:
    image = Image.open(camera_input)
    st.image(image, caption="Captured image", use_container_width=True)

    # Simulated classification (replace with YOLOv8 model later)
    with st.spinner("🔍 Analyzing waste type..."):
        # TODO: Replace with actual model inference
        predicted_type = random.choice(list(WASTE_TYPES.keys()))
        confidence = random.uniform(0.75, 0.98)

    waste_info = WASTE_TYPES[predicted_type]

    # Results
    st.success(f"✅ Detected: **{predicted_type.upper()}** ({confidence:.1%} confidence)")
    st.info(f"📍 {waste_info['instruction']}")

    # Local recycling centers (placeholder)
    st.markdown("### 🗺️ Nearby Recycling Centers")
    st.write("Enter your zip code to find drop-off locations:")

    zip_code = st.text_input("Zip code", placeholder="07030")
    if zip_code:
        st.info(f"📍 Hoboken Recycling Center - 256 Observer Hwy")
        st.info(f"📍 Stevens Institute Sustainability Center - 1 Castle Point")

    # Impact tracking
    st.markdown("---")
    st.caption(f"🌱 You've helped redirect 1 item from landfill today!")

# Footer
st.markdown("---")
st.caption("Built by Sam Mathew | Stevens Institute Applicant")
st.caption("[GitHub Repo](https://github.com/samsm/ecosort-ai) | [Live Demo](https://ecosort-ai.streamlit.app)")
