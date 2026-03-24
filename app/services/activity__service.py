from app.models.activity import Activity
from app.models.action import Action
from app.models.user import User

class ActivityService:
    
    def __init__(self):
        self.__activities = []
    
    def log(self, action : Action, model_type : str, model_id : int, details : str, user : User):
        activity = Activity(action, model_type, model_id, details, user)
        self.__activities.append(activity)

        