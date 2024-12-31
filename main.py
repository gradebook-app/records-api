from fastapi import FastAPI

from routers.grades.controller import router as grades_router

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

app.include_router(grades_router, prefix="/grades")


@app.get("/")
def health_checkpoint():
    return {"Status": "All Systems Operational"}
