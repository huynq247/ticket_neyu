from fastapi import FastAPI
import uvicorn

# Tạo app FastAPI đơn giản để kiểm tra
app = FastAPI(
    title="User Service Test",
    description="Test User Service API",
    version="0.1.0"
)

@app.get("/")
def read_root():
    """
    API root endpoint
    """
    return {"status": "ok", "service": "user-service-test"}

@app.get("/test")
def test_endpoint():
    """
    Test endpoint
    """
    return {"message": "This is a test endpoint"}

if __name__ == "__main__":
    uvicorn.run("test_server:app", host="0.0.0.0", port=8000, reload=True)