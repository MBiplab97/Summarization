# 📄 Document Summarizer

A powerful web application for extracting, processing, and summarizing documents from Google Drive and local sources using AI-powered summarization.

## 🌟 Features

- **📦 Multiple Document Sources**
  - Google Drive integration with OAuth2 authentication
  - Local file uploads and processing
  
- **📝 Document Format Support**
  - PDF files
  - DOCX (Word documents)
  - TXT (Plain text files)

- **🤖 AI-Powered Summarization**
  - Intelligent document summarization using Ollama
  - LLaMA 3.2 Vision model for advanced processing
  - Async processing for improved performance

- **📊 Export & Reporting**
  - Generate CSV reports with summaries
  - Batch document processing
  - Summary delivery and download

- **🔧 Modern Architecture**
  - FastAPI async backend with type hints
  - Streamlit web UI
  - RESTful API endpoints
  - Docker containerization support

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **Uvicorn** - ASGI web server
- **Ollama** - Local AI model inference
- **Google API Client** - Google Drive integration
- **PyMuPDF** - PDF processing
- **python-docx** - Word document parsing

### Frontend
- **Streamlit** - Interactive web UI framework

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Python 3.11+** - Runtime

## 📋 Prerequisites

### Required
- Python 3.11 or higher
- pip or conda package manager
- Ollama (for AI summarization) - [Download here](https://ollama.ai)

### For Google Drive Integration
- Google Cloud Project with Drive API enabled
- OAuth 2.0 credentials (Client ID & Secret)

## 🚀 Installation & Setup

### Option 1: Local Development Setup

#### 1. Clone the Repository
```bash
git clone <repo_url>
cd <repo_folder>
```

#### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Start Ollama Service
Ollama must be running to power the summarization. In a separate terminal:
```bash
ollama serve
```

Then pull the required model:
```bash
ollama pull llama3.2-vision
```

#### 5. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GOOGLE_CLIENT_ID=<your_client_id>
GOOGLE_CLIENT_SECRET=<your_client_secret>
```

#### 6. Run the Backend
```bash
python app/main.py
```
The API will be available at `http://localhost:8000`

#### 7. Run the Streamlit UI (in another terminal)
Navigate to the Streamlit directory:
```bash
streamlit run streamlit_ui/ui.py
```
The UI will be accessible at `http://localhost:8501`

### Option 2: Docker Deployment

#### Prerequisites
- Docker & Docker Compose installed
- Ollama running on your machine

#### Run with Docker Compose
```bash
docker-compose up
```

This will start:
- Backend API on `http://localhost:8000`
- Streamlit UI on `http://localhost:8501`

## ⚙️ Configuration

### Google Drive Setup

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable the Google Drive API

2. **Generate OAuth 2.0 Credentials**
   - Navigate to Credentials
   - Create OAuth 2.0 Client ID
   - Choose "Desktop application" as the application type
   - Download the credentials JSON file

3. **Configure in Application**
   - Place credentials in the project root
   - Update environment variables with Client ID and Secret

### Ollama Model Configuration

The application uses `llama3.2-vision` by default. To customize:
- Edit `app/modules/summarizer.py`
- Modify the `model` parameter in `SummarizerService.__init__()`

Available models can be viewed at [Ollama Library](https://ollama.ai/library)

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Health Check
```
GET /health
```
Returns: `{"status": "healthy"}`

### Summarize Folder
```
POST /summarize-folder
```

**Parameters:**
- `source` (string): `"google_drive"` or `"local"` (default: `"google_drive"`)
- `folder_id` (string): Google Drive folder ID (required if source is `google_drive`)

**Response:**
```json
{
  "documents": [
    {
      "filename": "document.pdf",
      "summary": "Generated summary...",
      "length": 450
    }
  ],
  "csv_report": "base64_encoded_csv"
}
```

## 📁 Project Structure

```
Summarization/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── api/
│   │   └── summarization.py    # API routes
│   ├── models/
│   │   └── entities.py         # Data models
│   └── modules/
│       ├── google_drive.py     # Google Drive integration
│       ├── local_documents.py  # Local file handling
│       ├── summarizer.py       # AI summarization service
│       ├── report_generator.py # CSV report generation
│       └── utils.py            # Utility functions
├── streamlit_ui/
│   └── ui.py                   # Streamlit web interface
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose orchestration
└── README.md                   # This file
```

## 🎯 Usage

### Web Interface (Streamlit)
1. Open `http://localhost:8501` in your browser
2. Select document source:
   - **Google Drive**: Enter folder ID and authenticate
   - **Local Documents**: Upload files from your computer
3. Click "Summarize" to process documents
4. Download the CSV report with summaries

```

## 🔧 Troubleshooting

### Ollama Connection Error
**Problem**: "Could not connect to Ollama"

**Solution**:
- Ensure Ollama is running: `ollama serve`
- Verify it's running on default port (11434)
- Check firewall settings

### Google Drive Authentication Issues
**Problem**: OAuth redirect fails or credentials not found

**Solution**:
- Verify credentials file is in the correct location
- Ensure Client ID and Secret are correct
- Delete the cached token and re-authenticate

### Port Already in Use
**Problem**: "Address already in use"

**Solution**:
```bash
# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Model Download Issues
**Problem**: "Model not found" error

**Solution**:
```bash
ollama pull llama3.2-vision
```

## 📦 Dependencies

See [requirements.txt](requirements.txt) for the complete list of dependencies:
- FastAPI, Uvicorn (API framework)
- Streamlit (Web UI)
- Google Auth libraries (Google Drive integration)
- PyMuPDF, python-docx (Document parsing)
- Ollama (AI inference)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ❓ Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section above

## 🔗 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Google Drive API Documentation](https://developers.google.com/drive/api)

---