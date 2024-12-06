import streamlit as st
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

def connect_snowflake():
    conn = snowflake.connector.connect(
        account='your_account',
        user='your_username',
        password='your_password',
        warehouse='your_warehouse',
        database='your_database',
        schema='your_schema'
    )
    return conn

def query_cortex_analyst(query):
    conn = connect_snowflake()
    cursor = conn.cursor()
    
    try:
        # Example Cortex AI query
        result = cursor.execute(f"""
            SELECT CORTEX.ML.SUMMARIZE(
                '{query}', 
                language => 'it'
            ) AS summary
        """)
        return result.fetchone()[0]
    finally:
        cursor.close()
        conn.close()

st.title('Cortex Analyst Dashboard')

user_query = st.text_input('Inserisci query per analisi')
if st.button('Analizza'):
    result = query_cortex_analyst(user_query)
    st.write(result)
