from fastapi import FastAPI


app = FastAPI()


@app.post("/api/v1/bank/get_balance")
def get_balance():
    ...


@app.get("/")
def read_root():
    return {"message": "ping pong!"}
