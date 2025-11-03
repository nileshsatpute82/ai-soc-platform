#!/bin/bash

# Full AWS Infrastructure Deployment Script
# Deploys RDS, DocumentDB, ElastiCache for AI SOC Platform

set -e

echo "🚀 Deploying Full AWS Infrastructure for AI SOC Platform"
echo "=================================================="

# Configuration
STACK_PREFIX="ai-soc-platform"
REGION="us-east-1"
DB_PASSWORD="AiSocSecure123!"

echo "📋 Configuration:"
echo "  Region: $REGION"
echo "  Stack Prefix: $STACK_PREFIX"
echo ""

# Deploy RDS PostgreSQL
echo "🗄️  Deploying RDS PostgreSQL..."
aws cloudformation create-stack \
  --stack-name "${STACK_PREFIX}-rds" \
  --template-body file://rds-stack.yaml \
  --parameters ParameterKey=DBPassword,ParameterValue="$DB_PASSWORD" \
  --region $REGION

echo "✅ RDS stack creation initiated"

# Deploy DocumentDB
echo "📄 Deploying DocumentDB..."
aws cloudformation create-stack \
  --stack-name "${STACK_PREFIX}-docdb" \
  --template-body file://documentdb-stack.yaml \
  --parameters ParameterKey=MasterUserPassword,ParameterValue="$DB_PASSWORD" \
  --region $REGION

echo "✅ DocumentDB stack creation initiated"

# Deploy ElastiCache Redis
echo "⚡ Deploying ElastiCache Redis..."
aws cloudformation create-stack \
  --stack-name "${STACK_PREFIX}-redis" \
  --template-body file://elasticache-stack.yaml \
  --region $REGION

echo "✅ ElastiCache stack creation initiated"

echo ""
echo "🕐 Waiting for stacks to complete (this may take 10-15 minutes)..."
echo ""

# Wait for RDS
echo "⏳ Waiting for RDS..."
aws cloudformation wait stack-create-complete \
  --stack-name "${STACK_PREFIX}-rds" \
  --region $REGION
echo "✅ RDS deployment complete"

# Wait for DocumentDB
echo "⏳ Waiting for DocumentDB..."
aws cloudformation wait stack-create-complete \
  --stack-name "${STACK_PREFIX}-docdb" \
  --region $REGION
echo "✅ DocumentDB deployment complete"

# Wait for ElastiCache
echo "⏳ Waiting for ElastiCache..."
aws cloudformation wait stack-create-complete \
  --stack-name "${STACK_PREFIX}-redis" \
  --region $REGION
echo "✅ ElastiCache deployment complete"

echo ""
echo "🎉 All infrastructure deployed successfully!"
echo ""

# Get endpoints
echo "📋 Getting connection endpoints..."
echo ""

RDS_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_PREFIX}-rds" \
  --query 'Stacks[0].Outputs[?OutputKey==`DBEndpoint`].OutputValue' \
  --output text \
  --region $REGION)

DOCDB_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_PREFIX}-docdb" \
  --query 'Stacks[0].Outputs[?OutputKey==`ClusterEndpoint`].OutputValue' \
  --output text \
  --region $REGION)

REDIS_ENDPOINT=$(aws cloudformation describe-stacks \
  --stack-name "${STACK_PREFIX}-redis" \
  --query 'Stacks[0].Outputs[?OutputKey==`RedisEndpoint`].OutputValue' \
  --output text \
  --region $REGION)

echo "🔗 Connection Details:"
echo "====================="
echo ""
echo "RDS PostgreSQL:"
echo "  POSTGRES_HOST=$RDS_ENDPOINT"
echo "  POSTGRES_PORT=5432"
echo "  POSTGRES_USER=aisocadmin"
echo "  POSTGRES_PASSWORD=$DB_PASSWORD"
echo "  POSTGRES_DB=ai_soc_db"
echo ""
echo "DocumentDB:"
echo "  DOCDB_HOST=$DOCDB_ENDPOINT"
echo "  DOCDB_PORT=27017"
echo "  DOCDB_USER=aisocadmin"
echo "  DOCDB_PASSWORD=$DB_PASSWORD"
echo "  DOCDB_DATABASE=security_investigations"
echo ""
echo "ElastiCache Redis:"
echo "  REDIS_HOST=$REDIS_ENDPOINT"
echo "  REDIS_PORT=6379"
echo ""
echo "📝 Add these environment variables to your Render.com dashboard"
echo "🚀 Then deploy your application!"