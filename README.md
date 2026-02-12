# 🌡️ Autonomic Digital Twin for IoT Cooling System

A self-managed **Autonomic Digital Twin (DT)** for an IoT cooling system that detects silent failures and autonomously applies corrective actions using **Signal Temporal Logic (STL)** and **Node-RED orchestration**.

---

## 🔎 Overview

This project implements a four-layer Digital Twin architecture:

- **Physical Layer** – ESP32 + DHT22 + Fan (Wokwi simulation)  
- **Communication Layer** – MQTT (HiveMQ broker)  
- **Cognitive Layer** – Python + RTAMT for STL runtime verification  
- **Orchestration Layer** – Node-RED Dashboard & logging  

The Digital Twin continuously monitors system safety and overrides faulty physical behavior when violations are detected.

---

## 🧠 Core Innovation

The Cognitive Engine evaluates the formal safety rule:

```
((temp > 30) implies (fan_status >= 1))
```

If robustness < 0:
- 🚨 A safety violation is detected  
- 🔄 The Digital Twin intervenes  
- 📝 The event is logged for forensic analysis  

---

## ⚙️ Key Features

- 🔐 Unique device identity via MQTT `CLIENT_ID`
- 🔄 Real-time state reflection (every 2 seconds)
- 🔁 Bidirectional entanglement (cloud overrides device logic)
- 🧮 Formal runtime verification using STL
- 📊 Live monitoring dashboard with robustness visualization
- 🗂 Persistent violation logging

---

## 🚀 Tech Stack

- **ESP32 (Wokwi Simulation)**
- **MQTT (HiveMQ)**
- **Python (paho-mqtt, RTAMT)**
- **Node-RED Dashboard**
- **Signal Temporal Logic (STL)**

---

## 📸 System Demo

```markdown
[Wokwi Simulation](images/wokwi.png)
[Dashboard Monitoring](images/dashboard.png)
[STL Robustness Output](images/terminal.png)
```

---

## 📂 Project Structure

```
firmware/
cognitive-engine/
orchestrator/
images/
```

---

## 🎯 Why This Project Matters

This work demonstrates:

- Formal verification in IoT systems  
- Self-healing cyber-physical systems  
- Practical implementation of Digital Twin theory  
- Integration of embedded systems + cloud + formal methods  
