# 🚀 FULL AWS SETUP - No Mock Components

## 📋 **REQUIRED ENVIRONMENT VARIABLES**

Add these to your Render.com dashboard:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1

# Enable Real AWS Mode
USE_REAL_AWS=true
ENABLE_REAL_DATABASES=true

# RDS PostgreSQL (Required)
POSTGRES_HOST=ai-soc-platform-db.cm7kca0c0wr4.us-east-1.rds.amazonaws.com
POSTGRES_PORT=5432
POSTGRES_USER=aisocadmin
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=ai_soc_db

# DocumentDB (Required)
DOCDB_HOST=ai-soc-platform-docdb.cluster-cm7kca0c0wr4.us-east-1.docdb.amazonaws.com
DOCDB_PORT=27017
DOCDB_USER=aisocadmin
DOCDB_PASSWORD=your_secure_password_here
DOCDB_DATABASE=security_investigations

# ElastiCache Redis (Required)
REDIS_HOST=ai-soc-platform-redis.cm7kca.cache.amazonaws.com
REDIS_PORT=6379

# SQS Queue (Already configured)
AWS_SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/058264157287/ai-soc-platform-security-alerts
```

## 🏗️ **DEPLOY AWS INFRASTRUCTURE**

Run these CloudFormation commands to create real AWS resources:

```bash
# Deploy RDS PostgreSQL
aws cloudformation create-stack \
  --stack-name ai-soc-rds \
  --template-body file://aws-infrastructure/rds-stack.yaml \
  --parameters ParameterKey=DBPassword,ParameterValue=YourSecurePassword123!

# Deploy DocumentDB
aws cloudformation create-stack \
  --stack-name ai-soc-docdb \
  --template-body file://aws-infrastructure/documentdb-stack.yaml \
  --parameters ParameterKey=MasterUserPassword,ParameterValue=YourSecurePassword123!

# Deploy ElastiCache Redis
aws cloudformation create-stack \
  --stack-name ai-soc-redis \
  --template-body file://aws-infrastructure/elasticache-stack.yaml
```

## ⚡ **QUICK DEPLOY SCRIPT**

```bash
cd aws-infrastructure
./deploy-full-infrastructure.sh
```

## 💰 **MONTHLY COSTS**

- **RDS (db.t3.micro)**: ~$13/month
- **DocumentDB (db.t3.medium)**: ~$50/month  
- **ElastiCache (cache.t3.micro)**: ~$12/month
- **Bedrock Claude**: ~$1-5/month (usage-based)
- **SQS**: ~$0.40/month
- **Total**: ~$76-81/month

## 🔧 **VERIFICATION STEPS**

1. **Deploy infrastructure** using CloudFormation
2. **Get endpoint URLs** from AWS Console
3. **Add environment variables** to Render.com
4. **Deploy application** 
5. **Check health endpoint** - should show all "real" services

## ✅ **SUCCESS INDICATORS**

Health check should show:
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