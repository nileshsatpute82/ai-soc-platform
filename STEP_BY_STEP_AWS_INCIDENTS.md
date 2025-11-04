# 🚨 Step-by-Step Real AWS Incident Generation

## ⚠️ **Execute ONE command at a time - Wait and observe results**

---

## 🔧 **Step 1: Prerequisites Check**

### **Check AWS CLI Configuration**
```bash
aws sts get-caller-identity
```
**Expected**: Shows your AWS account ID and user

### **Check GuardDuty Status**
```bash
aws guardduty list-detectors
```
**Expected**: Shows detector ID (enable GuardDuty if empty)

---

## 🚨 **Step 2: Generate First Real Incident**

### **Command 1: Suspicious IAM User Creation**
```bash
aws iam create-user --user-name security-test-user-001
```
**What happens**: Creates IAM user, logs to CloudTrail
**Wait**: 2-3 minutes, then check CloudTrail

### **Command 2: Attach Admin Policy (HIGH RISK)**
```bash
aws iam attach-user-policy --user-name security-test-user-001 --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```
**What happens**: Triggers GuardDuty "Privilege Escalation" alert
**Wait**: 5-15 minutes for GuardDuty detection

---

## 🔍 **Step 3: Check for Alerts**

### **Command 3: Check GuardDuty Findings**
```bash
aws guardduty list-findings --detector-id $(aws guardduty list-detectors --query 'DetectorIds[0]' --output text)
```
**Expected**: Should show finding IDs if incidents detected

### **Command 4: Check Your AI SOC Platform**
```bash
curl https://your-app.onrender.com/api/alerts/
```
**Expected**: Should show new security alerts

---

## 🌐 **Step 4: Network-Based Incident**

### **Command 5: Create Suspicious Security Group**
```bash
aws ec2 create-security-group --group-name test-open-sg --description "Test security group with open access"
```
**What happens**: Creates security group

### **Command 6: Add Dangerous Rule**
```bash
aws ec2 authorize-security-group-ingress --group-name test-open-sg --protocol tcp --port 22 --cidr 0.0.0.0/0
```
**What happens**: Opens SSH to entire internet (triggers security alerts)
**Wait**: 5-10 minutes

---

## 📊 **Step 5: Data Access Incident**

### **Command 7: Enumerate S3 Buckets**
```bash
aws s3 ls
```
**What happens**: Lists all S3 buckets (reconnaissance activity)

### **Command 8: Multiple Region Access**
```bash
aws ec2 describe-instances --region us-east-1
```
**Wait 30 seconds, then:**
```bash
aws ec2 describe-instances --region us-west-2
```
**Wait 30 seconds, then:**
```bash
aws ec2 describe-instances --region eu-west-1
```
**What happens**: Unusual cross-region activity pattern

---

## 🔐 **Step 6: Authentication Incident**

### **Command 9: Failed Authentication Simulation**
```bash
# Temporarily set invalid credentials
export TEMP_KEY=$AWS_ACCESS_KEY_ID
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
```

### **Command 10: Trigger Failed Auth**
```bash
aws s3 ls 2>/dev/null || echo "Failed authentication logged to CloudTrail"
```

### **Command 11: Restore Credentials**
```bash
export AWS_ACCESS_KEY_ID=$TEMP_KEY
unset TEMP_KEY
```

---

## 📈 **Step 7: Monitor Results**

### **Command 12: Check CloudTrail Events**
```bash
aws logs describe-log-groups --log-group-name-prefix CloudTrail
```

### **Command 13: Get GuardDuty Finding Details**
```bash
# First get finding IDs
DETECTOR_ID=$(aws guardduty list-detectors --query 'DetectorIds[0]' --output text)
FINDING_IDS=$(aws guardduty list-findings --detector-id $DETECTOR_ID --query 'FindingIds[0]' --output text)

# Get finding details
aws guardduty get-findings --detector-id $DETECTOR_ID --finding-ids $FINDING_IDS
```

---

## 🧹 **Step 8: Cleanup (IMPORTANT)**

### **Command 14: Remove Test IAM User**
```bash
aws iam detach-user-policy --user-name security-test-user-001 --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
aws iam delete-user --user-name security-test-user-001
```

### **Command 15: Remove Test Security Group**
```bash
aws ec2 delete-security-group --group-name test-open-sg
```

---

## 📋 **Execution Checklist**

**Before starting:**
- [ ] AWS CLI configured
- [ ] GuardDuty enabled
- [ ] Test AWS account (not production)
- [ ] Billing alerts set up

**After each command:**
- [ ] Wait specified time
- [ ] Check for errors
- [ ] Monitor AWS console
- [ ] Check AI SOC platform

**After completion:**
- [ ] Run all cleanup commands
- [ ] Verify resources deleted
- [ ] Check GuardDuty findings
- [ ] Review costs

---

## ⏱️ **Timeline Expectations**

- **CloudTrail events**: Immediate (1-2 minutes)
- **GuardDuty findings**: 5-15 minutes
- **AI SOC alerts**: 2-5 minutes after GuardDuty
- **Cost impact**: $0.50-2.00 per day

---

## 🎯 **What You'll See**

**In AWS Console:**
- GuardDuty findings with threat details
- CloudTrail events showing API calls
- Security Hub alerts (if enabled)

**In Your AI SOC Platform:**
- Real security alerts from AWS
- AI analysis of actual threats
- MITRE ATT&CK technique mapping

**Expected GuardDuty Findings:**
- "Privilege escalation via IAM policy"
- "Unusual API call patterns"
- "Reconnaissance activity detected"

---

## 🚨 **Safety Notes**

1. **Execute ONE command at a time**
2. **Wait between commands** as specified
3. **Monitor costs** in AWS billing
4. **Clean up immediately** after testing
5. **Never run in production** accounts

**This creates REAL AWS security incidents - proceed carefully!** ⚠️