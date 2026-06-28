import time
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✏️ FILL IN YOUR DETAILS HERE:
MY_EMAIL = "22f3003131@ds.study.iitm.ac.in"   # your IITM login email
ALLOWED_ORIGIN =  "https://dash-jnu0hl.example.com"   # from the TDS panel

# ─── CORS Middleware ───────────────────────────────────────────────────────────
# This is the "bouncer" — it checks WHERE a request is coming from.
# Only requests from ALLOWED_ORIGIN get the Access-Control-Allow-Origin header.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],   # ← only this origin is allowed, no wildcard *
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# ─── Main Endpoint ─────────────────────────────────────────────────────────────
@app.get("/stats")
def get_stats(values: str, request: Request):
    start_time = time.time()  # start the stopwatch

    # Parse the comma-separated numbers, e.g. "1,2,3" → [1, 2, 3]
    nums = [int(v.strip()) for v in values.split(",")]

    count = len(nums)
    total = sum(nums)
    minimum = min(nums)
    maximum = max(nums)
    mean = total / count

    process_time = time.time() - start_time  # how long did this take?

    return Response(
        content=f'{{"email":"{"22f3003131@ds.study.iitm.ac.in"}","count":{count},"sum":{total},"min":{minimum},"max":{maximum},"mean":{mean:.6f}}}',
        media_type="application/json",
        headers={
            "X-Request-ID": str(uuid.uuid4()),       # unique ID for this request
            "X-Process-Time": f"{process_time:.6f}", # time in seconds
        }
    )