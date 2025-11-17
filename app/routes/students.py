from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from app.database import database
from app.models import students
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ------------------ Student Registration ------------------
@router.post("/studentRegister")
async def register_student(
    name: str = Form(...),
    roll_number: str = Form(...),
    password: str = Form(...),
    admission_year: int = Form(...),
    class_id: int = Form(...)
):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    query = """
        INSERT INTO students (name, roll_no, password, admission_year, class_id)
        VALUES (:name, :roll_no, :password, :admission_year, :class_id)
    """
    await database.execute(query=query, values={
        "name": name,
        "roll_no": roll_number,
        "password": hashed_password,
        "admission_year": admission_year,
        "class_id": class_id
    })
    return RedirectResponse(url="/student/login-form", status_code=302)

# ------------------ Student Login ------------------
@router.post("/studentLogin")
async def login_student(request: Request, roll_number: str = Form(...), password: str = Form(...)):
    query = students.select().where(students.c.roll_no == roll_number)
    student = await database.fetch_one(query)
    if student and bcrypt.checkpw(password.encode('utf-8'), student["password"].encode('utf-8')):
        request.session["student_id"] = student["student_id"]
        return RedirectResponse(url="/studentDashboard", status_code=302)
    return templates.TemplateResponse("studentLogin.html", {
        "request": request,
        "error": "Incorrect roll number or password"
    })

# ------------------ SQL Queries ------------------
SQL_CLASS_AVERAGES = """
SELECT
    s.subject_name,
    CAST(AVG(f.rating) AS DECIMAL(10, 2)) AS average_rating,
    COUNT(DISTINCT f.student_id) AS total_students_rated
FROM
    feedback f
INNER JOIN
    students st ON f.student_id = st.student_id
INNER JOIN
    teacher_subjects ts ON f.teacher_subject_id = ts.id
INNER JOIN
    subjects s ON ts.subject_id = s.subject_id
WHERE
    st.class_id = :class_id
GROUP BY
    s.subject_name
ORDER BY
    average_rating DESC;
"""

SQL_STUDENT_ACTIVITY = """
SELECT
    s.subject_name,
    f.rating,
    f.updated_at AS feedback_time
FROM
    feedback f
INNER JOIN
    teacher_subjects ts ON f.teacher_subject_id = ts.id
INNER JOIN
    subjects s ON ts.subject_id = s.subject_id
WHERE
    f.student_id = :student_id
ORDER BY
    f.updated_at DESC
LIMIT 5;
"""

# ------------------ Student Dashboard ------------------
@router.get("/studentDashboard", response_class=HTMLResponse)
async def show_dashboard(request: Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/login", status_code=302)

    student_query = "SELECT * FROM students WHERE student_id = :student_id"
    student = await database.fetch_one(student_query, values={"student_id": student_id})
    class_id = student["class_id"]

    # Updated modules query (no class_subjects)
    modules_query = """
        SELECT ts.id AS teacher_subject_id, s.subject_name, t.name AS teacher_name,
               EXISTS(
                   SELECT 1 
                   FROM feedback f
                   WHERE f.student_id = :student_id
                     AND f.teacher_subject_id = ts.id
               ) AS feedback_given
        FROM teacher_subjects ts
        INNER JOIN subjects s ON ts.subject_id = s.subject_id
        INNER JOIN teachers t ON ts.teacher_id = t.teacher_id
        WHERE ts.class_id = :class_id
        ORDER BY s.subject_name
    """
    modules = await database.fetch_all(
        modules_query,
        values={"student_id": student_id, "class_id": class_id}
    )

    class_ratings = await database.fetch_all(SQL_CLASS_AVERAGES, values={"class_id": class_id})
    student_activity = await database.fetch_all(SQL_STUDENT_ACTIVITY, values={"student_id": student_id})

    return templates.TemplateResponse("studentDashboard.html", {
        "request": request,
        "student": student,
        "subjects": modules,
        "class_ratings": class_ratings,
        "student_activity": student_activity
    })

# ------------------ Module Rating ------------------
@router.get("/module-rating", response_class=HTMLResponse)
async def module_rating(request: Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/login", status_code=302)

    student_query = "SELECT * FROM students WHERE student_id = :student_id"
    student = await database.fetch_one(student_query, values={"student_id": student_id})
    class_id = student["class_id"]

    modules_query = """
        SELECT ts.id AS teacher_subject_id, s.subject_name, t.name AS teacher_name
        FROM teacher_subjects ts
        INNER JOIN subjects s ON ts.subject_id = s.subject_id
        INNER JOIN teachers t ON ts.teacher_id = t.teacher_id
        WHERE ts.class_id = :class_id
        ORDER BY s.subject_name
    """
    modules = await database.fetch_all(modules_query, values={"class_id": class_id})

    updated_modules = []
    for module in modules:
        module_dict = dict(module)
        feedback_query = """
            SELECT AVG(rating) AS student_avg
            FROM feedback
            WHERE teacher_subject_id = :teacher_subject_id
              AND student_id = :student_id
        """
        result = await database.fetch_one(feedback_query, values={
            "teacher_subject_id": module_dict["teacher_subject_id"],
            "student_id": student_id
        })
        module_dict["student_avg_rating"] = round(result["student_avg"] if result and result["student_avg"] else 0, 1)
        updated_modules.append(module_dict)

    return templates.TemplateResponse("studentModuleRating.html", {
        "request": request,
        "student": student,
        "modules": updated_modules
    })

# ------------------ Rate Subject ------------------
@router.get("/rate/{teacher_subject_id}", response_class=HTMLResponse)
async def rate_subject(request: Request, teacher_subject_id: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return RedirectResponse(url="/login", status_code=302)

    student = await database.fetch_one(
        "SELECT * FROM students WHERE student_id = :student_id",
        {"student_id": student_id}
    )
    class_id = student["class_id"]

    check_query = """
        SELECT ts.id
        FROM teacher_subjects ts
        WHERE ts.id = :teacher_subject_id
          AND ts.class_id = :class_id
    """
    valid = await database.fetch_one(check_query, {"teacher_subject_id": teacher_subject_id, "class_id": class_id})
    if not valid:
        raise HTTPException(status_code=403, detail="You cannot rate this subject")

    questions = await database.fetch_all("SELECT * FROM questions ORDER BY question_id ASC")

    sub_query = """
        SELECT ts.id AS teacher_subject_id, s.subject_name, t.name AS teacher_name
        FROM teacher_subjects ts
        JOIN subjects s ON ts.subject_id = s.subject_id
        JOIN teachers t ON ts.teacher_id = t.teacher_id
        WHERE ts.id = :teacher_subject_id
    """
    subject = await database.fetch_one(sub_query, {"teacher_subject_id": teacher_subject_id})

    return templates.TemplateResponse("rate.html", {
        "request": request,
        "questions": questions,
        "subject": subject
    })

# ------------------ Submit Feedback ------------------
@router.post("/submit-feedback")
async def submit_feedback(request: Request, teacher_subject_id: int = Form(...)):
    student_id = request.session.get("student_id")
    if not student_id:
        raise HTTPException(status_code=401, detail="Student not logged in")

    form = await request.form()
    responses = {}
    for key, value in form.items():
        if key.startswith("responses[") and value:
            qid = int(key.replace("responses[", "").replace("]", ""))
            responses[qid] = int(value)

    delete_query = """
        DELETE FROM feedback
        WHERE student_id = :student_id
          AND teacher_subject_id = :teacher_subject_id
    """
    await database.execute(delete_query, values={
        "student_id": student_id,
        "teacher_subject_id": teacher_subject_id
    })

    insert_query = """
        INSERT INTO feedback (student_id, teacher_subject_id, question_id, rating)
        VALUES (:student_id, :teacher_subject_id, :question_id, :rating)
    """
    for qid, rating in responses.items():
        await database.execute(insert_query, values={
            "student_id": student_id,
            "teacher_subject_id": teacher_subject_id,
            "question_id": qid,
            "rating": rating
        })

    return RedirectResponse(url="/module-rating", status_code=303)

# ------------------ Logout ------------------
@router.get("/logout")
async def logout(request: Request):
    request.session.pop("student_id", None)
    return RedirectResponse(url="/student/login-form", status_code=302)