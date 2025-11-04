# ⚠️ REAL AWS Security Incident Generation Commands

## 🚨 **WARNING: THESE COMMANDS CREATE REAL AWS INCIDENTS**

**These commands will:**
- ✅ Generate actual AWS security events
- ✅ Trigger real GuardDuty findings
- ✅ Create CloudTrail logs
- ✅ Generate real AWS costs
- ✅ Send alerts to your AI SOC platform

**⚠️ IMPORTANT: Only run in test/development AWS accounts!**

---

## 📋 **Prerequisites**

1. **AWS CLI installed and configured**
2. **IAM permissions for testing**
3. **GuardDuty enabled in your region**
4. **CloudTrail enabled**
5. **Test AWS account (not production)**

---

## 🔥 **Critical Severity - Real AWS Incidents**

### **1. Suspicious IAM Activity**
```bash
# Create suspicious IAM user
aws iam create-user --user-name suspicious-test-user-$(date +%s)

# Attach admin policy (triggers GuardDuty)
aws iam attach-user-policy --user-name suspicious-test-user-$(date +%s) --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Create access keys
aws iam create-access-key --user-name suspicious-test-user-$(date +%s)
```

### **2. Cryptocurrency Mining Detection**
```bash
# Launch EC2 instance with suspicious name (triggers GuardDuty)
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t2.micro \
  --key-name your-key-pair \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=bitcoin-miner-test}]'
```

### **3. Malicious IP Communication**
```bash
# Create security group allowing suspicious traffic
aws ec2 create-security-group \
  --group-name malicious-test-sg \
  --description "Test security group for malicious traffic"

# Add rule for known malicious IP ranges (triggers GuardDuty)
aws ec2 authorize-security-group-ingress \
  --group-name malicious-test-sg \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

---

## ⚠️ **High Severity - Real AWS Incidents**

### **4. Unusual API Calls**
```bash
# Make unusual API calls from different regions
aws s3 ls --region us-west-1
aws s3 ls --region eu-west-1
aws s3 ls --region ap-southeast-1

# Rapid successive calls (triggers rate limiting alerts)
for i in {1..50}; do aws sts get-caller-identity; done
```

### **5. S3 Bucket Policy Changes**
```bash
# Create test bucket
aws s3 mb s3://security-test-bucket-$(date +%s)

# Apply overly permissive policy (triggers security alerts)
aws s3api put-bucket-policy --bucket security-test-bucket-$(date +%s) --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::security-test-bucket-*/*"
  }]
}'
```

### **6. Root Account Usage**
```bash
# Note: Only run if you have root access and this is a test account
# Root account API calls trigger high-priority alerts
aws sts get-caller-identity
aws iam list-users
```

---

## 🟡 **Medium Severity - Real AWS Incidents**

### **7. Failed Authentication Attempts**
```bash
# Attempt to access with invalid credentials (modify AWS config temporarily)
export AWS_ACCESS_KEY_ID="INVALID_KEY_ID"
export AWS_SECRET_ACCESS_KEY="INVALID_SECRET"

# These will fail and create CloudTrail events
aws s3 ls 2>/dev/null || echo "Failed authentication logged"
aws ec2 describe-instances 2>/dev/null || echo "Failed authentication logged"

# Restore real credentials
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
```

### **8. Unusual Resource Creation**
```bash
# Create resources in unusual patterns
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=test-suspicious-vpc}]'

# Create multiple security groups rapidly
for i in {1..10}; do
  aws ec2 create-security-group --group-name test-sg-$i --description "Test security group $i"
done
```

### **9. Cross-Region Activity**
```bash
# Rapid cross-region API calls (unusual pattern)
aws ec2 describe-instances --region us-east-1
aws ec2 describe-instances --region us-west-2
aws ec2 describe-instances --region eu-west-1
aws ec2 describe-instances --region ap-southeast-1
```

---

## 🌐 **Network-Based Real Incidents**

### **10. VPC Flow Log Anomalies**
```bash
# Create VPC with flow logs enabled
VPC_ID=$(aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)

# Enable VPC Flow Logs
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids $VPC_ID \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name VPCFlowLogs
```

### **11. DNS Tunneling Simulation**
```bash
# Create Route53 hosted zone for testing
aws route53 create-hosted-zone \
  --name suspicious-domain-test.com \
  --caller-reference $(date +%s)

# Create suspicious DNS records
aws route53 change-resource-record-sets \
  --hosted-zone-id YOUR_ZONE_ID \
  --change-batch file://suspicious-dns-records.json
```

---

## 🔍 **Data Access Incidents**

### **12. Bulk Data Access**
```bash
# List all S3 buckets (data discovery)
aws s3 ls

# Attempt to access multiple buckets
aws s3 ls s3://bucket1 2>/dev/null || echo "Access attempt logged"
aws s3 ls s3://bucket2 2>/dev/null || echo "Access attempt logged"
aws s3 ls s3://bucket3 2>/dev/null || echo "Access attempt logged"
```

### **13. Database Access Attempts**
```bash
# List RDS instances (reconnaissance)
aws rds describe-db-instances

# List DynamoDB tables
aws dynamodb list-tables

# Attempt to access database snapshots
aws rds describe-db-snapshots
```

---

## 🤖 **Automated Incident Generation Script**

### **Create Multiple Real Incidents**
```bash
#!/bin/bash
# real-incident-generator.sh

echo "🚨 Generating REAL AWS security incidents..."

# 1. Suspicious IAM activity
aws iam create-user --user-name test-suspicious-$(date +%s)

# 2. Unusual API patterns
for region in us-east-1 us-west-2 eu-west-1; do
  aws ec2 describe-instances --region $region
done

# 3. Resource enumeration
aws s3 ls
aws iam list-users
aws ec2 describe-security-groups

# 4. Failed access attempts
export AWS_ACCESS_KEY_ID="FAKE_KEY"
aws s3 ls 2>/dev/null || echo "Failed access logged"
unset AWS_ACCESS_KEY_ID

echo "✅ Real incidents generated - check GuardDuty in 5-15 minutes"
```

---

## 📊 **Monitor Real Incidents**

### **Check GuardDuty Findings**
```bash
# List active GuardDuty findings
aws guardduty list-findings --detector-id YOUR_DETECTOR_ID

# Get finding details
aws guardduty get-findings --detector-id YOUR_DETECTOR_ID --finding-ids FINDING_ID
```

### **Check CloudTrail Events**
```bash
# Look for recent security events
aws logs filter-log-events \
  --log-group-name CloudTrail/SecurityEvents \
  --start-time $(date -d '1 hour ago' +%s)000
```

### **Check Your AI SOC Platform**
```bash
# Your platform should automatically detect these via SQS/EventBridge
curl https://your-app.onrender.com/api/alerts/
```

---

## 💰 **Cost Estimation**

**Running all commands:**
- **GuardDuty**: ~$0.50-2.00 per day
- **CloudTrail**: ~$0.10-0.50 per day  
- **EC2 instances**: ~$0.01 per hour (t2.micro)
- **S3 operations**: ~$0.01-0.05
- **Total daily cost**: ~$1-5 for testing

---

## 🧹 **Cleanup Commands**

### **Remove Test Resources**
```bash
#!/bin/bash
# cleanup-test-incidents.sh

# Delete test users
aws iam list-users --query 'Users[?contains(UserName, `test-suspicious`)].UserName' --output text | \
xargs -I {} aws iam delete-user --user-name {}

# Delete test security groups
aws ec2 describe-security-groups --query 'SecurityGroups[?contains(GroupName, `test-`)].GroupId' --output text | \
xargs -I {} aws ec2 delete-security-group --group-id {}

# Terminate test instances
aws ec2 describe-instances --query 'Reservations[].Instances[?contains(Tags[?Key==`Name`].Value, `test`)].InstanceId' --output text | \
xargs -I {} aws ec2 terminate-instances --instance-ids {}

echo "✅ Test resources cleaned up"
```

---

## ⚠️ **SAFETY WARNINGS**

1. **Test Account Only**: Never run in production
2. **Monitor Costs**: Set up billing alerts
3. **Clean Up**: Always remove test resources
4. **GuardDuty Findings**: Will show as real threats
5. **Compliance**: May trigger compliance alerts

## 🎯 **Expected Results**

After running these commands:
- **GuardDuty findings** appear in 5-15 minutes
- **CloudTrail events** logged immediately  
- **Your AI SOC platform** receives real alerts via SQS
- **Real AWS security incidents** for testing

**🚨 These create REAL AWS security events - use responsibly!**