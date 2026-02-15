# 🚀 Quick Reference Guide - AI Flow

## ⚡ TL;DR - Get Started in 5 Minutes

### For Local Testing
```bash
pip install -r requirements-lite.txt
python app_lite.py
# Visit http://localhost:8000
```

### For Koyeb Deployment
1. Push to GitHub
2. Connect to Koyeb
3. Use `Dockerfile.lite`
4. Deploy!

---

## 📁 File Structure

```
ai-flow/
├── app.py                  # Full version (GPU, Stable Diffusion)
├── app_lite.py            # Lite version (CPU, OpenCV) ⭐ USE THIS
├── requirements.txt        # Dependencies for full version
├── requirements-lite.txt   # Dependencies for lite ⭐ USE THIS
├── Dockerfile             # Docker for full version
├── Dockerfile.lite        # Docker for lite ⭐ USE THIS
├── templates/
│   └── index.html         # Frontend UI
├── static/                # (empty, for future assets)
├── README.md              # Main documentation
├── DEPLOYMENT.md          # Koyeb deployment guide
├── PROJECT_OVERVIEW.md    # Complete overview
├── test.py               # Test script
├── start.sh              # Quick start script
└── .gitignore            # Git ignore rules
```

---

## 🎯 Which Files to Use?

### For Koyeb Free Tier (Recommended)
- ✅ `app_lite.py`
- ✅ `requirements-lite.txt`
- ✅ `Dockerfile.lite`
- ✅ `templates/index.html`

### For Local Development
- ✅ `app_lite.py` (fast, CPU)
- OR `app.py` (slow, GPU, better quality)

### For Production with GPU
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `Dockerfile`

---

## 🔧 Quick Commands

### Installation
```bash
# Lite version (recommended)
pip install -r requirements-lite.txt

# Full version (GPU required)
pip install -r requirements.txt
```

### Run Locally
```bash
# Lite version
python app_lite.py

# Full version
python app.py
```

### Test
```bash
python test.py
```

### Docker Build
```bash
# Lite version
docker build -f Dockerfile.lite -t ai-flow-lite .

# Full version
docker build -t ai-flow .
```

### Docker Run
```bash
docker run -p 8000:8000 ai-flow-lite
```

---

## 🌐 API Endpoints

### Generate Video
```bash
POST /generate
Form Data:
  - image1: File (start frame)
  - image2: File (end frame)
  - prompt: String (transition description)
  - num_frames: Integer (8-32)
  - fps: Integer (4-16)

Response:
{
  "success": true,
  "video": "base64_encoded_video_data",
  "message": "Generated 16 frames successfully!"
}
```

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "mode": "lightweight"
}
```

---

## 🎨 Example Prompts

| Prompt | Description |
|--------|-------------|
| `smooth transition` | Basic morph |
| `house grows on giant tree` | Creative growth |
| `day to night, cinematic` | Lighting change |
| `portrait ages naturally` | Aging effect |
| `winter to spring landscape` | Season change |
| `city to futuristic metropolis` | Transformation |

---

## ⚙️ Recommended Settings

### Lite Version (Koyeb Free Tier)
- **Frames**: 8-16 (not 24-32)
- **FPS**: 4-8 (not 12-16)
- **Timeout**: 180 seconds
- **Workers**: 1
- **Memory**: 512 MB

### Full Version (GPU)
- **Frames**: 16-32
- **FPS**: 8-16
- **Timeout**: 300 seconds
- **Workers**: 1-2
- **Memory**: 4-8 GB

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Out of memory | Use `app_lite.py` + 8-16 frames |
| Timeout | Reduce frames, increase timeout |
| Port already in use | Change PORT env var |
| Module not found | `pip install -r requirements-lite.txt` |
| Build fails on Koyeb | Check Dockerfile.lite, requirements-lite.txt |

---

## 📊 Performance

| Metric | Lite Version | Full Version |
|--------|--------------|--------------|
| Speed | 5-10 seconds | 30-60 seconds |
| Quality | Good ⭐⭐⭐ | Excellent ⭐⭐⭐⭐⭐ |
| Memory | 512 MB | 4-8 GB |
| CPU | Yes | Yes (slow) |
| GPU | No | Yes (fast) |

---

## 🔗 Important Links

- **Koyeb**: https://www.koyeb.com/
- **Docker Hub**: https://hub.docker.com/
- **Flask Docs**: https://flask.palletsprojects.com/
- **OpenCV Docs**: https://docs.opencv.org/

---

## 📋 Deployment Checklist

### Before Deploying
- [ ] Test locally: `python test.py`
- [ ] Run app locally: `python app_lite.py`
- [ ] Test in browser: http://localhost:8000
- [ ] Generate test video
- [ ] Check files exist (see File Structure)

### Koyeb Deployment
- [ ] Push to GitHub
- [ ] Sign up on Koyeb
- [ ] Create new app
- [ ] Connect GitHub repo
- [ ] Select Dockerfile.lite
- [ ] Use Nano instance (512 MB)
- [ ] Set port to 8000
- [ ] Deploy
- [ ] Wait 5-10 minutes
- [ ] Test health endpoint
- [ ] Generate test video

### Post-Deployment
- [ ] Test health: `curl https://your-app.koyeb.app/health`
- [ ] Generate video via UI
- [ ] Check logs in Koyeb dashboard
- [ ] Monitor memory usage
- [ ] Share your URL!

---

## 💰 Cost Breakdown

### Koyeb Free Tier
- **Cost**: $0/month
- **Instances**: 1 Nano (512 MB)
- **Features**: SSL, CDN, auto-deploy
- **Perfect for**: Personal use, demos

### Koyeb Paid
- **Small**: $7/month (1 GB RAM)
- **Medium**: $14/month (2 GB RAM)
- **Large**: $28/month (4 GB RAM)

### AWS/GCP (GPU)
- **Cost**: $50-200/month
- **Instance**: GPU-enabled
- **Best for**: High quality, high volume

---

## 🎯 Next Steps

1. **Test locally**: Run `./start.sh`
2. **Deploy to Koyeb**: Follow DEPLOYMENT.md
3. **Customize**: Edit templates/index.html
4. **Share**: Tell others about your URL
5. **Improve**: Add features, optimize

---

## 📞 Need Help?

1. Read full docs: README.md, DEPLOYMENT.md, PROJECT_OVERVIEW.md
2. Run tests: `python test.py`
3. Check Koyeb logs
4. Open GitHub issue

---

**Happy creating! 🎬✨**
