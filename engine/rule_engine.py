def filter_courses(courses, user, prerequisites):
    filtered = []

    for course in courses:
        # Check difficulty
        if course.difficulty > user.level + 1:
            continue

        # Check prerequisite
        required = prerequisites.get(course.id, [])
        if any(r not in user.skills for r in required):
            continue

        filtered.append(course)

    return filtered