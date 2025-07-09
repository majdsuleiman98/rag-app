from fastapi import FastAPI
app = FastAPI()


def welcome_message():
    return {"message": "Welcome to the RAG-APP!"}

@app.get("/welcome")
def read_root():
    return welcome_message()