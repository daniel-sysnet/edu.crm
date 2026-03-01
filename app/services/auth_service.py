from app.model.user import User


class AuthService:

    def __init__(self):
        self.users = [
            User(1, 'admin',    'admin123'),
            User(2, 'etudiant', 'etudiant123'),
            User(3, 'prof',     'prof123'),
        ]

    def login(self, login: str, password: str):
        for user in self.users:
            if user.login == login and user.password == password:
                return user
        return None