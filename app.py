from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import os

# ─────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────

class Course:
    def __init__(self, id, name, skills, difficulty, duration):
        self.id = id
        self.name = name
        self.skills = skills
        self.difficulty = difficulty
        self.duration = duration

class Resource:
    def __init__(self, id, title, type, url, course_id):
        self.id = id
        self.title = title
        self.type = type
        self.url = url
        self.course_id = course_id

class User:
    def __init__(self, goal, skills, level, time):
        self.goal = goal
        self.skills = skills
        self.level = level
        self.available_time = time
    def has_skill(self, skill_id):
        return skill_id in self.skills

# ─────────────────────────────────────────────
# DATA LOADER (inline JSON — no file I/O needed on deploy)
# ─────────────────────────────────────────────

SKILLS_DATA = [
  {"id":"python_basic","name":"Python Basic","level":1},
  {"id":"python_advanced","name":"Python Advanced","level":2},
  {"id":"sql","name":"SQL","level":2},
  {"id":"data_structures","name":"Data Structures","level":2},
  {"id":"etl","name":"ETL","level":3},
  {"id":"data_warehouse","name":"Data Warehouse","level":3},
  {"id":"big_data","name":"Big Data","level":3},
  {"id":"machine_learning","name":"Machine Learning","level":3},
  {"id":"html","name":"HTML","level":1},
  {"id":"css","name":"CSS","level":1},
  {"id":"javascript","name":"JavaScript","level":2},
  {"id":"react","name":"React","level":2},
  {"id":"backend","name":"Backend","level":2},
  {"id":"api","name":"API","level":2}
]

COURSES_DATA = [
  {"id":"c1","name":"Advanced React","skills":["react"],"difficulty":2,"duration":22},
  {"id":"c2","name":"Python Basic Bootcamp","skills":["python_basic"],"difficulty":1,"duration":19},
  {"id":"c3","name":"CSS Fundamentals","skills":["css"],"difficulty":1,"duration":18},
  {"id":"c4","name":"Python Advanced Practical Guide","skills":["python_advanced"],"difficulty":2,"duration":9},
  {"id":"c5","name":"HTML Bootcamp","skills":["html"],"difficulty":1,"duration":21},
  {"id":"c6","name":"Intro to Python Basic","skills":["python_basic"],"difficulty":1,"duration":13},
  {"id":"c7","name":"Advanced SQL","skills":["sql"],"difficulty":2,"duration":12},
  {"id":"c8","name":"React Fundamentals","skills":["react"],"difficulty":2,"duration":22},
  {"id":"c9","name":"Python Basic for Beginners","skills":["python_basic"],"difficulty":1,"duration":14},
  {"id":"c10","name":"Data Warehouse Fundamentals","skills":["data_warehouse"],"difficulty":3,"duration":16},
  {"id":"c11","name":"ETL Fundamentals","skills":["etl"],"difficulty":3,"duration":14},
  {"id":"c12","name":"React Practical Guide","skills":["react"],"difficulty":2,"duration":14},
  {"id":"c13","name":"ETL Bootcamp","skills":["etl"],"difficulty":3,"duration":24},
  {"id":"c14","name":"Big Data for Beginners","skills":["big_data"],"difficulty":3,"duration":9},
  {"id":"c15","name":"Big Data Bootcamp","skills":["big_data"],"difficulty":3,"duration":9},
  {"id":"c16","name":"Intro to Python Advanced","skills":["python_advanced"],"difficulty":2,"duration":12},
  {"id":"c17","name":"API Bootcamp","skills":["api"],"difficulty":2,"duration":18},
  {"id":"c18","name":"Data Structures Bootcamp","skills":["data_structures"],"difficulty":2,"duration":17},
  {"id":"c19","name":"Intro to API","skills":["api"],"difficulty":2,"duration":12},
  {"id":"c20","name":"Advanced Data Structures","skills":["data_structures"],"difficulty":2,"duration":19},
  {"id":"c21","name":"Advanced HTML","skills":["html"],"difficulty":1,"duration":19},
  {"id":"c22","name":"CSS Practical Guide","skills":["css"],"difficulty":1,"duration":18},
  {"id":"c23","name":"Machine Learning for Beginners","skills":["machine_learning"],"difficulty":3,"duration":11},
  {"id":"c24","name":"Advanced Data Warehouse","skills":["data_warehouse"],"difficulty":3,"duration":15},
  {"id":"c25","name":"ETL Practical Guide","skills":["etl"],"difficulty":3,"duration":20},
  {"id":"c26","name":"Data Warehouse Bootcamp","skills":["data_warehouse"],"difficulty":3,"duration":16},
  {"id":"c27","name":"Intro to CSS","skills":["css"],"difficulty":1,"duration":18},
  {"id":"c28","name":"SQL for Beginners","skills":["sql"],"difficulty":2,"duration":20},
  {"id":"c29","name":"Intro to SQL","skills":["sql"],"difficulty":2,"duration":10},
  {"id":"c30","name":"Backend Fundamentals","skills":["backend"],"difficulty":2,"duration":13},
  {"id":"c31","name":"React for Beginners","skills":["react"],"difficulty":2,"duration":24},
  {"id":"c32","name":"Big Data Fundamentals","skills":["big_data"],"difficulty":3,"duration":15},
  {"id":"c33","name":"Data Structures Fundamentals","skills":["data_structures"],"difficulty":2,"duration":12},
  {"id":"c34","name":"Advanced Python Advanced","skills":["python_advanced"],"difficulty":2,"duration":24},
  {"id":"c35","name":"HTML Fundamentals","skills":["html"],"difficulty":1,"duration":20},
  {"id":"c36","name":"Python Basic Fundamentals","skills":["python_basic"],"difficulty":1,"duration":23},
  {"id":"c37","name":"JavaScript for Beginners","skills":["javascript"],"difficulty":2,"duration":25},
  {"id":"c38","name":"Intro to ETL","skills":["etl"],"difficulty":3,"duration":20},
  {"id":"c39","name":"Backend Practical Guide","skills":["backend"],"difficulty":2,"duration":23},
  {"id":"c40","name":"Advanced JavaScript","skills":["javascript"],"difficulty":2,"duration":18},
  {"id":"c41","name":"Python Advanced for Beginners","skills":["python_advanced"],"difficulty":2,"duration":23},
  {"id":"c42","name":"Backend Bootcamp","skills":["backend"],"difficulty":2,"duration":20},
  {"id":"c43","name":"Advanced Backend","skills":["backend"],"difficulty":2,"duration":11},
  {"id":"c44","name":"ETL for Beginners","skills":["etl"],"difficulty":3,"duration":12},
  {"id":"c45","name":"JavaScript Bootcamp","skills":["javascript"],"difficulty":2,"duration":15},
  {"id":"c46","name":"Advanced Python Basic","skills":["python_basic"],"difficulty":1,"duration":17},
  {"id":"c47","name":"Intro to Big Data","skills":["big_data"],"difficulty":3,"duration":18},
  {"id":"c48","name":"Intro to JavaScript","skills":["javascript"],"difficulty":2,"duration":25},
  {"id":"c49","name":"Python Basic Practical Guide","skills":["python_basic"],"difficulty":1,"duration":20},
  {"id":"c50","name":"Data Structures for Beginners","skills":["data_structures"],"difficulty":2,"duration":13},
  {"id":"c51","name":"Advanced API","skills":["api"],"difficulty":2,"duration":21},
  {"id":"c52","name":"React Bootcamp","skills":["react"],"difficulty":2,"duration":18},
  {"id":"c53","name":"HTML Practical Guide","skills":["html"],"difficulty":1,"duration":20},
  {"id":"c54","name":"Python Advanced Bootcamp","skills":["python_advanced"],"difficulty":2,"duration":9},
  {"id":"c55","name":"Machine Learning Practical Guide","skills":["machine_learning"],"difficulty":3,"duration":13},
  {"id":"c56","name":"Advanced Machine Learning","skills":["machine_learning"],"difficulty":3,"duration":9},
  {"id":"c57","name":"Machine Learning Bootcamp","skills":["machine_learning"],"difficulty":3,"duration":25},
  {"id":"c58","name":"Big Data Practical Guide","skills":["big_data"],"difficulty":3,"duration":14},
  {"id":"c59","name":"API for Beginners","skills":["api"],"difficulty":2,"duration":10},
  {"id":"c60","name":"API Fundamentals","skills":["api"],"difficulty":2,"duration":12}
]

PREREQUISITES_DATA = []  # empty — add if needed

RESOURCES_DATA = [
  {"id":"r1","title":"CSS Tricks Guide","type":"MOOC","url":"https://css-tricks.com/","course_id":"c22"},
  {"id":"r2","title":"Python for Everybody","type":"MOOC","url":"https://www.coursera.org/specializations/python","course_id":"c2"},
  {"id":"r3","title":"React Official Docs","type":"Book","url":"https://react.dev/learn","course_id":"c1"},
  {"id":"r4","title":"NodeJS Learn","type":"MOOC","url":"https://nodejs.dev/en/learn/","course_id":"c39"},
  {"id":"r5","title":"SQLBolt Interactive Tutorial","type":"Book","url":"https://sqlbolt.com/","course_id":"c28"},
  {"id":"r7","title":"Effective Python Book","type":"Book","url":"https://effectivepython.com/","course_id":"c54"},
  {"id":"r8","title":"freeCodeCamp HTML Course","type":"Article","url":"https://www.freecodecamp.org/learn/responsive-web-design/","course_id":"c35"},
  {"id":"r9","title":"Python Advanced Topics","type":"Video","url":"https://www.datacamp.com/courses/intermediate-python","course_id":"c34"},
  {"id":"r10","title":"Data Engineering Foundations","type":"Book","url":"https://www.coursera.org/learn/data-engineering-foundations","course_id":"c44"},
  {"id":"r11","title":"React freeCodeCamp","type":"Book","url":"https://www.freecodecamp.org/news/learn-react-course/","course_id":"c8"},
  {"id":"r12","title":"freeCodeCamp HTML Course","type":"MOOC","url":"https://www.freecodecamp.org/learn/responsive-web-design/","course_id":"c5"},
  {"id":"r13","title":"MDN JavaScript Guide","type":"Video","url":"https://developer.mozilla.org/en-US/docs/Web/JavaScript","course_id":"c37"},
  {"id":"r14","title":"Apache Spark Documentation","type":"Book","url":"https://spark.apache.org/docs/latest/","course_id":"c47"},
  {"id":"r15","title":"JavaScript Info","type":"Video","url":"https://javascript.info/","course_id":"c45"},
  {"id":"r17","title":"Scrimba React Course","type":"Video","url":"https://scrimba.com/learn/learnreact","course_id":"c52"},
  {"id":"r18","title":"Introduction to Data Engineering","type":"Article","url":"https://www.datacamp.com/courses/introduction-to-data-engineering","course_id":"c38"},
  {"id":"r23","title":"Kaggle ML Course","type":"Video","url":"https://www.kaggle.com/learn/intro-to-machine-learning","course_id":"c23"},
  {"id":"r25","title":"Google ML Crash Course","type":"Article","url":"https://developers.google.com/machine-learning/crash-course","course_id":"c57"},
  {"id":"r26","title":"Postman API Fundamentals","type":"MOOC","url":"https://learning.postman.com/","course_id":"c59"},
  {"id":"r30","title":"NodeJS Learn","type":"MOOC","url":"https://nodejs.dev/en/learn/","course_id":"c30"},
  {"id":"r34","title":"Mode SQL Tutorial","type":"Book","url":"https://mode.com/sql-tutorial/","course_id":"c29"},
  {"id":"r41","title":"freeCodeCamp Python Course","type":"Book","url":"https://www.freecodecamp.org/learn/scientific-computing-with-python/","course_id":"c9"},
  {"id":"r43","title":"Postman API Fundamentals","type":"Video","url":"https://learning.postman.com/","course_id":"c17"},
  {"id":"r84","title":"FastAPI Tutorial","type":"Video","url":"https://fastapi.tiangolo.com/tutorial/","course_id":"c39"},
  {"id":"r95","title":"Machine Learning Andrew Ng","type":"MOOC","url":"https://www.coursera.org/learn/machine-learning","course_id":"c56"},
  {"id":"r96","title":"REST API Tutorial","type":"MOOC","url":"https://restfulapi.net/","course_id":"c60"},
]

# ─────────────────────────────────────────────
# BUSINESS LOGIC
# ─────────────────────────────────────────────

GOAL_MAP = {
    "Data Engineer": ["sql", "etl", "data_warehouse"],
    "ML Engineer": ["python_advanced", "machine_learning"],
    "Data Mining Engineer": ["python_basic", "sql", "machine_learning"],
    "Frontend Developer": ["html", "css", "javascript", "react"],
    "Backend Developer": ["python_basic", "sql", "api", "backend"],
    "Fullstack Developer": ["html", "css", "javascript", "python_basic", "sql", "api"],
    "Web Developer": ["html", "css", "javascript"]
}

def load_courses():
    return [Course(**c) for c in COURSES_DATA]

def load_resources():
    return [Resource(**r) for r in RESOURCES_DATA]

def filter_courses(courses, user):
    filtered = []
    prerequisites = {item["course_id"]: item.get("requires", []) for item in PREREQUISITES_DATA}
    for course in courses:
        if course.difficulty > user.level + 1:
            continue
        required = prerequisites.get(course.id, [])
        if any(r not in user.skills for r in required):
            continue
        filtered.append(course)
    return filtered

def score_course(course, user):
    score = 0
    if any(skill in GOAL_MAP[user.goal] for skill in course.skills):
        score += 3
    if course.difficulty <= user.level + 1:
        score += 2
    if course.duration <= user.available_time:
        score += 1
    return score

# ─────────────────────────────────────────────
# FASTAPI APP
# ─────────────────────────────────────────────

app = FastAPI(
    title="Course Recommender API",
    description="Hệ thống gợi ý khóa học dựa trên mục tiêu nghề nghiệp, kỹ năng và thời gian của bạn.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Pydantic schemas ───

class RecommendRequest(BaseModel):
    goal: str
    skills: List[str]
    level: int
    available_time: int

class ResourceOut(BaseModel):
    id: str
    title: str
    type: str
    url: str

class CourseOut(BaseModel):
    id: str
    name: str
    skills: List[str]
    difficulty: int
    duration: int
    score: int
    resources: List[ResourceOut]

class RecommendResponse(BaseModel):
    goal: str
    total_filtered: int
    recommendations: List[CourseOut]

class SkillOut(BaseModel):
    id: str
    name: str
    level: int

# ─── Endpoints ───

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    return HTMLResponse(content=HTML_PAGE)

@app.get("/skills", response_model=List[SkillOut], tags=["Data"])
async def get_skills():
    """Trả về danh sách tất cả kỹ năng có trong hệ thống."""
    return SKILLS_DATA

@app.get("/goals", tags=["Data"])
async def get_goals():
    """Trả về danh sách mục tiêu nghề nghiệp."""
    return {"goals": list(GOAL_MAP.keys())}

@app.post("/recommend", response_model=RecommendResponse, tags=["Recommend"])
async def recommend(req: RecommendRequest):
    """
    Gợi ý top 5 khóa học phù hợp nhất dựa trên:
    - **goal**: Mục tiêu nghề nghiệp
    - **skills**: Danh sách kỹ năng hiện có (dùng id từ /skills)
    - **level**: Trình độ hiện tại (1=Beginner, 2=Intermediate, 3=Advanced)
    - **available_time**: Thời gian rảnh (giờ/tuần)
    """
    if req.goal not in GOAL_MAP:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Goal không hợp lệ. Chọn một trong: {list(GOAL_MAP.keys())}")
    if req.level not in [1, 2, 3]:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Level phải là 1, 2 hoặc 3")

    user = User(goal=req.goal, skills=req.skills, level=req.level, time=req.available_time)
    courses = load_courses()
    resources = load_resources()

    filtered = filter_courses(courses, user)
    scored = [(c, score_course(c, user)) for c in filtered]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)[:5]

    result = []
    for course, score in ranked:
        related = [r for r in resources if r.course_id == course.id][:3]
        result.append(CourseOut(
            id=course.id,
            name=course.name,
            skills=course.skills,
            difficulty=course.difficulty,
            duration=course.duration,
            score=score,
            resources=[ResourceOut(id=r.id, title=r.title, type=r.type, url=r.url) for r in related]
        ))

    return RecommendResponse(
        goal=req.goal,
        total_filtered=len(filtered),
        recommendations=result
    )

# ─────────────────────────────────────────────
# FRONTEND HTML (served at /)
# ─────────────────────────────────────────────

HTML_PAGE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>CourseAI — Gợi ý khóa học</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet"/>
<style>
:root {
  --bg: #0a0a0f;
  --surface: #111118;
  --surface2: #1a1a26;
  --border: rgba(255,255,255,0.07);
  --accent: #6c63ff;
  --accent2: #ff6b9d;
  --accent3: #00d4aa;
  --text: #f0f0f8;
  --muted: #6b6b8a;
  --card-glow: rgba(108,99,255,0.12);
}
/* ── light mode ── */
[data-theme="light"] {
  --bg: #f5f5f5;
  --surface: #ffffff;
  --surface2: #f0f0f0;
  --border: rgba(0,0,0,0.1);
  --text: #111;
  --muted: #555;
  --accent: #6c63ff;
  --accent2: #ff6b9d;
  --accent3: #00a884;
}
/* ── ── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{
  background:var(--bg);
  color:var(--text);
  font-family:'DM Sans',sans-serif;
  font-size:15px;
  min-height:100vh;
  overflow-x:hidden;
}

/* ── Background mesh ── */
body::before{
  content:'';
  position:fixed;inset:0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(108,99,255,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(255,107,157,0.06) 0%, transparent 50%),
    radial-gradient(ellipse 40% 60% at 60% 30%, rgba(0,212,170,0.04) 0%, transparent 50%);
  pointer-events:none;z-index:0;
}

/* ── Layout ── */
.wrapper{position:relative;z-index:1;max-width:880px;margin:0 auto;padding:0 24px;}

/* ── Header ── */
header{
  padding:56px 0 40px;
  display:flex;align-items:center;gap:16px;
  animation:fadeDown .6s ease both;
}
.logo-mark{
  width:44px;height:44px;border-radius:12px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  display:flex;align-items:center;justify-content:center;
  font-size:20px;flex-shrink:0;
  box-shadow:0 0 24px rgba(108,99,255,0.4);
}
header h1{
  font-family:'Syne',sans-serif;
  font-size:clamp(22px,4vw,30px);
  font-weight:800;letter-spacing:-0.5px;
}
header h1 span{
  background:linear-gradient(90deg,var(--accent),var(--accent2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.badge{
  margin-left:auto;
  background:rgba(108,99,255,0.15);
  border:1px solid rgba(108,99,255,0.3);
  color:var(--accent);
  font-size:11px;font-weight:600;letter-spacing:1px;
  padding:4px 10px;border-radius:20px;text-transform:uppercase;
  white-space:nowrap;
}

/* ── Card ── */
.card{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:20px;padding:32px;
  margin-bottom:24px;
  transition:box-shadow .3s,border-color .3s;
}
.card:hover{
  box-shadow:0 0 40px var(--card-glow);
  border-color:rgba(108,99,255,0.2);
}

/* ── Form ── */
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
@media(max-width:600px){.form-grid{grid-template-columns:1fr;}}

.field{display:flex;flex-direction:column;gap:8px;}
.field label{
  font-size:11px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;
  color:var(--muted);
}
.field label .req{color:var(--accent2);}

select,input[type=number]{
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:10px;
  color:var(--text);
  font-family:'DM Sans',sans-serif;
  font-size:14px;
  padding:12px 14px;
  width:100%;
  outline:none;
  transition:border-color .2s,box-shadow .2s;
  appearance:none;
  -webkit-appearance:none;
}
select:focus,input[type=number]:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px rgba(108,99,255,0.15);
}
select option{background:var(--surface2);color:var(--text);}

/* Skills multi-select */
.skills-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;
}
.skill-chip{
  display:flex;align-items:center;gap:8px;
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:8px;
  padding:8px 12px;
  cursor:pointer;
  transition:all .2s;
  user-select:none;
}
.skill-chip:hover{border-color:rgba(108,99,255,0.4);background:rgba(108,99,255,0.08);}
.skill-chip.active{
  border-color:var(--accent);
  background:rgba(108,99,255,0.15);
  color:var(--accent);
}
.skill-chip input[type=checkbox]{display:none;}
.skill-check{
  width:16px;height:16px;border-radius:4px;
  border:1.5px solid var(--muted);
  flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-size:10px;transition:all .2s;
}
.skill-chip.active .skill-check{
  background:var(--accent);border-color:var(--accent);color:#fff;
}
.skill-name{font-size:13px;font-weight:500;}

/* Level selector */
.level-group{display:flex;gap:8px;}
.level-btn{
  flex:1;padding:10px;border-radius:10px;
  border:1px solid var(--border);
  background:var(--surface2);
  color:var(--muted);
  cursor:pointer;text-align:center;
  font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;
  transition:all .2s;
}
.level-btn:hover{border-color:rgba(108,99,255,0.4);}
.level-btn.active{
  border-color:var(--accent);
  background:rgba(108,99,255,0.15);
  color:var(--text);
}
.level-label{font-size:11px;color:var(--muted);margin-top:2px;}

/* Submit */
.btn-submit{
  width:100%;margin-top:24px;
  padding:16px;border-radius:12px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  border:none;color:#fff;
  font-family:'Syne',sans-serif;font-size:15px;font-weight:700;letter-spacing:0.5px;
  cursor:pointer;
  transition:opacity .2s,transform .2s,box-shadow .2s;
  box-shadow:0 4px 20px rgba(108,99,255,0.3);
}
.btn-submit:hover{opacity:.9;transform:translateY(-1px);box-shadow:0 8px 30px rgba(108,99,255,0.4);}
.btn-submit:active{transform:translateY(0);}
.btn-submit:disabled{opacity:.5;cursor:not-allowed;transform:none;}

/* ── Section heading ── */
.section-head{
  display:flex;align-items:center;gap:12px;
  margin-bottom:24px;
}
.section-head h2{
  font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
}
.section-head .pill{
  background:rgba(0,212,170,0.12);
  border:1px solid rgba(0,212,170,0.25);
  color:var(--accent3);
  font-size:11px;font-weight:600;letter-spacing:0.8px;
  padding:3px 10px;border-radius:20px;text-transform:uppercase;
}

/* ── Result cards ── */
#results{animation:fadeUp .5s ease both;}

.result-card{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:16px;
  padding:24px;margin-bottom:16px;
  position:relative;overflow:hidden;
  transition:all .3s;
  animation:fadeUp .4s ease both;
}
.result-card:nth-child(2){animation-delay:.05s;}
.result-card:nth-child(3){animation-delay:.1s;}
.result-card:nth-child(4){animation-delay:.15s;}
.result-card:nth-child(5){animation-delay:.2s;}

.result-card::before{
  content:'';
  position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--accent),var(--accent2));
  opacity:0;transition:opacity .3s;
}
.result-card:hover{
  border-color:rgba(108,99,255,0.25);
  box-shadow:0 8px 32px var(--card-glow);
}
.result-card:hover::before{opacity:1;}

.rank-badge{
  position:absolute;top:20px;right:20px;
  width:36px;height:36px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-family:'Syne',sans-serif;font-size:13px;font-weight:800;
}
.rank-1{background:rgba(255,215,0,0.15);color:#ffd700;border:1px solid rgba(255,215,0,0.3);}
.rank-2{background:rgba(192,192,192,0.12);color:#c0c0c0;border:1px solid rgba(192,192,192,0.25);}
.rank-3{background:rgba(205,127,50,0.12);color:#cd7f32;border:1px solid rgba(205,127,50,0.25);}
.rank-other{background:var(--surface2);color:var(--muted);border:1px solid var(--border);}

.course-name{
  font-family:'Syne',sans-serif;font-size:16px;font-weight:700;
  margin-bottom:12px;padding-right:50px;
}
.course-meta{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;}
.meta-tag{
  display:inline-flex;align-items:center;gap:5px;
  font-size:12px;font-weight:500;
  padding:4px 10px;border-radius:6px;
}
.tag-skill{background:rgba(108,99,255,0.12);color:var(--accent);border:1px solid rgba(108,99,255,0.2);}
.tag-diff{background:rgba(255,107,157,0.1);color:var(--accent2);border:1px solid rgba(255,107,157,0.2);}
.tag-time{background:rgba(0,212,170,0.1);color:var(--accent3);border:1px solid rgba(0,212,170,0.2);}
.tag-score{background:rgba(255,215,0,0.1);color:#ffd700;border:1px solid rgba(255,215,0,0.2);}

.score-bar{height:4px;background:var(--surface2);border-radius:2px;margin-bottom:16px;overflow:hidden;}
.score-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width 1s ease;}

.resources-label{
  font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;
  color:var(--muted);margin-bottom:8px;
}
.resource-list{display:flex;flex-direction:column;gap:6px;}
.resource-item{
  display:flex;align-items:center;gap:10px;
  padding:8px 12px;border-radius:8px;
  background:var(--surface2);
  text-decoration:none;color:var(--text);
  font-size:13px;
  transition:background .2s,color .2s;
  border:1px solid transparent;
}
.resource-item:hover{background:rgba(108,99,255,0.1);border-color:rgba(108,99,255,0.2);color:var(--accent);}
.resource-type{
  font-size:10px;font-weight:700;letter-spacing:.8px;
  padding:2px 7px;border-radius:4px;flex-shrink:0;
}
.rt-mooc{background:rgba(108,99,255,0.2);color:var(--accent);}
.rt-book{background:rgba(0,212,170,0.15);color:var(--accent3);}
.rt-video{background:rgba(255,107,157,0.15);color:var(--accent2);}
.rt-article{background:rgba(255,215,0,0.12);color:#ffd700;}
.resource-arrow{margin-left:auto;color:var(--muted);font-size:12px;}

/* ── Loading ── */
.loading{
  display:none;
  text-align:center;padding:48px;
  animation:pulse 1.5s ease infinite;
}
.loading.show{display:block;}
.spinner{
  width:40px;height:40px;border-radius:50%;
  border:3px solid var(--border);
  border-top-color:var(--accent);
  animation:spin .7s linear infinite;
  margin:0 auto 16px;
}
.loading p{color:var(--muted);font-size:14px;}

/* ── Empty state ── */
.empty{
  text-align:center;padding:48px;color:var(--muted);
}
.empty-icon{font-size:48px;margin-bottom:12px;}

/* ── Toast ── */
.toast{
  position:fixed;bottom:24px;right:24px;
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:12px;padding:14px 20px;
  font-size:13px;max-width:300px;
  box-shadow:0 8px 32px rgba(0,0,0,0.4);
  transform:translateX(120%);transition:transform .3s;
  z-index:999;
}
.toast.show{transform:translateX(0);}
.toast.error{border-color:rgba(255,107,157,0.4);color:var(--accent2);}

/* ── Docs link ── */
.docs-bar{
  display:flex;align-items:center;gap:10px;
  padding:14px 20px;
  background:rgba(0,212,170,0.06);
  border:1px solid rgba(0,212,170,0.15);
  border-radius:12px;margin-bottom:32px;
  font-size:13px;color:var(--muted);
  animation:fadeDown .6s .2s ease both;opacity:0;animation-fill-mode:forwards;
}
.docs-bar a{color:var(--accent3);text-decoration:none;font-weight:600;}
.docs-bar a:hover{text-decoration:underline;}
.docs-dot{width:7px;height:7px;border-radius:50%;background:var(--accent3);animation:pulse 1.5s ease infinite;}

/* ── Animations ── */
@keyframes fadeDown{from{opacity:0;transform:translateY(-14px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
@keyframes spin{to{transform:rotate(360deg);}}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:.5;}}

.form-section-title{
  font-size:11px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;
  color:var(--muted);margin-bottom:12px;margin-top:4px;
}

/* ── Theme Toggle ── */
.theme-toggle{
  margin-left:auto;
  display:flex;align-items:center;gap:8px;
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:99px;
  padding:6px 12px 6px 8px;
  cursor:pointer;
  transition:border-color .25s, box-shadow .25s;
  outline:none;
}
.theme-toggle:hover{
  border-color:rgba(108,99,255,0.4);
  box-shadow:0 0 0 3px rgba(108,99,255,0.1);
}
.theme-toggle-track{
  width:34px;height:18px;
  background:rgba(108,99,255,0.2);
  border-radius:99px;
  position:relative;
  border:1px solid rgba(108,99,255,0.3);
  flex-shrink:0;
  transition:background .3s;
}
[data-theme="light"] .theme-toggle-track{
  background:rgba(108,99,255,0.35);
}
.theme-toggle-thumb{
  position:absolute;top:2px;left:2px;
  width:12px;height:12px;
  border-radius:50%;
  background:var(--accent);
  transition:transform .3s cubic-bezier(.34,1.56,.64,1);
  box-shadow:0 0 6px rgba(108,99,255,0.6);
}
[data-theme="light"] .theme-toggle-thumb{
  transform:translateX(16px);
}
.theme-toggle-icon{
  font-size:13px;line-height:1;
  transition:opacity .2s, transform .2s;
}
.theme-icon-moon{ opacity:1; }
.theme-icon-sun { opacity:.4; }
[data-theme="light"] .theme-icon-moon{ opacity:.4; }
[data-theme="light"] .theme-icon-sun { opacity:1; }
</style>
</head>
<body>
<div class="wrapper">

  <!-- Header -->
  <header>
    <h1><span>RECOMMEND</span> SYSTEM</h1>
    <div class="badge">v1.0</div>
    <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()" aria-label="Toggle theme">
      <span class="theme-toggle-track">
        <span class="theme-toggle-thumb"></span>
      </span>
      <span class="theme-toggle-icon theme-icon-moon">🌙</span>
      <span class="theme-toggle-icon theme-icon-sun">☀️</span>
    </button>
  </header>

  <!-- Docs bar
  <div class="docs-bar">
    <div class="docs-dot"></div>
    <span>API đang chạy — thử trực tiếp tại</span>
    <a href="/docs" target="_blank">/docs (Swagger UI)</a>
    <span>hoặc</span>
    <a href="/redoc" target="_blank">/redoc</a>
  </div> -->

  <!-- Form card -->
  <div class="card" style="animation:fadeUp .5s .1s ease both;opacity:0;animation-fill-mode:forwards;">
    <div class="section-head">
      <h2>Thông tin của bạn</h2>
      <div class="pill">Step 1</div>
    </div>

    <!-- Goal -->
    <div class="field" style="margin-bottom:20px;">
      <label>Mục tiêu nghề nghiệp <span class="req">*</span></label>
      <select id="goal">
        <option value="">— Chọn nghề bạn muốn hướng đến —</option>
        <option>Data Engineer</option>
        <option>ML Engineer</option>
        <option>Data Mining Engineer</option>
        <option>Frontend Developer</option>
        <option>Backend Developer</option>
        <option>Fullstack Developer</option>
        <option>Web Developer</option>
      </select>
    </div>

    <!-- Skills -->
    <div class="field" style="margin-bottom:20px;">
      <label>Kỹ năng hiện có <span class="req">*</span></label>
      <p style="font-size:12px;color:var(--muted);margin-bottom:10px;">Chọn tất cả kỹ năng bạn đã có</p>
      <div class="skills-grid" id="skillsGrid"></div>
    </div>

    <!-- Level + Time -->
    <div class="form-grid">
      <div class="field">
        <label>Trình độ hiện tại <span class="req">*</span></label>
        <div class="level-group" id="levelGroup">
          <div class="level-btn" data-val="1" onclick="setLevel(1)">
            <div>🌱 Beginner</div>
            <div class="level-label">Mới bắt đầu</div>
          </div>
          <div class="level-btn" data-val="2" onclick="setLevel(2)">
            <div>⚡ Mid</div>
            <div class="level-label">Có kinh nghiệm</div>
          </div>
          <div class="level-btn" data-val="3" onclick="setLevel(3)">
            <div>🔥 Senior</div>
            <div class="level-label">Nâng cao</div>
          </div>
        </div>
        <input type="hidden" id="level" value=""/>
      </div>
      <div class="field">
        <label>Thời gian rảnh <span class="req">*</span></label>
        <input type="number" id="time" placeholder="VD: 20" min="1" max="168" oninput="if(this.value>168)this.value=168;if(this.value<0)this.value='';"/>
        <span style="font-size:11px;color:var(--muted);margin-top:4px;">giờ / tuần</span>
      </div>
    </div>

    <button class="btn-submit" onclick="submit()">✨ Gợi ý khóa học phù hợp</button>
  </div>

  <!-- Loading -->
  <div class="loading" id="loading">
    <div class="spinner"></div>
    <p>Đang phân tích và gợi ý...</p>
  </div>

  <!-- Results -->
  <div id="results"></div>

</div>

<!-- Toast -->
<div class="toast" id="toast"></div>

<script>
const SKILLS = [
  {id:"python_basic",name:"Python Basic"},
  {id:"python_advanced",name:"Python Advanced"},
  {id:"sql",name:"SQL"},
  {id:"data_structures",name:"Data Structures"},
  {id:"etl",name:"ETL"},
  {id:"data_warehouse",name:"Data Warehouse"},
  {id:"big_data",name:"Big Data"},
  {id:"machine_learning",name:"Machine Learning"},
  {id:"html",name:"HTML"},
  {id:"css",name:"CSS"},
  {id:"javascript",name:"JavaScript"},
  {id:"react",name:"React"},
  {id:"backend",name:"Backend"},
  {id:"api",name:"API"}
];

// Build skills grid
const grid = document.getElementById('skillsGrid');
SKILLS.forEach(s => {
  const chip = document.createElement('div');
  chip.className = 'skill-chip';
  chip.dataset.id = s.id;
  chip.innerHTML = `<div class="skill-check"></div><span class="skill-name">${s.name}</span>`;
  chip.onclick = () => {
    chip.classList.toggle('active');
    chip.querySelector('.skill-check').textContent = chip.classList.contains('active') ? '✓' : '';
  };
  grid.appendChild(chip);
});

let selectedLevel = null;

function setLevel(val) {
  selectedLevel = val;
  document.getElementById('level').value = val;
  document.querySelectorAll('.level-btn').forEach(b => {
    b.classList.toggle('active', parseInt(b.dataset.val) === val);
  });
}

function showToast(msg, isError=false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast show' + (isError ? ' error' : '');
  setTimeout(() => t.className = 'toast', 3000);
}

function diffLabel(d) {
  return d === 1 ? 'Beginner' : d === 2 ? 'Intermediate' : 'Advanced';
}
function typeClass(t) {
  const m = {MOOC:'rt-mooc',Book:'rt-book',Video:'rt-video',Article:'rt-article'};
  return m[t] || 'rt-article';
}
function rankClass(i) {
  return ['rank-1','rank-2','rank-3','rank-other','rank-other'][i] || 'rank-other';
}

async function submit() {
  const goal = document.getElementById('goal').value;
  const level = document.getElementById('level').value;
  const time = parseInt(document.getElementById('time').value);
  const skills = [...document.querySelectorAll('.skill-chip.active')].map(c => c.dataset.id);

  if (!goal) return showToast('⚠️ Vui lòng chọn mục tiêu nghề nghiệp', true);
  if (!level) return showToast('⚠️ Vui lòng chọn trình độ của bạn', true);
  if (!time || time < 1) return showToast('⚠️ Vui lòng nhập thời gian hợp lệ', true);
  if (time > 168) return showToast('⚠️ Một tuần chỉ có 168 giờ thôi nhé!', true);

  document.getElementById('loading').classList.add('show');
  document.getElementById('results').innerHTML = '';
  document.querySelector('.btn-submit').disabled = true;

  try {
    const res = await fetch('/recommend', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({goal, skills, level: parseInt(level), available_time: time})
    });
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || 'Lỗi server');

    renderResults(data);
  } catch(e) {
    showToast('❌ ' + e.message, true);
  } finally {
    document.getElementById('loading').classList.remove('show');
    document.querySelector('.btn-submit').disabled = false;
  }
}

function renderResults(data) {
  const container = document.getElementById('results');

  if (!data.recommendations.length) {
    container.innerHTML = `<div class="empty"><div class="empty-icon">🔍</div><p>Không tìm thấy khóa học phù hợp.<br>Thử tăng thời gian hoặc giảm yêu cầu trình độ.</p></div>`;
    return;
  }

  let html = `<div class="card" style="animation:fadeUp .4s ease both;">
    <div class="section-head">
      <h2>Kết quả gợi ý</h2>
      <div class="pill">${data.recommendations.length} khóa học · ${data.total_filtered} phù hợp</div>
    </div>`;

  data.recommendations.forEach((c, i) => {
    const pct = Math.round((c.score / 6) * 100);
    const rHtml = c.resources.length ? `
      <div class="resources-label">Tài liệu học tập</div>
      <div class="resource-list">
        ${c.resources.map(r => `
          <a class="resource-item" href="${r.url}" target="_blank" rel="noopener">
            <span class="resource-type ${typeClass(r.type)}">${r.type}</span>
            <span>${r.title}</span>
            <span class="resource-arrow">↗</span>
          </a>`).join('')}
      </div>` : '';

    html += `<div class="result-card">
      <div class="rank-badge ${rankClass(i)}">${i+1}</div>
      <div class="course-name">${c.name}</div>
      <div class="course-meta">
        ${c.skills.map(s => `<span class="meta-tag tag-skill">📚 ${s}</span>`).join('')}
        <span class="meta-tag tag-diff">⚡ ${diffLabel(c.difficulty)}</span>
        <span class="meta-tag tag-time">⏱ ${c.duration}h</span>
        <span class="meta-tag tag-score">★ ${c.score}/6</span>
      </div>
      <div class="score-bar"><div class="score-fill" style="width:${pct}%"></div></div>
      ${rHtml}
    </div>`;
  });

  html += '</div>';
  container.innerHTML = html;

  // Animate score bars after render
  setTimeout(() => {
    document.querySelectorAll('.score-fill').forEach(el => {
      const w = el.style.width;
      el.style.width = '0';
      requestAnimationFrame(() => { el.style.width = w; });
    });
  }, 50);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");

  if (current === "light") {
    document.documentElement.removeAttribute("data-theme");
    localStorage.setItem("theme", "dark");
  } else {
    document.documentElement.setAttribute("data-theme", "light");
    localStorage.setItem("theme", "light");
  }
}

window.onload = () => {
  const saved = localStorage.getItem("theme");
  if (saved === "light") {
    document.documentElement.setAttribute("data-theme", "light");
  }
};
</script>
</body>
</html>"""

# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
