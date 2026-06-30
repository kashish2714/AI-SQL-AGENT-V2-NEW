import time
import pandas as pd
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sql_agent import generate_sql, generate_plan
from security import validate_sql


def fix_sql(question, bad_sql, error, table_name, columns):
    from llm import llm

    prompt = f"""
Fix this SQL query for SQLite.

RULES:
- Use ONLY table: {table_name}
- Use ONLY columns: {columns}
- Return ONLY SQL

Question: {question}
Wrong SQL: {bad_sql}
Error: {error}

Fixed SQL:
"""

    response = llm.invoke(prompt)
    sql = response.content.strip()

    sql = sql.replace("```sql", "").replace("```", "").strip()
    sql = sql.split(";")[0]

    return sql


df = pd.read_csv("evaluation/dataset.csv")

conn = sqlite3.connect("evaluation.db")
df.to_sql("eval_data", conn, if_exists="replace", index=False)

benchmark = pd.read_csv("evaluation/benchmark.csv")

success = 0
fail = 0
latencies = []

for _, row in benchmark.iterrows():

    question = row["question"]
    expected_value = row["expected_value"]
    metric_type = row["metric_type"]

    print("\nQ:", question)

    start = time.perf_counter()

    try:
        # STEP 1: PLAN
        plan = generate_plan(question, "eval_data", list(df.columns))

        # STEP 2: SQL
        sql_query = generate_sql(question, "eval_data", list(df.columns), plan)
        print("\nRAW SQL OUTPUT:\n", sql_query)

        print("SQL:", sql_query)

        # STEP 3: VALIDATION
        is_valid, message = validate_sql(sql_query, "eval_data")

        if not is_valid:
            sql_query = fix_sql(question, sql_query, message, "eval_data", list(df.columns))

        # STEP 4: EXECUTION
        try:
            result = pd.read_sql_query(sql_query, conn)
        except Exception as e:
            sql_query = fix_sql(question, sql_query, str(e), "eval_data", list(df.columns))
            result = pd.read_sql_query(sql_query, conn)

        # STEP 5: SCORING
        is_correct = False

        if metric_type == "scalar":
            try:
                is_correct = abs(float(result.iloc[0, 0]) - float(expected_value)) < 0.01
            except:
                is_correct = False

        elif metric_type == "rows":
            is_correct = len(result) == int(expected_value)

        if is_correct:
            success += 1
        else:
            fail += 1

    except Exception as e:
        print("Error:", e)
        fail += 1

    end = time.perf_counter()
    latencies.append(end - start)


print("\n========== EVALUATION REPORT ==========")
print("Total:", len(benchmark))
print("Success:", success)
print("Fail:", fail)
print("Execution Success Rate:", round(success / len(benchmark) * 100, 2), "%")
print("Avg Latency:", round(sum(latencies) / len(latencies), 4), "sec")

conn.close()