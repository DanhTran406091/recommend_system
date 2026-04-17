import json
import random
import os

# =========================
# RESOURCE TYPES
# =========================
RESOURCE_TYPES = ["MOOC", "Book", "Article", "Video"]

# =========================
# SKILL → REAL LINKS
# =========================
RESOURCE_LINKS = {

    "python_basic": [
        ("Python Official Tutorial", "https://docs.python.org/3/tutorial/"),
        ("Python for Everybody", "https://www.coursera.org/specializations/python"),
        ("freeCodeCamp Python Course", "https://www.freecodecamp.org/learn/scientific-computing-with-python/"),
        ("LearnPython.org", "https://www.learnpython.org/")
    ],

    "python_advanced": [
        ("Advanced Python Programming", "https://realpython.com/"),
        ("Python Advanced Topics", "https://www.datacamp.com/courses/intermediate-python"),
        ("Effective Python Book", "https://effectivepython.com/")
    ],

    "sql": [
        ("SQL for Data Science", "https://www.coursera.org/learn/sql-for-data-science"),
        ("SQL Tutorial W3Schools", "https://www.w3schools.com/sql/"),
        ("Mode SQL Tutorial", "https://mode.com/sql-tutorial/"),
        ("SQLBolt Interactive Tutorial", "https://sqlbolt.com/")
    ],

    "machine_learning": [
        ("Machine Learning Andrew Ng", "https://www.coursera.org/learn/machine-learning"),
        ("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course"),
        ("Kaggle ML Course", "https://www.kaggle.com/learn/intro-to-machine-learning")
    ],

    "etl": [
        ("Introduction to Data Engineering", "https://www.datacamp.com/courses/introduction-to-data-engineering"),
        ("Data Engineering Foundations", "https://www.coursera.org/learn/data-engineering-foundations")
    ],

    "big_data": [
        ("Big Data Specialization", "https://www.coursera.org/specializations/big-data"),
        ("Apache Spark Documentation", "https://spark.apache.org/docs/latest/")
    ],

    "html": [
        ("HTML Tutorial", "https://www.w3schools.com/html/"),
        ("MDN HTML Guide", "https://developer.mozilla.org/en-US/docs/Web/HTML"),
        ("freeCodeCamp HTML Course", "https://www.freecodecamp.org/learn/responsive-web-design/")
    ],

    "css": [
        ("CSS Tutorial", "https://www.w3schools.com/css/"),
        ("MDN CSS Guide", "https://developer.mozilla.org/en-US/docs/Web/CSS"),
        ("CSS Tricks Guide", "https://css-tricks.com/")
    ],

    "javascript": [
        ("JavaScript Info", "https://javascript.info/"),
        ("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"),
        ("freeCodeCamp JavaScript", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/")
    ],

    "react": [
        ("React Official Docs", "https://react.dev/learn"),
        ("React freeCodeCamp", "https://www.freecodecamp.org/news/learn-react-course/"),
        ("Scrimba React Course", "https://scrimba.com/learn/learnreact")
    ],

    "backend": [
        ("NodeJS Learn", "https://nodejs.dev/en/learn/"),
        ("FastAPI Tutorial", "https://fastapi.tiangolo.com/tutorial/")
    ],

    "api": [
        ("REST API Tutorial", "https://restfulapi.net/"),
        ("Postman API Fundamentals", "https://learning.postman.com/")
    ]
}

# =========================
# LOAD COURSES
# =========================
def load_courses():
    with open("data/courses.json", "r", encoding="utf-8") as f:
        return json.load(f)

# =========================
# GENERATE RESOURCES
# =========================
def generate_resources(courses, n=120):

    resources = []
    resource_id = 1

    while len(resources) < n:

        course = random.choice(courses)
        skill = course["skills"][0]

        if skill not in RESOURCE_LINKS:
            continue

        title, url = random.choice(RESOURCE_LINKS[skill])

        resource = {
            "id": f"r{resource_id}",
            "title": title,
            "type": random.choice(RESOURCE_TYPES),
            "url": url,
            "course_id": course["id"]
        }

        resources.append(resource)
        resource_id += 1

    return resources

# =========================
# SAVE JSON
# =========================
def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# =========================
# MAIN
# =========================
def main():

    os.makedirs("data", exist_ok=True)

    courses = load_courses()

    resources = generate_resources(courses, 120)

    save_json(resources, "data/resources.json")

    print("120 REAL resources generated!")

if __name__ == "__main__":
    main()