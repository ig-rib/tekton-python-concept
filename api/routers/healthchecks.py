from fastapi import APIRouter


healthchecks_router = APIRouter()

@healthchecks_router.get("/", status_code=200)
def main_status_check():
    return {"Status_What?": "OK --> What?"}