# 🚀 Koyeb Deployment Guide

Complete step-by-step guide to deploy AI Flow on Koyeb's free tier.

## 📋 Prerequisites

- GitHub account
- Koyeb account (sign up at https://www.koyeb.com/)
- Git installed on your computer

## 🎯 Step-by-Step Deployment

### 1. Prepare Your GitHub Repository

#### Create a new repository on GitHub:
```bash
# On GitHub.com:
# 1. Click "New repository"
# 2. Name it "ai-flow-video"
# 3. Set to Public
# 4. Don't initialize with README (we have one)
# 5. Click "Create repository"
```

#### Push your code:
```bash
# In your project folder
git init
git add .
git commit -m "Initial commit - AI Flow Video Generator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-flow-video.git
git push -u origin main
```

### 2. Configure for Koyeb Free Tier

Make sure your repository has:
- ✅ `Dockerfile.lite` (will be used as Dockerfile)
- ✅ `app_lite.py` (will be used as app.py)
- ✅ `requirements-lite.txt` (will be used as requirements.txt)
- ✅ `templates/index.html`
- ✅ Empty `static/` folder

### 3. Deploy on Koyeb

#### A. Sign Up
1. Go to https://www.koyeb.com/
2. Sign up with GitHub (recommended)
3. Verify your email

#### B. Create New App
1. Click **"Create App"** button
2. Select **"GitHub"** as source

#### C. Connect GitHub
1. Click **"Connect with GitHub"**
2. Authorize Koyeb to access your repos
3. Select your `ai-flow-video` repository

#### D. Configure Build Settings

**Builder Settings:**
```
Builder: Docker
Dockerfile: Dockerfile.lite
```

**Port Settings:**
```
Port: 8000
Protocol: HTTP
```

**Instance Settings:**
```
Instance Type: Nano (Free Tier)
- 512 MB RAM
- 0.1 vCPU
Region: Choose closest to you (e.g., Washington DC, Frankfurt)
```

**Scaling:**
```
Min instances: 1
Max instances: 1
```

#### E. Environment Variables (Optional)
```
PORT=8000
PYTHONUNBUFFERED=1
```

#### F. Deploy!
1. Click **"Deploy"**
2. Wait 5-10 minutes for build
3. Monitor build logs

### 4. Access Your App

Once deployed, you'll get a URL like:
```
https://your-app-name-your-username.koyeb.app
```

Visit it and start generating videos! 🎉

## 🔧 Configuration Files for Koyeb

### Option A: Rename Files (Recommended)
```bash
# Copy lite version as main version
cp app_lite.py app.py
cp requirements-lite.txt requirements.txt
cp Dockerfile.lite Dockerfile

# Commit and push
git add .
git commit -m "Configure for Koyeb"
git push
```

### Option B: Modify Dockerfile
Keep filenames but update Dockerfile to use lite versions:
```dockerfile
COPY app_lite.py app.py
COPY requirements-lite.txt requirements.txt
```

## 📊 Monitoring

### View Logs
1. Go to Koyeb dashboard
2. Select your app
3. Click "Logs" tab
4. View real-time logs

### Check Health
```bash
curl https://your-app-name.koyeb.app/health
```

Should return:
```json
{
  "status": "healthy",
  "mode": "lightweight"
}
```

## ⚡ Performance Optimization

### For Free Tier (512 MB RAM):

1. **Use Lite Version** ✅
   - No heavy AI models
   - Fast CPU processing
   - Low memory usage

2. **Optimize Settings**:
   ```
   Workers: 1
   Threads: 1
   Timeout: 180 seconds
   ```

3. **Recommended User Settings**:
   - Frames: 8-16 (not 24-32)
   - FPS: 4-8 (not 12-16)
   - Image size: Auto-resized to 512x512

## 🐛 Common Issues & Solutions

### Issue 1: Build Fails
**Error**: "Requirements not found"
**Solution**: 
```bash
# Make sure requirements-lite.txt exists
ls requirements-lite.txt

# Or rename it
mv requirements-lite.txt requirements.txt
```

### Issue 2: Out of Memory
**Error**: "Container killed (OOMKilled)"
**Solution**:
- Confirm using `app_lite.py` (not `app.py`)
- Reduce frames to 8-12
- Check Dockerfile uses `requirements-lite.txt`

### Issue 3: Timeout
**Error**: "Request timeout"
**Solution**:
```dockerfile
# In Dockerfile, increase timeout
CMD ["gunicorn", "--timeout", "300", ...]
```

### Issue 4: Port Binding Failed
**Error**: "Cannot bind to port"
**Solution**:
```dockerfile
# Ensure PORT is 8000
ENV PORT=8000
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", ...]
```

### Issue 5: App Not Responding
**Checklist**:
- ✅ Build completed successfully?
- ✅ Health endpoint working?
- ✅ Logs show app started?
- ✅ Port 8000 exposed?

## 🎯 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app.koyeb.app/health
```

### 2. Generate Video
```bash
curl -X POST https://your-app.koyeb.app/generate \
  -F "image1=@test1.jpg" \
  -F "image2=@test2.jpg" \
  -F "prompt=smooth transition" \
  -F "num_frames=8" \
  -F "fps=8"
```

### 3. Load Test
```bash
# Use a tool like Apache Bench
ab -n 10 -c 2 https://your-app.koyeb.app/health
```

## 🔄 Updates & Redeployment

### Automatic Deployment
Koyeb auto-deploys on git push:
```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Koyeb automatically rebuilds and redeploys!
```

### Manual Redeploy
1. Go to Koyeb dashboard
2. Click your app
3. Click "Redeploy"
4. Confirm

## 💰 Cost Monitoring

### Free Tier Includes:
- ✅ 1 Nano instance (512 MB)
- ✅ Unlimited builds
- ✅ Automatic SSL
- ✅ Global CDN
- ✅ Custom domains

### Stay in Free Tier:
1. Use only 1 instance
2. Use Nano size (512 MB)
3. Monitor usage in dashboard
4. No credit card required!

## 🌟 Production Tips

### 1. Custom Domain
```
Settings → Domains → Add Custom Domain
your-domain.com → your-app.koyeb.app
```

### 2. HTTPS (Automatic)
Koyeb provides free SSL for:
- *.koyeb.app domains
- Custom domains

### 3. Monitoring
Enable in Koyeb dashboard:
- Request metrics
- Error rates
- Response times
- Memory usage

## 📚 Additional Resources

- [Koyeb Documentation](https://www.koyeb.com/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Flask Production](https://flask.palletsprojects.com/en/stable/deploying/)
- [Gunicorn Settings](https://docs.gunicorn.org/en/stable/settings.html)

## 🎉 Success!

Your AI Flow video generator is now live!

Share your URL:
```
https://your-app-name.koyeb.app
```

## 🆘 Need Help?

1. Check Koyeb logs in dashboard
2. Review this guide
3. Check Koyeb community forum
4. Open GitHub issue

---

Happy deploying! 🚀
