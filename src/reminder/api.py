from fastapi import FastAPI

app = FastAPI()

@app.get("/reminders")
async def get_reminders():
    return {"message": "Get reminders"}