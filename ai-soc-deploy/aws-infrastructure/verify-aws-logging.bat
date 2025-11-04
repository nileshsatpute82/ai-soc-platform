@echo off
echo ========================================
echo AWS Security Logging Verification
echo ========================================
echo.

echo 1. Checking CloudTrail Status...
aws cloudtrail get-trail-status --name ai-soc-security-trail
echo.

echo 2. Checking GuardDuty Status...
aws guardduty list-detectors
echo.

echo 3. Checking Security Hub Status...
aws securityhub describe-hub
echo.

echo 4. Checking VPC Flow Logs...
aws ec2 describe-flow-logs --filter "Name=resource-type,Values=VPC"
echo.

echo 5. Checking S3 Buckets for Logs...
aws s3 ls | findstr ai-soc
echo.

echo 6. Checking EventBridge Rules...
aws events list-rules --name-prefix ai-soc
echo.

echo 7. Checking SQS Queues...
aws sqs list-queues | findstr ai-soc
echo.

echo ========================================
echo Verification Complete!
echo ========================================
pause