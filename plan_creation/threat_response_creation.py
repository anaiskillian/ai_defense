import requests
import json
import os
from typing import Dict, List, Any
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langgraph.graph import StateGraph
from langgraph.checkpoint import MemorySaver
import langgraph as lg

# You can use open-source models like Llama 3 or OpenAI models
# For open source deployment, change this to use a local model
from langchain_community.llms import HuggingFaceHub

# Define the initial state structure
class AgentState(dict):
    """State for the threat response agent"""
    threat_data: Dict[str, Any]
    analysis: Dict[str, Any] = None
    response_plan: Dict[str, Any] = None
    recommendations: Dict[str, Dict[str, Any]] = None
    status: str = "initialized"

# Define the nodes of our agentic system
def threat_analyzer(state: AgentState) -> AgentState:
    """Analyze the detected threat and its implications"""
    llm = HuggingFaceHub(repo_id="meta-llama/Llama-3.1-8B-Instruct", 
                          huggingfacehub_api_token=os.environ["HF_TOKEN"])
    
    # Define the threat analysis prompt
    analysis_template = """
    You are a naval defense threat analysis system. Analyze the following detection data
    and provide a comprehensive threat assessment:
    
    DETECTION DATA:
    {detection_data}
    
    COORDINATES: {coordinates}
    ENVIRONMENT: {environment}
    
    Your analysis should include:
    1. Threat identification and classification
    2. Potential intentions of the detected object(s)
    3. Risk assessment to nearby assets (submarines, ships, undersea cables, etc.)
    4. Confidence level of your assessment
    5. Additional intelligence requirements
    
    FORMAT YOUR RESPONSE AS A JSON object with the following keys:
    - threat_type
    - threat_level 
    - risk_assessment
    - confidence_level
    - intelligence_gaps
    - situational_summary
    """
    
    analysis_prompt = PromptTemplate(
        template=analysis_template,
        input_variables=["detection_data", "coordinates", "environment"]
    )
    
    analysis_chain = LLMChain(llm=llm, prompt=analysis_prompt)
    
    # Extract relevant data from the state
    detection_data = state["threat_data"]["raw_description"]
    coordinates = json.dumps(state["threat_data"]["coordinates"])
    environment = json.dumps(state["threat_data"]["environment_conditions"])
    
    # Run the analysis
    analysis_result = analysis_chain.run(
        detection_data=detection_data,
        coordinates=coordinates,
        environment=environment
    )
    
    # Parse the result (assuming it's valid JSON)
    try:
        analysis_json = json.loads(analysis_result)
    except:
        # In case the LLM doesn't return valid JSON
        analysis_json = {
            "threat_type": "unknown",
            "threat_level": state["threat_data"]["threat_level"],
            "risk_assessment": "Could not analyze properly",
            "confidence_level": "low",
            "intelligence_gaps": ["complete analysis failed"],
            "situational_summary": analysis_result
        }
    
    # Update the state with the analysis
    state["analysis"] = analysis_json
    state["status"] = "analyzed"
    
    return state

def response_planner(state: AgentState) -> AgentState:
    """Generate response plans based on the threat analysis"""
    llm = HuggingFaceHub(repo_id="meta-llama/Llama-3.1-8B-Instruct", 
                          huggingfacehub_api_token=os.environ["HF_TOKEN"])
    
    # Define the response planning prompt
    response_template = """
    You are a naval defense strategic response system. Based on the following threat analysis,
    develop a comprehensive response plan:
    
    THREAT ANALYSIS:
    {analysis}
    
    RAW DETECTION DATA:
    {detection_data}
    
    COORDINATES: {coordinates}
    
    Your response plan should include:
    1. Immediate actions to be taken by the monitoring drone
    2. Secondary deployment recommendations (additional drones, vessels, etc.)
    3. Communication protocols and information sharing requirements
    4. Escalation thresholds and conditions
    5. Timeline for implementation
    
    FORMAT YOUR RESPONSE AS A JSON object with the following keys:
    - drone_actions (list of specific actions for the monitoring drone)
    - secondary_deployments (list of recommended additional resources)
    - communication_protocols (specific communication recommendations)
    - escalation_conditions (when to escalate the response)
    - timeline (timeframes for different actions)
    - priority_level (numerical 1-5, with 5 being highest)
    """
    
    response_prompt = PromptTemplate(
        template=response_template,
        input_variables=["analysis", "detection_data", "coordinates"]
    )
    
    response_chain = LLMChain(llm=llm, prompt=response_prompt)
    
    # Run the response planning
    response_result = response_chain.run(
        analysis=json.dumps(state["analysis"]),
        detection_data=state["threat_data"]["raw_description"],
        coordinates=json.dumps(state["threat_data"]["coordinates"])
    )
    
    # Parse the result
    try:
        response_json = json.loads(response_result)
    except:
        # Fallback if parsing fails
        response_json = {
            "drone_actions": ["Maintain surveillance", "Collect additional data"],
            "secondary_deployments": ["None specified"],
            "communication_protocols": ["Standard reporting"],
            "escalation_conditions": ["Significant change in threat behavior"],
            "timeline": "Immediate drone actions, reassess in 30 minutes",
            "priority_level": 3
        }
    
    # Update the state
    state["response_plan"] = response_json
    state["status"] = "response_planned"
    
    return state

def agency_recommendations(state: AgentState) -> AgentState:
    """Generate agency-specific recommendations"""
    llm = HuggingFaceHub(repo_id="meta-llama/Llama-3.1-8B-Instruct", 
                          huggingfacehub_api_token=os.environ["HF_TOKEN"])
    
    # Define the agency recommendations prompt
    recommendations_template = """
    You are a defense intelligence coordination system. Based on the following threat analysis and response plan,
    provide specific recommendations for relevant US government agencies:
    
    THREAT ANALYSIS:
    {analysis}
    
    RESPONSE PLAN:
    {response_plan}
    
    RAW DETECTION DATA:
    {detection_data}
    
    Generate specific, actionable recommendations for each of these agencies that might need to be involved:
    - US Navy
    - Coast Guard
    - ICE (Immigration and Customs Enforcement)
    - FBI
    - DHS (Department of Homeland Security)
    - NMIO (National Maritime Intelligence-Integration Office)
    
    For each relevant agency, determine if they should be notified based on the threat context.
    Only include agencies that should be involved given the specific threat.
    
    FORMAT YOUR RESPONSE AS A JSON object with agency names as keys and for each agency include:
    - notify (boolean indicating if they should be notified)
    - priority (1-5 with 5 being highest)
    - recommended_actions (list of specific actions for this agency)
    - intelligence_sharing (what information should be shared with this agency)
    - coordination (how this agency should coordinate with others)
    """
    
    recommendations_prompt = PromptTemplate(
        template=recommendations_template,
        input_variables=["analysis", "response_plan", "detection_data"]
    )
    
    recommendations_chain = LLMChain(llm=llm, prompt=recommendations_prompt)
    
    # Run the recommendations generation
    rec_result = recommendations_chain.run(
        analysis=json.dumps(state["analysis"]),
        response_plan=json.dumps(state["response_plan"]),
        detection_data=state["threat_data"]["raw_description"]
    )
    
    # Parse the result
    try:
        rec_json = json.loads(rec_result)
    except:
        # Fallback if parsing fails
        rec_json = {
            "US Navy": {
                "notify": True,
                "priority": 4,
                "recommended_actions": ["Monitor situation", "Standby for deployment if needed"],
                "intelligence_sharing": "Full detection data and analysis",
                "coordination": "Lead maritime response coordination"
            }
        }
    
    # Update the state
    state["recommendations"] = rec_json
    state["status"] = "completed"
    
    return state

# Define the agentic workflow
def build_agent_workflow():
    """Build and return the agent workflow graph"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("threat_analyzer", threat_analyzer)
    workflow.add_node("response_planner", response_planner) 
    workflow.add_node("agency_recommendations", agency_recommendations)
    
    # Define edges
    workflow.add_edge("threat_analyzer", "response_planner")
    workflow.add_edge("response_planner", "agency_recommendations")
    
    # Set entry point
    workflow.set_entry_point("threat_analyzer")
    
    # Compile the workflow
    return workflow.compile()

# Function to process a new threat detection
def process_threat_detection(detection_data: Dict[str, Any]):
    """Process a detection and run it through the agent workflow"""
    # Initialize the state
    initial_state = AgentState(
        threat_data=detection_data,
        status="initialized"
    )
    
    # Build the workflow
    agent_workflow = build_agent_workflow()
    
    # Run the workflow with checkpointing
    memory_saver = MemorySaver()
    for output in agent_workflow.stream(initial_state, config={"checkpointer": memory_saver}):
        pass
    
    # Return the final state
    return output

# Function to connect to the detection service
def fetch_and_process_detections(detection_service_url: str = "http://localhost:8000"):
    """Poll the detection service and process any new threats"""
    # In a real implementation, this would either:
    # 1. Subscribe to a message queue where detections are published
    # 2. Poll an endpoint periodically
    # Here we show a simplified polling approach
    
    try:
        response = requests.get(f"{detection_service_url}/latest_detections")
        if response.status_code == 200:
            detections = response.json()
            
            for detection in detections:
                # Process each detection
                result = process_threat_detection(detection)
                
                # Submit results to relevant systems
                # In real implementation, this might trigger alerts, update dashboards, etc.
                print(f"Processed threat: {result}")
                
                # Example: Send high-priority threats to a special endpoint
                if result["analysis"]["threat_level"] in ["high", "critical"]:
                    requests.post(
                        f"{detection_service_url}/high_priority_alert",
                        json=result
                    )
    
    except Exception as e:
        print(f"Error processing detections: {e}")

# API endpoint to directly process a detection
def analyze_detection_api(detection_data: Dict[str, Any]) -> Dict[str, Any]:
    """API function to analyze a detection directly"""
    return process_threat_detection(detection_data)

if __name__ == "__main__":
    # This would typically run in a loop or be triggered by events
    import time
    while True:
        fetch_and_process_detections()
        time.sleep(60)  # Poll every minute
