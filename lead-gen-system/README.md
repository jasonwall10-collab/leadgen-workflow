# LeadGen Workflow System

## Overview
A complete autonomous workflow system for researching and upgrading local business websites.

## Architecture
- **Backend**: FastAPI REST API
- **Frontend**: Vue.js single-page dashboard
- **Database**: SQLite with job state tracking
- **Vector Store**: ChromaDB for summary retention
- **Communication**: Telegram bot for approvals

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Telegram bot token
- Coolify project access

### Deployment

1. **Clone and Configure**
   ```bash
   git clone https://github.com/your-org/leadgen-workflow
   cd lead-gen-workflow
   cp .env.example .env
   # Edit .env with your Telegram bot token and chat ID
   ```

2. **Build and Deploy**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Access the System**
   - Frontend: http://localhost:8080
   - API: http://localhost:8000

### API Endpoints

#### Business Management
- `POST /api/intake` - Add new business for processing
- `GET /api/business/{id}` - Get business details
- `POST /api/upload-csv` - Bulk import from CSV

#### Workflow Stages
- `POST /api/analyze` - Website audit
- `POST /api/competitors` - Competitor research
- `POST /api/rebuild` - Site rebuild generation
- `POST /api/demo` - Demo site deployment
- `POST /api/pitch` - Pitch generation

#### Status Management
- `GET /api/status/{job_id}` - Get job status
- `GET /api/jobs` - List all jobs
- `GET /api/logs` - View system logs

## Features

### Automated Workflow
- Intake → Analysis → Competitors → Rebuild → Demo → Pitch
- State machine tracking with retry logic
- Resume capability after interruptions

### Approval System
- Telegram bot for business approval
- Dashboard approval gate with audit trail
- Automated status updates

### Data Management
- SQLite database for persistence
- ChromaDB vector store for summaries
- CSV import/export functionality

### Security
- JWT authentication (configurable)
- Input validation with Pydantic
- Rate limiting on API endpoints

## Configuration

### Environment Variables
- `TELEGRAM_TOKEN`: Telegram bot token
- `TELEGRAM_CHAT_ID`: Chat ID for approvals
- `DATABASE_PATH`: SQLite database location
- `API_HOST`: API host address
- `API_PORT`: API port number
- `FRONTEND_PORT`: Frontend port number

### Coolify Deployment
1. Create new project in Coolify
2. Add environment variables
3. Deploy using docker-compose
4. Configure domain and SSL

## Usage

### Manual Processing
1. Add business via API or CSV upload
2. System processes through workflow stages
3. Approve demo sites via Telegram or dashboard
4. Receive final pitch materials

### Batch Processing
1. Upload CSV with lead list
2. System processes all businesses automatically
3. Track progress via dashboard
4. Review results in database

## Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
python app.py

# Run frontend (Vue.js)
npm run serve
```

### Testing
```bash
# Run unit tests
pytest

# Run integration tests
pytest -m integration
```

## API Documentation

Swagger UI available at `/docs` endpoint.

## Support

For issues and questions:
- Check the logs: `docker-compose logs`
- Review the database: `sqlite3 data/leads.db`
- Check Telegram bot status

## License
MIT License - see LICENSE file for details.

## Changelog

### v1.0.0
- Initial release
- Complete workflow automation
- Telegram integration
- CSV import functionality

### v1.1.0
- Added A/B testing for rebuild strategies
- Enhanced security features
- Improved error handling

### v1.2.0
- Added Google Analytics integration
- Enhanced frontend dashboard
- Performance optimizations