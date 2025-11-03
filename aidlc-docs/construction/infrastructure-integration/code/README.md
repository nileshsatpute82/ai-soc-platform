# AI-Powered Security Operations Platform - Infrastructure Unit

## Quick Start (Working Prototype)

### 1. GitHub Repository Setup

```bash
# Create new repository
git init
git add .
git commit -m "Initial AI SOC Infrastructure"
git branch -M main
git remote add origin https://github.com/yourusername/ai-soc-platform.git
git push -u origin main
```

### 2. Render.com Deployment

1. **Connect GitHub**: Link your GitHub repository to Render.com
2. **Auto-Deploy**: Pushes to `main` branch automatically deploy
3. **Environment Variables**: Set these in Render dashboard:

```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
POSTGRES_HOST=your-rds-endpoint
POSTGRES_PASSWORD=your_password
DOCDB_HOST=your-docdb-endpoint
DOCDB_PASSWORD=your_password
REDIS_HOST=your-elasticache-endpoint
SECRET_KEY=your-flask-secret
```

### 3. AWS Services Setup

**Required AWS Services:**
- **RDS PostgreSQL**: For structured data
- **DocumentDB**: For investigation data
- **ElastiCache Redis**: For caching
- **Bedrock**: For AI processing
- **SQS**: For message queues

### 4. Test Deployment

```bash
# Health check
curl https://your-app.onrender.com/health/

# API endpoints
curl https://your-app.onrender.com/api/config/
curl https://your-app.onrender.com/api/mitre/techniques
```

## API Endpoints

- `GET /health/` - System health
- `GET /api/config/` - Configuration management
- `GET /api/audit/events` - Audit logs
- `GET /api/mitre/techniques` - MITRE ATT&CK data

## Architecture

```
Render.com (Flask App) → AWS Services
├── RDS PostgreSQL (structured data)
├── DocumentDB (investigations)
├── ElastiCache Redis (caching)
├── Bedrock (AI processing)
└── SQS (message queues)
```

## Next Steps

1. Deploy infrastructure unit
2. Add Core Platform Service unit
3. Add AI Crew units
4. Add Frontend Dashboard unit