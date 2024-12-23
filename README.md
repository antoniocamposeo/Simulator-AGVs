# Multi-AGV Optimization System for Machine Load-Unload Process

## Overview
This project implements an optimization system for managing **Automated Guided Vehicles (AGVs)** in a warehouse environment. The main objective is to minimize the **makespan**, the maximum time required for all AGVs to complete their tasks and return to the base.

---

## Features
- **Optimized Scheduling:** Uses a **Mixed-Integer Linear Programming (MILP)** model to allocate tasks efficiently.
- **Dynamic Task Management:** Real-time scheduling of AGVs for loading, processing, and unloading.
- **Multi-AGV Support:** Scales to multiple AGVs and machines with customizable configurations.
- **Performance Analysis:** Evaluates system efficiency based on variable speeds and the number of AGVs.
![prova](https://github.com/user-attachments/assets/54627e60-b4f3-46c6-aa27-1ad9bcafb2a6)

---

## Problem Description
- **AGVs:** Mobile robots that transport materials within the warehouse.
- **Machines:** Perform specific tasks like loading, processing, and unloading.
- **Objective:** Minimize the makespan while meeting operational constraints, such as machine capacity and AGV exclusivity.
![prova](https://github.com/user-attachments/assets/b8719c0f-7193-4b93-98f9-8b5cf7840b30)

---

## Model Overview
The problem is formulated as a MILP with the following components:

### Decision Variables
1. **\( x_{a,m}(t) \):** Indicates if AGV \( a \) is assigned to machine \( m \) at time \( t \).
2. **\( z_{a,m}(t) \):** Indicates if AGV \( a \) is loading/unloading at machine \( m \) at time \( t \).
3. **\( y_{a}(t) \):** Indicates if AGV \( a \) is idle at time \( t \).
4. **\( t_{makespan} \):** Represents the maximum completion time.

### Objective Function
Minimize the **makespan**:
\[
\min t_{makespan}
\]

### Constraints
1. **Task Sequencing:** Machines must follow the sequence of loading, processing, and unloading.
2. **Machine Capacity:** Only one AGV can operate at a machine at a given time.
3. **Task Exclusivity:** Each AGV performs one task at a time.
4. **Movement Timing:** AGVs must account for travel time to machines.
5. **Task Completion:** All machines complete their assigned tasks within the makespan.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-agv-project.git
   cd your-agv-project
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
1. Define the problem parameters (e.g., number of AGVs, machines, and task durations) in the configuration file.
2. Run the optimization model:
   ```bash
   python optimize.py
   ```
3. View the results, including the task schedule and makespan.

---

## Configuration
Customize the following parameters in `config.json`:
- **Number of AGVs:**
  ```json
  "num_agvs": 5
  ```
- **Machine Task Durations:**
  ```json
  "task_durations": {
    "load": 10,
    "process": 20,
    "unload": 15
  }
  ```
- **Speed Settings:**
  ```json
  "agv_speeds": [1.0, 2.0]
  ```

---

## Performance Analysis
The system evaluates the impact of:
- **Variable AGV Speeds:** From 1 to 2 m/s.
- **Number of AGVs:** Up to 5 units.

Results include:
- Optimal scheduling for different configurations.
- Insights on efficiency improvements with speed and AGV count variations.
![test](https://github.com/user-attachments/assets/6edeec17-b86b-4190-9263-9b062630d51e)

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes and push:
   ```bash
   git commit -m "Add feature-name"
   git push origin feature-name
   ```
4. Open a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Contact
For questions or feedback, contact [antoniocamposeo@gmail.com].

![prova](https://github.com/user-attachments/assets/54627e60-b4f3-46c6-aa27-1ad9bcafb2a6)



