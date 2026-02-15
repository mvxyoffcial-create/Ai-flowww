# 🎬 AI Flow - Video Transition Generator

Generate amazing transition videos between two images using AI, **just like Gemini Flow**!

[![Deploy to Koyeb](https://img.shields.io/badge/Deploy-Koyeb-blue?logo=koyeb)](https://www.koyeb.com/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🖼️ **Upload two images** (start and end frame)
- ✍️ **Natural language prompts** to describe transitions
- 🎞️ **Advanced optical flow** for smooth video transitions
- ⚡ **Real-time progress tracking** during generation
- 🎨 **Beautiful Gemini Flow-inspired UI** with animations
- 🚀 **Free deployment** on Koyeb (512 MB RAM works perfectly!)
- 📱 **Responsive design** - works on mobile and desktop

## 🎯 How It Works

1. Upload your **Start Frame** and **End Frame**
2. Describe the transition (e.g., "house grows on giant tree")
3. Choose frame count (8-32) and FPS (4-16)
4. Click "Generate Video"
5. Download your AI-generated transition video!

## 🚀 Quick Start (3 methods)

### Method 1: One-Line Setup
```bash
./setup.sh
# Choose option 1 for quick start
```

### Method 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements-lite.txt

# Run the app
python app_lite.py

# Visit http://localhost:8000
```

### Method 3: Docker
```bash
docker build -f Dockerfile.lite -t ai-flow .
docker run -p 8000:8000 ai-flow
```

## 🌐 Deploy to Koyeb (FREE!)

### Quick Deploy
1. **Fork/Clone this repo to GitHub**
2. **Sign up** at [koyeb.com](https://www.koyeb.com/)
3. **Create new app** → Connect GitHub
4. **Configure**:
   - Builder: Docker
   - Dockerfile: `Dockerfile.lite`
   - Port: `8000`
   - Instance: **Nano** (Free tier - 512 MB)
5. **Deploy** and wait 5-10 minutes!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guide.

## 📦 What's Included

```
ai-flow/
├── app_lite.py              # Main app (CPU, optimized for Koyeb)
├── app.py                   # Full version (GPU, Stable Diffusion)
├── requirements-lite.txt    # Lightweight dependencies
├── requirements.txt         # Full dependencies
├── Dockerfile.lite         # Docker for Koyeb
├── Dockerfile              # Docker for GPU version
├── templates/
│   └── index.html          # Beautiful UI
├── setup.sh                # Auto-setup script
├── test.py                 # Test suite
├── README.md               # This file
├── DEPLOYMENT.md           # Deployment guide
└── QUICK_START.md          # Quick reference

```

## 🎨 Example Prompts

| Prompt | Result |
|--------|--------|
| `house grows on giant tree` | Building morphs and grows into tree |
| `day transforms into night, cinematic` | Time-lapse lighting transition |
| `portrait ages from young to old` | Realistic aging effect |
| `winter landscape melts into spring` | Seasonal transformation |
| `city morphs into futuristic metropolis` | Architectural evolution |

## ⚙️ Technical Details

### Lite Version (Recommended for Koyeb)
- **Algorithm**: Advanced optical flow with bidirectional warping
- **Easing**: Smooth hermite interpolation
- **Processing**: CPU-optimized with bilateral filtering
- **Quality**: High quality with edge preservation
- **Speed**: 5-10 seconds per video
- **Memory**: Works perfectly on 512 MB RAM

### Full Version (For GPU Servers)
- **AI Model**: Stable Diffusion (InstructPix2Pix)
- **Quality**: Excellent with creative AI enhancements
- **Speed**: 30-60 seconds per video
- **Memory**: Requires 4-8 GB RAM + GPU

## 🛠️ Tech Stack

- **Backend**: Python 3.8+, Flask
- **Computer Vision**: OpenCV (optical flow, warping, filtering)
- **AI (Optional)**: Stable Diffusion, Diffusers
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Deployment**: Docker, Gunicorn
- **Hosting**: Koyeb (or any Docker platform)

## 🎯 Performance

| Metric | Lite Version | Full Version |
|--------|--------------|--------------|
| Speed | ⚡ 5-10s | 🐌 30-60s |
| Quality | ⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Outstanding |
| Memory | 512 MB | 4-8 GB |
| GPU | Not needed | Recommended |
| Free Hosting | ✅ Yes (Koyeb) | ❌ No |

## 🔧 Configuration

### Frame Settings
```javascript
8 frames  - Fast, good for previews
16 frames - Balanced (recommended)
24 frames - Smooth transitions
32 frames - Ultra smooth, cinematic
```

### FPS Settings
```javascript
4 FPS  - Slow motion effect
8 FPS  - Standard video (recommended)
12 FPS - Smooth playback
16 FPS - Fast, cinematic
```

## 🧪 Testing

Run the complete test suite:
```bash
python test.py
```

This tests:
- ✅ Package imports
- ✅ File structure
- ✅ Flask app initialization
- ✅ OpenCV functionality
- ✅ Frame generation

## 📊 API Reference

### POST /generate
Generate transition video

**Request:**
```bash
curl -X POST http://localhost:8000/generate \
  -F "image1=@start.jpg" \
  -F "image2=@end.jpg" \
  -F "prompt=smooth transition" \
  -F "num_frames=16" \
  -F "fps=8"
```

**Response:**
```json
{
  "success": true,
  "video": "base64_encoded_mp4_data",
  "message": "Generated 16 frames successfully!"
}
```

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "mode": "lightweight"
}
```

## 🐛 Troubleshooting

### Issue: Out of Memory on Koyeb
**Solution**: You're using the correct `app_lite.py`, right? Reduce frames to 8-12.

### Issue: Slow Generation
**Solution**: Reduce frame count or increase FPS for shorter video.

### Issue: Build Fails
**Solution**: Ensure you're using `Dockerfile.lite` and `requirements-lite.txt`.

## 💡 Pro Tips

1. **Similar compositions work best** - Images with similar subjects/layouts
2. **Use descriptive prompts** - "smooth cinematic transition" vs just "transition"
3. **Start with 16 frames** - Good balance of quality and speed
4. **Test locally first** - Make sure it works before deploying
5. **Check the examples** - Built-in prompts show what works well

## 🌟 Advanced Features

### Custom Algorithms
The lite version uses:
- Bidirectional optical flow
- Flow-based image warping
- Smooth hermite easing
- Bilateral filtering (edge-preserving)
- Adaptive sharpening
- Cross-fade blending

### UI Enhancements
- Gradient animations
- Real-time progress tracking
- Smooth transitions
- Responsive design
- Loading states
- Error handling

## 📄 License

MIT License - Free to use, modify, and distribute!

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🙏 Credits

- **Optical Flow**: OpenCV community
- **Stable Diffusion**: Stability AI
- **UI Inspiration**: Google Gemini Flow
- **Hosting**: Koyeb

## 📞 Support

- 📚 [Full Documentation](DEPLOYMENT.md)
- 🚀 [Quick Start Guide](QUICK_START.md)
- 💬 Open an issue for bugs/features
- ⭐ Star the repo if you like it!

## 🎉 Get Started Now!

```bash
# Clone the repo
git clone YOUR_REPO_URL
cd ai-flow

# Quick start
./setup.sh

# Or manual
pip install -r requirements-lite.txt
python app_lite.py
```

Visit http://localhost:8000 and start creating! 🎬

---

**Made with ❤️ for the AI community**

Deploy now → [koyeb.com](https://www.koyeb.com/) 🚀
