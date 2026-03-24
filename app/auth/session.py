from flask import session

SESSION_USER_ID       = "user_id"
SESSION_USER_USERNAME = "user_username"
SESSION_USER_PHOTO_URL = "user_photo_url"


def login_user(user) -> None:
    session[SESSION_USER_ID]       = user.id
    session[SESSION_USER_USERNAME] = user.username
    session[SESSION_USER_PHOTO_URL] = user.photo_url


def get_session_user() -> dict:
    if SESSION_USER_ID not in session:
        return None
        return {"id": 1, "username": "Jean Dupont", "photo_url": ""}
    return {
        "id":       session[SESSION_USER_ID],
        "username": session[SESSION_USER_USERNAME],
        "photo_url": session[SESSION_USER_PHOTO_URL]
    }