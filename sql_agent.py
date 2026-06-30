from llm import llm


def generate_sql(question, table_name, columns, plan=None):
    """
    Convert natural language → SQL safely.
    """

    prompt = f"""
You are an expert SQLite SQL generator.

Convert the question into a valid SQL query.

RULES:
- Use ONLY table: {table_name}
- Use ONLY columns: {columns}
- DO NOT invent columns
- Return ONLY SQL (no markdown, no explanation)
- Use double quotes for column names with spaces
- Must be valid SQLite

IMPORTANT:
- Prefer simple queries
- Use GROUP BY only if needed
- Use ORDER BY for ranking questions
- Use LIMIT for top/bottom questions

"""

    if plan:
        prompt += f"""
PLAN:
{plan}
Follow this plan strictly.
"""

    prompt += f"""

Question:
{question}

SQL:
"""

    response = llm.invoke(prompt)
    sql = response.content.strip()

    # safety cleanup (VERY IMPORTANT)
    sql = sql.replace("```sql", "").replace("```", "").strip()
    sql = sql.split(";")[0]

    return sql


def generate_plan(question, table_name, columns):
    """
    Simple reasoning step (optional but helps accuracy)
    """

    prompt = f"""
Break the question into 2-3 simple SQL steps.

Rules:
- Do NOT write SQL
- Keep it short

Table: {table_name}
Columns: {columns}

Question:
{question}

Plan:
"""

    response = llm.invoke(prompt)
    return response.content.strip()


def generate_insight(question, result_df):
    """
    Convert result → human explanation
    """

    prompt = f"""
You are a data analyst.

Question:
{question}

Result:
{result_df.to_string(index=False)}

Explain in 2-3 simple business lines.
Do NOT repeat table.
"""

    response = llm.invoke(prompt)
    return response.content.strip()