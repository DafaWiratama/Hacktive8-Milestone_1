import pandas as pd
import streamlit as st


def landing_page(df: pd.DataFrame):
    global _df
    _df = df
    st.title("Milestone 1")
    st.markdown("""
        Hi, I'm an Data Scientist Trainee at **Hacktiv8**.  
        My name is **Dafa Wiratama** from **Batch 09** under supervision of Buddy **Sardi Irfan**.
        
        in this project, I will be using **Streamlit** to build a Data Science Dashboard that will help me to learn more about Data Science,
        and to share my Insight of the dataset
        
        this dataset was collected from [Kaggle](https://www.kaggle.com/aungpyaeap/supermarket-sales) with original author **Aung Pyae**.
        
        I hope you enjoy my project, and if you have any questions, please feel free to contact me at **DafaWiratama13@gmail.com** or LinkedIn **https://www.linkedin.com/in/wiratama13**
        
        ---
    """)

    st.checkbox("Show Data", on_change=on_show_data_change, key="show_data")


def on_show_data_change():
    global _df
    if st.session_state.show_data:
        st.subheader("Data")
        st.dataframe(_df)
