from app.model.user import User


class AuthService:

    def __init__(self, users: list[User] = None):
        self.users = users if users is not None else [
            User(1, 'admin@gmail.com', 'admin123'),
            User(2, 'ism@gmail.com', 'ism123'),
        ]

    def login(self, login: str = None, password: str = None):
        for user in self.users:
            if user.login == login and user.password == password:
                return user
        return None