# AI-Based-Energy-Consumption-Optimizer-For-Commercial-And-Industrial-Buildings
AI-powered energy optimization system that combines LSTM-based environmental forecasting with PPO reinforcement learning to intelligently optimize fan operation in industrial and commercial buildings.

# AI-Based Energy Consumption Optimizer for Industrial and Commercial Buildings

An intelligent energy optimization system that combines LSTM-based environmental forecasting with Proximal Policy Optimization (PPO) Reinforcement Learning to make predictive and energy-efficient fan control decisions for industrial and commercial buildings.


# Overview

Buildings consume a significant amount of energy through ventilation and cooling systems. Conventional control methods typically rely on fixed thresholds or manual operation, making them unable to adapt to continuously changing environmental conditions.

This project presents an AI-based solution that predicts future environmental conditions using historical sensor data through an LSTM model and determines the optimal fan operation using a PPO reinforcement learning agent. The system aims to reduce unnecessary energy consumption while maintaining occupant comfort through predictive and adaptive decision-making.


# Key Features

- Predictive environmental forecasting using LSTM
- Intelligent fan control using PPO Reinforcement Learning
- Automated energy optimization report generation
- Support for CSV and Excel dataset uploads
- Historical data validation before analysis
- Real-time prediction of indoor and outdoor environmental conditions
- Responsive web-based interface
- Downloadable sample datasets for testing



# System Architecture

```
Historical Sensor Data
          │
          ▼
Data Validation
          │
          ▼
Preprocessing
          │
          ▼
LSTM Forecasting Model
          │
          ▼
Predicted Environmental Conditions
          │
          ▼
PPO Reinforcement Learning Agent
          │
          ▼
Optimal Fan Control Decision
          │
          ▼
Energy Optimization Report
```



# Workflow

1. Upload a historical environmental dataset.
2. Validate the uploaded dataset.
3. Extract the latest 24 historical records.
4. Predict future environmental conditions using the trained LSTM model.
5. Pass the predicted conditions along with occupancy information to the PPO agent.
6. Generate the optimal fan control decision.
7. Display the complete environmental analysis and recommendation.



# Artificial Intelligence Models

## LSTM Forecasting Model

The LSTM model predicts future environmental conditions using the previous 24 historical sensor records.

### Input Features

- Indoor Temperature
- Indoor Humidity
- Outdoor Temperature
- Outdoor Humidity
- Outdoor Wind Speed
- Occupancy Presence

### Predicted Outputs

- Indoor Temperature
- Indoor Humidity
- Outdoor Temperature
- Outdoor Humidity



## PPO Reinforcement Learning Agent

The PPO agent receives:

- Predicted Indoor Temperature
- Predicted Indoor Humidity
- Predicted Outdoor Temperature
- Predicted Outdoor Humidity
- Current Occupancy State

Based on these inputs, the agent determines the optimal fan state to maximize energy efficiency while maintaining occupant comfort.



# Technology Stack

## Artificial Intelligence

- TensorFlow
- Keras
- Stable-Baselines3
- Gymnasium
- NumPy
- Pandas
- Scikit-learn

## Backend

- Python
- FastAPI

## Frontend

- HTML5
- CSS3
- JavaScript

---

# Project Structure

```
AI-Based-Energy-Consumption-Optimizer/

│
├── backend/
├── frontend/
├── datasets/
├── docs/
├── screenshots/
├── README.md
├── LICENSE
└── .gitignore
```



# Screenshots

### Home Page

<p align="center">

  <img src="AI-Based-Energy-Consumption-Optimizer/docs/Project-Pics/Home page.png" width="90%">

</p>

### Analysis Interface

<p align="center">

  <img src="AI-Based-Energy-Consumption-Optimizer/docs/Project-Pics/Analysis Page.png" width="90%">

</p>

### Energy Optimization Report

<p align="center">

  <img src="AI-Based-Energy-Consumption-Optimizer/docs/Project-Pics/Report Page.png" width="90%">

</p>



# Architecture Diagram

*(Insert Architecture Diagram)*



# Workflow Diagram

*(Insert Workflow Diagram)*



# Sample Datasets

The repository contains multiple sample datasets representing different environmental scenarios for demonstration and testing purposes.

These include:

- Cool Office Environment
- Hot Summer Conditions
- Empty Building
- Fully Occupied Building
- Highly Dynamic Environmental Conditions
- Mixed Daily Environmental Profile

---

# Deployment

Live Application

```
Add deployment URL here
```

---

# Research Paper

The complete research paper associated with this project is available in:

```
Publication is in Process!!
```


# Conference Presentation Certificate

The project certificate is available in:

[Project Certificate](AI-Based-Energy-Consumption-Optimizer/docs/632_Atharva%20Khairnar_certificate.pdf)



# Future Scope

- Integration with IoT sensor networks
- Intelligent HVAC optimization
- Multi-device energy scheduling
- Building-wide reinforcement learning
- Cloud deployment
- Renewable energy integration
- Explainable AI
- Digital Twin implementation


# License

This project is released under the MIT License.
