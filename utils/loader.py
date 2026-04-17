import json
from models.course import Course
from models.skill import Skill
from models.resource import Resource

def load_skills(path):
    import json
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Skill(**s) for s in data]

def load_courses(path):
    with open(path) as f:
        data = json.load(f)
    return [Course(**c) for c in data]

def load_resources(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Resource(**r) for r in data]

def load_json(path):
    with open(path) as f:
        return json.load(f)