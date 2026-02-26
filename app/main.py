# Import routes after all other imports to avoid circular dependency
from fastapi import FastAPI
from api import summarization

# Create FastAPI instance
app = FastAPI(title="Document Summarizer")

# Include the router
app.include_router(summarization.router, prefix="/api")

# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)