# Tech Spec Analyzer Pro

## Overview

Professional-grade technical document analysis application with AI-powered parameter extraction and component compatibility checking. The application has been completely restructured into a modular, scalable architecture with advanced features including real-time analysis, interactive UI, confidence scoring, and multiple export formats.

## Recent Changes (January 2025)

✓ **Complete Architecture Overhaul**: Restructured into professional modular design with separate backend, frontend, AI, and config modules
✓ **Enhanced User Interface**: Modern dark theme with interactive features, animations, keyboard shortcuts, and parameter preview cards
✓ **Advanced AI Engine**: Sophisticated parameter extraction with confidence scoring and multi-component support
✓ **Professional Features**: Export capabilities, formatted reports, real-time validation, and auto-save functionality
✓ **Better Organization**: Clear separation of concerns with proper package structure and documentation

## User Preferences

Preferred communication style: Simple, everyday language.
Architecture preference: Modular, professional structure with clear separation of concerns.

## System Architecture

This is now a professional-grade modular Flask application with advanced features:

### Project Structure
```
tech-spec-analyzer-pro/
├── backend/                 # Flask application core
├── frontend/               # Static assets and templates
├── ai/                     # Advanced AI analysis modules
├── config/                 # Configuration management
├── docs/                   # Professional documentation
└── main.py                 # Application entry point
```

### Core Components
- **Backend**: Type-annotated Flask with comprehensive error handling and health checks
- **Frontend**: Interactive Bootstrap 5 interface with advanced JavaScript functionality
- **AI Module**: Extensible parameter extraction engine with confidence scoring
- **Configuration**: Environment-based settings with development/production modes

## Key Components

### Web Framework
- **Flask**: Lightweight Python web framework chosen for simplicity and rapid development
- **Template Engine**: Jinja2 templates for server-side rendering
- **Static Assets**: Bootstrap CSS framework with custom styling

### Text Analysis Engine
- **Parameter Extraction**: Regex-based pattern matching for technical specifications
- **Numerical Processing**: Custom functions to extract and validate numerical values
- **Document Processing**: Text analysis for technical documentation and datasheets

### User Interface
- **Bootstrap 5**: Dark theme UI framework for responsive design
- **Icons**: Bootstrap Icons for visual elements
- **Form Handling**: AJAX-based form submission for seamless user experience

## Data Flow

1. **Input Phase**: User pastes technical document content and enters query via web form
2. **Submission**: Form data sent via POST request to `/analyze` endpoint as JSON
3. **Processing**: Flask server processes document text using regex patterns to extract parameters
4. **Analysis**: System matches extracted parameters against user query requirements
5. **Response**: Results returned as structured JSON with compatibility decisions and justifications
6. **Display**: Frontend renders analysis results in formatted, readable format

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Logging**: Built-in Python logging for debugging and monitoring

### Frontend Libraries
- **Bootstrap 5**: CSS framework loaded via CDN
- **Bootstrap Icons**: Icon library for UI elements
- **Custom CSS**: Application-specific styling

### Environment Variables
- **SESSION_SECRET**: Flask session key (falls back to development default)

## Deployment Strategy

### Development Setup
- **Entry Point**: `main.py` runs Flask development server
- **Configuration**: Debug mode enabled for development
- **Host Binding**: Configured for `0.0.0.0:5000` to work with Replit

### Production Considerations
- Environment-based secret key management
- Logging configuration for different deployment environments
- Static file serving through Flask (suitable for small-scale deployment)

### Architecture Decisions

**Problem**: Need to analyze technical documents and extract parameters
**Solution**: Regex-based pattern matching with predefined parameter templates
**Rationale**: Simple, reliable, and doesn't require external AI service dependencies

**Problem**: User interface for document input and result display
**Solution**: Bootstrap-based responsive web interface with dark theme
**Rationale**: Professional appearance, mobile-friendly, and integrates well with Replit

**Problem**: Data exchange between frontend and backend
**Solution**: JSON-based REST API with AJAX form submission
**Rationale**: Clean separation of concerns and good user experience without page reloads

**Problem**: Session management and security
**Solution**: Flask's built-in session handling with environment-based secret keys
**Rationale**: Simple implementation suitable for demonstration purposes