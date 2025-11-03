# 🧪 Dashboard Testing Commands

## AWS IAM User Management Commands

### Create Test IAM User
```bash
# Create IAM user for testing
aws iam create-user --user-name ai-soc-test-user

# Create access key
aws iam create-access-key --user-name ai-soc-test-user

# Attach required policies
aws iam attach-user-policy --user-name ai-soc-test-user --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
aws iam attach-user-policy --user-name ai-soc-test-user --policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess
aws iam attach-user-policy --user-name ai-soc-test-user --policy-arn arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess
```

### Delete Test IAM User
```bash
# List and delete access keys first
aws iam list-access-keys --user-name ai-soc-test-user
aws iam delete-access-key --user-name ai-soc-test-user --access-key-id YOUR_ACCESS_KEY_ID

# Detach policies
aws iam detach-user-policy --user-name ai-soc-test-user --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
aws iam detach-user-policy --user-name ai-soc-test-user --policy-arn arn:aws:iam::aws:policy/AmazonSQSFullAccess
aws iam detach-user-policy --user-name ai-soc-test-user --policy-arn arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess

# Delete user
aws iam delete-user --user-name ai-soc-test-user
```

## Quick Dashboard Test URLs

### Health Check
```bash
curl https://your-app.onrender.com/health/
```

### Process Test Alert
```bash
curl -X POST https://your-app.onrender.com/api/process-alert \
  -H "Content-Type: application/json" \
  -d '{"alert_type": "test", "severity": "high"}'
```

### Get Recent Alerts
```bash
curl https://your-app.onrender.com/api/alerts/recent
```

## Local Testing (if running locally)

### Start Local Server
```bash
cd ai-soc-deploy
python demo_app.py
```

### Test Endpoints
```bash
# Health check
curl http://localhost:5000/health/

# Dashboard
open http://localhost:5000/

# Process alert
curl -X POST http://localhost:5000/api/process-alert \
  -H "Content-Type: application/json" \
  -d '{"alert_type": "GuardDuty", "severity": "HIGH"}'
```

## Environment Variable Testing

### Test with Mock Mode
```bash
# Remove AWS credentials to test mock mode
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset USE_REAL_AWS
```

### Test with Real AWS
```bash
export AWS_ACCESS_KEY_ID=your_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_here
export USE_REAL_AWS=true
export AWS_REGION=us-east-1
```

## One-Line Test Commands

### Complete IAM User Creation
```bash
aws iam create-user --user-name ai-soc-test && aws iam create-access-key --user-name ai-soc-test && aws iam attach-user-policy --user-name ai-soc-test --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

### Complete IAM User Deletion
```bash
aws iam detach-user-policy --user-name ai-soc-test --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess && aws iam delete-access-key --user-name ai-soc-test --access-key-id $(aws iam list-access-keys --user-name ai-soc-test --query 'AccessKeyMetadata[0].AccessKeyId' --output text) && aws iam delete-user --user-name ai-soc-test
```