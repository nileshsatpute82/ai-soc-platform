@echo off
echo Setting up VPC Flow Logs for AI-SOC Security Platform...

REM Get default VPC ID
echo Getting default VPC ID...
for /f "tokens=*" %%i in ('aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query Vpcs[0].VpcId --output text') do set VPC_ID=%%i

if "%VPC_ID%"=="" (
    echo WARNING: Could not find default VPC. Skipping VPC Flow Logs.
    pause
    exit /b 0
)

echo Default VPC ID: %VPC_ID%

REM Get AWS Account ID
for /f "tokens=*" %%i in ('aws sts get-caller-identity --query Account --output text') do set ACCOUNT_ID=%%i

REM Create S3 bucket for VPC Flow Logs
set FLOW_LOGS_BUCKET=ai-soc-vpc-flow-logs-%ACCOUNT_ID%
echo Creating S3 bucket for VPC Flow Logs: %FLOW_LOGS_BUCKET%
aws s3 mb s3://%FLOW_LOGS_BUCKET% --region us-east-1

REM Create VPC Flow Logs
echo Creating VPC Flow Logs...
aws ec2 create-flow-logs --resource-type VPC --resource-ids %VPC_ID% --traffic-type ALL --log-destination-type s3 --log-destination s3://%FLOW_LOGS_BUCKET%/vpc-flow-logs/
if %errorlevel% neq 0 (
    echo WARNING: VPC Flow Logs creation failed. May already exist or insufficient permissions.
)

echo.
echo ✅ VPC Flow Logs setup complete!
echo VPC ID: %VPC_ID%
echo S3 Bucket: %FLOW_LOGS_BUCKET%
echo Traffic Type: ALL
echo.
pause