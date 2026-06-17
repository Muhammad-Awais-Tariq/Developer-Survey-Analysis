import streamlit as st
import pandas as pd
from main import replace_multiselect , 
st.set_page_config(page_title="Survey Analysis", layout="centered")

st.title("Stack overflow surver analysis")
st.header("Upload file")
file = st.file_uploader("upload the survey")
file_df = pd.read_csv(file)
st.subheader("Statistical Summary")
st.dataframe(file_df.describe())

st.title("Demographics")
