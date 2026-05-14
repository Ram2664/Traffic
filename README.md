# Digital Twin–Based Cascading Failure Modeling and Adaptive Resilience Optimization in Urban Transportation Networks

## Overview

This project presents a **Digital Twin–based smart-city resilience framework** for modeling, analyzing, and optimizing urban transportation networks under cascading failure scenarios.

The system creates a virtual representation of a real-world city transportation network using graph theory and OpenStreetMap data. It simulates infrastructure failures, propagates cascading effects through load redistribution, evaluates resilience degradation using structural metrics, and compares multiple adaptive recovery strategies.

The project is designed as a **research-grade infrastructure resilience simulator** and decision-support platform for smart-city planning, disaster management, and transportation optimization.

---

# Key Features

## Digital Twin Modeling
- Real-world road network extraction using OpenStreetMap
- Graph-based transportation modeling
- Node and edge attribute assignment
- Interactive network visualization

---

## Centrality-Based Critical Node Analysis
Compute:
- Degree Centrality
- Betweenness Centrality
- Closeness Centrality
- Eigenvector Centrality

Identify vulnerable and high-impact transportation nodes.

---

## Failure Simulation Engine
Support for:
- Random failures
- Targeted attacks
- Configurable attack size
- Step-based simulations

---

## Cascading Failure Propagation
Dynamic overload-based cascading mechanism:
- Traffic load redistribution
- Capacity threshold checking
- Domino-effect infrastructure collapse simulation

---

## Resilience Evaluation

### Metrics Used
- Largest Connected Component (LCC)
- Connectivity Loss
- Average Path Length
- Network Efficiency
- Failure Ratio
- Recovery Efficiency

---

## Recovery Strategy Optimization

Implemented strategies:
- Random Repair
- High-Traffic-First Repair
- Critical-Node-First Repair
- Hybrid Recovery

---

## Composite Urban Resilience Index

Unified resilience scoring framework combining:
- Connectivity retention
- Network efficiency
- Recovery speed
- Survivability
- Stability

---

## Interactive Visualization Dashboard
- Interactive city maps
- Cascading failure animations
- Resilience curves
- Recovery comparison graphs
- Critical node heatmaps

---

# System Architecture

```text
                +----------------------+
                |   OpenStreetMap      |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |  Digital Twin Model  |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Centrality Analysis  |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Failure Simulation   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Cascading Engine     |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Resilience Metrics   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Recovery Optimization|
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Visualization Layer  |
                +----------------------+
```

---

# Tech Stack

## Backend
- Python
- FastAPI / Flask

## Graph & Simulation Libraries
- NetworkX
- OSMnx
- NumPy
- Pandas
- SciPy

## Visualization
- Plotly
- Matplotlib
- Folium

## Frontend
- React.js
- Tailwind CSS
- JavaScript / TypeScript

## Data Source
- OpenStreetMap (OSM)

## Database
- SQLite / PostgreSQL

---

# Project Structure

```text
project-root/
│
├── backend/
│   ├── api/
│   ├── simulation/
│   ├── cascade/
│   ├── recovery/
│   ├── metrics/
│   ├── visualization/
│   ├── ai/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── App.jsx
│
├── data/
├── results/
├── docs/
├── README.md
└── requirements.txt
```

---

# Core Modules

## 1. Digital Twin Generation
Creates graph representation of transportation network using real-world OSM data.

---

## 2. Centrality Analysis
Identifies critical infrastructure nodes.

---

## 3. Failure Simulation
Simulates random and targeted transportation disruptions.

---

## 4. Cascading Failure Engine
Models overload propagation and domino-effect failures.

---

## 5. Resilience Metrics
Measures degradation and recovery behavior.

---

## 6. Recovery Optimization
Evaluates adaptive infrastructure restoration strategies.

---

## 7. Visualization Dashboard
Provides interactive analysis and simulation monitoring.

---

# Recovery Strategies

| Strategy | Description |
|---|---|
| Random Repair | Repairs random failed nodes |
| High-Traffic-First | Repairs nodes with highest traffic load |
| Critical-Node-First | Repairs highest-centrality nodes |
| Hybrid Recovery | Combines traffic and centrality |

---

# Metrics Used

| Metric | Purpose |
|---|---|
| LCC | Measures surviving connected network |
| Connectivity Loss | Measures fragmentation |
| Average Path Length | Measures routing degradation |
| Network Efficiency | Measures transport efficiency |
| Failure Ratio | Measures infrastructure damage |
| Recovery Efficiency | Measures restoration performance |

---

# Applications

- Smart City Planning
- Disaster Management
- Transportation Optimization
- Infrastructure Resilience Analysis
- Urban Risk Assessment
- Emergency Response Planning

---

# Future Enhancements

## AI-Based Failure Prediction
Predict vulnerable intersections using machine learning.

## Reinforcement Learning Recovery
Train intelligent repair agents.

## Real-Time Traffic Integration
Use live traffic feeds for dynamic simulation.

## Multi-Layer Infrastructure Modeling
Integrate:
- power grids,
- communication systems,
- emergency services.

## Emergency Vehicle Routing
Dynamic ambulance and fire-truck rerouting.

---

# Gemini API Integration (Optional)

Gemini API can later be integrated for:

- predictive analysis,
- infrastructure recommendations,
- resilience report generation,
- intelligent recovery suggestions.

## Important
Store API keys securely in `.env` files.

Never expose API keys in frontend code.

Example:

```env
GEMINI_API_KEY=your_api_key
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd project-root
```

## Install Backend Dependencies

```bash
pip install -r requirements.txt
```

## Run Backend

```bash
uvicorn backend.main:app --reload
```

## Run Frontend

```bash
npm install
npm run dev
```

---

# Expected Outputs

- Critical node rankings
- Cascading failure visualizations
- Resilience degradation curves
- Recovery strategy comparison
- Interactive transportation maps
- Composite resilience scores

---

# Conclusion

This project provides a research-grade framework for modeling cascading failures and resilience optimization in urban transportation systems using Digital Twin technology.

It combines:
- graph theory,
- network science,
- resilience engineering,
- and smart-city infrastructure analysis

to support better urban planning and infrastructure decision-making.

