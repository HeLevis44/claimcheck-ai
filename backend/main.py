from fastapi import FastAPI

app = FastAPI(
    title="ClaimChecker AI API",
    description="Backend API for verifying whether generated claims are supported by source documents.",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}