import sqlparse
import re
def is_select_query(sql: str) -> bool:
    """
    Returns True only if the SQL statement is a SELECT query.
    """

    parsed = sqlparse.parse(sql)

    if not parsed:
        return False

    statement = parsed[0]

    return statement.get_type() == "SELECT"


def contains_dangerous_keywords(sql: str) -> bool:
    """
    Returns True if the SQL contains dangerous statements.
    """

    dangerous_keywords = [
        "DELETE",
        "DROP",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "ATTACH",
        "DETACH"
    ]

    sql_upper = sql.upper()

    return any(keyword in sql_upper for keyword in dangerous_keywords)
def validate_table_name(sql: str, expected_table: str) -> bool:
    """
    Returns True if the SQL references only the expected table.
    """

    match = re.search(r"FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)", sql, re.IGNORECASE)

    if not match:
        return False

    table_name = match.group(1)

    return table_name.lower() == expected_table.lower()
def validate_sql(sql: str, expected_table: str):
    """
    Validates the SQL query before execution.
    Returns (is_valid, message).
    """

    if contains_dangerous_keywords(sql):
        return False, "Dangerous SQL keywords detected."

    if not is_select_query(sql):
        return False, "Only SELECT queries are allowed."

    if not validate_table_name(sql, expected_table):
        return False, f"Query must use the '{expected_table}' table."

    return True, "SQL validation passed."
if __name__ == "__main__":
    print(validate_sql(
        "SELECT * FROM uploaded_data",
        "uploaded_data"
    ))

    print(validate_sql(
        "DELETE FROM uploaded_data",
        "uploaded_data"
    ))

    print(validate_sql(
        "SELECT * FROM employees",
        "uploaded_data"
    ))
