from app.model.user import User


class AuthService:
    _users = [
        User(1, 'admin',    'admin123'),
        User(2, 'etudiant', 'etudiant123'),
    ]

    @staticmethod
    def login(login: str, password: str):
        """
        Vérifie les credentials et retourne l'objet User si valide,
        sinon retourne None.
        """
        for user in AuthService._users:
            if user.login == login and user.password == password:
                return user
        return None