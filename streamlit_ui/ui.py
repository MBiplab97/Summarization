import streamlit as st
import requests
import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


st.title("📄 Document Summarizer")

# Add source selection
source = st.radio("Select Document Source:", ["Google Drive", "Local Documents"])

folder_id = None
if source == "Google Drive":
    folder_id = st.text_input("Enter Google Drive Folder ID")

if st.button("Summarize"):
    params = {"source": "google_drive" if source == "Google Drive" else "local"}
    if source == "Google Drive" and folder_id:
        params["folder_id"] = folder_id

    with st.spinner("Processing documents..."):
        response = requests.post(
            "http://localhost:8000/api/summarize-folder",
            params=params
        )

    data = response.json()
    
    if data.get("status") == "success":
        st.success(f"✅ Processed {len(data['data'])} document(s) from: {data.get('source', 'unknown')}")
        
        for item in data["data"]:
            with st.expander(f"📄 {item['file_name']}"):
                # Show summary
                summary = item.get("summary", "No summary")
                st.subheader("📝 Summary")
                st.info(summary)
                
                # Show full content
                with st.expander("📋 Full Content"):
                    content = item.get("content", "No content")
                    
                    if len(content) > 500:
                        st.text_area(
                            label="File Content:",
                            value=content,
                            height=300,
                            disabled=True,
                            key=item["file_name"]
                        )
                    else:
                        st.text(content)

        if "report_path" in data and data["report_path"]:
            st.download_button(
                "Download CSV",
                data=open(data["report_path"], "rb"),
                file_name="summary_report.csv"
            )
    else:
        st.error(f"❌ Error: {data.get('detail', 'Unknown error')}")