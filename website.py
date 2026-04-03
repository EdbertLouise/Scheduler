import streamlit as st
from main import processInput

st.write("Input")

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "png", "jpg"],
    accept_multiple_files=True
)

# for files in uploaded_files:
#     print("FUN", files.name)

with st.form("Input"):
    text = st.text_area("")
    submitted = st.form_submit_button("》》")

    if submitted:
        logResults = processInput(text, uploaded_files)
        for logs in logResults:
            st.write(logs)

