# app/main.py

from fastapi import FastAPI
from app.database import database
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from app.routes import students
from app.routes import admin
from app.routes import feedback


app = FastAPI()

# Add session middleware (use a strong secret key)
app.add_middleware(SessionMiddleware, secret_key="VinodKamrajAcharya")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/student/register-form")
def student_register_form(request: Request):
    return templates.TemplateResponse("studentRegistration.html", {"request": request})

@app.get("/admin/register-form")
def admin_register_form(request: Request):
    return templates.TemplateResponse("adminRegistration.html", {"request": request})

@app.get("/get-courses/{stream_id}")
async def get_courses_by_stream(stream_id: int):
    query = "SELECT course_id AS id, course_name AS name FROM courses WHERE stream_id = :stream_id"
    result = await database.fetch_all(query=query, values={"stream_id": stream_id})
    return JSONResponse(content={"courses": [dict(row) for row in result]})

@app.get("/get-classes/{course_id}")
async def get_classes(course_id: int):
    query = "SELECT class_id AS id, class_name AS name FROM classes WHERE course_id = :course_id"
    rows = await database.fetch_all(query, {"course_id": course_id})
    return JSONResponse(content={"classes": [dict(row) for row in rows]})

@app.get("/student/login-form")
def student_login_form(request: Request):
    return templates.TemplateResponse("studentLogin.html", {"request": request})

@app.get("/admin/login-form")
def admin_login_form(request: Request):
    return templates.TemplateResponse("adminLogin.html", {"request": request})



@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(students.router)
app.include_router(admin.router)
app.include_router(feedback.router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hello")
def say_hello():
    return {"message": "Hello student!"}