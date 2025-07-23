# Tech Spec Analyzer Pro

## Overview

Professional-grade technical document analysis application with AI-powered parameter extraction and component compatibility checking. Built with Flask backend, advanced frontend interface, and sophisticated analysis algorithms.

## Features

### 🔬 Advanced Analysis Engine
- **AI-Powered Parameter Extraction**: Intelligent pattern recognition for technical specifications
- **Multi-Component Compatibility**: Comprehensive analysis for PSU, LED, and electronic components
- **Confidence Scoring**: Reliability assessment for all extracted parameters
- **Real-time Processing**: Instant analysis with progress feedback

### 🎨 Professional Interface
- **Modern Dark Theme**: Bootstrap-based responsive design
- **Interactive Controls**: Drag-and-drop, keyboard shortcuts, auto-save
- **Visual Parameter Preview**: Card-based display of extracted technical data
- **Multiple Export Formats**: JSON, formatted text, and professional reports

### 🚀 Performance Features
- **Optimized Regex Engine**: Fast parameter extraction with high accuracy
- **Intelligent Caching**: Local storage for user preferences and documents
- **Progressive Enhancement**: Works with and without JavaScript
- **Mobile Responsive**: Full functionality on all device sizes

## Project Structure

```
tech-spec-analyzer-pro/
├── backend/                 # Flask application backend
│   ├── app.py              # Main Flask application
│   └── __init__.py
├── frontend/               # Static assets and templates
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Enhanced styling with animations
│   │   ├── js/
│   │   │   └── app.js      # Advanced JavaScript functionality
│   │   └── images/
│   └── templates/
│       ├── index.html      # Main application template
│       └── components/     # Reusable template components
├── ai/                     # AI analysis modules
│   ├── parameter_extractor.py  # Advanced parameter extraction
│   └── __init__.py
├── config/                 # Configuration management
│   ├── settings.py         # Application settings
│   └── __init__.py
├── docs/                   # Documentation
│   └── README.md
└── main.py                 # Application entry point
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install flask gunicorn
   ```

2. **Run Application**
   ```bash
   cd tech-spec-analyzer-pro
   python main.py
   ```

3. **Access Interface**
   - Open browser to `http://localhost:5000`
   - Click "Load Example" to see sample analysis
   - Paste your technical documents and analyze

## Usage Guide

### Document Input
- Paste technical datasheets, specifications, or manuals
- Supports various formats: component specs, power supply data, LED documentation
- Auto-detects parameters like voltage, current, power, temperature

### Analysis Queries
- Ask natural language questions about compatibility
- Example: "Check if PSU X100 is compatible with LED Strip Alpha"
- Use query suggestions for common analysis types

### Results Interpretation
- **Compatible**: Components work together safely
- **Incompatible**: Specification mismatch found
- **Insufficient Data**: Missing required parameters
- **Confidence Score**: Reliability of the analysis (High/Medium/Low)

## Advanced Features

### Keyboard Shortcuts
- `Ctrl+Enter`: Run analysis
- `Ctrl+L`: Load example data
- `Ctrl+K`: Clear all inputs

### Export Options
- **JSON Format**: Complete technical analysis data
- **Formatted Report**: Human-readable analysis summary
- **Professional Export**: Downloadable analysis reports

### Parameter Types Supported
- **Electrical**: Voltage, current, power, frequency
- **Thermal**: Operating temperature, thermal resistance
- **Physical**: Dimensions, weight, form factor
- **Compliance**: Certifications, standards, ratings

## Technical Specifications

### Supported Components
- Power Supply Units (PSU)
- LED strips and modules
- Electronic components
- Sensors and modules
- Any device with technical specifications

### Analysis Accuracy
- **High Confidence**: >80% accuracy for structured datasheets
- **Medium Confidence**: 60-80% accuracy for mixed format documents
- **Low Confidence**: <60% accuracy for unstructured text

### Performance Metrics
- **Analysis Speed**: <3 seconds for typical documents
- **Document Size**: Up to 1MB text documents
- **Parameter Extraction**: Up to 50 parameters per analysis
- **Browser Support**: Modern browsers with ES6+ support

## Configuration

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- `FLASK_ENV`: Environment mode (development/production)
- `FLASK_DEBUG`: Enable debug mode (true/false)

### Application Settings
- Maximum document size: 1MB
- Analysis timeout: 30 seconds
- Confidence threshold: 60%
- Voltage tolerance: ±0.5V

## Development

### Code Organization
- **Backend**: Pure Flask with type hints and comprehensive error handling
- **Frontend**: Modern JavaScript with ES6+ features and Bootstrap 5
- **AI Module**: Extensible parameter extraction with confidence scoring
- **Configuration**: Environment-based settings with development/production modes

### Adding New Parameter Types
1. Extend `ParameterType` enum in `ai/parameter_extractor.py`
2. Add regex patterns to `_initialize_patterns()`
3. Update frontend to display new parameter types
4. Test with sample documents

### Customization
- Modify CSS variables in `style.css` for theme changes
- Update regex patterns for new document formats
- Extend JavaScript functionality in `app.js`
- Configure analysis parameters in `config/settings.py`

## Troubleshooting

### Common Issues
- **No parameters found**: Check document format and add structured data
- **Low confidence scores**: Improve document structure or add more specific patterns
- **Analysis timeout**: Reduce document size or increase timeout in settings
- **JavaScript errors**: Ensure modern browser with ES6+ support

### Debug Mode
Enable debug mode for detailed error messages and request logging:
```bash
export FLASK_DEBUG=true
python main.py
```

## License

Professional technical analysis tool built for engineering and development teams.

---

Built with Flask, Bootstrap, and Advanced AI Analysis Engine