import streamlit as st
import requests

st.title("📄 Google Drive Document Summarizer")

folder_id = st.text_input("Enter Google Drive Folder ID")

if st.button("Summarize"):

    response = requests.post(
        "http://localhost:8000/api/summarize-folder",
        params={"folder_id": folder_id}
    )

    data = response.json()

    for item in data["data"]:
        st.subheader(item["file_name"])
        st.write(item["summary"])

    st.download_button(
        "Download CSV",
        data=open(data["report_path"], "rb"),
        file_name="summary_report.csv"
    )