from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

API_KEY = "ak_r2t1pyglsgzq7pwijeptbepd"

app = FastAPI()

# Allow browser-based grading
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"}
        )

    total_events = len(request.events)

    unique_users = len({e.user for e in request.events})

    revenue = 0.0

    user_totals = {}

    for e in request.events:
        if e.amount > 0:
            revenue += e.amount
            user_totals[e.user] = user_totals.get(e.user, 0) + e.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": "24f2005647@ds.study.iitm.ac.in",
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }
