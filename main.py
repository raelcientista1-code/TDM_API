from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "TDM API rodando"}