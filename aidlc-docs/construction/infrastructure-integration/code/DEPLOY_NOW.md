# 🚀 DEPLOY TO RENDER.COM NOW - 5 MINUTES

## Step 1: Copy Code (30 seconds)

Copy all files from this directory to a new folder on your computer:
```
aidlc-docs/construction/infrastructure-integration/code/
```

## Step 2: GitHub Setup (2 minutes)

```bash
# In the code directory
git init
git add .
git commit -m "AI SOC Platform - Demo Ready"
git branch -M main

# Create GitHub repo at github.com/new
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/ai-soc-demo.git
git push -u origin main
```

## Step 3: Render.com Deploy (2 minutes)

1. Go to **render.com** → Sign up/Login
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repo: `ai-soc-demo`
4. Settings:
   - **Name**: `ai-soc-demo`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python demo_app.py`

## Step 4: Environment Variables (30 seconds)

In Render dashboard, add ONE environment variable:
```
SECRET_KEY = demo-secret-key-12345
```

## Step 5: Test Your Deployment (30 seconds)

Your app will be live at: `https://ai-soc-demo.onrender.com`

**Test these URLs:**
- `https://ai-soc-demo.onrender.com/` - Home page
- `https://ai-soc-demo.onrender.com/health/` - Health check
- `https://ai-soc-demo.onrender.com/demo/` - Demo operations

## What You'll See

✅ **Working AI Security Platform**
- Health monitoring dashboard
- Configuration management
- Audit logging system
- MITRE ATT&CK integration
- Mock AI security analysis

✅ **API Endpoints**
- `/health/` - System status
- `/api/config/` - Configuration
- `/api/audit/events` - Security events
- `/api/mitre/techniques` - MITRE data
- `/demo/` - Live security operations demo

## Next Steps After Deployment

1. **Verify deployment** - Check all endpoints work
2. **Add real AWS services** - Replace mock mode
3. **Build additional units** - Core Platform, AI Crews, Frontend
4. **Scale infrastructure** - Add production AWS services

**🎉 You now have a working AI Security Operations Platform deployed on Render.com!**