import json
import random
import os

# =========================
# 1. SKILLS (ADD WEB)
# =========================
skills = [
    # DATA
    {"id": "python_basic", "name": "Python Basic", "level": 1},
    {"id": "python_advanced", "name": "Python Advanced", "level": 2},
    {"id": "sql", "name": "SQL", "level": 2},
    {"id": "data_structures", "name": "Data Structures", "level": 2},
    {"id": "etl", "name": "ETL", "level": 3},
    {"id": "data_warehouse", "name": "Data Warehouse", "level": 3},
    {"id": "big_data", "name": "Big Data", "level": 3},
    {"id": "machine_learning", "name": "Machine Learning", "level": 3},

    # WEB
    {"id": "html", "name": "HTML", "level": 1},
    {"id": "css", "name": "CSS", "level": 1},
    {"id": "javascript", "name": "JavaScript", "level": 2},
    {"id": "react", "name": "React", "level": 2},
    {"id": "backend", "name": "Backend", "level": 2},
    {"id": "api", "name": "API", "level": 2}
]

# =========================
# 2. COURSE TEMPLATES
# =========================
course_names = [
    "Intro to {}",
    "{} for Beginners",
    "Advanced {}",
    "{} Fundamentals",
    "{} Practical Guide",
    "{} Bootcamp"
]

# =========================
# 3. GENERATE COURSES (NO DUPLICATE)
# =========================
def generate_courses(n=60):
    courses = []
    used_names = set()

    for i in range(n):
        while True:
            skill = random.choice(skills)
            name_template = random.choice(course_names)
            name = name_template.format(skill["name"])

            if name not in used_names:
                used_names.add(name)
                break

        course = {
            "id": f"c{i+1}",
            "name": name,
            "skills": [skill["id"]],
            "difficulty": skill["level"],
            "duration": random.randint(8, 25)
        }

        courses.append(course)

    return courses

# =========================
# 4. GENERATE PREREQUISITES (UPGRADE)
# =========================
def generate_prerequisites(courses):
    prereqs = []

    for course in courses:
        skill = course["skills"][0]
        requires = []

        # ===== DATA =====
        if skill == "python_advanced":
            requires.append("python_basic")

        elif skill == "sql":
            requires.append("python_basic")

        elif skill == "etl":
            requires.append("sql")

        elif skill == "data_warehouse":
            requires.append("sql")

        elif skill == "big_data":
            requires.append("python_basic")

        elif skill == "machine_learning":
            requires.append("python_advanced")

        # ===== WEB =====
        elif skill == "css":
            requires.append("html")

        elif skill == "javascript":
            requires.append("html")

        elif skill == "react":
            requires.append("javascript")

        elif skill == "backend":
            requires.append("python_basic")

        elif skill == "api":
            requires.append("backend")

        if requires:
            prereqs.append({
                "course_id": course["id"],
                "requires": requires
            })

    return prereqs

# =========================
# 5. SAVE FILE
# =========================
def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# =========================
# 6. MAIN
# =========================
def main():
    os.makedirs("data", exist_ok=True)

    courses = generate_courses(60)
    prerequisites = generate_prerequisites(courses)

    save_json(skills, "data/skills.json")
    save_json(courses, "data/courses.json")
    save_json(prerequisites, "data/prerequisites.json")

    print("Dataset generated (Data + Web)!")

if __name__ == "__main__":
    main()