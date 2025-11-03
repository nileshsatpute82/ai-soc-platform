# Deployment Guide - Working Prototype

## Step-by-Step Deployment

### 1. GitHub Setup (2 minutes)

```bash
# In your project directory
git init
git add .
git commit -m "AI SOC Infrastructure - Working Prototype"
git branch -M main

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/ai-soc-platform.git
git push -u origin main
```

### 2. Render.com Setup (5 minutes)

1. **Sign up**: Go to render.com and create account
2. **New Web Service**: Click "New" → "Web Service"
3. **Connect GitHub**: Select your `ai-soc-platform` repository
4. **Configure**:
   - **Name**: `ai-soc-infrastructure`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main_app.py`

### 3. Environment Variables (3 minutes)

In Render dashboard, add these environment variables:

```
# Required for basic functionality
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
AWS_REGION=us-east-1

# AWS Credentials (get from AWS Console)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...

# Database URLs (set up AWS services first)
POSTGRES_HOST=your-rds.amazonaws.com
POSTGRES_PASSWORD=your-password
DOCDB_HOST=your-docdb.amazonaws.com
DOCDB_PASSWORD=your-password
REDIS_HOST=your-elasticache.amazonaws.com
```

### 4. AWS Services Quick Setup

**Option A: Manual Setup (10 minutes)**
1. **RDS**: Create PostgreSQL instance
2. **DocumentDB**: Create cluster
3. **ElastiCache**: Create Redis cluster
4. **Bedrock**: Enable Claude access

**Option B: Mock Mode (0 minutes)**
- App includes mock mode for immediate testing
- Set `MOCK_MODE=true` in environment variables

### 5. Deploy & Test (2 minutes)

```bash
# Auto-deployment triggers on git push
git push origin main

# Test endpoints (replace with your Render URL)
curl https://ai-soc-infrastructure.onrender.com/health/
curl https://ai-soc-infrastructure.onrender.com/api/config/
```

## Verification Checklist

- [ ] GitHub repository created and pushed
- [ ] Render.com service deployed successfully
- [ ] Environment variables configured
- [ ] Health check returns 200 OK
- [ ] API endpoints respond correctly

## Troubleshooting

**Build Fails**: Check requirements.txt and Python version
**Health Check Fails**: Verify environment variables
**AWS Errors**: Check credentials and service availability

## Next Phase

Once infrastructure unit is deployed:
1. Add Core Platform Service unit
2. Add AI Crew units (Triage, Investigation, etc.)
3. Add Frontend Dashboard unit
4. Connect real AWS security services