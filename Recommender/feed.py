import streamlit as st
import pandas as pd

# streamlit run feed.py


@st.cache_data
def load_feed():
    return pd.read_csv(
        "/Users/iansnyder/Desktop/Projects/LLM/Repository/Feed.csv", index_col="Id"
    )


data_df = load_feed()


st.data_editor(
    data_df,
    column_config={
        "Title": st.column_config.TextColumn(
            "Paper Title",
            help="The title of the paper",
            default="st.",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        ),
        "URL": st.column_config.LinkColumn(
            "View PDF",
            help="The top trending Streamlit apps",
            max_chars=100,
        ),
    },
    hide_index=True,
)
