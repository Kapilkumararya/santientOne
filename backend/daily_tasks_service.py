from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/plan_trip")
async def plan_trip(destination: str, start_date: str, end_date: str):
    # Logic to plan a trip
    return {"message": "Trip planned successfully", "destination": destination, "start_date": start_date, "end_date": end_date}

@app.post("/budget")
async def budget(income: float, expenses: list):
    # Logic to calculate budget
    return {"message": "Budget calculated successfully", "income": income, "expenses": expenses}

@app.post("/repair_advice")
async def repair_advice(issue: str):
    # Logic to provide repair advice
    return {"message": "Repair advice provided", "issue": issue}