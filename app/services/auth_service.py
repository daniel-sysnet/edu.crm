from app.models.user import User


class AuthService:

    def __init__(self, users: list[User] = None):
        self.users = users if users is not None else []

    def login(self, login: str = None, password: str = None):
        user = User.query.filter_by(email=login).first()
        if user is None:
            return None
        if not user.check_password(password):
            return None
        return user