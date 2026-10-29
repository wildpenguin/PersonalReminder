from fastapi import FastAPI

app = FastAPI()

@app.get("/reminders/{id}")
async def get_reminders(id: int):
    return {"message": f"Get reminders - {id}"}