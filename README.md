# EcoSort AI ♻️

**Real-time waste classification app — built to solve a real problem**

## What It Does

Point your phone camera at a waste item → the app classifies it → it tells you how and where to dispose of it correctly.

## Why I Built It

Too much recyclable material ends up in landfill because people don't know *where* it goes. EcoSort closes that gap: instant disposal guidance at the moment you're standing in front of the bin.

## Tech Stack

- **Frontend:** Streamlit (Python web app)
- **AI Model:** YOLOv8 image classifier trained on the TrashNet dataset (6 classes: cardboard, glass, metal, paper, plastic, trash)
- **Location data:** recycling-center lookup *(planned)*
- **Hosting:** Streamlit Community Cloud (free)

## Status

✅ **Working MVP.** End-to-end: camera → real YOLOv8 inference → disposal instruction. The classifier is trained on TrashNet (6 classes). Validation accuracy: **{{TOP1}}% top-1**. Weights load from `models/ecosort.pt`.

**Roadmap:**
- [x] Working app scaffold (camera input, results UI)
- [x] Real YOLOv8 inference wired in
- [x] Model trained on TrashNet and weights committed
- [ ] Public deployment on Streamlit Cloud
- [ ] Live recycling-center lookup

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

1. Push this repo to GitHub with `models/ecosort.pt` committed.
2. Go to share.streamlit.io → New app → pick `samsmathew939/ecosort-ai`, main branch, `app.py`.
3. Deploy. You get a public URL to demo.

## What's Next

- Mobile app expansion (React Native)
- Multi-language support
- Live recycling-center lookup

---

Built by Sam Mathew — open source.
