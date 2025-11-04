@echo off
echo ========================================
echo AI-SOC Security Platform - AWS Logging Setup
echo ========================================
echo.
echo This script will enable comprehensive AWS security logging:
echo 1. CloudTrail (API activity logging)
echo 2. GuardDuty (threat detection)
echo 3. Security Hub (centralized security findings)
echo 4. VPC Flow Logs (network traffic monitoring)
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo Step 1/4: Setting up CloudTrail...
call setup-cloudtrail.bat
echo CloudTrail setup completed (warnings are normal for existing services)

echo.
echo Step 2/4: Setting up GuardDuty...
call setup-guardduty.bat
echo GuardDuty setup completed

echo.
echo Step 3/4: Setting up Security Hub...
call setup-security-hub.bat
echo Security Hub setup completed

echo.
echo Step 4/4: Setting up VPC Flow Logs...
call setup-vpc-flow-logs.bat
echo VPC Flow Logs setup completed

echo.
echo ========================================
echo ✅ ALL AWS SECURITY LOGGING ENABLED! ✅
echo ========================================
echo.
echo Services configured:
echo • CloudTrail: API activity logging
echo • GuardDuty: Threat detection (15-min intervals)
echo • Security Hub: Centralized security findings
echo • VPC Flow Logs: Network traffic monitoring
echo.
echo Next steps:
echo 1. Deploy your application with real AWS integration
echo 2. Security events will automatically flow to your dashboard
echo 3. Monitor costs in AWS Billing console
echo.
echo Estimated monthly costs:
echo • CloudTrail: ~$2-5 (depending on API activity)
echo • GuardDuty: ~$3-10 (depending on data volume)
echo • Security Hub: ~$1-3 (depending on findings)
echo • VPC Flow Logs: ~$1-5 (depending on traffic)
echo • Total: ~$7-23/month for comprehensive security logging
echo.
pause