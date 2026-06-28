import time
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI()

MY_EMAIL = "22f3003131@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-jnu0hl.example.com"

@app.options("/stats")
async def preflight(request: Request):
    origin = request.headers.get("origin", "")
    if origin == ALLOWED_ORIGIN:
        return Response(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )
    # Evil origin — return no ACAO header
    return Response(status_code=403)

@app.get("/stats")
async def get_stats(values: str, request: Request):
    start_time = time.time()

    nums = [int(v.strip()) for v in values.split(",")]
    count = len(nums)
    total = sum(nums)
    minimum = min(nums)
    maximum = max(nums)
    mean = total / count

    process_time = time.time() - start_time

    origin = request.headers.get("origin", "")
    headers = {
        "X-Request-ID": str(uuid.uuid4()),
        "X-Process-Time": f"{process_time:.6f}",
    }
    if origin == ALLOWED_ORIGIN:
        headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    return Response(
        content=f'{{"email":"{MY_EMAIL}","count":{count},"sum":{total},"min":{minimum},"max":{maximum},"mean":{mean:.6f}}}',
        media_type="application/json",
        headers=headers,
    )