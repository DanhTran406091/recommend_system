class Resource:

    def __init__(self, id, title, type, url, course_id):
        self.id = id
        self.title = title
        self.type = type
        self.url = url
        self.course_id = course_id

    def __repr__(self):
        return f"Resource({self.title}, {self.type})"