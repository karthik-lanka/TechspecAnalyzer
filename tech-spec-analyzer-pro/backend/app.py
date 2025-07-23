from flask import Flask, render_template, request, jsonify
import re
import os
import logging
from typing import Optional, Dict, List, Any

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, 
           template_folder='../frontend/templates',
           static_folder='../frontend/static')
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-for-tech-analyzer")

def extract_parameter(text: str, patterns: List[str]) -> Optional[str]:
    """Extracts a parameter from text using a list of regex patterns."""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def extract_numerical_value(text: str) -> Optional[float]:
    """Extracts numerical value from a parameter string."""
    if not text:
        return None
    match = re.search(r'(\d+(?:\.\d+)?)', text)
    return float(match.group(1)) if match else None

def analyze_compatibility(psu_voltage: Optional[float], psu_current: Optional[float], 
                         led_voltage: Optional[float], led_current: Optional[float]) -> Dict[str, Any]:
    """Analyzes compatibility between PSU and LED based on extracted parameters."""
    if None in [psu_voltage, psu_current, led_voltage, led_current]:
        return {
            "compatible": False,
            "reason": "Missing parameter values",
            "voltage_match": False,
            "current_sufficient": False
        }
    
    # Type check to ensure all values are not None
    if not all(isinstance(val, (int, float)) for val in [psu_voltage, psu_current, led_voltage, led_current]):
        return {
            "compatible": False,
            "reason": "Invalid parameter types",
            "voltage_match": False,
            "current_sufficient": False
        }
    
    voltage_match = abs(psu_voltage - led_voltage) < 0.1  # Allow small tolerance
    current_sufficient = psu_current >= led_current
    
    return {
        "compatible": voltage_match and current_sufficient,
        "reason": "Compatible" if voltage_match and current_sufficient else "Incompatible",
        "voltage_match": voltage_match,
        "current_sufficient": current_sufficient
    }

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyzes the provided document and query."""
    try:
        data = request.get_json()
        document_text = data.get('document_text', '')
        user_query = data.get('user_query', '')
        
        app.logger.debug(f"Analyzing document of length {len(document_text)}")
        app.logger.debug(f"User query: {user_query}")
        
        # Enhanced regex patterns for better parameter extraction
        psu_output_voltage_patterns = [
            r"Output Voltage:\s*([0-9]+\s*V\s*DC)",
            r"Output:\s*([0-9]+\s*V\s*DC)",
            r"DC Output:\s*([0-9]+\s*V)",
            r"Voltage Output:\s*([0-9]+\s*V)"
        ]
        
        psu_max_current_patterns = [
            r"Max Output Current:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Maximum Current:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Output Current:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Current Rating:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)"
        ]
        
        led_input_voltage_patterns = [
            r"Required Input Voltage:\s*([0-9]+\s*V\s*DC)",
            r"Input Voltage:\s*([0-9]+\s*V\s*DC)",
            r"Operating Voltage:\s*([0-9]+\s*V\s*DC)",
            r"Supply Voltage:\s*([0-9]+\s*V\s*DC)"
        ]
        
        led_current_draw_patterns = [
            r"Current Draw:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Power Consumption:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Current Requirement:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Current Usage:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)"
        ]
        
        # Extract parameters
        psu_voltage_str = extract_parameter(document_text, psu_output_voltage_patterns)
        psu_current_str = extract_parameter(document_text, psu_max_current_patterns)
        led_voltage_str = extract_parameter(document_text, led_input_voltage_patterns)
        led_current_str = extract_parameter(document_text, led_current_draw_patterns)
        
        app.logger.debug(f"Extracted PSU voltage: {psu_voltage_str}")
        app.logger.debug(f"Extracted PSU current: {psu_current_str}")
        app.logger.debug(f"Extracted LED voltage: {led_voltage_str}")
        app.logger.debug(f"Extracted LED current: {led_current_str}")
        
        extracted_data = {
            "PSU_Output_Voltage": psu_voltage_str or "Not Found",
            "PSU_Max_Output_Current": psu_current_str or "Not Found",
            "LED_Required_Voltage": led_voltage_str or "Not Found",
            "LED_Current_Draw": led_current_str or "Not Found"
        }
        
        # Initialize response variables
        decision = "Not Explicitly Covered"
        justification = "Could not determine compatibility. One or more required parameters were not found in the document."
        confidence = "Low"
        referenced_sections = []
        
        # Check if all required parameters were found
        all_params_found = all([psu_voltage_str, psu_current_str, led_voltage_str, led_current_str])
        
        if all_params_found:
            try:
                # Extract numerical values
                psu_voltage_val = extract_numerical_value(psu_voltage_str)
                psu_current_val = extract_numerical_value(psu_current_str)
                led_voltage_val = extract_numerical_value(led_voltage_str)
                led_current_val = extract_numerical_value(led_current_str)
                
                app.logger.debug(f"Numerical values - PSU: {psu_voltage_val}V, {psu_current_val}A; LED: {led_voltage_val}V, {led_current_val}A")
                
                # Perform compatibility analysis
                compatibility_result = analyze_compatibility(psu_voltage_val, psu_current_val, led_voltage_val, led_current_val)
                
                if compatibility_result["compatible"]:
                    referenced_sections = [
                        {"section_name": "PSU - Output Voltage", "details": f"Output Voltage: {psu_voltage_str}"},
                        {"section_name": "PSU - Max Output Current", "details": f"Max Output Current: {psu_current_str}"},
                        {"section_name": "LED - Required Input Voltage", "details": f"Required Input Voltage: {led_voltage_str}"},
                        {"section_name": "LED - Current Draw", "details": f"Current Draw: {led_current_str}"}
                    ]
                    
                    if compatibility_result["voltage_match"] and compatibility_result["current_sufficient"]:
                        decision = "Compatible"
                        justification = (f"The Power Supply provides {psu_voltage_str}, which matches the LED's required {led_voltage_str}. "
                                       f"The PSU's max current of {psu_current_str} is sufficient to handle the LED's draw of {led_current_str}.")
                        confidence = "High"
                    else:
                        decision = "Incompatible"
                        justification_parts = []
                        if not compatibility_result["voltage_match"]:
                            justification_parts.append(f"Voltage mismatch: PSU provides {psu_voltage_str} but LED requires {led_voltage_str}.")
                        if not compatibility_result["current_sufficient"]:
                            justification_parts.append(f"Insufficient current: PSU provides a max of {psu_current_str} but LED requires {led_current_str}.")
                        justification = " ".join(justification_parts)
                        confidence = "High"
                else:
                    justification = "Found parameters but could not perform numerical analysis."
                    confidence = "Medium"
                    
            except Exception as e:
                app.logger.error(f"Error during numerical analysis: {e}")
                justification = "Found parameters but encountered an error during numerical analysis."
                confidence = "Low"
        
        # Construct final response
        response_data = {
            "Decision": decision,
            "Justification": justification,
            "Referenced_Sections": referenced_sections,
            "Extracted_Technical_Data": extracted_data,
            "Confidence_Score": confidence,
            "Analysis_Details": {
                "parameters_found": all_params_found,
                "extraction_success": bool(psu_voltage_str and psu_current_str and led_voltage_str and led_current_str)
            }
        }
        
        app.logger.debug(f"Analysis complete: {decision}")
        return jsonify(response_data)
        
    except Exception as e:
        app.logger.error(f"Error in analyze endpoint: {e}")
        return jsonify({
            "Decision": "Error",
            "Justification": f"An error occurred during analysis: {str(e)}",
            "Referenced_Sections": [],
            "Extracted_Technical_Data": {},
            "Confidence_Score": "Low",
            "Analysis_Details": {"error": str(e)}
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "healthy", "service": "Tech Spec Analyzer Pro"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)