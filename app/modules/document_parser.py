import fitz
import docx

class DocumentParser:

    async def extract_text(self, filename: str, file_content):

        if filename.endswith(".pdf"):
            doc = fitz.open(stream=file_content.read(), filetype="pdf")
            return " ".join(page.get_text() for page in doc)

        elif filename.endswith(".docx"):
            document = docx.Document(file_content)
            return "\n".join(p.text for p in document.paragraphs)

        elif filename.endswith(".txt"):
            return file_content.read().decode("utf-8")

        return ""