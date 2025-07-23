from flask import Flask, render_template, request, jsonify
import re
import os
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-for-tech-analyzer")

def extract_parameter(text, patterns):
    """Extracts a parameter from text using a list of regex patterns."""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def extract_numerical_value(text):
    """Extracts numerical value from a parameter string."""
    if not text:
        return None
    match = re.search(r'(\d+(?:\.\d+)?)', text)
    return float(match.group(1)) if match else None

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
            r"DC Output:\s*([0-9]+\s*V)"
        ]
        
        psu_max_current_patterns = [
            r"Max Output Current:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Maximum Current:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Output Current:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)"
        ]
        
        led_input_voltage_patterns = [
            r"Required Input Voltage:\s*([0-9]+\s*V\s*DC)",
            r"Input Voltage:\s*([0-9]+\s*V\s*DC)",
            r"Operating Voltage:\s*([0-9]+\s*V\s*DC)"
        ]
        
        led_current_draw_patterns = [
            r"Current Draw:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Power Consumption:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)",
            r"Current Requirement:\s*([0-9]+(?:\.[0-9]+)?\s*Amps?)"
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
                
                if all([psu_voltage_val, psu_current_val, led_voltage_val, led_current_val]):
                    voltage_match = (psu_voltage_val == led_voltage_val)
                    current_sufficient = (psu_current_val >= led_current_val)
                    
                    referenced_sections = [
                        {"section_name": "PSU - Output Voltage", "details": f"Output Voltage: {psu_voltage_str}"},
                        {"section_name": "PSU - Max Output Current", "details": f"Max Output Current: {psu_current_str}"},
                        {"section_name": "LED - Required Input Voltage", "details": f"Required Input Voltage: {led_voltage_str}"},
                        {"section_name": "LED - Current Draw", "details": f"Current Draw: {led_current_str}"}
                    ]
                    
                    if voltage_match and current_sufficient:
                        decision = "Compatible"
                        justification = (f"The Power Supply provides {psu_voltage_str}, which matches the LED's required {led_voltage_str}. "
                                       f"The PSU's max current of {psu_current_str} is sufficient to handle the LED's draw of {led_current_str}.")
                        confidence = "High"
                    else:
                        decision = "Incompatible"
                        justification_parts = []
                        if not voltage_match:
                            justification_parts.append(f"Voltage mismatch: PSU provides {psu_voltage_str} but LED requires {led_voltage_str}.")
                        if not current_sufficient:
                            justification_parts.append(f"Insufficient current: PSU provides a max of {psu_current_str} but LED requires {led_current_str}.")
                        justification = " ".join(justification_parts)
                        confidence = "High"
                else:
                    justification = "Found parameters but could not parse numerical values to perform comparison."
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
            "Confidence_Score": confidence
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
            "Confidence_Score": "Low"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
