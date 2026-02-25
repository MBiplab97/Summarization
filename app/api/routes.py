from fastapi import APIRouter, Depends
from app.modules.google_drive import GoogleDriveService
from app.modules.document_parser import DocumentParser
from app.modules.summarizer import SummarizerService
from app.modules.report_generator import ReportGenerator

router = APIRouter()

@router.post("/summarize-folder")
async def summarize_folder(folder_id: str):

    drive_service = GoogleDriveService()
    parser = DocumentParser()
    summarizer = SummarizerService()
    report = ReportGenerator()

    files = await drive_service.list_files(folder_id)

    results = []

    for file in files:
        content = await drive_service.download_file(file)
        text = await parser.extract_text(file["name"], content)
        summary = await summarizer.summarize(text)

        results.append({
            "file_name": file["name"],
            "summary": summary
        })

    report_path = await report.generate_csv(results)

    return {
        "status": "success",
        "report_path": report_path,
        "data": results
    }