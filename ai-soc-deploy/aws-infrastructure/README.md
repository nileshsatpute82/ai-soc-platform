# 🚀 AWS Infrastructure for AI Security Operations Platform

## 📋 Quick Setup Guide

### 1. Deploy AWS Infrastructure (5 minutes)

```bash
# Navigate to infrastructure directory
cd aws-infrastructure

# Deploy CloudFormation stack
aws cloudformation deploy \
  --template-file cloudformation-stack.yaml \
  --stack-name ai-soc-platform-infrastructure \
  --region us-east-1 \
  --capabilities CAPABILITY_NAMED_IAM

# Get SQS Queue URL for environment variables
aws cloudformation describe-stacks \
  --stack-name ai-soc-platform-infrastructure \
  --query 'Stacks[0].Outputs[?OutputKey==`SecurityAlertsQueueUrl`].OutputValue' \
  --output text
```

### 2. Update Render.com Environment Variables

Add this to your Render.com environment variables:
```
AWS_SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/YOUR_ACCOUNT/ai-soc-platform-security-alerts
```

### 3. Generate Test Security Alerts

```bash
# Install dependencies
pip install boto3

# Generate test alerts
python generate-test-alerts.py
```

## 🎯 What Gets Created

### AWS Resources:
- **SQS Queue**: `ai-soc-platform-security-alerts` - Receives security alerts
- **SNS Topic**: `ai-soc-platform-security-alerts` - Distributes security events
- **EventBridge Rules**: Detect security events:
  - Failed login attempts
  - Root account usage
  - IAM changes (user/role creation/deletion)

### Security Event Detection:
- **Failed Logins**: Detects failed AWS console login attempts
- **Root Account Usage**: Alerts when root account is used
- **IAM Changes**: Monitors user/role creation, deletion, policy changes

## 🔧 Generate Real Security Alerts

### Method 1: Failed Login Simulation
1. Go to AWS Console sign-in page
2. Enter incorrect credentials 3-5 times
3. **Result**: Failed login alerts appear in your platform

### Method 2: Root Account Usage
1. Sign in to AWS Console with root account
2. **Result**: Root usage alert appears in your platform

### Method 3: IAM Changes
1. Go to AWS Console → IAM → Users
2. Create a new test user: `test-security-user`
3. Delete the test user
4. **Result**: IAM change alerts appear in your platform

### Method 4: Programmatic Test Alerts
```bash
python generate-test-alerts.py
```

## 📊 Monitoring Your Platform

### Check Alert Processing:
```bash
# Visit your platform
https://your-app.onrender.com/health/

# Look for:
{
  "real_alerts": {
    "status": "healthy",
    "queue_configured": true
  }
}
```

### View Real Alerts:
```bash
# Your platform will show real AWS alerts mixed with demo alerts
https://your-app.onrender.com/
```

## 🛡️ Security Events Captured

| Event Type | Trigger | Severity | MITRE Mapping |
|------------|---------|----------|---------------|
| Failed Login | Wrong credentials | HIGH | T1110, T1078 |
| Root Usage | Root account access | CRITICAL | T1078 |
| User Creation | New IAM user | MEDIUM | T1136, T1098 |
| User Deletion | Delete IAM user | HIGH | T1531 |
| Policy Changes | Attach/detach policies | MEDIUM | T1098 |

## 💰 Cost Estimate

- **SQS**: ~$0.40 per million requests (free tier: 1M requests/month)
- **SNS**: ~$0.50 per million notifications (free tier: 1M notifications/month)
- **EventBridge**: ~$1.00 per million events (free tier: 100M events/month)
- **CloudTrail**: Free for management events

**Total monthly cost for demo usage**: < $1.00

## 🔍 Troubleshooting

### No Alerts Appearing?
1. Check SQS queue URL in environment variables
2. Verify EventBridge rules are enabled
3. Check CloudTrail is logging events

### Permission Issues?
Ensure your IAM user has these policies:
- `AmazonSQSFullAccess`
- `AmazonSNSFullAccess`
- `AmazonEventBridgeFullAccess`

### Test Infrastructure:
```bash
# Check if queue exists
aws sqs list-queues --queue-name-prefix ai-soc-platform

# Check EventBridge rules
aws events list-rules --name-prefix ai-soc-platform
```

## 🎉 Success Indicators

✅ CloudFormation stack deployed successfully  
✅ SQS queue URL added to Render.com  
✅ Platform health check shows `queue_configured: true`  
✅ Test alerts appear in platform within 30 seconds  
✅ Real AWS events trigger platform alerts  

**Your AI Security Operations Platform is now processing real AWS security events!**