Project Brief: City Pulse - An Agentic AI City Companion
1. High-Level Vision
City Pulse is an AI-powered companion that transforms the chaos of urban life into a single, intelligent, and personalized feed. The goal is to create a personal city concierge that understands what's happening, what it means for the city, and what it means for the user. It moves beyond simple data aggregation to provide synthesized, predictive, and personalized insights.

2. Production Architecture: GKE-based Microservices
The long-term vision is a robust, scalable platform built on a microservices architecture running on Google Kubernetes Engine (GKE).

Services: The architecture is composed of distinct, independent services, each with a specific responsibility:

Data Ingest Service: Responsible for polling external data sources.

Event Processing Service: The core analysis engine that enriches raw data.

User Personalization Service: Manages user interaction, personalization, and learning.

Communication: Services communicate asynchronously via Google Cloud Pub/Sub, creating a resilient, event-driven system.

Gateway & Auth: A Google Cloud API Gateway serves as the single, secure entry point, with user identity managed by Firebase Authentication.

Database: Cloud Firestore is the primary database for storing structured, real-time data like incidents, events, and user profiles.

3. Core Components & Technology Stack
Language: Python is the language of choice due to its mature AI/ML ecosystem.

Framework: Microservices are built using FastAPI for its high performance and modern features.

Data Validation: Pydantic models are used to enforce strict data contracts and ensure API robustness.

Containerization: All services are containerized using Docker for portability and consistent deployment.

4. The Agentic Core
The "magic" of City Pulse lies in its team of specialized agents, whose logic is built using the Vertex AI ADK and powered by the Gemini API.

Scout Agent (within the Data Ingest Service):

Polls external data sources (Twitter, News, Events, Weather).

Performs initial data enrichment, including a sophisticated Trust Score Algorithm for sources and users. This algorithm uses a multiplicative model based on account age, verified status, and affiliations.

Handles initial dereferencing of URLs and referenced content.

Analyst Agent (within the Event Processing Service):

Synthesizes and de-duplicates information from multiple sources (e.g., understands that a tweet and a news article are about the same incident).

Predictor Agent (within the Event Processing Service):

Acts as a second layer of analysis, predicting the real-world impact of a verified incident (e.g., "Severe congestion for 90 minutes").

Concierge Agent (within the User Personalization Service):

Manages the user-facing interaction.

Understands nuanced, natural language queries.

Executes a "continuous learning" loop by identifying new interests from user queries and suggesting updates to their profile.

5. Hackathon MVP Strategy
The immediate goal is to build a high-fidelity prototype that proves the core agentic concepts.

Mock API Server: A crucial pre-built component. It's a Firestore-powered Flask/FastAPI microservice that simulates all external APIs, providing a stable and controllable data source for the demo.

Focus: The hackathon build will focus on implementing the agent logic and the A2A (Agent-to-Agent) communication, which will be achieved via direct REST API calls between the orchestrated services.

Technology: The MVP will be built and deployed using Cloud Run for its speed and simplicity, with a clear architectural path to migrate the containerized services to GKE for the production version.


Your job as an agent is to help me assist with creating the mock API part of this. We are creating a dockerized API to be eventually run in google cloud run so we can demo a POC in the hackathon.