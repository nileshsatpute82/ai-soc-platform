@echo off
echo Fixing remaining AWS security services...

echo 1. Enabling Security Hub...
aws securityhub enable-security-hub --enable-default-standards
if %errorlevel% neq 0 (
    echo WARNING: Security Hub may already be enabled or needs manual setup
)

echo.
echo 2. Getting VPC ID for Flow Logs...
for /f "tokens=*" %%i in ('aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text') do set VPC_ID=%%i

if not "%VPC_ID%"=="" (
    echo Found VPC: %VPC_ID%
    echo 3. Creating S3 bucket for VPC Flow Logs...
    aws s3 mb s3://ai-soc-vpc-flow-logs-058264157287 --region us-east-1
    echo 4. Creating VPC Flow Logs...
    aws ec2 create-flow-logs --resource-type VPC --resource-ids %VPC_ID% --traffic-type ALL --log-destination-type s3 --log-destination arn:aws:s3:::ai-soc-vpc-flow-logs-058264157287
    if %errorlevel% neq 0 (
        echo WARNING: VPC Flow Logs may already exist
    )
) else (
    echo WARNING: Could not find default VPC
)

echo.
echo ✅ Setup complete! Run verify-aws-logging.bat to check status.
pause