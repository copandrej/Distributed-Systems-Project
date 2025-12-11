import numpy as np
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Echo Service"}

@app.post("/echo")
async def echo(request: Request):
    size = 100
    try:
        body = await request.json()
    except Exception:
        body = await request.body()
        body = body.decode()
    
    # Simulate computational load
    # Create two random matrices of size x size
    matrix_a = np.random.rand(size, size)
    matrix_b = np.random.rand(size, size)
    # Perform matrix multiplication
    _ = np.dot(matrix_a, matrix_b)

    return {"echo": body}
