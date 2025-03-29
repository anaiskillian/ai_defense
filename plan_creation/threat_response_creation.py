import json
import os
import time
import argparse
from dotenv import load_dotenv
from typing import Dict, List, Any
import subprocess
from pathlib import Path

def call_llama_model(prompt: str) -> str:
    """Call the Llama model using the main function from llama_modal.py"""
    print(f"Calling Llama model with prompt...")
    try:
        # Call the main function from llama_modal.py with the prompt
        result = subprocess.run(
            ["python", str(Path(__file__).parent.parent / "llama_modal.py"), "--prompt", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract the response from the output
        output_lines = result.stdout.strip().split('\n')
        response_line = ""
        for line in output_lines:
            if line.startswith("Response:"):
                response_line = line[len("Response:"):].strip()
                break
        
        print(f"Received response from Llama model")
        return response_line
    except subprocess.CalledProcessError as e:
        print(f"Error calling Llama model: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return f"Error: {e}"

def format_threat_prompt(detection_data: Dict[str, Any]) -> str:
    """Format detection data into a prompt for the Llama model"""
    prompt = f"""You are a naval defense threat analysis system. Format your response as JSON with the following structure:
{{
    "threat_analysis": {{
        "type": "string",
        "severity": "low|medium|high",
        "confidence": "float between 0-1",
        "details": "string"
    }},
    "agency_actions": {{
        "border_patrol": ["action1", "action2"],
        "coast_guard": ["action1", "action2"],
        "law_enforcement": ["action1", "action2"],
        "emergency_response": ["action1", "action2"]
    }}
}}

DETECTION DATA:
{json.dumps(detection_data, indent=2)}

Based on this information, analyze the threat and propose immediate actions for each agency."""
    
    return prompt

def parse_llm_response(response: str) -> Dict[str, Any]:
    """Parse the response from the Llama model"""
    try:
        json_response = json.loads(response)
        return json_response
    except json.JSONDecodeError:
        print("Warning: Response not valid JSON. Attempting to extract JSON...")
        # Try to extract JSON from text response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start >= 0 and json_end > 0:
            try:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            except json.JSONDecodeError:
                print("Failed to extract valid JSON")
        
        # Return a structured error response
        return {
            "threat_analysis": {
                "type": "error",
                "severity": "unknown",
                "confidence": 0,
                "details": "Failed to parse response"
            },
            "agency_actions": {}
        }

def process_threat_detection(detection_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a detection and generate a threat response"""
    print("\nAnalyzing threat...")
    
    # Format the prompt
    prompt = format_threat_prompt(detection_data)
    
    # Call the Llama model
    response = call_llama_model(prompt)
    
    # Parse the response
    analysis = parse_llm_response(response)
    
    # Extract threat level
    threat_level = analysis.get("threat_analysis", {}).get("severity", "low")
    
    # Format the response
    result = {
        "threat_level": threat_level,
        "detection": {
            "type": detection_data.get("type", "Unknown"),
            "timestamp": detection_data.get("timestamp", time.time()),
            "location": detection_data.get("location", {})
        },
        "analysis": analysis
    }
    
    print("\nThreat Response Summary:")
    print(json.dumps(result, indent=2))
    return result

def poll_detection_service(mock_mode: bool) -> List[Dict[str, Any]]:
    """Poll for new threat detections"""
    if mock_mode:
        print("Running in mock mode. Loading data from mock_detections.json")
        try:
            with open("plan_creation/mock_detections.json", "r") as f:
                detections = json.load(f)
        except FileNotFoundError:
            print("Error: mock_detections.json not found")
            return []
        
        responses = []
        for detection in detections:
            print(f"Processing detection: {detection.get('type', 'Unknown')}")
            response = process_threat_detection(detection)
            responses.append(response)
            
        return responses
    else:
        # Try to load video detection data
        try:
            video_file = "plan_creation/YouTube Video Qpfrs2kNbAE 720x1280_detections.json"
            print(f"Looking for video file at: {video_file}")
            
            with open(video_file, "r") as f:
                video_data = json.load(f)
                unique_objects = video_data["unique_objects"]
                print(f"Found video data with objects: {unique_objects}")
                
                # Create video surveillance detection without pre-defined threat assessment
                detection = {
                    "type": "video_surveillance",
                    "timestamp": time.time(),
                    "location": {
                        "type": "border_zone",
                        "coordinates": {"lat": 25.8371, "lon": -97.4023},
                        "area": "Southern Border Maritime Zone"
                    },
                    "detections": {
                        "persons": unique_objects.get("person", 0),
                        "vehicles": {
                            "land": {
                                "trucks": unique_objects.get("truck", 0),
                                "cars": unique_objects.get("car", 0)
                            },
                            "water": {
                                "boats": unique_objects.get("boat", 0)
                            }
                        },
                        "other": {k: v for k, v in unique_objects.items() 
                                if k not in ["person", "truck", "car", "boat"]}
                    },
                    "video_metadata": video_data["video_info"]
                }
                print("Processing video surveillance data...")
                response = process_threat_detection(detection)
                return [response]
                
        except FileNotFoundError as e:
            print(f"Error: Video detection file not found - {e}")
        except KeyError as e:
            print(f"Error: Invalid video detection format - {e}")
        except Exception as e:
            print(f"Error processing video data: {e}")
        
        # If video detection didn't work, try sonar detections
        try:
            with open("plan_creation/sonar_detections.json", "r") as f:
                sonar_data = json.load(f)
                detections = sonar_data.get("detections", [])
                
                responses = []
                for detection in detections:
                    print(f"Processing sonar detection...")
                    response = process_threat_detection(detection)
                    responses.append(response)
                
                return responses
                
        except FileNotFoundError as e:
            print(f"Error: Sonar detection file not found - {e}")
        except Exception as e:
            print(f"Error processing sonar data: {e}")
        
        print("No detection data found.")
        return []

def main(mock_mode: bool = False):
    """Main function to run the threat response agent"""
    print("Starting Threat Response Agent...")
    print("Polling for new detections...")
    
    # Poll for detections
    responses = poll_detection_service(mock_mode)
    
    if not responses:
        print("No detections found.")
    
    # Save responses to a file
    if responses:
        output_file = "plan_creation/threat_responses.json"
        with open(output_file, "w") as f:
            json.dump(responses, f, indent=2)
        print(f"Saved threat responses to {output_file}")

if __name__ == "__main__":
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Run the threat response agent')
    parser.add_argument('--mock', action='store_true', help='Run with mock data')
    args = parser.parse_args()
    
    main(mock_mode=args.mock)