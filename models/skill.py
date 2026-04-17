class Skill:
    def __init__(self, id, name, level):
        self.id = id
        self.name = name
        self.level = level

    def __repr__(self):
        return f"Skill(id={self.id}, level={self.level})"