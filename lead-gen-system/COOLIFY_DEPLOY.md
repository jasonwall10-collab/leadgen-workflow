# LeadGen Workflow System - Coolify Deployment Guide

## Prerequisites
- A Coolify account with access to the "OpenClaw" project
- Docker Hub or private registry access (optional, for image pushes)

## Option 1: Deploy via Coolify Web UI (Recommended)

1. **Log into Coolify** and navigate to your "OpenClaw" project

2. **Create New Resource** → "Docker Compose"

3. **Upload Configuration**
   - Repository URL: (leave blank if uploading files directly)
   - Upload the entire `lead-gen-system` directory as a ZIP file, OR
   - Use the files from the workspace: `C:\Users\admin\.openclaw\workspace\lead-gen-system\`

4. **Environment Variables**
   In Coolify resource settings, add these environment variables:
   ```
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHAT_ID=your_telegram_chat_id_here
   DATABASE_PATH=/app/data/leads.db
   API_HOST=0.0.0.0
   API_PORT=8000
   NODE_ENV=production
   ```

5. **Volumes**
   Add persistent volume mapping:
   - Host path: `/var/lib/coolify/containers/leadgen-workflow/data`
   - Container path: `/app/data`

6. **Network**
   Ensure the backend is accessible on port 8000
   The frontend will be accessible through the Coolify proxy

7. **Deploy**
   Click "Deploy" and wait for the containers to start

## Option 2: Deploy via Coolify CLI (if installed)

```bash
# Login to Coolify (if not already)
coolify login

# Create application from local directory
coolify create application \
  --name "leadgen-workflow" \
  --project "OpenClaw" \
  --source ./lead-gen-system \
  --docker-compose ./lead-gen-system/docker-compose.yml

# Set environment variables
coolify set-env --application leadgen-workflow \
  --key TELEGRAM_TOKEN --value "YOUR_TOKEN"
coolify set-env --application leadgen-workflow \
  --key TELEGRAM_CHAT_ID --value "YOUR_CHAT_ID"

# Deploy
coolify deploy --application leadgen-workflow
```

## Option 3: Build and Push to Docker Registry

```bash
# Build images locally
cd lead-gen-system
docker-compose build

# Tag images for registry
docker tag leadgen-backend jasonwall10/leadgen-backend:latest
docker tag leadgen-frontend jasonwall10/leadgen-frontend:latest

# Push to Docker Hub
docker push jasonwall10/leadgen-backend:latest
docker push jasonwall10/leadgen-frontend:latest
```

Then in Coolify:
- Create a Docker Compose resource
- Use the pushed images
- Set environment variables
- Deploy

## Post-Deployment Steps

1. **Test the API**
   ```bash
   # Get your Coolify deployment URL
   curl https://your-coolify-domain.com/api/docs
   ```

2. **Upload CSV**
   ```bash
   curl -X POST https://your-coolify-domain.com/api/upload-csv \
     -F "file=@leads.csv"
   ```

3. **Configure Telegram Bot**
   - Set webhook: `https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your-domain.com/webhook`
   - The bot will send approval requests to your chat

4. **Monitor Logs**
   - Access Coolify logs for both backend and frontend containers

## File Structure in Coolify

```
lead-gen-system/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── models.py
│   └── data/ (mounted volume)
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf (optional)
├── docker-compose.yml
├── .env.example
├── deploy.sh
└── README.md
```

## Notes

- The SQLite database is stored in the `data` directory which is mounted as a volume for persistence
- The Telegram bot requires the `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` environment variables
- For production, consider adding SSL certificates through Coolify's built-in proxy
- The system is designed to run continuously; set restart policy to "always"

Need help? Coolify documentation: https://docs.coolify.io/