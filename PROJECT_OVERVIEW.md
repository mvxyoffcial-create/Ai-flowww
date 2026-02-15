# 🎬 AI Flow Video Generator - Complete Project Overview

## 📝 What is This?

AI Flow is a video transition generator inspired by Gemini Flow. It takes two images (start and end frames) and a text description, then generates a smooth transition video between them using AI.

**Example**: Upload a picture of a small plant and a giant tree, add prompt "plant grows into giant tree", and get an amazing transition video!

## 🎯 Key Features

✨ **Simple Interface**: Upload 2 images, describe transition, generate video
🤖 **AI-Powered**: Uses Stable Diffusion or OpenCV interpolation  
⚡ **Fast Generation**: 5-30 seconds depending on settings
🎨 **Customizable**: Adjust frames, FPS, and transition style
🆓 **Free to Deploy**: Works perfectly on Koyeb's free tier
🚀 **Production Ready**: Includes Docker, tests, and deployment guides

## 📦 What's Included

### Core Application Files

1. **app.py** - Full version with Stable Diffusion AI
   - Uses InstructPix2Pix model
   - Best quality transitions
   - Requires GPU or powerful CPU
   - Memory: 4-8 GB RAM

2. **app_lite.py** - Lightweight version for Koyeb
   - Uses OpenCV interpolation
   - Fast CPU processing
   - Good quality for simple transitions
   - Memory: 512 MB RAM (perfect for free tier!)

3. **templates/index.html** - Beautiful web interface
   - Modern, responsive design
   - Drag & drop image upload
   - Real-time preview
   - Example prompts included

### Configuration Files

4. **requirements.txt** - Python packages for full version
5. **requirements-lite.txt** - Python packages for lite version
6. **Dockerfile** - Docker config for full version
7. **Dockerfile.lite** - Docker config for lite version (Koyeb)
8. **.gitignore** - Git ignore rules

### Documentation

9. **README.md** - Main documentation
10. **DEPLOYMENT.md** - Complete Koyeb deployment guide
11. **test.py** - Test script to verify everything works
12. **start.sh** - Quick start script for easy setup

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (HTML/CSS/JS)          │
│  - Image upload                         │
│  - Prompt input                         │
│  - Video preview                        │
└─────────────┬───────────────────────────┘
              │ HTTP POST
              ↓
┌─────────────────────────────────────────┐
│          Backend (Flask/Python)         │
│  - Image processing                     │
│  - Frame generation                     │
│  - Video encoding                       │
└─────────────┬───────────────────────────┘
              │
      ┌───────┴────────┐
      ↓                ↓
┌──────────┐    ┌─────────────┐
│ Full AI  │    │    Lite     │
│ Stable   │    │   OpenCV    │
│Diffusion │    │Interpolation│
└──────────┘    └─────────────┘
```

## 🔧 How It Works

### Full Version (app.py)

1. User uploads two images and enters prompt
2. Images resized to 512x512
3. For each frame:
   - Blend images based on position
   - Pass through Stable Diffusion with prompt
   - Generate AI-enhanced frame
4. Compile frames into MP4 video
5. Return to user

**Pros**: Best quality, creative transitions
**Cons**: Slow (30-60s), needs GPU, high memory

### Lite Version (app_lite.py)

1. User uploads two images and enters prompt
2. Images resized to 512x512
3. For each frame:
   - Calculate optical flow between images
   - Interpolate pixels based on flow
   - Apply smoothing
4. Compile frames into MP4 video
5. Return to user

**Pros**: Fast (5-10s), CPU only, low memory
**Cons**: Simpler transitions (but still good!)

## 🚀 Deployment Options

### Option 1: Koyeb (Recommended for Free Hosting)

**Best for**: Free hosting, small-medium traffic
**Version**: Use Lite (app_lite.py)
**Memory**: 512 MB (free tier)
**Setup time**: 15 minutes

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push origin main

# 2. Deploy on Koyeb dashboard
# - Connect GitHub repo
# - Use Dockerfile.lite
# - Select Nano instance (free)
# - Deploy!
```

See **DEPLOYMENT.md** for complete guide.

### Option 2: Run Locally

**Best for**: Development, testing, personal use
**Version**: Either version
**Memory**: 512 MB (lite) or 4+ GB (full)

```bash
# Quick start
./start.sh

# Or manual
pip install -r requirements-lite.txt
python app_lite.py
```

### Option 3: Other Cloud Platforms

**Heroku**: Similar to Koyeb, use lite version
**Railway**: Similar to Koyeb, use lite version  
**Render**: Similar to Koyeb, use lite version
**AWS/GCP/Azure**: Use full version with GPU instance

## 📊 Performance Comparison

| Feature | Lite Version | Full Version |
|---------|-------------|--------------|
| Speed | ⚡⚡⚡ 5-10s | 🐌 30-60s |
| Quality | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| Memory | 512 MB | 4-8 GB |
| GPU Required | ❌ No | ✅ Yes |
| Koyeb Free Tier | ✅ Yes | ❌ No |
| Cost | $0/month | $50-200/month |

## 🎨 Usage Examples

### Simple Transitions
```
Start: Photo of a seed
End: Photo of a tree
Prompt: "seed grows into tree"
Settings: 16 frames, 8 FPS
Result: 2-second growth animation
```

### Creative Transitions
```
Start: Day cityscape
End: Night cityscape
Prompt: "day transforms into night, cinematic lighting"
Settings: 24 frames, 12 FPS
Result: 2-second day-to-night transition
```

### Portrait Aging
```
Start: Young person photo
End: Old person photo
Prompt: "person ages naturally over time"
Settings: 32 frames, 8 FPS
Result: 4-second aging effect
```

## 🔐 Security Considerations

1. **File Upload Limits**: Set max file size (e.g., 10 MB)
2. **Rate Limiting**: Prevent abuse (add Flask-Limiter)
3. **Input Validation**: Sanitize file types and prompts
4. **Timeout**: Set reasonable generation timeout
5. **HTTPS**: Always use HTTPS in production (Koyeb provides free SSL)

## 🔄 Future Enhancements

Potential features to add:

- [ ] Multiple transition styles (fade, wipe, zoom)
- [ ] Batch processing (multiple video pairs)
- [ ] Custom video length
- [ ] Audio/music support
- [ ] GIF export option
- [ ] Template library
- [ ] User accounts and history
- [ ] API for programmatic access
- [ ] Mobile app (React Native)
- [ ] Video-to-video (not just images)

## 📈 Scaling

### Current Capacity (Koyeb Free Tier)
- Concurrent users: 1-2
- Videos/hour: ~30-60 (lite version)
- Response time: 5-10 seconds

### To Scale Up
1. **Horizontal Scaling**: Add more instances
2. **Vertical Scaling**: Upgrade to larger instances
3. **Caching**: Cache common transitions
4. **Queue System**: Use Celery + Redis for background processing
5. **CDN**: Use for serving videos
6. **Database**: Store generated videos (PostgreSQL)

## 🧪 Testing

### Run All Tests
```bash
python test.py
```

### Manual Testing
```bash
# Start app
python app_lite.py

# In another terminal, test API
curl -X POST http://localhost:8000/generate \
  -F "image1=@test1.jpg" \
  -F "image2=@test2.jpg" \
  -F "prompt=smooth transition" \
  -F "num_frames=8" \
  -F "fps=8"
```

### Load Testing
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test
ab -n 100 -c 10 http://localhost:8000/health
```

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r requirements-lite.txt
```

### Issue: "Out of memory"
**Solution**: 
- Use lite version (app_lite.py)
- Reduce frames to 8-12
- Upgrade Koyeb instance

### Issue: "Video generation too slow"
**Solution**:
- Use lite version for faster results
- Reduce frame count
- Use full version with GPU for quality

### Issue: "Deployment fails on Koyeb"
**Solution**:
- Check you're using Dockerfile.lite
- Verify requirements-lite.txt exists
- Check build logs in Koyeb dashboard

## 💡 Tips for Best Results

### For Lite Version:
1. **Simple transitions work best**: Fade, morph, blend
2. **Use fewer frames**: 8-16 frames optimal
3. **Lower FPS**: 4-8 FPS looks good
4. **Similar images**: Better results with similar compositions
5. **Clear subjects**: Images with distinct subjects

### For Full Version:
1. **Creative prompts work**: "cinematic", "magical", "surreal"
2. **More frames**: 16-32 frames for smoothness
3. **Higher FPS**: 12-16 FPS for cinematic feel
4. **Experiment**: AI can handle complex transitions
5. **Be specific**: Detailed prompts = better results

## 📚 Learning Resources

### Python & Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)

### AI & Computer Vision
- [OpenCV Tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Stable Diffusion](https://github.com/Stability-AI/stablediffusion)
- [Diffusers Library](https://huggingface.co/docs/diffusers/)

### Deployment
- [Koyeb Docs](https://www.koyeb.com/docs)
- [Docker Tutorial](https://docs.docker.com/get-started/)
- [Gunicorn Deployment](https://docs.gunicorn.org/en/stable/deploy.html)

## 🤝 Contributing

Want to improve AI Flow? Here's how:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

Ideas for contributions:
- New transition algorithms
- UI improvements
- Performance optimizations
- Documentation updates
- Bug fixes

## 📄 License

MIT License - Free to use, modify, and distribute!

## 🙏 Credits

- **Stable Diffusion**: Stability AI
- **InstructPix2Pix**: Timothy Brooks et al.
- **OpenCV**: Open Source Computer Vision Library
- **Flask**: Pallets Projects
- **Koyeb**: Cloud hosting platform

## 📞 Support

Need help? Try these:

1. **Read the docs**: README.md, DEPLOYMENT.md
2. **Run tests**: `python test.py`
3. **Check logs**: Koyeb dashboard → Logs tab
4. **GitHub Issues**: Report bugs/request features
5. **Community**: Share your creations!

## 🎉 Get Started Now!

Ready to create amazing video transitions?

```bash
# Clone/download the project
git clone YOUR_REPO_URL

# Quick start
./start.sh

# Or deploy to Koyeb
# See DEPLOYMENT.md for full guide
```

---

**Made with ❤️ for the AI community**

Start creating amazing transitions today! 🚀
