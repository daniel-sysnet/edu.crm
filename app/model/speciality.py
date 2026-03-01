from enum import Enum

class Speciality(Enum):
    WEB = "Web"
    DATA = "Data"
    NETWORK = "Network"
<<<<<<< HEAD
    AI = "AI"
=======
    AI = "AI"
    
    @classmethod
    def from_string(cls, label):
        # On nettoie la chaîne (espaces et casse) pour comparer
        label = label.strip().capitalize() 
        for item in cls:
            if item.value == label:
                return item
        raise ValueError(f"{label} n'est pas une spécialité valide.")
>>>>>>> Étudiant-3-Responsable-TEACHERS
