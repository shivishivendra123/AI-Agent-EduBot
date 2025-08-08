from connect_db import client
def create_course_announcements(body: str) -> str:
    # This function will handle the creation of course announcements
    # For now, we will just return a placeholder response

    db = client["ai_education"]
    collection = db["course_announcements"]
    collection.insert_one({"body": body})
    return body