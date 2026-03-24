from app.models.user import User


class AuthService:

    def login(self, login: str = None, password: str = None):
        user = User.query.filter_by(email=login).first()
        if user is not None and user.check_password(password):
            return user
        return None