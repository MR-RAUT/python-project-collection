# 📦 FastBox – Mystery Delivery System (Python)

A logistics simulation system that models one day of package delivery operations for a fictional company called **FastBox**.
The system assigns packages to delivery agents based on proximity, simulates deliveries, measures efficiency, and generates detailed reports.

This project is designed to be closely resembling real-world backend logic.

---

## 🧠 Problem Overview

FastBox operates with:

* Multiple **warehouses**
* Multiple **delivery agents**
* Multiple **packages**

### Objectives:

1. Read and parse JSON input data
2. Assign each package to the nearest agent (Euclidean distance)
3. Simulate delivery routes
4. Calculate total distance traveled per agent
5. Identify the most efficient agent
6. Generate reports in JSON and CSV formats
7. Validate correctness using multiple test cases

---

## 📁 Project Structure

```bash
fastbox-mystery-delivery/
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py        # JSON loader
│   ├── distance.py           # Euclidean distance logic
│   ├── assignment.py         # Package → Agent assignment
│   ├── simulation.py         # Delivery simulation (+ delay)
│   └── report.py             # JSON & CSV report generator
│
├── data/
│   └── data.json             # Original assignment input
│
├── Test_cases/
│   ├── test_case_1.json
│   ├── ...
│   └── test_case_10.json     # Scenario-based test cases
│
├── output/
│   ├── report.json
│   ├── top_agent.csv
│   └── test_case_report/
│       ├── test_case_1_report.csv
│       ├── ...
│       └── test_case_10_report.csv
│
├── base_case.json            # Sanity / demo input
├── main.py                   # Main execution file
├── test_runner.py            # Automated test runner
├── requirements.txt
└── README.md
```

---

## 🔄 System Flow

JSON Input
   ↓
Data Loading
   ↓
Agent–Package Assignment
   ↓
Delivery Simulation
   ↓
Efficiency Calculation
   ↓
Report Generation (JSON / CSV)
   ↓
Test Case Validation

---

## 📐 Distance Calculation

Euclidean distance is used to determine proximity:

distance = √((x₂ − x₁)² + (y₂ − y₁)²)

This is used for:

* Agent → Warehouse
* Warehouse → Destination

---

## 📊 Efficiency Metric

Each agent’s efficiency is calculated as:

efficiency = total_distance / packages_delivered


* Lower efficiency = better performance
* Agents with zero deliveries are excluded
* This avoids unfair comparison based only on volume

---

## 🏆 Best Agent Selection

The **best agent** is defined as:

> The agent who delivers packages using the least distance per delivery.

This reflects real-world logistics optimization.

---

## 🧪 Testing Strategy

### ✔ Scenario-Based Testing

* All test cases are stored as JSON files
* Each file represents a full day of operations
* Tests validate that **all packages are delivered**

### ✔ Automated Validation

* PASS / FAIL based on expected vs delivered packages
* No manual verification required

### ✔ CSV Report Per Test Case

For each test case, a CSV report is generated:

output/test_case_report/test_case_X_report.csv

Each CSV includes:

* Agent ID
* Packages delivered
* Total distance
* Efficiency
* Best agent status

---

## 🔄 Data Normalization

Some test cases use legacy or alternative JSON formats.

To ensure stability:

* Input data is normalized inside the test runner
* Core business logic remains unchanged
* Prevents schema-related runtime errors

This mirrors real-world systems that accept data from multiple sources.

---

## ⭐ Bonus Features Implemented

* ✅ **Random delivery delays** (optional, realistic simulation)
* ✅ **Mid-day agent joining** (data-driven, no logic change)
* ✅ **CSV export for analytics**
* ✅ **Best agent tagging**
* ✅ **Multiple input schemas supported**

---

## ▶️ How to Run

### Run base case / demo:

```bash
python main.py
```

### Run all test cases:

```bash
python test_runner.py
```

---

## 📦 Outputs

* `output/report.json` – Main summary report
* `output/top_agent.csv` – Agent performance summary
* `output/test_case_report/*.csv` – Per-test analytics

---

## 🎤 Explanation (Short)

> “I designed the system with modular components and scenario-based testing. Inputs are normalized for consistency, deliveries are simulated realistically, and performance metrics are exported for analysis. The system is data-driven and easy to extend.”

---

## ✅ Key Engineering Highlights

* Modular design
* Clean separation of concerns
* Data-driven logic
* Scalable testing approach
* Real-world efficiency metric
* Clear debugging and validation flow

---

## 🏁 Final Notes

* All requirements from the assignment are fully implemented
* Bonus features are included without breaking core logic
* The project is production-style, testable, and interview-ready

---


