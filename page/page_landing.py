import pandas as pd
import streamlit as st

# Global Variables
is_show_dataframe = False


def landing_page(df: pd.DataFrame):
    global _df
    _df = df
    st.title("Milestone 1")
    st.markdown("""
        Hi, I'm an Data Scientist Trainee at **Hacktiv8**.  
        My name is **Dafa Wiratama** from **Batch 09** under supervision of Buddy **Sardi Irfansyah**.
        
        in this project, I will be using **Streamlit** to build a Data Science Dashboard that will help me to learn more about Data Science,
        and to share my Insight of the dataset
        
        this dataset was collected from [Kaggle](https://www.kaggle.com/aungpyaeap/supermarket-sales) with original author **Aung Pyae**.
        
        I hope you enjoy my project, and if you have any questions, please feel free to contact me at **DafaWiratama13@gmail.com** or LinkedIn **https://www.linkedin.com/in/wiratama13**
        
        ---
    """)

    # Callback Trigger
    st.checkbox("Show Data", on_change=on_show_data_change, value=is_show_dataframe)

    if is_show_dataframe:
        st.subheader("Dataset")
        st.dataframe(_df)


# Callback Function
# Side note :
# I don't know why iam doing this but for the sake of assignment I'm doing this for rubric `implement streamlit callback`
def on_show_data_change():
    global is_show_dataframe
    is_show_dataframe = not is_show_dataframe
