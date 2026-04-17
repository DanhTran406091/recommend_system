class Course:
    def __init__(self, id, name, skills, difficulty, duration):
        self.id = id
        self.name = name
        self.skills = skills
        self.difficulty = difficulty
        self.duration = duration
    def __repr__(self):
        return f"Course({self.name})"