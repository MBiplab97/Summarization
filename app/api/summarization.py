# Refactor imports to avoid circular dependency
from fastapi import APIRouter
from modules.google_drive import GoogleDriveService
from modules.local_documents import LocalDocumentService
from modules.summarizer import SummarizerService
from modules.report_generator import ReportGenerator

# Initialize the router
router = APIRouter()

@router.post("/summarize-folder")
async def summarize_folder(folder_id: str = None, source: str = "google_drive"):
    """
    Summarize documents from a folder.
    
    Args:
        folder_id: Google Drive folder ID (required if source is "google_drive")
        source: "google_drive" or "local" (default: "google_drive")
    """
    
    if source == "local":
        doc_service = LocalDocumentService()
    else:
        doc_service = GoogleDriveService()
    
    summarizer = SummarizerService()

    if source == "local":
        files = await doc_service.list_files()
    else:
        files = await doc_service.list_files(folder_id)

    results = []

    for file in files:
        content = await doc_service.download_file(file)
        
        text = await doc_service.extract_text(file["name"], content)
        
        # Generate summary
        summary = await summarizer.summarize(text) if text else "No text to summarize"
        
        results.append({
            "file_name": file["name"],
            "content": text if text else "No text extracted",
            "summary": summary
        })

    return {
        "status": "success",
        "source": source,
        "data": results
    }