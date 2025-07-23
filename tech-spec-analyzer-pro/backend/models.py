"""
Database Models for Tech Spec Analyzer Pro
Stores analysis history, extracted parameters, and user preferences
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class AnalysisSession(db.Model):
    """Stores complete analysis sessions with documents and results"""
    __tablename__ = 'analysis_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), unique=True, nullable=False, index=True)
    document_text = Column(Text, nullable=False)
    user_query = Column(Text, nullable=False)
    analysis_results = Column(JSON, nullable=True)  # Complete JSON response
    decision = Column(String(50), nullable=True)    # Compatible/Incompatible/etc
    confidence_score = Column(String(20), nullable=True)  # High/Medium/Low
    justification = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_successful = Column(Boolean, default=False, nullable=False)
    processing_time_ms = Column(Integer, nullable=True)
    document_size = Column(Integer, nullable=True)  # Character count
    
    # Relationships
    extracted_parameters = relationship("ExtractedParameter", back_populates="session", cascade="all, delete-orphan")
    referenced_sections = relationship("ReferencedSection", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<AnalysisSession {self.session_id}: {self.decision}>'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'decision': self.decision,
            'confidence_score': self.confidence_score,
            'justification': self.justification,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_successful': self.is_successful,
            'processing_time_ms': self.processing_time_ms,
            'document_size': self.document_size,
            'parameter_count': len(self.extracted_parameters)
        }

class ExtractedParameter(db.Model):
    """Stores individual extracted technical parameters"""
    __tablename__ = 'extracted_parameters'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), ForeignKey('analysis_sessions.session_id'), nullable=False)
    parameter_name = Column(String(100), nullable=False)
    parameter_value = Column(String(200), nullable=False)
    numerical_value = Column(Float, nullable=True)
    unit = Column(String(20), nullable=True)
    parameter_type = Column(String(50), nullable=True)  # voltage, current, power, etc
    confidence = Column(Float, nullable=True)  # 0.0 to 1.0
    source_text = Column(Text, nullable=True)  # Original text where parameter was found
    extraction_pattern = Column(String(200), nullable=True)  # Which regex pattern matched
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    session = relationship("AnalysisSession", back_populates="extracted_parameters")
    
    def __repr__(self):
        return f'<ExtractedParameter {self.parameter_name}: {self.parameter_value}>'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'parameter_name': self.parameter_name,
            'parameter_value': self.parameter_value,
            'numerical_value': self.numerical_value,
            'unit': self.unit,
            'parameter_type': self.parameter_type,
            'confidence': self.confidence,
            'source_text': self.source_text
        }

class ReferencedSection(db.Model):
    """Stores sections of documents referenced in analysis"""
    __tablename__ = 'referenced_sections'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), ForeignKey('analysis_sessions.session_id'), nullable=False)
    section_name = Column(String(200), nullable=False)
    section_details = Column(Text, nullable=False)
    relevance_score = Column(Float, nullable=True)  # How relevant this section was
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    session = relationship("AnalysisSession", back_populates="referenced_sections")
    
    def __repr__(self):
        return f'<ReferencedSection {self.section_name}>'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'section_name': self.section_name,
            'section_details': self.section_details,
            'relevance_score': self.relevance_score
        }

class ComponentType(db.Model):
    """Catalog of known component types and their typical parameters"""
    __tablename__ = 'component_types'
    
    id = Column(Integer, primary_key=True)
    type_name = Column(String(100), unique=True, nullable=False)  # PSU, LED_Strip, etc
    display_name = Column(String(100), nullable=False)  # Power Supply Unit
    description = Column(Text, nullable=True)
    typical_parameters = Column(JSON, nullable=True)  # List of expected parameter types
    validation_rules = Column(JSON, nullable=True)    # Validation rules for this component
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<ComponentType {self.type_name}: {self.display_name}>'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'type_name': self.type_name,
            'display_name': self.display_name,
            'description': self.description,
            'typical_parameters': self.typical_parameters,
            'validation_rules': self.validation_rules,
            'is_active': self.is_active
        }

class AnalysisTemplate(db.Model):
    """Pre-defined analysis templates for common compatibility checks"""
    __tablename__ = 'analysis_templates'
    
    id = Column(Integer, primary_key=True)
    template_name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    query_template = Column(Text, nullable=False)  # Template query string
    required_components = Column(JSON, nullable=False)  # List of required component types
    compatibility_rules = Column(JSON, nullable=True)  # Custom compatibility logic
    example_document = Column(Text, nullable=True)  # Example document for this template
    usage_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<AnalysisTemplate {self.template_name}>'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'template_name': self.template_name,
            'display_name': self.display_name,
            'description': self.description,
            'query_template': self.query_template,
            'required_components': self.required_components,
            'usage_count': self.usage_count,
            'is_active': self.is_active
        }

class UserPreference(db.Model):
    """User preferences and settings"""
    __tablename__ = 'user_preferences'
    
    id = Column(Integer, primary_key=True)
    user_session = Column(String(64), unique=True, nullable=False, index=True)  # Browser session ID
    analysis_history_enabled = Column(Boolean, default=True, nullable=False)
    auto_save_enabled = Column(Boolean, default=True, nullable=False)
    default_confidence_threshold = Column(Float, default=0.6, nullable=False)
    preferred_export_format = Column(String(20), default='json', nullable=False)  # json, csv, pdf
    ui_theme = Column(String(20), default='dark', nullable=False)  # dark, light
    keyboard_shortcuts_enabled = Column(Boolean, default=True, nullable=False)
    last_document_text = Column(Text, nullable=True)  # Auto-saved document
    last_query_text = Column(Text, nullable=True)    # Auto-saved query
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<UserPreference {self.user_session}>'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'user_session': self.user_session,
            'analysis_history_enabled': self.analysis_history_enabled,
            'auto_save_enabled': self.auto_save_enabled,
            'default_confidence_threshold': self.default_confidence_threshold,
            'preferred_export_format': self.preferred_export_format,
            'ui_theme': self.ui_theme,
            'keyboard_shortcuts_enabled': self.keyboard_shortcuts_enabled,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Database utility functions
def create_tables():
    """Create all database tables"""
    db.create_all()

def drop_tables():
    """Drop all database tables (for development/testing)"""
    db.drop_all()

def seed_default_data():
    """Seed database with default component types and analysis templates"""
    
    # Default component types
    component_types = [
        {
            'type_name': 'PSU',
            'display_name': 'Power Supply Unit',
            'description': 'DC or AC power supply units and adapters',
            'typical_parameters': ['output_voltage', 'max_current', 'input_voltage', 'efficiency', 'power_rating'],
            'validation_rules': {
                'output_voltage': {'min': 1, 'max': 1000, 'unit': 'V'},
                'max_current': {'min': 0.1, 'max': 1000, 'unit': 'A'}
            }
        },
        {
            'type_name': 'LED_STRIP',
            'display_name': 'LED Strip Light',
            'description': 'LED strips, modules, and lighting components',
            'typical_parameters': ['input_voltage', 'current_draw', 'power_consumption', 'color_temperature'],
            'validation_rules': {
                'input_voltage': {'min': 1, 'max': 100, 'unit': 'V'},
                'current_draw': {'min': 0.01, 'max': 100, 'unit': 'A'}
            }
        },
        {
            'type_name': 'ELECTRONIC_MODULE',
            'display_name': 'Electronic Module',
            'description': 'General electronic components and modules',
            'typical_parameters': ['operating_voltage', 'current_consumption', 'operating_temperature'],
            'validation_rules': {
                'operating_voltage': {'min': 1, 'max': 50, 'unit': 'V'}
            }
        }
    ]
    
    for ct_data in component_types:
        existing = ComponentType.query.filter_by(type_name=ct_data['type_name']).first()
        if not existing:
            ct = ComponentType(**ct_data)
            db.session.add(ct)
    
    # Default analysis templates
    analysis_templates = [
        {
            'template_name': 'PSU_LED_COMPATIBILITY',
            'display_name': 'PSU and LED Compatibility Check',
            'description': 'Check if a power supply can safely power LED components',
            'query_template': 'Check if the power supply is compatible with the LED component based on voltage and current requirements',
            'required_components': ['PSU', 'LED_STRIP'],
            'compatibility_rules': {
                'voltage_tolerance': 0.5,
                'current_safety_margin': 0.1,
                'required_checks': ['voltage_match', 'current_sufficient']
            },
            'example_document': '''Power Supply Unit Model: PSU-12V-5A
Output Voltage: 12V DC
Max Output Current: 5 Amps
Input: 100-240V AC

LED Strip Model: RGB-5M
Required Input Voltage: 12V DC
Current Draw: 4 Amps
Power: 48W'''
        },
        {
            'template_name': 'GENERAL_COMPONENT_ANALYSIS',
            'display_name': 'General Component Analysis',
            'description': 'Extract and analyze technical parameters from any component',
            'query_template': 'Extract all technical parameters and specifications from the provided component documentation',
            'required_components': [],
            'compatibility_rules': {},
            'example_document': '''Component Datasheet
Operating Voltage: 5V DC
Current Consumption: 100mA
Operating Temperature: -20°C to 85°C
Interface: I2C, SPI'''
        }
    ]
    
    for at_data in analysis_templates:
        existing = AnalysisTemplate.query.filter_by(template_name=at_data['template_name']).first()
        if not existing:
            at = AnalysisTemplate(**at_data)
            db.session.add(at)
    
    db.session.commit()
    print("Database seeded with default data")

def get_analysis_statistics() -> Dict[str, Any]:
    """Get analysis statistics for dashboard"""
    total_sessions = AnalysisSession.query.count()
    successful_sessions = AnalysisSession.query.filter_by(is_successful=True).count()
    total_parameters = ExtractedParameter.query.count()
    
    # Recent activity (last 7 days)
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_sessions = AnalysisSession.query.filter(AnalysisSession.created_at >= week_ago).count()
    
    # Most common decisions
    decision_stats = db.session.query(
        AnalysisSession.decision,
        db.func.count(AnalysisSession.decision)
    ).group_by(AnalysisSession.decision).all()
    
    return {
        'total_sessions': total_sessions,
        'successful_sessions': successful_sessions,
        'success_rate': (successful_sessions / total_sessions * 100) if total_sessions > 0 else 0,
        'total_parameters': total_parameters,
        'recent_sessions': recent_sessions,
        'decision_breakdown': dict(decision_stats),
        'average_parameters_per_session': (total_parameters / total_sessions) if total_sessions > 0 else 0
    }