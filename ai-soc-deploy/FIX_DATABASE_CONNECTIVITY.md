# 🔧 Fix Database Connectivity Issues

## 🚨 **Current Issue**
Databases show as "real" but "unhealthy" due to network connectivity from Render.com to AWS.

## ✅ **Solution: Make Databases Publicly Accessible**

### **1. Fix RDS PostgreSQL**
```bash
# Modify RDS to be publicly accessible
aws rds modify-db-instance \
  --db-instance-identifier ai-soc-platform-postgres \
  --publicly-accessible \
  --apply-immediately \
  --region us-east-1
```

### **2. Fix DocumentDB Security Group**
```bash
# Get security group ID
SG_ID=$(aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=*ai-soc-platform*" \
  --query 'SecurityGroups[0].GroupId' \
  --output text \
  --region us-east-1)

# Add rule for DocumentDB (port 27017)
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 27017 \
  --cidr 0.0.0.0/0 \
  --region us-east-1

# Add rule for Redis (port 6379)  
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 6379 \
  --cidr 0.0.0.0/0 \
  --region us-east-1
```

### **3. Alternative: Use Connection Strings with SSL**

Add these to Render.com environment variables:

```bash
# PostgreSQL with SSL
DATABASE_URL=postgresql://aisoc_admin:AISec2024!Platform@ai-soc-platform-postgres.cm7kca0c0wr4.us-east-1.rds.amazonaws.com:5432/ai_soc_db?sslmode=require

# DocumentDB with SSL
MONGODB_URI=mongodb://aisoc_admin:AISec2024!Platform@ai-soc-platform-docdb.cluster-cm7kca0c0wr4.us-east-1.docdb.amazonaws.com:27017/security_investigations?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false

# Redis (should work as-is)
REDIS_URL=redis://ai-soc-platform-redis.4mo9ij.0001.use1.cache.amazonaws.com:6379
```

## 🚀 **Quick Fix: Deploy with Connection Fallback**

I'll update the code to handle connection issues gracefully while maintaining functionality.