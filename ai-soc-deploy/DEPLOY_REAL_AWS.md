# 🚀 Deploy Full Real AWS Infrastructure

## 📋 **STEP 1: Deploy AWS Infrastructure**

Run this single command to deploy everything:

```bash
cd ai-soc-deploy/aws-infrastructure

# Deploy complete stack
aws cloudformation create-stack \
  --stack-name ai-soc-platform-complete \
  --template-body file://real-aws-stack.yaml \
  --parameters ParameterKey=DBPassword,ParameterValue=AiSocSecure123! \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

## ⏳ **STEP 2: Wait for Deployment (10-15 minutes)**

```bash
# Monitor deployment
aws cloudformation wait stack-create-complete \
  --stack-name ai-soc-platform-complete \
  --region us-east-1

echo "✅ Infrastructure deployed!"
```

## 📋 **STEP 3: Get Connection Details**

```bash
# Get all endpoints
aws cloudformation describe-stacks \
  --stack-name ai-soc-platform-complete \
  --query 'Stacks[0].Outputs' \
  --region us-east-1
```

## 🔧 **STEP 4: Add Environment Variables to Render.com**

Copy these exact values to your Render.com dashboard:

```bash
# AWS Credentials (your existing ones)
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1

# Enable Real AWS Mode
USE_REAL_AWS=true
ENABLE_REAL_DATABASES=true

# Database Connections (get from CloudFormation outputs)
POSTGRES_HOST=ai-soc-platform-postgres.xxxxx.us-east-1.rds.amazonaws.com
POSTGRES_PORT=5432
POSTGRES_USER=aisoc_admin
POSTGRES_PASSWORD=AiSocSecure123!
POSTGRES_DB=ai_soc_db

DOCDB_HOST=ai-soc-platform-docdb-cluster.cluster-xxxxx.us-east-1.docdb.amazonaws.com
DOCDB_PORT=27017
DOCDB_USER=aisoc_admin
DOCDB_PASSWORD=AiSocSecure123!
DOCDB_DATABASE=security_investigations

REDIS_HOST=ai-soc-platform-redis.xxxxx.cache.amazonaws.com
REDIS_PORT=6379

# SQS Queue (get from CloudFormation outputs)
AWS_SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/your-account/ai-soc-platform-security-alerts
```

## 🚀 **STEP 5: Deploy Application**

```bash
cd c:\Users\Sulochana Meena\Documents\acc
git add .
git commit -m "Full real AWS infrastructure - no mock components"
git push origin main
```

## ✅ **STEP 6: Verify Everything Works**

Visit your app health endpoint - should show:

```json
{
  "mode": "real_aws",
  "services": {
    "bedrock": "real",
    "rds": "real", 
    "documentdb": "real",
    "elasticache": "real",
    "sqs": "real"
  }
}
```

## 💰 **Monthly Cost: ~$76-81**

- RDS PostgreSQL: ~$13/month
- DocumentDB: ~$50/month  
- ElastiCache Redis: ~$12/month
- Bedrock: ~$1-5/month
- SQS: ~$0.40/month

## 🗑️ **Cleanup (when done)**

```bash
aws cloudformation delete-stack \
  --stack-name ai-soc-platform-complete \
  --region us-east-1
```

**🎉 You now have a fully production-ready AI Security Operations Platform with zero mock components!**