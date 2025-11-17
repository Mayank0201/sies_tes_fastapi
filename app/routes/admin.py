from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.database import database
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# admin registration form page
@router.get("/admin/register-form", response_class=HTMLResponse)
async def admin_register_form(request: Request):
    # fetch all courses for dropdown
    query = "SELECT course_id, course_name FROM courses ORDER BY course_name"
    rows = await database.fetch_all(query)
    courses = [dict(r) for r in rows]

    return templates.TemplateResponse(
        "adminRegistration.html",
        {"request": request, "courses": courses}
    )

# admin registration post
@router.post("/adminRegister")
async def admin_register(
    admin_name: str = Form(...),
    admin_email: str = Form(...),
    admin_password: str = Form(...),
    confirm_password: str = Form(...),
    course_id: int = Form(...)
):

    if admin_password != confirm_password:
        return templates.TemplateResponse(
            "adminRegistration.html",
            {
                "request": Request,
                "error": "Passwords do not match."
            },
            status_code=400
        )

    hashed_password = bcrypt.hashpw(
        admin_password.encode("utf-8"), bcrypt.gensalt()
    ).decode()

    query = """
        INSERT INTO admins (admin_name, admin_email, admin_password, course_id)
        VALUES (:admin_name, :admin_email, :admin_password, :course_id)
    """
    values = {
        "admin_name": admin_name,
        "admin_email": admin_email,
        "admin_password": hashed_password,
        "course_id": course_id
    }

    await database.execute(query=query, values=values)

    return RedirectResponse(url="/admin/login-form", status_code=302)

# admin login page
@router.get("/admin/login-form", response_class=HTMLResponse)
async def admin_login_form(request: Request):
    return templates.TemplateResponse("adminLogin.html", {"request": request})

# admin login post
@router.post("/adminLogin")
async def admin_login(
    request: Request,
    admin_name: str = Form(...),
    admin_password: str = Form(...)
):
    query = "SELECT * FROM admins WHERE admin_name = :name"
    admin = await database.fetch_one(query=query, values={"name": admin_name})

    if not admin or not bcrypt.checkpw(
        admin_password.encode("utf-8"),
        admin["admin_password"].encode("utf-8")
    ):
        return templates.TemplateResponse(
            "adminLogin.html",
            {"request": request, "error": "Invalid name or password."},
            status_code=401,
        )

    # save admin in session including course_id
    request.session["admin_id"] = admin["admin_id"]
    request.session["course_id"] = admin["course_id"]

    return RedirectResponse(url="/admin/dashboard", status_code=302)

# helper function
async def get_logged_in_admin(request: Request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return None

    query = "SELECT * FROM admins WHERE admin_id = :admin_id"
    return await database.fetch_one(query=query, values={"admin_id": admin_id})

# dashboard
@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    return templates.TemplateResponse(
        "adminDashboard.html",
        {"request": request, "admin": admin, "active_page": "dashboard"},
    )

# manage students page
@router.get("/admin/manage-students", response_class=HTMLResponse)
async def admin_students(request: Request):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    query = """
        SELECT s.*
        FROM students s
        JOIN classes c ON s.class_id = c.class_id
        WHERE c.course_id = :course_id
        ORDER BY s.student_id
    """

    students = await database.fetch_all(
        query=query,
        values={"course_id": admin["course_id"]}
    )

    return templates.TemplateResponse(
        "adminStudents.html",
        {"request": request, "admin": admin, "students": students, "active_page": "students"},
    )

# add student
@router.post("/admin/add-student")
async def add_student(
    name: str = Form(...),
    roll_no: str = Form(...),
    class_id: int = Form(...),
    admission_year: int = Form(...),
    course_id: int = Form(...),
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

# update student
@router.post("/admin/update-student")
async def update_student(
    student_id: int = Form(...),
    name: str = Form(...),
    roll_no: str = Form(...),
    class_id: int = Form(...),
    admission_year: int = Form(...),
    course_id: int = Form(...),
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
        "is_eligible": is_eligible
    }

    await database.execute(query, values)
    return JSONResponse(content={"message": "Student updated successfully"})

# delete student
@router.delete("/admin/delete-student/{student_id}")
async def delete_student(student_id: int):
    query = "DELETE FROM students WHERE student_id = :student_id"
    await database.execute(query, {"student_id": student_id})
    return JSONResponse(content={"message": "Student deleted successfully"})

# manage teachers page
@router.get("/admin/manage-teachers", response_class=HTMLResponse)
async def admin_teachers(request: Request):
    admin = await get_logged_in_admin(request)
    if not admin:
        return RedirectResponse(url="/admin/login-form", status_code=302)

    query = """
    SELECT *
    FROM teachers
    WHERE course_id = :course_id
    ORDER BY teacher_id
    """

    teachers = await database.fetch_all(
        query=query,
        values={"course_id": admin["course_id"]}
    )

    return templates.TemplateResponse(
        "adminTeachers.html",
        {"request": request, "admin": admin, "teachers": teachers, "active_page": "teachers"},
    )

# add teacher
@router.post("/admin/add-teacher")
async def add_teacher(request: Request):
    form = await request.form()
    name = form.get("name")
    course_id = int(form.get("course_id"))

    query = "INSERT INTO teachers (name, course_id) VALUES (:name, :course_id)"
    await database.execute(query, values={"name": name, "course_id": course_id})

    return JSONResponse(content={"message": "Teacher added successfully"})

# update teacher
@router.post("/admin/update-teacher")
async def update_teacher(
    teacher_id: int = Form(...),
    name: str = Form(...)
):
    query = "UPDATE teachers SET name = :name WHERE teacher_id = :teacher_id"
    await database.execute(query, {"teacher_id": teacher_id, "name": name})
    return JSONResponse(content={"message": "Teacher updated successfully"})

# delete teacher
@router.delete("/admin/delete-teacher/{teacher_id}")
async def delete_teacher(teacher_id: int):
    query = "DELETE FROM teachers WHERE teacher_id = :teacher_id"
    await database.execute(query, {"teacher_id": teacher_id})
    return JSONResponse(content={"message": "Teacher deleted successfully"})

# admin logout
@router.get("/admin/logout")
async def admin_logout(request: Request):
    request.session.pop("admin_id", None)
    request.session.pop("course_id", None)
    return RedirectResponse(url="/admin/login-form", status_code=302)
