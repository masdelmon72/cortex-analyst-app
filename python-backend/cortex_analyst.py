import os
import streamlit as st
import snowflake.connector
from snowflake.snowpark import Session

def create_snowpark_session():
    connection_parameters = {
        "account": st.secrets["snowflake"]["account"],
        "user": st.secrets["snowflake"]["username"],
        "password": st.secrets["snowflake"]["password"],
        "warehouse": st.secrets["snowflake"]["warehouse"],
        "database": st.secrets["snowflake"]["database"],
        "schema": st.secrets["snowflake"]["schema"]
    }
    return Session.builder.configs(connection_parameters).create()

def cortex_analyst_query(session, query):
    try:
        result = session.sql(f"""
            SELECT CORTEX.ML.SUMMARIZE(
                '{query}', 
                language => 'en'
            ) AS summary
        """).collect()
        return result[0]['SUMMARY']
    except Exception as e:
        st.error(f"Cortex Analysis Error: {e}")
        return None

def main():
    st.title("Cortex Analyst Dashboard")
    
    with st.form(key='cortex_query_form'):
        query_input = st.text_area("Enter your analysis query")
        submit_button = st.form_submit_button(label='Analyze')
        
        if submit_button and query_input:
            with st.spinner('Analyzing with Cortex...'):
                try:
                    session = create_snowpark_session()
                    analysis_result = cortex_analyst_query(session, query_input)
                    
                    if analysis_result:
                        st.success("Analysis Complete")
                        st.write(analysis_result)
                except Exception as e:
                    st.error(f"Connection Error: {e}")

if __name__ == "__main__":
    main()
