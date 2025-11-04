# 🚀 Enable Complete AWS Security Logging

## Quick Setup (5 minutes)

Run this single command to enable all AWS security logging:

```bash
cd ai-soc-deploy\aws-infrastructure
setup-all-logging.bat
```

## Manual Setup (if needed)

### Step 1: CloudTrail (API Activity Logging)
```bash
setup-cloudtrail.bat
```

### Step 2: GuardDuty (Threat Detection)
```bash
setup-guardduty.bat
```

### Step 3: Security Hub (Centralized Findings)
```bash
setup-security-hub.bat
```

### Step 4: VPC Flow Logs (Network Monitoring)
```bash
setup-vpc-flow-logs.bat
```

## What Gets Enabled

### 🔍 CloudTrail
- **Purpose**: Logs all AWS API calls
- **Events**: IAM actions, resource changes, console logins
- **Storage**: S3 bucket (ai-soc-cloudtrail-logs-{account-id})
- **Cost**: ~$2-5/month

### 🛡️ GuardDuty
- **Purpose**: AI-powered threat detection
- **Events**: Malicious IPs, compromised instances, crypto mining
- **Frequency**: Every 15 minutes
- **Cost**: ~$3-10/month

### 🎯 Security Hub
- **Purpose**: Centralized security findings
- **Events**: Compliance checks, security standards
- **Standards**: AWS Foundational Security Standard
- **Cost**: ~$1-3/month

### 🌐 VPC Flow Logs
- **Purpose**: Network traffic monitoring
- **Events**: All network connections in/out of VPC
- **Storage**: S3 bucket (ai-soc-vpc-flow-logs-{account-id})
- **Cost**: ~$1-5/month

## Integration with Your Dashboard

All these events will automatically flow to your AI-SOC dashboard:

1. **EventBridge Rules**: Route findings to SQS queue
2. **SQS Processing**: Your app polls for new alerts
3. **AI Analysis**: Claude analyzes each security event
4. **MITRE Mapping**: Techniques mapped to ATT&CK framework
5. **Dashboard Display**: Real-time security operations view

## Verification

After setup, check your dashboard:
- Visit: `https://your-app.onrender.com/`
- Look for real AWS alerts (marked with 🔴)
- MITRE techniques should show detection counts
- System health should show "real_aws" mode

## Cost Summary

**Total estimated monthly cost: $7-23**
- CloudTrail: $2-5
- GuardDuty: $3-10  
- Security Hub: $1-3
- VPC Flow Logs: $1-5

## Troubleshooting

### Permission Issues
Ensure your IAM user has these policies:
- `CloudTrailFullAccess`
- `AmazonGuardDutyFullAccess`
- `AWSSecurityHubFullAccess`
- `AmazonVPCFullAccess`

### Service Already Enabled
If services are already enabled, the scripts will show warnings but continue.

### No Events Appearing
1. Wait 5-10 minutes for initial setup
2. Generate test activity (create/delete IAM users)
3. Check SQS queue in AWS console
4. Verify EventBridge rules are active

## Next Steps

1. **Run the setup**: `setup-all-logging.bat`
2. **Deploy your app**: Push to GitHub (auto-deploys to Render)
3. **Generate test events**: Create IAM users, modify security groups
4. **Monitor dashboard**: Watch real AWS security events flow in
5. **Populate MITRE data**: Visit `/api/demo/populate-mitre` (POST request)

Your AI-powered security operations center will now monitor your entire AWS environment! 🛡️