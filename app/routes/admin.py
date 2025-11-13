from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.database import database
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ---------------------------
# Admin Registration Form Page
# ---------------------------
@router.get("/admin/register-form", response_class=HTMLResponse)
async def admin_register_form(request: Request):
    return templates.TemplateResponse("adminRegistration.html", {"request": request})


# ---------------------------
# Admin Registration POST
# ---------------------------
@router.post("/adminRegister")
async def admin_register(
    admin_name: str = Form(...),
    admin_email: str = Form(...),
    admin_password: str = Form(...)
):
    # Hash password
    hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode()

    # Insert admin into database
    query = """
        INSERT INTO admins (admin_name, admin_email, admin_password)
        VALUES (:admin_name, :admin_email, :admin_password)
    """
    values = {
        "admin_name": admin_name,
        "admin_email": admin_email,
        "admin_password": hashed_password
    }
    await database.execute(query=query, values=values)

    # Redirect to login page
    return RedirectResponse(url="/admin/login-form", status_code=302)


# ---------------------------
# Admin Login Form Page
# ---------------------------
@router.get("/admin/login-form", response_class=HTMLResponse)
async def admin_login_form(request: Request):
    return templates.TemplateResponse("adminLogin.html", {"request": request})


# ---------------------------
# Admin Login POST
# ---------------------------
@router.post("/adminLogin")
async def admin_login(
    request: Request,
    admin_name: str = Form(...),
    admin_password: str = Form(...)
):
    # Fetch admin by name
    query = "SELECT * FROM admins WHERE admin_name = :name"
    admin = await database.fetch_one(query=query, values={"name": admin_name})

    # Verify password
    if not admin or not bcrypt.checkpw(admin_password.encode('utf-8'), admin["admin_password"].encode('utf-8')):
        return templates.TemplateResponse(
            "adminLogin.html",
            {"request": request, "error": "Invalid name or password."},
            status_code=401
        )

    # Save admin_id to session
    request.session["admin_id"] = admin["admin_id"]

    return RedirectResponse(url="/admin/dashboard", status_code=302)


# ---------------------------
# Helper function to get logged-in admin
# ---------------------------
async def get_logged_in_admin(request: Request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return None
    query = "SELECT * FROM admins WHERE admin_id = :admin_id"
    return await database.fetch_one(query=query, values={"admin_id": admin_id})


# ---------------------------
# Admin Dashboard
# ---------------------------
@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    return templates.TemplateResponse(
        "adminDashboard.html",
        {"request": request, "admin": admin, "active_page": "dashboard"}
    )


# ---------------------------
# Manage Students Page
# ---------------------------
# ---------------------------
# Manage Students Page
# ---------------------------

@router.get("/admin/manage-students", response_class=HTMLResponse)
async def admin_students(request: Request):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    query = "SELECT * FROM students"
    students = await database.fetch_all(query)

    return templates.TemplateResponse(
        "adminStudents.html",
        {
            "request": request,
            "admin": admin,
            "students": students,
            "active_page": "students"
        }
    )

# Add Student
@router.post("/admin/add-student")
async def add_student(
    name: str = Form(...),
    roll_no: str = Form(...),
    class_id: int = Form(...),
    admission_year: int = Form(...),
    course_id: str = Form(...),
    is_eligible: int = Form(...)
):
    query = """
        INSERT INTO students (name, roll_no, class_id, admission_year, course_id, is_eligible, password)
        VALUES (:name, :roll_no, :class_id, :admission_year, :course_id, :is_eligible, :password)
    """
    values = {
        "name": name,
        "roll_no": roll_no,
        "class_id": class_id,
        "admission_year": admission_year,
        "course_id": course_id,
        "is_eligible": is_eligible,
        "password": "123456"
    }
    await database.execute(query, values)
    return JSONResponse(content={"message": "Student added successfully"})


@router.post("/admin/update-student")
async def update_student(
    student_id: int = Form(...),
    name: str = Form(...),
    roll_no: str = Form(...),
    class_id: int = Form(...),
    admission_year: int = Form(...),
    course_id: str = Form(...),
    is_eligible: int = Form(...)
):
    query = """
        UPDATE students
        SET name = :name,
            roll_no = :roll_no,
            class_id = :class_id,
            admission_year = :admission_year,
            course_id = :course_id,
            is_eligible = :is_eligible,
            password = "123456"
        WHERE student_id = :student_id
    """
    values = {
        "student_id": student_id,
        "name": name,
        "roll_no": roll_no,
        "class_id": class_id,
        "admission_year": admission_year,
        "course_id": course_id,
        "is_eligible": is_eligible,
    }
    await database.execute(query, values)
    return JSONResponse(content={"message": "Student updated successfully"})

@router.delete("/admin/delete-student/{student_id}")
async def delete_student(student_id: int):
    query = "DELETE FROM students WHERE student_id = :student_id"
    await database.execute(query, {"student_id": student_id})
    return JSONResponse(content={"message": "Student deleted successfully"})

# ---------------------------
# Manage Teachers Page
# ---------------------------

@router.get("/admin/manage-teachers", response_class=HTMLResponse)
async def admin_teachers(request: Request):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    query = "SELECT * FROM teachers order by teacher_id"
    teachers = await database.fetch_all(query)

    return templates.TemplateResponse(
        "adminTeachers.html",
        {
            "request": request,
            "admin": admin,
            "teachers": teachers,
            "active_page": "teachers"
        }
    )

@router.post("/admin/add-teacher")
async def add_teacher(name: str = Form(...)):
    query = "INSERT INTO teachers (name) VALUES (:name)"
    await database.execute(query, {"name": name})
    return JSONResponse(content={"message": "Teacher added successfully"})

@router.delete("/admin/delete-teacher/{teacher_id}")
async def delete_teacher(teacher_id: int):
    query = "DELETE FROM teachers WHERE teacher_id = :teacher_id"
    await database.execute(query, {"teacher_id": teacher_id})
    return JSONResponse(content={"message": "Teacher deleted successfully"})

@router.post("/admin/update-teacher")
async def update_teacher(teacher_id: int = Form(...), name: str = Form(...)):
    query = "UPDATE teachers SET name = :name WHERE teacher_id = :teacher_id"
    await database.execute(query, {"teacher_id": teacher_id, "name": name})
    return JSONResponse(content={"message": "Teacher updated successfully"})

# ---------------------------
# Admin Logout
# ---------------------------
@router.get("/admin/logout")
async def admin_logout(request: Request):
    request.session.pop("admin_id", None)
    return RedirectResponse(url="/admin/login-form", status_code=302)
