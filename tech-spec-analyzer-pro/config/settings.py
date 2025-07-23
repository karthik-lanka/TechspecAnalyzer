"""
Application Configuration Settings
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get("SESSION_SECRET", "dev-secret-key-tech-spec-analyzer-pro")
    DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    
    # Analysis settings
    MAX_DOCUMENT_SIZE = 1024 * 1024  # 1MB max document size
    MAX_PARAMETERS_EXTRACTED = 50    # Maximum parameters to extract
    CONFIDENCE_THRESHOLD = 0.6       # Minimum confidence for parameter acceptance
    
    # Parameter extraction settings
    VOLTAGE_TOLERANCE = 0.5          # Voltage matching tolerance in volts
    CURRENT_SAFETY_MARGIN = 0.1      # Minimum current safety margin (10%)
    
    # UI settings
    DEFAULT_ANALYSIS_TIMEOUT = 30    # Analysis timeout in seconds
    AUTO_SAVE_INTERVAL = 5           # Auto-save interval in seconds
    
    # Feature flags
    ENABLE_ADVANCED_AI = True
    ENABLE_EXPORT_FEATURES = True
    ENABLE_REAL_TIME_VALIDATION = True
    
    @classmethod
    def get_analysis_config(cls) -> Dict[str, Any]:
        """Get analysis-specific configuration"""
        return {
            "max_document_size": cls.MAX_DOCUMENT_SIZE,
            "max_parameters": cls.MAX_PARAMETERS_EXTRACTED,
            "confidence_threshold": cls.CONFIDENCE_THRESHOLD,
            "voltage_tolerance": cls.VOLTAGE_TOLERANCE,
            "current_safety_margin": cls.CURRENT_SAFETY_MARGIN,
            "timeout": cls.DEFAULT_ANALYSIS_TIMEOUT
        }

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    ENABLE_ADVANCED_AI = True

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get("SESSION_SECRET")
    if not SECRET_KEY:
        raise ValueError("SESSION_SECRET environment variable must be set in production")

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    MAX_DOCUMENT_SIZE = 512 * 1024  # Smaller for testing

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration class based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config_map.get(config_name, DevelopmentConfig)