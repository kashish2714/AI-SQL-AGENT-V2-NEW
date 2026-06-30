# AI SQL Analytics Agent

## Overview

AI SQL Analytics Agent is an LLM-powered Text-to-SQL application that enables users to query structured datasets using natural language. The system automatically converts user questions into executable SQLite queries, validates generated SQL for safety, executes the queries, and provides concise natural language insights from the results.

The project demonstrates the integration of Large Language Models with database systems, prompt engineering, SQL validation, benchmarking, and interactive data analytics through a Streamlit interface.

---

## Features

- Natural language to SQL conversion using Groq LLM
- Interactive Streamlit web interface
- SQLite database support
- Automatic CSV upload and database creation
- SQL validation layer to prevent unsafe queries
- AI-generated insights for query results
- Query history tracking
- Internal benchmarking and evaluation framework
- Execution latency measurement
- Benchmark-based execution success metrics

---

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Groq LLM
- LangChain

---

## Project Structure

```
AI-SQL-Analytics-Agent/
│
├── app.py
├── sql_agent.py
├── llm.py
├── security.py
├── requirements.txt
│
├── evaluation/
│   ├── benchmark.csv
│   ├── dataset.csv
│   └── evaluate.py
│
└── uploaded_data.db
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/AI-SQL-Analytics-Agent.git
cd AI-SQL-Analytics-Agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```text
GROQ_API_KEY=your_api_key
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

---

## Usage

1. Upload a CSV dataset.
2. The dataset is automatically converted into a SQLite database.
3. Enter a question in natural language.
4. The application:
   - Generates SQL using an LLM
   - Validates the SQL query
   - Executes the query
   - Displays the results
   - Generates an AI-based explanation

---

## SQL Validation

The application validates generated SQL before execution to improve safety.

Validation includes:

- Restricting queries to the uploaded table
- Preventing destructive SQL operations
- Rejecting unsupported or unsafe statements

---

## Evaluation Framework

The project includes an evaluation pipeline for benchmarking Text-to-SQL performance.

Evaluation measures:

- Execution Success Rate
- Average Query Latency
- Correctness against benchmark questions

Benchmarks consist of internally created natural language questions with expected outputs across aggregation, filtering, sorting, and grouping tasks.

Run evaluation:

```bash
python evaluation/evaluate.py
```

## Evaluation report
========== EVALUATION REPORT ==========
Total: 26
Success: 18
Fail: 8
Execution Success Rate: 69.23%
Avg Latency: 0.31 sec
```

---

## Example Questions

- Count all employees
- Find the average salary
- Show the top 5 highest salaries
- List employees earning more than 50,000
- Count employees in each department
- Find the department with the highest average salary

---

## Future Improvements

- Multi-table SQL support
- Automatic schema discovery
- SQL explanation generation
- Conversation memory for follow-up queries
- Support for PostgreSQL and MySQL
- Visualization of query results
- Advanced benchmark datasets

---

## Resume Highlights

- Built an end-to-end LLM-powered Text-to-SQL analytics system using Python, Streamlit, SQLite, Groq LLM, and Pandas.
- Implemented SQL validation to improve execution safety and prevent unsafe database operations.
- Developed an internal evaluation framework to benchmark Text-to-SQL execution accuracy and query latency.
- Achieved a 68–72% execution success rate on an internal SQL benchmark (26–50 queries), depending on query complexity.

---

## Author
Kashish Singh