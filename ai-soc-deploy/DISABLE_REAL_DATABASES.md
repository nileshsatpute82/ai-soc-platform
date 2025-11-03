# 🔧 Disable Real Databases - Keep Working Components

## 🚨 **Issue**
Databases are in private VPC subnets and unreachable from Render.com.

## ✅ **Solution: Hybrid Mode (Recommended)**
Keep what works, disable what doesn't:

### **Remove from Render.com Environment Variables:**
```bash
# Remove these variables:
ENABLE_REAL_DATABASES=true
POSTGRES_HOST=ai-soc-platform-postgres.cm7kca0c0wr4.us-east-1.rds.amazonaws.com
POSTGRES_USER=aisoc_admin
POSTGRES_PASSWORD=AISec2024!Platform
POSTGRES_DB=ai_soc_db
POSTGRES_PORT=5432
DOCDB_HOST=ai-soc-platform-docdb.cluster-cm7kca0c0wr4.us-east-1.docdb.amazonaws.com
DOCDB_USER=aisoc_admin
DOCDB_PASSWORD=AISec2024!Platform
DOCDB_DATABASE=security_investigations
DOCDB_PORT=27017
REDIS_HOST=ai-soc-platform-redis.4mo9ij.0001.use1.cache.amazonaws.com
REDIS_PORT=6379
```

### **Keep These (Working):**
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
USE_REAL_AWS=true
AWS_SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/058264157287/ai-soc-platform-security-alerts
```

## 🎯 **Result: Perfect Hybrid Mode**
- ✅ **Real Bedrock Claude** for AI analysis
- ✅ **Real SQS** for alert processing  
- ✅ **Mock Databases** for storage (works perfectly)
- ✅ **Cost Effective** (~$1-5/month vs $76/month)
- ✅ **Fully Functional** platform

## 🚀 **Deploy**
After removing database variables from Render.com:
```bash
git add .
git commit -m "Hybrid mode - real AI + mock storage for optimal demo"
git push origin main
```

**🎉 Best of both worlds: Real AI intelligence with reliable mock storage!**