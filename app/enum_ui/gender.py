from app.models.gender import Gender
from .enum_ui import registry, EnumView

registry.register({
    Gender.M: EnumView(
        label   = "Masculin",
        icon    = "male",
        classes = "bg-blue-100 text-blue-700",
    ),
    Gender.F: EnumView(
        label   = "Féminin",
        icon    = "female",
        classes = "bg-pink-100 text-pink-700",
    ),
})