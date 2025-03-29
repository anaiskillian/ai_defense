# AI Defense Hackathon

## A real-time air-to-sea multi-modal drone sentry system for anomaly detection, object detection, and anti-submarine defense and deterrence

### Description: A sentry system that dispatches air-to-sea drones from a central submarine/naval carrier or other military base to monitor submarine routes, undersea communication cables, mine detection, mitigate illegal immigration, etc using AI agents. The system sends information back to the home base in real-time and uses an agentic system to plan emergency responses, actions, and give recommendations to the relevant agencies (ICE, US Navy, etc).

### Features:

#### Underwater Drone Coverage (Anaïs)
- **Sonar Capabilities (Mode 1)**
  - Collection and analysis of underwater sound signatures
  - Patrol-based monitoring using sonar and hydrophones

#### Navigation & Threat Prediction Engine (Divyam)
- **Camera System (Mode 2)**
  - Real-time aerial path planning
  - Threat score-based navigation

#### Active Defense & Deterrence System
- **Communication System**
  - Military base alert system for anomaly and attack detection
  - Real-time threat reporting
- **Counter-measures**
  - Drone-based sonar jamming through destructive interference

#### Frontend Interface (Divyam)
- **Monitoring Dashboard**
  - SONAR data visualization
  - Camera feed integration
- **Technology Stack**
  - React
  - Tailwind CSS
  - Windsurf integration


### Team Members:
- Anaïs Killian
- Divyam Jindal
- Rut Mehta
- Aryan Ghariwala

### Project Structure:




## Setup


### Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/anaiskillian/ai_defense.git
cd ai_defense
```

2. Set up Python virtual environment:
```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend
npm install
```

### Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn app.main:app --reload
```

2. In a new terminal, start the frontend development server:
```bash
cd frontend
npm run dev
```

The application should now be running on:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
