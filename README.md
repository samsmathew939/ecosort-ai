# EcoSort AI ♻️

**Real-time waste classification app — built to solve a real problem**

🔗 **Live demo:** https://ecosort-ai-trash-sorter.streamlit.app/

## What It Does

Point your phone camera at a waste item → the app classifies it → it tells you how and where to dispose of it correctly. Packaged products can also be identified by **barcode** for a more accurate result.

## Why I Built It

Too much recyclable material ends up in landfill because people don't know *where* it goes. EcoSort closes that gap: instant disposal guidance at the moment you're standing in front of the bin.

## Tech Stack

- **Frontend:** Streamlit (Python web app)
- **AI Model:** YOLOv8 image classifier trained on the TrashNet dataset (6 classes: cardboard, glass, metal, paper, plastic, trash)
- **Barcode:** pyzbar + Open Food Facts API — identifies packaged products and their packaging material
- **Location data:** zip-code recycling-center lookup via Google Maps
- **Hosting:** Streamlit Community Cloud (free)

## Status

✅ **Live and working.** End-to-end: camera → real YOLOv8 inference → disposal instruction, plus barcode scanning and a recycling-center lookup. The classifier is trained on TrashNet (6 classes). Validation accuracy: **91.5% top-1**.

**Roadmap:**
- [x] Working app scaffold (camera input, results UI)
- [x] Real YOLOv8 inference wired in
- [x] Model trained on TrashNet and weights committed
- [x] Public deployment on Streamlit Cloud
- [x] Barcode scanning for packaged products
- [x] Recycling-center lookup (Google Maps)

## Quick Start

```bash
# Clone & run locally
git clone https://github.com/samsmathew939/ecosort-ai.git
cd ecosort-ai
pip install -r requirements.txt
streamlit run app.py
```

## Train the model

The trained weights (`models/ecosort.pt`, ~3 MB) are produced by the notebook in `train/EcoSort_TrainTrashNet.ipynb` (Colab, free T4 GPU, ~10 min). Set runtime to GPU, Run all, download `ecosort.pt`, and place it in `models/`. A CPU equivalent is in `train/train_local.py`.

## Deploy (Streamlit Community Cloud, free)

Deployed from this repo at **https://ecosort-ai-trash-sorter.streamlit.app/**. To redeploy your own: share.streamlit.io → New app → `samsmathew939/ecosort-ai`, `main`, `app.py`.

## What's Next

- Mobile app expansion (React Native)
- Multi-language support
- Broader product coverage for barcode lookups

---

Built by Sam Mathew — open source.
