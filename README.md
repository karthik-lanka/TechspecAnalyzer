# TechspecAnalyzer

A professional-grade web application for analyzing technical documents and determining component compatibility using advanced AI-powered parameter extraction.

## 🎯 Overview

Tech Spec Analyzer Pro is a sophisticated Flask-based web application that revolutionizes how engineers and technical professionals analyze component specifications. The system intelligently extracts technical parameters from documents and performs compatibility analysis, with initial focus on PSU/LED components and expandable architecture for other component types.

## ✨ Key Features

- **🔍 Advanced Parameter Extraction**: AI-powered regex-based analysis with confidence scoring
- **📊 Real-time Analysis**: Instant compatibility decisions with detailed justifications
- **💾 Database Integration**: PostgreSQL-backed history tracking and statistics
- **🎨 Modern Interface**: Dark theme with interactive animations and keyboard shortcuts
- **📈 Analytics Dashboard**: Comprehensive statistics and session management
- **📤 Export Capabilities**: Multiple format support for analysis reports
- **⚡ Auto-save**: Automatic content preservation and recovery

## 🏗️ System Architecture

```
Tech Spec Analyzer Pro
├── Backend (Flask + SQLAlchemy)
│   ├── REST API Endpoints
│   ├── Parameter Extraction Engine
│   ├── Database Models
│   └── Session Management
├── Frontend (Bootstrap 5 + JavaScript)
│   ├── Interactive UI Components
│   ├── Real-time Updates
│   ├── History Management
│   └── Export Functions
├── AI Engine
│   ├── Pattern Recognition
│   ├── Confidence Scoring
│   └── Multi-component Support
└── Database (PostgreSQL)
    ├── Analysis History
    ├── Statistics Tracking
    └── User Preferences
```

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL database
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd tech-spec-analyzer-pro

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Set required environment variables
export DATABASE_URL="postgresql://username:password@localhost/dbname"
export SESSION_SECRET="your-secret-key-here"
```

### 3. Database Setup

```bash
# Initialize database tables
python -c "from backend.app import db; db.create_all()"
```

### 4. Run Application

```bash
# Start the development server
python main.py

# Or use Gunicorn for production
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

The application will be available at `http://localhost:5000`

## 🔄 Application Flow

### Analysis Workflow

```mermaid
graph TD
    A[User Input] --> B[Document Text + Query]
    B --> C[Parameter Extraction]
    C --> D[Pattern Matching]
    D --> E[Numerical Analysis]
    E --> F[Compatibility Decision]
    F --> G[Results Display]
    G --> H[Save to Database]
    H --> I[Update Statistics]
    
    J[View History] --> K[Load Statistics]
    K --> L[Display Sessions]
    L --> M[Filter & Export]
```

### Data Processing Pipeline

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant AI as AI Engine
    participant DB as Database
    
    U->>F: Submit document & query
    F->>B: POST /analyze
    B->>AI: Extract parameters
    AI->>B: Return extracted data
    B->>B: Perform compatibility analysis
    B->>DB: Save analysis session
    B->>F: Return results
    F->>U: Display formatted results
    
    U->>F: View history
    F->>B: GET /api/history
    B->>DB: Fetch sessions
    DB->>B: Return session data
    B->>F: Send history
    F->>U: Show history modal
```

### Component Architecture

```mermaid
graph LR
    subgraph "Frontend Layer"
        A[HTML Templates]
        B[CSS Styling]
        C[JavaScript Logic]
    end
    
    subgraph "Backend Layer"
        D[Flask Routes]
        E[Business Logic]
        F[Database Models]
    end
    
    subgraph "AI Layer"
        G[Parameter Extractor]
        H[Pattern Engine]
        I[Confidence Scorer]
    end
    
    subgraph "Data Layer"
        J[PostgreSQL]
        K[Session Storage]
        L[Statistics]
    end
    
    A --> D
    B --> A
    C --> D
    D --> E
    E --> F
    E --> G
    G --> H
    H --> I
    F --> J
    J --> K
    J --> L
```

## 📚 API Documentation

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application interface |
| `/analyze` | POST | Perform document analysis |
| `/api/history` | GET | Retrieve analysis history |
| `/api/stats` | GET | Get usage statistics |
| `/api/session/<id>` | GET | Get specific session details |
| `/api/clear-history` | POST | Clear analysis history |
| `/health` | GET | Application health check |

### Request/Response Examples

#### Analysis Request
```json
{
  "document_text": "Power Supply: Output 12V, 5A max current...",
  "user_query": "Can this PSU power an LED strip requiring 10V-14V, 3A?"
}
```

#### Analysis Response
```json
{
  "Decision": "Compatible",
  "Confidence_Score": "High",
  "Justification": "PSU voltage (12V) is within LED requirements (10V-14V)...",
  "Extracted_Technical_Data": {
    "PSU_Output_Voltage": "12V",
    "PSU_Max_Current": "5A",
    "LED_Min_Voltage": "10V",
    "LED_Max_Voltage": "14V",
    "LED_Current": "3A"
  },
  "Referenced_Sections": [
    {
      "section_name": "Power Requirements",
      "details": "Voltage and current specifications"
    }
  ]
}
```

## 🎨 User Interface Guide

### Main Interface

The application features a clean, dark-themed interface with:

- **Document Input Area**: Large textarea for pasting technical documents
- **Query Input**: Specific compatibility question input
- **Quick Suggestions**: Pre-defined query templates
- **Analysis Results**: Formatted output with confidence indicators
- **Parameter Preview**: Visual cards showing extracted parameters
- **History Access**: Modal for viewing past analyses

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Start analysis |
| `Ctrl+L` | Load example |
| `Ctrl+K` | Clear inputs |

### Interactive Features

- **Real-time validation**: Input validation with visual feedback
- **Auto-save**: Automatic content preservation
- **Export options**: JSON and formatted text export
- **History management**: Full session tracking with statistics

## 🔧 Configuration

### Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:port/dbname
SESSION_SECRET=your-secret-key

# Optional
FLASK_ENV=development
DEBUG=True
```

### Application Settings

The application can be configured through the `config/settings.py` file:

```python
class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## 📁 Project Structure

```
tech-spec-analyzer-pro/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── database.py         # Database initialization
│   └── models.py           # Database models
├── frontend/
│   ├── templates/
│   │   └── index.html      # Main UI template
│   └── static/
│       ├── css/
│       │   └── styles.css  # Custom styling
│       └── js/
│           └── app.js      # Frontend logic
├── ai/
│   └── parameter_extractor.py  # AI analysis engine
├── config/
│   └── settings.py         # Configuration management
├── docs/
│   └── api.md              # API documentation
├── main.py                 # Application entry point
└── README.md               # This file
```

## 🛠️ Development

### Adding New Component Types

1. **Extend Pattern Recognition**: Add new regex patterns in `ai/parameter_extractor.py`
2. **Update Analysis Logic**: Modify compatibility rules in `backend/app.py`
3. **Enhance UI**: Add new parameter types to frontend display

### Database Schema

The application uses the following main models:

- **AnalysisSession**: Stores complete analysis results
- **ExtractedParameter**: Individual parameter extractions
- **ReferencedSection**: Document sections used in analysis

### Testing

```bash
# Run basic functionality test
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"document_text":"Test document","user_query":"Test query"}'

# Check health endpoint
curl http://localhost:5000/health
```

## 📊 Performance & Analytics

### Built-in Analytics

- **Success Rate Tracking**: Monitor analysis accuracy
- **Processing Time Metrics**: Performance monitoring
- **Usage Statistics**: Session and query analytics
- **Decision Breakdown**: Compatibility result distribution

### Optimization Features

- **Efficient Regex Patterns**: Optimized for speed and accuracy
- **Database Indexing**: Fast query performance
- **Frontend Caching**: Reduced server load
- **Session Management**: Memory-efficient storage

## 🔐 Security

### Data Protection

- **Session Management**: Secure Flask sessions
- **Input Validation**: Comprehensive input sanitization
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **XSS Protection**: Template auto-escaping

### Privacy

- **Local Processing**: All analysis performed locally
- **No External APIs**: Self-contained analysis engine
- **Data Retention**: User-controlled history management

## 🚀 Deployment

### Production Deployment

1. **Set Environment Variables**
2. **Initialize Database**
3. **Configure Web Server** (Gunicorn + Nginx)
4. **Set Up SSL Certificate**
5. **Configure Monitoring**

### Docker Deployment

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Check the documentation in `/docs`
- Review the API endpoints
- Examine the application logs
- Test with the health check endpoint

## 🔄 Version History

- **v1.0.0**: Initial release with basic analysis
- **v2.0.0**: Added database functionality and history tracking
- **v2.1.0**: Enhanced UI with interactive features
- **v2.2.0**: Added statistics and export capabilities

---

Built with ❤️ using Flask, Bootstrap, and PostgreSQL for reliable technical document analysis.
