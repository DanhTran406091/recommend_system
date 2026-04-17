class Difficulty:
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3

    @staticmethod
    def to_string(level):
        mapping = {
            1: "Beginner",
            2: "Intermediate",
            3: "Advanced"
        }
        return mapping.get(level, "Unknown")