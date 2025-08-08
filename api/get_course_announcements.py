from connect_db import client
def get_course_announcements(text: str = None) -> list:
    # This function will handle the retrieval of course announcements
    # For now, we will just return a placeholder response
    db = client["ai_education"]
    collection = db["course_announcements"]
    announcements = collection.find()

    return [announcement["body"] for announcement in announcements]
