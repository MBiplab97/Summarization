# Document Summarizer via Google Drive Integration

## Features
- Google Drive OAuth2 integration
- PDF, DOCX, TXT parsing
- AI-powered summarization
- CSV report download
- FastAPI async backend
- Streamlit UI
- Docker support

## Setup

### 1. Clone repo
git clone <repo_url>

### 2. Create virtual env
python -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Add credentials.json
Place Google service account credentials file in root.

### 5. Run backend
uvicorn app.app:app --reload

### 6. Run Streamlit
streamlit run streamlit_ui/ui.py