"""
Advanced AI-powered parameter extraction module for technical documents.
Handles complex pattern matching and parameter validation.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class ParameterType(Enum):
    VOLTAGE = "voltage"
    CURRENT = "current"
    POWER = "power"
    TEMPERATURE = "temperature"
    FREQUENCY = "frequency"
    DIMENSION = "dimension"

@dataclass
class ExtractedParameter:
    name: str
    value: str
    numerical_value: Optional[float]
    unit: str
    confidence: float
    source_text: str
    parameter_type: ParameterType

class TechnicalParameterExtractor:
    """Advanced parameter extraction engine with AI-like pattern recognition."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.extraction_patterns = self._initialize_patterns()
        
    def _initialize_patterns(self) -> Dict[ParameterType, List[Dict[str, Any]]]:
        """Initialize comprehensive regex patterns for different parameter types."""
        return {
            ParameterType.VOLTAGE: [
                {
                    "patterns": [
                        r"(?:Output|Input|Supply|Operating|Required)\s+Voltage:\s*([0-9]+(?:\.[0-9]+)?\s*V(?:\s*(?:DC|AC))?)",
                        r"Voltage\s+(?:Output|Input|Supply|Rating):\s*([0-9]+(?:\.[0-9]+)?\s*V(?:\s*(?:DC|AC))?)",
                        r"([0-9]+(?:\.[0-9]+)?\s*V\s*(?:DC|AC))\s+(?:output|input|supply)",
                        r"V(?:out|in|supply|dd|cc):\s*([0-9]+(?:\.[0-9]+)?\s*V)"
                    ],
                    "unit_patterns": [r"(V(?:olts?)?(?:\s*(?:DC|AC))?)", r"(V)"],
                    "confidence_boost": 0.1
                }
            ],
            ParameterType.CURRENT: [
                {
                    "patterns": [
                        r"(?:Max|Maximum|Output|Input|Draw|Consumption)\s+Current:\s*([0-9]+(?:\.[0-9]+)?\s*(?:A|Amps?|mA))",
                        r"Current\s+(?:Draw|Rating|Consumption|Output|Input):\s*([0-9]+(?:\.[0-9]+)?\s*(?:A|Amps?|mA))",
                        r"([0-9]+(?:\.[0-9]+)?\s*(?:A|Amps?|mA))\s+(?:current|draw|consumption)",
                        r"I(?:out|in|max):\s*([0-9]+(?:\.[0-9]+)?\s*(?:A|Amps?|mA))"
                    ],
                    "unit_patterns": [r"(A|Amps?|mA|Amperes?)", r"(A)"],
                    "confidence_boost": 0.1
                }
            ],
            ParameterType.POWER: [
                {
                    "patterns": [
                        r"(?:Max|Maximum|Output|Input|Rated)\s+Power:\s*([0-9]+(?:\.[0-9]+)?\s*(?:W|Watts?))",
                        r"Power\s+(?:Rating|Consumption|Output|Input):\s*([0-9]+(?:\.[0-9]+)?\s*(?:W|Watts?))",
                        r"([0-9]+(?:\.[0-9]+)?\s*(?:W|Watts?))\s+(?:power|consumption)"
                    ],
                    "unit_patterns": [r"(W|Watts?)", r"(W)"],
                    "confidence_boost": 0.05
                }
            ],
            ParameterType.TEMPERATURE: [
                {
                    "patterns": [
                        r"Operating\s+Temperature:\s*([0-9-]+°?C?\s*to\s*[0-9]+°?C?)",
                        r"Temperature\s+Range:\s*([0-9-]+°?C?\s*to\s*[0-9]+°?C?)",
                        r"Temp\.?\s*Range:\s*([0-9-]+°?C?\s*to\s*[0-9]+°?C?)"
                    ],
                    "unit_patterns": [r"(°C|Celsius)", r"(°C)"],
                    "confidence_boost": 0.05
                }
            ],
            ParameterType.FREQUENCY: [
                {
                    "patterns": [
                        r"Frequency:\s*([0-9]+(?:\.[0-9]+)?\s*(?:Hz|KHz|MHz|GHz))",
                        r"([0-9]+(?:\.[0-9]+)?\s*(?:Hz|KHz|MHz|GHz))\s+frequency"
                    ],
                    "unit_patterns": [r"(Hz|KHz|MHz|GHz)", r"(Hz)"],
                    "confidence_boost": 0.05
                }
            ]
        }
    
    def extract_all_parameters(self, document_text: str) -> List[ExtractedParameter]:
        """Extract all technical parameters from document text."""
        all_parameters = []
        
        for param_type, pattern_groups in self.extraction_patterns.items():
            for pattern_group in pattern_groups:
                parameters = self._extract_parameter_type(
                    document_text, param_type, pattern_group
                )
                all_parameters.extend(parameters)
        
        return self._deduplicate_parameters(all_parameters)
    
    def _extract_parameter_type(self, text: str, param_type: ParameterType, 
                               pattern_group: Dict[str, Any]) -> List[ExtractedParameter]:
        """Extract parameters of a specific type using pattern group."""
        parameters = []
        
        for pattern in pattern_group["patterns"]:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                param_value = match.group(1).strip()
                numerical_value = self._extract_numerical_value(param_value)
                unit = self._extract_unit(param_value, pattern_group["unit_patterns"])
                
                # Calculate confidence based on pattern specificity and context
                confidence = self._calculate_confidence(
                    match, text, pattern_group.get("confidence_boost", 0)
                )
                
                parameter = ExtractedParameter(
                    name=f"{param_type.value}_{len(parameters)}",
                    value=param_value,
                    numerical_value=numerical_value,
                    unit=unit,
                    confidence=confidence,
                    source_text=match.group(0),
                    parameter_type=param_type
                )
                
                parameters.append(parameter)
        
        return parameters
    
    def _extract_numerical_value(self, text: str) -> Optional[float]:
        """Extract numerical value from parameter string."""
        if not text:
            return None
        
        # Handle ranges (take the first value)
        range_match = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*(?:to|-)\s*[0-9]+', text)
        if range_match:
            return float(range_match.group(1))
        
        # Handle single values
        match = re.search(r'([0-9]+(?:\.[0-9]+)?)', text)
        return float(match.group(1)) if match else None
    
    def _extract_unit(self, text: str, unit_patterns: List[str]) -> str:
        """Extract unit from parameter string."""
        for pattern in unit_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return ""
    
    def _calculate_confidence(self, match: re.Match, full_text: str, boost: float) -> float:
        """Calculate confidence score for extracted parameter."""
        base_confidence = 0.6
        
        # Boost confidence if parameter is in a structured section
        context_start = max(0, match.start() - 100)
        context_end = min(len(full_text), match.end() + 100)
        context = full_text[context_start:context_end]
        
        # Look for structured indicators
        if re.search(r'(?:datasheet|specification|spec|technical)', context, re.IGNORECASE):
            base_confidence += 0.15
        
        if re.search(r'(?:\d+\.|\*|\-|\|)', context):
            base_confidence += 0.1
        
        # Pattern specificity boost
        base_confidence += boost
        
        return min(1.0, base_confidence)
    
    def _deduplicate_parameters(self, parameters: List[ExtractedParameter]) -> List[ExtractedParameter]:
        """Remove duplicate parameters, keeping the one with highest confidence."""
        seen_values = {}
        
        for param in parameters:
            key = (param.parameter_type, param.numerical_value, param.unit.lower())
            
            if key not in seen_values or param.confidence > seen_values[key].confidence:
                seen_values[key] = param
        
        return list(seen_values.values())
    
    def find_psu_led_parameters(self, document_text: str) -> Dict[str, Any]:
        """Specialized extraction for PSU and LED compatibility analysis."""
        all_params = self.extract_all_parameters(document_text)
        
        # Categorize parameters for PSU/LED analysis
        psu_voltage = None
        psu_current = None
        led_voltage = None
        led_current = None
        
        for param in all_params:
            if param.parameter_type == ParameterType.VOLTAGE:
                if self._is_psu_parameter(param.source_text):
                    if not psu_voltage or param.confidence > psu_voltage.confidence:
                        psu_voltage = param
                elif self._is_led_parameter(param.source_text):
                    if not led_voltage or param.confidence > led_voltage.confidence:
                        led_voltage = param
            
            elif param.parameter_type == ParameterType.CURRENT:
                if self._is_psu_parameter(param.source_text):
                    if not psu_current or param.confidence > psu_current.confidence:
                        psu_current = param
                elif self._is_led_parameter(param.source_text):
                    if not led_current or param.confidence > led_current.confidence:
                        led_current = param
        
        return {
            "psu_voltage": psu_voltage,
            "psu_current": psu_current,
            "led_voltage": led_voltage,
            "led_current": led_current,
            "all_parameters": all_params
        }
    
    def _is_psu_parameter(self, source_text: str) -> bool:
        """Determine if parameter belongs to PSU based on context."""
        psu_indicators = [
            "power supply", "psu", "adapter", "charger", "output", "supply unit"
        ]
        return any(indicator in source_text.lower() for indicator in psu_indicators)
    
    def _is_led_parameter(self, source_text: str) -> bool:
        """Determine if parameter belongs to LED based on context."""
        led_indicators = [
            "led", "strip", "light", "lamp", "input", "required", "consumption", "draw"
        ]
        return any(indicator in source_text.lower() for indicator in led_indicators)

class CompatibilityAnalyzer:
    """Advanced compatibility analysis with detailed reporting."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_psu_led_compatibility(self, psu_voltage: Optional[ExtractedParameter],
                                    psu_current: Optional[ExtractedParameter],
                                    led_voltage: Optional[ExtractedParameter],
                                    led_current: Optional[ExtractedParameter]) -> Dict[str, Any]:
        """Perform comprehensive PSU-LED compatibility analysis."""
        
        if not all([psu_voltage, psu_current, led_voltage, led_current]):
            missing = []
            if not psu_voltage: missing.append("PSU voltage")
            if not psu_current: missing.append("PSU current")
            if not led_voltage: missing.append("LED voltage")
            if not led_current: missing.append("LED current")
            
            return {
                "compatible": False,
                "decision": "Insufficient Data",
                "confidence": "Low",
                "missing_parameters": missing,
                "analysis_details": "Cannot perform analysis without all required parameters"
            }
        
        # Voltage compatibility check
        voltage_compatible = self._check_voltage_compatibility(
            psu_voltage.numerical_value, led_voltage.numerical_value
        )
        
        # Current compatibility check
        current_compatible = self._check_current_compatibility(
            psu_current.numerical_value, led_current.numerical_value
        )
        
        overall_compatible = voltage_compatible["compatible"] and current_compatible["compatible"]
        
        # Calculate overall confidence
        confidence_score = min(
            psu_voltage.confidence, psu_current.confidence,
            led_voltage.confidence, led_current.confidence
        )
        
        confidence_level = "High" if confidence_score > 0.8 else "Medium" if confidence_score > 0.6 else "Low"
        
        return {
            "compatible": overall_compatible,
            "decision": "Compatible" if overall_compatible else "Incompatible",
            "confidence": confidence_level,
            "confidence_score": confidence_score,
            "voltage_analysis": voltage_compatible,
            "current_analysis": current_compatible,
            "parameter_confidence": {
                "psu_voltage": psu_voltage.confidence,
                "psu_current": psu_current.confidence,
                "led_voltage": led_voltage.confidence,
                "led_current": led_current.confidence
            },
            "analysis_details": self._generate_detailed_analysis(
                voltage_compatible, current_compatible, overall_compatible
            )
        }
    
    def _check_voltage_compatibility(self, psu_voltage: float, led_voltage: float) -> Dict[str, Any]:
        """Check voltage compatibility with tolerance."""
        tolerance = 0.5  # 0.5V tolerance
        difference = abs(psu_voltage - led_voltage)
        compatible = difference <= tolerance
        
        return {
            "compatible": compatible,
            "psu_voltage": psu_voltage,
            "led_voltage": led_voltage,
            "difference": difference,
            "tolerance": tolerance,
            "analysis": f"PSU provides {psu_voltage}V, LED requires {led_voltage}V (diff: {difference:.1f}V)"
        }
    
    def _check_current_compatibility(self, psu_current: float, led_current: float) -> Dict[str, Any]:
        """Check current compatibility (PSU must provide at least LED requirement)."""
        compatible = psu_current >= led_current
        safety_margin = (psu_current - led_current) / led_current if led_current > 0 else 0
        
        return {
            "compatible": compatible,
            "psu_current": psu_current,
            "led_current": led_current,
            "safety_margin": safety_margin,
            "margin_percentage": safety_margin * 100,
            "analysis": f"PSU provides {psu_current}A, LED draws {led_current}A (margin: {safety_margin*100:.1f}%)"
        }
    
    def _generate_detailed_analysis(self, voltage_analysis: Dict, current_analysis: Dict, 
                                  overall_compatible: bool) -> str:
        """Generate detailed human-readable analysis."""
        analysis_parts = []
        
        if voltage_analysis["compatible"]:
            analysis_parts.append(f"✓ Voltage match: {voltage_analysis['analysis']}")
        else:
            analysis_parts.append(f"✗ Voltage mismatch: {voltage_analysis['analysis']}")
        
        if current_analysis["compatible"]:
            analysis_parts.append(f"✓ Current sufficient: {current_analysis['analysis']}")
        else:
            analysis_parts.append(f"✗ Current insufficient: {current_analysis['analysis']}")
        
        conclusion = "Components are compatible" if overall_compatible else "Components are not compatible"
        analysis_parts.append(f"\nConclusion: {conclusion}")
        
        return ". ".join(analysis_parts)