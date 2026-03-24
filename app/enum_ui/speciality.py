from app.models.speciality import Speciality
from .enum_ui import registry, EnumView

registry.register({
    Speciality.WEB:     EnumView(
        label   = "Web",
        icon    = "language",
        classes = "bg-purple-50 text-purple-600 border border-purple-200",
    ),
    Speciality.DATA:    EnumView(
        label   = "Data",
        icon    = "database",
        classes = "bg-slate-100 text-slate-600 border border-slate-200",
    ),
    Speciality.NETWORK: EnumView(
        label   = "Network",
        icon    = "hub",
        classes = "bg-orange-50 text-orange-600 border border-orange-200",
    ),
    Speciality.AI:      EnumView(
        label   = "AI",
        icon    = "psychology",
        classes = "bg-teal-50 text-teal-600 border border-teal-200",
    ),
})