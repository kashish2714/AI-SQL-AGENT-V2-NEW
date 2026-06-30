import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

from database import create_database
from sql_agent import generate_sql, generate_insight
from security import validate_sql


# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="AI SQL Analytics Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI SQL Analytics Agent")
st.write("Upload CSV → Ask questions → Get SQL + Insights + Charts")

st.divider()


# ----------------------------
# Session State (History)
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = []


# ----------------------------
# Chart Function (SAFE)
# ----------------------------
def generate_chart(df):

    if df is None or df.empty:
        return None

    if df.shape[1] < 2:
        return None

    numeric_cols = df.select_dtypes(include=['number']).columns

    if len(numeric_cols) == 0:
        return None

    y_col = numeric_cols[0]
    x_col = df.columns[0]

    fig, ax = plt.subplots()
    ax.bar(df[x_col].astype(str), df[y_col])

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{y_col} by {x_col}")

    plt.xticks(rotation=45)

    return fig


# ----------------------------
# Upload CSV
# ----------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])


if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    create_database(df)

    st.success("✅ File uploaded & database created!")

    st.divider()

    # ----------------------------
    # Dataset Preview
    # ----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.write("### Columns")
    st.write(list(df.columns))

    st.divider()


    # ----------------------------
    # Sidebar History
    # ----------------------------
    st.sidebar.title("🧠 Query History")

    if st.sidebar.button("Clear History"):
        st.session_state.history = []

    for i, item in enumerate(reversed(st.session_state.history)):
        with st.sidebar.expander(f"Q{i+1}: {item['question']}"):
            st.code(item["sql"], language="sql")
            st.write(item["insight"])


    # ----------------------------
    # Query Section
    # ----------------------------
    st.subheader("Ask Questions About Your Data")

    question = st.text_input("Enter your question")

    if question:

        # Generate SQL
        sql_query = generate_sql(
         question=question,
         table_name="uploaded_data",
         columns=list(df.columns)
        )

        st.write("### 🧠 Generated SQL")
        st.code(sql_query, language="sql")

        conn = sqlite3.connect("uploaded_data.db")
        is_valid, message = validate_sql(
            sql_query,
            expected_table="uploaded_data"
        )
        if not is_valid:
           st.error(message)
           conn.close()
           st.stop()



        try:
            result = pd.read_sql_query(sql_query, conn)

            if result is None or result.empty:
                st.warning("No results returned. Try another question.")
                st.stop()

            # Result
            st.write("### 📊 Result")
            st.dataframe(result)

            # Insight
            st.write("### 💡 Insight")
            insight = generate_insight(question, result)
            st.info(insight)

            # Save to history
            st.session_state.history.append({
                "question": question,
                "sql": sql_query,
                "insight": insight
            })

            # Chart
            st.write("### 📈 Visualization")
            fig = generate_chart(result)

            if fig:
                st.pyplot(fig)
            else:
                st.info("Chart not available for this result shape.")

        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

        finally:
            conn.close()