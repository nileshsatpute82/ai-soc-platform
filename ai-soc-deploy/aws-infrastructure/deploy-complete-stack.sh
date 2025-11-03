#!/bin/bash

# Deploy Complete Real AWS Stack for AI Security Operations Platform

STACK_NAME="ai-soc-platform-complete"
REGION="us-east-1"
DB_PASSWORD="AISec2024!Platform"

echo "🚀 Deploying Complete AI Security Operations Platform Stack..."
echo "⚠️  This will create real AWS resources with costs!"
echo "💰 Estimated monthly cost: $80-120 (RDS + DocumentDB + ElastiCache)"
echo ""

read -p "Continue with deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

# Deploy complete stack
aws cloudformation deploy \
  --template-file real-aws-stack.yaml \
  --stack-name $STACK_NAME \
  --region $REGION \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    ProjectName=ai-soc-platform \
    DBUsername=aisoc_admin \
    DBPassword=$DB_PASSWORD

if [ $? -eq 0 ]; then
    echo "✅ Complete stack deployed successfully!"
    
    # Get all outputs
    echo "📋 Getting stack outputs..."
    aws cloudformation describe-stacks \
      --stack-name $STACK_NAME \
      --region $REGION \
      --query 'Stacks[0].Outputs' \
      --output table
    
    # Get specific endpoints for environment variables
    POSTGRES_HOST=$(aws cloudformation describe-stacks \
      --stack-name $STACK_NAME \
      --region $REGION \
      --query 'Stacks[0].Outputs[?OutputKey==`PostgreSQLEndpoint`].OutputValue' \
      --output text)
    
    DOCDB_HOST=$(aws cloudformation describe-stacks \
      --stack-name $STACK_NAME \
      --region $REGION \
      --query 'Stacks[0].Outputs[?OutputKey==`DocumentDBEndpoint`].OutputValue' \
      --output text)
    
    REDIS_HOST=$(aws cloudformation describe-stacks \
      --stack-name $STACK_NAME \
      --region $REGION \
      --query 'Stacks[0].Outputs[?OutputKey==`ElastiCacheEndpoint`].OutputValue' \
      --output text)
    
    QUEUE_URL=$(aws cloudformation describe-stacks \
      --stack-name $STACK_NAME \
      --region $REGION \
      --query 'Stacks[0].Outputs[?OutputKey==`SecurityAlertsQueueUrl`].OutputValue' \
      --output text)
    
    echo ""
    echo "🔧 Add these environment variables to Render.com:"
    echo "================================================"
    echo "# Database Connections"
    echo "POSTGRES_HOST=$POSTGRES_HOST"
    echo "POSTGRES_USER=aisoc_admin"
    echo "POSTGRES_PASSWORD=$DB_PASSWORD"
    echo "POSTGRES_DB=ai_soc_db"
    echo ""
    echo "DOCDB_HOST=$DOCDB_HOST"
    echo "DOCDB_USER=aisoc_admin"
    echo "DOCDB_PASSWORD=$DB_PASSWORD"
    echo "DOCDB_DATABASE=security_investigations"
    echo ""
    echo "REDIS_HOST=$REDIS_HOST"
    echo ""
    echo "# SQS Queue"
    echo "AWS_SQS_QUEUE_URL=$QUEUE_URL"
    echo ""
    echo "# Enable Full Real AWS Mode"
    echo "USE_REAL_AWS=true"
    echo "ENABLE_REAL_DATABASES=true"
    echo ""
    echo "🎉 Your complete AI Security Operations Platform is ready!"
    echo "💡 All alerts will now be saved to persistent storage"
    echo "📊 Dashboard will show real statistics and historical data"
    
else
    echo "❌ Stack deployment failed!"
    exit 1
fi