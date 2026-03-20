from app.models.user import User


class AuthService:

    def __init__(self, users: list[User] = None):
        self.users = users if users is not None else [
            User('admin@gmail.com', 'admin123', 'Administrateur'),
            User('ism@gmail.com', 'ism123', 'Ismail'),
        ]

    def login(self, login: str = None, password: str = None):
        for user in self.users:
            if user.login == login and user.password == password:
                return user
        return None