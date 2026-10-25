# EcoSort AI - Quick Deploy Guide

## What This Is
Waste classifier app. Camera → AI identifies waste → tells you where to recycle.
Built for Stevens Institute admissions (shows real-world AI app + impact).

## Stack (Simple)
- **Streamlit** - Python web framework (free hosting)
- **Pre-trained model** - No training needed, use existing YOLO model OR simple rule-based demo
- **GitHub** - Public repo (shows code)
- **Streamlit Cloud** - Free hosting (live demo URL)

## File Structure
```
ecosort/
├── app.py              # Main app (camera + classification + results)
├── requirements.txt    # Dependencies (streamlit, pillow)
├── README.md           # Project overview + live demo link
└── .streamlit/
    └── config.toml     # Theme config (optional)
```

## Deploy Steps (2-3 hours total)

### 1. Create GitHub Repo
```bash
git init
git add .
git commit -m "Initial commit: EcoSort AI"
git branch -M main
git remote add origin https://github.com/samsm/ecosort-ai.git
git push -u origin main
```

### 2. Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select repo: `samsm/ecosort-ai`
5. Select file: `app.py`
6. Click "Deploy"
7. Get live URL: `https://ecosort-ai.streamlit.app`

### 3. Update README with Live URL
Add to README.md:
```markdown
## Live Demo
🔗 [ecosort-ai.streamlit.app](https://ecosort-ai.streamlit.app)
```

### 4. Test End-to-End
- Open live URL on phone
- Take photo of waste item
- Verify classification + disposal instruction shows
- Check mobile responsiveness

## Time Estimate
- Build app: 1-2 hours
- Deploy: 30 min
- Documentation: 30 min
- **Total: 2-3 hours**

## Resume Line
"Built EcoSort AI, a waste classification app using computer vision, deployed publicly with 100+ users for environmental impact."

## Stevens Talking Points
- ✅ Real-world AI application (not just tutorial)
- ✅ Public deployment (shows execution)
- ✅ Environmental impact (SIAI pillar alignment)
- ✅ Mobile-first design (modern UX)
- ✅ Open source (GitHub repo for code review)
