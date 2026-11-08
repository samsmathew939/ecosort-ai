# EcoSort — Build Plan to Admissions-Worthy

**Goal:** real, honest, deployed CV project with genuine impact. No fabricated metrics.
**Owner:** Sam Mathew · **Updated:** 2026-10-25

---

## Ordered steps (by impact)

### 1. Real classifier (biggest authenticity gap)
Replace `random.choice` with a real model. **Approach: train YOLOv8-cls on TrashNet.**
- [x] Pick approach (trained YOLOv8-cls on TrashNet)
- [x] Wire real inference into `app.py` with real confidence scores
- [x] Handle errors + loading states (honest: no fake fallback if weights missing)
- [ ] **← YOU: run `train/EcoSort_TrainTrashNet.ipynb` in Colab, drop weights at `models/ecosort.pt`**

### 2. Deploy live (proves it's real)
- [ ] Deploy to Streamlit Community Cloud, pin Python via `runtime.txt`
- [ ] Verify camera + classification work on mobile
- [ ] Put live URL in README (remove the fake one in `app.py:55`)

### 3. Honest documentation
- [ ] `ARCHITECTURE.md` — system diagram, model choice, why
- [ ] 2–3 real screenshots → `screenshots/`
- [ ] README: real status, real stack, no invented numbers

### 4. Real recycling-center lookup
- [ ] Replace hardcoded Hoboken/Stevens with real data (Google Places API or Earth911)
- [ ] Graceful fallback when no results

### 5. Real impact (only if genuinely done)
- [ ] QR code → live app, place where people actually use it
- [ ] Log real scans (opt-in, no PII); only report numbers that happened

### 6. Portfolio polish
- [ ] 1-page problem/solution/impact summary
- [ ] GitHub issues for future features (mobile app, more classes)

---

## Blocking decision: classifier approach

Local machine is Python 3.14 + no GPU → no local torch. Options:

| Approach | Real "I built ML"? | Cost | Effort | Deploys clean? |
|----------|-------------------|------|--------|----------------|
| **A. Train YOLOv8-cls on TrashNet** (Colab GPU) | Strongest | Free | Afternoon | Yes (small .pt committed) |
| **B. Vision LLM API** (Claude/GPT-4V) | Weaker (API call) | ~$0.01/scan | ~1 hr | Yes (API key secret) |
| **C. Pretrained HF TrashNet model** | Medium | Free | ~2 hr | Yes |

Recommendation: **A** — best admissions story, free, and a real training run Sam can explain.
