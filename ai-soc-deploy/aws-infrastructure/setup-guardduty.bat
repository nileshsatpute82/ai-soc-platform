@echo off
echo Setting up AWS GuardDuty for AI-SOC Security Platform...

REM Enable GuardDuty
echo Enabling GuardDuty...
aws guardduty create-detector --enable --finding-publishing-frequency FIFTEEN_MINUTES
if %errorlevel% neq 0 (
    echo WARNING: GuardDuty already enabled or creation failed. Continuing...
)

REM Get detector ID
echo Getting GuardDuty detector ID...
for /f "tokens=*" %%i in ('aws guardduty list-detectors --query DetectorIds[0] --output text') do set DETECTOR_ID=%%i

if "%DETECTOR_ID%"=="" (
    echo WARNING: Could not retrieve GuardDuty detector ID. Service may not be available in this region.
)

echo GuardDuty Detector ID: %DETECTOR_ID%

REM Create EventBridge rule for GuardDuty findings
echo Creating EventBridge rule for GuardDuty findings...
aws events put-rule --name ai-soc-guardduty-findings --event-pattern "{\"source\":[\"aws.guardduty\"],\"detail-type\":[\"GuardDuty Finding\"]}" --description "Route GuardDuty findings to AI-SOC platform"

REM Get SQS queue ARN (assuming it exists from infrastructure setup)
echo Getting SQS queue ARN...
for /f "tokens=*" %%i in ('aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/$(aws sts get-caller-identity --query Account --output text)/ai-soc-security-alerts --attribute-names QueueArn --query Attributes.QueueArn --output text') do set QUEUE_ARN=%%i

if not "%QUEUE_ARN%"=="" (
    echo Adding EventBridge target for SQS queue...
    aws events put-targets --rule ai-soc-guardduty-findings --targets "Id"="1","Arn"="%QUEUE_ARN%"
)

echo.
echo ✅ GuardDuty setup complete!
echo Detector ID: %DETECTOR_ID%
echo Finding frequency: Every 15 minutes
echo EventBridge rule: ai-soc-guardduty-findings
echo.
pause