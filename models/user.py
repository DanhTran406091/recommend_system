class User:
    def __init__(self, goal, skills, level, time):
        self.goal = goal
        self.skills = skills
        self.level = level
        self.available_time = time
    def has_skill(self, skill_id):
        return skill_id in self.skills