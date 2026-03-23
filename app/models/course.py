from datetime import datetime
from app.extensions import db
from app.models.student import enrollment


class Course(db.Model):
    __tablename__ = "courses"

    id         = db.Column(db.Integer,    primary_key=True)
    code       = db.Column(db.String(20), unique=True, nullable=False)
    title      = db.Column(db.String(200), nullable=False)
    teacher_id = db.Column(db.Integer,    db.ForeignKey("teachers.id"), nullable=False)
    created_at = db.Column(db.DateTime,   default=datetime.utcnow, nullable=False)

    # Relation Many-to-One avec Teacher
    teacher  = db.relationship("Teacher", back_populates="courses")

    # Relation M:N avec Student via table d'association
    students = db.relationship("Student", secondary=enrollment, back_populates="courses")

    @staticmethod
    def generate_code(id: int) -> str:
        return f"CRS-{id:03d}"

    def __repr__(self) -> str:
        return f"<Course {self.code} — {self.title}>"