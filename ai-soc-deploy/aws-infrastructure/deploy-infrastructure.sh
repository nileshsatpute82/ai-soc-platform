#!/bin/bash

# Deploy AWS Infrastructure for AI Security Operations Platform

STACK_NAME="ai-soc-platform-infrastructure"
REGION="us-east-1"

echo "🚀 Deploying AI Security Operations Platform Infrastructure..."

# Deploy CloudFormation stack
aws cloudformation deploy \
  --template-file cloudformation-stack.yaml \
  --stack-name $STACK_NAME \
  --region $REGION \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides ProjectName=ai-soc-platform

if [ $? -eq 0 ]; then
    echo "✅ Infrastructure deployed successfully!"
    
    # Get outputs
    echo "📋 Getting stack outputs..."
    aws cloudformation describe-stacks \
      --stack-name $STACK_NAME \
      --region $REGION \
      --query 'Stacks[0].Outputs' \
      --output table
    
    # Get SQS Queue URL for environment variables
    QUEUE_URL=$(aws cloudformation describe-stacks \
      --stack-name $STACK_NAME \
      --region $REGION \
      --query 'Stacks[0].Outputs[?OutputKey==`SecurityAlertsQueueUrl`].OutputValue' \
      --output text)
    
    echo ""
    echo "🔧 Add this to your Render.com environment variables:"
    echo "AWS_SQS_QUEUE_URL=$QUEUE_URL"
    echo ""
    echo "🎯 Infrastructure is ready for real security alerts!"
    
else
    echo "❌ Infrastructure deployment failed!"
    exit 1
fi