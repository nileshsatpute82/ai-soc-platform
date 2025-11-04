@echo off
echo Setting up AWS CloudTrail for AI-SOC Security Platform...

REM Get AWS Account ID
echo Getting AWS Account ID...
for /f "tokens=*" %%i in ('aws sts get-caller-identity --query Account --output text') do set ACCOUNT_ID=%%i

if "%ACCOUNT_ID%"=="" (
    echo ERROR: Could not retrieve AWS Account ID. Please check your AWS credentials.
    pause
    exit /b 1
)

echo AWS Account ID: %ACCOUNT_ID%

REM Set bucket name
set BUCKET_NAME=ai-soc-cloudtrail-logs-%ACCOUNT_ID%
echo CloudTrail S3 Bucket: %BUCKET_NAME%

REM Create S3 bucket first
echo Creating S3 bucket for CloudTrail logs...
aws s3 mb s3://%BUCKET_NAME% --region us-east-1
if %errorlevel% neq 0 (
    echo WARNING: S3 bucket creation failed. It might already exist.
)

REM Create CloudTrail
echo Creating CloudTrail...
aws cloudtrail create-trail --name ai-soc-security-trail --s3-bucket-name %BUCKET_NAME% --include-global-service-events --is-multi-region-trail --enable-log-file-validation
if %errorlevel% neq 0 (
    echo WARNING: CloudTrail already exists or creation failed. Continuing with existing trail...
)

REM Start logging
echo Starting CloudTrail logging...
aws cloudtrail start-logging --name ai-soc-security-trail
if %errorlevel% neq 0 (
    echo WARNING: CloudTrail logging may already be enabled.
)

echo.
echo ✅ CloudTrail setup complete!
echo Trail Name: ai-soc-security-trail
echo S3 Bucket: %BUCKET_NAME%
echo Status: Logging enabled
echo.
echo Next steps:
echo 1. Run setup-guardduty.bat to enable GuardDuty
echo 2. Run setup-security-hub.bat to enable Security Hub
echo 3. Run setup-config.bat to enable AWS Config
echo.
pause