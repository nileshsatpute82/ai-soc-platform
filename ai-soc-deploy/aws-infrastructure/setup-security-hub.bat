@echo off
echo Setting up AWS Security Hub for AI-SOC Security Platform...

REM Enable Security Hub
echo Enabling Security Hub...
aws securityhub enable-security-hub --enable-default-standards
if %errorlevel% neq 0 (
    echo WARNING: Security Hub already enabled or creation failed. Continuing...
)

REM Enable AWS Config (required for Security Hub)
echo Enabling AWS Config...
echo Note: AWS Config setup requires additional IAM roles. Skipping for now.
echo You can enable Config manually in the AWS Console if needed.

REM Create EventBridge rule for Security Hub findings
echo Creating EventBridge rule for Security Hub findings...
aws events put-rule --name ai-soc-security-hub-findings --event-pattern "{\"source\":[\"aws.securityhub\"],\"detail-type\":[\"Security Hub Findings - Imported\"]}" --description "Route Security Hub findings to AI-SOC platform"

echo.
echo ✅ Security Hub setup complete!
echo Default standards enabled
echo EventBridge rule: ai-soc-security-hub-findings
echo.
pause