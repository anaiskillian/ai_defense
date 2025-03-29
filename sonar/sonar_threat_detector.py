import joblib
import pandas as pd
import numpy as np
import json
import time
import requests
from pathlib import Path

def load_model():
    """Load the trained SVM model"""
    model_path = Path(__file__).parent / 'svm_model.pkl'
    return joblib.load(model_path)

def process_sonar_data(data_path):
    """Process sonar data and detect threats"""
    # Load the model
    model = load_model()
    
    # Read and process sonar data
    df = pd.read_csv(data_path, header=None)
    X = df.iloc[:, :-1]  # All columns except the last one
    
    # Make predictions
    predictions = model.predict(X)
    
    # Process each prediction
    threats = []
    for idx, pred in enumerate(predictions):
        if pred == 'M':  # If prediction is Mine
            threat_data = {
                "type": "underwater_threat",
                "timestamp": time.time(),
                "location": {
                    "type": "maritime_zone",
                    "coordinates": {"lat": 25.8371, "lon": -97.4023},  # Example coordinates
                    "area": "Southern Maritime Border Zone"
                },
                "detection": {
                    "type": "mine",
                    "confidence": float(model.decision_function([X.iloc[idx]])[0]),
                    "sonar_signature": X.iloc[idx].tolist()
                },
                "metadata": {
                    "detection_method": "sonar",
                    "sensor_type": "active_sonar",
                    "processing_timestamp": time.time()
                }
            }
            threats.append(threat_data)
    
    return threats

def send_threats_to_response_system(threats):
    """Send detected threats to the threat response system"""
    if not threats:
        print("No threats detected")
        return
    
    print(f"\nDetected {len(threats)} potential underwater threats")
    
    # Write threats to a file that threat_response_creation.py can read
    output_path = Path(__file__).parent.parent / 'plan_creation' / 'sonar_detections.json'
    with open(output_path, 'w') as f:
        json.dump({"detections": threats}, f, indent=2)
    
    print(f"Saved threat detections to {output_path}")
    print("Run threat_response_creation.py with --mock flag to process these threats")

def main():
    """Main function to process sonar data and detect threats"""
    data_path = Path(__file__).parent / 'sonar.csv'
    
    print("Processing sonar data...")
    threats = process_sonar_data(data_path)
    send_threats_to_response_system(threats)

if __name__ == "__main__":
    main()
