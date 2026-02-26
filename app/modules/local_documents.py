import os
import io
from pathlib import Path
import fitz
import docx

class LocalDocumentService:
    
    def __init__(self, documents_folder: str = "documents"):
        self.documents_folder = documents_folder
        # Create folder if it doesn't exist
        Path(self.documents_folder).mkdir(parents=True, exist_ok=True)
    
    async def list_files(self):
        """List all files in the local documents folder"""
        files = []
        
        if not os.path.exists(self.documents_folder):
            return files
        
        for filename in os.listdir(self.documents_folder):
            filepath = os.path.join(self.documents_folder, filename)
            
            # Only include files, not directories
            if os.path.isfile(filepath):
                file_ext = os.path.splitext(filename)[1].lower()
                
                # Only include supported file types
                if file_ext in ['.pdf', '.docx', '.txt', '.doc']:
                    files.append({
                        "name": filename,
                        "mimeType": self._get_mime_type(file_ext),
                        "path": filepath
                    })
        
        return files
    
    async def download_file(self, file: dict):
        """Download (read) a file from the local documents folder"""
        filepath = os.path.join(self.documents_folder, file["name"])
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, "rb") as f:
            file_data = io.BytesIO(f.read())
        
        return file_data

    async def extract_text(self, filename: str, file_content) -> str:
        """Extract text from any supported file type"""
        file_ext = os.path.splitext(filename)[1].lower()
        
        try:
            if file_ext == ".pdf":
                return self._extract_text_from_pdf(file_content)
            elif file_ext == ".docx":
                return self._extract_text_from_docx(file_content)
            elif file_ext == ".txt":
                return file_content.read().decode("utf-8")
            elif file_ext == ".doc":
                return f"DOC files require python-docx or similar library. Please convert to DOCX."
            else:
                return f"Unsupported file type: {file_ext}"
        except Exception as e:
            return f"Error reading {filename}: {str(e)}"

    def _extract_text_from_pdf(self, file_content) -> str:
        """Extract text from PDF using pymupdf"""
        try:
            file_content.seek(0)
            doc = fitz.open(stream=file_content.read(), filetype="pdf")
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    def _extract_text_from_docx(self, file_content) -> str:
        """Extract text from DOCX file"""
        try:
            file_content.seek(0)
            document = docx.Document(file_content)
            text = "\n".join(p.text for p in document.paragraphs)
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def _get_mime_type(self, extension: str) -> str:
        """Map file extensions to MIME types"""
        mime_types = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.doc': 'application/msword',
            '.txt': 'text/plain'
        }
        return mime_types.get(extension, 'application/octet-stream')
