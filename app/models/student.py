import uuid
from datetime import datetime
from app.extensions import db
from app.models.gender import Gender


# Table d'association Student ↔ Course (Many-to-Many)
enrollment = db.Table(
    "enrollment",
    db.Column("student_id", db.Integer, db.ForeignKey("students.id"), primary_key=True),
    db.Column("course_id",  db.Integer, db.ForeignKey("courses.id"),  primary_key=True),
)

def _generate_matricule() -> str:
    return f"STU-{uuid.uuid4().hex[:8].upper()}"

class Student(db.Model):
    __tablename__ = "students"

    id         = db.Column(db.Integer,     primary_key=True)
    matricule  = db.Column(db.String(20),  unique=True, nullable=False, default=_generate_matricule)
    name       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    phone      = db.Column(db.String(20),  nullable=False)
    gender     = db.Column(db.Enum(Gender), nullable=False)
    dob        = db.Column(db.Date,        nullable=True)
    address    = db.Column(db.Text,        nullable=True)
    created_at = db.Column(db.DateTime,    default=datetime.utcnow, nullable=False)

    # Relation M:N avec Course via table d'association
    courses = db.relationship("Course", secondary=enrollment, back_populates="students")

    def __repr__(self) -> str:
        return f"<Student {self.matricule} — {self.name}>"