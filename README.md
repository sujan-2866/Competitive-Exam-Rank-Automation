# 🧮 Competitive Exam Rank Automation

This project automates the **percentile and rank computation** process for competitive entrance exams like **JEE Mains**, **NEET**, and **JEE Advanced**. It simulates real-world test scenarios by generating synthetic student data, test sessions, and scorecards, and computes ranks using a customizable tie-breaker logic.

---

## 📌 Features

- 🧑‍🎓 Auto-generation of student master data (names, emails, contact)
- 📊 Simulated test session data generation (multiple sessions & attempts)
- 📈 Accurate percentile calculation up to 7 decimal places
- 🥇 Customizable ranking and tie-breaker algorithm
- 📤 CSV-based output for mark sheets, ranklists, and analytics
- 🔎 Query module to fetch toppers, marks/rank ranges
- 🗃️ Persistent storage using **MySQL**

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Libraries: `mysql-connector-python`, `numpy`, `pandas`, `yaml`, `getpass`

Install dependencies:
```bash
pip install mysql-connector-python numpy pandas pyyaml
```


## 🛠 Project Structure

├── generate_master_data.py        # Generate student profiles
├── generate_test_data.py          # Assign sessions and marks
├── compute_percentile_rank.py     # Compute percentiles & ranks
├── print_query_module.py          # Marksheet viewer & query interface
├── names.yaml                     # Sample name bank for random generation


## 🧪 How It Works
1. Generate Students
	•	Creates synthetic student profiles with unique RegIDs
	•	Stores student data in Student_Master table in MySQL

2. Assign Test Sessions & Marks
	•	Simulates 2 batches × 4 sessions = 8 total sessions
	•	Students can appear in one or both batches
	•	Marks are generated using realistic probabilistic distributions

3. Compute Percentile & Rank
	•	Calculates percentiles per session in all subjects and total
	•	Picks best attempt’s percentile for final rank
	•	Supports accurate tie-breaking logic (multi-level subject comparison)

4. Query Module
	•	View student marksheet by RegID
	•	Export toppers list
	•	Fetch students in rank/mark ranges
	•	Export reports as .csv

⸻

🖼 Sample Output
	•	Marksheet CSV
	•	Top Rankers List
	•	Custom Range Export

⸻

