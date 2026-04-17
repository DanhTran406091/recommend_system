from models.user import User
from utils.loader import load_courses, load_json, load_resources
from engine.rule_engine import filter_courses
from engine.scoring import score_course

def input_user():
    print("=== USER INPUT ===")

    # =====================
    # LOAD DATA
    # =====================
    skills_data = load_json("data/skills.json")
    all_skills = [s["id"] for s in skills_data]

    # =====================
    # GOAL MENU (FULL)
    # =====================
    goals = [
        "Data Engineer",
        "ML Engineer",
        "Data Mining Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Fullstack Developer",
        "Web Developer"
    ]

    print("\nChọn nghề bạn muốn hướng đến:")
    for i, g in enumerate(goals, 1):
        print(f"{i}. {g}")

    while True:
        try:
            choice = int(input("Nhập số: "))
            if 1 <= choice <= len(goals):
                goal = goals[choice - 1]
                break
        except:
            pass
        print("Invalid choice, try again!")

    # =====================
    # SKILL MULTI-SELECT
    # =====================
    print("\nLựa chọn kỹ năng mà bạn sở hữu:")
    for i, s in enumerate(all_skills, 1):
        print(f"{i}. {s}")

    print("Nhập nhiều số cách nhau bằng dấu cách (vd: 1 3 5)")

    while True:
        try:
            choices = input("Enter: ").split()
            selected = set(int(c) for c in choices)

            if not selected:
                raise ValueError

            skills = []
            for idx in selected:
                if 1 <= idx <= len(all_skills):
                    skills.append(all_skills[idx - 1])
                else:
                    raise ValueError

            break
        except:
            print("Invalid Input, Try Again")

    # =====================
    # LEVEL
    # =====================
    while True:
        try:
            level = int(input("\nNhập mức trình độ của bạn hiện tại (1-3): "))
            if level in [1, 2, 3]:
                break
        except:
            pass
        print("Invalid level!")

    # =====================
    # TIME
    # =====================
    while True:
        try:
            time = int(input("Thời gian rảnh (hours): "))
            break
        except:
            print("Invalid time!")

    return User(goal, skills, level, time)

# =========================
# MAIN MENU
# =========================
def menu():
    print("\n===== MENU =====")
    print("1. Gợi ý khóa học")
    print("2. Thoát")

    choice = input("Lựa chọn: ")
    return choice

# =========================
# MAIN LOGIC
# =========================
def run_recommender():
    # Load data
    courses = load_courses("data/courses.json")
    prereq_list = load_json("data/prerequisites.json")
    resources = load_resources("data/resources.json")

    # Convert prerequisite list -> dict
    prerequisites = {}
    for item in prereq_list:
        prerequisites[item["course_id"]] = item["requires"]

    # Input user
    user = input_user()

    # Filter
    filtered_courses = filter_courses(courses, user, prerequisites)

    # Score
    scored = [(c, score_course(c, user)) for c in filtered_courses]

    # Sort
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    # Output
    print("\n========= GỢI Ý KHÓA HỌC =========")

    for course, score in ranked[:5]:
        print(f"\nKhóa học: {course.name}")
        print(f"Kỹ năng: {course.skills}")
        print(f"Thời lượng: {course.duration} giờ")
        print(f"Score: {score}")

        # Hiển thị tài nguyên học tập
        related = [r for r in resources if r.course_id == course.id]

        if related:
            print("Tài liệu học tập:")
            for r in related[:3]:
                print(f"- {r.title} ({r.type})")
                print(f"  Link: {r.url}")
        print("-" * 80)

# =========================
# ENTRY POINT
# =========================
def main():
    while True:
        choice = menu()

        if choice == "1":
            run_recommender()
        elif choice == "2":
            print("Tạm biệt!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()