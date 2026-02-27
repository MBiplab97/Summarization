import streamlit as st
import requests
import sys
import asyncio
import pandas as pd
from io import BytesIO

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


st.title("📄 Document Summarizer")

# Add source selection
source = st.radio("Select Document Source:", ["Google Drive", "Local Documents"])

folder_id = None
if source == "Google Drive":
    folder_id = st.text_input("Enter Google Drive Folder ID")

if source == "Google Drive":
    if st.button("Summarize"):
        st.write('Kindly use local folder for now.')
if source == "Local Documents":
    if st.button("Summarize"):
        params = {"source": "local"}
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
                # Create Excel file with input (content) and output (summary)
                excel_data = []
                for item in data["data"]:
                    excel_data.append({
                        "File Name": item["file_name"],
                        "Original Content": item.get("content", ""),
                        "Summary": item.get("summary", "")
                    })
                
                df = pd.DataFrame(excel_data)
                
                # Create Excel file in memory
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                    df.to_excel(writer, sheet_name="Summaries", index=False)
                
                excel_buffer.seek(0)
                
                st.download_button(
                    "📥 Download Excel Report",
                    data=excel_buffer,
                    file_name="summary_report.xls",
                    mime="application/vnd.ms-excel"
                )
        else:
            st.error(f"❌ Error: {data.get('detail', 'Unknown error')}")