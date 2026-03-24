from datetime import datetime
from app.extensions import db
from app.models.action_type import ActionType
from app.models.entity_type import EntityType


class Activity(db.Model):
    __tablename__ = "activities"

    id          = db.Column(db.Integer,          primary_key=True)
    action      = db.Column(db.Enum(ActionType), nullable=False)
    entity_type = db.Column(db.Enum(EntityType), nullable=False)
    entity_id   = db.Column(db.String(20),       nullable=False)
    details     = db.Column(db.String(200),      nullable=True)
    created_at  = db.Column(db.DateTime,         default=datetime.utcnow, nullable=False)

    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user        = db.relationship("User", backref="activities")

    def __repr__(self) -> str:
        return f"<Activity {self.action.value} {self.entity_type.value} {self.entity_id}>"