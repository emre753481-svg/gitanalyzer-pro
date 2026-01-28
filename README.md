# 🚀 GitAnalyzer Pro

**Enterprise-level GitHub Repository Analysis Platform with AI-Powered Documentation Generation**

GitAnalyzer Pro automatically analyzes GitHub repositories and generates comprehensive documentation including UML diagrams, BPMN processes, architecture documents, business analysis, requirements, and code quality reports using AI (Claude/GPT).

---

## ✨ Features

### 📊 **Analysis Capabilities**
- **Project Scope Document** - Objectives, scope, assumptions, constraints, deliverables
- **UML Diagrams** - Use case, class, sequence, and activity diagrams
- **BPMN Diagrams** - Business process flows and workflows
- **Flow Diagrams** - User journey maps and data flow diagrams
- **Business Analysis** - SWOT analysis, ROI analysis, stakeholder analysis
- **Requirements** - Functional, non-functional requirements, user stories
- **Architecture** - System architecture, component diagrams, ERD, API docs
- **Code Quality Reports** - Quality scores, technical debt, recommendations

### 🤖 **AI Integration**
- Support for **Anthropic Claude** (Claude 3.5 Sonnet)
- Support for **OpenAI GPT** (GPT-4 Turbo)
- Configurable AI parameters (temperature, max tokens)

### 📥 **Export Formats**
- **PDF** - Professional formatted documents
- **Markdown** - Developer-friendly format
- **JSON** - Machine-readable data

---

## 🏗️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11+** - Programming language
- **Anthropic Claude API** - AI-powered analysis
- **OpenAI GPT API** - Alternative AI provider
- **Pydantic** - Data validation
- **httpx** - Async HTTP client
- **WeasyPrint** - PDF generation

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool
- **TailwindCSS** - Utility-first CSS
- **Zustand** - State management
- **Axios** - HTTP client
- **React Router** - Navigation
- **Lucide React** - Icons

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Railway** - Cloud deployment platform
- **Nginx** - Web server and reverse proxy

---

## 📦 Installation

### Prerequisites
- Docker and Docker Compose
- GitHub Personal Access Token
- Anthropic API Key or OpenAI API Key

### Quick Start with Docker

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/gitanalyzer-pro.git
cd gitanalyzer-pro
```

2. **Configure environment variables**

Create `.env` file in the root directory:
```bash
# GitHub Configuration
GITHUB_TOKEN=your_github_token_here

# AI Provider (anthropic or openai)
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

3. **Start the application**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Installation

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Run the server
uvicorn main:app --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

---

## 🎯 Usage

### 1. **Start Analysis**
- Enter GitHub repository URL
- Provide your GitHub access token
- Select analyzers (optional - leave empty for all)
- Choose AI provider (Anthropic Claude or OpenAI GPT)
- Click "Start Analysis"

### 2. **Monitor Progress**
- Real-time progress tracking
- Current step indication
- Progress percentage
- Estimated time remaining

### 3. **View Results**
- Browse through different analysis tabs
- View scope document, architecture, requirements, etc.
- Explore diagrams and visualizations

### 4. **Export Results**
- Export as PDF for presentations
- Export as Markdown for documentation
- Export as JSON for integration

---

## 📖 API Documentation

### Endpoints

#### `POST /api/analyze`
Start a new repository analysis

**Request:**
```json
{
  "repository_url": "https://github.com/owner/repo",
  "github_token": "ghp_xxxxxxxxxxxxx",
  "analyzers": ["scope", "architecture"],
  "ai_provider": "anthropic"
}
```

**Response:**
```json
{
  "analysis_id": "uuid",
  "status": "pending",
  "created_at": "2024-01-28T10:30:00Z",
  "repository_url": "https://github.com/owner/repo"
}
```

#### `GET /api/analysis/{id}/status`
Get analysis status

**Response:**
```json
{
  "analysis_id": "uuid",
  "status": "processing",
  "progress_percentage": 45,
  "current_step": "Running architecture analyzer",
  "started_at": "2024-01-28T10:30:00Z",
  "completed_at": null,
  "error_message": null
}
```

#### `GET /api/analysis/{id}/results`
Get complete analysis results

#### `POST /api/export/{id}/{format}`
Export analysis results (format: pdf, markdown, json)

For full API documentation, visit: `http://localhost:8000/docs`

---

## 🚀 Deployment

### Railway Deployment

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize project**
```bash
railway init
```

4. **Set environment variables**
```bash
railway variables set ANTHROPIC_API_KEY=your_key_here
railway variables set GITHUB_TOKEN=your_token_here
```

5. **Deploy**
```bash
railway up
```

### Docker Production Deployment

```bash
# Build and run
docker-compose -f docker-compose.yml up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔧 Configuration

### Backend Configuration (`backend/.env`)

```bash
# API Configuration
DEBUG=false
API_VERSION=v1
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# GitHub
GITHUB_TOKEN=your_github_token

# AI Provider
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key

# Model Configuration
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
OPENAI_MODEL=gpt-4-turbo-preview
AI_MAX_TOKENS=8000
AI_TEMPERATURE=0.7

# Storage
ANALYSIS_RESULTS_DIR=./analysis_results

# Logging
LOG_LEVEL=INFO
```

### Frontend Configuration (`frontend/.env`)

```bash
VITE_API_BASE_URL=http://localhost:8000
```

---

## 📂 Project Structure

```
gitanalyzer-pro/
├── backend/
│   ├── core/               # Core utilities (config, logger, exceptions)
│   ├── services/           # GitHub, AI, Export services
│   ├── analyzers/          # 8 analyzer modules
│   ├── models/             # Pydantic models
│   ├── routes/             # API routes
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
│
├── frontend/
│   └── src/
│       ├── components/     # React components
│       ├── pages/          # Page components
│       ├── services/       # API service
│       ├── store/          # Zustand state management
│       ├── types/          # TypeScript types
│       └── main.tsx        # Application entry
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml      # Multi-container setup
├── railway.toml            # Railway deployment config
└── README.md
```

---

## 🔐 Security

- **API Keys**: Never commit API keys to version control
- **GitHub Token**: Use personal access tokens with minimal required permissions
- **Environment Variables**: Always use `.env` files for sensitive data
- **CORS**: Configure CORS origins appropriately for production
- **Rate Limiting**: Built-in rate limiting for API endpoints

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🐛 Troubleshooting

### Common Issues

**1. API Key Errors**
```
Error: ANTHROPIC_API_KEY not configured
```
Solution: Ensure your `.env` file contains valid API keys

**2. GitHub Rate Limiting**
```
Error: GitHub API rate limit exceeded
```
Solution: Use a GitHub token with higher rate limits or wait for reset

**3. PDF Generation Issues**
```
Error: Failed to generate PDF
```
Solution: Ensure WeasyPrint dependencies are installed (Cairo, Pango)

**4. Port Already in Use**
```
Error: Address already in use
```
Solution: Change ports in docker-compose.yml or stop conflicting services

---

## 📧 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Contact: support@gitanalyzer.pro
- Documentation: https://docs.gitanalyzer.pro

---

## 🎉 Acknowledgments

- **Anthropic** for Claude AI
- **OpenAI** for GPT models
- **FastAPI** team for the amazing framework
- **React** team for the UI library
- All open-source contributors

---

**Made with ❤️ by the GitAnalyzer Pro Team**
