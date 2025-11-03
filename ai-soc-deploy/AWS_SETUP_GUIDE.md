# 🚀 AWS Integration Setup Guide

## 📋 **STEP-BY-STEP AWS SETUP**

### **Step 1: AWS Account Setup (5 minutes)**

1. **Create AWS Account** (if you don't have one)
   - Go to aws.amazon.com
   - Sign up for free tier account

2. **Create IAM User for the Application**
   - Go to AWS Console → IAM → Users
   - Click "Create User"
   - Username: `ai-soc-platform`
   - Access type: ✅ Programmatic access
   - Attach policies:
     - `AmazonBedrockFullAccess`
     - `AmazonRDSFullAccess` 
     - `AmazonDocDBFullAccess`
     - `ElastiCacheFullAccess`
     - `AmazonSQSFullAccess`
     - `AmazonSSMFullAccess`

3. **Save Credentials**
   - Copy `Access Key ID`
   - Copy `Secret Access Key`

### **Step 2: Enable AWS Bedrock (2 minutes)**

1. **Go to AWS Bedrock Console**
   - Region: `us-east-1` (recommended)
   - Navigate to "Model access"

2. **Request Model Access**
   - Find "Anthropic Claude 3.5 Sonnet"
   - Click "Request model access"
   - Fill out use case: "AI Security Operations Platform"
   - Submit request (usually approved instantly)

### **Step 3: Set Environment Variables in Render.com (3 minutes)**

In your Render.com dashboard, add these environment variables:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1

# Enable Real AWS Mode
USE_REAL_AWS=true

# Optional: Database URLs (if you want to set up databases)
POSTGRES_HOST=your-rds-endpoint.amazonaws.com
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=ai_soc_db

DOCDB_HOST=your-docdb-cluster.amazonaws.com
DOCDB_USER=your_docdb_user
DOCDB_PASSWORD=your_docdb_password
DOCDB_DATABASE=security_investigations

REDIS_HOST=your-elasticache-cluster.amazonaws.com
```

### **Step 4: Deploy Updated Code (2 minutes)**

```bash
cd c:\Users\Sulochana Meena\Documents\acc
git add .
git commit -m "AWS Integration - Real AWS Services"
git push origin main
```

### **Step 5: Test AWS Integration (1 minute)**

1. **Check Health Status**
   - Go to your app: `https://your-app.onrender.com/health/`
   - Look for `"mode": "real_aws"`

2. **Test AI Processing**
   - Click "Process Alert" button
   - Should now use real AWS Bedrock Claude!

## 🎯 **INTEGRATION MODES**

### **Automatic Mode Detection:**
- ✅ **Real AWS Mode**: When credentials are provided
- ✅ **Mock Mode**: When no credentials (safe fallback)
- ✅ **Hybrid Mode**: Real Bedrock + Mock databases (cost-effective)

### **Current Status Check:**
Visit `/health/` endpoint to see:
```json
{
  "mode": "real_aws",
  "aws_integration": {
    "bedrock": "real",
    "rds": "mock", 
    "sqs": "real"
  }
}
```

## 💰 **COST ESTIMATION**

### **AWS Bedrock Costs:**
- **Claude 3.5 Sonnet**: ~$0.003 per 1K input tokens
- **Typical security alert analysis**: ~$0.01-0.02 per alert
- **Demo usage**: <$1/month

### **Optional Database Costs:**
- **RDS (t3.micro)**: ~$13/month
- **DocumentDB (t3.medium)**: ~$50/month  
- **ElastiCache (t3.micro)**: ~$12/month

## 🔧 **QUICK START OPTIONS**

### **Option 1: Bedrock Only (Recommended)**
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
USE_REAL_AWS=true
```
**Result**: Real AI analysis + Mock databases (cost-effective!)

### **Option 2: Full AWS Integration**
Add all database environment variables above
**Result**: Complete production setup

### **Option 3: Stay in Mock Mode**
Don't add any AWS credentials
**Result**: Continues working as demo (no costs)

## ✅ **VERIFICATION CHECKLIST**

- [ ] AWS IAM user created with proper permissions
- [ ] Bedrock Claude 3.5 Sonnet access approved
- [ ] Environment variables set in Render.com
- [ ] Code deployed successfully
- [ ] Health check shows "real_aws" mode
- [ ] "Process Alert" uses real AI analysis

**🎉 Your AI Security Operations Platform is now powered by real AWS services!**