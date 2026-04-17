GOAL_MAP = {
    # ===== DATA =====
    "Data Engineer": ["sql", "etl", "data_warehouse"],
    "ML Engineer": ["python_advanced", "machine_learning"],
    "Data Mining Engineer": ["python_basic", "sql", "machine_learning"],
    # ===== WEB =====
    "Frontend Developer": ["html", "css", "javascript", "react"],
    "Backend Developer": ["python_basic", "sql", "api", "backend"],
    "Fullstack Developer": ["html", "css", "javascript", "python_basic", "sql", "api"],
    "Web Developer": ["html", "css", "javascript"]
}

def score_course(course, user):
    score = 0

    # Goal match
    if any(skill in GOAL_MAP[user.goal] for skill in course.skills):
        score += 3

    # Difficulty
    if course.difficulty <= user.level + 1:
        score += 2

    # Time
    if course.duration <= user.available_time:
        score += 1

    return score