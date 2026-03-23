from datetime import datetime
from app.extensions import db
from app.models.gender     import Gender
from app.models.speciality import Speciality


class Teacher(db.Model):
    __tablename__ = "teachers"

    id         = db.Column(db.Integer,          primary_key=True)
    matricule  = db.Column(db.String(20),        unique=True, nullable=False)
    name       = db.Column(db.String(120),       nullable=False)
    email      = db.Column(db.String(120),       unique=True, nullable=False)
    phone      = db.Column(db.String(20),        nullable=False)
    gender     = db.Column(db.Enum(Gender),      nullable=False)
    speciality = db.Column(db.Enum(Speciality),  nullable=False)
    dob        = db.Column(db.Date,              nullable=True)
    address    = db.Column(db.Text,              nullable=True)
    created_at = db.Column(db.DateTime,          default=datetime.utcnow, nullable=False)

    # Relation One-to-Many avec Course
    courses = db.relationship("Course", back_populates="teacher")

    @staticmethod
    def generate_matricule(id: int) -> str:
        return f"ENS-{id:03d}"

    def __repr__(self) -> str:
        return f"<Teacher {self.matricule} — {self.name}>"