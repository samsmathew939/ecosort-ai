# EcoSort AI ♻️

**Real-time waste classification app — built to solve a real problem**

## What It Does

Point your phone camera at a waste item → the app classifies it → it tells you how and where to dispose of it correctly.

## Why I Built It

Too much recyclable material ends up in landfill because people don't know *where* it goes. EcoSort closes that gap: instant disposal guidance at the moment you're standing in front of the bin.

## Tech Stack

- **Frontend:** Streamlit (Python web app)
- **AI Model:** YOLOv8 on the TrashNet dataset (6 waste classes) — *in progress; current build uses a simulated classifier as a working demo*
- **Location data:** Google Maps Places API for recycling centers *(planned)*
- **Hosting:** Streamlit Community Cloud (free)

## Status

🚧 **MVP in active development.** The app scaffold runs end-to-end (camera → classification → disposal instruction → nearby centers). The classification is currently simulated while the YOLOv8 model is being integrated.

**Roadmap:**
- [x] Working app scaffold (camera input, results UI, zip-code lookup)
- [ ] Replace simulated classifier with YOLOv8 pre-trained model
- [ ] Fine-tune on TrashNet for 6 waste classes
- [ ] Live Google Maps recycling-center lookup
- [ ] Public deployment on Streamlit Cloud

## Quick Start

```bash
# Clone & run locally
git clone https://github.com/samsm/ecosort-ai.git
cd ecosort-ai
pip install -r requirements.txt
streamlit run app.py
```

## What's Next

- Real YOLOv8 inference (replacing the demo classifier)
- Mobile app expansion (React Native)
- Multi-language support

---

Built by Sam Mathew — open source.
